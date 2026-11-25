# Mug print check - 25 Nov

Only one mug has ever been printed: Alex's test mug FACT TO FILE (Etsy test order, 2 Nov, Harrier bp 635, black handle). No customer mug orders yet (etsy/mug_orders_done.json).

| Check | Result | Verdict |
|---|---|---|
| Pixel size | 2475 x 1155 RGB = Harrier print area at 1x (about 300 DPI) | FAULT - 1x, no oversample; printer resample softens edges. The 2x rule (5 Nov) was put in the website order tool, but the automatic order script etsy/mug_orders.py STILL renders at 1x (2475x1155, white mug 2582x1120) |
| ICC profile | none | RISK |
| Logo strip | ZANS RACING TOOLS about 2 mm tall, small bitmap logo | FAULT - too small, the logo is a low-res bitmap |
| Thin white line under the cap band | about 8 px = 0.7 mm | FAULT - hairline, prints uneven |
| Name text | about 17 mm tall, bold, green on cream | OK |
| Edges | name plates about 5 mm in from left/right ends | borderline - handle seam area |

Root cause: our file. Fix: render at 2x (4950x2310) in mug_orders.py and every mug route, embed sRGB, logo as vector or 3 mm+ text, no hairlines under 1.5 mm, name plates 8 mm+ from the wrap ends. Corrected file to #26 before any order.
