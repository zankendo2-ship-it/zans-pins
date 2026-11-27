# Full evidence bundle for 2026-11-27: Newbury, Doncaster, Musselburgh, Southwell, Dundalk (v2, with results extracts)

306 files, 9.8 MB, copied byte for byte from the private racing repo except the results extracts, which are filtered by course. Every file is in MANIFEST.json with its sha256. Combined sha256 `a66af84021e781e031a1b862e7a566c25641de3272e3a348708cf548b67ae722`.

Under `data/` (same paths as the private repo):
- `results/<course>_results_2019_2026.csv.gz`: every run at the five courses, 2019 to 26 Nov 2026 (race, off time, type, class, distance, going, field size, position, draw, beaten lengths, horse, age, weight, headgear, time, SP, jockey, trainer, prize). Dundalk has only Oct 2025 to May 2026 because our history source lacks earlier Dundalk. Use these to check the course tables below.
- `reports/course_kb/courses/`: per course and code draw, pace, weight, going, trip, favourite, trainer/jockey tables, 2019-21 and 2022-26 A/E with sample sizes.
- `reports/track_stats/*.csv`: national and course draw, pace and weight bias tables (all courses). `reports/speed/standards.csv`: ZANS standard times.
- `reports/track_dna/2026-11-27/`: the whole Track DNA run. `methods/`, `reports/methods/`, `config/course_profiles/`: course methods and every rule's tested A/E.
- `reports/racecards/2026-11-27/`: frozen pre-race evidence per runner (includes Racing Post ratings already public in the sealed pack), speed/pace map, connections, form coverage; `reports/predictions/2026-11-27/`: each model's course output, Data picks and reasons; going, odds, stewards (last 7 days).
- `predict/*.py`, `speed/*.py`, `track_stats/*.py`, `config/predict_weights.json`, `config/csf_model.json`: the model code and weights. `rules/RULES.md`, `reports/knowledge_pack/`, `reports/research/2026-11-*`: pre-registered rules and research notes.

Held back (not published): the Racing Post ratings (RPR, Topspeed), BHA official ratings and Racing Post comment text in the results extracts, the full UK/IRE history for the other courses, the Betfair and BHA bulk files, and the owner-facing project memory. These are third-party licensed or private. If the owner confirms the rights, they can be added.
