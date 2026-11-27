# Newbury - Flat (turf) - ZANS course knowledge base

Built 2026-10-19. UK and Ireland racing only. Course id `newbury`, code FLAT. Our results history: 2019-04-12 to 2026-09-19 (954 races; split 2019-21 / 2022-26). Going = the exact official description at the time of the race ('X, Y in places' counts as X). Rows with 20-59 races are LOW, 60-149 MEDIUM, 150+ HIGH; under 20 races only the count is shown. Every row also shows the figure for 2019-21 and 2022-26 separately (n = races or runners in that period).

Contents: 1 Course profile - 2 Guide facts - 3 Sample sizes - 4 Tables a-k - 5 ZANS method and rule tests - 6 Related research

## 1. Course profile

From our hand-written profile (`config/course_profiles/newbury.json`, our own words), kept to what applies to flat (turf):

- **Direction:** Left-handed
- **Character:** Galloping and among the fairest tracks in Britain
- **Straight mile:** Undulating; used for races such as the Lockinge
- **Round mile:** Starts in a chute, one turn after about 3f, then a 5f straight
- **Surface:** Turf

**Layout**
- A wide, galloping, left-handed course with an undulating straight mile; the home straight runs almost exactly east to west.
- Races from nine to thirteen furlongs start on the back straight; the round mile starts in a chute and makes one turn into a five-furlong straight.

**Tactics**
- Suits big, long-striding horses, especially when rain makes it testing.
- Many winners come down the middle of the straight course; the stands' rail can be favoured depending on field size and stall position.
- Only the round mile start is notably draw-sensitive.

**Ground**
- Soft ground makes Newbury a stiff test that suits long-striding stayers.

- Season: flat from spring to autumn, jumps in winter

- **ZANS stiffness indicator** (our standard times v the median UK/IRE track, same trips): Flat: +0.1% against the median UK/IRE track over the same 9 trip(s)

## 2. Guide facts

> Third-party quotes from a public course guide (source below). Research only: rewrite in your own words for customer guides.

Source: https://www.horseracingbettingsites.co.uk/racecourses/newbury/

- **Track direction** (HIGH): LEFT_HANDED
- **Layout** (SOURCE_BACKED): 
  - "The home straight runs almost exactly east to west."
  - "Flat Course Newbury’s Flat racing course is left-handed and definitely galloping in nature."
  - "Both the straight mile and the round course are thought to be ideal for bigger horses with a longer stride pattern."
  - "In terms of draw or track position bias, many winners at Newbury have come straight down the middle of the straight course."
  - "Races from nine furlongs to 13 furlongs begin on the back straight and are not draw dependent, with the only start punters should be aware of from a draw perspective being the round mile (1 mile, 7 yards)."
  - "Riders’ feedback is that the track is large and certainly galloping, though their words suggest that punters should be wary when the ground gets soft."
  - "Not only can the track prove to be testing, but it can be even slower down the back straight as the nearby heavy woodland affects the racing ground underneath meaning the mid-part of a race can tire some horses out early."
- **Distance configuration** (SOURCE_BACKED): It starts up the chute with the runners taking one turn after just three furlongs into the long, five-furlong straight.
- **Going** (SOURCE_BACKED): 
  - "Such types have an even bigger advantage when the rain comes here as the track can become very testing and takes some getting."
  - "Riders’ feedback is that the track is large and certainly galloping, though their words suggest that punters should be wary when the ground gets soft."
  - "Not only can the track prove to be testing, but it can be even slower down the back straight as the nearby heavy woodland affects the racing ground underneath meaning the mid-part of a race can tire some horses out early."
- **Draw** (NARRATIVE_ONLY_NOT_NUMERIC): 
  - "In terms of draw or track position bias, many winners at Newbury have come straight down the middle of the straight course."
  - "Sometimes the advantage is on the stands side rail, but that may depend on field size and the position of the stalls."
- **Distances described** (SOURCE_BACKED): 5f, 1m, 1m1f, 1m5f

**Per-distance guide quotes:**
- 5f: "It starts up the chute with the runners taking one turn after just three furlongs into the long, five-furlong straight."
- 1m: "Races from nine furlongs to 13 furlongs begin on the back straight and are not draw dependent, with the only start punters should be aware of from a draw perspective being the round mile (1 mile, 7 yards)."
- 1m1f: "Races from nine furlongs to 13 furlongs begin on the back straight and are not draw dependent, with the only start punters should be aware of from a draw perspective being the round mile (1 mile, 7 yards)."
- 1m5f: "Races from nine furlongs to 13 furlongs begin on the back straight and are not draw dependent, with the only start punters should be aware of from a draw perspective being the round mile (1 mile, 7 yards)."

## 3. Sample sizes - races by trip and going

| Trip | Good to Firm | Good | Good to Soft | Soft | Heavy | All goings |
|---|---|---|---|---|---|---|
| 5f | 18 | 17 | 8 | 5 | 2 | 50 |
| 6f | 62 | 70 | 31 | 11 | 10 | 184 |
| 6½f | 8 | 4 | 4 | 4 | 4 | 24 |
| 7f | 59 | 83 | 31 | 35 | 15 | 223 |
| 1m | 29 | 51 | 22 | 16 | 11 | 129 |
| 1m1f |  |  | 1 | 2 |  | 3 |
| 1m2f | 46 | 66 | 21 | 20 | 10 | 163 |
| 1m3f | 7 | 10 | 4 | 2 |  | 23 |
| 1m4f | 23 | 36 | 15 | 14 | 7 | 95 |
| 1m5½f | 11 | 6 | 7 | 3 | 5 | 32 |
| 2m | 6 |  |  | 3 | 4 | 13 |
| 2m½f | 6 | 5 | 2 | 1 |  | 14 |
| 2m2f |  |  |  | 1 |  | 1 |
| **All trips** | 275 | 348 | 146 | 117 | 68 | 954 |
| of which 2019-21 | 52 | 107 | 73 | 51 | 31 | 314 |
| of which 2022-26 | 223 | 241 | 73 | 66 | 37 | 640 |

## 4. Tables by going and by trip

### a) Draw

**a) Draw by trip and going (stall thirds of the runners' draw order; PRB 0.50 = average; IV = share of winners / share of runners; A/E = winners / margin-free SP chances, 1.00 = as priced)** - counts every runner in races where all runners had a draw and 6+ ran; races 2019-04-12 to 2026-09-19 (954 races; split 2019-21 / 2022-26).
| Trip | Going | Races | Third | Runners | Win % | PRB | IV | A/E | A/E 2019-21 | A/E 2022-26 | Level |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 5f | All goings | 48 | Low | 159 | 6.9% | 0.50 | 0.77 | 0.80 | 0.93 (n=16) | 0.73 (n=32) | LOW |
| 5f | All goings | 48 | Middle | 180 | 10.0% | 0.56 | 1.11 | 1.14 | 1.11 (n=16) | 1.15 (n=32) | LOW |
| 5f | All goings | 48 | High | 193 | 9.8% | 0.44 | 1.09 | 1.04 | 0.95 (n=16) | 1.08 (n=32) | LOW |
| 5f | Good to Firm | 18 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 5f | Good | 17 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 5f | Good to Soft | 8 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 5f | Soft | 4 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 5f | Heavy | 1 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 6f | All goings | 178 | Low | 580 | 11.0% | 0.53 | 1.18 | 1.13 | 1.19 (n=53) | 1.10 (n=125) | HIGH |
| 6f | All goings | 178 | Middle | 636 | 9.9% | 0.51 | 1.06 | 1.05 | 1.11 (n=53) | 1.02 (n=125) | HIGH |
| 6f | All goings | 178 | High | 693 | 7.4% | 0.47 | 0.79 | 0.84 | 0.74 (n=53) | 0.88 (n=125) | HIGH |
| 6f | Good to Firm | 60 | Low | 185 | 10.8% | 0.54 | 1.10 | 0.99 | 0.98 (n=12) | 0.99 (n=48) | MEDIUM |
| 6f | Good to Firm | 60 | Middle | 201 | 10.4% | 0.48 | 1.06 | 1.07 | 0.78 (n=12) | 1.14 (n=48) | MEDIUM |
| 6f | Good to Firm | 60 | High | 223 | 8.5% | 0.48 | 0.86 | 0.94 | 1.24 (n=12) | 0.87 (n=48) | MEDIUM |
| 6f | Good | 69 | Low | 237 | 12.7% | 0.56 | 1.43 | 1.37 | 1.49 (n=17) | 1.33 (n=52) | MEDIUM |
| 6f | Good | 69 | Middle | 262 | 8.0% | 0.50 | 0.90 | 0.85 | 0.82 (n=17) | 0.87 (n=52) | MEDIUM |
| 6f | Good | 69 | High | 280 | 6.4% | 0.45 | 0.73 | 0.80 | 0.73 (n=17) | 0.82 (n=52) | MEDIUM |
| 6f | Good to Soft | 30 | Low | 98 | 6.1% | 0.41 | 0.66 | 0.72 | 0.91 (n=18) | 0.50 (n=12) | LOW |
| 6f | Good to Soft | 30 | Middle | 107 | 12.1% | 0.54 | 1.31 | 1.23 | 1.53 (n=18) | 0.75 (n=12) | LOW |
| 6f | Good to Soft | 30 | High | 118 | 9.3% | 0.54 | 1.00 | 0.99 | 0.56 (n=18) | 1.76 (n=12) | LOW |
| 6f | Soft | 10 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 6f | Heavy | 9 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 6½f | All goings | 24 | Low | 78 | 10.3% | 0.51 | 1.12 | 1.04 | 1.07 (n=5) | 1.03 (n=19) | LOW |
| 6½f | All goings | 24 | Middle | 86 | 10.5% | 0.52 | 1.14 | 1.06 | 0.62 (n=5) | 1.16 (n=19) | LOW |
| 6½f | All goings | 24 | High | 97 | 7.2% | 0.47 | 0.78 | 0.89 | 1.33 (n=5) | 0.79 (n=19) | LOW |
| 6½f | Good to Firm | 8 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 6½f | Good | 4 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 6½f | Good to Soft | 4 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 6½f | Soft | 4 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 6½f | Heavy | 4 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 7f | All goings | 209 | Low | 647 | 9.7% | 0.52 | 0.99 | 0.95 | 0.98 (n=72) | 0.94 (n=137) | HIGH |
| 7f | All goings | 209 | Middle | 708 | 11.2% | 0.51 | 1.14 | 1.11 | 1.10 (n=72) | 1.11 (n=137) | HIGH |
| 7f | All goings | 209 | High | 786 | 8.7% | 0.48 | 0.88 | 0.95 | 0.92 (n=72) | 0.97 (n=137) | HIGH |
| 7f | Good to Firm | 53 | Low | 155 | 11.0% | 0.51 | 1.05 | 0.99 | 1.08 (n=8) | 0.98 (n=45) | LOW |
| 7f | Good to Firm | 53 | Middle | 167 | 10.8% | 0.51 | 1.04 | 0.95 | 0.72 (n=8) | 0.99 (n=45) | LOW |
| 7f | Good to Firm | 53 | High | 187 | 9.6% | 0.48 | 0.92 | 1.06 | 1.19 (n=8) | 1.03 (n=45) | LOW |
| 7f | Good | 81 | Low | 269 | 7.8% | 0.50 | 0.85 | 0.81 | 0.94 (n=32) | 0.73 (n=49) | MEDIUM |
| 7f | Good | 81 | Middle | 292 | 10.6% | 0.50 | 1.16 | 1.14 | 1.12 (n=32) | 1.16 (n=49) | MEDIUM |
| 7f | Good | 81 | High | 323 | 9.0% | 0.50 | 0.98 | 1.04 | 0.93 (n=32) | 1.11 (n=49) | MEDIUM |
| 7f | Good to Soft | 29 | Low | 90 | 8.9% | 0.49 | 0.88 | 0.93 | 1.05 (n=13) | 0.83 (n=16) | LOW |
| 7f | Good to Soft | 29 | Middle | 100 | 13.0% | 0.52 | 1.29 | 1.18 | 1.01 (n=13) | 1.32 (n=16) | LOW |
| 7f | Good to Soft | 29 | High | 107 | 8.4% | 0.49 | 0.83 | 0.96 | 0.94 (n=13) | 0.97 (n=16) | LOW |
| 7f | Soft | 31 | Low | 89 | 10.1% | 0.54 | 1.00 | 1.00 | 0.73 (n=14) | 1.22 (n=17) | LOW |
| 7f | Soft | 31 | Middle | 102 | 11.8% | 0.53 | 1.16 | 1.18 | 1.39 (n=14) | 1.07 (n=17) | LOW |
| 7f | Soft | 31 | High | 115 | 8.7% | 0.45 | 0.86 | 0.85 | 0.96 (n=14) | 0.72 (n=17) | LOW |
| 7f | Heavy | 15 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 1m | All goings | 120 | Low | 409 | 9.8% | 0.54 | 1.09 | 0.98 | 0.74 (n=44) | 1.12 (n=76) | MEDIUM |
| 1m | All goings | 120 | Middle | 442 | 8.1% | 0.49 | 0.91 | 0.91 | 1.12 (n=44) | 0.80 (n=76) | MEDIUM |
| 1m | All goings | 120 | High | 485 | 9.1% | 0.48 | 1.01 | 1.10 | 1.14 (n=44) | 1.08 (n=76) | MEDIUM |
| 1m | Good to Firm | 23 | Low | 69 | 8.7% | 0.51 | 0.87 | 0.80 | 0.53 (n=6) | 0.90 (n=17) | LOW |
| 1m | Good to Firm | 23 | Middle | 76 | 10.5% | 0.49 | 1.05 | 1.02 | 1.51 (n=6) | 0.85 (n=17) | LOW |
| 1m | Good to Firm | 23 | High | 84 | 10.7% | 0.50 | 1.07 | 1.17 | 0.94 (n=6) | 1.26 (n=17) | LOW |
| 1m | Good | 49 | Low | 183 | 9.8% | 0.54 | 1.20 | 1.04 | 0.66 (n=13) | 1.18 (n=36) | LOW |
| 1m | Good | 49 | Middle | 199 | 7.5% | 0.49 | 0.92 | 0.93 | 1.35 (n=13) | 0.77 (n=36) | LOW |
| 1m | Good | 49 | High | 216 | 7.4% | 0.47 | 0.90 | 1.02 | 1.00 (n=13) | 1.03 (n=36) | LOW |
| 1m | Good to Soft | 22 | Low | 76 | 11.8% | 0.59 | 1.33 | 1.09 | 1.00 (n=13) | 1.23 (n=9) | LOW |
| 1m | Good to Soft | 22 | Middle | 81 | 8.6% | 0.48 | 0.97 | 1.14 | 1.62 (n=13) | 0.41 (n=9) | LOW |
| 1m | Good to Soft | 22 | High | 90 | 6.7% | 0.44 | 0.75 | 0.79 | 0.47 (n=13) | 1.22 (n=9) | LOW |
| 1m | Soft | 15 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 1m | Heavy | 11 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 1m1f | All goings | 3 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 1m1f | Good to Soft | 1 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 1m1f | Soft | 2 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 1m2f | All goings | 147 | Low | 452 | 11.9% | 0.53 | 1.22 | 1.14 | 0.87 (n=49) | 1.27 (n=98) | MEDIUM |
| 1m2f | All goings | 147 | Middle | 509 | 11.0% | 0.53 | 1.12 | 1.07 | 1.14 (n=49) | 1.04 (n=98) | MEDIUM |
| 1m2f | All goings | 147 | High | 551 | 6.9% | 0.45 | 0.70 | 0.80 | 0.98 (n=49) | 0.69 (n=98) | MEDIUM |
| 1m2f | Good to Firm | 35 | Low | 90 | 16.7% | 0.56 | 1.49 | 1.34 | 1.15 (n=12) | 1.43 (n=23) | LOW |
| 1m2f | Good to Firm | 35 | Middle | 106 | 10.4% | 0.51 | 0.93 | 0.81 | 0.87 (n=12) | 0.78 (n=23) | LOW |
| 1m2f | Good to Firm | 35 | High | 117 | 7.7% | 0.45 | 0.69 | 0.88 | 1.02 (n=12) | 0.79 (n=23) | LOW |
| 1m2f | Good | 64 | Low | 215 | 11.6% | 0.51 | 1.28 | 1.24 | 1.08 (n=16) | 1.28 (n=48) | MEDIUM |
| 1m2f | Good | 64 | Middle | 243 | 9.5% | 0.53 | 1.05 | 0.99 | 0.86 (n=16) | 1.03 (n=48) | MEDIUM |
| 1m2f | Good | 64 | High | 260 | 6.5% | 0.46 | 0.72 | 0.83 | 1.08 (n=16) | 0.74 (n=48) | MEDIUM |
| 1m2f | Good to Soft | 20 | Low | 66 | 7.6% | 0.53 | 0.81 | 0.78 | 0.44 (n=7) | 0.96 (n=13) | LOW |
| 1m2f | Good to Soft | 20 | Middle | 71 | 16.9% | 0.56 | 1.80 | 1.84 | 2.05 (n=7) | 1.72 (n=13) | LOW |
| 1m2f | Good to Soft | 20 | High | 76 | 3.9% | 0.41 | 0.42 | 0.42 | 0.44 (n=7) | 0.42 (n=13) | LOW |
| 1m2f | Soft | 18 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 1m2f | Heavy | 10 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 1m3f | All goings | 18 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 1m3f | Good to Firm | 4 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 1m3f | Good | 8 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 1m3f | Good to Soft | 4 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 1m3f | Soft | 2 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 1m4f | All goings | 82 | Low | 229 | 7.9% | 0.51 | 0.73 | 0.77 | 0.79 (n=28) | 0.76 (n=54) | MEDIUM |
| 1m4f | All goings | 82 | Middle | 247 | 13.4% | 0.50 | 1.24 | 1.24 | 1.34 (n=28) | 1.19 (n=54) | MEDIUM |
| 1m4f | All goings | 82 | High | 283 | 11.0% | 0.49 | 1.01 | 0.97 | 0.89 (n=28) | 1.01 (n=54) | MEDIUM |
| 1m4f | Good to Firm | 18 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 1m4f | Good | 31 | Low | 91 | 11.0% | 0.53 | 1.05 | 1.07 | 1.07 (n=11) | 1.08 (n=20) | LOW |
| 1m4f | Good | 31 | Middle | 95 | 12.6% | 0.50 | 1.20 | 1.20 | 1.27 (n=11) | 1.17 (n=20) | LOW |
| 1m4f | Good | 31 | High | 109 | 8.3% | 0.47 | 0.79 | 0.77 | 0.73 (n=11) | 0.79 (n=20) | LOW |
| 1m4f | Good to Soft | 13 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 1m4f | Soft | 13 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 1m4f | Heavy | 7 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 1m5½f | All goings | 24 | Low | 59 | 8.5% | 0.47 | 0.68 | 0.73 | 0.00 (n=9) | 1.02 (n=15) | LOW |
| 1m5½f | All goings | 24 | Middle | 66 | 16.7% | 0.50 | 1.34 | 1.49 | 1.94 (n=9) | 1.24 (n=15) | LOW |
| 1m5½f | All goings | 24 | High | 76 | 11.8% | 0.52 | 0.95 | 0.93 | 1.13 (n=9) | 0.76 (n=15) | LOW |
| 1m5½f | Good to Firm | 5 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 1m5½f | Good | 6 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 1m5½f | Good to Soft | 7 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 1m5½f | Soft | 2 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 1m5½f | Heavy | 4 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 2m | All goings | 9 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 2m | Good to Firm | 2 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 2m | Soft | 3 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 2m | Heavy | 4 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 2m½f | All goings | 13 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 2m½f | Good to Firm | 5 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 2m½f | Good | 5 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 2m½f | Good to Soft | 2 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 2m½f | Soft | 1 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 2m2f | All goings | 1 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 2m2f | Soft | 1 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |

**a) Draw by trip and field size (all goings)** - counts the same runners, by number of runners; races 2019-04-12 to 2026-09-19 (954 races; split 2019-21 / 2022-26).
| Trip | Field | Races | Third | Runners | Win % | PRB | IV | A/E | A/E 2019-21 | A/E 2022-26 | Level |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 5f | 6-9 | 25 | Low | 57 | 12.3% | 0.48 | 0.98 | 1.05 | 0.74 (n=11) | 1.27 (n=14) | LOW |
| 5f | 6-9 | 25 | Middle | 69 | 11.6% | 0.57 | 0.92 | 0.88 | 1.25 (n=11) | 0.59 (n=14) | LOW |
| 5f | 6-9 | 25 | High | 73 | 13.7% | 0.45 | 1.09 | 1.08 | 0.93 (n=11) | 1.20 (n=14) | LOW |
| 5f | 10-13 | 15 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 5f | 14+ | 8 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 6f | 6-9 | 64 | Low | 150 | 16.0% | 0.51 | 1.25 | 1.14 | 1.42 (n=23) | 1.01 (n=41) | MEDIUM |
| 6f | 6-9 | 64 | Middle | 169 | 13.0% | 0.50 | 1.02 | 1.04 | 0.66 (n=23) | 1.25 (n=41) | MEDIUM |
| 6f | 6-9 | 64 | High | 182 | 9.9% | 0.49 | 0.77 | 0.82 | 0.96 (n=23) | 0.74 (n=41) | MEDIUM |
| 6f | 10-13 | 83 | Low | 280 | 9.6% | 0.52 | 1.07 | 1.08 | 0.88 (n=23) | 1.16 (n=60) | MEDIUM |
| 6f | 10-13 | 83 | Middle | 302 | 9.3% | 0.51 | 1.03 | 0.96 | 1.51 (n=23) | 0.76 (n=60) | MEDIUM |
| 6f | 10-13 | 83 | High | 343 | 8.2% | 0.47 | 0.91 | 0.97 | 0.61 (n=23) | 1.11 (n=60) | MEDIUM |
| 6f | 14+ | 31 | Low | 150 | 8.7% | 0.57 | 1.35 | 1.20 | 1.44 (n=7) | 1.15 (n=24) | LOW |
| 6f | 14+ | 31 | Middle | 165 | 7.9% | 0.50 | 1.23 | 1.31 | 1.17 (n=7) | 1.36 (n=24) | LOW |
| 6f | 14+ | 31 | High | 168 | 3.0% | 0.43 | 0.46 | 0.49 | 0.42 (n=7) | 0.51 (n=24) | LOW |
| 6½f | 6-9 | 8 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 6½f | 10-13 | 14 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 6½f | 14+ | 2 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 7f | 6-9 | 96 | Low | 220 | 13.6% | 0.52 | 1.03 | 0.96 | 1.35 (n=33) | 0.77 (n=63) | MEDIUM |
| 7f | 6-9 | 96 | Middle | 239 | 15.1% | 0.50 | 1.14 | 1.16 | 0.70 (n=33) | 1.37 (n=63) | MEDIUM |
| 7f | 6-9 | 96 | High | 274 | 11.3% | 0.48 | 0.85 | 0.92 | 0.95 (n=33) | 0.90 (n=63) | MEDIUM |
| 7f | 10-13 | 77 | Low | 258 | 8.9% | 0.52 | 0.99 | 0.96 | 0.45 (n=23) | 1.16 (n=54) | MEDIUM |
| 7f | 10-13 | 77 | Middle | 282 | 9.6% | 0.50 | 1.07 | 0.99 | 1.34 (n=23) | 0.84 (n=54) | MEDIUM |
| 7f | 10-13 | 77 | High | 318 | 8.5% | 0.49 | 0.95 | 1.05 | 1.11 (n=23) | 1.02 (n=54) | MEDIUM |
| 7f | 14+ | 36 | Low | 169 | 5.9% | 0.52 | 0.90 | 0.90 | 0.90 (n=16) | 0.89 (n=20) | LOW |
| 7f | 14+ | 36 | Middle | 187 | 8.6% | 0.52 | 1.31 | 1.23 | 1.44 (n=16) | 1.05 (n=20) | LOW |
| 7f | 14+ | 36 | High | 194 | 5.2% | 0.46 | 0.79 | 0.84 | 0.57 (n=16) | 1.06 (n=20) | LOW |
| 1m | 6-9 | 44 | Low | 103 | 17.5% | 0.59 | 1.37 | 1.11 | 0.88 (n=17) | 1.23 (n=27) | LOW |
| 1m | 6-9 | 44 | Middle | 117 | 12.8% | 0.49 | 1.01 | 1.19 | 1.20 (n=17) | 1.18 (n=27) | LOW |
| 1m | 6-9 | 44 | High | 126 | 8.7% | 0.44 | 0.69 | 0.73 | 0.95 (n=17) | 0.57 (n=27) | LOW |
| 1m | 10-13 | 53 | Low | 188 | 7.4% | 0.51 | 0.85 | 0.84 | 0.49 (n=18) | 1.04 (n=35) | LOW |
| 1m | 10-13 | 53 | Middle | 193 | 7.8% | 0.48 | 0.89 | 0.82 | 1.13 (n=18) | 0.66 (n=35) | LOW |
| 1m | 10-13 | 53 | High | 224 | 10.7% | 0.51 | 1.22 | 1.33 | 1.40 (n=18) | 1.29 (n=35) | LOW |
| 1m | 14+ | 23 | Low | 118 | 6.8% | 0.54 | 1.13 | 1.03 | 0.97 (n=9) | 1.06 (n=14) | LOW |
| 1m | 14+ | 23 | Middle | 132 | 4.5% | 0.50 | 0.76 | 0.71 | 0.98 (n=9) | 0.55 (n=14) | LOW |
| 1m | 14+ | 23 | High | 135 | 6.7% | 0.46 | 1.12 | 1.34 | 1.05 (n=9) | 1.56 (n=14) | LOW |
| 1m1f | 6-9 | 0 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 1m1f | 10-13 | 3 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 1m1f | 14+ | 0 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 1m2f | 6-9 | 68 | Low | 154 | 16.9% | 0.54 | 1.30 | 1.21 | 0.74 (n=24) | 1.42 (n=44) | MEDIUM |
| 1m2f | 6-9 | 68 | Middle | 178 | 13.5% | 0.54 | 1.04 | 1.02 | 1.38 (n=24) | 0.81 (n=44) | MEDIUM |
| 1m2f | 6-9 | 68 | High | 191 | 9.4% | 0.43 | 0.72 | 0.78 | 0.82 (n=24) | 0.76 (n=44) | MEDIUM |
| 1m2f | 10-13 | 56 | Low | 187 | 11.2% | 0.51 | 1.24 | 1.23 | 0.81 (n=20) | 1.46 (n=36) | LOW |
| 1m2f | 10-13 | 56 | Middle | 208 | 10.1% | 0.53 | 1.11 | 1.00 | 1.08 (n=20) | 0.96 (n=36) | LOW |
| 1m2f | 10-13 | 56 | High | 232 | 6.5% | 0.47 | 0.71 | 0.84 | 1.08 (n=20) | 0.67 (n=36) | LOW |
| 1m2f | 14+ | 23 | Low | 111 | 6.3% | 0.55 | 0.99 | 0.82 | 1.47 (n=5) | 0.62 (n=18) | LOW |
| 1m2f | 14+ | 23 | Middle | 123 | 8.9% | 0.50 | 1.41 | 1.42 | 0.00 (n=5) | 1.79 (n=18) | LOW |
| 1m2f | 14+ | 23 | High | 128 | 3.9% | 0.45 | 0.61 | 0.74 | 1.45 (n=5) | 0.56 (n=18) | LOW |
| 1m3f | 6-9 | 9 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 1m3f | 10-13 | 7 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 1m3f | 14+ | 2 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 1m4f | 6-9 | 48 | Low | 104 | 12.5% | 0.50 | 0.92 | 0.97 | 0.70 (n=18) | 1.17 (n=30) | LOW |
| 1m4f | 6-9 | 48 | Middle | 115 | 13.9% | 0.48 | 1.02 | 1.04 | 1.22 (n=18) | 0.93 (n=30) | LOW |
| 1m4f | 6-9 | 48 | High | 133 | 14.3% | 0.52 | 1.05 | 0.99 | 1.07 (n=18) | 0.95 (n=30) | LOW |
| 1m4f | 10-13 | 26 | Low | 87 | 4.6% | 0.50 | 0.50 | 0.52 | 0.88 (n=7) | 0.37 (n=19) | LOW |
| 1m4f | 10-13 | 26 | Middle | 90 | 13.3% | 0.53 | 1.46 | 1.54 | 2.08 (n=7) | 1.37 (n=19) | LOW |
| 1m4f | 10-13 | 26 | High | 108 | 9.3% | 0.48 | 1.01 | 0.95 | 0.36 (n=7) | 1.16 (n=19) | LOW |
| 1m4f | 14+ | 8 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 1m5½f | 6-9 | 17 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 1m5½f | 10-13 | 5 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 1m5½f | 14+ | 2 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 2m | 6-9 | 4 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 2m | 10-13 | 3 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 2m | 14+ | 2 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 2m½f | 6-9 | 7 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 2m½f | 10-13 | 4 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 2m½f | 14+ | 2 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 2m2f | 6-9 | 1 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 2m2f | 10-13 | 0 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |
| 2m2f | 14+ | 0 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |

### b) Pace

**b) Pace by trip and going (running style from the race comment; leaders' IV is about 2 everywhere because comments are written after the race, so compare with the national figure for the same trip and going)** - counts every runner whose comment shows its position; national = all UK/IRE flat; races 2019-04-12 to 2026-09-19 (954 races; split 2019-21 / 2022-26).
| Trip | Going | Races | Style | Runners | Win % | IV | A/E | National win % | National IV | A/E 2019-21 | A/E 2022-26 | Level |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5f | All goings | 49 | Led | 50 | 14.0% | 1.57 | 1.50 | 21.5% | 1.96 | 0.00 (n=15) | 2.28 (n=30) | LOW |
| 5f | All goings | 49 | Prominent | 194 | 8.2% | 0.92 | 0.88 | 12.5% | 1.14 | 0.71 (n=16) | 0.95 (n=29) | LOW |
| 5f | All goings | 49 | Midfield | 49 | 6.1% | 0.68 | 0.87 | 5.7% | 0.52 | 1.84 (n=4) | 0.42 (n=13) | LOW |
| 5f | All goings | 49 | Held up | 143 | 9.1% | 1.02 | 1.02 | 6.8% | 0.62 | 1.55 (n=14) | 0.73 (n=33) | LOW |
| 5f | Good to Firm | 18 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 5f | Good | 17 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 5f | Good to Soft | 8 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 5f | Soft | 4 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 5f | Heavy | 2 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 6f | All goings | 182 | Led | 171 | 19.9% | 2.09 | 1.60 | 19.7% | 2.03 | 1.41 (n=48) | 1.68 (n=115) | HIGH |
| 6f | All goings | 182 | Prominent | 661 | 11.6% | 1.22 | 1.07 | 11.1% | 1.14 | 1.00 (n=52) | 1.10 (n=125) | HIGH |
| 6f | All goings | 182 | Midfield | 277 | 5.4% | 0.57 | 0.64 | 5.4% | 0.56 | 0.76 (n=34) | 0.58 (n=72) | HIGH |
| 6f | All goings | 182 | Held up | 548 | 5.8% | 0.61 | 0.77 | 6.6% | 0.68 | 0.89 (n=51) | 0.73 (n=127) | HIGH |
| 6f | Good to Firm | 62 | Led | 58 | 13.8% | 1.38 | 0.92 | 20.4% | 1.92 | 1.35 (n=10) | 0.83 (n=46) | MEDIUM |
| 6f | Good to Firm | 62 | Prominent | 232 | 12.9% | 1.29 | 1.23 | 12.1% | 1.14 | 0.99 (n=12) | 1.28 (n=48) | MEDIUM |
| 6f | Good to Firm | 62 | Midfield | 79 | 5.1% | 0.51 | 0.52 | 5.1% | 0.48 | 0.98 (n=7) | 0.36 (n=27) | MEDIUM |
| 6f | Good to Firm | 62 | Held up | 180 | 7.2% | 0.72 | 0.97 | 7.5% | 0.71 | 0.77 (n=12) | 1.02 (n=48) | MEDIUM |
| 6f | Good | 68 | Led | 63 | 31.7% | 3.43 | 2.75 | 21.0% | 2.27 | 1.78 (n=15) | 3.05 (n=46) | MEDIUM |
| 6f | Good | 68 | Prominent | 246 | 8.9% | 0.97 | 0.88 | 10.3% | 1.11 | 0.97 (n=15) | 0.85 (n=52) | MEDIUM |
| 6f | Good | 68 | Midfield | 125 | 8.0% | 0.86 | 1.06 | 5.7% | 0.62 | 1.57 (n=11) | 0.87 (n=34) | MEDIUM |
| 6f | Good | 68 | Held up | 214 | 3.7% | 0.40 | 0.48 | 5.7% | 0.62 | 0.56 (n=15) | 0.46 (n=52) | MEDIUM |
| 6f | Good to Soft | 31 | Led | 28 | 7.1% | 0.76 | 0.65 | 15.1% | 1.52 | 0.83 (n=16) | 0.00 (n=11) | LOW |
| 6f | Good to Soft | 31 | Prominent | 108 | 14.8% | 1.58 | 1.17 | 11.8% | 1.19 | 1.17 (n=18) | 1.17 (n=12) | LOW |
| 6f | Good to Soft | 31 | Midfield | 48 | 2.1% | 0.22 | 0.22 | 6.6% | 0.66 | 0.00 (n=12) | 0.55 (n=6) | LOW |
| 6f | Good to Soft | 31 | Held up | 94 | 7.4% | 0.80 | 1.09 | 7.5% | 0.76 | 1.45 (n=18) | 0.67 (n=13) | LOW |
| 6f | Soft | 11 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 6f | Heavy | 10 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 6½f | All goings | 23 | Led | 24 | 12.5% | 1.44 | 0.85 | 15.1% | 1.97 | 0.00 (n=4) | 0.95 (n=18) | LOW |
| 6½f | All goings | 23 | Prominent | 92 | 13.0% | 1.51 | 1.13 | 10.3% | 1.34 | 1.39 (n=4) | 1.09 (n=19) | LOW |
| 6½f | All goings | 23 | Midfield | 36 | 2.8% | 0.32 | 0.43 | 4.4% | 0.58 | 0.00 (n=4) | 0.65 (n=11) | LOW |
| 6½f | All goings | 23 | Held up | 79 | 5.1% | 0.58 | 0.88 | 4.8% | 0.63 | 0.92 (n=4) | 0.87 (n=19) | LOW |
| 6½f | Good to Firm | 8 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 6½f | Good | 4 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 6½f | Good to Soft | 4 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 6½f | Soft | 3 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 6½f | Heavy | 4 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 7f | All goings | 221 | Led | 215 | 16.3% | 1.60 | 1.22 | 19.2% | 1.99 | 1.50 (n=66) | 1.09 (n=133) | HIGH |
| 7f | All goings | 221 | Prominent | 756 | 11.9% | 1.17 | 1.03 | 11.7% | 1.22 | 1.04 (n=72) | 1.03 (n=145) | HIGH |
| 7f | All goings | 221 | Midfield | 279 | 6.8% | 0.67 | 0.86 | 6.0% | 0.62 | 0.23 (n=42) | 1.26 (n=68) | HIGH |
| 7f | All goings | 221 | Held up | 648 | 7.6% | 0.74 | 0.91 | 6.3% | 0.66 | 1.09 (n=70) | 0.82 (n=134) | HIGH |
| 7f | Good to Firm | 58 | Led | 56 | 21.4% | 1.93 | 1.32 | 20.5% | 1.89 | 1.70 (n=6) | 1.26 (n=47) | LOW |
| 7f | Good to Firm | 58 | Prominent | 211 | 12.3% | 1.11 | 1.07 | 12.4% | 1.14 | 1.21 (n=6) | 1.06 (n=50) | LOW |
| 7f | Good to Firm | 58 | Midfield | 37 | 10.8% | 0.98 | 1.29 | 6.8% | 0.63 | 0.00 (n=2) | 1.61 (n=16) | LOW |
| 7f | Good to Firm | 58 | Held up | 156 | 5.8% | 0.52 | 0.61 | 7.5% | 0.69 | 0.50 (n=6) | 0.63 (n=45) | LOW |
| 7f | Good | 83 | Led | 78 | 19.2% | 2.17 | 1.66 | 20.1% | 2.16 | 2.28 (n=28) | 1.27 (n=46) | MEDIUM |
| 7f | Good | 83 | Prominent | 286 | 11.2% | 1.26 | 1.04 | 11.1% | 1.19 | 1.05 (n=32) | 1.04 (n=50) | MEDIUM |
| 7f | Good | 83 | Midfield | 153 | 5.2% | 0.59 | 0.69 | 6.0% | 0.65 | 0.21 (n=22) | 1.02 (n=30) | MEDIUM |
| 7f | Good | 83 | Held up | 262 | 5.3% | 0.60 | 0.75 | 5.8% | 0.63 | 0.81 (n=31) | 0.72 (n=48) | MEDIUM |
| 7f | Good to Soft | 31 | Led | 33 | 15.2% | 1.44 | 1.18 | 17.3% | 1.73 | 1.33 (n=14) | 0.82 (n=15) | LOW |
| 7f | Good to Soft | 31 | Prominent | 103 | 11.7% | 1.10 | 0.93 | 11.8% | 1.18 | 1.01 (n=15) | 0.87 (n=16) | LOW |
| 7f | Good to Soft | 31 | Midfield | 45 | 4.4% | 0.42 | 0.64 | 7.2% | 0.72 | 1.01 (n=7) | 0.47 (n=10) | LOW |
| 7f | Good to Soft | 31 | Held up | 94 | 10.6% | 1.01 | 1.32 | 7.1% | 0.71 | 0.96 (n=14) | 1.56 (n=16) | LOW |
| 7f | Soft | 34 | Led | 35 | 8.6% | 0.74 | 0.63 | 18.0% | 1.89 | 0.00 (n=13) | 0.88 (n=17) | LOW |
| 7f | Soft | 34 | Prominent | 104 | 15.4% | 1.33 | 1.20 | 12.5% | 1.31 | 1.18 (n=14) | 1.21 (n=19) | LOW |
| 7f | Soft | 34 | Midfield | 30 | 10.0% | 0.86 | 1.06 | 5.7% | 0.60 | 0.00 (n=8) | 1.85 (n=9) | LOW |
| 7f | Soft | 34 | Held up | 90 | 8.9% | 0.77 | 0.95 | 5.8% | 0.61 | 1.38 (n=14) | 0.49 (n=15) | LOW |
| 7f | Heavy | 15 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 1m | All goings | 128 | Led | 124 | 16.1% | 1.78 | 1.49 | 18.4% | 1.89 | 1.09 (n=40) | 1.78 (n=76) | MEDIUM |
| 1m | All goings | 128 | Prominent | 459 | 10.5% | 1.16 | 0.99 | 11.4% | 1.17 | 1.16 (n=45) | 0.91 (n=81) | MEDIUM |
| 1m | All goings | 128 | Midfield | 211 | 6.6% | 0.73 | 0.85 | 6.4% | 0.66 | 0.95 (n=31) | 0.77 (n=44) | MEDIUM |
| 1m | All goings | 128 | Held up | 400 | 6.5% | 0.72 | 0.84 | 7.1% | 0.73 | 0.67 (n=42) | 0.93 (n=78) | MEDIUM |
| 1m | Good to Firm | 29 | Led | 29 | 20.7% | 1.84 | 1.52 | 19.4% | 1.76 | 0.90 (n=7) | 1.77 (n=20) | LOW |
| 1m | Good to Firm | 29 | Prominent | 95 | 11.6% | 1.03 | 1.00 | 12.0% | 1.09 | 1.35 (n=7) | 0.87 (n=22) | LOW |
| 1m | Good to Firm | 29 | Midfield | 28 | 10.7% | 0.95 | 1.36 | 7.4% | 0.67 | 1.46 (n=3) | 1.31 (n=11) | LOW |
| 1m | Good to Firm | 29 | Held up | 70 | 7.1% | 0.63 | 0.72 | 8.6% | 0.78 | 0.82 (n=6) | 0.70 (n=19) | LOW |
| 1m | Good | 50 | Led | 47 | 12.8% | 1.64 | 1.80 | 18.1% | 1.91 | 1.59 (n=12) | 1.92 (n=34) | LOW |
| 1m | Good | 50 | Prominent | 204 | 9.3% | 1.19 | 0.98 | 11.5% | 1.21 | 1.32 (n=13) | 0.89 (n=36) | LOW |
| 1m | Good | 50 | Midfield | 98 | 4.1% | 0.52 | 0.55 | 6.3% | 0.66 | 0.82 (n=10) | 0.42 (n=21) | LOW |
| 1m | Good | 50 | Held up | 189 | 6.9% | 0.88 | 0.97 | 6.7% | 0.70 | 0.50 (n=12) | 1.17 (n=36) | LOW |
| 1m | Good to Soft | 22 | Led | 23 | 8.7% | 0.99 | 0.76 | 17.4% | 1.75 | 0.57 (n=11) | 1.13 (n=8) | LOW |
| 1m | Good to Soft | 22 | Prominent | 77 | 7.8% | 0.89 | 0.73 | 11.4% | 1.14 | 0.78 (n=13) | 0.65 (n=9) | LOW |
| 1m | Good to Soft | 22 | Midfield | 33 | 12.1% | 1.38 | 1.53 | 6.9% | 0.69 | 0.64 (n=7) | 2.85 (n=5) | LOW |
| 1m | Good to Soft | 22 | Held up | 72 | 8.3% | 0.95 | 1.04 | 7.8% | 0.78 | 1.36 (n=13) | 0.71 (n=9) | LOW |
| 1m | Soft | 16 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 1m | Heavy | 11 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 1m1f | All goings | 3 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 1m1f | Good to Soft | 1 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 1m1f | Soft | 2 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 1m2f | All goings | 162 | Led | 149 | 14.1% | 1.44 | 1.07 | 18.9% | 1.76 | 1.21 (n=41) | 1.03 (n=103) | HIGH |
| 1m2f | All goings | 162 | Prominent | 457 | 11.8% | 1.21 | 1.07 | 12.4% | 1.16 | 0.64 (n=48) | 1.24 (n=108) | HIGH |
| 1m2f | All goings | 162 | Midfield | 263 | 7.2% | 0.74 | 0.88 | 7.1% | 0.66 | 1.18 (n=32) | 0.68 (n=68) | HIGH |
| 1m2f | All goings | 162 | Held up | 524 | 8.0% | 0.82 | 0.89 | 8.1% | 0.76 | 1.27 (n=50) | 0.71 (n=107) | HIGH |
| 1m2f | Good to Firm | 46 | Led | 41 | 19.5% | 1.93 | 1.09 | 22.1% | 1.80 | 1.03 (n=12) | 1.11 (n=29) | LOW |
| 1m2f | Good to Firm | 46 | Prominent | 124 | 13.7% | 1.36 | 1.01 | 13.3% | 1.08 | 0.45 (n=13) | 1.21 (n=33) | LOW |
| 1m2f | Good to Firm | 46 | Midfield | 46 | 6.5% | 0.65 | 0.65 | 8.0% | 0.65 | 1.29 (n=8) | 0.00 (n=14) | LOW |
| 1m2f | Good to Firm | 46 | Held up | 116 | 4.3% | 0.43 | 0.47 | 9.1% | 0.74 | 0.74 (n=13) | 0.38 (n=30) | LOW |
| 1m2f | Good | 66 | Led | 62 | 8.1% | 0.89 | 0.69 | 17.5% | 1.70 | 0.83 (n=13) | 0.66 (n=47) | MEDIUM |
| 1m2f | Good | 66 | Prominent | 202 | 12.4% | 1.36 | 1.30 | 12.1% | 1.18 | 0.81 (n=16) | 1.41 (n=49) | MEDIUM |
| 1m2f | Good | 66 | Midfield | 137 | 6.6% | 0.72 | 0.94 | 6.7% | 0.65 | 1.05 (n=11) | 0.90 (n=34) | MEDIUM |
| 1m2f | Good | 66 | Held up | 258 | 8.1% | 0.89 | 0.96 | 8.0% | 0.78 | 1.39 (n=16) | 0.80 (n=49) | MEDIUM |
| 1m2f | Good to Soft | 21 | Led | 20 | 15.0% | 1.43 | 1.37 | 17.1% | 1.63 | 1.18 (n=6) | 1.48 (n=12) | LOW |
| 1m2f | Good to Soft | 21 | Prominent | 57 | 7.0% | 0.67 | 0.65 | 12.3% | 1.18 | 0.00 (n=7) | 1.08 (n=12) | LOW |
| 1m2f | Good to Soft | 21 | Midfield | 41 | 9.8% | 0.93 | 0.98 | 7.4% | 0.71 | 1.19 (n=5) | 0.84 (n=11) | LOW |
| 1m2f | Good to Soft | 21 | Held up | 73 | 12.3% | 1.18 | 1.49 | 8.2% | 0.78 | 2.16 (n=8) | 1.07 (n=13) | LOW |
| 1m2f | Soft | 19 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 1m2f | Heavy | 10 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 1m3f | All goings | 23 | Led | 21 | 23.8% | 2.02 | 1.90 | 21.0% | 1.80 | 2.65 (n=7) | 1.60 (n=14) | LOW |
| 1m3f | All goings | 23 | Prominent | 66 | 12.1% | 1.03 | 0.85 | 13.5% | 1.16 | 0.54 (n=9) | 1.06 (n=14) | LOW |
| 1m3f | All goings | 23 | Midfield | 32 | 9.4% | 0.80 | 0.72 | 7.6% | 0.65 | 0.00 (n=6) | 1.11 (n=9) | LOW |
| 1m3f | All goings | 23 | Held up | 68 | 8.8% | 0.75 | 1.04 | 8.4% | 0.72 | 1.75 (n=9) | 0.58 (n=14) | LOW |
| 1m3f | Good to Firm | 7 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 1m3f | Good | 10 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 1m3f | Good to Soft | 4 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 1m3f | Soft | 2 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 1m4f | All goings | 95 | Led | 94 | 13.8% | 1.30 | 1.17 | 15.9% | 1.51 | 0.54 (n=32) | 1.48 (n=58) | MEDIUM |
| 1m4f | All goings | 95 | Prominent | 262 | 11.8% | 1.11 | 0.92 | 13.1% | 1.24 | 1.15 (n=34) | 0.77 (n=57) | MEDIUM |
| 1m4f | All goings | 95 | Midfield | 128 | 10.2% | 0.95 | 1.12 | 6.7% | 0.64 | 1.00 (n=19) | 1.18 (n=38) | MEDIUM |
| 1m4f | All goings | 95 | Held up | 277 | 8.7% | 0.81 | 0.81 | 8.3% | 0.79 | 0.76 (n=34) | 0.84 (n=60) | MEDIUM |
| 1m4f | Good to Firm | 23 | Led | 24 | 16.7% | 1.20 | 1.18 | 17.2% | 1.32 | 0.00 (n=5) | 1.52 (n=18) | LOW |
| 1m4f | Good to Firm | 23 | Prominent | 55 | 16.4% | 1.18 | 0.94 | 15.9% | 1.22 | 1.26 (n=5) | 0.84 (n=17) | LOW |
| 1m4f | Good to Firm | 23 | Midfield | 10 | 10.0% | 0.72 | 1.12 | 7.7% | 0.59 | - (n=0) | 1.12 (n=8) | LOW |
| 1m4f | Good to Firm | 23 | Held up | 55 | 10.9% | 0.79 | 0.91 | 10.4% | 0.80 | 0.73 (n=5) | 0.95 (n=17) | LOW |
| 1m4f | Good | 36 | Led | 33 | 9.1% | 0.91 | 0.77 | 16.1% | 1.55 | 0.00 (n=11) | 1.25 (n=20) | LOW |
| 1m4f | Good | 36 | Prominent | 96 | 10.4% | 1.04 | 0.82 | 12.8% | 1.23 | 1.06 (n=13) | 0.66 (n=21) | LOW |
| 1m4f | Good | 36 | Midfield | 58 | 8.6% | 0.86 | 1.05 | 7.1% | 0.68 | 1.06 (n=9) | 1.04 (n=14) | LOW |
| 1m4f | Good | 36 | Held up | 113 | 10.6% | 1.06 | 0.98 | 7.9% | 0.76 | 0.98 (n=13) | 0.98 (n=23) | LOW |
| 1m4f | Good to Soft | 15 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 1m4f | Soft | 14 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 1m4f | Heavy | 7 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 1m5½f | All goings | 32 | Led | 31 | 32.3% | 2.81 | 2.14 | 25.6% | 2.65 | 0.69 (n=11) | 2.79 (n=19) | LOW |
| 1m5½f | All goings | 32 | Prominent | 84 | 8.3% | 0.73 | 0.61 | 10.8% | 1.11 | 1.26 (n=12) | 0.27 (n=19) | LOW |
| 1m5½f | All goings | 32 | Midfield | 25 | 12.0% | 1.05 | 1.12 | 5.9% | 0.61 | 1.73 (n=4) | 0.66 (n=6) | LOW |
| 1m5½f | All goings | 32 | Held up | 78 | 6.4% | 0.56 | 0.55 | 5.2% | 0.53 | 0.76 (n=10) | 0.38 (n=18) | LOW |
| 1m5½f | Good to Firm | 11 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 1m5½f | Good | 6 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 1m5½f | Good to Soft | 7 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 1m5½f | Soft | 3 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 1m5½f | Heavy | 5 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 2m | All goings | 13 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 2m | Good to Firm | 6 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 2m | Soft | 3 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 2m | Heavy | 4 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 2m½f | All goings | 14 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 2m½f | Good to Firm | 6 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 2m½f | Good | 5 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 2m½f | Good to Soft | 2 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 2m½f | Soft | 1 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 2m2f | All goings | 1 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |
| 2m2f | Soft | 1 | too few races (under 20) - count only |  |  |  |  |  |  |  |  |  |

### c) Weight in handicaps

**c) Weight in handicaps by trip and going (lb below the top weight CARRIED in the race)** - counts every runner in handicaps with weights in our results; races 2019-04-12 to 2026-09-19 (954 races; split 2019-21 / 2022-26).
| Trip | Going | Races | Weight band | Runners | Win % | PRB | A/E | A/E 2019-21 | A/E 2022-26 | Level |
|---|---|---|---|---|---|---|---|---|---|---|
| 5f | All goings | 50 | Top 0-2lb | 226 | 11.1% | 0.52 | 1.06 | 0.91 (n=17) | 1.12 (n=33) | LOW |
| 5f | All goings | 50 | Upper 3-9lb | 187 | 8.6% | 0.51 | 0.97 | 1.32 (n=13) | 0.81 (n=25) | LOW |
| 5f | All goings | 50 | Middle 10-16lb | 105 | 7.6% | 0.47 | 0.97 | 0.93 (n=9) | 1.00 (n=18) | LOW |
| 5f | All goings | 50 | Low 17lb+ | 24 | 4.2% | 0.44 | 0.62 | 0.00 (n=3) | 1.23 (n=8) | LOW |
| 5f | Good to Firm | 18 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 5f | Good | 17 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 5f | Good to Soft | 8 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 5f | Soft | 5 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 5f | Heavy | 2 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 6f | All goings | 184 | Top 0-2lb | 1085 | 10.8% | 0.52 | 1.02 | 1.02 (n=54) | 1.03 (n=130) | HIGH |
| 6f | All goings | 184 | Upper 3-9lb | 645 | 8.4% | 0.48 | 1.00 | 0.97 (n=48) | 1.01 (n=102) | HIGH |
| 6f | All goings | 184 | Middle 10-16lb | 152 | 7.2% | 0.48 | 0.90 | 0.76 (n=17) | 0.96 (n=39) | HIGH |
| 6f | All goings | 184 | Low 17lb+ | 53 | 3.8% | 0.47 | 0.61 | 1.84 (n=8) | 0.00 (n=17) | HIGH |
| 6f | Good to Firm | 62 | Top 0-2lb | 335 | 11.0% | 0.52 | 0.98 | 0.93 (n=12) | 0.99 (n=50) | MEDIUM |
| 6f | Good to Firm | 62 | Upper 3-9lb | 227 | 9.7% | 0.49 | 1.07 | 1.18 (n=11) | 1.04 (n=39) | MEDIUM |
| 6f | Good to Firm | 62 | Middle 10-16lb | 45 | 4.4% | 0.40 | 0.64 | 0.00 (n=6) | 0.97 (n=10) | MEDIUM |
| 6f | Good to Firm | 62 | Low 17lb+ | 12 | 8.3% | 0.50 | 1.56 | 4.46 (n=3) | 0.00 (n=5) | MEDIUM |
| 6f | Good | 70 | Top 0-2lb | 483 | 10.6% | 0.51 | 1.09 | 1.09 (n=17) | 1.09 (n=53) | MEDIUM |
| 6f | Good | 70 | Upper 3-9lb | 230 | 6.1% | 0.47 | 0.78 | 0.49 (n=15) | 0.87 (n=39) | MEDIUM |
| 6f | Good | 70 | Middle 10-16lb | 52 | 9.6% | 0.52 | 1.14 | 2.76 (n=2) | 0.82 (n=16) | MEDIUM |
| 6f | Good | 70 | Low 17lb+ | 17 | 0.0% | 0.53 | 0.00 | 0.00 (n=2) | 0.00 (n=5) | MEDIUM |
| 6f | Good to Soft | 31 | Top 0-2lb | 200 | 10.5% | 0.53 | 1.01 | 0.84 (n=18) | 1.24 (n=13) | LOW |
| 6f | Good to Soft | 31 | Upper 3-9lb | 98 | 7.1% | 0.46 | 0.91 | 1.16 (n=15) | 0.39 (n=11) | LOW |
| 6f | Good to Soft | 31 | Middle 10-16lb | 18 | 11.1% | 0.51 | 1.24 | 2.19 (n=3) | 0.87 (n=5) | LOW |
| 6f | Good to Soft | 31 | Low 17lb+ | 12 | 8.3% | 0.39 | 1.07 | 1.88 (n=2) | 0.00 (n=3) | LOW |
| 6f | Soft | 11 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 6f | Heavy | 10 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 6½f | All goings | 24 | Top 0-2lb | 207 | 9.2% | 0.52 | 0.92 | 0.66 (n=5) | 0.96 (n=19) | LOW |
| 6½f | All goings | 24 | Upper 3-9lb | 53 | 9.4% | 0.45 | 1.53 | 1.54 (n=4) | 1.52 (n=14) | LOW |
| 6½f | All goings | 24 | Middle 10-16lb | 1 | 0.0% | 0.00 | 0.00 | - (n=0) | 0.00 (n=1) | LOW |
| 6½f | All goings | 24 | Low 17lb+ | 0 | - | - | - | - (n=0) | - (n=0) | LOW |
| 6½f | Good to Firm | 8 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 6½f | Good | 4 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 6½f | Good to Soft | 4 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 6½f | Soft | 4 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 6½f | Heavy | 4 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 7f | All goings | 223 | Top 0-2lb | 1119 | 11.2% | 0.52 | 0.98 | 1.02 (n=76) | 0.96 (n=147) | HIGH |
| 7f | All goings | 223 | Upper 3-9lb | 742 | 10.1% | 0.49 | 1.09 | 0.87 (n=59) | 1.20 (n=110) | HIGH |
| 7f | All goings | 223 | Middle 10-16lb | 275 | 7.6% | 0.48 | 0.95 | 1.46 (n=30) | 0.76 (n=68) | HIGH |
| 7f | All goings | 223 | Low 17lb+ | 68 | 4.4% | 0.45 | 0.62 | 0.53 (n=13) | 0.68 (n=29) | HIGH |
| 7f | Good to Firm | 59 | Top 0-2lb | 244 | 11.5% | 0.51 | 0.94 | 1.04 (n=8) | 0.93 (n=51) | LOW |
| 7f | Good to Firm | 59 | Upper 3-9lb | 195 | 13.8% | 0.52 | 1.35 | 0.47 (n=8) | 1.45 (n=40) | LOW |
| 7f | Good to Firm | 59 | Middle 10-16lb | 82 | 3.7% | 0.42 | 0.40 | 1.66 (n=4) | 0.29 (n=28) | LOW |
| 7f | Good to Firm | 59 | Low 17lb+ | 16 | 6.2% | 0.57 | 0.56 | 2.09 (n=2) | 0.00 (n=9) | LOW |
| 7f | Good | 83 | Top 0-2lb | 445 | 11.5% | 0.52 | 1.06 | 1.13 (n=33) | 1.01 (n=50) | MEDIUM |
| 7f | Good | 83 | Upper 3-9lb | 320 | 6.6% | 0.47 | 0.81 | 0.75 (n=27) | 0.86 (n=37) | MEDIUM |
| 7f | Good | 83 | Middle 10-16lb | 102 | 8.8% | 0.50 | 1.25 | 1.32 (n=13) | 1.22 (n=24) | MEDIUM |
| 7f | Good | 83 | Low 17lb+ | 24 | 8.3% | 0.49 | 1.13 | 0.00 (n=4) | 1.90 (n=10) | MEDIUM |
| 7f | Good to Soft | 31 | Top 0-2lb | 159 | 10.1% | 0.53 | 0.88 | 0.85 (n=15) | 0.92 (n=16) | LOW |
| 7f | Good to Soft | 31 | Upper 3-9lb | 102 | 11.8% | 0.47 | 1.27 | 1.15 (n=10) | 1.34 (n=13) | LOW |
| 7f | Good to Soft | 31 | Middle 10-16lb | 40 | 10.0% | 0.50 | 1.26 | 2.30 (n=3) | 0.87 (n=9) | LOW |
| 7f | Good to Soft | 31 | Low 17lb+ | 5 | 0.0% | 0.23 | 0.00 | - (n=0) | 0.00 (n=4) | LOW |
| 7f | Soft | 35 | Top 0-2lb | 185 | 10.8% | 0.50 | 0.91 | 0.92 (n=15) | 0.91 (n=20) | LOW |
| 7f | Soft | 35 | Upper 3-9lb | 92 | 12.0% | 0.50 | 1.14 | 0.99 (n=11) | 1.24 (n=14) | LOW |
| 7f | Soft | 35 | Middle 10-16lb | 36 | 11.1% | 0.51 | 1.45 | 1.66 (n=7) | 1.05 (n=4) | LOW |
| 7f | Soft | 35 | Low 17lb+ | 12 | 0.0% | 0.42 | 0.00 | 0.00 (n=5) | 0.00 (n=3) | LOW |
| 7f | Heavy | 15 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 1m | All goings | 129 | Top 0-2lb | 654 | 10.2% | 0.52 | 0.97 | 0.99 (n=46) | 0.95 (n=83) | MEDIUM |
| 1m | All goings | 129 | Upper 3-9lb | 443 | 8.8% | 0.48 | 1.02 | 1.08 (n=36) | 1.00 (n=71) | MEDIUM |
| 1m | All goings | 129 | Middle 10-16lb | 198 | 9.6% | 0.51 | 1.14 | 1.01 (n=22) | 1.22 (n=43) | MEDIUM |
| 1m | All goings | 129 | Low 17lb+ | 80 | 5.0% | 0.42 | 0.82 | 0.61 (n=14) | 0.93 (n=23) | MEDIUM |
| 1m | Good to Firm | 29 | Top 0-2lb | 100 | 12.0% | 0.51 | 0.93 | 1.20 (n=7) | 0.84 (n=22) | LOW |
| 1m | Good to Firm | 29 | Upper 3-9lb | 97 | 14.4% | 0.50 | 1.31 | 1.11 (n=5) | 1.38 (n=19) | LOW |
| 1m | Good to Firm | 29 | Middle 10-16lb | 38 | 2.6% | 0.52 | 0.27 | 0.00 (n=4) | 0.36 (n=13) | LOW |
| 1m | Good to Firm | 29 | Low 17lb+ | 20 | 10.0% | 0.43 | 1.12 | 0.00 (n=1) | 1.19 (n=7) | LOW |
| 1m | Good | 51 | Top 0-2lb | 271 | 10.0% | 0.54 | 1.02 | 1.08 (n=14) | 1.00 (n=37) | LOW |
| 1m | Good | 51 | Upper 3-9lb | 205 | 6.3% | 0.47 | 0.85 | 1.02 (n=12) | 0.79 (n=34) | LOW |
| 1m | Good | 51 | Middle 10-16lb | 96 | 10.4% | 0.49 | 1.30 | 0.95 (n=8) | 1.42 (n=23) | LOW |
| 1m | Good | 51 | Low 17lb+ | 35 | 2.9% | 0.41 | 0.61 | 0.00 (n=5) | 0.94 (n=11) | LOW |
| 1m | Good to Soft | 22 | Top 0-2lb | 101 | 9.9% | 0.51 | 0.89 | 0.59 (n=13) | 1.35 (n=9) | LOW |
| 1m | Good to Soft | 22 | Upper 3-9lb | 79 | 7.6% | 0.47 | 1.00 | 1.52 (n=13) | 0.59 (n=8) | LOW |
| 1m | Good to Soft | 22 | Middle 10-16lb | 48 | 10.4% | 0.53 | 1.43 | 1.48 (n=8) | 1.28 (n=3) | LOW |
| 1m | Good to Soft | 22 | Low 17lb+ | 19 | 5.3% | 0.47 | 0.81 | 1.20 (n=7) | 0.00 (n=3) | LOW |
| 1m | Soft | 16 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 1m | Heavy | 11 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 1m1f | All goings | 3 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 1m1f | Good to Soft | 1 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 1m1f | Soft | 2 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 1m2f | All goings | 163 | Top 0-2lb | 591 | 12.5% | 0.53 | 1.03 | 0.93 (n=52) | 1.07 (n=111) | HIGH |
| 1m2f | All goings | 163 | Upper 3-9lb | 581 | 10.3% | 0.50 | 1.04 | 1.01 (n=42) | 1.06 (n=96) | HIGH |
| 1m2f | All goings | 163 | Middle 10-16lb | 316 | 7.6% | 0.46 | 0.91 | 1.10 (n=33) | 0.79 (n=66) | HIGH |
| 1m2f | All goings | 163 | Low 17lb+ | 99 | 6.1% | 0.44 | 0.89 | 1.16 (n=18) | 0.72 (n=36) | HIGH |
| 1m2f | Good to Firm | 46 | Top 0-2lb | 116 | 16.4% | 0.58 | 0.94 | 1.29 (n=13) | 0.84 (n=33) | LOW |
| 1m2f | Good to Firm | 46 | Upper 3-9lb | 144 | 14.6% | 0.50 | 1.20 | 0.92 (n=12) | 1.32 (n=31) | LOW |
| 1m2f | Good to Firm | 46 | Middle 10-16lb | 80 | 5.0% | 0.41 | 0.59 | 0.42 (n=9) | 0.69 (n=16) | LOW |
| 1m2f | Good to Firm | 46 | Low 17lb+ | 25 | 8.0% | 0.40 | 1.30 | 1.95 (n=6) | 0.98 (n=9) | LOW |
| 1m2f | Good | 66 | Top 0-2lb | 313 | 13.1% | 0.53 | 1.24 | 0.96 (n=16) | 1.34 (n=50) | MEDIUM |
| 1m2f | Good | 66 | Upper 3-9lb | 268 | 6.7% | 0.48 | 0.78 | 0.89 (n=14) | 0.75 (n=40) | MEDIUM |
| 1m2f | Good | 66 | Middle 10-16lb | 112 | 6.2% | 0.49 | 0.86 | 1.64 (n=9) | 0.53 (n=28) | MEDIUM |
| 1m2f | Good | 66 | Low 17lb+ | 33 | 3.0% | 0.41 | 0.55 | 0.00 (n=5) | 0.93 (n=11) | MEDIUM |
| 1m2f | Good to Soft | 21 | Top 0-2lb | 60 | 6.7% | 0.48 | 0.59 | 0.69 (n=8) | 0.52 (n=13) | LOW |
| 1m2f | Good to Soft | 21 | Upper 3-9lb | 81 | 9.9% | 0.54 | 1.15 | 1.43 (n=4) | 1.03 (n=11) | LOW |
| 1m2f | Good to Soft | 21 | Middle 10-16lb | 62 | 12.9% | 0.49 | 1.34 | 0.85 (n=6) | 1.66 (n=10) | LOW |
| 1m2f | Good to Soft | 21 | Low 17lb+ | 15 | 6.7% | 0.43 | 0.75 | 1.49 (n=3) | 0.00 (n=7) | LOW |
| 1m2f | Soft | 20 | Top 0-2lb | 79 | 8.9% | 0.50 | 0.75 | 0.78 (n=10) | 0.71 (n=10) | LOW |
| 1m2f | Soft | 20 | Upper 3-9lb | 58 | 17.2% | 0.52 | 1.59 | 1.45 (n=7) | 1.70 (n=9) | LOW |
| 1m2f | Soft | 20 | Middle 10-16lb | 33 | 9.1% | 0.46 | 0.93 | 1.19 (n=4) | 0.65 (n=7) | LOW |
| 1m2f | Soft | 20 | Low 17lb+ | 15 | 0.0% | 0.50 | 0.00 | 0.00 (n=2) | 0.00 (n=5) | LOW |
| 1m2f | Heavy | 10 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 1m3f | All goings | 23 | Top 0-2lb | 96 | 11.5% | 0.51 | 0.85 | 1.15 (n=9) | 0.70 (n=14) | LOW |
| 1m3f | All goings | 23 | Upper 3-9lb | 62 | 9.7% | 0.47 | 0.91 | 0.57 (n=8) | 1.30 (n=10) | LOW |
| 1m3f | All goings | 23 | Middle 10-16lb | 31 | 12.9% | 0.50 | 1.29 | 1.87 (n=5) | 0.99 (n=6) | LOW |
| 1m3f | All goings | 23 | Low 17lb+ | 7 | 28.6% | 0.61 | 4.36 | 0.00 (n=2) | 5.90 (n=3) | LOW |
| 1m3f | Good to Firm | 7 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 1m3f | Good | 10 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 1m3f | Good to Soft | 4 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 1m3f | Soft | 2 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 1m4f | All goings | 95 | Top 0-2lb | 229 | 14.8% | 0.52 | 1.02 | 1.03 (n=34) | 1.01 (n=61) | MEDIUM |
| 1m4f | All goings | 95 | Upper 3-9lb | 352 | 12.5% | 0.50 | 1.19 | 1.24 (n=31) | 1.17 (n=57) | MEDIUM |
| 1m4f | All goings | 95 | Middle 10-16lb | 161 | 7.5% | 0.49 | 0.72 | 0.61 (n=22) | 0.80 (n=37) | MEDIUM |
| 1m4f | All goings | 95 | Low 17lb+ | 77 | 6.5% | 0.46 | 0.61 | 0.72 (n=14) | 0.55 (n=26) | MEDIUM |
| 1m4f | Good to Firm | 23 | Top 0-2lb | 45 | 15.6% | 0.51 | 0.87 | 1.53 (n=5) | 0.66 (n=18) | LOW |
| 1m4f | Good to Firm | 23 | Upper 3-9lb | 59 | 18.6% | 0.55 | 1.42 | 1.37 (n=3) | 1.43 (n=16) | LOW |
| 1m4f | Good to Firm | 23 | Middle 10-16lb | 34 | 11.8% | 0.47 | 0.86 | 0.00 (n=4) | 1.19 (n=11) | LOW |
| 1m4f | Good to Firm | 23 | Low 17lb+ | 20 | 5.0% | 0.40 | 0.40 | 0.00 (n=2) | 0.45 (n=10) | LOW |
| 1m4f | Good | 36 | Top 0-2lb | 103 | 14.6% | 0.53 | 1.03 | 0.78 (n=13) | 1.16 (n=23) | LOW |
| 1m4f | Good | 36 | Upper 3-9lb | 140 | 10.7% | 0.48 | 1.06 | 0.89 (n=13) | 1.15 (n=22) | LOW |
| 1m4f | Good | 36 | Middle 10-16lb | 51 | 7.8% | 0.49 | 0.86 | 1.53 (n=8) | 0.37 (n=11) | LOW |
| 1m4f | Good | 36 | Low 17lb+ | 24 | 8.3% | 0.52 | 0.76 | 1.45 (n=7) | 0.00 (n=7) | LOW |
| 1m4f | Good to Soft | 15 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 1m4f | Soft | 14 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 1m4f | Heavy | 7 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 1m5½f | All goings | 32 | Top 0-2lb | 61 | 16.4% | 0.51 | 1.16 | 1.30 (n=12) | 1.05 (n=20) | LOW |
| 1m5½f | All goings | 32 | Upper 3-9lb | 75 | 12.0% | 0.44 | 0.94 | 0.88 (n=11) | 0.97 (n=19) | LOW |
| 1m5½f | All goings | 32 | Middle 10-16lb | 70 | 12.9% | 0.50 | 0.89 | 1.16 (n=11) | 0.76 (n=18) | LOW |
| 1m5½f | All goings | 32 | Low 17lb+ | 32 | 15.6% | 0.64 | 1.34 | 0.78 (n=6) | 1.63 (n=10) | LOW |
| 1m5½f | Good to Firm | 11 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 1m5½f | Good | 6 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 1m5½f | Good to Soft | 7 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 1m5½f | Soft | 3 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 1m5½f | Heavy | 5 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 2m | All goings | 13 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 2m | Good to Firm | 6 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 2m | Soft | 3 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 2m | Heavy | 4 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 2m½f | All goings | 14 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 2m½f | Good to Firm | 6 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 2m½f | Good | 5 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 2m½f | Good to Soft | 2 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 2m½f | Soft | 1 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 2m2f | All goings | 1 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 2m2f | Soft | 1 | too few races (under 20) - count only |  |  |  |  |  |  |  |

### d) Favourites

**d) Clear SP favourites by going (joint favourites left out; placed = each-way places: 2 for 5-7 runners, 3 for 8+, 4 in handicaps of 16+, win only under 5)** - counts one clear favourite per race; races 2019-04-12 to 2026-09-19 (954 races; split 2019-21 / 2022-26).
| Going | Races | Favourites won | Win % | Placed % | A/E | £1 SP P/L | A/E 2019-21 | A/E 2022-26 | Level |
|---|---|---|---|---|---|---|---|---|---|
| Good to Firm | 275 | 85 | 33.5% | 60.2% | 1.04 | -32.85 | 1.17 (n=49) | 1.02 (n=205) | HIGH |
| Good | 348 | 90 | 28.0% | 57.8% | 0.90 | -82.76 | 0.88 (n=98) | 0.92 (n=224) | HIGH |
| Good to Soft | 146 | 37 | 28.5% | 61.5% | 0.94 | -29.22 | 0.70 (n=64) | 1.20 (n=66) | MEDIUM |
| Soft | 117 | 26 | 23.6% | 51.8% | 0.76 | -44.99 | 0.97 (n=49) | 0.59 (n=61) | MEDIUM |
| Heavy | 68 | 16 | 26.7% | 51.7% | 0.94 | -13.05 | 0.93 (n=27) | 0.94 (n=33) | MEDIUM |
| **All** | 954 | 254 | 29.0% | 57.9% | 0.94 | -202.87 | 0.91 (n=287) | 0.95 (n=589) | HIGH |

**d) Clear SP favourites by trip** - counts one clear favourite per race; races 2019-04-12 to 2026-09-19 (954 races; split 2019-21 / 2022-26).
| Trip | Races | Favourites won | Win % | Placed % | A/E | £1 SP P/L | A/E 2019-21 | A/E 2022-26 | Level |
|---|---|---|---|---|---|---|---|---|---|
| 5f | 50 | 8 | 17.0% | 46.8% | 0.62 | -21.67 | 0.68 (n=16) | 0.59 (n=31) | LOW |
| 6f | 184 | 46 | 26.9% | 57.9% | 0.90 | -44.83 | 0.90 (n=49) | 0.90 (n=122) | HIGH |
| 6½f | 24 | 10 | 47.6% | 81.0% | 1.41 | +1.53 | 0.77 (n=5) | 1.55 (n=16) | LOW |
| 7f | 223 | 56 | 27.5% | 57.4% | 0.87 | -66.20 | 1.01 (n=70) | 0.79 (n=134) | HIGH |
| 1m | 129 | 32 | 28.3% | 61.1% | 0.93 | -23.73 | 0.91 (n=38) | 0.94 (n=75) | MEDIUM |
| 1m1f | 3 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 1m2f | 163 | 54 | 36.2% | 63.1% | 1.20 | +5.27 | 1.19 (n=49) | 1.21 (n=100) | HIGH |
| 1m3f | 23 | 2 | 9.1% | 40.9% | 0.27 | -18.20 | 0.00 (n=9) | 0.46 (n=13) | LOW |
| 1m4f | 95 | 24 | 26.4% | 52.7% | 0.81 | -29.41 | 0.82 (n=31) | 0.80 (n=60) | MEDIUM |
| 1m5½f | 32 | 9 | 29.0% | 48.4% | 0.86 | -10.03 | 0.74 (n=12) | 0.94 (n=19) | LOW |
| 2m | 13 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 2m½f | 14 | too few races (under 20) - count only |  |  |  |  |  |  |  |
| 2m2f | 1 | too few races (under 20) - count only |  |  |  |  |  |  |  |

### e) Big-priced winners

**e) Winners at 21.00 (20/1) or bigger by going** - counts race winners with an SP; races 2019-04-12 to 2026-09-19 (954 races; split 2019-21 / 2022-26).
| Going | Races | Winners at 21.00+ | % of races | % 2019-21 | % 2022-26 | Level |
|---|---|---|---|---|---|---|
| Good to Firm | 275 | 9 | 3.3% | 0.0% (n=52) | 4.0% (n=223) | HIGH |
| Good | 348 | 28 | 8.0% | 6.5% (n=107) | 8.7% (n=241) | HIGH |
| Good to Soft | 146 | 8 | 5.5% | 1.4% (n=73) | 9.6% (n=73) | MEDIUM |
| Soft | 117 | 9 | 7.7% | 9.8% (n=51) | 6.1% (n=66) | MEDIUM |
| Heavy | 68 | 4 | 5.9% | 6.5% (n=31) | 5.4% (n=37) | MEDIUM |
| All | 954 | 58 | 6.1% | 4.8% (n=314) | 6.7% (n=640) | HIGH |

### f) Claimers

**f) Claimers (INFERRED: a rider's claim is worked out from handicap weights - carried weight + rating gap to the top-rated horse - month by month; checked against the claims printed on our racecards since 23 Sep 2026: 89.9% agreement on 4,875 jockey-days)** - counts rides; races 2019-04-12 to 2026-09-19 (954 races; split 2019-21 / 2022-26).
| Claim | Runners | Wins | Win % | Placed % | A/E | £1 SP P/L | A/E 2019-21 | A/E 2022-26 | Level |
|---|---|---|---|---|---|---|---|---|---|
| No claim | 8390 | 883 | 10.5% | 28.5% | 1.02 | -1075.77 | 1.03 (n=2775) | 1.01 (n=5615) | HIGH |
| 3lb | 306 | 12 | 3.9% | 19.3% | 0.54 | -203.32 | 0.30 (n=87) | 0.64 (n=219) | HIGH |
| 5lb | 405 | 29 | 7.2% | 26.7% | 0.85 | -194.66 | 0.50 (n=137) | 1.00 (n=268) | HIGH |
| 7lb | 323 | 32 | 9.9% | 23.8% | 1.16 | +28.69 | 1.15 (n=129) | 1.17 (n=194) | HIGH |

### g-h) Trainers, jockeys and partnerships

**g) Top 12 trainers here (most wins, 30+ runs)** - counts runs; races 2019-04-12 to 2026-09-19 (954 races; split 2019-21 / 2022-26).
| Trainer | Runs | Wins | Win % | Placed % | A/E | £1 SP P/L | A/E 2019-21 | A/E 2022-26 |
|---|---|---|---|---|---|---|---|---|
| Richard Hannon | 689 | 78 | 11.3% | 29.5% | 1.12 | +62.98 | 1.32 (n=220) | 1.03 (n=469) |
| William Haggas | 302 | 59 | 19.5% | 41.7% | 1.03 | -30.68 | 0.83 (n=88) | 1.12 (n=214) |
| Andrew Balding | 387 | 55 | 14.2% | 40.1% | 1.05 | +42.76 | 1.15 (n=129) | 1.01 (n=258) |
| Ralph Beckett | 264 | 35 | 13.3% | 32.6% | 1.07 | -21.70 | 1.08 (n=75) | 1.07 (n=189) |
| Charlie Appleby | 115 | 34 | 29.6% | 51.3% | 1.10 | -0.64 | 0.99 (n=35) | 1.15 (n=80) |
| Ed Walker | 268 | 34 | 12.7% | 36.2% | 1.05 | -85.76 | 1.12 (n=81) | 1.02 (n=187) |
| John & Thady Gosden | 186 | 31 | 16.7% | 43.5% | 0.89 | -47.36 | 1.10 (n=40) | 0.82 (n=146) |
| Clive Cox | 231 | 22 | 9.5% | 33.8% | 0.92 | -27.25 | 0.87 (n=81) | 0.95 (n=150) |
| Roger Charlton | 98 | 21 | 21.4% | 31.6% | 1.68 | +34.37 | 1.68 (n=98) | - (n=0) |
| Eve Johnson Houghton | 251 | 20 | 8.0% | 28.3% | 0.90 | -70.04 | 1.05 (n=68) | 0.85 (n=183) |
| Owen Burrows | 80 | 19 | 23.8% | 50.0% | 1.45 | +18.81 | 0.53 (n=23) | 1.83 (n=57) |
| Roger Varian | 191 | 17 | 8.9% | 39.3% | 0.57 | -94.18 | 0.79 (n=83) | 0.41 (n=108) |

**g) Top 5 trainers on each going (most wins, 10+ runs on that going)** - counts runs; races 2019-04-12 to 2026-09-19 (954 races; split 2019-21 / 2022-26).
| Going | Trainer | Runs | Wins | Win % | Placed % | A/E | £1 SP P/L | A/E 2019-21 | A/E 2022-26 |
|---|---|---|---|---|---|---|---|---|---|
| Good to Firm | Richard Hannon | 170 | 21 | 12.4% | 31.2% | 1.21 | -23.59 | 1.92 (n=34) | 1.05 (n=136) |
| Good to Firm | Ed Walker | 82 | 13 | 15.9% | 36.6% | 1.10 | -27.21 | 3.15 (n=10) | 0.92 (n=72) |
| Good to Firm | Andrew Balding | 87 | 13 | 14.9% | 43.7% | 0.95 | -16.21 | 0.00 (n=14) | 1.07 (n=73) |
| Good to Firm | William Haggas | 61 | 12 | 19.7% | 50.8% | 0.90 | -17.38 | 0.84 (n=10) | 0.91 (n=51) |
| Good to Firm | Eve Johnson Houghton | 86 | 9 | 10.5% | 26.7% | 0.99 | -1.25 | 0.58 (n=13) | 1.09 (n=73) |
| Good | Richard Hannon | 285 | 32 | 11.2% | 27.7% | 1.19 | -39.03 | 1.84 (n=89) | 0.82 (n=196) |
| Good | Andrew Balding | 180 | 25 | 13.9% | 40.6% | 1.08 | +86.41 | 1.36 (n=52) | 0.97 (n=128) |
| Good | William Haggas | 118 | 22 | 18.6% | 35.6% | 1.07 | -15.03 | 1.12 (n=36) | 1.04 (n=82) |
| Good | John & Thady Gosden | 107 | 19 | 17.8% | 44.9% | 0.97 | -9.97 | 1.18 (n=25) | 0.89 (n=82) |
| Good | Charlie Appleby | 52 | 16 | 30.8% | 50.0% | 1.16 | +4.35 | 2.03 (n=10) | 1.01 (n=42) |
| Good to Soft | Richard Hannon | 119 | 14 | 11.8% | 34.5% | 1.06 | +137.88 | 0.51 (n=50) | 1.52 (n=69) |
| Good to Soft | William Haggas | 54 | 12 | 22.2% | 35.2% | 1.22 | +18.33 | 0.24 (n=20) | 1.94 (n=34) |
| Good to Soft | Andrew Balding | 60 | 10 | 16.7% | 40.0% | 1.32 | -2.43 | 1.60 (n=34) | 0.94 (n=26) |
| Good to Soft | Roger Charlton | 15 | 6 | 40.0% | 53.3% | 2.82 | +17.75 | 2.82 (n=15) | - (n=0) |
| Good to Soft | Charlie Appleby | 24 | 6 | 25.0% | 62.5% | 0.91 | -3.51 | 0.59 (n=13) | 1.26 (n=11) |
| Soft | William Haggas | 39 | 11 | 28.2% | 56.4% | 1.50 | +6.40 | 1.63 (n=9) | 1.46 (n=30) |
| Soft | Ralph Beckett | 40 | 8 | 20.0% | 40.0% | 1.53 | +7.91 | 0.94 (n=12) | 1.68 (n=28) |
| Soft | Richard Hannon | 73 | 8 | 11.0% | 28.8% | 0.97 | +10.23 | 0.84 (n=28) | 1.03 (n=45) |
| Soft | Roger Charlton | 18 | 5 | 27.8% | 50.0% | 2.01 | +14.75 | 2.01 (n=18) | - (n=0) |
| Soft | Charlie Appleby | 14 | 4 | 28.6% | 42.9% | 0.86 | -3.47 | 0.72 (n=8) | 1.05 (n=6) |
| Heavy | Ralph Beckett | 42 | 10 | 23.8% | 45.2% | 1.65 | +46.98 | 1.45 (n=14) | 1.75 (n=28) |
| Heavy | Hughie Morrison | 19 | 4 | 21.1% | 31.6% | 2.11 | +26.75 | 1.46 (n=13) | 3.85 (n=6) |
| Heavy | Roger Charlton | 14 | 3 | 21.4% | 21.4% | 2.06 | +15.25 | 2.06 (n=14) | - (n=0) |
| Heavy | Ed Walker | 15 | 3 | 20.0% | 46.7% | 1.54 | +5.50 | 2.66 (n=8) | 0.00 (n=7) |
| Heavy | Eve Johnson Houghton | 17 | 3 | 17.6% | 41.2% | 1.82 | -4.79 | 1.94 (n=8) | 1.76 (n=9) |

**g) Top 12 jockeys here (most wins, 30+ runs)** - counts runs; races 2019-04-12 to 2026-09-19 (954 races; split 2019-21 / 2022-26).
| Jockey | Runs | Wins | Win % | Placed % | A/E | £1 SP P/L | A/E 2019-21 | A/E 2022-26 |
|---|---|---|---|---|---|---|---|---|
| Tom Marquand | 397 | 66 | 16.6% | 36.5% | 1.21 | +4.16 | 1.14 (n=107) | 1.23 (n=290) |
| Oisin Murphy | 343 | 64 | 18.7% | 43.7% | 1.13 | +11.45 | 1.17 (n=142) | 1.11 (n=201) |
| William Buick | 298 | 59 | 19.8% | 38.3% | 1.06 | -6.53 | 1.02 (n=72) | 1.07 (n=226) |
| Sean Levey | 337 | 36 | 10.7% | 28.2% | 1.02 | -10.39 | 1.63 (n=89) | 0.82 (n=248) |
| James Doyle | 217 | 35 | 16.1% | 35.0% | 1.06 | -27.69 | 1.09 (n=116) | 1.03 (n=101) |
| Jim Crowley | 234 | 35 | 15.0% | 33.8% | 1.06 | +4.72 | 0.98 (n=114) | 1.14 (n=120) |
| Rossa Ryan | 269 | 29 | 10.8% | 33.5% | 0.93 | -20.52 | 0.60 (n=54) | 1.00 (n=215) |
| David Probert | 318 | 28 | 8.8% | 25.2% | 1.00 | +21.12 | 1.12 (n=117) | 0.95 (n=201) |
| Jason Watson | 197 | 26 | 13.2% | 30.5% | 1.34 | -1.38 | 1.80 (n=105) | 0.65 (n=92) |
| Pat Dobbs | 201 | 26 | 12.9% | 30.8% | 1.37 | +26.47 | 1.29 (n=56) | 1.39 (n=145) |
| David Egan | 219 | 25 | 11.4% | 27.4% | 1.08 | -33.18 | 0.83 (n=73) | 1.22 (n=146) |
| Hector Crouch | 174 | 24 | 13.8% | 32.8% | 1.35 | -1.88 | 0.44 (n=25) | 1.48 (n=149) |

**g) Top 5 jockeys on each going (most wins, 10+ runs on that going)** - counts runs; races 2019-04-12 to 2026-09-19 (954 races; split 2019-21 / 2022-26).
| Going | Jockey | Runs | Wins | Win % | Placed % | A/E | £1 SP P/L | A/E 2019-21 | A/E 2022-26 |
|---|---|---|---|---|---|---|---|---|---|
| Good to Firm | Oisin Murphy | 88 | 21 | 23.9% | 47.7% | 1.18 | +12.43 | 1.09 (n=21) | 1.20 (n=67) |
| Good to Firm | William Buick | 84 | 19 | 22.6% | 34.5% | 1.28 | -0.63 | 0.60 (n=12) | 1.36 (n=72) |
| Good to Firm | Tom Marquand | 103 | 16 | 15.5% | 42.7% | 1.00 | -36.21 | 1.23 (n=22) | 0.96 (n=81) |
| Good to Firm | Sean Levey | 81 | 13 | 16.0% | 33.3% | 1.23 | +10.19 | 2.90 (n=13) | 0.91 (n=68) |
| Good to Firm | Hollie Doyle | 69 | 10 | 14.5% | 31.9% | 1.21 | -17.97 | 1.02 (n=14) | 1.27 (n=55) |
| Good | William Buick | 123 | 24 | 19.5% | 37.4% | 1.08 | -4.51 | 1.41 (n=38) | 0.98 (n=85) |
| Good | Oisin Murphy | 141 | 23 | 16.3% | 41.8% | 1.08 | +11.59 | 1.20 (n=64) | 0.99 (n=77) |
| Good | Jim Crowley | 99 | 19 | 19.2% | 38.4% | 1.26 | +11.73 | 1.12 (n=50) | 1.43 (n=49) |
| Good | Tom Marquand | 140 | 17 | 12.1% | 27.1% | 0.94 | -56.58 | 0.90 (n=35) | 0.95 (n=105) |
| Good | James Doyle | 84 | 15 | 17.9% | 32.1% | 1.35 | +3.50 | 1.44 (n=46) | 1.23 (n=38) |
| Good to Soft | Tom Marquand | 72 | 17 | 23.6% | 40.3% | 2.02 | +72.75 | 0.57 (n=19) | 2.41 (n=53) |
| Good to Soft | Oisin Murphy | 66 | 11 | 16.7% | 37.9% | 1.08 | -17.03 | 1.29 (n=38) | 0.75 (n=28) |
| Good to Soft | William Buick | 55 | 9 | 16.4% | 41.8% | 0.89 | +9.62 | 0.39 (n=11) | 1.06 (n=44) |
| Good to Soft | Jason Watson | 28 | 6 | 21.4% | 32.1% | 2.59 | +15.50 | 3.12 (n=24) | 0.00 (n=4) |
| Good to Soft | Pat Dobbs | 39 | 6 | 15.4% | 33.3% | 1.41 | +37.00 | 0.53 (n=17) | 2.12 (n=22) |
| Soft | Tom Marquand | 53 | 13 | 24.5% | 41.5% | 1.84 | +30.70 | 1.45 (n=25) | 2.09 (n=28) |
| Soft | James Doyle | 41 | 8 | 19.5% | 36.6% | 1.32 | +10.96 | 1.25 (n=20) | 1.40 (n=21) |
| Soft | William Buick | 27 | 6 | 22.2% | 48.1% | 0.90 | -5.00 | 0.97 (n=8) | 0.87 (n=19) |
| Soft | Rossa Ryan | 30 | 6 | 20.0% | 43.3% | 1.55 | +12.12 | 1.75 (n=5) | 1.51 (n=25) |
| Soft | Pat Dobbs | 16 | 5 | 31.2% | 43.8% | 2.46 | +24.23 | 0.00 (n=1) | 2.53 (n=15) |
| Heavy | Oisin Murphy | 10 | 5 | 50.0% | 70.0% | 2.53 | +16.00 | - (n=0) | 2.53 (n=10) |
| Heavy | Rob Hornby | 25 | 4 | 16.0% | 32.0% | 1.70 | +20.25 | 1.47 (n=20) | 3.30 (n=5) |
| Heavy | Charles Bishop | 20 | 3 | 15.0% | 30.0% | 1.76 | -7.79 | 1.88 (n=9) | 1.71 (n=11) |
| Heavy | Hector Crouch | 20 | 3 | 15.0% | 35.0% | 1.21 | -6.90 | 0.00 (n=5) | 1.35 (n=15) |
| Heavy | James Doyle | 26 | 3 | 11.5% | 42.3% | 0.74 | -11.75 | 0.42 (n=15) | 1.19 (n=11) |

**h) Top 10 trainer-jockey partnerships here (most wins, 20+ runs together)** - counts runs; races 2019-04-12 to 2026-09-19 (954 races; split 2019-21 / 2022-26).
| Trainer | Jockey | Runs | Wins | Win % | A/E | £1 SP P/L | A/E 2019-21 | A/E 2022-26 |
|---|---|---|---|---|---|---|---|---|
| William Haggas | Tom Marquand | 185 | 44 | 23.8% | 1.28 | +20.62 | 1.34 (n=37) | 1.27 (n=148) |
| Charlie Appleby | William Buick | 81 | 27 | 33.3% | 1.14 | -1.03 | 0.98 (n=16) | 1.18 (n=65) |
| Andrew Balding | Oisin Murphy | 127 | 26 | 20.5% | 1.11 | -0.08 | 1.31 (n=43) | 1.03 (n=84) |
| Richard Hannon | Sean Levey | 219 | 26 | 11.9% | 1.08 | -20.38 | 1.73 (n=65) | 0.82 (n=154) |
| Richard Hannon | Pat Dobbs | 161 | 25 | 15.5% | 1.51 | +60.47 | 1.45 (n=40) | 1.53 (n=121) |
| Eve Johnson Houghton | Charles Bishop | 174 | 15 | 8.6% | 0.91 | -36.04 | 1.26 (n=48) | 0.80 (n=126) |
| Roger Charlton | Jason Watson | 59 | 14 | 23.7% | 1.94 | +36.53 | 1.94 (n=59) | - (n=0) |
| Ralph Beckett | Rossa Ryan | 79 | 11 | 13.9% | 0.92 | +2.33 | 1.14 (n=7) | 0.90 (n=72) |
| John & Thady Gosden | Frankie Dettori | 35 | 9 | 25.7% | 1.13 | -4.49 | 1.77 (n=13) | 0.66 (n=22) |
| Ralph Beckett | Hector Crouch | 59 | 9 | 15.3% | 1.26 | -4.65 | 1.78 (n=4) | 1.21 (n=55) |

### j) Going pace

**j) Going pace: winners' times against the ZANS standard time for this track and trip (+ = slower than standard; the standard is a class-par time, so most winners run a few seconds over it - compare goings, not the raw number)** - counts race winners with a recorded time; races 2019-04-12 to 2026-09-19 (954 races; split 2019-21 / 2022-26).
| Trip | Going | Races timed | Mean secs off standard | Per furlong | Median | Mean 2019-21 | Mean 2022-26 | Level |
|---|---|---|---|---|---|---|---|---|
| 5f | All goings | 50 | +1.54 | +0.31 | +1.13 | +1.90 (n=17) | +1.35 (n=33) | LOW |
| 5f | Good to Firm | 18 | too few races (under 20) - count only |  |  |  |  |  |
| 5f | Good | 17 | too few races (under 20) - count only |  |  |  |  |  |
| 5f | Good to Soft | 8 | too few races (under 20) - count only |  |  |  |  |  |
| 5f | Soft | 5 | too few races (under 20) - count only |  |  |  |  |  |
| 5f | Heavy | 2 | too few races (under 20) - count only |  |  |  |  |  |
| 6f | All goings | 184 | +2.11 | +0.35 | +1.92 | +2.85 (n=54) | +1.80 (n=130) | HIGH |
| 6f | Good to Firm | 62 | +0.90 | +0.15 | +0.70 | +1.63 (n=12) | +0.72 (n=50) | MEDIUM |
| 6f | Good | 70 | +1.50 | +0.25 | +1.39 | +1.23 (n=17) | +1.59 (n=53) | MEDIUM |
| 6f | Good to Soft | 31 | +3.48 | +0.58 | +3.35 | +3.85 (n=18) | +2.98 (n=13) | LOW |
| 6f | Soft | 11 | too few races (under 20) - count only |  |  |  |  |  |
| 6f | Heavy | 10 | too few races (under 20) - count only |  |  |  |  |  |
| 6½f | All goings | 24 | +3.32 | +0.51 | +2.57 | +6.19 (n=5) | +2.57 (n=19) | LOW |
| 6½f | Good to Firm | 8 | too few races (under 20) - count only |  |  |  |  |  |
| 6½f | Good | 4 | too few races (under 20) - count only |  |  |  |  |  |
| 6½f | Good to Soft | 4 | too few races (under 20) - count only |  |  |  |  |  |
| 6½f | Soft | 4 | too few races (under 20) - count only |  |  |  |  |  |
| 6½f | Heavy | 4 | too few races (under 20) - count only |  |  |  |  |  |
| 7f | All goings | 224 | +2.78 | +0.40 | +2.22 | +2.99 (n=76) | +2.68 (n=148) | HIGH |
| 7f | Good to Firm | 59 | +1.11 | +0.16 | +1.12 | +1.54 (n=8) | +1.04 (n=51) | LOW |
| 7f | Good | 83 | +1.58 | +0.23 | +1.34 | +1.35 (n=33) | +1.73 (n=50) | MEDIUM |
| 7f | Good to Soft | 32 | +3.56 | +0.51 | +3.20 | +3.52 (n=15) | +3.60 (n=17) | LOW |
| 7f | Soft | 35 | +5.55 | +0.79 | +5.21 | +4.61 (n=15) | +6.26 (n=20) | LOW |
| 7f | Heavy | 15 | too few races (under 20) - count only |  |  |  |  |  |
| 1m | All goings | 129 | +3.46 | +0.43 | +2.40 | +4.73 (n=46) | +2.76 (n=83) | MEDIUM |
| 1m | Good to Firm | 29 | +1.10 | +0.14 | +1.11 | +1.70 (n=7) | +0.91 (n=22) | LOW |
| 1m | Good | 51 | +1.28 | +0.16 | +1.33 | +1.27 (n=14) | +1.28 (n=37) | LOW |
| 1m | Good to Soft | 22 | +4.33 | +0.54 | +4.27 | +4.53 (n=13) | +4.04 (n=9) | LOW |
| 1m | Soft | 16 | too few races (under 20) - count only |  |  |  |  |  |
| 1m | Heavy | 11 | too few races (under 20) - count only |  |  |  |  |  |
| 1m2f | All goings | 164 | +3.55 | +0.36 | +2.56 | +5.19 (n=52) | +2.79 (n=112) | HIGH |
| 1m2f | Good to Firm | 46 | +0.99 | +0.10 | +0.78 | +1.98 (n=13) | +0.59 (n=33) | LOW |
| 1m2f | Good | 67 | +1.99 | +0.20 | +1.81 | +3.05 (n=16) | +1.66 (n=51) | MEDIUM |
| 1m2f | Good to Soft | 21 | +4.92 | +0.49 | +4.60 | +5.92 (n=8) | +4.30 (n=13) | LOW |
| 1m2f | Soft | 20 | +8.93 | +0.89 | +9.69 | +8.01 (n=10) | +9.85 (n=10) | LOW |
| 1m2f | Heavy | 10 | too few races (under 20) - count only |  |  |  |  |  |
| 1m3f | All goings | 23 | +2.10 | +0.19 | +0.62 | +2.84 (n=9) | +1.61 (n=14) | LOW |
| 1m3f | Good to Firm | 7 | too few races (under 20) - count only |  |  |  |  |  |
| 1m3f | Good | 10 | too few races (under 20) - count only |  |  |  |  |  |
| 1m3f | Good to Soft | 4 | too few races (under 20) - count only |  |  |  |  |  |
| 1m3f | Soft | 2 | too few races (under 20) - count only |  |  |  |  |  |
| 1m4f | All goings | 95 | +4.81 | +0.40 | +2.81 | +5.84 (n=34) | +4.24 (n=61) | MEDIUM |
| 1m4f | Good to Firm | 23 | +1.39 | +0.12 | +1.18 | +1.19 (n=5) | +1.44 (n=18) | LOW |
| 1m4f | Good | 36 | +1.80 | +0.15 | +1.85 | +2.50 (n=13) | +1.41 (n=23) | LOW |
| 1m4f | Good to Soft | 15 | too few races (under 20) - count only |  |  |  |  |  |
| 1m4f | Soft | 14 | too few races (under 20) - count only |  |  |  |  |  |
| 1m4f | Heavy | 7 | too few races (under 20) - count only |  |  |  |  |  |
| 1m5½f | All goings | 33 | +5.33 | +0.39 | +4.24 | +8.48 (n=13) | +3.29 (n=20) | LOW |
| 1m5½f | Good to Firm | 11 | too few races (under 20) - count only |  |  |  |  |  |
| 1m5½f | Good | 6 | too few races (under 20) - count only |  |  |  |  |  |
| 1m5½f | Good to Soft | 8 | too few races (under 20) - count only |  |  |  |  |  |
| 1m5½f | Soft | 3 | too few races (under 20) - count only |  |  |  |  |  |
| 1m5½f | Heavy | 5 | too few races (under 20) - count only |  |  |  |  |  |
| 2m½f | All goings | 14 | too few races (under 20) - count only |  |  |  |  |  |
| 2m½f | Good to Firm | 6 | too few races (under 20) - count only |  |  |  |  |  |
| 2m½f | Good | 5 | too few races (under 20) - count only |  |  |  |  |  |
| 2m½f | Good to Soft | 2 | too few races (under 20) - count only |  |  |  |  |  |
| 2m½f | Soft | 1 | too few races (under 20) - count only |  |  |  |  |  |

### k) Method rule tests by going

**k) Method rule tests split by exact going (flagged runners only, rows with 60+ runners; same rules as the full table below)** - counts runners each rule flags, judged only on what was known before the race; races 2019-04-12 to 2026-09-19 (954 races; split 2019-21 / 2022-26).
| Rule | Going | Runners | Win % | A/E | £1 return | A/E 2019-21 | A/E 2022-26 |
|---|---|---|---|---|---|---|---|
| 3yo v older horses, August (weight-for-age) | Good to Firm | 85 | 15.3% | 1.10 | -18% | - (n=0) | 1.10 (n=85) |
| 3yo v older horses, other months | Good to Firm | 238 | 12.6% | 0.92 | -21% | 0.60 (n=57) | 1.02 (n=181) |
| 3yo v older horses, other months | Good | 193 | 12.4% | 1.00 | -18% | 1.18 (n=66) | 0.91 (n=127) |
| 3yo v older horses, other months | Good to Soft | 112 | 10.7% | 0.87 | -24% | 0.76 (n=47) | 0.97 (n=65) |
| 3yo v older horses, other months | Soft | 100 | 17.0% | 1.33 | -23% | 1.37 (n=12) | 1.32 (n=88) |
| 3yo v older horses, other months | Heavy | 109 | 9.2% | 0.83 | -37% | 0.80 (n=61) | 0.87 (n=48) |
| Bend Control Law: drawn 7+ at 7f | Good to Firm | 250 | 9.6% | 1.09 | -27% | 0.91 (n=26) | 1.12 (n=224) |
| Bend Control Law: drawn 7+ at 7f | Good | 447 | 9.8% | 1.24 | +43% | 1.09 (n=158) | 1.32 (n=289) |
| Bend Control Law: drawn 7+ at 7f | Good to Soft | 154 | 11.0% | 1.41 | +76% | 1.09 (n=69) | 1.67 (n=85) |
| Bend Control Law: drawn 7+ at 7f | Soft | 165 | 7.9% | 0.81 | -36% | 1.05 (n=76) | 0.60 (n=89) |
| Bend Control Law: drawn 7+ at 7f | Heavy | 100 | 5.0% | 0.63 | -69% | 0.59 (n=61) | 0.66 (n=39) |
| Course & distance winner (+-1f) | Good to Firm | 159 | 11.3% | 0.90 | -12% | 1.54 (n=12) | 0.83 (n=147) |
| Course & distance winner (+-1f) | Good | 187 | 11.8% | 1.00 | -10% | 1.24 (n=51) | 0.89 (n=136) |
| Course & distance winner (+-1f) | Good to Soft | 82 | 9.8% | 0.77 | -52% | 0.69 (n=39) | 0.87 (n=43) |
| Course & distance winner (+-1f) | Soft | 69 | 11.6% | 0.93 | +4% | 1.03 (n=18) | 0.90 (n=51) |
| Course winner | Good to Firm | 191 | 13.6% | 0.99 | -9% | 1.33 (n=16) | 0.95 (n=175) |
| Course winner | Good | 248 | 9.7% | 0.82 | -29% | 0.94 (n=69) | 0.77 (n=179) |
| Course winner | Good to Soft | 104 | 9.6% | 0.76 | -52% | 0.83 (n=50) | 0.68 (n=54) |
| Course winner | Soft | 91 | 14.3% | 1.05 | +13% | 1.72 (n=28) | 0.72 (n=63) |
| Favourite (any race) | Good to Firm | 294 | 30.3% | 1.00 | -16% | 1.19 (n=55) | 0.96 (n=239) |
| Favourite (any race) | Good | 372 | 26.3% | 0.90 | -25% | 0.87 (n=117) | 0.91 (n=255) |
| Favourite (any race) | Good to Soft | 159 | 26.4% | 0.94 | -24% | 0.72 (n=81) | 1.18 (n=78) |
| Favourite (any race) | Soft | 123 | 23.6% | 0.78 | -38% | 1.03 (n=53) | 0.59 (n=70) |
| Favourite (any race) | Heavy | 76 | 27.6% | 1.03 | -12% | 1.00 (n=35) | 1.06 (n=41) |
| HR1 unproven at trip (never ran within 1f) | Good to Firm | 134 | 11.9% | 0.81 | -41% | 0.83 (n=33) | 0.80 (n=101) |
| HR1 unproven at trip (never ran within 1f) | Good | 299 | 11.0% | 1.05 | -31% | 0.80 (n=84) | 1.15 (n=215) |
| HR1 unproven at trip (never ran within 1f) | Good to Soft | 125 | 10.4% | 1.01 | -3% | 1.44 (n=52) | 0.68 (n=73) |
| HR1 unproven at trip (never ran within 1f) | Soft | 89 | 12.4% | 1.00 | -24% | 1.43 (n=42) | 0.56 (n=47) |
| HR3 first-time jockey pairing (has run before) | Good to Firm | 919 | 12.0% | 1.08 | -17% | 1.13 (n=210) | 1.06 (n=709) |
| HR3 first-time jockey pairing (has run before) | Good | 1417 | 8.8% | 0.99 | -2% | 1.03 (n=417) | 0.98 (n=1000) |
| HR3 first-time jockey pairing (has run before) | Good to Soft | 580 | 7.9% | 0.89 | -36% | 1.05 (n=286) | 0.73 (n=294) |
| HR3 first-time jockey pairing (has run before) | Soft | 406 | 8.9% | 0.83 | -40% | 0.84 (n=174) | 0.83 (n=232) |
| HR3 first-time jockey pairing (has run before) | Heavy | 279 | 10.4% | 1.07 | -22% | 0.90 (n=146) | 1.24 (n=133) |
| HR4 jockey 12-month strike rate under 6% | Good to Firm | 77 | 9.1% | 1.40 | +21% | 0.00 (n=20) | 1.68 (n=57) |
| HR4 jockey 12-month strike rate under 6% | Good | 121 | 5.8% | 1.47 | -36% | 1.29 (n=35) | 1.55 (n=86) |
| HR4 jockey 12-month strike rate under 6% | Good to Soft | 81 | 7.4% | 1.43 | -58% | 1.70 (n=50) | 1.08 (n=31) |
| HR5 age 6+ | Good to Firm | 289 | 9.0% | 0.92 | -21% | 0.63 (n=42) | 0.96 (n=247) |
| HR5 age 6+ | Good | 320 | 7.5% | 1.14 | +8% | 1.15 (n=91) | 1.13 (n=229) |
| HR5 age 6+ | Good to Soft | 177 | 10.7% | 1.57 | +1% | 1.67 (n=98) | 1.42 (n=79) |
| HR5 age 6+ | Soft | 134 | 7.5% | 0.85 | +8% | 0.70 (n=65) | 1.01 (n=69) |
| HR5 age 6+ | Heavy | 89 | 14.6% | 1.60 | +51% | 1.94 (n=45) | 1.32 (n=44) |
| HR5 age 6+ with no win/2nd in last 3 runs | Good to Firm | 136 | 7.4% | 0.97 | -16% | 0.00 (n=19) | 1.08 (n=117) |
| HR5 age 6+ with no win/2nd in last 3 runs | Good | 144 | 6.2% | 1.18 | +15% | 0.85 (n=42) | 1.34 (n=102) |
| HR5 age 6+ with no win/2nd in last 3 runs | Good to Soft | 86 | 10.5% | 1.76 | +8% | 1.70 (n=55) | 1.89 (n=31) |
| HR5 age 6+ with no win/2nd in last 3 runs | Soft | 64 | 7.8% | 1.04 | +45% | 1.00 (n=36) | 1.10 (n=28) |
| HR6 weakened / no extra in either of last 2 runs | Good to Firm | 864 | 10.6% | 1.10 | -5% | 1.12 (n=120) | 1.10 (n=744) |
| HR6 weakened / no extra in either of last 2 runs | Good | 991 | 8.6% | 1.17 | -1% | 0.95 (n=219) | 1.23 (n=772) |
| HR6 weakened / no extra in either of last 2 runs | Good to Soft | 408 | 7.8% | 0.99 | +10% | 0.98 (n=166) | 0.99 (n=242) |
| HR6 weakened / no extra in either of last 2 runs | Soft | 293 | 8.5% | 0.98 | -27% | 1.07 (n=107) | 0.93 (n=186) |
| HR6 weakened / no extra in either of last 2 runs | Heavy | 185 | 8.6% | 1.06 | -10% | 1.58 (n=86) | 0.75 (n=99) |
| Improver: last RPR above its previous best | Good to Firm | 366 | 20.2% | 1.25 | -2% | 1.27 (n=70) | 1.24 (n=296) |
| Improver: last RPR above its previous best | Good | 575 | 12.9% | 1.00 | -26% | 0.90 (n=192) | 1.05 (n=383) |
| Improver: last RPR above its previous best | Good to Soft | 218 | 12.8% | 1.01 | -23% | 1.22 (n=108) | 0.80 (n=110) |
| Improver: last RPR above its previous best | Soft | 161 | 11.2% | 0.79 | -49% | 0.74 (n=65) | 0.83 (n=96) |
| Improver: last RPR above its previous best | Heavy | 105 | 15.2% | 1.07 | -13% | 0.94 (n=45) | 1.17 (n=60) |
| Lightly raced (5 or fewer runs of this code) | Good to Firm | 879 | 12.1% | 1.01 | -15% | 1.13 (n=190) | 0.98 (n=689) |
| Lightly raced (5 or fewer runs of this code) | Good | 1615 | 11.7% | 1.11 | +8% | 1.10 (n=518) | 1.11 (n=1097) |
| Lightly raced (5 or fewer runs of this code) | Good to Soft | 630 | 11.9% | 1.05 | -6% | 1.09 (n=324) | 1.00 (n=306) |
| Lightly raced (5 or fewer runs of this code) | Soft | 376 | 12.5% | 0.99 | -23% | 1.20 (n=173) | 0.78 (n=203) |
| Lightly raced (5 or fewer runs of this code) | Heavy | 246 | 10.6% | 0.92 | -49% | 1.01 (n=121) | 0.84 (n=125) |
| Lone front-runner (only habitual leader in race) | Good to Firm | 67 | 13.4% | 0.89 | -18% | 0.00 (n=13) | 1.06 (n=54) |
| Lone front-runner (only habitual leader in race) | Good | 93 | 10.8% | 1.07 | -42% | 1.26 (n=23) | 1.01 (n=70) |
| Low draw (1-4) on good or firmer | Good to Firm | 996 | 12.2% | 0.93 | -20% | 0.89 (n=198) | 0.94 (n=798) |
| Low draw (1-4) on good or firmer | Good | 1289 | 10.9% | 1.01 | -15% | 0.99 (n=403) | 1.02 (n=886) |
| Position Race Mandate: usually held up, race up to 7.5f, <2 front-runners | Good to Firm | 241 | 12.0% | 1.10 | -10% | 1.11 (n=34) | 1.10 (n=207) |
| Position Race Mandate: usually held up, race up to 7.5f, <2 front-runners | Good | 227 | 11.9% | 1.10 | +11% | 0.83 (n=75) | 1.25 (n=152) |
| Position Race Mandate: usually held up, race up to 7.5f, <2 front-runners | Good to Soft | 121 | 13.2% | 1.21 | -7% | 0.94 (n=64) | 1.46 (n=57) |
| Position Race Mandate: usually held up, race up to 7.5f, <2 front-runners | Soft | 68 | 10.3% | 0.92 | -11% | 0.91 (n=26) | 0.93 (n=42) |
| Rule 5.1 ground exclusivity (won on exact going; 1-2 in field have) | Good to Firm | 110 | 20.0% | 1.12 | -10% | 0.83 (n=27) | 1.22 (n=83) |
| Rule 5.1 ground exclusivity (won on exact going; 1-2 in field have) | Good | 133 | 14.3% | 0.98 | -24% | 0.68 (n=64) | 1.22 (n=69) |
| Rule 5.1 ground exclusivity (won on exact going; 1-2 in field have) | Good to Soft | 66 | 7.6% | 0.68 | -30% | 1.16 (n=31) | 0.26 (n=35) |
| Stamina Crossover: has run over jumps, flat 1m+ on yielding or softer | Good to Soft | 67 | 7.5% | 0.98 | -54% | 0.90 (n=38) | 1.04 (n=29) |
| Stamina Crossover: has run over jumps, flat 1m+ on yielding or softer | Heavy | 60 | 15.0% | 1.82 | +41% | 1.89 (n=29) | 1.76 (n=31) |
| Start risk: slow away 2+ of last 4, race up to 1m | Good to Firm | 97 | 11.3% | 1.08 | -19% | 0.76 (n=15) | 1.13 (n=82) |
| Start risk: slow away 2+ of last 4, race up to 1m | Good | 119 | 9.2% | 1.04 | +33% | 0.90 (n=33) | 1.11 (n=86) |
| Temperament: keen / hung in either of last 2 runs | Good to Firm | 790 | 12.9% | 1.09 | -14% | 1.34 (n=120) | 1.04 (n=670) |
| Temperament: keen / hung in either of last 2 runs | Good | 1100 | 10.3% | 1.07 | -1% | 1.17 (n=287) | 1.03 (n=813) |
| Temperament: keen / hung in either of last 2 runs | Good to Soft | 411 | 10.0% | 0.93 | -27% | 0.85 (n=169) | 0.99 (n=242) |
| Temperament: keen / hung in either of last 2 runs | Soft | 287 | 9.8% | 0.90 | -23% | 1.07 (n=107) | 0.80 (n=180) |
| Temperament: keen / hung in either of last 2 runs | Heavy | 203 | 10.8% | 0.97 | -12% | 1.00 (n=75) | 0.96 (n=128) |
| Top EXACT-conditions RPR (trip +-1f + same going) | Good to Firm | 264 | 23.1% | 1.29 | +15% | 1.62 (n=49) | 1.21 (n=215) |
| Top EXACT-conditions RPR (trip +-1f + same going) | Good | 314 | 13.1% | 0.85 | -36% | 0.88 (n=97) | 0.83 (n=217) |
| Top EXACT-conditions RPR (trip +-1f + same going) | Good to Soft | 99 | 8.1% | 0.66 | -49% | 0.88 (n=51) | 0.38 (n=48) |
| Top EXACT-conditions RPR (trip +-1f + same going) | Soft | 87 | 9.2% | 0.62 | -46% | 0.78 (n=34) | 0.52 (n=53) |
| Top recent RPR in race (best of last 3) | Good to Firm | 300 | 23.7% | 1.11 | +3% | 1.12 (n=56) | 1.11 (n=244) |
| Top recent RPR in race (best of last 3) | Good | 363 | 19.8% | 1.01 | -0% | 0.93 (n=115) | 1.04 (n=248) |
| Top recent RPR in race (best of last 3) | Good to Soft | 157 | 23.6% | 1.13 | +1% | 0.87 (n=82) | 1.46 (n=75) |
| Top recent RPR in race (best of last 3) | Soft | 119 | 15.1% | 0.75 | -44% | 0.89 (n=50) | 0.65 (n=69) |
| Top recent RPR in race (best of last 3) | Heavy | 73 | 21.9% | 1.17 | +7% | 1.52 (n=33) | 0.90 (n=40) |
| Usual front-runner (led in half of last 6) | Good to Firm | 150 | 12.0% | 0.95 | +0% | 0.78 (n=35) | 0.99 (n=115) |
| Usual front-runner (led in half of last 6) | Good | 218 | 10.6% | 1.17 | -15% | 1.22 (n=62) | 1.15 (n=156) |
| Usual front-runner (led in half of last 6) | Good to Soft | 92 | 7.6% | 0.83 | -61% | 1.07 (n=42) | 0.64 (n=50) |
| Usual front-runner (led in half of last 6) | Soft | 78 | 14.1% | 1.46 | +28% | 1.77 (n=34) | 1.21 (n=44) |
| Usually held up | Good to Firm | 607 | 11.7% | 1.00 | -21% | 1.13 (n=120) | 0.97 (n=487) |
| Usually held up | Good | 863 | 9.4% | 0.97 | -16% | 1.01 (n=265) | 0.94 (n=598) |
| Usually held up | Good to Soft | 389 | 11.3% | 1.15 | -19% | 1.10 (n=211) | 1.21 (n=178) |
| Usually held up | Soft | 284 | 12.0% | 1.16 | -1% | 0.99 (n=126) | 1.29 (n=158) |
| Usually held up | Heavy | 176 | 8.0% | 0.76 | -51% | 0.80 (n=86) | 0.73 (n=90) |
| Usually prominent | Good to Firm | 1067 | 12.2% | 1.02 | -18% | 0.94 (n=189) | 1.04 (n=878) |
| Usually prominent | Good | 1468 | 10.3% | 1.05 | -11% | 0.95 (n=425) | 1.10 (n=1043) |
| Usually prominent | Good to Soft | 583 | 9.4% | 0.95 | -7% | 0.88 (n=257) | 1.00 (n=326) |
| Usually prominent | Soft | 401 | 10.0% | 0.89 | -30% | 1.04 (n=154) | 0.79 (n=247) |
| Usually prominent | Heavy | 257 | 10.9% | 1.04 | -1% | 1.26 (n=107) | 0.91 (n=150) |
| Won last time | Good to Firm | 300 | 20.7% | 1.17 | -9% | 1.35 (n=56) | 1.11 (n=244) |
| Won last time | Good | 536 | 14.4% | 1.05 | -15% | 1.15 (n=179) | 1.00 (n=357) |
| Won last time | Good to Soft | 211 | 15.6% | 1.09 | -1% | 1.17 (n=123) | 0.96 (n=88) |
| Won last time | Soft | 146 | 11.6% | 0.72 | -54% | 0.63 (n=60) | 0.78 (n=86) |
| Won last time | Heavy | 104 | 19.2% | 1.28 | -7% | 1.22 (n=44) | 1.33 (n=60) |

## 5. ZANS method and rule tests

_No ZANS method for this course and code yet; section 4 k) still tests the standard rules._

## 6. Related research files in the project

_None that names this course._
