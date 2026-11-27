# Ascot — Flat — ZANS method v1.3 (data-built + owner reviews tested + Champions Day trials)

No owner method has been uploaded for Ascot. Built from our history after the Fri 2 Oct card.
Rule tests: `reports/methods/ascot_FLAT_rules.md` (855 races from 2019) + split 2019-21 / 2022-26.

## Rules (predict/course_method.py)

| Rule | Factor | History (A/E, runners; 2019-21 / 2022-26) |
|---|---|---|
| Top recent RPR (best of last 3) | x1.06 | 1.11 (986; 1.15 / 1.09) |
| Slow away 2+ of last 4, race up to 1m | x1.05 | 1.27, +5% at SP (513; 1.24 / 1.28) - provisional |

Notes, not rules: favourites are under-rated at Ascot (1.17, +1%, 912; 1.21 / 1.15) - never oppose an
Ascot favourite on evidence alone. Front-runners 0.92 (1.08 / 0.84) and lone front-runners 0.99
(1.30 / 0.86) flipped between periods - no rule. Exact-conditions RPR 1.00 (1.23 / 0.88) - no rule.
Age 6+ out of form 0.91 (0.94 / 0.90) - small, watch.

## Change log
- v1.0 (2026-10-02, review of Fri 2 Oct: win picks 2/5 + Cranachan non-runner; Who Wants Me, a race-morning
  value pick, won at 17.00): built from history.

## Owner's Ascot reviews (uploaded 3 Oct: ASCOT FLAT REVIEW 2.pdf = Reviews 001-016, v27-v31, May-Jun 2026;
## ASCOT FLAT Review.pdf = Reviews 1.1-2.4, v33.1+, 11 Jul - 6 Sep 2026)
- **Best card: 17 Jun 2026 (Royal Ascot, v30.0 "Stiff Finish Positionalist" / v31.0): 3 winners (Limestone, Blue Bolt,
  Alobayyah), +£4.58.** Other v30-31 cards: Review 015 -£4.17, 19 Jun -£3.00 (2 winners: Venetian Sun, Precise).
- **Slump: v33.1 onwards (Jul - Sep): 11 Jul 2/7, Review 1.2 1/5 staked, 26 Jul 1/7, 9 Aug 0/6, 5 Sep 1/7, 6 Sep 1/7**,
  as more rejection rules piled up (weak-finish reject, start-risk reject, seasonal handbrake, wind laws).

| Owner rule (v30/31) | Ascot data 2019-26 (A/E; 2019-21 / 2022-26) | Verdict |
|---|---|---|
| Top RPR / class proven | top recent RPR 1.11 (1.15 / 1.09) | KEPT x1.06 |
| HR3 weak finish ("no extra / weakened / faded") = reject | straight 0.98 (1.00 / 0.98), round 1.06 (1.10 / 1.05) | DROPPED |
| HR4 start risk: slowly away in 5-6f or 15+ runners = reject | straight big fields 1.09 (0.76 / 1.24); slow starters up to 1m 1.27 | REVERSED (x1.05 kept) |
| Swinley Slingshot: round course, hold-ups only if pace collapses | round-course hold-ups 0.83 (0.58 / 0.98); mid-division 1.21 (1.21 / 1.21) | NOTE - recent years neutral, so no factor yet |
| Straight course: tearaway leaders vulnerable | straight usual leaders 0.97 (1.08 / 0.94) | NOTE only |
| HR11 seasonal / trial layoff handbrake | back 120+ days under 2/1: 0.98 (27) | DROPPED (no edge) |
| Favourites | 1.17, +1% (912) | never oppose an Ascot favourite on evidence alone |

- v1.1 (2026-10-03 11:00 UK): owner reviews onboarded. NO CHANGE to factors: the only rule that would have touched today
  (round-course hold-up caution, 14:25) is neutral since 2022, so it stays a note. Today's Ascot picks unchanged.
- NO CHANGE (2026-10-03 review of Sat 3 Oct: win picks 1/6): Four of the five beaten picks were placed or close, two winners came from off the pace, and the front-runner record at Ascot is 0.92 overall but not consistent (1.08 in 2019-21, 0.84 since 2022), so one day of hold-up winners is not a rule. The top-RPR factor stays: its horses won 1 of 6 today but have A/E 1.11 over 986 runners. Evidence: Ascot flat from 2019: top recent RPR A/E 1.11 (986; 1.15 / 1.09); slow away up to 1m 1.27 (513); front-runners 0.92 (1.08 / 0.84); favourites 1.17. Today: top card-RPR horse in each race 1/6 won (So Regal), 2 placed (Tenability 3rd, Rosario 3rd at 11.00).
- v1.2 (2026-10-15, Champions Day study - reports/research/2026-10-15_champions_day_research.md): three TRIAL rules for Group
  races, each tested AGAINST OUR MODEL on races it had not seen (model fitted on races before 2023; 2023-24 | 2025-26, all
  UK/IRE Group races) so they add something the model does not already know:
  * usual front-runner in a Group race at 1m2f-1m4f x1.12: A/E 1.26 (95) | 1.22 (59); at Ascot against the price 1.52 | 1.84,
    hold-up horses there 0.62 | 0.49.
  * 4-year-old in a Group race in September-October x0.88: A/E 0.83 (174) | 0.63 (120); Group 1s at SP 0.65 | 0.76.
  * usually races midfield in a Group race at 5-7f x0.85: A/E 0.64 (139) | 0.43 (67).
  Not used (no consistent edge over the model): won on the going (0.98 | 1.14), won at the trip (1.01 | 1.15), Group 1
  runner never placed (1.02 | 0.52). Effect on Sat 17 Oct picks (d-2 prices): no win pick changed (Almeraq 37.6% -> 36.4%).
  Judge on the Champions Day results; national use only if they hold.
- v1.3 (2026-10-15 evening, owner: "is all this extra research going to go into every prediction"): the round-2 Champions Day
  findings were tested a SECOND time, against OUR MODEL on races it had not seen (model fitted before 2023; 2023-24 | 2025-26,
  reports/research/scripts/champions_day/a13_round2_v_model.py). Only findings that held in BOTH checks (price 2015-20 | 2021-26
  AND model 2023-24 | 2025-26) were added, as small TRIAL factors (samples are small):
  * low draw, 14+ runner 6f on good or firmer (far side) x1.10: v model 1.53 | 1.80 (10 winners); v price 1.21 | 1.56.
  * high draw, 14+ runner 6f on good or firmer x0.93: v model 0.67 | 0.80; v price 0.81 | 0.88.
  * high draw + usually races prominently / leads at 1m4f x1.08: v model 1.15 | 1.47; v price 1.34 | 1.53.
  * low draw at 1m4f on good or firmer x0.92: v model 0.74 | 0.71; v price 0.73 | 0.70.
  * straight mile 16+, low or middle draw + usually held up / midfield x1.06 each: v model 2.13 | 1.42 and 1.44 | 2.26 (small);
    v price 1.35 | 1.31 and 1.33 | 1.92.
  * Aidan O'Brien runner 5th or bigger in the betting in a Group 1 x0.85: 1 winner from 86 in 2023-26 Group 1s (v model 0.62 |
    0.00); at Ascot 1 winner from 113 since 2015.
  NOT added (failed the second check): QEII round-mile low draw (v model 0.54 | 1.02), Champion Stakes middle draw (1.75 | 0.92),
  Balmoral weight 14lb+ below top (Ascot 1.10 | 0.44; all UK/IRE 16+ turf handicaps 0.95 | 0.93 - the "1 winner from 121" was
  the price, not something our model misses), 1m4f high draw + held up (price 1.13 | 0.56, model 0.59 | 0.63 - not both periods).
  Effect on Sat 17 Oct (d-2 prices): no win pick changed; Kalpana 34.1% -> 32.7% (drawn 1), Amelia Earhart / Hawk Mountain /
  Sugar Island (O'Brien outsiders) trimmed, Sprint low draws up / high draws down, Balmoral held-up runners from low/middle up.

- NO CHANGE (2026-10-17 review of Sat 17 Oct): No change to Ascot FLAT v1.3. The lesson goes into the slip rules instead: never override the data-gap rule by judgement. The two Ascot picks that ran badly, Kalpana and Gstaad, were both horses whose latest run was abroad and missing from our data. Our standing rule keeps such picks off the bets and I overrode it, so this was my error, not the course method's. The Sprint lottery rule cost a winner today (Almeraq) but rests on eleven renewals, so it stays for now. Evidence: Today: data-gap picks Kalpana 7th at 2.00 and Gstaad 8th; complete-form picks won 2/5 (Almeraq, Ombudsman). Flat horses that have never won on the going after 4+ tries: A/E 0.97 (2015-20) and 1.01 (2021-26); top three in the betting 1.04 and 1.07, so this is not a caution.
- WATCH (2026-10-18, owner on Minnie Hauk): age4_autumn_group x0.88 counted against Minnie Hauk (14:40 Fillies & Mares, won 8.50, SP 6.00). It cut her joint chance from about 14% to 12.2%, while her evidence-only chance was 23.5%, the best in the race. NO CHANGE: one race against the 294-runner test (0.83 / 0.63 against our model). Re-test at the next Ascot Group card.
