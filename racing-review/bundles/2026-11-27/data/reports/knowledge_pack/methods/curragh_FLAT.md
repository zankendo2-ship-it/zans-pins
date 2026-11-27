# Curragh — Flat turf — course onboarding review + ZANS method v28.5

Source: owner's `CURRAGH FLAT Review.pdf` (88 pages; `source/`), 5 reviewed cards, AURORA-X v26.0 -> v28.4.
Rule tests: `reports/methods/curragh_FLAT_rules.md` (1,349 Curragh races since 2019). Claimed winners checked.

## 1. Scorecard (£1 win, from the chat ledger)
| Card | Method | Win picks | P/L |
|---|---|---|---|
| 19 Jul (1.1) | v27.0 | 1/8 | -£5.90 |
| **9 Aug (1.2)** | **v27.1** | **4/8** (Ibelieveicanfly, Shakespeare, Sun Goddess + 1) | **+£6.41** |
| 16 Aug (1.3) | v28.0 | 3/8 (Comfort Line, Zarak Pasha, A Boy Named Susie) | +£0.64 |
| 29 Aug (1.4) | v28.2 | 2/6 gradeable | +£1.17 |
| 13 Sep (1.5) | v28.3-28.4 | 3 gradeable | +£1.70 |
| **Total** | | | **+£4.02 on £32 (+12.6%)** |

## 2. Best spell and what was in it
Best = **9-16 Aug (v27.1-v28.0): 7/16**. Active: Favourite-Anchor for non-handicaps/maidens/Group races (3/4 on
9 Aug), Handicap Favourite Fade (0/3 then 0/4 hcap favs), field-reduction gates, improver override (exp.),
high draw at 5-6f in 15+ fields. Later versions mostly added process controls (data verification gates) after
non-runner errors - sensible, no loss of winners.

## 3. Rules v our data
| Rule | Data | Verdict |
|---|---|---|
| Top recent RPR | **A/E 1.23, +2% (1,462)** - the strongest angle at the course | KEEP (x1.10) |
| Exact-conditions RPR | 1.10 (1,157) | KEEP (x1.05) |
| Favourites (any race) | 1.10 (1,449) | NOTE - the win model already weighs price |
| Handicap favourite fade | not directly tested (fav any race 1.10) | UNVERIFIED - shown as caution only |
| Position Race Mandate (reject hold-ups 5-7f) | 1.01 (1,650) | DROPPED (no edge) |
| Usual front-runners | **0.83, -38% (922)** | KEEP as a penalty (x0.92) |
| Lone front-runner | 0.87 (427) | penalty (x0.94) |
| Won last time | 0.94 (1,931) | SOFT penalty (x0.97) |
| Ground specialist | 0.94 (446) | SOFT penalty (x0.96) |
| Slow starters at 5-6f | 1.25 (300) - they do BETTER than priced | NOTE (no penalty) |

## 4. ZANS METHOD v28.5 — CURRAGH — FLAT
WIN PICK: ZANS model x multipliers + all-course lessons. RPR PICK: owner's RPR rule. BET: 8+ and evidence agrees.

## Extra owner cards (uploaded 28 Sep 2026, `source/CURRAGH FLAT REVIEWS 2.pdf`, June 2026)
| Card | Review | Races | Winner picks won | £1 win P/L |
|---|---|---|---|---|
| Fri 26 Jun | 14 | 7 (1 NR) | 4 (5 favourites won on the card) | +£8.63 |
| Sat 27 Jun | 05 | 8 | 3 | -£2.64 |
| **Extra total** | | **15** | **7 (47%)** | **+£5.99** |
Both June cards were favourite-heavy (5 and 4 favourites won); the chat credits the Sharp Trip DNA tag. Consistent with
v28.5 (top RPR 1.23, leaders 0.83) -> NO CHANGE.

## Change log
- v28.5 (2026-09-26, ZANS onboarding): built around the v27.1 peak; data-backed RPR boost; hold-up rejection dropped.
- 2026-09-26 (review of 26 Sep, v28.6): win picks 2/8 (Noble Exhibit, Trean), RPR pick Controlla won, favs 2/8. Three big-field winners came from high draws (Red Evolution 20, Trean 18, Come What May 13) on yielding. Tested /tmp/claude-0/sp/pattern_tests.py (2016-26, split 2016-21 / 2022-26): top third of a 12+ field A/E 1.06 (5,299; 1.09 / 1.04) -> ADDED draw_high:12 1.03; front-runners on yielding/soft A/E 0.64 (385; 0.40 / 0.79) -> ADDED leader@SOFT 0.85 (on top of the course leader 0.92). Excellent Believe (hampered, 3rd) watchlisted.
- 2026-09-28 review of Sun 27 Sep (heavy): win picks 3/7 ran (Soul Love 5/2, Valentino Eclipse 2/5, Curracloe 13/8 won; Hmas Perth NR). Kingdom Of Camelot 4th at 5/6 never tried heavy - one race, flat soft/heavy first-time not penalised nationally (A/E 1.09). NO CHANGE (single card; rules need 30+ runners and both periods).

- NO CHANGE (2026-10-04 review of Sun 4 Oct: win picks 3/8): NO CHANGE to Curragh FLAT v28.5. The winners came where the evidence was strong (maidens and the Listed fillies' race) and the losses were in big soft-ground handicaps and two narrow defeats. The Curragh's soft-ground front-runner caution (0.85) did not bite today because Pirate Anne Bonny was the only front-running winner. No pattern from one card beats the history. Evidence: Curragh flat (owner v28.5): top recent RPR A/E 1.23; usual front-runners 0.83 overall and 0.85 on soft (draw-high rule for 12+ runners at 1.03). Today: 3/8 winners, two picks beaten under half a length / 4 lengths.

- NO CHANGE (2026-10-15 review): win picks 2/8 plus seconds beaten 0.75L and 0.3L. Out-of-sample test of top picks in Irish flat handicaps 16+ runners on soft/heavy: 17 races, 2 won v 2.9 predicted - too few for a rule.

- 2026-10-20 review: NO CHANGE. No change to Curragh FLAT v28.5. Why: We tested whether confident picks lose on soft-type ground at the Curragh, using favourites as the stand-in for 7/10+ picks (TEST). Short favourites (2.50 or less) on exact YIELDING lost in both periods: 4/19, A/E 0.48 (2019-21), and 9/24, 0.89 (2022-26). On SOFT they did not: 1.04 | 1.12. The samples are tiny, and the overlays are price-free, so no favourite rule can be coded. Two-year-old favourites on yielding or softer were weaker in both periods (22/85, 0.86 | 24/91, 0.81), against 1.12 | 1.13 at other Irish courses. But the 2-year-olds having their first try on that ground did fine (1.10 | 1.16), so Maire Rua's profile is not the weak group.
