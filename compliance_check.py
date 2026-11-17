#!/usr/bin/env python3
"""ZANS compliance check for a batch of social posts (rulebook Sections 1-3 and 6).

Usage:  python3 compliance_check.py batch/2026-11-17/batch.json
Exit code 0 = no FAIL lines. WARN lines need a human look but do not block.
It checks words and limits only. It cannot judge a picture, a fact or a silks
colour: the independent check and Alex's yes are still needed.
"""
import json
import re
import sys

FOOTER = ("18+ Only. Begambleaware.org. Past track statistics do not guarantee future race outcomes. "
          "Insights are for informational and entertainment use only.")
PRODUCT_LINE = "Make finding a winner a little easier."
BIO = "Link in bio 👉 www.zanshorseracing.co.uk"
XMAS = "Wishing you a Merry Christmas"
HASHTAG_MAX = {"tiktok": 5, "instagram": 5, "facebook": 3, "x": 2, "youtube": 3, "pinterest": 0, "linkedin": 3}

BANNED = [r"tips?", r"tipster", r"tipping", r"guaranteed?", r"sure thing", r"can't lose", r"beat the bookies",
          r"banker", r"lock", r"profits?", r"investment", r"second income", r"winning system", r"nap",
          r"certain winner", r"pay the bills", r"betting slip", r"unlock", r"dive in", r"game-changer", r"elevate",
          r"official", r"wikipedia", r"royal ascot", r"free", r"giveaway", r"made in the uk"]
MEDIA = [r"racing post", r"rpr", r"topspeed", r"timeform", r"at the races", r"sporting life", r"bet365", r"betfair",
         r"paddy power", r"sky bet", r"william hill", r"ladbrokes", r"coral", r"betfred", r"tote", r"oddschecker"]
OWNERS = [r"juddmonte", r"godolphin", r"coolmore", r"ricci", r"magnier", r"darley", r"shadwell", r"mcmanus",
          r"gigginstown", r"aga khan", r"cheveley park"]
BAIT = [r"tag a friend", r"tag (the|your|a) ", r"comment yes", r"like if", r"double tap", r"#fyp", r"#foryou", r"#viral"]
ARCHIVED = [r"breeders'? cup"]
# Flat turf posts are paused (rulebook Section 2): all-weather only.
FLAT_TURF = [r"ascot", r"goodwood", r"epsom", r"newmarket", r"flat guide", r"flat racing", r"#?flatracing"]
# TikTok Strike Shield: none of these may appear anywhere in a TikTok post.
SHIELD = [r"odds", r"stalls?", r"draw", r"going", r"winners?", r"winning", r"wins?", r"won", r"bets?", r"betting",
          r"gambl\w*", r"prices?", r"value", r"guides?", r"favourites", r"clear favourite", r"selections?", r"race ?day", r"today",
          r"18\+", r"£"]
CLAIMS = [r"\+£", r"\d+ winners? (this|last) (week|month)", r"\broi\b", r"our strike rate"]


def find(patterns, text):
    hits = []
    for pat in patterns:
        rx = pat if pat in (r"£", r"18\+", r"\+£") or pat.startswith("#") else rf"\b{pat}\b"
        hits += [m.group(0) for m in re.finditer(rx, text, re.I)]
    return hits


def x_len(text):
    text = re.sub(r"https?://\S+", "x" * 23, text)
    return len(text) + len(re.findall("[\U0001F000-\U0001FAFF]", text))


def check_post(post):
    out = []
    fail = lambda net, msg: out.append(("FAIL", post["id"], net, msg))
    warn = lambda net, msg: out.append(("WARN", post["id"], net, msg))
    betting, nets = post["kind"] == "betting", post["networks"]
    img = post.get("on_image", {})
    img_text = " ".join(str(v) for v in img.values() if isinstance(v, str)) + " " + json.dumps(
        img.get("rows", "") or img.get("cards", ""), ensure_ascii=False)
    words = len(img.get("headline", "").split())
    if not 5 <= words <= 8:
        fail("image", f"headline is {words} words (rule 3.4: 5 to 8)")
    if betting and "tiktok" in nets:
        fail("tiktok", "Strike Shield: a guide or betting-adjacent post is routed to TikTok")
    if "youtube" in nets:
        warn("youtube", "YouTube needs a video")
    for net, d in nets.items():
        text = d["text"]
        every = " ".join(str(d.get(k, "")) for k in ("title", "text", "first_comment", "reply"))
        scan = every + " " + img_text + " " + post.get("alt", "")
        scan = scan.replace(FOOTER, "")  # the approved footer is a negated line, so it is allowed
        for label, pats in (("banned word", BANNED), ("bookmaker or media name", MEDIA), ("owner name", OWNERS),
                            ("engagement bait", BAIT), ("archived topic", ARCHIVED),
                            ("paused Flat turf topic", FLAT_TURF), ("results claim", CLAIMS)):
            hits = find(pats, scan)
            if hits:
                fail(net, f"{label}: {sorted(set(h.lower() for h in hits))}")
        n_tags = len(re.findall(r"#\w+", every))
        if n_tags > HASHTAG_MAX[net]:
            fail(net, f"{n_tags} hashtags (limit {HASHTAG_MAX[net]})")
        first = text.split("\n")[0]
        if re.search(r"www\.|https?://|£|get yours", first, re.I):
            fail(net, "line 1 opens with a link, a price or GET YOURS")
        # One open question to answer. A rhetorical hook in line 1 is allowed on top of it.
        hook_q = first.count("?") if net != "x" else max(0, text.count("?") - 1)
        questions = text.count("?") - hook_q
        if net != "pinterest" and (questions != 1 or hook_q > 1):
            fail(net, f"{text.count('?')} question marks (rule: one open question, plus at most one in the hook)")
        if "finding a winner" in every and PRODUCT_LINE not in every:
            fail(net, "product line is not word for word")
        if "finding a winner" in every and not betting:
            fail(net, "product line used on a gift post (rule 3.4)")
        # footers
        if net != "tiktok":
            if betting and FOOTER not in every:
                fail(net, "betting footer missing or not word for word")
            if not betting and re.search(r"18\+|begambleaware|gamble responsibly", every, re.I):
                fail(net, "18+ line on a merch post")
        # house lines
        if net in ("instagram", "tiktok") and text.strip().split("\n")[-1] != BIO:
            fail(net, "last line is not the Link in bio house line")
        if post["christmas"] and XMAS not in every:
            fail(net, "Christmas post without the Merry Christmas line")
        if not post["christmas"] and XMAS in every:
            fail(net, "Merry Christmas line on a non-Christmas post")
        # network rules
        if net == "facebook" and re.search(r"www\.|https?://", text):
            fail(net, "link in the Facebook post body (belongs in the first comment)")
        if net == "x":
            if re.search(r"www\.|https?://", text):
                fail(net, "link in the X post (belongs in the reply)")
            for part in ("text", "reply"):
                if x_len(d.get(part, "")) > 280:
                    fail(net, f"X {part} is {x_len(d[part])} characters (limit 280)")
        if net == "pinterest":
            if len(d["title"]) > 100:
                fail(net, f"pin title {len(d['title'])} characters (limit 100)")
            if not 200 <= len(text) <= 500:
                fail(net, f"pin description {len(text)} characters (200 to 500)")
        if net == "tiktok":
            hits = find(SHIELD, scan)
            if hits:
                fail(net, f"Strike Shield word: {sorted(set(h.lower() for h in hits))}")
            if len(d.get("title", "")) > 90:
                fail(net, f"TikTok title {len(d['title'])} characters (limit 90)")
            if img.get("t") != "bauble":
                fail(net, "Visual Hook Rule 3.6: image is not a real-life lifestyle scene")
        if post.get("showcase") and re.search(r"etsy", every, re.I):
            fail(net, "showcase bauble post mentions or links to Etsy")
    return out


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    batch = json.load(open(sys.argv[1], encoding="utf-8"))
    results = [r for post in batch for r in check_post(post)]
    cuts = sum(len(p["networks"]) for p in batch)
    for level, pid, net, msg in results:
        print(f"{level}  {pid}  {net:<9}  {msg}")
    fails = sum(1 for r in results if r[0] == "FAIL")
    print(f"\n{len(batch)} posts, {cuts} network cuts checked: {fails} FAIL, {len(results) - fails} WARN")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
