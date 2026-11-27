"""Pace map — who is likely to lead today, how strong the early pace should be, who it suits.

Each runner's usual position early in its races comes from the in-running comments of its
last 6 runs (track_stats.parse.running_style: led / prominent / mid-division / held up).
  role   LEADER     led in at least half of its readable recent runs (2+ runs read)
         PROMINENT  up with the pace (led or prominent) in at least half
         HOLD_UP    held up / in rear in at least half
         MIDFIELD   the rest;  UNKNOWN when fewer than 2 runs can be read (debutants etc.)
  race   projected early pace from the number of likely leaders:
         0 -> SLOW (no natural leader: prominent horses can dictate)
         1 -> LONE_LEADER (one horse could get an easy lead: the classic pace angle)
         2 -> EVEN
         3+ -> STRONG (a contested lead: set up for horses coming from behind)
  fit    SUITS / AGAINST / NEUTRAL for each runner's role under that scenario - only the calls
         the backtest supported (see FIT), separately for flat and jumps.
The scenario only helps if it held in the past, so speed.validate backtests every rule on
historic races before we rely on it.
"""
from collections import Counter

READ_RUNS = 6
MIN_READ = 2

SCENARIO_TEXT = {
    "SLOW": "Slow early pace likely - no habitual front-runner; those racing prominently "
            "can dictate",
    "LONE_LEADER": "Lone front-runner - {leader} could get an easy lead",
    "EVEN": "Even pace likely - two habitual front-runners",
    "STRONG": "Strong early pace likely - {n} habitual front-runners should take each other on",
    "UNKNOWN": "Pace unclear - too few runners with readable running styles",
}

# SUITS / AGAINST calls, kept only where the 2025-26 backtest (speed/validate.py, A/E vs SP)
# agreed with the racing logic; everything else stays NEUTRAL. Flat and jumps differ: flat
# front-runners did NOT suffer in strongly run races, and hold-up horses only struggled on the
# flat when one horse could dictate.
FIT = {
    "FLAT": {
        "SLOW": {"PROMINENT": "SUITS"},
        "LONE_LEADER": {"LEADER": "SUITS", "HOLD_UP": "AGAINST"},
    },
    "JUMPS": {
        "SLOW": {"PROMINENT": "SUITS", "HOLD_UP": "AGAINST"},
        "STRONG": {"HOLD_UP": "SUITS", "MIDFIELD": "SUITS"},
    },
}


def runner_role(styles):
    """styles: running-style scores (4 led .. 1 held up) of recent runs, newest last."""
    read = [s for s in styles if s][-READ_RUNS:]
    if len(read) < MIN_READ:
        return "UNKNOWN", 0.0, len(read)
    count = Counter(read)
    led = count[4] / len(read)
    if led >= 0.5:
        role = "LEADER"
    elif (count[4] + count[3]) / len(read) >= 0.5:
        role = "PROMINENT"
    elif count[1] / len(read) >= 0.5:
        role = "HOLD_UP"
    else:
        role = "MIDFIELD"
    return role, round(led, 2), len(read)


def race_scenario(roles):
    """roles: {horse: role}. Returns (scenario, leaders list)."""
    known = [h for h, r in roles.items() if r != "UNKNOWN"]
    leaders = [h for h, r in roles.items() if r == "LEADER"]
    if len(known) < max(2, len(roles) / 2):
        return "UNKNOWN", leaders
    if not leaders:
        return "SLOW", leaders
    if len(leaders) == 1:
        return "LONE_LEADER", leaders
    if len(leaders) == 2:
        return "EVEN", leaders
    return "STRONG", leaders


def fit(scenario, role, disc=None):
    code = "JUMPS" if disc in ("HURDLE", "CHASE", "NHF", "JUMPS") else "FLAT"
    return FIT[code].get(scenario, {}).get(role, "NEUTRAL")


def scenario_text(scenario, leaders):
    return SCENARIO_TEXT[scenario].format(leader=", ".join(leaders), n=len(leaders))
