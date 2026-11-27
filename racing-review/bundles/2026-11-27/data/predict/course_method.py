"""Apply a course's ZANS method (methods/<course>/<CODE>.md) on top of the model's chances.

Newmarket flat v25.0: the model chance of each runner is multiplied by the evidence-backed
angle factors below (the course A/E, shrunk about halfway towards 1.00 for sample size),
then renormalised within the race. The RPR anchor (best RPR at today's trip +-1f on today's
going group) is always printed with its status. Caution tags are shown but never block a pick.

    python -m predict.course_method --date 2026-09-24 --course newmarket --history history/*.csv.gz
"""
import argparse
import csv
import json
import re
from pathlib import Path

from form.history import days_since, name_key, open_text, to_int, weight_lbs
from track_stats.parse import course_key, dist_to_furlongs, going_group

from .today import CONFIDENCE, LONGSHOT_PRICE, confidence, frac, frac_at_least, num

REPO_ROOT = Path(__file__).resolve().parent.parent
from predict import bet_tag  # noqa: E402
SHORT_FAV_PRICE = 2.5  # owner 2026-09-30: a short-priced favourite our evidence disagrees with -> caution
BET_RULE = "confidence"   # 9 Oct: back to "confidence" (8+ and evidence agrees) - the 2.00-2.99 "price_band" trial (2-9 Oct) won 24/59
                          # -£24.90 at the 09:30 price v the old rule 32/48 +£84.80, and the old rule was ahead in both halves
BET_BAND = (2.0, 3.0)      # decimal price range for a BET under the trial rule (2.00 up to 2.99)


def is_bet(conf, agrees, price):
    if BET_RULE == "confidence":
        return conf >= 8 and agrees
    return bool(agrees and price and BET_BAND[0] <= price < BET_BAND[1])
SLOW_START = re.compile(r"dwelt|slowly away|missed break|slowly into stride|started slowly", re.I)

# Course overlays: (course, family) -> list of (rule, factor, evidence). Factors = the course
# A/E from methods.audit shrunk about halfway towards 1 for sample size (methods/<course>/*.md).
# PRICE-FREE (owner rule 2026-09-24): no rule may use the price or favourite status.
# Rule kinds: lone_leader, leader[lo-hi f], held_up_short, slow_start[max f], exact_rpr,
# top_rpr, ground_spec, cd_winner, older, older_hcap, improver, won_last, weak_finish, light,
# held_up[lo-hi f], hung, layoff[lo-hi days], course_win_not_cd, older_noform, unproven_trip.
ANGLES = {
    ("newmarket", "FLAT"): [
        ("lone_leader", 1.08, "lone front-runner: Newmarket A/E 1.13, +9% (298 runners)"),
        ("older_hcap", 1.08, "6yo+ in a handicap: under-rated here, A/E 1.19 (898)"),
        ("slow_start:6.5", 0.93, "slow starter at 5-6f: A/E 0.90, -57% (105)"),
        ("exact_rpr", 1.05, "top exact-conditions RPR: A/E 1.04, -5% (1,075; 1.04 / 1.04) - trimmed from 1.08 on 3 Oct re-test"),
        ("top_rpr", 1.05, "top recent RPR: Newmarket A/E 1.10 (1,371; 1.15 / 1.07)"),
        ("improver", 0.96, "improver is OVER-bet at Newmarket: A/E 0.92 (2,364; 0.99 / 0.87)"),
        ("won_last", 0.97, "won last time is over-bet at Newmarket: A/E 0.94 (2,244; 1.00 / 0.90)"),
    ],
    ("listowel", "FLAT"): [
        ("lone_leader:6.5-12", 1.15, "lone front-runner 6.5f-1m4f: Listowel A/E 1.42 (51)"),
        ("leader:6.5-12", 1.10, "usual front-runner 6.5f-1m4f: Listowel A/E 1.36 (114)"),
        ("slow_start:8.5", 0.70, "slow away 2+ of last 4, up to 1m: Listowel A/E 0.55, -70% (79)"),
        ("ground_spec", 1.15, "won on today's going, only 1-2 in field have: A/E 1.58, +18% (91)"),
        ("exact_rpr", 1.05, "top exact-conditions RPR: Listowel A/E 1.06 (Sep-Nov 1.14)"),
        ("held_up_short", 0.95, "held-up type, up to 7.5f, <2 leaders: A/E 0.96 (145)"),
        ("weak_finish", 0.97, "weakened / no extra in last 2: A/E 0.96 (726)"),
        ("cd_winner", 1.03, "course & distance winner: A/E 1.07 (93)"),
    ],
    ("listowel", "JUMPS"): [
        ("exact_rpr", 1.12, "top exact-conditions RPR: Listowel jumps A/E 1.29, +86% (304)"),
        ("lone_leader", 1.10, "lone front-runner: Listowel jumps A/E 1.24, +20% (117)"),
        ("leader", 1.06, "usual front-runner: Listowel jumps A/E 1.15 (243)"),
        ("ground_spec", 1.10, "won on today's going, only 1-2 in field have: A/E 1.24 (162)"),
        ("weak_finish", 0.92, "weakened / no extra in last 2: A/E 0.91, -45% (1,305); 25 Sep 0/4"),
        ("cd_winner", 0.90, "course & distance winner: over-bet here, A/E 0.78, -78% (97)"),
        ("unproven_trip", 0.86, "never run within 1f of this trip: Listowel jumps wins 5.9%, A/E 0.77 (544)"),
    ],
    ("worcester", "JUMPS"): [
        ("cd_winner", 1.06, "course & distance winner: Worcester A/E 1.12, +20% (585)"),
        ("top_rpr", 1.02, "top recent RPR: A/E 1.05 (888)"),
        ("leader", 0.95, "usual front-runner: over-bet at Worcester, A/E 0.91 (576)"),
        ("lone_leader", 0.93, "lone front-runner: A/E 0.86 (292)"),
        ("ground_spec", 0.94, "ground-specialist angle over-bet here: A/E 0.88 (349)"),
        ("light", 0.96, "lightly raced (5 or fewer runs): A/E 0.93, -32% (2,154)"),
    ],
    ("haydock", "FLAT"): [
        ("improver", 1.04, "improver (last RPR a career best): Haydock A/E 1.08 (1,417)"),
        ("won_last", 1.03, "won last time: A/E 1.06, break-even (1,156)"),
        ("leader", 0.96, "usual front-runner: leaders struggle at Haydock, A/E 0.93 (755)"),
        ("slow_start:8.5", 0.92, "slow away 2+ of last 4, up to 1m: A/E 0.84 (360)"),
        ("exact_rpr", 0.96, "top exact-conditions RPR over-bet at Haydock: A/E 0.93 (907)"),
        ("ground_spec", 0.93, "ground-specialist angle over-bet here: A/E 0.86 (429)"),
        ("older", 0.97, "age 6+: A/E 0.95 (1,314)"),
    ],
    ("newcastle", "AW_FLAT"): [
        ("top_rpr", 1.04, "top recent RPR: Newcastle AW A/E 1.08 (3,922)"),
        # 20 Oct review: lone front-runners hold up over 5-6f only (A/E 1.15 (115) 2019-21 | 1.14 (283) 2022-26 v other AW 1.07 | 1.02);
        # 7f+ flips (1.23 | 0.99) -> sprint-only rule, general x1.04 dropped
        ("lone_leader:0-6.5", 1.08, "lone front-runner 5-6f: Newcastle A/E 1.15 / 1.14 (398) v other AW 1.07 / 1.02"),
        ("improver", 1.02, "improver: A/E 1.05 (3,151)"),
        ("older", 0.97, "age 6+: A/E 0.95 (8,164)"),
        ("cd_winner", 0.98, "course & distance winner: A/E 0.96 (8,301)"),
        ("older_noform", 0.96, "age 6+ with no win/2nd in last 3: Newcastle AW A/E 0.89 (4,685; ~0.91 2019-21 / 0.88 since 2022) - v1.8 29 Oct"),
    ],
    ("dundalk", "AW_FLAT"): [
        ("leader", 0.93, "usual front-runner: over-bet at Dundalk, A/E 0.80, -59% (115; 2025-26 only)"),
        ("slow_start:8.5", 0.96, "slow away 2+ of last 4, up to 1m: A/E 0.89 (167)"),
        ("older", 0.96, "age 6+: A/E 0.90 (752)"),
        # top_rpr 0.96 REMOVED 2026-09-26: thin 2025-26 sample (320) and 25 Sep both hits won (Haven, Military Order)
        ("top_rpr", 1.00, "top recent RPR is NOT an edge at Dundalk: A/E 0.87, -36% (341, 2022-26 only) - national boost off (v13.3, 2 Oct)"),
        ("prominent", 1.04, "usually races prominent: Dundalk A/E 1.18 (2025) / 1.08 (2026), 1,364 runs; all GB/IRE AW 1.02 / 1.01 - TRIAL v13.4"),
    ],
    ("southwell", "AW_FLAT"): [
        ("exact_rpr", 1.05, "top exact-conditions RPR (owner's RPR Anchor): Southwell A/E 1.09 (2,948)"),
        ("top_rpr", 1.03, "top recent RPR: Southwell A/E 1.06 (3,285)"),
        ("ground_spec", 1.10, "won on today's surface/going, only 1-2 in field have: A/E 1.20, +4% (779)"),
        ("lone_leader", 1.06, "lone front-runner: Southwell A/E 1.12 (993)"),
        ("slow_start:6", 0.94, "slow starter at 5-6f: A/E 0.89 (807)"),
        ("leader", 0.96, "usual front-runner (owner's stamina-loop fade): A/E 0.93 (2,239; 0.95 in 2016-21, 0.92 in 2022-26)"),
        ("older", 0.98, "age 6+: A/E 0.96 (6,700)"),
    ],
    ("curragh", "FLAT"): [
        ("top_rpr", 1.10, "top recent RPR: Curragh A/E 1.23, +2% (1,462)"),
        ("exact_rpr", 1.05, "top exact-conditions RPR: Curragh A/E 1.10 (1,157)"),
        ("leader", 0.92, "usual front-runner over-bet at the Curragh: A/E 0.83, -38% (922)"),
        ("lone_leader", 0.94, "lone front-runner: A/E 0.87 (427)"),
        ("ground_spec", 0.96, "ground-specialist angle over-bet here: A/E 0.94 (446)"),
        ("won_last", 0.97, "won last time: over-bet here, A/E 0.94 (1,931)"),
        # 26 Sep review: tested on 2016-26 history (split periods) before adding
        ("draw_high:12", 1.03, "drawn in the top third of a 12+ field: Curragh A/E 1.06 (5,299; 1.09 in 2016-21, 1.04 in 2022-26)"),
        ("leader@SOFT", 0.85, "usual front-runner on yielding/soft: Curragh A/E 0.64 (385; 0.40 / 0.79)"),
    ],
    ("market_rasen", "JUMPS"): [
        ("top_rpr", 1.08, "top recent RPR: Market Rasen jumps A/E 1.16 (983)"),
        ("cd_winner", 0.94, "course & distance winner over-bet here: A/E 0.88, -36% (542)"),
        ("ground_spec", 0.91, "ground-specialist angle over-bet here: A/E 0.82 (482)"),
        ("leader", 0.98, "usual front-runner: A/E 0.96 (645)"),
    ],
    ("epsom", "FLAT"): [   # methods/epsom/FLAT.md v1.0 (owner v22 peak = 5 Jun card, 4/7 +£14)
        ("exact_rpr", 1.07, "top exact-conditions RPR: Epsom A/E 1.15, +13% (422)"),
        ("top_rpr", 1.03, "top recent RPR: Epsom A/E 1.05, +14% (517)"),
        ("course_win_not_cd", 1.12, "Epsom winner at another trip (handles the track): A/E 1.50 (221; 1.34 in 2016-21, 1.54 in 2022-26)"),
        ("leader:10.6-99", 1.05, "usual front-runner at 1m3f+: Epsom A/E 1.17 (199; 1.05 / 1.22)"),
        ("slow_start:8.5", 0.86, "slow away 2+ of last 4, up to 1m (owner's HR3): Epsom A/E 0.71, -53% (160)"),
        ("held_up:10.6-99", 0.89, "usual hold-up at 1m3f+ (owner's HR4): Epsom A/E 0.78 (475; 0.83 / 0.75)"),
        ("layoff:46-99", 0.90, "46-99 days off (owner's HR8): Epsom A/E 0.77 (361; 0.62 / 0.83)"),
        ("older_noform", 0.93, "age 6+ with no win/2nd in last 3: Epsom A/E 0.85 (318)"),
    ],
    ("ffos_las", "FLAT"): [   # methods/ffos_las/FLAT.md v2.0 (owner v1.0-1.2 peak = 4-12 Aug, 6/13 +£11.96)
        ("top_rpr", 1.06, "top recent RPR: Ffos Las A/E 1.12, +3% (407)"),
        ("cd_winner", 1.08, "course & distance winner (owner's Gdl G): Ffos Las A/E 1.21 (127; 1.65 / 1.07)"),
        ("hung", 0.82, "hung in either of last 2 runs: Ffos Las A/E 0.66, -49% (304; 0.46 / 0.71)"),
        ("leader:0-7.5", 0.90, "usual front-runner at 5-7f (owner's Trap 3): Ffos Las A/E 0.80, -44% (148; 0.57 / 0.92)"),
        ("layoff:46-99", 0.89, "46-99 days off (owner's Trap 1): Ffos Las A/E 0.77 (333; 0.80 / 0.76)"),
        ("older_noform", 0.87, "age 6+ with no win/2nd in last 3: Ffos Las A/E 0.73, -60% (243)"),
        ("unproven_trip", 0.95, "never run within 1f of this trip (owner's HR1): Ffos Las A/E 0.89, -44% (317)"),
    ],
    ("ripon", "FLAT"): [
        ("exact_rpr", 1.12, "top exact-conditions RPR: Ripon A/E 1.25, +10% (729)"),
        ("top_rpr", 1.06, "top recent RPR: Ripon A/E 1.13 (867)"),
        ("ground_spec", 1.10, "won on today's going, only 1-2 in field have: A/E 1.20 (313)"),
        ("won_last", 1.04, "won last time: Ripon A/E 1.09 (617)"),
        ("cd_winner", 1.03, "course & distance winner: Ripon A/E 1.06 (900)"),
        ("held_up_short", 0.92, "held-up type up to 7.5f, <2 leaders (owner's hold-up rule): A/E 0.85, -39% (623)"),
        ("lone_leader", 0.94, "lone front-runner over-bet at Ripon: A/E 0.87 (264)"),
        ("slow_start:8.5", 0.94, "slow away 2+ of last 4, up to 1m: A/E 0.88 (310)"),
    ],
    ("brighton", "FLAT"): [   # methods/brighton/FLAT.md v18.0 (owner v17.0/v17.2 cards 7+24 Aug, 4/12; slump v17.1 0/6)
        ("exact_rpr", 1.10, "top exact-conditions RPR: Brighton A/E 1.15, +0% (843; 1.19 / 1.13)"),
        ("ground_spec", 1.08, "won on today's going, only 1-2 in field have: A/E 1.14 (420; 1.22 / 1.10)"),
        ("lone_leader", 0.88, "lone front-runner over-bet (owner's SP17 keen leader fade): A/E 0.74, -30% (286; 0.57 / 0.82)"),
        ("unproven_trip", 0.95, "never run within 1f of this trip (owner's HR2): A/E 0.86 (243; 0.94 / 0.81)"),
    ],
    ("hamilton", "FLAT"): [   # methods/hamilton/FLAT.md v37.0 (owner v36.0/v36.2 cards 1 Aug + 2 Sep, 7/12)
        ("top_rpr", 1.00, "top recent RPR is NOT an edge at Hamilton: A/E 0.99 (947; 1.06 / 0.96) - national boost off"),
        ("cd_winner", 1.05, "course & distance winner: Hamilton A/E 1.07 (1,268; 1.04 / 1.08)"),
        ("won_last", 1.04, "won last time: A/E 1.07 (710; 1.09 / 1.06)"),
        ("improver", 1.05, "improver (last RPR a new best): A/E 1.14 (717; 1.35 / 1.04)"),
        ("lone_leader", 0.88, "lone front-runner: A/E 0.77, -36% (301; 0.64 / 0.82)"),
        ("leader", 0.92, "usual front-runner with rivals for the lead: A/E 0.82 (566; 0.72 / 0.87)"),
        ("held_up", 0.95, "usually held up (uphill finish still favours the prominent): A/E 0.90 (2,281; 0.88 / 0.91)"),
        ("older_noform", 0.94, "age 6+ with no win/2nd in last 3 (owner's HR7): A/E 0.90 (937; 0.88 / 0.91)"),
        ("ground_first@SOFT", 0.90, "first time on soft/heavy (3+ runs): Hamilton A/E 0.80 (148; 0.50 / 0.88) - added 28 Sep review"),
    ],
    ("newton_abbot", "JUMPS"): [   # methods/newton_abbot/JUMPS.md v6.0 (owner v5.0 peak = 27 Aug, 4/7 +£1.95)
        ("top_rpr", 1.06, "top recent RPR: Newton Abbot A/E 1.11, +2% (740; 1.27 / 1.01)"),
        ("improver", 1.04, "improver (last RPR a new best): A/E 1.10, +1% (635; 1.22 / 1.02)"),
        ("held_up", 1.03, "usually held up: A/E 1.07 (1,563; 1.10 / 1.05) - owner's 'handy only' law not supported"),
        ("jockey_low", 0.93, "jockey under 6% strike rate: A/E 0.89 (629; 0.91 / 0.87)"),
        ("weak_finish", 0.97, "weakened / no extra in either of last 2: A/E 0.95 (2,045; 0.92 / 0.97)"),
    ],
    ("lingfield", "JUMPS"): [   # methods/lingfield/JUMPS.md v1.0 (data-built 2 Nov, no owner jumps method; 368 races)
        ("leader", 0.94, "usual front-runner: Lingfield jumps A/E 0.59 (297; ~0.69 / 0.52)"),
        ("older_noform", 1.04, "age 6+ with no win/2nd in last 3: A/E 1.25 (1,079; ~1.25 / 1.25) - under-bet here"),
        ("improver", 1.03, "improver (last RPR a new best): A/E 1.09 (355; ~1.06 / 1.11)"),
        ("exact_rpr", 0.97, "top exact-conditions RPR: A/E 0.92 (332; ~0.93 / 0.91)"),
        ("top_rpr", 1.00, "top recent RPR flips here (~0.83 / 1.02) - national boost off"),
    ],
    ("newbury", "JUMPS"): [   # methods/newbury/JUMPS.md v1.0 (data-built 4 Nov for Thu 5 Nov, no owner method; 535 races)
        ("top_rpr", 1.06, "top recent RPR: Newbury jumps A/E 1.21, +1% (592; ~1.30 / 1.16)"),
        ("lone_leader", 1.04, "lone front-runner: A/E 1.25 (185; ~1.47 / 1.11)"),
        ("held_up", 0.97, "usually held up: A/E 0.94 (1,080; ~0.94 / 0.94)"),
        ("weak_finish", 0.96, "weakened / no extra in either of last 2: A/E 0.91 (1,526; ~0.89 / 0.92)"),
    ],
    ("naas", "JUMPS"): [   # methods/naas/JUMPS.md v1.0 (data-built 7 Nov for Sun 8 Nov, owner method is FLAT only; 430 races)
        ("top_rpr", 1.00, "top recent RPR flips here (~1.42 / 0.96) - national boost off"),
        ("exact_rpr", 1.05, "top exact-conditions RPR: Naas jumps A/E 1.18 (386; ~1.21 / 1.16)"),
        ("cd_winner", 1.05, "course & distance winner: A/E 1.27, +7% (170; ~1.49 / 1.18)"),
        ("won_last", 1.05, "won last time: A/E 1.21 (453; ~1.34 / 1.14)"),
        ("improver", 1.05, "improver (last RPR a new best): A/E 1.22 (717; ~1.34 / 1.15)"),
        ("ground_spec", 1.04, "won on today's going, only 1-2 in field have: A/E 1.24 (229; ~1.11 / 1.33)"),
        ("held_up", 0.97, "usually held up: A/E 0.91 (1,341; ~0.87 / 0.94)"),
        ("weak_finish", 0.94, "weakened / no extra in either of last 2: A/E 0.82 (1,604; ~0.66 / 0.88)"),
        ("older_noform", 0.93, "age 6+ with no win/2nd in last 3: A/E 0.80 (1,807; ~0.89 / 0.75)"),
    ],
    ("sandown", "JUMPS"): [   # methods/sandown/JUMPS.md v1.0 (data-built 7 Nov for Sun 8 Nov, owner file is FLAT only; 387 races)
        ("top_rpr", 1.03, "top recent RPR: Sandown jumps A/E 1.11 (426; ~1.28 / 1.02)"),
        ("improver", 1.04, "improver (last RPR a new best): A/E 1.14 (731; ~1.26 / 1.07)"),
        ("ground_spec", 1.03, "won on today's going, only 1-2 in field have: A/E 1.11 (148; ~1.14 / 1.08)"),
        ("held_up", 0.94, "usually held up: A/E 0.85 (764; ~0.89 / 0.82)"),
        ("weak_finish", 0.95, "weakened / no extra in either of last 2: A/E 0.89 (868; ~0.94 / 0.86)"),
    ],
    ("wincanton", "JUMPS"): [   # methods/wincanton/JUMPS.md v1.0 (data-built 6 Nov for Sat 7 Nov, no owner method; 665 races)
        ("top_rpr", 1.06, "top recent RPR: Wincanton jumps A/E 1.18, +4% (710; ~1.18 / 1.18)"),
        ("ground_spec", 1.05, "won on today's going, only 1-2 in field have: A/E 1.26, +1% (346; ~1.12 / 1.37)"),
        ("exact_rpr", 1.04, "top exact-conditions RPR: A/E 1.15 (628; ~1.12 / 1.17)"),
        ("improver", 1.02, "improver (last RPR a new best): A/E 1.06 (803; ~1.08 / 1.04)"),
        ("cd_winner", 0.95, "course & distance winner: A/E 0.87 (345; ~0.71 / 0.95)"),
        ("jockey_low", 0.94, "jockey under 6% in 12 months: A/E 0.86 (653; ~0.88 / 0.84)"),
    ],
    ("warwick", "JUMPS"): [   # methods/warwick/JUMPS.md v1.0 (data-built 2 Nov, no owner method; 808 races)
        ("improver", 1.05, "improver (last RPR a new best): Warwick A/E 1.23 (828; ~1.39 / 1.11)"),
        ("exact_rpr", 1.04, "top exact-conditions RPR: A/E 1.13 (750; ~1.21 / 1.08)"),
        ("won_last", 1.03, "won last time: A/E 1.09 (721; ~1.15 / 1.05)"),
        ("unproven_trip", 1.02, "unproven at the trip: A/E 1.04 (1,170; ~1.03 / 1.05)"),
        ("cd_winner", 0.97, "course & distance winner: A/E 0.92 (298; ~0.97 / 0.89)"),
        ("older_noform", 0.96, "age 6+ with no win/2nd in last 3: A/E 0.92 (2,233; ~0.91 / 0.93)"),
        ("top_rpr", 1.00, "top recent RPR no longer an edge here: 0.97 since 2022 (536; ~1.47 before) - national boost off"),
    ],
    ("chelmsford_city", "AW_FLAT"): [   # methods/chelmsford_city/AW_FLAT.md v1.0 (data-built 1 Nov, no owner method)
        ("exact_rpr", 1.04, "top exact-conditions RPR: Chelmsford A/E 1.07 (2,597; ~1.06 / 1.08)"),
        ("improver", 1.03, "improver (last RPR a new best): A/E 1.07 (2,409; ~1.11 / 1.03)"),
        ("leader", 1.02, "usual front-runner: A/E 1.05 (1,793; ~1.06 / 1.04)"),
        ("jockey_low", 0.95, "jockey under 6% strike rate: A/E 0.89 (1,801; ~0.97 / 0.79)"),
        ("older_noform", 0.96, "age 6+ with no win/2nd in last 3: A/E 0.92 (2,405; ~0.89 / 0.95)"),
        ("top_rpr", 1.00, "top recent RPR no longer an edge here: A/E 1.01 since 2022 (1,610; ~1.16 before) - national boost off"),
    ],
    ("wolverhampton", "AW_FLAT"): [   # methods/wolverhampton/AW_FLAT.md v2.0 (owner updates 8-10 peak, 31 Jul-17 Aug 5/13)
        ("top_rpr", 1.06, "top recent RPR: Wolverhampton A/E 1.09 (5,255; 1.07 / 1.10)"),
        ("won_last", 1.04, "won last time: A/E 1.06 (3,553; 1.08 / 1.05)"),
        ("improver", 1.04, "improver (last RPR a new best): A/E 1.06 (3,851; 1.06 / 1.06)"),
        ("older_noform", 0.97, "age 6+ with no win/2nd in last 3: A/E 0.95 (5,316; 0.97 / 0.94)"),
    ],
    ("roscommon", "JUMPS"): [   # methods/roscommon/JUMPS.md v1.0 (data-built, no owner method)
        ("top_rpr", 1.00, "top recent RPR is NOT an edge at Roscommon jumps: A/E 0.93 (203; 1.00 / 0.89) - national boost off"),
        ("ground_spec", 1.05, "won on today's going, only 1-2 in field have: A/E 1.43 (78; 1.69 / 1.07)"),
        ("lone_leader", 1.06, "lone front-runner: A/E 1.40, +14% (46; 1.18 / 1.49)"),
        ("jockey_low", 0.85, "jockey under 6% strike rate: A/E 0.74, -58% (742; 0.70 / 0.76)"),
        ("weak_finish", 0.90, "weakened / no extra in either of last 2: A/E 0.83, -44% (768; 0.89 / 0.81)"),
        ("cd_winner", 0.93, "course & distance winner over-bet here: A/E 0.61 (42, small sample)"),
    ],
    ("hereford", "JUMPS"): [   # methods/hereford/JUMPS.md v1.0 (data-built 13 Oct, no owner method; 656 races 2019-26)
        ("top_rpr", 1.06, "top recent RPR: Hereford A/E 1.15 (711; 2019-21 ~1.30 / 2022-26 1.08)"),
        ("won_last", 1.05, "won last time: A/E 1.17 (419; ~1.3 / 1.11)"),
        ("exact_rpr", 1.04, "top exact-conditions RPR: A/E 1.10 (609; ~1.08 / 1.11)"),
        ("improver", 1.04, "last RPR above its previous best: A/E 1.12 (658; ~1.10 / 1.13)"),
        ("cd_winner", 1.03, "course & distance winner: A/E 1.10 (277; ~1.15 / 1.08)"),
        ("jockey_low", 0.88, "jockey under 6% strike rate: A/E 0.72 (780; ~0.76 / 0.70)"),
        ("leader", 0.95, "usual front-runner: A/E 0.87 (521; ~0.91 / 0.85)"),
        ("weak_finish", 0.96, "weakened / no extra in either of last 2: A/E 0.93 (2,365; 0.93 / 0.93)"),
    ],
    ("punchestown", "JUMPS"): [   # methods/punchestown/JUMPS.md v1.1 (data-built 13 Oct + owner reviews 14 Oct, best 13 May 2/6; 1,076 races 2019-26)
        ("top_rpr", 1.00, "top recent RPR is NOT an edge lately at Punchestown: A/E 1.09 (1,146) but 0.99 since 2022 - national boost off"),
        ("won_last", 1.05, "won last time: A/E 1.16 (1,327; ~1.15 / 1.17)"),
        ("exact_rpr", 1.04, "top exact-conditions RPR: A/E 1.14 (943; ~1.18 / 1.11)"),
        ("improver", 1.03, "last RPR above its previous best: A/E 1.12 (1,818; ~1.22 / 1.04)"),
        ("older_noform", 0.95, "age 6+ with no win/2nd in last 3: A/E 0.87 (4,525; 0.87 / 0.87)"),
    ],
    ("cheltenham", "JUMPS"): [   # methods/cheltenham/JUMPS.md v1.0 (data-built 22 Oct, no owner method; 759 races 2019-26)
        ("top_rpr", 1.00, "top recent RPR is NOT a steady edge at Cheltenham: A/E 1.09 (838; ~1.27 / 0.98 since 2022) - national boost off"),
        ("improver", 1.02, "last RPR above its previous best: A/E 1.05 (2,199; ~1.05 / 1.05)"),
        ("weak_finish", 0.97, "weakened / no extra in either of last 2: A/E 0.93 (2,183; ~0.95 / 0.92)"),
    ],
    ("doncaster", "FLAT"): [   # methods/doncaster/FLAT.md v1.0 (data-built 22 Oct, no owner method; 1,282 races 2019-26)
        ("top_rpr", 1.08, "top recent RPR: Doncaster flat A/E 1.19 (1,452; 2019-21 ~1.17 / 2022-26 1.20)"),
        ("won_last", 1.04, "won last time: A/E 1.11 (1,667; ~1.15 / 1.09)"),
        ("held_up", 1.04, "usually held up: A/E 1.10 (3,850; ~1.12 / 1.09)"),
        ("improver", 1.03, "last RPR above its previous best: A/E 1.09 (1,932; ~1.05 / 1.11)"),
        ("older_noform", 1.03, "age 6+ out of form is UNDER-bet here: A/E 1.13 (1,174; ~1.11 / 1.14)"),
        ("weak_finish", 0.95, "weakened / no extra in either of last 2: A/E 0.91 (4,694; ~0.83 / 0.94)"),
        ("leader", 0.95, "usual front-runner: A/E 0.87 (947; ~0.73 / 0.94)"),
        ("jockey_low", 0.93, "jockey under 6% strike rate: A/E 0.83 (970; ~0.64 / 0.93)"),
    ],
    ("newbury", "FLAT"): [   # methods/newbury/FLAT.md v1.0 (data-built 22 Oct, no owner method; 943 races 2019-26)
        ("top_rpr", 1.00, "top recent RPR is NOT an edge at Newbury: A/E 1.04 (1,015; ~1.00 / 1.06) - national boost off"),
        ("older_noform", 1.05, "age 6+ out of form is UNDER-bet here: A/E 1.24 (465; ~1.21 / 1.26)"),
        ("won_last", 1.03, "won last time: A/E 1.07 (1,297; ~1.14 / 1.03)"),
        ("weak_finish", 1.03, "weakened / no extra in either of last 2 is under-bet here: A/E 1.10 (2,745; ~1.07 / 1.11)"),
    ],
    ("ffos_las", "JUMPS"): [   # methods/ffos_las/JUMPS.md v1.1 (data-built 13 Oct + owner reviews 14 Oct, peak 5 May 3/6; 672 races 2019-26)
        ("top_rpr", 1.05, "top recent RPR: Ffos Las jumps A/E 1.10 (714; 2019-21 ~1.08 / 2022-26 1.11)"),
        ("won_last", 1.03, "won last time: A/E 1.10 (503; ~1.03 / 1.14)"),
        ("improver", 1.03, "last RPR above its previous best: A/E 1.09 (663; ~1.17 / 1.04)"),
        ("weak_finish", 1.03, "weakened / no extra in either of last 2 is UNDER-bet here: A/E 1.14 (2,193; ~1.18 / 1.12)"),
        ("jockey_low", 0.92, "jockey under 6% strike rate: A/E 0.80 (689; ~0.72 / 0.85)"),
        ("unproven_trip", 0.97, "never run within 1f of this trip: A/E 0.94 (843; ~0.98 / 0.92)"),
    ],
    ("perth", "JUMPS"): [   # methods/perth/JUMPS.md v2.0 (owner Gemini reviews 3-6 + data, 14 Oct; 694 races 2019-26)
        ("top_rpr", 1.00, "top recent RPR: Perth jumps A/E 1.05 (747; 2019-21 ~1.15 / 2022-26 0.99) - boost off"),
        ("exact_rpr", 1.04, "top exact-conditions RPR: A/E 1.12 (685; ~1.17 / 1.09)"),
        ("cd_winner", 1.03, "course & distance winner: A/E 1.09 (651; ~1.09 / 1.09)"),
        ("ground_spec", 1.03, "ground specialist: A/E 1.11 (317; ~1.07 / 1.14)"),
        ("improver", 1.03, "last RPR above its previous best: A/E 1.13 (724; ~1.29 / 1.05)"),
        ("won_last", 1.02, "won last time: A/E 1.07 (658; ~1.03 / 1.09)"),
        ("lone_leader", 1.02, "lone front-runner: A/E 1.08 (249; ~1.03 / 1.11)"),
        ("weak_finish", 0.96, "weakened in either of last 2: A/E 0.91 (2,225; 0.91 / 0.91)"),
        ("older_noform", 0.97, "age 6+ no win/2nd in last 3: A/E 0.92 (1,996; ~0.84 / 0.97)"),
        ("unreliable", 0.85, "owner's Gate E/F - 2+ pulled up / unseated / fell in last 3: Perth A/E 0.37 / 0.51 (104 / 194)"),
        ("jockey_name:bowen", 1.04, "owner's Bowen axis - Sean or James Bowen riding: Perth A/E 1.32 / 1.22 (65 / 348)"),
    ],
    ("carlisle", "JUMPS"): [   # methods/carlisle/JUMPS.md v1.0 (data-built 21 Oct, no owner method; 529 races 2019-26)
        ("top_rpr", 1.00, "top recent RPR is NOT an edge at Carlisle jumps: A/E 0.98 (568; 2019-21 ~0.88 / 2022-26 1.04) - national boost off"),
        ("lone_leader", 1.04, "lone front-runner: Carlisle jumps A/E 1.20, +2% (198; ~1.40 / 1.08)"),
        ("held_up", 1.02, "usually held up: A/E 1.05 (1,244; ~1.02 / 1.07)"),
        ("exact_rpr", 0.95, "top exact-conditions RPR over-bet here: A/E 0.87 (509; ~0.74 / 0.95)"),
        ("cd_winner", 0.97, "course & distance winner over-bet here: A/E 0.93 (373; ~0.83 / 0.98)"),
        ("jockey_low", 0.90, "jockey under 6% strike rate: A/E 0.69 (445; ~0.60 / 0.80)"),
    ],
    ("ascot", "JUMPS"): [   # methods/ascot/JUMPS.md v1.0 (data-built 30 Oct, owner method is flat only; 342 races 2019-26, provisional)
        ("top_rpr", 1.05, "top recent RPR: Ascot jumps A/E 1.22 (366; 2019-21 ~1.46 / 2022-26 1.04)"),
        ("cd_winner", 1.04, "course & distance winner: A/E 1.21 (238; ~1.21 / 1.21)"),
        ("improver", 1.04, "last RPR above its previous best: A/E 1.11 (606; ~1.11 / 1.11)"),
        ("prominent", 1.02, "usually races prominent: A/E 1.05 (1,640; ~1.06 / 1.04)"),
        ("jockey_low", 0.90, "jockey under 6% strike rate: A/E 0.44 (141; ~0.42 / 0.46)"),
        ("older_noform", 0.95, "age 6+ with no win/2nd in last 3: A/E 0.84 (540; ~0.83 / 0.85)"),
        ("held_up", 0.95, "usually held up: A/E 0.85 (652; ~0.82 / 0.88)"),
        ("weak_finish", 0.97, "weakened / no extra in last 2: A/E 0.93 (871; ~0.90 / 0.95)"),
    ],
    ("ayr", "JUMPS"): [   # methods/ayr/JUMPS.md v1.0 (data-built 30 Oct, owner method is flat only; 597 races 2019-26, provisional)
        ("top_rpr", 1.04, "top recent RPR: Ayr jumps A/E 1.08 (656; 2019-21 ~1.13 / 2022-26 1.05)"),
        ("ground_spec", 1.04, "won on today's going, only 1-2 in field have: A/E 1.09 (287; ~1.09 / 1.09)"),
        ("lone_leader", 1.03, "lone front-runner: A/E 1.10 (197; ~1.22 / 1.04)"),
        ("older_noform", 0.95, "age 6+ with no win/2nd in last 3: A/E 0.88 (1,798; ~0.88 / 0.88)"),
        ("cd_winner", 0.96, "course & distance winner over-bet here: A/E 0.94 (497; ~0.89 / 0.96)"),
        ("unproven_trip", 0.97, "never run within 1f of this trip: A/E 0.94 (759; ~0.95 / 0.93)"),
    ],
    ("catterick", "JUMPS"): [],   # methods/catterick/JUMPS.md v1.0 (data-built 19 Nov): national defaults only until the reviewer PASSes the proposed factors
    ("kempton", "JUMPS"): [],   # methods/kempton/JUMPS.md v1.0 DATA-BUILT 23 Nov 2026: national defaults only
    ("taunton", "JUMPS"): [],   # methods/taunton/JUMPS.md v1.0 DATA-BUILT 24 Nov 2026: national defaults only
    ("doncaster", "JUMPS"): [],   # methods/doncaster/JUMPS.md v1.0 DATA-BUILT 26 Nov 2026: national defaults only
    ("musselburgh", "JUMPS"): [],   # methods/musselburgh/JUMPS.md v1.0 DATA-BUILT 26 Nov 2026: national defaults only
    ("exeter", "JUMPS"): [],   # methods/exeter/JUMPS.md v1.0 DATA-BUILT 21 Nov 2026: national defaults only
    ("haydock", "JUMPS"): [],   # methods/haydock/JUMPS.md v1.0 DATA-BUILT 20 Nov 2026: national defaults only; HAY-1 failed live 20 Nov, runs as a shadow
    ("wetherby", "JUMPS"): [   # methods/wetherby/JUMPS.md v1.0 (data-built 13 Oct, no owner method; 611 races 2019-26)
        ("top_rpr", 1.06, "top recent RPR: Wetherby jumps A/E 1.14 (670; 2019-21 ~1.23 / 2022-26 1.08)"),
        ("improver", 1.04, "last RPR above its previous best: A/E 1.16 (627; ~1.22 / 1.12)"),
        ("won_last", 1.03, "won last time: A/E 1.08 (554; ~1.10 / 1.07)"),
        ("exact_rpr", 1.02, "top exact-conditions RPR: A/E 1.06 (588; ~1.06 / 1.06)"),
        ("cd_winner", 0.94, "course & distance winner over-bet here: A/E 0.83 (331; ~0.95 / 0.77)"),
    ],
    ("roscommon", "FLAT"): [   # methods/roscommon/FLAT.md v1.0 (data-built 12 Oct, no owner method; 290 races 2019-26)
        ("top_rpr", 1.08, "top recent RPR: Roscommon flat A/E 1.32 (321; 2019-21 ~1.44 / 2022-26 1.27)"),
        ("exact_rpr", 1.05, "top exact-conditions RPR: A/E 1.32 (225; ~1.24 / 1.36)"),
        ("won_last", 1.05, "won last time: A/E 1.27 (185; ~1.45 / 1.19)"),
        ("improver", 1.03, "last RPR above its previous best: A/E 1.11 (320; ~1.04 / 1.14)"),
        ("older", 0.93, "age 6+: A/E 0.70 (536; 0.68 / 0.71)"),
        ("jockey_low", 0.95, "jockey under 6% strike rate: A/E 0.87 (884; 0.89 / 0.86)"),
    ],
    ("down_royal", "FLAT"): [   # methods/down_royal/FLAT.md v1.0 (data-built, no owner method)
        ("top_rpr", 1.06, "top recent RPR: Down Royal A/E 1.14 (269; 1.30 / 1.06)"),
        ("improver", 1.08, "improver (last RPR a new best): A/E 1.28, -10% (321; 1.28 / 1.28)"),
        ("held_up", 1.04, "usually held up: A/E 1.13 (710; 1.28 / 1.06)"),
    ],
    ("ayr", "FLAT"): [   # methods/ayr/FLAT.md v17.0 (owner v16.0 + v16.3 peak = 8 Aug + 19 Sep, 5/14 +£22.48)
        ("top_rpr", 1.00, "top recent RPR is NOT an edge at Ayr: A/E 1.01 (996; 1.14 / 0.95) - national boost off"),
        ("improver", 1.05, "improver (last RPR a new best): Ayr A/E 1.09 (861; 1.07 / 1.10)"),
        ("lone_leader", 1.06, "lone front-runner: Ayr A/E 1.15 (269; 1.29 / 1.08)"),
        ("slow_start:6.5", 0.90, "slow away 2+ of last 4 at 5-6f: Ayr A/E 0.67, -55% (286; 0.48 / 0.74)"),
        ("slow_start:8.5", 0.92, "slow away 2+ of last 4, up to 1m: Ayr A/E 0.80, -44% (644; 0.72 / 0.84)"),
    ],
    ("bath", "FLAT"): [   # methods/bath/FLAT.md v41.0 (owner Review-42 engine = 31 Jul, 2/5 +£0.88; 2 cards only)
        ("top_rpr", 1.08, "top recent RPR: Bath A/E 1.21, +5% at SP (1,127; 1.24 / 1.19)"),
        ("lone_leader", 1.06, "lone front-runner: Bath A/E 1.16 (347; 1.26 / 1.08)"),
        ("cd_winner", 0.95, "course & distance winner is OVER-bet at Bath: A/E 0.90, -32% (1,371; 0.85 / 0.93)"),
        ("unproven_trip", 0.95, "never run within 1f of the trip: Bath A/E 0.90 (722; 0.89 / 0.91)"),
        ("jockey_low", 0.92, "jockey under 6% strike rate: Bath A/E 0.82 (895; 0.86 / 0.79)"),
    ],
    ("cork", "FLAT"): [   # methods/cork/FLAT.md v1.4 (owner v1.0/v1.1 peak, 3/4; 2 cards only)
        ("unproven_trip", 0.93, "never run within 1f of the trip: Cork A/E 0.77, -61% (615; 0.93 / 0.69)"),
    ],
    ("sedgefield", "JUMPS"): [   # methods/sedgefield/JUMPS.md v15.2 (1 owner card 28 Aug, 2/7; data-tested)
        ("top_rpr", 1.02, "top recent RPR: Sedgefield A/E 1.03 (833; 1.09 / 0.99) - national 1.05 trimmed"),
        ("improver", 1.05, "improver (last RPR a new best): Sedgefield A/E 1.12 (681; 1.19 / 1.07)"),
        ("held_up", 1.04, "usually held up: Sedgefield A/E 1.09, +2% at SP (1,881; 1.13 / 1.06)"),
        ("weak_finish", 0.96, "weakened / no extra in either of last 2: Sedgefield A/E 0.93 (2,416; 0.95 / 0.92)"),
    ],
    ("sligo", "JUMPS"): [   # methods/sligo/JUMPS.md v1.0 (data-built, provisional - no owner method)
        ("top_rpr", 1.00, "top recent RPR is NOT an edge at Sligo jumps: A/E 0.92 (304; 0.81 / 0.98) - national boost off"),
        ("cd_winner", 1.04, "course & distance winner: Sligo A/E 1.09 (119; 1.22 / 1.05)"),
    ],
    ("nottingham", "FLAT"): [   # methods/nottingham/FLAT.md v19.0 (owner v18.0-v18.2 peak, 30 Jul + 11 Aug: 7/13)
        ("older_noform", 1.06, "age 6+ out of form is UNDER-rated at Nottingham: A/E 1.19, +10% (712; 1.11 / 1.24)"),
        ("exact_rpr", 1.03, "top exact-conditions RPR (owner HR12): Nottingham A/E 1.11, -2% (841; 1.04 / 1.15) - provisional"),
    ],
    ("salisbury", "FLAT"): [   # methods/salisbury/FLAT.md v7.0 (owner v1.0 peak, 3 May: 3/6)
        ("lone_leader", 1.08, "lone front-runner (owner v1.0 pace dominance): Salisbury A/E 1.23 (204; 1.38 / 1.14)"),
        ("older_noform", 1.08, "age 6+ out of form is UNDER-rated at Salisbury: A/E 1.35, +105% (359; 1.49 / 1.29)"),
    ],
    ("southwell", "JUMPS"): [   # methods/southwell/JUMPS.md v14.0 (owner v11.1-v12.0, 11 May + 2 Jun: 5/14 +£6.37)
        ("exact_rpr", 1.06, "top exact-conditions RPR (owner's mandate, 4/7 on 2 Jun): Southwell jumps A/E 1.13, +0% (830; 1.17 / 1.11)"),
        ("improver", 1.04, "improver (last RPR a new best): Southwell jumps A/E 1.08 (817; 1.08 / 1.08)"),
        ("light", 0.97, "lightly raced (5 or fewer runs): Southwell jumps A/E 0.95 (2,483; 0.95 / 0.95)"),
    ],
    ("clonmel", "JUMPS"): [   # methods/clonmel/JUMPS.md v1.0 DATA-BUILT (no owner method)
        ("improver", 1.07, "improver (last RPR a new best): Clonmel A/E 1.15 (739; 1.23 / 1.10)"),
        ("ground_spec", 1.05, "won on today's exact going, 1-2 in field: Clonmel A/E 1.10 (261; 1.05 / 1.13)"),
        ("older_noform", 1.04, "age 6+ out of form is under-rated at Clonmel: A/E 1.08 (3,020; 1.08 / 1.08)"),
        ("lone_leader", 1.03, "lone front-runner: Clonmel A/E 1.07 (192; 1.07 / 1.07)"),
    ],
    ("bellewstown", "FLAT"): [   # methods/bellewstown/FLAT.md v1.2 (method only, no scored cards - data-tested)
        ("ground_spec", 1.06, "won on today's exact going, 1-2 in field: Bellewstown A/E 1.22 (90; 1.18 / 1.24)"),
        ("older", 1.06, "age 6+ is under-rated at Bellewstown: A/E 1.29 (700; 1.17 / 1.34)"),
    ],
    ("catterick", "FLAT"): [   # methods/catterick/FLAT.md v2.2 (owner v1.4 peak card +£2.97)
        ("top_rpr", 1.06, "top recent RPR: Catterick A/E 1.14 (949; 1.06 / 1.19)"),
        ("lone_leader", 1.06, "lone front-runner: Catterick A/E 1.18 (287; 1.32 / 1.06)"),
        ("ground_spec", 1.04, "won on today's exact going, 1-2 in field: Catterick A/E 1.09 (404; 1.09 / 1.09)"),
        ("slow_start:8.5", 0.90, "slow away 2+ of last 4, up to 1m: Catterick A/E 0.72, -52% (391; 0.59 / 0.80)"),
        ("slow_start:6.5", 0.95, "slow starter at 5-6f: Catterick A/E 0.81 (204; 0.90 / 0.75)"),
    ],
    ("kempton", "AW_FLAT"): [   # methods/kempton/AW_FLAT.md v21.1 (owner v20.3-v20.9 peak)
        ("improver", 1.05, "improver (last RPR a new best): Kempton A/E 1.10 (3,581; 1.11 / 1.09)"),
        ("top_rpr", 1.04, "top recent RPR: Kempton A/E 1.05 (3,802; 1.05 / 1.05)"),
        ("older", 0.95, "age 6+: Kempton A/E 0.90 (5,080; 0.90 / 0.90)"),
    ],
    ("fakenham", "JUMPS"): [   # methods/fakenham/JUMPS.md v1.0 DATA-BUILT 15 Oct (no owner method)
        ("top_rpr", 1.04, "top recent RPR: Fakenham A/E 1.10 (507; since 2022 1.05)"),
        ("exact_rpr", 1.04, "top exact-conditions RPR: Fakenham A/E 1.11 (435; since 2022 1.11)"),
        ("older_noform", 0.96, "age 6+ with no win/2nd in last 3: Fakenham A/E 0.89 (1,037; since 2022 0.90)"),
        ("weak_finish", 0.97, "weakened / no extra in either of last 2: Fakenham A/E 0.90 (1,265; since 2022 0.95)"),
    ],
    ("ascot", "FLAT"): [   # methods/ascot/FLAT.md v1.2 DATA-BUILT (no owner method; v1.0 2 Oct review, v1.1 3 Oct owner reviews, v1.2 15 Oct Champions Day study)
        ("top_rpr", 1.06, "top recent RPR: Ascot A/E 1.11 (986; 1.15 / 1.09)"),
        ("slow_start:8.5", 1.05, "slow away 2+ of last 4, up to 1m, is UNDER-rated at Ascot: A/E 1.27, +5% (513; 1.24 / 1.28) - provisional"),
        # 15 Oct (Champions Day study, reports/research/2026-10-15_champions_day_research.md): A/E against OUR MODEL, races it had
        # not seen (fit < 2023; 2023-24 | 2025-26), all UK/IRE Group races - TRIAL at Ascot only
        ("leader_group:9.5-12.5", 1.12, "usual front-runner in a Group race at 1m2f-1m4f: beats our model, A/E 1.26 / 1.22 (154; market "
                                        "A/E at Ascot 1.52 / 1.84) - trial"),
        ("age4_autumn_group", 0.88, "4-year-old in a Group race in September-October: A/E 0.83 / 0.63 against our model (294; G1s at "
                                    "SP 0.65 / 0.76) - trial"),
        ("midfield_group:0-7.5", 0.85, "usually races midfield in a Group race at 5-7f: A/E 0.64 / 0.43 against our model (206) - trial"),
        # 15 Oct evening, v1.3 (owner: "is all this extra research going to go into every prediction"): round-2 findings that held
        # BOTH against the price (2015-20 / 2021-26, a11/a12) AND against our model on races it never saw (fit < 2023; 2023-24 /
        # 2025-26, reports/research/scripts/champions_day/a13_round2_v_model.py) - small samples, TRIAL at Ascot only
        ("draw3:low,5.5-6.5,14@GOOD|FAST", 1.10, "low draw, 14+ runner Ascot 6f on good or firmer (far side): beats our model A/E 1.53 / "
                                                  "1.80 (10 winners); v price 1.21 / 1.56 - trial"),
        ("draw3:high,5.5-6.5,14@GOOD|FAST", 0.93, "high draw, 14+ runner Ascot 6f on good or firmer: A/E 0.67 / 0.80 against our model; "
                                                   "v price 0.81 / 0.88 - trial"),
        ("draw3:high,11.5-12.5,8,front", 1.08, "high draw and usually races prominently / leads, Ascot 1m4f: A/E 1.15 / 1.47 against our "
                                               "model; v price 1.34 / 1.53 - trial"),
        ("draw3:low,11.5-12.5,8@GOOD|FAST", 0.92, "low draw at Ascot 1m4f on good or firmer: A/E 0.74 / 0.71 against our model; v price "
                                                  "0.73 / 0.70 - trial"),
        ("draw3:low,7.5-8.5,16,back", 1.06, "low draw and usually held up / midfield, Ascot straight mile 16+: A/E 2.13 / 1.42 against "
                                            "our model (small); v price 1.35 / 1.31 - trial"),
        ("draw3:mid,7.5-8.5,16,back", 1.06, "middle draw and usually held up / midfield, Ascot straight mile 16+: A/E 1.44 / 2.26 against "
                                            "our model (small); v price 1.33 / 1.92 - trial"),
        ("aob_outsider", 0.85, "Aidan O'Brien runner 5th or bigger in the betting in a Group 1: 1 winner from 86 in 2023-26 Group 1s (A/E "
                               "0.62 / 0.00 against our model); at Ascot 1 winner from 113 since 2015 - trial"),
    ],
    ("kelso", "JUMPS"): [   # methods/kelso/JUMPS.md v36.0 (owner v35 peak card 24 May +£0.25; data-tested 3 Oct)
        ("cd_winner", 1.10, "course & distance winner: Kelso A/E 1.26, +8% at SP (535; 1.35 / 1.22)"),
        ("improver", 1.08, "improver (last RPR a new best): Kelso A/E 1.20 (778; 1.28 / 1.15)"),
        ("leader", 0.94, "usual front-runner: Kelso A/E 0.86 (573; 0.75 / 0.93)"),
        # v36.1 (24 Oct review): soft-type going only - Kelso soft 0.88 (1,265; 0.90 / 0.87) v good/firmer 1.03 (870; 1.07 / 1.01)
        ("weak_finish@SOFT", 0.97, "weakened / no extra in either of last 2, on soft-type ground: Kelso A/E 0.88 (1,265; 0.90 / 0.87)"),
    ],
    ("uttoxeter", "JUMPS"): [   # methods/uttoxeter/JUMPS.md v17.0 (owner peak 13 Jun +£2.00; 11 hard gates tested 3 Oct)
        ("jockey_low", 0.93, "jockey under 6% strike rate: Uttoxeter A/E 0.87, -41% (1,099; 0.86 / 0.88)"),
        ("weak_finish", 0.97, "weakened / no extra in either of last 2: Uttoxeter A/E 0.94 (3,990; 0.94 / 0.94)"),
        ("improver", 1.04, "improver (last RPR a new best): Uttoxeter A/E 1.11 (1,290; 1.25 / 1.03)"),
        ("top_rpr", 1.03, "top recent RPR: Uttoxeter A/E 1.06 (1,215; 1.12 / 1.02) - national 1.05 trimmed"),
        ("leader", 1.04, "usual front-runner: Uttoxeter A/E 1.13 (840; 1.00 / 1.21) - added 4 Oct v17.1, provisional"),
        ("unproven_trip", 1.03, "first time at the trip is UNDER-bet here: Uttoxeter A/E 1.10 (1,506; ~1.10 / 1.10) - owner gate reversed, v17.2 29 Oct"),
    ],
    ("killarney", "JUMPS"): [   # methods/killarney/JUMPS.md v1.0 DATA-BUILT (owner has no Killarney method)
        ("exact_rpr", 1.12, "top exact-conditions RPR: Killarney A/E 1.39, +6% at SP (319; 1.26 / 1.48)"),
        ("top_rpr", 1.07, "top recent RPR: Killarney A/E 1.15 (378; 1.08 / 1.19)"),
        ("cd_winner", 1.07, "course & distance winner: Killarney A/E 1.23 (165; 1.15 / 1.27)"),
        ("leader", 1.06, "usual front-runner: Killarney A/E 1.25 (236; 1.09 / 1.35)"),
        ("unproven_trip", 0.88, "never run within 1f of the trip: Killarney A/E 0.80, -58% (503; 0.74 / 0.84)"),
        ("weak_finish", 0.92, "weakened / no extra in either of last 2: Killarney A/E 0.85 (1,222; 0.74 / 0.88)"),
        ("older_noform", 0.93, "age 6+ with no win/2nd in last 3: Killarney A/E 0.88, -50% (1,407; 0.90 / 0.87)"),
        ("won_last", 0.96, "won last time is over-bet at Killarney: A/E 0.92 (310; 0.87 / 0.95)"),
    ],
    ("pontefract", "FLAT"): [   # methods/pontefract/FLAT.md v19.0 (owner peak 29 Apr 4/7 +£2.96; 16 Aug v18.2 3/7; data-tested 5 Oct)
        ("won_last", 0.92, "won last time is over-bet at Pontefract: A/E 0.83, -34% (618; 0.89 / 0.80)"),
        ("held_up_short", 0.94, "held-up type up to 7.5f, <2 leaders: Pontefract A/E 0.84 (585; 0.66 / 0.95)"),
        ("exact_rpr", 1.03, "top exact-conditions RPR: Pontefract A/E 1.06 (711; 1.04 / 1.07)"),
        ("improver", 0.97, "improver is over-bet at Pontefract: A/E 0.94 (651; 0.99 / 0.91)"),
    ],
    ("yarmouth", "FLAT"): [   # methods/yarmouth/FLAT.md v2.0 (owner best card 17 Sep 2/7, RPR 3/7; all 7 cards losing; data-tested 5 Oct)
        ("leader", 0.90, "usual front-runner: Yarmouth A/E 0.83, -40% (581; 0.80 / 0.85)"),
        ("lone_leader", 0.90, "lone front-runner: Yarmouth A/E 0.80, -50% (356; 0.75 / 0.83)"),
        ("held_up", 1.03, "usually held up: Yarmouth A/E 1.05 (3,185; 1.04 / 1.06)"),
        ("cd_winner", 0.93, "course-and-distance winner is over-bet at Yarmouth: A/E 0.87 (1,033; 0.83 / 0.89)"),
        ("ground_spec", 0.90, "won on today's going, 1-2 in field have: Yarmouth A/E 0.76, -35% (578; 0.78 / 0.75)"),
        ("improver", 1.04, "improver: Yarmouth A/E 1.07 (1,145; 1.07 / 1.07)"),
        ("exact_rpr", 0.97, "top exact-conditions RPR is over-bet at Yarmouth: A/E 0.93 (1,031; 0.90 / 0.95)"),
    ],
    ("navan", "FLAT"): [   # methods/navan/FLAT.md v10.0 (owner AURORA-X v9.5 22 Oct 2025 1/7 = best of 2 cards; data-tested 6 Oct)
        ("won_last", 0.90, "won last time is over-bet at Navan: A/E 0.74 (399; 0.65 / 0.79) - owner's 'Horse In Form' reversed"),
        ("unproven_trip", 0.92, "never run within 1f of this trip (owner's Gate A): Navan A/E 0.83 (942; 0.76 / 0.87)"),
        ("held_up_short", 0.88, "held-up type, up to 7.5f, <2 leaders: Navan A/E 0.73 (537; 0.81 / 0.67)"),
        ("improver", 0.94, "improver is over-bet at Navan: A/E 0.86 (668; 0.86 / 0.86)"),
        ("cd_winner", 0.96, "course & distance winner over-bet: A/E 0.93 (465; 0.93 / 0.93)"),
        ("leader@SOFT", 1.06, "usual front-runner on yielding or softer: Navan A/E 1.34 (151; 1.72 / 1.15); good/firm 0.99 flips (1.42 / 0.81) - no boost there (v10.1, 21 Oct)"),
        ("older_noform", 1.08, "age 6+ out of form is UNDER-bet: A/E 1.41 (831; 1.91 / 1.21) - owner's 6yo+ gate reversed"),
        ("top_rpr", 1.00, "top recent RPR barely beats the market here: A/E 1.03 (545; 0.97 / 1.06) - national boost off"),
    ],
    ("windsor", "JUMPS"): [],   # methods/windsor/JUMPS.md v1.0 (14 Nov; Windsor's first jumps meeting since our registry
                                # listed it FLAT only; 49 jumps races 2019-26 = too few for course rules -> national defaults only)
    ("thurles", "FLAT"): [   # methods/thurles/FLAT.md v1.0 DATA-BUILT (owner has no Thurles method, 7 Oct; only 59 races - provisional)
        ("older", 1.05, "age 6+ is under-bet at Thurles flat: A/E 1.33, -1% at SP (138; 1.43 / 1.25) - small sample"),
        ("improver", 1.03, "improver: Thurles flat A/E 1.16 (60; 1.23 / 1.10) - small sample"),
    ],
    ("thurles", "JUMPS"): [   # methods/thurles/JUMPS.md v1.0 DATA-BUILT (11 Nov; owner has no Thurles jumps method; 496 races 2019-26)
        ("cd_winner", 0.94, "course & distance winner over-bet at Thurles jumps: A/E 0.67, -42% (229; 2019-21 ~0.50 / 2022-26 0.76)"),
        ("unproven_trip", 1.02, "never run within 1f of the trip is slightly UNDER-bet: A/E 1.06 (915; ~1.06 / 1.06)"),
        ("top_rpr", 1.00, "top recent RPR: A/E 1.13 overall but 1.01 since 2022 (532; ~1.30 / 1.01) - national boost off"),
    ],
    ("navan", "JUMPS"): [   # methods/navan/JUMPS.md v1.1 DATA-BUILT (13 Nov, v1.1 14 Nov front-runner boosts @SOFT only; owner has a Navan FLAT method only)
        ("top_rpr", 1.06, "top recent RPR: Navan A/E 1.18 (538; 1.14 / 1.21)"),
        ("leader@SOFT", 1.04, "usual front-runner on yielding or softer: Navan jumps A/E 1.19 (344; 1.23 / 1.16); good/good to yielding 0.78 (56) - no boost there (v1.1, 14 Nov review)"),
        ("won_last", 1.03, "won last time: Navan A/E 1.12 (540; 1.08 / 1.15)"),
        ("lone_leader@SOFT", 1.03, "lone front-runner on yielding or softer: Navan jumps A/E 1.30 (151; 1.43 / 1.21); good 0.82 (40) - small sample, provisional (v1.1)"),
        ("improver", 1.02, "improver: Navan A/E 1.07 (824; 1.04 / 1.10)"),
        ("weak_finish", 0.96, "weakened in either of last 2 runs: Navan A/E 0.88, -46% (1,776; 0.71 / 0.96)"),
    ],
    ("tramore", "JUMPS"): [   # methods/tramore/JUMPS.md v1.0 DATA-BUILT (owner has no Tramore method, 7 Oct)
        ("leader", 1.05, "usual front-runner: Tramore A/E 1.13 (286; 1.16 / 1.11)"),
        ("improver", 1.04, "improver: Tramore A/E 1.10 (681; 1.14 / 1.07)"),
        ("exact_rpr", 1.03, "top exact-conditions RPR: Tramore A/E 1.07 (499; 1.01 / 1.11) - provisional"),
        ("older_noform", 0.96, "age 6+ with no win/2nd in last 3: Tramore A/E 0.93, -38% (2,488; 0.93 / 0.93)"),
        ("jockey_low", 0.97, "jockey under 6% strike rate: Tramore A/E 0.95, -42% (1,503; 0.96 / 0.94)"),
    ],
    ("york", "FLAT"): [   # methods/york/FLAT.md v41.0 (owner v35-v40 + Ebor series v1.4-v1.7, 8 cards verified 19/55 +£3.33; data-tested 8 Oct)
        ("top_rpr", 1.08, "top recent RPR: York A/E 1.19 (1,080; 1.17 / 1.20) - the strongest York rule"),
        ("draw_low", 1.03, "drawn 1-4 on good or firmer: York A/E 1.08 (2,635; 1.06 / 1.09)"),
        ("older_noform", 0.88, "age 6+ with no win/2nd in last 3: York A/E 0.74, -49% (1,073; 0.78 / 0.72) - owner's HR5 kept"),
        ("older", 0.96, "age 6+ at York: A/E 0.89, -41% (2,333; 0.87 / 0.90)"),
        ("jockey_low", 0.90, "jockey under 6% strike rate: York A/E 0.73, -60% (784; 0.55 / 0.86) - owner's HR4 kept"),
    ],
    ("goodwood", "FLAT"): [   # methods/goodwood/FLAT.md v1.0 (owner v39.3-v40.3 + Gemini v22.x; peak 28 Aug v40.0 3/5 +£10.96 verified; data-tested 11 Oct)
        ("exact_rpr", 1.05, "top exact-conditions RPR: Goodwood A/E 1.13 (856; since 2022 1.11)"),
        ("top_rpr", 1.00, "top recent RPR only A/E 1.00 at Goodwood (1,044) - national boost switched off"),
        ("cd_winner", 1.02, "course & distance winner: Goodwood A/E 1.07 (734; since 2022 1.04)"),
        ("unproven_trip", 1.03, "first time at the trip: Goodwood A/E 1.07 (743; since 2022 1.13) - owner's HR1 trip gate REVERSED"),
        ("bend_7f", 0.90, "drawn 7+ over 7f (owner's Bend Control Law): Goodwood A/E 0.76, -45% (638; since 2022 0.62)"),
        ("slow_start:0-8", 0.96, "slow away 2+ of last 4, up to 1m: Goodwood A/E 0.87 (312; since 2022 0.93) - owner's start risk kept"),
        ("lone_leader", 0.96, "lone front-runner: Goodwood A/E 0.87 (286; since 2022 0.90)"),
    ],
    ("cork", "JUMPS"): [   # methods/cork/JUMPS.md v1.0 DATA-BUILT 11 Oct (owner's Cork Jumps upload was empty); full 2019+ / since 2022
        ("top_rpr", 1.05, "top recent RPR: Cork jumps A/E 1.11 (598; since 2022 1.08)"),
        ("improver", 1.05, "last RPR above its previous best: Cork jumps A/E 1.12 (792; since 2022 1.13)"),
        ("won_last", 1.03, "won last time: Cork jumps A/E 1.07 (443; since 2022 1.15)"),
        ("cd_winner", 0.90, "course & distance winner is OVER-bet at Cork jumps: A/E 0.65, -61% (178; since 2022 0.62)"),
        ("jockey_low", 0.93, "jockey under 6% strike rate: Cork jumps A/E 0.83 (2,013; since 2022 0.79)"),
        ("older_noform", 0.95, "age 6+ with no win/2nd in last 3: Cork jumps A/E 0.91 (2,395; since 2022 0.85)"),
        ("unproven_trip", 0.97, "never run within 1f of the trip: Cork jumps A/E 0.92 (1,272; since 2022 0.94)"),
    ],
    ("leopardstown", "FLAT"): [   # methods/leopardstown/FLAT.md v19.0 (owner AURORA-X v18.x + reviews; cards 12 Apr 0/7, 9 Jul 1/7, 12 Sep 2/9 verified; data-tested 16 Oct, full 2019+ / since 2022)
        ("lone_leader", 1.05, "lone front-runner: Leopardstown A/E 1.19 (269; since 2022 1.28, +30%) - owner's 'Low + Lead' pace bias kept"),
        ("leader", 1.04, "usual front-runner: Leopardstown A/E 1.18 (527; since 2022 1.18)"),
        ("top_rpr", 1.04, "top recent RPR: Leopardstown A/E 1.09 (954; since 2022 1.05)"),
        ("improver", 1.04, "last RPR above its previous best: Leopardstown A/E 1.12 (1,272; since 2022 1.13)"),
        ("draw_low", 1.02, "drawn 1-4 on good or firmer: Leopardstown A/E 1.05 (2,043; since 2022 1.04)"),
        ("held_up", 0.96, "usually held up: Leopardstown A/E 0.91 (2,541; since 2022 0.87)"),
        ("older_noform", 0.93, "age 6+ with no win/2nd in last 3: Leopardstown A/E 0.76, -53% (990; since 2022 0.79)"),
        ("ground_spec", 0.95, "won on today's exact going, only 1-2 in the field have: Leopardstown A/E 0.90 (305; since 2022 0.75)"),
        ("cd_winner", 0.97, "course & distance winner over-bet here: Leopardstown A/E 0.86 (851; since 2022 0.94)"),
    ],
    ("beverley", "FLAT"): [   # methods/beverley/FLAT.md ZANS v3.0 (29 Oct 2026; owner AURORA-X v1.7-v2.0 onboarded; Beverley flat 2019-26, A/E 2019-21 / 2022-26)
        ("top_rpr", 1.06, "top recent RPR (best of last 3): Beverley A/E 1.10 (1,093; 1.14 / 1.08)"),
        ("lone_leader", 1.04, "lone front-runner (owner's pace hierarchy): Beverley A/E 1.08 (331; 1.12 / 1.06)"),
        ("leader", 1.03, "usual front-runner: Beverley A/E 1.06 (645; 1.08 / 1.05)"),
        ("held_up_short", 0.95, "held-up type up to 7.5f, <2 leaders (uphill run-in suits the prominent): A/E 0.93 (1,039; 0.93 / 0.93)"),
        ("held_up:6.5-7.5", 0.96, "usually held up over 7f96y: Beverley A/E 0.84 (629; 0.81 / 0.85)"),
        ("bend_7f", 1.05, "drawn 7+ over 7f96y: Beverley A/E 1.18 (831; 1.15 / 1.20) - owner's low-draw premium is priced in"),
        ("draw3:low,0-5.5,6@GOOD|FAST", 0.96, "low third over 5f on good or firmer: over-bet, A/E 0.88 (618; 0.90 / 0.87)"),
        ("draw3:high,0-8.5,6@SOFT", 1.04, "high third up to 1m on good to soft or softer (owner's HR9 inversion): A/E 1.14 (712; 1.08 / 1.16)"),
        ("draw3:low,0-8.5,6@SOFT", 0.96, "low third up to 1m on good to soft or softer: A/E 0.87 (482; 0.77 / 0.92)"),
        ("improver", 1.03, "improver (last RPR a career best): Beverley A/E 1.06 (760; 1.12 / 1.03)"),
        ("layoff:60-999", 0.96, "60+ days off (owner's HR8): Beverley A/E 0.91 (1,050; 0.88 / 0.92)"),
    ],
    ("carlisle", "FLAT"): [   # methods/carlisle/FLAT.md ZANS v7.0 (29 Oct 2026; owner AURORA-X v6.6-v6.9 onboarded; Carlisle flat 2019-26, A/E 2019-21 / 2022-26)
        ("held_up:5.5-6.5", 1.05, "usually held up over 6f: Carlisle A/E 1.16 (418; 1.18 / 1.15) - owner's HR16 low-draw hold-up trap reversed (1.32, 114)"),
        ("slow_start:6.5", 1.05, "slow starter at 5-6f: Carlisle A/E 1.52 (154; 1.89 / 1.37) - start-risk gate reversed"),
        ("improver", 1.04, "improver (last RPR a career best): Carlisle A/E 1.12 (551; 1.20 / 1.08)"),
        ("cd_winner", 1.03, "course & distance winner: Carlisle A/E 1.07 (524; 1.12 / 1.05)"),
        ("draw3:low,0-5.5,6", 1.04, "low third over 5f: Carlisle A/E 1.22 good/firm (97), 1.32 soft (72), up in both periods - small sample"),
        ("bend_7f", 1.03, "drawn 7+ over 6f195y: Carlisle A/E 1.10 (347; 1.10 / 1.10)"),
        ("older", 0.95, "age 6+ (owner's HR4): Carlisle A/E 0.86 (1,172; 0.68 / 0.93)"),
        ("jockey_low", 0.95, "jockey strike rate under 6% (owner's HR3): Carlisle A/E 0.84 (585; 0.76 / 0.88)"),
        ("exact_rpr", 0.97, "top exact-conditions RPR is over-bet here: A/E 0.92 (599; 0.83 / 0.96) - owner's HR11 mandate dropped"),
        ("layoff:46-99", 0.97, "46-99 days off (owner's HR8): Carlisle A/E 0.86 (390; 0.56 / 0.97)"),
        ("course_win_not_cd", 0.96, "course winner at another trip: Carlisle A/E 0.61 (77; 0.94 / 0.45) - small sample"),
    ],
    ("lingfield", "AW_FLAT"): [   # methods/lingfield/AW_FLAT.md ZANS v30.0 (29 Oct 2026; owner AURORA-X v25.0-v29.0, 9 cards verified 18/56 -£1.64, peak v26.1-v28.0 11-27 Aug 13/34 +£9.02; Lingfield AW 2019-26, A/E 2019-21 / 2022-26)
        ("top_rpr", 1.04, "top recent RPR: Lingfield AW A/E 1.09 (3,539; 1.07 / 1.10)"),
        ("leader:0-6.5", 1.05, "usual front-runner over 5-6f (owner's Gdl L): Lingfield AW A/E 1.12 (719; 1.12 / 1.12)"),
        ("prominent:6.5-8.5", 1.03, "usually prominent over 7f-1m (owner's Gdl L): Lingfield AW A/E 1.07 (4,706; 1.12 / 1.04)"),
        ("draw3:mid,9.5-10.5,6", 1.04, "middle draw over 1m2f (owner's stalls 5-7): Lingfield AW A/E 1.08 (1,406; 1.12 / 1.06)"),
        ("draw3:high,9.5-10.5,10", 0.95, "high draw over 1m2f in 10+ runners: Lingfield AW A/E 0.87 (1,053; 0.85 / 0.89)"),
        ("draw3:low,4.5-5.5,6", 0.95, "low draw over 5f is OVER-bet at Lingfield AW: A/E 0.87 (638; 0.88 / 0.86) - owner's Golden Highway reversed"),
        ("draw3:low,6.5-8.5,6", 0.95, "low draw over 7f-1m is OVER-bet at Lingfield AW: A/E 0.90 (3,018; 0.95 / 0.86) - owner's stalls 1-4 law reversed"),
        ("won_last", 1.02, "won last time: Lingfield AW A/E 1.06 (2,572; 1.09 / 1.04)"),
        ("improver", 1.02, "last RPR above its previous best: Lingfield AW A/E 1.05 (2,841; 1.08 / 1.03)"),
        ("layoff:91-999", 1.03, "91+ days off is UNDER-bet at Lingfield AW: A/E 1.08 (2,979; 1.12 / 1.05) - owner's layoff penalty reversed"),
        ("slow_start:0-8.5", 0.94, "slow away 2+ of last 4, up to 1m (owner's Gdl J): Lingfield AW A/E 0.83 (1,254; 0.91 / 0.78)"),
        ("jockey_low", 0.93, "jockey under 6% strike rate: Lingfield AW A/E 0.86 (1,915; 0.82 / 0.89)"),
        ("weak_finish", 0.97, "weakened / no extra in either of last 2 (owner's stamina red flag): Lingfield AW A/E 0.95 (10,414; 0.91 / 0.97)"),
        ("unproven_trip", 0.97, "never run within 1f of the trip (owner's HR1, caution only): Lingfield AW A/E 0.94 (2,076; 0.90 / 0.97)"),
    ],
    ("lingfield", "FLAT"): [   # methods/lingfield/FLAT.md ZANS v21.0 (29 Oct 2026; owner AURORA-X v19.0-v20.2, 3 cards verified 10/16 +£4.90, peak 1 Aug v20.0 5/7; Lingfield turf 2019-26 (590 races), A/E 2019-21 / 2022-26) - provisional
        ("top_rpr", 1.06, "top recent RPR: Lingfield turf A/E 1.16 (682; 1.13 / 1.18)"),
        ("exact_rpr", 1.02, "top exact-conditions RPR (owner's RPR anchor): Lingfield turf A/E 1.04 (533; 1.04 / 1.04)"),
        ("draw3:high,4.5-7.9,10", 1.04, "high draw on the straight 5-7f, 10+ runners (owner's stands-rail law): Lingfield turf A/E 1.14 (551; 1.11 / 1.18)"),
        ("draw3:low,4.5-7.9,10", 0.95, "low draw on the straight 5-7f, 10+ runners: Lingfield turf A/E 0.84 (332; 0.96 / 0.72)"),
        ("draw3:low,7.9-10.5,6", 1.04, "low draw over 1m-1m2f: Lingfield turf A/E 1.52 (168; 1.52 / 1.51) - small sample, provisional"),
        ("draw3:mid,7.9-10.5,6", 0.95, "middle draw over 1m-1m2f: Lingfield turf A/E 0.75 (182; 0.80 / 0.73) - owner's stalls 5-7 law reversed, provisional"),
        ("layoff:91-999", 0.94, "91+ days off: Lingfield turf A/E 0.77 (461; 0.68 / 0.85)"),
        ("won_last", 0.96, "won last time is OVER-bet at Lingfield turf: A/E 0.91 (399; 0.86 / 0.94)"),
    ],
    ("cartmel", "JUMPS"): [   # methods/cartmel/JUMPS.md v16.0 (owner AURORA-X v15.1; 1 card 29 Aug 2026 4/5 +£9.33 verified; data-tested 29 Oct)
        ("lone_leader", 1.05, "lone front-runner: Cartmel jumps A/E 1.27 (128; 1.55 / 1.16) - owner's position-early law (HR14) kept"),
        ("cd_winner", 1.03, "course & distance winner: Cartmel A/E 1.11 (511; 1.17 / 1.10) - owner's course-specialist DNA kept"),
        ("top_rpr", 1.03, "top recent RPR: Cartmel A/E 1.10 (456; 1.02 / 1.14) - national boost trimmed"),
        ("won_last", 1.02, "won last time: Cartmel A/E 1.05 (497; 1.09 / 1.04)"),
        ("jockey_name:mclernon", 1.05, "owner's Haslam/McLernon value pair - Richie McLernon riding: Cartmel A/E 1.56 (127; 2.24 / 1.44)"),
        ("jockey_name:charlotte jones", 1.04, "owner's Moffatt/Jones local axis - Charlotte Jones riding: Cartmel A/E 1.34 (172; 1.83 / 1.17)"),
        ("jockey_name:brian hughes", 0.97, "owner: Hughes is NOT a Cartmel target - Cartmel A/E 0.85 (220; 0.96 / 0.77)"),
        ("unproven_trip", 0.95, "never run within 1f of the trip (owner's Gate A): Cartmel A/E 0.89 (495; 0.89 / 0.89)"),
        ("hung", 0.93, "hung in either of last 2 (owner's wide-trip tax; tested as keen-or-hung): Cartmel A/E 0.82 (583; 0.82 / 0.82)"),
        ("unreliable", 0.88, "owner's Gate J - 2+ pulled up / unseated / fell in last 3: Cartmel A/E 0.57 (192; 0.28 / 0.69)"),
        ("layoff:120-9999", 0.94, "owner's LAYOFF TRAP - back from 120+ days: Cartmel A/E 0.73 (351; 0.70 / 0.77)"),
    ],
    ("chepstow", "FLAT"): [   # methods/chepstow/FLAT.md v5.0 (owner AURORA-X v4.6; 3 cards verified 4/17 +£6.65, peak 31 Aug v4.5 2/8 +£11.00; data-tested 29 Oct)
        ("top_rpr", 1.00, "top recent RPR: Chepstow flat A/E 1.02 (848; 1.13 / 0.96) - national boost switched off"),
        ("draw3:high,0-5.5,6@GOOD|FAST", 1.04, "high third over 5f on good or firmer (owner's 5f draw DNA): Chepstow A/E 1.19 (260; 1.05 / 1.27)"),
        ("draw3:low,0-5.5,6@GOOD|FAST", 0.95, "low third over 5f on good or firmer: Chepstow A/E 0.80 (180; 0.72 / 0.84)"),
        ("draw3:high,0-5.5,6,front@SOFT", 0.95, "owner's Fusion cap on soft ground - high draw + front-runner over 5f on soft: A/E 0.64 (80; 0.59 / 0.66)"),
        ("draw3:low,5.6-6.5,6", 1.03, "low third over 6f: Chepstow A/E 1.13 (358; 1.09 / 1.15) - owner's 'middle-high best' at 6f REVERSED"),
        ("improver", 1.03, "last RPR above its previous best (owner's Improver engine): Chepstow A/E 1.06 (596; 1.06 / 1.06)"),
        ("cd_winner", 1.02, "course & distance winner: Chepstow A/E 1.06 (995; 1.04 / 1.06)"),
        ("slow_start:0-8", 1.04, "slow away 2+ of last 4, up to 1m: Chepstow A/E 1.16 (433; 1.11 / 1.19) - owner's HR4 start-risk REVERSED"),
        ("jockey_name:gina mangan", 1.03, "owner's specialist jockey list - Gina Mangan riding: Chepstow A/E 1.45 (190; 1.31 / 1.48)"),
        ("unproven_trip", 0.95, "never run within 1f of the trip: Chepstow A/E 0.89 (333; 0.89 / 0.89)"),
        ("weak_finish", 0.96, "weakened / no extra in either of last 2 (owner's HR5 finishing): Chepstow A/E 0.91 (2,753; 0.91 / 0.91)"),
        ("leader", 0.96, "usual front-runner: Chepstow A/E 0.92 (506; 0.92 / 0.92)"),
        ("lone_leader", 0.96, "lone front-runner: Chepstow A/E 0.88 (247; 0.64 / 0.96)"),
    ],
    ("chester", "FLAT"): [   # methods/chester/FLAT.md v35.0 (owner AURORA-X v34.1-v34.7; 5 cards verified 8/32 -£12.54, peak 2 Aug v34.3 3/6; data-tested 29 Oct)
        ("exact_rpr", 1.06, "top exact-conditions RPR (owner's G9 RPR anchor): Chester A/E 1.15 (704; 1.19 / 1.13)"),
        ("lone_leader", 1.08, "lone front-runner (owner's G2 pace gate): Chester A/E 1.30 (281; 1.16 / 1.37)"),
        ("leader", 1.03, "habitual front-runner (not alone): Chester A/E 1.08 (564; 1.07 / 1.09)"),
        ("improver", 1.04, "last RPR above its previous best: Chester A/E 1.11 (964; 1.07 / 1.13)"),
        ("older", 1.03, "age 6+ is under-bet at Chester: A/E 1.09 (1,412; 1.05 / 1.11)"),
        ("draw3:low,0-6.5,6", 1.04, "low third over 5-6f (owner's DNA draw table, softened): Chester A/E 1.12 (482; 1.20 / 1.08)"),
        ("draw3:high,0-6.5,6", 0.96, "high third over 5-6f: Chester A/E 0.85 (666; 0.58 / 0.97)"),
        ("held_up", 0.97, "usually held up (owner's pace gate, caution not reject): Chester A/E 0.94 (1,689; 0.94 / 0.94)"),
        ("slow_start:0-8", 0.90, "slow away 2+ of last 4, up to 1m (owner's G4 start risk): Chester A/E 0.62, -38% (207; 0.66 / 0.60)"),
    ],
    ("fairyhouse", "FLAT"): [   # methods/fairyhouse/FLAT.md v15.0 (owner AURORA-X v14.0/v14.1; 1 card verified 1/5 +£1.50; data-tested 29 Oct, PROVISIONAL)
        ("exact_rpr", 1.08, "top exact-conditions RPR: Fairyhouse flat A/E 1.24 (312; 1.33 / 1.19)"),
        ("top_rpr", 1.00, "top recent RPR only matches the market here: A/E 1.00 (356; 0.98 / 1.01) - national boost off"),
        ("lone_leader", 1.08, "lone front-runner: Fairyhouse flat A/E 1.74 (93; 1.70 / 1.77)"),
        ("slow_start:0-8", 1.05, "slow away 2+ of last 4, up to 1m is UNDER-bet here: A/E 1.48 (160; 1.35 / 1.53) - owner's HR4 REVERSED"),
        ("jockey_name:coen", 1.04, "jockey Ben Coen (owner's Murtagh/Coen combo): Fairyhouse flat A/E 1.79 (41) / 1.52 (114) - provisional"),
        ("draw3:high,0-6.5,6", 1.03, "high third over 5-6f: Fairyhouse flat A/E 1.10 (616; 1.05 / 1.14)"),
        ("light", 1.02, "lightly raced (5 or fewer runs): A/E 1.06 (1,687; 1.07 / 1.05)"),
        ("weak_finish", 0.97, "weakened / no extra in either of last 2 (owner's HR3, caution only): A/E 0.92 (1,406; 0.83 / 0.96)"),
        ("cd_winner", 0.94, "course & distance winner is over-bet here: A/E 0.82 (175; 0.65 / 0.90)"),
        ("held_up", 0.94, "usually held up (owner's Position Race Mandate, caution): A/E 0.83 (1,078; 0.88 / 0.78)"),
    ],
    ("down_royal", "JUMPS"): [   # methods/down_royal/JUMPS.md v1.0 DATA-BUILT 29 Oct (owner has no Down Royal jumps method; 409 races 2019-26)
        ("top_rpr", 1.00, "top recent RPR: Down Royal jumps A/E 1.05 (429; ~1.24 2019-21 / 0.93 since 2022) - flips, national boost off"),
        ("ground_spec", 1.04, "won on today's exact going, only 1-2 in the field have: Down Royal jumps A/E 1.27 (240; ~1.43 / 1.12)"),
        ("unproven_trip", 0.95, "first time at the trip: Down Royal jumps A/E 0.89 (659; ~0.79 / 0.94)"),
        ("lone_leader", 0.96, "lone front-runner: Down Royal jumps A/E 0.87 (129; ~0.92 / 0.83) - small sample"),
    ],
    ("punchestown", "FLAT"): [   # methods/punchestown/FLAT.md v1.0 DATA-BUILT 28 Oct (owner has no Punchestown flat method; only 93 races 2019-26 - provisional)
        ("top_rpr", 1.00, "top recent RPR: Punchestown flat A/E 0.78 (91; ~1.28 2019-21 / 0.56 since 2022) - flips, national boost off"),
        ("jockey_low", 0.95, "jockey under 6% strike rate: Punchestown flat A/E 0.79 (296; ~0.70 / 0.83)"),
        ("older_noform", 0.95, "age 6+ with no win/2nd in last 3: Punchestown flat A/E 0.79 (94; ~0.86 / 0.73)"),
        ("draw_low", 0.96, "drawn 1-4 on good or firmer: Punchestown flat A/E 0.61 (84; ~0.86 / 0.51) - small sample"),
        ("exact_rpr", 0.97, "top exact-conditions RPR: Punchestown flat A/E 0.60 (61; ~0.50 / 0.63) - small sample"),
        ("prominent@SOFT", 1.03, "usually prominent on yielding or softer: Punchestown flat A/E 1.31 (153; 1.57 / 1.24) - provisional v1.1, 29 Oct review"),
    ],
    ("gowran_park", "FLAT"): [   # methods/gowran_park/FLAT.md v1.0 DATA-BUILT 18 Oct (owner has no Gowran flat method; 720 races 2019-26)
        ("draw_low", 1.05, "drawn 1-4 on good or firmer: Gowran Park flat A/E 1.15 (1,030; since 2022 1.14)"),
        ("top_rpr", 1.04, "top recent RPR: Gowran Park flat A/E 1.10 (782; since 2022 1.05)"),
        ("leader", 1.03, "usual front-runner: Gowran Park flat A/E 1.08 (305; since 2022 1.12)"),
        ("older_noform", 0.94, "age 6+ with no win/2nd in last 3: Gowran Park flat A/E 0.86 (883; since 2022 0.87)"),
        ("weak_finish", 0.97, "weakened / no extra in either of last 2: Gowran Park flat A/E 0.94 (2,792; since 2022 0.95)"),
    ],
    ("plumpton", "JUMPS"): [   # methods/plumpton/JUMPS.md v1.0 DATA-BUILT 18 Oct (owner has no Plumpton method; 730 races 2019-26)
        ("top_rpr", 1.08, "top recent RPR: Plumpton A/E 1.25, +7% (786; since 2022 1.19)"),
        ("unproven_trip", 0.95, "first time at the trip: Plumpton A/E 0.90 (908; since 2022 0.90)"),
        ("ground_spec", 1.03, "won on today's exact going, only 1-2 in the field have: Plumpton A/E 1.09 (433; since 2022 1.11)"),
        ("leader", 1.03, "usual front-runner: Plumpton A/E 1.11 (534; since 2022 1.05)"),
        ("improver", 1.02, "last RPR above its previous best: Plumpton A/E 1.14 (677; since 2022 1.02)"),
    ],
    ("limerick", "JUMPS"): [   # methods/limerick/JUMPS.md v1.0 DATA-BUILT 16 Oct (owner's upload was a title only; 713 races 2019-26)
        ("top_rpr", 1.06, "top recent RPR: Limerick jumps A/E 1.17, +1% (766; since 2022 1.17)"),
        ("leader", 1.04, "usual front-runner: Limerick jumps A/E 1.19 (419; since 2022 1.09)"),
        ("improver", 1.04, "last RPR above its previous best: Limerick jumps A/E 1.10 (1,026; since 2022 1.11)"),
        ("won_last", 1.03, "won last time: Limerick jumps A/E 1.07 (546; since 2022 1.11)"),
        ("cd_winner", 0.94, "course & distance winner over-bet here: Limerick jumps A/E 0.90 (271; since 2022 0.77)"),
        ("older_noform", 0.96, "age 6+ with no win/2nd in last 3: Limerick jumps A/E 0.91 (3,268; since 2022 0.92)"),
    ],
    ("naas", "FLAT"): [   # methods/naas/FLAT.md v6.0 (owner AURORA-X v5.1; cards 4 Jul 4/8 +£0.73, 23 Aug 2/7 +£3.10 verified; data-tested 10 Oct)
        ("top_rpr", 1.06, "top recent RPR: Naas A/E 1.16 (727; 1.25 / 1.12)"),
        ("unproven_trip", 1.05, "first time at the trip: Naas A/E 1.31 (456; 1.43 / 1.23) - owner's trip gate REVERSED"),
        ("ground_spec", 1.05, "won on today's exact going, only 1-2 in the field have: Naas A/E 1.27 (248; 1.34 / 1.23)"),
        ("slow_start:6.5", 1.04, "slow starter in a 5-6f race: Naas A/E 1.29 (194; 1.42 / 1.23) - owner's start-risk reject REVERSED"),
        ("improver", 1.02, "last RPR above its previous best: Naas A/E 1.06 (1,046; 1.01 / 1.09)"),
        ("draw_low", 1.02, "drawn 1-4 on good or firmer: Naas A/E 1.09 (1,114; 1.21 / 1.03)"),
        ("lone_leader@SOFT", 1.05, "only habitual front-runner in the race, soft ground: Naas A/E 1.41 (118; 1.20 / 1.53) - "
                                   "on good 0.68 (v6.1, 11 Oct review)"),
        ("jockey_low", 0.97, "jockey under 6% strike rate: Naas A/E 0.91 (2,165; 0.82 / 0.98)"),
    ],
    ("chepstow", "JUMPS"): [   # methods/chepstow/JUMPS.md v17.0 (owner v16.6; 11 Apr v3.1 card 5/7 +£9.79 verified; data-tested 8 Oct)
        ("top_rpr", 1.08, "top recent RPR: Chepstow jumps A/E 1.23 (816; 1.19 / 1.25)"),
        ("exact_rpr", 1.06, "top exact-conditions RPR: Chepstow A/E 1.28 (705; 1.24 / 1.30)"),
        ("ground_spec", 1.05, "one of only 1-2 winners on this exact going: Chepstow A/E 1.20 (410; 1.10 / 1.26)"),
        ("won_last", 1.03, "won last time: Chepstow A/E 1.09 (687; 1.07 / 1.10)"),
        ("older_noform", 0.95, "age 6+ with no win/2nd in last 3: Chepstow A/E 0.89, -39% (2,297; 0.93 / 0.86)"),
        ("hung", 0.95, "keen / hung in either of last 2: Chepstow A/E 0.88, -43% (1,312; 0.84 / 0.90)"),
    ],
    ("downpatrick", "JUMPS"): [   # methods/downpatrick/JUMPS.md v1.5 (owner v1.4; 2 cards 3/12 +£2.95; data-tested 8 Oct)
        ("leader", 1.05, "usual front-runner: Downpatrick A/E 1.14 (298; 1.10 / 1.17) - stiff, undulating track"),
        ("lone_leader", 1.04, "lone front-runner: Downpatrick A/E 1.12 (165; 1.07 / 1.16)"),
        ("top_rpr", 1.00, "top recent RPR only matches the market here: A/E 1.01 (563; 0.93 / 1.06) - national boost off"),
    ],
    ("killarney", "FLAT"): [   # methods/killarney/FLAT.md v1.0 DATA-BUILT (owner upload was a title only, 5 Oct)
        ("top_rpr", 1.10, "top recent RPR: Killarney flat A/E 1.26, +6% at SP (352; 1.27 / 1.25)"),
        ("leader", 0.88, "usual front-runner: Killarney flat A/E 0.75 (120; 0.70 / 0.79)"),
        ("lone_leader", 0.88, "lone front-runner: Killarney flat A/E 0.69 (76; 0.78 / 0.62)"),
        ("held_up", 1.05, "usually held up: Killarney flat A/E 1.12 (976; 1.08 / 1.15)"),
        ("weak_finish", 0.95, "weakened / no extra in either of last 2: A/E 0.90 (907; 0.85 / 0.92)"),
        ("older_noform", 0.93, "age 6+ with no win/2nd in last 3: A/E 0.83 (364; 0.93 / 0.79)"),
        ("exact_rpr", 0.96, "top exact-conditions RPR is over-bet here: A/E 0.89 (267; 0.98 / 0.82)"),
    ],
    ("stratford", "JUMPS"): [   # methods/stratford/JUMPS.md v1.0 (owner cards 17 May 1/7, 25 Aug 0/6 - no peak; data-built 5 Oct)
        ("top_rpr", 1.08, "top recent RPR: Stratford A/E 1.16, -2% at SP (778; 1.28 / 1.09)"),
        ("exact_rpr", 1.05, "top exact-conditions RPR (owner's HR11): A/E 1.11 (674; 1.20 / 1.05)"),
        ("leader", 1.05, "usual front-runner: Stratford A/E 1.11 (571; 1.06 / 1.14)"),
        ("lone_leader", 1.05, "lone front-runner: Stratford A/E 1.15 (255; 1.30 / 1.06)"),
        ("improver", 1.06, "improver: Stratford A/E 1.12 (599; 1.19 / 1.08)"),
        ("ground_spec", 0.95, "won on today's going, 1-2 in field have: A/E 0.86 (348; 0.69 / 0.96)"),
    ],
    ("fairyhouse", "JUMPS"): [   # methods/fairyhouse/JUMPS.md v1.0 (owner framework, no cards; data-built 5 Oct)
        ("unproven_trip", 0.90, "never run within 1f of the trip (owner priority 1): Fairyhouse A/E 0.84, -40% (1,624; 0.82 / 0.85)"),
        ("improver", 1.05, "improver: Fairyhouse A/E 1.10 (1,460; 1.20 / 1.03)"),
        ("won_last", 1.05, "won last time: Fairyhouse A/E 1.11 (971; 1.16 / 1.08)"),
        ("lone_leader", 0.90, "lone front-runner: Fairyhouse A/E 0.77 (277; 0.74 / 0.79)"),
    ],
    ("leicester", "FLAT"): [   # methods/leicester/FLAT.md v27.0 (owner v26.8-v26.16, 5 cards all losing; best 26 May v26.8 2/7; data-tested 6 Oct)
        ("exact_rpr", 1.08, "top exact-conditions RPR: Leicester A/E 1.13, -9% at SP (774; 1.11 / 1.14)"),
        ("top_rpr", 1.03, "top recent RPR: Leicester A/E 1.05 (968; 1.11 / 1.02)"),
        ("slow_start:6.5", 0.88, "slow starter at 5-6f: Leicester A/E 0.83, -57% (143; 0.77 / 0.86)"),
        ("improver", 0.96, "improver is over-bet here: A/E 0.94 (827; 0.94 / 0.94)"),
    ],
    ("aintree", "JUMPS"): [   # methods/aintree/JUMPS.md v1.0 DATA-BUILT (no owner method; 380 races 2019-26), built 24 Oct
        ("top_rpr", 1.06, "top recent RPR: Aintree jumps A/E 1.25 (413; 2019-21 ~1.38 / 2022-26 1.18)"),
        ("unproven_trip", 1.03, "never run within 1f of this trip is UNDER-bet here: A/E 1.20 (642; ~1.27 / 1.15)"),
        ("exact_rpr", 0.95, "top exact-conditions RPR over-bet here: A/E 0.87 (369; ~0.87 / 0.87)"),
        ("cd_winner", 0.97, "course & distance winner over-bet here: A/E 0.90 (251; ~0.76 / 0.95)"),
        ("leader", 0.95, "usual front-runner: A/E 0.83 (535; ~0.83 / 0.83)"),
        ("older_noform", 0.96, "age 6+ with no win/2nd in last 3: A/E 0.90 (810; ~0.89 / 0.91)"),
    ],
    ("galway", "FLAT"): [   # methods/galway/FLAT.md v1.0 DATA-BUILT 26 Oct (no owner method; 357 races 2019-26)
        ("top_rpr", 1.06, "top recent RPR: Galway flat A/E 1.15 (401; ~1.26 / 1.07)"),
        ("cd_winner", 1.06, "course and distance winner: A/E 1.51 (228; ~2.37 / 1.18)"),
        ("won_last", 1.04, "won last time: A/E 1.29 (435; ~1.62 / 1.05)"),
        ("leader", 1.04, "usual front-runner: A/E 1.18 (224; ~1.20 / 1.17)"),
        ("older_noform", 0.94, "age 6+ no win/2nd in last 3: A/E 0.78 (527; ~0.38 / 0.95)"),
        ("slow_start:8.5", 0.92, "slow away 2+ of last 4, up to 1m: A/E 0.38 (133; ~0.63 / 0.21)"),
        ("bend_7f", 0.95, "drawn 7+ at 7f: A/E 0.85 (854; ~0.82 / 0.87)"),
    ],
    ("newcastle", "JUMPS"): [   # methods/newcastle/JUMPS.md v1.0 DATA-BUILT 26 Oct (no owner method; 616 races 2019-26)
        ("top_rpr", 1.05, "top recent RPR: Newcastle jumps A/E 1.12 (655; ~1.18 / 1.08)"),
        ("exact_rpr", 1.04, "top exact-conditions RPR: A/E 1.11 (563; ~1.09 / 1.12)"),
        ("ground_spec", 1.05, "won on today's exact going, 1-2 in field have: A/E 1.16 (363; ~1.18 / 1.15)"),
        ("leader", 0.96, "usual front-runner: A/E 0.91 (452; ~0.86 / 0.94)"),
    ],
    ("bangor_on_dee", "JUMPS"): [   # methods/bangor_on_dee/JUMPS.md v1.0 DATA-BUILT 26 Oct (no owner method; 599 races 2019-26)
        ("ground_spec", 1.05, "won on today's exact going, 1-2 in field have: A/E 1.18 (266; ~1.22 / 1.16)"),
        ("improver", 1.03, "last RPR above its previous best: A/E 1.11 (596; ~1.22 / 1.06)"),
        ("won_last", 1.03, "won last time: A/E 1.07 (508; ~1.07 / 1.07)"),
    ],
    ("wexford", "JUMPS"): [   # methods/wexford/JUMPS.md v1.0 DATA-BUILT (no owner method; 609 races 2019-26), built 24 Oct
        ("top_rpr", 1.04, "top recent RPR: Wexford jumps A/E 1.09 (657; 2019-21 ~1.15 / 2022-26 1.06)"),
        ("unproven_trip", 1.02, "never run within 1f of this trip: A/E 1.10 (1,031; ~1.17 / 1.06)"),
        ("leader", 0.95, "usual front-runner: A/E 0.84 (351; ~0.84 / 0.84)"),
        ("ground_spec", 0.97, "won on today's exact going, 1-2 in field have - over-bet here: A/E 0.88 (295; ~0.91 / 0.86)"),
        ("lone_leader", 0.95, "only habitual front-runner in the race: Wexford jumps A/E 0.83 (209; ~0.86 / 0.81), national 1.01 - v1.1 25 Oct"),
    ],
    ("galway", "JUMPS"): [   # methods/galway/JUMPS.md v1.0 DATA-BUILT (owner upload was a title only, 6 Oct)
        ("held_up", 1.08, "usually held up: Galway jumps A/E 1.16 (1,262; 1.12 / 1.20)"),
        ("ground_spec", 1.10, "won on today's exact going, 1-2 in field have: A/E 1.27 (169; 1.34 / 1.20)"),
        ("exact_rpr", 1.03, "top exact-conditions RPR: A/E 1.07 (347; 1.13 / 1.03)"),
        ("unproven_trip", 0.93, "never run within 1f of this trip: A/E 0.90, -59% (739; 0.94 / 0.87)"),
        ("older_noform", 0.95, "age 6+ with no win/2nd in last 3: A/E 0.86 (1,512; 0.73 / 0.96)"),
        ("top_rpr", 1.00, "top recent RPR boost OFF: 1.75 in 2019-21 but 1.00 since 2022 (405)"),
    ],
    ("huntingdon", "JUMPS"): [   # methods/huntingdon/JUMPS.md v1.0 DATA-BUILT (owner upload was a title only, 6 Oct)
        ("exact_rpr", 1.06, "top exact-conditions RPR: Huntingdon A/E 1.10, -2% at SP (808; 1.05 / 1.13)"),
        ("jockey_low", 0.85, "jockey under 6% (5y, 30+ rides): A/E 0.76, -54% (714; 0.85 / 0.68)"),
        ("cd_winner", 0.95, "C&D winner is over-bet here: A/E 0.92 (446; 0.84 / 0.95)"),
        ("hung", 0.95, "keen / hung in either of last 2 runs: A/E 0.91 (1,583; 0.91 / 0.91)"),
    ],
    ("fontwell", "JUMPS"): [   # methods/fontwell/JUMPS.md v16.0 (owner peak v15.0, 28 Aug 3/6 +£0.54; data-tested 3 Oct)
        ("top_rpr", 1.10, "top recent RPR: Fontwell A/E 1.19, +7% at SP (1,000; 1.19 / 1.19) - strongest rule here"),
    ],
    ("redcar", "FLAT"): [   # methods/redcar/FLAT.md v4.0 (owner peak v3.0-v3.5, Apr-May +£5.58 / +£3.96 / +£2.10)
        ("top_rpr", 1.07, "top recent RPR: Redcar A/E 1.14 (974; 1.10 / 1.16)"),
        ("won_last", 1.07, "won last time: Redcar A/E 1.17 (598; 1.25 / 1.12)"),
        ("improver", 1.03, "improver (last RPR a new best): Redcar A/E 1.07 (792; 1.11 / 1.05)"),
        ("older", 0.97, "age 6+ (owner HR4 age screen, softened): Redcar A/E 0.93 (1,400; 0.91 / 0.94)"),
        ("back_bighcap:12", 1.06, "usually held up / midfield in a 12+ runner handicap: Redcar A/E 1.17 / 1.10 (2019-22 / 2023-26, 1,152; all GB/IRE 12+ handicaps ~1.00) - TRIAL v4.1"),
        ("front_bighcap:12", 0.94, "usual front-runner / prominent in a 12+ runner handicap: Redcar A/E 0.82 / 0.91 (1,174) - TRIAL v4.1"),
    ],
    ("gowran_park", "JUMPS"): [   # methods/gowran_park/JUMPS.md v1.0 DATA-BUILT (no owner method, 2 Oct review)
        ("top_rpr", 1.08, "top recent RPR: Gowran Park jumps A/E 1.32, +7% at SP (348; 1.62 / 1.10)"),
        ("improver", 1.06, "improver (last RPR a new best): Gowran Park jumps A/E 1.14 (499; 1.10 / 1.17)"),
    ],
    ("hexham", "JUMPS"): [   # methods/hexham/JUMPS.md v1.0 DATA-BUILT (no owner method, 2 Oct review)
        ("held_up", 1.05, "usually held up: Hexham A/E 1.11 (1,887; 1.11 / 1.11)"),
        ("improver", 1.07, "improver (last RPR a new best): Hexham A/E 1.18 (578; 1.30 / 1.10)"),
        ("unproven_trip", 0.93, "never run within 1f of the trip: Hexham A/E 0.86, -49% (603; 0.87 / 0.85)"),
        ("weak_finish", 0.95, "weakened / no extra in either of last 2: Hexham A/E 0.87 (2,274; 0.78 / 0.92)"),
        ("top_rpr", 1.02, "top recent RPR: Hexham A/E 1.04 (719; 1.08 / 1.01) - national 1.05 trimmed"),
    ],
    ("musselburgh", "FLAT"): [   # methods/musselburgh/FLAT.md v1.6 (owner review 006/007 peak card +£11.16)
        ("lone_leader", 1.08, "lone front-runner: Musselburgh A/E 1.21, +35% (293; 1.08 / 1.31)"),
        ("leader", 1.04, "usual front-runner with rivals: Musselburgh A/E 1.10, +8% (635; 1.14 / 1.07)"),
        ("top_rpr", 1.05, "top recent RPR: Musselburgh A/E 1.10 (885; 1.08 / 1.11)"),
        ("held_up", 0.96, "usually held up: Musselburgh A/E 0.93 (2,180; 0.93 / 0.93)"),
        ("jockey_low", 0.93, "jockey under 6% strike rate: Musselburgh A/E 0.86 (718; 0.88 / 0.84)"),
        ("won_last", 0.96, "won last time (over-bet here): Musselburgh A/E 0.92 (654; 0.94 / 0.91)"),
    ],
}
GROUND_FIRST_TIME = {
    ("JUMPS", "SOFT"): (0.86, "never run on soft/heavy (jumps): wins 6.5%, A/E 0.86 (812 runners, 2023-26)"),
    ("FLAT", "GOOD"): (0.90, "never run on good (flat): A/E 0.89 (2,086 runners, 2023-26)"),
    ("FLAT", "FAST"): (0.97, "never run on good-to-firm/firm (flat): A/E 0.97 (2,834 runners, 2023-26)"),
    # FLAT SOFT not penalised: first time on soft A/E 1.09 (2,711) - they do fine; JUMPS GOOD/FAST 1.06-1.07
}
WEAK_FINISH = re.compile(r"weakened|no extra|faded|one pace|tired|found little|emptied", re.I)
HUNG = re.compile(r"hung (left|right|badly)|hanging (left|right)", re.I)
JUMPS_TYPES = ("hurdle", "chase", "nh flat")


def family(disc):
    return "JUMPS" if disc in ("HURDLE", "CHASE", "NHF", "JUMPS") else disc


# Lessons that hold across ALL UK/IRE courses (owner 2026-09-26: carry learning from one method to the
# others). Used at every course unless its own method has a tested rule of the same kind.
DEFAULT_ANGLES = {
    "FLAT": [("top_rpr", 1.04, "top recent RPR (best of last 3): all UK/IRE flat A/E 1.09 (38,336)")],
    "AW_FLAT": [("top_rpr", 1.03, "top recent RPR (best of last 3): all UK/IRE AW A/E 1.07 (22,944)")],
    "JUMPS": [("top_rpr", 1.05, "top recent RPR (best of last 3): all UK/IRE jumps A/E 1.12 (39,230)")],
}


def angles_for(course, disc):
    fam = family(disc)
    own = ANGLES.get((course, fam), [])
    kinds = {rule.partition(":")[0] for rule, _, _ in own}
    return own + [a for a in DEFAULT_ANGLES.get(fam, []) if a[0] not in kinds]


def _range(spec):
    lo, _, hi = spec.partition("-")
    return (float(lo), float(hi)) if hi else (0.0, float(lo))


def horse_history(paths, horses, before):
    runs = {h: [] for h in horses}
    seen = set()
    for path in paths:
        with open_text(path) as handle:
            for row in csv.DictReader(handle):
                day = str(row.get("date") or "").replace("/", "-")
                key = name_key(row.get("horse"))
                if key not in runs or day >= before or (day, key) in seen:
                    continue
                seen.add((day, key))
                ck_, aw_ = course_key(row.get("course") or "")
                runs[key].append({"date": day, "course": ck_, "aw": aw_ or going_group(row.get("going")) == "STANDARD",
                                  "course_name": row.get("course") or "",
                                  "going_raw": str(row.get("going") or "").strip().lower(),
                                  "furlongs": dist_to_furlongs(row.get("dist")),
                                  "going": going_group(row.get("going")), "rpr": to_int(row.get("rpr")),
                                  "pos": to_int(row.get("pos")), "pos_raw": str(row.get("pos") or "").strip().upper(),
                                  "lbs": weight_lbs(row),
                                  "type": (row.get("type") or "").lower(),
                                  "comment": row.get("comment") or ""})
    for v in runs.values():
        v.sort(key=lambda r: r["date"])
    return runs


def main_going(text):
    """'Good to Firm (Good in places)' / 'Soft, Heavy in places' -> 'good to firm' / 'soft' (the official main going)."""
    t = re.split(r"[(,;]| in places", str(text or "").lower())[0].replace(" / ", " to ")   # SL 'Standard / Slow'
    return re.sub(r"\s+", " ", t).strip()


def exact_rpr_selection(rows, runs, fam, furlongs, going_raw, today_aw, top_recent_name):
    """Owner's EXACT RPR selection (2026-09-26, Centigrade at Haydock): the runner with the highest
    RPR from a past run on EXACTLY today's going (same description, e.g. heavy) over the same trip
    (within half a furlong), same code (flat turf / AW / jumps). Shows the weight it carried then vs
    today. Backtest 2023-26, UK/IRE only (46,647 races, scripts/exact_rpr_backtest.py): pick in 80% of races,
    wins 15.7%, 1.04 x its market chance; when it is ALSO the top recent-RPR horse (CONFIRMED)
    23.4%, 1.10 (11,480); when not, 12.2%, 0.99. Carrying less weight than that run did NOT help
    (lighter 1.03 vs heavier 1.05), so weight is shown, not used to pick."""
    best = None
    for r in rows:
        for h in runs[name_key(r["name"])]:
            if not h["rpr"] or not h["furlongs"] or not furlongs:
                continue
            if (h["type"] in JUMPS_TYPES) != (fam == "JUMPS") or (fam != "JUMPS" and h["aw"] != today_aw):
                continue
            if abs(h["furlongs"] - furlongs) > 0.5 or main_going(h["going_raw"]) != main_going(going_raw):
                continue
            if best is None or h["rpr"] > best[1]["rpr"] or (h["rpr"] == best[1]["rpr"] and h["date"] > best[1]["date"]):
                best = (r, h)
    if not best:
        return {"exact_rpr_pick": "", "exact_rpr": None, "exact_rpr_run": "no runner has run on this exact going over this trip",
                "exact_weight_change": None, "exact_confirmed": False}
    r, h = best
    today_lbs = to_int(r.get("lbs"))
    change = today_lbs - h["lbs"] if today_lbs and h["lbs"] else None
    st = lambda lb: f"{lb // 14}-{lb % 14}"
    wtxt = ("" if change is None else f"; carried {st(h['lbs'])} then, {st(today_lbs)} today ("
            + ("same weight" if change == 0 else f"{abs(change)}lb {'lighter' if change < 0 else 'heavier'}") + ")")
    return {"exact_rpr_pick": r["name"], "exact_rpr": h["rpr"],
            "exact_rpr_run": f"RPR {h['rpr']} at {h['course_name']} {h['date']}, {h['going_raw']} {h['furlongs']:g}f"
                             f" (finished {h['pos'] or '-'}){wtxt}",
            "exact_weight_change": change, "exact_confirmed": r["name"] == top_recent_name}


# owner 2026-10-07 ("try extra extra hard ... get more winners on all cards"): live locked races 25 Sep-6 Oct (490): when our
# top pick had DRIFTED 15%+ from the day-before price to the race-morning price, it won 5 of 58; the next-best pick that had
# not drifted won 15 of those 58. Rule = top pick unless drifted 15%+ overnight, then the next of our top 3 that has not.
# Picks 159 -> 169 winners (£1 SP -78.18 -> -39.78); held in both halves (25-30 Sep 1 v 3 switched winners, 1-6 Oct 4 v 12)
# and at every threshold 1.10-1.33. TRIAL - race-day prices only (the day before has nothing to compare). False = off.
# OFF (owner 2026-10-07 evening: "we need to make a decision that it doesn't fully change to the backed in horse as all our
# evidence and data goes to waste!"): the win pick is ALWAYS our top pick on the evidence + data. A 15%+ overnight drift is
# shown as a DRIFTING warning (DRIFT_WARN) and the betslip keeps a drifted horse out of the multiples - nothing is switched.
PRICE_RULE_KINDS = {"aob_outsider"}   # rule kinds that look at the betting (left out of the Data pick)
DRIFT_SWITCH = False
DRIFT_WARN = 1.15


def overnight_prices(race_date, course):
    """Day-before price per (off_time, horse) for this course: the evening check, else the morning one. Empty unless a
    race-day (d0) price check exists, so Early / Early Bird builds never switch."""
    day = REPO_ROOT / "reports" / "odds" / race_date
    if not DRIFT_WARN or not (day / "d0_morning.csv").exists():
        return {}
    for check in ("d-1_evening", "d-1_morning"):
        f = day / f"{check}.csv"
        if f.exists():
            out = {}
            for r in csv.DictReader(open(f, encoding="utf-8")):
                if course_key(r["course"])[0] == course:
                    v = num(r.get("best_dec")) or num(r.get("sl_dec"))
                    if v:
                        out[(r["off_time"], name_key(r["horse"]))] = v
            if out:
                return out
    return {}


def overnight_move(overnight, row, price):
    """'2.10 -> 2.50 (drifted)' from the day-before price when the evidence pack has no price move (Brookside La, 7 Oct:
    drifted 2.10 -> 2.50 overnight but its move was blank, so the slip's drift check let it into the Lucky 63)."""
    eve = overnight.get((row["off_time"], name_key(row["name"])))
    if not eve or not price or abs(eve - price) < 0.005:
        return ""
    return f"{eve:.2f} -> {price:.2f} ({'drifted' if price > eve else 'shortened'})"


NON_COMPLETION = {"PU", "UR", "F", "RO", "BD", "SU", "REF", "RR", "CO", "LFT"}
DRY_WON, DRY_NEVER = 1.04, 0.96   # weather dry-out factors (test A/E 1.06 / 0.93, set a little softer)


def weather_trends(race_date):
    """course key -> ground trend from today's weather check (weather/fetch.py), '' when there is none."""
    p = REPO_ROOT / "reports" / "weather" / race_date / "weather.json"
    if not p.exists():
        return {}
    return {course_key(name)[0]: v.get("trend", "") for name, v in json.loads(p.read_text()).get("courses", {}).items()}


def build(race_date, course, paths):
    day_dir = REPO_ROOT / "reports" / "racecards" / race_date
    evidence = [r for r in csv.DictReader(open(day_dir / "evidence.csv", encoding="utf-8"))
                if r["course_id"] == course]
    from predict.today import apply_latest_going
    apply_latest_going(race_date, evidence)   # 19 Oct Pontefract: use the newest official going, not the 06:15 card
    # 9 Nov (review team): Trasna Na Pairce (12:30 Punchestown) was the EXACT RPR pick and Captain Connor (14:15
    # Stratford) stayed in the field although our 08:15 price check listed both as NONRUNNER - predict.today drops
    # those, this overlay read evidence.csv unfiltered. Drop any runner a price check of this race day calls a non-runner.
    nr_race = set()
    for path in sorted((REPO_ROOT / "reports" / "odds" / race_date).glob("d*_*.csv")):
        for r in csv.DictReader(open(path, encoding="utf-8")):
            if (r.get("status") or "").upper() in ("NONRUNNER", "NON-RUNNER", "NR", "WITHDRAWN"):
                nr_race.add(((r.get("off_time") or "")[:5], name_key(r["horse"])))
    evidence = [r for r in evidence if ((r.get("off_time") or "")[:5], name_key(r["name"])) not in nr_race]
    cards = json.loads((day_dir / "racecards.json").read_text())
    cards = {str(r["race_id"]): r for r in (cards["races"] if isinstance(cards, dict) else cards)}
    preds = json.loads((REPO_ROOT / "reports" / "predictions" / race_date / "predictions.json").read_text())
    preds = {p["race_id"]: p for p in preds}
    runs = horse_history(paths, {name_key(r["name"]) for r in evidence}, race_date)
    overnight = overnight_prices(race_date, course)
    weather = weather_trends(race_date)
    from predict.ground_check import softness   # lazy: ground_check imports this module
    races = {}
    for r in evidence:
        races.setdefault(r["race_id"], []).append(r)
    out = []
    for race_id, rows in sorted(races.items(), key=lambda kv: kv[1][0]["off_time"]):
        card, pred = cards[race_id], preds[race_id]
        model = {a["name"]: a["chance"] for a in pred["all"]}
        furlongs = card.get("furlongs") or 0
        going = going_group(rows[0]["going"])
        hcap = bool(card.get("handicap"))
        cls = str(card.get("race_class") or "")
        prices = [num(r["price_dec"]) or num(r["forecasted_odds"]) for r in rows]
        fav = min(p for p in prices if p) if any(prices) else None
        exact = {}
        for r in rows:
            vals = [h["rpr"] for h in runs[name_key(r["name"])] if h["rpr"]
                    and (h["type"] in JUMPS_TYPES) == (family(pred.get("discipline") or "FLAT") == "JUMPS")
                    and h["furlongs"] and abs(h["furlongs"] - furlongs) <= 1 and h["going"] == going]
            exact[r["name"]] = max(vals) if vals else None
        top_exact = max([v for v in exact.values() if v] or [0])
        fam = family(pred.get("discipline") or "FLAT")
        rules = angles_for(course, pred.get("discipline") or "FLAT")
        same_fam = lambda hist: [h for h in hist if (h["type"] in JUMPS_TYPES) == (fam == "JUMPS")]
        leaders = sum(1 for r in rows if r["pace_role"] == "LEADER")
        # exact going, as methods.audit tested it (26 Oct fix: the going GROUP made Yielding/Soft/Heavy one ground -
        # Galway exact 1.19 | 1.38 v group 0.93 | 1.12)
        today_main = main_going(rows[0]["going"])
        ground_winners = {r["name"] for r in rows if any(
            h["pos"] == 1 and main_going(h["going_raw"]) == today_main for h in same_fam(runs[name_key(r["name"])]))}
        recent_best = {}
        for r in rows:
            vals = [h["rpr"] for h in same_fam(runs[name_key(r["name"])])[-3:] if h["rpr"]]
            recent_best[r["name"]] = max(vals) if vals else None
        top_recent = max([v for v in recent_best.values() if v] or [0])
        s0 = softness(rows[0]["going"])
        dry_out = (s0 - 1) if (s0 is not None and weather.get(course_key(rows[0].get("course_name") or course)[0], "").startswith("MAY DRY OUT")) else None
        adj, notes = [], {}
        data_f = {}   # owner 4 Nov 2026 'Data pick': course-method factors that never look at the price
        for r, price in zip(rows, prices):
            f, why, neg = 1.0, [], []
            f_np = 1.0
            hist = same_fam(runs[name_key(r["name"])])
            for rule, factor, text in rules:
                rule_core, _, only_going = rule.partition("@")   # "leader@SOFT" = only on that going group
                if only_going and going not in only_going.split("|"):   # "draw3:...@GOOD|FAST" = either going group
                    continue
                kind, _, spec = rule_core.partition(":")
                lo, hi = _range(spec) if spec and kind not in ("jockey_name", "draw3") else (0.0, 99.0)
                in_trip = lo <= furlongs <= hi
                hit = False
                if kind == "lone_leader":
                    hit = in_trip and r["pace_role"] == "LEADER" and r["race_pace_scenario"] == "LONE_LEADER"
                elif kind == "leader":
                    hit = in_trip and r["pace_role"] == "LEADER" and r["race_pace_scenario"] != "LONE_LEADER"
                elif kind == "held_up_short":
                    hit = r["pace_role"] == "HOLD_UP" and furlongs <= 7.5 and leaders < 2
                elif kind == "slow_start":
                    hit = in_trip and sum(bool(SLOW_START.search(h["comment"])) for h in hist[-4:]) >= 2
                elif kind == "exact_rpr":
                    hit = bool(exact[r["name"]]) and exact[r["name"]] == top_exact
                elif kind == "top_rpr":
                    hit = bool(recent_best[r["name"]]) and recent_best[r["name"]] == top_recent
                elif kind == "ground_spec":
                    hit = r["name"] in ground_winners and 1 <= len(ground_winners) <= 2
                elif kind == "cd_winner":
                    hit = any(h["pos"] == 1 and h.get("course") == course and h["furlongs"]
                              and abs(h["furlongs"] - furlongs) <= 1 for h in hist)
                elif kind == "older":
                    hit = (num(r["age"]) or 0) >= 6
                elif kind == "older_hcap":
                    hit = hcap and (num(r["age"]) or 0) >= 6
                elif kind == "improver":
                    hit = len(hist) >= 3 and bool(hist[-1]["rpr"]) and all(
                        (h["rpr"] or 0) < hist[-1]["rpr"] for h in hist[:-1])
                elif kind == "won_last":
                    hit = bool(hist) and hist[-1]["pos"] == 1
                elif kind == "weak_finish":
                    hit = any(WEAK_FINISH.search(h["comment"]) for h in hist[-2:])
                elif kind == "light":
                    hit = 0 < len(hist) <= 5
                elif kind == "held_up":
                    hit = in_trip and r["pace_role"] == "HOLD_UP"
                elif kind == "prominent":   # usually races prominent (not the habitual leader) - Dundalk 16 Oct
                    hit = in_trip and r["pace_role"] == "PROMINENT"
                elif kind == "draw_high":   # spec = minimum field size; drawn in the top third
                    stall, field = num(r.get("draw")) or 0, len(rows)
                    hit = bool(stall) and field >= (float(spec) if spec else 12) and stall > 2 * field / 3
                elif kind == "draw_low":   # spec = highest stall (default 4); good or firmer ground only
                    stall = num(r.get("draw")) or 0
                    hit = 1 <= stall <= (float(spec) if spec else 4) and going in ("FAST", "GOOD")
                elif kind == "bend_7f":   # Goodwood Bend Control Law: drawn 7 or wider over 6.5-7.5f
                    hit = (num(r.get("draw")) or 0) >= 7 and 6.5 <= furlongs <= 7.5
                elif kind == "hung":
                    hit = any(HUNG.search(h["comment"]) for h in hist[-2:])
                elif kind == "layoff":
                    hit = lo <= (days_since(r.get("last_run")) or 0) <= hi
                elif kind == "course_win_not_cd":
                    wins_here = [h for h in hist if h["pos"] == 1 and h.get("course") == course]
                    hit = bool(wins_here) and not any(h["furlongs"] and abs(h["furlongs"] - furlongs) <= 1 for h in wins_here)
                elif kind == "older_noform":
                    hit = (num(r["age"]) or 0) >= 6 and len(hist) >= 3 and not any(h["pos"] in (1, 2) for h in hist[-3:])
                elif kind == "jockey_low":   # jockey's 5-year strike rate in this discipline under 6% (30+ rides)
                    m = re.match(r"\s*(\d+)/(\d+)", r.get("jockey_discipline_5y") or "")
                    hit = bool(m) and int(m.group(2)) >= 30 and int(m.group(1)) / int(m.group(2)) < 0.06
                elif kind == "unproven_trip":
                    hit = len(hist) >= 1 and not any(h["furlongs"] and abs(h["furlongs"] - furlongs) <= 1 for h in hist)
                elif kind == "unreliable":   # 2+ pulled up / unseated / fell / refused in the last 3 (owner's Perth Gate E/F)
                    hit = sum(1 for h in hist[-3:] if h.get("pos_raw") in NON_COMPLETION) >= 2
                elif kind == "jockey_name":   # named jockey(s), spec = '|'-separated name parts, e.g. jockey_name:bowen
                    hit = any(part and part in (r.get("jockey") or "").lower() for part in spec.split("|"))
                elif kind == "leader_group":   # usual front-runner in a Group race over the trip range (15 Oct)
                    hit = in_trip and r["pace_role"] == "LEADER" and str(card.get("pattern") or "").startswith("Group")
                elif kind == "midfield_group":   # usually races midfield in a Group race over the trip range (15 Oct)
                    hit = in_trip and r["pace_role"] == "MIDFIELD" and str(card.get("pattern") or "").startswith("Group")
                elif kind == "age4_autumn_group":   # 4-year-old in a Group race in September or October (15 Oct)
                    hit = (num(r["age"]) or 0) == 4 and race_date[5:7] in ("09", "10") and str(card.get("pattern") or "").startswith("Group")
                elif kind == "draw3":   # stall third + trip + minimum field [+ usual style], spec 'low,5.5-6.5,14[,front|back]' (15 Oct)
                    third, trip, minf, style = (spec.split(",") + ["", "", "", ""])[:4]
                    tlo, thi = _range(trip)
                    stall, field = num(r.get("draw")) or 0, len(rows)
                    pos = "" if not stall or field < 6 else "low" if stall <= field / 3 else "high" if stall > 2 * field / 3 else "mid"
                    grp = {"front": ("LEADER", "PROMINENT"), "back": ("MIDFIELD", "HOLD_UP")}.get(style)
                    hit = (pos == third and tlo <= furlongs <= thi and field >= float(minf or 0)
                           and (grp is None or r["pace_role"] in grp))
                elif kind == "aob_outsider":   # Aidan O'Brien runner 5th or bigger in the betting in a Group 1 (15 Oct)
                    rank = 1 + sum(1 for q in prices if q and q < price) if price else 0
                    hit = (str(card.get("pattern") or "") == "Group 1" and rank >= 5
                           and (r.get("trainer") or "").replace("'", "").lower() in ("a p obrien", "aidan obrien"))
                elif kind in ("back_bighcap", "front_bighcap", "prominent"):   # usual style in a handicap of spec+ runners (default 12; Redcar 16 Oct)
                    grp = ("HOLD_UP", "MIDFIELD") if kind == "back_bighcap" else ("LEADER", "PROMINENT")
                    hit = hcap and len(rows) >= (float(spec) if spec else 12) and r["pace_role"] in grp
                elif kind == "ground_first":   # 3+ runs of this code, never on today's going group (use with @GOING)
                    hit = len(hist) >= 3 and not any(h["going"] == going for h in hist)
                if hit and r.get("coverage", "COMPLETE") in ("BEHIND", "MISSING", "PARTIAL") \
                        and (kind in ("lone_leader", "leader", "held_up_short", "held_up", "exact_rpr", "top_rpr", "leader_group", "midfield_group",
                                      "unproven_trip", "hung", "older_noform", "course_win_not_cd", "ground_first", "unreliable",
                                      "back_bighcap", "front_bighcap")
                             or (kind == "draw3" and spec.count(",") >= 3)):   # style-based draw rules need a complete record
                    hit = False  # data-gap rule: no history-based claim on an incomplete record
                if hit and factor != 1.0:   # a 1.00 rule only switches a national default off - nothing to show
                    f *= factor
                    if kind not in PRICE_RULE_KINDS:
                        f_np *= factor
                    (why if factor > 1 else neg).append(text)   # penalties are cautions, not angles
            # ALL COURSES (owner 2026-09-26: "never run on the ground is not acceptable unless it's an
            # elite horse"): applied only where history shows a real penalty (2023-26 turf, 3+ runs)
            rule = GROUND_FIRST_TIME.get((fam, going))
            if rule and len(hist) >= 3 and r.get("coverage", "COMPLETE") not in ("BEHIND", "MISSING", "PARTIAL") \
                    and not any(h["going"] == going for h in hist):
                vals = sorted((v for v in recent_best.values() if v), reverse=True)
                mine = recent_best.get(r["name"])
                elite = bool(mine) and mine == vals[0] and (len(vals) < 2 or mine - vals[1] >= 5)
                if not elite:
                    f *= rule[0]
                    f_np *= rule[0]
                    neg.append(rule[1])
            # WEATHER DRY-OUT (owner 10 Oct: "if it's good to soft but it's very hot and sunny, the ground will dry up"):
            # when today's weather check says the turf MAY DRY OUT, horses that have WON on ground one step quicker get a lift
            # and horses that ran on it but never won are marked down. TEST (/tmp/claude-0/wx/test.py, UK/IRE turf 2018-26,
            # going firmer later in the meeting than race 1): won on the quicker ground A/E 1.06 (5,679; 1.06 / 1.05), ran on it
            # never won 0.93 (5,729; 0.90 / 0.96); when the going went SOFTER there was no edge (1.02 / 1.02) -> rain: no change
            if dry_out and len(hist) >= 3 and r.get("coverage", "COMPLETE") not in ("BEHIND", "MISSING", "PARTIAL"):
                on = [h for h in hist if (sv := softness(h.get("going_raw"))) is not None and sv <= dry_out + 0.5
                      and abs(sv - dry_out) <= 1]
                if any(h["pos"] == 1 for h in on):
                    f *= DRY_WON
                    f_np *= DRY_WON
                    why.append("weather: ground may dry out - has won on quicker ground (A/E 1.06 when the going firmed)")
                elif on:
                    f *= DRY_NEVER
                    f_np *= DRY_NEVER
                    neg.append("weather: ground may dry out - has run on quicker ground but never won (A/E 0.93)")
            caution = list(neg)
            ds = days_since(r["last_run"])
            if ds and ds >= 120 and price and price < 3.0:
                caution.append(f"back from {int(ds)} days at under 2/1 (NOTE: no trap in data)")
            if hcap and price and price < 3.0 and hist and not any("handicap" in h["type"] for h in hist) \
                    and r["ofr"] not in ("", "-") and len(hist) <= 3:
                caution.append("possible handicap debut at under 2/1 (NOTE)")
            adj.append(model.get(r["name"], 0.0) * f)
            data_f[r["name"]] = f_np
            notes[r["name"]] = (why, caution)
        total = sum(adj) or 1
        chances = [a / total for a in adj]
        order = sorted(range(len(rows)), key=lambda i: -chances[i])
        top = order[0]
        drift_switch = drift_warning = drift_alt = ""
        if overnight:
            def drifted(i):
                eve = overnight.get((rows[i]["off_time"], name_key(rows[i]["name"])))
                return bool(eve and prices[i] and prices[i] >= eve * (DRIFT_SWITCH or DRIFT_WARN))
            if drifted(top) and not DRIFT_SWITCH:
                eve = overnight[(rows[top]["off_time"], name_key(rows[top]["name"]))]
                drift_warning = (f"{rows[top]['name']} drifted {eve:.2f} -> {prices[top]:.2f} overnight - still our pick on "
                                 f"the evidence, kept out of the multiples")
                # background only (owner 8 Oct: "I still want that monitored in the background"): the horse the old
                # drift switch would have chosen, graded nightly by predict.drift_tracker - never shown or bet
                alt = next((i for i in order[1:3] if not drifted(i)), None)
                drift_alt = rows[alt]["name"] if alt is not None else ""
            elif drifted(top):
                alt = next((i for i in order[1:3] if not drifted(i)), None)
                if alt is not None:
                    eve = overnight[(rows[top]["off_time"], name_key(rows[top]["name"]))]
                    drift_switch = (f"{rows[top]['name']} drifted {eve:.2f} -> {prices[top]:.2f} overnight "
                                    f"(drifted top picks won 5 of 58 live) - switched to {rows[alt]['name']}")
                    top = alt
        p, price = chances[top], prices[top]
        conf = confidence(p, pred.get("discipline"))
        # owner 2026-09-25: never back a favourite just because it is favourite. Our evidence alone
        # (form, DNA, connections - no price) must agree with the pick for it to be a BET.
        # 2025-26: evidence agrees with the fav -> fav won 39-42%; evidence disagrees -> the fav
        # still won ~30% but our evidence horse only ~15%, so the pick stays, flagged PRICE-LED.
        ev_all = {a["name"]: a.get("form_chance", a["chance"]) for a in pred["all"]}
        evidence_pick = max(ev_all, key=ev_all.get) if ev_all else rows[top]["name"]
        agrees = evidence_pick == rows[top]["name"]
        # DATA PICK (owner 4 Nov 2026: "data driven selections of which you ignore the price ... the best horse which ticks
        # all stats and historic and course data ... ignoring the price", "It's called data pick"): the price-free model
        # (form_chance: 46 features, no market) x the course-method factors that never use the price. Shown on every card
        # in place of the Gemini pick. Never on the slip.
        dp_raw = {n: v * data_f.get(n, 1.0) for n, v in ev_all.items()}
        dp_tot = sum(dp_raw.values()) or 1.0
        data_pick = max(dp_raw, key=dp_raw.get) if dp_raw else ""
        data_chance = dp_raw.get(data_pick, 0) / dp_tot
        anchor = max(rows, key=lambda r: exact[r["name"]] or 0) if top_exact else None
        if anchor is None:
            anchor_line = "no runner has an RPR at this trip on this going"
        elif anchor["name"] == rows[top]["name"]:
            anchor_line = f"{anchor['name']} (RPR {top_exact} at trip/going) = WIN PICK"
        elif anchor["name"] == pred["rpr_pick"]:
            anchor_line = f"{anchor['name']} (RPR {top_exact} at trip/going) = RPR PICK"
        else:
            anchor_line = f"{anchor['name']} (RPR {top_exact} at trip/going) = shortlist (our chance {chances[rows.index(anchor)]:.0%})"
        watch = []
        for i in order:
            if prices[i] and prices[i] >= 11.0 and chances[i] * prices[i] >= 1.0:
                watch.append(f"{rows[i]['name']} {frac(prices[i])} (our chance {chances[i]:.0%}, fair {frac(1 / chances[i])})")
        # every 6+ runner race names its best 14/1+ runner: STRONG (value >= 0.9, a bet) or
        # SPECULATIVE (best available, not a bet) - owner's request 2026-09-24
        longshot, long_label = None, ""
        if len(rows) >= 6:
            # owner's rule: our best-RANKED runner priced 14/1+ (15.00+); STRONG only if it is in
            # our top 3 on the data, otherwise SPECULATIVE (never labelled by price x chance)
            # ranked by our EVIDENCE alone (no price): a longshot is a big-priced horse our
            # evidence rates highly (owner 2026-09-25: the price only defines the 15.00+ band)
            ev_order = sorted(range(len(rows)), key=lambda i: -ev_all.get(rows[i]["name"], 0))
            for pos, i in enumerate(ev_order):
                if prices[i] and prices[i] >= LONGSHOT_PRICE:
                    longshot = rows[i]
                    long_label = (f"STRONG (ranked {pos + 1}{['st', 'nd', 'rd'][pos]} by us)" if pos < 3
                                  else f"SPECULATIVE (ranked {pos + 1}th by us)")
                    break
        # owner 10 Oct ("exactly what went wrong yesterday"): Cosmic Connection (9 Oct Chepstow BET, stopped quickly) had its
        # latest run missing from our data. A pick whose latest run we don't hold (BEHIND) or with no form at all in our
        # results (MISSING) is never a BET and is kept off the slip. Live 26 Sep-9 Oct: such BET picks 0/4.
        data_gap = rows[top].get("coverage", "COMPLETE") in ("BEHIND", "MISSING")
        top_recent_name = max(rows, key=lambda r: recent_best[r["name"]] or 0)["name"] if top_recent else ""
        exact_sel = exact_rpr_selection(rows, runs, fam, furlongs, str(rows[0]["going"] or "").strip().lower(),
                                        course_key(rows[0].get("course_name") or course)[1] or going == "STANDARD",
                                        top_recent_name)
        out.append({**exact_sel,
            "time": rows[0]["off_time"], "race": card["race_name"], "distance": rows[0]["distance_label"],
            # 15 Oct: every runner's chance after the course method (Champions Day slip: forecasts + each-way use these)
            "field": [{"name": rows[i]["name"], "chance": round(chances[i], 4),
                       "angles": notes[rows[i]["name"]][0], "cautions": notes[rows[i]["name"]][1]} for i in order],
            "going": rows[0]["going"], "runners": len(rows), "handicap": hcap, "class": cls,
            "win": rows[top]["name"], "price": frac(price), "chance": p, "fair": frac_at_least(1 / p),
            # TRIAL (owner 2026-10-01 "Yes let's trial it - I want to trial everything until it works"): BET = our evidence
            # agrees AND the price is 2.00-2.99 (locked picks 26-30 Sep: 10/21 +£36 at £10; the old confidence-8+ BETs were
            # mostly odds-on, 6/18 -£76). Odds-on picks are never a BET. Set BET_RULE = "confidence" to go back.
            # owner 1 Nov 2026 (firm): 8/10+ is ALWAYS a BET tag, 7/10 and below ALWAYS NO BET (predict.bet_tag); evidence /
            # data-gap / drift checks stay as notes and keep a horse off the bet slip, they no longer change the tag
            "confidence": conf, "verdict": bet_tag.tag(conf),
            "old_rule_bet": bool(is_bet(conf, agrees, price) and not data_gap),
            "data_gap": data_gap,
            "evidence_agrees": agrees, "evidence_pick": evidence_pick,
            "data_pick": data_pick, "data_chance": round(data_chance, 4),
            "data_conf": confidence(data_chance, pred.get("discipline")) if data_pick else None,
            "data_price": next((frac(prices[i]) for i in range(len(rows)) if rows[i]["name"] == data_pick and prices[i]), ""),
            "data_angles": notes.get(data_pick, ([], []))[0], "data_cautions": notes.get(data_pick, ([], []))[1],
            "evidence_chance": ev_all.get(evidence_pick, 0),
            # owner 2026-09-30: "when our evidence disagrees with short priced favourites we proceed with caution"
            # (locked picks 26-29 Sep: price-led picks at SP <= 2.50 won 10/25, -7.63 pts; our evidence horse in
            # those races 5/20, +16.63 pts) - flagged CAUTION: SHORT FAV on the cards, never a bet
            "evidence_price": next((frac(prices[i]) for i in range(len(rows)) if rows[i]["name"] == evidence_pick and prices[i]), ""),
            "short_fav_caution": bool(not agrees and price and price <= SHORT_FAV_PRICE),
            "win_angles": notes[rows[top]["name"]][0], "win_caution": notes[rows[top]["name"]][1],
            "move": rows[top]["price_move"] or overnight_move(overnight, rows[top], price),
            "drift_switch": drift_switch,
            "drift_warning": drift_warning,
            "drift_alt": drift_alt,
            # 20 Nov: a walkover (one runner left) crashed the whole course here and the pack used a stale file
            "second": (f"{rows[order[1]]['name']} {frac(prices[order[1]])} ({chances[order[1]]:.0%})"
                       if len(order) > 1 else "none (only one runner)"),
            "rpr_pick": pred["rpr_pick"], "rpr_reason": pred["rpr_reason"], "anchor": anchor_line,
            "longshot": f"{longshot['name']} {frac(num(longshot['price_dec']))} {long_label}" if longshot else "no longshot",
            "watchlist": watch, "pace": rows[0]["race_pace_text"] or rows[0]["race_pace_scenario"],
            "changed": rows[top]["name"] != pred["win"],
            "model_pick": pred["win"],
        })
    return out


def render(race_date, course, picks):
    lines = [f"# {course.title()} {race_date} — ZANS course method selections", ""]
    for p in picks:
        lines += [f"## {p['time']} {p['race']} ({p['distance']}, {p['going']}, {p['runners']} ran)",
                  f"- WIN: **{p['win']}** {p['price']} — {p['confidence']}/10 — **{p['verdict']}** "
                  f"(our chance {p['chance']:.0%}, fair {p['fair']}; {p['move']})",
                  f"  - angles: {'; '.join(p['win_angles']) or 'none'}"
                  + (f"; caution: {'; '.join(p['win_caution'])}" if p["win_caution"] else ""),
                  f"  - next best: {p['second']}"
                  + (f" (course method changed the pick from {p['model_pick']})" if p["changed"] else ""),
                  f"- RPR ANCHOR: {p['anchor']}",
                  f"- RPR PICK: **{p['rpr_pick']}** — {p['rpr_reason']}",
                  f"- EXACT RPR: **{p.get('exact_rpr_pick') or 'none'}**{' (CONFIRMED: also top recent RPR)' if p.get('exact_confirmed') else ''} — {p.get('exact_rpr_run', '')}",
                  f"- LONGSHOT: {p['longshot']}",
                  f"- EARLY-PRICE WATCHLIST: {'; '.join(p['watchlist']) or 'none'}",
                  f"- PACE: {p['pace']}", ""]
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--course", required=True)
    parser.add_argument("--history", nargs="+", required=True)
    args = parser.parse_args(argv)
    picks = build(args.date, args.course, args.history)
    out = REPO_ROOT / "reports" / "predictions" / args.date
    (out / f"{args.course}_method.json").write_text(json.dumps(picks, indent=1))
    text = render(args.date, args.course, picks)
    (out / f"{args.course}_method.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
