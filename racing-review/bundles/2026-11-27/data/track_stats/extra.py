"""Weight DNA and draw-by-field-size DNA (ideas kept from the owner's "historic data pull").

weight_bias.csv       HANDICAPS only. Each runner is banded by how far it is below the
                      race's top weight (TOP 0-2lb, UPPER 3-9lb, MIDDLE 10-16lb, LOW 17lb+).
                      Per course / discipline / trip / going: runners, win %, share of rivals
                      beaten (PRB) and A/E (winners / winners the market expected, SP with
                      the bookmakers' margin removed: 1.00 = exactly as priced)
                      for each band, and a verdict RELATIVE to the national picture for the
                      same discipline, trip band and going (nationally the top weights are
                      the best horses, so only a course that differs from that means anything).
draw_field_bias.csv   FLAT / AW. Draw thirds split by field size (6-9, 10-13, 14+ runners),
                      with PRB and A/E, because a draw bias in big fields can vanish in small ones.

Usage:
    python -m track_stats.extra --uki data/results_uki.csv.gz --form data/results_form.csv.gz \\
        --out reports/track_stats
"""
import argparse
import csv
import gzip
import re
import sys
from collections import defaultdict
from pathlib import Path

from .build import confidence, distance_band, load_courses, to_int, write_csv
from .parse import course_key, discipline, dist_to_furlongs, furlongs_label, going_group, race_code

WEIGHT_BANDS = ("TOP", "UPPER", "MIDDLE", "LOW")
DRAW_BANDS = ("LOW", "MIDDLE", "HIGH")
FIELD_BANDS = ("6-9", "10-13", "14+")
MIN_FIELD = 6


def weight_band(below_top):
    return "TOP" if below_top <= 2 else "UPPER" if below_top <= 9 else \
        "MIDDLE" if below_top <= 16 else "LOW"


def field_band(field):
    return "6-9" if field <= 9 else "10-13" if field <= 13 else "14+"


def lbs(wgt):
    m = re.fullmatch(r"(\d+)-(\d+)", str(wgt or "").strip())
    return int(m.group(1)) * 14 + int(m.group(2)) if m else None


def sp_decimal(sp):
    raw = str(sp or "").strip()
    if raw.lower().startswith("ev"):
        return 2.0
    core = re.sub(r"[A-Za-z]+$", "", raw).strip()
    m = re.fullmatch(r"(\d+)/(\d+)", core)
    if m:
        return int(m.group(1)) / int(m.group(2)) + 1 if int(m.group(2)) else None
    m = re.fullmatch(r"\d+\.\d+", core)  # already decimal (owner shows decimal odds)
    return float(core) if m and float(core) > 1 else None


def new_bucket():
    return {"runners": 0, "winners": 0, "prb": 0.0, "expected": 0.0}


def add(bucket, won, prb, chance):
    bucket["runners"] += 1
    bucket["winners"] += won
    bucket["prb"] += prb
    if chance:
        bucket["expected"] += chance


def summarise(buckets, labels):
    row = {}
    for label in labels:
        b = buckets[label]
        name = label.lower().replace("-", "_").replace("+", "plus")
        row[f"{name}_runners"] = b["runners"]
        row[f"{name}_win_pct"] = round(100 * b["winners"] / b["runners"], 1) if b["runners"] else ""
        row[f"{name}_prb"] = round(b["prb"] / b["runners"], 3) if b["runners"] else ""
        row[f"{name}_ae"] = round(b["winners"] / b["expected"], 2) if b["expected"] else ""
    return row


def grouped_races(path, courses, keep):
    """Yield (meta, rows) per race for known UK/IRE courses (file is sorted by date, race_id)."""
    current, rows = None, []
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["race_id"] != current:
                if rows:
                    yield from _race(rows, courses, keep)
                current, rows = row["race_id"], []
            rows.append(row)
    if rows:
        yield from _race(rows, courses, keep)


def _race(rows, courses, keep):
    first = rows[0]
    cid, is_aw = course_key(first["course"])
    code = race_code(first["type"], is_aw)
    if code is None or cid not in courses or code not in courses[cid]["codes"]:
        return
    since = courses[cid].get("surface_since", {}).get(code)
    if since and first["date"] < since:
        return
    furlongs = dist_to_furlongs(first["dist"])
    if furlongs is None or not keep(first):
        return
    yield (cid, discipline(first["type"], is_aw), furlongs, going_group(first["going"])), rows


def finishers(rows):
    """(row, won, share of rivals beaten, market chance) per runner. The market chance is the
    SP's implied probability with the bookmakers' margin removed (the race's chances add up
    to 1), so an A/E of 1.00 means exactly as the market expected."""
    field = len(rows)
    implied = [1 / d if d else None for d in (sp_decimal(r["sp"]) for r in rows)]
    book = sum(p for p in implied if p) if all(implied) else None
    out = []
    for r, p in zip(rows, implied):
        pos = to_int(r["pos"])
        place = pos if pos is not None and 1 <= pos <= field else field
        out.append((r, 1 if place == 1 else 0, (field - place) / (field - 1),
                    p / book if book else None))
    return out


def build(uki_path, form_path, out_dir):
    courses = load_courses()
    handicaps = set()
    with gzip.open(uki_path, "rt", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row.get("rating_band"):
                handicaps.add(row["race_id"])

    # ---- weight DNA (handicaps, from the form extract which has weights) ----
    weight = defaultdict(lambda: {b: new_bucket() for b in WEIGHT_BANDS})
    weight_races = defaultdict(int)
    national = defaultdict(lambda: {b: new_bucket() for b in WEIGHT_BANDS})
    for (cid, disc, furlongs, going), rows in grouped_races(
            form_path, courses, lambda r: r["race_id"] in handicaps):
        if len(rows) < MIN_FIELD:
            continue
        weights = [lbs(r["wgt"]) for r in rows]
        if None in weights:
            continue
        top = max(weights)
        for going_key in (going, "ALL"):
            key = (cid, disc, furlongs_label(furlongs), furlongs, going_key)
            weight_races[key] += 1
            nat = national[(disc, distance_band(disc, furlongs), going_key)]
            for (r, won, prb, chance), w in zip(finishers(rows), weights):
                band = weight_band(top - w)
                add(weight[key][band], won, prb, chance)
                add(nat[band], won, prb, chance)

    weight_rows = []
    for key in sorted(weight, key=lambda k: (k[0], k[1], k[3], k[4])):
        cid, disc, dist, furlongs, going_key = key
        row = {"course_id": cid, "course_name": courses[cid]["course_name"], "discipline": disc,
               "distance": dist, "furlongs": furlongs, "going": going_key,
               "races": weight_races[key]}
        row.update(summarise(weight[key], WEIGHT_BANDS))
        nat = summarise(national[(disc, distance_band(disc, furlongs), going_key)], WEIGHT_BANDS)
        row["confidence"] = confidence(row["races"])
        row["verdict"] = weight_verdict(row, nat)
        weight_rows.append(row)

    # ---- draw by field size (flat/AW, from the track extract which has draw + SP) ----
    draw = defaultdict(lambda: {b: new_bucket() for b in DRAW_BANDS})
    draw_races = defaultdict(int)
    for (cid, disc, furlongs, going), rows in grouped_races(
            uki_path, courses, lambda r: r["type"].strip().lower() == "flat"):
        field = len(rows)
        draws = [to_int(r["draw"]) for r in rows]
        if field < MIN_FIELD or None in draws:
            continue
        order = {d: i for i, d in enumerate(sorted(draws))}
        for going_key in (going, "ALL"):
            key = (cid, disc, furlongs_label(furlongs), furlongs, going_key, field_band(field))
            draw_races[key] += 1
            for (r, won, prb, chance), d in zip(finishers(rows), draws):
                frac = order[d] / (field - 1)
                band = "LOW" if frac < 1 / 3 else "HIGH" if frac > 2 / 3 else "MIDDLE"
                add(draw[key][band], won, prb, chance)
    draw_rows = []
    for key in sorted(draw, key=lambda k: (k[0], k[1], k[3], k[4], FIELD_BANDS.index(k[5]))):
        cid, disc, dist, furlongs, going_key, fb = key
        row = {"course_id": cid, "course_name": courses[cid]["course_name"], "discipline": disc,
               "distance": dist, "furlongs": furlongs, "going": going_key, "field_size": fb,
               "races": draw_races[key]}
        row.update(summarise(draw[key], DRAW_BANDS))
        row["confidence"] = confidence(row["races"])
        row["verdict"] = draw_field_verdict(row)
        draw_rows.append(row)

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    write_csv(out / "weight_bias.csv", weight_rows)
    write_csv(out / "draw_field_bias.csv", draw_rows)
    return len(weight_rows), len(draw_rows)


def weight_verdict(row, nat):
    """Compare the heavy end (TOP+UPPER) with the light end (MIDDLE+LOW) here vs nationally."""
    if row["confidence"] == "TOO_FEW":
        return "Not enough races"

    def gap(r):
        heavy = [r[f"{b}_prb"] for b in ("top", "upper") if r[f"{b}_prb"] != ""]
        light = [r[f"{b}_prb"] for b in ("middle", "low") if r[f"{b}_prb"] != ""]
        return (sum(heavy) / len(heavy) - sum(light) / len(light)) if heavy and light else None

    here, base = gap(row), gap(nat)
    if here is None or base is None:
        return "Not enough races"
    diff = here - base
    row["heavy_minus_light_prb"] = round(here, 3)
    row["national_heavy_minus_light_prb"] = round(base, 3)
    if abs(diff) < 0.03:
        verdict = "Typical — weight matters as much as nationally"
    elif diff > 0:
        verdict = ("Top weights do better here than nationally" if diff >= 0.06
                   else "Leans towards top weights (vs national)")
    else:
        verdict = ("Low weights do better here than nationally" if diff <= -0.06
                   else "Leans towards low weights (vs national)")
    if row["confidence"] == "LOW":
        verdict += " (small sample — treat with caution)"
    return verdict


def draw_field_verdict(row):
    if row["confidence"] == "TOO_FEW":
        return "Not enough races"
    low, high = row.get("low_prb"), row.get("high_prb")
    if low == "" or high == "":
        return "Not enough races"
    gap = low - high
    if abs(gap) < 0.04:
        verdict = "No meaningful draw bias"
    else:
        side = "LOW" if gap > 0 else "HIGH"
        verdict = f"{'Strong' if abs(gap) >= 0.10 else 'Clear' if abs(gap) >= 0.06 else 'Slight'} {side} draw advantage"
    if row["confidence"] == "LOW":
        verdict += " (small sample — treat with caution)"
    return verdict


def main(argv=None):
    parser = argparse.ArgumentParser(description="Weight DNA + draw by field size.")
    parser.add_argument("--uki", required=True)
    parser.add_argument("--form", required=True)
    parser.add_argument("--out", default="reports/track_stats")
    args = parser.parse_args(argv)
    w, d = build(args.uki, args.form, args.out)
    print(f"weight_bias rows: {w}, draw_field_bias rows: {d}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
