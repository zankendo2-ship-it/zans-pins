"""E13-LIVE 'well handicapped' forward test - pre-registered in rules/RULES.md (23 Oct 2026). Background only.

A handicap runner whose best RPR in its last 3 runs (UK/IRE history, runs within 2 years) is 10lb or more above today's
official mark, priced 2.00-3.99 by Sky Bet at the 09:30 (d0_morning) check. Same code family only (flat+AW / jumps). History (scripts/well_handicapped_check.py,
margin-free SP A/E, 2019-22 | 2023-26): flat 1.36 (553, +16.6% SP) | 1.31 (629, +12.0%); jumps 1.40 (838, +20.4%) |
1.19 (469, +1.3%); all other handicap runners at 2.00-3.99 1.03-1.06, -8% to -10%. Found by the ZANS Review team.

    python -m predict.well_handicapped --date D            # after the 09:30 pack is locked
    python -m predict.well_handicapped --date D --check d-1_evening   # night-before PREVIEW (never settled)
    python -m predict.well_handicapped --date D --settle   # evening review -> reports/predictions/well_handicapped_record.md
"""
import argparse
import csv
import glob
import gzip
import json
import sys
from datetime import date as Date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from form.history import name_key  # noqa: E402
from predict.bet_now import parse_terms  # noqa: E402
from predict.fav_filter import NON_RUNNER, sp_dec  # noqa: E402
from track_stats.parse import course_key  # noqa: E402

PRED = REPO / "reports" / "predictions"
GAP, LO, HI = 10, 2.0, 3.99


def fam_of(text):
    """F = flat turf + all-weather, J = jumps (a hurdle / chase RPR is not comparable with a flat mark)."""
    return "J" if str(text).upper() in ("HURDLE", "CHASE", "NH FLAT", "JUMPS") else "F"


def best3(names, day):
    """Best RPR of each horse's last 3 runs in each code family before `day` (runs within 730 days)."""
    runs = {}
    cut = Date.fromisoformat(day)
    for f in sorted(glob.glob(str(REPO / "history" / "*.csv.gz"))):
        with gzip.open(f, "rt", encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                k = name_key(r.get("horse"))
                if k not in names:
                    continue
                try:
                    d = Date.fromisoformat(str(r["date"])[:10])
                    rpr = float(r.get("rpr") or "")
                except ValueError:
                    continue
                if d < cut and (cut - d).days <= 730:
                    runs.setdefault((k, fam_of(r.get("type"))), {})[(d, str(r.get("course")))] = rpr  # same run in two files counted once
    return {k: max(v[x] for x in sorted(v)[-3:]) for k, v in runs.items()}


def sky(day, check="d0_morning"):
    out = {}
    path = REPO / "reports" / "odds" / day / f"{check}.csv"
    for r in csv.DictReader(open(path, encoding="utf-8")) if path.exists() else []:
        if (r.get("status") or "").upper() not in ("RUNNER", ""):
            continue
        s = [t for t in parse_terms(r.get("bookie_terms")) if t["bookie"] == "Sky Bet" and t["dec"]]
        if s:
            out[(course_key(r["course"])[0], r["off_time"][:5], name_key(r["horse"]))] = s[0]["dec"]
    return out


def record(day, check="d0_morning"):
    """check d0_morning = the E13 record; any other check = a PREVIEW file only (never settled, never counted)."""
    card = json.loads((REPO / "reports" / "racecards" / day / "racecards.json").read_text())
    races = [r for r in card if r.get("handicap") and r.get("country") in ("GB", "IRE")]
    names = {name_key(x["name"]) for r in races for x in r["runners"] if not x.get("non_runner")}
    b3, prices = best3(names, day), sky(day, check)
    rows = []
    for r in races:
        for x in r["runners"]:
            k = name_key(x["name"])
            kf = (k, fam_of(r.get("race_code")))
            try:
                mark = int(x.get("ofr"))
            except (TypeError, ValueError):
                continue
            price = prices.get((course_key(r["course_name"])[0], r["off_time"][:5], k))
            if x.get("non_runner") or kf not in b3 or not price or not (LO <= price <= HI):
                continue
            if b3[kf] >= mark + GAP:
                rows.append({"course": r["course_name"], "time": r["off_time"][:5], "horse": x["name"],
                             "code": r.get("race_code"), "mark": mark, "best3": b3[kf], "gap": int(b3[kf] - mark),
                             "price_0930" if check == "d0_morning" else f"price_{check}": price})
    (PRED / day).mkdir(parents=True, exist_ok=True)
    out = "well_handicapped.json" if check == "d0_morning" else f"well_handicapped_preview_{check}.json"
    (PRED / day / out).write_text(json.dumps({"date": day, "check": check, "rows": rows}, indent=1))
    print(f"{day} ({check}{'' if check == 'd0_morning' else ' - PREVIEW only'}): {len(rows)} well-handicapped runners (best of last 3 RPR {GAP}+ lb above the mark, Sky Bet {LO:.2f}-{HI:.2f})")
    for x in rows:
        print(f"  `{x['time']} {x['course'].upper()}` {x['horse']} - mark {x['mark']}, best RPR {x['best3']:.0f} "
              f"(+{x['gap']} lb), Sky Bet {x.get('price_0930') or x.get('price_' + check):.2f}")
    return rows


def settle(day):
    path = PRED / day / "well_handicapped.json"
    if not path.exists():
        record(day)
    data = json.loads(path.read_text())
    res = {}
    rpath = REPO / "reports" / "results_sl" / day / "results.csv"
    for r in csv.DictReader(open(rpath, encoding="utf-8")) if rpath.exists() else []:
        res[(course_key(r["course"])[0], r["off"][:5], name_key(r["horse"]))] = (str(r["pos"]), sp_dec(r.get("sp")))
    for x in data["rows"]:
        got = res.get((course_key(x["course"])[0], x["time"], name_key(x["horse"])))
        if not got:
            x["result"] = None
            continue
        pos, sp = got
        if pos.upper() in NON_RUNNER:
            x.update(result="NR", void=True)
            continue
        won = pos == "1"
        x.update(result=pos, sp=sp, won=won, pl_0930=round(10 * (x["price_0930"] - 1) if won else -10, 2),
                 pl_sp=round(10 * (sp - 1) if won else -10, 2) if sp else None,
                 pl_bog=round(10 * (max(x["price_0930"], sp or 0) - 1) if won else -10, 2))
    path.write_text(json.dumps(data, indent=1))
    rows = []
    for f in sorted(PRED.glob("2026-*/well_handicapped.json")):
        rows += [dict(x, day=f.parent.name) for x in json.loads(f.read_text())["rows"] if x.get("result") and not x.get("void")]
    n = len(rows)
    lines = ["# E13-LIVE well-handicapped runners - forward test (pre-registered rules/RULES.md, 23 Oct 2026)", "",
             f"Handicap runners, best RPR of the last 3 runs {GAP}+ lb above today's mark, Sky Bet {LO:.2f}-{HI:.2f} at 09:30. "
             "£10 win. Background only - not on the slip.", ""]
    if n:
        won = sum(x["won"] for x in rows)
        for k, lab in (("pl_0930", "Sky Bet 09:30 price"), ("pl_sp", "SP"), ("pl_bog", "BOG")):
            pl = sum(x[k] or -10 for x in rows)
            lines.append(f"- {lab}: {n} bets, {won} won, {pl:+.2f} ({pl / (10 * n):+.1%})")
    else:
        lines.append("- no settled bets yet")
    lines += ["", f"Days: {len({x['day'] for x in rows})}. Pass rule (RULES.md E13): 150+ bets and profit at the Sky Bet 09:30 "
              "price in both halves, before it may go near the slip (owner decides)."]
    (PRED / "well_handicapped_record.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[4:]))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    ap.add_argument("--settle", action="store_true")
    ap.add_argument("--check", default="d0_morning", help="another price check (e.g. d-1_evening) = preview file only")
    a = ap.parse_args(argv)
    settle(a.date) if a.settle else record(a.date, a.check)


if __name__ == "__main__":
    main()
