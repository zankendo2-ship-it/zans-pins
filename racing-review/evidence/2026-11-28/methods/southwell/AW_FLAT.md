# Southwell — All-weather (Tapeta) — course onboarding review + ZANS method v2.3

Source: owner's `SOUTHWELL AW Review.pdf` (102 pages; text in `source/`), 4 reviewed cards, methods
Update 5 v2.0 -> v2.2 "RPR Anchor Supremacy". Rule tests: `reports/methods/southwell_AW_FLAT_rules.md`
(2,811 Southwell races since 2019). Claimed winners checked against the official results.

## 1. Scorecard (£1 win on every Winner Selection)
| Card | Method | Win picks | RPR picks | Longshots |
|---|---|---|---|---|
| **16 Aug (Review 1.1)** | **v2.0** | **5/8, +£9.22** (Heretic, Palladas, Prosperity, Yordan, Massimo Blue) | 4/8 | 0/2 |
| **27 Aug (Review 1.2)** | **v2.1** | **3/7** (Mr Noble, Market Leader, Massimo Blue) | **5/7** (chat said 6/7 - Adelaide Bay did NOT win) | 0/7 |
| Review 1.3 | v2.2 | 2/7, +£9.00 (incl. 11.00 winner) | 0/8 | 0/1 (2nd at 10.00) |
| 17 Sep (Review 1.4) | v2.2 post-40 | 3/8 named (paper - NO BET day) | 2/3 verified | - |

## 2. Best spell and what was in it
Best spell = **16-27 Aug under v2.0-v2.1: 8/15 winners, RPR picks 9/15**. Active then: the five hard rules
(trip proof +-2f, vet flags, apprentice first-time, weight burden, seasonal returner) + Exact-Conditions RPR
Anchor + C&D + improver score + Tapeta pace/draw. v2.2 ("Anchor Supremacy") made the anchor dominant and the
RPR stream then went 0/8 - so v2.3 keeps the v2.0-2.1 balance (anchor strong, not absolute).

## 3. Rules v our data (A/E, 1.00 = as priced)
| Rule | Data | Verdict |
|---|---|---|
| Exact-conditions RPR Anchor | A/E 1.09 (2,948) | KEEP (x1.05) |
| Top recent RPR | 1.06 (3,285) | KEEP (x1.03) |
| Ground/surface specialist (1-2 in field) | **1.20, +4% (779)** | KEEP (x1.10) |
| Lone front-runner | 1.12 (993) | KEEP (x1.06) |
| Stamina-loop fade of front-runners | usual leaders 0.96 (2,014) | SOFT (x0.98) |
| Slow starters at 5-6f | 0.89 (807) | KEEP (x0.94) |
| C&D winners | 1.00 (5,592) | NOTE only (priced correctly) |
| HR1 trip proof | unproven 0.97 (1,245) | NOTE |
| HR5 age 6+ out of form | 0.93 (3,690) | SOFT (age 6+ x0.98) |
| Improver score | improver 1.05 (2,624) | NOTE (model already uses trend) |

## 4. ZANS METHOD v2.3 — SOUTHWELL — AW (code: predict/course_method.py)
WIN PICK: ZANS model (evidence + price) x the multipliers above + all-course lessons.
RPR PICK: owner's exact-conditions RPR anchor. BET: confidence 8+ and our evidence agrees. LONGSHOT: 15.00+, 6+ runners.

## Change log
- v2.3 (2026-09-26, ZANS onboarding): scorecard verified; best spell v2.0-2.1; rules tested; built around the peak.
- 2026-09-26 (review of 26 Sep, v2.4): win picks 2/9 (Elyam, Pyramid), 5/9 winners held up. Tested /tmp/claude-0/sp/pattern_tests.py (2016-26, split 2016-21 / 2022-26): held-up types A/E 1.01 (7,929) = today was variance -> NO CHANGE for hold-ups. Front-runners A/E 0.93 (2,239; 0.95 / 0.92) -> leader 0.98 -> 0.96. Early Bird pick New Image (21.00) WON. Canons House, Madjid, R P McMurphy (hampered/dwelt) watchlisted.
- 2026-10-03: owner's SOUTHWELL AW REVIEWS 2 (Reviews 31-37, Apr-Jun 2026: +£1.68, +£4.75 on 7 May = best card, -£0.57,
  +£2.93) - NO CHANGE: re-test confirms the rules (top RPR 1.06 both periods, lone leader 1.12 (1.18 / 1.09), usual
  front-runner 0.96, age 6+ 0.96). Exact RPR 1.09 overall but 1.01 since 2022 - kept at x1.05, watch.
- NO CHANGE (2026-10-03 review of Sat 3 Oct: win picks 5/8): Five winners from eight with the current method, and the losers were beaten by normal race variance or a drifting nursery pick. The usual front-runner caution (x0.96) fits South Parade fading, and the exact-RPR and ground-specialist factors still hold on history, so nothing is changed. Evidence: Southwell AW from 2019: top exact-conditions RPR A/E 1.09 (2,948; 1.25 / 1.01); top recent RPR 1.06 (3,285; 1.08 / 1.05); ground exclusivity 1.20 (779; 1.23 / 1.18); usual front-runner 0.96 (0.92 since 2022).

- NO CHANGE (2026-10-06 review of Tue 6 Oct): 2/7 + 1 non-runner (Encore): Engraved and Popular Dream won, Jahami beaten a short head. Zafaan pulled hard, Affettuoso hung badly left, Insuspense missed the break - horse problems on the day, not rules the history contradicts.

- NO CHANGE (2026-10-08 review of Thu 8 Oct): Today 1/9 won, 3 placed within 2 lengths. Top-RPR picks 0/4 today; Southwell history top-RPR A/E 1.06 (3,285 runners). One winner from nine is a bad night, but three of the beaten picks were placed within two lengths, two lost through a bad start or trouble in running, and two had drifting or handicap-debut warnings already on the card. Over 3,285 runs the top-RPR rule still shows A/E 1.06, so one card is not a reason to change it.

- 2026-10-10 (owner: "Absolutely shit at Southwell!!! This must improve"): BET SLIP RULE - Southwell all-weather HANDICAP picks are
  kept off every bet (still picked on the card, with a CAUTION note). Live locked picks 26 Sep-10 Oct: handicaps 7/31 (-£102.50 at
  £10, 09:30 price) v non-handicaps 4/10 (-£0.80). History out of sample: 632 handicaps won 28.5% v 30.5% predicted, -18% at SP v
  -6% at other AW tracks (2025 -21% v -5%; 2026 -13% v -9%), class 6 -20% v -2%. Our pick was the 09:30 favourite in 40 of 44
  Southwell races - the method overlays changed only 1 pick, so the weakness is in the races, not in a method rule. NO ANGLE CHANGE.
  Final count after the 10 Oct 20:30 (Domination won at 3.50): Southwell AW handicaps 8/32, -£77.50 at £10 (09:30 price).

- NO CHANGE (2026-10-15 review): win picks 5/9; AW handicap picks 3/7 today (course slip rule stays: 632 history races -18% at SP); Mrs Blue (AW debut nursery) the one method error, already flagged pre-race.

- NO CHANGE (2026-10-17 review of Sat 17 Oct): No change to Southwell AW v2.3; the Southwell AW handicap slip rule stays. Four winners from nine with three more beaten by a short head is a strong card for the picks. The handicap/non-handicap split today (2/7 against 2/2) matches the history behind keeping Southwell AW handicaps off the slip, so the rule stays and the tally keeps counting. Evidence: Southwell AW handicaps history 632 races -18% at SP; today handicap picks 2/7 (The Third Star, Thankfully), non-handicaps 2/2 (Fully Stocked, Oxbridge); three seconds by 0.3 lengths or less.

- 2026-10-19 review: NO CHANGE. No change to Southwell AW v2.3. The Southwell AW handicap slip rule stays until the owner decides on the re-test below. No AW-debut caution is added. Why: Three of the four beaten picks were making their all-weather debut, but a TEST on history does not support a rule that holds in both periods. Southwell favourites on AW debut had A/E 0.71 (44 races) in 2019-21 but 1.03 (207) in 2022-26, the Tapeta years. Fancied AW-debut nursery runners at all AW courses had A/E 1.12 (232) then 0.90 (401). Both results flip between the periods, so neither passes the both-periods test.

- 2026-10-22 review: NO CHANGE. Six of the eight beaten picks were placed and four were beaten by about a length or less, including one hampered, so this was a bad night in the results, not a rule the history contradicts. The handicap-only collapse (0 from 7) is already covered by the slip rule. A TEST of Southwell handicap favourites shows them priced about right in both periods, so there is no reason to change the overlays. The more likely weak point today is data: incomplete all-weather form in the 09:30 state, now fixed. Evidence: TEST, data/results_full 2019 to 21 May 2026, Southwell all-weather, A/E = winners / margin-free SP chance (scratch hcap_test.py). Handicap SP favourites: 224/708, A/E 1.07 (2019-21) and 456/1,615, A/E 1.02 (2022-26). 2nd-3rd in the betting: 1.01 and 0.99. Non-handicap favourites: 1.05 and 1.12. Handicap 10.0+ shots: 0.74 and 0.89. Apprentice handicap favourites: 1.25 (20) and 0.61 (56), which flips between periods and is too small for a rule. Live first locked d0 pack, £10 at listed price (scratch tally.py): handicap picks 26 Sep-22 Oct 20/69, -£41.10; since 13 Oct 11/32, +£58.90; today 0/7, -£70.00; non-handicaps 11/21, +£20.80.

- 2026-10-24 review: NO CHANGE. Flick Of An Eye lost through a slow start that had happened once before, so I tested whether one slow start last time should already count. Across all UK/IRE all-weather sprints it does not: A/E is about 0.97-0.98 in both periods, and favourites are 0.95 and 0.99. At Southwell, lightly raced 2yos that were slow last time won only 4 from 113 (A/E 0.41). The same group flips nationally (0.78 then 1.03), and the Tapeta-era Southwell sample is 87 runs with 4 winners against about 7.5 expected, so it is too small for a rule. The draw was not a cause, and the other beaten picks were placed or low-confidence handicappers. The one real fault today is data: a reused horse name. That needs a data fix, not a method change. Evidence: TEST /tmp/claude-0/review24/southwell_slowstart_check.py (output .txt next to it). UK/IRE all-weather flat 5-6f, history to 2026-10-23, A/E = winners / margin-free SP chance, 2019-21 | 2022-26 (Southwell was Fibresand until Dec 2021, Tapeta after). ALL AW: slow start last time, only one in the last 4: 376/3,830, A/E 0.98 (0.97 | 0.98). Slow 2+ of the last 4: 0.98 (1.02 | 0.95). Favourite slow last time, only once: 124/405, A/E 0.97 (0.95 | 0.99). Favourite with no slow start: 1.05 (1.07 | 1.03). 2yo with 3 or fewer runs, slow last time: 78/932, A/E 0.93 (0.78 | 1.03). SOUTHWELL: slow last time, only once: 63/635, A/E 0.97 (1.19 | 0.84). 2yo with 3 or fewer runs, slow last time: 4/113, A/E 0.41 (0/26 | 4/87 0.53). Favourite slow last time: 20/71, A/E 0.87 (0.98 | 0.81). Draw (reports/track_stats/draw_field_bias.csv, Southwell 6f, 6-9 runners): low 1.05, middle 0.95, high 0.99 = no bias. Live tally /tmp/claude-0/review24/southwell_tally.py, Southwell ALL-WEATHER only, first locked d0 pack, £10 at the listed price: handicaps 26 Sep-24 Oct 19/65 +£7.60; AW days 15-24 Oct 11/33 +£85.10; non-handicaps 10/21 +£11.50; 7/10+ 11/23 +£0.20; today handicaps 2/6 +£40.00, non-handicaps 1/3 -£9.00.

## 26 Oct - review of Mon 26 Oct
- 0 of 9 won (five 2nds, four beaten 1L or less). Handicap slip rule kept 7 losers off. No change.
- 2026-10-31 review: NO CHANGE - FOG abandoned the meeting before race 4 (17:40-20:30 void); 1 of 3 that ran won (Oppenheimer); National Honour 10/10 BET 4th, bumped by two claimers (stewards' cautions). Back within 3 days 1.19 | 0.80 flips.

- 2026-11-05 review: NO CHANGE. 4 of 9 won (Fenaroli, Lady Mariko, Celestial Fire, That's Random); handicap course rule kept 7 picks off (2 won, -£3.70 at £10 Sky). TEST 2019-21 | 2022-26: led last Southwell run 1.10 (270) | 1.04 (755) not significant; age 6+ 0.94 (600) | 0.97 (1,418) confirms the x0.98 caution; held up last time 5-6f under 5.0 1.28 (42) | 0.96 (151) flips.

- 2026-11-07 review: NO CHANGE. Win picks 4/9. I TESTed three ideas the races suggested, on margin-free SP A/E, 2019-21 | 2022-26. (1) Our handicap favourites were beaten: SP favourites in Southwell AW handicaps are 1.01 (662 races) | 1.05 (1,630), and under 3.0 they are 1.07 (311) | 1.08 (671). So the handicap weakness is our pick, not the favourite. Non-handicap favourites are 1.14 (132) | 1.10 (414), which matches today's 3 from 3. (2) Course winners (Blackjack 3/24, Leading Times 2/2): 2+ earlier Southwell AW wins are 0.90 (403) | 0.98 (1,007), and 1 win is 1.11 | 1.03, so there is no course-winner boost. (3) High draw in 5f with 10+ runners: 0.89 (60 races) | 1.09 (134). It flips. Nothing holds in both periods.
- 2026-11-17 review: NO CHANGE (v2.3). 1 of 9 won (Hayate, on the slip double). Handicap picks 0/7, all off the slip by the Southwell AW handicap rule. TEST, Tapeta unique SP favourites, Dec 2021-23 | 2024-26: handicaps A/E 1.09 (570) | 1.05 (1,087); non-handicaps 1.11 (125) | 1.09 (312) - supports keeping the slip rule, no method rule.

- 27 Nov 2026 review: NO CHANGE (see reports/reviews/2026-11-27/southwell_learning.json).
