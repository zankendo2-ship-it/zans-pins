# REVIEW REQUEST: Etsy five-star review on TikTok (TASK 3dc4423), draft, not booked

File: `ETSY-REVIEW-five-stars-TIKTOK-DRAFT.mp4`, 1080x1920, 17.5 s. Built from the two slides Alex approved on 22 Nov (review card, then the locked Santa end card), padded to 9:16 in racing green with the metal strip top and bottom.

Voice (Aoede, locked style, each clip transcribed and matching):
1. "Five stars on Etsy! Love this item for our Christmas tree!" (the review is quoted word for word: "Love this item for our Christmas tree")
2. "Dad and Mum, each in their own racing silks. Thank you so much!"
3. "Which name would you have on yours?" / "Tell us in the comments!" (existing approved clips)
4. "Wishing you a Merry Christmas!" on the end card (existing approved clip)
Music: `batch/2026-11-17/music/4-celesta-jingle-bells.m4a` (our own, public-domain carol).

TikTok caption:
"Five stars on Etsy for our horse racing Christmas baubles 🎄 "Love this item for our Christmas tree." Which name would you have on yours? 👇 #horseracing #christmasbauble #racingsilks #personalisedgift #christmasgifts"
Title (under 90): "Five stars for our racing silks baubles 🎄"

Checks: real review, quoted exactly, no buyer name, nothing added; no price, odds, bet or race words; no 18+; gift post, so inside the Strike Shield; commercial-content own-brand toggle on; AI label off.
Weak points: the review card holds still for 13.7 s (only the voice moves it along), and it is 17.5 s, under the 25 s the new rulebook asks for story posts (it is a product post). Christmas music before 1 Dec: CLAUDE.md section 7 says Christmas music from 1 Dec, but the bauble posts already carry it; say if this should use the plain bed instead.

Proposed slots (for Alex's yes): Tue 24 Nov 12:30 Honeysuckle, 17:00 this review post, Tiger Roll to Wed 25 Nov 12:30, Constitution Hill bauble TikTok off Tuesday.


## UPDATE: strip size (note 2f22298)
The video keeps the 28px strip, which meets the settled size (about 2.4% of the short side = 26px on 1080). The 36px video strip I made first was too thick and is removed. Christmas cards with strips (4, 6, 7, 19) are raised from 26px to 36px.

## FIXES DONE after ADVICE a88143a: v2, native 9:16
File: `ETSY-REVIEW-five-stars-TIKTOK-v2-DRAFT.mp4` (17.5 s; v1 removed). Frames: `ETSY-REVIEW-TIKTOK-v2-frames.png`.
- [x] Native 1080x1920, no letterbox, one metal strip top and bottom (28px).
- [x] Opens on the bauble photo, full width, with a push-in from frame 1; the five gold stars and "FIVE STARS ON ETSY" land at 0.5 s.
- [x] No long still: photo scene 0 to 6 s, quote scene 6 to 13.7 s, tall green Santa end card to the end; each scene pushes in.
- Same voice clips, music and caption as v1.
Still true: the photo is the 762px crop from the review screenshot, shown at 1000px wide (slightly enlarged). The full-size original would be sharper.

## v3 after JOINT VERDICT d74a4cf
File: `ETSY-REVIEW-five-stars-TIKTOK-v3-DRAFT.mp4` (17.5 s, native 9:16; v2 removed). Frames: `ETSY-REVIEW-TIKTOK-v3-frames.png`.
- 0 to 2.5 s: five big stars and the review, word for word, with the buyer's photo.
- 2.5 to 6 s: the silks bauble on the tree by candlelight ("ON THE TREE").
- 6 to 9.5 s: a second design ("ANY COLOURS / ANY NAME").
- 9.5 to 13.7 s: the DAD and MUM baubles in their gift boxes ("BOXED TO GIVE", "DESIGN YOURS · LINK IN BIO").
- 13.7 s to end: the green Santa end card.
Fewer, bigger words on every scene; every scene pushes in. Same approved voice clips and music.
Not done: no new racecourse or people scenes; the two silks variations are our existing example designs (Snow Dancer and Your Horse), and the second is flat artwork in a circle, not a photographed bauble.

Also from the verdict: Christmas card 6 now reads "CHRISTMAS NOTICE · 25 DEC"; the order-by line is off the sample pin.
NOT done: the "ignore ChatGPT" line in CLAUDE.md is Alex's rule 12 and is changed only when Alex tells this chat himself. Honeysuckle and Tiger Roll revisions are not started.

## JOINT FIXES 85926b5 (23 Nov, 23:00 UTC), same file name v3
- [x] End card now carries "LINK IN BIO" under the website.
- [x] The second-design scene is labelled "DESIGN PREVIEW" (it is flat artwork, not a photographed bauble).
- [x] Packaging: I CANNOT confirm that baubles are sent in the kraft gift boxes shown in the buyer's photo; nothing in this repo says so. So the caption "BOXED TO GIVE" is removed and the scene now reads "FOR MUM AND DAD". The photo is still the buyer's own picture as shown on the review. If Alex confirms the box is standard, the line can come back.
- [x] Music rights: the bed is `batch/2026-11-17/music/4-celesta-jingle-bells.m4a`, made note by note by our own script `templates/music.py` from "Jingle Bells" (James Lord Pierpont, published 1857, public domain). No sample, recording or library track is used. The voice is our Gemini Aoede voice.
