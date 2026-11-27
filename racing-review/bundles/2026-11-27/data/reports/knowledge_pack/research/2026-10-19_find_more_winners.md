# Find more winners - deep research, Mon 19 Oct 2026

Owner: "are we getting better than when we first started ... YOU MUST FIND MORE WINNERS ... pick the favourites when we think
they are going to win but leave them out when we don't" / "Deep research a way to improve!"

Live = the FIRST locked race-day pack each day (predict.leak_finder.first_locked), 26 Sep-18 Oct, 830 races with a result
and a 09:30 price; £10 win at the 09:30 best price unless stated. History = every UK/IRE race 2025 and 2026 (22,519), scored
by the current 46-feature model fitted ONLY on earlier years (fit < 2025 for 2025, fit < 2026 for 2026), at SP.
Scripts + outputs: reports/research/scripts/improve_2026-10-19/.

## 1. Are we getting better? (live)

| Week | Races | Win picks won | 7/10+ picks | 7/10+ P/L | Under 7/10 P/L |
|---|---|---|---|---|---|
| 26 Sep-2 Oct | 250 | 65 (26%) | 38/85 (45%) | -£68.90 | -£689.00 |
| 3-9 Oct | 248 | 87 (35%) | 46/79 (58%) | +£132.10 | -£237.70 |
| 10-16 Oct | 258 | 94 (36%) | 49/91 (54%) | +£113.30 | -£65.10 |
| 17-18 Oct | 74 | 26 (35%) | 14/30 (47%) | -£29.00 | -£41.20 |

Counted bet slips (slip_review.json, one slip a day + Champions Day slips): 25 Sep -£55.49; 26 Sep-2 Oct -£32.71 (2 of 7
days up); 3-9 Oct +£387.78 (3/7); 10-16 Oct +£89.11 (5/7); 17-18 Oct -£100.55 (0/2, incl. Champions Day). Total +£288.14.
-> strike rate went from 26% (week 1) to 35-36%; the 7/10+ picks have made money in 3 of the 4 weeks.

## 2. Does picking against the favourite find more winners? NO

History 2025 | 2026, races where our pick is NOT the favourite (no joint favourites): our pick 182/804 | 148/619, the
favourite 187/804 | 160/619. The data-only horse (no price) wins 28.4% | 27.0% of all races v our pick 34.5% | 34.2%.
Live, where our pick was not the 09:30 favourite (80 races): our pick won 19, the favourite 15.
-> Leaving a favourite out of the PICK does not find more winners. The place to leave favourites out is the BET SLIP.

## 3. Which favourites win? Our confidence sorts them

History, the favourite by our chance for it: under 25% won 23.6% | 24.0%; 25-35% 29.9% | 32.3%; 35-42% 37.7% | 39.9%;
42-50% 46.0% | 43.4%; 50-60% 54.7% | 51.6%; 60%+ 69.3% | 71.7%. Our 7/10+ picks win 47.9% | 47.3%, under 7/10 25.4% | 25.6%.
Live: 7/10+ picks 147/285 (52%) +£147.50 (both halves up: +£61.40 / +£86.10); under 7/10 125/545 (23%) -£1,033.00.
-> "Back the favourites we think will win, leave out the rest" = the 7/10+ rule the slip already uses since 5 Oct.
At SP, every confidence band loses 4-13% in history: the profit comes from the PRICE TAKEN (next point).

## 4. The price taken is the biggest lever (live, 7/10+ picks, £10 win)

| | Won | 09:30 price | SP | Best Odds Guaranteed |
|---|---|---|---|---|
| All 7/10+ picks | 147/285 | +£147.50 | +£29.50 | +£318.75 |
| Under 7/10 picks | 125/545 | -£1,033.00 | -£1,144.82 | -£702.78 |

The 09:30 price was bigger than SP for 160 of the 285 7/10+ picks. -> Always take the 09:30 price WITH Best Odds Guaranteed.

## 5. The slip safety rules (live 7/10+ picks; all | 26 Sep-7 Oct | 8-18 Oct; 09:30 price)

Passed every rule, 2.00+: 37/72 +£153 (+£38 / +£115). Kept out by a safety rule: 77/163 -£51 (+£13 / -£64).
Per rule (a pick can hit several): maiden/novice jumps 25/65 -£159.30 (-£94 / -£65) KEEP; off 90+ days 22/52 -£63.70
(-£34 / -£30) KEEP; never run on the going (where it blocks) 19/47 -£94.50 (-£56 / -£38) KEEP; never run at the trip 42/75
+£83.40 (+£105 / -£21) MIXED - keep, watching; drifted 15%+ 13/25 +£35.10 (-£33 / +£68) MIXED - keep, watching.

## 6. CHANGE ADOPTED (TRIAL from Tue 20 Oct): win singles for 7/10+ picks priced UNDER 2.00

7/10+ picks that passed every rule but got no win single because they were under 2.00: 33/50 (66%), +£45 at the 09:30
price, +£22 at SP, +£60 with BOG; both halves up (15/24 +£10 / 18/26 +£35 at the 09:30 price; 1.00-1.49 10/12 +£16.10,
1.50-1.99 23/38 +£28.90). History at SP (all 7/10+ picks, no slip rules): 1.00-1.49 -4.0% | -3.6%, 1.50-1.99 -5.9% | -12.3%
-> TRIAL, judged nightly. predict/betslip.CONF_SINGLE_MIN_PRICE 2.0 -> 1.0. Replay on the d0_morning files: 15 Oct + My Boo
Boo 1.83 (won), Grove Street 1.67 (won); 16 Oct + Arthurian 1.33 (won), Qila 1.91 (won), My Girl Dee Mo 1.91 (lost);
18 Oct + Sunatia 1.91 (lost), Come What May 1.91 (won).

## 7. Tested, NOT adopted

- Evidence agrees with the pick (7/10+): history wins more (51.1% | 49.6% v 42.9% | 44.8%) but ROI mixed; live the
  OPPOSITE (agrees 87/173 +£4.00, disagrees 60/112 +£143.50) -> no rule.
- Favourite segments at SP (history): only favourites priced 5.50+ (A/E 1.54 | 1.52, +23% | +17%, 320 | 229) and in 16+
  runner fields (A/E 1.30 both) beat the market - those are the OPEN races where our confidence is lowest. Small; noted.
- Noon re-pick (running record, 20 days): 259 v 253 morning winners; slips better in the morning -> stays background.
- Switching to another Claude model (owner asked about Fable): the picks come from our own trained model, not from the
  chat model - a different chat model would not change a single pick.

## 8. Helper results (19 Oct night) + figure note

FIGURE NOTE: sections 1-6 count only picks matched to the d0_morning price FILE (285 7/10+ picks). predict.leak_finder.collect
(price as printed in the locked pack, non-runners void) counts 307 7/10+ picks: 161 won, +£189.10 at the 09:30 price,
+£392.46 with BOG, +£87.07 at SP. Both are real; the 307 figure is the fuller one.
- When to bet (reports/research/helpers/2026-10-19_when_to_bet.md): bet the locked 7/10+ pick at 09:30 with BOG - best in both
  halves (+£226.61 / +£165.85). Noon with BOG +£261.62 v 09:30 +£313.56 (races after noon); the day-before pack's own 7/10+ picks
  at the evening price -£50.30 v +£164.20 (only 119 of 193 stayed the pick). Sky Bet's own price = best price (+£228.30 v +£219.90).
  Under 7/10 picks that drift 09:30 -> noon won 10/107.
- Second-stage filter (reports/research/helpers/2026-10-19_second_stage_filter.txt): no gain over raw confidence in either
  direction 2025 <-> 2026 (AUC 0.665 v 0.664).
