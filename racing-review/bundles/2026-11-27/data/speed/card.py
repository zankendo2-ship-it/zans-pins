"""Speed figures + pace map for every runner on a race day.

For each runner (from runners.csv) it looks up the horse's past runs in our results and adds:
  speed   (flat and jumps figures kept apart - different scales)
          last figure (+ date, course), best and average of the last 3, best in the last 12
          months, best at a similar trip in the same code, the last 6 figures, and the
          horse's rank in today's race (by best of last 3)
  pace    usual early position (LEADER / PROMINENT / MIDFIELD / HOLD_UP / UNKNOWN), how often
          it led, the race's projected pace (SLOW / LONE_LEADER / EVEN / STRONG) and whether
          that suits this horse
It also notes how the ground rode at the last meeting at each of today's courses (going
allowance). Missing figures are NEUTRAL gaps, never zeros. Only runs BEFORE the race day
are used.

Output: reports/racecards/<date>/speed_pace.csv, speed_pace.json and speed_pace.md
Usage:
    python -m speed.card --date 2026-09-24 --history history/*.csv.gz
"""
import argparse
import csv
import json
import sys
from collections import defaultdict
from datetime import date as Date
from pathlib import Path

from form.history import family, name_key
from track_stats.parse import dist_to_furlongs, running_style

from .figures import JUMPS, SpeedModel, describe_going, load_races
from .pacemap import fit, race_scenario, runner_role, scenario_text

REPO_ROOT = Path(__file__).resolve().parent.parent
FIELDS = ["date", "course_id", "off_time", "race_id", "name", "horse_id", "speed_status",
          "speed_last", "speed_last_date", "speed_last_course", "speed_best3", "speed_avg3",
          "speed_best_12m", "speed_best_similar_trip", "speed_figs_last6", "speed_rank",
          "speed_top_gap", "pace_role", "pace_led_share", "pace_runs_read",
          "race_pace_scenario", "race_pace_text", "pace_map_fit"]
SIMILAR_TRIP_F = 1.0


def read_csv(path):
    with open(path, encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def code_group(disc):
    """Flat (turf + all-weather) and jumps figures sit on different scales: never mix them."""
    return "JUMPS" if disc in JUMPS else "FLAT"


def speed_fields(runs, card, race_date):
    group = code_group(card.get("discipline"))
    runs = [r for r in runs if code_group(r["disc"]) == group]
    figs = [r for r in runs if r["fig"] is not None]
    if not figs:
        why = ("no previous runs" if group == "FLAT" else "no previous jumps runs") if not runs \
            else "no timed runs within 30 lengths"
        return {"speed_status": f"NEUTRAL_GAP: {why}"}
    year_ago = Date.fromisoformat(race_date).toordinal() - 365
    last3 = [r["fig"] for r in figs[-3:]]
    today_f = dist_to_furlongs(card.get("distance_label"))
    fam = family(card.get("discipline"))
    similar = [r["fig"] for r in figs if family(r["disc"]) == fam and today_f
               and abs(r["furlongs"] - today_f) <= SIMILAR_TRIP_F]
    recent = [r["fig"] for r in figs if Date.fromisoformat(r["date"]).toordinal() >= year_ago]
    last = figs[-1]
    return {"speed_status": "AVAILABLE", "speed_last": last["fig"],
            "speed_last_date": last["date"], "speed_last_course": last["course"],
            "speed_best3": max(last3), "speed_avg3": round(sum(last3) / len(last3)),
            "speed_best_12m": max(recent) if recent else "",
            "speed_best_similar_trip": max(similar) if similar else "",
            "speed_figs_last6": " ".join("-" if r["fig"] is None else str(r["fig"])
                                         for r in reversed(runs[-6:]))}


def last_going(model, course_ids):
    """Latest meeting going allowance at each of today's courses, per code family."""
    out = {}
    for (day, cid, fam) in model.going:
        ga = model.ground_vs_good((day, cid, fam))
        if cid in course_ids and ((cid, fam) not in out or day > out[(cid, fam)][0]):
            out[(cid, fam)] = (day, ga)
    return out


def build(race_date, cards, history_paths):
    cards = [c for c in cards if str(c.get("reserve")) not in ("True", "true", "1")]
    horses = {name_key(c["name"]) for c in cards}
    races = load_races(history_paths, keep_horses=horses, before=race_date)
    model = SpeedModel(races)
    runs = model.horse_runs()
    rows, by_race = [], defaultdict(list)
    for card in cards:
        horse_runs = runs.get(name_key(card["name"]), [])
        row = {k: card.get(k, "") for k in FIELDS[:6]}
        row["_disc"] = card.get("discipline")
        row.update(speed_fields(horse_runs, card, race_date))
        role, led, read = runner_role([running_style(r["comment"]) for r in horse_runs])
        row.update(pace_role=role, pace_led_share=led if read >= 2 else "", pace_runs_read=read)
        rows.append(row)
        by_race[card["race_id"]].append(row)
    for race_rows in by_race.values():
        scenario, leaders = race_scenario({r["name"]: r["pace_role"] for r in race_rows})
        text = scenario_text(scenario, leaders)
        rated = sorted((r["speed_best3"] for r in race_rows if r.get("speed_best3") != ""
                        and r.get("speed_best3") is not None), reverse=True)
        for r in race_rows:
            r.update(race_pace_scenario=scenario, race_pace_text=text,
                     pace_map_fit=fit(scenario, r["pace_role"], r.get("_disc")))
            if r.get("speed_best3") not in ("", None):
                r["speed_rank"] = rated.index(r["speed_best3"]) + 1
                r["speed_top_gap"] = r["speed_best3"] - rated[0]
    going = last_going(model, {c["course_id"] for c in cards})
    summary = {"date": race_date, "runners": len(rows),
               "with_speed_figure": sum(r["speed_status"] == "AVAILABLE" for r in rows),
               "with_pace_role": sum(r["pace_role"] != "UNKNOWN" for r in rows),
               "standards": len(model.standards),
               "last_going_allowance": {f"{cid} {fam}": {"date": d, "allowance_s_per_f": round(ga, 2),
                                                          "races_run": describe_going(ga)}
                                        for (cid, fam), (d, ga) in sorted(going.items())},
               "rule": "Evidence only; missing figures are neutral, never zero."}
    return rows, summary, going


def render_md(race_date, cards, rows, going):
    card_by_horse = {c["horse_id"]: c for c in cards}
    lines = [f"# Speed figures + pace map — {race_date}", "",
             "Speed figure = our own time-based rating in pounds (same scale as official "
             "ratings). Best3 = best of the last 3 runs. Figures newest first. "
             "Pace role from each horse's last 6 in-running comments.", ""]
    races = defaultdict(list)
    for r in rows:
        races[(r["course_id"], r["off_time"], r["race_id"])].append(r)
    for (cid, off, _), race_rows in sorted(races.items()):
        first = card_by_horse.get(race_rows[0]["horse_id"], {})
        fam = family(first.get("discipline"))
        lines += [f"## {first.get('course_name', cid)} {off} — {first.get('distance_label', '')} "
                  f"{first.get('discipline', '')}, {first.get('going', '')}", ""]
        if (cid, fam) in going:
            d, ga = going[(cid, fam)]
            lines.append(f"Last meeting here ({d}): races were run {describe_going(ga)}.")
        lines += [f"**Pace:** {race_rows[0]['race_pace_text']}", "",
                  "| Horse | Speed best3 | Rank | Last 6 figs | Similar trip | Pace role | Pace fit |",
                  "|---|---|---|---|---|---|---|"]
        for r in sorted(race_rows, key=lambda x: (x.get("speed_rank") or 99, x["name"])):
            lines.append(f"| {r['name']} | {r.get('speed_best3', '') or '-'} | "
                         f"{r.get('speed_rank', '') or '-'} | {r.get('speed_figs_last6', '') or '-'} | "
                         f"{r.get('speed_best_similar_trip', '') or '-'} | {r['pace_role']} | "
                         f"{r['pace_map_fit']} |")
        lines.append("")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Speed figures + pace map for a race day.")
    parser.add_argument("--date", required=True)
    parser.add_argument("--history", nargs="*", default=[])
    parser.add_argument("--cards-dir", default=str(REPO_ROOT / "reports" / "racecards"))
    args = parser.parse_args(argv)
    out = Path(args.cards_dir) / args.date
    if not (out / "runners.csv").exists() or not args.history:
        print(f"::warning::No runner list or history for {args.date}; speed/pace skipped")
        return 0
    cards = read_csv(out / "runners.csv")
    rows, summary, going = build(args.date, cards, args.history)
    with open(out / "speed_pace.csv", "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    (out / "speed_pace.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    (out / "speed_pace.md").write_text(render_md(args.date, cards, rows, going), encoding="utf-8")
    print(f"Speed figures for {summary['with_speed_figure']}/{summary['runners']} runners, "
          f"pace roles for {summary['with_pace_role']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
