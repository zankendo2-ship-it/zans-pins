# Worcester — Jumps — course onboarding review + ZANS method v13.2

Source: owner's `WORCESTER_JUMPS_REVIEW.pdf` (43 pages): ONE scored card, 23 Aug 2026 (Review
1.3, method AURORA-X v13.1). Rule tests: `reports/methods/worcester_JUMPS_rules.md` (815
Worcester jumps races 2019–2026). Odds in decimals.

## 1. Scorecard — 23 Aug 2026 (Good)

| Race | Pick | Result | Winner |
|---|---|---|---|
| 14:08 | **Axel Bleue** | **WON 3.50 fav** | |
| 14:38 | **Little Ledgend** | **WON 3.75** | |
| 15:08 | Turbogeist | 4th, 3.75 | I've Got A Friend 11.00 |
| 15:38 | **Down To Business** | **WON 1.67 fav** | |
| 16:08 | Playful Fox | non-runner (no bet) | |
| 16:38 | Trouville | 2nd, 6.50 (beaten ½L by top-weight C&D winner) | Letterston Lily 3.25 |
| 17:08 | Mya Du Clos | 5th, 21.00 (drifted from 4.50 forecast) | The Secret Pearl 13.00 |

**3 from 6, +£2.92 (+49%).** The chat's sums are right. Only one card, so no best spell yet.
**Little Ledgend runs again tomorrow (13:30).**
Note Mya Du Clos: a big drift before the off (4.50 → 21.00) was a warning sign. Our price checks
now log moves like this.

## 2. Rules v our data

| Claim | Data | Verdict |
|---|---|---|
| **"Prominent / front-running bias at ≤2m4f"** | **Backwards.** Pace table: 2m hurdles "hold-up horses favoured", 2m4f hurdles and 2m½f/2m4f chases "lean to hold-up"; usual front-runners A/E **0.91**, lone leaders **0.86** | **REVERSE: front-runners over-bet here** (x0.95 / x0.93) |
| Staying chases 2m7f+ suit patient rides | Pace table: 2m7f chases "typical" | NOTE |
| C&D / top-weight C&D exception (Letterston Lily) | C&D winners A/E **1.12, +20%** (585) | **KEEP, strengthened** (x1.06) |
| Distance proof ±2f | Unproven at trip, nationally A/E 0.98 | SOFT |
| Apprentice/claimer first-time (Hard Rule 2) | first-time pairing A/E 1.03 | **DROP** |
| Lightly raced / PTP-only | A/E 0.93, −32% (2,154) | x0.96 |
| Ground specialist | A/E 0.88 here | x0.94 |
| Top recent RPR | A/E 1.05 | x1.02 |

## 3. ZANS METHOD v13.2 — WORCESTER — JUMPS (code: predict/course_method.py)

```
WIN PICK: price-free ZANS model, then Worcester multipliers:
  C&D winner x1.06 | top recent RPR x1.02 | usual front-runner x0.95 | lone front-runner x0.93
  ground specialist x0.94 | lightly raced (<=5 runs) x0.96
TRACK: flat, left-handed, galloping; long straights; horses that hang right under pressure exposed.
DROPPED: "prominent bias <=2m4f" (data says the opposite), apprentice first-time hard rule.
KEPT FROM YOUR METHOD: late-NR rescore; chase completion check (2+ non-completions in last 3);
  layoff caution (note only).
BET: confidence 8+ (data only). LONGSHOT: 14.0+ decimal, 6+ runners.
```

## 4. Change log
- v13.2 (2026-09-24, ZANS onboarding): results verified; pace claim reversed on 815 races;
  C&D angle promoted.
- 2026-09-26 (review of 25 Sep): win picks 1/7 under the morning price-free rule (Worcester favourites won 4/6 -> the main cause; the win pick now includes the price). C&D-winner angle fired on 3 picks, all beaten, but history A/E 1.12 (585) -> NO CHANGE on one card; watch it.
- 2026-09-26: + ground rule (never run on soft/heavy 0.86 unless elite); own top_rpr rule kept.

- NO CHANGE (2026-10-07 review of Wed 7 Oct): Worcester JUMPS v13.2 unchanged. Four winners and two seconds from eight picks is a strong card, and the beaten horses were undone by a lone front-runner, a keen-going mistake at the last and a horse backed beyond its form. None of these contradicts a Worcester rule on history; the bigger lesson (drifting picks still win) has already changed the whole system tonight. Evidence: Today 4/8 won, 2 second, 1 third. Overnight drifters among the picks: Kelijoe 2nd, Dundee Law WON, Brookside La WON (Jollie Dame drifted later, also WON).

- NO CHANGE (2026-10-12 review of Mon 12 Oct): Worcester JUMPS v13.2 unchanged. Four winners from six runners and a narrow second is the method working. The money was lost through the slip's 90-day layoff rule, not the course method, so the course method stays as it is and the layoff rule is reviewed with all the live numbers in the summary. Evidence: Worcester today: picks 4/6 runners (1 non-runner). 7/10+ picks off 90+ days since the slip rule started on 9 Oct: 8 of 15 won, +£13.40 at £10 at the 09:30 price - money the rule kept off the slip.
- 2026-10-21 review: NO CHANGE - 4/8 (+£7.13 at £1 SP). 7 of 8 winners off 194-272 days, but Worcester 180+ day returners flip (1.33 / 0.80); poor jumpers not over-bet (1.01 / 1.12).
