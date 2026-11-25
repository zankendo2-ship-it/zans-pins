# Print fix v4 - original approved artwork, technical fixes only (25 Nov 2026)

v3 is withdrawn (Alex rejected it as a redesign). v4 starts from the ORIGINAL artwork:
- baubles: the live bauble designer's own print SVG for Alex's 3 design codes (the same artwork as etsy/orders/own-*.png, printed 19 Nov);
- mug: the exact file Printify printed for the FACT TO FILE test mug, plus the same design code on the white-mug template.
Shapes, fonts (Jost), letter spacing, cap, seams, patterns, panel, name colours and the logo tab are kept as they were.

## Invisible fixes (look the same, all files)
1. Every word turned into vector outlines (no font substitution at the printer).
2. ZANS logo strip redrawn as vector (traced horse mark + Jost "ZANS RACING TOOLS"), same size and place - was a blurry 750 px bitmap.
3. Cap shine: the 70%-see-through stripe is flattened into the solid colour it already showed (Loussiemoo #F6C8D7 @70% = #F5C2D2; Zoo Olympios #A4A4A4 @70% = #7B7B7B; Rexs Romance white on white = white). Print files carry no transparency.
4. Exact supplier template size (bauble 990 x 990 px = 74.9 mm; mugs 2475 x 1155 Harrier / 2582 x 1120 white), lossless PNG with sRGB embedded, placement centre 0.5 / 0.5 / scale 1.
5. Background printed to the edge (full bleed) so a small shift shows pattern, not white.

## Visible changes - each needs a yes or no
| # | Product | Change | Why |
|---|---|---|---|
| V1 | all 3 baubles | Thin gold ring at the very edge REMOVED | It sat 2 mm from the edge, inside the 5 mm band where sublimation shifts the print; any shift makes it look off centre - the main "off centre" complaint. |
| V2 | baubles, option B only | MERRY CHRISTMAS letters 1.7 mm -> 3.5 mm tall (same font, weight, colour, place) | 1.7 mm letters blur on ceramic; 3.5 mm is the minimum we set for print. Option A keeps 1.7 mm and fails our check. |
| V3 | baubles, option B only | ZANS logo tab + strip 2.2x bigger, moved up to stay 6 mm inside the edge | Logo letters were 0.7 mm (unreadable when printed); now 1.5 mm. Option A keeps the original size and fails our check. |
| V4 | FACT TO FILE mug | ZANS logo tab moved to the true centre of the wrap | It was 9.5 mm right of centre in the printed file (built for an older 2700 px template). |
| V5 | FACT TO FILE mug | Name plates 3% smaller (white mug 5%) | They ended 4.4 mm from the bottom edge; now 6 mm (safe zone). |

## Not changed - flagged for Alex
- Loussiemoo name stays green #6CC24A on cream as approved (contrast 2.0 : 1, low). Ink #1C1C1C would read better - only as a separate option if he wants it.
- FACT TO FILE mug colours are the 2 Nov design code (green/gold hoops, red top strip). Irish Racing + Sporting Life describe the McManus colours as "green and gold hoops" and don't state the cap; ChatGPT says green and orange hoops, white cap. NOT recoloured - Alex decides.
- A whole-print shift of 5 mm can still show a thin unprinted strip at one edge: the template gives no room for extra bleed.
- Harrier's hanging-hole size is not published; key content is kept 12 mm clear of the top.
- A physical sample is still required before any production order. Nothing ordered, uploaded or published.

## Gate results (etsy/print_qa/preflight.py, fail-closed)
- Baubles option A: FAIL (MERRY CHRISTMAS 1.7 mm < 3.5 mm; logo letters 0.7 mm < 1.5 mm) - shown only to prove A is identical to the original.
- Baubles option B: PASS x3 (336 DPI, key content 6.7 mm inside, all colours approved, centring within 0.2 mm).
- Mugs v4: PASS x2 (6.2 / 6.4 mm inside, colours approved, centring 0.2 mm).
