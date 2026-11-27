"""Parsers for raw results fields: distance, going, race code, course and running style."""
import re

# ============================================================
# DISTANCE
# ============================================================

_DIST = re.compile(r"^(?:(\d+)m)?\s*(?:(\d+)?(½)?f)?$")


def dist_to_furlongs(dist):
    """'1m2½f' -> 10.5, '6f' -> 6.0, '2m' -> 16.0. None if unparseable."""
    text = str(dist or "").strip().replace(" ", "")
    match = _DIST.match(text)
    if not text or not match or not any(match.groups()):
        return None
    miles, furlongs, half = match.groups()
    return int(miles or 0) * 8 + int(furlongs or 0) + (0.5 if half else 0)


def furlongs_label(furlongs):
    miles, rem = divmod(furlongs, 8)
    half = "½" if rem % 1 else ""
    rem = int(rem)
    furlong_part = f"{rem or ''}{half}f" if rem or half else ""
    parts = (f"{int(miles)}m" if miles else "") + furlong_part
    return parts or "0f"


# ============================================================
# GOING
# ============================================================

GOING_GROUPS = {
    "FAST": {"hard", "firm", "good to firm", "fast", "standard to fast"},
    "GOOD": {"good", "good to yielding"},
    "SOFT": {"good to soft", "soft", "heavy", "yielding", "yielding to soft", "soft to heavy",
             "very soft"},
    "STANDARD": {"standard", "standard to slow", "slow"},
}


def going_group(going):
    going = str(going or "").strip().lower()
    for group, values in GOING_GROUPS.items():
        if going in values:
            return group
    return "OTHER"


# ============================================================
# COURSE + RACE CODE
# ============================================================

COURSE_ALIASES = {
    "chelmsford": "chelmsford_city",
    "great_yarmouth": "yarmouth",
    "bangor": "bangor_on_dee",
    "bangor_on_dee": "bangor_on_dee",
    "the_curragh": "curragh",
    "epsom_downs": "epsom",
    "newmarket_july": "newmarket",
    "newmarket_rowley": "newmarket",
    "royal_ascot": "ascot",
}

# OWNER RULE (2026-09-26): "Always UK and Ireland, nowhere else". Every UK/IRE course is in
# config/courses.json; these closed British courses still count as UK history.
UK_IRE_EXTRA = {"towcester"}
_UK_IRE = None


def is_uk_ire(course):
    """True only for British and Irish racecourses (registry + closed UK courses)."""
    global _UK_IRE
    if _UK_IRE is None:
        import json
        from pathlib import Path
        reg = Path(__file__).resolve().parent.parent / "config" / "courses.json"
        _UK_IRE = set(json.loads(reg.read_text())["courses"]) | UK_IRE_EXTRA
    tags = {t.strip().upper() for t in re.findall(r"\((.*?)\)", str(course or ""))}
    if tags - {"AW", "IRE", "GB", "UK", "JULY", "ROWLEY"}:
        return False    # e.g. "Ascot (AUS)", "Newcastle (AUS)", "Down Royal (FR)"
    return course_key(course)[0] in _UK_IRE


OVERSEAS_BRED = re.compile(r"\((AUS|NZ)\)\s*$")


def overseas_bred_race(horse_names):
    """True when most runners in a race are Australian/New Zealand-bred: an overseas race filed under a British course
    name (15 Oct 2026: 21 races from Ascot, Perth WA, Oct 2025-May 2026, were in our history as plain 'Ascot').
    No British or Irish race has a majority of AUS/NZ-bred runners."""
    names = [str(n or "") for n in horse_names if n]
    return bool(names) and 2 * sum(1 for n in names if OVERSEAS_BRED.search(n.strip())) >= len(names)


def course_key(course):
    """'Southwell (AW)' -> ('southwell', True); 'Killarney (IRE)' -> ('killarney', False)."""
    text = str(course or "")
    is_aw = "(AW)" in text
    name = re.sub(r"\(.*?\)", "", text).strip().lower()
    key = re.sub(r"[^a-z0-9]+", "_", name).strip("_")
    return COURSE_ALIASES.get(key, key), is_aw


DISCIPLINES = {"flat": "FLAT", "hurdle": "HURDLE", "chase": "CHASE", "nh flat": "NHF"}
JUMPS_DISCIPLINES = ("HURDLE", "CHASE", "NHF")
DISCIPLINE_NAMES = {"FLAT": "Flat", "AW_FLAT": "All-weather flat", "HURDLE": "Hurdles",
                    "CHASE": "Chases", "NHF": "National Hunt flat (bumpers)"}


def discipline(race_type, is_aw):
    """Finer split than race_code: FLAT, AW_FLAT, HURDLE, CHASE or NHF."""
    value = DISCIPLINES.get(str(race_type or "").strip().lower())
    if value == "FLAT" and is_aw:
        return "AW_FLAT"
    return value


def race_code(race_type, is_aw):
    race_type = str(race_type or "").strip().lower()
    if race_type == "flat":
        return "AW_FLAT" if is_aw else "FLAT"
    if race_type in {"hurdle", "chase", "nh flat"}:
        return "JUMPS"
    return None


# ============================================================
# RUNNING STYLE (from the in-running comment's opening words)
# ============================================================

# Scores: 4 = led, 3 = prominent, 2 = mid-division, 1 = held up / rear.
STYLE_RULES = [
    (4, r"^(made (virtually )?all|made most|led|set (a |the )?(steady |strong |fair |modest |good )?pace|"
        r"soon led|disputed lead|disputed|with leader|joint lead|went left start,? led|"
        r"narrow lead|always leading)"),
    (3, r"^(prominent|tracked (leader|leaders|winner|pace)|chased (leader|leaders|winner|clear leader)|"
        r"pressed (leader|winner)|close up|handy|handily|in touch with leaders?|raced keenly,? prominent|"
        r"cl(o)?se up|on heels of leaders?|always prominent|chased leading|with leaders|"
        r"tracked leading (pair|trio|group|quartet)|tracked leader)"),
    (2, r"^(mid[- ]?division|midfield|in touch|raced in mid|towards rear of mid|never better than mid)"),
    (1, r"^(held up|behind|in rear|towards rear|always (behind|in rear|towards rear)|"
        r"dwelt|slowly away|missed break|rear|detached|outpaced (early|in rear)|never (a factor|dangerous|"
        r"near|nearer|on terms)|reared|restless in stalls|awkward start|started slowly|last|"
        r"waited with|very slowly away|slowly into stride)"),
]
_STYLE = [(score, re.compile(pattern, re.I)) for score, pattern in STYLE_RULES]
STYLE_NAMES = {4: "LED", 3: "PROMINENT", 2: "MIDFIELD", 1: "HELD_UP"}


def running_style(comment):
    """Return 1-4 from the opening of an in-running comment, or None if unclassifiable."""
    text = str(comment or "").strip()
    # A start incident ("Dwelt - soon led") is followed by the settled position; judge that
    # first, falling back to the whole comment ("Dwelt - always behind" -> held up).
    settled = re.sub(r"^((awkward|dwelt|(very )?slowly (away|into stride)|missed break|"
                     r"went (left|right)|jinked|bumped|hampered|took (a )?(keen|strong) hold|"
                     r"raced keenly|pulled hard|steadied (at )?start|taken down early|"
                     r"soon pushed along|raced wide|broke well|not fluent|"
                     r"raced (on )?(stands'?|far|centre|towards (stands'?|far))( side)?)"
                     r"[^,;-]*[,;-]\s*)+(soon |then |quickly )?",
                     "", text, flags=re.I)
    candidates = []
    for candidate in (settled, text):
        candidates += [candidate, re.sub(r"^(soon|settled|early)\s+", "", candidate, flags=re.I)]
    for candidate in dict.fromkeys(candidates):
        for score, pattern in _STYLE:
            if pattern.search(candidate):
                return score
    return None
