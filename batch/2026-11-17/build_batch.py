#!/usr/bin/env python3
"""Builds batch.json and CAPTIONS.md: one caption per network for each post."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE = "www.zanshorseracing.co.uk"
FOOTER = ("18+ Only. Begambleaware.org. Past track statistics do not guarantee future race outcomes. "
          "Insights are for informational and entertainment use only.")
XMAS = "Wishing you a Merry Christmas 🎅"
BIO = f"Link in bio 👉 {SITE}"
WEB_GIFTS = f"Visit {SITE} for horse racing gifts, the perfect present for Christmas 🎄"
WEB_GUIDES = f"Visit {SITE} for horse racing guides and gifts"
ETSY_SHOP = "https://www.etsy.com/uk/shop/ZANSRacingTools"
DESIGNER = f"https://{SITE}/bauble-designer/"
BAUBLE_CTA = f"Design yours at {SITE}/bauble-designer/ or search ZANSRacingTools on Etsy. Silks bauble Premium, £14.99."
BAUBLE_CTA_FB = "Design yours on our website or search ZANSRacingTools on Etsy. Silks bauble Premium, £14.99."
SHOW_CTA = "Silks bauble Premium, £14.99."
SHOW_NOTE = ("This one's a showcase, not a ready-made bauble. You pick the pattern, the colours and the name. "
             "We print yours.")
SHOW_NOTE_TT = "This one's a showcase. You pick the pattern, the colours and the name."

POSTS = [
 dict(id="post1", name="Silks bauble", kind="merch", xmas=True, tiktok=True, image="post1-silks-bauble.png",
      when={"facebook": "Tue 17 Nov 20:00", "x": "Tue 17 Nov 20:15", "linkedin": "Tue 17 Nov 20:15",
            "instagram": "Tue 17 Nov 20:30", "tiktok": "Tue 17 Nov 20:30", "pinterest": "Tue 17 Nov 20:45"},
      hook="Personalised horse racing Christmas bauble 🎄🏇 Their racing silks, on the tree.",
      story=("Every syndicate has one. The member who is impossible to buy for. Sorted: 25 silks patterns, any "
             "colours, any name. Theirs, the horse's or the syndicate's. Round ceramic, about 7.5 cm, printed both "
             "sides, with a ribbon."),
      story_tt=("Every syndicate has one. The member who is impossible to buy for. Sorted: 25 silks patterns, any "
                "colours, any name. Theirs, the horse's or the syndicate's."),
      prompt="Send this to whoever buys the syndicate presents.", cta=BAUBLE_CTA, cta_fb=BAUBLE_CTA_FB,
      question="Whose name would you hang on the tree? 👇", web=WEB_GIFTS,
      tags=["horseracinggifts", "christmasbaubles", "personalisedbauble", "racingsilks", "christmasgifts"],
      x=("Personalised horse racing Christmas bauble 🎄🏇 Their racing silks, on the tree. 25 patterns, any colours, "
         "any name. Whose name would you hang on yours? #ChristmasBaubles #HorseRacing"),
      link="https://www.etsy.com/uk/listing/4611232428", tt_title="Their racing silks, on the Christmas tree 🎄🏇",
      pin_title="Personalised Horse Racing Christmas Bauble - Racing Silks and Any Name",
      pin=("Personalised horse racing Christmas bauble in their own racing silks. Pick from 25 silks patterns, choose "
           "the colours and add any name: theirs, their horse's or the syndicate's. Printed the same on both sides of a "
           "round ceramic bauble, about 7.5 cm, with a ribbon. A Christmas gift for racing fans, owners and syndicates."),
      alt="Personalised racing silks Christmas bauble, red with white stars and the name Snow Dancer, hanging on a Christmas tree"),
 dict(id="post2", name="Ombudsman showcase bauble", kind="merch", xmas=True, tiktok=True, showcase=True,
      image="post2-ombudsman-showcase.png",
      when={"instagram": "Wed 18 Nov 08:00", "facebook": "Wed 18 Nov 08:30", "x": "Wed 18 Nov 09:00",
            "linkedin": "Wed 18 Nov 09:00", "tiktok": "Wed 18 Nov 09:30", "pinterest": "Wed 18 Nov 10:30"},
      hook="With talk of Ombudsman retiring soon, why not hang him on your tree this Christmas? 🎄🏇",
      story=f"Design a personalised silks bauble with your favourite horse's name at {SITE}. {SHOW_NOTE}",
      story_fb=f"Design a personalised silks bauble with your favourite horse's name on our website. {SHOW_NOTE}",
      story_tt=f"Design a personalised silks bauble with your favourite horse's name. {SHOW_NOTE_TT}",
      prompt="Send this to an Ombudsman fan.", cta=SHOW_CTA, cta_fb=SHOW_CTA, question="", web=WEB_GIFTS,
      tags=["horseracinggifts", "christmasbaubles", "personalisedbauble", "racingsilks", "horseracing"],
      x=("With talk of Ombudsman retiring soon, why not hang him on your tree this Christmas? 🎄🏇 A showcase design: "
         "yours can carry any horse's name. #ChristmasBaubles #HorseRacing"),
      link=DESIGNER, tt_title="Hang your favourite horse on the tree 🎄 Personalised silks bauble",
      pin_title="Personalised Racehorse Name Christmas Bauble - Racing Silks Gift",
      pin=("A personalised silks bauble with your favourite horse's name. This showcase design carries Ombudsman; "
           "yours can carry any name, in any of 25 silks patterns and any colours. Round ceramic, about 7.5 cm, with a "
           "ribbon. A Christmas gift for horse racing fans."),
      alt="Showcase racing silks Christmas bauble in blue with the name Ombudsman, hanging on a Christmas tree"),
 dict(id="post3", name="Kempton 6f draw sheet (all-weather)", kind="betting", xmas=False, tiktok=False,
      image="post3-kempton-draw.png",
      when={"pinterest": "Wed 18 Nov 12:30", "facebook": "Wed 18 Nov 13:00", "x": "Wed 18 Nov 15:00",
            "linkedin": "Wed 18 Nov 17:00", "instagram": "Wed 18 Nov 19:00"},
      hook="Kempton draw bias over 6 furlongs 🏇 One for the all-weather regulars.",
      story=("Six furlongs at Kempton, and the stalls matter. We went through 639 all-weather races since 2019. "
             "Lowest third of the stalls: about 1 in 7 won (14.6% of 1,839 runners). Highest third: about 1 in 14 "
             "(7.1% of 2,256). Low draws also had 11% more winners than their odds suggested. Drawn wide and "
             "you've got work to do."),
      prompt="Save this before your next night at Kempton.",
      cta=("It's from the work behind our Kempton Track DNA guide, coming soon. Make finding a winner a little "
           "easier. Follow us so you don't miss it."),
      question="Low draw or high draw over 6f at Kempton: where do you want to be? 👇",
      data="Data: Kempton all-weather, Jan 2019 to Oct 2026, races with 6 or more runners, ZANS results database.",
      web=WEB_GUIDES,
      tags=["kempton", "horseracing", "allweatherracing", "drawbias", "racecourseguide"],
      x=("Kempton draw bias over 6f 🏇 639 all-weather races since 2019: the lowest third of the stalls won about "
         "1 in 7, the highest third about 1 in 14. Low draw or high draw over 6f at Kempton: where do you want to "
         "be? #Kempton #HorseRacing"),
      x_reply="Our Kempton Track DNA guide is coming soon. Make finding a winner a little easier.",
      link=ETSY_SHOP,
      pin_title="Kempton Draw Bias Cheat Sheet - 6 Furlong Stall Stats from 639 All-Weather Races",
      pin=("Kempton draw bias over 6 furlongs, from 639 all-weather races since 2019. The lowest third of the stalls "
           "won about 1 in 7, the middle third about 1 in 10 and the highest third about 1 in 14. Save this before "
           "your next night at Kempton. The ZANS Kempton Track DNA racecourse guide is coming soon."),
      alt="Kempton 6 furlong draw bias cheat sheet: low stalls 1 in 7, middle stalls 1 in 10, high stalls 1 in 14, from 639 all-weather races since 2019"),
 dict(id="post4", name="Lossiemouth showcase bauble", kind="merch", xmas=True, tiktok=True, showcase=True,
      image="post4-lossiemouth-showcase.png",
      when={"instagram": "Thu 19 Nov 08:00", "facebook": "Thu 19 Nov 08:30", "x": "Thu 19 Nov 09:00",
            "linkedin": "Thu 19 Nov 09:00", "tiktok": "Thu 19 Nov 09:30", "pinterest": "Thu 19 Nov 10:30"},
      hook="Who wouldn't want Lossiemouth on their Christmas tree? 🎄🏇",
      story=f"Customise your own silks bauble with any horse's name at {SITE}. {SHOW_NOTE}",
      story_fb=f"Customise your own silks bauble with any horse's name on our website. {SHOW_NOTE}",
      story_tt=f"Customise your own silks bauble with any horse's name. {SHOW_NOTE_TT}",
      prompt="Send this to a Lossiemouth fan.", cta=SHOW_CTA, cta_fb=SHOW_CTA, question="", web=WEB_GIFTS,
      tags=["horseracinggifts", "christmasbaubles", "personalisedbauble", "racingsilks", "jumpracing"],
      x=("Who wouldn't want Lossiemouth on their Christmas tree? 🎄🏇 A showcase design: yours can carry any horse's "
         "name. #ChristmasBaubles #HorseRacing"),
      link=DESIGNER, tt_title="Your favourite horse on the Christmas tree 🎄 Personalised silks bauble",
      pin_title="Personalised Horse Name Christmas Bauble in Racing Silks - Gift for Racing Fans",
      pin=("Customise your own silks bauble with any horse's name. This showcase design carries Lossiemouth; yours can "
           "carry any name, in any of 25 silks patterns and any colours. Round ceramic, about 7.5 cm, with a ribbon. "
           "A Christmas gift for horse racing fans."),
      alt="Showcase racing silks Christmas bauble in pink with light green spots and the name Lossiemouth, hanging on a Christmas tree"),
 dict(id="post5", name="All-weather guides coming soon", kind="betting", xmas=False, tiktok=False,
      image="post5-all-weather-coming-soon.png",
      when={"pinterest": "Thu 19 Nov 12:30", "facebook": "Thu 19 Nov 13:00", "x": "Thu 19 Nov 15:00",
            "linkedin": "Thu 19 Nov 17:00", "instagram": "Thu 19 Nov 19:00"},
      hook="All-weather racing guides are coming 🏇 Kempton, Southwell, Wolverhampton and Newcastle.",
      story=("Winter's here and the floodlights are on. We've been through 14,736 all-weather races since 2019 to "
             "build four Track DNA guides: 4,739 at Wolverhampton, 3,521 at Newcastle, 3,454 at Kempton and 3,022 at "
             "Southwell. That's a lot of cold Tuesday nights."),
      prompt="Send this to your all-weather racing mate.",
      cta=("Make finding a winner a little easier. Beginner, Advanced and Pro editions for each track. Follow us so "
           "you don't miss the first one."),
      question="Which all-weather track do you want first? 👇", web=WEB_GUIDES,
      tags=["allweatherracing", "horseracing", "kempton", "wolverhampton", "racecourseguide"],
      x=("Coming soon 🏇 Track DNA guides for Kempton, Southwell, Wolverhampton and Newcastle, built from 14,736 "
         "all-weather races since 2019. Which all-weather track do you want first? #HorseRacing #AllWeather"),
      x_reply="Beginner, Advanced and Pro editions for each track. Make finding a winner a little easier.",
      link=ETSY_SHOP,
      pin_title="All-Weather Racecourse Guides Coming Soon - Kempton, Southwell, Wolverhampton, Newcastle",
      pin=("Coming soon: ZANS Track DNA racecourse guides for Kempton, Southwell, Wolverhampton and Newcastle, built "
           "from 14,736 all-weather races since 2019. Beginner, Advanced and Pro editions for each track: 4,739 races at "
           "Wolverhampton, 3,521 at Newcastle, 3,454 at Kempton and 3,022 at Southwell."),
      alt="Coming soon: ZANS Track DNA guides for Kempton, Southwell, Wolverhampton and Newcastle, with the number of races studied at each"),
 dict(id="post6", name="Syndicate and owner bauble reminder", kind="merch", xmas=True, tiktok=True,
      image="post6-syndicate-reminder.png",
      when={"instagram": "Fri 20 Nov 08:00", "facebook": "Fri 20 Nov 08:30", "x": "Fri 20 Nov 09:00",
            "linkedin": "Fri 20 Nov 09:00", "tiktok": "Fri 20 Nov 09:30", "pinterest": "Fri 20 Nov 10:30"},
      hook="Racehorse syndicate Christmas gift 🎄🏇 35 days to Christmas and counting.",
      story=("One bauble for every owner in the syndicate. Your silks, your horse's name, on every tree. Pick from 25 "
             "silks patterns and choose your colours. Round ceramic, about 7.5 cm, printed both sides, with a ribbon."),
      story_tt=("One bauble for every owner in the syndicate. Your silks, your horse's name, on every tree. Pick from "
                "25 silks patterns and choose your colours."),
      prompt="Send this to your syndicate group chat.", cta=BAUBLE_CTA, cta_fb=BAUBLE_CTA_FB,
      question="How many are in your syndicate? 👇", web=WEB_GIFTS,
      tags=["racehorsesyndicate", "racehorseowner", "horseracinggifts", "christmasbaubles", "personalisedbauble"],
      x=("35 days to Christmas 🎄🏇 One bauble for every owner in the syndicate, in your silks with your horse's name. "
         "How many are in your syndicate? #HorseRacing #ChristmasBaubles"),
      link="https://www.etsy.com/uk/listing/4611232428", tt_title="35 days to Christmas 🎄 One bauble for every syndicate member",
      pin_title="Racehorse Syndicate Christmas Gift - Personalised Silks Bauble for Owners",
      pin=("A Christmas gift for racehorse syndicates and owners: one bauble for every member, in your silks with your "
           "horse's name. Pick from 25 silks patterns and choose your colours. Round ceramic, about 7.5 cm, with a "
           "ribbon, printed the same on both sides."),
      alt="Racing silks Christmas bauble in green and yellow hoops with the name Lucky Seven, hanging on a Christmas tree"),
]


def join(*parts):
    return "\n\n".join(p for p in parts if p)


def tags(post, n):
    return " ".join("#" + t for t in post["tags"][:n])


def build(post):
    betting, xmas = post["kind"] == "betting", post["xmas"]
    foot = FOOTER if betting else ""
    body = [post["hook"], post["story"], post["prompt"], post["cta"], post["question"], post.get("data", "")]
    fb_body = [post["hook"], post.get("story_fb", post["story"]), post["prompt"], post.get("cta_fb", post["cta"]),
               post["question"], post.get("data", "")]
    nets = {
        "instagram": dict(text=join(*body, post["web"], XMAS if xmas else "", foot, tags(post, 5), BIO)),
        "facebook": dict(text=join(*fb_body, XMAS if xmas else "", foot, tags(post, 3)),
                         first_comment=f"{'Design yours' if not betting else 'The ZANS guides'}: {post['link']}"),
        "x": dict(text=post["x"],
                  reply=" ".join(p for p in [post.get("x_reply", f"Design yours: {post['link']}"),
                                             XMAS if xmas else "", foot] if p)),
        "pinterest": dict(title=post["pin_title"], link=post["link"],
                          text=" ".join(p for p in [post["pin"], XMAS if xmas else "", foot] if p)),
        "linkedin": dict(text=join(*body, post["web"], XMAS if xmas else "", foot, tags(post, 3))),
    }
    if post["tiktok"]:
        nets["tiktok"] = dict(title=post["tt_title"],
                              text=join(post["hook"], post["story_tt"], post["question"], XMAS if xmas else "",
                                        tags(post, 5), BIO))
    for net, data in nets.items():
        data["when"] = post["when"][net]
    return dict(id=post["id"], name=post["name"], kind=post["kind"], christmas=xmas,
                showcase=post.get("showcase", False), image=post["image"], alt=post["alt"], networks=nets)


def main():
    on_image = json.loads((HERE / "on-image-text.json").read_text(encoding="utf-8"))
    batch = []
    for i, post in enumerate(POSTS, 1):
        built = build(post)
        built["on_image"] = on_image[f"p{i}"]
        batch.append(built)
    (HERE / "batch.json").write_text(json.dumps(batch, indent=1, ensure_ascii=False), encoding="utf-8")
    lines = ["# 6-post batch, 17 to 20 Nov 2026", "", "Nothing here is booked until Alex says yes. UK times.", ""]
    for b in batch:
        lines += [f"## {b['id']}: {b['name']} · `{b['image']}`", ""]
        for net, d in b["networks"].items():
            lines += [f"### {net} · {d['when']}", ""]
            if "title" in d:
                lines += [f"Title: {d['title']}", ""]
            lines += ["```", d["text"], "```", ""]
            for extra in ("first_comment", "reply", "link"):
                if extra in d:
                    lines += [f"{extra.replace('_', ' ').capitalize()}: {d[extra]}", ""]
    (HERE / "CAPTIONS.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(batch)} posts, {sum(len(b['networks']) for b in batch)} network cuts written")


if __name__ == "__main__":
    main()
