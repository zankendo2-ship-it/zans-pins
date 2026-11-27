# ZANS Etsy SEO overhaul - all 26 listings, complete proposed replacement copy

Prepared 26 Nov 2026 (overnight) by the Etsy thread (Claude). **NOTHING HAS BEEN PUBLISHED TO ETSY.** Every change needs Alex's approval. Backup of the live copy: `UNDO_current_copy_all_26_listings_2026-11-26.json` (26 listings: title, tags, attributes, category, shipping, full description; read via Etsy API 26 Nov 21:15 UTC, zans-pins branch claude/project-thread-xwwh7g commit a44e81b2).

## 0. Honest status and limits
- **ChatGPT review (v4):** v1 REVISE (#26 7204216509); v2 structure PASS plus 4 fixes (7205130348); v3 structure PASS, copy REVISE (7206071406). v4 applies the two copy fixes (Cheltenham Advanced opening now "form and going analysis guide"; legacy "doesn't guarantee winners" bullet removed from Ascot Flat Advanced). v4 full-description coverage PASS, with one REVISE (7206221624): download wording (Etsy downloads are not in the app) and the cancellation wording; both applied in v5. v5 has not been re-reviewed. Status: PREPARED, NOT APPLIED. Full-description paid review: batch A (listings 1-13) on 27 Nov, batch B (14-26) on 28 Nov.
- **Keyword research limits:** Etsy search terms, volumes and competition data are not available to us (seller-only, not in the API; Etsy pages are blocked from this sandbox). Tags are built from (a) what each product genuinely is, (b) the live copy and the 23 Nov logged-out UK search baseline (ZANS ranks for silks/bauble/ornament and course-specific guide terms, not generic gift terms), (c) public UK gift-guide and racing-gift pages seen in web searches tonight (e.g. racing fan Christmas gift guides, racing club share gifts, 'gift for dad who likes horse racing', Father's Day racing gifts, personalised racing silks gifts). Every tag is a HYPOTHESIS, not a measured volume. Alex's Etsy Stats / Search Terms screenshots would let us prune.
- **Products that do not exist yet:** pom pom hats, hats, accessories, trainer-specific and Cheltenham Festival gifts other than the Cheltenham guides are not in the shop, so no listing copy was invented for them. 'Royal Ascot' is NOT used (shop rule: never as a tag; also a protected event name). Cheltenham Festival / Grand National appear only as race-meeting references already in the live copy.
- **Descriptions:** the live descriptions already hold the verified facts (page counts, race counts, sizes, delivery, returns). To avoid invented features, each new description = a rewritten keyword-led opening + the live body unchanged, plus a gift-ideas paragraph on Beginner guides and refreshed lead paragraphs on the 3 Christmas/owner gifts. The full text of every new description is below.
- **True controls (v2):** green bauble 4611213915 and Premium Silks Mug 4608193933: title and tags untouched. Ascot Flat Beginner 4601073843 and Cheltenham Jumps Advanced 4622511552: tags untouched (tag controls) but titles shortened to the shop word limit.
- **Etsy Ads / hold:** the growth thread notes a 30-day no-change window on the ad campaign from 23 Nov (to 1 Dec). Alex's call whether to apply before or after.

## 0a. ChatGPT review #1 fixes applied in this v2
1. Ascot Flat Beginner title cut from 17 to 12 words. 2. **Pro / Advanced restored in the title** of all 14 Pro/Advanced guides (<=14 words, no repeats). 3. 'For adults aged 18 and over' removed from all 19 guide descriptions. 4. Ascot Flat Advanced: the five named owners removed, generic wording. 5. 'stocking filler' removed from the silks bauble and Premium Silks Mug (Christmas) copy. 6. Green bauble description no longer says 'double gold ring' (final art has no rings). 7. 'not promise winners or profit' replaced everywhere with 'This guide is informational and does not make selections or guarantee future outcomes.' 8. Experiment design below; second Beginner tag now course/event-specific (first grand national, first jumps meeting, first kempton visit, first night racing, first festival visit, first ascot visit); 'gift for racing fan' kept as a test on 3 Beginner guides (Aintree, Sandown, Cheltenham) plus Cheltenham Advanced (unchanged control).

## 0a2. ChatGPT review #2 (v2) fixes applied in v3
1. 4601073843: 'beginner tips ... place your bets ... finding a winner' wording replaced with neutral course-data wording (Wave 0 compliance). 2. Advanced titles now lead with 'Form and Going Analysis' instead of 'Betting'; 'betting' tags in Advanced listings replaced with going/form-analysis tags, except the Cheltenham Advanced control (tags unchanged). No ranking claim is made; there is no search-term evidence either way, so this is a positioning choice. 3. Review metadata updated; status stays NOT APPLIED. 4. orchestrator/ZANS_RULES.md line 20 still allows 18+ on guides: reconcile to the #26 checklist (no 18+ in Etsy text) via a PR (see #41).

## 0b. Apply in waves (compliance separate from the SEO experiment)
- **Wave 0, compliance only (text, no SEO variable):** the description fixes above on every listing that has them (18+ line, neutral disclaimer, owner names, stocking filler, ring wording) plus the Ascot Flat Beginner and Cheltenham Advanced title shortening. Safe to apply together.
- **Wave 1, SEO test on low-view listings:** new titles + tags + openers on the zero-view guides (17 listings minus the Cheltenham Advanced control), Ascot Flat Pro (8 views) and Advanced (5 views), Cheltenham Beginner (1), Christmas mug (3) and white mug (7). One treatment per listing; measure views after 7 and 14 days.
- **Wave 2 (after wave 1 is read):** silks bauble 4611232428 tag swap (31 views).
- **Never touched:** green bauble 4611213915 and Premium Silks Mug 4608193933 (true controls: no tag or title change).
- The paid run is not required to apply any of this; applying always needs Alex's yes.

## 1. Validation (scripted)
- 26/26 listings pass: exactly 13 tags, all unique within the listing, each 20 characters or fewer, lower-case letters/numbers/spaces only, title 140 characters or fewer, title 14 words or fewer with no repeated words (live gift titles that are unchanged are exempt).
- Tag duplicates: within each course the Beginner / Advanced / Pro tag sets share only deliberately common words; generic phrases are rotated so each sits on at most ~3-4 listings. `horse racing gift` stays on every Beginner guide and gift (shop rule: untouched). 'racing for beginners' and 'first time racegoer' sit on all Beginner guides because they are the same buyer; accepted, flagged for ChatGPT.
- Accuracy: no numbers added except page counts and race meetings already in the live copy. No 'tips', winner or profit promises; no betting sites, owners or 'Royal Ascot'.

## 2. Shop-wide search coverage (new tags + titles)

| Search cluster | Listings covering it (of 26) | Notes |
|---|---|---|
| Horse racing gift / present | 13 | |
| Gift for racing fan | 6 | |
| Dad / mum / grandad | 1 | |
| Birthday | 0 | |
| Christmas / Secret Santa / xmas | 6 | |
| Owner / syndicate / racing club | 4 | |
| Trainer / yard | 1 | |
| Jockey / silks / colours | 14 | |
| Cheltenham Festival | 3 | |
| Grand National / Aintree | 3 | |
| Ascot | 6 | |
| Kempton / King George / Boxing Day | 6 | |
| Sandown / Tingle Creek | 3 | |
| Mug | 3 | |
| Bauble / ornament / tree | 5 | |
| Personalised | 4 | |
| Beginner / first-timer | 7 | |
| Form guide / betting / each way | 14 | |
| Statistics / data / ratings | 8 | |
| Day out / racegoer | 7 | |
| All-weather / Polytrack / floodlit | 3 | |
| National Hunt / jumps | 14 | |

Gaps we cannot fill honestly yet: pom pom hats, hats, hip flasks and other accessories (no such products), trainer-targeted designs, Cheltenham Festival gifts beyond the guides, non-Christmas gift occasions for the baubles (seasonal). Spelling variations (racing colours / colors, bauble / ornament / decoration, xmas / christmas) are covered across listings rather than repeated inside one.

## 3. Summary table

| ID | Type | Price | Views | Primary keyword | New title |
|---|---|---|---|---|---|
| 4623060095 | Advanced guide | £12.49 | 0 | aintree form guide pdf | Aintree Racecourse Guide PDF Advanced - Horse Racing Form and Going Analysis, Grand National |
| 4623059959 | Beginner guide | £7.49 | 0 | aintree racecourse guide for beginners | Aintree Racecourse Guide PDF for Beginners, Horse Racing Gift, Grand National, Instant Download |
| 4623069940 | Pro guide | £20.82 | 0 | aintree horse racing statistics | Aintree Racecourse Guide PDF Pro - 135-Page Horse Racing Statistics Book, Grand National, Download |
| 4604440668 | Advanced guide | £12.49 | 5 | ascot flat form guide pdf | Ascot Flat Racecourse Guide PDF Advanced - Horse Racing Form and Going Analysis, Download |
| 4601073843 | Beginner guide | £7.49 | 38 | ascot flat racecourse guide for beginners | Ascot Flat Racecourse Guide PDF for Beginners, Horse Racing Gift, Instant Download |
| 4604430033 | Pro guide | £20.82 | 8 | ascot flat horse racing statistics | Ascot Flat Racecourse Guide PDF Pro - 71-Page Horse Racing Statistics Book, Instant Download |
| 4622450389 | Advanced guide | £12.49 | 0 | ascot jumps form guide pdf | Ascot Jumps Racecourse Guide PDF Advanced - Horse Racing Form and Going Analysis, Download |
| 4622457762 | Beginner guide | £7.49 | 0 | ascot jumps racecourse guide for beginners | Ascot Jumps Racecourse Guide PDF for Beginners, Horse Racing Gift, Racegoer Basics, Download |
| 4622458108 | Pro guide | £20.82 | 0 | ascot jumps horse racing statistics | Ascot Jumps Racecourse Guide PDF Pro - 134-Page Horse Racing Statistics Book, Instant Download |
| 4622511552 | Advanced guide | £12.49 | 0 | cheltenham form guide pdf | Cheltenham Racecourse Guide PDF Advanced - Horse Racing Form and Going Analysis, Festival |
| 4622511316 | Beginner guide | £7.49 | 1 | cheltenham racecourse guide for beginners | Cheltenham Racecourse Guide PDF for Beginners, Horse Racing Gift, Festival Racegoers, Download |
| 4622511788 | Pro guide | £20.82 | 0 | cheltenham horse racing statistics | Cheltenham Racecourse Guide PDF Pro - 198-Page Horse Racing Statistics Book, Festival, Download |
| 4622635592 | Advanced guide | £12.49 | 0 | kempton all-weather form guide pdf | Kempton All-Weather Racecourse Guide PDF Advanced - Horse Racing Form and Going Analysis, Polytrack |
| 4622635374 | Beginner guide | £7.49 | 0 | kempton all-weather racecourse guide for beginners | Kempton All-Weather Racecourse Guide PDF for Beginners, Horse Racing Gift, Floodlit Evenings, Download |
| 4622627387 | Pro guide | £20.82 | 0 | kempton all-weather horse racing statistics | Kempton All-Weather Racecourse Guide PDF Pro - 119-Page Horse Racing Statistics Book, Polytrack, Download |
| 4622626437 | Advanced guide | £12.49 | 0 | kempton jumps form guide pdf | Kempton Jumps Racecourse Guide PDF Advanced - Horse Racing Form and Going Analysis, Download |
| 4622634750 | Beginner guide | £7.49 | 0 | kempton jumps racecourse guide for beginners | Kempton Park Racecourse Guide PDF for Beginners, Horse Racing Gift, King George, Instant Download |
| 4622635120 | Pro guide | £20.82 | 0 | kempton jumps horse racing statistics | Kempton Jumps Racecourse Guide PDF Pro - 132-Page Horse Racing Statistics Book, Instant Download |
| 4622672428 | Advanced guide | £12.49 | 0 | sandown park form guide pdf | Sandown Park Racecourse Guide PDF Advanced - Horse Racing Form and Going Analysis, Download |
| 4622672152 | Beginner guide | £7.49 | 0 | sandown park racecourse guide for beginners | Sandown Park Racecourse Guide PDF for Beginners, Horse Racing Gift, Tingle Creek, Instant Download |
| 4622672622 | Pro guide | £20.82 | 0 | sandown park horse racing statistics | Sandown Park Racecourse Guide PDF Pro - 115-Page Horse Racing Statistics Book, Instant Download |
| 4608193933 | Mug | £14.99 | 64 | jockey silks mug | Horse Racing Christmas Gift Mug, Premium Jockey Silks with Name, Racehorse Owner Syndicate Cup |
| 4611213915 | Bauble | £12.99 | 76 | racehorse ornament | Horse Racing Christmas Gift, Green & Gold Ornament with Name, Personalised Racehorse Tree Decoration |
| 4612435420 | Mug | £11.99 | 7 | white silks mug | Horse Racing Christmas Gift, Personalised White Silks Mug 11oz with Racehorse Name, Jockey Colours |
| 4611232428 | Bauble | £14.99 | 31 | jockey silks bauble | Horse Racing Christmas Gift, Premium Jockey Silks Bauble with Name, Personalised Racehorse Owner Ornament |
| 4609859882 | Mug | £14.99 | 3 | horse racing secret santa gift | Horse Racing Christmas Gift, Premium Silks Mug, Secret Santa, Personalised Racegoer Xmas Present |

## 4. The 26 listings, in full

### 1. 4623060095 - Advanced guide - Aintree Racecourse Guide PDF Advanced - Horse Racing Form and Going Analysis, Grand National
https://www.etsy.com/listing/4623060095  | £12.49 | 0 views lifetime | 0 favourites | section: Jumps Racecourse Guides

**BEFORE title (122):** Aintree Racecourse Guide PDF Advanced - Horse Racing Betting Form by Distance and Going, Instant Download, Jumps Track DNA
**AFTER title (92):** Aintree Racecourse Guide PDF Advanced - Horse Racing Form and Going Analysis, Grand National

**BEFORE tags:** aintree betting | aintree form guide | grand national form | grand national pdf | topham chase | becher chase form | aintree festival | jumps each way pdf | placepot form pdf | national hunt value | racecourse guide pdf | horse racing gift | gift for racing fan
**AFTER tags (13):** aintree form | aintree going guide | grand national form | becher chase form | horse racing form | going analysis pdf | each way guide pdf | horse racing value | racing going guide | form study pdf | trainer form guide | racing form guide | form analysis pdf
Tags kept 2, new 11.

**Primary keyword:** aintree form guide pdf
**Secondary keywords:** form analysis guide, horse racing form guide, each way guide pdf, racing going guide
**Extra phrases covered:** form study, value and over-bet, trainer form, course meeting hook
**Audience and why:** The racing follower who already goes to Aintree or backs horses there and searches for form, going and each-way study material. Own vocabulary (form, betting, going, each-way) so it does not compete with the Beginner gift listing or the Pro statistics listing.

**Category:** Books, Movies & Music > Books > Guides & How Tos (section: Jumps Racecourse Guides).
**Attributes now:** Primary color=Green; Secondary color=Purple; Self-published=Yes; Book format=eBook; Number of pages=36
**Attribute / category actions:** No change needed (category and attributes consistent with the product)

**FULL NEW DESCRIPTION (2785 characters):**

````text
Aintree form guide and horse racing form analysis PDF for the Grand National and Becher Chase meetings: value and over-bet points for each of the 9 main hurdle, chase and bumper distances, split by going (ground conditions), measured against the starting prices. Course data to help you know the track before the off. Includes a full colour version AND a black-and-white printable version. Digital file only, nothing is posted.

Each point shows how often that kind of horse won and whether it won more or less often than its odds said, tagged VALUE, AS PRICED, OVER-BET or LONGSHOT. It is different research from the Beginner edition, not a copy with extra pages. Figures are ZANS's own analysis of 388 Aintree jumps races, April 2019 to May 2026.

WHAT'S INSIDE (36 pages)
• Pick your distance, how the Advanced edition works, the course map and the going explained
• Every main distance: value and over-bet points, by going where there are enough races (23 pages)
• The price: where the odds were right and wrong
• Trainers and jockeys against the odds
• Smart money: outsider specialists and short-priced names
• The Placepot (a pool bet) and a race-day checklist
• Big-race winners' colours, 2025-26 and 2024-25
• Summary for every main distance, glossary

WHAT YOU GET
• One zip holding the colour PDF and the black-and-white print PDF, 36 pages each.

WHO IT'S FOR
Regular racegoers, each-way and Placepot players and form readers who know the basics and want value and price context at Aintree over jumps, the Grand National meeting included.

GOOD TO KNOW
• Instant download: after purchase, sign in to Etsy in a mobile browser or on a computer, then go to Purchases and download your files. On an iPhone, tap the zip in the Files app to open it.
• Two PDFs: a full colour version and a mainly black-and-white print version (jockey colours are kept in colour).
• Tick boxes on the distance-and-going pages and the race-day checklist can be tapped in compatible PDF apps, or print the guide and tick by hand.
• Information and entertainment only. This guide is informational and does not make selections or guarantee future outcomes.
• ZANS is not connected with or approved by Aintree Racecourse or any jockey, trainer or owner named.
• Maps, charts and jockey colours were drawn by ZANS with the help of AI design tools. All figures are ZANS's own analysis.

RETURNS
Digital download: if you agreed at checkout to start the download straight away, you may lose your 14-day right to cancel once the file is available. If a file won't open or isn't as described, message us and we'll fix it or refund you. This doesn't affect your statutory rights.

MORE FROM ZANS
Also available: the Aintree Jumps Beginner and Pro editions as separate listings, plus the Sandown, Kempton, Cheltenham Jumps and Ascot guides. More racecourses are on the way.
````

### 2. 4623059959 - Beginner guide - Aintree Racecourse Guide PDF for Beginners, Horse Racing Gift, Grand National, Instant Download
https://www.etsy.com/listing/4623059959  | £7.49 | 0 views lifetime | 0 favourites | section: Jumps Racecourse Guides

**BEFORE title (111):** Aintree Racecourse Guide PDF Beginner - Horse Racing Gift for Racegoers, Instant Download, Jumps Track DNA 2027
**AFTER title (95):** Aintree Racecourse Guide PDF for Beginners, Horse Racing Gift, Grand National, Instant Download

**BEFORE tags:** aintree racecourse | aintree races | aintree guide pdf | becher chase | liverpool racing | new racegoer gift | beginner jumps pdf | racing first timer | jumps day out | bechers brook | racecourse guide pdf | horse racing gift | gift for racing fan
**AFTER tags (13):** aintree races | aintree guide pdf | grand national guide | becher chase guide | racing for beginners | first grand national | horse racing gift | gift for racing fan | horse racing present | racecourse day out | racing day out gift | new racegoer gift | racing starter guide
Tags kept 5, new 8.

**Primary keyword:** aintree racecourse guide for beginners
**Secondary keywords:** aintree races, aintree guide pdf, horse racing gift for beginners, first time racegoer gift
**Extra phrases covered:** racing for beginners, racecourse day out, horse racing present, gift for dad / mum / grandad who loves racing
**Audience and why:** The gift buyer or new racegoer heading to Aintree who searches by course name or for a racing present and wants something instant and easy. Different from the Advanced and Pro editions, which target form students; this one carries the gift, first-timer and day-out vocabulary.

**Category:** Books, Movies & Music > Books > Guides & How Tos (section: Jumps Racecourse Guides).
**Attributes now:** Primary color=Green; Secondary color=Purple; Self-published=Yes; Book format=eBook; Number of pages=16
**Attribute / category actions:** No change needed (category and attributes consistent with the product)

**FULL NEW DESCRIPTION (3050 characters):**

````text
Aintree racecourse guide for beginners to horse racing over jumps: a simple instant-download PDF and horse racing gift for a day at Aintree, home of the Grand National, with the Becher Chase meeting in December and the Grand National meeting in April. Course data to help you know the track before the off. Includes a full colour version AND a black-and-white printable version. Digital file only, nothing is posted.

Each of the 9 main hurdle, chase and bumper distances raced at Aintree gets simple advice in plain words: how often the favourite won, the good signs and warning signs to check your horse against, and the jockey colours to look out for. Figures are ZANS's own analysis of 388 Aintree jumps races, April 2019 to May 2026.

WHAT'S INSIDE (16 pages)
• Start here: three easy steps and every main distance with its page number
• The course map: the Grand National course and the inner Mildmay course, with a numbered key to the famous fences
• Hurdles, fences, bumpers and ground conditions explained
• Jumps racing explained in pictures
• Trainers, jockeys and their colours
• Big-race winners' colours, 2024-25 and 2025-26
• Simple advice for every main distance (5 pages)
• Advice for beginners, a race-day checklist with tick boxes, words to know, and a page before you go

WHAT YOU GET
• One zip holding the colour PDF and the black-and-white print PDF, 16 pages each.

WHO IT'S FOR
New racegoers, family and friends heading to Aintree for a jumps meeting (the Grand National meeting included), and anyone who wants a clear starting point before reading a racecard.

GIFT IDEAS
A racing gift for dad, mum, grandad or a friend heading to a race meeting for the first time, for a birthday, Father's Day or Christmas. Instant download, so nothing to post and nothing to wrap.

GOOD TO KNOW
• Instant download: after purchase, sign in to Etsy in a mobile browser or on a computer, then go to Purchases and download your files. On an iPhone, tap the zip in the Files app to open it.
• Two PDFs: a full colour version and a mainly black-and-white print version (jockey colours are kept in colour).
• The race-day checklist has tick boxes you can tap in compatible PDF apps, or print it and tick by hand.
• Information and entertainment only. This guide is informational and does not make selections or guarantee future outcomes.
• ZANS is not connected with or approved by Aintree Racecourse or any jockey, trainer or owner named.
• The photos and explainer pictures were made with AI image tools. Maps, charts and jockey colours were drawn by ZANS with the help of AI design tools. All figures are ZANS's own analysis.

RETURNS
Digital download: if you agreed at checkout to start the download straight away, you may lose your 14-day right to cancel once the file is available. If a file won't open or isn't as described, message us and we'll fix it or refund you. This doesn't affect your statutory rights.

MORE FROM ZANS
Also available: the Aintree Jumps Advanced and Pro editions as separate listings, plus the Sandown, Kempton, Cheltenham Jumps and Ascot guides. More racecourses are on the way.
````

### 3. 4623069940 - Pro guide - Aintree Racecourse Guide PDF Pro - 135-Page Horse Racing Statistics Book, Grand National, Download
https://www.etsy.com/listing/4623069940  | £20.82 | 0 views lifetime | 0 favourites | section: Jumps Racecourse Guides

**BEFORE title (112):** Aintree Racecourse Guide PDF Pro - 135-Page Horse Racing Statistics Book, Instant Download, Jumps Track DNA Gift
**AFTER title (98):** Aintree Racecourse Guide PDF Pro - 135-Page Horse Racing Statistics Book, Grand National, Download

**BEFORE tags:** national hunt stats | jumps research pdf | racing data analysis | handicap mark stats | racing ratings book | jumps form manual | chase data analysis | hurdle data pdf | trainer jockey odds | racing stats book | racecourse guide pdf | horse racing gift | gift for racing fan
**AFTER tags (13):** aintree stats | grand national data | national hunt data | racing ratings pdf | horse racing ebook | racing data book | racing analysis pdf | trainer jockey stats | handicap data pdf | racing research pdf | form student gift | racing handbook pdf | racing stats book
Tags kept 1, new 12.

**Primary keyword:** aintree horse racing statistics
**Secondary keywords:** horse racing data book, racing ratings pdf, horse racing ebook, racing research pdf
**Extra phrases covered:** racing analysis, trainer jockey stats, handicap data, form student gift
**Audience and why:** The data-minded form student who searches for statistics, ratings and research for Aintree. Own vocabulary (statistics, data, ratings, ebook, research) separate from the Beginner gift and Advanced form listings.

**Category:** Books, Movies & Music > Books > Guides & How Tos (section: Jumps Racecourse Guides).
**Attributes now:** Primary color=Green; Secondary color=Purple; Self-published=Yes; Book format=eBook; Number of pages=135
**Attribute / category actions:** No change needed (category and attributes consistent with the product)

**FULL NEW DESCRIPTION (2988 characters):**

````text
Aintree horse racing statistics book and data PDF (Pro edition): a 135-page National Hunt research manual for the home of the Grand National, with course evidence by distance and going for hurdles, chases and bumpers, every finding checked in two periods and its limits stated. Course data to help you know the track before the off. Includes a full colour version AND a black-and-white printable version. Digital file only, nothing is posted.

Built from 610 Aintree jumps races and 6,616 runners, April 2015 to 15 May 2026. Every group is compared with the margin-free starting prices in 2015-20 and again in 2021-26, with ranges and sample sizes shown, so you can see which patterns held and which did not.

WHAT'S INSIDE (135 pages)
• Distance by distance: profiles, figures by going and two-period tests for the 9 main Aintree jumps distances
• Price calibration, the price map and the value decision
• Big prices and high odds by distance
• Aintree returners: the historical signal, the 2027 Aintree list and returners up close
• The handicapper's lens, the ZANS ratings lab, jumps specifics, going
• Trainers and jockeys against the odds, partnerships; jockeys and their colours; big-race winners' colours
• Two-period testing, model evaluation, drift over time, limitations and a findings register
• Case studies, each-way and the Placepot, a race-day audit sheet to print or copy, post-race review, research audit, glossary and method

WHAT YOU GET
• One zip holding the colour PDF and the black-and-white print PDF, 135 pages each.

WHO IT'S FOR
Experienced form students, handicap followers and data-minded racing fans who want the full evidence (handicap marks, the ZANS rating and price bands), with the method and limits shown, before forming their own view.

GOOD TO KNOW
• Instant download: after purchase, sign in to Etsy in a mobile browser or on a computer, then go to Purchases and download your files. On an iPhone, tap the zip in the Files app to open it.
• Two PDFs: a full colour version and a mainly black-and-white print version (jockey colours are kept in colour).
• Tick boxes in the distance-by-distance chapter can be tapped in compatible PDF apps, or print the guide and tick by hand.
• Information and entertainment only. This guide is informational and does not make selections or guarantee future outcomes.
• ZANS is not connected with or approved by Aintree Racecourse or any jockey, trainer or owner named.
• Maps, charts and jockey colours were drawn by ZANS with the help of AI design tools. All figures are ZANS's own analysis.

RETURNS
Digital download: if you agreed at checkout to start the download straight away, you may lose your 14-day right to cancel once the file is available. If a file won't open or isn't as described, message us and we'll fix it or refund you. This doesn't affect your statutory rights.

MORE FROM ZANS
Also available: the Aintree Jumps Beginner and Advanced editions as separate listings, plus the Sandown, Kempton, Cheltenham Jumps and Ascot guides. More racecourses are on the way.
````

### 4. 4604440668 - Advanced guide - Ascot Flat Racecourse Guide PDF Advanced - Horse Racing Form and Going Analysis, Download
https://www.etsy.com/listing/4604440668  | £12.49 | 5 views lifetime | 1 favourites | section: Flat Racecourse Guides

**BEFORE title (119):** Ascot Flat Racecourse Guide PDF Advanced - Horse Racing Betting Form by Distance and Going, Instant Download, Track DNA
**AFTER title (89):** Ascot Flat Racecourse Guide PDF Advanced - Horse Racing Form and Going Analysis, Download

**BEFORE tags:** ascot racecourse | ascot form guide | racecourse guide | racing form guide | flat racing guide | racecourse draw bias | horse racing data | racing silks guide | horse racing ratings | horse racing stats | horse racing gift | racecourse guide pdf | gift for racing fan
**AFTER tags (13):** ascot form guide | draw bias guide | flat racing form | uk racecourse guide | handicap guide pdf | price and form pdf | horse racing form | going analysis pdf | each way guide pdf | horse racing value | racing going guide | form study pdf | trainer form guide
Tags kept 1, new 12.

**Primary keyword:** ascot flat form guide pdf
**Secondary keywords:** form analysis guide, horse racing form guide, each way guide pdf, racing going guide
**Extra phrases covered:** form study, value and over-bet, trainer form, course meeting hook
**Audience and why:** The racing follower who already goes to Ascot Flat or backs horses there and searches for form, going and each-way study material. Own vocabulary (form, betting, going, each-way) so it does not compete with the Beginner gift listing or the Pro statistics listing.

**Category:** Books, Movies & Music > Books > Guides & How Tos (section: Flat Racecourse Guides).
**Attributes now:** Primary color=Pink; Secondary color=Silver; Self-published=Yes; Book format=eBook
**Attribute / category actions:** Add Number of pages = 37 (stated in the live description); description does not mention print version wording consistently - checked file wording kept

**FULL NEW DESCRIPTION (4177 characters):**

````text
Ascot Flat form guide and horse racing form analysis PDF: a 37-page, course-specific data and form-analysis guide that teaches you to assess draw, going, field size, race conditions, ZANS ratings, handicaps and connections through historical results and worked examples. Instant PDF download, with a full colour version AND a printable version in black, white and grey. Digital file only, nothing is posted.

Data on draws, ground conditions, field size and much more: ZANS's own analysis of 1,340 Flat races and 15,896 runners at Ascot, April 2015 to 17 October 2026. Every key figure is shown for both periods, 2015-20 and 2021-26, so you can see whether a pattern has held up. Green means a group did at least 10% better than its odds in both periods, with enough runners in each; red means at least 10% worse. Most chapters give a plain-English page first, then a page of the figures behind it.

The ratings in this guide are ZANS ratings: our own figures, worked out from finishing distances, weights, official handicap marks and race times. The method page at the back explains exactly how they are made.

WHAT'S INSIDE (37 pages, 19 chapters)
1. Cover
2. How to use the Advanced guide: a five-step method for every Ascot Flat race, and where to start in each type of race
3. Course DNA: the straight course, the round course and the mile, on one map
4. The draw: low, middle and high stalls at each trip (2 pages)
5. Draw and going: how the ground changes the draw (2 pages)
6. Speed: winners' whole-race times against the ZANS standard on each going
7. Draw and field size: how the number of runners changes the draw (2 pages)
8. Ratings, handicap marks and recent form: which ZANS rating to trust, and when (3 pages)
9. Same-conditions finder: form on the same going and at the same trip (2 pages)
10. Ground and going changes: what to do when the going changes during the day (2 pages)
11. Distance and stamina: does the form support today's trip? (2 pages)
12. Handicaps, weight and the handicap mark: is the horse well treated today? (2 pages)
13. Trainers, jockeys and owners: who does well at Ascot then and now, how to judge a booking, worked examples of how owners' colours are read, and the colours of every Group 1 winner at Ascot in 2025 and 2026 (6 pages)
14. Field size, experience and allowances (2 pages)
15. Value and the price: finding the overlooked higher-odds runner, and how to tell if a price is big enough (2 pages)
16. Putting it together: one worked race, step by step, from the evidence to the price and the no-bet decision (3 pages)
17. A printable race-day worksheet
18. Glossary and responsible use
19. Method and sources

WHAT YOU GET
One zip file containing two PDFs:
1. Full colour version, to read on your phone, tablet or computer
2. Printable version in black, white and grey (the jockey silks stay in colour), cheap to print at home

WHO IT'S FOR
- Regular racegoers who want more than the basics
- Beginner Edition owners ready for the next step
- A gift for a racing fan (it arrives instantly)

GOOD TO KNOW
- Instant download: after purchase, sign in to Etsy in a mobile browser or on a computer, then go to Purchases and download your files.
- Open the zip on a computer or phone (most phones open zips in the Files app)
- This is an information and entertainment guide. It shows how Ascot has raced in the past; this guide is informational and does not make selections or guarantee future outcomes.
- ZANS is not connected with or approved by Ascot Racecourse or any jockey, trainer or owner named in the guide. Owners' colours are shown only to help you recognise them.
- Maps, silks and charts were drawn by ZANS with the help of AI design tools. All figures are ZANS's own analysis.

RETURNS
Digital download: if you agreed at checkout to start the download straight away, you may lose your 14-day right to cancel once the file is available. If a file won't open or isn't as described, message us and we'll fix it or refund you. This doesn't affect your statutory rights.

MORE FROM ZANS
The Ascot Racecourse Guide is also in the shop as a Beginner Edition and a Pro Edition. Jumps guides and more racecourses are on the way.
````

### 5. 4601073843 - Beginner guide - Ascot Flat Racecourse Guide PDF for Beginners, Horse Racing Gift, Instant Download
https://www.etsy.com/listing/4601073843  | £7.49 | 38 views lifetime | 1 favourites | section: Flat Racecourse Guides

**BEFORE title (108):** Ascot Flat Racecourse Guide PDF Beginner - Horse Racing Gift for Racegoers, Instant Download, Track DNA 2027
**AFTER title (82):** Ascot Flat Racecourse Guide PDF for Beginners, Horse Racing Gift, Instant Download

**BEFORE tags:** ascot racecourse | racecourse guide | horse racing guide | horse racing pdf | racing form guide | horse racing form | uk racecourse guide | flat racing guide | horse racing gift | horse racing data | racecourse guide pdf | ascot horse racing | gift for racing fan
**AFTER tags (13):** ascot racecourse | racecourse guide | horse racing guide | horse racing pdf | racing form guide | horse racing form | uk racecourse guide | flat racing guide | horse racing gift | horse racing data | racecourse guide pdf | ascot horse racing | gift for racing fan
Tags kept 13, new 0.

**Primary keyword:** ascot flat racecourse guide for beginners
**Secondary keywords:** ascot flat races, ascot flat guide pdf, horse racing gift for beginners, first time racegoer gift
**Extra phrases covered:** racing for beginners, racecourse day out, horse racing present, gift for dad / mum / grandad who loves racing
**Audience and why:** The gift buyer or new racegoer heading to Ascot Flat who searches by course name or for a racing present and wants something instant and easy. Different from the Advanced and Pro editions, which target form students; this one carries the gift, first-timer and day-out vocabulary.
**Note:** CONTROL for tags: tags unchanged. Compliance fixes only: title shortened to 12 words (ChatGPT rule applies to controls), 18+ line and winners/profit wording replaced. Title change is a deliberate trade-off on the best guide (38 views): Alex's call.

**Category:** Books, Movies & Music > Books > Guides & How Tos (section: Flat Racecourse Guides).
**Attributes now:** Primary color=Pink; Self-published=Yes; Book format=eBook; Number of pages=13; Secondary color=Bronze
**Attribute / category actions:** No change needed (category and attributes consistent with the product)

**FULL NEW DESCRIPTION (2776 characters):**

````text
Ascot Racecourse Guide for beginners: a horse racing form guide PDF packed with Ascot course data, including the draw (starting stalls), the going (ground conditions), top trainers and jockeys, and a clear course map. Course data to help you know Ascot before the off. Includes a full colour version AND a black-and-white printable version. Digital file only, nothing is posted.

ZANS Track DNA shows how a racecourse tends to race, using ZANS's own analysis of every Flat race at Ascot from May 2019 to October 2026. The Beginner Edition is easy to read, with no jargon and every term explained.

WHAT'S INSIDE (13 pages)
- A clear, numbered map of the course: the straight mile, the round course and where races start
- Starting stalls explained, with a simple green and red gate guide
- A page for each type of ground (Good to Firm, Good, Good to Soft, Soft)
- Quick pointers on every ground page to help you pick a horse: gates, recent form, course form and top trainers
- What kind of horse wins at Ascot, from our own figures
- How often favourites win and finish in the places
- The top trainers and jockeys for 2027, the jockeys' colours to look out for and the best jockey and trainer partnerships
- Every distance in a nutshell: a one-page summary
- Advice for beginners, a fill-in race-day checklist and a glossary of racing words

WHAT YOU GET
One zip file containing two PDFs:
1. Full colour version, to read on your phone, tablet or computer
2. Black-and-white printable version, quick and cheap to print at home and take racing with you (jockey colours stay in colour)

WHO IT'S FOR
- First-time racegoers and anyone new to Flat racing
- Anyone heading to Ascot who wants to understand the course before the off
- A thoughtful gift for a racing fan (it's a download, so it arrives instantly)

GOOD TO KNOW
- Instant download: after purchase, sign in to Etsy in a mobile browser or on a computer, then go to Purchases and download your files.
- Open the zip on a computer or phone (most phones open zip files in their Files app)
- This is an information and entertainment guide. It shows how Ascot has raced in the past; this guide is informational and does not make selections or guarantee future outcomes.
- ZANS is independent and not connected with or approved by Ascot Racecourse
- Maps, charts and jockey colours were drawn by ZANS with the help of AI design tools. All figures are ZANS's own analysis.

RETURNS
Digital download: if you agreed at checkout to start the download straight away, you may lose your 14-day right to cancel once the file is available. If a file won't open or isn't as described, message us and we'll fix it or refund you. This doesn't affect your statutory rights.
Step
MORE FROM ZANS
Advanced and Pro editions, Jumps guides, more racecourses and festival packs are on the way. Follow the shop so you don't miss them.
````

### 6. 4604430033 - Pro guide - Ascot Flat Racecourse Guide PDF Pro - 71-Page Horse Racing Statistics Book, Instant Download
https://www.etsy.com/listing/4604430033  | £20.82 | 8 views lifetime | 1 favourites | section: Flat Racecourse Guides

**BEFORE title (100):** Ascot Flat Racecourse Guide PDF Pro - Horse Racing Statistics Book, Instant Download, Track DNA Gift
**AFTER title (92):** Ascot Flat Racecourse Guide PDF Pro - 71-Page Horse Racing Statistics Book, Instant Download

**BEFORE tags:** ascot racecourse | racecourse guide | racing form guide | flat racing guide | racecourse draw bias | horse racing data | racing silks guide | horse racing stats | horse racing gift | horse racing ebook | uk racecourse guide | racecourse guide pdf | gift for racing fan
**AFTER tags (13):** ascot statistics | draw statistics | racing silks guide | racing method pdf | official ratings pdf | racing form data | horse racing data | racing statistics | racing ratings pdf | horse racing ebook | racing data book | racing analysis pdf | trainer jockey stats
Tags kept 3, new 10.

**Primary keyword:** ascot flat horse racing statistics
**Secondary keywords:** horse racing data book, racing ratings pdf, horse racing ebook, racing research pdf
**Extra phrases covered:** racing analysis, trainer jockey stats, handicap data, form student gift
**Audience and why:** The data-minded form student who searches for statistics, ratings and research for Ascot Flat. Own vocabulary (statistics, data, ratings, ebook, research) separate from the Beginner gift and Advanced form listings.

**Category:** Books, Movies & Music > Books > Guides & How Tos (section: Flat Racecourse Guides).
**Attributes now:** Primary color=Pink; Self-published=Yes; Book format=eBook; Secondary color=Gold
**Attribute / category actions:** Add Number of pages = 71 (stated in the live description; check the file first)

**FULL NEW DESCRIPTION (4120 characters):**

````text
Ascot Flat horse racing statistics book and research manual, Pro edition: an instant 71-page PDF download for experienced racing followers, with course-specific evidence, form and ZANS rating interpretation, draw analysis, and the silks of the leading jockeys, trainers and owners. Includes a full colour version AND a printer-friendly version (mostly black and white, with the silks kept in colour). Digital file only, nothing is posted. This is a downloadable research and analysis guide, not a live data subscription or a prediction service.

ZANS's own analysis of 1,340 Flat races and 15,896 runners at Ascot, April 2015 to 17 October 2026. Every finding is checked in two separate periods, 2015-20 and 2021-26, with its range and sample size, and 453 tested groups are listed in a findings register so you can see what held up and what did not. The price is treated as the last check, not the first.

WHAT'S INSIDE (71 pages)
- Start here: the method behind every figure, and the ZANS rating explained
- The price map and the value decision: what the market already knows, and how to judge whether a price is big enough
- Big prices, live or trap
- High odds by distance: every trip from 5f to 2m and further, with measured results kept apart from ideas to check, the strongest counterargument and a data-confidence line for each, plus a worked 7f example (5 pages)
- Ascot returners: horses placed at 10/1 or bigger on their last Ascot run, the 2027 returner list and detailed profiles with owners' colours drawn by ZANS (12 pages)
- The handicapper's lens and the ratings lab: handicap marks, the ZANS rating (our own rating, built from handicap marks, distances beaten, weight carried and race times) and recent form
- Draw evidence by trip, field size and going, and the going pages (5 pages)
- Trainers and jockeys at a price
- Jockeys and trainers with their silks: the leading riders and stables at Ascot, the colours they carry, their 2025-26 record and best partnerships (2 pages)
- Owner networks: owner and trainer combinations, and whose colours you are looking at
- Group 1 winners' silks: every Ascot Group 1 winner of 2025 and 2026 with trainer, jockey, price and colours (2 pages)
- Two-period scoreboard, model check, drift over time and limitations at a glance
- Findings register: every group tested, with its grade (12 pages)
- Five worked examples, step by step: four example races built from real Ascot figures, plus one real Ascot booking story from the June meeting
- Each-way and the Placepot
- Race-day evidence audit with a ranked shortlist, and a post-race review sheet
- Research audit, sources, glossary and method

WHAT YOU GET
One zip file containing two PDFs:
1. Full colour version, to read on your phone, tablet or computer
2. Printer-friendly version (mostly black and white, silks in colour), cheap to print at home

WHO IT'S FOR
- Experienced racing followers who want the full evidence, with its limits stated
- Advanced Edition owners ready for the deepest level
- A gift for a racing fan (it arrives instantly)

GOOD TO KNOW
- Instant download: after purchase, sign in to Etsy in a mobile browser or on a computer, then go to Purchases and download your files.
- Open the zip on a computer or phone (most phones open zips in the Files app)
- The guide helps you weigh the evidence and build a shortlist of credible contenders. It does not pick horses for you.
- This is an information and entertainment guide.
- ZANS is independent and not connected with or approved by Ascot Racecourse or any jockey, trainer or owner named in the guide. Owners' colours are shown only to help you recognise them.
- Maps, silks and charts were drawn by ZANS with the help of AI design tools. All figures are ZANS's own analysis.

RETURNS
Digital download: if you agreed at checkout to start the download straight away, you may lose your 14-day right to cancel once the file is available. If a file won't open or isn't as described, message us and we'll fix it or refund you. This doesn't affect your statutory rights.

MORE FROM ZANS
The Ascot Racecourse Guide is also in the shop as a Beginner Edition and an Advanced Edition. Jumps guides and more racecourses are on the way.
````

### 7. 4622450389 - Advanced guide - Ascot Jumps Racecourse Guide PDF Advanced - Horse Racing Form and Going Analysis, Download
https://www.etsy.com/listing/4622450389  | £12.49 | 0 views lifetime | 0 favourites | section: Jumps Racecourse Guides

**BEFORE title (120):** Ascot Jumps Racecourse Guide PDF Advanced - Horse Racing Betting Form by Distance and Going, Instant Download, Track DNA
**AFTER title (90):** Ascot Jumps Racecourse Guide PDF Advanced - Horse Racing Form and Going Analysis, Download

**BEFORE tags:** ascot racecourse | racecourse guide pdf | uk racecourse guide | national hunt racing | racing form guide | form guide pdf | betting guide pdf | each way guide | horse racing going | jockey trainer stats | horse racing gift | gift for racing fan | racegoer gift
**AFTER tags (13):** ascot form | ascot going guide | ascot jumps form | ascot form analysis | horse racing form | over bet guide | placepot guide pdf | racing odds guide | price and form pdf | going analysis pdf | each way guide pdf | horse racing value | racing going guide
Tags kept 0, new 13.

**Primary keyword:** ascot jumps form guide pdf
**Secondary keywords:** form analysis guide, horse racing form guide, each way guide pdf, racing going guide
**Extra phrases covered:** form study, value and over-bet, trainer form, course meeting hook
**Audience and why:** The racing follower who already goes to Ascot Jumps or backs horses there and searches for form, going and each-way study material. Own vocabulary (form, betting, going, each-way) so it does not compete with the Beginner gift listing or the Pro statistics listing.

**Category:** Books, Movies & Music > Books > Guides & How Tos (section: Jumps Racecourse Guides).
**Attributes now:** Primary color=Green; Secondary color=Pink; Self-published=Yes; Number of pages=34; Book format=eBook
**Attribute / category actions:** No change needed (category and attributes consistent with the product)

**FULL NEW DESCRIPTION (2714 characters):**

````text
Ascot jumps form guide and horse racing form analysis PDF: value and over-bet points for each of the 9 main hurdle, chase and bumper distances, split by going (ground conditions) where there are enough races, measured against the starting prices. Course data to help you know the track before the off. Includes a full colour version AND a black-and-white printable version. Digital file only, nothing is posted.

Each point shows how often that kind of horse won and whether it won more or less often than its odds said, tagged VALUE, AS PRICED, OVER-BET or LONGSHOT. It is different research from the Beginner edition, not a copy with extra pages. Figures are ZANS's own analysis of Ascot jumps results, January 2019 to March 2026.

WHAT'S INSIDE (34 pages)
• How the Advanced edition works, the course map and the going explained
• Every main distance: value and over-bet points, by going where there are enough races (21 pages)
• The price: where Ascot pays over jumps
• Trainers, jockeys and partnerships against the odds
• Smart money: outsider specialists, and win and place chances by price
• The Placepot (a pool bet) and a race-day checklist
• Big-race winners with their prices and colours; stars to look out for in 2027
• Summary for every main distance, glossary

WHAT YOU GET
• One zip holding the colour PDF and the black-and-white print PDF, 34 pages each.

WHO IT'S FOR
Regular racegoers, each-way and Placepot players and form readers who know the basics and want value and price context at Ascot over jumps through the winter.

GOOD TO KNOW
• Instant download: after purchase, sign in to Etsy in a mobile browser or on a computer, then go to Purchases and download your files. On an iPhone, tap the zip in the Files app to open it.
• Two PDFs: a full colour version and a mainly black-and-white print version (jockey colours are kept in colour).
• Tick boxes are fillable in compatible PDF apps, or print the guide and tick them by hand.
• Information and entertainment only. This guide is informational and does not make selections or guarantee future outcomes.
• ZANS is not connected with or approved by Ascot Racecourse or any jockey, trainer or owner named.
• Maps, charts and jockey colours were drawn by ZANS with the help of AI design tools. All figures are ZANS's own analysis.

RETURNS
Digital download: if you agreed at checkout to start the download straight away, you may lose your 14-day right to cancel once the file is available. If a file won't open or isn't as described, message us and we'll fix it or refund you. This doesn't affect your statutory rights.

MORE FROM ZANS
Also available: the Ascot Jumps Beginner and Pro editions as separate listings, and the Ascot Flat guides (Beginner, Advanced and Pro). More racecourses are on the way.
````

### 8. 4622457762 - Beginner guide - Ascot Jumps Racecourse Guide PDF for Beginners, Horse Racing Gift, Racegoer Basics, Download
https://www.etsy.com/listing/4622457762  | £7.49 | 0 views lifetime | 0 favourites | section: Jumps Racecourse Guides

**BEFORE title (109):** Ascot Jumps Racecourse Guide PDF Beginner - Horse Racing Gift for Racegoers, Instant Download, Track DNA 2027
**AFTER title (92):** Ascot Jumps Racecourse Guide PDF for Beginners, Horse Racing Gift, Racegoer Basics, Download

**BEFORE tags:** ascot racecourse | ascot guide pdf | racecourse guide | racing for beginners | horse racing basics | horse racing guide | race day guide | hurdle racing | horse racing gifts | racegoer gift | horse racing pdf | racecourse guide pdf | horse racing gift
**AFTER tags (13):** ascot races | ascot guide pdf | ascot jumps guide | hurdles and chases | racing for beginners | first ascot visit | horse racing gift | racing checklist pdf | racecourse guide pdf | racegoer gift | horse racing present | racecourse day out | racing day out gift
Tags kept 5, new 8.

**Primary keyword:** ascot jumps racecourse guide for beginners
**Secondary keywords:** ascot jumps races, ascot jumps guide pdf, horse racing gift for beginners, first time racegoer gift
**Extra phrases covered:** racing for beginners, racecourse day out, horse racing present, gift for dad / mum / grandad who loves racing
**Audience and why:** The gift buyer or new racegoer heading to Ascot Jumps who searches by course name or for a racing present and wants something instant and easy. Different from the Advanced and Pro editions, which target form students; this one carries the gift, first-timer and day-out vocabulary.

**Category:** Books, Movies & Music > Books > Guides & How Tos (section: Jumps Racecourse Guides).
**Attributes now:** Primary color=Green; Secondary color=Pink; Self-published=Yes; Number of pages=16; Book format=eBook
**Attribute / category actions:** No change needed (category and attributes consistent with the product)

**FULL NEW DESCRIPTION (2993 characters):**

````text
Ascot jumps racecourse guide for beginners to horse racing: a simple instant-download National Hunt PDF and racegoer gift for a race day at Ascot, distance by distance, covering hurdles, steeplechases, bumpers, the going and the jockey colours. Course data to help you know the track before the off. Includes a full colour version AND a black-and-white printable version. Digital file only, nothing is posted.

Each of the 9 main hurdle, chase and bumper distances at Ascot gets simple advice in plain words: how often the favourite won, the good signs and warning signs to check your horse against, and the jockey colours to look out for. A race-day checklist with tick boxes is included too. Figures are ZANS's own analysis of 366 Ascot jumps races, January 2019 to March 2026.

WHAT'S INSIDE (16 pages)
• Start here: three easy steps, every distance with its page number, and Ascot jumps at a glance
• The course map, with the hurdle and chase courses and a numbered key
• Hurdles, fences, bumpers and ground conditions explained
• Jumps racing explained in pictures
• Jockeys, trainers and their colours
• Star horses and big names to look out for
• Past big-race winners' colours
• Simple advice for every main distance (5 pages)
• Advice for beginners, a race-day checklist and words to know

WHAT YOU GET
• One zip holding the colour PDF and the black-and-white print PDF, 16 pages each.

WHO IT'S FOR
New racegoers, family and friends heading to Ascot for a jumps meeting, and anyone who wants a clear starting point before reading a racecard.

GIFT IDEAS
A racing gift for dad, mum, grandad or a friend heading to a race meeting for the first time, for a birthday, Father's Day or Christmas. Instant download, so nothing to post and nothing to wrap.

GOOD TO KNOW
• Instant download: after purchase, sign in to Etsy in a mobile browser or on a computer, then go to Purchases and download your files. On an iPhone, tap the zip in the Files app to open it.
• Two PDFs: a full colour version and a mainly black-and-white print version (jockey colours are kept in colour).
• Tick boxes are fillable in compatible PDF apps, or print the guide and tick them by hand.
• Information and entertainment only. This guide is informational and does not make selections or guarantee future outcomes.
• ZANS is not connected with or approved by Ascot Racecourse or any jockey, trainer or owner named.
• The photos and explainer pictures were made with AI image tools. Maps, charts and jockey colours were drawn by ZANS with the help of AI design tools. All figures are ZANS's own analysis.

RETURNS
Digital download: if you agreed at checkout to start the download straight away, you may lose your 14-day right to cancel once the file is available. If a file won't open or isn't as described, message us and we'll fix it or refund you. This doesn't affect your statutory rights.

MORE FROM ZANS
Also available: the Ascot Jumps Advanced and Pro editions as separate listings, and the Ascot Flat guides (Beginner, Advanced and Pro). More racecourses are on the way.
````

### 9. 4622458108 - Pro guide - Ascot Jumps Racecourse Guide PDF Pro - 134-Page Horse Racing Statistics Book, Instant Download
https://www.etsy.com/listing/4622458108  | £20.82 | 0 views lifetime | 0 favourites | section: Jumps Racecourse Guides

**BEFORE title (110):** Ascot Jumps Racecourse Guide PDF Pro - 134-Page Horse Racing Statistics Book, Instant Download, Track DNA Gift
**AFTER title (94):** Ascot Jumps Racecourse Guide PDF Pro - 134-Page Horse Racing Statistics Book, Instant Download

**BEFORE tags:** horse racing data | horse racing stats | horse racing ratings | racing statistics | official ratings | handicap ratings | racing research | hurdle racing stats | horse racing ebook | steeplechase racing | racecourse guide pdf | horse racing gift | gift for racing fan
**AFTER tags (13):** ascot stats | ascot jumps data | national hunt data | jockey stats pdf | trainer stats pdf | handicap analysis | racing method pdf | official ratings pdf | racing form data | horse racing data | racing statistics | racing ratings pdf | horse racing ebook
Tags kept 3, new 10.

**Primary keyword:** ascot jumps horse racing statistics
**Secondary keywords:** horse racing data book, racing ratings pdf, horse racing ebook, racing research pdf
**Extra phrases covered:** racing analysis, trainer jockey stats, handicap data, form student gift
**Audience and why:** The data-minded form student who searches for statistics, ratings and research for Ascot Jumps. Own vocabulary (statistics, data, ratings, ebook, research) separate from the Beginner gift and Advanced form listings.

**Category:** Books, Movies & Music > Books > Guides & How Tos (section: Jumps Racecourse Guides).
**Attributes now:** Primary color=Green; Secondary color=Pink; Self-published=Yes; Book format=eBook; Number of pages=134
**Attribute / category actions:** No change needed (category and attributes consistent with the product)

**FULL NEW DESCRIPTION (2990 characters):**

````text
Ascot jumps horse racing statistics and ratings ebook: a 134-page National Hunt research manual and analysis PDF (Pro edition), with course evidence by distance and going for hurdles, chases and bumpers, every finding checked in two periods and its limits stated. Course data to help you know the track before the off. Includes a full colour version AND a black-and-white printable version. Digital file only, nothing is posted.

Built from 578 Ascot jumps races and 4,850 runners, January 2015 to 31 October 2026. Every group is compared with the margin-free starting prices in 2015-20 and again in 2021-26, with ranges and sample sizes shown, so you can see which patterns held and which did not.

WHAT'S INSIDE (134 pages)
• Distance by distance: profiles, price bands and two-period figures for each of the 9 main Ascot jumps distances, with tick boxes for every distance and going
• Price calibration, the price map and the value decision
• Big prices and high odds by distance
• Ascot returners: the historical signal, the 2027 returner list and ten profiles
• The handicapper's lens, the ZANS rating lab, fences v hurdles and jumping, going
• Trainers and jockeys against the odds; jockeys, trainers and their silks; Grade 1 and 2 winners' silks
• Two-period scoreboard, model evaluation, drift over time, limitations and a findings register
• Case studies, each-way and the Placepot, a race-day audit sheet to fill in, research audit, glossary and method

WHAT YOU GET
• One zip holding the colour PDF and the black-and-white print PDF, 134 pages each.

WHO IT'S FOR
Experienced form students, handicap followers and data-minded racing fans who want the full evidence (official marks, the handicapper's view, the ZANS rating and price bands), with the method and limits shown, before forming their own view.

GOOD TO KNOW
• Instant download: after purchase, sign in to Etsy in a mobile browser or on a computer, then go to Purchases and download your files. On an iPhone, tap the zip in the Files app to open it.
• Two PDFs: a full colour version and a mainly black-and-white print version (jockey colours are kept in colour).
• Tick boxes are fillable in compatible PDF apps, or print the guide and tick them by hand.
• Information and entertainment only. This guide is informational and does not make selections or guarantee future outcomes.
• ZANS is not connected with or approved by Ascot Racecourse or any jockey, trainer or owner named.
• Maps, charts and jockey colours were drawn by ZANS with the help of AI design tools. All figures are ZANS's own analysis.

RETURNS
Digital download: if you agreed at checkout to start the download straight away, you may lose your 14-day right to cancel once the file is available. If a file won't open or isn't as described, message us and we'll fix it or refund you. This doesn't affect your statutory rights.

MORE FROM ZANS
Also available: the Ascot Jumps Beginner and Advanced editions as separate listings, and the Ascot Flat guides (Beginner, Advanced and Pro). More racecourses are on the way.
````

### 10. 4622511552 - Advanced guide - Cheltenham Racecourse Guide PDF Advanced - Horse Racing Form and Going Analysis, Festival
https://www.etsy.com/listing/4622511552  | £12.49 | 0 views lifetime | 0 favourites | section: Jumps Racecourse Guides

**BEFORE title (125):** Cheltenham Racecourse Guide PDF Advanced - Horse Racing Betting Form by Distance and Going, Instant Download, Jumps Track DNA
**AFTER title (89):** Cheltenham Racecourse Guide PDF Advanced - Horse Racing Form and Going Analysis, Festival

**BEFORE tags:** cheltenham betting | cheltenham form | cheltenham racing | festival form guide | jumps form guide | steeplechase betting | hurdle betting | festival betting pdf | trainer form guide | chase betting guide | racecourse guide pdf | horse racing gift | gift for racing fan
**AFTER tags (13):** cheltenham betting | cheltenham form | cheltenham racing | festival form guide | jumps form guide | steeplechase betting | hurdle betting | festival betting pdf | trainer form guide | chase betting guide | racecourse guide pdf | horse racing gift | gift for racing fan
Tags kept 13, new 0.

**Primary keyword:** cheltenham form guide pdf
**Secondary keywords:** form analysis guide, horse racing form guide, each way guide pdf, racing going guide
**Extra phrases covered:** form study, value and over-bet, trainer form, course meeting hook
**Audience and why:** The racing follower who already goes to Cheltenham or backs horses there and searches for form, going and each-way study material. Own vocabulary (form, betting, going, each-way) so it does not compete with the Beginner gift listing or the Pro statistics listing.
**Note:** CONTROL for tags: tags unchanged (growth thread rule). Title shortened to the shop word limit; description compliance fixes only.

**Category:** Books, Movies & Music > Books > Guides & How Tos (section: Jumps Racecourse Guides).
**Attributes now:** Primary color=Green; Self-published=Yes; Number of pages=55; Book format=eBook; Secondary color=Blue
**Attribute / category actions:** No change needed (category and attributes consistent with the product)

**FULL NEW DESCRIPTION (2891 characters):**

````text
Cheltenham form and going analysis guide and National Hunt horse racing form guide, Advanced edition: a jumps PDF for Cheltenham, from the winter meetings to the Festival in March, with value and over-bet points for each of the 14 main hurdle, chase and bumper distances, split by going (ground conditions) where there are enough races, measured against the starting prices. Course data to help you know Cheltenham over jumps before the off. Includes a full colour version AND a black-and-white printable version. Digital file only, nothing is posted.

Each point shows how often that kind of horse won and whether it won more or less often than its odds said, tagged VALUE, AS PRICED, OVER-BET or LONGSHOT. It is different research from the Beginner edition, not a copy with extra pages. Figures are ZANS's own analysis of 784 Cheltenham jumps races, January 2019 to October 2026.

WHAT'S INSIDE (55 pages)
• Pick your distance, how the Advanced edition works, the course map and the going explained
• Every main distance: value and over-bet points, by going where there are enough races (41 pages)
• The price: where Cheltenham pays over jumps
• Trainers, jockeys and partnerships against the odds
• Smart money: outsider specialists and short-priced names
• The Placepot (a pool bet) and a race-day checklist
• Festival winners' colours, 2026 and 2025
• Summary for every main distance, glossary

WHAT YOU GET
• One zip holding the colour PDF and the black-and-white print PDF, 55 pages each.

WHO IT'S FOR
Regular racegoers, each-way and Placepot players and form readers who know the basics and want value and price context at Cheltenham over jumps, the Festival included.

GOOD TO KNOW
• Instant download: after purchase, sign in to Etsy in a mobile browser or on a computer, then go to Purchases and download your files. On an iPhone, tap the zip in the Files app to open it.
• Two PDFs: a full colour version and a mainly black-and-white print version (jockey colours are kept in colour).
• Tick boxes on the distance pages, the how-to page and the race-day checklist can be tapped in compatible PDF apps, or print the guide and tick by hand.
• Information and entertainment only. This guide is informational and does not make selections or guarantee future outcomes.
• ZANS is not connected with or approved by Cheltenham Racecourse or any jockey, trainer or owner named.
• Maps, charts and jockey colours were drawn by ZANS with the help of AI design tools. All figures are ZANS's own analysis.

RETURNS
Digital download: if you agreed at checkout to start the download straight away, you may lose your 14-day right to cancel once the file is available. If a file won't open or isn't as described, message us and we'll fix it or refund you. This doesn't affect your statutory rights.

MORE FROM ZANS
Also available: the Cheltenham Jumps Beginner and Pro editions as separate listings, plus the Ascot Jumps and Ascot Flat guides. More racecourses are on the way.
````

### 11. 4622511316 - Beginner guide - Cheltenham Racecourse Guide PDF for Beginners, Horse Racing Gift, Festival Racegoers, Download
https://www.etsy.com/listing/4622511316  | £7.49 | 1 views lifetime | 0 favourites | section: Jumps Racecourse Guides

**BEFORE title (114):** Cheltenham Racecourse Guide PDF Beginner - Horse Racing Gift for Racegoers, Instant Download, Jumps Track DNA 2027
**AFTER title (94):** Cheltenham Racecourse Guide PDF for Beginners, Horse Racing Gift, Festival Racegoers, Download

**BEFORE tags:** cheltenham races | cheltenham guide pdf | cheltenham gift | racecourse guide | jockey colours guide | racecourse day out | beginners racing | festival racing gift | hurdles and chases | horse racing present | racecourse guide pdf | horse racing gift | gift for racing fan
**AFTER tags (13):** cheltenham races | cheltenham guide pdf | cheltenham gift | festival racing gift | racing for beginners | first festival visit | horse racing gift | jockey colours guide | beginners racing pdf | racing glossary pdf | racing checklist pdf | racecourse guide pdf | gift for racing fan
Tags kept 8, new 5.

**Primary keyword:** cheltenham racecourse guide for beginners
**Secondary keywords:** cheltenham races, cheltenham guide pdf, horse racing gift for beginners, first time racegoer gift
**Extra phrases covered:** racing for beginners, racecourse day out, horse racing present, gift for dad / mum / grandad who loves racing
**Audience and why:** The gift buyer or new racegoer heading to Cheltenham who searches by course name or for a racing present and wants something instant and easy. Different from the Advanced and Pro editions, which target form students; this one carries the gift, first-timer and day-out vocabulary.

**Category:** Books, Movies & Music > Books > Guides & How Tos (section: Jumps Racecourse Guides).
**Attributes now:** Primary color=Green; Self-published=Yes; Book format=eBook; Number of pages=18; Secondary color=Blue
**Attribute / category actions:** No change needed (category and attributes consistent with the product)

**FULL NEW DESCRIPTION (3000 characters):**

````text
Cheltenham racecourse guide for beginners to horse racing over jumps: a simple instant-download PDF and horse racing gift for a race day at Cheltenham, from a winter Saturday to the Festival in March, covering hurdles, chases, bumpers, the going and the jockey colours. Course data to help you know the track before the off. Includes a full colour version AND a black-and-white printable version. Digital file only, nothing is posted.

Each of the 14 main hurdle, chase and bumper distances raced at Cheltenham gets simple advice in plain words: how often the favourite won, the good signs and warning signs to check your horse against, and the jockey colours to look out for. Figures are ZANS's own analysis of 784 Cheltenham jumps races, January 2019 to October 2026.

WHAT'S INSIDE (18 pages)
• Start here: three easy steps, every main distance with its page number, and Cheltenham jumps at a glance
• The course map: the Old, New and Cross Country courses, with a numbered key
• Hurdles, fences, bumpers and ground conditions explained
• Jumps racing explained in pictures
• Jockeys, trainers and their colours
• Festival winners' colours, 2025 and 2026
• Simple advice for every main distance (7 pages)
• Advice for beginners, a race-day checklist with tick boxes, and words to know

WHAT YOU GET
• One zip holding the colour PDF and the black-and-white print PDF, 18 pages each.

WHO IT'S FOR
New racegoers, family and friends heading to Cheltenham for a jumps meeting, and anyone who wants a clear starting point before reading a racecard.

GIFT IDEAS
A racing gift for dad, mum, grandad or a friend heading to a race meeting for the first time, for a birthday, Father's Day or Christmas. Instant download, so nothing to post and nothing to wrap.

GOOD TO KNOW
• Instant download: after purchase, sign in to Etsy in a mobile browser or on a computer, then go to Purchases and download your files. On an iPhone, tap the zip in the Files app to open it.
• Two PDFs: a full colour version and a mainly black-and-white print version (jockey colours are kept in colour).
• The race-day checklist has tick boxes you can tap in compatible PDF apps, or print it and tick by hand.
• Information and entertainment only. This guide is informational and does not make selections or guarantee future outcomes.
• ZANS is not connected with or approved by Cheltenham Racecourse or any jockey, trainer or owner named.
• The photos and explainer pictures were made with AI image tools. Maps, charts and jockey colours were drawn by ZANS with the help of AI design tools. All figures are ZANS's own analysis.

RETURNS
Digital download: if you agreed at checkout to start the download straight away, you may lose your 14-day right to cancel once the file is available. If a file won't open or isn't as described, message us and we'll fix it or refund you. This doesn't affect your statutory rights.

MORE FROM ZANS
Also available: the Cheltenham Jumps Advanced and Pro editions as separate listings, plus the Ascot Jumps and Ascot Flat guides. More racecourses are on the way.
````

### 12. 4622511788 - Pro guide - Cheltenham Racecourse Guide PDF Pro - 198-Page Horse Racing Statistics Book, Festival, Download
https://www.etsy.com/listing/4622511788  | £20.82 | 0 views lifetime | 0 favourites | section: Jumps Racecourse Guides

**BEFORE title (115):** Cheltenham Racecourse Guide PDF Pro - 198-Page Horse Racing Statistics Book, Instant Download, Jumps Track DNA Gift
**AFTER title (95):** Cheltenham Racecourse Guide PDF Pro - 198-Page Horse Racing Statistics Book, Festival, Download

**BEFORE tags:** jumps statistics | national hunt data | steeplechase stats | hurdle statistics | racing handbook pdf | trainer statistics | jockey statistics | festival statistics | form study pdf | racing data pdf | racecourse guide pdf | horse racing gift | gift for racing fan
**AFTER tags (13):** cheltenham stats | festival statistics | national hunt data | racing numbers pdf | racing evidence pdf | racing study guide | jockey stats pdf | trainer stats pdf | handicap analysis | racing method pdf | official ratings pdf | racing form data | horse racing data
Tags kept 2, new 11.

**Primary keyword:** cheltenham horse racing statistics
**Secondary keywords:** horse racing data book, racing ratings pdf, horse racing ebook, racing research pdf
**Extra phrases covered:** racing analysis, trainer jockey stats, handicap data, form student gift
**Audience and why:** The data-minded form student who searches for statistics, ratings and research for Cheltenham. Own vocabulary (statistics, data, ratings, ebook, research) separate from the Beginner gift and Advanced form listings.

**Category:** Books, Movies & Music > Books > Guides & How Tos (section: Jumps Racecourse Guides).
**Attributes now:** Primary color=Green; Self-published=Yes; Book format=eBook; Number of pages=198; Secondary color=Blue
**Attribute / category actions:** No change needed (category and attributes consistent with the product)

**FULL NEW DESCRIPTION (3032 characters):**

````text
Cheltenham horse racing statistics book and data PDF (Pro edition): a 198-page National Hunt research manual, Festival races included, with course evidence by distance and going for hurdles, chases and bumpers, every finding checked in two periods and its limits stated. Course data to help you know the track before the off. Includes a full colour version AND a black-and-white printable version. Digital file only, nothing is posted.

Built from 1,224 Cheltenham jumps races and 14,275 runners, January 2015 to 24 October 2026. Every group is compared with the margin-free starting prices in 2015-20 and again in 2021-26, with ranges and sample sizes shown, so you can see which patterns held and which did not.

WHAT'S INSIDE (198 pages)
• Distance by distance: profiles, price bands and two-period figures for the 14 main Cheltenham jumps distances, with tick boxes
• Price calibration, the price map and the value decision
• Big prices and high odds by distance
• Cheltenham returners: the historical signal, the 2027 returner list and returner profiles
• The handicapper's lens, the ZANS rating lab, fences v hurdles and jumping, going
• Trainers and jockeys against the odds; jockeys, trainers and their silks; Festival Grade 1 winners' silks
• Two-period scoreboard, model evaluation, drift over time, limitations and a findings register
• Case studies, each-way and the Placepot, a race-day audit sheet to print or copy, research audit, glossary and method

WHAT YOU GET
• One zip holding the colour PDF and the black-and-white print PDF, 198 pages each.

WHO IT'S FOR
Experienced form students, handicap followers and data-minded racing fans who want the full evidence (handicap marks, the handicapper's view, the ZANS rating and price bands), with the method and limits shown, before forming their own view.

GOOD TO KNOW
• Instant download: after purchase, sign in to Etsy in a mobile browser or on a computer, then go to Purchases and download your files. On an iPhone, tap the zip in the Files app to open it.
• Two PDFs: a full colour version and a mainly black-and-white print version (jockey colours are kept in colour).
• Tick boxes on each distance's all-going and going pages can be tapped in compatible PDF apps, or print the guide and tick by hand.
• Information and entertainment only. This guide is informational and does not make selections or guarantee future outcomes.
• ZANS is not connected with or approved by Cheltenham Racecourse or any jockey, trainer or owner named.
• Maps, charts and jockey colours were drawn by ZANS with the help of AI design tools. All figures are ZANS's own analysis.

RETURNS
Digital download: if you agreed at checkout to start the download straight away, you may lose your 14-day right to cancel once the file is available. If a file won't open or isn't as described, message us and we'll fix it or refund you. This doesn't affect your statutory rights.

MORE FROM ZANS
Also available: the Cheltenham Jumps Beginner and Advanced editions as separate listings, plus the Ascot Jumps and Ascot Flat guides. More racecourses are on the way.
````

### 13. 4622635592 - Advanced guide - Kempton All-Weather Racecourse Guide PDF Advanced - Horse Racing Form and Going Analysis, Polytrack
https://www.etsy.com/listing/4622635592  | £12.49 | 0 views lifetime | 0 favourites | section: All-Weather Guides

**BEFORE title (128):** Kempton All-Weather Racecourse Guide PDF Advanced - Horse Racing Betting Form by Distance and Going, Instant Download, Track DNA
**AFTER title (99):** Kempton All-Weather Racecourse Guide PDF Advanced - Horse Racing Form and Going Analysis, Polytrack

**BEFORE tags:** kempton betting | kempton form | kempton racing | all weather form | flat form guide | polytrack racing | draw bias guide | trainer form guide | horse racing value | placepot guide pdf | racecourse guide pdf | horse racing gift | gift for racing fan
**AFTER tags (13):** kempton form | kempton going guide | polytrack form guide | draw bias guide | horse racing form | going and distance | racing value guide | form analysis pdf | racecourse form pdf | horse racing guide | handicap form guide | over bet guide | placepot guide pdf
Tags kept 3, new 10.

**Primary keyword:** kempton all-weather form guide pdf
**Secondary keywords:** form analysis guide, horse racing form guide, each way guide pdf, racing going guide
**Extra phrases covered:** form study, value and over-bet, trainer form, course meeting hook
**Audience and why:** The racing follower who already goes to Kempton All-Weather or backs horses there and searches for form, going and each-way study material. Own vocabulary (form, betting, going, each-way) so it does not compete with the Beginner gift listing or the Pro statistics listing.

**Category:** Books, Movies & Music > Books > Guides & How Tos (section: All-Weather Guides).
**Attributes now:** Primary color=Green; Secondary color=Orange; Self-published=Yes; Book format=eBook; Number of pages=26
**Attribute / category actions:** No change needed (category and attributes consistent with the product)

**FULL NEW DESCRIPTION (2923 characters):**

````text
Kempton all-weather form guide and horse racing form analysis PDF (Advanced edition) for Polytrack Flat racing: value and over-bet points for each of the six main distances, with the draw and the pace measured against the starting prices. Course data to help you know the track before the off. Includes a full colour version AND a black-and-white printable version. Digital file only, nothing is posted.

Each point shows how often that kind of horse won and whether it won more or less often than its odds said, tagged VALUE, AS PRICED, OVER-BET or LONGSHOT, and each pattern is checked in two periods, 2019-21 and 2022-26. It is different research from the Beginner edition, not a copy with extra pages. Figures are ZANS's own analysis of 3,467 Kempton all-weather races with a full set of starting prices (34,131 runners), January 2019 to November 2026.

WHAT'S INSIDE (26 pages)
• Pick your distance, how the Advanced edition works, and the course, the draw and the pace at a glance
• Every main distance: value and over-bet points, best case and worst case
• The draw and the pace against the odds, by distance and field size
• The price: where the odds were right and wrong at Kempton
• Trainers, jockeys and partnerships against the odds
• Smart money: outsider specialists
• The Placepot (a pool bet) and a race-day checklist
• Big-race winners' colours, 2026 and 2025
• Summary for every main distance, glossary

WHAT YOU GET
• One zip holding the colour PDF and the black-and-white print PDF, 26 pages each.

WHO IT'S FOR
Regular racegoers, each-way and Placepot players and form readers who know the basics and want value, draw and price context at Kempton on the all-weather.

GOOD TO KNOW
• Instant download: after purchase, sign in to Etsy in a mobile browser or on a computer, then go to Purchases and download your files. On an iPhone, tap the zip in the Files app to open it.
• Two PDFs: a full colour version and a mainly black-and-white print version (jockey colours are kept in colour).
• Tick boxes on the distance pages and the race-day checklist can be tapped in compatible PDF apps, or print the guide and tick by hand.
• Information and entertainment only. This guide is informational and does not make selections or guarantee future outcomes.
• ZANS is not connected with or approved by Kempton Park Racecourse or any jockey, trainer or owner named.
• Maps, charts and jockey colours were drawn by ZANS with the help of AI design tools. All figures are ZANS's own analysis.

RETURNS
Digital download: if you agreed at checkout to start the download straight away, you may lose your 14-day right to cancel once the file is available. If a file won't open or isn't as described, message us and we'll fix it or refund you. This doesn't affect your statutory rights.

MORE FROM ZANS
Also available: the Kempton All-Weather Beginner and Pro editions as separate listings, plus the Cheltenham Jumps, Ascot Jumps and Ascot Flat guides. More racecourses are on the way.
````

### 14. 4622635374 - Beginner guide - Kempton All-Weather Racecourse Guide PDF for Beginners, Horse Racing Gift, Floodlit Evenings, Download
https://www.etsy.com/listing/4622635374  | £7.49 | 0 views lifetime | 0 favourites | section: All-Weather Guides

**BEFORE title (117):** Kempton All-Weather Racecourse Guide PDF Beginner - Horse Racing Gift for Racegoers, Instant Download, Track DNA 2027
**AFTER title (102):** Kempton All-Weather Racecourse Guide PDF for Beginners, Horse Racing Gift, Floodlit Evenings, Download

**BEFORE tags:** kempton races | kempton guide pdf | kempton park gift | racecourse guide | all weather racing | jockey colours guide | racecourse day out | beginners racing | flat racing guide | horse racing present | racecourse guide pdf | horse racing gift | gift for racing fan
**AFTER tags (13):** kempton races | kempton guide pdf | polytrack racing | racing under lights | racing for beginners | first night racing | horse racing gift | learn horse racing | racing words guide | race meeting guide | jockey colours guide | beginners racing pdf | racing glossary pdf
Tags kept 4, new 9.

**Primary keyword:** kempton all-weather racecourse guide for beginners
**Secondary keywords:** kempton all-weather races, kempton all-weather guide pdf, horse racing gift for beginners, first time racegoer gift
**Extra phrases covered:** racing for beginners, racecourse day out, horse racing present, gift for dad / mum / grandad who loves racing
**Audience and why:** The gift buyer or new racegoer heading to Kempton All-Weather who searches by course name or for a racing present and wants something instant and easy. Different from the Advanced and Pro editions, which target form students; this one carries the gift, first-timer and day-out vocabulary.

**Category:** Books, Movies & Music > Books > Guides & How Tos (section: All-Weather Guides).
**Attributes now:** Primary color=Green; Secondary color=Orange; Self-published=Yes; Book format=eBook; Number of pages=13
**Attribute / category actions:** No change needed (category and attributes consistent with the product)

**FULL NEW DESCRIPTION (2990 characters):**

````text
Kempton all-weather racecourse guide for beginners to Flat racing: a simple instant-download PDF and horse racing gift for a race day or an evening under the floodlights at Kempton, covering the starting stalls, the draw, the pace, the Polytrack surface and the jockey colours. Course data to help you know the track before the off. Includes a full colour version AND a black-and-white printable version. Digital file only, nothing is posted.

Each of the six main all-weather distances raced at Kempton (6f to 1m7f218y) gets simple advice in plain words: how often the favourite won, the good signs and warning signs to check your horse against, how the draw and the pace played out, and the jockey colours to look out for. Figures are ZANS's own analysis of 3,489 Kempton all-weather races, January 2019 to November 2026.

WHAT'S INSIDE (13 pages)
• Start here: three easy steps, every main distance with its page number, and Kempton all-weather at a glance
• The course map: the inner and outer loops, right-handed, with a numbered key
• Stalls, the draw, the pace and the Polytrack surface explained
• Trainers, jockeys and their colours
• Big-race winners' colours, 2026 and 2025
• Simple advice for every main distance
• Advice for beginners, a race-day checklist with tick boxes, and words to know

WHAT YOU GET
• One zip holding the colour PDF and the black-and-white print PDF, 13 pages each.

WHO IT'S FOR
New racegoers, family and friends heading to Kempton for a Flat meeting on the all-weather, and anyone who wants a clear starting point before reading a racecard.

GIFT IDEAS
A racing gift for dad, mum, grandad or a friend heading to a race meeting for the first time, for a birthday, Father's Day or Christmas. Instant download, so nothing to post and nothing to wrap.

GOOD TO KNOW
• Instant download: after purchase, sign in to Etsy in a mobile browser or on a computer, then go to Purchases and download your files. On an iPhone, tap the zip in the Files app to open it.
• Two PDFs: a full colour version and a mainly black-and-white print version (jockey colours are kept in colour).
• The race-day checklist has tick boxes you can tap in compatible PDF apps, or print it and tick by hand.
• Information and entertainment only. This guide is informational and does not make selections or guarantee future outcomes.
• ZANS is not connected with or approved by Kempton Park Racecourse or any jockey, trainer or owner named.
• Maps, charts and jockey colours were drawn by ZANS with the help of AI design tools. All figures are ZANS's own analysis.

RETURNS
Digital download: if you agreed at checkout to start the download straight away, you may lose your 14-day right to cancel once the file is available. If a file won't open or isn't as described, message us and we'll fix it or refund you. This doesn't affect your statutory rights.

MORE FROM ZANS
Also available: the Kempton All-Weather Advanced and Pro editions as separate listings, plus the Cheltenham Jumps, Ascot Jumps and Ascot Flat guides. More racecourses are on the way.
````

### 15. 4622627387 - Pro guide - Kempton All-Weather Racecourse Guide PDF Pro - 119-Page Horse Racing Statistics Book, Polytrack, Download
https://www.etsy.com/listing/4622627387  | £20.82 | 0 views lifetime | 0 favourites | section: All-Weather Guides

**BEFORE title (118):** Kempton All-Weather Racecourse Guide PDF Pro - 119-Page Horse Racing Statistics Book, Instant Download, Track DNA Gift
**AFTER title (105):** Kempton All-Weather Racecourse Guide PDF Pro - 119-Page Horse Racing Statistics Book, Polytrack, Download

**BEFORE tags:** all weather stats | flat racing data | polytrack statistics | draw statistics | racing handbook pdf | trainer statistics | jockey statistics | racing data pdf | racing research pdf | form study pdf | racecourse guide pdf | horse racing gift | gift for racing fan
**AFTER tags (13):** kempton stats | draw statistics | polytrack statistics | racing stats book | racing data guide | horse racing manual | racing numbers pdf | racing evidence pdf | racing study guide | jockey stats pdf | trainer stats pdf | handicap analysis | racing method pdf
Tags kept 2, new 11.

**Primary keyword:** kempton all-weather horse racing statistics
**Secondary keywords:** horse racing data book, racing ratings pdf, horse racing ebook, racing research pdf
**Extra phrases covered:** racing analysis, trainer jockey stats, handicap data, form student gift
**Audience and why:** The data-minded form student who searches for statistics, ratings and research for Kempton All-Weather. Own vocabulary (statistics, data, ratings, ebook, research) separate from the Beginner gift and Advanced form listings.

**Category:** Books, Movies & Music > Books > Guides & How Tos (section: All-Weather Guides).
**Attributes now:** Primary color=Green; Secondary color=Orange; Self-published=Yes; Book format=eBook; Number of pages=119
**Attribute / category actions:** No change needed (category and attributes consistent with the product)

**FULL NEW DESCRIPTION (2876 characters):**

````text
Kempton all-weather horse racing statistics book and data PDF (Pro edition): a 119-page Flat racing research manual for Kempton's Polytrack, with course evidence by distance, draw, pace and price, every finding checked in two periods and its limits stated. Course data to help you know the track before the off. Includes a full colour version AND a black-and-white printable version. Digital file only, nothing is posted.

Built from 5,219 Kempton all-weather races and 52,040 runners, January 2015 to 18 November 2026. Every group is compared with the margin-free starting prices in 2015-20 and again in 2021-26, with ranges and sample sizes shown, so you can see which patterns held and which did not.

WHAT'S INSIDE (119 pages)
• Distance by distance: profiles, price bands and two-period figures for the main Kempton all-weather distances, with tick boxes
• Price calibration and the price map
• Big prices and high odds by distance
• Kempton returners and the 2027 returner list
• The handicapper's lens and the ZANS ratings lab
• Pace and running style, and the draw
• Trainers and jockeys against the odds; jockeys and their silks; big-race winners' silks
• Findings register, case studies, each-way and the Placepot, a race-day audit sheet, research audit, glossary and method

WHAT YOU GET
• One zip holding the colour PDF and the black-and-white print PDF, 119 pages each.

WHO IT'S FOR
Experienced form students, handicap followers and data-minded racing fans who want the full evidence (handicap marks, the draw, the pace and price bands), with the method and limits shown, before forming their own view.

GOOD TO KNOW
• Instant download: after purchase, sign in to Etsy in a mobile browser or on a computer, then go to Purchases and download your files. On an iPhone, tap the zip in the Files app to open it.
• Two PDFs: a full colour version and a mainly black-and-white print version (jockey colours are kept in colour).
• Tick boxes on the distance pages can be tapped in compatible PDF apps, or print the guide and tick by hand. The race-day audit sheet is there to fill in.
• Information and entertainment only. This guide is informational and does not make selections or guarantee future outcomes.
• ZANS is not connected with or approved by Kempton Park Racecourse or any jockey, trainer or owner named.
• Maps, charts and jockey colours were drawn by ZANS with the help of AI design tools. All figures are ZANS's own analysis.

RETURNS
Digital download: if you agreed at checkout to start the download straight away, you may lose your 14-day right to cancel once the file is available. If a file won't open or isn't as described, message us and we'll fix it or refund you. This doesn't affect your statutory rights.

MORE FROM ZANS
Also available: the Kempton All-Weather Beginner and Advanced editions as separate listings, plus the Cheltenham Jumps, Ascot Jumps and Ascot Flat guides. More racecourses are on the way.
````

### 16. 4622626437 - Advanced guide - Kempton Jumps Racecourse Guide PDF Advanced - Horse Racing Form and Going Analysis, Download
https://www.etsy.com/listing/4622626437  | £12.49 | 0 views lifetime | 0 favourites | section: Jumps Racecourse Guides

**BEFORE title (122):** Kempton Jumps Racecourse Guide PDF Advanced - Horse Racing Betting Form by Distance and Going, Instant Download, Track DNA
**AFTER title (92):** Kempton Jumps Racecourse Guide PDF Advanced - Horse Racing Form and Going Analysis, Download

**BEFORE tags:** kempton betting | kempton form guide | king george chase | boxing day betting | jumps betting guide | chase form guide | hurdles form guide | each way guide pdf | national hunt form | christmas hurdle | racecourse guide pdf | horse racing gift | gift for racing fan
**AFTER tags (13):** kempton form | kempton going guide | king george form | christmas hurdle | horse racing form | racing form guide | price and form pdf | each way form pdf | going and distance | racing value guide | form analysis pdf | racecourse form pdf | horse racing guide
Tags kept 1, new 12.

**Primary keyword:** kempton jumps form guide pdf
**Secondary keywords:** form analysis guide, horse racing form guide, each way guide pdf, racing going guide
**Extra phrases covered:** form study, value and over-bet, trainer form, course meeting hook
**Audience and why:** The racing follower who already goes to Kempton Jumps or backs horses there and searches for form, going and each-way study material. Own vocabulary (form, betting, going, each-way) so it does not compete with the Beginner gift listing or the Pro statistics listing.

**Category:** Books, Movies & Music > Books > Guides & How Tos (section: Jumps Racecourse Guides).
**Attributes now:** Primary color=Green; Secondary color=Green; Self-published=Yes; Number of pages=36; Book format=eBook
**Attribute / category actions:** No change needed (category and attributes consistent with the product)

**FULL NEW DESCRIPTION (2973 characters):**

````text
Kempton Park jumps form guide and horse racing form analysis PDF for the Christmas meeting with the King George VI Chase: value and over-bet points for each of the 7 main hurdle, chase and bumper distances, split by going (ground conditions) where there are enough races. Course data to help you know the track before the off. Includes a full colour version AND a black-and-white printable version. Digital file only, nothing is posted.

Going to Kempton Park on Boxing Day (26 December) for the King George VI Chase meeting? This guide shows how the course rides at every distance and on every going before you go.

Each point shows how often that kind of horse won and whether it won more or less often than its odds said, tagged VALUE, AS PRICED, OVER-BET or LONGSHOT. It is different research from the Beginner edition, not a copy with extra pages. Figures are ZANS's own analysis of 531 Kempton jumps races, January 2019 to March 2026.

WHAT'S INSIDE (36 pages)
• Pick your distance, how the Advanced edition works, the course map and the going explained
• Every main distance: value and over-bet points, by going where there are enough races (23 pages)
• The price: where Kempton pays over jumps
• Trainers, jockeys and partnerships against the odds
• Smart money: outsider specialists and short-priced names
• The Placepot (a pool bet) and a race-day checklist
• Big-race winners' colours, 2025-26 and 2024-25
• Summary for every main distance, glossary

WHAT YOU GET
• One zip holding the colour PDF and the black-and-white print PDF, 36 pages each.

WHO IT'S FOR
Regular racegoers, each-way and Placepot players and form readers who know the basics and want value and price context at Kempton over jumps, Boxing Day included.

GOOD TO KNOW
• Instant download: after purchase, sign in to Etsy in a mobile browser or on a computer, then go to Purchases and download your files. On an iPhone, tap the zip in the Files app to open it.
• Two PDFs: a full colour version and a mainly black-and-white print version (jockey colours are kept in colour).
• Tick boxes on the how-to page, each distance-and-going page and the race-day checklist can be tapped in compatible PDF apps, or print the guide and tick by hand.
• Information and entertainment only. This guide is informational and does not make selections or guarantee future outcomes.
• ZANS is not connected with or approved by Kempton Park Racecourse or any jockey, trainer or owner named.
• Maps, charts and jockey colours were drawn by ZANS with the help of AI design tools. All figures are ZANS's own analysis.

RETURNS
Digital download: if you agreed at checkout to start the download straight away, you may lose your 14-day right to cancel once the file is available. If a file won't open or isn't as described, message us and we'll fix it or refund you. This doesn't affect your statutory rights.

MORE FROM ZANS
Also available: the Kempton Jumps Beginner and Pro editions as separate listings, plus the Cheltenham Jumps and Ascot guides. More racecourses are on the way.
````

### 17. 4622634750 - Beginner guide - Kempton Park Racecourse Guide PDF for Beginners, Horse Racing Gift, King George, Instant Download
https://www.etsy.com/listing/4622634750  | £7.49 | 0 views lifetime | 0 favourites | section: Jumps Racecourse Guides

**BEFORE title (111):** Kempton Jumps Racecourse Guide PDF Beginner - Horse Racing Gift for Racegoers, Instant Download, Track DNA 2027
**AFTER title (97):** Kempton Park Racecourse Guide PDF for Beginners, Horse Racing Gift, King George, Instant Download

**BEFORE tags:** kempton park | kempton races | kempton guide pdf | boxing day gift | racing gift for dad | jumps racing guide | national hunt guide | christmas racing | racing stocking gift | jump racing basics | racecourse guide pdf | horse racing gift | gift for racing fan
**AFTER tags (13):** kempton races | kempton guide pdf | king george chase | boxing day racing | racing for beginners | first kempton visit | horse racing gift | new racegoer gift | racing starter guide | horse racing basics | learn horse racing | racing words guide | race meeting guide
Tags kept 3, new 10.

**Primary keyword:** kempton jumps racecourse guide for beginners
**Secondary keywords:** kempton jumps races, kempton jumps guide pdf, horse racing gift for beginners, first time racegoer gift
**Extra phrases covered:** racing for beginners, racecourse day out, horse racing present, gift for dad / mum / grandad who loves racing
**Audience and why:** The gift buyer or new racegoer heading to Kempton Jumps who searches by course name or for a racing present and wants something instant and easy. Different from the Advanced and Pro editions, which target form students; this one carries the gift, first-timer and day-out vocabulary.

**Category:** Books, Movies & Music > Books > Guides & How Tos (section: Jumps Racecourse Guides).
**Attributes now:** Primary color=Green; Secondary color=Green; Self-published=Yes; Book format=eBook; Number of pages=15
**Attribute / category actions:** No change needed (category and attributes consistent with the product)

**FULL NEW DESCRIPTION (3182 characters):**

````text
Kempton Park racecourse guide for beginners to horse racing over jumps: a simple instant-download PDF and Christmas horse racing gift for the Christmas meeting with the King George VI Chase on Boxing Day, covering hurdles, chases, bumpers, the going and the jockey colours. Course data to help you know the track before the off. Includes a full colour version AND a black-and-white printable version. Digital file only, nothing is posted.

Going to Kempton Park on Boxing Day (26 December) for the King George VI Chase meeting? This guide shows how the course rides at every distance and on every going before you go.

Each of the 7 main hurdle, chase and bumper distances raced at Kempton gets simple advice in plain words: how often the favourite won, the good signs and warning signs to check your horse against, and the jockey colours to look out for. Figures are ZANS's own analysis of 531 Kempton jumps races, January 2019 to March 2026.

WHAT'S INSIDE (15 pages)
• Start here: three easy steps, every main distance with its page number, and Kempton jumps at a glance
• The course map: the right-handed triangle, with a numbered key
• Hurdles, fences, bumpers and ground conditions explained
• Jumps racing explained in pictures
• Jockeys, trainers and their colours
• Big-race winners' colours, 2024-25 and 2025-26
• Simple advice for every main distance (4 pages)
• Advice for beginners, a race-day checklist with tick boxes, and words to know

WHAT YOU GET
• One zip holding the colour PDF and the black-and-white print PDF, 15 pages each.

WHO IT'S FOR
New racegoers, family and friends heading to Kempton for a jumps meeting (Boxing Day included), and anyone who wants a clear starting point before reading a racecard.

GIFT IDEAS
A racing gift for dad, mum, grandad or a friend heading to a race meeting for the first time, for a birthday, Father's Day or Christmas. Instant download, so nothing to post and nothing to wrap.

GOOD TO KNOW
• Instant download: after purchase, sign in to Etsy in a mobile browser or on a computer, then go to Purchases and download your files. On an iPhone, tap the zip in the Files app to open it.
• Two PDFs: a full colour version and a mainly black-and-white print version (jockey colours are kept in colour).
• The race-day checklist has tick boxes you can tap in compatible PDF apps, or print it and tick by hand.
• Information and entertainment only. This guide is informational and does not make selections or guarantee future outcomes.
• ZANS is not connected with or approved by Kempton Park Racecourse or any jockey, trainer or owner named.
• The photos and explainer pictures were made with AI image tools. Maps, charts and jockey colours were drawn by ZANS with the help of AI design tools. All figures are ZANS's own analysis.

RETURNS
Digital download: if you agreed at checkout to start the download straight away, you may lose your 14-day right to cancel once the file is available. If a file won't open or isn't as described, message us and we'll fix it or refund you. This doesn't affect your statutory rights.

MORE FROM ZANS
Also available: the Kempton Jumps Advanced and Pro editions as separate listings, plus the Cheltenham Jumps and Ascot guides. More racecourses are on the way.
````

### 18. 4622635120 - Pro guide - Kempton Jumps Racecourse Guide PDF Pro - 132-Page Horse Racing Statistics Book, Instant Download
https://www.etsy.com/listing/4622635120  | £20.82 | 0 views lifetime | 0 favourites | section: Jumps Racecourse Guides

**BEFORE title (112):** Kempton Jumps Racecourse Guide PDF Pro - 132-Page Horse Racing Statistics Book, Instant Download, Track DNA Gift
**AFTER title (96):** Kempton Jumps Racecourse Guide PDF Pro - 132-Page Horse Racing Statistics Book, Instant Download

**BEFORE tags:** racing stats pdf | jumps racing data | race form analysis | racing ratings pdf | handicap analysis | trainer jockey data | racing data book | form student gift | chase statistics | hurdle race data | racecourse guide pdf | horse racing gift | gift for racing fan
**AFTER tags (13):** kempton stats | kempton jumps data | national hunt data | racing research pdf | form student gift | racing handbook pdf | racing stats book | racing data guide | horse racing manual | racing numbers pdf | racing evidence pdf | racing study guide | jockey stats pdf
Tags kept 1, new 12.

**Primary keyword:** kempton jumps horse racing statistics
**Secondary keywords:** horse racing data book, racing ratings pdf, horse racing ebook, racing research pdf
**Extra phrases covered:** racing analysis, trainer jockey stats, handicap data, form student gift
**Audience and why:** The data-minded form student who searches for statistics, ratings and research for Kempton Jumps. Own vocabulary (statistics, data, ratings, ebook, research) separate from the Beginner gift and Advanced form listings.

**Category:** Books, Movies & Music > Books > Guides & How Tos (section: Jumps Racecourse Guides).
**Attributes now:** Primary color=Green; Secondary color=Green; Self-published=Yes; Book format=eBook; Number of pages=132
**Attribute / category actions:** No change needed (category and attributes consistent with the product)

**FULL NEW DESCRIPTION (3182 characters):**

````text
Kempton Park jumps horse racing statistics book and data PDF (Pro edition): a 132-page National Hunt research manual, Christmas meeting included, with course evidence by distance and going for hurdles, chases and bumpers, every finding checked in two periods and its limits stated. Course data to help you know the track before the off. Includes a full colour version AND a black-and-white printable version. Digital file only, nothing is posted.

Going to Kempton Park on Boxing Day (26 December) for the King George VI Chase meeting? This guide shows how the course rides at every distance and on every going before you go.

Built from 883 Kempton jumps races and 7,089 runners, January 2015 to 23 March 2026. Every group is compared with the margin-free starting prices in 2015-20 and again in 2021-26, with ranges and sample sizes shown, so you can see which patterns held and which did not.

WHAT'S INSIDE (132 pages)
• Distance by distance: profiles, price bands and two-period figures for the Kempton jumps distances, with tick boxes
• Price calibration, the price map and the value decision
• Big prices and high odds by distance
• Kempton returners: the historical signal, the 2027 returner list and returner profiles
• The handicapper's lens, the ZANS rating lab, fences v hurdles and jumping, going
• Trainers and jockeys against the odds; jockeys, trainers and their silks; big-race winners' silks
• Two-period scoreboard, model evaluation, drift over time, limitations and a findings register
• Case studies, each-way and the Placepot, a race-day audit sheet to print or copy, research audit, glossary and method

WHAT YOU GET
• One zip holding the colour PDF and the black-and-white print PDF, 132 pages each.

WHO IT'S FOR
Experienced form students, handicap followers and data-minded racing fans who want the full evidence (handicap marks, the handicapper's view, the ZANS rating and price bands), with the method and limits shown, before forming their own view.

GOOD TO KNOW
• Instant download: after purchase, sign in to Etsy in a mobile browser or on a computer, then go to Purchases and download your files. On an iPhone, tap the zip in the Files app to open it.
• Two PDFs: a full colour version and a mainly black-and-white print version (jockey colours are kept in colour).
• Tick boxes in the distance-by-distance chapter can be tapped in compatible PDF apps, or print the guide and tick by hand.
• Information and entertainment only. This guide is informational and does not make selections or guarantee future outcomes.
• ZANS is not connected with or approved by Kempton Park Racecourse or any jockey, trainer or owner named.
• Maps, charts and jockey colours were drawn by ZANS with the help of AI design tools. All figures are ZANS's own analysis.

RETURNS
Digital download: if you agreed at checkout to start the download straight away, you may lose your 14-day right to cancel once the file is available. If a file won't open or isn't as described, message us and we'll fix it or refund you. This doesn't affect your statutory rights.

MORE FROM ZANS
Also available: the Kempton Jumps Beginner and Advanced editions as separate listings, plus the Cheltenham Jumps and Ascot guides. More racecourses are on the way.
````

### 19. 4622672428 - Advanced guide - Sandown Park Racecourse Guide PDF Advanced - Horse Racing Form and Going Analysis, Download
https://www.etsy.com/listing/4622672428  | £12.49 | 0 views lifetime | 0 favourites | section: Jumps Racecourse Guides

**BEFORE title (127):** Sandown Park Racecourse Guide PDF Advanced - Horse Racing Betting Form by Distance and Going, Instant Download, Jumps Track DNA
**AFTER title (91):** Sandown Park Racecourse Guide PDF Advanced - Horse Racing Form and Going Analysis, Download

**BEFORE tags:** sandown betting | sandown form guide | tingle creek chase | celebration chase | imperial cup | chase betting pdf | hurdle betting guide | each way racing | jumps placepot pdf | jumps form pdf | racecourse guide pdf | horse racing gift | gift for racing fan
**AFTER tags (13):** sandown form | sandown going guide | tingle creek form | sandown chase form | horse racing form | racing going guide | form study pdf | trainer form guide | racing form guide | form analysis pdf | each way form pdf | going and distance | racing value guide
Tags kept 0, new 13.

**Primary keyword:** sandown park form guide pdf
**Secondary keywords:** form analysis guide, horse racing form guide, each way guide pdf, racing going guide
**Extra phrases covered:** form study, value and over-bet, trainer form, course meeting hook
**Audience and why:** The racing follower who already goes to Sandown Park or backs horses there and searches for form, going and each-way study material. Own vocabulary (form, betting, going, each-way) so it does not compete with the Beginner gift listing or the Pro statistics listing.

**Category:** Books, Movies & Music > Books > Guides & How Tos (section: Jumps Racecourse Guides).
**Attributes now:** Primary color=Green; Self-published=Yes; Book format=eBook; Number of pages=28; Secondary color=Blue
**Attribute / category actions:** No change needed (category and attributes consistent with the product)

**FULL NEW DESCRIPTION (2784 characters):**

````text
Sandown Park form guide and horse racing form analysis PDF for the Tingle Creek meeting and the rest of the jumps season: value and over-bet points for each of the 5 main hurdle and chase distances, split by going (ground conditions) where there are enough races. Course data to help you know the track before the off. Includes a full colour version AND a black-and-white printable version. Digital file only, nothing is posted.

Each point shows how often that kind of horse won and whether it won more or less often than its odds said, tagged VALUE, AS PRICED, OVER-BET or LONGSHOT. It is different research from the Beginner edition, not a copy with extra pages. Figures are ZANS's own analysis of 395 Sandown jumps races, January 2019 to April 2026.

WHAT'S INSIDE (28 pages)
• Pick your distance, how the Advanced edition works, the course map and the going explained
• Every main distance: value and over-bet points, by going where there are enough races (15 pages)
• The price: where the odds were right and wrong
• Trainers and jockeys against the odds
• Smart money: outsider specialists and short-priced names
• The Placepot (a pool bet) and a race-day checklist
• Big-race winners' colours, 2025-26 and 2024-25
• Summary for every main distance, glossary

WHAT YOU GET
• One zip holding the colour PDF and the black-and-white print PDF, 28 pages each.

WHO IT'S FOR
Regular racegoers, each-way and Placepot players and form readers who know the basics and want value and price context at Sandown over jumps, the Tingle Creek meeting included.

GOOD TO KNOW
• Instant download: after purchase, sign in to Etsy in a mobile browser or on a computer, then go to Purchases and download your files. On an iPhone, tap the zip in the Files app to open it.
• Two PDFs: a full colour version and a mainly black-and-white print version (jockey colours are kept in colour).
• Tick boxes on the distance-and-going pages and the race-day checklist can be tapped in compatible PDF apps, or print the guide and tick by hand.
• Information and entertainment only. This guide is informational and does not make selections or guarantee future outcomes.
• ZANS is not connected with or approved by Sandown Park Racecourse or any jockey, trainer or owner named.
• Maps, charts and jockey colours were drawn by ZANS with the help of AI design tools. All figures are ZANS's own analysis.

RETURNS
Digital download: if you agreed at checkout to start the download straight away, you may lose your 14-day right to cancel once the file is available. If a file won't open or isn't as described, message us and we'll fix it or refund you. This doesn't affect your statutory rights.

MORE FROM ZANS
Also available: the Sandown Jumps Beginner and Pro editions as separate listings, plus the Kempton, Cheltenham Jumps and Ascot guides. More racecourses are on the way.
````

### 20. 4622672152 - Beginner guide - Sandown Park Racecourse Guide PDF for Beginners, Horse Racing Gift, Tingle Creek, Instant Download
https://www.etsy.com/listing/4622672152  | £7.49 | 0 views lifetime | 0 favourites | section: Jumps Racecourse Guides

**BEFORE title (116):** Sandown Park Racecourse Guide PDF Beginner - Horse Racing Gift for Racegoers, Instant Download, Jumps Track DNA 2027
**AFTER title (98):** Sandown Park Racecourse Guide PDF for Beginners, Horse Racing Gift, Tingle Creek, Instant Download

**BEFORE tags:** sandown park | sandown races | sandown guide pdf | tingle creek | gift for racing fan | jump racing gift | beginner racing pdf | racing day out | racegoer gift idea | hurdles and chases | racecourse guide pdf | horse racing gift | sandown racecourse
**AFTER tags (13):** sandown races | sandown guide pdf | sandown park guide | tingle creek day | racing for beginners | first jumps meeting | horse racing gift | gift for racing fan | racecourse day out | racing day out gift | new racegoer gift | racing starter guide | horse racing basics
Tags kept 4, new 9.

**Primary keyword:** sandown park racecourse guide for beginners
**Secondary keywords:** sandown park races, sandown park guide pdf, horse racing gift for beginners, first time racegoer gift
**Extra phrases covered:** racing for beginners, racecourse day out, horse racing present, gift for dad / mum / grandad who loves racing
**Audience and why:** The gift buyer or new racegoer heading to Sandown Park who searches by course name or for a racing present and wants something instant and easy. Different from the Advanced and Pro editions, which target form students; this one carries the gift, first-timer and day-out vocabulary.

**Category:** Books, Movies & Music > Books > Guides & How Tos (section: Jumps Racecourse Guides).
**Attributes now:** Primary color=Green; Self-published=Yes; Book format=eBook; Number of pages=14; Secondary color=Blue
**Attribute / category actions:** No change needed (category and attributes consistent with the product)

**FULL NEW DESCRIPTION (2998 characters):**

````text
Sandown Park racecourse guide for beginners to horse racing over jumps: a simple instant-download PDF and horse racing gift for a race day at Sandown, with the Tingle Creek meeting in December, covering hurdles, chases, bumpers, the going and the jockey colours. Course data to help you know the track before the off. Includes a full colour version AND a black-and-white printable version. Digital file only, nothing is posted.

Each of the 5 main hurdle and chase distances raced at Sandown gets simple advice in plain words: how often the favourite won, the good signs and warning signs to check your horse against, and the jockey colours to look out for. Figures are ZANS's own analysis of 395 Sandown jumps races, January 2019 to April 2026.

WHAT'S INSIDE (14 pages)
• Start here: three easy steps and every main distance with its page number
• The course map: the right-handed oval with its uphill finish, with a numbered key
• Hurdles, fences, bumpers and ground conditions explained
• Jumps racing explained in pictures
• Trainers, jockeys and their colours
• Big-race winners' colours, 2024-25 and 2025-26
• Simple advice for every main distance (3 pages)
• Advice for beginners, a race-day checklist with tick boxes, and words to know

WHAT YOU GET
• One zip holding the colour PDF and the black-and-white print PDF, 14 pages each.

WHO IT'S FOR
New racegoers, family and friends heading to Sandown for a jumps meeting (the Tingle Creek meeting included), and anyone who wants a clear starting point before reading a racecard.

GIFT IDEAS
A racing gift for dad, mum, grandad or a friend heading to a race meeting for the first time, for a birthday, Father's Day or Christmas. Instant download, so nothing to post and nothing to wrap.

GOOD TO KNOW
• Instant download: after purchase, sign in to Etsy in a mobile browser or on a computer, then go to Purchases and download your files. On an iPhone, tap the zip in the Files app to open it.
• Two PDFs: a full colour version and a mainly black-and-white print version (jockey colours are kept in colour).
• The race-day checklist has tick boxes you can tap in compatible PDF apps, or print it and tick by hand.
• Information and entertainment only. This guide is informational and does not make selections or guarantee future outcomes.
• ZANS is not connected with or approved by Sandown Park Racecourse or any jockey, trainer or owner named.
• The photos and explainer pictures were made with AI image tools. Maps, charts and jockey colours were drawn by ZANS with the help of AI design tools. All figures are ZANS's own analysis.

RETURNS
Digital download: if you agreed at checkout to start the download straight away, you may lose your 14-day right to cancel once the file is available. If a file won't open or isn't as described, message us and we'll fix it or refund you. This doesn't affect your statutory rights.

MORE FROM ZANS
Also available: the Sandown Jumps Advanced and Pro editions as separate listings, plus the Kempton, Cheltenham Jumps and Ascot guides. More racecourses are on the way.
````

### 21. 4622672622 - Pro guide - Sandown Park Racecourse Guide PDF Pro - 115-Page Horse Racing Statistics Book, Instant Download
https://www.etsy.com/listing/4622672622  | £20.82 | 0 views lifetime | 0 favourites | section: Jumps Racecourse Guides

**BEFORE title (117):** Sandown Park Racecourse Guide PDF Pro - 115-Page Horse Racing Statistics Book, Instant Download, Jumps Track DNA Gift
**AFTER title (95):** Sandown Park Racecourse Guide PDF Pro - 115-Page Horse Racing Statistics Book, Instant Download

**BEFORE tags:** racing statistics | jumps data pdf | form analysis pdf | racing ratings pdf | handicap marks | trainer stats pdf | racing research | betting data pdf | steeplechase stats | hurdling statistics | racecourse guide pdf | horse racing gift | gift for racing fan
**AFTER tags (13):** sandown stats | tingle creek data | national hunt data | racing analysis pdf | trainer jockey stats | handicap data pdf | racing research pdf | form student gift | racing handbook pdf | racing stats book | racing data guide | horse racing manual | racing numbers pdf
Tags kept 0, new 13.

**Primary keyword:** sandown park horse racing statistics
**Secondary keywords:** horse racing data book, racing ratings pdf, horse racing ebook, racing research pdf
**Extra phrases covered:** racing analysis, trainer jockey stats, handicap data, form student gift
**Audience and why:** The data-minded form student who searches for statistics, ratings and research for Sandown Park. Own vocabulary (statistics, data, ratings, ebook, research) separate from the Beginner gift and Advanced form listings.

**Category:** Books, Movies & Music > Books > Guides & How Tos (section: Jumps Racecourse Guides).
**Attributes now:** Primary color=Green; Self-published=Yes; Number of pages=115; Book format=eBook; Secondary color=Blue
**Attribute / category actions:** No change needed (category and attributes consistent with the product)

**FULL NEW DESCRIPTION (2965 characters):**

````text
Sandown Park horse racing statistics book and data PDF (Pro edition): a 115-page National Hunt research manual, Tingle Creek meeting included, with course evidence by distance and going for hurdles and chases, every finding checked in two periods and its limits stated. Course data to help you know the track before the off. Includes a full colour version AND a black-and-white printable version. Digital file only, nothing is posted.

Built from 636 Sandown jumps races and 5,262 runners, January 2015 to 25 April 2026. Every group is compared with the margin-free starting prices in 2015-20 and again in 2021-26, with ranges and sample sizes shown, so you can see which patterns held and which did not.

WHAT'S INSIDE (115 pages)
• Distance by distance: profiles, figures by going and two-period tests for the 5 main Sandown jumps distances
• Price calibration, the price map and the value decision
• Big prices and high odds by distance
• Sandown returners: the historical signal, the 2027 returner list and returner profiles
• The handicapper's lens, the ZANS ratings lab, jumps specifics, going
• Trainers and jockeys against the odds, partnerships; jockeys and their colours; big-race winners' colours
• Two-period scoreboard, model evaluation, drift over time, limitations and a findings register
• Case studies, each-way and the Placepot, a race-day audit sheet to print or copy, research audit, glossary and method

WHAT YOU GET
• One zip holding the colour PDF and the black-and-white print PDF, 115 pages each.

WHO IT'S FOR
Experienced form students, handicap followers and data-minded racing fans who want the full evidence (handicap marks, the ZANS rating and price bands), with the method and limits shown, before forming their own view.

GOOD TO KNOW
• Instant download: after purchase, sign in to Etsy in a mobile browser or on a computer, then go to Purchases and download your files. On an iPhone, tap the zip in the Files app to open it.
• Two PDFs: a full colour version and a mainly black-and-white print version (jockey colours are kept in colour).
• Tick boxes in the distance-by-distance chapter can be tapped in compatible PDF apps, or print the guide and tick by hand.
• Information and entertainment only. This guide is informational and does not make selections or guarantee future outcomes.
• ZANS is not connected with or approved by Sandown Park Racecourse or any jockey, trainer or owner named.
• Maps, charts and jockey colours were drawn by ZANS with the help of AI design tools. All figures are ZANS's own analysis.

RETURNS
Digital download: if you agreed at checkout to start the download straight away, you may lose your 14-day right to cancel once the file is available. If a file won't open or isn't as described, message us and we'll fix it or refund you. This doesn't affect your statutory rights.

MORE FROM ZANS
Also available: the Sandown Jumps Beginner and Advanced editions as separate listings, plus the Kempton, Cheltenham Jumps and Ascot guides. More racecourses are on the way.
````

### 22. 4608193933 - Mug - Horse Racing Christmas Gift Mug, Premium Jockey Silks with Name, Racehorse Owner Syndicate Cup
https://www.etsy.com/listing/4608193933  | £14.99 | 64 views lifetime | 0 favourites | section: Horse Racing Gifts

**BEFORE title (94):** Horse Racing Christmas Gift Mug, Premium Jockey Silks with Name, Racehorse Owner Syndicate Cup
**AFTER title (94):** Horse Racing Christmas Gift Mug, Premium Jockey Silks with Name, Racehorse Owner Syndicate Cup  _(unchanged)_

**BEFORE tags:** jockey silks mug | horse racing mug | racing silks mug | racehorse xmas gift | racehorse mug | racehorse owner mug | racehorse owner gift | jockey silks gift | jockey colours mug | horse racing xmas | horse racing lover | horse racing gift | racing coffee mug
**AFTER tags (13):** jockey silks mug | horse racing mug | racing silks mug | racehorse xmas gift | racehorse mug | racehorse owner mug | racehorse owner gift | jockey silks gift | jockey colours mug | horse racing xmas | horse racing lover | horse racing gift | racing coffee mug
Tags kept 13, new 0.

**Primary keyword:** jockey silks mug
**Secondary keywords:** horse racing mug, racing silks mug, racehorse owner mug, personalised mug
**Extra phrases covered:** syndicate gift mug, jockey colours mug, racehorse xmas gift
**Audience and why:** Racehorse owners and syndicates wanting their own silks on an 11oz mug. Best-viewed listing (64 views); kept stable.
**Note:** TRUE CONTROL (64 views): title, tags and description unchanged.

**Category:** Home & Living > Kitchen & Dining > Drink & Barware > Drinkware > Mugs (section: Horse Racing Gifts).
**Attributes now:** Occasion=Birthday; Holiday=Christmas; Height=9.6; Width=8.2; Dishwasher safe=Yes; Microwave safe=Yes; Volume=330; Material multi=Ceramic; Insulated=No; Home graphic=Abstract & geometric; Handle=Yes; Primary color=White; Enamel=No
**Attribute / category actions:** Occasion=Birthday while Holiday=Christmas: leave (Etsy allows one Occasion); no change

**FULL NEW DESCRIPTION (3895 characters) - unchanged from live:**

````text
PREMIUM SILKS MUG: COLOURED HANDLE AND COLOURED INSIDE - pick from 9 colours.

Horse racing mug, personalised in your own jockey silks: pick a pattern and two colours, and we print them all the way round an 11oz ceramic coffee mug, with your horse's or syndicate's name on a name plate each side of the coloured handle.

A jockey silks gift for racehorse owners, syndicate members, racegoers and every horse racing lover: for a birthday, a retirement, Father's Day or just because.

PERFECT FOR
- Racehorse owners: your racing colours on your morning cuppa
- Syndicates: a racehorse owner mug for every member
- A horse racing birthday or retirement present for a racing dad, mum or friend
- Jockeys, stable staff and breeders, in the colours they know best

COLOUR OPTION = HANDLE COLOUR
The colour you choose from the drop-down menu is the colour of the mug's HANDLE and INSIDE only. The outside of the mug is printed all the way round with your own silks design.

Every owner races in their own colours. Now yours go on your morning cuppa.

HOW TO ORDER
1. Design your mug on our online designer at www.zanshorseracing.co.uk/mug-designer : pick a pattern and your two colours, and type the name. The mug turns as you go, so you see exactly what you'll get.
2. Tap "Copy design code".
3. Come back to this listing, choose your handle colour in the menu above, paste the code in the design code box and type the name in the name box.
No time for the designer? Write the pattern and your two colours in the design code box instead (the name still goes in the name box), and we'll make it and send you a picture to check before it's printed.

CAN'T FIND YOUR SILKS?
Message us on Etsy with the name and a photo or description of the silks. We'll draw them for you free of charge and send you a preview to check before you order.

WHAT YOU CAN CHOOSE
- Pattern (25 to choose from): plain, hoops, broad hoop, stripes, broad stripes, halves, seams, braces, spots, large spots, big discs, stars, big stars, diamonds, large diamonds, triple diamonds, chevrons, broad chevrons, checks, quartered, diagonal stripes, sash, cross belts, three big spots or crosses
- Two colours from 18 racing colours
- Handle and inside colour: Black, Navy, Light Blue, Purple, Red, Pink, Orange, Yellow or Light Green
- Name: up to 28 characters including spaces, printed on a name plate on each side of the handle (long names go onto two lines)

THE MUG
- 11oz white glossy ceramic mug with a coloured handle and coloured inside
- Pattern printed all the way round, with a small ZANS Racing Tools mark
- The handle and inside are one solid colour (handles can't be printed)
- Printed to order for you by our print partner

MAKE IT A SET
Our personalised jockey silks baubles come in the same 25 silks patterns and 18 racing colours. You'll find them in our shop.

THE PERFECT SYNDICATE GIFT
One for every member, all in your horse's colours. Buying 5 or more mugs with the same design? Message us before ordering and we'll set up a group price.

GOOD TO KNOW
- Made to order: please allow up to 10 working days for us to make and send it, plus delivery time. Order early for Christmas.
- We check every design before it's printed and will message you if anything is unclear
- Any name you like, up to 28 characters; we won't print rude or offensive words
- ZANS is independent and not connected with or approved by any racecourse, owner, jockey or trainer
- The white-background photos are our print partner's previews of real ZANS designs. The racecourse and Christmas scenes were made with AI image tools to show the mugs in use. All names shown are examples.

RETURNS
Personalised items are made just for you, so we can't accept change-of-mind returns. If your mug arrives damaged, misprinted or not as described, message us with a photo and we'll replace it or refund you. This doesn't affect your statutory rights.
````

### 23. 4611213915 - Bauble - Horse Racing Christmas Gift, Green & Gold Ornament with Name, Personalised Racehorse Tree Decoration
https://www.etsy.com/listing/4611213915  | £12.99 | 76 views lifetime | 1 favourites | section: Horse Racing Gifts

**BEFORE title (100):** Horse Racing Christmas Gift, Green & Gold Ornament with Name, Personalised Racehorse Tree Decoration
**AFTER title (100):** Horse Racing Christmas Gift, Green & Gold Ornament with Name, Personalised Racehorse Tree Decoration  _(unchanged)_

**BEFORE tags:** horse racing xmas | horse racing gift | racehorse ornament | horse racing bauble | horse racing tree | racehorse decoration | christmas racehorse | jockey jersey bauble | jockey cap bauble | racing keepsake | racehorse xmas gift | racing tree bauble | horse racing decor
**AFTER tags (13):** horse racing xmas | horse racing gift | racehorse ornament | horse racing bauble | horse racing tree | racehorse decoration | christmas racehorse | jockey jersey bauble | jockey cap bauble | racing keepsake | racehorse xmas gift | racing tree bauble | horse racing decor
Tags kept 13, new 0.

**Primary keyword:** racehorse ornament
**Secondary keywords:** horse racing bauble, racehorse decoration, horse racing xmas, racehorse owner gift
**Extra phrases covered:** jockey jersey bauble, racing tree decoration, green and gold ornament, christmas racehorse
**Audience and why:** Racehorse owners, syndicate members and racing families wanting a traditional green and gold horse racing Christmas ornament with the horse's name. Best seller: change kept minimal.
**Note:** TRUE CONTROL (best seller, 4 sold): title and tags unchanged. Only change: description no longer mentions the double gold ring (final art has no rings).

**Category:** Home & Living > Home Decor > Seasonal Decor > Ornaments (section: Horse Racing Gifts).
**Attributes now:** Primary color=Green; Material multi=Ceramic; Holiday=Christmas; Season=Winter; Indoor/Outdoor=Indoor; Secondary color=Gold; Width=7.5; Height=7.5
**Attribute / category actions:** No change needed (category and attributes consistent with the product)

**FULL NEW DESCRIPTION (4710 characters):**

````text
RACING GREEN BAUBLE: YOUR JOCKEY SILKS IN THE MIDDLE. For silks all over, see our Premium Silks Bauble.

Size: 7.5 cm (2.95 in, just under 3 inches) across. A flat round ceramic bauble, printed on both sides, with a red ribbon to hang it.

Horse racing ornament in racing green and gold, personalised with your jockey silks: a flat round ceramic Christmas tree decoration with your jersey, sleeves and cap in the middle, your horse's, syndicate's or any name in gold and MERRY CHRISTMAS underneath.

A racehorse ornament with a classic green and gold finish, the same on both sides and printed to order in the UK. A racehorse Christmas decoration for owners, syndicates, racegoers and every horse racing fan, and a keepsake that keeps a horse's name on the tree year after year.

PERFECT FOR
- A traditional green and gold horse racing tree decoration
- Racehorse owners and syndicate members, with the horse's name in gold
- A Christmas racehorse keepsake for a racegoer, a breeder or a stable
- Matching a whole tree of baubles, one for each horse

HOW TO ORDER
1. Design your bauble first at www.zanshorseracing.co.uk/bauble-designer
Choose Racing green bauble, pick your jersey pattern, two colours, sleeves and cap colour, and type the name. You can hang it on our Christmas tree on screen to see how it looks.
2. Tap "Copy design code". Your code starts with ZBB.
3. Come back to this listing, paste the code in the design code box, type the name in the name box and add it to your basket.
Code starts ZBA? That's our Silks bauble, so please order it from that listing instead.
No time for the designer? Write your jersey pattern, two colours, sleeves and cap colour in the design code box instead (the name still goes in the name box), and we'll make it up and send you a picture to check before it's printed.

CAN'T FIND YOUR SILKS?
Message us on Etsy with the name and a photo or description of the silks. We'll draw them for you free of charge and send you a preview to check before you order.

WHAT YOU CAN CHOOSE
- Jersey pattern (25 to choose from, the same as our silks mugs): plain, hoops, stripes, spots, stars, diamonds, chevrons, check, diagonal stripes, large spots, quartered, broad hoop, broad stripes, halves, seams, braces, sash, cross belts, large diamonds, triple diamonds, big stars, big discs, three big spots, crosses or broad chevrons
- Sleeves (14 choices): plain in your main colour (shown as "Same as jersey"), plain in your second colour, hoops, stripes, armlets, spots, stars, chevrons, diamonds, check, diagonal stripes, cuffs, armlet and cuffs or large spots
- Two colours from 18 racing colours, or any other shade you like
- Cap colour: the jockey cap is one colour of your choice, with a darker peak and gold edging
- Name: up to 28 characters including spaces, using letters (accents such as é and ó are fine), numbers and - ' & . #, printed in gold capital letters. Longer names are printed smaller or on two lines.

THE BAUBLE
- Flat round ceramic bauble, about 7.5 cm (2.95 in) across
- Racing green and gold, your jersey and cap in the middle, the name in gold, MERRY CHRISTMAS in small gold capitals underneath and a small ZANS Racing Tools logo at the bottom
- The same design printed on both sides by dye-sublimation
- Small hole near the top for the red hanging ribbon (ribbon included)
- Printed for you by our print partner in the UK
- The gold is a printed colour, not metallic foil

MAKE IT A SET
Our personalised jockey silks mugs come in the same 25 silks patterns and 18 racing colours, so you can make a matching mug. You'll find them in our shop.

GOOD TO KNOW
- Made to order: please allow up to 10 working days for us to make and send it, plus delivery time. Order early for Christmas.
- We check every design before it's printed and will message you if anything is unclear
- Any name you like, up to 28 characters; we won't print rude or offensive words
- Printed colours can look slightly different from your screen
- A decoration, not a toy: ceramic can break if dropped
- ZANS is independent and not connected with or approved by any racecourse, owner, jockey or trainer
- Gift box and tissue are not included: they are shown in some photos for display only
- The baubles in our photos are previews of real ZANS designs. The scene photos (trees, rooms and racecourses) were made with AI image tools to show the bauble in use. All names shown are examples.

RETURNS
Personalised items are made just for you, so we can't accept change-of-mind returns. If your bauble arrives damaged, misprinted or not as described, message us with a photo and we'll replace it or refund you. This doesn't affect your statutory rights.

Wishing you a Merry Christmas
````

### 24. 4612435420 - Mug - Horse Racing Christmas Gift, Personalised White Silks Mug 11oz with Racehorse Name, Jockey Colours
https://www.etsy.com/listing/4612435420  | £11.99 | 7 views lifetime | 0 favourites | section: Horse Racing Gifts

**BEFORE title (98):** Horse Racing Christmas Gift, Personalised White Silks Mug 11oz with Racehorse Name, Jockey Colours
**AFTER title (98):** Horse Racing Christmas Gift, Personalised White Silks Mug 11oz with Racehorse Name, Jockey Colours  _(unchanged)_

**BEFORE tags:** white silks mug | personalised mug | horse name mug | horse racing mug | racehorse name mug | racing colours mug | owner silks mug | racehorse xmas gift | horse racing gift | silks coffee mug | racing gift for dad | jockey colour mug | horse racing cup
**AFTER tags (13):** white silks mug | personalised mug | horse name mug | horse racing mug | racehorse name mug | racing colours mug | owner silks mug | racehorse xmas gift | horse racing gift | silks coffee mug | racing gift for dad | racing club gift | trainer gift mug
Tags kept 11, new 2.

**Primary keyword:** white silks mug
**Secondary keywords:** personalised horse racing mug, horse name mug, racing colours mug, owner silks mug
**Extra phrases covered:** racing gift for dad, racing club gift, trainer gift mug, silks coffee mug
**Audience and why:** Buyers who want the simpler all-white mug and the lower price; also owners, syndicates, racing clubs and trainers' yards as gift givers.
**Note:** Title and description unchanged. 2 tag swaps: cup/colour phrases had no search evidence.

**Category:** Home & Living > Kitchen & Dining > Drink & Barware > Drinkware > Mugs (section: Horse Racing Gifts).
**Attributes now:** Occasion=Birthday; Holiday=Christmas; Height=9.6; Width=8.2; Dishwasher safe=Yes; Microwave safe=Yes; Volume=330; Material multi=Ceramic; Insulated=No; Home graphic=Abstract & geometric; Handle=Yes; Primary color=White; Enamel=No
**Attribute / category actions:** Occasion=Birthday while Holiday=Christmas: leave (Etsy allows one Occasion); no change

**FULL NEW DESCRIPTION (2952 characters):**

````text
WHITE MUG: WHITE HANDLE AND WHITE INSIDE
This is our standard silks mug: a white glossy 11oz ceramic mug with a white handle and white inside, with your own silks printed all the way round. Want a coloured handle and inside? Look for our Premium Silks Mug in the shop.

Personalised horse racing silks mug: a white 11oz ceramic mug with your jockey silks printed all the way round and your horse's or syndicate's name on a name plate either side of the handle. Pick from 25 silks patterns and two colours. A Christmas or birthday gift for racehorse owners, syndicate members, racing club members, trainers' yards and racing fans.

FREE UK DELIVERY

HOW TO ORDER
1. Design your mug on our free designer at www.zanshorseracing.co.uk/mug-designer : pick a pattern and your two colours, and type the name.
2. Tap "Copy design code".
3. Paste the design code and type the name in the personalisation boxes above.
No time for the designer? Just write the pattern, your two colours and the name in the personalisation box and we'll make it and send you a picture to check before it's printed.

CAN'T FIND YOUR SILKS?
Message us on Etsy with the name and a photo or description of the silks. We'll draw them for you free of charge and send you a preview to check before you order.

WHAT YOU CAN CHOOSE
- Pattern (25 to choose from): plain, hoops, broad hoop, stripes, broad stripes, halves, seams, braces, spots, large spots, big discs, stars, big stars, diamonds, large diamonds, triple diamonds, chevrons, broad chevrons, checks, quartered, diagonal stripes, sash, cross belts, three big spots or crosses
- Two colours from 18 racing colours
- Name: up to 28 characters including spaces, printed on a name plate on each side of the handle

THE MUG
- 11oz (330 ml) white glossy ceramic mug, white handle and white inside
- Pattern printed all the way round, with a small ZANS Racing Tools mark
- Dishwasher and microwave safe
- Printed to order for you in the UK by our print partner

THE PERFECT SYNDICATE GIFT
One for every member, all in your horse's colours. Buying 5 or more mugs with the same design? Message us before ordering and we'll set up a group price.

GOOD TO KNOW
- Made to order: please allow 3-10 working days to make, plus delivery. Order early for Christmas.
- We check every design before it's printed and will message you if anything is unclear
- Any name you like, up to 28 characters; we won't print rude or offensive words
- ZANS is independent and not connected with or approved by any racecourse, owner, jockey or trainer
- The photos show example ZANS designs and names. Your mug is printed with your own silks and name, on a white mug with a white handle and white inside.

RETURNS
Personalised items are made just for you, so we can't accept change-of-mind returns. If your mug arrives damaged, misprinted or not as described, message us with a photo and we'll replace it or refund you. This doesn't affect your statutory rights.
````

### 25. 4611232428 - Bauble - Horse Racing Christmas Gift, Premium Jockey Silks Bauble with Name, Personalised Racehorse Owner Ornament
https://www.etsy.com/listing/4611232428  | £14.99 | 31 views lifetime | 1 favourites | section: Horse Racing Gifts

**BEFORE title (105):** Horse Racing Christmas Gift, Premium Jockey Silks Bauble with Name, Personalised Racehorse Owner Ornament
**AFTER title (105):** Horse Racing Christmas Gift, Premium Jockey Silks Bauble with Name, Personalised Racehorse Owner Ornament  _(unchanged)_

**BEFORE tags:** jockey silks bauble | racing silks bauble | jockey bauble | silks ornament | jockey ornament | horse racing bauble | racehorse bauble | jockey silks xmas | horse racing xmas | racehorse xmas gift | personalised bauble | horse racing gift | racehorse keepsake
**AFTER tags (13):** jockey silks bauble | racing silks bauble | syndicate gift | silks ornament | jockey ornament | horse racing bauble | racehorse bauble | jockey silks xmas | horse racing xmas | racehorse xmas gift | personalised bauble | horse racing gift | racing club gift
Tags kept 11, new 2.

**Primary keyword:** jockey silks bauble
**Secondary keywords:** racing silks bauble, silks ornament, personalised bauble, racehorse bauble
**Extra phrases covered:** syndicate gift, racing club gift, racehorse owner ornament, racing xmas
**Audience and why:** Owners and syndicates who want their own colours printed all over a Christmas bauble. Own search vocabulary (silks, syndicate, racing club) kept apart from the green bauble.
**Note:** Title and description unchanged. 2 tags swapped: jockey bauble pulled the wrong products on Etsy page 1 (earlier check), replaced with owner and syndicate gift searches.

**Category:** Home & Living > Home Decor > Seasonal Decor > Ornaments (section: Horse Racing Gifts).
**Attributes now:** Material multi=Ceramic; Holiday=Christmas; Season=Winter; Indoor/Outdoor=Indoor; Width=7.5; Height=7.5; Primary color=Red
**Attribute / category actions:** Add a Secondary colour / multicolour value only if Etsy offers it for ornaments (pattern is customer-chosen); currently Primary Red only

**FULL NEW DESCRIPTION (4342 characters):**

````text
PREMIUM SILKS BAUBLE: YOUR SILKS PRINTED ALL OVER.

Size: 7.5 cm (2.95 in, just under 3 inches) across. A flat round ceramic bauble, printed on both sides, with a red ribbon to hang it.

Personalised jockey silks Christmas bauble: a flat round ceramic horse racing ornament printed all over in your own silks pattern, with a jockey cap in your cap colour across the top and your horse's, syndicate's or any name with MERRY CHRISTMAS on a cream plate. It looks the same on both sides and is printed to order in the UK.

A racehorse owner Christmas gift, a gift for syndicate and racing club members, a horse racing Secret Santa, or a keepsake in a much-loved horse's colours.

PERFECT FOR
- Racehorse owners: your own silks on your own tree
- Syndicates: one jockey silks ornament for every member
- Racegoers and horse racing fans: a horse racing Secret Santa gift
- Remembering a retired or much-missed horse in its racing colours

HOW TO ORDER
1. Design your bauble first at www.zanshorseracing.co.uk/bauble-designer
Choose Silks bauble, pick your pattern, two colours and cap colour, and type the name. You can hang it on our Christmas tree on screen to see how it looks.
2. Tap "Copy design code". Your code starts with ZBA.
3. Come back to this listing, paste the code in the design code box, type the name in the name box and add it to your basket.
Code starts ZBB? That's our Racing green bauble, so please order it from that listing instead.
No time for the designer? Write your pattern, two colours and cap colour in the design code box instead (the name still goes in the name box), and we'll make it up and send you a picture to check before it's printed.

CAN'T FIND YOUR SILKS?
Message us on Etsy with the name and a photo or description of the silks. We'll draw them for you free of charge and send you a preview to check before you order.

WHAT YOU CAN CHOOSE
- Pattern (25 to choose from, the same as our silks mugs): plain, hoops, stripes, spots, stars, diamonds, chevrons, check, diagonal stripes, large spots, quartered, broad hoop, broad stripes, halves, seams, braces, sash, cross belts, large diamonds, triple diamonds, big stars, big discs, three big spots, crosses or broad chevrons
- Two colours from 18 racing colours, or any other shade you like
- Cap colour: the jockey cap is one colour of your choice, with a darker peak and gold edging
- Name: up to 28 characters including spaces, using letters (accents such as é and ó are fine), numbers and - ' & . #, printed in capital letters. Longer names are printed smaller or on two lines.

THE BAUBLE
- Flat round ceramic bauble, about 7.5 cm (2.95 in) across
- The same design printed on both sides by dye-sublimation
- Your silks pattern all over, a jockey cap across the top, the name and MERRY CHRISTMAS on a cream plate with a gold edge, a gold ring round the design and a small ZANS Racing Tools logo at the bottom
- Small hole near the top for the red hanging ribbon (ribbon included)
- Printed for you by our print partner in the UK
- The gold is a printed colour, not metallic foil

MAKE IT A SET
Our personalised jockey silks mugs come in the same 25 silks patterns and 18 racing colours, so you can make a matching mug. You'll find them in our shop.

GOOD TO KNOW
- Made to order: please allow up to 10 working days for us to make and send it, plus delivery time. Order early for Christmas.
- We check every design before it's printed and will message you if anything is unclear
- Any name you like, up to 28 characters; we won't print rude or offensive words
- Printed colours can look slightly different from your screen
- A decoration, not a toy: ceramic can break if dropped
- ZANS is independent and not connected with or approved by any racecourse, owner, jockey or trainer
- Gift box and tissue are not included: they are shown in some photos for display only
- The baubles in our photos are previews of real ZANS designs. The scene photos (trees, rooms and racecourses) were made with AI image tools to show the bauble in use. All names shown are examples.

RETURNS
Personalised items are made just for you, so we can't accept change-of-mind returns. If your bauble arrives damaged, misprinted or not as described, message us with a photo and we'll replace it or refund you. This doesn't affect your statutory rights.

Wishing you a Merry Christmas
````

### 26. 4609859882 - Mug - Horse Racing Christmas Gift, Premium Silks Mug, Secret Santa, Personalised Racegoer Xmas Present
https://www.etsy.com/listing/4609859882  | £14.99 | 3 views lifetime | 0 favourites | section: Horse Racing Gifts

**BEFORE title (113):** Horse Racing Christmas Gift, Premium Silks Mug, Secret Santa, Stocking Filler, Personalised Racegoer Xmas Present
**AFTER title (96):** Horse Racing Christmas Gift, Premium Silks Mug, Secret Santa, Personalised Racegoer Xmas Present

**BEFORE tags:** horse racing gift | racing secret santa | horse racing present | horse racing xmas | christmas jockey mug | racing christmas mug | racing xmas gift | racehorse owner xmas | racehorse owner gift | horse racing santa | racing silks mug | racing lover gift | jockey silks mug
**AFTER tags (13):** horse racing gift | racing secret santa | horse racing present | horse racing xmas | christmas jockey mug | racing christmas mug | racing xmas gift | racehorse owner xmas | racehorse owner gift | secret santa mug | racing silks mug | christmas gift mug | jockey silks mug
Tags kept 11, new 2.

**Primary keyword:** horse racing secret santa gift
**Secondary keywords:** racing christmas mug, christmas jockey mug, horse racing xmas, secret santa mug
**Extra phrases covered:** racing xmas gift, christmas gift mug, racehorse owner xmas, racing secret santa
**Audience and why:** Christmas buyers for a horse racing Secret Santa or Christmas present (yard, syndicate, office). Christmas vocabulary kept here so it does not compete with the general silks mug.
**Note:** Title and description unchanged. 2 tags swapped for the personalised mug search and a plain racing mug gift phrase.

**Category:** Home & Living > Kitchen & Dining > Drink & Barware > Drinkware > Mugs (section: Horse Racing Gifts).
**Attributes now:** Occasion=Birthday; Holiday=Christmas; Height=9.6; Width=8.2; Dishwasher safe=Yes; Microwave safe=Yes; Volume=330; Material multi=Ceramic; Insulated=No; Home graphic=Abstract & geometric; Primary color=White; Handle=Yes; Enamel=No
**Attribute / category actions:** Occasion=Birthday while Holiday=Christmas: leave (Etsy allows one Occasion); no change

**FULL NEW DESCRIPTION (3860 characters):**

````text
PREMIUM SILKS MUG: COLOURED HANDLE AND COLOURED INSIDE - pick from 9 colours.

Horse racing Christmas gift mug: a personalised jockey silks mug printed all the way round in your own racing colours, with a coloured handle and inside (9 colours) and your horse's, syndicate's, pet's or loved one's name on a name plate each side of the handle.

A horse racing Secret Santa, Christmas present or gift for racehorse owners, syndicate members, racegoers, dads, mums and every racing lover. Order early for Christmas.

PERFECT FOR
- Racing Secret Santa at the yard, the syndicate or the office
- A Christmas gift in your horse's colours
- A racehorse owner Xmas present that's personal to them
- A racegoer gift to use all winter long

COLOUR OPTION = HANDLE COLOUR
The colour you choose from the drop-down menu is the colour of the mug's HANDLE and INSIDE only. The outside of the mug is printed all the way round with your own silks design.

Every owner races in their own colours. Now yours go on your morning cuppa.

HOW TO ORDER
1. Design your mug on our online designer at www.zanshorseracing.co.uk/mug-designer : pick a pattern and your two colours, and type the name. The mug turns as you go, so you see exactly what you'll get.
2. Tap "Copy design code".
3. Come back to this listing, choose your handle colour in the menu above, paste the code in the design code box and type the name in the name box.
No time for the designer? Write the pattern and your two colours in the design code box instead (the name still goes in the name box), and we'll make it and send you a picture to check before it's printed.

CAN'T FIND YOUR SILKS?
Message us on Etsy with the name and a photo or description of the silks. We'll draw them for you free of charge and send you a preview to check before you order.

WHAT YOU CAN CHOOSE
- Pattern (25 to choose from): plain, hoops, broad hoop, stripes, broad stripes, halves, seams, braces, spots, large spots, big discs, stars, big stars, diamonds, large diamonds, triple diamonds, chevrons, broad chevrons, checks, quartered, diagonal stripes, sash, cross belts, three big spots or crosses
- Two colours from 18 racing colours
- Handle and inside colour: Black, Navy, Light Blue, Purple, Red, Pink, Orange, Yellow or Light Green
- Name: up to 28 characters including spaces, printed on a name plate on each side of the handle (long names go onto two lines)

THE MUG
- 11oz white glossy ceramic mug with a coloured handle and coloured inside
- Pattern printed all the way round, with a small ZANS Racing Tools mark
- The handle and inside are one solid colour (handles can't be printed)
- Printed to order for you by our print partner

MAKE IT A SET
Match it with a personalised jockey silks Christmas bauble in the same silks: you'll find them in our shop.

THE PERFECT SYNDICATE GIFT
One for every member, all in your horse's colours. Buying 5 or more mugs with the same design? Message us before ordering and we'll set up a group price.

GOOD TO KNOW
- Made to order: please allow up to 10 working days for us to make and send it, plus delivery time. Order early for Christmas.
- We check every design before it's printed and will message you if anything is unclear
- Any name you like, up to 28 characters; we won't print rude or offensive words
- ZANS is independent and not connected with or approved by any racecourse, owner, jockey or trainer
- The mugs shown on white are our print partner's previews of real ZANS designs. The Christmas scenes were made with AI image tools to show the mugs in use. All names shown are examples.

RETURNS
Personalised items are made just for you, so we can't accept change-of-mind returns. If your mug arrives damaged, misprinted or not as described, message us with a photo and we'll replace it or refund you. This doesn't affect your statutory rights.

Wishing you a Merry Christmas
````
