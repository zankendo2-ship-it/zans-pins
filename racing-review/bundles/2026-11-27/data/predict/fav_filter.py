"""E6-LIVE favourite filter - forward test, pre-registered in rules/RULES.md (22 Oct 2026). Background only.

For every locked race-day win pick that is the 09:30 favourite: score = ln(p_evidence / p_powered_market), where p_evidence is
the evidence-only chance (form_chance) normalised in the race and p_powered_market = the Sky Bet 09:30 price normalised and
raised to the power b (flat 1.11, jumps 1.15). FILTER-PASS = score above the cut-off (40th percentile of SP favourites
2021-26: flat -0.5071, jumps -0.5527). Settled at the Sky Bet 09:30 price, SP and BOG, with CLV = 09:30 price / SP - 1.

    python -m predict.fav_filter --date D            # after the 09:30 pack is locked
    python -m predict.fav_filter --date D --settle   # evening review -> reports/predictions/fav_filter_record.md
"""
import argparse
import csv
import json
import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from predict.bet_now import parse_terms  # noqa: E402
from predict.leak_finder import first_locked  # noqa: E402
from track_stats.parse import course_key  # noqa: E402

B = {"FLAT": 1.11, "JUMPS": 1.15}
CUT = {"FLAT": -0.5071, "JUMPS": -0.5527}
PRED = REPO / "reports" / "predictions"
NON_RUNNER = {"NR", "RR", "WITHDRAWN", "VOID", "NON-RUNNER", "W"}


def fam(disc):
    return "FLAT" if str(disc).upper() in ("FLAT", "AW_FLAT") else "JUMPS"


def nkey(name):
    return "".join(ch for ch in str(name).lower() if ch.isalnum())


def sky_prices(day):
    path = REPO / "reports" / "odds" / day / "d0_morning.csv"
    out = {}
    if not path.exists():
        return out
    for r in csv.DictReader(open(path, encoding="utf-8")):
        if (r.get("status") or "").upper() not in ("RUNNER", ""):
            continue
        # Sky Bet ONLY (second opinion 22 Oct: the test is about the owner's bookmaker - no silent best_dec fallback)
        sky = [t for t in parse_terms(r.get("bookie_terms")) if t["bookie"] == "Sky Bet" and t["dec"]]
        if sky:
            out.setdefault((course_key(r["course"])[0], r["off_time"][:5]), {})[nkey(r["horse"])] = (sky[0]["dec"], True)
    return out


def record(day):
    lock = first_locked(day)
    src = lock / "predictions.json" if lock and (lock / "predictions.json").exists() else PRED / day / "predictions.json"
    races = json.loads(src.read_text())
    # 4 Nov (review team): predictions.json is the model BEFORE the course-method overlay; the locked win pick the owner saw is
    # in the course jsons of the same folder (11 of 501 races differed 23 Oct-4 Nov). Use the published pick (E6: "locked picks").
    pub = {}
    for fp in sorted(lock.glob("*.json")) if lock else []:
        try:
            j = json.loads(fp.read_text())
        except ValueError:
            continue
        if isinstance(j, dict) and isinstance(j.get("picks"), list):
            for p in j["picks"]:
                if p.get("win"):
                    pub[(course_key(j.get("course") or fp.stem)[0], str(p.get("time"))[:5])] = p
    for r in races:
        p = pub.get((course_key(r["course"])[0], r["off_time"][:5]))
        if p:
            r["win"], r["confidence"] = p["win"], p.get("confidence", r.get("confidence"))
    prices = sky_prices(day)
    rows, no_sky = [], []
    for r in races:
        book = prices.get((course_key(r["course"])[0], r["off_time"][:5]))
        if not book or nkey(r["win"]) not in book:
            no_sky.append(f'{r["off_time"][:5]} {r["course"]} {r["win"]}')  # reported separately, never scored
            continue
        field = [(x["name"], x.get("form_chance"), book.get(nkey(x["name"]))) for x in r.get("all", [])]
        field = [f for f in field if f[1] and f[2]]
        if len(field) < 2:
            continue
        fav = min(field, key=lambda f: f[2][0])
        if nkey(fav[0]) != nkey(r["win"]):
            continue  # only races where our win pick is the 09:30 favourite
        f = fam(r["discipline"])
        pe_sum = sum(x[1] for x in field)
        pw = {nkey(x[0]): (1 / x[2][0]) ** B[f] for x in field}
        pw_sum = sum(pw.values())
        score = math.log((fav[1] / pe_sum) / (pw[nkey(fav[0])] / pw_sum))
        p_mkt = (1 / fav[2][0]) / sum(1 / x[2][0] for x in field)  # margin-free Sky Bet 09:30 chance (for A/E)
        rows.append({"course": r["course"], "time": r["off_time"][:5], "horse": r["win"], "code": f,
                     "confidence": r.get("confidence"), "price_0930": fav[2][0], "sky": fav[2][1],
                     "p_mkt": round(p_mkt, 4), "score": round(score, 4), "filter": "PASS" if score > CUT[f] else "FAIL"})
    out = PRED / day / "fav_filter.json"
    out.write_text(json.dumps({"date": day, "source": str(src.relative_to(REPO)), "rows": rows, "no_sky_price": no_sky}, indent=1))
    n_pass = sum(1 for x in rows if x["filter"] == "PASS")
    print(f"{day}: {len(rows)} win picks are the 09:30 favourite - FILTER-PASS {n_pass}, FILTER-FAIL {len(rows) - n_pass}"
          + (f"; {len(no_sky)} picks without a Sky Bet price left out" if no_sky else ""))
    return rows


def sp_dec(text):
    t = str(text or "").strip().upper().rstrip("FJC").strip()
    if t in ("EVENS", "EVS", "EVEN"):
        return 2.0
    if "/" in t:
        a, b = t.split("/")[:2]
        return 1 + float(a) / float(b)
    try:
        return float(t)
    except ValueError:
        return None


def settle(day):
    path = PRED / day / "fav_filter.json"
    if not path.exists():
        record(day)
    data = json.loads(path.read_text())
    res = {}
    rpath = REPO / "reports" / "results_sl" / day / "results.csv"
    for r in csv.DictReader(open(rpath, encoding="utf-8")) if rpath.exists() else []:
        res[(course_key(r["course"])[0], r["off"][:5], nkey(r["horse"]))] = (str(r["pos"]), sp_dec(r.get("sp")))
    for x in data["rows"]:
        got = res.get((course_key(x["course"])[0], x["time"], nkey(x["horse"])))
        if not got:
            x["result"] = None
            continue
        pos, sp = got
        if pos.upper() in NON_RUNNER:  # void - never a £10 loss (second opinion 22 Oct)
            x.update(result="NR", void=True)
            continue
        won = pos == "1"
        x.update(result=pos, sp=sp, won=won,
                 pl_0930=round(10 * (x["price_0930"] - 1) if won else -10, 2),
                 pl_sp=round(10 * (sp - 1) if won else -10, 2) if sp else None,
                 pl_bog=round(10 * (max(x["price_0930"], sp or 0) - 1) if won else -10, 2),
                 clv=round(x["price_0930"] / sp - 1, 4) if sp else None)
    path.write_text(json.dumps(data, indent=1))
    running()


def running():
    rows = []
    for f in sorted(PRED.glob("2026-*/fav_filter.json")):
        rows += [dict(x, day=f.parent.name) for x in json.loads(f.read_text())["rows"] if x.get("result") and not x.get("void")]
    lines = ["# E6-LIVE favourite filter - forward test (pre-registered rules/RULES.md, 22 Oct 2026)", "",
             "Locked 09:30 win picks that are the 09:30 favourite. £10 win at the Sky Bet 09:30 price, SP and BOG. "
             "CLV = 09:30 price / SP - 1. Background only - not on the slip.", "",
             "| Group | Bets | Won | A/E v margin-free Sky 09:30 (SE) | ROI 09:30 | ROI SP | ROI BOG | Mean CLV (t) |",
             "|---|---|---|---|---|---|---|---|"]
    ae = {}
    for g in ("PASS", "FAIL"):
        s = [x for x in rows if x["filter"] == g]
        if not s:
            continue
        n = len(s)
        clv = [x["clv"] for x in s if x.get("clv") is not None]
        m = sum(clv) / len(clv) if clv else 0
        sd = (sum((c - m) ** 2 for c in clv) / (len(clv) - 1)) ** 0.5 if len(clv) > 1 else 0
        t = m / (sd / len(clv) ** 0.5) if sd else 0
        roi = lambda k: sum(x[k] or -10 for x in s) / (10 * n)
        exp = sum(x["p_mkt"] for x in s if x.get("p_mkt"))
        var = sum(x["p_mkt"] * (1 - x["p_mkt"]) for x in s if x.get("p_mkt"))
        a_e = sum(x["won"] for x in s if x.get("p_mkt")) / exp if exp else 0
        se = var ** 0.5 / exp if exp else 0
        ae[g] = (a_e, se)
        lines.append(f"| FILTER-{g} | {n} | {sum(x['won'] for x in s)} | {a_e:.2f} ({se:.2f}) | {roi('pl_0930'):+.1%} | "
                     f"{roi('pl_sp'):+.1%} | "
                     f"{roi('pl_bog'):+.1%} | {m:+.3f} ({t:.1f}) |")
    if "PASS" in ae and "FAIL" in ae:
        d = ae["PASS"][0] - ae["FAIL"][0]
        z = d / ((ae["PASS"][1] ** 2 + ae["FAIL"][1] ** 2) ** 0.5 or 1)
        lines += ["", f"A/E gap PASS - FAIL: {d:+.2f} (z {z:.1f})."]
    voids = sum(1 for f in PRED.glob("2026-*/fav_filter.json") for x in json.loads(f.read_text())["rows"] if x.get("void"))
    lines += ["", f"Days: {len({x['day'] for x in rows})}. Non-runners void ({voids}), picks without a Sky Bet price left out. "
              "Pass rule (RULES.md, amended 22 Oct before any live bet): 300+ FILTER-PASS bets, PASS A/E above FAIL A/E against "
              "the margin-free Sky Bet 09:30 price with z >= 2, and PASS beats FAIL at the 09:30 price. CLV is a separate "
              "timing check (09:30 v SP), not a filter test. BOG only if the owner's Sky Bet Club qualification is confirmed."]
    (PRED / "fav_filter_record.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[4:]))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    ap.add_argument("--settle", action="store_true")
    a = ap.parse_args(argv)
    settle(a.date) if a.settle else record(a.date)


if __name__ == "__main__":
    main()
