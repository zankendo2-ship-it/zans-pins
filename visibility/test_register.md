# Test register (issue #26)
Status: PREPARED / APPROVED (Alex) / LIVE / DONE. Nothing here is live unless it says LIVE with a time.

| ID | Test | Creative path | Destination | Owner | Status | Baseline | Readings |
|---|---|---|---|---|---|---|---|
| E1 | 21 guide titles + tags + text-led photo 1 (all changed together) | horse-racing-extraction- `claude/project-thread-bf8h9h` etsy/media/main-photos/ | 21 guide listings | upload thread | LIVE 23 Nov 19:00-19:05 UTC | guides 0 sales; Ads CTR 0.91% (24 Oct-23 Nov, all 15 ad listings) | Mon 30 Nov, Mon 7 Dec |
| E2 | Phone-crop v2 on 3 guides only (1 Beg / 1 Adv / 1 Pro) | same branch, commit e27be747f | 3 listings TBC | upload thread | PREPARED, needs Alex yes | E1 period | 7 + 14 days after go-live |
| E3 | Gift photo 1 = version C on the 2 BAUBLES | gifts_C/ | silks bauble 4611232428 (photo 8915061904), green bauble 4611213915 (8915062460) | upload thread | LIVE 23 Nov 21:23 UTC (image created_timestamp, upload-thread API readback 24 Nov 12:14; not independently verified) | Post-change anchor 23 Nov 22:52 only (not pre-treatment) | 30 Nov, 7 Dec; missing metrics = unavailable, not zero |
| E3b | Mug photo 1 = version C on 2 MUGS | gifts_C/ | Christmas silks mug 4609859882 (8965516431), white mug 4612435420 (8917742720) | upload thread | LIVE 24 Nov 09:05-09:06 UTC (Alex yes 09:02; API readback 12:14) | Anchor = 24 Nov 12:14 reading | 30 Nov, 7 Dec |
| E3c | REX silks mug 4608193933 hero replacement | gifts_C/ REX draft | 4608193933 | upload thread | APPROVED (joint PASS + Alex mugs yes 09:02), NOT LIVE - old photo 8843164847 still up at 12:14. Only photo-1-unchanged gift, not a true static control | 24 Nov 12:14 reading | when live |
| T1 | Mug handle-colour demo (adapts 9 Nov 804-view video) | TBC | bio link -> website mug designer | code chat | REQUESTED | gift videos since 16 Nov median 241 | 2h/24h/48h/7d |
| T2 | Gift review TikTok v7.2 ("Love this item for our Christmas tree" real Etsy review, snow end card) | friendly-curie batch/2026-11-24/review-tiktok/ v7-2 | TikTok 7711714549145062678, YT lCs0-ObXqJY, Pinterest 1105211564844688702 -> bio link | code chat | LIVE 24 Nov 12:30 UK (code chat readback; ChatGPT could not open URLs). Native playback, caption, bio tap, sound gate and music rights NOT yet evidenced | gift videos since 16 Nov median 241 (within 1-23 Nov baseline) | 24h/48h/7d by platform: reach, watch, completion, product clicks, orders, revenue; missing = unavailable |
| T4 | Racing story with a news hook (history only) | TBC | bio link | code chat | REQUESTED | story videos since 16 Nov median 188 | same |
| T5 | Conny story TikTok (separate creative/topic) | code chat | TikTok | code chat | BOOKED 24 Nov 18:00 UK (not the planned 18:15). Timing comparison v T2 is CONFOUNDED by creative/topic; repeat matched formats before any time-of-day claim | 188 | same |
| T3 | Bauble transformation, different opening from T1 | TBC | bio link -> bauble designer | code chat | REQUESTED | 241 | same |
| W1 | Website: homepage Breeders' Cup SECTION + top-NAV links removed (11 pages). Footer link /breeders-cup-guide/ deliberately KEPT (guide still sold); /horse-racing-gifts/ links listings 4608193933 (x2), 4611213915, 4611232428, 4612435420 + shop | PR #27 into `claude/project-thread-cbdh5k` /docs | www.zanshorseracing.co.uk | visibility thread | LIVE 23 Nov 21:26 UTC per PR merge; source verified by Claude + ChatGPT 24 Nov; live page + click-throughs NOT verified (proxy blocks both of us) - needs a native phone check. Delivery-copy fix = separate pending REVISE, needs Alex yes | Website sessions 24 Oct-23 Nov - NOT YET RECORDED | 30 Nov, 7 Dec |

TikTok rules in force (2 strikes): no race-today posts, no race times, no win/strike-rate claims near a race, no predictions or "who will win/ride" questions, commercial disclosure only on gift posts, all visuals ZANS-made or AI (no fetched or licensed race footage).


Pending copy change (joint REVISE, needs Alex yes): gifts page delivery text - remove 'order by Mon 7 Dec'; replace '£14.99 plus postage' with 'Made to order - see Etsy checkout for the current delivery estimate'; free UK/IE delivery only once checkout confirms.

E3 EARLY POST-CHANGE ANCHOR - NOT a pre-treatment baseline (snapshot 23 Nov 22:52 UTC is ~1h24m AFTER the 21:28 UTC photo change; true pre-change figures to be recovered from Etsy Stats if possible) (Etsy API readback by upload thread; API has no date-range visits/views -> views = lifetime, favourites = current, orders/items/item revenue = receipts 24 Oct-23 Nov, item price only):
| Listing | Role | Lifetime views | Favourites | Orders / items / item revenue (24 Oct-23 Nov) |
|---|---|---|---|---|
| 4611232428 silks bauble | TEST | 21 | 1 | 0 |
| 4611213915 racing green bauble | TEST | 64 | 1 | 3 / 4 / £51.96 |
| 4608193933 silks mug | control* | 57 | 0 | 1 / 1 / £0.20 (likely discounted/test order, unchecked) |
| 4609859882 Christmas silks mug | control* | 3 | 0 | 0 |
| 4612435420 white mug | control* | 6 | 0 | 0 |
Readings on 30 Nov + 7 Dec = change in lifetime views + favourites, orders since 23 Nov 21:30 UTC. True 30-day visits need Alex's Etsy Stats (phone).

*Mug controls become NON-STATIC if the REX recolour / podium deletes go live - log that change with its own time; no causal comparison of mugs v baubles. Also: green bauble 4611213915 live photos show a green/gold hooped DAD example (McManus-like) - if replaced, log a new version + time and reset that listing's baseline. Still missing: per-listing visits/clicks (Etsy Stats, Alex's phone), W1 website baseline, TikTok account status + audience active hours.

24 Nov 12:15 UTC check (visibility thread):
- W1 link check, from SOURCE only. The live site and etsy.com are both refused by this session's proxy, so I could not open either. /docs/horse-racing-gifts/index.html on claude/project-thread-cbdh5k links to listings 4608193933 (x2), 4611213915, 4611232428 and 4612435420, plus the shop ZANSRacingTools (x2). All 4 listing IDs were in the active-listings API readback of 24 Nov 08:30 UTC. The live page and a real click-through still need checking from a phone or by ChatGPT. No website sessions reading yet.
- E3 earliest reading: requested from the upload thread (Etsy API, 5 gift listings: views lifetime, favourites, orders since the 23 Nov 22:52 anchor). Still pending.
- T2 review TikTok v7.2 booked 12:30 UK 24 Nov (TikTok 440166760, YT Short 440166793, Pinterest 440166832). Audio identical to v7. Readings due at 24h, 48h and 7d.

E3 early reading at 24 Nov 12:14 UTC (Etsy API readback by the upload thread, reports/etsy/listing_baseline_2026-11-24_1215.json). Views are lifetime, favourites current, orders/revenue since 23 Nov 22:52 UTC:

| Listing | Views | Favs | Orders | Photo 1 ID (uploaded UTC) | Photos |
|---|---|---|---|---|---|
| 4611232428 silks bauble (TEST) | 22 | 1 | 0 | 8915061904 (23 Nov 21:23) | 10 |
| 4611213915 green bauble (TEST) | 66 | 1 | 0 | 8915062460 (23 Nov 21:23) | 12 |
| 4608193933 silks mug REX (control, photo 1 unchanged) | 59 | 0 | 0 | 8843164847 (23 Nov 18:39) | 20 |
| 4609859882 Christmas silks mug | 3 | 0 | 0 | 8965516431 (24 Nov 09:05, NEW C) | 17 |
| 4612435420 white mug | 7 | 0 | 0 | 8917742720 (24 Nov 09:06, NEW C) | 7 |

New step change E3b: mug photo 1 version C went live on 4609859882 and 4612435420 at 24 Nov 09:05-09:06 UTC (Alex yes 09:02). Those 2 mugs are no longer controls. REX 4608193933 is the only unchanged gift until its approved hero goes up. Revenue since the anchor is £0 on all 5. Readings only, no causal claim.

T2 LIVE 24 Nov 12:30 UK (code chat readback): review TikTok v7.2
- TikTok https://www.tiktok.com/@zansracingtools/video/7711714549145062678
- YT Short https://www.youtube.com/shorts/lCs0-ObXqJY
- Pinterest https://www.pinterest.es/pin/1105211564844688702
Readings due 25 Nov 12:30 (24h), 26 Nov 12:30 (48h), 1 Dec 12:30 (7d): views, average watch time, completion rate, likes, profile visits and link clicks where available, plus Etsy orders on the 5 gift listings. Comparison slot for the 12:30 v 18:15 test.

T2 native evidence (code chat, 24 Nov 13:11 UTC; the proxy blocks the platforms for all of us):
- Metricool getScheduledPosts 12:41 UTC: TikTok 440166760 PUBLISHED, publicUrl .../video/7711714549145062678. Caption matches the approved text. YT Short + Pinterest PUBLISHED. Native playback: UNVERIFIED (no screenshot).
- Bio-link tap by Alex: UNVERIFIED (not done as far as known).
- Music: our own script-generated celesta "Jingle Bells" (Pierpont 1857, public domain), batch/2026-11-17/music/4-celesta-jingle-bells.m4a. No library or sample, baked into the MP4, autoAddMusic false. Voice is our Gemini Aoede.
- Audio: stream md5 643523e6... identical in v7 and v7.2 (also decoded-PCM sha1 match, Claude). No one has listened to the live post; nobody has done a human listen to v7 either (ChatGPT did not listen). Sound gate: UNVERIFIED.

W1 live check: Alex reported at 24 Nov 16:07 UTC "Website all work fine" (relayed by the coordinator). The live gifts-page links are owner-verified from his phone. Per-link Etsy destinations were not individually logged.

P01 owner phone checks, 24 Nov 17:08 UTC (Alex, relayed by the coordinator):
- TikTok bio: NO LINK. TikTok needs 1,000 followers for a website link; we have 64. FAIL, and nothing can fix it yet. Rule: never say "LINK IN BIO" on TikTok; use "Search ZANS Racing on Etsy". The live T2 v7.2 video shows LINK IN BIO on screen twice (caption OK); left for Alex to decide.
- Pinterest: goes to the website. Per Metricool, today's review pin 440166832 has pinLink https://www.etsy.com/uk/listing/4611213915 (direct to Etsy). The Conny pin 1105211564844704695 and tomorrow's Jon Bon pin link to /bauble-designer/ on the website.
- Website gifts page: PASS (16:07).
- YouTube, Instagram bio, Facebook: UNVERIFIED.
Metricool 17:10: the 18:00 Conny TikTok and 25 Nov Jon Bon TikTok captions already say "Search ZANS Racing on Etsy". On-screen text being checked by the code chat.

## 24 Nov 17:20 UTC updates
- E4 (step change): ALL 21 guide listings got the v3 photo 1 (big "<COURSE> <CODE> RACECOURSE GUIDE" heading, bronze/silver/gold strip by edition, DIGITAL PDF DOWNLOAD), 16:03-16:05 UTC 24 Nov. Approval: Alex 16:00:38 UTC ("get the pdf and mugs / baulbeks all changed on Etsy thumbnails now"). The old photo 1 is now photo 2. Report: reports/etsy/main_photo_guides_v3_2026-11-24.json. The mixed v2 replacement is pending.
- P04: the £0.20 REX order = Alex's test buy on 2 Nov, EXCLUDED. The silks mug has 0 real orders 25 Oct-24 Nov.
- P01: TikTok FEATURE BLOCKED (65/1,000 followers). Scheduled TikToks are clean ("Search ZANS Racing on Etsy"). IG Reels say "Link in bio"; the IG bio link is unverified. X Conny 24 Nov 17:00 FAILED (duplicate content).
- P08: Search Console unavailable from this session; the owner step was requested. SEO source gaps are verified (home description guides only; gifts title/H1 mugs only; "7 December" + "plus postage").
- E5 (step change): layout C guide photo 1 (big centred edition badge, no DIGITAL PDF) live on all 21 guides from 18:26 UTC 24 Nov. Alex's own approval came at 18:24 ("Perfect get them all live"). It replaces E4 v3. ChatGPT's review is advice only.
- W2 (step change): website PR #28 live ~19:05 UTC 24 Nov. It adds the returns/privacy/terms/contact pages and SEO on /horse-racing-gifts/ + /gifts-for-racehorse-owners/ (mugs + baubles, bauble Etsy buttons £14.99/£12.99, Product JSON-LD). Approved by Alex. Audit run 45465993648 passed. Baseline from GSC (Alex screenshot via ChatGPT): 414 impressions / 14 clicks / 3.4% CTR over 3 months; 9 indexed, 4 not; both gift pages "Discovered, not indexed" (16 Nov).
- P01: Alex submitted a TikTok Shop UK individual seller application (under review, 24 Nov).
- W2b: Alex requested GSC indexing for /horse-racing-gifts/ + /gifts-for-racehorse-owners/ at 19:15 UTC on 24 Nov. Check index status from 1 Dec.
- OA1 (Offsite Ads baseline, owner screenshot via ChatGPT 7142622576): 26 Oct-24 Nov, 17 clicks, 3 orders, 4 units, all green and gold bauble 4611213915; £51.96 sales, £7.80 fees. Kept separate from API receipts.
- T6: Tiger Roll v3.2 booked Wed 25 Nov: TikTok 12:30 (Metricool 440820605), YT 12:30 (440820636), Pinterest 13:00 (440820663). Alex's yes 19:55 UTC 24 Nov. Gates: Red Rum cap/year + audio (code chat).

## 24 Nov 20:30 UTC sync (ChatGPT 7143441091)
- Owner steps reported done by Alex (relayed by the coordinator, 20:04): GSC indexing requested for both gift pages; website + Etsy links added to the YouTube channel and phone verification done; TikTok bio changed to "Search ZANS Racing on Etsy". No YouTube logo change.
- T6 Tiger Roll: owner approved and booked for Wed 25 Nov, but NOT release-ready. Two gates must be on file first: a dated Red Rum reference and an actual audio listen. Pull it if either fails.
- T2 readings: 24h on 25 Nov 12:30, seven-day on 1 Dec 12:30 (30 Nov = interim only).
- E5 Guide C: frozen for 7 days (to 1 Dec). Still to do: all 21 photo IDs + native crops, and a check that each listing still shows it is a digital product.
- Catalogue matrix v1: coverage PASS; diagnosis and execution REVISE. v2 due 25 Nov 10:00 UTC.
- GSC: no more indexing requests; next check 1 Dec (28-day queries and clicks).

## 25 Nov 00:08 UTC sync (ChatGPT 7147506595)
- P04 margin: the green bauble is at loss risk. Printify costs are in USD, $13.13 incl. VAT. At an illustrative $1.30 to £1: £12.99 - £4.31 Etsy fees - £10.10 = about -£1.42 on an Offsite Ads order. The earlier "push the green bauble" recommendation is WITHDRAWN. Incremental promotion is paused; the listing is unchanged.
- P04 still open: actual GBP card debit, VAT on fees, multi-item shipping, price and provider options for Alex. Reconcile the 6 digital guide orders with the earlier zero-guide baseline without overwriting it.
- P07 storyboards: #2 and #3 concept PASS; #1 REVISE (opening voice). All three need re-timing before render. No visual PASS yet.
- T6 Tiger Roll: evidence gate REVISE. Needed: Bonhams lot URL and date, the reference image, the final frame and the final audio QC record. Owner chose KEEP.
- No boxes closed.

## T2 24h reading (Metricool analytics read 25 Nov 12:50 UTC, about 24h20m after the 12:30 UK post)
| Platform | Views / impressions | Likes | Shares | Saves / clicks | Watch / completion | v baseline |
|---|---|---|---|---|---|---|
| TikTok 7711714549145062678 | 172 views | 10 | 0 | n/a | full-watch rate, avg watch, For You share, reach: UNAVAILABLE (null in Metricool) | gift median 241: **below (-29%)**. Most likes of any TikTok since 18 Nov (tied with 22 Nov 12:30) |
| YouTube Short lCs0-ObXqJY | UNAVAILABLE (Metricool returns no rows for videos published 24-25 Nov) | - | - | - | - | - |
| Pinterest 1105211564844688702 | 0 impressions | - | - | 0 saves / 0 pin clicks / 0 outbound | 0 video views | no baseline; the Conny pin 1105211564844704695 also reads 0, so this may be Pinterest data lag |
Product clicks, orders, revenue attributable to T2: UNAVAILABLE (no UTM/attribution; Etsy Stats not read). For reference, other TikToks since 16 Nov in the same Metricool read: 135 (Conny 24 Nov 18:09), 564, 236, 205, 407, 163, 686, 230, 242, 191. Story median 188 kept separate; not compared. Next readings: 48h on 26 Nov ~12:45 UTC, then 7-day on 1 Dec 12:30.

### 25 Nov 13:10 UTC sync (ChatGPT 7162868107; draft verdicts, no boxes close)
- Cufflinks/tie clips v4: concept PASS for CH cufflinks, Fact To File pair+clip, Lossiemouth pair+clip (approved pink/green kept). CH tie clip REVISE (one tiny jersey; try a bolder black band or larger motif at real 6 mm). Sources recorded, not reopened by ChatGPT; owner permission is not third-party rights clearance. Supplier REVISE: no verified SKU, UK single-order fulfilment, Etsy integration, landed cost or sample. Cufflinks first; tie clip separate; no "coming soon" until supply is confirmed.
- Cards v3: visual PASS. Set copy REVISE: US Letter folded = 5.5 x 8.5 in; duplex flip edge from the actual print test; cancellation wording conditional on express consent. No release PASS.
- Matrix: v2.1 (reconciliation: 9 = 5 BC + 1 test + 3 bauble; earlier 10/6 include the 25 Oct 11:18 Ascot order outside the API window). Five legacy "betting" slugs: ID-only links, no relist.
- T2 24h reading recorded above (c439e308); TikTok native playback, bio link and other link checks still open.

## T2 48h reading (Metricool analytics read 26 Nov 12:48 UTC, about 48h18m after the 12:30 UK post)

- TikTok 7711714549145062678: 177 views (24h: 172), 13 likes (24h: 10), 0 shares. That is -27% against the gift median of 241. It has the most likes of any TikTok since 18 Nov. Reach, full-watch rate, average watch time and traffic source: UNAVAILABLE (not returned).
- YouTube Short lCs0-ObXqJY: 34 views, the other returned fields 0. For comparison, the 24 Nov 16:03 YT video DUsgLzDe61o has 123 views.
- Pinterest 1105211564844688702: 0 across all fields. Every pin since 24 Nov reads 0, so the feed probably isn't reporting. UNAVAILABLE, not a true zero.
- Product clicks, orders and revenue attributable to T2: UNAVAILABLE (no attribution path; TikTok bio has no link).
- Other TikToks since 18 Nov in the same read: 686, 569, 560, 497, 407, 242, 238, 232, 229, 191, 164, and 139 (Conny story). The story median of 188 is kept separate.
- Growth 24h->48h: +5 views. The post has essentially stopped being distributed. Next: 7-day reading on 1 Dec 12:30.

## Sync 26 Nov 17:30 UTC (for ChatGPT 7198969070)
- Bauble v9 sample (3 ring-free baubles): the products thread reports it SUBMITTED at 16:32 UTC on Alex's own tap. Not independently verified here. The receipt is kept private, not in this public repo. Physical centring and small-logo readability: HOLD until the sample arrives.
- Mug B (bauble-style personalised mug), all 3 designs: REVISE (peak/brim gap, brim cusp, Loussiemoo dot tangencies). Draft only; nothing purchased or listed.
- Live green inset-ring design: blocked for new production pending Alex's decision.
- T2: 48h reading d47d692b; 7-day reading due 1 Dec 12:30 UK.
