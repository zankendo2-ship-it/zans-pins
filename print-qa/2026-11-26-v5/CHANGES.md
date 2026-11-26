# Print fix v5 (26 Nov 2026) - answers ChatGPT REVISE 7179585428 on v4 (9b53119)

ONE corrected version per bauble (no options). Baubles: original approved artwork (style A live designer, as printed 19 Nov) + technical print fixes.
Mugs: print files pixel-identical to v4 (only a gate tag added, see below).

## Invisible fixes (same as v4 A)
1. All text outlined (no font can change at the printer).
2. ZANS logo redrawn as vector (was a small bitmap = blur).
3. Cap shine transparency flattened to the same solid colour (palette rule flattened_shine).
4. Full bleed (round clip + its def removed).

## Visible changes, each with its reason
| # | Change | Original | v5 | Reason |
|---|---|---|---|---|
| V1 | Thin gold edge ring removed | ring 2 mm from the edge | none | sat inside the printer's shift band - any shift shows it off centre (ChatGPT PASS) |
| V2 | MERRY CHRISTMAS size + weight | capitals 1.7 mm, weight 600, 433 px wide | capitals 2.55 mm, LIGHTER weight 500, 0.3 em spacing capped at 540 px wide, same baseline | 1.7 mm (~7 pt) is below print guidance; the lighter weight keeps the name (700, unchanged) dominant |
| V3 | ZANS RACING TOOLS strip | capitals 0.7 mm, tab 181 x 34 px | capitals 1.52 mm (smallest that meets 1.5 mm), tab = logo + ORIGINAL padding (not scaled), raised only as far as the 6 mm safe zone needs | 0.7 mm (~3 pt) cannot print sharply; v4 B scaled the padding too (2.2x) - v5 keeps the tab tight |
| V4 | Cap peak gold edge | 6 px = 0.45 mm | 7 px = 0.53 mm (same as the cap seams) | Printify minimum stroke 0.5 mm |

Not changed: name text, spelling, letter spacing and size of the names, panel size and position, every colour (hex list identical to v4 A), Loussiemoo green on cream (low contrast 2.0:1 stays a physical-proof gate - not recoloured).

## Where the minimum sizes come from (supplier/industry evidence)
No Harrier or T Shirt and Sons figure is published. The gate now uses published print guidance instead of our own unsourced numbers (old: text 3.5 mm, stroke 0.4 mm):
- Printify, common print file mistakes: "keep every stroke at or above 1.5pt (0.5mm)" -> min_stroke_mm 0.5 (STRICTER than before).
- Sticker Mule, minimum font size: "6 pt font is the minimum size we recommend" -> 6 pt Jost = ~1.5 mm capitals -> min_logo_text_mm 1.5.
- Printful, design file guidelines: font sizes "generally between 10 and 12 pts" -> min_text_mm 2.5 (~10 pt Jost capitals). Names keep 4 mm (bauble) / 6 mm (mug).
These are guidance, not a Harrier guarantee: the PHYSICAL SAMPLE stays the release gate.

## Actual-size proof
"Baubles v5 actual size proof (print at 100%).pdf": original and v5 at 74.9 mm, with a 50 mm check bar. Shows size/legibility only - colour and sharpness need the supplier sample.

## Mugs
- Print files = v4 (pixel-identical; ChatGPT PASS on visual fidelity V4/V5 mug).
- Gate fix: FACT / TO FILE now tagged as names, so the 6 mm mug name rule actually runs on mugs (it was not applied before). Both templates PASS.
- No real-silks claim: custom code kept, not marketed as JP McManus silks (red cap/strip + gold/orange dispute open).
- Still needed: Printify template placement proof (needs a Printify draft product = an upload, so Alex's yes first) + physical sample. No order.

## Gate results (preflight, racing repo claude/project-thread-1htexo 50b3d08b7)
Loussiemoo / Zoo Olympios / Rexs Romance v5: PASS (336 DPI, 6.4 mm safe, colours approved, centred within 0.2 mm). Mugs 2475 + 2582: PASS. 68 gate tests pass.
