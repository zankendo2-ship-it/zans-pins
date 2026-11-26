# Offline placement proof (26 Nov 2026) - answers ChatGPT 7180745343 step 1
These are OFFLINE overlays: our print files on the Printify placeholder sizes. They are NOT Printify mock-ups. Nothing was uploaded.

## Template source (Printify's own records, saved in the racing repo reports/)
| Product | Record | Placeholder | Our file |
|---|---|---|---|
| Bauble | catalog blueprints/1676/print_providers/94/variants: variant 115590, 2.95'' x 2.95'' Round, front, dye-sublimation | 990 x 990 | 990 x 990, x .5 y .5 scale 1 |
| Harrier 11oz mug | live product 6aeb63... (bp 635 / pp 94) print_areas | front 2475 x 1155, x .5 y .5 scale 1 | 2475 x 1155, same |
| White 11oz mug | live product 6af037... (bp 535 / pp 6) print_areas | front 2582 x 1120, x .5 y .5 scale 1 | 2582 x 1120, same |

## Files
- `Baubles v5 placement proof.png`: print area, finished face circle, 5 mm shift band, 6 mm safe zone, centre lines, 12 mm hole keep-out (our estimate).
- `FACT TO FILE mug v5 placement proof 2475x1155.png` / `...2582x1120.png`: placeholder, 6 mm safe zone, centre lines.
- `Baubles v5 actual size proof (print at 100%).pdf` + `actual size proof - page 1 render.png`: rendered and MEASURED with PyMuPDF. 1 page A4. The 50 mm bar measures 50.01 mm. The left column baubles measure 74.88 mm. The right column measures 75.14 x 74.88 mm (browser pixel snap, 0.3 %).
- `preflight-log.txt`: gate output for all 5 files, plus a NEGATIVE test. FACT is shrunk to 30 px, and the gate BLOCKS it with "letters 1.9 mm tall < 6 mm". That proves the mug name rule now runs.

## Still open (cannot be closed offline)
- Mug handle position relative to the artwork: not in the Printify data we hold. Needs a Printify mock-up (a draft product = upload) or the sample.
- Harrier hanging-hole size: not published. The 12 mm keep-out is our estimate.
- Real print tolerance, sharpness, and the Loussiemoo 2:1 green contrast: physical sample only.
