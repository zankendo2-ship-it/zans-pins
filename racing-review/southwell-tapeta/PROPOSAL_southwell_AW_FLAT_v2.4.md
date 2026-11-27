# Southwell AW_FLAT method v2.4 (Tapeta only) - PROPOSAL, nothing live changed

Status: TEST. Not adopted. Needs reviewer PASS (and the pre-registered test v our model, two halves) before any factor reaches picks. Today's sealed Southwell picks are untouched.

Data: races on Tapeta only, from 7 Dec 2021 (first Tapeta race, Racing Post 7 Dec 2021). Rule tests v SP: rules_tapeta_since_2021-12-07.md (2,264 races) and rules_tapeta_since_2024-06-01.md (1,298 races, second half). Old mixed test kept for comparison: rules_mixed_since_2019-01-01.md (3,043 races). Rebuilt course knowledge file: southwell_aw_TAPETA_ONLY_course_kb.md (2,282 races to 17 Nov 2026; the old 2019-21 column is empty by design).
Factor convention used by predict/course_method.py: factor = 1 + (A/E - 1) / 2, rounded.

| Rule (kind) | Live factor, basis | Mixed 2019+ A/E | Tapeta A/E (n runners) | Tapeta from Jun 2024 A/E (n) | Proposed |
|---|---|---|---|---|---|
| exact_rpr | x1.05, A/E 1.09 (2,948) | 1.07 | 0.99 (2,370) | 0.98 (1,354) | drop (x1.00) |
| top_rpr | x1.03, A/E 1.06 | 1.06 | 1.06 (2,661) | 1.03 (1,524) | keep x1.03 |
| ground_spec | x1.10, A/E 1.20 (779) | 1.21 | 1.16 (562) | 1.12 (277) | x1.08 |
| lone_leader | x1.06, A/E 1.12 (993) | 1.13 | 1.11 (774) | 0.96 (423) | drop (x1.00): unstable |
| slow_start:6 | x0.94, A/E 0.89 (807) | 0.90 | 0.98 (645) | 1.21 (342) | drop (x1.00) |
| leader | x0.96, A/E 0.93 (2,239) | 0.96 | 0.93 (1,630) | 0.86 (914) | keep x0.96 (data supports lower, not changed) |
| older (age 6+) | x0.98, A/E 0.96 | 0.96 | 0.97 (5,154) | 0.95 (2,773) | keep x0.98 |

Honest reading: the two factors that most changed the picks (exact-RPR boost, slow-start penalty) were carried by Fibresand-era races; on Tapeta alone they are 0.99 and 0.98 and the evidence for them is gone. The lone-leader boost and slow-start result flip between Tapeta periods, so no factor should rest on them. A/E v SP is not the pre-registered test: the model-based two-half test (flat/AW, winners + log-likelihood) must be run before adoption; if it is not better in both halves, keep v2.3 and report.
Method file methods/southwell/AW_FLAT.md and the guide text are owned by the racing-branch session; this folder holds the evidence only.
