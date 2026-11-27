# Newcastle — All-weather (Tapeta) — course onboarding review + ZANS method v1.7

Source: owner's `NEWCASTLE_AW_FLAT_REVIEW.pdf` (161 pages). It lists earlier reviews 10–20
(Apr–Jul 2026, no ledgers in this file), then 5 scored cards, 31 Jul – 19 Sep 2026
(methods Review 20 → 1.1 → 1.5). Rule tests: `reports/methods/newcastle_AW_FLAT_rules.md` (3,357
Newcastle AW races 2019–2026). Results re-checked against official results. Odds in decimals.

## 1. Scorecard (£1 win on every Winner Selection, SP)

| Card | Method | Picks | Won | P/L | Favourites picked |
|---|---|---|---|---|---|
| 31 Jul | Review 20 | 6 (1 NR) | 1 (Wicklow Way 2.50) | −£3.50 | 3 |
| **20 Aug** | **1.2** | **6** | **2 (Niffler 2.63, Spirited Gesture 1.17)** | **−£2.21** | 3 |
| **2 Sep** | **1.3** | **9** | **3 (Koko Blue 2.38, Yordan 1.15, Beattie Is Back 4.00)** | **−£1.47** | **9 of 9** |
| 5 Sep | 1.4 | 9 | 1 (Niffler 1.25) | −£7.75 | 3 |
| 19 Sep | 1.5 | 9 | 1 (Weffaag 1.57) | −£7.43 | 5 |
| **Total** | | **39** | **8 (21%)** | **−£22.36 (−57%)** | 23 |

- The chat's sums are right. (The horse names Papa Don't Preach, Bonnie's Boy and Ellie's de Vega
  are spelt without apostrophes in the official results; all checked.)
- Four 2nds on 5 Sep and three on 19 Sep: close, but a 21% strike rate is below the favourite's
  ~31% at Newcastle.

## 2. Best spell — and what was in it

- **Best spell: 20 Aug + 2 Sep (v1.2–v1.3): 5 winners from 15.** It still lost money (−25%).
  On 2 Sep **every pick was the favourite**, so the "best" card was really the market's card.
- **What changed next (v1.4, after 2 Sep):** wider Class 6 shortlists (5–6 runners).
  **After 5 Sep (v1.5):** "reduce standalone RPR authority", "Uphill Weight Concession Tax"
  (−1 for conceding 6lb+ to a C&D winner or claimer), and a 2yo novice discount for elite yards.
  Two cards, two winners from 18.
- **Our data says the v1.5 turn went the wrong way:** at Newcastle the top recent RPR is the
  best single rule (A/E **1.08**, 3,922 runners). Cutting RPR authority threw away the edge.
  The weight tax is untested (no evidence either way). So v1.7 goes back to the v1.2–v1.3 core,
  with RPR restored.

## 3. Rules v our data

| Claim / rule | Data | Verdict |
|---|---|---|
| Straight 5f–1m: middle-to-high draws | Correct but small: high third IV 1.14 at 5f and 6f (HIGH confidence) | KEEP as a note (priced in) |
| Pace (stiff, uphill 4½f straight) | Pace table: **hold-up horses favoured** at 5f–1m and 1m4½f+ | Don't favour front-runners in general |
| Lone front-runner | A/E **1.09** (1,058) | KEEP (x1.04) |
| RPR authority | Top recent RPR A/E **1.08**; exact-conditions RPR 1.00 | **RESTORE** (x1.04) |
| Veteran / 6yo+ downgrade | A/E 0.95 (8,164) | SOFT (x0.97) |
| C&D winner | A/E 0.96 (8,301): slightly over-bet | x0.98 |
| Improver | A/E 1.05 | x1.02 |
| Apprentice first-time | A/E 0.99 (first-time pairing) | DROP |
| Wet-Tapeta speed bias, weight tax, nursery top-weight | Not testable yet / 1–3 races each | NOTE only |

## 4. ZANS METHOD v1.7 — NEWCASTLE — AW (code: predict/course_method.py)

```
WIN PICK: price-free ZANS model, then Newcastle multipliers:
  top recent RPR x1.04 | lone front-runner x1.04 | improver x1.02 | age 6+ x0.97 | C&D winner x0.98
NOTES: straight-course high draw slight (5f/6f); hold-up horses do well up the long uphill straight.
DROPPED: "reduce RPR authority" (v1.5), apprentice first-time trap; weight tax / nursery rules = NOTE.
BET: confidence 8+ (data only). LONGSHOT: 14.0+ decimal, 6+ runners.
```

## 5. Change log
- v1.7 (2026-09-24, ZANS onboarding): built on v1.2–v1.3 (best spell); RPR restored (v1.5 cut it,
  data says RPR is the best rule here); results verified.
- 2026-09-26 (review of 25 Sep): win picks 2/8 (Farabove The Limit, Invincible Crown), One Of The Boys (BET) 2nd. 4 unlucky runs (Lord Abama blindfold late + dwelt, Respectable Jack hampered). 4 of 8 winners were usual hold-up horses, but history says hold-up horses are priced correctly here (A/E 1.00, 11,964) -> NO CHANGE.
- 2026-09-26: ground rule does not apply to all-weather; own top_rpr rule kept.


## Extra owner cards (uploaded 28 Sep 2026, `source/NEWCASTLE AW REVIEWS 2.pdf`, May-June 2026)
| Card | Review | Races | Winner picks won | £1 win P/L |
|---|---|---|---|---|
| Tue 2 Jun | 16 | 6 | 1 | -£2.50 |
| Fri 26 Jun | 17 | 7 | 1 (Viper 7/2) | -£2.50 |
| Sat 27 Jun | 20 | 7 | 1 | -£2.67 (chat approx.) |
| **Extra total** | | **20** | **3 (15%)** | **-£7.67** |
These pre-date the v1.2-1.3 peak; the "finishing power + C&D" philosophy the chat defends is already tested in v1.7
(top RPR A/E 1.08 restored) -> NO CHANGE.
- 2026-10-01 review: NO CHANGE (1/8; three winners made all, five picks dwelt). Slow starter 5-6f 0.97 (1,262), slow away up to 1m 1.00 (2,844), usual front-runner 1.03 (1,992) - no rule; lone leader 1.09 already in.
- 2026-10-02 review (win picks 4/9: Koko Blue, Noozhaa, Finn Ironside, Blazing Son): NO CHANGE. Front-runners re-tested:
  usual front-runner 1.03 (1,992) but 0.96 since 2022; lone front-runner 1.09 / 1.03 since 2022 (rule already in).

- NO CHANGE (2026-10-12 review of Mon 12 Oct): Newcastle AW v1.7 unchanged (top RPR authority restored; favourites not opposed). Six of the nine picks were rated 2/10 to 4/10 in tight handicaps that were never likely to be won often, and three picks finished second. The one clear failure, Great Balls OFire, is a rating issue in a single race, so I will test 9/10 hold-up picks against a likely lone front-runner before changing anything. Evidence: Newcastle AW history behind v1.7: top RPR A/E 1.08. Tonight 0/9, three seconds; BET NOW Woolridge won.

- NO CHANGE (2026-10-16 review of Fri 16 Oct: win picks 2/9, four seconds): Newcastle AW v1.7 unchanged. Test asked for on 12 Oct: strong (30%+) held-up favourites facing one habitual leader on the all-weather did A/E 1.04 (2019-22) / 1.20 (2023-26), so there is no confidence cut. Watching: Newcastle picks under 7/10 backed 13%+ overnight have won 1/20 since 26 Sep (other courses 80/307). They are never on the slip.

- 2026-10-20 review: CHANGE. Newcastle AW: the lone front-runner rule now covers 5-6f only, at x1.08 (was x1.04 at every trip). Why: Lone front-runners at Newcastle over 5-6f beat their market chance in both periods, A/E 1.15 on 115 runners in 2019-21 and 1.14 on 283 in 2022-26, against 1.07 and 1.02 at other all-weather courses. Over 7f and further it flips from 1.23 to 0.99, so the general boost is dropped there.
