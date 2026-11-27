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

## E14-LIVE - drifted-pick swap trial, forward test - registered 2026-10-29 18:50 UTC, BEFORE any live day is opened
- Source: owner's choice "Off the slip + trial the swap", relayed by the ZANS Review chat 29 Oct 18:35 UTC (to be confirmed
  by the owner in the main chat). Evidence re-checked here (locked packs 1-28 Oct, pick = Sky Bet 09:30 favourite, 'move'
  first price -> pack price up 10%+, £10 win at the Sky 09:30 price): 13/90 -£451 (1-14 Oct 6/41 -£209 | 15-28 Oct 7/49 -£242).
- Rule: python -m predict.drift_swap_trial --date D in the evening review, from 30 Oct for 28 race days. For every race whose
  LOCKED win pick drifted 10%+ (move field): record the kept pick, our 2nd choice ('second') and the evidence pick, each at the
  Sky Bet d0_morning price and at SP (£10 win). Separate list: picks that SHORTENED 10%+ with evidence agreeing.
  Non-runners void. Background only - never changes picks, cards or the slip.
- PASS (to put to the owner): the 2nd choice (or the evidence pick) beats the kept pick at the Sky 09:30 price in BOTH 2-week
  halves. Anything else = no swap.

## E15-LIVE - Gemini challenger, forward test - registered 2026-10-29 20:00 UTC, BEFORE any Gemini pick exists
- Source: owner 29 Oct 19:31 UTC (Review chat, relayed): "Can you use Gemini to enhance your methods and predictions?" -> a 4-week
  challenger. Repo secret GEMINI_API_KEY (never printed or written).
- Rule: scripts/gemini_challenger.py (gemini.yml, dispatched by the 09:30 routine after the pack is locked). Input = the frozen
  reports/racecards/<D>/evidence_prerace.csv fields (card, form, ratings, speed figures, draw, pace, trainer/jockey records) + the
  Sky Bet 09:30 price; NOT our picks or chances. One request per meeting; strict JSON win pick + confidence 1-10 + reason.
  Sealed in reports/challenger/<D>/gemini_picks.json (UTC time + sha256, committed); races off before the seal are excluded.
- Comparison: Gemini pick v our LOCKED win pick, same races, £10 win at the Sky 09:30 price and at SP; groups = all races and each
  side's own 7+ confidence picks; 2-week halves; judged after 4 weeks (28 race days). Background only - nothing changes unless the
  owner decides on the result. A PASS needs Gemini ahead at the Sky 09:30 price in BOTH halves.
- AMENDMENT 2026-10-29 20:15 UTC (before any live Gemini pick; owner 19:39 + 19:40 UTC, relayed by the Review chat):
  (1) input widened to EVERY frozen evidence column (ids and our pipeline status labels left out) + the course method file
  (methods/<course>/<CODE>.md, first 8,000 characters); still never our picks or chances. (2) Gemini runs BEFORE the pack (09:30
  routine, step 1) and its pick is SHOWN on every course card from Fri 30 Oct as 'Gemini pick (trial)' with confidence + reason,
  marked 'GEMINI - TRIAL, NOT ON THE SLIP'; if it has not answered when the pack is built the card says 'Gemini pick missing'.
  It stays off the slip, the customer pack and BET NOW. Comparison, settlement and the PASS rule are unchanged.
- AMENDMENT 2026-10-30 10:35 UTC (before any 30 Oct result; owner turned on the paid Gemini tier 09:26 UK and asked for "the pro
  search", relayed by the Review chat; points from the Review chat's check of the commits):
  (a) Model order: the newest Pro model the key lists first, with Google Search grounding on (GEMINI_SEARCH=1); Flash, then
  Flash-Lite only when Pro errors or times out. Each race records the model that answered and its search count; each file
  records tokens + an estimated cost.
  (b) GRADED FILE = the sealed reports/challenger/<D>/gemini_picks.json used on the cards and the Gemini bet slip, nothing else.
  Later runs (e.g. gemini_picks_v2_pro_search.json, asked 09:45 UTC 30 Oct) are background comparisons and are NEVER graded or
  swapped in afterwards - so we cannot choose the better version after the results.
  (c) A search-grounded request is never made for a race already off: every run after the first race uses --after HH:MM (races
  still to run only), and a pick whose asked_utc is after the off is void (a web search after the off can return the result).
  (d) 29 Oct stays out (test runs asked 22:16 UTC, after racing). E15 starts with Fri 30 Oct.
  (e) The Gemini bet slip (predict/gemini_slip.py) uses Gemini's OWN 1-10 confidence against our 7+ cut-off; that scale is not
  calibrated like ours, so gemini_slip_record.md also logs Gemini's strike rate by its own confidence band from day 1.

- CLOSED 2026-11-04 as STOPPED (not PASS, not FAIL): Gemini credits ran out 4 Nov 07:50 UTC and the owner stopped Gemini picks
  (voiceover only, 4 Nov). Final count, 5 race days 30 Oct-3 Nov (reports/challenger/daily_v_record.md, gemini_slip_record.md):
  win picks ZANS 67/173 v Gemini 62/173; £10 win at the Sky Bet 09:30 price ZANS -£51.40 v Gemini -£246.30; Gemini bet slip
  -£61.41 on £764.75 staked. Far short of the 28 race days the rule needed - no conclusion either way.

## DATA PICK (shown on the cards from 4 Nov) - NOT a registered experiment
- Owner 4 Nov: price-free 'Data pick' on every race, never on the slip. Tracked nightly against the win pick (winners, £10 at the
  Sky 09:30 price, SP). If it is ever to go on the slip, pre-register it here first. Prior (verified 4 Nov from
  reports/predictions/*/disagree.json, 26 Sep-3 Nov, races where the evidence-only horse differed from the win pick, £1 SP): the
  closest earlier measure (form-model top horse, no course factors) won 119/766 (15.5%, -122.36 pts) v our win pick 221/787
  (28.1%, -135.85 pts).

## E16-LIVE - PRICE MIX slip, forward test - registered 2026-11-03 16:30 UTC, BEFORE the first slip built under it (Wed 4 Nov)
- Source: owner 3 Nov (his words, relayed by the ZANS Review chat: "Having stupid low bets on our slip is pointless! We need
  structural value!", "Mixtures of high middle and low predictions", "Just do a mixture and get this working"; decision card PRICE MIX).
- Rule (predict/betslip.py PRICE_MIX_TRIAL): win singles = 7/10+ locked win picks priced 2.00+ at 09:30 passing every slip safety
  rule (betslip._gap, drift 10%+); no single under 2.00. Price mix = best value (our chance x 09:30 price) safe 5/10+ pick in each
  band <2.00 / 2.00-3.49 / 3.50+ (empty band filled by the next-best value) -> treble of all three, double of the first two.
  Lucky 15 / 63 = best-value 7/10+ 2.00+ singles. Accumulators unchanged (8/10+). Slip legs under 8/10 carry an amber
  'N/10 PRICE MIX' box, not a BET / NO BET tag.
- Look-back (TEST, chosen after seeing these days, so optimistic): locked race-day picks 26 Sep-2 Nov, £10 at the 09:30 price,
  reports/research/scripts/pricemix_2026-11-03/: singles 58/117 +£172.40 (+109.70 | +62.70); treble +£304.65 (+113.62 | +191.03);
  double +£134.80 (+69.30 | +65.50); old 8/10+ singles 68/117 +£50.40 (+69.20 | -18.80).
- Comparison: the old 8/10+ slip is built and settled every day as a background record (predict.shadow7 mode old8,
  reports/predictions/shadow_old8_record.md), plus the 7/10 shadow.
- Judge after 30 race days (to ~5 Dec): keep if the trial slip's P/L at the 09:30 price beats the old 8/10+ slip's over the
  same days AND its singles are not losing at the 09:30 price; otherwise report to the owner and propose going back.

## E17-LIVE - DATA BIG-PRICE trial - registered 2026-11-04 11:05 UTC (owner 4 Nov: "Do whatever you think is right but get us some winners")
- Source: reports/research/2026-11-04_big_price_patterns.md (TEST). History 2018-26, unique top on best-of-last-3 RPR at SP 5.00+:
  FLAT non-handicaps A/E 1.14 | 1.11 (2018-21 | 2022-26), chases up to 2m1f 1.21 | 1.21; live 26 Sep-3 Nov data-top horse at 5.00+:
  flat non-handicaps 41, 8 won, A/E 1.50, +£105; chases 49, 10 won, A/E 1.54, +£185 (£10 win at the 09:30 price). Every group still
  lost at SP in 2022-26 (-7% to -12%), so this is NOT proven profitable.
- Rule (predict/bigprice_trial.py): in every race of the LOCKED 09:30 pack, the runner with the highest evidence-only chance
  (form_chance, price ignored) qualifies when its 09:30 price (Sky Bet from d0_morning bookie_terms, else the pack's best price)
  is 5.00-10.99 AND the race is a FLAT turf non-handicap or a CHASE AND a bookmaker priced the race (no Racing Post forecast
  prices; added 11:10 UTC before any result). One per race. Races off before the trial file is written are
  excluded (4 Nov: races after 11:05 UTC only).
- Record: £10 win at the 09:30 price, at SP, and BOG (bigger of the two) - reports/predictions/bigprice_trial_record.md.
  Background only: never on the slip, customer pack or BET NOW; listed in the 09:30 message so the owner can see them.
- Judge after 100 settled bets: keep and offer for the slip only if profit at the 09:30 price is positive in BOTH halves; stop
  if it is below -15% ROI at the 09:30 price after 100 bets.
- NOT changed (same day): the strong-value rule. The narrower 'top RPR not fancied + handicap + 11.00-25.99 bookmaker price'
  rule made +£184 on 186 bets v the current rule +£804 on 322 (first bookmaker price, 24 Sep-3 Nov) -> no case to switch.

## E18-LIVE - DATA OVERRIDE watch - registered 2026-11-04 13:00 UTC (owner 4 Nov: "identify when the data pick should be our winner regardless of the price")
- Source: reports/research/2026-11-04_data_pick_when.md (TEST). Races where the Data pick differs from the win pick, win pick 5/10 or
  less, Data pick under 4.00: history Data pick won 144 v 141 (2023-24) | 155 v 150 (2025-26), ROI -5.0% v -8.9% | -4.1% v -11.5% at
  SP; live 26 Sep-3 Nov CORRECTED 4 Nov evening (the first figure '7 v 3, 19 races, +£62.50 v -£90.00' came from an unsaved script and
  could not be reproduced): evidence-pick proxy, Sky 09:30 price under 4.00 = 17 races, 5 v 3, £10 win +£10.00 v -£70.00 (best bookmaker
  price: 19 races, 6 v 2) - reports/research/scripts/datapick_2026-11-04/live_e18.py (the auditor's rebuild). Rule found by a combination
  search -> must hold live.
- Rule (predict/data_pick_tracker.is_override): LOCKED 09:30 pack; win pick confidence <= 5; Data pick a different horse; Data pick's
  Sky Bet 09:30 price (d0_morning bookie_terms) under 4.00. No Sky price = not counted.
- Record: nightly in reports/predictions/data_pick_record.md (E18 section), £10 win at the Sky 09:30 price, both horses.
- Judge after 100 races: PASS if the Data pick won at least as many races as the win pick AND made more at the 09:30 price, in BOTH
  halves -> offer the owner 'Data pick becomes the win selection in these races'. Background only until then (or the owner's yes).
- AMENDMENT 2026-11-04 21:10 UTC (before any qualifying live race - the tracker shows none yet), after the expert AUDITOR's digest
  (reports/research/experts/digest/2026-11-04.md on experts/auditor: FAIL as a pick switch - 299 v 291 over all 1,104 history races,
  p 0.39; 2024 68 v 69, 2025 71 v 71; cut-offs 3.50 / 4.50 / 6 of 10 give FEWER Data-pick winners; history chose races by SP = look-ahead;
  a 09:30-safe filter (Data chance >= 0.30) gives 167 v 209 | 152 v 154): judged ONLY on Sky Bet 09:30 prices; PASS needs 300+ races AND
  a one-sided p < 0.05 (binomial on the races where exactly one of the two horses won) AND more profit at the Sky 09:30 price. The
  '100 races, both halves' test above is withdrawn (equal horses pass it ~29% of the time by luck). Background record only.

## E19 - QUICK RETURN 7/10+ picks (last run 8-14 days ago) - registered 2026-11-05 12:45 UTC, BACKGROUND RECORD ONLY
Source: ZANS Review team deep research 5 Nov (plan item A6, colleague proposal). The slip rule is NOT switched on: per the
standing leak rule the owner decides, and long-run history does not support it.
- Live (verified here, predict/leak_finder.collect, 7/10+ locked picks 26 Sep-4 Nov, £10 at the 09:30 price): 8-14 days 17/56
  won, -£189.20 (H1 26 Sep-15 Oct 12/32 -£59.80 | H2 16 Oct-4 Nov 5/24 -£129.40); 0-7 days 21/38 +£67.50; 15-30 109/194
  +£218.00; 31-60 45/79 +£132.90. Found by scanning ~74 segments.
- History (TEST, history/*.csv.gz 2019-26, SP under 3.00, margin-free SP A/E; /tmp/claude-0/teamplan/days_hist.py):
  8-14 days 1.07 (3,610) | 1.07 (3,989) = the same as 15-30 days 1.07 | 1.07 -> the market prices quick returners correctly;
  the live gap is chance or our model over-rating them.
- Record: predict/team_trials.py -> reports/predictions/<D>/team_trials.json + team_trials_record.md (£10 at Sky 09:30, SP, BOG).
- Proposal to the owner: keep these picks off every bet for 4 weeks. STOP (rule off) if the kept-off picks win 45%+ over the
  first 30, or the kept picks' strike rate falls below the kept-off group's. Nothing changes until he says yes.

## E20 - UNDER-7 PICKS BACKED OVERNIGHT - registered 2026-11-05 12:45 UTC, BACKGROUND RECORD ONLY
Source: review team plan item A8 (team figure 97/318 +£343.80 at 09:30, both halves, found by scanning - not checked here).
- Group: win picks under 7/10 whose Sky Bet price shortened 10%+ from the night before (d-1_evening, else d-1_morning) to
  09:30 (d0_morning). Settled at £10 win at the Sky 09:30 price, SP and BOG; never a bet.
- Judge after 4 weeks (from 5 Nov): a bet only if it wins at least the market's chance AND makes money at the 09:30 price in
  both 2-week halves; then put to the owner.

## REVIEW-TEAM PLAN (5 Nov 2026) - what went live for the Fri 6 Nov pack, registered 2026-11-05 13:40 UTC
Owner 5 Nov 12:13 UTC (his words, relayed verbatim by the ZANS Review chat): "Make this happen along with all improvements that
you gave during your deep research 60+ % strike rate plan." Each item checked here first; figures from our own files.
- LIVE A1: win singles only on 7/10+ picks priced 2.00+ passing every safety rule (CONF_SINGLE_MIN_PRICE 2.0, since 5 Nov).
- LIVE A4: 5-fold OFF (betslip.BET_FIVE_FOLD False). Locked race-day slips 25 Sep-4 Nov recounted by bet type: 5-fold 4 bets, 0 won,
  -£40.00. Forecasts / each-way singles were already off. Super Heinz kept (4 bets, -£0.77). Measure: none needed (a removal).
- LIVE A8: red 'DRIFTING - NO BET' label on course cards for win picks under 7/10 whose Sky Bet price drifted 10%+ from the night
  before (d-1_evening, else d-1_morning) to 09:30. Display only - under-7 picks are never on the slip.
- LIVE A9: every WIN bet on the slip (singles, double, treble, Lucky 15/63, Super Heinz) says '09:30 price, claim Best Odds
  Guaranteed' (betslip.BOG_NOTE). Never on the each-way bets.
- LIVE A10: Early Selections Review now shows the FIRST Sky Bet price at or after the flag (the first price the owner could back)
  and settles £5 E/W there too. Backfilled 26 Sep-4 Nov (4 day-stage sets left out where today's rebuild found a different set):
  Early 204 bets with a Sky price +£89.38 at the first Sky price v 230 bets +£316.25 at the flagged quote; Early Bird 20 bets
  +£121.00 v 22 bets +£305.75. BET NOW and the extra-place trial already use Sky Bet prices only.
- LIVE A11 (5 Nov): stake warning on the slip over £150. LIVE A12: review classes OWN DOING + NOT GOOD ENOUGH.
- LIVE Phase B: predict/plan_line.py nightly -> summary.md + reports/predictions/plan_line.md: races with no Sky Bet price at
  09:30, and safe 7/10+ picks v the honest 55% target (60% line shown, never promised). To 4 Nov: safe 7/10+ 159/287 = 55.4%,
  +£379.60 at the 09:30 price; halves 59.5% | 50.4% (split 16 Oct). All 7/10+ 261/521 = 50.1%, +£8.50.
- NOT LIVE A2/A3/A5 (slip shape): the PRICE MIX trial stays (owner's own choice 3 Nov, E16, judged ~5 Dec). Since 4 Nov there is no
  3-4-5 treble already (price-mix treble = best value in each price band). Changed only if the owner says so in the ZANS chat.
- NOT LIVE A6 (8-14 days off the slip): live 7/10+ 8-14 days 17/56 -£189.20, but the picks the slip can actually take (safe, 2.00+)
  were 12/28, -£0.30 (rest 80/142 +£451.30) - nearly all the loss came from picks already kept off; history 2019-26 SP<3.00 A/E
  1.07 | 1.07 (same as 15-30 days). Stays a background record (E19).
- NOT APPLICABLE A7 (8-10/10 in 6-8 runner fields / jumps never lead a multiple): price-mix legs are chosen by price band and value,
  not by rank. Live 7/10+ under 8 runners 134/257 +£49.30 (leak finder segment).
- UNCHANGED: race-day 09:30 BET NOW alerts (owner's call), free tip of the day (waits for the 'Send one daily free value tip'
  thread's spec - one spec, not two).

## E21-LIVE - MARK RISE caution (pre-registered 6 Nov 2026, live from Sat 7 Nov; LABEL + BACKGROUND RECORD ONLY)
- Source: owner 6 Nov 19:50 UK (relayed by the ZANS Review team): "Sort it for Tommorow !!!!", decision card "Yes, caution label now
  + re-test". Team test (exploratory, found after looking) re-computed here: predict/mark_rise.py --backtest 2026-09-26 2026-11-05
  -> reports/predictions/mark_rise_test.json.
- Rule: locked win pick = Sky Bet race-morning favourite (or joint), confidence under 7, FLAT or AW_FLAT HANDICAP, latest flat run in
  our store carries an OR (no label when the latest run is missing), today's card OR minus that OR = +1 to +7 lb.
- Test (locked race-day packs 26 Sep-5 Nov, £10 win at the 09:30 Sky price): labelled 22/158 (13.9%) -£812.90 (H1 13/76 -£272.60 |
  H2 9/82 -£540.30) v mark level/lower 81/233 (34.8%) +£642.70 (+£329.20 | +£313.50). Team's own count 20/131 (15%) -£602.50
  (different coverage filter) - same direction. Our 2nd-ranked horse in labelled races 20/80 +£239.90 = RECORD ONLY, no switch.
- Action: card Notes / selection report / public_picks 'mark_rise' caution "FAVOURITE UP Xlb IN THE HANDICAP ... NO BET (trial)".
  Slip logic unchanged (these picks are under 7/10 = never on the slip anyway). Never a pick switch.
- Judge: after 60+ labelled live picks from 7 Nov: PASS if their win rate is 8+ points below the level/lower-mark control AND they
  lose at the 09:30 Sky price in BOTH halves of the live period. FAIL -> remove the label.
- Daily: python -m predict.mark_rise --date D after the 09:30 lock -> reports/predictions/<D>/mark_rise_trial.json; evening
  python -m predict.mark_rise --date D --settle -> reports/predictions/mark_rise_record.md (one summary.md line).

### E6-LIVE RESULT - FAILED at the first judgement point (recorded 16 Nov 2026)
- FILTER-PASS reached 431 bets (gate 300+) on 24 days to 15 Nov.
- A/E against the margin-free Sky 09:30 price: PASS 1.14 (SE 0.07) v FAIL 1.29 (SE 0.10). Gap -0.14, z -1.2.
- ROI at the 09:30 price: PASS -2.5% v FAIL +5.6%.
- The pass rule needs PASS above FAIL with z >= 2 AND PASS beating FAIL at 09:30. Both parts fail, so E6 = FAIL. Never live; nothing changes on the cards or the slip.
- The record keeps running in the background for information only (reports/predictions/fav_filter_record.md).

### Under-2.00 win singles trial (CONF_SINGLE_MIN_PRICE 1.0, from 20 Oct) - CLOSED 16 Nov 2026
- On the counted slips: 13/28, -£68.80.
- Last bet 3 Nov. Superseded on 4 Nov by the price-mix slip, which has no single under 2.00.
