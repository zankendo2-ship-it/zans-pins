"""Pre-race features for every runner, built by walking our historic results in date order.

Everything a runner is scored on is known BEFORE its race: the walk scores a race from the
state built out of earlier races only, then adds that race's results to the state. The same
state, after the last historic day, scores today's runners - so the backtest and the live
picks use exactly the same features.

Features (race-relative where it matters, so a Group race and a seller are comparable):
  rpr_b3 / spd_b3   best RPR / our speed figure of the last 3 runs within a year (same code:
                    flat+AW or jumps), minus the best in the race, /10
  rpr_last          last run's RPR minus the race's best last-run RPR, /10
  or_rel            official rating minus the race's top rating, /10 (0 when no ratings)
  wgt               weight carried minus the race average, /7
  fresh/rest/long   days since last run <=14 / 91-365 / 366+ (the gap between is the base)
  debut, runs       no previous run; log(1 + runs)
  cd_course/cd_dist has won at this course (same code) / over this trip (+-1f, same code)
  won_last, placed_last
  trainer_sr/jockey_sr  strike rate in the last 365 days (shrunk to 10% with 20 dummy runs)
  trainer_14d       trainer's strike rate last 14 days (shrunk, 10 dummy runs)
  pace_suits/against  pace-map call (speed.pacemap.FIT)
  spd_trend         last speed figure minus best-of-3 (improving horses), /10
"""
import bisect
import csv
import math
import re
from collections import defaultdict
from datetime import date as Date
from pathlib import Path

from form.history import name_key, open_text, to_int, weight_lbs
from speed.figures import JUMPS, SpeedModel, load_races
from speed.pacemap import fit as pace_fit, race_scenario, runner_role
from track_stats.parse import course_key, discipline, dist_to_furlongs, going_group, running_style
from track_stats.extra import sp_decimal

FEATURES = ["rpr_b3", "rpr_miss", "spd_b3", "spd_miss", "rpr_last", "or_rel", "or_miss",
            "wgt", "fresh", "rest", "long", "debut", "runs", "cd_course", "cd_dist",
            "won_last", "placed_last", "trainer_sr", "trainer_14d", "jockey_sr",
            "pace_suits", "pace_against", "spd_trend",
            # track / course layer (price-free "best horse for THIS track today")
            "going_fit", "going_miss", "trip_rpr", "trip_spd", "course_placed",
            "trainer_course", "jockey_course", "draw_bias", "pace_bias",
            # connections form + "primed" + weight
            "jockey_14d", "trainer_jockey", "won_at_weight", "class_drop", "class_rise",
            "weight_bias"]
# 13 Oct research (reports/research/2026-10-13_*): each beat the market in both test periods; added AFTER the 38 so a
# weights file that lists only the first 38 (config/predict_weights.json "features") scores exactly as before
EXTRA_FEATURES = ["new_trainer", "rpr_cb7", "jump_mistake_lto", "fell_lto", "ft_visor_jumps", "hg_removed_flat",
                  "mare_v_geldings",
                  # 13 Oct evening: handicaps only, best RPR of the last 3 minus today's mark (/10, -2..+2) - "ahead of the
                  # handicapper" (10lb+ above: A/E 1.34 | 1.16, reports/research/2026-10-13_angles_round3.txt)
                  "mark_gap"]
ALL_FEATURES = FEATURES + EXTRA_FEATURES
FALLERS = {"F", "UR", "BD", "SU", "RO"}
LOOKBACK = 365
FIVE_YEARS = 1826
REPO = __import__("pathlib").Path(__file__).resolve().parent.parent


class TrackDNA:
    """Measured course draw + pace bias (reports/track_stats) as numbers for the model."""

    def __init__(self):
        self.draw, self.pace = {}, {}
        base = REPO / "reports" / "track_stats"
        try:
            for r in csv.DictReader(open(base / "draw_bias.csv", encoding="utf-8")):
                if r["confidence"] in ("TOO_FEW", ""):
                    continue
                w = 0.5 if r["confidence"] == "LOW" else 1.0
                self.draw[(r["course_id"], r["race_code"], float(r["furlongs"]), r["going"])] = (
                    w, [float(r[f"{t}_prb"] or 0.5) - 0.5 for t in ("low", "middle", "high")])
            for r in csv.DictReader(open(base / "pace_bias.csv", encoding="utf-8")):
                if r["confidence"] in ("TOO_FEW", ""):
                    continue
                w = 0.5 if r["confidence"] == "LOW" else 1.0
                led = float(r["led_vs_avg"] or 1) - 1
                held = float(r["held_up_vs_avg"] or 1) - 1
                self.pace[(r["course_id"], r["discipline"], float(r["furlongs"]), r["going"])] = (
                    w * max(min(led, 1), -1), w * max(min(held, 1), -1))
            self.weight = {}
            for r in csv.DictReader(open(base / "weight_bias.csv", encoding="utf-8")):
                if r["confidence"] in ("TOO_FEW", ""):
                    continue
                w = 0.5 if r["confidence"] == "LOW" else 1.0
                self.weight[(r["course_id"], r["discipline"], float(r["furlongs"]), r["going"])] = (
                    w, {b: float(r[f"{b}_prb"] or 0.5) - 0.5 for b in ("top", "upper", "middle", "low")})
        except (OSError, KeyError, ValueError):
            pass

    def weight_edge(self, course_id, disc, furlongs, going, below_top):
        if below_top is None or not hasattr(self, "weight"):
            return 0.0
        key = next((k for k in ((course_id, disc, float(round(furlongs)), going),
                                (course_id, disc, float(round(furlongs)), "ALL")) if k in self.weight), None)
        if not key:
            return 0.0
        band = "top" if below_top <= 2 else "upper" if below_top <= 9 else "middle" if below_top <= 16 else "low"
        w, prbs = self.weight[key]
        return w * prbs[band] * 10

    def draw_edge(self, course_id, code, furlongs, going, draw, field):
        if not draw or not field or field < 4 or code == "JUMPS":
            return 0.0
        key = next((k for k in ((course_id, code, float(round(furlongs)), going),
                                (course_id, code, float(round(furlongs)), "ALL")) if k in self.draw), None)
        if not key:
            return 0.0
        w, prbs = self.draw[key]
        third = 0 if draw <= field / 3 else 2 if draw > 2 * field / 3 else 1
        return w * prbs[third] * 10

    def pace_edge(self, course_id, disc, furlongs, going, role):
        key = next((k for k in ((course_id, disc, float(round(furlongs)), going),
                                (course_id, disc, float(round(furlongs)), "ALL")) if k in self.pace), None)
        if not key:
            return 0.0
        led, held = self.pace[key]
        return led if role in ("LEADER", "PROMINENT") else held if role == "HOLD_UP" else 0.0


DNA = None


def dna():
    global DNA
    if DNA is None:
        DNA = TrackDNA()
    return DNA


_INCIDENTS = None


def stewards_incidents():
    """(date, horse key) -> stewards'/vet categories that day (GB BHA reports + Irish IHRB), from the history copied to
    data/bha/ (data-bha branch, scripts/fetch_history.sh) and the daily reports/stewards/<D>/ files."""
    global _INCIDENTS
    if _INCIDENTS is not None:
        return _INCIDENTS
    import glob
    import gzip
    from bha.collect import CATS
    from bha.ihrb import EXTRA
    out = defaultdict(set)
    files = sorted(glob.glob(str(REPO / "data" / "bha" / "*incidents*.csv.gz"))) + \
        sorted(glob.glob(str(REPO / "reports" / "stewards" / "*" / "*incidents.csv")))
    for path in files:
        irish = "ihrb" in Path(path).name
        with (gzip.open(path, "rt", encoding="utf-8") if path.endswith(".gz") else open(path, encoding="utf-8")) as fh:
            for r in csv.DictReader(fh):
                key = (r["date"], name_key(r["horse"]))
                if irish:   # Irish rows are re-read from their text with the latest category rules
                    out[key].update(c for c, pat in list(CATS) + list(EXTRA) if pat.search(r.get("text") or ""))
                else:
                    out[key].add(r["category"])
    _INCIDENTS = out
    return out


def breed_map(path=None):
    """(race_id, horse key) -> (headgear, sex) from the Kaggle profile extract (data/results_breed.csv.gz)."""
    path = path or REPO / "data" / "results_breed.csv.gz"
    out = {}
    try:
        with open_text(path) as handle:
            for r in csv.DictReader(handle):
                out[(r["race_id"], name_key(r["horse"]))] = ((r.get("hg") or "").strip().lower(), (r.get("sex") or "").strip().upper())
    except OSError:
        pass
    return out


def fam_of(disc):
    return "JUMPS" if disc in JUMPS else "FLAT"


def ordinal(day):
    return Date.fromisoformat(day).toordinal()


class Rolling:
    """(ordinal, won) lists per person for rolling strike rates."""

    def __init__(self):
        self.days = defaultdict(list)
        self.wins = defaultdict(list)   # cumulative wins aligned with days

    def add(self, who, day, won):
        d, w = self.days[who], self.wins[who]
        d.append(day)
        w.append((w[-1] if w else 0) + won)

    def rate(self, who, day, window, prior=0.10, dummy=20):
        d = self.days.get(who)
        if not d:
            return prior, 0
        hi = bisect.bisect_left(d, day)
        lo = bisect.bisect_left(d, day - window)
        n = hi - lo
        if n <= 0:
            return prior, 0
        w = self.wins[who]
        won = (w[hi - 1] if hi else 0) - (w[lo - 1] if lo else 0)
        return (won + prior * dummy) / (n + dummy), n


def person_key(name):
    """'William Buick' / 'W Buick' -> 'w buick' (Racing Post and Sporting Life spell names
    differently; first initial + surname matches both)."""
    parts = re.sub(r"[^a-z &'-]", "", str(name or "").lower()).replace("&", " ").split()
    if not parts:
        return ""
    return f"{parts[0][0]} {parts[-1]}"


class State:
    def __init__(self):
        self.runs = defaultdict(list)    # horse -> [run dict]
        self.trainers = Rolling()
        self.jockeys = Rolling()
        self.trainer_course = Rolling()
        self.jockey_course = Rolling()
        self.trainer_jockey = Rolling()

    def best(self, runs, day, field, fam, n=3):
        cut = day - LOOKBACK
        vals = [r[field] for r in [r for r in runs if r["fam"] == fam][-n:]
                if r[field] is not None and r["day"] >= cut]
        return max(vals) if vals else None

    def runner(self, horse, day, fam, course_id, furlongs, trainer, jockey, days_since=None,
               going=None, race_class=None):
        """Raw (not yet race-relative) facts about one runner going into a race."""
        trainer, jockey = person_key(trainer), person_key(jockey)
        runs = [r for r in self.runs.get(horse, ()) if r["day"] < day]
        same = [r for r in runs if r["fam"] == fam]
        last = runs[-1] if runs else None
        last_same = same[-1] if same else None
        if days_since is None and last:
            days_since = day - last["day"]
        spd_b3 = self.best(runs, day, "fig", fam)
        spd_last = last_same["fig"] if last_same and last_same["day"] >= day - LOOKBACK else None
        return {
            "rpr_b3": self.best(runs, day, "rpr", fam),
            "spd_b3": spd_b3,
            "spd_last": spd_last,
            "rpr_last": last_same["rpr"] if last_same and last_same["day"] >= day - LOOKBACK else None,
            "days_since": days_since,
            "n_runs": len(runs),
            "cd_course": any(r["won"] and r["course_id"] == course_id for r in same),
            "cd_dist": any(r["won"] and r["furlongs"] and abs(r["furlongs"] - furlongs) <= 1
                           for r in same),
            "won_last": bool(last and last["won"]),
            "placed_last": bool(last and last["pos"] in (2, 3)),
            "trainer_sr": self.trainers.rate(trainer, day, LOOKBACK)[0] if trainer else 0.10,
            "trainer_14d": self.trainers.rate(trainer, day, 14, dummy=10)[0] if trainer else 0.10,
            "jockey_sr": self.jockeys.rate(jockey, day, LOOKBACK)[0] if jockey else 0.10,
            "role": runner_role([r["style"] for r in same])[0],
            **self.track_facts(same, day, course_id, furlongs, trainer, jockey, going),
            "jockey_14d": self.jockeys.rate(jockey, day, 14, dummy=10)[0] if jockey else 0.10,
            "tj_sr": self.trainer_jockey.rate((trainer, jockey), day, FIVE_YEARS)[0] if trainer and jockey else 0.10,
            "win_lbs": max([r["lbs"] for r in same if r["won"] and r["lbs"]] or [None]),
            "class_move": (race_class - last_same["cls"]) if race_class and last_same and last_same.get("cls") else None,
            **self.extra_facts(runs, same, trainer, days_since),
        }

    @staticmethod
    def extra_facts(runs, same, trainer, days_since):
        last = runs[-1] if runs else {}
        rp = [r["rpr"] for r in same if r.get("rpr")]
        return {
            "x_new_trainer": bool(trainer and last.get("tr") and trainer != last["tr"]
                                  and days_since is not None and days_since <= LOOKBACK),
            "x_rpr_cb7": bool(len(rp) >= 3 and rp[-1] >= max(rp[:-1]) + 7),
            "x_jm": bool(last.get("jm")),
            "x_fell": bool(last.get("fell")),
            "x_last_hg": last.get("hg"),
            "x_hg_letters": set("".join(r.get("hg") or "" for r in runs)),
            "x_sex": next((r["sex"] for r in reversed(runs) if r.get("sex")), None),
        }

    def track_facts(self, same, day, course_id, furlongs, trainer, jockey, going):
        cut = day - 2 * LOOKBACK
        on_going = [r for r in same if going and r["going"] == going]
        trip = [r for r in same if r["furlongs"] and abs(r["furlongs"] - furlongs) <= 1 and r["day"] >= cut]
        at_course = [r for r in same if r["course_id"] == course_id]
        return {
            "going_w": sum(r["won"] for r in on_going), "going_n": len(on_going),
            "going_p": sum(r["pos"] in (1, 2, 3) for r in on_going),
            "trip_rpr": max([r["rpr"] for r in trip if r["rpr"]] or [None]),
            "trip_spd": max([r["fig"] for r in trip if r["fig"] is not None] or [None]),
            "course_p": sum(r["pos"] in (1, 2, 3) for r in at_course), "course_n": len(at_course),
            "tc_sr": self.trainer_course.rate((trainer, course_id), day, FIVE_YEARS)[0] if trainer else 0.10,
            "jc_sr": self.jockey_course.rate((jockey, course_id), day, FIVE_YEARS)[0] if jockey else 0.10,
        }

    def add(self, horse, day, fam, course_id, furlongs, going, pos, rpr, fig, lbs, style,
            trainer, jockey, cls=None, hg=None, sex=None, jm=False, fell=False):
        trainer, jockey = person_key(trainer), person_key(jockey)
        self.runs[horse].append({"day": day, "fam": fam, "course_id": course_id,
                                 "furlongs": furlongs, "going": going, "pos": pos,
                                 "won": pos == 1, "rpr": rpr, "fig": fig, "lbs": lbs,
                                 "style": style, "cls": cls, "tr": trainer, "hg": hg, "sex": sex,
                                 "jm": jm, "fell": fell})
        if trainer:
            self.trainers.add(trainer, day, pos == 1)
            self.trainer_course.add((trainer, course_id), day, pos == 1)
        if jockey:
            self.jockeys.add(jockey, day, pos == 1)
            self.jockey_course.add((jockey, course_id), day, pos == 1)
        if trainer and jockey:
            self.trainer_jockey.add((trainer, jockey), day, pos == 1)


def race_vectors(raws, lbs, ors, disc, course=None, draws=None, handicap=False, hg=None, hg_first=None):
    """course = (course_id, race_code, furlongs, going group) for the track-DNA features."""
    """Race-relative feature rows for one race from the runners' raw facts."""
    def rel(values, scale=10, floor=-4.0):
        known = [v for v in values if v is not None]
        top = max(known) if known else None
        return [max((v - top) / scale, floor) if v is not None else 0.0 for v in values]

    rpr_b3 = rel([r["rpr_b3"] for r in raws])
    spd_b3 = rel([r["spd_b3"] for r in raws])
    rpr_last = rel([r["rpr_last"] for r in raws])
    trip_rpr = rel([r.get("trip_rpr") for r in raws])
    trip_spd = rel([r.get("trip_spd") for r in raws])
    draws = draws or [None] * len(raws)
    top_lbs = max([x for x in lbs if x] or [0])
    or_rel = rel(ors)
    known_lbs = [x for x in lbs if x]
    mean_lbs = sum(known_lbs) / len(known_lbs) if known_lbs else 0
    scenario, _ = race_scenario({i: r["role"] for i, r in enumerate(raws)})
    hg = hg or [None] * len(raws)               # today's headgear ('' = none, None = unknown)
    hg_first = hg_first or [None] * len(raws)   # card's first-time headgear flag (None = work it out from history)
    jumps = disc in JUMPS
    sexes = [r.get("x_sex") for r in raws]
    rows = []
    for i, r in enumerate(raws):
        ds = r["days_since"]
        call = pace_fit(scenario, r["role"], disc) if r["role"] != "UNKNOWN" else "NEUTRAL"
        trend = 0.0
        if r["spd_last"] is not None and r["spd_b3"] is not None:
            trend = max(min((r["spd_last"] - r["spd_b3"]) / 10, 0), -3.0)
        rows.append([
            rpr_b3[i], float(r["rpr_b3"] is None), spd_b3[i], float(r["spd_b3"] is None),
            rpr_last[i], or_rel[i], float(ors[i] is None),
            ((lbs[i] or mean_lbs) - mean_lbs) / 7 if mean_lbs else 0.0,
            float(ds is not None and ds <= 14), float(ds is not None and 91 <= ds <= 365),
            float(ds is not None and ds > 365), float(r["n_runs"] == 0),
            math.log1p(r["n_runs"]), float(r["cd_course"]), float(r["cd_dist"]),
            float(r["won_last"]), float(r["placed_last"]),
            (r["trainer_sr"] - 0.10) * 10, (r["trainer_14d"] - 0.10) * 10,
            (r["jockey_sr"] - 0.10) * 10,
            float(call == "SUITS"), float(call == "AGAINST"), trend,
            ((r.get("going_w", 0) + 0.3) / (r.get("going_n", 0) + 3) - 0.1) * 10
            + ((r.get("going_p", 0) + 0.9) / (r.get("going_n", 0) + 3) - 0.3) * 3,
            float(not r.get("going_n")),
            trip_rpr[i], trip_spd[i],
            ((r.get("course_p", 0) + 0.9) / (r.get("course_n", 0) + 3) - 0.3) * 3,
            (r.get("tc_sr", 0.1) - 0.10) * 10, (r.get("jc_sr", 0.1) - 0.10) * 10,
            dna().draw_edge(course[0], course[1], course[2], course[3], draws[i], len(raws)) if course else 0.0,
            dna().pace_edge(course[0], disc, course[2], course[3], r["role"]) if course else 0.0,
            (r.get("jockey_14d", 0.1) - 0.10) * 10, (r.get("tj_sr", 0.1) - 0.10) * 10,
            float(bool(r.get("win_lbs") and lbs[i] and r["win_lbs"] >= lbs[i] - 3)),
            float((r.get("class_move") or 0) > 0), float((r.get("class_move") or 0) < 0),
            dna().weight_edge(course[0], disc, course[2], course[3],
                              (top_lbs - lbs[i]) if (handicap and lbs[i] and top_lbs) else None) if course else 0.0,
            # EXTRA_FEATURES
            float(bool(r.get("x_new_trainer"))), float(bool(r.get("x_rpr_cb7"))),
            float(bool(r.get("x_jm"))), float(bool(r.get("x_fell"))),
            float(jumps and hg[i] is not None and "v" in hg[i] and r["n_runs"] > 0
                  and (bool(hg_first[i]) if hg_first[i] is not None else "v" not in r.get("x_hg_letters", set()))),
            float(not jumps and hg[i] == "" and bool(r.get("x_last_hg"))),
            float(jumps and sexes[i] == "M" and any(x in ("G", "H") for j, x in enumerate(sexes) if j != i)),
            max(min((r["rpr_b3"] - ors[i]) / 10, 2.0), -2.0) if (handicap and r["rpr_b3"] and ors[i]) else 0.0,
        ])
    return rows, scenario


def class_num(text):
    m = __import__("re").search(r"(\d)", str(text or ""))
    return int(m.group(1)) if m else None


def handicap_races(path=REPO / "data" / "results_uki.csv.gz"):
    out = set()
    try:
        with open_text(path) as handle:
            for row in csv.DictReader(handle):
                if (row.get("rating_band") or "").strip():
                    out.add(row.get("race_id"))
    except OSError:
        pass
    return out


def load_rows(paths):
    """All historic runner rows grouped by race, oldest first."""
    races, seen = {}, set()
    hcaps = handicap_races()
    breed = breed_map()
    for path in paths:
        with open_text(path) as handle:
            for row in csv.DictReader(handle):
                day = str(row.get("date") or "").replace("/", "-")
                if not day[:4].isdigit():
                    continue
                cid, is_aw = course_key(row.get("course") or "")
                horse = name_key(row.get("horse"))
                if (day, cid, horse) in seen:
                    continue
                seen.add((day, cid, horse))
                disc = discipline(row.get("type"), is_aw)
                furlongs = dist_to_furlongs(row.get("dist"))
                if not disc or not furlongs:
                    continue
                key = (day, cid, row.get("race_id") or row.get("off"))
                race = races.setdefault(key, {"key": key, "date": day, "course_id": cid,
                                              "disc": disc, "furlongs": furlongs,
                                              "going": going_group(row.get("going")),
                                              "cls": class_num(row.get("class")),
                                              "handicap": (row.get("race_id") in hcaps) or bool((row.get("rating_band") or "").strip()),
                                              "runners": []})
                race["runners"].append({
                    "horse": horse, "pos": to_int(row.get("pos")), "lbs": weight_lbs(row),
                    "or": to_int(row.get("or")), "rpr": to_int(row.get("rpr")),
                    "sp": sp_decimal(row.get("sp")), "trainer": row.get("trainer") or "",
                    "jockey": row.get("jockey") or "", "draw": to_int(row.get("draw")),
                    "style": running_style(row.get("comment") or ""),
                    "pos_code": str(row.get("pos") or "").strip().upper(),
                    **dict(zip(("hg", "sex"), (((row.get("hg") or "").strip().lower(), (row.get("sex") or "").strip().upper())
                                               if "hg" in row else breed.get((row.get("race_id"), horse), (None, None))))),
                })
    return sorted(races.values(), key=lambda r: r["date"])


def speed_figures(paths, fit_before):
    model = SpeedModel(load_races(paths), fit_before=fit_before)
    figs = {}
    for race in model.races:
        for horse, fig, _ in model.runner_figures(race):
            if fig is not None:
                figs[(race.key, horse)] = fig
    return figs, model


def walk(paths, fit_before="2025-01-01", min_field=4, collect_from="2019-01-01"):
    """Walk history: returns (state, samples) where samples = [(race dict, rows, won index,
    sp chances)] for races with a full SP book from collect_from on."""
    figs, model = speed_figures(paths, fit_before)
    races = load_rows(paths)
    incidents = stewards_incidents()
    state = State()
    samples = []
    for race in races:
        day = ordinal(race["date"])
        fam = fam_of(race["disc"])
        runners = race["runners"]
        if race["date"] >= collect_from and len(runners) >= min_field:
            sps = [r["sp"] for r in runners]
            winners = [i for i, r in enumerate(runners) if r["pos"] == 1]
            if all(sps) and len(winners) == 1:
                raws = [state.runner(r["horse"], day, fam, race["course_id"], race["furlongs"],
                                     r["trainer"], r["jockey"], going=race["going"],
                                     race_class=race["cls"]) for r in runners]
                code = "JUMPS" if fam == "JUMPS" else race["disc"]
                rows, _ = race_vectors(raws, [r["lbs"] for r in runners],
                                       [r["or"] for r in runners], race["disc"],
                                       (race["course_id"], code, race["furlongs"], race["going"]),
                                       [r["draw"] for r in runners], race["handicap"],
                                       hg=[r.get("hg") for r in runners])
                book = sum(1 / s for s in sps)
                samples.append((race, rows, winners[0], [1 / s / book for s in sps], sps))
        for r in runners:
            state.add(r["horse"], day, fam, race["course_id"], race["furlongs"], race["going"],
                      r["pos"], r["rpr"], figs.get((race["key"], r["horse"])), r["lbs"],
                      r["style"], r["trainer"], r["jockey"], race["cls"], hg=r.get("hg"), sex=r.get("sex"),
                      jm="JUMPING" in incidents.get((race["date"], r["horse"]), ()), fell=r.get("pos_code") in FALLERS)
    return state, samples, model
