# ZANS print production workflow (PERMANENT - Alex + ChatGPT, 25 Nov 2026)

Applies to EVERY physical product and EVERY order route (automatic and manual, Etsy and Alex's own orders, new suppliers too).

1. Customer personalises the product (Etsy design code + name).
2. Artwork is generated from the approved VECTOR master: locked silks hexes (never darkened without Alex's yes), vector text and branding, no embedded bitmaps, no semi-transparency, gradients, blur or shadows.
3. Export for the supplier: EXACT template pixels for that blueprint + provider (not stretched, not oversized), 300 DPI or more at real size, sRGB IEC61966-2.1 embedded, lossless PNG, full bleed (no transparency) on wrap/round products.
4. Automatic FAIL-CLOSED preflight (print_qa/preflight.py): template size, DPI, ICC, transparency/halos, file size, master has no bitmap / semi-transparency / gradient, strokes >= SKU minimum (1.5 mm bauble, 1.0 mm mug), Printify payload blueprint + variant + placement (front, x .5, y .5, scale 1, angle 0).
5. PASS -> may go to the printer (approved templates + Alex-authorised live route only). FAIL -> BLOCKED, nothing uploaded; fix the artwork and re-run; unresolved = manual review.

Layout rules (not all automatic yet - checked by eye + measured on the proof): key content 6 mm inside the edge, no thin rings/borders near the edge, name panel measured dead centre, text 3.5 mm+ (names 6 mm+), contrast 7:1 on light panels.
New products / suppliers / templates: Claude + ChatGPT independent approval AND a good physical sample before release.

Per-SKU specs: print_qa/sku_specs.json. Tests proving bad files are blocked: print_qa/tests (pytest).
Open: provider file-size/format limits taken from Alex's spec (Printify 100 MB raster / 20 MB SVG), not re-verified against Printify docs; safe-zone and centring are measured on proofs, not yet automatic; 2x upload not used (exact template size instead).
