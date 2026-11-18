#!/usr/bin/env python3
"""Captions for the 8 Christmas bauble videos (18 Nov 2026): one cut per network. Nothing is scheduled.
Writes batch.json (for compliance_check.py), CAPTIONS.md and CAPTIONS.txt."""
import importlib.util, json
from pathlib import Path
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("b17", HERE.parent / "2026-11-17" / "build_batch.py"); b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
SITE, XMAS, BIO, WEB, DESIGNER = b.SITE, b.XMAS, b.BIO, b.WEB_GIFTS, b.DESIGNER
Q = "Which name would you have on yours? 👇"
QX = "Which name would you have on yours?"
NOTE, NOTE_TT, PRICE = b.SHOW_NOTE, b.SHOW_NOTE_TT, b.SHOW_CTA
TAGS = ["horseracinggifts", "christmasbaubles", "personalisedbauble", "racingsilks", "christmasgifts"]
WHEN = "Not scheduled"
def show(key, name, hook, fact, fan, x, tt_title, yt_title, pin_title, pin, alt, card, tiktok):
    design = f"Design a personalised silks bauble with any horse's name at {SITE}."
    return dict(id=key, name=name, kind="merch", xmas=True, tiktok=tiktok, showcase=True, image=f"{key}-slide1.png", video=f"{key}-video.mp4",
                when={n: WHEN for n in ("instagram", "facebook", "x", "linkedin", "tiktok", "pinterest", "youtube")},
                hook=hook, story=f"{fact} {design} {NOTE}", story_fb=f"{fact} Design a personalised silks bauble with any horse's name on our website. {NOTE}",
                story_tt=f"{fact} Design a personalised silks bauble with any horse's name. {NOTE_TT}",
                prompt=fan, cta=PRICE, cta_fb=PRICE, question=Q, web=WEB, tags=TAGS, x=x, link=DESIGNER, tt_title=tt_title, yt_title=yt_title,
                yt=f"{fact} Design a personalised silks bauble with any horse's name at {SITE}.", pin_title=pin_title, pin=pin, alt=alt, card=card)
POSTS = [
 show("ombudsman", "Ombudsman showcase bauble",
      "With talk of Ombudsman retiring soon, why not hang him on your tree this Christmas? 🎄🏇",
      "Royal blue silks, a white cap and his name, hanging on a frosty branch.", "Send this to an Ombudsman fan.",
      f"With talk of Ombudsman retiring soon, why not hang him on your tree this Christmas? 🎄🏇 A showcase design. {QX} #ChristmasBaubles #HorseRacing",
      "Hang your favourite horse on the tree 🎄 Personalised silks bauble", "Personalised Racehorse Name Christmas Bauble 🎄",
      "Personalised Racehorse Name Christmas Bauble - Racing Silks Gift",
      "A personalised silks bauble with your favourite horse's name. This showcase design carries Ombudsman; yours can carry any name, in any of 25 silks patterns and any colours. Round ceramic, about 7.5 cm, with a ribbon. A Christmas gift for horse racing fans.",
      "Showcase racing silks Christmas bauble in blue with a white cap and the name Ombudsman, hanging from a frosted branch at a snowy racecourse",
      "Ombudsman retiring? Put him on your tree this Christmas.", True),
 show("lossiemouth", "Lossiemouth showcase bauble",
      "Is Lossiemouth the best jumps mare ever? 🎄🏇 Here she is on a Christmas bauble.",
      "Four Cheltenham Festivals, and never beaten there. Green silks, pink spots and her name on the tree.", "Send this to a Lossiemouth fan.",
      f"Is Lossiemouth the best jumps mare ever? 🎄🏇 Four Cheltenham Festivals, never beaten there. A showcase bauble. {QX} #ChristmasBaubles #HorseRacing",
      "Her silks on the Christmas tree 🎄 Personalised silks bauble", "Horse Racing Christmas Bauble: Lossiemouth Showcase 🎄",
      "Horse Racing Christmas Bauble - Personalised Racing Silks and Any Horse's Name",
      "A personalised silks bauble with any horse's name. This showcase design carries Lossiemouth in green with pink spots; yours can carry any name, in any of 25 silks patterns and any colours. Round ceramic, about 7.5 cm, with a ribbon. A Christmas gift for jumps racing fans.",
      "Showcase racing silks Christmas bauble in green with pink spots and the name Lossiemouth, hanging on a lit Christmas tree",
      "Best jumps mare ever? Four Festivals. Never beaten there.", True),
 show("no-drama-this-end", "No Drama This End showcase bauble",
      "The next big chaser? 🎄🏇 No Drama This End, on a horse racing Christmas bauble.",
      "A Grade 1 novice hurdler last season, and now he's gone over fences. Navy and white hoops, a red cap and his name.", "Send this to someone who follows the novice chasers.",
      f"The next big chaser? 🎄🏇 No Drama This End: a Grade 1 hurdler, now over fences. A showcase bauble. {QX} #ChristmasBaubles #HorseRacing",
      "Navy and white hoops on the tree 🎄 Personalised silks bauble", "Horse Racing Christmas Bauble: No Drama This End 🎄",
      "Jumps Racing Christmas Bauble - Personalised Racing Silks and Any Horse's Name",
      "A personalised silks bauble with any horse's name. This showcase design carries No Drama This End in navy and white hoops with a red cap; yours can carry any name, in any of 25 silks patterns and any colours. Round ceramic, about 7.5 cm, with a ribbon. A Christmas gift for jumps racing fans.",
      "Showcase racing silks Christmas bauble in navy and white hoops with a red cap and the name No Drama This End, hanging from a frosted branch at a snowy racecourse",
      "The next big chaser? A Grade 1 hurdler, now over fences.", True),
 show("jon-bon", "Jon Bon showcase bauble",
      "Britain's best chaser? 🎄🏇 Jon Bon's green and yellow hoops, on a horse racing Christmas bauble.",
      "Three Shloer Chases in a row at Cheltenham. Not many do that.", "Send this to the two-mile chase fan in your life.",
      f"Britain's best chaser? 🎄🏇 Three Shloer Chases in a row. Green and yellow hoops on a showcase bauble. {QX} #ChristmasBaubles #HorseRacing",
      "Green and yellow hoops on the tree 🎄 Personalised silks bauble", "Horse Racing Christmas Bauble: Green and Yellow Hoops 🎄",
      "Green and Yellow Hoops Christmas Bauble - Personalised Racing Silks, Any Name",
      "A personalised silks bauble with any horse's name. This showcase design carries Jon Bon in green and yellow hoops with a white cap; yours can carry any name, in any of 25 silks patterns and any colours. Round ceramic, about 7.5 cm, with a ribbon. A Christmas gift for jumps racing fans.",
      "Showcase racing silks Christmas bauble in green and yellow hoops with a white cap and the name Jon Bon, hanging from a frosted branch at a snowy racecourse",
      "Britain's best chaser? Three Shloer Chases in a row.", True),
 show("billy", "Billy silks bauble",
      "Champion jockey Billy 🎄🏇 A personalised horse racing Christmas bauble for the fan in your life.",
      "The youngest champion jockey in over 100 years deserves a spot on the tree. Yellow silks, black spots and a black cap.", "Send this to a Billy you know.",
      f"Champion jockey Billy 🎄🏇 The youngest champion in over 100 years, on a showcase silks bauble. {QX} #ChristmasBaubles #HorseRacing",
      "A silks bauble for the Billy in your life 🎄", "Personalised Jockey Silks Christmas Bauble 🎄",
      "Personalised Jockey Silks Christmas Bauble - Any Name, Any Racing Colours",
      "A personalised silks bauble with any name. This showcase design carries Billy in yellow with black spots and a black cap; yours can carry any name, in any of 25 silks patterns and any colours. Round ceramic, about 7.5 cm, with a ribbon. A Christmas gift for horse racing fans.",
      "Showcase racing silks Christmas bauble in yellow with black spots and the name Billy, hanging on a lit Christmas tree",
      "Champion jockey Billy. Youngest in over 100 years.", True),
 show("constitution-hill-green", "Constitution Hill showcase bauble (racing green)",
      "Is Constitution Hill the most popular horse ever? 🎄🏇 Here he is on a racing green Christmas bauble.",
      "He pulls a crowd wherever he goes. Come on Conny!", "Send this to a Conny fan.",
      f"Is Constitution Hill the most popular horse ever? 🎄🏇 Pulling crowds wherever he goes. A showcase bauble. Come on Conny! {QX} #ChristmasBaubles #HorseRacing",
      "The most popular horse ever? 🎄 Personalised silks bauble", "Horse Racing Christmas Bauble: Constitution Hill 🎄",
      "Racing Green Christmas Bauble - Personalised Racehorse Name and Silks",
      "A personalised racing green bauble with any horse's name. This showcase design carries Constitution Hill with his white silks and black cap; yours can carry any name and any silks. Round ceramic, about 7.5 cm, with a ribbon. A Christmas gift for horse racing fans.",
      "Showcase racing green Christmas bauble with white silks, a black cap and the name Constitution Hill, hanging from a frosted branch at a snowy racecourse",
      "Most popular horse ever? Pulling crowds wherever he goes.", True),
 show("constitution-hill-white", "Constitution Hill showcase bauble (white)",
      "Is this the most popular horse ever? 🎄🏇 Constitution Hill's white silks and black cap, on a Christmas bauble.",
      "He pulls a crowd wherever he goes, and now he's on the tree. Come on Conny!", "Send this to a Conny fan.",
      f"Is this the most popular horse ever? 🎄🏇 Constitution Hill's white silks and black cap on a showcase bauble. Come on Conny! {QX} #ChristmasBaubles #HorseRacing",
      "Your favourite horse on the Christmas tree 🎄 Personalised silks bauble", "Personalised Racing Silks Christmas Bauble 🎄",
      "White Silks and Black Cap Christmas Bauble - Personalised Racehorse Name",
      "A personalised silks bauble with any horse's name. This showcase design carries Constitution Hill in white silks with a black cap; yours can carry any name, in any of 25 silks patterns and any colours. Round ceramic, about 7.5 cm, with a ribbon. A Christmas gift for horse racing fans.",
      "Showcase racing silks Christmas bauble in white with a black cap and the name Constitution Hill, hanging on a lit Christmas tree",
      "Most popular horse ever? Pulling crowds wherever he goes.", True),
]
s = dict(b.POSTS[0]); s.update(id="silks-bauble", image="silks-bauble-slide1.png", video="silks-bauble-video.mp4", question=Q,
    when={n: WHEN for n in ("instagram", "facebook", "x", "linkedin", "tiktok", "pinterest", "youtube")},
    x=f"Personalised horse racing Christmas bauble 🎄🏇 Their racing silks, on the tree. 25 patterns, any colours, any name. {QX} #ChristmasBaubles #HorseRacing",
    alt="Personalised racing silks Christmas bauble, red with white stars and the name Snow Dancer, hanging above a candlelit table",
    yt_title="Personalised Horse Racing Christmas Bauble 🎄", yt="25 silks patterns, any colours, any name: theirs, the horse's or the syndicate's. Search ZANSRacingTools on Etsy.",
    card="Their silks, on the tree. Any colours, any name.")
POSTS.append(s)
def main():
    batch = []
    for p in POSTS:
        if not p["tiktok"]: p = dict(p, tt_title="")
        built = b.build(p)
        if not p["tiktok"]: built["networks"].pop("tiktok", None)
        built["networks"]["youtube"] = dict(title=p["yt_title"], when=WHEN,
            text=b.join(p["hook"], p["yt"], p["question"], XMAS, "#Shorts #HorseRacing #ChristmasGifts"))
        built["on_image"] = {"t": "bauble", "headline": "", "card": p["card"], "question": QX, "end": "Wishing you a Merry Christmas. Buy now. www.zanshorseracing.co.uk"}
        batch.append(built)
    (HERE / "batch.json").write_text(json.dumps(batch, indent=1, ensure_ascii=False), encoding="utf-8")
    md = ["# Captions: 8 Christmas bauble videos (18 Nov 2026)", "", "Nothing here is booked. Every post needs Alex's yes first.", ""]
    for x in batch:
        md += [f"## {x['name']} · `{x['video']}`", "", f"Alt text: {x['alt']}", ""]
        if "tiktok" not in x["networks"]: md += ["TikTok: not for TikTok (the hook mentions racing results; Strike Shield).", ""]
        for net, d in x["networks"].items():
            md += [f"### {net}", ""]
            if d.get("title"): md += [f"Title: {d['title']}", ""]
            md += ["```", d["text"], "```", ""]
            for extra in ("first_comment", "reply", "link"):
                if extra in d: md += [f"{extra.replace('_', ' ').capitalize()}: {d[extra]}", ""]
    (HERE / "CAPTIONS.md").write_text("\n".join(md), encoding="utf-8")
    (HERE / "CAPTIONS.txt").write_text("\n".join(l for l in md if l != "```").replace("### ", "--- ").replace("## ", "\n==== ").replace("# ", ""), encoding="utf-8")
    print(len(batch), "posts,", sum(len(x["networks"]) for x in batch), "network cuts")
if __name__ == "__main__":
    main()
