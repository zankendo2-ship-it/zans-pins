# ZANS course knowledge base

Everything the ZANS project has measured about each UK and Irish racecourse, one file per course AND code:
`courses/<course>_flat.md`, `courses/<course>_aw.md`, `courses/<course>_jumps.md` (only the codes the course runs).
Built 2026-10-19 by `scripts/course_kb.py` from our own results history (2019 onwards). Use it for course guides at three
levels: beginner (sections 1-2 and the favourites table), advanced (sections 3-4 a-e), pro (4 f-k and section 5).

## What every table follows
- **Going** is the exact official description: GB turf Firm / Good to Firm / Good / Good to Soft / Soft / Heavy (Hard if
  any); Ireland adds Good to Yielding / Yielding / Yielding to Soft / Soft to Heavy; all-weather Fast / Standard to Fast /
  Standard / Standard to Slow / Slow. "X, Y in places" counts as X.
- **Sample labels:** LOW 20-59 races, MEDIUM 60-149, HIGH 150+. Under 20 races only the race count is shown.
- **Two periods on every row:** 2019-21 and 2022-26, each with its count (n = races, or runners/rides for people and groups).
  Trust a pattern only when both periods point the same way.
- Every table title says what it counts and over which dates.
- Jumps files split every table into Hurdles, Chases and Bumpers (NH flat).

## How to read the figures
- **A/E (actual / expected)**: winners divided by the winners the starting prices predicted, bookmaker margin removed.
  1.00 = exactly as priced; 1.10 = 10% more winners than the market expected; under 1.00 = over-bet.
- **PRB (percentage of rivals beaten)**: 0.50 = average; not distorted by field size.
- **IV (impact value)**: share of winners / share of runners. Leaders' pace IV is about 2 everywhere (comments are written
  after the race), so compare with the national figure for the same trip and going, which every pace row shows.
- **£1 SP P/L**: level stakes at starting price.
- **Claims are inferred** from handicap weights (carried weight + rating gap to the top-rated horse) month by month, because
  our results do not record claims; checked against the claims printed on our racecards since 23 Sep 2026
  (89.9% of 4,875 jockey-days agree (23 Sep-18 Oct 2026); by the claim printed on the card: no claim 96%, 3lb 73%, 5lb 90%, 7lb 68% (most misses are 7lb riders read as no claim), 10lb 76%).
- **Going pace** = winners' times against the ZANS standard time for the track and trip (a class-par time, so most winners
  run a few seconds over it): compare goings with each other, not the raw number.
- **ZANS stiffness indicator** = our standard times against the median UK/IRE track over the same trips.

## Sources and rules for customer copy
- Results: UK/IRE results (Kaggle Racing Post-format archive to May 2026 + our own Racing Post results store since).
  Our own figures (A/E, PRB, IV, standard times, method tests) are ZANS's to publish.
- Section 2 guide facts are QUOTES from public course guides: research only, rewrite in your own words.
- No Racing Post ratings (RPR/Topspeed), comments or Spotlight text in customer copy. Rules that mention "top RPR" describe
  how ZANS picks; say "top-rated on recent form" for customers.
- UK and Ireland only.

## Gaps
- Dundalk: the archive lacks Dundalk before 2025, so its counts are small.
- Newmarket: Rowley Mile only (no July Course history in the archive).
- Draw tables need every runner's draw and 6+ runners; pace needs a readable race comment.

## Files
| Course | Country | Code | File | Races since 2019 | ZANS method |
|---|---|---|---|---|---|
| Aintree | GB | JUMPS | [courses/aintree_jumps.md](courses/aintree_jumps.md) | 388 | - |
| Ascot | GB | FLAT | [courses/ascot_flat.md](courses/ascot_flat.md) | 886 | yes |
| Ascot | GB | JUMPS | [courses/ascot_jumps.md](courses/ascot_jumps.md) | 367 | - |
| Ayr | GB | FLAT | [courses/ayr_flat.md](courses/ayr_flat.md) | 924 | yes |
| Ayr | GB | JUMPS | [courses/ayr_jumps.md](courses/ayr_jumps.md) | 617 | - |
| Ballinrobe | IRE | FLAT | [courses/ballinrobe_flat.md](courses/ballinrobe_flat.md) | 128 | - |
| Ballinrobe | IRE | JUMPS | [courses/ballinrobe_jumps.md](courses/ballinrobe_jumps.md) | 429 | - |
| Bangor-on-Dee | GB | JUMPS | [courses/bangor_on_dee_jumps.md](courses/bangor_on_dee_jumps.md) | 613 | - |
| Bath | GB | FLAT | [courses/bath_flat.md](courses/bath_flat.md) | 1,035 | yes |
| Bellewstown | IRE | FLAT | [courses/bellewstown_flat.md](courses/bellewstown_flat.md) | 313 | yes |
| Bellewstown | IRE | JUMPS | [courses/bellewstown_jumps.md](courses/bellewstown_jumps.md) | 141 | - |
| Beverley | GB | FLAT | [courses/beverley_flat.md](courses/beverley_flat.md) | 968 | - |
| Brighton | GB | FLAT | [courses/brighton_flat.md](courses/brighton_flat.md) | 957 | yes |
| Carlisle | GB | FLAT | [courses/carlisle_flat.md](courses/carlisle_flat.md) | 618 | - |
| Carlisle | GB | JUMPS | [courses/carlisle_jumps.md](courses/carlisle_jumps.md) | 551 | - |
| Cartmel | GB | JUMPS | [courses/cartmel_jumps.md](courses/cartmel_jumps.md) | 437 | - |
| Catterick | GB | FLAT | [courses/catterick_flat.md](courses/catterick_flat.md) | 893 | yes |
| Catterick | GB | JUMPS | [courses/catterick_jumps.md](courses/catterick_jumps.md) | 453 | - |
| Chelmsford City | GB | AW_FLAT | [courses/chelmsford_city_aw.md](courses/chelmsford_city_aw.md) | 2,593 | - |
| Cheltenham | GB | JUMPS | [courses/cheltenham_jumps.md](courses/cheltenham_jumps.md) | 770 | - |
| Chepstow | GB | FLAT | [courses/chepstow_flat.md](courses/chepstow_flat.md) | 753 | - |
| Chepstow | GB | JUMPS | [courses/chepstow_jumps.md](courses/chepstow_jumps.md) | 815 | yes |
| Chester | GB | FLAT | [courses/chester_flat.md](courses/chester_flat.md) | 760 | - |
| Clonmel | IRE | FLAT | [courses/clonmel_flat.md](courses/clonmel_flat.md) | 61 | - |
| Clonmel | IRE | JUMPS | [courses/clonmel_jumps.md](courses/clonmel_jumps.md) | 567 | yes |
| Cork | IRE | FLAT | [courses/cork_flat.md](courses/cork_flat.md) | 548 | yes |
| Cork | IRE | JUMPS | [courses/cork_jumps.md](courses/cork_jumps.md) | 565 | yes |
| Curragh | IRE | FLAT | [courses/curragh_flat.md](courses/curragh_flat.md) | 1,384 | yes |
| Doncaster | GB | FLAT | [courses/doncaster_flat.md](courses/doncaster_flat.md) | 1,302 | - |
| Doncaster | GB | JUMPS | [courses/doncaster_jumps.md](courses/doncaster_jumps.md) | 607 | - |
| Down Royal | IRE | FLAT | [courses/down_royal_flat.md](courses/down_royal_flat.md) | 280 | yes |
| Down Royal | IRE | JUMPS | [courses/down_royal_jumps.md](courses/down_royal_jumps.md) | 413 | - |
| Downpatrick | IRE | JUMPS | [courses/downpatrick_jumps.md](courses/downpatrick_jumps.md) | 526 | yes |
| Dundalk | IRE | AW_FLAT | [courses/dundalk_aw.md](courses/dundalk_aw.md) | 279 | yes |
| Epsom | GB | FLAT | [courses/epsom_flat.md](courses/epsom_flat.md) | 507 | yes |
| Exeter | GB | JUMPS | [courses/exeter_jumps.md](courses/exeter_jumps.md) | 746 | - |
| Fairyhouse | IRE | FLAT | [courses/fairyhouse_flat.md](courses/fairyhouse_flat.md) | 346 | - |
| Fairyhouse | IRE | JUMPS | [courses/fairyhouse_jumps.md](courses/fairyhouse_jumps.md) | 869 | yes |
| Fakenham | GB | JUMPS | [courses/fakenham_jumps.md](courses/fakenham_jumps.md) | 504 | yes |
| Ffos Las | GB | FLAT | [courses/ffos_las_flat.md](courses/ffos_las_flat.md) | 443 | yes |
| Ffos Las | GB | JUMPS | [courses/ffos_las_jumps.md](courses/ffos_las_jumps.md) | 701 | yes |
| Fontwell | GB | JUMPS | [courses/fontwell_jumps.md](courses/fontwell_jumps.md) | 1,029 | yes |
| Galway | IRE | FLAT | [courses/galway_flat.md](courses/galway_flat.md) | 359 | - |
| Galway | IRE | JUMPS | [courses/galway_jumps.md](courses/galway_jumps.md) | 412 | yes |
| Goodwood | GB | FLAT | [courses/goodwood_flat.md](courses/goodwood_flat.md) | 954 | yes |
| Gowran Park | IRE | FLAT | [courses/gowran_park_flat.md](courses/gowran_park_flat.md) | 723 | yes |
| Gowran Park | IRE | JUMPS | [courses/gowran_park_jumps.md](courses/gowran_park_jumps.md) | 348 | yes |
| Hamilton | GB | FLAT | [courses/hamilton_flat.md](courses/hamilton_flat.md) | 903 | yes |
| Haydock | GB | FLAT | [courses/haydock_flat.md](courses/haydock_flat.md) | 1,069 | yes |
| Haydock | GB | JUMPS | [courses/haydock_jumps.md](courses/haydock_jumps.md) | 398 | - |
| Hereford | GB | JUMPS | [courses/hereford_jumps.md](courses/hereford_jumps.md) | 686 | yes |
| Hexham | GB | JUMPS | [courses/hexham_jumps.md](courses/hexham_jumps.md) | 726 | yes |
| Huntingdon | GB | JUMPS | [courses/huntingdon_jumps.md](courses/huntingdon_jumps.md) | 880 | yes |
| Kelso | GB | JUMPS | [courses/kelso_jumps.md](courses/kelso_jumps.md) | 723 | yes |
| Kempton | GB | AW_FLAT | [courses/kempton_aw.md](courses/kempton_aw.md) | 3,281 | yes |
| Kempton | GB | JUMPS | [courses/kempton_jumps.md](courses/kempton_jumps.md) | 550 | - |
| Kilbeggan | IRE | JUMPS | [courses/kilbeggan_jumps.md](courses/kilbeggan_jumps.md) | 534 | - |
| Killarney | IRE | FLAT | [courses/killarney_flat.md](courses/killarney_flat.md) | 365 | yes |
| Killarney | IRE | JUMPS | [courses/killarney_jumps.md](courses/killarney_jumps.md) | 385 | yes |
| Laytown | IRE | FLAT | [courses/laytown_flat.md](courses/laytown_flat.md) | 36 | - |
| Leicester | GB | FLAT | [courses/leicester_flat.md](courses/leicester_flat.md) | 908 | yes |
| Leicester | GB | JUMPS | [courses/leicester_jumps.md](courses/leicester_jumps.md) | 372 | - |
| Leopardstown | IRE | FLAT | [courses/leopardstown_flat.md](courses/leopardstown_flat.md) | 882 | yes |
| Leopardstown | IRE | JUMPS | [courses/leopardstown_jumps.md](courses/leopardstown_jumps.md) | 421 | - |
| Limerick | IRE | FLAT | [courses/limerick_flat.md](courses/limerick_flat.md) | 250 | - |
| Limerick | IRE | JUMPS | [courses/limerick_jumps.md](courses/limerick_jumps.md) | 733 | yes |
| Lingfield | GB | FLAT | [courses/lingfield_flat.md](courses/lingfield_flat.md) | 606 | - |
| Lingfield | GB | AW_FLAT | [courses/lingfield_aw.md](courses/lingfield_aw.md) | 2,946 | - |
| Lingfield | GB | JUMPS | [courses/lingfield_jumps.md](courses/lingfield_jumps.md) | 323 | - |
| Listowel | IRE | FLAT | [courses/listowel_flat.md](courses/listowel_flat.md) | 220 | yes |
| Listowel | IRE | JUMPS | [courses/listowel_jumps.md](courses/listowel_jumps.md) | 346 | yes |
| Ludlow | GB | JUMPS | [courses/ludlow_jumps.md](courses/ludlow_jumps.md) | 719 | - |
| Market Rasen | GB | JUMPS | [courses/market_rasen_jumps.md](courses/market_rasen_jumps.md) | 1,013 | yes |
| Musselburgh | GB | FLAT | [courses/musselburgh_flat.md](courses/musselburgh_flat.md) | 845 | yes |
| Musselburgh | GB | JUMPS | [courses/musselburgh_jumps.md](courses/musselburgh_jumps.md) | 493 | - |
| Naas | IRE | FLAT | [courses/naas_flat.md](courses/naas_flat.md) | 695 | yes |
| Naas | IRE | JUMPS | [courses/naas_jumps.md](courses/naas_jumps.md) | 435 | - |
| Navan | IRE | FLAT | [courses/navan_flat.md](courses/navan_flat.md) | 539 | yes |
| Navan | IRE | JUMPS | [courses/navan_jumps.md](courses/navan_jumps.md) | 495 | - |
| Newbury | GB | FLAT | [courses/newbury_flat.md](courses/newbury_flat.md) | 954 | - |
| Newbury | GB | JUMPS | [courses/newbury_jumps.md](courses/newbury_jumps.md) | 556 | - |
| Newcastle | GB | AW_FLAT | [courses/newcastle_aw.md](courses/newcastle_aw.md) | 3,384 | yes |
| Newcastle | GB | JUMPS | [courses/newcastle_jumps.md](courses/newcastle_jumps.md) | 635 | - |
| Newmarket | GB | FLAT | [courses/newmarket_flat.md](courses/newmarket_flat.md) | 1,291 | yes |
| Newton Abbot | GB | JUMPS | [courses/newton_abbot_jumps.md](courses/newton_abbot_jumps.md) | 820 | yes |
| Nottingham | GB | FLAT | [courses/nottingham_flat.md](courses/nottingham_flat.md) | 1,086 | yes |
| Perth | GB | JUMPS | [courses/perth_jumps.md](courses/perth_jumps.md) | 729 | yes |
| Plumpton | GB | JUMPS | [courses/plumpton_jumps.md](courses/plumpton_jumps.md) | 771 | yes |
| Pontefract | GB | FLAT | [courses/pontefract_flat.md](courses/pontefract_flat.md) | 804 | yes |
| Punchestown | IRE | FLAT | [courses/punchestown_flat.md](courses/punchestown_flat.md) | 93 | - |
| Punchestown | IRE | JUMPS | [courses/punchestown_jumps.md](courses/punchestown_jumps.md) | 1,101 | yes |
| Redcar | GB | FLAT | [courses/redcar_flat.md](courses/redcar_flat.md) | 919 | yes |
| Ripon | GB | FLAT | [courses/ripon_flat.md](courses/ripon_flat.md) | 823 | yes |
| Roscommon | IRE | FLAT | [courses/roscommon_flat.md](courses/roscommon_flat.md) | 298 | yes |
| Roscommon | IRE | JUMPS | [courses/roscommon_jumps.md](courses/roscommon_jumps.md) | 219 | yes |
| Salisbury | GB | FLAT | [courses/salisbury_flat.md](courses/salisbury_flat.md) | 767 | yes |
| Sandown | GB | FLAT | [courses/sandown_flat.md](courses/sandown_flat.md) | 720 | - |
| Sandown | GB | JUMPS | [courses/sandown_jumps.md](courses/sandown_jumps.md) | 396 | - |
| Sedgefield | GB | JUMPS | [courses/sedgefield_jumps.md](courses/sedgefield_jumps.md) | 821 | yes |
| Sligo | IRE | FLAT | [courses/sligo_flat.md](courses/sligo_flat.md) | 159 | - |
| Sligo | IRE | JUMPS | [courses/sligo_jumps.md](courses/sligo_jumps.md) | 307 | yes |
| Southwell | GB | AW_FLAT | [courses/southwell_aw.md](courses/southwell_aw.md) | 2,847 | yes |
| Southwell | GB | JUMPS | [courses/southwell_jumps.md](courses/southwell_jumps.md) | 861 | yes |
| Stratford | GB | JUMPS | [courses/stratford_jumps.md](courses/stratford_jumps.md) | 818 | yes |
| Taunton | GB | JUMPS | [courses/taunton_jumps.md](courses/taunton_jumps.md) | 609 | - |
| Thirsk | GB | FLAT | [courses/thirsk_flat.md](courses/thirsk_flat.md) | 816 | - |
| Thurles | IRE | FLAT | [courses/thurles_flat.md](courses/thurles_flat.md) | 68 | yes |
| Thurles | IRE | JUMPS | [courses/thurles_jumps.md](courses/thurles_jumps.md) | 500 | - |
| Tipperary | IRE | FLAT | [courses/tipperary_flat.md](courses/tipperary_flat.md) | 288 | - |
| Tipperary | IRE | JUMPS | [courses/tipperary_jumps.md](courses/tipperary_jumps.md) | 277 | - |
| Tramore | IRE | FLAT | [courses/tramore_flat.md](courses/tramore_flat.md) | 92 | - |
| Tramore | IRE | JUMPS | [courses/tramore_jumps.md](courses/tramore_jumps.md) | 539 | yes |
| Uttoxeter | GB | JUMPS | [courses/uttoxeter_jumps.md](courses/uttoxeter_jumps.md) | 1,209 | yes |
| Warwick | GB | JUMPS | [courses/warwick_jumps.md](courses/warwick_jumps.md) | 846 | - |
| Wetherby | GB | FLAT | [courses/wetherby_flat.md](courses/wetherby_flat.md) | 155 | - |
| Wetherby | GB | JUMPS | [courses/wetherby_jumps.md](courses/wetherby_jumps.md) | 644 | yes |
| Wexford | IRE | FLAT | [courses/wexford_flat.md](courses/wexford_flat.md) | 6 | - |
| Wexford | IRE | JUMPS | [courses/wexford_jumps.md](courses/wexford_jumps.md) | 611 | - |
| Wincanton | GB | JUMPS | [courses/wincanton_jumps.md](courses/wincanton_jumps.md) | 691 | - |
| Windsor | GB | FLAT | [courses/windsor_flat.md](courses/windsor_flat.md) | 1,256 | - |
| Windsor | GB | JUMPS | [courses/windsor_jumps.md](courses/windsor_jumps.md) | 51 | - |
| Wolverhampton | GB | AW_FLAT | [courses/wolverhampton_aw.md](courses/wolverhampton_aw.md) | 4,528 | yes |
| Worcester | GB | JUMPS | [courses/worcester_jumps.md](courses/worcester_jumps.md) | 916 | yes |
| Great Yarmouth | GB | FLAT | [courses/yarmouth_flat.md](courses/yarmouth_flat.md) | 1,259 | yes |
| York | GB | FLAT | [courses/york_flat.md](courses/york_flat.md) | 961 | yes |
