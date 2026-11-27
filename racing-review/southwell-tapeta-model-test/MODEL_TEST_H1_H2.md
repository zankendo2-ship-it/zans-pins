# Southwell AW v2.3 v v2.4: model-based two-half test (reply to ChatGPT REVISE, 27 Nov)

TEST ONLY. Nothing here changes any pick, slip or rule. Nine Southwell picks stay on HOLD.

## Set-up
- Scored: Southwell AW_FLAT races from the first Tapeta race (7 Dec 2021) to 26 Nov 2026. 2,264 races (2,282 candidates - 14 with fewer than 4 runners - 4 dead heats = 2,264). H1 = 7 Dec 2021 to 31 May 2024 (966 races); H2 = 1 Jun 2024 onward (1,298 races).
- Models: joint (form features + log market) and form-only, fitted on FLAT-family races dated 2019-01-01 to before 2021-12-07 only (no look-ahead into the test period). v2.3 and v2.4 = base model chance times the Southwell factors (v2.3: exact_rpr 1.05, top_rpr 1.03, ground_spec 1.10, lone_leader 1.06, slow_start 0.94, leader 0.96, older 0.98; v2.4: exact_rpr 1.00, top_rpr 1.03, ground_spec 1.08, lone_leader 1.00, slow_start 1.00, leader 0.96, older 0.98). Rule flags come from methods.audit.flags_for_race (the audit's version of the rules, not course_method's live code).
- Intervals: 95% bootstrap over races, paired (v2.4 minus v2.3).
- Four modes: asis (date-only order, all history), strict_only (a day's races all scored before any is added), surface_only (1,045 pre-Tapeta Southwell AW races dropped from history, jockey records, standards and training), strict_surface (both).

## Results (joint model; log loss lower = better)
| Mode | Half | Races | Top-winner hit v2.3 | v2.4 | Log loss v2.3 | v2.4 | v2.4 - v2.3 log loss [95%] | v2.4 - v2.3 hit [95%] |
|---|---|---|---|---|---|---|---|---|
| strict_surface | H1 | 966 | 0.3261 | 0.3230 | 1.8421 | 1.8433 | +0.00116 [-0.0003, +0.0025] | -0.0031 [-0.0083, +0.0021] |
| strict_surface | H2 | 1,298 | 0.3251 | 0.3282 | 1.7778 | 1.7769 | -0.00088 [-0.0021, +0.0003] | +0.0031 [-0.0023, +0.0092] |
| strict_surface | ALL | 2,264 | 0.3255 | 0.3260 | 1.8053 | 1.8052 | -0.00001 [-0.0009, +0.0009] | +0.0004 [-0.0035, +0.0044] |
| asis | H1 | 966 | 0.3313 | 0.3261 | 1.8419 | 1.8429 | +0.00104 [-0.0004, +0.0024] | -0.0052 [-0.0114, +0.0010] |
| asis | H2 | 1,298 | 0.3282 | 0.3282 | 1.7777 | 1.7768 | -0.00087 [-0.0020, +0.0004] | 0.0000 [-0.0046, +0.0046] |

Market baseline (SP, margin-free): H1 hit 0.3168, log loss 1.8491; H2 hit 0.3459, log loss 1.7845. Base model without Southwell factors: strict_surface H1 0.3251 / 1.8439, H2 0.3297 / 1.7771. Full per-mode JSON (including form-only model): mt_*.json in this folder.

## Findings
1. v2.4 is not shown better or worse than v2.3 in either half. Every interval spans zero. The signs flip between halves (H1 slightly worse, H2 slightly better), so the "not worse anywhere" rule is NOT met. v2.3 stays; v2.4 stays a proposal.
2. Both versions are within about 0.002 log loss of the plain base model in both halves: the Southwell-specific factors add almost nothing measurable on 2,264 races. In H2 both sit slightly behind the market on top-winner hit rate (0.325-0.328 v 0.346).
3. Surface-aware history changes the numbers slightly (H1 base hit 0.3282 -> 0.3251) but not the v2.3 v v2.4 verdict.
4. Strict date ordering gave results identical to date-only ordering at four decimals (asis = strict_only, surface_only = strict_surface). Same-day leakage exists in the code (methods.audit.load() and predict.features.walk() order by date only and update after each race), but it did not change this test. I cannot tell from this whether it matters for other courses.
5. Caveats: speed standards use fit_before 2026-01-01 (same for both versions, so the paired difference is unaffected); flags are the audit's approximations; only the Southwell factors are overlaid.

## Exclusions
1,045 pre-Tapeta Southwell AW races dropped from history/training in the surface modes. Scored set 2,282 candidates - 14 (under 4 runners) - 4 (dead heats) = 2,264; 0 unmatched.

## Code (full files, this folder's code/)
model_test.py (harness), course_kb_data.py and course_kb_rules.py (full surface_since-aware copies; the earlier patch is surface_since_filter.patch). Run from a worktree holding history/ and data/ (scripts/fetch_history.sh): `python3 model_test.py --mode strict_surface --out result.json`.
