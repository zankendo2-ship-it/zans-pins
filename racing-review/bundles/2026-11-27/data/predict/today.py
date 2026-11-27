"""Today's selections for every race: WIN pick, RPR pick, confidence /10, BET / NO BET, longshot.

Inputs: the day's evidence pack (reports/racecards/<date>/evidence.csv: runners, prices),
racecards.json (RP horse course/distance/going stats for the RPR rule), our historic results
(walked by predict.features up to the day before) and the fitted weights (predict.train).

  WIN pick     highest COMBINED chance (form model + today's best price)
  confidence   from the combined chance, on a scale checked on 2025-26 races (see CONFIDENCE)
  RPR pick     owner's rule: highest card RPR that has run at today's distance + going
               (RP stats), else at the distance, walking down the RPR order; weight check
  BET          trial rule: confidence >= 6 AND today's price at least our fair price
  longshot     price 14/1+ (decimal 15+) in a race of 6+ runners: the runner with the best
               combined chance x price, if that is at least 0.9; else "no longshot"
"""
import argparse
import csv
import hashlib
import json
import math
import pickle
import re
from datetime import date as Date, datetime, timezone
from pathlib import Path

import numpy as np

from form.history import days_since, name_key
from speed.figures import JUMPS

from track_stats.parse import going_group

from .features import ALL_FEATURES, FEATURES, class_num, fam_of, race_vectors

REPO_ROOT = Path(__file__).resolve().parent.parent
WEIGHTS = REPO_ROOT / "config" / "predict_weights.json"

# combined chance of the top pick -> confidence; 2025-26 test strike rates in weights file
LONGSHOT_PRICE = 15.0   # 14/1
# our chance x price needed; 2025-26 test at SP: flat 0.9 -> 368 picks, 4.6% won, ~break-even;
# jumps longshots lost heavily at 0.9-1.05, so jumps need 1.1 (44 picks, -16%: still weak)
LONGSHOT_VALUE = {"FLAT": 0.9, "JUMPS": 1.1}
CONFIDENCE = [(0.60, 10), (0.50, 9), (0.42, 8), (0.35, 7), (0.30, 6), (0.25, 5), (0.20, 4),
              (0.15, 3), (0.0, 2)]


# 7 Oct 2026 (owner: "use all the data ... get more winners", deep research run): the model's chances are honest for
# flat, all-weather and hurdles, but OVER-confident for chases and bumpers. 2025-26 history (out of sample), picks rated
# 7/10+: chases won 41.4% v 46.9% predicted in 2025 and 44.4% v 47.0% in 2026 (ratio 0.88 / 0.94); NH flat 44.4% v 48.3%
# and 44.0% v 48.4% (0.92 / 0.91); hurdles 0.98 / 1.00, flat 0.96 / 0.98, AW 1.06 / 1.01. The confidence rating (and so
# the 7/10+ multiples legs) uses the chance x this factor; chase picks it demotes from 7+ to 6 won 31% (= 6/10 form).
CONF_CAL = {"CHASE": 0.91, "NHF": 0.92}


def confidence(p, disc=None):
    p = p * CONF_CAL.get(str(disc or "").upper(), 1.0)
    return next(c for lo, c in CONFIDENCE if p >= lo)


def frac(dec):
    """Price for display: DECIMAL odds (owner's choice 2026-09-24; 8/13 -> 1.62)."""
    if not dec:
        return "-"
    return f"{int(dec * 100 + 0.5 + 1e-9) / 100:.2f}"


def frac_at_least(dec):
    """'Worth a bet at' price: decimal, rounded UP to 2 places so it is never below fair."""
    import math
    return f"{math.ceil(dec * 100 - 1e-9) / 100:.2f}"


def num(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def softmax(u):
    e = np.exp(u - u.max())
    return e / e.sum()


def rp_stat(runner, key):
    s = ((runner.get("stats") or {}).get("horse") or {}).get(key) or {}
    try:
        return int(s.get("runs") or 0), int(s.get("wins") or 0)
    except ValueError:
        return 0, 0


def rpr_pick(rows, card, state, day, fam):
    """Owner's RPR rule with the reasoning written out."""
    by_id = {str(r["horse_id"]): r for r in card["runners"]}
    ranked = sorted([r for r in rows if num(r["rpr"])], key=lambda r: -num(r["rpr"]))
    if not ranked:
        return None, "No runner has an RPR"
    skipped = []
    for tier in ("distance+going", "distance"):
        for r in ranked:
            c = by_id.get(str(r["horse_id"]), {})
            d_runs, d_wins = rp_stat(c, "distance")
            g_runs, g_wins = rp_stat(c, "going")
            ok = d_runs > 0 and (g_runs > 0 or tier == "distance")
            if not ok:
                if tier == "distance+going":
                    skipped.append(f"{r['name']} ({int(num(r['rpr']))}) "
                                   f"{'not run at the trip' if not d_runs else 'not run on the going'}")
                continue
            why = (f"RPR {int(num(r['rpr']))}; distance {d_wins}/{d_runs}, going {g_wins}/{g_runs} "
                   f"(wins/runs)")
            if tier == "distance":
                why += "; nobody higher had run at both trip and going"
            if skipped:
                why += "; passed over: " + ", ".join(skipped[:3])
            why += weight_check(r, state, day, fam)
            return r, why
    top = ranked[0]
    return top, (f"RPR {int(num(top['rpr']))}; no runner has run at today's trip - top RPR kept"
                 + weight_check(top, state, day, fam))


def weight_check(r, state, day, fam):
    lbs = num(r["lbs"])
    runs = [x for x in state.runs.get(name_key(r["name"]), ()) if x["fam"] == fam and x["day"] < day]
    if not lbs or not runs or not runs[-1]["lbs"]:
        return ""
    card_days = days_since(r.get("last_run"))
    if card_days and abs((day - runs[-1]["day"]) - card_days) > 3:
        # our results miss the horse's latest run(s) (e.g. the June-August 2026 gap): comparing
        # with an older run would be wrong (e.g. a 2yo run a year ago v a 3yo weight today)
        return f"; weight check not possible - its last run ({int(card_days)} days ago) isn't in our results yet"
    up = lbs - runs[-1]["lbs"]
    if up < 5:
        return f"; weight {'+' if up >= 0 else ''}{int(up)}lb vs last run - fine"
    if runs[-1]["pos"] == 1:
        return (f"; up {int(up)}lb after WINNING last time (the handicapper's rise) - has to "
                f"prove it can follow up off the higher mark")
    carried = [x for x in runs if x["lbs"] and x["lbs"] >= lbs - 2 and x["pos"] in (1, 2, 3)]
    if carried:
        return (f"; up {int(up)}lb on last run BUT has finished top-3 {len(carried)}x carrying "
                f"{int(lbs - 2)}lb+ before - can cope")
    return f"; WARNING up {int(up)}lb on last run and never placed carrying this much"


def fill_recent_runs(state, race_date, rows_by_race, cards):
    """No horse may go in with missing form (owner, 2026-09-24): wherever the card shows a
    newer run than our results hold, add the missing runs from the Sporting Life race pages
    (reports/results_sl/<date>/recent_runs.csv). Returns {horse key: status}."""
    from track_stats.parse import course_key, dist_to_furlongs, is_uk_ire
    from .features import fam_of as _fam
    path = REPO_ROOT / "reports" / "results_sl" / race_date / "recent_runs.csv"
    recent = {}
    if path.exists():
        for r in csv.DictReader(open(path, encoding="utf-8")):
            if r["date"] < race_date:
                recent.setdefault(name_key(r["horse"]), []).append(r)
    day = Date.fromisoformat(race_date).toordinal()
    sl_runners = set()
    res_path = REPO_ROOT / "reports" / "results_sl" / race_date / "runners.csv"
    if not res_path.exists():  # older fetches: the results file doubled as the runner list
        res_path = res_path.with_name("results.csv")
    sl_races = set()   # (course, off time) Sporting Life lists: a horse is only a non-runner
    if res_path.exists():  # if SL has ITS race and the horse isn't in it (early cards!)
        for r in csv.DictReader(open(res_path, encoding="utf-8")):
            sl_runners.add(name_key(r["horse"]))
            sl_races.add((course_key(r.get("course") or "")[0], (r.get("off") or "")[:5]))
    status = {}
    for race_id, rows in rows_by_race.items():
        fam = _fam(rows[0]["discipline"])
        for r in rows:
            k = name_key(r["name"])
            card_days = days_since(r["last_run"])
            if not card_days:
                status[k] = "DEBUT" if r["coverage"] == "DEBUT" else "COMPLETE"
                continue
            runs = state.runs.get(k, [])
            last = max([x["day"] for x in runs if x["day"] < day] or [0])
            if abs((day - last) - card_days) <= 3:
                status[k] = "COMPLETE"
                continue
            race_listed = (course_key(r.get("course_name") or r.get("course_id") or "")[0], (r.get("off_time") or "")[:5]) in sl_races
            if sl_runners and race_listed and k not in sl_runners:
                status[k] = "NON-RUNNER"      # not in Sporting Life's list of runners
                continue
            if (day - last) < card_days - 3:
                status[k] = "COMPLETE"        # we hold a later run than the card counts
                continue
            added = 0
            for x in recent.get(k, []):
                d = Date.fromisoformat(x["date"]).toordinal()
                if d <= last or not is_uk_ire(x["course_name"]):
                    continue    # owner: UK and Ireland only - an overseas run stays a labelled gap
                furl = dist_to_furlongs(re.sub(r"\s*\d+y$", "", str(x["distance"] or "")).replace(" ", ""))
                pos = int(x["position"]) if str(x["position"]).isdigit() else None
                m = re.fullmatch(r"(\d+)-(\d+)", str(x.get("weight") or ""))
                state.runs.setdefault(k, []).append({
                    "day": d, "fam": fam, "course_id": course_key(x["course_name"] or "")[0],
                    "furlongs": furl, "going": going_group(re.sub(r"\s*\(.*", "", x["going"] or "")),
                    "pos": pos, "won": pos == 1, "rpr": None, "fig": None,
                    "lbs": int(m.group(1)) * 14 + int(m.group(2)) if m else None, "style": None, "cls": None})
                added += 1
            state.runs[k].sort(key=lambda x: x["day"]) if k in state.runs else None
            last = max([x["day"] for x in state.runs.get(k, []) if x["day"] < day] or [0])
            if abs((day - last) - card_days) > 3:
                # Sporting Life lists UK/IRE runs only: a gap left after filling = a run abroad
                status[k] = "ABROAD" if recent.get(k) else "MISSING"
            else:
                status[k] = "FILLED" if added else "COMPLETE"
    return status


def clean_going(text):
    """Sporting Life going text -> the racecard's main description, so track_stats.going_group can read it (22 Oct:
    'Standard / Slow', 'Good-good to yielding in places' and Irish 'Straight: yielding; round: good to yielding' all
    fell into OTHER and the Kempton picks lost their going/draw/pace figures)."""
    g = re.sub(r"\s*\(.*", "", str(text or "")).strip()
    m = re.search(r"round:\s*([^;]+)", g, re.I)  # split straight/round going -> the round course (most races)
    if m:
        g = m.group(1)
    elif ":" in g:
        g = g.split(":", 1)[1].split(";")[0]
    g = re.sub(r"\s*-\s*.*in places.*$", "", g, flags=re.I)  # 'Good-good to firm in places' -> 'Good'
    g = re.sub(r"\s*/\s*", " to ", g)  # 'Standard / Slow' -> 'Standard to Slow'
    return g.strip().title()


def latest_going(race_date):
    """(course key, off time) -> the going in the NEWEST race-day price check (d0_morning / d0_midday), main
    description only ('Good to Soft (Good in places)' -> 'Good To Soft'). 19 Oct: the BHA changed Pontefract to Soft at
    06:51 and our 09:18 check said Soft, but the 09:43 pack used the racecard's 06:15 'Good To Soft' (races ran on Heavy).
    Picks must use the newest official going we hold."""
    from track_stats.parse import course_key
    best = {}
    for chk in ("d0_morning", "d0_midday"):
        path = REPO_ROOT / "reports" / "odds" / race_date / f"{chk}.csv"
        if not path.exists():
            continue
        for r in csv.DictReader(open(path, encoding="utf-8")):
            g = clean_going(r.get("going"))
            if not g or not (r.get("fetched_at") or "").startswith(race_date):
                continue
            k = (course_key(r.get("course") or "")[0], (r.get("off_time") or "")[:5])
            if k not in best or r["fetched_at"] >= best[k][0]:
                best[k] = (r["fetched_at"], g.title())
    # 29 Oct: the BHA eased Bath to Soft (07:15) and Stratford to Good to Soft (07:32) while Sporting Life still showed
    # Heavy / Soft at 08:16. The clerk's official going (reports/going/<D>/going.json, GB only) wins for its course.
    gpath = REPO_ROOT / "reports" / "going" / race_date / "going.json"
    if gpath.exists():
        try:
            bha = json.loads(gpath.read_text())
        except ValueError:
            bha = []
        for m in (bha.get("meetings") or []) if isinstance(bha, dict) else bha:
            g = clean_going(m.get("going")) if isinstance(m, dict) else None
            if not g or not str(m.get("updated") or "").startswith(race_date):
                continue
            ck = course_key(m.get("course") or "")[0]
            for k in best:  # 'Stratford-on-Avon' (BHA) = 'stratford' (Sporting Life)
                if k[0] == ck or ck.startswith(k[0] + "_") or k[0].startswith(ck + "_"):
                    best[k] = (best[k][0], g.title())
    return {k: v[1] for k, v in best.items()}


def apply_latest_going(race_date, rows):
    """Overwrite each evidence row's going with latest_going() where we hold a newer one; returns rows changed."""
    from track_stats.parse import course_key
    new = latest_going(race_date)
    changed = 0
    for r in rows:
        g = new.get((course_key(r.get("course_name") or r.get("course_id") or "")[0], (r.get("off_time") or "")[:5]))
        if g and g.lower() != str(r.get("going") or "").strip().lower():
            r["going"] = g
            changed += 1
    return changed


def build(race_date, state, weights, cards_dir):
    day = Date.fromisoformat(race_date).toordinal()
    evidence = list(csv.DictReader(open(cards_dir / "evidence.csv", encoding="utf-8")))
    apply_latest_going(race_date, evidence)
    cards = json.loads((cards_dir / "racecards.json").read_text(encoding="utf-8"))
    cards = {str(r["race_id"]): r for r in (cards["races"] if isinstance(cards, dict) else cards)}
    races = {}
    for row in evidence:
        races.setdefault(row["race_id"], []).append(row)
    fill = fill_recent_runs(state, race_date, races, cards)
    for rows in races.values():
        for r in rows:
            st = fill.get(name_key(r["name"]))
            if st in ("COMPLETE", "FILLED"):
                r["coverage"] = "COMPLETE" if st == "COMPLETE" else "FILLED (Sporting Life)"
    missing = sorted({r["name"] for rows in races.values() for r in rows if fill.get(name_key(r["name"])) == "MISSING"})
    nr = {k for k, v in fill.items() if v == "NON-RUNNER"}
    # 19 Oct (Dandana, 18:15 Wolverhampton): our own 09:18 price check marked it NONRUNNER but the 09:43 pack still
    # picked it - the check above only looks at horses whose form is behind. Any horse a price check of this race day
    # lists as a non-runner is out of THAT race (a non-runner never comes back in; Irish double declarations keep the other).
    from track_stats.parse import course_key
    nr_race = set()
    for path in sorted((cards_dir.parent.parent / "odds" / race_date).glob("d*_*.csv")):
        for r in csv.DictReader(open(path, encoding="utf-8")):
            if (r.get("status") or "").upper() in ("NONRUNNER", "NON-RUNNER", "NR", "WITHDRAWN"):
                nr_race.add((course_key(r.get("course") or "")[0], (r.get("off_time") or "")[:5], name_key(r["horse"])))
    (cards_dir.parent.parent / "predictions" / race_date).mkdir(parents=True, exist_ok=True)
    (cards_dir.parent.parent / "predictions" / race_date / "coverage_check.json").write_text(json.dumps({
        "runners": sum(len(v) for v in races.values()),
        "complete": sum(1 for v in fill.values() if v == "COMPLETE"),
        "filled_from_sporting_life": sum(1 for v in fill.values() if v == "FILLED"),
        "debut": sum(1 for v in fill.values() if v == "DEBUT"),
        "non_runners": sorted(r["name"] for rows in races.values() for r in rows if fill.get(name_key(r["name"])) == "NON-RUNNER"),
        "last_run_abroad": sorted(r["name"] for rows in races.values() for r in rows if fill.get(name_key(r["name"])) == "ABROAD"),
        "still_missing": missing}, indent=1))
    races = {rid: [r for r in rows if name_key(r["name"]) not in nr
                   and (course_key(r.get("course_name") or r.get("course_id") or "")[0], (r.get("off_time") or "")[:5],
                        name_key(r["name"])) not in nr_race] for rid, rows in races.items()}
    out = []
    for race_id, rows in sorted(races.items(), key=lambda kv: (kv[1][0]["off_time"], kv[1][0]["course_name"])):
        card = cards.get(race_id, {})
        if not rows or "runners" not in card:
            # 7 Nov: Wincanton (abandoned, hard ground) rows were left in evidence.csv from the previous day's Racing API
            # card -> a race with no card today crashed the whole build. A race that is not on today's card is skipped.
            print(f"SKIPPED race {race_id} ({rows[0].get('course_name') if rows else '?'}): not on today's racecard")
            continue
        disc = rows[0]["discipline"]
        fam = fam_of(disc)
        w = weights[fam]
        furlongs = card.get("furlongs") or 0
        raws, notes = [], []
        going = going_group(rows[0]["going"])
        race_class = class_num(card.get("race_class"))
        for r in rows:
            raw = state.runner(name_key(r["name"]), day, fam, r["course_id"], furlongs,
                               r["trainer"], r["jockey"],
                               days_since=days_since(r["last_run"]) or None,
                               going=going, race_class=race_class)
            # our results miss some recent runs: if the card shows newer runs than we hold,
            # fall back to the card's RPR for the form rating (and label the horse DATA GAP)
            if (r["coverage"] in ("BEHIND", "MISSING") or r["coverage"].startswith("FILLED")) and num(r["rpr"]):
                raw["rpr_b3"] = max(raw["rpr_b3"] or 0, num(r["rpr"]))
            raws.append(raw)
        code = "JUMPS" if fam == "JUMPS" else disc
        X, scenario = race_vectors(raws, [num(r["lbs"]) for r in rows],
                                   [num(r["ofr"]) for r in rows], disc,
                                   (rows[0]["course_id"], code, furlongs, going),
                                   [int(num(r["draw"])) if num(r["draw"]) else None for r in rows],
                                   bool(card.get("handicap")),
                                   hg=[(r.get("headgear") or "").strip().lower() for r in rows],
                                   hg_first=[str(r.get("headgear_first")) == "True" for r in rows])
        # only as many columns as the active weights were fitted on (38 = before the 13 Oct extras)
        X = np.asarray(X, float)[:, :len(weights.get("features") or FEATURES)]
        prices = [num(r["price_dec"]) or num(r["forecasted_odds"]) for r in rows]
        priced = all(prices)
        if priced:
            implied = np.array([1 / p for p in prices])
            market = implied / implied.sum()
        else:
            market = np.full(len(rows), 1 / len(rows))
        beta = np.asarray(w["form"])
        form = softmax(X @ beta)  # what our evidence alone says (used for value vs the price)
        # THE WIN PICK USES EVERYTHING (owner, 2026-09-25, replaces the 2026-09-24 price-free rule):
        # price + track DNA + form + connections - the horse most likely to win, favourite or not
        joint = np.asarray(w["joint"])
        p = softmax(X @ joint[:-1] + joint[-1] * np.log(np.clip(market, 1e-4, 1))) if priced else form
        order = [int(i) for i in np.argsort(-p)]
        top = order[0]
        exception = ""
        conf = confidence(p[top], disc)
        price = prices[top]
        fair = 1 / p[top]
        # BET = our strongest calls, confidence 8+
        bet = conf >= 8
        contrib = beta * (X[top] - X.mean(axis=0))
        rpr_row, rpr_why = rpr_pick(rows, card, state, day, fam)
        longshot, long_why = None, "no longshot (needs 6+ runners and a 14/1+ price)"
        if len(rows) >= 6:
            cands = [i for i in order if prices[i] and prices[i] >= LONGSHOT_PRICE]
            if cands:
                i = cands[0]
                rank = order.index(i) + 1
                longshot = rows[i]
                long_why = (f"{'STRONG' if rank <= 3 else 'SPECULATIVE'}: our {ordinal_word(rank)} "
                            f"best horse on the evidence (chance {p[i]:.0%})")
            else:
                long_why = "no runner priced 14/1 or bigger"
        reasons = reason_text(rows[top], raws[top], X[top], rows, contrib)
        if exception:
            reasons = exception + "; " + reasons
        out.append({
            "date": race_date, "course": rows[0]["course_name"], "off_time": rows[0]["off_time"],
            "race_id": race_id, "race_name": card.get("race_name", ""), "discipline": disc,
            "distance": rows[0]["distance_label"], "going": rows[0]["going"], "runners": len(rows),
            "win": rows[top]["name"], "win_no": rows[top]["number"], "win_price": frac(price),
            "win_price_dec": price, "win_chance": round(float(p[top]), 3),
            "market_chance": round(float(market[top]), 3), "fair_price": frac_at_least(fair),
            "confidence": conf, "verdict": "BET" if conf >= 8 else "NO BET",   # owner 1 Nov: 8+ = BET, always
            "second": rows[int(order[1])]["name"] if len(rows) > 1 else "",
            "second_chance": round(float(p[order[1]]), 3) if len(rows) > 1 else None,
            "win_reasons": reasons,
            "rpr_pick": rpr_row["name"] if rpr_row else "", "rpr_reason": rpr_why,
            "longshot": longshot["name"] if longshot else "",
            "longshot_price": frac(num(longshot["price_dec"])) if longshot else "",
            "longshot_reason": long_why, "pace": scenario,
            "is_favourite": bool(priced and prices[top] == min(prices)),
            "data_gap": rows[top]["coverage"] in ("BEHIND", "MISSING"),
            "coverage": rows[top]["coverage"],
            "prices_from": rows[0]["price_check"] + " " + rows[0]["price_time_utc"],
            "all": [{"name": rows[i]["name"], "chance": round(float(p[i]), 3),
                     "rank": order.index(i) + 1,
                     "factors": factor_list(beta * (X[i] - X.mean(axis=0))),
                     "coverage": rows[i]["coverage"],
                     "form_chance": round(float(form[i]), 3),
                     "price": frac(prices[i]) if prices[i] else "-"} for i in order],
        })
    return out


LABELS = {
    "rpr_b3": "best recent ratings", "rpr_last": "last-run rating", "spd_b3": "our speed figures",
    "trip_rpr": "rating at this trip", "trip_spd": "speed figure at this trip",
    "going_fit": "record on this going", "course_placed": "course form",
    "trainer_course": "trainer's record at this course", "jockey_course": "jockey's record at this course",
    "trainer_jockey": "trainer + jockey partnership", "trainer_sr": "trainer's strike rate",
    "jockey_sr": "jockey's strike rate", "trainer_14d": "yard in form (14 days)",
    "jockey_14d": "jockey in form (14 days)", "draw_bias": "draw suits this track",
    "pace_bias": "running style suits this track", "weight_bias": "weight band suits this track",
    "won_last": "won last time", "placed_last": "placed last time", "or_rel": "handicap mark",
    "class_drop": "dropping in class", "wgt": "weight", "won_at_weight": "has won at this weight",
    "cd_course": "course winner", "cd_dist": "trip winner",
}


def factor_list(contrib):
    """Every labelled factor's effect on this runner vs the race average (log-odds points)."""
    return {n: round(float(c), 3) for c, n in zip(contrib, ALL_FEATURES) if n in LABELS and abs(c) >= 0.02}


def ordinal_word(n):
    return {1: "1st", 2: "2nd", 3: "3rd"}.get(n, f"{n}th")


def reason_text(row, raw, x, rows, contrib=None):
    f = dict(zip(ALL_FEATURES, x))
    bits = []
    if contrib is not None:
        strengths = sorted(((c, n) for c, n in zip(contrib, ALL_FEATURES) if n in LABELS and c > 0.05),
                           reverse=True)[:4]
        if strengths:
            bits.append("strongest factors: " + ", ".join(LABELS[n] for _, n in strengths))
    if raw["rpr_b3"] and f["rpr_b3"] == 0:
        bits.append(f"best recent RPR in the race ({int(raw['rpr_b3'])})")
    elif raw["rpr_b3"]:
        bits.append(f"recent RPR {int(raw['rpr_b3'])} ({f['rpr_b3'] * 10:+.0f} vs best)")
    if raw["spd_b3"] is not None:
        bits.append("top speed figure" if f["spd_b3"] == 0 else f"speed fig {int(raw['spd_b3'])}")
    if raw["won_last"]:
        bits.append("won last time")
    elif raw["placed_last"]:
        bits.append("placed last time")
    if raw["cd_course"]:
        bits.append("course winner")
    if raw["cd_dist"]:
        bits.append("trip winner")
    if raw["trainer_14d"] >= 0.2:
        bits.append("trainer in good form (last 14 days)")
    if f["pace_suits"]:
        bits.append("pace map suits")
    if f["pace_against"]:
        bits.append("pace map against")
    return "; ".join(bits) or "little form to go on"


def render(race_date, picks):
    lines = [f"# ZANS selections — {race_date} (TRIAL)", "",
             f"Prices: best bookmaker price at {picks[0]['prices_from']} UTC. "
             "Confidence /10 is calibrated on 2025-26 races (see strike rates below).", ""]
    course = None
    for p in picks:
        if p["course"] != course:
            course = p["course"]
            lines += [f"## {course}", ""]
        lines += [f"**{p['off_time']} — {p['race_name']}** ({p['distance']}, {p['going']}, "
                  f"{p['runners']} ran)",
                  f"- WIN: **{p['win']}** {p['win_price']} — confidence **{p['confidence']}/10** "
                  f"— **{p['verdict']}** (our chance {p['win_chance']:.0%}, fair {p['fair_price']})",
                  f"  - why: {p['win_reasons']}",
                  f"- RPR: **{p['rpr_pick']}** — {p['rpr_reason']}",
                  f"- LONGSHOT: " + (f"**{p['longshot']}** {p['longshot_price']} — {p['longshot_reason']}"
                                     if p["longshot"] else p["longshot_reason"]), ""]
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Today's selections.")
    parser.add_argument("--date", required=True)
    parser.add_argument("--state", required=True, help="pickled predict.features State")
    parser.add_argument("--out")
    args = parser.parse_args(argv)
    cards_dir = REPO_ROOT / "reports" / "racecards" / args.date
    state = pickle.load(open(args.state, "rb"))
    weights = json.loads(WEIGHTS.read_text())
    picks = build(args.date, state, weights, cards_dir)
    out = Path(args.out or REPO_ROOT / "reports" / "predictions" / args.date)
    out.mkdir(parents=True, exist_ok=True)
    body = json.dumps(picks, indent=1)
    (out / "predictions.json").write_text(body, encoding="utf-8")
    (out / "predictions.md").write_text(render(args.date, picks), encoding="utf-8")
    seal = {"frozen_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "sha256": hashlib.sha256(body.encode()).hexdigest(), "races": len(picks)}
    (out / "seal.json").write_text(json.dumps(seal, indent=1), encoding="utf-8")
    print(f"{len(picks)} races -> {out}; sha256 {seal['sha256'][:16]}")


if __name__ == "__main__":
    main()
