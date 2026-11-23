# ZANS visibility workstream (issue #26)

Ledger: https://github.com/zankendo2-ship-it/zans-pins/issues/26 . Files here are read-only evidence for ChatGPT and Claude.

## Social account inventory (from Metricool brand 7641306 "zanshorseracing", read 23 Nov 2026 20:20 UTC)
| Platform | Account (as connected in Metricool) | Public URL | Status |
|---|---|---|---|
| Website | www.zanshorseracing.co.uk | https://www.zanshorseracing.co.uk | live; source = zans-pins branch `claude/project-thread-cbdh5k` /docs (GitHub Pages) |
| Etsy | ZANSRacingTools | https://www.etsy.com/uk/shop/ZANSRacingTools | live; 21 guides + 3 mugs + 2 baubles (+ others); no API access from this thread |
| TikTok | zansracingtools | https://www.tiktok.com/@zansracingtools | active, ~2 posts/day; 2 Community-Guidelines strikes (31 Oct, 13 Nov) |
| Instagram | zanshorseracing | https://www.instagram.com/zanshorseracing | active |
| Facebook Page | page id 1334837319720038 | https://www.facebook.com/1334837319720038 | active |
| Pinterest | zanshorseracing | https://www.pinterest.com/zanshorseracing | connected but 0-2 impressions/day, no data 22 Nov |
| X | zansracing | https://x.com/zansracing | connected |
| YouTube | channel UCqwYTr5QYgwcxPIc-dbaX_Q | https://www.youtube.com/channel/UCqwYTr5QYgwcxPIc-dbaX_Q | connected (Shorts) |
| LinkedIn | personal profile connected | - | not used for ZANS posting |
| Threads / Bluesky | not connected | - | not present |

Bio link: the website (www.zanshorseracing.co.uk). Whether each bio link is a clickable profile link has NOT been verified from here (TikTok/IG pages block automated reads) - UNKNOWN.

## Data files
- `data/tiktok_posts_2026-11-01_to_23.csv` - every TikTok post 1-23 Nov from Metricool (views, likes, comments, shares, duration, type, topic label by Claude). Retention, For You share, profile visits and bio clicks came back EMPTY from Metricool for every post -> not available via this connector (NA, not zero).
- Earlier export (another chat): zans-pins branch `claude/friendly-curie-wcq9xc` `social_data/2026-11-09/`.
- Etsy readback for the 21 guides: repo **horse-racing-extraction-** (not zans-pins) branch `claude/project-thread-bf8h9h`, `reports/etsy/seo_apply_2026-11-23.json` + `main_photo_2026-11-23.json`.

## Key TikTok finding (23 Nov)
Median views by period, all post types: **1-15 Nov 682 (24 posts) v 16-23 Nov 209 (8 posts)**.
The drop hits every format alike: story videos 748 -> 188, gift videos 683 -> 241.
It came straight after the 2nd Community-Guidelines strike (13 Nov). The most likely cause is **account-level reach reduction**, not creative style alone. That's a hypothesis: Metricool gives no For You share, so it can't be confirmed from here. The only post since 16 Nov above 400 had a news hook (Ombudsman retiring, 684).
