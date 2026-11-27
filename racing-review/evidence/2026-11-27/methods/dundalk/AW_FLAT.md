# Dundalk — All-weather (Polytrack) — course onboarding review + ZANS method v13.4 (v13.3 2 Oct: top-RPR boost off; v13.4 16 Oct: prominent x1.04 trial)

Source: owner's `DUNDALK_AW_FLAT_REVIEW.pdf` (38 pages): a DNA calibration pass (Review 12.1)
and ONE scored card, 18 Sep 2026 (Review 13). Earlier reviews 1–12 are not in this file.
Rule tests: `reports/methods/dundalk_AW_FLAT_rules.md`. Odds in decimals.

**DATA WARNING:** our form history has Dundalk results only for 2010–2014 and 2025–2026. The
Kaggle source is **missing Dundalk 2015–2024**, so the rule tests here use 278 races (2025–26).
The pace and draw tables use 2010–14 + 2025–26. Fix planned: backfill Dundalk from Sporting Life.

## 1. Scorecard — 18 Sep 2026 (method Review 12.1)

| Race | Pick | Result | Winner |
|---|---|---|---|
| 17:25 | Hanney Boy | 2nd, 5.50 | Force Noir 2.50 fav |
| 18:00 | The Pipeman | 5th, 4.00 | Value Pending 13.00 |
| 18:30 | Send Harry | 2nd, 4.33 fav | Mickey The Steel 10.00 (the RPR pick) |
| 19:00 | Perfect Judgement | 8th, 5.00 | Starflow 11.00 |
| 19:30 | Pavilion End | 9th, 3.75 fav | Kilcrea Rock 5.00 |
| 20:00 | Without Love | 6th, 2.88 fav | Wild Berries 29.00 |
| 20:30 | **Numantia** | **WON 1.33 fav** | |

**1 from 7, −£5.67.** 4 of the 7 picks were favourites. The RPR pick won 1 (Mickey The Steel, 10.00).
Only one card, so there is no best spell yet.

## 2. Rules v our data

| Claim | Data | Verdict |
|---|---|---|
| Front-runners dominate at all trips | The pace table agrees (5f–1m4f "front-runners favoured"), **but** horses that usually lead are over-bet: A/E **0.80**, −59% (115) | The bias is real but priced in: x0.93 |
| Draw by field size (5f low best, 7f middle, 1m outside) | 6f–1m2½f **low** third best (IV 1.12–1.28, HIGH); 5f unclear (PRB says low, win-rate says high); 7f middle ≈ low | 6f–1m2½f low draw: NOTE; 5f claim unproven |
| Non-handicap favourites 39% v handicap 28% | Favourites overall A/E 1.06 | KEEP the "trust non-handicap favourites" idea (don't knock out) |
| Start risk | A/E 0.89 | x0.96 |
| Apprentice first-time (Hard Rule C) | first-time pairing A/E **1.07** | **DROP** |
| Age 6+ | A/E 0.90 | x0.96 |
| Top recent RPR | A/E 0.89 (small sample) | x0.96 (review when more data) |
| Big-field outsider watch | 2 winners at 13.00+ on the card; big-field market rank 9+ A/E ~0.82 in the chat's DNA | NOTE (our longshot rule covers it) |

## 3. ZANS METHOD v13.1 — DUNDALK — AW (code: predict/course_method.py)

```
WIN PICK: price-free ZANS model, then Dundalk multipliers (small sample, heavily shrunk):
  usual front-runner x0.93 | slow starter (<=1m) x0.96 | age 6+ x0.96 | top recent RPR x0.96
NOTES: 6f-1m2.5f low draw best (priced in); front-running bias real but over-bet.
DROPPED: Hard Rule C apprentice first-time; 5f bottom-third draw claim (not supported).
BET: confidence 8+ (data only). LONGSHOT: 14.0+ decimal, 6+ runners.
```

## 4. Change log
- v13.1 (2026-09-24, ZANS onboarding): results verified; rules tested; Dundalk data gap logged.
- v13.2 (2026-09-26, review of 25 Sep): win picks 3/7 (Caffu Zafeen, Haven BET, Military Order), RPR picks 4/7 (beat the win stream). The 'top recent RPR over-bet' penalty (0.96) rested on a thin 2025-26 sample (320 runners) and both horses it hit won -> penalty REMOVED until the Dundalk 2015-24 backfill lets us re-test it.
- 2026-09-26: + all-UK default "top recent RPR" 1.03 (national AW A/E 1.07) replaces the removed Dundalk penalty.
- v13.3 (2026-10-02, review of 2 Oct: win picks 2/8 - Caffu Zafeen, Golden Ring; 3 races won by front-runners):
  national "top recent RPR" boost (1.03) switched OFF at Dundalk (factor 1.00): Dundalk A/E 0.87, -36% (341
  runners, 2022-26 only - Kaggle still has no 2015-24). Front-runners: 3 made all tonight, but history still says
  usual front-runners are over-bet (0.82, 125) -> leader x0.93 KEPT. Usually prominent 1.10 (1,367) noted, single period.

- NO CHANGE (2026-10-09 review of Fri 9 Oct): Dundalk AW v13.3 unchanged (top-RPR boost off). One winner from seven is poor, but two picks were beaten narrowly, one was hampered and one was a debutant. The one clear miss was a BET pick never tried at the trip, and that is already covered by the slip's proven-trip rule, which kept Camino Lad out of the multiples. No Dundalk rule is contradicted by tonight's results. Evidence: Today 1/7 won (plus 1 non-runner), 1 third beaten 0.75L, 1 hampered. Five of eight winners raced prominently or led. Camino Lad was not on the slip (never run at 1m4f).

- CHANGE v13.4 (2026-10-16 review of Fri 16 Oct: win picks 2/8): usual PROMINENT runners x1.04 (TRIAL, new rule kind 'prominent'). At Dundalk, horses that usually race prominently beat their price in both years we hold (A/E 1.18 in 2025 from 580 runs, 1.08 in 2026 from 784), while across all GB/IRE all-weather tracks they are exactly as priced (1.02 / 1.01), so this is a course effect. TEST on Friday: the 18:30 pick changes from Go Out (2nd, beaten 0.5L) to Sedro Woolley (won 6.50); no other pick changes. Provisional: Dundalk history before 2025 is missing (backfill planned for November). Usual front-runner 1.10 / 0.98 and held up 1.00 / 0.88 left as they are.

- 2026-10-23 review: NO CHANGE. Win picks 1/7 (Washington Heights, off every bet - data gap). VERIFIED: 7 of the 8 races (17:15-20:15)
  had NO bookmaker price at d-1_evening, d0_morning or d0_midday (only the 17:10 copy carried bookie terms) -> picks ran on static
  Sporting Life quotes; big moves (Surpass And Shine 34.00 -> SP 4/1, Bobardi 15.00 -> 2/1 fav) were invisible. 'prominent' x1.04
  trial card 1: flagged runners 3/36 v 3.08 expected (0.97). TEST: fancied first-time AW (SP<5) GB/IRE 1.02 (572) | 1.08 (1,047) =
  no weakness; Dundalk 12+ low draw 0.84 (2025) | 0.87 (2026) over-bet - WATCH (no Dundalk history before 2025). Scripts
  /tmp/claude-0/team23/dundalk/.
- 2026-10-28 review: NO CHANGE - The prominent trial looks good over two cards but changed no pick today. The only flagged pick was Crayons In The Sky, at 55% against 23%, so removing the x1.04 leaves all eight picks the same. Gallo Dell Cielo would only have become the 17:30 pick with a factor near x1.07, and one race is not evidence for that. Dundalk history still holds 2025-26 only, so a bigger factor cannot pass the two-period test until the November backfill. The hold-up-in-a-slow-race idea from 23 Oct failed on history, so there is no new rule from it.
- 2026-10-29 re-test (newest results to 28 Oct): NO CHANGE - every live rule still points the same way in both periods (reports: /tmp/claude-0/retest).

## Change log
- 2026-10-30 review: NO CHANGE - 5/7; prominent x1.04 trial after 3 cards 9/87 v 7.69 expected (1.17), changed no pick - stays a trial.

- NO CHANGE (2026-11-04 review of Wed 4 Nov): Dundalk AW v13.4 unchanged (prominent x1.04 trial kept; it changed no pick). 3 of 7 win
  picks won (Apache Outlaw, Carrigans Grove, The Rock Factor). TEST on our short Dundalk history (Oct 2025-Mar 2026 | Apr-Nov 2026, 353
  races): non-handicap favourites 1.01 (79) | 1.52 (44), handicap favourites 1.04 (171) | 0.97 (59), trainer hot at Dundalk 14 days
  1.17 (92) | 0.97 (30), won last Dundalk run 1.03 (98) | 0.64 (25), 2+ Dundalk wins 1.27 (42) | 1.05 (32, -£14.70 at £1 SP) - nothing
  holds in both halves; history too short (no 2015-24).

- 2026-11-06 review: NO CHANGE. Win picks 2/7. TEST on our Dundalk history. The file covers only 17 Oct 2025 - 5 Nov 2026, so there is no 2019-21 period. I used 360 races after dedupe, split Oct 2025-Mar 2026 (250) | Apr-Nov 2026 (110), with A/E against margin-free SP. Horses that usually raced up with the pace in previous Dundalk runs (2+ runs, 50%+ early) scored 1.11 (177 races) | 1.06 (78) against 1.04 (158) | 0.94 (76) for the rest, but both groups lose heavily at SP. This is the same direction as the existing trial and already covered by it. SP favourites at 2.00 or shorter in non-handicaps: 1.06 (21 races) | 1.61 (12), a small sample in both, so tonight's two beaten maiden favourites are no reason to oppose them. Handicap favourites 1.04 (171) | 0.97 (63) flip. Nothing new holds in two 30+ race periods.

- NO CHANGE (2026-11-11 review of Wed 11 Nov, win picks 1/7): only Lookingforarainbow won; favourites 0/7 on the card. Slip legs: Justenzia 2nd beaten 1.5L by Shoot To Kill (draw 1, 6lb less, named lone front-runner by our pace map) - single, double and treble lost; Eastern Peace 7th (weakened, 7th of 14 on our speed figures). Noon re-pick changed 3 races, all would have lost. prominent x1.04 trial 17/157 v 16.03 expected over six cards (A/E 1.06) - kept. TEST: AW quick return after a win 1.05 | 1.04 - not a weakness.

- 2026-11-13 review: NO CHANGE. No change. Dundalk AW stays at v13.4: top-RPR boost off, usual front-runner x0.93, slow starter x0.96, age 6+ x0.96, and the 'usually races prominent' x1.04 TRIAL. Why: No beaten pick was a clear method error. Four were placed or close, one ran keen, one was a non-runner, and Crayons In The Sky was beaten on merit with no warning. The prominent trial changed no pick; Crayons would have stayed top without it. Its flagged runners went 4 from 23 against 2.86 expected tonight (A/E 1.40). The running total over seven live cards is 21 from 180 against 18.89 (1.11); all other runners are 29 from 387 against 30.97 (0.94). That is positive but still a single period, and Dundalk history before 2025 is missing. Two of the four flagged winners (Rock On Johnny and Honouramongthieves) won from off the pace, so the label is not measuring what it claims. The front-runner caution x0.93 was 1 from 4 (Firewalker won) against 0.49 expected: one card, no change. The serial-placer maiden favourite idea raised by Sangreal does not hold: those favourites beat their price in both periods. methods.audit was not re-run because no rule was proposed.

- 2026-11-18 review: NO CHANGE. No beaten pick was a clear method error. Three were beaten 0.5L or less, Pradas World had no clear run, and Celtic Comet hung. The prominent trial changed no pick tonight; every pick stays top with x1.04 taken off. Its flagged runners went 2/28 against 2.38 expected (A/E 0.84). The running total over eight live cards is 23/208 against 21.27 (A/E 1.08), down from 1.11. That is still a single period, because Dundalk history holds 2025-26 only, so nothing can pass the two-period test. 12 of tonight's 28 flagged runners raced off the pace, including the winner Tempted Angel. No other rule was proposed. Evidence: Script /tmp/claude-0/drafts/tally18.py: field angles from the locked reports/predictions/2026-11-18/sent/3_d0_morning_0933/dundalk.json, results + margin-free SP from reports/results_sl/2026-11-18/results.csv, giving 2/28 v 2.38 expected. Running total adds the 13 Nov notes' 21/180 v 18.89. The pick-change check divides the chance of flagged runners by 1.04 and finds no change in any of the 8 races. history/results_form.csv.gz holds Dundalk rows for 2025 (1,632) and 2026 (1,534) only. Golddream: runners.csv reserve=True, d0_morning jockey 'Reserve 1', Sky Bet v2 3.5; not in evidence_prerace.csv. Stewards: reports/stewards/2026-11-18/ihrb_incidents.csv is header only, so no Irish stewards' report is in yet. Slip: Otsana won its treble leg; the treble was lost to Divine Whisper (Kempton 17:30, 2nd).
- 20 Nov 2026: NO CHANGE - prominent x1.04 trial changed no pick; running 28/243 v 24.87 expected (reports/reviews/2026-11-20/dundalk_learning.json).

- 2026-11-25 review: NO CHANGE to Dundalk AW_FLAT v13.4. 0 winners from 8 against 2.43 expected; every winner 4/1-18/1, SP favourites beaten across the card. Two 9/10 odds-on picks lost (Sharpe Ratio, Lets Smash It) - tally kept, no rule from one card.
