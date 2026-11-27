# Doncaster — FLAT — ZANS method v1.0 (DATA-BUILT, no owner method)

Built 22 Oct 2026 for Fri 23 Oct (and the Group 1 card on Sat 24 Oct). Owner has no Doncaster method.
Tested on 1,282 Doncaster flat races 2019-26 (reports/methods/doncaster_FLAT_rules.md) and 842 races 2022-26
(..._since2022.md); 2019-21 worked out from the difference (~). A rule is used only when both periods agree.
History built AFTER the 22 Oct all-weather type fix (does not affect turf Doncaster).

## Angles
- Top recent RPR x1.08 - A/E 1.19 (1,452); ~1.17 / 1.20.
- Won last time x1.04 - A/E 1.11 (1,667); ~1.15 / 1.09.
- Usually held up x1.04 - A/E 1.10 (3,850); ~1.12 / 1.09.
- Improver x1.03 - A/E 1.09 (1,932); ~1.05 / 1.11.
- Age 6+ out of form x1.03 - under-bet here: A/E 1.13 (1,174); ~1.11 / 1.14.

## Cautions
- Weakened / no extra in either of last 2 x0.95 - A/E 0.91 (4,694); ~0.83 / 0.94.
- Usual front-runner x0.95 - A/E 0.87 (947); ~0.73 / 0.94.
- Jockey under 6% x0.93 - A/E 0.83 (970); ~0.64 / 0.93.

## Not used (periods disagree)
- Course & distance winner 0.94 (~1.22 / 0.85), lone front-runner 0.94 (~0.54 / 1.15), ground specialist,
  unproven trip 1.06 (~0.98 / 1.10), held-up short-trip mandate 1.05 (~1.21 / 0.98).
- Favourites A/E 1.13 (both periods) - never opposed.

## Change log
- v1.0 (2026-10-22): data-built for Fri 23 Oct.

- 2026-10-23 review (first card on v1.0, going Soft -> Heavy (Soft in places) after 8.6mm overnight): NO CHANGE. Win picks 1/8
  (Bulletsnap, kept off the slip by the drift rule); Desert Romance (9/10) 3rd at 4/6 - single + double lost. TEST (UK/IRE flat
  turf, margin-free SP A/E 2019-21 | 2022-26): Appleby on soft/heavy 1.11 | 1.11 (no weakness); Doncaster won last on soft/heavy
  1.02 | 1.27, top RPR on soft/heavy 1.01 | 1.29, led last time 0.94 | 1.32 - not consistent. CANDIDATE (not used): low third of
  the draw, 5-7.5f straight, 10+ runners, soft/heavy 1.53 (124, 29 races) | 1.23 (263), -8.9% at SP; good to soft 0.50 (22) | 1.08
  (95), so our SOFT going group (which includes good to soft) would not match it - to be tested against OUR MODEL first (research
  queue). Scripts /tmp/claude-0/team23/doncaster/.

- 2026-10-24 review: NO CHANGE. The Doncaster-only heavy pattern holds in both periods, but it rests on just 72 heavy races (16 of them in 2019-21, where the 'never' group had only 32 runners and 2 winners). Across all UK/IRE heavy flat turf it disappears: never-on-soft/heavy horses A/E 1.06 | 0.99, and fancied ones 0.96 | 1.07, which flips. Today's card went the other way: never-on-soft/heavy runners won 3 from 21, A/E 1.13, while horses that had already won on soft/heavy won 3 from 33, A/E 0.75. The slip-level heavy-ground safety trial (betslip.HEAVY_SAFETY, from 24 Oct) already keeps flat picks that have never run on soft/heavy out of the multiples on heavy, and that is where the risk sits. A course pick-rule on this sample would be fitting noise. Doncaster soft and heavy combined shows no effect (1.01; 0.93 | 1.04). The fancied 'won on soft/heavy' figure (0.68; 0.77 | 0.66) is the reverse of the national one (1.08; 1.16 | 1.04) and rests on 81 runners, so it is a candidate only. Evidence: TEST /tmp/claude-0/review24/doncaster/heavy_test.py -> heavy_test_out.txt (history/*.csv.gz 2018+ for prior form, RP store preferred over SL; flat turf; races with SP book under 100% or missing SPs dropped; margin-free SP A/E). Soft/heavy = main going Soft, Soft To Heavy, Heavy or Heavy To Soft on any earlier turf run (variant B adding Yielding To Soft gives the same picture). DONCASTER FLAT, main going HEAVY (72 races, 829 runners), A/E (wins/runners) full | 2019-21 | 2022-26: NEVER ran on soft/heavy 0.77 (12/173) | 0.62 (2/32) | 0.80 (10/141), SP ROI -38%; ran on soft/heavy but never won 1.00 (19/248) | 0.74 | 1.11; WON on soft/heavy 1.11 (35/341) | 1.21 | 1.09; debutants 1.03 (6/67). Doncaster HEAVY, SP under 4.0: never 0.39 (2/15) | 0.00 (0/3) | 0.50 (2/12); won before 1.18 (8/24). Doncaster SOFT or HEAVY (302 races): never 1.01 (80/781) | 0.93 | 1.04; won before 0.99 | 0.96 | 1.00; SP under 4.0, won before 0.68 (16/81) | 0.77 (3/13) | 0.66 (13/68), ran but never won 1.38 (25/59) | 1.33 | 1.41. ALL UK/IRE flat turf HEAVY (1,594 races): never 1.02 (386/3,701) | 1.06 | 0.99; won before 0.99 | 0.97 | 1.00; SP under 4.0 never 1.03 (146/427) | 0.96 | 1.07; 2yo SP under 4.0 never 1.04 (77/217) | 0.88 | 1.13. Today (not in the test): never 3/21 (expected 2.65, A/E 1.13), won before 3/33 (4.00, 0.75), ran but never won 2/23 (1.35, 1.48). Limits: name-keyed history (reused names possible); duplicate SL/RP rows under different course names (e.g. Epsom / Epsom Downs) can remain.

- 2026-11-07 review: NO CHANGE. Win picks 5/8. TEST tonight on the Doncaster history file (flat turf 2019-26, deduped across the two sources, today excluded, margin-free SP A/E). Straight 5-7f, 10+ runners, main going Good to Soft or softer. Low third: 15/137 won, A/E 1.28 (35 races) in 2019-21 and 34/358, A/E 1.18 (94 races) in 2022-26. Middle third: 0.94 (35) | 0.78 (94). High third: 1.10 | 1.10. Soft/heavy only (no Good to Soft): low 1.43 (29 races, under 30) | 1.20 (71). It holds in both periods with 30+ races, but the effect is really 'edges beat the middle', not only 'low'. With 16+ runners the cells drop to 4-17 races and flip. The course method's draw_low kind has no trip or field-size limit, so applying it as is would also hit round-course races. It needs a variant first and a check against our model, as queue 15 says.
