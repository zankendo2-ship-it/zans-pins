# Ffos Las — FLAT (turf) — ZANS method v2.0

Onboarded 2026-09-26 from the owner's Perplexity review PDF (`source/`, 173 pages, reviews FFOS-005 to 009).
Process: methods/README.md. Rule test: `reports/methods/ffos_las_FLAT_rules.md` (2019-26) + split-period
check (2016-21 vs 2022-26, UK/IRE history only).

## 1. Review cards (owner-reported - NOT yet verified)

Our Sporting Life results store has no Ffos Las races for any August 2026 date (a force re-fetch on
26 Sep still returned none), and the Racing Post store stops before August, so these figures are the
chat's own. Verify when the results backfill reaches August.

| Card | Review | Method | Races | Winner picks won | £1 win P/L |
|---|---|---|---|---|---|
| Tue 4 Aug | FFOS-005 | v1.0 -> v1.1 | 7 | 3 | +£9.42 |
| Wed 12 Aug | FFOS-006 | v1.2 | 6 | 3 | +£2.54 |
| Fri 21 Aug | FFOS-007 | v1.3 | 6 | 3 (Safari Dream, Oviedo, Korbut) | +£1.45 |
| Thu 27 Aug | FFOS-008 | v1.4 (HR7 promoted, Value Inversion) | 6 | 2 (Tumishi, Macarone) | -£0.77 |
| Fri 28 Aug | FFOS-009 | v1.5 (Trap 4 promoted) | 6 | 1 | -£4.00 |
| **Total** | | | **31** | **12 (39%)** | **+£8.64** |

## 2. Best spell and slump (owner rule: build around the peak)

- **Peak = 4-12 Aug, v1.0-v1.2**: 6 winners from 13 (+£11.96). Rule set: HR1 trip +-2f, HR2 first-time
  apprentice, HR3 going-conditional weight, HR4 vet flags, HR6 poor C&D run, Trap 1 layoff (>45 days) cap,
  Trap 3 front-runner sprint cap, Guidelines A-M (C&D > finish proof > pace > trip > weight > ratings).
- **Slump = 27-28 Aug, v1.4-v1.5**: 3 winners from 12 (-£4.77). Added after the peak: HR7 promoted to an
  ACTIVE rule with VALUE INVERSION (drop a handicap favourite for a bigger price), Trap 4 keen-3yo veto,
  marathon weight rule, extra place/longshot streams. The chat itself notes "HR7 inversions still missed
  true winners twice" and "Main missed, LS hit" when inversion fired.
- Our national test says the same: opposing the favourite on evidence alone HALVES the strike rate
  (fav still wins ~30%, the alternative ~15%). So v2.0 keeps the peak rules and drops Value Inversion.

## 3. Rule verdicts (Ffos Las history, A/E = wins vs market chance)

| Owner rule | Test | Ffos Las result | Verdict |
|---|---|---|---|
| Gdl H class / RPR | top recent RPR | A/E 1.12, +3% (407) | **KEEP** (angle 1.06) |
| Gdl G exact C&D proof | C&D winner | A/E 1.21 (127); 1.65 / 1.07 | **KEEP** (1.08) |
| Gdl D / temperament | hung in either of last 2 | A/E 0.66, -49% (304); 0.46 / 0.71 | **KEEP** (0.82) - strongest angle |
| Trap 3 front-runner sprint | usual leader at 5-7f | A/E 0.80, -44% (148); 0.57 / 0.92 | **KEEP** (0.90) |
| Trap 1 layoff >45 days | 46-99 days off | A/E 0.77 (333); 0.80 / 0.76 | **KEEP** (0.89) |
| HR1 trip +-2f | never ran within 1f | A/E 0.89, -44% (317) | **SOFT** (0.95) |
| age | 6yo+, no win/2nd in last 3 | A/E 0.73, -60% (243) | **KEEP** (0.87) |
| HR7 handicap fav fragility | handicap fav under 2/1 | A/E 0.92 (175); 0.91 / 0.92 | NOTE - mildly over-bet but still wins 37%: confidence cap only, NEVER value inversion |
| Value Inversion | drop fav for a bigger price | slump cards; national data halves strike rate | **DROPPED** |
| Non-handicap favourites "6/7" | non-hcp fav | 43% win, A/E 0.99 (120) | NOTE - normal, not an edge |
| HR3 top weight on soft (-18%) | 9st7+ / top weight on soft | 0.99 / 0.93 | NOTE (tiny effect) |
| HR3 top weight on good/firm (+12%) | 9st7+ on good / fast | 0.84 / 1.02 | **DROPPED** (no plus) |
| Gdl I draw 1-6 at 5-6f sound ground | stall 1-6 vs 7+ | 1.01 vs 0.95 | NOTE |
| Marathon weight relief (Trap 5) | 1m6f+ hcp under 9st / 10st+ | 0.88 / 0.99 | **DROPPED** |
| slow start | slow away in last 2 | A/E 1.19 | DROPPED (not a negative here) |
| Trap 4 keen 3yo veto | keen in last 2 | 1.03-1.07 | DROPPED |

## 4. ZANS method v2.0 (used for Ffos Las picks from 27 Sep 2026)

1. ZANS joint model (evidence + price) picks the winner; BET only with EVIDENCE AGREES and confidence 8+.
   Handicap favourites under 2/1 are never "inverted" away; the joint model already prices them.
2. Course angles (ANGLES["ffos_las","FLAT"]): top recent RPR 1.06, C&D winner 1.08; cautions: hung 0.82,
   5-7f front-runner 0.90, 46-99 days off 0.89, 6yo+ out of form 0.87, unproven trip 0.95.
3. Cross-course: never-run-on-the-ground penalty unless elite; Exact RPR column (at Ffos Las exact RPR is
   only A/E 0.98, so it is shown, not boosted).
4. Soft ground days (like 27 Sep): the owner's DNA says rain turns it into a stamina test - our data has no
   separate soft-ground edge yet; logged for the evening review.

## Change log
- v2.0 (2026-09-26): rebuilt on the v1.0-v1.2 peak; Value Inversion, marathon weight, Trap 4, HR3 good-ground
  plus and slow-start penalty dropped on the data; hung-horse and front-runner cautions confirmed.
- 2026-09-28 review of Sun 27 Sep (first live card on v2.0, soft ground; results from Racing Post - Sporting Life does not carry Ffos Las): win picks 5/8 (Macarone 3/1, Rhodes Runner 9/4F, Call Time 4/9F, Carthusian 9/4 BET, Wellwhatshappenin 9/4 BET); Silent Force 2nd at 2/7F, Arvana Belle 2nd at 10/11F, Homeland 8th. NO CHANGE (v2.0 confirmed on its first card; single card).
