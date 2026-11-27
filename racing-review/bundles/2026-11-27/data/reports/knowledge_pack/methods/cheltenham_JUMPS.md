# Cheltenham — JUMPS — ZANS method v1.0 (DATA-BUILT, no owner method)

Built 22 Oct 2026 for Fri 23 Oct. Owner has no Cheltenham method.
Tested on 759 Cheltenham jumps races 2019-26 (reports/methods/cheltenham_JUMPS_rules.md) and 472 races 2022-26
(..._since2022.md); 2019-21 worked out from the difference (~). A rule is used only when both periods agree.
Cheltenham is the hardest jumps course to beat: almost every rule is at 0.95-1.05 here (the market prices it well).

## Angles
- Improver x1.02 - A/E 1.05 (2,199); ~1.05 / 1.05.

## Cautions
- Weakened / no extra in either of last 2 x0.97 - A/E 0.93 (2,183); ~0.95 / 0.92.

## National default switched off
- Top recent RPR boost OFF (x1.00): A/E 1.09 (838), but ~1.27 in 2019-21 and only 0.98 since 2022.

## Not used (periods disagree or no edge)
- Exact-conditions RPR 0.98 (~0.86 / 1.05), front-runner 0.95 (~1.02 / 0.91), jockey under 6% 0.99 (~1.35 / 0.77),
  held up 1.04 (~1.00 / 1.07), keen/hung 0.90 (~0.85 / 0.92 - live rule checks 'hung' only), lightly raced 1.07
  (~1.06 / 1.08 - no rule kind yet).
- Favourites A/E 1.06 (1.10 since 2022) - never opposed.

## Change log
- v1.0 (2026-10-22): data-built for Fri 23 Oct.

- 2026-10-23 review (first card on v1.0): NO CHANGE. Win picks 2/7 (Bowensonfire, JPR One); Mr Hollywood (9/10 BET) 4th of 7 -
  DATA GAP: latest run ParisLongchamp 3 Oct (7th/10) was missing and the card's '86 (20F)' was not parsed (fixed 23 Oct night,
  form.history.days_since). TEST (margin-free SP A/E 2019-21 | 2022-26): Cheltenham jumpers last run on the flat 0.47 (49) | 1.54
  (102), non-handicap novice/maiden hurdle favourites 1.20 (46) | 0.83 (69) - both flip, no rule. Script
  /tmp/claude-0/team23/cheltenham/tests.py.

- 2026-10-24 review: NO CHANGE. (1) Habitual leaders in a strong-pace race (3+ leaders) at Cheltenham won A/E 0.71: 0.82 in 2019-21 and 0.61 in 2022-26. Nationally the figure is 0.94, and the method has no rule kind for 'leader in a strong-pace race' (the existing 'leader' kind also covers EVEN races, where Cheltenham reads 1.25 then 0.84 = flips). This needs a new rule kind and a test against our model's pace features first. (2) Cheltenham jumpers 90-179 days off read 0.74 / 0.87 and 180+ days off 0.93 / 0.89, while nationally both are ~1.00. However, favourites back after 180+ days read 1.06 / 1.02 at Cheltenham, and the break was measured from our own history, which overstates it for pointers and runs abroad. The live rule uses card days, the model already has days-since, and the slip already excludes 90+ day horses. Today 3 of the 4 long-absent picks won, all of them favourites. So no rule from today alone. Evidence: TEST scripts /tmp/claude-0/review24/pace_test.py (-> pace_test.txt) and /tmp/claude-0/review24/layoff_test.py (-> layoff_test.txt). Data: history/results_form.csv.gz to 2026-05-27 plus history/store_2026-06..10, UK/IRE jumps 2019-01-01 to 2026-10-23. Races whose 1/SP book is under 1.00 were dropped. Horses are keyed by form.history.name_key. Roles come from speed.pacemap (last 6 readable comments). Figures are FULL | 2019-21 | 2022-26. Cheltenham, strong pace (3+ habitual leaders): LEADER 0.71 (503 runners, 28 won) | 0.82 (210, 15) | 0.61 (293, 13); HOLD_UP 1.37 (374, 29) | 1.27 | 1.47; all UK/IRE jumps LEADER 0.94 (5,816) | 0.90 | 0.96, HOLD_UP 1.11 | 1.17 | 1.07. Cheltenham lone leader 0.92 (234) | 0.91 | 0.93; the lone leader actually led in only 39% of races (49% | 34%) by our comment reading (national 38%). Lone leader with a keen prominent rival 1.11 (39) | 0.86 (93) v without 0.74 (46) | 1.03 (56) = flips. Prominent runner that was keen in either of its last 2 runs, in a lone-leader race, at Cheltenham: 1.19 (191, 29 won) | 1.09 (56) | 1.24 (135), v not keen 0.99; national 1.04 | 1.08 | 1.03 (small, watch). Layoffs at Cheltenham: under 90 days 1.03 (7,092) | 1.03 | 1.03; 90-179 days 0.82 (548, 29 won) | 0.74 (220) | 0.87 (328); 180+ days 0.91 (1,026, 86 won) | 0.93 (387) | 0.89 (639); SP favourites back 180+ days 1.03 (100, 30 won) | 1.06 | 1.02. National 90-179 days 1.01 | 0.99 | 1.01; 180+ days 1.00 | 1.04 | 0.97.
