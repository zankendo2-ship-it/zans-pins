# Haydock — Flat turf — course onboarding review + ZANS method v1.5

Source: owner's `HAYDOCK_FLAT_REVIEW.pdf` (110 pages; text in `source/`). 4 reviewed cards,
7 Aug – 5 Sep 2026, methods v1.0 → v1.4. Rule tests: `reports/methods/haydock_FLAT_rules.md`
(1,019 Haydock flat races 2019–2026). Every pick was re-checked against the official results
(`reports/methods/owner_picks_verified_2026-09-24.json`). Odds shown as decimals.

## 1. Scorecard (£1 win on every Winner Selection, SP)

| Card | Going | Method used | Races | Won | P/L | Favourites picked | RPR picks won |
|---|---|---|---|---|---|---|---|
| 7 Aug | Good | v1.0 | 6 | 1 (Ancestor 1.53) | −£4.47 | 1 | 1 |
| 8 Aug | Good (GTF places) | v1.1 | 7 | 1 (Sallaal 1.50) | −£5.50 | 5 | 2 |
| **4 Sep** | **Heavy** | **v1.2** | **7** | **3 (Zimmerman 2.63, Girl Scout 3.25, Etonnante 1.50)** | **+£0.38** | 3 | **4** |
| 5 Sep | Heavy | v1.3 | 7 run (1 NR) | 0 (four 2nds) | −£7.00 (−£5.00 with BET gate) | 4 | 1 (Persica 4.33) |
| **Total** | | | **27** | **5 (19%)** | **−£16.59 (−61%)** | 13 | **8 (30%)** |

- The chat's sums are right. One slip: Naturalia (4 Sep) finished 8th at 11.00, not "4th 13.00".
- **The RPR stream beat the Winner stream: 8 winners v 5.**

## 2. Best spell — and what was in it

- **Best card: 4 Sep under v1.2.** 3 winners from 7, and the RPR picks won 4 from 7.
- **What v1.2 had:** the exact-conditions RPR mandate (HR11/HR13), which kept the Win and RPR
  picks independent; the 7f low-draw module; and hard eliminations for heavy-ground attrition.
- **What v1.3 added (after 4 Sep), then the 0 from 7:** two experimental rules built on one
  card: (a) "upgrade 6f C&D high-draw runners on Heavy" (from Kodi Lion) and (b) "heavy-ground
  attrition can't eliminate on its own" (from Homestrait). The chat itself says rule (a) put up
  **Big Mojo** (3rd) in the Group 1 won by Almeraq. The BET gate (v1.3) saved £2 but found no winner.
- **Lesson (same as Newmarket):** the best card came from the calmer rule set, and the slump
  followed rules added after a single card. So v1.5 below is built on v1.2's core, uses the
  RPR stream more, and drops the v1.3 one-card rules.

## 3. Rules v our data (A/E: 1.00 = as priced)

| Claim / rule | Data | Verdict |
|---|---|---|
| Front-runners disadvantaged (5f "PI 1.28", uphill finish) | Correct: usual leaders A/E **0.93** (755); pace table: hold-up favoured at 5f, 6f, 7f, 1m, 1m2f, 1m4f | **KEEP** (leader x0.96) |
| 7f (6f212y) low draw strongly favoured | Correct: low third IV 1.13 (309 races), on Good 1.24 | **KEEP as a note** (model already uses draw) |
| 5f/6f high draw on Good/GTF | **Wrong on Good** (5f high IV 0.86); high draw only helps on **Soft** (5f high IV 1.36) | **CORRECT the rule: soft ground only** |
| Exact-conditions RPR mandate | At Haydock the top exact-conditions RPR is **over-bet** (A/E 0.93, −25%); top **recent** RPR is better (A/E 1.04) | **Use recent RPR, not exact-only** (exact x0.96) |
| Ground specialist | A/E 0.86 here (over-bet) | **DROP** (x0.93) |
| Improver | A/E **1.08** (1,417) | **KEEP** (x1.04) |
| Won last time | A/E 1.06, break-even | KEEP (x1.03) |
| Slow starter, up to 1m | A/E 0.84 | KEEP (x0.92) |
| Age 6+ | A/E 0.95 | SOFT (x0.97) |
| Apprentice / first-time jockey | A/E 1.02: no effect | **DROP** |
| Favourites | A/E 1.06 | Don't knock favourites out |

## 4. ZANS METHOD v1.5 — HAYDOCK — FLAT (code: predict/course_method.py)

```
WIN PICK: price-free ZANS model, then these Haydock multipliers:
  improver x1.04 | won last time x1.03 | usual front-runner x0.96 | slow starter (<=1m) x0.92
  top exact-conditions RPR x0.96 | ground specialist x0.93 | age 6+ x0.97
NOTES: 7f low draw (priced in), 5f/6f high draw on SOFT only. Front-runners struggle up the hill.
RPR PICK: highest recent RPR proven at trip/going (owner's RPR rule). Haydock evidence: the RPR
  stream out-scored the Winner stream 8 v 5 over the 4 cards.
DROPPED: v1.3 one-card rules (6f C&D high-draw upgrade on Heavy, heavy-attrition exception),
  apprentice first-time trap, "high draw on Good" sprint rule.
BET: confidence 8+ (data only). LONGSHOT: 14.0+ decimal, 6+ runners.
```

## 5. Change log
- v1.5 (2026-09-24, ZANS onboarding): built around v1.2 (best card); v1.3 one-card rules dropped;
  draw rule corrected to soft ground; RPR stream given more weight; results verified.
- 2026-09-26 (review of 25 Sep, reports/reviews/2026-09-25/haydock.md): win picks 3/7 (Condotti, Jassas BET, Glory Road), RPR 0/7, longshots 0 won / 1 placed (Brave Country 2nd at 17.00, dwelt). 4 of 7 winners were usual prominent racers, but history says prominent runners are over-bet here (A/E 0.96, 4,177) -> NO CHANGE (variance). Unlucky/ran well flagged in methods/watchlist.json.
- 2026-09-26 (cross-course lessons): + all-UK default "top recent RPR" 1.04 (A/E 1.09, 38,336); + ground rule for all courses: never run on good 0.90 / on firm 0.97 unless elite (top RPR by 5lb+). Owner flagged Mr Noble (never ran on soft): history says flat horses on soft for the first time win as often as priced (A/E 1.09, 2,711), so flat SOFT is NOT penalised - Mr Noble lost for other reasons (weakened, hung).
- 2026-09-26 (review of 26 Sep): win picks 3/7 +£3.16 (King Of Light, Kaguyahime, Mister Whippy); 6/7 winners led or raced prominently on heavy. Tested /tmp/claude-0/sp/pattern_tests.py (2016-26, split 2016-21 / 2022-26): front-runners on soft/heavy at Haydock A/E 0.80 (394; 0.83 / 0.77) - the opposite of today -> NO CHANGE (leader 0.96 caution stays; today = variance). Centigrade (exact-RPR pick) won - Exact RPR column now live.


## Extra owner cards (uploaded 28 Sep 2026, `source/HAYDOCK FLATS REVIEW 2.pdf`, earlier thread, spring 2026)
| Card | Review | Races settled | Winner picks won | £1 win P/L |
|---|---|---|---|---|
| Spring 1 | 001 | 7 | 1 (Symbol Of Majesty 1/2) | -£5.50 |
| Spring 2 | 002 | 7 | 2 (Secret Of Life 13/8 jf, Trilby 15/8 jf) | -£1.49 |
| Spring 3 | 003 | 5 (1 no bet, 1 NR) | 2 (Rosy Affair 5/2, The Bookkeeper 5/2) | +£2.00 |
| Spring 4 | 004 | 3 (1 NR, 3 abandoned) | 1 (Noble Vow 3/1f) | +£1.00 |
| **Extra total** | | **22** | **6 (27%)** | **-£3.99** |
All-time owner record now 11 winners from 49 settled races, -£20.58. The extra cards back the v1.5 verdicts (favourite-led
picks won; nothing new that passes the data) -> NO CHANGE to v1.5.

- NO CHANGE (2026-10-16 review of Fri 16 Oct, heavy ground: win picks 3/7, High Storm non-runner): Haydock FLAT v1.5 unchanged. The losers were down to a slow start (Desperate Dan), a blocked run (Resemblance), a fly-jump at the start (Asheyra) and a narrow third (City Captain), not to a rule the data contradicts. Asheyra's case was tested: fancied flat horses (top two in the betting) on heavy ground that had never run on soft or heavy did A/E 0.99 (2015-20) / 0.94 (2021-26), against 1.03 / 1.04 for those that had, which is too small for a rule. Watching.
