# v3 print fix - what the website designers must change (SUPERSEDES print-qa/v2 and */corrected/)

Code: horse-racing-extraction- branch claude/project-thread-1htexo, etsy/print_qa/ (render.py, outline.py, preflight.py,
palette.json, sku_specs.json, tests). Port ONLY to the preview paths docs/bauble-designer-v2/ and docs/mug-designer-v2/.
Done = `python etsy/print_selftest.py out --mug-url <mug preview> --bauble-url <bauble preview> --strict` exits 0
(GitHub: Actions > Print QA > Run workflow, selftest=yes, mug_url/bauble_url = the previews, strict=yes).

## Bauble designer (reference: reference/fixC.js + gen_baubles.py)
1. Expose `ZANSBauble.printMaster()` = the print SVG at 990x990 with NO clip-path (full bleed; the PNG is rendered from it).
2. Colours = the design code's hexes EXACTLY. No darker/lighter variants. Only extra colours: palette.json brand colours and
   the Cap A shading shade(cap, 0.7 / 1.3 / 1.25 / 1.6).
3. Lettering colour = the design's darker colour if contrast on cream #F6F1E7 >= 4.5:1, else ink #1C1C1C (no invented shade).
4. No opacity / fill-opacity anywhere (cap shine etc. must be solid colour), no filters, no <image>, no <style>.
5. Strokes >= 20 px (1.5 mm) - cap seams included.
6. Name panel 760 px wide centred on x=495 (tags: data-safe="1" data-centre="x" data-label="name panel");
   name text fitted to 640 px (data-role="name" data-inside="name panel"), Jost 700, letters >= 4.0 mm (53 px cap height);
   MERRY CHRISTMAS 66 px Jost 700 (>= 3.5 mm letters).
7. Logo = the traced vector horse (etsy/print_qa/brand/zans_horse_mark_traced_v1.svg) in a cream tab with gold border, 150 px,
   centred (data-centre="x"); no bitmap logo. Pending Alex's approval of the trace.
8. Keep every key item >= 6 mm (79 px) inside the circle and out of the 12 mm keep-out at the top centre (hanging hole).

## Mug designer (reference: reference/gen_mug.py)
1. Print SVG at the template size (Harrier 2475x1155, white T Shirt and Sons 2582x1120), centre = w/2 (old file centred at 2700).
2. Logo = traced horse + "ZANS RACING TOOLS" Jost 700 62 px, letter-spacing 2, in a #FBF7F0 tab WIDE ENOUGH for the text
   + 34 px each side (v3 first draft let TOOLS run off the tab - caught 25 Nov; preflight now checks data-inside="logo tab").
3. Name plates scaled so they sit >= 6 mm inside the top/bottom edge (live layout was 4.4 mm from the bottom).
4. Line under the cap band >= 24 px (2 mm). No opacity, no <image>, no <style>. Names >= 6 mm letters.
