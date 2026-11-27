"""Runner-level table for the course knowledge base (scripts/course_kb.py).

One row per runner, UK/IRE races 2018 onwards: Kaggle full results (race names, bands, comments,
times) + our Racing Post store (June 2026 on), weights from the Kaggle form file. Adds exact
going, margin-free SP chance, clear favourite, draw third, running style, handicap flag,
weight below top, an INFERRED jockey claim, days since last run, last-time-out winner, course and
distance winner, and the winner's time against the ZANS standard.

    python scripts/course_kb_data.py --out /tmp/claude-0/kb/runners.pkl [--check-claims]
"""
import argparse
import glob
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from speed.figures import track_key  # noqa: E402
from track_stats.parse import course_key, dist_to_furlongs, is_uk_ire, overseas_bred_race, running_style  # noqa: E402

COLS = ["date", "course", "race_id", "off", "race_name", "type", "class", "pattern", "rating_band", "dist", "going",
        "ran", "pos", "draw", "horse", "age", "lbs", "time", "secs", "sp", "jockey", "trainer", "or", "comment", "region"]
CLAIMS = (3, 5, 7, 10)


def norm_going(g):
    text = re.split(r"[,(]", str(g or ""))[0].strip()
    if not text or text.lower() == "nan":
        return None
    return " ".join(w.lower() if w.lower() == "to" else w for w in text.title().split())


def sp_dec(sp):
    m = re.match(r"\s*(\d+)/(\d+)", str(sp or ""))
    if m:
        return 1 + int(m.group(1)) / int(m.group(2))
    return 2.0 if re.match(r"\s*evens?", str(sp or ""), re.I) else np.nan


def secs_of(t):
    m = re.fullmatch(r"\s*(?:(\d+):)?(\d+(?:\.\d+)?)\s*", str(t or ""))
    if not m:
        return np.nan
    return int(m.group(1) or 0) * 60 + float(m.group(2))


def wgt_lbs(w):
    m = re.fullmatch(r"(\d+)-(\d+)", str(w or "").strip())
    return int(m.group(1)) * 14 + int(m.group(2)) if m else np.nan


def load():
    frames = []
    for p in sorted(glob.glob(str(REPO / "data" / "results_full_*.csv.gz"))):
        if int(re.search(r"(\d{4})", Path(p).name).group(1)) < 2018:
            continue
        d = pd.read_csv(p, low_memory=False, usecols=lambda c: c in COLS)
        d["src"] = 1
        frames.append(d)
    for p in sorted(glob.glob(str(REPO / "history" / "store_*.csv.gz"))):
        d = pd.read_csv(p, low_memory=False, usecols=lambda c: c in COLS)
        d["src"] = 0
        frames.append(d)
    d = pd.concat(frames, ignore_index=True)
    d["date"] = d["date"].astype(str).str.replace("/", "-").str[:10]
    d = d[d["date"] >= "2018-01-01"]
    d["hname"] = d["horse"].astype(str).str.replace(r"\s*\([A-Z]{2,3}\)\s*$", "", regex=True).str.lower().str.replace(r"[^a-z0-9]", "", regex=True)
    d = d.sort_values("src").drop_duplicates(["date", "course", "hname"]).copy()
    # weights for Kaggle rows come from the form file
    form = pd.read_csv(REPO / "history" / "results_form.csv.gz", low_memory=False, usecols=["race_id", "horse", "wgt"])
    form["hname"] = form["horse"].astype(str).str.replace(r"\s*\([A-Z]{2,3}\)\s*$", "", regex=True).str.lower().str.replace(r"[^a-z0-9]", "", regex=True)
    form["lbs_f"] = form["wgt"].map(wgt_lbs)
    form = form.drop_duplicates(["race_id", "hname"])[["race_id", "hname", "lbs_f"]]
    d["race_id"] = pd.to_numeric(d["race_id"], errors="coerce")
    form["race_id"] = pd.to_numeric(form["race_id"], errors="coerce")
    d = d.merge(form, on=["race_id", "hname"], how="left")
    d["lbs"] = pd.to_numeric(d["lbs"], errors="coerce").fillna(d["lbs_f"])
    d = d[d["course"].map(is_uk_ire)]
    return d


def build():
    d = load()
    keys = d["course"].map(course_key)
    d["cid"] = keys.map(lambda k: k[0])
    d["aw"] = keys.map(lambda k: k[1])
    d["track"] = d["course"].map(track_key)
    t = d["type"].astype(str).str.lower().str.strip()
    d["disc"] = t.map({"flat": "FLAT", "hurdle": "HURDLE", "chase": "CHASE", "nh flat": "NHF"})
    d.loc[(d["disc"] == "FLAT") & d["aw"], "disc"] = "AW_FLAT"
    d = d[d["disc"].notna()].copy()
    # 27 Nov: AW rows before a course's surface switch (Southwell Fibresand -> Tapeta 7 Dec 2021 ...) are a different surface
    import json as _j
    _cs = _j.load(open("config/courses.json")); _cs = _cs.get("courses", _cs)
    for _cid, _c in _cs.items():
        _since = (_c.get("surface_since") or {}).get("AW_FLAT")
        if _since:
            d = d[~((d["cid"] == _cid) & (d["disc"] == "AW_FLAT") & (d["date"] < _since))]
    d["code"] = d["disc"].map({"FLAT": "FLAT", "AW_FLAT": "AW_FLAT", "HURDLE": "JUMPS", "CHASE": "JUMPS", "NHF": "JUMPS"})
    d["going"] = d["going"].map(norm_going)
    d["fur"] = d["dist"].map(dist_to_furlongs)
    d["fur"] = (d["fur"] * 2).round() / 2
    d["rkey"] = d["date"] + "|" + d["course"].astype(str) + "|" + d["off"].astype(str)
    # overseas-bred fields filed under a UK name (Ascot WA, Newcastle NSW)
    bad = d.groupby("rkey")["horse"].apply(lambda s: overseas_bred_race(list(s.astype(str))))
    d = d[~d["rkey"].isin(bad[bad].index)].copy()
    d["posraw"] = d["pos"].astype(str).str.strip()
    d["posn"] = pd.to_numeric(d["pos"], errors="coerce")
    d["won"] = d["posn"] == 1
    d["n"] = d.groupby("rkey")["hname"].transform("size")
    d["dec"] = d["sp"].map(sp_dec)
    imp = 1 / d["dec"]
    full = d["dec"].notna().groupby(d["rkey"]).transform("all")
    d["chance"] = (imp / imp.groupby(d["rkey"]).transform("sum")).where(full)
    mn = d.groupby("rkey")["dec"].transform("min")
    d["is_fav"] = d["dec"].notna() & (d["dec"] == mn)
    d["fav"] = d["is_fav"] & (d.groupby("rkey")["is_fav"].transform("sum") == 1)
    d["year"] = d["date"].str[:4].astype(int)
    d["period"] = np.where(d["date"] < "2019-01-01", "", np.where(d["date"] < "2022-01-01", "2019-21", "2022-26"))
    # each-way places by field size (5-7: 2, 8+: 3, handicap 16+: 4; under 5 win only)
    rb = d["rating_band"].astype(str).str.strip()
    d["hcap"] = (rb.ne("") & rb.ne("nan")) | d["race_name"].astype(str).str.contains("handicap", case=False)
    places = np.where(d["n"] >= 16, np.where(d["hcap"], 4, 3), np.where(d["n"] >= 8, 3, np.where(d["n"] >= 5, 2, 1)))
    d["placed"] = d["posn"] <= places
    d["pl"] = np.where(d["won"], d["dec"] - 1, -1.0)
    d.loc[d["dec"].isna(), "pl"] = np.nan
    d["prb"] = (d["n"] - d["posn"].fillna(d["n"])) / (d["n"] - 1).clip(lower=1)
    # draw thirds (flat/AW, every runner drawn, 6+ runners)
    d["draw"] = pd.to_numeric(d["draw"], errors="coerce")
    drawn = d["draw"].notna().groupby(d["rkey"]).transform("sum")
    ok = d["code"].isin(["FLAT", "AW_FLAT"]) & (drawn == d["n"]) & (d["n"] >= 6)
    rank = d.loc[ok].groupby("rkey")["draw"].rank(method="first")
    d["third"] = None
    nn = d.loc[ok, "n"]
    d.loc[ok, "third"] = np.where(rank <= nn / 3, "Low", np.where(rank > 2 * nn / 3, "High", "Middle"))
    d["fieldband"] = pd.cut(d["n"], [0, 5, 9, 13, 99], labels=["2-5", "6-9", "10-13", "14+"]).astype(str)
    # running style from the in-running comment
    d["run_style"] = d["comment"].map(running_style).map({4: "Led", 3: "Prominent", 2: "Midfield", 1: "Held up"})
    # weight: lb below the top weight carried in the race (handicaps)
    d["below"] = d.groupby("rkey")["lbs"].transform("max") - d["lbs"]
    d["wband"] = pd.cut(d["below"], [-1, 2, 9, 16, 999], labels=["Top 0-2lb", "Upper 3-9lb", "Middle 10-16lb", "Low 17lb+"]).astype(str)
    d.loc[~d["hcap"] | d["lbs"].isna(), "wband"] = None
    # INFERRED claim: in handicaps, carried + (top OR - OR) = the race's top weight unless the
    # rider claims (3/5/7, 10 for conditionals) -> majority per jockey per month, applied to all rides
    d["or"] = pd.to_numeric(d["or"], errors="coerce")
    base = d["lbs"] + d.groupby("rkey")["or"].transform("max") - d["or"]
    mode = base.groupby(d["rkey"]).transform(lambda s: s.mode().iloc[0] if s.notna().any() else np.nan)
    gap = mode - base
    obs = d["hcap"] & base.notna()
    d["claim_obs"] = np.where(obs & gap.isin(CLAIMS), gap, np.where(obs & (gap == 0), 0, np.nan))
    d["jname"] = d["jockey"].astype(str).str.replace(r"\s*\(\d+\)$", "", regex=True).str.strip()
    d["ym"] = d["date"].str[:7]
    o = d.dropna(subset=["claim_obs"]).groupby(["jname", "ym"])["claim_obs"].agg(lambda s: s.mode().iloc[0])
    o = o.reset_index().rename(columns={"claim_obs": "claim"})
    o["mi"] = o["ym"].str[:4].astype(int) * 12 + o["ym"].str[5:7].astype(int)
    d["mi"] = d["year"] * 12 + d["ym"].str[5:7].astype(int)
    d = d.sort_values("mi")
    o = o.sort_values("mi")
    d = pd.merge_asof(d, o[["jname", "mi", "claim"]], on="mi", by="jname", direction="nearest", tolerance=2)
    # winner time v the ZANS standard (track, discipline, trip)
    st = pd.read_csv(REPO / "reports" / "speed" / "standards.csv")
    st["fur"] = (st["furlongs"] * 2).round() / 2
    st = st.groupby(["track", "discipline", "fur"])["standard_secs"].first()
    sec = pd.to_numeric(d.get("secs"), errors="coerce").fillna(d["time"].map(secs_of))
    d["wsecs"] = np.where(d["won"], sec, np.nan)
    d["std"] = [st.get((a, b, c), np.nan) for a, b, c in zip(d["track"], d["disc"], d["fur"])]
    d["off_std"] = d["wsecs"] - d["std"]
    # horse history: days since last run, last time out winner, course + distance winner
    d["hkey"] = d["hname"] + "_" + (d["year"] - pd.to_numeric(d["age"], errors="coerce").fillna(0).astype(int)).astype(str)
    d = d.sort_values(["hkey", "date"]).reset_index(drop=True)
    prev_date = d.groupby("hkey")["date"].shift()
    d["days_off"] = (pd.to_datetime(d["date"]) - pd.to_datetime(prev_date)).dt.days
    d["lto_won"] = d.groupby("hkey")["won"].shift().fillna(False).astype(bool)
    d["cd_key"] = d["hkey"] + "|" + d["cid"] + "|" + d["aw"].astype(str) + "|" + d["code"] + "|" + d["fur"].astype(str)
    d["cd_winner"] = d.groupby("cd_key")["won"].transform(lambda s: s.shift().fillna(False).astype(bool).cummax())
    d["age"] = pd.to_numeric(d["age"], errors="coerce")
    keep = ["date", "year", "period", "course", "cid", "aw", "track", "disc", "code", "race_name", "hcap", "class", "pattern",
            "rkey", "fur", "going", "n", "fieldband", "posraw", "posn", "won", "placed", "dec", "chance", "fav", "pl", "prb",
            "draw", "third", "run_style", "lbs", "below", "wband", "or", "claim", "jname", "trainer", "age", "off_std", "wsecs",
            "std", "days_off", "lto_won", "cd_winner", "hkey"]
    return d[keep]


def check_claims(d):
    """Compare inferred claims with the claims printed on our racecards (23 Sep onwards)."""
    rows = []
    for p in sorted(glob.glob(str(REPO / "reports" / "racecards" / "*" / "runners.csv"))):
        c = pd.read_csv(p, low_memory=False, usecols=lambda x: x in ("date", "jockey", "jockey_allowance"))
        rows.append(c)
    c = pd.concat(rows)
    c["card"] = pd.to_numeric(c["jockey_allowance"], errors="coerce").fillna(0)
    c["jname"] = c["jockey"].astype(str).str.strip()
    c = c.drop_duplicates(["date", "jname"])
    m = c.merge(d[["date", "jname", "claim"]].drop_duplicates(["date", "jname"]), on=["date", "jname"])
    m = m[m["claim"].notna()]
    agree = (m["card"] == m["claim"]).mean()
    print(f"claim check: {len(m):,} jockey-days on our cards with an inferred claim; agree {agree:.1%}")
    print(pd.crosstab(m["card"], m["claim"]))
    return len(m), agree


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--check-claims", action="store_true")
    a = ap.parse_args()
    df = build()
    df.to_pickle(a.out)
    print(f"{len(df):,} runners -> {a.out}")
    if a.check_claims:
        check_claims(df)
