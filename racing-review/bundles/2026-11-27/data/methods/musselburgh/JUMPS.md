# Musselburgh — JUMPS — ZANS method v1.0 (DATA-BUILT, no owner method)

Built 26 Nov 2026 for Fri 27 Nov. The owner has no Musselburgh jumps method on file (methods/musselburgh/FLAT.md is separate).

LIVE: **national defaults only** (predict/course_method.py ANGLES[("musselburgh","JUMPS")] = []). Picks are the same as with no course method. Any course factor needs a reviewer PASS first.

## Tested on history (methods.audit, Musselburgh jumps, margin-free SP A/E)
Tables: reports/methods/musselburgh_JUMPS_rules.md (2019-26, 482 races) and reports/methods/musselburgh_JUMPS_rules_since2022.md (272 races). 2019-21 approximate.

| Rule | 2019-26 | 2022-26 | 2019-21 (approx) | Verdict |
|---|---|---|---|---|
| Top recent RPR | 1.09 (522) | 1.07 (298) | ~1.12 | holds; national default already applies |
| Improver | 1.08 (523) | 1.07 (293) | ~1.09 | holds -> candidate |
| Usual front-runner | 1.06 (442) | 1.07 (260) | ~1.05 | holds -> candidate (small) |
| Age 6+ no win/2nd in last 3 | 0.88 (1,293) | 0.81 (693) | ~0.96 | weak in 2019-21 -> not used |
| Unproven at trip | 1.12 (529) | 1.21 (302) | ~1.00 | flips -> not used |
| Course & distance winner | 0.91 (461) | 0.77 (298) | ~1.17 | flips -> not used |

Tested v SP only, not v our model pick, no forward sample -> nothing proposed for live.

## Change log
- 26 Nov 2026 v1.0: created, national defaults only. Candidates noted for a later shadow test.
