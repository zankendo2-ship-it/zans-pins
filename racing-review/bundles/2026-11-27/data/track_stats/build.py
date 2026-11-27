"""Build draw-bias and pace-bias tables for every UK & Irish course / code / distance / going.

Usage:
    python -m track_stats.build --results data/results_uki.csv.gz --out reports/track_stats

Metrics (per group of runners):
    runners, winners, win_pct
    iv   Impact Value = share of winners / share of runners (1.0 = neutral, >1 = favoured)
    prb  Percentage of Rivals Beaten, averaged (0.5 = neutral). Uses every runner, not just
         winners, so it is far more stable than win% on small samples.
"""
import argparse
import csv
import gzip
import json
import sys
from collections import defaultdict
from pathlib import Path

from .parse import (STYLE_NAMES, course_key, discipline, dist_to_furlongs, furlongs_label,
                    going_group, race_code, running_style)

REPO_ROOT = Path(__file__).resolve().parent.parent
COURSES_FILE = REPO_ROOT / "config" / "courses.json"

MIN_FIELD_DRAW = 6          # draw analysis ignores smaller fields
MIN_STYLED_SHARE = 0.6      # pace analysis needs most of the field classified
DRAW_BANDS = ("LOW", "MIDDLE", "HIGH")


# ============================================================
# LOADING
# ============================================================

def load_courses():
    return json.loads(COURSES_FILE.read_text(encoding="utf-8"))["courses"]


def to_int(value):
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def load_races(path, courses, unmatched):
    """Yield (race_key, runners) for UK/IRE races with a known course and code."""
    races = defaultdict(list)
    meta = {}
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            cid, is_aw = course_key(row["course"])
            code = race_code(row["type"], is_aw)
            if code is None:
                continue
            if cid not in courses:
                unmatched[row["course"]] += 1
                continue
            course = courses[cid]
            if code not in course["codes"]:
                continue
            since = course.get("surface_since", {}).get(code)
            if since and row["date"] < since:
                continue
            furlongs = dist_to_furlongs(row["dist"])
            if furlongs is None:
                continue
            race_id = row["race_id"]
            races[race_id].append(row)
            meta[race_id] = (cid, code, discipline(row["type"], is_aw), furlongs,
                             going_group(row["going"]), row["date"])
    for race_id, runners in races.items():
        yield meta[race_id], runners


# ============================================================
# PER-RACE FEATURES
# ============================================================

def race_features(runners):
    """Return per-runner dicts with won, prb, draw_band, style (None where unknown)."""
    field = len(runners)
    if field < 2:
        return []
    out = []
    for r in runners:
        pos = to_int(r["pos"])
        finished = pos is not None and 1 <= pos <= field
        place = pos if finished else field  # non-finishers beat nobody
        out.append({
            "won": 1 if place == 1 else 0,
            "prb": (field - place) / (field - 1),
            "draw": to_int(r["draw"]),
            "style": running_style(r["comment"]),
        })

    drawn = sorted((x for x in out if x["draw"] is not None), key=lambda x: x["draw"])
    if len(drawn) == field and field >= MIN_FIELD_DRAW:
        for rank, x in enumerate(drawn):
            frac = rank / (field - 1)
            x["draw_band"] = "LOW" if frac < 1 / 3 else ("HIGH" if frac > 2 / 3 else "MIDDLE")
    styled = sum(1 for x in out if x["style"] is not None)
    if styled / field < MIN_STYLED_SHARE:
        for x in out:
            x["style"] = None
    return out


# ============================================================
# AGGREGATION
# ============================================================

def new_bucket():
    return {"runners": 0, "winners": 0, "prb_sum": 0.0}


def summarise(buckets, labels, races):
    total_runners = sum(buckets[b]["runners"] for b in labels)
    total_winners = sum(buckets[b]["winners"] for b in labels)
    row = {"races": races, "runners": total_runners}
    for label in labels:
        b = buckets[label]
        name = label.lower()
        row[f"{name}_runners"] = b["runners"]
        row[f"{name}_win_pct"] = round(100 * b["winners"] / b["runners"], 1) if b["runners"] else ""
        share_w = b["winners"] / total_winners if total_winners else 0
        share_r = b["runners"] / total_runners if total_runners else 0
        row[f"{name}_iv"] = round(share_w / share_r, 2) if share_r else ""
        row[f"{name}_prb"] = round(b["prb_sum"] / b["runners"], 3) if b["runners"] else ""
    return row


def confidence(races):
    return "HIGH" if races >= 150 else "MEDIUM" if races >= 60 else "LOW" if races >= 25 else "TOO_FEW"


def draw_verdict(row):
    if confidence(row["races"]) == "TOO_FEW":
        return "Not enough races"
    low, high = row.get("low_prb"), row.get("high_prb")
    if low == "" or high == "":
        return "Not enough races"
    gap = low - high
    if abs(gap) < 0.04:
        return "No meaningful draw bias"
    side = "LOW" if gap > 0 else "HIGH"
    strength = "Strong" if abs(gap) >= 0.10 else "Clear" if abs(gap) >= 0.06 else "Slight"
    return f"{strength} {side} draw advantage"


def distance_band(disc, furlongs):
    """Distance bands for comparing a course with the national picture."""
    if disc not in ("FLAT", "AW_FLAT"):
        return "2m" if furlongs <= 17.5 else "2m4f" if furlongs <= 22.5 else "3m+"
    return ("sprint" if furlongs <= 6.5 else "mile" if furlongs <= 9
            else "middle" if furlongs <= 13 else "staying")


def pace_verdict(row):
    """Judge pace bias against the national average for the same code / band / going.

    Hurdles, chases and bumpers each have their own baseline: leaders fare very
    differently over fences than over hurdles.
    Comments are written after the race, so leaders always show IV > 1 (typically ~2);
    only the ratio to the national baseline says whether *this track* suits them.
    """
    if confidence(row["races"]) == "TOO_FEW":
        return "Not enough races"
    led = row.get("led_vs_avg")
    held = row.get("held_up_vs_avg")
    if led in ("", None):
        return "Not enough races"
    if held in ("", None):  # no held-up winners anywhere in the band: judge on leaders only
        held = 1.0
    if led >= 1.30:
        return "Front-runners strongly favoured (vs national average)"
    if led >= 1.12:
        return "Front-runners favoured (vs national average)"
    if held >= 1.25 and led <= 0.95:
        return "Hold-up horses favoured — leaders struggle (vs national average)"
    if held >= 1.12 or led <= 0.88:
        return "Leans towards hold-up horses (vs national average)"
    return "Typical — no track-specific pace bias"


def build(results_path, out_dir):
    courses = load_courses()
    unmatched = defaultdict(int)

    draw = defaultdict(lambda: {b: new_bucket() for b in DRAW_BANDS})
    draw_races = defaultdict(int)
    pace = defaultdict(lambda: {s: new_bucket() for s in STYLE_NAMES.values()})
    pace_races = defaultdict(int)
    first_date, last_date = "9999", "0000"

    races = load_races(results_path, courses, unmatched)
    for (cid, code, disc, furlongs, going, date), runners in races:
        first_date, last_date = min(first_date, date), max(last_date, date)
        feats = race_features(runners)
        dist = furlongs_label(furlongs)
        for going_key in (going, "ALL"):
            key = (cid, code, disc, dist, furlongs, going_key)
            if disc in ("FLAT", "AW_FLAT") and all("draw_band" in f for f in feats) and feats:
                draw_races[key] += 1
                for f in feats:
                    b = draw[key][f["draw_band"]]
                    b["runners"] += 1
                    b["winners"] += f["won"]
                    b["prb_sum"] += f["prb"]
            if feats and any(f["style"] for f in feats):
                pace_races[key] += 1
                for f in feats:
                    if f["style"] is None:
                        continue
                    b = pace[key][STYLE_NAMES[f["style"]]]
                    b["runners"] += 1
                    b["winners"] += f["won"]
                    b["prb_sum"] += f["prb"]

    def rows(table, race_counts, labels, verdict):
        out = []
        for key in sorted(table, key=lambda k: (k[0], k[1], k[2], k[4], k[5])):
            cid, code, disc, dist, furlongs, going_key = key
            row = {"course_id": cid, "course_name": courses[cid]["course_name"],
                   "race_code": code, "discipline": disc, "distance": dist,
                   "furlongs": furlongs, "going": going_key}
            row.update(summarise(table[key], labels, race_counts[key]))
            row["confidence"] = confidence(row["races"])
            row["verdict"] = verdict(row)
            if row["confidence"] == "LOW" and row["verdict"] != "Not enough races":
                row["verdict"] += " (small sample — treat with caution)"
            out.append(row)
        return out

    # National baseline per (discipline, band, going): pooled share of winners / runners.
    baseline = defaultdict(lambda: {s: new_bucket() for s in STYLE_NAMES.values()})
    for (cid, code, disc, dist, furlongs, going_key), buckets in pace.items():
        base = baseline[(disc, distance_band(disc, furlongs), going_key)]
        for style, b in buckets.items():
            for field in b:
                base[style][field] += b[field]
    baseline_iv = {k: summarise(v, list(STYLE_NAMES.values()), 0) for k, v in baseline.items()}

    def pace_verdict_with_baseline(row):
        band = distance_band(row["discipline"], row["furlongs"])
        base = baseline_iv[(row["discipline"], band, row["going"])]
        row["band"] = band
        for style in ("led", "held_up"):
            iv, avg = row.get(f"{style}_iv"), base.get(f"{style}_iv")
            row[f"{style}_iv_national"] = avg
            row[f"{style}_vs_avg"] = round(iv / avg, 2) if iv not in ("", None) and avg else ""
        return pace_verdict(row)

    draw_rows = rows(draw, draw_races, DRAW_BANDS, draw_verdict)
    pace_rows = rows(pace, pace_races, list(STYLE_NAMES.values()), pace_verdict_with_baseline)

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(out_dir / "draw_bias.csv", draw_rows)
    write_csv(out_dir / "pace_bias.csv", pace_rows)
    meta = {
        "results_file": str(results_path),
        "first_date": first_date,
        "last_date": last_date,
        "draw_groups": len(draw_rows),
        "pace_groups": len(pace_rows),
        "unmatched_courses": dict(sorted(unmatched.items(), key=lambda x: -x[1])),
    }
    (out_dir / "build_info.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return meta


def write_csv(path, rows):
    fields = []
    for row in rows:
        fields.extend(k for k in row if k not in fields)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Build draw & pace bias tables.")
    parser.add_argument("--results", required=True, help="results_uki.csv.gz extract")
    parser.add_argument("--out", default=str(REPO_ROOT / "reports" / "track_stats"))
    args = parser.parse_args(argv)
    meta = build(args.results, args.out)
    print(json.dumps({k: v for k, v in meta.items() if k != "unmatched_courses"}, indent=2))
    if meta["unmatched_courses"]:
        top = list(meta["unmatched_courses"].items())[:15]
        print(f"Unmatched course names ({len(meta['unmatched_courses'])}, overseas/closed "
              f"courses are expected; top 15):", dict(top))
    return 0


if __name__ == "__main__":
    sys.exit(main())
