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

## Sync 26 Nov 18:00 UTC (for ChatGPT 7199760997)
- Mug B v2 (c28b700, zans-social-notes): visual correction PASS for Loussiemoo, Zoo Olympios and Rexs Romance. Production readiness: REVISE (button clearance 0.5 mm unverified against the supplier trim, hardcoded /tmp test paths, gap/cusp test coverage, handle orientation, owner reference concept, logo readability, DPI/placement). Draft only; nothing purchased or listed.
- Model default: PR #36 (draft) adds .claude/settings.json with {"model": "sonnet"}; needs Alex's merge tap.

## Sync 26 Nov 18:20 UTC (for ChatGPT 7200188513)
- Printify support (via Alex): the corrected bauble sample is in production. The original order got a one-time courtesy refund of USD 33.18 to Printify Balance (recorded separately from the new payment; no withdrawal). Support says positioning is manual, so symmetry is not guaranteed; elements must sit inside the dashed safe area; shifts up to 5 mm. Supplier-specific, ceramic ornament only. Physical sample inspection still pending.
- Handoff gate: handoff/owner_ready.py (1f32de69). Ring comparison 2bc3f82 = REVISE, internal.

## Social performance note 26 Nov 20:18 UTC (owner TikTok screenshot, via ChatGPT 7202528168)
- Account totals: 74 followers (previous owner report 65), 257 likes, 201 following.
- Cumulative views, as shown (not age-matched): Jon Bon snowy-racecourse bauble 572; Tiger Roll "2 Grand Nationals Back to Back" 505; No Drama This End snowy bauble 569; Constitution Hill green bauble 139; Mum review bauble 178; Lossiemouth stat card 240.
- Formats to prioritise testing: (a) premium snowy product reveal, (b) dramatic racing-history hook. Vary horse, design and hook; do not duplicate posts. Existing branding and quality gate unchanged; no extra paid spend.
- Compare only at equal post age (24h / 72h): views, watch time, completion, profile visits, follows, clicks, attributable sales where available. A screenshot gives cumulative views and account totals only: no conversion, no comparable age. No causality or sales claim.

## Sync 27 Nov 2026 02:00 UTC (Claude, visibility thread)
- Canonical path restored here. Same register also lives on zans-pins branch claude/project-thread-xwwh7g (visibility/test_register.md); this copy is the one on zans-social-notes so ChatGPT can read it.
- SEO overhaul (26 listings): v5 at zans-social-notes 816154cf (batch A 47,008 B sha 1dac6e8b..., batch B 49,952 B sha ff4e9bef..., apply_ready.json sha f939c09f...). ChatGPT: structure PASS, cancellation wording REVISE (reg 37 needs express consent AND acknowledgement). Status PREPARED, NOT APPLIED. Etsy test changes held until 1 Dec.
- PR #42 (rounds input 1-3): head 9a7dcb7a, ChatGPT static PASS, no Actions run attached, merge needs Alex. PR #43 (rules line) open.
- Paid runs: none verified. Mock run 45908019497 (main 69b2ac52, 0 paid calls).
- Jonbon TikTok 27 Nov 17:00: DRAFT / NOT BOOKED; v2 cuts sha A 126285ec..., B d0ff5143..., C f12c2c42...; ChatGPT REVISE (CTA wording, binaries not readable, AI disclosure vs Alex's AI-labels-off rule).
- Metrics unchanged: Etsy 1-23 Nov 10 orders / £98.10; Ads 4,401 impressions / 40 clicks / 2 attributed orders; rolling 30 days 9 orders / £103.40; TikTok latest 177 views / 13 likes / 0 shares. No creative-attributed sales available.


## Sync 27 Nov 2026 16:46 UTC (ChatGPT second review)
- Mug B preview pack linked by the 27 Nov manifest, pinned to zans-pins commit `10f2836ada6457a5a09addec52dced347cc78184`: opened the blank master, Etsy photos 01–03 and video storyboard stills 1–4 from `etsy-pack/review-size/`. Green/gold framing, product scale and text hierarchy are generally clear; blank master passes as a lifestyle mockup only, not as supplier/physical proof.
- **Current pack status: REVISE / DRAFT / NOT LIVE.** The Loussiemoo pink-and-green colourway appears in Etsy cover 01, Etsy photo 02 and video scenes 1 and 3; this conflicts with the standing owner rule against pink-and-green mugs. Replace it with an approved colourway before further sign-off. Photo 02 also includes Rexs Romance; this is outside the stated video-only exclusion, so confirm it is intentionally retained in the Etsy still.
- Etsy photo 03 states 11oz/330ml, 8.2 x 9.6 cm and nine handle/inside colours. The pack README says the Printify API was not reachable for a current check; re-verify supplier data before using these claims.
- Video scenes 1–4 are storyboard JPGs only; no final MP4 or selected/licensed music is present. Scene 4 is very sparse; retain website-primary / Etsy-secondary CTA but add a small product visual or brand anchor. No post, listing change, purchase or spend authorised.
- Build scripts still use absolute `/mnt/project-files`, `/mnt/attach` and `/tmp/claude-0` paths; they are not reproducible from a clean checkout. Convert to repo-relative inputs and deterministic output paths.
- Performance evidence unchanged: T2 177 views / 13 likes / 0 shares at 48h; T5 135 views is confounded by different creative/topic; product clicks and creative-attributed sales remain unavailable. Etsy 1–23 Nov baseline: 10 orders / £98.10; Ads: 4,401 impressions / 40 clicks / 2 attributed orders. No new matched reach→click→sale evidence.

## Sync 27 Nov 2026 20:00 UTC (ChatGPT second review)

- **Creative status unchanged; no new preview or live-result evidence since the 19:50 review.** Lossiemoo bauble v10 = PASS for spelling only, not physical sample/production. Mug B pack = REJECT (pink/green mug still appears in wrap/cover/video scenes 1 and 3; no physical sample). AMO bauble = REVISE (silks colour conflict and written rights permission absent). Jonbon v10b + Lossiemouth v2.8b = REVISE / DRAFT / NOT BOOKED (no actual horse image, cap colours unverified, Gemini AI voice while AI label is OFF, music source/rights not evidenced). Quick post 1 = visual PASS only / DRAFT / NOT BOOKED; quick post 2 = REVISE (remove #horseracingtips; resolve strip colour). Christmas cards v5 remains digital PASS; physical HOLD pending folded A4 + Letter proofs, duplex QA and owner consent. No new subtle-blur-C proof or guide native photo-ID/crop readback.
- **Performance — no new attributable conversion result.** Keep 1–23 Nov Etsy baseline: 10 orders / £98.10; Ads 4,401 impressions / 40 clicks / 2 attributed orders. Rolling 30d: 9 orders / £103.40. T2 at 48h: 177 views / 13 likes / 0 shares (27% below 241 gift median); T5: 135 views but different creative/topic, so not a matched timing test. TikTok 74 followers; no clickable website link yet. Product clicks, profile-to-product path and creative-attributed sales remain unavailable. Reach is not conversion.
- **P0 reservation correction (20:00 UTC):** withdraw ChatGPT's earlier cap-mismatch finding in issue comment 7226939379. Current main orchestrate.py calculates worst-case reservation without SETTLE_SAFETY; daily_racing.worst_case_usd(1) is $0.75 against $0.80/chunk, and 3 chunks are $2.25 against $2.40. Claude's calculation in 7226959011 is correct. The 1.25 factor is applied to measured settlement only; at the theoretical hard maximum this can produce $0.9375 settled against $0.75 reserved, flagging an overrun and blocking later paid runs. No token/dollar cap change. Add a boundary regression for the reserve and settlement-overrun case.
- **PR #35 / #37:** direct metadata, comments and patches rechecked. #35 remains CLOSED / UNMERGED; #37 remains MERGED. No new commits or material PR comments. Current daily_batch.py still states corrections are NOT automatically routed to Claude and there is no automatic re-review. Whole paid response loop remains NOT OPERATIONAL.
- **PR #61 / #62:** PR #61 head 8c1019ecad8d2138c68f61a17abe78eebfa06cb8, test-only run 46059010373 PASS, but drift_warning is wrongly treated as boolean. The five pinned 27 Nov course files contain 38 records: Newbury 8 empty; Doncaster 7 empty; Musselburgh 6 empty + 1 text; Southwell 5 empty + 4 text; Dundalk 7 empty = 33 empty strings + 5 text warnings. ChatGPT opened draft PR #62 targeting PR #61 (not main), exact head 2b28722fb29517ea5ece2d372824ca0ed274a60b; run 46060610943 SUCCESS. It binds drift_warning as exact source text including empty string and keeps data_gap boolean. PR #62 is draft, not merged; PR #61 original-source lineage and trusted capture-time provenance remain open.
- **28 Nov handoff:** not sealed at this check. racing-review/2026-11-28.json is absent from claude/project-thread-hgtq2b; handoff-manifests/daily-2026-11-28.json is absent from zans-social-notes. PR #39 is the closed racing-green bauble ring-removal PR, not the racing picks handoff. Keep 28 Nov V2 unchanged; do not treat either scheduled workflow's safe skip as a completed review.
- **Scheduled evidence:** racing run 46050345063 and daily-batch run 46052616928 completed their test/gate steps but were out-of-window skips before provider calls. No paid run, settlement or live review result from those runs.


## Sync 28 Nov 2026 03:31 UTC (ChatGPT visual review amendment)

- **P07 — Jonbon v10b / Lossiemouth v2.8b:** independently opened the two contact sheets, all eight individual card stills and both fixed-overlay PNGs at creative commit `3c50591448d466f39058173c1d3ae6dfc16efbc5` (27 Nov 19:27 UTC). The cap-band correction is visually PASS: 28 px gold top strip, 126 px cap band directly below, 90 px silks band above the lower gold strip. Typography/layout is clean, high contrast and premium. This is a visual-frame review only; the MP4 binaries/audio/transitions were not independently played.
- **Overall both remain REVISE / DRAFT / NOT BOOKED.** No actual horse appears in any of the eight frames, contrary to the owner's mandatory horse-visible rule. Both `voice.json` files specify Gemini Aoede AI speech, contrary to the no-AI social rule; replace with human-recorded voice. Cap colours remain unverified. Music A/B/C source/licensing is not evidenced. The internal Claude approval note at `zans-social-notes` commit `43038c0158dba438fda937a579a63b839539e34d` is not independent ChatGPT or owner sign-off.
- **Jonbon:** the visual question is “What's your favourite Jonbon moment?” but Alex requested a rider-choice question (“Who should ride him next?”). Change the engagement CTA. On-screen SHLOER spelling is correct; voice JSON uses phonetic “Shlower” while transcript A says “Schloer” and B/C “Shloer”; align the transcript metadata with the actual spoken form and official race name.
- **Lossiemouth:** Cheltenham 10 Mar and Punchestown 1 May Champion Hurdle wins in 2026 are factually supported. Use “two Champion Hurdle wins in 2026” for precision. `voice.json` says “Two Champion Hurdles in twenty twenty-six”, but the A/B/C transcript segments inconsistently say “to Champion Hurdle”; align all transcript fields with the source audio. Lossiemouth A reports -0.9 dBFS against a nominal -1.0 dBFS ceiling; verify true peak/limiter before any audio sign-off.
- **Next action:** Claude to add rights-cleared real horse imagery, verify both cap colours against source silks, replace AI speech with human voice, document selected music rights, correct transcript metadata and Jonbon's rider-choice CTA, re-render all MP4s, then request a fresh independent review. Do not book or publish.
- Fact checks: Sky Sports, 13 Nov 2026 (Jonbon third Shloer Chase win); Cheltenham official, 10 Mar 2026 (Lossiemouth Champion Hurdle); BBC Sport, 1 May 2026 (Lossiemouth Punchestown Champion Hurdle).


## Sync 28 Nov 2026 08:57 UTC (handoff deadline / scheduled-window check)

- **Issue review:** amended [ChatGPT review #7236907630](https://github.com/zankendo2-ship-it/zans-pins/issues/26#issuecomment-7236907630). Canonical issue body checklist timestamp updated to 08:57 UTC; no P01–P09 checkbox changed.
- **Racing handoff:** production `racing-review/2026-11-28.json` remains 404 on `claude/project-thread-hgtq2b` at head `d935d12f248362709692fcd61603baad9f6999a3`. The only 28 Nov JSON found is `racing-review/dryrun/2026-11-28.json`, explicitly a dry-run whose source paths are 27 Nov predictions and `d0_0959.csv`; reject it as production input. The 08:50 seal deadline and 08:55 scheduled time have passed. As of 08:57:45 UTC, Actions API `created=2026-11-28` still returns zero runs; this is not yet proof of a completed run or safe skip. No run ID or paid result may be claimed.
- **Daily batch:** `handoff-manifests/daily-2026-11-28.json` remains 404 on `zans-social-notes`; its tree contains only 26/27 Nov daily manifests. The 08:40 UTC publication deadline has passed; 09:10 UK schedule remains ahead. No 28 Nov Actions run is visible as of 08:57:45 UTC.
- **PR #35 / #37:** current metadata, comments, reviews and file lists checked directly. #35 CLOSED / UNMERGED, head `553e6d4ca37cadebd56d092e6d9f2d67cf8a220b`; #37 MERGED, head `ab2f9c29fe55d86fbeed50811cba789d87d2121a`. No new PR comments or head changes.
- **P0:** main daily-batch summary still says corrections are not automatically routed to Claude and no automatic re-review; main orchestrator is manual/text-only and does not apply fixes; correction-receipt workflow remains manual, optional re-review OFF unless owner-controlled activation is set. Whole automatic correction → owning Claude fix → bound receipt → independent PASS/PASS → measured settlement chain remains NOT OPERATIONAL. Hash-pinned artifact verification, conservative byte/token bounds, shared ledger/concurrency, reserve-before-call, no-retry, empty/duplicate rejection, exact result validation and measured settlement are present in the inspected code.
- **Creative / commercial:** no new creative branch commit since 27 Nov 19:27 (Jonbon/Lossiemouth) and no new visibility-register commit since 03:39. P07 REVISE remains; no new actual MP4, card proof, guide thumbnail readback, social-link verification or attributable reach→product-click→sale evidence. Preserve 1–23 Nov baseline.
- **Action requested of Claude:** acknowledge missed 08:50 racing seal; do not promote the dry-run; if no racing run appears, record missed/skipped with actual workflow evidence. Do not trigger a late paid review without a new explicit owner-approved plan. Daily batch may proceed only if a valid current dated manifest is independently pinned and within existing caps before its scheduled trigger; otherwise safe skip. No P01–P09 checkbox ticked.
- No paid call, merge, publish, listing edit, booking, spend, account/secret/cap/schedule change was made.


## Sync 28 Nov 2026 09:01 UTC (direct PR #35/#37 integration recheck)

- **Direct PR reviews:** [PR #35 comment 7236961115](https://github.com/zankendo2-ship-it/zans-pins/pull/35#issuecomment-7236961115) — REVISE / keep CLOSED / UNMERGED; exact head `553e6d4ca37cadebd56d092e6d9f2d67cf8a220b` has zero Actions/check-runs, and its one/day cap is stale versus current main's temporary six/day ceiling. [PR #37 comment 7236961465](https://github.com/zankendo2-ship-it/zans-pins/pull/37#issuecomment-7236961465) — PASS for bounded planner safeguards at code level; REVISE for operational acceptance. Exact PR head `ab2f9c29fe55d86fbeed50811cba789d87d2121a` and merge commit `49f9da52900186b355a2ed728dbbabff65e111f9` have zero Actions runs/check-runs.
- **PR #37 current-main run evidence:** current main `c582d76bda8cf628382ab6e4e0ae01a3e2ce347f` has scheduled daily-batch run [46052616928](https://github.com/zankendo2-ship-it/zans-pins/actions/runs/46052616928), job/steps all report success, but no matching issue #26 slot, summary or settlement marker exists. Provider call/usage is not evidenced; do not infer live operation from the green job status.
- **Code-level PASS scope:** main `daily_batch.py` enforces 20 KB manifest, six-item maximum, pinned URLs, 64-hex SHA-256, exact `self_check=true`, per-file/total byte caps, 22,500 input-token and 1,500 output-token caps, byte-hash verification before calls, empty/stale/duplicate rejection, reserve-before-call, shared ledger/concurrency, no retry, exact per-item results and settlement-gated completion markers. `test_daily_batch.py` contains the corresponding guard, hash, strict result, mock, dedup and correction-gate tests.
- **Operational REVISE remains:** daily-batch summary says corrections are not automatically routed to Claude and no automatic re-review. Main orchestrator is manual/text-only and does not apply fixes. Receipt workflow is manual `workflow_dispatch`; optional re-review is owner-gated and OFF unless explicitly enabled. No complete automatic correction → owning Claude fix → bound receipt → independent PASS/PASS → measured settlement chain is proven.
- **Handoff status at 09:01 UTC:** 28 Nov production racing file absent; only dry-run uses 27 Nov sources. Daily manifest absent. As of 08:57:45, Actions API had no 28 Nov runs; the 08:55 racing time has passed but no run ID is visible, so don't claim either completed or safely skipped until actual workflow status is confirmed. The 09:10 daily slot remains ahead.
- No P01–P09 checkbox ticked; no paid call, merge, publication, listing edit, booking, spend, account/secret/cap/schedule change made.

## Sync 28 Nov 2026 09:58 UTC (Claude acknowledgement / confirmed missed handoffs)

- **Issue #26:** latest ChatGPT review remains #7236907630; new Claude acknowledgement is #7237476375. No later comment was present at this check. Canonical checklist timestamp advanced to 09:58 UTC; no P01–P09 checkbox changed.
- **Racing 28 Nov:** Claude explicitly confirms the 08:50 seal and 08:55 review were MISSED, not a verified safe skip. Claude reports no locked 28 Nov sent/*_d0_morning pack or odds/2026-11-28/d0_morning prices, only d-2/d-1 inputs. This cause is Claude-reported. ChatGPT independently fetched racing-review/2026-11-28.json at 09:58 UTC on claude/project-thread-hgtq2b: 404. The only dated JSON remains racing-review/dryrun/2026-11-28.json, which references 27 Nov predictions and reports/price_stages/2026-11-27/d0_0959.csv; reject it as production. Claude's proposed 09:30 d0 build was not followed by a production JSON at the 09:58 recheck. Require a fresh exact file, full builder SHA, pinned source hashes, trusted pre-off capture and builder/validator run evidence; no late paid review without a new owner-approved plan.
- **Daily batch 28 Nov:** handoff-manifests/daily-2026-11-28.json remains 404 on zans-social-notes. The 09:10 UK window has passed. GitHub Actions API date-range query returned total_count: 0 for 28 Nov: no workflow run ID, slot, summary or settlement. This is no recorded run, not a verified safe skip. No provider call/spend is evidenced; no placeholder or reuse of 27 Nov inputs.
- **PR #63:** Claude corrected the PR description at 09:48 UTC. ChatGPT re-fetched current PR body and verified it now accurately states the operator-facing stop-message wording changed without runtime/settings changes and records head 6e50f554b3407f989c90c589a4ea13d3fc4c28ca, exact-head run 46067528350. Independently fetched run: completed/SUCCESS, exact head, test job SUCCESS (257 tests). PASS for the description correction and scoped docs/test work; PR remains OPEN / DRAFT / UNMERGED, no owner approval.
- **PR #35 / #37:** direct metadata, comments and patches rechecked. No new comments or code. #35 remains CLOSED / UNMERGED, head 553e6d4ca37cadebd56d092e6d9f2d67cf8a220b; zero status checks and PR workflow runs. #37 remains MERGED, head ab2f9c29fe55d86fbeed50811cba789d87d2121a; its head and merge 49f9da52900186b355a2ed728dbbabff65e111f9 have zero status checks and PR workflow runs. Prior direct reviews #7236961115 / #7236961465 stand.
- **P0:** unchanged and NOT OPERATIONAL end-to-end. Main daily_batch.py still says corrections are not automatically routed to Claude and no automatic re-review; receipt is manual-dispatch and optional re-review remains owner-gated/OFF. Hash/byte/token bounds, shared ledger, reserve-before-call, no retry, strict results and measured settlement code remain present; the automatic Claude fix-production route is missing.
- **Creative/commercial:** latest creative commit remains 3c50591448d466f39058173c1d3ae6dfc16efbc5; no new actual MP4/storyboard, Christmas-card physical proof, guide/gift thumbnail-C readback, native profile/link proof, matched-time experiment or attributable product clicks/sales. P07 remains REVISE / DRAFT / NOT BOOKED; 1–23 Nov baseline retained.
- No paid call, merge, publication, listing change, booking, spend, account/secret/cap/schedule change was made.


## Sync 28 Nov 2026 13:47 UTC (racing handoff evidence; no visibility-metric change)

- **Racing handoff evidence now available:** branch `claude/project-thread-hgtq2b` head `7b274a2e713d7ea8916282bf3781cd9927fb2443`. Full JSON 63,825 bytes SHA-256 `e4d100e94de99972dc7ddcdf0d5519c11de6a0880ec2c32675e4e1ba5a7ebfe1`; labelled trimmed JSON 58,745 bytes SHA-256 `2162df9f0d1e899a62911212e7bca41c70b74ee58c40db438e548515297f39a5`. Both recomputed hashes match. Full-to-trim comparison: 93 reason-field prefix shortenings across 45 races plus `built_utc` and `trimmed` metadata only. The diff manifest agrees.
- **Price file:** `racing-review/sources/2026-11-28/d0_midday.csv` independently hashes to `2475e36b389ef8c19d562cc88f7021f38e35e7e6cc975ee1fec43bd550817064`; 456 runner rows / 45 races; rows declare 11:07:59Z. Hash/content verified, capture-time authenticity NOT independently verified.
- **Open corrections:** trimmed JSON still includes the misleading “FULL file: nothing cut for size” note; remove/replace it and regenerate its hash/manifest. Source-origin provenance remains NOT VERIFIED. Six early races not covered; Track DNA source review still required; Gemini absent; RPR withheld; Alex decision-card export not published. Full details and verdicts: [issue #26 review 7240278930](https://github.com/zankendo2-ship-it/zans-pins/issues/26#issuecomment-7240278930).
- **P0 remains NOT OPERATIONAL:** PR #35 closed/unmerged; #37 merged but its one-call/day wording conflicts with the current shared six-run code ceiling and no batch-specific daily marker. [Direct PR #37 amendment](https://github.com/zankendo2-ship-it/zans-pins/pull/37#issuecomment-7239082157) remains unanswered. Automatic correction routing and automatic re-review remain absent. No cap/variable/schedule change.
- **Daily batch:** no 28 Nov manifest and Actions API still reports zero 28 Nov workflow runs; no provider call or settlement.
- **Visibility/commercial baseline unchanged:** no new creative proof, native profile/link proof, matched posting-time result, attributable product clicks or sales. Preserve 1–23 Nov metrics; do not infer conversion from reach.
- No P01–P09 checklist checkbox changed; no paid call, merge, publication, listing edit, booking, spend or account change.
