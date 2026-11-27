"""ZANS Bet Slip: every bet for the day across ALL cards, in one branded page / PDF (owner,
2026-09-25: "a separate PDF called ZANS Bet Slip with all the bets ... doubles, forecasts,
Lucky 15s, trebles, singles across all cards", sent with every morning pack).

Built from the course-method picks (reports/predictions/<date>/*_method.json) and the latest value
check. Rules (CLAUDE.md, owner 2026-09-23):
- WIN SINGLES = every BET pick (trial from 2 Oct: our evidence agrees AND the price is 2.00-2.99; odds-on never).
- EACH-WAY SINGLES = high-odds horses: our value picks at 12.00+ (15.00+ first) and STRONG longshots (15.00+,
  ranked in our top 3), best 5 by our chance x price.
- DOUBLE / TREBLE / LUCKY 15 / LUCKY 63 from the BET picks (strongest first; picks from different
  courses are combined freely). E/W LUCKY 15 / 63 from the each-way horses.
- FORECAST / REVERSE FORECAST: the 2 races where our 1st and 2nd are most likely to finish 1-2
  (Harville p1 x p2 / (1 - p1)); reverse when our 2nd's chance is close to our 1st's.
- STAKING: every bet costs £10 or as close as possible, never over; unit = floor(£10 / lines)
  to the penny, minimum 5p a line (so never more than 200 lines).

    python -m predict.betslip --date 2026-09-26 --check d-1_morning
"""
import argparse
import base64
import csv
from track_stats.parse import going_group
import functools
import json
import math
import re
import sys
from datetime import date as Date
from pathlib import Path

from form.history import days_since, name_key
from predict.cards import BET_LONGSHOTS, version_banner, CSS, e, pill, course_colour, course_on, colour_clashes, VERDICT_CSS, HIGH_CONF

REPO = Path(__file__).resolve().parent.parent
BUDGET_P = 1000  # £10 in pence
MIN_UNIT_P = 5
# owner 2026-10-02: "I don't want any each way bets under 11/1 ideally under 14/1 [=ideally 14/1+] but I'll let it
# slide on a few occasions" -> each-way minimum 12.00 (11/1); 15.00+ (14/1+) value picks go first
EW_MIN_PRICE = 12.0
EW_IDEAL_PRICE = 15.0
# owner 2026-10-02 ("Stop making excuses and get me results!!"): verified on his own slips 25 Sep-1 Oct, win singles
# -£75.20 (15/32) while doubles +£32.24, trebles +£44.50, E/W Lucky 15 +£22.50 -> win singles OFF the slip; the BET picks
# are still played, but only inside the double / treble / Lucky 15. Set True to bring singles back.
BET_WIN_SINGLES = False
# owner 2026-10-05 ("Yes"): single-only BET picks (never run on today's going / trip, or drifted 15%+) went 4/13 -£61.40 as
# win singles on his slips 28 Sep-4 Oct -> no win single for them; they stay on the course cards as BET picks only.
# (Replaces the 3 Oct So Regal rule that gave every single-only BET pick a win single.) Set True to bring them back.
SINGLE_ONLY_SINGLES = False
# owner 2026-10-08 ("If they pay yes"): 7/10+ win picks on the locked 09:30 packs 26 Sep-7 Oct (TEST) - not drifted 15%+ and
# priced 2.00+ won 45/87: £10 win +£168.10 at the 09:30 price, +£246.60 with Best Odds Guaranteed (26-30 Sep +£125.50,
# 1-7 Oct +£121.10 BOG); 1.50-1.99 picks 30/53 lost (-£14.50), drifted 3/10 -£26.50 -> left out. Win singles come back for
# these picks only (same legs as the multiples: 7/10+, not drifted, proven trip + going, one per race). TRIAL, judged nightly.
CONF_WIN_SINGLES = True
# owner 2026-10-19 ("pick the favourites when we think they are going to win but leave them out when we don't"; "find
# more winners"): locked 7/10+ picks 26 Sep-18 Oct that passed every slip rule but were priced UNDER 2.00 (so got no win
# single) won 33/50 (66%): £10 win +£45 at the 09:30 price, +£22 at SP, +£60 Best Odds Guaranteed, ahead in both halves
# (26 Sep-7 Oct 15/24 +£10 / 8-18 Oct 18/26 +£35 at the 09:30 price). History 2025-26 at SP: 7/10+ picks under 2.00
# -4% to -12% -> TRIAL from Tue 20 Oct, judged nightly (reports/research/2026-10-19_find_more_winners.md). Was 2.00.
# 22 Oct second opinion: ALL 7/10+ picks at 1.50-1.99 (26 Sep-21 Oct) 58/106 -£59.60 at the 09:30 price (H1 +£0.50, H2
# -£60.10); after the drift / maiden-novice jumps / 90-day rules 41/71 +£7.70 (-£14.80 / +£22.50) - weak either way.
# STOP RULE: back to 2.00 if the live trial singles under 2.00 (from 20 Oct) are losing at the 09:30 price after 30 bets.
CONF_SINGLE_MIN_PRICE = 2.0   # 5 Nov: the 20 Oct under-2.00 trial is closed (live 13/27 -£59 at 09:30; owner's 3 Nov rule = no single under 2.00)
# owner 2026-10-05 ("we need to start winning more ... work out how to win more"): live locked picks 25 Sep-5 Oct at SP -
# confidence 7+ and not drifted 69/127 (54%) +£14.70 at £10 v confidence 3-6 48/243 (20%); multiples from those legs:
# treble 4/10 +£21.98, Lucky 15 5/10 +£34.07, double 5/10 +£0.23 v BET-pick legs double 2/10 -£25.65, Lucky 15 2/8 -£31.84.
# -> the double / treble / Lucky 15 / 63 legs = our 7+ confidence win picks (any price, not drifted, proven), not the BET band.
# owner 1 Nov 2026 ("You've got no bet selections on there 7/10!!"): only 8/10+ (BET-tagged) win picks go on the slip -
# singles, doubles, trebles, Lucky 15/63 and accumulators. Was 7.
MULTI_MIN_CONF = 8
DRIFT_MIN = 1.10   # price up 10%+ since first priced = drifting -> off every bet (owner 29 Oct "whatever you think best";
                   # Sky 09:30 favourite picks drifted 10%+ 1-28 Oct won 13/90 -£451 at £10, both halves; was 1.15)
ACC_MIN_CONF = 8   # 8+ from 1 Nov (owner: no NO BET horse on the slip); was 7+ from 5 Oct (conf 6 picks won 29% live v 54% for 7+); accumulator legs (5-fold / Super Heinz): owner 3 Oct; 6+ so a normal card gives 5-7 legs
# owner 2026-09-28: longshots on the cards, but no 15.00+ horse on the slip while predict.cards.BET_LONGSHOTS is False
LONGSHOT_PRICE = 15.0
# owner 2026-09-30: "Let's remove the forecasts then for now" (forecasts -£80 over 25-29 Sep) - set True to bring them back
BET_FORECASTS = False
# review team plan A4 (owner 5 Nov 2026, his words relayed by the ZANS Review chat: "Make this happen along with all
# improvements"): no 5-fold. Locked race-day slips 25 Sep-4 Nov (recounted): 5-fold 4 bets, 0 won, -£40.00; the Super Heinz
# (same legs, pays on doubles up) stays. Forecasts and each-way singles were already off. Set True to bring the 5-fold back.
BET_FIVE_FOLD = False
# plan A9: every WIN bet (singles, doubles, trebles, Lucky 15/63, Super Heinz) carries this line; never the each-way bets
# (Sky Bet Club BOG may not apply in extra-place races). Owner is a Sky Bet Club member (22 Oct).
BOG_NOTE = "09:30 price, claim Best Odds Guaranteed"
# owner 2026-10-07 ("you do what's right"): verified on his counted slips 25 Sep-6 Oct, each-way singles 8/34 paid, -£83.75
# (win singles -£84.90, forecasts -£90, 5-fold -£30) while doubles +£51.38, trebles +£150.27, Lucky 15 +£79.85 -> each-way
# singles OFF the slip; the value horses stay on the cards, in the Value Predictions and in the BET NOW emails, and are
# still tracked. Set True to bring them back.
BET_EW_SINGLES = False
# owner 10 Oct ("one horse let us down on all the bets ... It's ok the same horse in a few bets but not in all of them"):
# Desert Castle (beaten 0.3L) was in 4 of the 6 doubles/trebles on the final slip. The all-must-win bets (doubles, trebles,
# 5-fold) never share a horse with the first double: double = picks 1+2, treble = picks 3+4+5 (only 4 picks -> a second
# double 3+4; only 3 -> no treble). The Lucky 15 / 63 / Super Heinz pay on singles and smaller combinations, so one loser
# there loses only its own lines. TEST (locked 7/10+ picks 26 Sep-10 Oct, double + treble + Lucky 15, £10 each, SP-free
# morning prices): top-3 treble +£205.23 (one horse sank the double AND treble on 6 of 15 days) v spread treble +£443.80
# (0 days), 10 v 9 winning days, ahead in both halves - the extra profit is mostly which trebles happened to land.
SPREAD_MULTIPLES = True
# OWNER DECISION 3 Nov 2026 (his words, relayed by the ZANS Review chat: "Having stupid low bets on our slip is pointless! We
# need structural value!", "Mixtures of high middle and low predictions. That's what we need!!!!", "Just do a mixture and get
# this working!!!!!!!"; his decision-card answer: PRICE MIX). TRIAL from Wed 4 Nov, judged at 30 days, old 8/10+ slip kept as a
# background record (predict.shadow7 --mode old8). Re-checked here on OUR safety rules (betslip._gap + 10% drift), locked
# race-day picks 26 Sep-2 Nov, £10 at the 09:30 price (TEST - the rules were chosen after seeing these days):
#   win singles 7/10+ priced 2.00+ 58/117 +£172.40 (26 Sep-14 Oct +109.70 | 15 Oct-2 Nov +62.70), BOG +£240.30;
#   7/10+ under 2.00 45/75 -£14.70 (+13.40 | -28.10) -> no single under 2.00; old 8/10+ singles 68/117 +£50.40 (+69.20 | -18.80);
#   PRICE-MIX treble (best value = chance x price in each band <2.00 / 2.00-3.49 / 3.50+, 5/10+, safe) +£304.65 (+113.62 |
#   +191.03), BOG +£485.37; double of the short + middle legs +£134.80 (+69.30 | +65.50); Lucky 15 of the 2.00+ singles by value
#   +£79.76 (+75.39 | +4.37). Scripts /tmp/claude-0/pmix/check.py, multi.py, var.py (copied to reports/research/scripts/pricemix_2026-11-03/).
#   Kept at 8/10+ the price mix is all short (replay 3 Nov: 1.73 / 1.73 / 1.62; 1 Nov: 1.67 / 1.62 / 1.67) = exactly the "stupid
#   low bets" the owner objected to, so the team's floors are used: singles 7/10+, price-mix legs 5/10+. Those legs are NOT
#   tagged BET / NO BET on the slip (his 1 Nov tag rule stays on the cards): they carry an amber 'N/10 PRICE MIX' box. 8/10+
#   alternative tested the same way: singles 2.00+ 23/43 +£55.10 (+45.80 | +9.30); treble +£191.49 (+134.15 | +57.34).
PRICE_MIX_TRIAL = True
SINGLE_MIN_CONF = 7          # win singles: SINGLE_MIN_CONF+ priced PRICE_MIX_SINGLE_MIN+ (trial)
PRICE_MIX_SINGLE_MIN = 2.0   # no win single under 2.00 whatever the confidence (trial)
MIX_MIN_CONF = 5             # price-mix legs on the slip: safe 5/10+ win picks (team proposal, owner's PRICE MIX choice)
HEADLINE_MIN_CONF = 5        # headline TOP 3 (video / social, not a bet on the slip): every safe 5/10+ win pick
LAST_HEADLINE = []
MIX_BANDS = ((0.0, 2.0, "SHORT"), (2.0, 3.5, "MIDDLE"), (3.5, 1000.0, "BIGGER"))
LAST_MIX = []


def price_mix(cands):
    """Best value (chance x price) in each price band; an empty band is filled by the next-best value pick from the others."""
    def val(s):
        return (s["chance"] or 0) * (s["price"] or 0)
    top = []
    for lo, hi, band in MIX_BANDS:
        b = sorted((s for s in cands if lo <= (s["price"] or 0) < hi), key=lambda s: -val(s))
        if b:
            top.append(dict(b[0], band=band))
    taken = {(s["course"], s["time"]) for s in top}
    rest = sorted((s for s in cands if (s["course"], s["time"]) not in taken), key=lambda s: -val(s))
    top += [dict(s, band="FILL (empty band)") for s in rest[:3 - len(top)]]
    return top


def spread_problems(slip):
    """Horses that are in EVERY all-must-win bet (doubles, trebles, N-folds) when there are 2+ of them - must be empty."""
    allwin = [b for b in slip if (b["name"] in ("Double", "Treble") or b["name"].endswith("-fold"))
              and not (b.get("note") or "").startswith("PRICE MIX double")]   # owner 3 Nov: double = 2 legs of the treble
    if len(allwin) < 2:
        return []
    sets = [{(l["course"], l["time"], l["horse"]) for l in b["legs"]} for b in allwin]
    return sorted(h for _, _, h in set.intersection(*sets))


CHECKS = ("d0_midday", "d0_morning", "d-1_morning", "d-1_evening", "d-2_morning", "d-2_evening")


def unit_stake(lines):
    """Unit stake in pence for a bet with this many lines, or None if 5p a line would break £10."""
    unit = BUDGET_P // lines
    return unit if unit >= MIN_UNIT_P else None


def money(p):
    return f"£{p // 100}.{p % 100:02d}"


def dec(price):
    try:
        v = float(price)
        return v if v > 1 else None
    except (TypeError, ValueError):
        return None


def parse_second(text):
    """'The Flying Rambler 67.00 (12%)' -> ('The Flying Rambler', 67.0, 0.12)."""
    m = re.match(r"(.+?)\s+([\d.]+|-)?\s*\((\d+)%\)", text or "")
    if not m:
        return None
    return m.group(1).strip(), dec(m.group(2)), int(m.group(3)) / 100


from predict.bet_tag import tag, tag_html, header_count, colour  # noqa: E402


LAST_TREBLE = []


def slip_conf_problems(picks, slip):
    """Owner 1 Nov 2026: no horse rated 7/10 or lower (a NO BET) may be in any bet on the slip."""
    conf = {(p["course"].lower(), p["time"], name_key(p["win"])): int(p.get("confidence") or 0) for p in picks}
    bad = []
    for b in slip:
        for l in b.get("legs", []):
            c = conf.get(((l.get("course") or "").lower(), l.get("time"), name_key(l.get("horse") or "")))
            m = re.match(r"(\d+)/10", l.get("why") or "")
            c = int(m.group(1)) if m else c
            # owner 3 Nov price-mix trial: price-mix legs (double / treble marked PRICE MIX) may be MIX_MIN_CONF+, every
            # other bet SINGLE_MIN_CONF+; before it, every leg MULTI_MIN_CONF+ (owner 1 Nov)
            need = ((MIX_MIN_CONF if (b.get("note") or "").startswith("PRICE MIX") else SINGLE_MIN_CONF)
                    if PRICE_MIX_TRIAL else MULTI_MIN_CONF)
            if c is not None and c < need:
                bad.append(f"{b['name']}: {l.get('time')} {l.get('horse')} is {c}/10 (below {need}/10 for this bet)")
    return bad


def load_picks(race_date):
    picks = []
    for f in sorted((REPO / "reports" / "predictions" / race_date).glob("*_method.json")):
        course = f.name.replace("_method.json", "").replace("_", " ").title()
        for r in json.loads(f.read_text()):
            picks.append({**r, "course": course})
    return picks


def load_value(race_date, check):
    """Value rows from the requested check, else the newest check available."""
    from odds.value_report import build as value_build
    for c in [check] + [c for c in CHECKS if c != check]:
        if (REPO / "reports" / "odds" / race_date / f"watchlist_{c}.json").exists():
            try:
                return value_build(race_date, c)[1:]
            except FileNotFoundError:
                continue
    return [], []


def sel(course, time, horse, price, chance, why):
    return {"course": course, "time": time, "horse": horse, "price": price, "chance": chance, "why": why}


def bookie_price(race_date, check, x):
    """The each-way price the owner can actually take: Sky Bet's own price (any bookmaker only if Sky Bet is missing),
    from this check's price file. None when no bookmaker has priced the horse yet.
    23 Oct (bet guard): two legs of the E/W Lucky 15 carried a Sporting Life quote with no bookmaker price
    (Gonna Be Golden 26.00, Friendly Invoice 21.00 - Sky Bet was 17.00). Sporting Life also listed a duplicate copy of
    the Dundalk 17:15 race at 17:10 that held the real bookmaker prices -> the same horse at the same course in
    another copy of the race counts."""
    import csv
    from predict.bet_now import best_places, parse_terms
    path = REPO / "reports" / "odds" / race_date / f"{check}.csv"
    if not path.exists():
        return None
    rows = list(csv.DictReader(path.open()))
    hid, name, course = str(x.get("sl_horse_id") or ""), name_key(x["horse"]), str(x.get("course") or "").lower()
    same = [r for r in rows if (hid and r.get("sl_horse_id") == hid)
            or (name_key(r.get("horse") or "") == name and (r.get("course") or "").lower() == course)]
    # a horse double-declared at the same meeting (Irish cards) must not take the other race's price: only rows within
    # 10 minutes of this race's off time count (review chat, 23 Oct)
    def mins(t):
        try:
            h, m = str(t).split(":")[:2]
            return int(h) * 60 + int(m)
        except ValueError:
            return None
    off = mins(x.get("off_time"))
    near = [r for r in same if off is not None and mins(r.get("off_time")) is not None
            and abs(mins(r.get("off_time")) - off) <= 10]
    for r in (near if off is not None else same):   # a copy of another race (more than 10 minutes away) never counts
        best = best_places(parse_terms(r.get("bookie_terms")))
        if best and best.get("dec"):
            return best
    return None


_EV = {}


def evidence_chance(race_date, course, time, horse):
    """Our evidence-only chance (no price) for a runner, from predictions.json."""
    if race_date not in _EV:
        path = REPO / "reports" / "predictions" / race_date / "predictions.json"
        idx = {}
        if path.exists():
            for r in json.loads(path.read_text()):
                for a in r["all"]:
                    idx[(r["course"].lower(), r["off_time"], a["name"].lower())] = a.get("form_chance", a["chance"])
        _EV[race_date] = idx
    return _EV[race_date].get((course.lower(), time, horse.lower()), 0)


def one_per_race(sels):
    """A multiple can't hold two horses from the same race: keep the first (strongest) per race."""
    out, races = [], set()
    for s in sels:
        key = (s["course"].lower(), s["time"])
        if key not in races:
            races.add(key)
            out.append(s)
    return out


@functools.lru_cache(maxsize=8)
def _card_stats(race_date):
    from predict.review import card_stats
    return card_stats(race_date)


def unproven(race_date, horse):
    """Why a horse is unproven for today's conditions ('' if proven): never run on today's going or over
    today's trip, from the racecard's horse stats (wins/runs)."""
    stats = _card_stats(race_date).get(name_key(horse))
    if not stats:
        return "no form record"
    gaps = [label for key, label in (("going", "never run on this going"), ("distance", "never run at this trip"))
            if stats.get(key, "0/0").endswith("/0")]
    return ", ".join(gaps)


def overseas_picks(race_date):
    """Owner 4 Oct ("a combined bet slip please with Paris in on it as well"): overseas picks from
    reports/overseas/<date>/selections.json as card-style picks + their value each-way horses. Proven / moved come
    from the overseas card itself (our UK/IRE racecard stats don't hold these horses)."""
    path = REPO / "reports" / "overseas" / race_date / "selections.json"
    if not path.exists():
        return [], []
    d = json.loads(path.read_text())
    course = "Paris" if "longchamp" in d.get("course", "").lower() else d.get("course", "Overseas")
    first = {}   # earliest overseas check's prices -> move (backed / drifted)
    for f in sorted(path.parent.glob("d-*_*.csv")) + sorted(path.parent.glob("d0_*.csv")):
        for r in csv.DictReader(f.open()):
            key = (r.get("off_time"), r.get("horse", "").split(" (")[0].lower())
            pr = r.get("best_dec") or r.get("sl_dec")
            if key not in first and pr and float(pr) > 1:
                first[key] = float(pr)
    picks, ew = [], []
    for r in d["races"]:
        if not r.get("win_price"):
            continue
        w = next(x for x in r["field"] if x["horse"] == r["win"])
        gaps = [lab for k, lab in (("going_r", "never run on this going"), ("dist_r", "never run at this trip")) if not w.get(k)]
        f0 = first.get((r["time"], r["win"].lower()))
        move = f"{f0:.2f} -> {r['win_price']:.2f}" if f0 and abs(f0 - r["win_price"]) > 0.001 else ""
        picks.append({"course": course, "time": r["time"], "win": r["win"], "price": f"{r['win_price']:.2f}",
                      "chance": r["chance"], "confidence": r["confidence"], "verdict": r["verdict"],
                      "evidence_agrees": r["evidence_agrees"], "move": move, "unproven": ", ".join(gaps),
                      "runners": r["runners"], "longshot": ""})
        for v in r.get("value", []):
            if v["price"] and v["price"] >= EW_MIN_PRICE:
                ew.append(sel(course, r["time"], v["horse"], v["price"], v.get("evidence") or 0,
                              f"value pick, E/W {v.get('fraction') or ''} odds, {v['places']} places"
                              + (" (EXTRA)" if v.get("extra") else "") + f", {v.get('bookie') or ''}"))
    return picks, ew


# owner 2026-10-09 ("We have to be careful on horses that haven't ran for 3 months plus! ... keep them off the bet slip"):
# locked 09:30 picks 26 Sep-8 Oct, 7/10+ off 90+ days 10/22 -£23.80 at £10 v under 90 days 74/136 +£149.20 -> any horse off
# LAYOFF_DAYS or more (racecard days since last run) is kept off every bet on the slip; it stays a pick on its course card.
LAYOFF_DAYS = 90


@functools.lru_cache(maxsize=8)
def _days_off(race_date):
    out = {}
    path = REPO / "reports" / "racecards" / race_date / "racecards.json"
    if path.exists():
        for race in json.loads(path.read_text()):
            for r in race.get("runners", []):
                if days_since(r.get("last_run")) is not None:
                    out[name_key(r["name"])] = days_since(r.get("last_run"))
    return out


def layoff(race_date, horse):
    """'off N days' if the horse has been off LAYOFF_DAYS+ days, else ''."""
    days = _days_off(race_date).get(name_key(horse))
    return f"off {days} days" if days is not None and days >= LAYOFF_DAYS else ""


# owner 2026-10-09 (Young Doran, 2.00 maiden hurdler, after Sytadel on 4 Oct): locked 09:30 7/10+ picks 26 Sep-8 Oct in maiden /
# novice / beginners' / bumper JUMPS races won 17/39 (44%) -£76.70 at £10 v all other races 75/133 (56%) +£225.40 -> those
# races are kept off EVERY bet on the slip (was: only moved to the back of the multiples order). Stays a pick on its card.
MAIDEN_JUMPS_OFF = True
# owner 10 Oct: "Keep the treble and lucky 15s. I also want a high odds lucky 15" -> every slip gets an each-way Lucky 15 of
# 4 value horses (12.00+) when 4 qualify; drifted value horses fill the gaps (TRIAL - judged nightly in the Bet Slip Review)
HIGH_ODDS_L15 = True


def maiden_novice_jumps(race):
    return bool(re.search(r"maiden|novice|beginner|bumper|nh flat|national hunt flat", race or "", re.I)
                and re.search(r"hurdle|chase|bumper|nh flat|national hunt", race or "", re.I))


# owner 10 Oct ("Absolutely shit at Southwell!!! This must improve"): segments where our win picks lose money in our history
# (out of sample, 2025 AND 2026) and live -> kept off EVERY bet, still picked on the card.
#  - Southwell ALL-WEATHER HANDICAPS: live locked picks 26 Sep-10 Oct 8/32 incl. the 10 Oct 20:30 (-£77.50 at £10, 09:30 price; non-handicaps 4/10
#    -£0.80); history 632 races won 28.5% v 30.5% predicted, -18% at SP v -6% at other AW tracks (2025 -21% v -5%, 2026 -13% v
#    -9%), class 6 -20% v -2%.
#  - Fairyhouse JUMPS NON-HANDICAPS: history 164 races won 31.1% v 35.4% predicted, -23% v -9% (2025 -16%, 2026 -36%).
COURSE_OFF = [("southwell", "AW", True, "Southwell all-weather handicap"),
              ("fairyhouse", "JUMPS", False, "Fairyhouse jumps non-handicap")]


def course_off(p):
    """Reason text if this pick's race is in a COURSE_OFF segment, else ''."""
    c = str(p.get("course") or "").lower()
    code = "AW" if going_group(p.get("going") or "") == "STANDARD" else (
        "JUMPS" if re.search(r"hurdle|chase|bumper|nh flat|national hunt", p.get("race") or "", re.I) else "FLAT")
    for course, want, hcap, why in COURSE_OFF:
        if c.startswith(course) and code == want and bool(p.get("handicap")) == hcap:
            return why
    return ""


# 29 Oct (Ffos Las forecast 2.63 legs on the slip): a race with no bookmaker price at ANY check keeps its win pick on the card
# (FORECAST label) but stays off every bet. Relayed as the owner's choice by the Review chat - ON only once he confirms it here.
UNPRICED_OFF = True   # owner 29 Oct: "Whatever you thinks best just make it better" (the Review-chat choice confirmed)


def _gap(race_date, p, horse):
    gap = p["unproven"] if "unproven" in p else unproven(race_date, horse)
    gap = ", ".join(x for x in (gap, course_off(p)) if x)
    if MAIDEN_JUMPS_OFF and maiden_novice_jumps(p.get("race")):
        gap = ", ".join(x for x in (gap, "maiden/novice jumps race") if x)
    # owner 5 Oct (Lady Branksome): first time on the ALL-WEATHER is not a weakness - UK/IRE AW 2023-26 first-timers
    # A/E 1.03-1.04 (8,424), favourites 1.08-1.10, v 1.00 for horses with AW form -> 'never run on this going' doesn't
    # count on a standard (all-weather) surface; the trip check still does
    if gap and going_group(p.get("going") or "") == "STANDARD":
        gap = ", ".join(g for g in gap.split(", ") if g != "never run on this going")
    # owner stance "keep what works" (11 Oct, 0-bet slip): on the FLAT, 'never run on this going' alone is not a weakness -
    # live locked 7/10+ flat turf picks 26 Sep-10 Oct: never on the going but proven at the trip 19/29 (66%) +£67.90 at £10
    # v proven on the going 13/23 +£42.20; unproven on BOTH going and trip 7/17 -£38.90 (still blocked). National history:
    # flat first time on soft A/E 1.09. Jumps keep the going check (jumps never on soft/heavy A/E 0.86).
    elif gap and "never run at this trip" not in gap and not re.search(r"hurdle|chase|bumper|nh flat|national hunt", p.get("race") or "", re.I):
        gap = ", ".join(g for g in gap.split(", ") if g != "never run on this going")
    off = layoff(race_date, horse)
    # owner 10 Oct: a pick whose latest run is missing from our data (coverage BEHIND / MISSING) stays off every bet
    dg = "latest run missing from our data" if p.get("data_gap") else ""
    if UNPRICED_OFF:
        from predict.cards import is_unpriced
        if is_unpriced(race_date, p.get("course"), p.get("time")):
            dg = ", ".join(x for x in (dg, "no bookmaker price - kept off the slip") if x)
    return ", ".join(x for x in (gap, off, dg) if x)


# 24 Oct TRIAL (review team, owner delegated rule decisions to them that day: "You decide"; Doncaster HEAVY - 3 of the 4 Lucky 15
# legs were Doncaster flat picks, 2 of them never on soft/heavy): (1) on HEAVY ground (main going 'soft to heavy' or 'heavy') a FLAT
# pick that has never run on soft or softer ground in our history keeps its win single but stays OUT of every multiple; (2) no
# treble / Lucky 15 / Lucky 63 / 5-fold takes more than 2 legs from one HEAVY meeting. History (ALL UK/IRE flat turf, main going
# HEAVY, 1,594 races, margin-free SP A/E, 2019-21 | 2022-26; reports/research/scripts/heavy_2026-10-24/): never ran on soft/heavy
# 1.02 (3,701 runners; 1.06 | 0.99), at SP under 4.0 1.03 (427; 0.96 | 1.07) = NO edge either way - a SAFETY rule, not an edge
# claim. STOP RULE (review chat 24 Oct): every kept-out leg is logged (predict/heavy_tracker.py, nightly in slip_review); after 30
# kept-out legs, the rule is dropped if they win at least as often as the heavy-meeting legs kept in (09:30 price).
HEAVY_SAFETY = True
HEAVY_MAX_LEGS = 2


def heavy_going(going):
    from predict.ground_check import softness
    return (softness(going) or 0) >= 5.5


@functools.lru_cache(maxsize=4)
def _soft_record(race_date, horses):
    from predict.ground_check import ground_record
    return ground_record(set(horses), True, 5, race_date)


def heavy_untried(race_date, p, horse, flat_horses):
    """'' unless the pick is a flat runner on HEAVY ground with no soft-or-softer run in our history."""
    if not HEAVY_SAFETY or not heavy_going(p.get("going")) or going_group(p.get("going") or "") == "STANDARD":
        return ""
    if re.search(r"hurdle|chase|bumper|nh flat|national hunt", p.get("race") or "", re.I):
        return ""
    rec = _soft_record(race_date, tuple(sorted(flat_horses))).get(name_key(horse), [0, 0, 0])
    return "" if rec[0] else "never run on soft or heavy - heavy ground today"


def cap_heavy(pool, n, heavy_courses):
    """Up to n legs in order, never more than HEAVY_MAX_LEGS from one meeting on HEAVY ground."""
    out, count = [], {}
    for s in pool:
        c = s["course"].lower()
        if HEAVY_SAFETY and c in heavy_courses and count.get(c, 0) >= HEAVY_MAX_LEGS:
            continue
        out.append(s)
        count[c] = count.get(c, 0) + 1
        if len(out) == n:
            break
    return out


def owner_excluded(race_date):
    p = REPO / "config" / "slip_exclude.json"
    if not p.exists():
        return set()
    out = set()
    for item in json.loads(p.read_text()).get(race_date, []):
        course, _, time = item.rpartition(" ")
        out.add((course.strip().lower(), time.strip()))
    return out


# review team 6 Nov (verified): the slip quoted the best price of 3 bookmakers, but the owner bets only with Sky Bet
# (2 Oct rule) -> every win-pick leg now carries the Sky Bet price from the same check (best price kept as best_price);
# the price-mix bands, value order, singles floor and settlement all use what he can actually back.
SKY_PRICES = True


def sky_prices(race_date, check, picks):
    """Swap each pick's price for the Sky Bet price in this check's file (unchanged when Sky Bet has no price)."""
    if not SKY_PRICES:
        return picks
    from predict.team_trials import _sky
    from track_stats.parse import course_key
    sky = _sky(race_date, check)
    if not sky:
        return picks
    for p in picks:
        k = (course_key(p.get("course") or "")[0], str(p.get("time") or "")[:5], name_key(p.get("win") or ""))
        d = sky.get(k)
        if d and dec(p.get("price")):
            p["best_price"], p["price"], p["price_source"] = p["price"], f"{d:.2f}", "Sky Bet"
    return picks


def build_bets(race_date, check, after="", overseas=False):
    picks = sky_prices(race_date, check, [p for p in load_picks(race_date) if p["time"] > after])
    value_rows, value_best = load_value(race_date, check)
    os_picks, os_ew = overseas_picks(race_date) if overseas else ([], [])
    picks += [p for p in os_picks if p["time"] > after]

    bets_sel = [dict(sel(p["course"], p["time"], p["win"], dec(p["price"]), p.get("chance") or 0,
                         f"{p['confidence']}/10 confidence"), **({"unproven": p["unproven"]} if "unproven" in p else {}))
                for p in picks if p["verdict"] == "BET"]
    bets_sel.sort(key=lambda s: (-int(s["why"].split("/")[0]), -s["chance"]))
    bets_sel = one_per_race(bets_sel)
    # owner 2026-09-29 ("you can't make mistakes", after Cyberspace - never on soft - sank Monday's double and
    # treble): a BET pick that has never run on today's going or over today's trip stays a single, but is kept
    # OUT of every multiple, so one unproven horse can't take the whole slip down with it.
    for s in bets_sel:
        gap = _gap(race_date, s, s["horse"])
        if gap:
            s["why"] += f" - single only, not in multiples ({gap})"
    # owner 2026-10-02 ("we need to get more single, double and treble winners"): our records show drifting win picks
    # win 3 of 41 (7%) v backed-in picks 45 of 156 (29%) -> a BET pick whose price has drifted since it was first
    # priced stays a single and is kept out of the multiples; backed-in picks go first in the multiples
    moves = {(p["course"], p["time"]): p.get("move") or "" for p in picks}
    warn = {(p["course"], p["time"]): p.get("drift_warning") for p in picks}
    for s in bets_sel:
        m = re.match(r"([\d.]+) -> ([\d.]+)", moves.get((s["course"], s["time"]), ""))
        # owner 3 Oct ("Why didn't you put So Regal on the bet??!"): a 2.00 -> 2.10 move is noise, not a drift - only a
        # rise of DRIFT_MIN (10%) or more counts as drifting
        if m and float(m.group(2)) >= float(m.group(1)) * DRIFT_MIN and "single only" not in s["why"]:
            s["why"] += f" - single only, not in multiples (drifted {m.group(1)} -> {m.group(2)})"
        elif warn.get((s["course"], s["time"])) and "single only" not in s["why"]:
            s["why"] += " - single only, not in multiples (drifted overnight)"
        s["backed"] = bool(m and float(m.group(2)) < float(m.group(1)))
    # owner 4 Oct (Sytadel, a maiden hurdler, led the double, treble, Lucky 15, 5-fold and Super Heinz and "lost by a mile"):
    # picks in maiden / novice / beginners' / bumper JUMPS races never lead the double and treble (BET picks in those races
    # 2/6 v other races 18/36, 26 Sep-3 Oct) - they go to the back of the order (still in the Lucky 15 / 63 if needed)
    races = {(p["course"], p["time"]): p.get("race") or "" for p in picks}
    def maiden_jumps(s):
        r = races.get((s["course"], s["time"]), "")
        return bool(re.search(r"maiden|novice|beginner|bumper|nh flat", r, re.I) and re.search(r"hurdle|chase|bumper|nh flat", r, re.I))
    heavy_flat = [name_key(p["win"]) for p in picks if heavy_going(p.get("going"))]
    heavy_courses = {p["course"].lower() for p in picks if heavy_going(p.get("going"))}
    strong = []
    floor = min(MIX_MIN_CONF, HEADLINE_MIN_CONF) if PRICE_MIX_TRIAL else MULTI_MIN_CONF
    for p in picks:
        if int(p.get("confidence") or 0) < floor or not dec(p["price"]):
            continue
        m = re.match(r"([\d.]+) -> ([\d.]+)", p.get("move") or "")
        # 13 Oct (Royal County Glory 1.62 -> 1.91 overnight, card said 'kept out of the multiples' but it was in the treble):
        # the card's overnight drift warning (course_method DRIFT_WARN) counts as drifting too
        if (m and float(m.group(2)) >= float(m.group(1)) * DRIFT_MIN) or p.get("drift_warning") or _gap(race_date, p, p["win"]):
            continue
        a = sel(p["course"], p["time"], p["win"], dec(p["price"]), p.get("chance") or 0, f"{p['confidence']}/10 confidence")
        a["backed"] = bool(m and float(m.group(2)) < float(m.group(1)))
        a["heavy"] = heavy_untried(race_date, p, p["win"], heavy_flat)
        strong.append(a)
    strong = one_per_race(strong)
    strong = [s for s in strong if (s["course"].lower(), s["time"]) not in owner_excluded(race_date)]
    global LAST_TREBLE, LAST_MIX, LAST_HEADLINE
    LAST_MIX, LAST_HEADLINE = [], []
    conf_of = lambda s: int(s["why"].split("/")[0])
    if PRICE_MIX_TRIAL:
        # owner 3 Nov: price-mix top 3 (short / middle / bigger, best value in each band) -> the double (short + middle) and
        # the treble (all three) from the MIX_MIN_CONF+ safe picks; the headline TOP 3 from every safe HEADLINE_MIN_CONF+ pick
        LAST_HEADLINE = [dict(s) for s in price_mix([s for s in strong if not s.get("heavy") and conf_of(s) >= HEADLINE_MIN_CONF])]
        LAST_MIX = price_mix([s for s in strong if not s.get("heavy") and conf_of(s) >= MIX_MIN_CONF])
        for s in LAST_MIX:
            s["why"] = f"{s['why']} - PRICE MIX {s['band'].lower()} leg (best value in its price band)"
        # singles + Lucky 15/63: 7/10+ picks priced 2.00+ only, ranked by value
        strong = [s for s in strong if conf_of(s) >= SINGLE_MIN_CONF and (s["price"] or 0) >= PRICE_MIX_SINGLE_MIN]
        multi_sel = sorted((s for s in strong if not s.get("heavy")),
                           key=lambda s: (maiden_jumps(s), -(s["chance"] or 0) * (s["price"] or 0)))
        LAST_TREBLE = [dict(s) for s in LAST_MIX] if len(LAST_MIX) == 3 else []
    else:
        multi_sel = sorted((s for s in strong if not s.get("heavy")),
                           key=lambda s: (maiden_jumps(s), -int(s["why"].split("/")[0]), not s.get("backed"), -s["chance"]))
        # owner 1 Nov ("I only want to give trebles for a start"): the public treble = our 3 strongest 8/10+ legs that pass
        # every slip rule (saved as <out>_treble.json by main for the video / social posts; the daily slip is unchanged)
        LAST_TREBLE = [dict(s) for s in multi_sel[:3]] if len(multi_sel) >= 3 else []
    for s in strong:
        if s.get("heavy"):
            s["why"] += f" - single only, not in multiples ({s['heavy']})"

    # owner 2026-10-03 (after winning a 5-fold at 62.43, a treble and a Super Heinz on our win picks: "these are the kind of
    # bets that we should be doing along with your bets"): ACCUMULATORS from our strongest win picks at ANY price -
    # evidence agrees, MULTI_MIN_CONF+ (8/10+ from 1 Nov) confidence, not drifted, proven at the trip and on the going; one per race
    acc_sel = []
    for p in picks:
        if not p.get("evidence_agrees") or int(p.get("confidence") or 0) < ACC_MIN_CONF or not dec(p["price"]):
            continue
        m = re.match(r"([\d.]+) -> ([\d.]+)", p.get("move") or "")
        # 13 Oct (Royal County Glory 1.62 -> 1.91 overnight, card said 'kept out of the multiples' but it was in the treble):
        # the card's overnight drift warning (course_method DRIFT_WARN) counts as drifting too
        if (m and float(m.group(2)) >= float(m.group(1)) * DRIFT_MIN) or p.get("drift_warning") or _gap(race_date, p, p["win"]):
            continue
        if heavy_untried(race_date, p, p["win"], heavy_flat):
            continue
        a = sel(p["course"], p["time"], p["win"], dec(p["price"]), p.get("chance") or 0, f"{p['confidence']}/10 confidence")
        a["backed"] = bool(m and float(m.group(2)) < float(m.group(1)))
        acc_sel.append(a)
    # 15 Oct: races ruled out for the day (config/slip_exclude.json) are out of the accumulators too (they were only
    # taken out of the singles/multiples and each-ways before)
    acc_sel = [s for s in acc_sel if (s["course"].lower(), s["time"]) not in owner_excluded(race_date)]
    acc_sel = sorted(one_per_race(acc_sel), key=lambda s: (-int(s["why"].split("/")[0]), -s["chance"]))
    # owner 4 Oct: one horse must not sink every all-must-win bet - a horse in the double AND treble stays out of the 5-fold
    # (it may still be in the Super Heinz, where one loser only loses its own lines)
    lead = {(s["course"], s["time"]) for s in multi_sel[:2]} if len(multi_sel) >= 2 else set()  # any double (5 Oct)
    if PRICE_MIX_TRIAL:
        lead = {(s["course"], s["time"]) for s in LAST_MIX[:2]} if len(LAST_MIX) >= 2 else set()
    fold_sel = [s for s in acc_sel if (s["course"], s["time"]) not in lead]

    ew, ew_fill, seen = [], [], set()
    race_info = {(p["course"].lower(), p["time"]): p for p in picks}
    for r in value_rows:
        x = r["x"]
        if x["off_time"] <= after:
            continue
        bp = bookie_price(race_date, check, x)
        if not bp or bp["dec"] < EW_MIN_PRICE:   # no bookmaker price yet = can't be bet (23 Oct)
            continue
        if layoff(race_date, x["horse"]):   # owner 9 Oct: no horse off 90+ days on the slip
            continue
        if MAIDEN_JUMPS_OFF and maiden_novice_jumps(x.get("race")):   # owner 9 Oct: no maiden/novice jumps horse on the slip
            continue
        # 7 Nov (bet guard: Teardrops, Southwell AW handicap, got onto the E/W Lucky 15): the COURSE_OFF segments are "kept off
        # EVERY bet" - the race's going / handicap flag come from our win pick in the same race
        race_p = race_info.get((x["course"].lower(), x["off_time"]))
        if race_p and course_off(race_p):
            continue
        # value picks that passed every value check may be 15.00+ (owner wants big each-way prices); the card's
        # LONGSHOT column (ranked-only, no value check) stays off the slip while BET_LONGSHOTS is False
        key = (x["course"].lower(), x["off_time"], x["horse"].lower())
        seen.add(key)
        s_ = sel(x["course"], x["off_time"], x["horse"], bp["dec"], r["a"]["chance"],
                 "value pick" + (" (our best)" if r in value_best else "")
                 + f", {bp['bookie']} {bp['places']} places")
        # owner 10 Oct ("I also want a high odds lucky 15"): a value horse whose price has drifted since it was flagged is
        # only used to FILL the high-odds Lucky 15 when fewer than 4 steady / backed value horses are left
        (ew_fill if r["kind"] == "drifting" else ew).append(s_)
    for p in picks:
        ls = p.get("longshot") or ""
        if not BET_LONGSHOTS or "STRONG" not in ls:
            continue
        m = re.match(r"(.+?)\s+([\d.]+)\s+STRONG", ls)
        if not m:
            continue
        key = (p["course"].lower(), p["time"], m.group(1).lower())
        if key in seen:
            continue
        seen.add(key)
        rank = re.search(r"ranked (\w+)", ls)
        chance = evidence_chance(race_date, p["course"], p["time"], m.group(1))
        ew.append(sel(p["course"], p["time"], m.group(1), float(m.group(2)), chance,
                      f"strong longshot (ranked {rank.group(1) if rank else 'top 3'} by us)"))
    # value picks (passed every value check) first, then strong longshots; best chance x price within each
    ew.sort(key=lambda s: (not s["why"].startswith("value pick"), (s["price"] or 0) < EW_IDEAL_PRICE,
                           -(s["chance"] or 0) * (s["price"] or 0)))
    # owner rules for the day: races he has ruled out (config/slip_exclude.json), and never an each-way leg in a race where
    # a win pick of ours is already on the slip (10 Oct: Bowood each-way against our own Calm The Jets)
    excl = owner_excluded(race_date)
    win_races = {(s["course"].lower(), s["time"]) for s in strong}
    ew = [s for s in ew if (s["course"].lower(), s["time"]) not in excl | win_races]
    ew_fill = [s for s in ew_fill if (s["course"].lower(), s["time"]) not in excl | win_races]
    ew = one_per_race(ew)[:5]
    if len(ew) < 4 and HIGH_ODDS_L15:
        taken = {(s["course"], s["time"]) for s in ew}
        fill = sorted((s for s in ew_fill if (s["course"], s["time"]) not in taken),
                      key=lambda s: ((s["price"] or 0) < EW_IDEAL_PRICE, -(s["chance"] or 0) * (s["price"] or 0)))
        ew += [dict(s, why=s["why"] + " (price drifted since flagged)") for s in one_per_race(fill)][:4 - len(ew)]
    # overseas each-way picks go AFTER our own (never push a UK/IRE value bet off the slip), best chance x price first
    os_ew = sorted((x for x in os_ew if x["time"] > after), key=lambda s: -(s["chance"] or 0) * (s["price"] or 0))
    ew += one_per_race(os_ew)[:5]

    slip = []

    def add(section, name, legs, lines, note="", odds=None):
        unit = unit_stake(lines)
        if unit is None:
            return
        if section in ("Multiples", "Accumulators") and not name.startswith("Each-way") and BOG_NOTE not in note:
            note = f"{note} - {BOG_NOTE}" if note else BOG_NOTE   # plan A9: every win bet, never the each-way ones
        slip.append({"section": section, "name": name, "legs": legs, "lines": lines, "unit": unit,
                     "total": unit * lines, "note": note, "odds": odds})

    # a BET pick must never drop off the slip altogether (So Regal, 3 Oct: kept out of the multiples AND no win singles):
    # with win singles off, a BET pick that is single-only still gets its win single
    for s in (bets_sel if BET_WIN_SINGLES else [b for b in bets_sel if "single only" in b["why"] and SINGLE_ONLY_SINGLES]):
        add("Singles", "Win single", [s], 1, s["why"])
    done = {(b["legs"][0]["course"], b["legs"][0]["time"]) for b in slip}
    for s in (sorted(strong, key=lambda s: (s["course"], s["time"])) if CONF_WIN_SINGLES else []):
        if (s["price"] or 0) >= CONF_SINGLE_MIN_PRICE and (s["course"], s["time"]) not in done:
            add("Singles", "Win single", [s], 1, s["why"] + " - " + BOG_NOTE)
    for s in (ew if BET_EW_SINGLES else []):
        add("Singles", "Each-way single", [s], 2, s["why"])

    def product(legs):
        ps = [l["price"] for l in legs]
        return math.prod(ps) if all(ps) else None

    if PRICE_MIX_TRIAL:
        if len(LAST_MIX) >= 2:
            add("Multiples", "Double", LAST_MIX[:2], 1, "PRICE MIX double - the short + middle legs (best value in each price band, TRIAL)",
                product(LAST_MIX[:2]))
        if len(LAST_MIX) == 3:
            add("Multiples", "Treble", LAST_MIX, 1, "PRICE MIX treble - short, middle and bigger price (best value in each band, TRIAL)",
                product(LAST_MIX))
    elif len(multi_sel) >= 2:
        add("Multiples", "Double", multi_sel[:2], 1, "our 2 strongest win picks (8/10+, proven, not drifting)", product(multi_sel[:2]))
    if PRICE_MIX_TRIAL:
        pass
    elif not SPREAD_MULTIPLES and len(multi_sel) >= 3:
        add("Multiples", "Treble", multi_sel[:3], 1, "our 3 strongest win picks (8/10+, proven, not drifting)", product(multi_sel[:3]))
    elif SPREAD_MULTIPLES and len(cap_heavy(multi_sel[2:], 3, heavy_courses)) == 3:
        tre = cap_heavy(multi_sel[2:], 3, heavy_courses)
        add("Multiples", "Treble", tre, 1, "our next 3 strongest win picks - different horses from the double", product(tre))
    elif SPREAD_MULTIPLES and len(multi_sel) == 4:
        add("Multiples", "Double", multi_sel[2:4], 1, "our 3rd and 4th strongest win picks - different horses from the first double",
            product(multi_sel[2:4]))
    l15, l63, f5 = (cap_heavy(multi_sel, 4, heavy_courses), cap_heavy(multi_sel, 6, heavy_courses),
                    cap_heavy(fold_sel, 5, heavy_courses))
    if len(l15) == 4:
        add("Multiples", "Lucky 15", l15, 15, "4 singles, 6 doubles, 4 trebles, 1 four-fold"
            + (" - our 4 best-value win picks priced 2.00+" if PRICE_MIX_TRIAL else ""))
    if len(l63) == 6:
        add("Multiples", "Lucky 63", l63, 63, "6 singles, 15 doubles, 20 trebles, 15 four-folds, 6 five-folds, 1 six-fold")
    if len(f5) == 5 and BET_FIVE_FOLD:
        add("Accumulators", "5-fold", f5, 1, f"our 5 strongest win picks (evidence agrees, {MULTI_MIN_CONF}/10+, proven, not drifting)", product(f5))
    if len(acc_sel) >= 7:
        add("Accumulators", "Super Heinz", acc_sel[:7], 120, "7 picks: 21 doubles, 35 trebles, 35 four-folds, 21 five-folds, 7 six-folds, 1 seven-fold")
    if len(ew) >= 4:
        add("Multiples", "Each-way Lucky 15", ew[:4], 30, "HIGH-ODDS LUCKY 15 - each-way (15 bets win + 15 place), Sky Bet extra places where offered")
    if len(ew) >= 6:
        add("Multiples", "Each-way Lucky 63", ew[:6], 126, "high-odds each-way version (63 win + 63 place)")

    fc = []
    for p in picks:
        second = parse_second(p.get("second"))
        p1 = p.get("chance") or 0
        if not second or not p1 or p.get("runners", 0) < 3 or p1 >= 1:
            continue
        name2, price2, p2 = second
        prob = p1 * p2 / (1 - p1)
        fc.append((prob, p, name2, price2, p2))
    fc.sort(key=lambda t: -t[0])
    for prob, p, name2, price2, p2 in (fc[:2] if BET_FORECASTS else []):
        a = sel(p["course"], p["time"], p["win"], dec(p["price"]), p["chance"], "our 1st")
        b = sel(p["course"], p["time"], name2, price2, p2, "our 2nd")
        if p2 >= 0.7 * p["chance"]:
            add("Forecasts", "Reverse forecast", [a, b], 2, f"our top 2 are close ({p['chance']:.0%} v {p2:.0%}) - either order")
        else:
            add("Forecasts", "Forecast", [a, b], 1, f"{a['horse']} to win, {name2} 2nd (our chances {p['chance']:.0%} / {p2:.0%})")
    return picks, slip


def leg_text(l):
    """One selection line: boxed time, course in capitals, horse, price (owner 1 Oct: easy-to-read course + time)."""
    price = f"{l['price']:.2f}" if l.get("price") else "TBC"
    fc = ('<div class="note">RP forecast - no bookmaker price yet: take the Sky Bet price or SP</div>'
          if l.get("forecast") else "")
    return (f'<li class="leg"><div class="where"><span class="time">{e(l["time"])}</span>'
            f'<span class="course">{e(l["course"]).upper()}</span></div>'
            f'<div class="what"><b class="horse">{e(l["horse"])}</b><span class="price">{price}</span></div>{fc}</li>')


def bet_card(b):
    legs = sorted(b.get("legs", []), key=lambda l: (l.get("time", ""), l.get("course", "")))
    ret = (f" · all win at these prices: returns <b>{money(int(b['unit'] * b['odds']))}</b>" if b.get("odds") else "")
    return (f'<div class="bet"><div class="bethead"><span class="betname">{e(b["name"])}</span>'
            f'<span class="betstake">{money(b["total"])}</span></div>'
            + (f'<div class="betnote">{e(b["note"])}</div>' if b.get("note") else "")
            + f'<ol class="legs">{"".join(leg_text(l) for l in legs)}</ol>'
            f'<div class="betfoot">{b["lines"]} line{"s" if b["lines"] != 1 else ""} x {money(b["unit"])}{ret}</div></div>')


def conf_box(l, scope="body"):
    """Rating + BET / NO BET tag for a slip leg, drawn by predict.bet_tag (owner 1 Nov 2026: 8+ = BET, 7 and below = NO BET)."""
    m = re.match(r"(\d+)/10", l.get("why") or "")
    if not m:
        return ""
    if PRICE_MIX_TRIAL and int(m.group(1)) < 8:
        # owner 3 Nov price mix: a 5-7/10 leg is on the slip for its price band / value, so it is not drawn as a BET or a
        # NO BET (the cards keep the 1 Nov tag rule) - an amber box says why it is there
        return f'<span class="vbox vmix">{int(m.group(1))}/10 PRICE MIX</span>'
    return tag_html(int(m.group(1)), scope=scope)


def leg_class(l):
    """Horse-name colour on the slip: gold 9-10/10, green 8/10, ink 7/10 and below (owner 1 Nov 2026)."""
    m = re.match(r"(\d+)/10", l.get("why") or "")
    return {"gold": "vm", "green": "vg", "red": "vi"}[colour(int(m.group(1)) if m else 0)] if m else "vg"


def _note_tail(b):
    return re.sub(r"^\d+/10 confidence\s*-\s*", "", b.get("note", ""))


def single_row(b):
    """A single is one horse: one compact row under its racecourse heading."""
    l = b["legs"][0]
    price = f"{l['price']:.2f}" if l.get("price") else "TBC"
    return (f'<div class="sel single"><span class="time">{e(l["time"])}</span><span class="horse"><span class="pk {leg_class(l)}">{e(l["horse"])}</span></span>'
            f'<span class="price">{price}</span><span class="in">{conf_box(l, "single")} {e(b["name"])} · {e(_note_tail(b))}</span>'
            f'<span class="stk">{money(b["total"])}</span>'
            + ('<span class="in">RP forecast - no bookmaker price yet: take the Sky Bet price or SP</span>' if l.get("forecast") else "")
            + '</div>')


SLIP_CSS = """.vbox.vmix{color:#1C1C1C;background:#FFC20E;border-color:#FFC20E}

.logo{width:min(260px,70%);margin:18px auto 10px}
.head{text-align:center}.head h1{font-size:28px}.head .sub{max-width:560px;margin:4px auto 0}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:16px}
.stat{border:1px solid var(--line);background:var(--card);border-radius:4px;padding:10px 12px;text-align:center}
.stat b{display:block;font:600 22px "IBM Plex Mono",monospace}
.stat span{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.08em}
h2{margin-top:34px}
.coursebar{display:flex;justify-content:space-between;align-items:baseline;gap:10px;background:var(--ink);color:#EAE2D8;
 border-radius:4px;padding:9px 14px;margin:18px 0 8px;font:600 19px/1.2 Jost,sans-serif;letter-spacing:.08em;text-transform:uppercase;break-after:avoid}
.coursebar small{font:500 12px Jost,sans-serif;letter-spacing:.08em;opacity:.8;white-space:nowrap}
.sel{display:grid;grid-template-columns:62px 1fr auto;gap:4px 12px;align-items:baseline;background:var(--card);
 border:1px solid var(--line);border-radius:4px;padding:9px 12px;margin-bottom:6px;break-inside:avoid}
.sel .time,.leg .time{font:700 15px "IBM Plex Mono",monospace}
.sel .horse{font:600 17px/1.25 "Source Sans 3",sans-serif;overflow-wrap:anywhere}
.sel .price,.leg .price{font:600 16px "IBM Plex Mono",monospace;white-space:nowrap}
.sel .in{grid-column:2/3;font-size:13px;color:var(--muted)}
.sel .stk{font:700 15px "IBM Plex Mono",monospace;text-align:right;white-space:nowrap;color:#3F7D3C}
.sel:not(.single) .in{grid-column:2/4}
.bets{display:grid;gap:12px}
.bet{background:var(--card);border:1px solid var(--line);border-left:5px solid #3F7D3C;border-radius:4px;padding:12px 14px;break-inside:avoid}
.bethead{display:flex;justify-content:space-between;align-items:baseline;gap:10px}
.betname{font:600 18px Jost,sans-serif;letter-spacing:.03em}
.betstake{font:700 18px "IBM Plex Mono",monospace;white-space:nowrap;color:#3F7D3C}
.betnote{color:var(--muted);font-size:13.5px;margin-top:2px}
.legs{list-style:none;padding:0;margin:10px 0 0;display:grid;gap:0}
.leg{border-top:1px solid var(--line);padding:8px 0}
.where{display:flex;gap:10px;align-items:baseline}
.leg .course{font:600 13px Jost,sans-serif;letter-spacing:.12em}
.what{display:flex;justify-content:space-between;gap:10px;align-items:baseline;margin-top:1px}
.leg .horse{font:600 16.5px/1.25 "Source Sans 3",sans-serif;overflow-wrap:anywhere}
.betfoot{border-top:1px solid var(--line);padding-top:7px;font-size:13px;color:var(--muted)}
.rg{margin-top:26px;text-align:center;font:600 14px Jost,sans-serif;letter-spacing:.06em;border:1.5px solid var(--ink);border-radius:4px;padding:10px}
@media (max-width:640px){.stats{grid-template-columns:1fr 1fr 1fr;gap:6px}.stat{padding:8px 4px}.stat b{font-size:18px}
 .coursebar{font-size:17px}.sel{grid-template-columns:54px 1fr auto}}
@media print{.wrap{padding-block:0 12px}h2{break-after:avoid}}
"""


def stakes_rule_html():
    if PRICE_MIX_TRIAL:
        return (f"<li>PRICE MIX (owner's choice, 3 Nov - TRIAL): win singles = our {SINGLE_MIN_CONF}/10+ win picks priced "
                f"{PRICE_MIX_SINGLE_MIN:.2f} or bigger - no short-priced singles. The treble = the best-value {MIX_MIN_CONF}/10+ pick "
                "in each price band (under 2.00, 2.00-3.49, 3.50+); the double = its short and middle legs. The Lucky 15 = our 4 "
                f"best-value {SINGLE_MIN_CONF}/10+ picks priced 2.00+. Every leg has not drifted and has run at the trip and on the "
                "going. Take the 09:30 price with a Best Odds Guaranteed bookmaker - if the starting price is bigger, you get that.</li>")
    return (f"<li>Win singles = our {MULTI_MIN_CONF}/10+ win picks that have not drifted and have run at the trip and on the going "
            f"(going = ground conditions). Doubles, trebles and Lucky 15s use the same {MULTI_MIN_CONF}/10+ picks, spread out: the "
            "treble uses different horses from the double, so one loser cannot sink every multiple. Take the 09:30 price with a "
            "Best Odds Guaranteed bookmaker - if the starting price is bigger, you get that.</li>")


def empty_box(race_date, picks):
    """Review team 2 Nov: the empty-slip box said 'No race reached confidence 8/10' on a day two 8/10+ picks were kept
    off by the safety rules -> name every 8/10+ pick and the rule that kept it off (no-false-information rule)."""
    kept = []
    for p in sorted(picks or [], key=lambda p: p.get("time") or ""):
        try:
            conf = int(p.get("confidence") or 0)
        except (TypeError, ValueError):
            conf = 0
        if conf < MULTI_MIN_CONF or not p.get("win"):
            continue
        why = _gap(race_date, p, p["win"])
        if not why and p.get("drift_warning"):
            why = "drifted overnight"
        m = re.match(r"([\d.]+) -> ([\d.]+)", p.get("move") or "")
        if not why and m and float(m.group(2)) >= float(m.group(1)) * DRIFT_MIN:
            why = f"drifted {m.group(1)} -> {m.group(2)}"
        kept.append(f"{e(p.get('time', ''))} {e((p.get('course') or '').upper())} - <b>{e(p['win'])}</b> "
                    f"({conf}/10): {e(why or 'kept off by the slip rules')}")
    if kept:
        n = len(kept)
        return ("<div class=\"box\"><b>No bets on this slip.</b> " + f"{n} pick{'s' if n != 1 else ''} reached "
                f"{MULTI_MIN_CONF}/10 or more but {'were' if n != 1 else 'was'} kept off by the slip safety rules:<br>"
                + "<br>".join(kept) + "<br>A quiet slip is a deliberate choice, not a gap.</div>")
    return ("<div class=\"box\"><b>No bets on this slip yet.</b> No race reached confidence "
            f"{MULTI_MIN_CONF}/10 and no horse passed our each-way rules. We only bet when our data says so - a quiet "
            "slip is a deliberate choice, not a gap.</div>")


def render(race_date, check, title, picks, slip):
    from predict.cards import is_unpriced
    for b in slip:   # team check 29 Oct: Ffos Las forecast prices showed on the slip with no label
        for l in b.get("legs", []):
            l["forecast"] = is_unpriced(race_date, l.get("course"), l.get("time"))
    d = Date.fromisoformat(race_date)
    nice = d.strftime("%A %d %B %Y").replace(" 0", " ")
    logo = base64.b64encode((REPO / "assets" / "brand" / "zans_logo_badge_small.jpg").read_bytes()).decode()
    total = sum(b["total"] for b in slip)
    # review team 5 Nov (A11): days staked £150+ were 1 won / 4 lost, -£209.53 (both halves) - a plain warning, the owner sets his stakes
    stake_warn = ('<p class="note"><b>STAKE WARNING:</b> this slip costs over £150 in total. Days with £150+ staked have lost '
                  'more often (1 winning day of 5 since 26 Sep). Consider leaving the extra bets out.</p>') if total > 15000 else ""
    # owner 30 Oct: "the bets are all crammed in and unorganised with the name of the track hard to read" ->
    # 1) every selection once, under its racecourse heading, with the bets it is in; 2) one card per bet
    horses = {}
    for b in slip:
        for l in b.get("legs", []):
            k = (l.get("course", ""), l.get("time", ""), l.get("horse", ""))
            h = horses.setdefault(k, {"leg": l, "in": []})
            if b["name"] not in h["in"]:
                h["in"].append(b["name"])
    by_course = {}
    for (c, t, hname), h in sorted(horses.items(), key=lambda x: (x[0][1], x[0][0])):
        by_course.setdefault(c, []).append(h)
    course_order = sorted(by_course, key=lambda c: min(h["leg"]["time"] for h in by_course[c]))
    sel_html = []
    for c in course_order:
        n = len(by_course[c])
        sel_html.append(f'<div class="coursebar" style="background:{course_colour(c, race_date, course_order)};color:{course_on(c, race_date, course_order)}">{e(c)}<small>{n} selection{"s" if n != 1 else ""}</small></div>')
        for h in by_course[c]:
            l = h["leg"]
            price = f"{l['price']:.2f}" if l.get("price") else "TBC"
            sel_html.append(f'<div class="sel"><span class="time">{e(l["time"])}</span><span class="horse"><span class="pk {leg_class(l)}">{e(l["horse"])}</span></span>'
                            f'<span class="price">{price}</span><span class="in">{conf_box(l)} In: {e(", ".join(h["in"]))}</span>'
                            + ('<span class="in">RP forecast - no bookmaker price yet: take the Sky Bet price or SP</span>'
                               if l.get("forecast") else "") + '</div>')
    sections = []
    extra = tuple(dict.fromkeys(b["section"] for b in slip if b["section"] not in ("Singles", "Multiples", "Accumulators", "Forecasts")))
    for section in ("Singles", "Multiples", "Accumulators") + (("Forecasts",) if BET_FORECASTS else ()) + extra:
        rows = [b for b in slip if b["section"] == section]
        if not rows:
            sections.append(f"<h2>{section}</h2><p class=\"note\">None today - no horse passed our rules for this bet type.</p>")
            continue
        if section == "Singles":   # singles grouped under their racecourse
            sub = {}
            for b in rows:
                sub.setdefault(b["legs"][0]["course"] if b.get("legs") else "", []).append(b)
            body = []
            for c in sorted(sub, key=lambda c: min(b["legs"][0]["time"] for b in sub[c])):
                n = len(sub[c])
                body.append(f'<div class="coursebar" style="background:{course_colour(c, race_date, course_order)};color:{course_on(c, race_date, course_order)}">{e(c)}<small>{n} single{"s" if n != 1 else ""}</small></div>'
                            + "".join(single_row(b) for b in sorted(sub[c], key=lambda b: b["legs"][0]["time"])))
            sections.append(f"<h2>Singles</h2>{''.join(body)}")
        else:
            sections.append(f'<h2>{section}</h2><div class="bets">{"".join(bet_card(b) for b in rows)}</div>')
    # owner 1 Nov: the header = the number of green BET tags in the selection rows below it (8/10+ legs)
    n_bets = sum(1 for h in horses.values() if tag((re.match(r"(\d+)/10", h["leg"].get("why") or "") or [0, 0])[1]) == "BET"
                 and re.match(r"\d+/10", h["leg"].get("why") or ""))
    empty = "" if slip else empty_box(race_date, picks)
    early = "" if check == "d0_morning" else ("<div class=\"box\">EARLY SLIP: built before race morning. Prices and "
                                              "non-runners can change; the race-morning slip is the final one.</div>")
    sel_block = f"<h2>Today's selections by racecourse</h2>{''.join(sel_html)}" if sel_html else ""
    return f"""<title>ZANS Bet Slip {d.day} {d.strftime('%b')}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jost:wght@500;600&family=Source+Sans+3:wght@400;600&family=IBM+Plex+Mono:wght@500;600;700&display=swap">
<style>{CSS}{SLIP_CSS}{VERDICT_CSS}</style>
<div class="wrap" data-gold-trim>
 {version_banner(race_date, __import__('predict.flags', fromlist=['flags_for_slip']).flags_for_slip(slip) or None)}
 <div class="head">
 <img class="logo" alt="ZANS — Horse Racing Tips" src="data:image/jpeg;base64,{logo}">
 <h1>{e(title)}<br>{e(nice)}</h1>
 <p class="sub">Every bet for the day across all cards · {e(', '.join(c for c in course_order) or ', '.join(sorted({p["course"] for p in picks})))} · decimal odds</p>
 </div>
 <div class="stats"><div class="stat"><b>{len(slip)}</b><span>bets</span></div>
 <div class="stat">{header_count(n_bets, "BET selections (8+/10)")}</div>
 <div class="stat"><b>{money(total)}</b><span>total outlay</span></div></div>
 {early}{empty}{stake_warn}
 {sel_block}
 {''.join(sections)}
 <h2>How the stakes work</h2>
 <ul><li>Every bet costs £10, or as close as possible without going over: stake per line = £10 ÷ number of lines, rounded down to the penny.</li>
 <li>Each-way bets are two lines (win + place). A Lucky 15 is 15 lines, a Lucky 63 is 63 lines; each-way versions double that. Minimum 5p a line.</li>
 {stakes_rule_html()}
 <li>No horse that has been off the track for 90 days or more, and no horse in a maiden, novice, beginners' or bumper jumps race, goes on the slip (owner's rules, 9 Oct 2026).</li></ul>
 <p class="rg">18+ only · Please gamble responsibly · BeGambleAware.org</p>
 <p class="foot">TRIAL: every bet is checked against the result and starting price after racing. Not financial or betting advice; past results don't guarantee future results.</p>
</div>"""


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    ap.add_argument("--check", default="d0_morning")
    ap.add_argument("--title", default="ZANS Bet Slip")
    ap.add_argument("--after", default="", help="only races after this UK time (HH:MM), for an updated slip")
    ap.add_argument("--overseas", action="store_true", help="add reports/overseas/<date>/selections.json (e.g. Paris)")
    ap.add_argument("--out", default="betslip", help="file stem; the locked slip is betslip - use another for extra slips")
    a = ap.parse_args(argv)
    picks, slip = build_bets(a.date, a.check, a.after, a.overseas)
    day = REPO / "reports" / "predictions" / a.date
    (day / f"{a.out}.json").write_text(json.dumps(slip, indent=1))
    html = render(a.date, a.check, a.title, picks, slip)
    clash = colour_clashes(html)   # owner 7 Nov: every racecourse its own colour - never send a slip with two the same
    if clash:
        raise SystemExit("COLOUR CHECK FAILED - courses share a colour: " + "; ".join(f"{c} = {', '.join(n)}" for c, n in clash.items()))
    print("COLOUR CHECK OK")
    (day / f"{a.out}.html").write_text(html)
    for h in spread_problems(slip):
        print(f"WARNING: {h} is in every double/treble/accumulator - one loser sinks them all")
    (day / f"{a.out}_treble.json").write_text(json.dumps(
        {"date": a.date, "check": a.check, "legs": LAST_TREBLE,
         "odds": round(math.prod(l["price"] for l in LAST_TREBLE), 2) if LAST_TREBLE and all(l["price"] for l in LAST_TREBLE) else None},
        indent=1))
    print(f"SLIP TREBLE: " + (" / ".join(f"{l['time']} {l['course']} {l['horse']} {l['price']}" for l in LAST_TREBLE)
                               if LAST_TREBLE else f"none today (fewer than 3 x {MIX_MIN_CONF if PRICE_MIX_TRIAL else MULTI_MIN_CONF}/10+ picks pass every slip rule)"))
    if PRICE_MIX_TRIAL:
        (day / f"{a.out}_top3.json").write_text(json.dumps(
            {"date": a.date, "check": a.check, "rule": f"price mix (owner 3 Nov): best value in each band <2.00 / 2.00-3.49 / 3.50+, "
             f"safe {HEADLINE_MIN_CONF}/10+ win picks", "legs": LAST_HEADLINE}, indent=1))
        print("HEADLINE TOP 3 (price mix): " + (" / ".join(f"{l['band']} {l['time']} {l['course']} {l['horse']} {l['price']} "
              f"({l['why'].split(' ')[0]})" for l in LAST_HEADLINE) or "none"))
    # owner 1 Nov: no 7/10-or-lower (NO BET) horse anywhere on the slip, and every tag / header count must agree
    from predict.bet_tag import check_html
    bad = slip_conf_problems(picks, slip)
    probs, c = check_html((day / f"{a.out}.html").read_text(encoding="utf-8"), a.title, slip=True)
    bad += probs
    # review chat 2 Nov: the stakes box still said '7/10+' after the 8/10+ rule - no contradictions on a sheet
    html_txt = (day / f"{a.out}.html").read_text(encoding="utf-8")
    floor_txt = min(SINGLE_MIN_CONF, MIX_MIN_CONF) if PRICE_MIX_TRIAL else MULTI_MIN_CONF
    for lo in range(1, floor_txt):
        if f"{lo}/10+" in html_txt:
            bad.append(f"slip text says '{lo}/10+' but the slip rule is {floor_txt}/10+")
    print(f"{len(slip)} bets, total {money(sum(b['total'] for b in slip))} -> {day / (a.out + '.html')}")
    if bad:
        print("NOT SENDABLE: " + "; ".join(bad))
        sys.exit(1)


if __name__ == "__main__":
    main()
