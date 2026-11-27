# Doncaster FLAT - low draw on soft/heavy, straight 5f-7.5f, 10+ runners (research queue 15) - TEST

Helper research 26 Oct 2026, scripts and outputs in /tmp/claude-0/research26/ (scratch). A/E on margin-free SP.

- Market A/E, low third: 2015-21 27/313 (72 races) 1.18, -19% SP | 2022-26 28/287 (71 races) 1.24, -25% SP.
  2015-18 alone 11/189 = 0.89; single years swing 0.44-1.89. Heavy 18/146 = 1.65, soft 37/454 = 1.07.
- Against OUR MODEL (46 features, walk-forward from 2021, 2019-20 cross-fitted): 2019-21 15/123 joint 1.41 | 2022-26 30/313 1.23.
  Controls v model: good to soft 1.01 | 0.98; good or firmer 0.99 | 0.97. The model's all-going draw factor does not absorb it.
- Verdict: passes the two-period test against the model but thin (15 and 30 winners, 2024 0.67).
  Proposal: provisional Doncaster FLAT factor x1.04 for low third on SOFT/HEAVY, straight 5f-7.5f, 10+ runners -
  needs a draw_low variant with trip + field-size limits before coding. Doncaster's last flat card is usually early Nov
  (6 Nov 2021, 5 Nov 2022, 9 Nov 2024, 8 Nov 2025) - build before then if the fixture is confirmed.
