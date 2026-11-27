"""Read the built draw/pace tables and render them for a course's track DNA report."""
import csv
from functools import lru_cache
from pathlib import Path

from .parse import DISCIPLINE_NAMES, JUMPS_DISCIPLINES, going_group

REPO_ROOT = Path(__file__).resolve().parent.parent
STATS_DIR = REPO_ROOT / "reports" / "track_stats"


@lru_cache(maxsize=4)
def _load(stats_dir):
    tables = {}
    for name in ("draw_bias", "pace_bias", "weight_bias", "draw_field_bias"):
        path = Path(stats_dir) / f"{name}.csv"
        rows = list(csv.DictReader(path.open(encoding="utf-8"))) if path.exists() else []
        # Tables built before the jumps split have no discipline column.
        tables[name] = {(r["course_id"], r.get("discipline") or r["race_code"], r["distance"],
                         r["going"]) + ((r["field_size"],) if name == "draw_field_bias" else ()): r
                        for r in rows}
    return tables


def disciplines_for(race_code):
    """A jumps meeting is reported as hurdles, chases and bumpers separately."""
    return JUMPS_DISCIPLINES if race_code == "JUMPS" else (race_code,)


def course_stats(course_id, disc, official_going="", stats_dir=STATS_DIR):
    """Rows per distance for one discipline: overall plus today's going group."""
    tables = _load(str(stats_dir))
    today = going_group(str(official_going).replace("_", " "))
    distances = sorted(
        {(float(r["furlongs"]), r["distance"]) for (c, d, _, g), r in tables["pace_bias"].items()
         if c == course_id and d == disc and g == "ALL"})
    out = []
    for _, dist in distances:
        entry = {"distance": dist}
        for going in ("ALL", today):
            draw = tables["draw_bias"].get((course_id, disc, dist, going))
            pace = tables["pace_bias"].get((course_id, disc, dist, going))
            weight = tables["weight_bias"].get((course_id, disc, dist, going))
            fields = {fb: tables["draw_field_bias"].get((course_id, disc, dist, going, fb))
                      for fb in ("6-9", "10-13", "14+")}
            entry[going] = {"draw": draw, "pace": pace, "weight": weight, "draw_field": fields}
        entry["today_going"] = today
        out.append(entry)
    return out


def _draw_text(row):
    if not row:
        return "—"
    if row["verdict"] == "Not enough races":
        return f"Not enough races ({row['races']})"
    return (f"{row['verdict']} (rivals beaten: low {row['low_prb']}, mid {row['middle_prb']}, "
            f"high {row['high_prb']}; {row['races']} races)")


def _pace_text(row):
    if not row:
        return "—"
    if row["verdict"] == "Not enough races":
        return f"Not enough races ({row['races']})"
    return (f"{row['verdict']} (leaders win {row['led_vs_avg']}× the national rate; "
            f"hold-ups {row['held_up_vs_avg'] or '—'}×; {row['races']} races)")


def render_markdown(course_id, race_code, official_going="", stats_dir=STATS_DIR):
    lines = ["## Hard numbers — draw & pace from historic results", "",
             "Draw: average share of rivals beaten by stall third (0.5 = neutral), also split "
             "by field size. Pace: how often leaders / hold-up horses win compared with the "
             "UK & Ireland average for the same race type and trip. Weight (handicaps): "
             "top weights vs low weights here, compared with nationally.", ""]
    found = False
    for disc in disciplines_for(race_code):
        stats = course_stats(course_id, disc, official_going, stats_dir)
        section = _render_discipline(stats, disc)
        if section:
            found = True
            lines += [f"### {DISCIPLINE_NAMES[disc]}", ""] + section
    if not found:
        lines.append("_No historic results for this course and code._")
    return "\n".join(lines)


def _render_discipline(stats, disc):
    lines = []
    for entry in stats:
        overall = entry["ALL"]
        if all(not r or r["verdict"] == "Not enough races"
               for r in (overall["draw"], overall["pace"])):
            continue  # rarely-run trip: nothing trustworthy to say
        lines.append(f"#### {entry['distance']}")
        goings = [("ALL", "all going")]
        today = entry.get(entry["today_going"]) or {}
        same_as_all = all((today.get(k) or {}).get("races") == (overall[k] or {}).get("races")
                          for k in ("draw", "pace"))
        if entry["today_going"] not in ("ALL", "OTHER") and not same_as_all:
            goings.append((entry["today_going"], f"today's going ({entry['today_going'].lower()})"))
        for going, label in goings:
            cell = entry[going]
            if disc in ("FLAT", "AW_FLAT"):
                lines.append(f"- **Draw, {label}**: {_draw_text(cell['draw'])}")
            lines.append(f"- **Pace, {label}**: {_pace_text(cell['pace'])}")
            if disc in ("FLAT", "AW_FLAT"):
                by_field = [f"{fb} runners: {r['verdict']} ({r['races']})"
                            for fb, r in (cell.get("draw_field") or {}).items()
                            if r and r["verdict"] != "Not enough races"]
                if by_field:
                    lines.append(f"- **Draw by field size, {label}**: " + "; ".join(by_field))
            w = cell.get("weight")
            if w and w["verdict"] != "Not enough races":
                lines.append(f"- **Weight (handicaps), {label}**: {w['verdict']} "
                             f"(top weights beat {w['top_prb']} of rivals, low weights "
                             f"{w['low_prb'] or '—'}; {w['races']} handicaps)")
        lines.append("")
    return lines
