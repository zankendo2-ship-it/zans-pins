"""Bauble-style personalised mug (Alex 26 Nov 12:00 "I want a mug designing like the baulbel"; confirmed 16:28; "Start now" 16:53).
Built ONLY from the approved v9 bauble masters (vector): same silks body pattern, cap with seams + button (NO shine, no outer ring),
gold-trimmed cap peak, gold-bordered cream name panel with the same outlined lettering, and the approved mug's own ZANS logo strip.
Every bauble element is scaled by S (same proportions as the bauble, 17% bigger in mm so the name meets the mug 6 mm minimum).
Two faces (left-hand and right-hand drinker) at 1/4 and 3/4 of the wrap; wrap seam at the handle (both ends), logo at the back
centre exactly where the approved FACT TO FILE mug has it."""
import json, re, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'tools', 'print_drafts', 'print_qa'))
import render, preflight
B = os.path.join(HERE, 'inputs', '{}-v9.svg')
MUG = os.path.join(HERE, 'inputs', 'fact-to-file-mug-2475x1155-v4.svg')
W, H, MM = 2475, 1155, 209.55
S = (W / MM) / (990 / 74.9) * 6.2 / 5.3   # 1.045: bauble design scaled up 17% so the name letters are 6.2 mm (mug minimum 6 mm; bauble 5.3 mm)
FACES = (W / 4, 3 * W / 4)
APEX_MM = 6.2 + 24 * S / (W / MM) - 2 * S / (W / MM)   # centre of the button so its top edge is 6.2 mm from the top
PANEL_CY = 600                          # name panel centre on the mug (bauble: 545 of 990)
ITEMS = [('lossiemoo', 'ZBA-disc-F3B5C9-6CC24A-plain-F3B5C9', '#F3B5C9', 'lossiemouth'),
         ('zoo-olympios', 'ZBA-spot_diag-F5D130-1C1C1C-plain-1C1C1C', '#1C1C1C', None),
         ('rexs-romance', 'ZBA-plain-1C4FA0-FFFFFF-plain-FFFFFF', '#FFFFFF', None)]

import math
D_BRIM = None
def brim_y(x, y0, depth):
    """Brim: one scallop per face, y = y0 + depth*sin^2 - zero slope where faces meet (handle + back), so no cusp."""
    u = (x % (W / 2)) / (W / 2)
    return y0 + depth * math.sin(math.pi * u) ** 2

def pattern(svg):
    """The bauble body pattern laid round the wrap in the SAME phase around each face as around the bauble's centre
    (x 495, panel centre 545); x step nudged to an EVEN number of repeats so it meets itself at the seam and both faces match."""
    bg = re.search(r'<rect x="0" y="0" width="990" height="990" fill="(#\w{6})"/>', svg).group(1)
    cs = [(float(a), float(b), float(r), f) for a, b, r, f in re.findall(r'<circle cx="([-\d.]+)" cy="([-\d.]+)" r="([\d.]+)" fill="(#\w{6})"/>', svg)]
    cs = [c for c in cs if not (c[0] == 495 and c[1] == 30)]          # the cap button is not pattern
    out = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="{bg}"/>']
    if not cs: return out, bg
    ys = sorted({c[1] for c in cs}); row = {y: sorted(c[0] for c in cs if c[1] == y) for y in ys}
    step = row[ys[0]][1] - row[ys[0]][0]; dy = ys[1] - ys[0]; r = cs[0][2]; f = cs[0][3]
    delta = (row[ys[1]][0] - row[ys[0]][0]) % step
    n = 2 * round(W / (step * S) / 2); sx = W / n; k = sx / (step * S)
    cx1 = FACES[0]
    for j in range(-6, 12):
        yb = ys[0] + j * dy; y = PANEL_CY + (yb - 545) * S
        if y + r * S < 0 or y - r * S > H: continue
        ob = (row[ys[0]][0] + j * delta) % step
        mlo = math.floor(((-r * S - cx1) / (S * k) + 495 - ob) / step) - 1
        m = mlo
        while True:
            x = cx1 + (ob + m * step - 495) * S * k
            if x - r * S > W: break
            if x + r * S >= 0: out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r * S:.1f}" fill="{f}"/>')
            m += 1
    return out, bg

def cap(svg):
    band = re.search(r'<path d="M0,0 H990 V185 Q495,250 0,185 Z" fill="(#\w{6})"/>', svg).group(1)
    sc = re.findall(r'<path d="M495,28 Q[^"]+" fill="none" stroke="(#\w{6})" stroke-width="7" stroke-linecap="round"/>', svg)[0]
    y0, depth = 185 * S, 32.5 * S                       # same brim depth as the bauble's curve (185 -> 217.5 at the centre)
    xs = [i * W / 400 for i in range(401)]
    line = ' '.join(f'L{x:.1f},{brim_y(x, y0, depth):.2f}' for x in xs)
    out = [f'<path d="M0,0 H{W} V{y0:.1f} ' + ' '.join(f'L{x:.1f},{brim_y(x, y0, depth):.2f}' for x in reversed(xs)) + ' Z" fill="{}"/>'.format(band)]
    for cx in FACES:   # seams + button copied from the bauble cap, same order (no shine anywhere)
        # supplier trim: top button must sit >= 6.2 mm inside the top edge. Seams are squeezed vertically about the brim
        # (y -> y0 + k (y - y0)), the button stays a true circle at the new apex. Shapes and colours unchanged.
        k = (y0 / S - APEX_MM * (W / MM) / S) / (y0 / S - 28)
        g = f'<g transform="translate({cx - 495 * S:.2f},{y0 * (1 - k):.2f}) scale({S:.5f},{S * k:.5f})">'
        for m in re.finditer(r'<path d="(M495,28 Q[^"]+)" fill="none" stroke="#\w{6}" stroke-width="7" stroke-linecap="round"/>', svg):
            g += f'<path d="{m.group(1)}" fill="none" stroke="{sc}" stroke-width="8.2" stroke-linecap="round"/>'
        g += '</g>'
        out.append(g)
        out.append(f'<circle cx="{cx:.2f}" cy="{APEX_MM * (W / MM) + 2 * S:.2f}" r="{24 * S:.2f}" fill="{sc}"/>')
    pk = re.search(r'<path d="M225,219 [^"]+" fill="(#\w{6})" stroke="#C9A646" stroke-width="7"/>', svg).group(1)
    for cx in FACES:
        # peak: its top edge IS the brim (no body-colour gap); corners and underside = the bauble peak (M225,219 ... Q745,295
        # 495,303 Q245,295 225,219), dropped so its corners sit on the brim
        xl, xr = cx - 270 * S, cx + 270 * S; yl = brim_y(xl, y0, depth); dd = yl - 219 * S
        top = ' '.join(f'L{x:.1f},{brim_y(x, y0, depth):.2f}' for x in [xl + i * (xr - xl) / 60 for i in range(61)])
        P = lambda a, b: f'{cx + (a - 495) * S:.2f},{b * S + dd:.2f}'
        d = f'M{xl:.2f},{yl:.2f} {top} Q{P(745, 295)} {P(495, 303)} Q{P(245, 295)} {xl:.2f},{yl:.2f} Z'
        out.append(f'<path d="{d}" fill="{pk}" stroke="#C9A646" stroke-width="{7.2 * S:.2f}"/>')
    out.append(f'<path d="M0,{y0:.1f} {line}" fill="none" stroke="#C9A646" stroke-width="{8 * S:.2f}"/>')
    return out

def face(svg, cx, side):
    a = svg.index('<rect data-safe="1" data-centre="x" data-label="name panel"'); b = svg.index('<rect data-safe="1" data-label="logo tab"')
    body = svg[a:b]
    lab = f'name panel {side}'
    body = body.replace('data-centre="x" data-label="name panel"', f'data-centre="x@{cx:.2f}" data-label="{lab}"')
    body = body.replace('data-inside="name panel"', f'data-inside="{lab}"')
    body = re.sub(r'data-text="([^"]+)" (data-font-size="[\d.]+") data-role="name"', lambda m: f'data-text="{m.group(1)}" {m.group(2)} data-role="name" data-label="{m.group(1)} {side}" data-centre="x@{cx:.2f}"', body)
    ty = PANEL_CY - 545 * S
    return f'<g transform="translate({cx - 495 * S:.2f},{ty:.2f}) scale({S:.5f})">{body}</g>'

def logo():
    m = open(MUG).read()
    a = m.index('<rect data-safe="1" data-centre="x" data-label="logo tab"'); return m[a:m.rindex('</svg>')]

def build(ref, code, capcol, horse):
    svg = open(B.format(ref)).read()
    pat, bg = pattern(svg)
    parts = pat + cap(svg) + [face(svg, cx, s) for cx, s in zip(FACES, ('L', 'R'))] + [logo()]
    out = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + ''.join(parts) + '</svg>'
    os.makedirs(os.path.join(HERE, 'out'), exist_ok=True); base = os.path.join(HERE, 'out', f'{ref}-bauble-style-mug-{W}x{H}')
    render.make(out, base + '.png', W, H)
    pay = dict(position='front', x=.5, y=.5, scale=1, angle=0, blueprint_id=635, print_provider_id=94, variant_id=72180)
    des = dict(code=code, cap=capcol, **({'horse': horse} if horse else {}))
    json.dump(pay, open(base + '.payload.json', 'w')); json.dump(des, open(base + '.design.json', 'w'))
    f, nn = preflight.check('mug_harrier_11oz', base + '.png', base + '.svg', pay, des)
    print(ref, 'FAIL' if f else 'PASS', f, nn); return not f

if __name__ == '__main__':
    ok = [build(*it) for it in ITEMS]; sys.exit(0 if all(ok) else 1)
