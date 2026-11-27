# ZANS Review team proposals (23 Oct) - checked on our history (TEST)

Registered first in rules/RULES.md (V12). Data: UK/IRE runners 2019-01-01 to 2026-10-22 (Kaggle results_full + our RP store),
races with a broken SP book (<1.0) or a runner without SP dropped. A/E = winners / margin-free SP chance; ROI = £1 at SP.
Scripts: /tmp/claude-0/helper_item12/{build.py, claims.py, checks.py} (outputs claims_output.txt, checks_output.txt).
Claim 4 recomputed independently from the runner table: identical.

| # | Claim | Team | 2019-22 (n / A/E / ROI) | 2023-26 | Comparison | Verdict |
|---|---|---|---|---|---|---|
| 1 | Cold yard (0 from 5+ in 14 days), SP 5.0+ | 0.87 / 0.84 | 65,450 / 0.94 / -30.7% | 65,217 / 0.95 / -27.9% | rest 0.95 / 0.95 | DOES NOT HOLD |
| 2 | Turf Oct-Nov, 10.0+, off 61+ days | 0.67 / 0.62 | 9,542 / 0.85 / -36.7% | 7,191 / 0.76 / -48.5% | off 1-60: 0.83 / 0.83 | DOES NOT HOLD (all turf) |
| 2a | same, FLAT turf only | - | 1,538 / 0.68 / -50.7% | 1,284 / 0.66 / -58.4% | 0.89 / 0.89 | same way both, ~30 winners each = TOO SMALL |
| 3 | Unique top best-3 RPR = unique SP favourite | 1.12 / 1.10 | 13,827 / 1.14 / -1.5% | 13,426 / 1.10 / -5.9% | other favs 1.04 / 1.05 | HOLDS (still loses at SP) |
| 4 | Oct-Nov hurdle handicap favourites | 1.18 / 1.21 | 1,327 / 1.17 / -1.8% | 1,172 / 1.20 / +1.9% | Dec-Sep 1.11 / 1.03 | HOLDS; unique favs 1.19 / 1.22, +1.9% / +3.7% |
| 5 | Jumps hcap LTO winners raised 0-4 lb | 0.94 / 0.98 | 2,839 / 0.94 / -26.2% | 3,277 / 0.97 / -18.9% | raised 5-9 lb 1.04 / 1.07 | HOLDS (weak) |
| 6 | Flat favs 1.50-3.00, week after Champions Day | 0.95 / 0.92 | 277 / 0.95 / -16.3% | 204 / 0.93 / -20.5% | rest Oct-Nov 1.12 / 1.04 | TOO SMALL |
| 7 | Jumps unique favs <=3.5 off 90+ days | 1.117 / 1.077 | 2,093 / 1.12 / -5.0% | 1,965 / 1.08 / -9.3% | under 90: 1.08 / 1.08 | figures reproduced, but no difference 2023-26 |

What it means: the owner's 90-day rule is neither supported nor contradicted for jumps favourites by history (no edge either
way in 2023-26). Only claim 4 made money blind at SP (+2-4%, unique favourites). Claims 3 and 4 are inputs for the 2 Nov model
rebuild / multiples ordering, to be tested against OUR MODEL (not the SP) before any slip change. Claims 1 and 2 are dropped.

## Note on E13 (well-handicapped) history figures - review chat, 23 Oct 21:25 UTC (verified: scripts/well_handicapped_check.py
selects the 2.00-3.99 band on the SP and scores ROI at that SP)
That is look-ahead: in the morning nobody knows which horses will close at 2.00-3.99, and horses backed INTO the band are in it while
drifters out of it are not. The history ROI (flat +16.6% | +12.0%, jumps +20.4% | +1.3%) is an UPPER BOUND, never an expected
profit. Only the live forward test at the Sky Bet 09:30 price (RULES.md E13-LIVE) counts. When the Betfair BSP files arrive:
re-run with the band set on MORNINGWAP and scored at BSP. (Cosmetic: the AW lines print nan - the FLAT line already includes AW.)

## Live replay of E13 on our 09:30 Sky Bet prices (TEST, 23 Oct 21:40 UTC)
Handicap runners 26 Sep-23 Oct, best RPR of last 3 same-code runs (store RPRs) >= mark + 10, Sky Bet d0_morning 2.00-3.99: 14 bets,
2 won (Solarize, Spirit Lead Me), 7 second, -£82.50 at £10. Team's own replay: 13 bets, 2 won, -£72.50. -> E13 stays background only.
Likely reasons the history looked strong: SP-chosen band (look-ahead) and Kaggle RPRs that RP later revised.
