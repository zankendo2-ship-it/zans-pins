# Naas FLAT - ZANS v6.1 (from the owner's AURORA-X Naas Flat v5.1, onboarded 10 Oct 2026)

Source: methods/naas/source/NAAS FLATS Review.pdf (71 pages: Review 01 of 4 Jul 2026 -> method v5.0; Review 009 of 23 Aug 2026 on v5.1).

## Cards verified against our results (win selection, £1 win at SP)
| Card | Version | Winners | P/L | Note |
|---|---|---|---|---|
| 4 Jul 2026 | v4.x -> reviewed into v5.0 | 4/8 | +£0.73 | Concorde Landed, Keke, Carry The Flag, Mai Dahlia - all favourites. CHAT ERRORS: said "six of eight" then "5/8"; verified 4/8 (Nouvel Espoir, Florida Bay, Connecteo, Ocean's Breath lost) |
| 23 Aug 2026 | v5.1 | 2/7 | +£3.10 | Maeda Matsu 7/1, Zoar 11/10F; longshot Timeless Tale won 14/1, Chantez 28/1 missed |
Total 6/15, +£3.83. BEST SPELL: 23 Aug v5.1 by profit (+£3.10, a 7/1 winner); 4 Jul by strike rate (4/8, all favourites).
SLUMP: none clear - only two cards. 23 Aug missed three handicaps where the method over-trusted a previous C&D winner
(Dandy Land, Diamond Exchange) and filtered out apprentice-race and low-weight 3yo winners.

## Owner's rules tested on Naas flat 2019-26 (A/E; 2019-21 / 2022-26)
- KEPT top recent RPR 1.16 (727; 1.25 / 1.12) -> x1.06.
- KEPT ground suitability / exact-going specialist 1.27 (248; 1.34 / 1.23) -> x1.05.
- KEPT improver engine: last RPR above previous best 1.06 (1,046; 1.01 / 1.09) -> x1.02.
- KEPT low draw (1-4) on good or firmer 1.09 (1,114; 1.21 / 1.03) -> x1.02.
- KEPT weak jockey (<6%) as a caution 0.91 (2,165; 0.82 / 0.98) -> x0.97.
- REVERSED trip-proof gate: first time at the trip 1.31 (456; 1.43 / 1.23) -> x1.05.
- REVERSED start-risk rejection: slow starters at 5-6f 1.29 (194; 1.42 / 1.23) -> x1.04.
- DROPPED "same track + same distance PROMOTE": C&D winner 0.85 (531; 1.02 / 0.78) - worse lately; it cost 23 Aug
  (Dandy Land, Diamond Exchange). Not penalised either (flips between periods).
- NOT USED (flip): usual front-runner 1.01 (0.76 / 1.12), lone front-runner 1.09 (0.84 / 1.21) - the owner's front-runner
  bias is only supported since 2022; usually prominent 1.06 (1.04 / 1.07) is mild. Re-test at the next monthly rebuild.
- Favourites 1.08 (739) - the favourite stress test is not supported; favourites are never opposed on price alone.
- Apprentice first-time hard rejection: owner already marked REVIEW REQUIRED - dropped (no tested support).
- Full tables: reports/methods/naas_FLAT_rules.md (+ 2022-26 split).

## Change log
- v6.0 (2026-10-10): built around the owner's v5.1 (23 Aug) with only the rules that pass our history; C&D promotion dropped.

- NO CHANGE (2026-10-10 review of Sat 10 Oct): Naas FLAT v6.0 unchanged (top RPR x1.06, unproven trip x1.05, slow starters at 5-6f x1.04, ground specialist x1.05, improver x1.02, low draw x1.02, weak jockey x0.97). Four winners from seven, plus a narrow second, on the method's first day is the best possible start, and the two clear losers were beaten in an 18-runner maiden and a 10-runner handicap with no sign of a broken rule. One card is too few to strengthen any factor, so the method stays exactly as built this morning. Evidence: Naas history behind v6.0: top recent RPR, ground specialist and slow starters at 5-6f all above A/E 1.0 in both periods; C&D promotion dropped (A/E 0.85). Today: picks 4/7, five of seven in the first two.

- CHANGE (2026-10-11 review of Sun 11 Oct): Naas FLAT v6.0 -> v6.1: new angle lone_leader@SOFT x1.05 (the only habitual front-runner in the race, on soft ground). All other rules unchanged. On both Naas cards so far most winners raced up with the pace on soft ground. Naas history from 2019 shows the lone habitual front-runner on soft ground wins 41% more often than its price says, holding in both 2019-21 and 2022-26, while the same horses do worse than their price on good ground. So the rule only applies on soft. Evidence: Naas flat 2019-26 (scripts/naas_soft_pace_check.py): lone front-runner on soft 20/118 won, A/E 1.41 (2019-21 1.20 on 47, 2022-26 1.53 on 71); on good 8/96, A/E 0.68. Usually prominent on soft 1.05 (0.94 / 1.11) - not used.
