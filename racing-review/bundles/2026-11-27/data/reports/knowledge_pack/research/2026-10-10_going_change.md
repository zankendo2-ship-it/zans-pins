# Does the ground changing on the day help horses proven on the new ground? (owner 2026-10-10)

TEST on our UK/IRE turf results 2018-2026 (Racing Post data). For every meeting, the going of each race is compared with the
first race of the day: a full step FIRMER (ground dried out) or SOFTER (rain) later in the afternoon, else SAME. Horses with
3+ runs are split by their record on the new ground. Price check = margin-free A/E against the SP (1.00 = exactly as priced).
Script: reports/research/scripts/going_change_test.py.

| Ground during the meeting | Horse's record on the new ground | Runners | Win % | A/E | 2018-22 | 2023-26 |
|---|---|---|---|---|---|---|
| Dried out (firmer) | WON on it before | 5,679 | 12.7% | **1.06** | 1.06 | 1.05 |
| Dried out (firmer) | ran on it, never won | 5,729 | 9.1% | **0.93** | 0.90 | 0.96 |
| Dried out (firmer) | never run on it | 1,546 | 12.8% | 1.02 | 1.06 | 0.97 |
| Got softer (rain) | WON on it before | 7,724 | 11.8% | 1.02 | 1.04 | 0.99 |
| Got softer (rain) | ran on it, never won | 11,662 | 10.0% | 1.02 | 1.02 | 1.02 |
| Got softer (rain) | never run on it | 3,870 | 11.5% | 1.05 | 0.99 | 1.13 |
| No change | WON on it before | 223,732 | 12.5% | 1.01 | 1.01 | 1.00 |

Finding: when the ground DRIES OUT, horses that have won on the quicker ground beat their price by about 6% (both periods) and
horses that have run on it without winning do worse (0.93). When it gets SOFTER there is no reliable edge - the market copes.
Even the 1.06 group still loses at SP (-12.7% at £1) - it moves the picks, it is not a bet on its own.
Limit: this uses the official going during the meeting, not a weather forecast; our weather check is a forecast estimate.

Used from 11 Oct: predict/course_method - when the morning weather check says a turf course MAY DRY OUT, won-on-quicker-ground
x1.04, ran-on-it-never-won x0.96 (set softer than the test numbers). Rain: no change.
