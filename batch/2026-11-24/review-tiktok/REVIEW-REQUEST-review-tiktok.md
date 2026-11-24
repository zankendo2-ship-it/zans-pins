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

## JOINT FIXES round 2 (9d415e8), same file name v3
- [x] BUY NOW button removed from the end card; "LINK IN BIO" sits in its place above the website.
- [x] "FOR MUM AND DAD" is on one line, clear of the photo.
Note: the end card in this video now differs from the locked Santa end card (which carries BUY NOW). That is a change to Alex's locked layout for this one TikTok and needs his yes.

## v4 after JOINT VERDICTS 3dd202e
File: `ETSY-REVIEW-five-stars-TIKTOK-v4-DRAFT.mp4` (21.7 s, native 9:16). Frames: `ETSY-REVIEW-TIKTOK-v4-frames.png`. v3 kept for comparison.
- [x] URL removed from the end card; it reads "WISHING YOU A MERRY CHRISTMAS / LINK IN BIO" only. No BUY NOW.
- [x] The buyer's photo is gone from every scene, and with it the DAD green-and-gold hoops and the boxes.
- [x] Our own MUM bauble photo: a new FLUX tree scene with a blank disc (tree recipe, word for word, seed 186175725; blank kept as `templates/scenes/pool/disc-tree-bells-blank.webp`), printed with the website designer's own artwork by `mapart2.py`. Design code read back from the designer: `ZBB-spot_diag-FFFFFF-C8102E-plain-C8102E`, name MUM (white jersey, three red spots, red cap, on racing green). Scene: `templates/scenes/mum-green-tree-bells.png`.
- [x] "FOR MUM AND DAD" is now "PERSONALISED FOR THEM", one line.
- [x] No boxes or packaging anywhere.
Scenes: review (stars and the quote, word for word) 0 to 4.7 s; Snow Dancer on the tree to 7.8 s; design preview to 10.8 s; MUM bauble on the tree to 18 s; end card.
Voice: the old line about Dad and Mum is dropped. New Aoede clips, each transcribed and matching: "Here it is, on the tree!", "Any colours. Any name.", "Personalised, just for them!"; then the approved "Which name would you have on yours? / Tell us in the comments!" and "Wishing you a Merry Christmas!". Same music.
Weak points: scene 1 is words on green with no picture for 4.7 s; white with red spots on the MUM jersey is a made-up example and I have not checked it against any register; the end card is no longer Alex's locked end card (no BUY NOW, no URL), which needs his yes.

## v5 after JOINT VERDICTS f8414d4. FIXES DONE.
File: `ETSY-REVIEW-five-stars-TIKTOK-v5-DRAFT.mp4` (18.7 s). Frames: `ETSY-REVIEW-TIKTOK-v5-frames.png`.
- [x] Product on screen from the first frame: the Snow Dancer bauble on the tree sits under the stars and the quote, which stay on a dark band and readable. The separate "ON THE TREE" scene and its voice line are dropped, so no picture repeats.
- [x] "DESIGN EXAMPLE" label on the MUM tree scene.
- [x] End card unchanged from v4 (Merry Christmas, LINK IN BIO).
Scenes: review over the bauble 0 to 4.7 s; design preview to 7.7 s; MUM design example to 14.9 s; end card.

## ADD-ON d97115e. FIXES DONE.
- [x] Scene 1 line "Verified Etsy Buyer" now reads "Etsy review ★★★★★". DESIGN EXAMPLE stays on the MUM scene.
- CORRECTION to everything above in this file: the boxed DAD and MUM picture is NOT the buyer's photo. It is our own listing photo 1 for the racing green bauble (4611213915), which Etsy shows beside the review. Wherever this file says "the buyer's photo", read "our listing photo shown with the review". It is no longer used in the video.

## v6 after JOINT FIXES 97b65de. FIXES DONE.
File: `ETSY-REVIEW-five-stars-TIKTOK-v6-DRAFT.mp4` (18.7 s). Frames: `ETSY-REVIEW-TIKTOK-v6-frames-plus-tiger-roll-scene-1.png` (first four frames).
- [x] Scene 1 no longer uses the SNOW DANCER bauble. It shows the green MUM bauble on the tree (the racing green listing's own design, printed from the website designer's artwork), labelled DESIGN EXAMPLE, under the stars and the quote.
- [x] So no picture repeats, the later product scene is a new one: a green GRANDAD bauble hanging at a snowy racecourse at twilight (twilight recipe word for word, seed 1667926286, blank kept as `templates/scenes/pool/disc-twilight-course-blank-2.webp`; design code read back from the designer `ZBB-hoops-F28C28-17806D-plain-17806D`, orange with teal hoops, teal cap, a made-up set). Also labelled DESIGN EXAMPLE. Scene file `templates/scenes/grandad-green-twilight-course.png`.
- The names on screen are MUM, YOUR HORSE and GRANDAD: no horse name, real or invented.
- Unchanged: "Etsy review ★★★★★" line, design preview scene, end card, voice clips, music.
Not done: the real listing photo was not used, because it shows the DAD bauble in green and gold hoops.

## v7: snow on the end card (TASK 65b8eeb, ORDER CHANGE 68054cc). FIXES DONE.
File: `ETSY-REVIEW-five-stars-TIKTOK-v7-snow-end-card-DRAFT-48k.mp4` (18.7 s, 48 kHz audio copied from the v6 -48k file). Frame: `ETSY-REVIEW-TIKTOK-v7-snow-end-card-frame.jpg`.
- [x] Snow falls down the screen on the end card only (from 14.75 s, fading in over 0.4 s), drawn by our own script; the metal strips sit on top of it. Scenes 1 to 3 are the v6 pictures, re-encoded once; sound untouched.
Booking: NOT booked. CLAUDE.md requires Alex's own yes for every TikTok post, and for booking; a relayed go-ahead does not meet that in this chat. I have asked Alex for one word. If he says yes here, I book TikTok, YouTube Short and Pinterest for today 18:15 UK and put the Metricool ids in STATUS.
Proposed captions (all carry the review word for word):
- TikTok: "Five stars on Etsy for our horse racing Christmas baubles 🎄 "Love this item for our Christmas tree." Which name would you have on yours? 👇 #horseracing #christmasbauble #racingsilks #personalisedgift #christmasgifts" / title "Five stars for our racing silks baubles 🎄"
- YouTube Short title: "Horse Racing Christmas Bauble: Five Star Etsy Review 🎄" / text: "A five-star Etsy review for our personalised horse racing Christmas baubles: "Love this item for our Christmas tree." Any colours, any name. Search ZANSRacingTools on Etsy. Wishing you a Merry Christmas 🎅 #Shorts #HorseRacing #ChristmasGifts"
- Pinterest title: "Horse Racing Christmas Bauble - Five Star Review, Personalised Racing Silks and Name" / description: "A five-star Etsy review for our personalised horse racing Christmas baubles: "Love this item for our Christmas tree." Racing silks and any name on a round ceramic bauble, about 7.5 cm, with a ribbon. A Christmas gift for Mum, Dad and racing fans. Wishing you a Merry Christmas 🎅" / link https://www.etsy.com/uk/listing/4611213915
