# More winners — deep research run (7 Oct 2026)

Owner's brief: "use all the data, track DNA, knowledge, historic data ... to really get more winners", one deep
(ultrathink) research run whose tested rules then run every day at normal effort.

Data used:
- **Live:** 522 races we picked from 24 Sep to 6 Oct (446 with a locked race-day pick), each runner with its prices at
  every check, the frozen pre-race evidence (draw, pace, weight, coverage, trainer/jockey form, course/distance/going
  record) and the result.
- **History:** 19,857 UK/IRE races from 2025-01 to 2026-09, scored by the model out of sample (weights fitted to 2024).

Rule for adopting anything: more winners in **both** halves of the live period (25-30 Sep / 1-6 Oct), or in both
2025 and 2026 on history. Everything else is rejected, with its numbers below.

## Adopted (in the code from tomorrow's pack)

| Change | Evidence |
|---|---|
| **Drift switch** (adopted this morning): top pick drifted 15%+ from the day-before price to race morning -> next of our top 3 that has not drifted | Live: drifted top picks won 5/58, the switch horse 15/58; 159 -> 169 winners; both halves; every threshold 1.10-1.33 |
| **Confidence calibration for chases (x0.91) and bumpers (x0.92)** | History 7/10+ picks: chases won 41.4% v 46.9% predicted (2025) and 44.4% v 47.0% (2026); NH flat 44.4% v 48.3% and 44.0% v 48.4%. Hurdles/flat/AW are accurate. Chase picks demoted from 7+ to 6 won 31% = genuine 6/10 form. Effect: fewer over-rated chase/bumper legs in the doubles/trebles/Lucky 15 |
| **Model refit on 2019-2025** (was 2019-2024) | 2026 races unseen by either: flat 1,494 v 1,490 winners of 4,381; jumps 1,042 v 1,039 of 2,977; log-likelihood better in both and for the form-only model too. Old weights kept as config/predict_weights_fit2024.json |
| **Each-way singles off the slip** (adopted this morning) | Owner's counted slips 25 Sep-6 Oct: E/W singles 8/34 -£83.75; multiples +£281.50 |
| **Blank price moves filled from the day-before price** | Bug: Brookside La (2.10 -> 2.50) got into the 7 Oct Lucky 63 because its move was blank |

## Started (better data)

- **Racing Post results 11 Jun - 31 Aug 2026 were missing** from our store. Those months only had Sporting Life
  results, which carry **no RPR and no official rating** (July: 9,871 runs, 0 RPRs). RPR is the model's strongest input,
  so any horse that ran in the summer was being judged on older ratings. Backfill started on GitHub (results.yml,
  dates 2026/06/11-2026/08/31, limit raised to 330 minutes, saves weekly). Once it lands, the model state is rebuilt.

## Tested and REJECTED (would have cost winners)

Live, 522 races, baseline = model pick + drift switch = 178 winners:

| Idea | Result |
|---|---|
| Course-method overlays v plain model | They changed only 18 picks: 5 v 5 winners - neutral, kept as they are |
| Switch to #2 when it has the top RPR | 36 switches: 13 -> 4 winners |
| Switch to the horse our evidence (no price) prefers | 54 switches: 17 -> 8 |
| Tie-breakers among close top-2 (pace map, held up / leader, top speed figure, trainer or jockey hot 14 days, ran within 21 days, course / distance / going winner, first-time headgear, won / placed last, lighter weight, shorter price, complete data) | Every one equal or worse; jockey hot 14d 5 -> 0, first-time headgear 5 -> 0, ran within 21 days 7 -> 1 |
| Avoid a top pick that is a data gap / off 90+ days / pace AGAINST / trainer cold | No gain (0-4 switches each, equal or worse) |
| Steam switch (to a top-3 horse backed in by a third) | 93 switches: 24 -> 13 |
| Price-move adjustment of every runner's chance (fitted k) | 181 v 178 winners, worse in the second half - no better than the drift switch |
| Pick the morning favourite instead | Our pick 178 v favourite 164; where they differ 22 v 8 - our pick is better |
| Drift switch at 5-15% in handicaps | Looked good (2 -> 9) but non-handicaps went the other way - one of ~300 combinations tried, too likely to be luck; watch only |

## Where the winners are (and are not)

| Race type (live) | Our pick won |
|---|---|
| Fields of 2-7 | 50% |
| Non-handicaps | 48% |
| Handicaps | 27% |
| Handicaps with 12+ runners | 13% (history: 23%) |

Confidence is honest: 10/10 74%, 9/10 62%, 8/10 49%, 7/10 46%, 6/10 29% live (history 69 / 53 / 45 / 37 / 31%). The
cliff between 7 and 6 confirms 7/10+ as the multiples line.

**Big handicaps are the hardest races for everyone.** History: our pick 22.9%, SP favourite 24.4%, evidence 17.3%.
No feature we hold separates them better, so the honest move is not to rely on them for multiples (already the case:
7+ ratings are rare there).

## Timing (owner's decision, not changed)

Noon re-pick (later prices + confirmed non-runners) v the 09:30 lock, 10 days: **134 v 125 winners**, never fewer on any
day (+£30.96 at £1 SP). The slips themselves were mixed (3 Oct's big morning slip). Option: a short noon message with
only the picks that changed.

## History headline (2025-26, 19,857 races, at SP)

Model pick 34.4%, SP favourite 35.7%, evidence-only 27.4%. At the off the market is the best single guide; our live edge
comes from the morning, when the market has not yet caught up (live: our pick beats the morning favourite 178 v 164).

## Update 8 Oct 2026 03:20 UTC - summer data filled, model rebuilt
- Racing Post results for 11 Jun - 31 Aug 2026 are now in the results store (one week per run after two long runs hung):
  June 10,861 rows, July 11,025, August 10,328, with a Racing Post Rating on about 94% of rows (the rest are non-finishers).
- Model rebuilt on the full history (fit 2019-2025). Tested on the SAME 2026 races as the 7 Oct model (none used in fitting):
  flat 1,173 v 1,172 winners of 3,423 races; jumps 1,002 v 999 of 2,864; log-likelihood slightly better in both.
  Kept, because it is at least as good and the summer runs now carry their ratings for today's horses.
- Honest note: the gain on history is tiny (4 more winners in 6,287 races). The bigger benefit is for horses whose recent runs
  were in June-August - their form is now judged with full ratings instead of half the information.
