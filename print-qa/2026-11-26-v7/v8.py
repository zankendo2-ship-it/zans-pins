"""v8 (26 Nov 12:00, Alex "not correct" + ChatGPT 7191426833): cap shine moved under the seams so no seam is cut.
v7 (26 Nov 11:02, Alex: "Perfect but keep the logo the original size please") = v6 with the logo back at its original size (variant A logo, k=1).
v6 (26 Nov, Alex: identical to the original): v5 minus the greeting change. Only print-required changes remain:
edge ring removed (2 mm from the edge, inside Printify's up-to-5 mm placement shift), logo letters 0.7 -> 1.52 mm (below the 1.5 mm minimum),
cap peak line 0.45 -> 0.53 mm (Printify 0.5 mm minimum). Invisible: outlined text, vector logo, flattened shine, full bleed."""
"""v4 = Alex's ORIGINAL approved bauble artwork (live designer, style A, as printed 19 Nov) with technical print fixes only.
A = invisible fixes only: vector logo (same size/place), opacity flattened to the same solid colour, text outlined,
    full bleed (no clip), the thin gold edge ring removed (it sat 2 mm from the edge inside the 5 mm printer-shift band).
B = A + the two visible legibility fixes: MERRY CHRISTMAS letters 1.7 -> 3.5 mm, ZANS RACING TOOLS strip letters 0.7 -> 1.5 mm."""
import json, os, re, sys
sys.path.insert(0, '/tmp/claude-0/zp/tools/print_drafts/print_qa')
import render, preflight, outline
P1 = open('/tmp/claude-0/v3/horse_paths.txt').read().split('\n')[0]
PAY = dict(position='front', x=.5, y=.5, scale=1, angle=0, blueprint_id=1676, print_provider_id=94, variant_id=115590)
ITEMS = [('loussiemoo', 'ZBA-disc-F3B5C9-6CC24A-plain-F3B5C9', '#F3B5C9', 'lossiemouth'),
         ('zoo-olympios', 'ZBA-spot_diag-F5D130-1C1C1C-plain-1C1C1C', '#1C1C1C', None),
         ('rexs-romance', 'ZBA-plain-1C4FA0-FFFFFF-plain-FFFFFF', '#FFFFFF', None)]
shade = preflight.shade   # same rounding as the designer (JS Math.round)
def logo(x, y, w, h, k=1.0):
    # vector copy of the designer's bitmap strip (750x100): horse+ZANS mark at the left, ZANS RACING TOOLS in Jost 700
    W, H = w * k, h * k; x0 = x + (w - W) / 2; y0 = y + (h - H) / 2
    mh = H; mw = 850 * mh / 895
    tx = x0 + 112 / 750 * W; tw = (740 - 112) / 750 * W
    fs = 20.0
    for _ in range(30):
        _, _, _, wd = outline.shape('ZANS RACING TOOLS', fs, 700, 0); fs *= tw / wd
    base = y0 + 0.78 * H
    return (f'<g data-safe="1" data-centre="x" data-label="ZANS logo" data-inside="logo tab">'
            f'<g transform="translate({x0:.2f},{y0:.2f}) scale({mh / 895:.6f})"><path d="{P1}" fill="#1C1C1C"/></g>'
            f'<text data-role="logo" x="{tx:.2f}" y="{base:.2f}" font-family="Jost" font-weight="700" font-size="{fs:.2f}" fill="#1C1C1C">ZANS RACING TOOLS</text></g>')
PXMM = 990 / 74.9
GREET_MM = 2.55
def logo_cap(iw, ih, k):
    W = iw * k; tw = (740 - 112) / 750 * W; fs = 20.0
    for _ in range(30):
        _, _, _, wd = outline.shape('ZANS RACING TOOLS', fs, 700, 0); fs *= tw / wd
    return fs * 0.70 / PXMM
def logo_k(iw, ih):
    return round(1.52 / logo_cap(iw, ih, 1.0), 3)
def fix(svg, cap, variant):
    s = svg
    s = s.replace('<g clip-path="url(#mc)">', '<g>')                                   # full bleed
    s = re.sub(r'<defs><clipPath id="mc">.*?</clipPath></defs>', '', s)
    s, n = re.subn(r'<circle cx="495" cy="495" r="469" fill="none" stroke="#C9A646" stroke-width="14"/>', '', s); assert n == 1  # edge ring
    m = re.search(r'stroke="(#\w{6})" stroke-width="16" stroke-linecap="round" opacity="0.7"', s)   # cap shine at 70 %
    f = [f for f in (1.25, 1.3, 1.6) if shade(cap, f).lower() == m.group(1).lower()][0]
    s = s.replace(m.group(0), f'stroke="{shade(cap, round(1 + 0.7 * (f - 1), 3))}" stroke-width="16" stroke-linecap="round"')
    # v8 (Alex 26 Nov 12:00 "not correct"): the solid shine sat ON TOP of the outer-left seam and cut it (broken line, stray
    # fragment). Draw the shine first, so all 4 seams run continuous over it; shine colour and shape unchanged.
    sh = re.search(r'<path d="M195,155 Q265,70 455,48"[^>]*/>', s).group(0); s = s.replace(sh, '')
    first_seam = re.search(r'<path d="M495,28 Q346\.5,78\.8 165,187\.2"', s).group(0); s = s.replace(first_seam, sh + first_seam, 1)
    s, n = re.subn(r'(fill="#\w{6}" stroke="#C9A646") stroke-width="6"', r'\1 stroke-width="7"', s); assert n == 1   # peak gold edge 0.45 -> 0.53 mm (Printify 0.5 mm minimum)
    s = s.replace('stroke="#b3b3b3"', 'stroke="#B3B3B3"').replace('fill="#b3b3b3"', 'fill="#B3B3B3"')
    m = re.search(r'<rect x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)" rx="90" fill="#F6F1E7" stroke="#C9A646" stroke-width="12"/>', s)
    s = s.replace(m.group(0), m.group(0).replace('<rect ', '<rect data-safe="1" data-centre="x" data-label="name panel" '))
    s = re.sub(r'<text ([^>]*font-weight="700" font-size="[\d.]+" letter-spacing="3"[^>]*)>', r'<text data-role="name" data-inside="name panel" \1>', s)
    mc = re.search(r'<text (x="495" y="([\d.]+)" text-anchor="middle" font-family="Jost" font-weight="600" font-size="32" letter-spacing="9.6" (fill="#\w+"))>MERRY CHRISTMAS</text>', s)
    if variant in ('A', 'D'):   # D (v6): Alex's ORIGINAL greeting - same size 1.7 mm, weight 600, spacing, baseline (above the 1.5 mm hard minimum)
        s = s.replace(mc.group(0), mc.group(0).replace('<text ', '<text data-role="small" data-centre="x" data-inside="name panel" '))
    else:  # C: 2.55 mm letters (= 48.2 px font, ~10 pt), LIGHTER weight 500 (name stays 700), original 0.3 em spacing, original baseline
        fs = round(GREET_MM * PXMM / 0.70, 1); ls = round(0.3 * fs, 1)
        while outline.shape('MERRY CHRISTMAS', fs, 500, ls)[3] > 540: ls -= 0.5   # no wider than 540 px (original 433 px) so the panel keeps its margins
        y = float(mc.group(2))
        s = s.replace(mc.group(0), f'<text data-centre="x" data-inside="name panel" x="495" y="{y:.1f}" text-anchor="middle" font-family="Jost" font-weight="500" font-size="{fs:.1f}" letter-spacing="{ls:.1f}" {mc.group(3)}>MERRY CHRISTMAS</text>')
    t = re.search(r'<rect x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)" rx="7" opacity="0.92" fill="#F6F1E7"/>', s)
    im = re.search(r'<image [^>]*x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)"/>', s)
    tx, ty, tw, th = (float(v) for v in t.groups()); cx, cy = tx + tw / 2, ty + th / 2
    ix, iy, iw, ih = (float(v) for v in im.groups())
    k = 1.0 if variant == 'A' else logo_k(iw, ih)   # smallest scale that gives 1.52 mm logo letters
    padx, pady = (iw and (tw - iw) / 2), (th - ih) / 2      # ORIGINAL padding kept in px (tab not scaled beyond the logo)
    TW, TH = (tw, th) if k == 1 else (iw * k + 2 * padx, ih * k + 2 * pady)
    if k > 1:   # bigger strip: move it up until its lowest corner is 6.2 mm inside the round face (centre x unchanged)
        bot = min(ty + th, 495 + ((495 - 6.2 * 990 / 74.9) ** 2 - (TW / 2) ** 2) ** 0.5); cy = bot - TH / 2
    tab = f'<rect data-safe="1" data-label="logo tab" x="{cx - TW / 2:.2f}" y="{cy - TH / 2:.2f}" width="{TW:.2f}" height="{TH:.2f}" rx="7" fill="#F6F1E7"/>'
    s = s.replace(t.group(0), tab).replace(im.group(0), logo(cx - iw / 2, cy - ih / 2 + (iy + ih / 2 - (ty + th / 2)), iw, ih, k))
    return s
def main():
    os.makedirs("out8", exist_ok=True); res = {}
    for ref, code, cap, horse in ITEMS:
        orig = open(f'orig-{ref}.svg').read()
        for v in "A":
            svg = fix(orig, cap, v); base = f'out8/{ref}-v8'
            render.make(svg, base + '.png', 990, 990)
            design = dict(code=code, cap=cap, owner_waivers={'logo_text_mm': dict(value=0.68, by='Alex', source='cmsg_017LpptpymmcJZuGHLNRtGrsWh1B1WDPh3cT1yyLN6NSHm', at='2026-11-26T11:02Z', words='keep the logo the original size please')}); design.update({'horse': horse} if horse else {})
            json.dump(design, open(base + '.design.json', 'w')); json.dump(PAY, open(base + '.payload.json', 'w'))
            f, n = preflight.check('bauble_harrier', base + '.png', base + '.svg', PAY, design)
            res[f'{ref} {v}'] = (f, n); print(ref, v, 'FAIL' if f else 'PASS', f, n)
    json.dump(res, open('out8/results.json', 'w'), indent=1)

if __name__ == "__main__": main()
