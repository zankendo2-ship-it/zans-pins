# Test register (issue #26)
Status: PREPARED / APPROVED (Alex) / LIVE / DONE. Nothing here is live unless it says LIVE with a time.

| ID | Test | Creative path | Destination | Owner | Status | Baseline | Readings |
|---|---|---|---|---|---|---|---|
| E1 | 21 guide titles + tags + text-led photo 1 (all changed together) | horse-racing-extraction- `claude/project-thread-bf8h9h` etsy/media/main-photos/ | 21 guide listings | upload thread | LIVE 23 Nov 19:00-19:05 UTC | guides 0 sales; Ads CTR 0.91% (24 Oct-23 Nov, all 15 ad listings) | Mon 30 Nov, Mon 7 Dec |
| E2 | Phone-crop v2 on 3 guides only (1 Beg / 1 Adv / 1 Pro) | same branch, commit e27be747f | 3 listings TBC | upload thread | PREPARED, needs Alex yes | E1 period | 7 + 14 days after go-live |
| E3 | Gift photo 1 = version C (heading + whole product + FULLY CUSTOMISED pill), old photo 1 moved to photo 2 | zans-pins `claude/project-thread-xwwh7g` visibility/review/2026-11-23/final/gifts_C/ | TEST: silks bauble 4611232428, racing green bauble 4611213915. CONTROLS: mugs 4608193933, 4609859882, 4612435420 (unchanged; mug photo 1 redo pending - REX recolour / no-hoops rebuild) | upload thread | LIVE 23 Nov ~21:28 UTC (Alex 'Yes to all' 21:17 UTC; readback by upload thread, not independent) | Per listing, 24 Oct-23 Nov: visits / views / favourites / orders / revenue for each of the 5 listings - NOT YET RECORDED (no Etsy Stats access here; asked upload thread for readback) | 30 Nov (7d), 7 Dec (14d): same fields per listing, test v control, no causal claim from 2 listings |
| T1 | Mug handle-colour demo (adapts 9 Nov 804-view video) | TBC | bio link -> website mug designer | code chat | REQUESTED | gift videos since 16 Nov median 241 | 2h/24h/48h/7d |
| T2 | Racing story with a news hook (history only, no race today) | TBC | bio link | code chat | REQUESTED | story videos since 16 Nov median 188 | same |
| T3 | Bauble transformation, different opening from T1 | TBC | bio link -> bauble designer | code chat | REQUESTED | 241 | same |
| W1 | Website: homepage Breeders' Cup section + nav links removed (11 pages); /horse-racing-gifts/ links bauble 4611232428, green bauble 4611213915, White mug 4612435420 | PR #27 into `claude/project-thread-cbdh5k` /docs | www.zanshorseracing.co.uk | visibility thread | LIVE 23 Nov 21:26 UTC (PR #27 merged; public page not independently re-tested by ChatGPT) | Website sessions 24 Oct-23 Nov + Etsy referrals from website - NOT YET RECORDED (Metricool web / Etsy traffic sources) | 30 Nov, 7 Dec: sessions, gifts-page views, Etsy visits from website |

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
