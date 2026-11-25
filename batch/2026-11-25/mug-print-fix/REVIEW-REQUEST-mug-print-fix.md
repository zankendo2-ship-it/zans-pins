# REVIEW REQUEST - FACT TO FILE mug print file re-made (25 Nov 2026, 18:15 UTC) - TASK 7b01963

Folder `batch/2026-11-25/mug-print-fix/`. Builder `build.js` (new, written in zans-pins; the racing repo was not read or touched). No order, no spend. The locked master mug model is not changed.
- Print file: `ZANS-mug-PRINT-FILE-fact-to-file-4950x2310-DRAFT.png`
- Flat proof: `ZANS-mug-FLAT-PROOF-fact-to-file-300dpi-DRAFT.png` (the wrap at 90% of real size on a 300 dpi sheet, with the mm sizes)
- Measured figures: `print-check.json`

## PRINT PREFLIGHT (rule of 25 Nov)
| Check | Result |
|---|---|
| 1. Resolution | 4950 x 2310 px on a 209.6 x 97.8 mm print area = 600 dpi (2x). Drawn as vector, so edges are sharp at that size. PASS |
| 2. Safe zone and thin lines | Name plates 8.3 mm from each wrap end (were 6.3 mm). Thinnest line 1.6 mm: white line under the cap band 2.0 mm (was 1.2 mm), plate border 1.6 mm (was 1.2 mm). No ring. PASS. Note: a 6 mm safe zone top and bottom is NOT met by design: the cap band runs to the top edge and the hoops to the bottom, as on the printed test mug. Those are bleed colour, not text. |
| 3. Text | Name 7.5 mm tall, bold, green #00843D on cream #FBF7F0. Logo line "ZANS RACING TOOLS" 3.3 mm tall, vector text, ink on cream (was about 2 mm with a bitmap logo). Logo text is 3.3 mm, just under the general 3.5 mm rule; the task asked for 3 mm+. Say if it must be 3.5. |
| 4. Colours | Unchanged from the printed test file (sampled): cap band #C8102E, hoops #F5D130 and #00843D. These are saturated, not pastel. Silks not altered. PASS |
| 5. Profile | sRGB profile embedded (checked by re-opening the file). PASS |

## Changes from the test mug's file
1. 1x (2475 x 1155) -> 2x (4950 x 2310), vector-drawn.
2. Bitmap horse logo removed; the logo line is now text only, bigger. I have no vector of the horse logo, so it is left off rather than printed soft.
3. White hairline thickened to 2.0 mm; plate border to 1.6 mm.
4. Name plates moved 2 mm further in from the wrap ends.
5. sRGB embedded.

## Honest limits
- Positions were measured from the test file in `zans-social-notes:print-qa/2026-11-25-mugs/` and redrawn; this is not the website designer's own code. The live mug designer and the automatic order script still make the old 1x file until their code is changed.
- `/mnt/project-files/` is not mounted in this session: no copy made there.
- Only a printed sample proves the result.

## Also: PRINT PREFLIGHT for the bauble files (same rule)
All four bauble print files in `batch/2026-11-25/bauble-print-fix/`: 3960 x 3960 px on a 74.93 mm face = 1,342 dpi (PASS); 6 mm safe zone, no ring, thinnest line 0.35 mm (the darker outline round each Lossiemouth spot) and 0.55 to 0.7 mm ink outlines (FAIL against the new 1.5 mm line rule: the task of 17:05 asked for dark outlines but gave no width; tell me whether to thicken them to 1.5 mm or remove them); name 6.0 to 6.6 mm, MERRY CHRISTMAS 3.7 mm, ink on near-white (PASS); colours as listed in that review request, Loussiemoo A keeps the approved hexes (PASS); sRGB now embedded in all eight bauble PNGs (PASS).
