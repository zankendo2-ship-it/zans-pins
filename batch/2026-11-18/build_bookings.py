"""Builds the Metricool booking payloads for the 8 approved bauble posts (Alex approved them 18 Nov 2026).
One post a day, late afternoon UK time. Writes batch/2026-11-18/bookings.json. No keys or IDs of ours in here."""
import json, pathlib
H = pathlib.Path(__file__).parent
RAW = "https://raw.githubusercontent.com/zankendo2-ship-it/zans-pins/claude/friendly-curie-wcq9xc/batch/2026-11-18/brand-voice/"
BOARD = "1105211633496239725"
ORDER = [("2026-11-18", "silks-bauble"), ("2026-11-19", "ombudsman"), ("2026-11-20", "constitution-hill-white"), ("2026-11-21", "billy"),
         ("2026-11-22", "lossiemouth"), ("2026-11-23", "no-drama-this-end"), ("2026-11-24", "constitution-hill-green"), ("2026-11-25", "jon-bon")]
SLOT = {"youtube": "16:00", "pinterest": "16:30", "linkedin": "16:30", "facebook": "17:00", "twitter": "17:00", "instagram": "18:00", "story": "18:05", "tiktok": "18:00"}
posts = {p["id"]: p for p in json.load(open(H / "batch.json"))}
out = []
for day, key in ORDER:
    p = posts[key]; n = p["networks"]; vid = RAW + p["video"]
    def base(net, text, slot=None, **extra):
        t = f"{day}T{SLOT[slot or net]}:00"
        info = dict(autoPublish=True, draft=False, text=text, firstCommentText="", media=[vid], mediaAltText=[p["alt"]],
                    providers=[{"network": net}], publicationDate={"dateTime": t, "timezone": "Europe/London"}, shortener=False, smartLinkData={"ids": []}, descendants=[])
        info.update(extra)
        return dict(key=key, net=slot or net, date=t + "+00:00", info=info)
    out.append(base("youtube", n["youtube"]["text"], youtubeData=dict(title=n["youtube"]["title"], type="short", privacy="public", category="PEOPLE_BLOGS", madeForKids=False, isAiGeneratedContent=False)))
    out.append(base("pinterest", n["pinterest"]["text"], pinterestData=dict(boardId=BOARD, pinTitle=n["pinterest"]["title"], pinLink=n["pinterest"]["link"], pinNewFormat=False, isAiGenerated=False, isAiGeneratedPerson=False)))
    out.append(base("linkedin", n["linkedin"]["text"], linkedinData=dict(previewIncluded=True, type="post")))
    out.append(base("facebook", n["facebook"]["text"], firstCommentText=n["facebook"]["first_comment"], facebookData=dict(type="POST")))
    tw = base("twitter", n["x"]["text"], twitterData={})
    tw["info"]["descendants"] = [dict(text=n["x"]["reply"], providers=[{"network": "twitter"}], twitterData={}, media=[], autoPublish=True, draft=False,
                                      publicationDate=tw["info"]["publicationDate"])]
    out.append(tw)
    out.append(base("instagram", n["instagram"]["text"], instagramData=dict(type="REEL", showReelOnFeed=True, isAiGenerated=False)))
    st = base("instagram", "", slot="story", instagramData=dict(type="STORY", isAiGenerated=False)); st["info"]["mediaAltText"] = []
    out.append(st)
    out.append(base("tiktok", n["tiktok"]["text"], tiktokData=dict(title=n["tiktok"]["title"], privacyOption="PUBLIC_TO_EVERYONE", commercialContentOwnBrand=True, isAigc=False)))
json.dump(out, open(H / "bookings.json", "w"), ensure_ascii=False, indent=1)
print(len(out), "bookings")
