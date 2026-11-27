"""Speed figures from race times — our own, independent of Racing Post's Topspeed.

How a figure is made (the classic time-figure method):
  1. STANDARD TIME for every course + track + discipline + distance: the time a horse of a
     fixed ability would record on standard ground. Worked out from the winners' times of
     past races there, each adjusted for the class of the race (its "par") and the weight the
     winner carried, and for the ground on the day (step 2). Needs 10+ timed races.
  2. GOING ALLOWANCE for every meeting: how many seconds per furlong faster or slower than
     standard that day's races were run, after allowing for their class. Worked out from all
     the races at the meeting (shrunk towards zero when there are few), so it measures the
     ground as it actually rode, not the official description.
  3. WINNER'S FIGURE = (standard + going allowance x furlongs - actual time) in pounds
     + the weight carried. One second is worth more pounds over 5f than over 3m, so seconds
     are turned into lengths (from the race's own speed; a length ~ 2.4 m) and lengths into
     pounds (the usual scale: 3 lb per length at 5f down to ~1 lb at 3m+ over jumps).
  4. BEATEN HORSES: winner's figure - distance beaten x pounds per length + weight difference.
     Horses beaten more than 30 lengths (or not finishing) get no figure.
Races whose winner figure lands more than 30 lb above or 40 lb below the race par are
left unrated (distorted time). Figures sit on the same pound scale as ratings (a par winner of a class scores that class's
typical winner rating), so 80 means roughly "ran to a rating of 80".

Rules: only information from BEFORE a race is used when we rate its runners in advance; the
standards and pars can be fitted on an earlier period (fit_before) to test on a later one.
"""
import csv
import json
import re
import statistics
from collections import defaultdict
from pathlib import Path

from form.history import name_key, open_text, to_int, weight_lbs
from track_stats.parse import course_key, discipline, dist_to_furlongs, going_group

METRES_PER_FURLONG = 201.168
LENGTH_METRES = 2.4
FLAT_LBS_PER_LENGTH = [(5, 3.0), (6, 2.5), (7, 2.25), (8, 2.0), (10, 1.75), (12, 1.5),
                       (14, 1.35), (16, 1.25), (20, 1.1)]
JUMPS_LBS_PER_LENGTH = [(16, 1.25), (20, 1.1), (24, 1.0), (28, 0.9), (32, 0.85)]
MIN_STANDARD_RACES = 10
MAX_BEATEN_LENGTHS = 30
GOING_SHRINK = 1          # allowance = sum of race deviations / (races + 1)
OUTLIER_SECS_PER_F = 0.8  # a race this far from its meeting's median is left out of the allowance
JUMPS = ("HURDLE", "CHASE", "NHF")
# A winner's figure this far from the race's par means the time is distorted (a crawl then a
# sprint, a timing error or a wrong distance): the race gets no figures rather than bad ones.
MAX_ABOVE_PAR = 30
MAX_BELOW_PAR = 40


def interpolate(table, x):
    if x <= table[0][0]:
        return table[0][1]
    for (x0, y0), (x1, y1) in zip(table, table[1:]):
        if x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return table[-1][1]


def lbs_per_length(furlongs, disc):
    return interpolate(JUMPS_LBS_PER_LENGTH if disc in JUMPS else FLAT_LBS_PER_LENGTH, furlongs)


def lbs_per_second(furlongs, disc, seconds):
    lengths_per_second = furlongs * METRES_PER_FURLONG / seconds / LENGTH_METRES
    return lengths_per_second * lbs_per_length(furlongs, disc)


def parse_time(text):
    """'1:02.29' / '62.29' / '4m 5.30s' -> seconds (float) or None."""
    t = re.sub(r"\(.*?\)", "", str(text or "")).strip().lower()
    m = re.fullmatch(r"(\d+):(\d+(?:\.\d+)?)", t)
    if m:
        return int(m.group(1)) * 60 + float(m.group(2))
    m = re.fullmatch(r"(?:(\d+)\s*m(?:in)?\s*)?(\d+(?:\.\d+)?)\s*s?", t)
    if m and (m.group(1) or "." in m.group(2) or float(m.group(2)) > 30):
        return int(m.group(1) or 0) * 60 + float(m.group(2))
    return None


def to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def surface_changes():
    """course_id -> date the current all-weather surface was laid (config/courses.json)."""
    path = Path(__file__).resolve().parent.parent / "config" / "courses.json"
    try:
        courses = json.loads(path.read_text())["courses"]
    except (OSError, ValueError, KeyError):
        return {}
    return {cid: c["surface_since"]["AW_FLAT"] for cid, c in courses.items()
            if c.get("surface_since", {}).get("AW_FLAT")}


def track_key(course):
    """Keeps sub-tracks apart: 'Newmarket (July)' != 'Newmarket'; drops the (IRE) tag."""
    text = re.sub(r"\((IRE|GB)\)", "", str(course or ""))
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def class_group(race_class, course):
    m = re.search(r"(\d)", str(race_class or ""))
    if m:
        return f"C{m.group(1)}"
    return "IRE" if "(IRE)" in str(course or "") else "NA"


class Race:
    __slots__ = ("key", "date", "course", "course_id", "track", "disc", "furlongs", "going",
                 "secs", "class_grp", "min_age", "w_lbs", "w_or", "w_rpr", "runners", "par",
                 "fig_w", "ga")

    @property
    def skey(self):
        return (self.track, self.disc, self.furlongs)

    @property
    def mkey(self):
        fam = "JUMPS" if self.disc in JUMPS else self.disc
        return (self.date, self.course_id, fam)

    @property
    def pgroup(self):
        if self.disc in JUMPS:
            age = "young" if self.min_age and self.min_age <= 4 else "older"
        else:
            age = "2yo" if self.min_age == 2 else "3yo" if self.min_age == 3 else "older"
        return (self.disc, self.class_grp, age)


def load_races(paths, keep_horses=None, before=None):
    """Races from history files. Runner rows are kept for keep_horses (None = everyone)."""
    races, seen = {}, set()
    new_surface = surface_changes()
    for path in paths:
        with open_text(path) as handle:
            for row in csv.DictReader(handle):
                date = str(row.get("date") or "").replace("/", "-")
                if not date[:4].isdigit() or (before and date >= before):
                    continue
                cid, is_aw = course_key(row.get("course") or "")
                horse = name_key(row.get("horse"))
                if (date, cid, horse) in seen:
                    continue
                seen.add((date, cid, horse))
                disc = discipline(row.get("type"), is_aw)
                furlongs = dist_to_furlongs(row.get("dist"))
                if not disc or not furlongs:
                    continue
                key = (date, cid, row.get("race_id") or row.get("off"))
                race = races.get(key)
                if race is None:
                    race = races[key] = Race()
                    race.key, race.date, race.course, race.course_id = key, date, row.get("course"), cid
                    race.track, race.disc, race.furlongs = track_key(row.get("course")), disc, furlongs
                    if disc == "AW_FLAT" and cid in new_surface and date < new_surface[cid]:
                        race.track += "_old_surface"   # e.g. Southwell Fibresand before Tapeta
                    race.going = going_group(row.get("going"))
                    race.secs = race.w_lbs = race.w_or = race.w_rpr = race.min_age = None
                    race.class_grp = class_group(row.get("class"), row.get("course"))
                    race.runners, race.par, race.fig_w, race.ga = [], None, None, None
                secs = to_float(row.get("secs")) or parse_time(row.get("time"))
                pos, lbs, age = to_int(row.get("pos")), weight_lbs(row), to_int(row.get("age"))
                if age and (race.min_age is None or age < race.min_age):
                    race.min_age = age
                if pos == 1:
                    race.w_lbs, race.w_or, race.w_rpr = lbs, to_int(row.get("or")), to_int(row.get("rpr"))
                    race.secs = secs   # rows carry each horse's own time: the race time is the winner's
                if keep_horses is None or horse in keep_horses:
                    race.runners.append((horse, pos, to_float(row.get("ovr_btn")), lbs,
                                         to_int(row.get("rpr")), to_int(row.get("ts")),
                                         row.get("sp"), (row.get("comment") or "")[:60]))
    out = []
    for race in races.values():
        speed = race.furlongs * METRES_PER_FURLONG / race.secs if race.secs else 0
        if not 9.0 <= speed <= 19.5:   # impossible time for the trip -> data error
            race.secs = None
        out.append(race)
    out.sort(key=lambda r: r.date)
    return out


def fit_pars(races):
    """Typical winner rating per (discipline, class, age group) + winner RPR-minus-OR offset."""
    rpr, offset = defaultdict(list), defaultdict(list)
    for r in races:
        if r.w_rpr is None:
            continue
        rpr[r.pgroup].append(r.w_rpr)
        if r.w_or:
            offset[r.pgroup].append(r.w_rpr - r.w_or)
    return ({g: statistics.median(v) for g, v in rpr.items() if len(v) >= 20},
            {g: statistics.median(v) for g, v in offset.items() if len(v) >= 20})


def race_par(race, pars, offsets):
    """Expected winner figure from PRE-RACE facts: the winner's official rating if it had one
    (+ the usual winner margin over their mark), else the class/age typical winner rating."""
    if race.w_or and race.pgroup in offsets:
        return race.w_or + offsets[race.pgroup]
    return pars.get(race.pgroup)


class SpeedModel:
    def __init__(self, races, fit_before=None, iterations=4):
        self.races = races
        train = [r for r in races if r.secs and (not fit_before or r.date < fit_before)]
        self.pars, self.offsets = fit_pars(train)
        for r in races:
            r.par = race_par(r, self.pars, self.offsets)
        self.standards, self.counts, self.going = {}, {}, {}
        for _ in range(iterations):
            groups = defaultdict(list)
            for r in train:
                if r.par is None or r.w_lbs is None:
                    continue
                base = self.standards.get(r.skey, r.secs)
                lps = lbs_per_second(r.furlongs, r.disc, base)
                groups[r.skey].append(r.secs - self.going.get(r.mkey, 0.0) * r.furlongs
                                      + (r.par - r.w_lbs) / lps)
            self.standards = {k: statistics.median(v) for k, v in groups.items()
                              if len(v) >= MIN_STANDARD_RACES}
            self.counts = {k: len(groups[k]) for k in self.standards}
            self.going = self._going_allowances()
        for r in races:
            r.ga = self.going.get(r.mkey)
            r.fig_w = self._winner_figure(r)
        # Standards sit at our average ground; to describe the ground in words we measure
        # against a typical GOOD (turf) / STANDARD (all-weather) meeting instead.
        base = defaultdict(list)
        seen = set()
        for r in races:
            if r.ga is not None and r.mkey not in seen and r.going in ("GOOD", "STANDARD"):
                seen.add(r.mkey)
                base[r.mkey[2]].append(r.ga)
        self.good_base = {fam: statistics.median(v) for fam, v in base.items()}

    def ground_vs_good(self, mkey):
        ga = self.going.get(mkey)
        return None if ga is None else ga - self.good_base.get(mkey[2], 0.0)

    def _deviation(self, r):
        std = self.standards.get(r.skey)
        if std is None or r.secs is None or r.par is None or r.w_lbs is None:
            return None
        lps = lbs_per_second(r.furlongs, r.disc, std)
        return (r.secs - std + (r.par - r.w_lbs) / lps) / r.furlongs

    def _going_allowances(self):
        devs = defaultdict(list)
        for r in self.races:
            d = self._deviation(r)
            if d is not None:
                devs[r.mkey].append(d)
        out = {}
        for m, values in devs.items():
            mid = statistics.median(values)
            kept = [v for v in values if abs(v - mid) <= OUTLIER_SECS_PER_F] or values
            out[m] = sum(kept) / (len(kept) + GOING_SHRINK)
        return out

    def _winner_figure(self, r):
        std = self.standards.get(r.skey)
        if std is None or r.secs is None or r.w_lbs is None or r.ga is None:
            return None
        lps = lbs_per_second(r.furlongs, r.disc, std)
        fig = (std + r.ga * r.furlongs - r.secs) * lps + r.w_lbs
        if r.par is not None and not -MAX_BELOW_PAR <= fig - r.par <= MAX_ABOVE_PAR:
            return None
        return fig

    def runner_figures(self, race):
        """[(horse, figure or None, runner tuple)] for the kept runners of a race."""
        out = []
        lpl = lbs_per_length(race.furlongs, race.disc)
        for runner in race.runners:
            horse, pos, btn, lbs = runner[:4]
            fig = None
            if race.fig_w is not None and pos and lbs and race.w_lbs:
                btn = 0.0 if pos == 1 else btn
                if btn is not None and btn <= MAX_BEATEN_LENGTHS:
                    fig = round(race.fig_w - btn * lpl + (lbs - race.w_lbs))
            out.append((horse, fig, runner))
        return out

    def horse_runs(self):
        """horse -> [run dict] in date order, every kept runner with its figure."""
        runs = defaultdict(list)
        for race in self.races:
            for horse, fig, runner in self.runner_figures(race):
                runs[horse].append({"date": race.date, "course": race.course,
                                    "course_id": race.course_id, "disc": race.disc,
                                    "furlongs": race.furlongs, "going": race.going,
                                    "pos": runner[1], "ran": None, "fig": fig,
                                    "rpr": runner[4], "ts": runner[5], "sp": runner[6],
                                    "comment": runner[7], "race": race})
        return runs


def describe_going(ga):
    """ga = seconds per furlong vs a typical good-ground (AW: standard) meeting."""
    if ga is None:
        return ""
    if abs(ga) < 0.1:
        return f"like typical good ground ({ga:+.2f} s/f)"
    return f"{abs(ga):.2f} s/f {'slower' if ga > 0 else 'faster'} than typical good ground"
