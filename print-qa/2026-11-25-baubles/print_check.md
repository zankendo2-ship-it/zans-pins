# Bauble print check - 25 Nov (Loussiemoo, Rexs Romance, Zoo Olympios)

Files checked: horse repo branch claude/project-thread-1htexo, etsy/orders/own-*.png (the exact files uploaded to Printify).
Placement (etsy/own_bauble_order.py): Harrier round ceramic 2.95", front only, centred x .5 y .5, scale 1, angle 0.

| Check | Result | Verdict |
|---|---|---|
| Pixel size | 3960 x 3960 PNG, raster (drawn as vector, rasterised at 4x) | OK |
| Effective DPI on a 2.95" face | ~1,340 DPI | OK - resolution is NOT the cause |
| Sharpness at 100% | lettering edges crisp (see crop) | OK - file is not blurry |
| Colour profile | none embedded (plain sRGB) | RISK - no adjustment for ceramic sublimation |
| Bleed | full-square background | OK |
| Gold outer ring | starts 76 px (about 1.4 mm) in from the edge, 1 mm wide | FAULT - inside the 1-3 mm printing tolerance, so any shift makes it look off centre |
| Small text | MERRY CHRISTMAS about 1.7 mm tall, thin, lime green on cream; logo text about 1 mm | FAULT - too small and low contrast for sublimation, prints soft |
| Colours | pastel pink 243/181/201, lime 108/194/74, mid blue 28/79/160 | FAULT - pale tones wash out on glazed ceramic |

Root cause: BOTH. Our artwork put a thin ring right at the edge, used tiny low-contrast text and pastel colours,
with no ceramic colour adjustment. Printing then shifted slightly and softened, as sublimation always does.
The resolution was fine.

Fix (for the code chat to make, then checked here before any order):
1. Remove the thin outer ring (or make it 3 mm+ wide and 5 mm+ inside the edge); keep all key content inside a 6 mm safe zone.
2. Name text at least 6 mm tall, bold; drop or enlarge MERRY CHRISTMAS to 3.5 mm+ in dark ink on a light panel (or white on dark).
3. Deeper, more saturated colours (pink, lime, blue) for ceramic; dark text outlines where colours meet.
4. Pre-order print check (fixed step before ANY order): resolution, safe zone + centring, colour, text size/contrast - pass on the file, a flat proof shown to Alex, his yes.
