# Epsom — FLAT (turf) — ZANS method v1.0

Onboarded 2026-09-26 from the owner's two Perplexity review PDFs (`source/`). Process: methods/README.md.
Rule test: `reports/methods/epsom_FLAT_rules.md` (2019-26, 455 races) + split-period check
(2016-21 vs 2022-26, script /tmp/claude-0/sp/course_tests.py, UK/IRE history only).

## 1. Review cards (verified against the official results, reports/results_sl/)

| Card | Review | Races | Winner picks won | £1 win P/L at SP | Notes |
|---|---|---|---|---|---|
| Fri 5 Jun 2026 (Oaks day) | 003 | 8 (7 ran) | 4 (Naana's Shadow 7/2, Sallaal 5/2, Thundering On 5/1, Mister Winston 6/1) | +£14.00 on 7 | Northern Champion (17:15) is NOT in the result = non-runner (the chat wrongly said it "blundered out of the stalls"); Possessive SP 5/2 not 100/30 |
| Thu 30 Jul 2026 (evening) | 004 | 6 (5 ran) | 2 (Bobacious 4/1, Trio 9/4) | +£3.25 on 5 | Rebel Path non-runner; both odds-on/2-1 favourite picks lost |
| Mon 31 Aug 2026 | 005 | 7 | 2 (Summer Triangle 11/8, Aurora Majesty 7/2) | -£0.12 on 7 | 5 of 7 winners were excluded at "Stage 1" |
| **Total** | | **19 runners** | **8 (42%)** | **+£17.13** | RPR stream: 5 winners; longshots 0 from 7 |

## 2. Best spell and slump (owner rule: build around the peak)

- **Peak = 5 Jun (review 003)**: the core rule set HR1-HR11 + categories A-N, no weight ceilings, no hard draw
  gate, no market rule, no Stage-1 cut.
- **Slide**: 30 Jul added HR9 weight CEILINGS (1m4f <= 9-5) -> it threw out the winner Dream Harder (9-7);
  HR12 hard draw bands, HR13 market caution. 31 Aug added the Stage-1 field reduction -> 5 of 7 winners were
  cut before scoring (Proof, Hello Cotai, Seeking Charles, Tronido, Dapper Guest).
- So v1.0 = the 5 Jun rule set, keeping only the rules the data supports, and none of the later hard gates.

## 3. Rule verdicts (Epsom history, A/E = wins vs market chance, 1.00 = as priced)

| Owner rule | Test | Epsom result | Verdict |
|---|---|---|---|
| RPR anchor (exact conditions) | top RPR at trip +-1f on today's going | A/E 1.15, +13% (422) | **KEEP** (angle 1.07) |
| Top recent RPR | best of last 3 | A/E 1.05, +14% (517) | **KEEP** (1.03) |
| Cat D course form | Epsom winner at ANOTHER trip | A/E 1.50 (221); 1.34 early / 1.54 late | **KEEP** (1.12) - handles the track |
| Cat D C&D | C&D winner | 1.25 early / 0.98 late | NOTE (not stable) |
| HR3 start risk | slow away 2+ of last 4, up to 1m | A/E 0.71, -53% (160); 0.84 / 0.79 | **KEEP** (0.86) |
| HR4 hold-up | usual hold-up, 1m3f+ | A/E 0.78 (475); 0.83 / 0.75 | **KEEP** (0.89) |
| HR4 hold-up | usual hold-up, up to 1m2f | 0.89-1.07, unstable | NOTE |
| Cat B prominent | usual front-runner, 1m3f+ | A/E 1.17 (199); 1.05 / 1.22 | **SOFT** (1.05) |
| HR8 fitness | 46-99 days off | A/E 0.77 (361); 0.62 / 0.83 | **KEEP** (0.90) |
| HR11 trial trap | 100+ days, Apr/May/Oct/Nov | A/E 0.88 (187) | NOTE (in layoff angle's direction) |
| age | 6yo+ with no win/2nd in last 3 | A/E 0.85 (318) | **SOFT** (0.93) |
| HR7 finishing power | weakened/no extra 2 of last 3 | A/E 1.08 (722); 1.15 / 1.06 | **DROPPED** - these horses are UNDER-rated |
| HR5 camber (hung) | hung in last 2 | A/E 1.15 (426) | **DROPPED** |
| keen / pulled hard | keen in last 2 | <8f 1.19, 8f+ 0.96 | DROPPED (<8f) / NOTE (8f+) |
| HR9 weight | 9st7+ in handicaps | fast 0.91, good 0.98, soft 1.07 | **DROPPED** as a gate (NOTE on fast ground) |
| HR12 draw 7f-1m | low draw 1-4 | A/E 1.00 both sides | **DROPPED** |
| 5f high draw | high third, 5f | good 0.53 / soft 1.51 (tiny samples) | UNVERIFIED |
| HR13 market | non-handicap favourite | A/E 0.81 (235); 1.01 / 0.71 | NOTE - price-based, handled by the joint model + EVIDENCE AGREES |
| HR1 first-time apprentice | first-time jockey pairing | A/E 0.99 | DROPPED |
| Stage-1 cut | remove "weak form" runners before scoring | cut 5/7 winners on 31 Aug | **DROPPED** (score, never exclude) |

## 4. ZANS method v1.0 (used for Epsom picks from 27 Sep 2026)

1. ZANS joint model (evidence + price) picks the winner; BET only with EVIDENCE AGREES and confidence 8+.
2. Course angles (predict/course_method.py ANGLES["epsom","FLAT"]): exact RPR 1.07, top recent RPR 1.03,
   Epsom winner at another trip 1.12, front-runner 1m3f+ 1.05; cautions: slow starter up to 1m 0.86,
   hold-up 1m3f+ 0.89, 46-99 days off 0.90, 6yo+ out of form 0.93.
3. Cross-course: never-run-on-the-ground penalty (good 0.90 / firm 0.97) unless elite; Exact RPR column.
4. Nothing is ever excluded before scoring (the Stage-1 lesson); weights and draws are scored, not gated.

## Change log
- v1.0 (2026-09-26): built from the 5 Jun peak rule set; HR7, HR5, HR9, HR12 and Stage-1 dropped on the data.
- 2026-09-28 review of Sun 27 Sep: win picks 2/7 (Blue Noon 13/8, Matins 4/7 BET won). Fox Avatar 13th, Musical Angel 8th (exact-RPR confirmed, beaten). NO CHANGE (single card; exact RPR A/E 1.15 over 422 runners still holds).
