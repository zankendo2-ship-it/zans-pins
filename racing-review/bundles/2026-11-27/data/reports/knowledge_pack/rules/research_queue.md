# ZANS research queue - one idea per helper per night (owner 19 Oct: "Let's start using helper agents")

Rules for every helper test: UK/IRE only; history split 2019-21 | 2022-26 (or 2025 | 2026 out of sample with
/tmp/claude-0/improve/hist10.pkl) AND the live locked picks (predict.leak_finder.first_locked) split in halves; A/E v
margin-free market + profit at SP (and at the 09:30 price / BOG for live); never adopt from one period. Mark DONE with the
date + one-line result + report path. Main session decides; helpers never change predict/ code or push.

## Open
16. Irish evening AW cards (Dundalk 23 Oct): 7 of 8 races had NO bookmaker price at any of our checks -> picks ran on static
    Sporting Life quotes. Card flag 'no bookmaker price yet' + test a late (16:00 UK) price check for evening cards.
13. Test claims 3 + 4 (unique top-RPR favourite; Oct-Nov hurdle handicap favourites) against OUR MODEL (fit < test year) and live locked picks - multiples ordering / 2 Nov rebuild.
4. Stewards 'ran green last time' (A/E 1.20 | 1.10) and 'no explanation' (0.85 | 0.89) as model features (queued for the
   2 Nov rebuild) - measure on hist10 + 2026 live how many winners they would add.
5. Favourite priced 5.50+ / in 16+ runner fields (history A/E 1.54 / 1.30): small-stake win angle? test at the 09:30 price.
7. Big-field handicaps (12+ runners) 7/10+ picks live 14/32 -£27.20 (9 Oct) - re-test with all days since.
8. Second favourite when our pick is the favourite under 7/10: dutching the top two in weak-favourite races?
9. Trainer form 14d + course record together for 7/10+ picks (both cold v both hot).
11. JUMPS Oct-Nov runners whose last run was on the FLAT (market A/E 1.00 | 0.89 | 0.79, 2019-22 | 2023-25 | 2026)
   - re-test v the model at the end of Nov with live picks; E12 (mid-season jumps absence) is pre-registered for 2 Nov.
10. Going changed during the day (weather/ground_check) v our picks' results since 10 Oct.

17. (24 Oct) Cheltenham TEST v OUR MODEL: front-runner when 3+ front-runners 0.71 (503; 0.82 | 0.61); non-favourites back
    90-179 days 0.82 (0.74 | 0.87). Needs a new rule kind (strong-pace leader) - test on the model before any rule.
18. (24 Oct) DATA: Sporting Life results write PU for fallers/unseaters when no casualty code (Spectacularsunrise F, Society
    Soldier UR, Turndlightsdownlow UR) - read the comment ('fell', 'unseated') in results_sl.fetch; check fell_lto inputs.
19. (24 Oct) DATA: reused horse names (National Anthem debutant carried 7 runs of a 2018-20 namesake; Delusionofgrandeur, Berwick
    Law) - re-test scripts/identity_fix.patch at the 2 Nov rebuild; meanwhile coverage should flag runs dated before birth year+2.

## Done
15. (26 Oct) Doncaster soft/heavy low draw straight 5-7.5f 10+: v model 1.41 | 1.23 (thin) -> provisional x1.04 proposed; needs draw_low variant with trip/field limits before the early-Nov card (reports/research/helpers/2026-10-26_doncaster_soft_low_draw.md).
- 14. Lightly raced 7/10+ (24 Oct, reports/research/helpers/2026-10-24_lightly_raced.md): NOT data gaps (23/184) and not unexposed flat horses; loss = lightly raced jumps (mostly maiden/novice, already off the slip) + shorter prices; history favourites with <=4 runs no worse (flat 1.07|1.05, jumps 1.11|1.11). No rule.
- 12 (23 Oct) team proposals checked (reports/research/helpers/2026-10-23_team_proposals_check.md): HOLD = unique top-RPR favourite 1.14|1.10, Oct-Nov hurdle hcap favs 1.17|1.20 (unique +2-4% SP), jumps LTO winners up 0-4lb 0.94|0.97; NOT = cold yard, turf 61+ days (flat-only too small), jumps-fav 90-day relax (no difference 2023-26); Champions-week favs too small.
- 22 Oct: Sky Bet only v best price (7/10+ locked picks 2-21 Oct, 255 bets) - Sky best on 89%, Sky-only costs £8.50; Sky + BOG
  +£305.61 v best price +£156.40 -> keep Sky Bet + BOG. reports/research/helpers/2026-10-22_skybet_v_best.md
  (item 4 skipped tonight: /tmp/claude-0/improve/hist10.pkl was lost in the 22 Oct container reset - rebuild before running it)
- 21 Oct: drifted 15%+ rule - 'move' drift (first price -> 09:30) 2/13 -£78.70 both halves -> keep; overnight drift 1.15-1.33
  11/21 +£30.50 but 1/4 then 10/17 -> no change, re-test at 40. reports/research/helpers/2026-10-21_drift_rule.md
- 20 Oct: 'never run at this trip' rule - blanket rule not supported in history (2025|2026); only flat turf never-at-trip
  (A/E 1.01|1.00 v 1.06|1.08) + first run in the code weaker -> proposed narrowing to the owner.
  reports/research/helpers/2026-10-20_never_at_trip.md
- 19 Oct: jockey concentration (one jockey on many picks of a card) - no harm in 2025|2026 history or 2019-26 top-2
  runners; live 7/10+ k=4+ 5/14 (small) -> no rule; AW-after-G1 dip mixed (1.05 | 0.91), watch.
  reports/research/helpers/2026-10-19_jockey_concentration.md
- 19 Oct: second-stage winner filter (logistic / GBM / value) v raw confidence, 2025 <-> 2026: no gain (AUC 0.665 v 0.664);
  files /tmp/claude-0/improve/helper_filter/.
