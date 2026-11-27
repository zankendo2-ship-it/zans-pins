# Newmarket — Flat turf — course onboarding review + ZANS method v25.0

- Owner's material, both received on 2026-09-24, text kept in `source/`:
  1. `NEWMARKET_FLAT.pdf`: the July Course card of 4 July 2026, and method v24.0 → v24.1.
  2. `NEWMARKET JULY FLAT 2.pdf`, 126 pages: July Course cards on 31 Jul, 1 Aug, 7 Aug,
     8 Aug, 20 Aug and 21 Aug (methods v25.2 → v25.9), then the first Rowley Mile card on
     19 Sep (new thread, method v1.1).
- **8 cards, 53 races, 8 different method versions.** No cards from April or May are in
  these files.
- Evidence used: `reports/methods/newmarket_FLAT_rules.md`, from `python -m methods.audit`.
  It covers 958 Rowley Mile races from 2019 to 2026 plus every UK/IRE flat race.
- **Data gap:** our history has no July Course races. The 2018–2025 backfill is running
  (results.yml, course 174), so the July Course claims below are UNVERIFIED until it lands.

---

## 1. Scorecard of your picks (£1 win on every Winner Selection, SP)

| Card | Track | Method used | Races | Winner picks won | Returned | P/L | RPR picks won | Longshots won |
|---|---|---|---|---|---|---|---|---|
| 4 Jul | July | v24.0 | 7 | 1 | £4.50 | −£2.50 | 2 | 0 of 3 |
| 31 Jul | July | v25.2 | 6 | 2 | £5.63 | −£0.37 | 3 | 0 |
| 1 Aug | July | v25.4 | 7 | 1 | £5.00 | −£2.00 | 1 | 0 |
| 7 Aug | July | v25.5 | 6 | **4** | £7.23 | **+£1.23** | 3 | 0 |
| 8 Aug | July | v25.6 | 7 | 2 | £9.33 | **+£2.33** | 2 | 1 (Sugar Yes Please 11/1) |
| 20 Aug | July | v25.7 | 6 | 2 | £7.58 | **+£1.58** | 2 | 0 |
| 21 Aug | July | v25.8 | 6 | 1 | £1.33 | −£4.67 | 1 | 2 (Angel Shared, Allegrino) |
| 19 Sep | Rowley | v1.0 | 8 | 2 | £3.65 | −£4.35 | 2 | 0 |
| **Total** | | | **53** | **15 (28%)** | **£44.25** | **−£8.75 (−16.5%)** | **16 (30%)** | **3** |

- **By month:** July 3 of 13 (−22%). August 10 of 32 (31%, −5%): the best spell.
  September 2 of 8 (−54%).
- **Perplexity miscounted twice.** On 4 July the RPR picks won 2, not the 1 it reported. On
  19 September they won 2, not 3 (Lily Pink ran 2nd, so Flower Show was not an RPR winner).
  The totals above are recounted from the race-by-race tables.
- **Many winner picks were short-priced favourites** (1/3, 4/9, 2/5, 1/2, 8/11, 5/6…).
  A 28% strike rate is below what the favourite wins on average (about 31–34% on the flat).
  So the method has mostly been picking favourites, and slightly worse ones than the market.
- **The method changed after every single card** (8 versions in 8 cards). The swing from
  1 of 7 to 4 of 6 and back to 1 of 6 is normal noise for 6–7 races a day. No version was
  used long enough to show whether it was better or worse.
- **The best thing in the file is the longshot eye on 21 August.** Angel Shared and
  Allegrino were picked at **12/1 and 10/1 (forecast)**, were **backed into 11/4 and 2/1
  favourites**, and both won. That is exactly the "overpriced early, backed in" horse your
  price strategy wants. It only pays if the bet goes on at the early price, so we now record
  the price at every check.


### When your method was at its best, and what was in it

| Spell | Cards | Versions | Races | Winner picks won | P/L (£1 win, SP) |
|---|---|---|---|---|---|
| Early build-up | 4 Jul – 1 Aug | v24.0 – v25.4 | 20 | 4 (20%) | −£4.87 |
| **Best spell** | **7 – 20 Aug** | **v25.5 – v25.7** | **19** | **8 (42%)** | **+£5.14 (+27%)** |
| Slump | 21 Aug + 19 Sep | v25.8 – v25.9 (July), v1.0 (Rowley) | 14 | 3 (21%) | −£9.02 |

What the change logs in your PDFs show:
- **Best spell = the calmest method.** v25.5, v25.6 and v25.7 made **no active rule changes**.
  Every change was only a learning tag or a status flag. The engine was: RPR Anchor Safety
  Patch v2.0 (exact-conditions RPR), improver-first, hard rules HR1–HR9, and track DNA. The
  Favourite Reweight Patch was **downgraded to "review required"**, so short favourites were no
  longer being knocked out. The RPR stream kept matching or beating the winner stream.
- **The slump started when rules were added on thin evidence.** v25.8 added the
  "3yo August weight concession" and a 1m4f pace calibration. v25.9 made the 3yo concession
  ACTIVE after only 4 cards and added an experimental 2yo novice penalty cap. The Rowley Mile
  thread (v1.0) then started from scratch, without the July thread's learning.
- **Our data backs that reading.** The 3yo August concession tests at A/E 0.97 nationally, and
  0.89 at the Rowley Mile, so it is already in the price (DROPPED below). The RPR anchor
  that ran the best spell is the one rule that is profitable at Newmarket (A/E 1.10).
- **Caution on the sample:** 19 races is small. 8 winners from 19 could be luck, so the best
  spell is a pointer, not proof. That is why ZANS v25.0 keeps the best spell's core (RPR anchor,
  exact conditions, no knock-out of short favourites) only where our 10-year data also supports it.
  It also changes rules only on the promotion test at the end of this file.

## 2. What's right in your method (KEEP)

| Idea in your method | What the data says | Verdict |
|---|---|---|
| **RPR Anchor**: the best RPR under today's conditions (trip ±1f, same going) must be accounted for and never quietly dropped | At Newmarket this horse wins **16.6%**, A/E **1.10**, **+1%** at SP (849 runners, the only rule that is profitable at SP there). The simpler "top recent RPR" wins **21.9%**, A/E 1.10 | **KEEP, and it is now the backbone** |
| Never demote a clean RPR anchor for "narrative" reasons | Over the 8 cards your RPR picks won 16 to the winner picks' 15, and the anchor is the best rule in the audit | **KEEP** |
| Don't use blanket historic draw rules; watch today's stalls and rail | Rowley Mile has **no measurable draw bias** at 6f, 7f, 1m or 1m2f (hundreds of races each, HIGH confidence) | **KEEP** |
| Pace map and race shape | A **lone front-runner** at Newmarket wins 13.8%, A/E **1.13**, **+9%** (298 runners; 1.04 nationally) | **KEEP, and it becomes a scored angle** |
| Controlled self-learning (no permanent rule from one race) | This is the right principle, but v24.1 breaks it (see below) | **KEEP, with numbers enforced** |
| Rowley and July are two different courses | True. Our speed standards keep them apart | **KEEP** |

## 3. What's wrong in your method (CHANGE or DROP)

| Rule | What the data says | Verdict |
|---|---|---|
| **HR3** hard reject if first-time jockey pairing | It flags **about 40% of all runners**. They win 9.5% against 10.9%, and A/E is **1.00** (the market already allows for it). Rejecting them throws away 3,683 runners, including 350 winners | **DROP** |
| **HR5** hard reject aged 6+ | At Newmarket 6yo+ are **under-rated**: A/E **1.19**, −3% (898 runners). 6+ with no recent 1st or 2nd: A/E 1.17, **+2%** | **DROP** (this rule threw out value) |
| **HR4** jockey 12-month strike rate under 6% | They win less (6%), but the price already says so (A/E 1.29 at Newmarket, 0.96 nationally) | Information only, not a reject |
| **HR6** hard reject after "weakened / no extra" in the last 2 runs | It flags 2,443 runners. A/E 0.98, so there is no edge; almost every beaten horse has such a comment | **DROP** as a hard reject |
| **HR2A** trial trap (back from 120+ days at under 2/1, spring or autumn) | They win **37–42%**, A/E 0.95 at Newmarket and **1.04** nationally. No trap | **DROP** as a cap. Note only |
| **HR2C** handicap debut at under 2/1 cannot be the winner pick | Nationally 751 runners won 38.9%, A/E **1.03**: no trap. Newmarket has only 34 runners (A/E 0.81), too few to use. It was made ACTIVE after **one** horse (I'll Be Back), against the method's own rules | **Downgrade to CAUTION TAG** (no block) until the July backfill and 30+ cases say otherwise |
| **HR2D** mega-yard odds-on novice trap | They win **64%**, A/E 1.08. No trap | **DROP** |
| **Rule 5.1** ground exclusivity gives an automatic Tier-1 upgrade | A/E 1.02, −16%. The market prices it | **Soft plus only**, never an automatic upgrade |
| **Favourite stress test**: big-field Class 2/3 handicap favourites can't win tie-breaks | These favourites are **under-rated**: A/E **1.59**, +34% at Newmarket (41 runners), 1.09 nationally. The rule points the wrong way | **DROP** |
| **Improver engine** and "won last time" upgrades | Both are **over-bet** at Newmarket: A/E 0.92 and 0.94 | No upgrade. Never promote on these alone |
| **Longshot** 10/1+ with RPR/TS at least OR + 15 | Newmarket 0 of 6. Nationally 3.7%, A/E 0.94, −28% | **DROP**. Use the ZANS value test instead |
| July Course "front-runners strongly favoured (PI 1.33–1.40)" | No source is given, and we have no July data to check it yet. On the Rowley Mile, leaders do no better than the national average (A/E 0.97) | **UNVERIFIED** until the backfill |
| **3yo August weight concession** (made ACTIVE in v25.9 after 4 cards) | Nationally, 3yos taking on older horses in August win 11.0%, A/E **0.97**, −24% (9,184 runners). The weight-for-age is already in the price. At the Rowley Mile, 3yos v older are **over-bet** (A/E 0.89) | **DROP** |
| 2yo novice penalty cap (v25.9, experimental) | We can't test it yet (novice races aren't flagged in our history) | NOTE, re-test later |
| Stage 1 field reduction (v1.1 found it threw out 3 of 8 winners on 19 Sep) | This agrees with the audit: the hard gates remove winners | Hard gates become soft notes (see method) |
| Longshot "market synergy" (v25.9 learning tag: picks backed from 10–12/1 into favourite) | Right idea, and the best signal in your file. It is only worth money at the early price | **KEEP as the early-price watchlist**, scored on price taken v SP |
| Consensus grid of 100+ sources | It can't be checked and adds nothing the price doesn't already hold | **DROP** |
| 19 phases and 9 hard gates | Every extra gate that doesn't hold removes winners. The method grew after every review | **SIMPLIFY** |

## 4. Why results dropped after April/May (what the data shows)

1. **The rules don't wear out by season.** Nationally, top-RPR horses win 20% in Apr–May,
   **23%** in Jun–Aug and 20% in Sep–Nov. Favourites win 31%, 32% and 30%. A method based on
   ratings should not get worse in summer.
2. **Newmarket moves to the July Course from late June to August.** Your method's July
   "DNA" was never measured. That's a likely cause of summer misses at Newmarket, and it's
   the course in this review. The backfill fixes this.
3. **The method grew with every bad day.** Rules were added or made ACTIVE after single
   races (I'll Be Back, Silver Ghost). Each hard reject that doesn't hold cuts out winners.
   HR3 and HR5 alone remove about half the field, and the 6+ group is under-rated at
   Newmarket.
4. **Plain variance, made worse by constant changes.** With 6–7 races a card, one card
   says almost nothing. Changing the method after each one chases luck. August was the best
   month (31% winners), then the Rowley switch in September started a new, untested thread.
5. **The winner picks lean hard on favourites** at prices that leave no profit, and the hard
   rejects (age 6+, first-time jockey, weak finish) throw out horses the market underrates.

---

## 5. ZANS METHOD v25.0 — NEWMARKET — FLAT TURF (current method)

```
ZANS METHOD v25.0 — NEWMARKET (ROWLEY MILE + JULY COURSE) — FLAT TURF
Replaces Aurora-X v25.9 (July thread) and v1.1 (Rowley thread). Status of every rule is evidence-based:
KEEP (tested, holds) / SOFT (small plus or minus) / NOTE (shown, not scored) /
UNVERIFIED (not yet testable) / DROPPED (tested, does not hold).

SCOPE: Newmarket only, flat turf only. Rowley Mile (spring + autumn) and July Course
(late June - August) are separate tracks: speed standards, draw and pace are kept apart.

==================================================================
PHASE 0 — DATA LOCK (automatic, from the ZANS pipeline)
==================================================================
- Course + track in use (Rowley Mile / July Course), race times, field sizes, non-runners.
- Official going + OUR measured going allowance from the last meeting's race times.
- Stalls position and rail movements: when published (Racing Post / clerk). Otherwise
  mark NOT VERIFIED. This caps nothing, because Rowley has no measurable draw bias.
- Prices from all three checks: day before 09:00, day before 19:00, race day 07:30.
- Frozen pre-race snapshot + sha256, saved before the first race.

==================================================================
PHASE 1 — CORE RATING (the ZANS win model)
==================================================================
Every runner gets a win chance from the ZANS model. It is fitted on 2019-2024 races
and tested on 2025-26:
  - Best recent RPR and last-run RPR (same code, within a year).
  - OUR speed figure (best of last 3) and its trend.
  - Official rating vs race top, weight vs race average.
  - Days since run, number of runs, course winner, trip winner, won/placed last time.
  - Trainer (last 365 days + last 14 days) and jockey (365 days) strike rates.
  - Pace-map call (SUITS / AGAINST) for today's projected pace.
  - The market price (log chance), blended in, because the market knows a lot.
Output: win chance per runner. The fair price = 1 / chance.

==================================================================
PHASE 2 — RPR ANCHOR (KEEP — the backbone of your method, now proven)
==================================================================
Evidence: at Newmarket the top exact-conditions RPR horse wins 16.6%, A/E 1.10, +1% at SP
(849 runners, 2019-26). It is the only rule that is profitable at SP here.
1. RPR ANCHOR = the highest RPR recorded at today's trip (+-1f) on today's going
   group. If nobody qualifies: trip only, then the highest recent RPR.
2. The anchor MUST be printed with one of: WIN PICK / RPR PICK / REJECTED (+ reason).
   It can never disappear silently. (Kept from your Safety Patch.)
3. The anchor can only be rejected for: a non-runner risk on today's ground (never raced
   on it AND breeding/comments say it needs the opposite), or a WARNING weight rise
   (7lb+ above anything it has finished top-3 carrying).
4. If the anchor is not the win pick, it is the RPR PICK.
5. RPR PICK rule (owner's spec, unchanged): the highest card RPR that has run at today's
   distance AND going (RP course/distance/going stats). If none, distance only. Walk down
   the RPR order. Weight check: up 5lb+ on last run -> has it finished top-3 carrying
   this weight or more before? Show the reason.

==================================================================
PHASE 3 — NEWMARKET ANGLES (scored, evidence-backed only)
==================================================================
PLUS (use to split close calls, and flag to customers):
  + Lone front-runner (the only habitual leader in the race): 13.8% won, A/E 1.13,
    +9% (298 runners at Newmarket; 1.04 nationally). KEEP.
  + Top exact-conditions RPR (Phase 2). KEEP.
  + Big-field (12+) Class 2/3 handicap FAVOURITE: A/E 1.59 at Newmarket (41) / 1.09 UK.
    SOFT plus, the opposite of the old stress test. Recheck at 100+ cases.
  + Aged 6+: A/E 1.19 at Newmarket. Never a reject. SOFT plus in handicaps.
MINUS:
  - Slow starter (2+ of last 4 runs) in a 5-6f race: A/E 0.90, -57% (105 at Newmarket;
    neutral nationally). SOFT minus.
  - "Won last time" and "improver" are OVER-BET here (A/E 0.94 / 0.92): no upgrade from
    these on their own.
PACE BY TRIP (Rowley Mile, measured, vs national average):
  - 5f, 7f: typical (leaders do well everywhere, not extra well here).
  - 6f and 1m: lean towards hold-up horses. 1m1f: hold-up horses favoured, leaders struggle.
DRAW (Rowley Mile): no meaningful draw bias at 6f, 7f, 1m, 1m2f (HIGH confidence). Use
  only TODAY's visible bias (earlier races on the card) and published stalls/rail. Never
  a blanket historic draw rule. (Your Stalls/Draw Law: KEEP.)

==================================================================
PHASE 4 — JULY COURSE (UNVERIFIED until the 2018-2025 backfill is tested)
==================================================================
Until then: use Phase 1-3 and the national pace map. Your July "DNA" is held as
UNVERIFIED notes, not rules:
  - 5f-6f straight front-runners strongly favoured (claimed PI 1.33-1.40).
  - 7f front/prominent favoured (claimed PI ~1.36) + the 7f CD/pace tie-break.
  - Possible quicker strip on one side.
When the backfill lands: methods.audit --track newmarket_july re-tests each. Only those
with A/E >= 1.05 in BOTH halves of the data (out of sample) become rules.

==================================================================
PHASE 5 — CAUTION TAGS (shown on the card, NOT used to block a pick)
==================================================================
  - Handicap debut at under 2/1 (old HR2C): UK 751 runners, A/E 1.03, so no trap;
    Newmarket only 34 (A/E 0.81). NOTE. Re-test at 30+ Newmarket cases.
  - Back from 120+ days at under 2/1 in spring/autumn (old HR2A): A/E 0.95-1.04. NOTE.
  - Odds-on juvenile/novice from a big yard (old HR2D): A/E 1.08. NOTE.
  - Jockey 12-month strike rate under 6% (old HR4): wins less, but it's priced in. NOTE.
  - Ground exclusivity (old Rule 5.1): A/E 1.02. NOTE.

==================================================================
PHASE 6 — SELECTIONS
==================================================================
WIN PICK: the highest ZANS win chance after Phase 3 adjustments. One per race, every race.
CONFIDENCE /10: from the win chance, calibrated on 2025-26 races
  (flat: 10/10 won 71%, 9 52%, 8 45%, 7 38%, 6 29%, 5 26%, 4 23%, 3 19%).
BET / NO BET: BET only if confidence >= 6 AND the price we can take is at least our fair
  price. Prefer the EARLIEST check that meets it. Log the price taken vs SP for every bet.
LONGSHOT: 14/1+ at selection time, 6+ runners, the runner with the best chance x price if
  that is >= 0.9 (2025-26 flat test: about break-even at SP, better at early prices).
  Otherwise "no longshot".
EARLY-PRICE WATCHLIST (owner's longshot eye, v25.9 "market synergy"): horses we rate
  much shorter than their day-before price (10/1+), especially low-weight / pace-collapse
  types. Bet EACH-WAY at the early check, then score price taken v SP. (21 Aug 2026: Angel
  Shared 12/1 -> 11/4f WON, Allegrino 10/1 -> 2/1f WON.)
RPR PICK: Phase 2 rule 5.

==================================================================
PHASE 7 — OUTPUT PER RACE
==================================================================
Time / race / trip / going / runners
WIN: horse, price, confidence x/10, BET or NO BET, our chance, fair price, reasons
RPR: horse + qualifying reason + weight check
RPR ANCHOR: horse + status (WIN / RPR PICK / REJECTED: reason)
LONGSHOT: horse + price + value note, or "no longshot"
ANGLES: lone leader / pace note / today's draw note / caution tags

==================================================================
PHASE 8 — EVENING REVIEW + LEARNING (automatic)
==================================================================
- Ledger per pick: price taken, SP, result, beaten distance, in-running comment.
- Every beaten pick is classed: METHOD ERROR (evidence was there pre-race) / UNLUCKY
  (trouble in running, slow start, pace collapse) / BEATEN FAIR / NON-RUNNER (void).
- Rule scorecard across ALL cards, not one: runners flagged, wins, A/E, return.
- A rule is PROMOTED only with 30+ flagged runners at Newmarket (or 300+ UK) and A/E >= 1.05
  in both an earlier and a later period. It is DROPPED when A/E <= 0.95 over the same
  sample. Nothing changes from a single race or a single card.
- Beating the SP (price taken > SP) is tracked for every bet. It is the best early
  sign that the method finds value.

==================================================================
CHANGE LOG
==================================================================
v25.0 (2026-09-24, ZANS onboarding review; evidence: reports/methods/newmarket_FLAT_rules.md)
  KEPT: RPR Anchor + Silent Omission Ban (now the backbone), Stalls/Draw Law, Rowley/July
        split, pace map, controlled learning (now with numeric thresholds).
  ADDED: ZANS win model core (calibrated confidence, fair price, BET rule), lone
        front-runner plus, big-field handicap favourite plus, 6yo+ plus, slow-starter
        minus at 5-6f, measured Rowley pace by trip.
  DROPPED: HR3 first-time jockey reject, HR5 age reject, HR6 weak-finish reject,
        HR2A/HR2D trap caps, big-field favourite stress test, consensus grid, RPR>=OR+15
        longshot rule, improver / won-last-time upgrades.
  DOWNGRADED: HR2C handicap-debut block -> caution tag; Rule 5.1 -> note.
  UNVERIFIED: all July Course DNA claims (backfill running).
Replaces: July thread v25.9 (21 Aug 2026) and Rowley thread v1.1 (19 Sep 2026). Owner's
  8 cards under v24.0-v25.8 / v1.0: winner picks 15/53 (28%), -16.5%; RPR picks 16/53.
  Also DROPPED from v25.9: 3yo August weight concession (UK A/E 0.97). NOTE: 2yo novice
  penalty cap (untested). KEPT: longshot market synergy -> early-price watchlist.
```

---

## Review log

| Date | Track | Card | Win picks | £1 P/L | RPR picks | Longshots | Change |
|---|---|---|---|---|---|---|---|
| 2026-09-24 | Rowley | 7 races (published card: model v1 with price) | 2/7 | -£3.18 | 2/7 | 0/6 placed | NO METHOD CHANGE (variance); owner rule from 25 Sep: win picks price-free |

Full review: reports/reviews/2026-09-24/newmarket.md

## Change log
- 2026-10-21 review: NO CHANGE - official 1/7 (Lots Road demoted to 2nd for interference). Usual leaders on soft at Newmarket 0.44 / 0.38 (49 / 44 runners, crude leader rule, TEST) - re-test with the method's pace roles; debutant favourites flip (0.63 / 0.97).
- 2026-09-26 (review of 25 Sep): win picks 2/7 (Talk Of New York BET, Fortitudine), RPR picks 2 won + 4 second of 7 -> the RPR anchor (the peak-version rule, history A/E 1.10, 849) is confirmed: exact-conditions RPR weight 1.05 -> 1.08. Applesandpears (lost many lengths at the start) flagged.
- 2026-09-26 (cross-course lessons): + all-UK default "top recent RPR" 1.04 (Newmarket A/E 1.10); + ground rule (never on good 0.90 / firm 0.97 unless elite).
- 2026-09-26 (review of 26 Sep): win picks 1/6 (Sun Goddess), Sierra Belle non-runner; 3/7 winners held up incl. Pierre Royal 34.00. Tested /tmp/claude-0/sp/pattern_tests.py (2016-26, split 2016-21 / 2022-26): held-up types on soft at Newmarket A/E 0.92 (642; 0.93 / 0.91) -> today was variance -> NO CHANGE.
- v25.1 (2026-10-03): owner's NEWMARKET FLAT REVIEW (Rowley Mile spring 2026, v23.3 -> v23.8: 16 Apr 0/7 -£7, 3 May 0/7
  -£7, 15-16 May, 26 Jun 1/8) confirms the spring slump; the v25.5-v25.7 August peak stays the base. Re-test (1,371
  top-RPR runners): exact RPR 1.04 both periods -> trimmed 1.08 -> 1.05; top recent RPR 1.10 (1.15 / 1.07) -> own
  x1.05; improver OVER-bet 0.92 (0.99 / 0.87) -> x0.96; won last time 0.94 (1.00 / 0.90) -> x0.97. Kept: 6yo+ handicap
  1.08 (age 6+ 1.18, 1.24 / 1.15), slow starter 5-6f 0.93 (0.71), lone leader 1.08 (1.23; 0.89 / 1.45).
- NO CHANGE (2026-10-03 review of Sat 3 Oct: win picks 5/7): The new v25.1 factors had a strong first day (5 from 7). Front-runners did well, but the lone front-runner record at Newmarket is not steady across periods (0.89 in 2019-21, 1.45 since 2022), so the existing x1.08 stays as it is rather than being raised. Starlight Lass is a model-wide lesson (trainer strike rate weight), not a Newmarket rule. Evidence: Newmarket flat: lone front-runner A/E 1.23, +11% (380; 0.89 / 1.45); usual front-runner 1.00 (1,012; 0.96 / 1.03); held up 1.04; top recent RPR 1.10 (1,371). Today: 3 of 7 winners made all or led early.

- NO CHANGE (2026-10-09 review of Fri 9 Oct): Newmarket FLAT v25.1 unchanged (exact RPR x1.05, top RPR x1.05, improver x0.96, won last x0.97, lone front-runner x1.08). One winner from eight on a Group 1 card where only two favourites won is a day of outsiders, not a broken method. Our picks were second by 0.3 lengths, fifth by a length and fourth by under three lengths; nothing tonight contradicts a tested Newmarket rule, so the method is left exactly as it is. Evidence: Today 1/8 won, 1 second, 2 more within three lengths. Favourites 2/8; winners at 9.00, 11.00, 17.00 and 41.00. Two winners made the running.

- NO CHANGE (2026-10-10 review of Sat 10 Oct): Newmarket FLAT v25.1 unchanged (exact RPR x1.05, top RPR x1.05, improver x0.96, won last x0.97, lone front-runner x1.08). Two winners, three seconds beaten 1.5 lengths or less and one non-runner is a card where the picks were right on the day and the margins went against us. No beaten pick lost for a reason our Newmarket rules got wrong, so nothing is changed. The slip lesson has been dealt with separately. Evidence: Newmarket history: top recent RPR A/E 1.10 (1,371; 1.15 / 1.07); won last time A/E 0.94 (2,244; 1.00 / 0.90). From 11 Oct the treble uses different horses from the double (test 26 Sep-10 Oct: one horse sank both on 6 of 15 days with the old shape, 0 with the new).

- 2026-10-22 review: NO CHANGE. No change to Newmarket FLAT v25.1. Every idea tonight was tested on history and none holds in both periods: usual front-runners on exact Soft at Newmarket flip (0.66 then 1.10), lone leaders on Soft flip, hold-up horses facing a lone leader flip, and the quick-follow-up winner under more weight (Irish Nectar's profile) is if anything under-bet, not over-bet. Today's beaten picks were mostly close seconds and fourths, not horses our rules misjudged. Evidence: TEST /tmp/claude-0/team/newmarket/soft_pace_check.py + soft_exact_check.py (history/*.csv.gz, UK/IRE turf flat 2019-26, pace roles = methods.audit / speed.pacemap rule: led in 50%+ of last 6 readable runs; A/E v margin-free SP; 2019-21 | 2022-26). Newmarket exact Soft: usual leader 0.66 (52, 3 won) | 1.10 (86, 12); lone leader 0.00 (10) | 1.37 (30); held up 0.94 (159) | 1.11 (194); hold-up v lone leader 0.34 (57) | 1.12 (73). Newmarket soft group (soft/heavy/yielding): leader 0.83 (78) | 0.91 (108); national soft leader 0.98 | 0.98. Won last time within 7 days and carrying 7lb+ more, national soft 1.30 (85) | 1.20 (114); only 1 such runner at Newmarket.
