#!/usr/bin/env python3
"""ZANS Racing weekly social analytics loop.

What it does
------------
Reads one week of Metricool post data, works out which hooks, pillars and
formats earned the most saves, shares, comments and link clicks, and writes the
week's findings into social_lessons_learned.md (newest week first).

How the data gets here
----------------------
The Metricool connector is only available to Claude inside a session, not to a
standalone script, and no API keys are kept in this repo. So the weekly loop is:

  1. python3 analyze_social_performance.py --pull-plan
       prints the week's date range and the exact metric IDs for each source.
  2. Claude pulls each source with the Metricool connector
     (getAnalyticsDataByMetrics) and saves the answer as
       social_data/<week-start>/<SOURCE>.json
     in the shape {"source", "from", "to", "metrics": [...], "rows": [[...]]}.
  3. python3 analyze_social_performance.py --week <week-start>
       analyses the files and updates social_lessons_learned.md.

Weeks run Monday to Sunday. Standard library only.

Limits to keep in mind
----------------------
* Metricool cannot see Etsy. "Link clicks" are clicks on links in our posts and
  pins; Etsy visits and sales come from Etsy Stats and are added by hand.
* Our own link comment (Facebook first comment, X reply) is counted by the
  networks as a comment. One is taken off each Facebook feed post and X post.
* Small numbers prove nothing. A pattern is only called when both sides have
  at least MIN_POSTS posts; otherwise it is logged as "too few to call".
* This log is internal. Never quote these figures in a post or listing.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "social_data"
LESSONS = ROOT / "social_lessons_learned.md"
MIN_POSTS = 5          # smallest group we will draw a pattern from
MIN_VIEWS = 20         # posts under this are too small for a per-1,000 rate

# Source -> network, format, the metric IDs to pull (in order) and what each
# column means. "own_comment" = our own link comment is counted by the network.
SOURCES = {
    "IGPO": dict(network="Instagram", kind="feed", own_comment=0,
                 metrics=["IGPO01", "IGPO03", "IGPO06", "IGPO07", "IGPO08", "IGPO09",
                          "IGPO13", "IGPO14", "IGPO15", "IGPO27", "IGPO28"],
                 cols=["date", "text", "url", "type", "comments", "clicks", "likes",
                       "reach", "saves", "shares", "views"]),
    "IGRE": dict(network="Instagram", kind="video", own_comment=0,
                 metrics=["IGRE01", "IGRE03", "IGRE06", "IGRE07", "IGRE10", "IGRE11",
                          "IGRE12", "IGRE21", "IGRE23"],
                 cols=["date", "text", "url", "comments", "likes", "reach", "saves",
                       "shares", "views"]),
    "FBPO": dict(network="Facebook", kind="feed", own_comment=1,
                 metrics=["FBPO01", "FBPO03", "FBPO06", "FBPO07", "FBPO08", "FBPO09",
                          "FBPO11", "FBPO12", "FBPO13", "FBPO14", "FBPO23"],
                 cols=["date", "text", "url", "type", "comments", "clicks", "views",
                       "reach", "likes", "shares", "all_clicks"]),
    "FBRE": dict(network="Facebook", kind="video", own_comment=0,
                 metrics=["FBRE01", "FBRE05", "FBRE06", "FBRE08", "FBRE10", "FBRE11"],
                 cols=["date", "text", "url", "likes", "views", "reach"]),
    "TKPO": dict(network="TikTok", kind="typed", own_comment=0,
                 metrics=["TKPO01", "TKPO05", "TKPO03", "TKPO22", "TKPO07", "TKPO08",
                          "TKPO09", "TKPO10", "TKPO11"],
                 cols=["date", "text", "url", "type", "views", "likes", "comments",
                       "shares", "reach"]),
    "YTVP": dict(network="YouTube", kind="video", own_comment=0,
                 metrics=["YTVP01", "YTVP17", "YTVP05", "YTVP06", "YTVP09", "YTVP11",
                          "YTVP12"],
                 cols=["date", "text", "url", "views", "likes", "comments", "shares"]),
    "PIPO": dict(network="Pinterest", kind="pin", own_comment=0,
                 metrics=["PIPO01", "PIPO03", "PIPO04", "PIPO07", "PIPO08", "PIPO09",
                          "PIPO10", "PIPO11", "PIPO12"],
                 cols=["date", "text", "body", "url", "views", "saves", "pin_clicks",
                       "clicks", "video_views"]),
    "TTTW": dict(network="X", kind="feed", own_comment=1,
                 metrics=["TTTW01", "TTTW03", "TTTW04", "TTTW05", "TTTW06", "TTTW07",
                          "TTTW08", "TTTW09", "TTTW11", "TTTW12", "TTTW29"],
                 cols=["date", "text", "url", "likes", "shares", "clicks", "comments",
                       "quotes", "views", "video_views", "saves"]),
    "LIPO": dict(network="LinkedIn", kind="typed", own_comment=0,
                 metrics=["LIPO01", "LIPO04", "LIPO08", "LIPO19", "LIPO09", "LIPO10",
                          "LIPO12", "LIPO13", "LIPO16", "LIPO18"],
                 cols=["date", "text", "url", "type", "clicks", "comments", "views",
                       "likes", "video_views", "shares"]),
}
NUMERIC = {"comments", "clicks", "likes", "reach", "saves", "shares", "views",
           "all_clicks", "pin_clicks", "video_views", "quotes"}
# Which measures each source can actually report (so a missing measure is not
# mistaken for a zero).
TRACKS = {src: {c for c in cfg["cols"] if c in NUMERIC} for src, cfg in SOURCES.items()}

PILLARS = [
    # (label, pattern) - first match wins. Rulebook Section 3, rule 3.
    ("B: Gifts (mugs, baubles)",
     r"\b(mug|bauble|gift|gifts|personalised|stocking filler)\b"),
    ("Longshot series", r"\b(yankee|each-way|each way)\b"),
    ("C: Silks and nostalgia",
     r"\b(retire|retirement|legend|legends|greats|history|remember|greatest|"
     r"thank you|famous colours)\b"),
    ("A: Track data",
     r"(\d+(\.\d+)?%|\bknow the track\b|\bfavourites\b|\bdraw\b|\bgoing\b|"
     r"\bground\b|\bwin rate\b|\bstrike rate\b|\bdata:)"),
]
SAVE_PROMPT = re.compile(r"\bsave (this|it|for)\b", re.I)
SHARE_PROMPT = re.compile(r"\b(send|share|forward) (this|it)\b", re.I)
CHEESY_BAIT = re.compile(r"\b(tag (a|the|your)|comment (yes|below to win)|like if|"
                         r"double tap)\b", re.I)
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿️‍]")


def num(value) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def hook_of(text: str) -> str:
    """The first line of the caption, without emoji or hashtags."""
    first = (text or "").strip().split("\n")[0]
    first = EMOJI.sub("", first)
    first = re.sub(r"#\w+", "", first)
    first = re.split(r"(?<=[.?!])\s", first.strip())[0]
    return re.sub(r"\s+", " ", first).strip()[:110]


def pillar_of(text: str) -> str:
    for label, pattern in PILLARS:
        if re.search(pattern, text or "", re.I):
            return label
    return "Race news and previews"


def format_of(cfg: dict, row: dict) -> str:
    kind = cfg["kind"]
    if kind == "video":
        return "Video"
    if kind == "pin":
        return "Video pin" if row.get("video_views", 0) > 0 else "Pin"
    kind_text = str(row.get("type") or "").upper()
    if "VIDEO" in kind_text or "REEL" in kind_text:
        return "Video"
    if "CAROUSEL" in kind_text or "ALBUM" in kind_text or "MULTI" in kind_text:
        return "Carousel"
    if kind_text in ("PHOTO", "IMAGE", "PHOTOS"):
        return "Photo"
    return "Post"


def load_week(week: str) -> list[dict]:
    folder = DATA_DIR / week
    posts = []
    for src, cfg in SOURCES.items():
        path = folder / f"{src}.json"
        if not path.exists():
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("metrics") != cfg["metrics"]:
            raise SystemExit(f"{path}: metric list does not match the pull plan. "
                             f"Re-pull with: {cfg['metrics']}")
        for raw in payload["rows"]:
            row = dict(zip(cfg["cols"], raw))
            for key in list(row):
                if key in NUMERIC:
                    row[key] = num(row[key])
            text = str(row.get("text") or "")
            if row.get("body"):
                text_all = f"{text}\n{row['body']}"
            else:
                text_all = text
            comments = max(0.0, row.get("comments", 0.0) - cfg["own_comment"])
            views = row.get("views") or row.get("reach") or 0.0
            hook = hook_of(text)
            posts.append(dict(
                source=src, tracked=TRACKS[src], network=cfg["network"], date=str(row.get("date", "")),
                url=str(row.get("url") or ""), text=text_all, hook=hook,
                hook_words=len(hook.split()), pillar=pillar_of(text_all),
                format=format_of(cfg, row), views=views,
                saves=row.get("saves", 0.0), shares=row.get("shares", 0.0),
                comments=comments, likes=row.get("likes", 0.0),
                clicks=row.get("clicks", 0.0),
                has_question="?" in text_all,
                save_prompt=bool(SAVE_PROMPT.search(text_all)),
                share_prompt=bool(SHARE_PROMPT.search(text_all)),
                cheesy_bait=bool(CHEESY_BAIT.search(text_all)),
            ))
    return posts


def fmt(value: float) -> str:
    return f"{value:,.0f}" if float(value).is_integer() else f"{value:,.1f}"


def per_thousand(part: float, views: float) -> str:
    return "-" if views < MIN_VIEWS else f"{1000 * part / views:.1f}"


def group_table(posts: list[dict], key: str) -> list[str]:
    groups: dict[str, list[dict]] = {}
    for post in posts:
        groups.setdefault(post[key], []).append(post)
    lines = ["| Group | Posts | Views | Median views | Saves | Shares | Comments | "
             "Link clicks | Saves per 1,000 views |",
             "|---|---|---|---|---|---|---|---|---|"]
    ordered = sorted(groups.items(), key=lambda kv: -sum(p["views"] for p in kv[1]))
    for name, items in ordered:
        views = sum(p["views"] for p in items)

        def cell(measure: str) -> str:
            # "n/a" when no network in the group reports this measure at all.
            if not any(measure in p["tracked"] for p in items):
                return "n/a"
            return fmt(sum(p[measure] for p in items))

        save_views = sum(p["views"] for p in items if "saves" in p["tracked"])
        saves = sum(p["saves"] for p in items)
        rate = "n/a" if cell("saves") == "n/a" else per_thousand(saves, save_views)
        lines.append(
            f"| {name} | {len(items)} | {fmt(views)} | "
            f"{fmt(statistics.median(p['views'] for p in items))} | {cell('saves')} | "
            f"{cell('shares')} | {cell('comments')} | {cell('clicks')} | {rate} |")
    return lines


def top_posts(posts: list[dict], measure: str, limit: int = 5) -> list[str]:
    ranked = sorted((p for p in posts if p[measure] > 0),
                    key=lambda p: (-p[measure], -p["views"]))[:limit]
    if not ranked:
        return [f"- None. No post earned any {measure.replace('clicks', 'link clicks')} "
                f"this week."]
    return [f"- **{fmt(p[measure])}** · {p['network']} {p['format'].lower()} · "
            f"{p['pillar']} · \"{p['hook']}\" ({fmt(p['views'])} views)"
            for p in ranked]


def compare(posts: list[dict], flag: str, yes: str, no: str) -> str:
    with_flag = [p for p in posts if p[flag]]
    without = [p for p in posts if not p[flag]]
    if len(with_flag) < MIN_POSTS or len(without) < MIN_POSTS:
        return (f"- {yes}: {len(with_flag)} posts; {no}: {len(without)} posts. "
                f"Too few to call (need {MIN_POSTS} on each side).")
    def rate(items):
        views = sum(p["views"] for p in items)
        acts = sum(p["saves"] + p["shares"] + p["comments"] for p in items)
        return 1000 * acts / views if views else 0.0
    return (f"- {yes} ({len(with_flag)} posts): {rate(with_flag):.1f} saves, shares and "
            f"comments per 1,000 views. {no} ({len(without)} posts): "
            f"{rate(without):.1f}.")


def patterns(posts: list[dict], previous: list[dict] | None) -> list[str]:
    out = []
    total = {m: sum(p[m] for p in posts) for m in ("views", "saves", "shares",
                                                    "comments", "clicks")}
    if total["saves"] == 0:
        out.append("- **Saves are at zero.** Nothing posted this week was built to be "
                   "kept. Section 3 rule 1 (cheat-sheet posts with a save prompt) is the "
                   "first thing to test.")
    if total["shares"] <= 2:
        out.append(f"- **Shares are close to zero ({fmt(total['shares'])}).** No post "
                   "carried a 'send this to...' line. Rule 1 share prompts are untested.")
    by_network: dict[str, list[dict]] = {}
    for post in posts:
        by_network.setdefault(post["network"], []).append(post)
    for network, items in sorted(by_network.items()):
        groups: dict[str, list[float]] = {}
        for post in items:
            groups.setdefault(post["pillar"], []).append(post["views"])
        solid = {k: statistics.median(v) for k, v in groups.items() if len(v) >= 3}
        if len(solid) >= 2:
            best = max(solid, key=solid.get)
            worst = min(solid, key=solid.get)
            if solid[best] >= 2 * max(solid[worst], 1):
                out.append(f"- **{network}:** {best} posts had a median of "
                           f"{fmt(solid[best])} views against {fmt(solid[worst])} for "
                           f"{worst} (3 or more posts each).")
    prompts = sum(1 for p in posts if p["save_prompt"] or p["share_prompt"])
    out.append(f"- Posts carrying a save or share prompt: {prompts} of {len(posts)}.")
    bait = [p for p in posts if p["cheesy_bait"]]
    if bait:
        out.append(f"- **Rule break to fix:** {len(bait)} post(s) used engagement bait "
                   f"(for example \"{bait[0]['hook']}\" on {bait[0]['network']}). "
                   "Rule 2 bans it.")
    long_hooks = sum(1 for p in posts if p["hook_words"] > 12)
    out.append(f"- Caption first lines over 12 words: {long_hooks} of {len(posts)}. "
               "(The 5-to-8-word rule is for the headline on the graphic; shorter "
               "first lines are still easier to read in the feed.)")
    if previous:
        for measure in ("views", "saves", "shares", "comments", "clicks"):
            before = sum(p[measure] for p in previous)
            now = total[measure]
            if before:
                change = 100 * (now - before) / before
                out.append(f"- {measure.capitalize()} v last week: {fmt(now)} v "
                           f"{fmt(before)} ({change:+.0f}%).")
    return out


def build_section(week: str, posts: list[dict], previous: list[dict] | None,
                  extras: dict) -> str:
    start = dt.date.fromisoformat(week)
    end = start + dt.timedelta(days=6)
    lines = [f"## Week of {start:%-d %b} to {end:%-d %b %Y}", "",
             f"{len(posts)} posts across {len({p['network'] for p in posts})} networks. "
             f"Source: Metricool, pulled by Claude. Internal use only.", ""]
    totals = {m: sum(p[m] for p in posts) for m in ("views", "saves", "shares",
                                                     "comments", "likes", "clicks")}
    lines += ["### Totals",
              f"- Views: {fmt(totals['views'])}",
              f"- Saves: {fmt(totals['saves'])}",
              f"- Shares: {fmt(totals['shares'])}",
              f"- Comments (ours removed): {fmt(totals['comments'])}",
              f"- Likes: {fmt(totals['likes'])}",
              f"- Link clicks on posts and pins: {fmt(totals['clicks'])}"]
    for label, value in extras.items():
        lines.append(f"- {label}: {value}")
    lines += ["", "### Winning patterns", *patterns(posts, previous), "",
              "### By network", *group_table(posts, "network"), "",
              "### By content pillar", *group_table(posts, "pillar"), "",
              "### By format", *group_table(posts, "format"), "",
              "### Do the rules help? (saves + shares + comments per 1,000 views, all networks mixed)",
              compare(posts, "has_question", "With a question", "Without"),
              compare(posts, "save_prompt", "With a save prompt", "Without"),
              compare(posts, "share_prompt", "With a share prompt", "Without"), "",
              "### Top posts", "**Most saves**", *top_posts(posts, "saves"), "",
              "**Most shares**", *top_posts(posts, "shares"), "",
              "**Most comments**", *top_posts(posts, "comments"), "",
              "**Most link clicks**", *top_posts(posts, "clicks"), "",
              "**Most views**", *top_posts(posts, "views"), "",
              "### What the numbers cannot tell us",
              "- Instagram and TikTok do not report clicks on the bio link per post.",
              "- Facebook video posts report views and likes only (no saves or shares).",
              "- YouTube and LinkedIn do not report saves.",
              "- Etsy visits and sales are not in Metricool. Add them from Etsy Stats.",
              ""]
    return "\n".join(lines)


HEADER = """# ZANS social lessons learned

Written by `analyze_social_performance.py` once a week, newest week first.
Read the newest week before planning any post (rulebook Section 3, rule 5).
Internal working notes: never quote these figures in a post, listing or reply.

"""


def write_lessons(week: str, section: str) -> None:
    marker_start = f"<!-- week:{week} -->"
    marker_end = f"<!-- /week:{week} -->"
    block = f"{marker_start}\n{section}\n{marker_end}\n"
    body = LESSONS.read_text(encoding="utf-8") if LESSONS.exists() else HEADER
    if marker_start in body:
        body = re.sub(re.escape(marker_start) + r".*?" + re.escape(marker_end) + r"\n",
                      lambda _: block, body, flags=re.S)
    else:
        head, sep, rest = body.partition("<!-- week:")
        body = head + block + ("\n" + sep + rest if sep else "")
    LESSONS.write_text(body, encoding="utf-8")


def last_full_week(today: dt.date) -> dt.date:
    this_monday = today - dt.timedelta(days=today.weekday())
    return this_monday - dt.timedelta(days=7)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--week", help="Monday the week starts, YYYY-MM-DD "
                                       "(default: the last full week)")
    parser.add_argument("--pull-plan", action="store_true",
                        help="print the dates and metric IDs Claude should pull")
    args = parser.parse_args()
    start = (dt.date.fromisoformat(args.week) if args.week
             else last_full_week(dt.date.today()))
    if start.weekday() != 0:
        raise SystemExit("--week must be a Monday")
    week = start.isoformat()

    if args.pull_plan:
        end = start + dt.timedelta(days=6)
        print(f"Week {week}: from {week}T00:00:00+00:00 to {end}T23:59:59+00:00")
        print(f"Save each answer as social_data/{week}/<SOURCE>.json\n")
        for src, cfg in SOURCES.items():
            print(f"{src} ({cfg['network']}): {json.dumps(cfg['metrics'])}")
        return

    posts = load_week(week)
    if not posts:
        raise SystemExit(f"No data in social_data/{week}/. Run --pull-plan first.")
    previous_week = (start - dt.timedelta(days=7)).isoformat()
    previous = load_week(previous_week) if (DATA_DIR / previous_week).exists() else None
    extras_path = DATA_DIR / week / "account.json"
    extras = json.loads(extras_path.read_text(encoding="utf-8")) if extras_path.exists() else {}
    write_lessons(week, build_section(week, posts, previous, extras))
    print(f"{len(posts)} posts analysed. Updated {LESSONS.name} for week {week}.")


if __name__ == "__main__":
    main()
