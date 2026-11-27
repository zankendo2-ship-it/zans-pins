# When should the Data pick be the winner? (owner, 4 Nov 2026)

Owner: "We need to concentrate on these !! And identify when the data pick should be our winner regardless of the price."
All figures are TESTS on records, recomputed 4 Nov. Scripts + full outputs: reports/research/scripts/datapick_2026-11-04/.

## 1. The overall answer
In races where the Data pick (price ignored) and our win pick (price used) are DIFFERENT horses:

| Records | Races | Data pick won | Win pick won |
|---|---|---|---|
| History 2023-24 (models fitted on earlier years only) | 12,254 | 2,085 | 3,478 |
| History 2025-26 | 11,723 | 1,968 | 3,418 |
| Live locked 09:30 picks 26 Sep - 3 Nov | 720 | 108 | 199 |

Taken alone, the Data pick never wins more races than the win pick. That holds by course type, race type, data confidence (green 8/10+
Data picks that differ: live 8 v 16) and price band. "Regardless of the price" is not supported: Data picks at 5.00+ win far fewer.
The Data pick does beat ITS OWN price slightly (A/E 1.06 | 1.02 v margin-free SP), which is why it is useful for value.

## 2. The one situation where the Data pick should be the winner (held in all three periods)
Our win pick is WEAK (5/10 or less) AND the Data pick is a different horse that the market ALSO rates (priced under 4.00 = 3/1):

| Records | Races | Data pick won | Win pick won | Data pick profit | Win pick profit |
|---|---|---|---|---|---|
| History 2023-24 (SP) | 535 | 144 | 141 | -5.0% at SP | -8.9% |
| History 2025-26 (SP) | 569 | 155 | 150 | -4.1% at SP | -11.5% |
| Live 26 Sep - 3 Nov (Sky 09:30 price, evidence-pick proxy) - CORRECTED 4 Nov evening, see note | 17 | 5 | 3 | +£10.00 at £10 | -£70.00 |

So in those races the Data pick wins at least as often and loses less / makes more. It is a small edge, not a guaranteed profit
(both still lose at SP in history). Limits: history uses SP for the 'under 4.00' test (the live rule uses the 09:30 price); the rule
was found by searching many combinations, so it must now prove itself live. Today (4 Nov) no race qualifies.

CORRECTION (4 Nov evening): the first live line ('19 races, 7 v 3, +£62.50 v -£90.00') came from an unsaved one-off script and could
not be reproduced. The expert auditor's rebuild (reports/research/scripts/datapick_2026-11-04/live_e18.py, output live_e18_out.txt;
re-run and confirmed here) gives 17 races, 5 v 3 at the Sky 09:30 price (+£10.00 v -£70.00); best bookmaker price 19 races, 6 v 2.
AUDITOR VERDICT: FAIL as a pick switch - over all 1,104 history races 299 v 291 (p 0.39), 2024 68 v 69, 2025 71 v 71, nearby cut-offs
give fewer Data-pick winners, history chose races by SP (look-ahead), and a 09:30-safe filter gives the Data pick FEWER winners
(167 v 209 | 152 v 154). What is real: the Data pick loses less at SP in these races (value), not more winners. E18 stays a background
record with a stricter judge rule (rules/RULES.md amendment).

Stronger but smaller groups found in the same search (history only, n 60-180 per period, treat as pointers): Data pick clearly top
on the data (10%+ ahead of the next best) + under 4.00 + win pick 5/10 or less: 57 v 49 and 50 v 31 wins.

## 3. Pre-registered
rules/RULES.md E18-LIVE: tracked nightly by predict/data_pick_tracker.py (section 'E18 DATA OVERRIDE races' in
reports/predictions/data_pick_record.md). Background until the owner says to make the Data pick the win selection in those races.

## 4. Check of every Data pick on 4 Nov (owner: "go through all the data picks and double check they are all correct")
47 races (scripts/datapick_2026-11-04/verify.py, verify_out.txt): every Data pick = the top horse on the price-free chance; the same
horse in the locked 09:30 pack, the course card PDF and the GitHub file; every Data pick still in the 11:08 price list. Figures in the
reasons re-checked against the card / evidence pack (jockey + trainer 14 days, marks, days off, course/trip records, chances).
FAULTS FOUND IN THE REASON WORDING (fixed, cards re-drawn, picks unchanged):
- 'Well treated by the handicapper ... on its best form' used Racing Post's card rating (career figure), e.g. Alnofoor '35lb above'
  (its best run in our records since 2025 = 20lb above). Now uses the horse's own best of its last 3 runs within a year, with course + date.
- 'Back on a winning mark ... Nlb below its last winning mark' used an OLDER win when the last win's mark was missing (Rhoscolyn,
  Wobwobwob, Look Back Smiling had won last time). Now only the last win, and nothing is said when its mark is missing.
- The same run was counted twice when Racing Post + Sporting Life both held it (e.g. 'Curragh (IRE)' + 'Curragh') -> 'two runs ago' /
  'three runs ago' and trip counts could be wrong (Monologue, Saint Acclaim). Now one run per day.
28 of 47 races had at least one reason line changed.

## 5. Can any way of picking find MORE winners than the favourite? (owner 4 Nov evening: "not always the favourite wins")
History 2023-26, 47,638 UK/IRE races, models fitted on earlier years only (scripts blend.py, open.py):
- SP favourite 16,456 winners (34.5%); our joint model 16,206 (34.0%); Data pick (price ignored) 13,363 (28.1%).
- Giving the data MORE weight than now: x1.1 16,247, x1.5 15,958, x2.0 15,574 - every step up loses winners.
- 'Favourite unless the Data horse rates 2-3x its price': 15,240-15,952 - fewer winners.
- Open races (favourite 4.00+ at SP): favourite won 18% | 22%, Data pick 15% | 15%. 16+ runner handicaps: favourite 21% | 24%,
  Data pick 15% | 13%. The favourite or 2nd favourite wins 34-79% depending on the favourite's price.
Conclusion: in no group does a non-favourite rule find more winners than the favourite. Favourites lose ~2 races in 3, but nothing in
our data says WHICH horse wins those races better than the market. The edge is the price taken (09:30 + Best Odds Guaranteed, early
bookmaker prices, extra places) and which races to bet, not more winners. E18 (section 2) is the only group where the Data pick matched.
