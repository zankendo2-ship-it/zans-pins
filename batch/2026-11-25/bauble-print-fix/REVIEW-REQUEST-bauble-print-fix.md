# REVIEW REQUEST - round bauble print files re-made (25 Nov 2026, 17:45 UTC) - TASK 135f3d5

Folder `batch/2026-11-25/bauble-print-fix/`. Builder `build.js` (my own, written in zans-pins; the racing repo was not read or touched). No order placed, nothing spent.

Where the code lives: zans-pins had NO printFile code for the bauble (only `templates/cap12.js`, which screenshots the website designer). So I wrote a new generator here and matched the three printed designs from the copies in `zans-social-notes:print-qa/2026-11-25-baubles/` (spot size and spacing measured from those files).

## Files
| Print file (3960 x 3960 PNG, 74.93 mm face) | Flat real-size proof (300 dpi PNG) |
|---|---|
| `ZANS-bauble-PRINT-FILE-loussiemoo-A-approved-hexes-3960px-DRAFT.png` | `ZANS-bauble-FLAT-PROOF-loussiemoo-A-approved-hexes-300dpi-DRAFT.png` |
| `ZANS-bauble-PRINT-FILE-loussiemoo-B-deeper-ceramic-3960px-DRAFT.png` | `ZANS-bauble-FLAT-PROOF-loussiemoo-B-deeper-ceramic-300dpi-DRAFT.png` |
| `ZANS-bauble-PRINT-FILE-rexs-romance-3960px-DRAFT.png` | `ZANS-bauble-FLAT-PROOF-rexs-romance-300dpi-DRAFT.png` |
| `ZANS-bauble-PRINT-FILE-zoo-olympios-3960px-DRAFT.png` | `ZANS-bauble-FLAT-PROOF-zoo-olympios-300dpi-DRAFT.png` |
Sheet: `ALL-bauble-flat-proofs-CONTACT-SHEET.jpg`. Measured figures: `print-check.json` (written by the script, not typed).

## The fixes
1. Thin gold ring REMOVED. No ring at all.
2. 6 mm safe zone: the cap button and peak, the name panel and all text are inside it (furthest point of the panel: 31.1 mm from centre on Loussiemoo, 30.4 mm on the other two; safe radius 31.5 mm). The silks colour and the cap colour bleed to the edge of the square file.
3. Name: 6.0 mm tall (Loussiemoo, one line) and 6.6 mm tall (the two-line names), Jost bold, ink #1C1C1C. MERRY CHRISTMAS: 3.7 mm tall, bold, ink #1C1C1C on a near-white panel #FFFDF7. Heights are capital-letter heights measured by the script.
4. Logo text DROPPED (it was about 1 mm; no room to make it readable inside the safe zone).
5. Dark outlines: 0.7 mm ink line round the name panel, 0.55 mm ink line along the cap edge and peak, 0.35 mm darker-green line round each Lossiemouth spot.
6. Colours:
   - Loussiemoo A: approved hexes kept exactly, body/cap #F3B5C9, spots #6CC24A.
   - Loussiemoo B: deeper for ceramic, body/cap #EC89A9, spots #53AD2F. Alex chooses A or B.
   - Rexs Romance: blue #1C4FA0 -> #0E3D88; cap white.
   - Zoo Olympios: yellow #F5D130 -> #FFD209; spots and cap #111111.
7. Proofs: each is a 300 dpi sheet with the disc at real size (74.9 mm), the dashed 6 mm safe-zone circle, the mm sizes, the hexes, a PASS line and a 50 mm check line to measure after printing.

## Honest limits
- The "deeper" colours are a rule of thumb (more saturation, less lightness), not a printer's colour profile. Only a printed sample shows the true result. I would order ONE sample before any customer order, with Alex's yes.
- The name on Loussiemoo is exactly 6.0 mm: a 10-letter single word cannot go bigger inside the safe zone. Longer names will need two lines or will fall under 6 mm; the script reports a FAIL when that happens.
- Name text is now ink black on all three (before, it was the silks colour). Say if the name should stay in the silks colour where that colour is dark enough (the blue would pass; the green would not).
- This generator is NOT the website designer. The live designer still makes the old layout (thin ring, small text) for every customer order until its print file code is changed the same way. That code is not in this repo.
- `/mnt/project-files/` does not exist in this session, so I could not copy the files there. They are on the branch only.
- Printed-bauble faults I have NOT seen myself: I worked from the print check file, not from photos of the three printed baubles.

## FIXES DONE - ready for re-check (25 Nov 2026, 18:40 UTC) - ADVICE 4bcd2c7
- [x] 1. Lines: name-panel outline, cap edge and peak outline are now 1.5 mm. The 0.35 mm outlines round the Lossiemouth spots are REMOVED. The grey cap seams and button are REMOVED (at 1.5 mm they crowded the cap). Rexs Romance: the white cap now has the 1.5 mm ink edge along its lower line and peak. No line in any file is under 1.5 mm.
- [x] 2. Proof captions: each note is on its own line; "No ring" no longer overlaps anything.
- [x] 3. One figure everywhere, from `print-check.json`: MERRY CHRISTMAS 3.7 mm tall (3.66 measured); name 6.0 mm (Loussiemoo) and 6.6 mm (Rexs Romance, Zoo Olympios).
- [x] 4. Unchanged: ink-black names, the two Loussiemoo versions, colours, safe zone, sRGB (re-embedded and re-checked after the rebuild), 3960 px.
### PRINT PREFLIGHT (rule of 25 Nov)
| Check | Result |
|---|---|
| 1. Resolution | 3960 x 3960 px on a 74.93 mm face = 1,342 dpi. PASS |
| 2. Safe zone and lines | Cap peak, name panel and all text inside the 6 mm safe zone (key content within 31.1 mm / 30.4 mm of centre; safe radius 31.5 mm). No ring. Thinnest line 1.5 mm. PASS |
| 3. Text | Names 6.0 / 6.6 mm, MERRY CHRISTMAS 3.7 mm, bold, ink #1C1C1C on #FFFDF7. PASS |
| 4. Colours | Loussiemoo A approved hexes #F3B5C9 / #6CC24A (pastel pink by Alex's approval); B #EC89A9 / #53AD2F; Rexs #0E3D88; Zoo #FFD209 / #111111. PASS, with A flagged as pastel for Alex's choice |
| 5. Profile | sRGB embedded in all eight PNGs. PASS |
### Where the live designer code lives (for the coordinator)
Not in zans-pins. The bauble and mug designers run on the website (www.zanshorseracing.co.uk/bauble-designer/ and /mug-designer/); the files uploaded to the printer are built by `etsy/own_bauble_order.py` and `etsy/mug_orders.py` in the racing repo (named in the reviewer's own print checks). I have not opened either.
