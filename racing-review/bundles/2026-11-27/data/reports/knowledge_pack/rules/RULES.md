# ZANS pre-registered experiments (spec docs/ZANS_IMPLEMENTATION_SPEC.md, Part 5)

Each entry is written and committed BEFORE its test data is opened. The commit hash is the proof.

## E1 - Does a value engine exist? (Benter gain test) - registered 2026-10-22
- Data: UK/IRE history (history/*.csv.gz after the 22 Oct all-weather type fix), races 2019-01-01 -> 2026, 2+ runners,
  pre-race features from predict.features.walk (46 features), market = SP normalised within race (BSP not available:
  promo.betfair.com returns 403 to GitHub runners and this sandbox - reports/probes/data_probe5.json).
- Walk-forward by calendar year, test years 2021-2026, flat and jumps separately:
  stage 1 evidence-only logit fit on races < 1 Jan of year Y-1 minus 14 days (two-week gap), scored on year Y-1 and Y;
  stage 2 Benter blend c ~ exp(a ln p_evidence + b ln p_market) fit on year Y-1's out-of-sample p_evidence; tested on Y.
  Joint comparator: 46 features + ln p_market fit on races < Y minus 14 days.
- Metric: mean per-race log-loss of the winner; difference v market-only with a race-level bootstrap 95% CI (2,000 resamples).
- PASS: blend beats market-only (difference CI above zero) in EVERY test year for that code, and a > 0 in every year.
- FAIL: otherwise -> the features repackage the price; the product is a price-taking service and the 'value selection'
  (spec 4.3) never fires for that code.

## E1 RESULT (2026-10-22): FLAT PASS, JUMPS FAIL - reports/experiments/2026-10-22_E1_benter.md

## E2 / E3 / E5 - registered 2026-10-22, before opening (data = E1's out-of-sample probabilities, test years 2021-2026)
Market price = industry SP (BSP blocked). p_market = SP normalised within race; p_c = E1 Benter blend; p_e = evidence-only.
- E2 residual bands: r = p_c / p_market binned (<=0.9, 0.9-1.0, 1.0-1.1, 1.1-1.25, 1.25-1.5, >1.5) within market bands
  (0.30-0.45, 0.15-0.30, 0.05-0.15, <0.05); per cell n, wins, A/E v p_market +- SE, ROI at SP. Conditional logit
  win ~ ln p_market + ln r (per race): t on ln r. PASS (per code): A/E rises across r bins in the 0.05-0.30 bands, the top r
  bin's A/E lower bound > 1.00, and t >= 3.
- E3 advantage sweep: adv = p_c x SP - 1. Grid ADV_MIN {0, .03, .05, .10, .15, .20} x PRICE_CAP {none, 11.0, 7.0} x
  P_MIN {0, .05, .07, .10}; one bet per runner qualifying; per year bets, strike rate, A/E, ROI at SP. PASS: realised ROI
  rises with adv (slope of realised ROI on mean adv by adv decile between 0.7 and 1.3) AND a cell is positive at SP in
  >= 4 of the 5 years 2021-2025 (2026 reported as an extra hold-out). The chosen cell = best median-year ROI among passing cells.
- E5 data horse: races where the evidence-only top horse != SP favourite; A/E of the data horse v its own p_market +- SE,
  and A - E for those races' favourites. PASS: data-horse A/E lower bound > 1.00 (per code).

## DATA-VALIDITY AMENDMENT (2026-10-22, before any result was acted on)
302 of 72,228 test races (0.4%) have an SP book under 100% (sum 1/SP < 1.0) = runners missing from our history (incomplete
field). In them every horse looks over-priced, and they alone produced E3's apparent +40-100% flat ROI at advantage >= 0.20.
Rule: races with sum(1/SP) < 1.0 are excluded from E1-E5 and every later experiment. E1-E5 re-run under this rule; the
first (contaminated) E2/E3/E5 output is kept in git history and listed here as void.

## RESULTS 2026-10-22 (clean re-run, incomplete-field races excluded)
- E1 Benter gain: FLAT PASS (blend log-loss gain +0.0027 to +0.0034 per race, CI > 0 every year 2021-26, a 0.01-0.07);
  JUMPS FAIL (CI includes 0 in 2022 and 2026). Size: ~1/7 of Benter's published gain. reports/experiments/2026-10-22_E1_benter.md
- E2 residual bands: FLAT FAIL (t = 1.0); JUMPS FAIL on the pre-set rule (t = 4.6 and A/E rises to 1.13 at r 1.1-1.25, but the
  top r bin's lower bound is under 1 and every cell loses at SP). -> spec 4.3 'value selection' stays OFF.
- E3 advantage sweep at SP: FAIL both codes - realised ROI does not rise with advantage (slope -0.50 flat, 0.54 jumps); no cell
  positive in 4 of 5 years. No ADV_MIN can be pre-registered from SP data.
- E4: NOT RUN - Betfair promo BSP files blocked (403) from GitHub runners and this sandbox.
- E5 data horse: PASS both on the A/E rule (flat 1.039, CI 1.010-1.069; jumps 1.057, CI 1.022-1.092) BUT the favourites in the
  same races are as good or better (1.047 / 1.053): the data horse wins 17% v the favourite's 28-30%, and both lose at SP.
  reports/experiments/2026-10-22_E2_E3_E5.md

## CORRECTIONS from the second-opinion review (2026-10-22, reviewer = separate Claude project, read-only; verified here)
- E1 is RE-SCORED FAIL for BOTH codes. The blend's market weight b ~1.1 means most of the 'gain' over raw normalised SP was the
  SP's favourite-longshot bias being re-calibrated. Against a POWERED SP (market only, b fitted on the prior year), the blend's
  gain is within noise every year: flat -0.0002/+0.0002/-0.0002/+0.0001/+0.0002 (2022-26, every CI spans 0); jumps
  -0.0026 (CI below 0), +0.0006 (CI just above 0), +0.0008, +0.0003, -0.0005. Script /tmp/claude-0/e1/powered_check.py.
  -> Our features add nothing measurable over a calibrated SP. Future E1-type tests MUST use the powered-SP baseline.
- '177 v 174 expected' (7/10+ picks) used RAW 1/price (margin included) = about break-even before BOG, NOT an A/E. Against the
  margin-free 09:30 price expected ~148 (reviewer, 333 of 346 races) -> A/E ~1.2, mostly the favourite-longshot bias.
- E3 at SP is 'NOT TESTABLE' rather than 'no edge': the SP book (~1.18) leaves almost no runners with advantage > 0.
- E5's control should be other non-favourites at the same price; reviewer: jumps data horse A/E 1.07 v others 0.97-0.99.
- VERIFIED FINDING (TEST, history 2021-26, SP, /tmp/claude-0/e1/fav_quint.py): SP favourites split into fifths by
  ln(p_evidence / p_powered_SP). ROI at SP 2021-23 | 2024-26:
  FLAT Q1 -14.4 | -9.7, Q2 -12.2 | -10.3, Q3 -9.8 | -5.0, Q4 -9.6 | -3.6, Q5 -9.4 | -2.5.
  JUMPS Q1 -13.0 | -11.5, Q2 -11.3 | -7.4, Q3 -8.5 | -6.7, Q4 -8.4 | -2.7, Q5 -3.8 | -1.8.
  Leaving out the bottom 40% (Q1-Q2) is worth ~4-8 ROI points in both periods; every group still loses at SP.

## E6-LIVE - favourite filter, forward test - registered 2026-10-22, BEFORE any live day is opened
- Rule: a win pick that is the 09:30 favourite is 'FILTER-PASS' when its ln(p_evidence / p_powered_market) is NOT in the
  bottom 40% of that score (cut-offs fixed from 2021-26 SP favourites: per code, the 40th percentile in fav_quint.py).
- Judged forward from Fri 23 Oct 2026 on the locked 09:30 picks, background only (no change to the slip unless the owner
  decides): win rate, A/E v the margin-free Sky Bet 09:30 price, ROI at the Sky Bet 09:30 price, at SP and BOG, and CLV
  (Sky Bet 09:30 price / SP - 1) for FILTER-PASS v FILTER-FAIL favourites.
- PASS (to put on the slip): after 300+ FILTER-PASS bets, FILTER-PASS ROI at BOG > FILTER-FAIL ROI at BOG by 5+ points AND
  mean CLV of FILTER-PASS > 0 with t >= 2.
- Cut-offs (40th percentile of ln(p_evidence / p_powered_SP) among SP favourites 2021-26, b = 1.11 flat / 1.15 jumps):
  FLAT -0.5071, JUMPS -0.5527. Live p_evidence = the published form_chance; p_market = Sky Bet 09:30 normalised.
  Caveat: the live evidence model (fit 2019-25) is sharper than the walk-forward one, so the live FAIL share is checked weekly
  (expected ~40%); if it is far off, the cut-off is re-set from the first 2 weeks' live distribution and that change is logged.
- AMENDMENT 2026-10-22 evening (second-opinion review, made BEFORE any live E6 bet exists): the PASS rule above replaces
  "ROI at BOG by 5+ points AND CLV t >= 2" with: after 300+ FILTER-PASS bets, (1) FILTER-PASS A/E minus FILTER-FAIL A/E
  against the margin-free Sky Bet 09:30 price > 0 with z >= 2 (binomial SE per group), AND (2) FILTER-PASS ROI at the Sky Bet
  09:30 price > FILTER-FAIL ROI. Reason: at ~2.5 average odds each ROI is about +-10 points (95%) at 300 bets, so a 5-point ROI
  gap is noise; CLV (09:30 price v SP) measures WHEN the bet is struck, not the filter, so it is reported as a separate
  timing check. BOG figures are reported only, never used in the rule, until the owner confirms his Sky Bet Club
  qualification (Sky Bet BOG needs Club opt-in + £30 cash at evens+ the previous week, and does not apply to Extra Place races).
- Data rules: Sky Bet prices ONLY (a pick without a Sky Bet 09:30 price is listed separately, never scored); non-runners void.

## E12 - mid-season jumps absence (pre-registered 2026-10-23, BEFORE any fit; for the 2 Nov rebuild)
- Source: second-opinion review 23 Oct (model A/E 0.86 | 0.89 | 0.88 in 2019-22 | 2023-25 | 2026); my market-side check
  (scripts/season_check.py, margin-free SP, name-keyed): JUMPS back from 120-365 days off in Jan-Mar 0.92 (3,002) |
  0.91 (2,448) | 0.88 (674); Dec 1.05 | 0.90; Oct-Nov 1.04 | 1.04 | 1.00.
- Feature: jumps_midseason_absence = 1 when JUMPS race, month Dec-Mar, days since last run 91-365; else 0.
- Fit: walk-forward, weights fit before 2025-01-01; test 2025 and 2026 separately (flat untouched). ADOPT only if joint-model
  log-lik improves in BOTH test years AND winners of the top pick are not fewer in either year; report A/E of affected top
  picks v the margin-free SP. No live use before that test. Does not affect the slip (90+ days already off every bet).
- WATCH only (not registered as a feature): JUMPS in Oct-Nov whose last run was on the flat, market A/E 1.00 (2,417) |
  0.89 (1,460) | 0.79 (130); reviewer v model 1.02 | 0.90. Weak lately, fine in 2019-22 -> re-check monthly.
- E12 AMENDMENT 2026-10-23 (review chat, before any fit; adopt rule unchanged): the 2 Nov test also reports, as secondary
  lines only, the A/E for 91-119 days off on its own and for December on its own (the market check covered 120-365 days and
  December flipped 1.05 | 0.90), to show whether the wider band or month dilutes or drives the result.

## E13-LIVE - well-handicapped runners, forward test - registered 2026-10-23, BEFORE any live day is opened
- Source: ZANS Review team deep-research night 23 Oct; verified by scripts/well_handicapped_check.py (Kaggle full extract
  2019-26, UK/IRE, margin-free SP A/E, best RPR of the last 3 runs in the SAME code family): handicap runners at SP
  2.00-3.99 whose best3 RPR >= today's mark + 10: FLAT (incl. AW) 1.36 (553, +16.6% SP) | 1.31 (629, +12.0%); JUMPS 1.40
  (838, +20.4%) | 1.19 (469, +1.3%); every other handicap runner at 2.00-3.99 1.03-1.06, -8% to -9.4%.
  (reports/research/2026-10-23_well_handicapped_check.txt)
- Rule: python -m predict.well_handicapped --date D after the 09:30 pack -> every handicap runner (not only our picks) with
  best3 RPR (history, runs within 730 days, same code family) >= official mark + 10 and Sky Bet d0_morning price 2.00-3.99.
  £10 win at the Sky Bet 09:30 price; SP and BOG reported. Non-runners void. Background only - never on the slip or cards
  unless the owner decides.
- PASS (to put to the owner): 150+ live bets AND profit at the Sky Bet 09:30 price in BOTH halves (by date).
- Caveat: the model v10 already has mark_gap (same idea, capped) - live picks may overlap; reported separately.

## V12 - verification of the ZANS Review team's 23 Oct proposals (registered 2026-10-23 20:50 UTC, before any result was seen)
- Data: history/*.csv.gz (UK/IRE), margin-free SP A/E + £1 SP ROI, periods 2019-22 | 2023-26; scripts /tmp/claude-0/helper_item12/.
- Claims: cold yard 5.0+; turf 61+ days 10.0+ Oct-Nov; unique top best3-RPR favourite; Oct-Nov hurdle handicap favourites; jumps LTO
  winners raised 0-4 lb; flat favourites 1.5-3.0 the week after Champions Day; jumps favourites 90+ days off (v under 90).
- A claim HOLDS only if it points the same way in both periods. Holding is NOT enough for the slip: a slip-rule proposal also
  needs the live locked picks (26 Sep onwards) not to contradict it, and the owner decides.

- E13 NOTE (2026-10-23 21:30 UTC, registration unchanged): the history check behind E13 set the 2.00-3.99 band on the SP and scored at
  that SP (look-ahead) - its ROI is an upper bound and must never be quoted as expected profit. With the Betfair BSP files: re-test
  with the band on MORNINGWAP, scored at BSP.
