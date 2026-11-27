# Doncaster — JUMPS — ZANS method v1.0 (DATA-BUILT, no owner method)

Built 26 Nov 2026 for Fri 27 Nov. The owner has no Doncaster jumps method on file (methods/doncaster/FLAT.md is separate).

LIVE: **national defaults only** (predict/course_method.py ANGLES[("doncaster","JUMPS")] = []). Picks are the same as with no course method. Any course factor needs a reviewer PASS first (owner 19 Nov: reviewer in charge of prediction changes).

## Tested on history (methods.audit, Doncaster jumps, margin-free SP A/E)
Tables: reports/methods/doncaster_JUMPS_rules.md (2019-26, 581 races) and reports/methods/doncaster_JUMPS_rules_since2022.md (359 races). 2019-21 figures are worked out from the two tables (approximate).

| Rule | 2019-26 | 2022-26 | 2019-21 (approx) | Verdict |
|---|---|---|---|---|
| Top recent RPR | 1.16 (630) | 1.05 (391) | ~1.34 | weaker lately; national default (jumps 1.05) already applies |
| Exact-conditions RPR | 0.84 (558) | 0.78 (350) | ~0.95 | candidate caution (over-bet here) |
| Course & distance winner | 0.82 (293) | 0.81 (209) | ~0.85 | candidate caution |
| Age 6+ no win/2nd in last 3 | 1.11 (1,417) | 1.08 (803) | ~1.15 | holds -> no out-of-form penalty here |
| Usual front-runner | 1.07 (486) | 1.10 (303) | ~1.03 | small; candidate |
| Favourites | 0.92 (617) | 0.84 (379) | ~1.05 | flips -> not used |

Tested v SP only, not v our model pick, no forward sample -> nothing proposed for live.

## Change log
- 26 Nov 2026 v1.0: created, national defaults only. Candidates noted for a later shadow test.
