"""Form check - the owner's checklist for every win pick, shown on the course cards.

Owner 2026-10-09: "I don't feel you study the historic data enough at courses along with the horse data, jockey and trainer
strike rate, if the horse is suited to the ground, is it handicapped well, etc". The model already uses these facts; this
puts them in front of the owner, one line per pick:
  ground / trip / course record (Racing Post card stats), handicap mark v best RPR and v the rating it last won off (our
  history, same code: flat, hurdle, chase), trainer + jockey last 14 days and at this course (5 years), days off, and how far
  the trainer has sent the horse (trainer's home = middle of the courses they ran at in the last year, course positions
  approximate).

Travel TEST (2018-2026 UK/IRE history, margin-free A/E): horses sent 300km+ win more often (14.7% v 9.9% under 100km) but
the price mostly knows it - A/E 1.03 in both 2018-22 and 2023-26; under 10/1 A/E 1.04 (15,097 runners), 10/1+ A/E 0.95.
200-300km = 0.98. So travel is shown, not used to pick.

    python -m predict.formcheck --date 2026-10-10   -> reports/racecards/<date>/formcheck.json
"""
import argparse
import csv
import datetime as dt
import glob
import json
import math
import re
from collections import defaultdict
from pathlib import Path

from form.history import days_since, name_key, open_text, to_int

REPO = Path(__file__).resolve().parent.parent

# approximate racecourse positions (town level; good enough for 'how far did it travel')
COURSE_POS = {
    "aintree": (53.48, -2.95), "ascot": (51.41, -0.68), "ayr": (55.46, -4.61), "ballinrobe": (53.63, -9.23),
    "bangor": (52.99, -2.93), "bath": (51.42, -2.41), "bellewstown": (53.66, -6.34), "beverley": (53.85, -0.45),
    "brighton": (50.83, -0.11), "carlisle": (54.87, -2.92), "cartmel": (54.20, -2.95), "catterick": (54.38, -1.63),
    "chelmsford": (51.73, 0.53), "cheltenham": (51.92, -2.06), "chepstow": (51.65, -2.69), "chester": (53.19, -2.90),
    "clonmel": (52.36, -7.68), "cork": (52.13, -8.65), "curragh": (53.16, -6.82), "doncaster": (53.52, -1.10),
    "down royal": (54.49, -6.10), "downpatrick": (54.32, -5.73), "dundalk": (54.00, -6.40), "epsom": (51.32, -0.25),
    "exeter": (50.66, -3.62), "fairyhouse": (53.52, -6.54), "fakenham": (52.83, 0.85), "ffos las": (51.75, -4.23),
    "fontwell": (50.85, -0.62), "galway": (53.30, -8.98), "goodwood": (50.89, -0.75), "gowran": (52.62, -7.06),
    "hamilton": (55.78, -4.05), "haydock": (53.48, -2.62), "hereford": (52.07, -2.73), "hexham": (54.95, -2.12),
    "huntingdon": (52.33, -0.24), "kelso": (55.61, -2.43), "kempton": (51.42, -0.40), "kilbeggan": (53.37, -7.50),
    "killarney": (52.05, -9.50), "laytown": (53.68, -6.24), "leicester": (52.60, -1.10), "leopardstown": (53.27, -6.20),
    "limerick": (52.58, -8.75), "lingfield": (51.17, -0.02), "listowel": (52.45, -9.48), "ludlow": (52.40, -2.75),
    "market rasen": (53.38, -0.32), "musselburgh": (55.95, -3.05), "naas": (53.22, -6.66), "navan": (53.64, -6.70),
    "newbury": (51.40, -1.30), "newcastle": (55.02, -1.62), "newmarket": (52.23, 0.37), "newton abbot": (50.53, -3.60),
    "nottingham": (52.95, -1.11), "perth": (56.42, -3.43), "plumpton": (50.93, -0.06), "pontefract": (53.70, -1.33),
    "punchestown": (53.18, -6.63), "redcar": (54.61, -1.07), "ripon": (54.12, -1.50), "roscommon": (53.62, -8.20),
    "salisbury": (51.06, -1.85), "sandown": (51.37, -0.36), "sedgefield": (54.65, -1.45), "sligo": (54.27, -8.47),
    "southwell": (53.07, -0.95), "stratford": (52.18, -1.72), "taunton": (50.99, -3.10), "thirsk": (54.23, -1.35),
    "thurles": (52.68, -7.82), "tipperary": (52.47, -8.17), "tramore": (52.16, -7.15), "uttoxeter": (52.90, -1.85),
    "warwick": (52.28, -1.60), "wetherby": (53.93, -1.37), "wexford": (52.35, -6.48), "wincanton": (51.05, -2.40),
    "windsor": (51.48, -0.63), "wolverhampton": (52.59, -2.14), "worcester": (52.20, -2.23), "yarmouth": (52.62, 1.72),
    "york": (53.94, -1.10),
}


def pos_of(course):
    c = re.sub(r"\(.*?\)", "", str(course or "")).lower().replace("_", " ").replace("-", " ").strip()
    c = c.replace("great yarmouth", "yarmouth").replace("bangor on dee", "bangor").replace("gowran park", "gowran")
    for k, v in COURSE_POS.items():
        if c == k or c.startswith(k):
            return v
    return None


def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (*a, *b))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 12742 * math.asin(math.sqrt(h))


def person_key(name):
    text = re.sub(r"\(.*?\)|\bBt\b", "", str(name or "")).strip()
    parts = [p for p in re.split(r"[\s.]+", text) if p]
    if not parts:
        return ""
    last = re.sub(r"[^a-z]", "", parts[-1].lower())
    return f"{parts[0][0].lower()} {last}" if len(parts) > 1 else last


def code_of(race_type):
    t = str(race_type or "").lower()
    return "chase" if "chase" in t else "hurdle" if "hurdle" in t else "nhf" if "nh flat" in t or t == "nhf" else "flat"


def build(race_date):
    day = REPO / "reports" / "racecards" / race_date
    ev = list(csv.DictReader(open(day / "evidence.csv", encoding="utf-8")))
    want = {name_key(r["name"]) for r in ev}
    trainers = {person_key(r["trainer"]) for r in ev}
    since = (dt.date.fromisoformat(race_date) - dt.timedelta(days=365)).isoformat()
    runs = defaultdict(list)
    tpos = defaultdict(list)
    for path in sorted(glob.glob(str(REPO / "history" / "*.csv.gz"))):
        with open_text(path) as f:
            for x in csv.DictReader(f):
                d = x.get("date") or ""
                if d >= race_date:
                    continue
                if d >= since:
                    t = person_key(x.get("trainer"))
                    if t in trainers:
                        p = pos_of(x.get("course"))
                        if p:
                            tpos[t].append(p)
                k = name_key(x.get("horse"))
                if k in want:
                    runs[k].append((d, x.get("pos"), to_int(x.get("or")), code_of(x.get("type")), x.get("course")))
    home = {}
    for t, pts in tpos.items():
        if len(pts) >= 20:
            home[t] = (sorted(p[0] for p in pts)[len(pts) // 2], sorted(p[1] for p in pts)[len(pts) // 2])
    out = {}
    for r in ev:
        code = code_of(r.get("discipline"))
        rs = sorted(set(runs.get(name_key(r["name"]), [])), key=lambda x: x[0])
        wins = [x for x in rs if x[1] == "1" and x[2] and x[3] == code]
        h = home.get(person_key(r["trainer"]))
        cp = pos_of(r.get("course_name") or r.get("course_id"))
        out[f"{r['off_time']}|{r['course_id']}|{name_key(r['name'])}"] = {
            "last_win_or": wins[-1][2] if wins else None, "last_win_date": wins[-1][0] if wins else None,
            "best_win_or": max(x[2] for x in wins) if wins else None,
            "travel_km": round(km(h, cp)) if h and cp else None,
        }
    (day / "formcheck.json").write_text(json.dumps(out, indent=0))
    return out


def _card_keys(race_date):
    ev = REPO / "reports" / "racecards" / race_date / "evidence.csv"
    if not ev.exists():
        return set()
    return {f"{r['off_time']}|{r['course_id']}|{name_key(r['name'])}" for r in csv.DictReader(open(ev, encoding="utf-8"))}


def load(race_date):
    """3 Nov fix (Fairyhouse helper review): the file was built once (1 Nov, for the Early Bird pack) and never rebuilt, so
    the race-day cards read keys from the 2-days-before card (off times shifted). Rebuild whenever under 90% of the current
    card's runners are in the cached file."""
    p = REPO / "reports" / "racecards" / race_date / "formcheck.json"
    if p.exists():
        cached = json.loads(p.read_text())
        want = _card_keys(race_date)
        if not want or len(want & set(cached)) >= 0.9 * len(want):
            return cached
    try:
        return build(race_date)
    except FileNotFoundError:
        return json.loads(p.read_text()) if p.exists() else {}


def _wr(s):
    m = re.match(r"(\d+)-(\d+)", s or "")
    return (int(m.group(1)), int(m.group(2))) if m else None


def _sr(s):
    m = re.match(r"(\d+)/(\d+) \((\d+)%\)", s or "")
    return (int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None


def items(row, pick, fc):
    """[(label, text, mark)] mark = '+' supportive, '-' against, '' neutral/unknown. Only facts from our records."""
    out = []
    going = (row.get("going") or "").lower()
    for label, f, what in (("Ground", "rp_horse_going", f"on {going}" if going else "on this going"),
                           ("Trip", "rp_horse_distance", "at this trip"), ("Course", "rp_horse_course", "at this course")):
        v = _wr(row.get(f))
        if not v or not v[1]:
            out.append((label, f"never run {what}" if v else f"no record {what}", ""))
        else:
            out.append((label, f"won {v[0]} of {v[1]} {what}", "+" if v[0] else "-" if v[1] >= 3 else ""))
    o = to_int(row.get("ofr"))
    if pick.get("handicap") and o:
        bits = [f"rated {o}"]
        mark = ""
        b = to_int(row.get("best_rpr"))
        if b:
            gap = b - o
            bits.append(f"best RPR {b} ({abs(gap)}lb {'above' if gap >= 0 else 'below'} the mark)")
            mark = "+" if gap >= 3 else "-" if gap < -2 else ""
        lw = (fc or {}).get("last_win_or")
        if lw:
            diff = o - lw
            bits.append(f"last won off {lw} ({'same mark' if diff == 0 else str(abs(diff)) + 'lb ' + ('higher' if diff > 0 else 'lower') + ' today'})")
            mark = "+" if diff <= 0 and mark != "-" else ("-" if diff >= 7 else mark)
        else:
            bits.append("no win off a mark in our records")
        out.append(("Mark", ", ".join(bits), mark))
    for label, f14, fc5 in (("Trainer", "rp_trainer_14d", "trainer_course_5y"), ("Jockey", "rp_jockey_14d", "jockey_course_5y")):
        a, c = _sr(row.get(f14)), _sr(row.get(fc5))
        txt, mark = [], ""
        if a and a[1]:
            txt.append(f"{a[0]}/{a[1]} ({a[2]}%) last 14 days")
            mark = "+" if a[1] >= 8 and a[2] >= 18 else "-" if a[1] >= 8 and a[2] < 6 else ""
        if c and c[1]:
            txt.append(f"{c[0]}/{c[1]} ({c[2]}%) here in 5 years")
        out.append((label, "; ".join(txt) or "no recent record", mark))
    d = days_since(row.get("last_run"))
    out.append(("Days off", f"{d} days" if d is not None else "debut / unknown", "-" if d is not None and d >= 90 else ""))
    t = (fc or {}).get("travel_km")
    if t is not None:
        out.append(("Travel", f"about {t} km (estimated from where the trainer usually runs)", ""))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    a = ap.parse_args(argv)
    out = build(a.date)
    print(f"{len(out)} runners; last winning mark {sum(1 for v in out.values() if v['last_win_or'])}, "
          f"travel {sum(1 for v in out.values() if v['travel_km'] is not None)}")


if __name__ == "__main__":
    main()
