# Fontwell Park — Jumps — ZANS method v16.0 (owner peak v15.0, data-tested)

Source: owner's `FONTWELL JUMPS Review.pdf` (Review No. 031, AURORA-X v14.0 -> v15.0 Track DNA Edition, Review 1.1)
and `FONTWELL JUMPS REVIEW 2.pdf` (Reviews 1-6, Jan-May 2026, v11.6 -> v14.0). Rule tests:
`reports/methods/fontwell_JUMPS_rules.md` (940 races from 2019) + split 2019-21 / 2022-26.

## Peak and slump
- **Best spell: v15.0 Track DNA Edition, Fri 28 Aug 2026** - 3 winners from 6 bets (Salkadan 4/6, Delgany Second Now
  9/4, Youdecide 8/13), +£0.54 at £1; win pick = RPR pick in all three wins.
- **Slump: v11.6 - v14.0, Apr-May 2026** - Review 4 (8 Apr) -£6.00, Review 5 (14 May) -£6.00, next card -£5.17. Gates
  were added card by card (C&D first, ±2f trip proof, first-time claimer HARD-FAIL, 120+ day layoff HARD-FAIL).

## Owner rules v our data
| Owner rule | Fontwell data (A/E; 2019-21 / 2022-26) | Verdict |
|---|---|---|
| RPR / exact conditions RPR synergy (G) | top recent RPR **1.19, +7% at SP** (1,000; 1.19 / 1.19); exact-conditions 1.02 | KEEP - top recent RPR x1.10 |
| Pace 4/3 front-runners heavily favoured (D) | usual front-runner 0.93 (0.85 / 0.98); lone 0.97; prominent 1.00; held up 0.96 | DROPPED - no edge |
| Gate A distance proof ±2f | unproven at trip 1.00 (0.94 / 1.04) | DROPPED |
| Gate C first-time jockey HARD-FAIL | first-time pairing 1.04 (1.13 / 0.98) | DROPPED |
| Course specialist law / C&D | C&D winner 1.05 (0.98 / 1.09); course winner 1.03 | NOTE only (mixed) |
| Layoff 120+ trap | back 120+ days at under 2/1: 0.85 (56 - small; 1.03 / 0.71) | NOTE - not a rule (owner: jumps horses often return from a summer break) |
| Improver (7ex / well-in) | improver 1.04 (1.08 / 1.02) | NOTE only |
| Favourites | 1.03 (both periods) | not opposed |

## ZANS rules (predict/course_method.py)
- top recent RPR (best of last 3) x1.10

## Change log
- 2026-10-21 review: NO CHANGE - official 3/6 (I Love You Sivola first past the post, disqualified - rider weighed in light). Top recent RPR holds on soft (A/E 1.10 / 1.14; soft chases 1.34 / 1.31); good-ground chases 1.06 / 0.89 on watch.
- v16.0 (2026-10-03): onboarded from the owner's two PDFs; built around the v15.0 peak; only the rule that holds in
  both periods kept (top recent RPR). Gates and the front-runner law dropped on the data.
- NO CHANGE (2026-10-03 review of Sat 3 Oct: win picks 1/7): Three front-runners won today, but on history Fontwell front-runners are slightly over-bet (A/E 0.93 over 598) and lone front-runners only 0.97, so the owner's front-runner law stays dropped. Salkadan points to a juvenile-jumping caution, but that needs testing across all courses before it becomes a rule. Evidence: Fontwell jumps from 2019: usual front-runner A/E 0.93 (598); lone front-runner 0.97 (321, +7% at SP); held up 0.96 (1,987); top recent RPR (x1.10 in v16.0) A/E 1.19. Today: front-runners won 3 of 7 races.

- NO CHANGE (2026-10-15 review): win picks 3/7, all three winners backed in from the day before; beaten odds-on Emerald Quest was in a mares' maiden hurdle (already off the slip).
