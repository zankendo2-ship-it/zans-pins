# Speed figures + pace map — build and backtest

Standards and class pars fitted on races before **2025-04-01**; every race from then on (20,489 races) is rated from each runner's EARLIER runs only.

- Standard times: **1,059** course/track + discipline + distance combinations (10+ timed races each).
- Going allowances worked out for **14,866** meetings.

## 1. Do our figures agree with Racing Post's? (same runs, test period)

- vs Topspeed (RP's own time figure): correlation **0.85** over 113,508 runs
- vs RPR (RP's form rating): correlation **0.82** over 117,269 runs

## 2. Top-rated horse (best of last 3 runs within a year) — test period

| Rating | Races | Top-rated won | A/E vs SP |
|---|---|---|---|
| Our speed figure (all) | 11,187 | 18.0% | 1.02 |
| RPR (all) | 13,224 | 20.2% | 1.03 |
| Topspeed (all) | 13,322 | 18.7% | 1.01 |
| Speed + RPR average (all) | 11,370 | 19.2% | 1.02 |
| Our speed figure (flat) | 8,733 | 17.7% | 1.01 |
| RPR (flat) | 8,476 | 19.9% | 1.03 |
| Topspeed (flat) | 8,762 | 18.2% | 1.01 |
| Speed + RPR average (flat) | 8,885 | 19.2% | 1.01 |
| Our speed figure (jumps) | 2,454 | 19.0% | 1.06 |
| RPR (jumps) | 4,748 | 20.8% | 1.03 |
| Topspeed (jumps) | 4,560 | 19.5% | 1.02 |
| Speed + RPR average (jumps) | 2,485 | 19.5% | 1.03 |

A/E = winners / chances implied by the starting price with the bookmaker margin removed: 1.00 = exactly as the market expected; above 1 = the rating finds winners the market underrates.

## 3. Pace map — does the SUITS / AGAINST call hold up? (test period)

| Code | Pace map says | Runners | Won | A/E vs SP |
|---|---|---|---|---|
| flat | SUITS | 25,189 | 11.7% | 1.01 |
| flat | NEUTRAL | 57,837 | 10.1% | 1.00 |
| flat | AGAINST | 9,031 | 9.5% | 0.99 |
| jumps | SUITS | 14,302 | 12.0% | 1.03 |
| jumps | NEUTRAL | 34,874 | 10.7% | 1.00 |
| jumps | AGAINST | 7,926 | 8.9% | 0.94 |

### Every running style in every projected pace

| Code | Projected pace | Role | Runners | Won | A/E vs SP |
|---|---|---|---|---|---|
| flat | EVEN | HOLD_UP | 3,041 | 9.2% | 1.03 |
| flat | EVEN | LEADER | 2,760 | 11.2% | 0.99 |
| flat | EVEN | MIDFIELD | 1,093 | 8.1% | 0.87 |
| flat | EVEN | PROMINENT | 6,592 | 10.1% | 1.03 |
| flat | LONE_LEADER | HOLD_UP | 9,031 | 9.5% | 0.99 |
| flat | LONE_LEADER | LEADER | 3,545 | 11.7% | 0.97 |
| flat | LONE_LEADER | MIDFIELD | 3,249 | 9.0% | 0.94 |
| flat | LONE_LEADER | PROMINENT | 16,927 | 11.0% | 1.02 |
| flat | SLOW | HOLD_UP | 12,808 | 10.3% | 1.01 |
| flat | SLOW | MIDFIELD | 5,151 | 9.4% | 0.92 |
| flat | SLOW | PROMINENT | 21,644 | 11.7% | 1.02 |
| flat | STRONG | HOLD_UP | 1,173 | 7.7% | 1.03 |
| flat | STRONG | LEADER | 1,813 | 9.4% | 1.01 |
| flat | STRONG | MIDFIELD | 412 | 6.8% | 0.86 |
| flat | STRONG | PROMINENT | 2,818 | 8.0% | 0.98 |
| jumps | EVEN | HOLD_UP | 2,073 | 9.2% | 1.03 |
| jumps | EVEN | LEADER | 1,988 | 13.3% | 1.02 |
| jumps | EVEN | MIDFIELD | 875 | 9.1% | 1.13 |
| jumps | EVEN | PROMINENT | 4,279 | 9.9% | 0.95 |
| jumps | LONE_LEADER | HOLD_UP | 5,088 | 10.4% | 1.09 |
| jumps | LONE_LEADER | LEADER | 2,192 | 14.0% | 0.98 |
| jumps | LONE_LEADER | MIDFIELD | 2,189 | 9.0% | 0.96 |
| jumps | LONE_LEADER | PROMINENT | 9,337 | 11.5% | 0.98 |
| jumps | SLOW | HOLD_UP | 7,926 | 8.9% | 0.94 |
| jumps | SLOW | MIDFIELD | 3,975 | 10.0% | 1.04 |
| jumps | SLOW | PROMINENT | 13,261 | 12.3% | 1.02 |
| jumps | STRONG | HOLD_UP | 731 | 8.9% | 1.14 |
| jumps | STRONG | LEADER | 1,203 | 10.5% | 0.97 |
| jumps | STRONG | MIDFIELD | 310 | 8.4% | 1.15 |
| jumps | STRONG | PROMINENT | 1,675 | 8.3% | 0.98 |
