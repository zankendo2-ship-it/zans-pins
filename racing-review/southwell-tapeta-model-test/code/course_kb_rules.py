"""Method rule tests split by exact going, for every course and code (feeds scripts/course_kb.py).

Uses the same rules and pre-race facts as methods/audit.py, over every UK/IRE race from 2019,
and counts FLAGGED runners per (course, code, rule, going, period):
runners, winners, margin-free expected winners, £1 SP return.

    python scripts/course_kb_rules.py --out /tmp/claude-0/kb/rules_by_going.pkl
"""
import argparse
import glob
import pickle
import sys
from collections import defaultdict
from datetime import date as Date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from methods.audit import flags_for_race, load, race_info  # noqa: E402

CODE = {"FLAT": "FLAT", "AW_FLAT": "AW_FLAT", "HURDLE": "JUMPS", "CHASE": "JUMPS", "NHF": "JUMPS"}


def period(day):
    return "2019-21" if day < "2022-01-01" else "2022-26"


import json as _j
_c = _j.load(open(str(REPO / 'config' / 'courses.json'))); _c = _c.get('courses', _c)
SURF = {k: (v.get('surface_since') or {}).get('AW_FLAT') for k, v in _c.items() if (v.get('surface_since') or {}).get('AW_FLAT')}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--since", default="2019-01-01")
    args = ap.parse_args()
    races = load(sorted(glob.glob(str(REPO / "history" / "*.csv.gz"))), race_info(str(REPO / "data" / "results_uki.csv.gz")))
    hist = defaultdict(list)
    jockey_rides, jockey_runs = set(), defaultdict(list)
    tally = defaultdict(lambda: [0, 0, 0.0, 0.0])   # n, wins, expected, return
    for race in races:
        race["fam"] = "JUMPS" if race["disc"] in ("HURDLE", "CHASE", "NHF") else "FLAT"
        day = Date.fromisoformat(race["date"]).toordinal()
        sps = [r["sp"] for r in race["runners"]]
        winners = [r for r in race["runners"] if r["pos"] == 1]
        _ss = SURF.get(race["course_id"]) if race["disc"] == "AW_FLAT" else None
        if _ss and race["date"] < _ss:
            pass   # 27 Nov: before this course's AW surface switch = different surface, not tested
        elif race["date"] >= args.since and all(sps) and len(race["runners"]) >= 4 and len(winners) == 1:
            book = sum(1 / s for s in sps)
            flags = flags_for_race(race, hist, jockey_rides, jockey_runs)
            key0 = (race["course_id"], CODE[race["disc"]], race["going"].title(), period(race["date"]))
            for r, f in zip(race["runners"], flags):
                won, chance = r["pos"] == 1, 1 / r["sp"] / book
                for name, flag in f.items():
                    if flag:
                        t = tally[key0 + (name,)]
                        t[0] += 1
                        t[1] += won
                        t[2] += chance
                        t[3] += r["sp"] if won else 0.0
        for r in race["runners"]:
            hist[r["horse"]].append({"day": day, "fam": race["fam"], "course_id": race["course_id"],
                                     "furlongs": race["furlongs"], "going": race["going"],
                                     "pos": r["pos"], "won": r["pos"] == 1, "rpr": r["rpr"],
                                     "handicap": race["handicap"], "comment": r["comment"]})
            if r["jockey"]:
                jockey_rides.add((r["horse"], r["jockey"]))
                jockey_runs[r["jockey"]].append((day, r["pos"] == 1))
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "wb") as fh:
        pickle.dump(dict(tally), fh)
    print(f"{len(tally):,} cells -> {args.out}")


if __name__ == "__main__":
    main()
