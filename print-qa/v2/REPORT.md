# Print fix v2 - checked against Alex's POD spec (25 Nov 17:23) + ZANS rules

Built from vector (SVG) masters, exported straight from the vector at the EXACT Printify template size (no stretching, no oversize).
Automatic check: print-qa/preflight.py (fail-closed, exit 1 = order must stop). All 7 files PASS.

| Spec item | Baubles (6 files: 3 designs x approved / deeper colours) | Mug FACT TO FILE |
|---|---|---|
| Exact template pixels | 990 x 990 (Harrier bp 1676, 2.95" round) | 2475 x 1155 (Harrier bp 635, 11oz) |
| 300 DPI at real size | 336 DPI | 300 DPI |
| sRGB IEC61966-2.1 embedded | yes | yes |
| PNG, lossless | yes | yes |
| Vector master, no bitmap inside | yes (master-*.svg, 0 images) | yes (horse bitmap logo replaced by vector text) |
| No semi-transparent gradients/shadows | yes (cap shine + logo tab made solid) | yes |
| No edge halos / transparency | yes, full bleed, no alpha | yes, full bleed |
| Lines >= 1 mm (ZANS 1.5 mm) | thinnest 1.5 mm (cap seams, panel + mark borders) | white line under cap band 2.0 mm; plate borders 1.2 mm |
| Text >= 3.5 mm, bold, high contrast | name 6 mm+, MERRY CHRISTMAS ~3.5 mm, ZANS 3.6 mm; contrast 7.4:1 or better | name ~17 mm, ZANS RACING TOOLS 3.6 mm |
| Background to bleed, text in safe zone | name panel 10.9 mm+ and ZANS mark 13.2 mm inside the edge | plates 7.7 mm from both wrap ends |
| Centring | name panel 0.0 mm off centre (was 3.8 mm low) | logo strip 0.2 mm off centre (was 9.5 mm right - placed for the old 2700 px canvas); plates equal 7.7 / 7.7 mm |

Silks colours: "approved" files keep Alex's exact hexes; "deeper" files are an option only (Alex chooses).
Open points: the horse logo has no vector master (bauble shows ZANS only, mug shows ZANS RACING TOOLS text - Alex to confirm);
the cap seams/button at the very top of the bauble are background and may be cut by the edge; outlined-text variant not made yet;
a physical sample is still needed before any more orders.
