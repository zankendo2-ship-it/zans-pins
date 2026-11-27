# Free tip of the day - rule replay (TEST, 5 Nov 2026)

Alex 5 Nov: one free bet a day, only when there is value, never "stupid low odds"; reasons + best odds to lock in.

Data: the LOCKED race-day pack of every day 26 Sep-4 Nov (first non-superseded d0_morning folder), 1,525 win picks that ran.
Price = Sky Bet at the race-morning check (d0_morning bookie_terms; before 1 Oct the locked best price). £10 a tip.
Safety = the real slip's rules (betslip._gap: maiden/novice jumps, 90+ days off, unproven trip/going, data gap, no bookmaker
price; drifted 10%+; overnight drift warning). H1 = 26 Sep-15 Oct, H2 = 16 Oct-4 Nov. Value = our chance x Sky price.
Scripts: reports/research/scripts/free_tip_2026-11-05/ (build.py -> rows, sim.py, ew.py, ew2.py).

This is a TEST: the safety rules were partly chosen on these same days, 40 days only.

| Rule (one bet a day) | Tips | Won | Avg price | £10 P/L | H1 | H2 | Longest losing run |
|---|---|---|---|---|---|---|---|
| **ADOPTED: best-value 7/10+ safe single at 2.50+, else double of 2 safe 7/10+ at 2.00+ (combined 4.0+), else none** | 31/40 | 16 (52%) | 3.21 | **+£223.0** | +£114.3 | +£108.7 | 4 |
| single 2.00+ else double | 35 | 21 (60%) | 2.53 | +£180.1 | +£122.4 | +£57.7 | 3 |
| single 3.00+ else double | 30 | 10 (33%) | 5.27 | +£220.4 | +£139.6 | +£80.8 | - |
| double first, else single 2.50+ | 31 | 10 (32%) | 5.66 | +£266.8 | +£195.9 | +£70.8 | 9 |
| same rule, 8/10+ only | 10 | 3 | 4.43 | +£34.3 | +£74.2 | -£40.0 | - |
| one 15.00+ each-way a day, BET NOW alert, Sky 09:30 price + extra place (£5 E/W) | 30 | 1 win, 4 placed | - | -£60.0 | -£55 | -£5 | 26 losing days |
| one evening BET NOW each-way a day at the alert price (top RPR first) | 29 | 1 win, 8 placed | - | +£9.0 | -£25 | +£34 | 21 losing days (-£111 without the best) |

Why not each-way as the free tip: the BET NOW lists make money across ALL alerts (several a day), but ONE a day loses on
21-26 of ~30 days and rests on one winner (Beaumadier 23.00, 20 Oct). A public tip that loses most days does not build trust.
They stay in the paid BET NOW alerts.

Why 2.50 (6/4) and not 2.00: Alex ruled out "stupid low odds"; 2.00+ wins more often (60%) but makes less (+£180) and the
H2 half is weaker. 2.50+ keeps average price ~9/4.

Cross-check: the Specialist thread's own test (/mnt/project-files/agents/tests/2026-11-05_free_tip_rule.md, weaker safety:
drift_warning + data gap only) found 7/10+ at 2.00-3.49 +£137 (both halves) and 2.50+ +£91.50 (+£87.60 | +£3.90); its
always-a-double rule +£6.45. With the slip's full safety rules the 2.50+ single + 4.0 double fallback is stronger in both halves.

LIVE record starts 5 Nov 2026: reports/free_tips/record.md (python -m predict.free_tip --date D --settle).
