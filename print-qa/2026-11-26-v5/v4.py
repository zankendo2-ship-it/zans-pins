"""v4 = Alex's ORIGINAL approved bauble artwork (live designer, style A, as printed 19 Nov) with technical print fixes only.
A = invisible fixes only: vector logo (same size/place), opacity flattened to the same solid colour, text outlined,
    full bleed (no clip), the thin gold edge ring removed (it sat 2 mm from the edge inside the 5 mm printer-shift band).
B = A + the two visible legibility fixes: MERRY CHRISTMAS letters 1.7 -> 3.5 mm, ZANS RACING TOOLS strip letters 0.7 -> 1.5 mm."""
import json, os, re, sys
sys.path.insert(0, '/tmp/claude-0/r1h/etsy/print_qa')
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
def fix(svg, cap, variant):
    s = svg
    s = s.replace('<g clip-path="url(#mc)">', '<g>')                                   # full bleed
    s = re.sub(r'<defs><clipPath id="mc">.*?</clipPath></defs>', '', s)
    s, n = re.subn(r'<circle cx="495" cy="495" r="469" fill="none" stroke="#C9A646" stroke-width="14"/>', '', s); assert n == 1  # edge ring
    m = re.search(r'stroke="(#\w{6})" stroke-width="16" stroke-linecap="round" opacity="0.7"', s)   # cap shine at 70 %
    f = [f for f in (1.25, 1.3, 1.6) if shade(cap, f).lower() == m.group(1).lower()][0]
    s = s.replace(m.group(0), f'stroke="{shade(cap, round(1 + 0.7 * (f - 1), 3))}" stroke-width="16" stroke-linecap="round"')
    s = s.replace('stroke="#b3b3b3"', 'stroke="#B3B3B3"').replace('fill="#b3b3b3"', 'fill="#B3B3B3"')
    m = re.search(r'<rect x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)" rx="90" fill="#F6F1E7" stroke="#C9A646" stroke-width="12"/>', s)
    s = s.replace(m.group(0), m.group(0).replace('<rect ', '<rect data-safe="1" data-centre="x" data-label="name panel" '))
    s = re.sub(r'<text ([^>]*font-weight="700" font-size="[\d.]+" letter-spacing="3"[^>]*)>', r'<text data-role="name" data-inside="name panel" \1>', s)
    mc = re.search(r'<text (x="495" y="([\d.]+)" text-anchor="middle" font-family="Jost" font-weight="600" font-size="32" letter-spacing="9.6" (fill="#\w+"))>MERRY CHRISTMAS</text>', s)
    if variant == 'A':
        s = s.replace(mc.group(0), mc.group(0).replace('<text ', '<text data-centre="x" data-inside="name panel" '))
    else:  # 3.5 mm letters = 66 px font; spacing kept in proportion (0.3 em) and fitted to the panel's text width
        fs, ls = 66.0, 0.3 * 66
        while outline.shape('MERRY CHRISTMAS', fs, 600, ls)[3] > 660: ls -= 0.5
        y = float(mc.group(2))   # original baseline
        s = s.replace(mc.group(0), f'<text data-centre="x" data-inside="name panel" x="495" y="{y:.1f}" text-anchor="middle" font-family="Jost" font-weight="600" font-size="{fs:.0f}" letter-spacing="{ls:.1f}" {mc.group(3)}>MERRY CHRISTMAS</text>')
    t = re.search(r'<rect x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)" rx="7" opacity="0.92" fill="#F6F1E7"/>', s)
    im = re.search(r'<image [^>]*x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)"/>', s)
    k = 1.0 if variant == 'A' else 2.2
    tx, ty, tw, th = (float(v) for v in t.groups()); cx, cy = tx + tw / 2, ty + th / 2
    TW, TH = tw * k, th * k
    if k > 1:   # bigger strip: move it up until its lowest corner is 6.2 mm inside the round face (centre x unchanged)
        bot = min(ty + th, 495 + ((495 - 6.2 * 990 / 74.9) ** 2 - (TW / 2) ** 2) ** 0.5); cy = bot - TH / 2
    tab = f'<rect data-safe="1" data-label="logo tab" x="{cx - TW / 2:.2f}" y="{cy - TH / 2:.2f}" width="{TW:.2f}" height="{TH:.2f}" rx="{7 * k:.2f}" fill="#F6F1E7"/>'
    ix, iy, iw, ih = (float(v) for v in im.groups())
    s = s.replace(t.group(0), tab).replace(im.group(0), logo(cx - iw / 2, cy - ih / 2 + (iy + ih / 2 - (ty + th / 2)), iw, ih, k))
    return s
def main():
    os.makedirs("out", exist_ok=True); res = {}
    for ref, code, cap, horse in ITEMS:
        orig = open(f'orig-{ref}.svg').read()
        for v in 'AB':
            svg = fix(orig, cap, v); base = f'out/{ref}-v4{v}'
            render.make(svg, base + '.png', 990, 990)
            design = dict(code=code, cap=cap); design.update({'horse': horse} if horse else {})
            json.dump(design, open(base + '.design.json', 'w')); json.dump(PAY, open(base + '.payload.json', 'w'))
            f, n = preflight.check('bauble_harrier', base + '.png', base + '.svg', PAY, design)
            res[f'{ref} {v}'] = (f, n); print(ref, v, 'FAIL' if f else 'PASS', f, n)
    json.dump(res, open('out/results.json', 'w'), indent=1)

if __name__ == "__main__": main()
