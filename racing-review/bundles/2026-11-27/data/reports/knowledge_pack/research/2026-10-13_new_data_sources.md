# New data sources + angles (owner 13 Oct: "what other data can you get from online that will help get a lot more winners")

Status key: HAVE = already in the system; NEW-FREE = free and reachable; NEW-PAID = costs money; BLOCKED = not reachable from GitHub/cloud.

## New data (not yet used)
1. Sectional times (NEW-FREE, partial): At The Races result pages (Sectional Times / Sectional Tools tabs, ~48h after the race; finishing speed %).
   Free for the 4 all-weather courses (AW Championships); full GB coverage is licensed by TPD (NEW-PAID). Use: which horses finished fastest
   (hidden form), pace-collapse races, horses hampered by slow pace.
2. GoingStick readings + rail movements (NEW-FREE): TurfTrax / BHA going reports per fixture. Use: going drift during the day; rail moves change
   race distances (Wetherby was wrong for 5 years) and inside-draw value.
3. Jockey booking upgrades (NEW-FREE, derivable): top jockey booked for a lower-profile yard / first ride for a trainer; jockey travelling far for one ride.
4. Multiple entries + chosen race (NEW-FREE, from RP entries pages): horse entered in 2-3 races, trainer picks this one.
5. Horses-to-follow from in-running comments (HAVE the comments): "ran on well / not clear run / hampered / slowly away" -> next-time-out list.
6. Stable form cycles (HAVE data): trainer last 14/30 days already; add yard "cold spell" (0 from 20+).
7. Market data: Betfair exchange prices/volumes (BLOCKED - GitHub runners in USA get 403; owner said no paid feeds). Oddschecker 403. Sporting
   Life 3 bookmakers = what we have.
8. Paid ratings: Timeform, Racing Post RP+ (Topspeed history, Spotlight), Proform, Geegeez Gold (pace/draw/sectionals tools) (NEW-PAID).

## Scotty tips
Search found "Scotty Tips" linked to Indication Racing (paid UK tipping). Trustpilot reviews are mixed; one reviewer says no profit/loss record is
published. No verifiable results found -> cannot confirm "loads of money". Other Scottys found: Scotty Amor (Australian analyst), 'Scottielove' on
OLBG (self-reported +414 pts, 34% strike rate, not checked).
Sources: https://ca.trustpilot.com/review/indicationracing.com , https://www.olbg.com/best-tipsters/Horse_Racing/2/5764

## TESTED 13 Oct on our history (results_form 2018-2026, margin-free SP A/E; 2018-22 | 2023-26) - scripts/angles_history_check.py
| Angle (horse's next run) | A/E 2018-22 | ROI SP | A/E 2023-26 | ROI SP |
|---|---|---|---|---|
| quick return <=7d after winning | 1.07 | -10.6% | 1.08 | -10.4% |
| first run for new trainer | 1.10 | -16.6% | 1.07 | -23.0% |
| quick return <=7d after placing | 1.07 | -12.7% | 1.05 | -14.2% |
| jockey upgrade (prior-yr SR +6 pts) | 1.03 | -20.4% | 1.04 | -18.0% |
| LTO pulled hard, beaten <=5L | 1.03 | -17.5% | 1.04 | -15.3% |
| LTO vet/kit excuse (lost shoe, bled, vet said) | 1.02 | -29.7% | 1.04 | -14.7% |
| beaten favourite LTO | 1.03 | -17.3% | 1.02 | -18.1% |
| LTO interference (not clear run, hampered) | 1.02 | -21.1% | 1.01 | -21.2% |
| 2nd LTO beaten <=1L | 1.03 | -15.5% | 1.01 | -20.5% |
| LTO bad start (slowly away) | 0.98 | -30.5% | 0.96 | -27.9% |
| all runners (baseline) | 1.00 | -26.1% | 1.00 | -24.8% |
Short-priced (<=4.0): quick return after win 1.10/1.10, after 2nd/3rd 1.09/1.10, new trainer 1.06/1.10 - all still lose at SP (-5 to -10%).
MODEL TEST (scripts/newfeat_model_check.py): 4 new features (quick return after win / after place, new trainer, back within 14d after win)
added to the walk8 model, fitted 2019-24, scored 2025 + 2026: flat 2509->2509 and 1971->1962 winners, jumps 1784->1782 and 1366->1360;
log-lik unchanged -> NOT adopted (the price + current features already carry it).

## Pro tipsters / pro punters - what they actually do
- Scotty Tips (@ScottyTips; runs Indication Racing): Telegram community "2,000+ paid members", "1-2 tips a day", "37 of 46 months profit"
  (own claim, no independent proof found); Trustpilot split - critics: mostly short favourites / odds-on in free group, no P/L shown, bookmaker
  sign-up affiliate links. X posts: "All 4 VIP tips WON", a 25/1 winner. Promotes other tipsters. -> marketing + selectivity, not proven edge.
- Pricewise (Tom Segal, Racing Post): value at EARLY Saturday prices; long-run return claimed ~+50% at advised prices but prices go in 10-15 min;
  SBC measured about -9% to advised prices since 2021. Lesson: the edge is the early price.
- Patrick Veitch (~£10m 1999-2007): own ratings v the price, bet only when price > his chance, huge volume via agents, judged over many bets.
- Bill Benter (Hong Kong, ~$1bn): conditional logit form model BLENDED WITH THE PUBLIC ODDS (= our joint model design), bet only where the
  blend beats the price; 120+ variables.
- Alan Potts: value only, 2/1 minimum ("to make money under 2/1 you need a very high strike rate"), elimination to 1-4 contenders.
- SBC (Smart Betting Club): independently proofs tipsters; best long-term ones ~15-25% ROI over 10+ years, measured at BSP / proofed prices.
- Each-way extra places: the documented edge is bookmaker extra places v standard place terms (matched-betting style) - our BET NOW (Sky Bet
  extra places) is this idea.

## ROUND 2 (13 Oct, owner: "Get as much data tested as you can now")
Full tables: reports/research/2026-10-13_angles_batch2.txt (60+ form angles, 2018-22 v 2023-26) and _angles_breed.txt (sire/headgear/owner/sex,
2018-21 v 2022-26, from the new Kaggle breeding extract data-extract/results_breed.csv.gz, 1.29m runners 2015-26).
- Every angle loses at SP on its own. Beat the market in both periods (A/E >= 1.05): favourite in 16+ runner field 1.15/1.15, last RPR a career
  best by 7+ 1.16/1.07, favourites 1.08/1.07 (favourite-longshot bias: 20/1+ shots 0.74/0.75 = worst value in racing at SP), first-time visor
  in jumps 1.10/1.12, headgear removed (flat) 1.05/1.07. Owner's 2nd string (longer-priced of 2+ same-owner runners) 0.91/0.94; mares v geldings
  in jumps 0.95/0.93.
- SIRE STATS = NO EDGE: sire good on the going 1.02-1.07 then 1.02; sire good + horse first time on that going 0.98/0.99 (flat), 0.86/1.00 (jumps).
- MODEL TESTS (walk8, fit 2019-24, test 2025 / 2026, winners of the top pick):
  9 form features: flat 2509->2506 / 1971->1981, jumps 1784->1796 / 1366->1374, log-lik worse in 2025 both codes -> no.
  new trainer + RPR career-best-by-7: flat 2511 / 1969, jumps 1793 / 1362; log-lik better in all 4 sets (tiny).
  first-time visor (jumps) + headgear removed (flat) + owner 2nd string + mare v geldings: flat 2510 / 1972, jumps 1786 / 1374; log-lik better in all 4.
  -> small but consistent; about +15-20 winners per 22,000 races. Queue for the next model rebuild (needs live features: card headgear_first,
  owner, sex_code, last trainer). Not rushed into the live picks.
