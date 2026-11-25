# ZANS print production workflow (PERMANENT - Alex + ChatGPT, 25 Nov 2026, v3)

Applies to EVERY physical product and EVERY order route (automatic and manual, Etsy and Alex's own orders, new suppliers too).

1. Customer personalises the product (Etsy design code + name). The design code's colours are the colours. Nothing is deepened,
   lightened or swapped (owner mandate 25 Nov). Named horses must match palette.json exactly.
2. Artwork = vector master from the designer (no bitmaps, no opacity, no gradients/blur/shadow/filters, strokes >= SKU minimum,
   key content tagged data-safe / data-centre, names tagged data-role="name").
3. render.py is the ONLY way a print PNG is made: outline every text with HarfBuzz + the self-hosted Jost (no font can change
   at the printer), render with Chromium at the EXACT template pixels, lossless PNG with sRGB IEC61966-2.1 embedded, and a
   provenance sidecar <png>.prov.json (renderer, size, sha256 of the PNG and of the master).
4. preflight.py (FAIL-CLOSED, every input mandatory): file (PNG, exact px, >= 300 DPI on both axes, sRGB, no transparency,
   size), binding (sidecar hashes match this PNG + this master), master (XML-parsed allowlist: no <image>/<style>/<text>/<use>/
   filters/masks/gradients/style=/external refs/foreign namespaces/opacity; strokes), text (letters >= 3.5 mm, names >= 6 mm on mugs, >= 4.0 mm on the 75 mm bauble face; names and logo text must sit inside their panel - data-inside),
   layout (key content >= 6 mm inside the edge - Printify says placement can move up to 5 mm - and out of the bauble hole
   keep-out; name panel / logo centred within 0.5 mm), colour (every fill in the master and every colour covering >= 0.3% of
   the PNG is the design code's own colour, a registry horse colour, a brand colour or the approved Cap A shading),
   payload (blueprint, provider, variant, placement front / .5 / .5 / 1 / 0).
5. PASS -> may go to the printer (approved templates + Alex-authorised live route only). FAIL -> BLOCKED, nothing uploaded.

Wired into: mug_orders.py (renders via render.py, a FAIL or a drawing error HOLDS the order), bauble_order.py,
own_bauble_order.py, own_bauble_multi.py (every item checked before any upload). print_gate.py turns any error into BLOCKED.
Proof: tests/ (66 tests - every check has a test where the defect must be blocked; the 25 Nov files are blocked;
routes run with no API key and must stop at the gate). print_selftest.py draws real files through the website designers and
gates them (GitHub: Actions > Print QA > Run workflow). .github/workflows/print-qa.yml runs the tests on every code change.

New products / suppliers / templates: Claude + ChatGPT independent approval AND a good physical sample before release.
Missing references (flagged, not guessed): Harrier's hanging-hole size/position (12 mm keep-out used until a sample is
measured); Printify file-size limits from Alex's spec, not re-verified. The traced horse logo (brand/) needs Alex's approval.
