# Full evidence bundle for 2026-11-27: Newbury, Doncaster, Musselburgh, Southwell, Dundalk

Copied byte for byte from the private racing repo (branch claude/horse-racing-prediction-setup-a02c7r) so ChatGPT sees what Claude's models use. Every file is listed in MANIFEST.json with its sha256; combined sha256 `caa6c8642602d6a0f03ebb0f94a8a9f5c71deb302cbff3ce7acc143e84bb3158`.

Contents under `data/` (same paths as the private repo):
- `reports/track_dna/2026-11-27/` the whole Track DNA run: full course-guide text, accepted and rejected evidence, Track DNA fields, distance profiles, race-day notes, audit.
- `reports/course_kb/courses/` per course and code: draw, pace, weight, going, trip, favourite, trainer/jockey tables built from all UK/IRE results 2019 onward, split 2019-21 and 2022-26 with A/E and sample sizes.
- `methods/` and `reports/methods/` the course method files and every rule's tested A/E table (full history and since 2022).
- `config/course_profiles/` the hand-written course profiles.
- `reports/racecards/2026-11-27/` the frozen pre-race evidence for every runner (form, ratings, trainer/jockey records, draw and pace DNA, market), speed and pace map, connections, form coverage, form check, racecards.
- `reports/predictions/2026-11-27/` each course's method output and published picks, Data picks with reasons, ground check, seal.
- `reports/going/2026-11-27/`, `reports/odds/2026-11-27/` (d-1 evening, d0 morning, d0 midday prices), `reports/stewards/` last seven days.
- `rules/RULES.md` the pre-registered rules.

NOT included: the raw historical results database (history/*.csv.gz, hundreds of MB, too big for this repo). Its derived statistics are in the course_kb and rules tables above and each runner's own form lines are in the evidence file. Racing Post ratings and BHA/Weatherbys data are licensed: use for this review only, do not republish.
