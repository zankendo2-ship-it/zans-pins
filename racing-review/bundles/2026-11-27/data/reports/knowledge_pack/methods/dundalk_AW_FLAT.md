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
