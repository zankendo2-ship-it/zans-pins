"""DATA PICK reasons (owner 4 Nov 2026: "I need 3-4 reasons why every data pick was selected at the bottom of the
racecard and a confidence bar in red and green like the win selection, based on historical data, stats, ground
conditions etc. Everything taken into consideration ... The files then need uploading to GitHub so other chats can
access them ... Do this every time going forward").

For every race of the day: the Data pick (price-free model x course method, predict/course_method.data_pick), its
confidence out of 10, and 3-4 reasons. Every reason is a checked fact from our own records, strongest first:
  1. youtube.short.reasons - the horse's own runs from history/*.csv.gz (handicap mark, recent form, ground, trip,
     course, class, pace, trainer/jockey form and course records, headgear, quick return, ZANS speed figures);
     price-based reasons ("backed from ...") are dropped - the Data pick ignores the price.
  2. the course method angles that apply to the horse (each tested on history, A/E written in plain English);
  3. evidence-pack facts (RPR rank in the field, draw / pace / weight fit, ZANS speed rank, trainer/jockey records);
  4. our model's price-free chance for the horse.
Cautions (course-method penalty rules) are listed separately as 'Watch out'. Nothing is invented: a race whose horse has
fewer than 3 checkable facts shows only what we have.

    python -m predict.data_reasons --date 2026-11-04     -> reports/predictions/<D>/data_picks.{json,md}

predict.cards calls get(race_date) and draws the panel at the bottom of each race; the json is rebuilt automatically
when the day's Data picks change (cache keyed on the picks).
"""
import argparse
import csv
import hashlib
import json
import os
import re
from pathlib import Path

from form.history import name_key

REPO = Path(__file__).resolve().parent.parent
MAX_REASONS = 4
PRICE_WORDS = ("backed from", "money talks", "in the betting", "price")


def _pdir(race_date):
    return REPO / "reports" / "predictions" / race_date


def _picks(race_date):
    """[(course, pick dict)] from every <course>_method.json of the day."""
    out = []
    for f in sorted(_pdir(race_date).glob("*_method.json")):
        course = f.name[:-len("_method.json")]
        try:
            rows = json.loads(f.read_text())
        except ValueError:
            continue
        if isinstance(rows, list):
            out += [(course, p) for p in rows if isinstance(p, dict) and p.get("data_pick")]
    return out


def _key(picks):
    raw = json.dumps(sorted((c, p["time"], p["data_pick"], p.get("data_conf")) for c, p in picks))
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def _ae_text(txt):
    """'top recent RPR: Musselburgh A/E 1.10 (885; 1.08 / 1.11)' -> plain English."""
    m = re.match(r"(.+?):\s*(.*?)A/E ([\d.]+)(?:[^(]*)\(([\d,]+)", txt)
    if not m:
        return txt
    what, where, ae, n = m.group(1).strip(), m.group(2).strip().rstrip(","), float(m.group(3)), m.group(4)
    pct = round((ae - 1) * 100)
    where = where or "UK/IRE"
    names = {"top recent RPR": "Top-rated in the field on recent Racing Post Ratings",
             "top recent RPR (best of last 3)": "Top-rated in the field on its best Racing Post Rating of the last 3 runs",
             "top exact-conditions RPR": "Best rating in the field on exactly today's ground over this trip",
             "top exact-conditions RPR (owner HR12)": "Best rating in the field on exactly today's ground over this trip",
             "improver (last RPR a new best)": "Improving: its last run was a career-best rating",
             "won last time": "Won last time out", "lone front-runner": "The only front-runner in the race",
             "usually races prominent": "Races close to the pace",
             "one of only 1-2 winners on this exact going": "One of only 1-2 runners to have won on this exact going",
             "never run within 1f of this trip": "Trying a new trip", "age 6+": "Aged 6 or older",
             "won last time (over-bet here)": "Won last time - over-bet here", "usually held up": "Usually held up"}
    lead = names.get(what, what[:1].upper() + what[1:])
    if pct > 0:
        return f"{lead} - at {where} horses like this win {pct}% more often than their price suggests ({n} runners in our history)"
    if pct < 0:
        return f"{lead} - at {where} horses like this win {-pct}% less often than their price suggests ({n} runners in our history)"
    return f"{lead} ({where}, {n} runners in our history)"


def _ev_facts(ev, race_ev, name):
    """Supporting facts from the frozen evidence pack (only ones that favour the horse)."""
    out = []

    def num(v):
        try:
            return float(v)
        except (TypeError, ValueError):
            return None
    for col, label in (("best_rpr", "best Racing Post Rating"), ("last_rpr", "last-time-out rating")):
        vals = sorted({num(r.get(col)) for r in race_ev if num(r.get(col))}, reverse=True)
        me = num(ev.get(col))
        if me and vals:
            rank = vals.index(me) + 1
            if rank <= 2:
                out.append((6 if rank == 1 else 4, f"{'Highest' if rank == 1 else '2nd-highest'} {label} in the field ({int(me)})"))
                break
    if str(ev.get("pace_fit")) == "SUITS" or str(ev.get("pace_map_fit")) == "SUITS":
        out.append((5, f"Run style suits the way this race should be run ({(ev.get('race_pace_text') or ev.get('pace_verdict') or '').strip()})"))
    dv = str(ev.get("draw_verdict") or "")
    if dv and any(w in dv.lower() for w in ("favour", "good", "advantage", "best")) and "not" not in dv.lower():
        out.append((5, f"Drawn {ev.get('draw')} - {dv.lower()} at this course and trip"))
    if str(ev.get("speed_rank")) in ("1", "2") and ev.get("speed_best3"):
        out.append((5, f"{'Fastest' if str(ev.get('speed_rank')) == '1' else '2nd-fastest'} in the field on ZANS time figures (best of last 3: {ev['speed_best3']})"))
    for col, who in (("trainer_course_5y", ev.get("trainer")), ("jockey_course_5y", ev.get("jockey"))):
        m = re.match(r"(\d+)/(\d+) \((\d+)%\)", str(ev.get(col) or ""))
        if m and int(m.group(2)) >= 20 and int(m.group(3)) >= 15:
            out.append((4, f"{who} has {m.group(1)} winners from {m.group(2)} runners at this course in 5 years ({m.group(3)}%)"))
    for col, label in (("rp_horse_going", "on this ground"), ("rp_horse_distance", "over this trip"), ("rp_horse_course", "at this course")):
        m = re.match(r"(\d+)-(\d+)", str(ev.get(col) or ""))
        if m and int(m.group(1)) >= 1:
            out.append((5, f"Has won {label}: {m.group(1)} win{'s' if int(m.group(1)) > 1 else ''} from {m.group(2)} runs"))
    return out


def _watch(p, ev):
    """Cautions in plain words: course-method penalty rules (tested on history) + a long layoff."""
    out = []
    for c in p.get("data_cautions") or []:
        m = re.match(r"back from (\d+) days", c)
        if m:
            out.append(f"Back from {m.group(1)} days off")
        elif "no trap in data" not in c:
            out.append(_ae_text(c))
    from form.history import days_since
    d = days_since(ev.get("last_run")) if ev else None
    if d and d >= 90 and not any("days off" in o for o in out):
        out.append(f"Back from {d} days off")
    return out[:2]


def build(race_date):
    picks = _picks(race_date)
    evp = REPO / "reports" / "racecards" / race_date / "evidence_prerace.csv"
    if not evp.exists():
        evp = evp.with_name("evidence.csv")
    ev_rows = list(csv.DictReader(open(evp, encoding="utf-8"))) if evp.exists() else []
    try:
        preds = json.loads((_pdir(race_date) / "predictions.json").read_text())
    except (OSError, ValueError):
        preds = []
    from youtube import short
    from odds.value_report import ck
    short.load_history([p["data_pick"] for _, p in picks])
    out = []
    day_used = set()   # owner 4 Nov rule 5: no reason text repeats across horses on the day
    for course, p in sorted(picks, key=lambda cp: (cp[0], cp[1]["time"])):
        name = p["data_pick"]
        race_ev = [r for r in ev_rows if r["course_id"] == course and r["off_time"] == p["time"]]
        ev = next((r for r in race_ev if name_key(r["name"]) == name_key(name)), {})
        race = next((x for x in preds if x.get("off_time") == p["time"] and ck(x.get("course", "")) == ck(course)), None)
        cname = (ev.get("course_name") or course.replace("_", " ").title())
        facts = []
        if ev:
            try:
                for i, b in enumerate(short.reasons({**p, "win": name}, ev, cname, race, race_date)):
                    if not any(w in b.lower() for w in PRICE_WORDS):
                        facts.append((20 - i, b))
            except Exception as exc:   # one horse's odd record must never stop the cards
                facts.append((0, f"(history reasons unavailable: {type(exc).__name__})"))
            facts += [(s + 0.5, b) for s, b in _ev_facts(ev, race_ev, name)]
        facts += [(6.5, _ae_text(a)) for a in (p.get("data_angles") or [])]
        facts.sort(key=lambda x: -x[0])
        seen, reasons = set(), []
        for _, b in facts:
            k = re.sub(r"[^a-z]", "", b.lower().split(":")[0].split(" - ")[0])[:28]
            if k in seen or b.startswith("("):
                continue
            if re.sub(r"\W", "", b.lower()) in day_used:   # already given for another horse today
                continue
            seen.add(k)
            reasons.append(b)
        day_used.update(re.sub(r"\W", "", b.lower()) for b in reasons[:MAX_REASONS - 1])
        reasons = reasons[:MAX_REASONS - 1] if len(reasons) >= MAX_REASONS else reasons
        reasons.append(f"Our price-free model makes {name} the most likely winner: a {p.get('data_chance', 0):.0%} chance "
                       f"on form, ratings, course, trip, ground and connections (confidence {p.get('data_conf')}/10)")
        out.append({"course": course, "course_name": cname, "time": p["time"], "race": p.get("race"),
                    "distance": p.get("distance"), "going": p.get("going"), "runners": p.get("runners"),
                    "data_pick": name, "data_conf": p.get("data_conf"), "data_chance": p.get("data_chance"),
                    "data_price": p.get("data_price"), "same_as_win_pick": name == p.get("win"), "win_pick": p.get("win"),
                    "win_price": p.get("price"), "win_conf": p.get("confidence"),
                    "win_verdict": "BET" if int(p.get("confidence") or 0) >= 8 else "NO BET",
                    "reasons": reasons[:MAX_REASONS],
                    "watch_out": _watch(p, ev)})
    return out


def write(race_date):
    picks = _picks(race_date)
    rows = build(race_date)
    d = _pdir(race_date)
    (d / "data_picks.json").write_text(json.dumps({"date": race_date, "key": _key(picks), "races": rows}, indent=1))
    md = [f"# ZANS Data picks - {race_date}", "",
          "The Data pick ignores the price: the best horse on our stats, historic results and course data. "
          "Never on the bet slip. Confidence out of 10 on the same scale as the win pick.", ""]
    for r in rows:
        md += [f"## `{r['time']} {r['course_name'].upper()}` - {r['data_pick']} ({r['data_conf']}/10)",
               f"{r.get('race') or ''} · {r.get('distance') or ''} · {r.get('going') or ''} · {r.get('runners')} runners · "
               f"price {r.get('data_price') or 'n/a'} (not used)" + (" · same horse as the win pick" if r["same_as_win_pick"]
                                                                     else f" · win pick: {r['win_pick']}"), ""]
        md += [f"{i}. {b}" for i, b in enumerate(r["reasons"], 1)]
        if r["watch_out"]:
            md += ["", "Watch out: " + "; ".join(r["watch_out"])]
        md.append("")
    (d / "data_picks.md").write_text("\n".join(md))
    if not os.environ.get("ZANS_NO_SHARE"):
        _share(race_date, rows)
    return rows


SHARE = REPO / "reports" / "data_picks"
GITHUB = "https://github.com/zankendo2-ship-it/HORSE-RACING-EXTRACTION-/blob/claude/horse-racing-prediction-setup-a02c7r/"


def _share(race_date, rows):
    """reports/data_picks/<date>.md + README.md index - a fixed GitHub place other Claude chats can read (owner 4 Nov 2026:
    'The files then need uploading to GitHub so other chats can access them ... Do this every time going forward')."""
    from datetime import datetime
    from zoneinfo import ZoneInfo
    from predict.pdfpack import prefix, day_name
    SHARE.mkdir(parents=True, exist_ok=True)
    ver = prefix(race_date).strip() or "Race day"
    made = datetime.now(ZoneInfo("Europe/London")).strftime("%a %d %b %Y %H:%M")
    name0 = f"{prefix(race_date)}{day_name(race_date)}"
    md = [f"# ZANS selections + Data picks - {day_name(race_date)} ({race_date})", "",
          f"Version: **{ver}** · made {made} (UK time). UK & Irish racing only. Decimal odds.",
          "Win pick = our selection (uses the price). Data pick = best horse on stats, historic results and course data, "
          "price ignored, never on the bet slip. Confidence out of 10: 8 = green BET level, 9-10 = gold, 7 and below = red.",
          f"Course card PDFs: reports/pdf/{name0} <Course>.pdf in this repo.", ""]
    for r in rows:
        md += [f"## `{r['time']} {r['course_name'].upper()}` {r.get('race') or ''}",
               f"{r.get('distance') or ''} · {r.get('going') or ''} · {r.get('runners')} runners", "",
               f"- **Win pick:** {r['win_pick']} {('- ' + str(r.get('win_price'))) if r.get('win_price') else ''} "
               f"({r.get('win_conf')}/10, {r.get('win_verdict') or ''})",
               f"- **Data pick:** {r['data_pick']} ({r['data_conf']}/10)" + (" - same horse" if r["same_as_win_pick"] else ""), ""]
        md += [f"  {i}. {b}" for i, b in enumerate(r["reasons"], 1)]
        if r["watch_out"]:
            md += ["", "  Watch out: " + "; ".join(r["watch_out"])]
        md.append("")
    md += ["18+ | Please gamble responsibly | BeGambleAware.org | Not financial advice."]
    (SHARE / f"{race_date}.md").write_text("\n".join(md))
    days = sorted((f.stem for f in SHARE.glob("20*.md")), reverse=True)
    idx = ["# ZANS daily selections + Data picks - index", "",
           "One file per race day (the race-day version replaces the Early ones on the same date). Newest first.",
           "Each race: win pick, Data pick (price ignored) with confidence /10 and 3-4 reasons from our historic data.",
           "INTERNAL: reasons can quote Racing Post ratings - not for public posts (public posts use reports/public/).", ""]
    idx += [f"- [{x}]({x}.md) - {GITHUB}reports/data_picks/{x}.md" for x in days]
    (SHARE / "README.md").write_text("\n".join(idx) + "\n")


def get(race_date):
    """Data-pick reasons keyed (course, time); rebuilt when the day's Data picks changed."""
    f = _pdir(race_date) / "data_picks.json"
    picks = _picks(race_date)
    try:
        data = json.loads(f.read_text())
        if data.get("key") != _key(picks):
            raise ValueError
        rows = data["races"]
    except (OSError, ValueError, KeyError):
        rows = write(race_date)
    return {(r["course"], r["time"]): r for r in rows}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    a = ap.parse_args(argv)
    rows = write(a.date)
    few = [r for r in rows if len(r["reasons"]) < 3]
    print(f"{a.date}: {len(rows)} Data picks, reasons per race min {min((len(r['reasons']) for r in rows), default=0)}"
          f" (under 3: {len(few)}) -> {_pdir(a.date) / 'data_picks.md'}")


if __name__ == "__main__":
    main()
