"""Build the speed-figure standards and BACKTEST speed figures + pace map on later races.

Fits standard times and class pars on races before --fit-before, then walks every later race
in date order rating each runner ONLY from its earlier runs, and checks:
  1. agreement with Racing Post's Topspeed / RPR on the same runs (are the figures sane?)
  2. top-rated horse per race: win % and A/E (winners / margin-free SP chances; 1.00 = as
     the market expected, above 1 = beats the market) for our speed figures vs RPR vs Topspeed
  3. pace map: every role in every projected-pace scenario - win % and A/E, flat and jumps
Writes reports/speed/standards.csv and reports/speed/validation.md.

Usage:
    python -m speed.validate --history history/*.csv.gz --fit-before 2025-01-01
"""
import argparse
import csv
import math
from collections import defaultdict, deque
from datetime import date as Date
from pathlib import Path

from track_stats.extra import sp_decimal
from track_stats.parse import furlongs_label, running_style

from .figures import JUMPS, SpeedModel, load_races
from .pacemap import fit, race_scenario, runner_role

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "reports" / "speed"
MIN_FIELD = 5
LOOKBACK_DAYS = 365


def pearson(pairs):
    n = len(pairs)
    if n < 3:
        return None
    mx = sum(a for a, _ in pairs) / n
    my = sum(b for _, b in pairs) / n
    sxy = sum((a - mx) * (b - my) for a, b in pairs)
    sx = math.sqrt(sum((a - mx) ** 2 for a, _ in pairs))
    sy = math.sqrt(sum((b - my) ** 2 for _, b in pairs))
    return sxy / (sx * sy) if sx and sy else None


class Tally:
    def __init__(self):
        self.n = self.wins = 0
        self.expected = 0.0

    def add(self, won, chance):
        self.n += 1
        self.wins += won
        self.expected += chance or 0

    def row(self):
        if not self.n:
            return "0", "-", "-"
        ae = f"{self.wins / self.expected:.2f}" if self.expected else "-"
        return f"{self.n:,}", f"{self.wins / self.n:.1%}", ae


def chances(runners):
    implied = [1 / d if d else None for d in (sp_decimal(r[6]) for r in runners)]
    if not all(implied):
        return [None] * len(runners)
    book = sum(implied)
    return [p / book for p in implied]


def best_recent(history, day, field, group, n=3):
    cutoff = (Date.fromisoformat(day).toordinal() - LOOKBACK_DAYS)
    values = [h[field] for h in [h for h in history if h["group"] == group][-n:]
              if h[field] is not None and Date.fromisoformat(h["date"]).toordinal() >= cutoff]
    return max(values) if values else None


def write_standards(model, path):
    rows = []
    for (track, disc, furlongs), secs in sorted(model.standards.items()):
        rows.append({"track": track, "discipline": disc, "distance": furlongs_label(furlongs),
                     "furlongs": furlongs, "standard_secs": round(secs, 2),
                     "standard_time": f"{int(secs // 60)}:{secs % 60:05.2f}",
                     "races": model.counts[(track, disc, furlongs)]})
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def backtest(model, fit_before):
    state = defaultdict(lambda: deque(maxlen=12))
    agree = {"ts": [], "rpr": []}
    top = {k: {"ALL": Tally(), "FLAT": Tally(), "JUMPS": Tally()}
           for k in ("speed", "rpr", "ts", "combined")}
    pace, pace_fit = defaultdict(Tally), defaultdict(Tally)
    by_date = defaultdict(list)
    for race in model.races:
        by_date[race.date].append(race)
    for day in sorted(by_date):
        updates = []
        for race in by_date[day]:
            figs = model.runner_figures(race)
            test = day >= fit_before and len(race.runners) >= MIN_FIELD
            if test:
                probs = chances(race.runners)
                fam = "JUMPS" if race.disc in JUMPS else "FLAT"
                ratings = {"speed": [], "rpr": [], "ts": [], "combined": []}
                roles = {}
                for (horse, fig, runner), p in zip(figs, probs):
                    hist = state.get(horse, ())
                    for key, field in (("speed", "fig"), ("rpr", "rpr"), ("ts", "ts")):
                        ratings[key].append(best_recent(hist, day, field, fam))
                    sp_, rp_ = ratings["speed"][-1], ratings["rpr"][-1]
                    ratings.setdefault("combined", []).append(
                        (sp_ + rp_) / 2 if sp_ is not None and rp_ is not None else None)
                    roles[horse] = runner_role([h["style"] for h in hist])[0]
                    if fig is not None and runner[5] is not None:
                        agree["ts"].append((fig, runner[5]))
                    if fig is not None and runner[4] is not None:
                        agree["rpr"].append((fig, runner[4]))
                for key, values in ratings.items():
                    rated = [v for v in values if v is not None]
                    if len(rated) < 0.8 * len(values) or not rated:
                        continue
                    best = max(rated)
                    if values.count(best) != 1:
                        continue
                    i = values.index(best)
                    won, p = figs[i][2][1] == 1, probs[i]
                    top[key]["ALL"].add(won, p)
                    top[key][fam].add(won, p)
                scenario, _ = race_scenario(roles)
                for (horse, fig, runner), p in zip(figs, probs):
                    pace[(fam, scenario, roles[horse])].add(runner[1] == 1, p)
                    if roles[horse] != "UNKNOWN" and scenario != "UNKNOWN":
                        pace_fit[(fam, fit(scenario, roles[horse], race.disc))].add(runner[1] == 1, p)
            for horse, fig, runner in figs:
                updates.append((horse, {"date": day, "group": "JUMPS" if race.disc in JUMPS else "FLAT",
                                        "fig": fig, "rpr": runner[4],
                                        "ts": runner[5], "style": running_style(runner[7])}))
        for horse, entry in updates:
            state[horse].append(entry)
    return agree, top, pace, pace_fit


def render(model, fit_before, n_std, agree, top, pace, pace_fit):
    tested = sum(1 for r in model.races if r.date >= fit_before)
    lines = ["# Speed figures + pace map — build and backtest", "",
             f"Standards and class pars fitted on races before **{fit_before}**; every race from "
             f"then on ({tested:,} races) is rated from each runner's EARLIER runs only.", "",
             f"- Standard times: **{n_std:,}** course/track + discipline + distance combinations "
             f"(10+ timed races each).",
             f"- Going allowances worked out for **{len(model.going):,}** meetings.", ""]
    lines += ["## 1. Do our figures agree with Racing Post's? (same runs, test period)", ""]
    for key, name in (("ts", "Topspeed (RP's own time figure)"), ("rpr", "RPR (RP's form rating)")):
        r = pearson(agree[key])
        lines.append(f"- vs {name}: correlation **{r:.2f}** over {len(agree[key]):,} runs"
                     if r is not None else f"- vs {name}: not enough data")
    lines += ["", "## 2. Top-rated horse (best of last 3 runs within a year) — test period", "",
              "| Rating | Races | Top-rated won | A/E vs SP |", "|---|---|---|---|"]
    names = {"speed": "Our speed figure", "rpr": "RPR", "ts": "Topspeed",
             "combined": "Speed + RPR average"}
    for fam in ("ALL", "FLAT", "JUMPS"):
        for key in ("speed", "rpr", "ts", "combined"):
            n, sr, ae = top[key][fam].row()
            lines.append(f"| {names[key]} ({fam.lower()}) | {n} | {sr} | {ae} |")
    lines += ["", "A/E = winners / chances implied by the starting price with the bookmaker "
              "margin removed: 1.00 = exactly as the market expected; above 1 = the rating "
              "finds winners the market underrates.", "",
              "## 3. Pace map — does the SUITS / AGAINST call hold up? (test period)", "",
              "| Code | Pace map says | Runners | Won | A/E vs SP |", "|---|---|---|---|---|"]
    for fam in ("FLAT", "JUMPS"):
        for verdict in ("SUITS", "NEUTRAL", "AGAINST"):
            n, sr, ae = pace_fit[(fam, verdict)].row()
            lines.append(f"| {fam.lower()} | {verdict} | {n} | {sr} | {ae} |")
    lines += ["", "### Every running style in every projected pace", "", "| Code | Projected pace | Role | Runners | Won | A/E vs SP |", "|---|---|---|---|---|---|"]
    for (fam, scenario, role), tally in sorted(pace.items()):
        if role == "UNKNOWN" or scenario == "UNKNOWN" or tally.n < 200:
            continue
        n, sr, ae = tally.row()
        lines.append(f"| {fam.lower()} | {scenario} | {role} | {n} | {sr} | {ae} |")
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Build + backtest speed figures and pace map.")
    parser.add_argument("--history", nargs="+", required=True)
    parser.add_argument("--fit-before", default="2025-01-01")
    parser.add_argument("--out", default=str(OUT_DIR))
    args = parser.parse_args(argv)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    races = load_races(args.history)
    print(f"{len(races):,} races loaded; {sum(1 for r in races if r.secs):,} with a valid time")
    model = SpeedModel(races, fit_before=args.fit_before)
    n_std = write_standards(model, out / "standards.csv")
    agree, top, pace, pace_fit = backtest(model, args.fit_before)
    text = render(model, args.fit_before, n_std, agree, top, pace, pace_fit)
    (out / "validation.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
