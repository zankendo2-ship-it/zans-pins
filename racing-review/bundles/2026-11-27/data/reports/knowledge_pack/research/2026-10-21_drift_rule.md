# Drift rule (7/10+ picks kept off the slip when the price drifts 15%+) - helper research, 21 Oct 2026 (TEST)

Live locked 7/10+ picks, first locked d0 pack each day, 26 Sep - 20 Oct 2026: 332 picks. £10 win at the 09:30 price.
Figures re-checked by the main session from /tmp/claude-0/improve/helper_drift/live_rows.json.

## Overnight move (day-before price -> 09:30 price)
| Move | Won/run | £10 at 09:30 | 26 Sep-7 Oct | 8-20 Oct |
|---|---|---|---|---|
| shortened <0.90 | 52/101 | +34.90 | 21/33 +94.80 | 31/68 -59.90 |
| 0.90-1.00 | 50/76 | +219.30 | 20/29 +101.50 | 30/47 +117.80 |
| 1.00-1.15 | 27/57 | -43.00 | 14/24 +26.00 | 13/33 -69.00 |
| drifted 1.15-1.33 | 11/21 | +30.50 | 1/4 -15.00 | 10/17 +45.50 |
| 1.33+ | none | | | |

## First price -> 09:30 ('move' field, what betslip DRIFT_MIN reads)
- 1.15+: 2/13, -£78.70 (1/6 then 1/7) - losing in both halves.

## History stand-in (on-course first show -> SP, Sporting Life Jul-Sep 2026, model chance 0.40+, TEST)
- drifted 1.15-1.33: 20/38, A/E 1.06 v steady 0.93 (445). Not an overnight move, so only a stand-in.

## Verdict
- 'Move' drift (first price -> 09:30) 15%+: keep the rule (2/13, both halves losing).
- Overnight drift 15-33%: did not hurt in the second half (10/17) but lost in the first (1/4); samples tiny -> NO change,
  re-test at 40 picks. Not put to the owner as a proposal (does not hold in both periods).
Scripts: /tmp/claude-0/improve/helper_drift/live_drift.py, hist_drift.py (outputs .txt alongside).
