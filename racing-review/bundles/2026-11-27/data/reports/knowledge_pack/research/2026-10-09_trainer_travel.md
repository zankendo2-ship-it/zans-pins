# Trainer travel test (owner 2026-10-09: "pick up on when horses have travelled a good way")

TEST on our UK/IRE results 2018-2026 (Racing Post data). Trainer's base = the middle of the courses they ran at in the year
before (course positions approximate). Price check = margin-free A/E (1.00 = exactly as priced). Script:
reports/research/scripts/trainer_travel_test.py.

| Distance sent | Runners | Win % | A/E 2018-22 | A/E 2023-26 |
|---|---|---|---|---|
| under 100 km | 401,941 | 9.9% | 1.01 | 1.00 |
| 100-200 km | 281,654 | 11.1% | 1.00 | 1.00 |
| 200-300 km | 65,019 | 12.3% | 0.97 | 0.99 |
| 300 km+ | 24,944 | 14.7% | 1.03 | 1.03 |
| 300 km+, under 10/1 | 15,097 | 21.7% | 1.03 | 1.04 |
| 300 km+, 10/1+ | 9,847 | 4.0% | 0.99 | 0.91 |

Finding: horses sent a long way DO win more often, but the price mostly knows it. Only 300 km+ horses priced under 10/1
beat their price, by a small margin (A/E 1.04), in both periods. Long-travelling outsiders do worse than their price.
Still lost money at SP (-11.7% at £1). -> shown on every win pick's Form check (travel km); not used to pick yet.
Trainers who rarely travel far (under 10% of their runs) were no better (A/E 0.99).
