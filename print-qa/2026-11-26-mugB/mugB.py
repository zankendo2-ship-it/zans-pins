"""Bauble-style personalised mug (Alex 26 Nov 12:00 "I want a mug designing like the baulbel"; confirmed 16:28; "Start now" 16:53).
Built ONLY from the approved v9 bauble masters (vector): same silks body pattern, cap with seams + button (NO shine, no outer ring),
gold-trimmed cap peak, gold-bordered cream name panel with the same outlined lettering, and the approved mug's own ZANS logo strip.
Every bauble element is scaled by S (same proportions as the bauble, 17% bigger in mm so the name meets the mug 6 mm minimum).
Two faces (left-hand and right-hand drinker) at 1/4 and 3/4 of the wrap; wrap seam at the handle (both ends), logo at the back
centre exactly where the approved FACT TO FILE mug has it."""
import json, re, sys, os
sys.path.insert(0, '/tmp/claude-0/zp/tools/print_drafts/print_qa')
import render, preflight
B = '/tmp/claude-0/zp/print-qa/2026-11-26-v7/out9/{}-v9.svg'
MUG = '/tmp/claude-0/zp/print-qa/2026-11-25-v4/fact-to-file-mug-2475x1155-v4.svg'
W, H, MM = 2475, 1155, 209.55
S = (W / MM) / (990 / 74.9) * 6.2 / 5.3   # 1.045: bauble design scaled up 17% so the name letters are 6.2 mm (mug minimum 6 mm; bauble 5.3 mm)
FACES = (W / 4, 3 * W / 4)
PANEL_CY = 600                          # name panel centre on the mug (bauble: 545 of 990)
ITEMS = [('loussiemoo', 'ZBA-disc-F3B5C9-6CC24A-plain-F3B5C9', '#F3B5C9', 'lossiemouth'),
         ('zoo-olympios', 'ZBA-spot_diag-F5D130-1C1C1C-plain-1C1C1C', '#1C1C1C', None),
         ('rexs-romance', 'ZBA-plain-1C4FA0-FFFFFF-plain-FFFFFF', '#FFFFFF', None)]

def pattern(svg):
    """Re-tile the bauble's body pattern across the wrap at the same physical size; the x step is nudged (<3%) so the
    pattern meets itself at the wrap seam."""
    bg = re.search(r'<rect x="0" y="0" width="990" height="990" fill="(#\w{6})"/>', svg).group(1)
    cs = [(float(a), float(b), float(r), f) for a, b, r, f in re.findall(r'<circle cx="([-\d.]+)" cy="([-\d.]+)" r="([\d.]+)" fill="(#\w{6})"/>', svg)]
    cs = [c for c in cs if not (c[0] == 495 and c[1] == 30)]          # the cap button is not pattern
    out = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="{bg}"/>']
    if not cs: return out, bg
    ys = sorted({c[1] for c in cs}); xs0 = {y: sorted(c[0] for c in cs if c[1] == y) for y in ys}
    step = xs0[ys[0]][1] - xs0[ys[0]][0]; dy = ys[1] - ys[0]; r = cs[0][2]; f = cs[0][3]
    n = round(W / (step * S)); sx = W / n                              # exact tiling round the mug
    k = sx / (step * S)                                                  # same nudge applied to the row offsets
    offs = [((xs0[y][0] - xs0[ys[0]][0]) % step) * S * k for y in ys]   # per-row offset (stagger / diagonal)
    per = len(ys) if len(set(round(o, 1) for o in offs)) == len(ys) else 2
    i = 0; y = ys[0] * S
    while y - r * S < H:
        o = offs[i % len(offs)] if per == len(ys) else offs[i % 2]
        if per == len(ys) and i >= len(ys): o = (offs[-1] + (i - len(ys) + 1) * (offs[1] - offs[0])) % sx
        x = o - sx
        while x - r * S < W:
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r * S:.1f}" fill="{f}"/>'); x += sx
        i += 1; y += dy * S
    return out, bg

def cap(svg):
    band = re.search(r'<path d="M0,0 H990 V185 Q495,250 0,185 Z" fill="(#\w{6})"/>', svg).group(1)
    seams = re.findall(r'<path d="M495,28 Q[^"]+" fill="none" stroke="(#\w{6})" stroke-width="7" stroke-linecap="round"/>', svg)
    sc = seams[0]
    y0, yc, hw = 185 * S, 250 * S, W / 4   # one smooth brim curve per face, meeting at the handle and at the back
    d = f'M0,0 H{W} V{y0:.1f}'
    for cx in reversed(FACES): d += f' L{cx + hw:.1f},{y0:.1f} Q{cx:.1f},{yc:.1f} {cx - hw:.1f},{y0:.1f}'
    d += ' L0,{:.1f} Z'.format(y0)
    out = [f'<path d="{d}" fill="{band}"/>']
    gold = 'M0,{:.1f}'.format(y0)
    for cx in FACES: gold += f' L{cx - hw:.1f},{y0:.1f} Q{cx:.1f},{yc:.1f} {cx + hw:.1f},{y0:.1f}'
    gold += f' L{W},{y0:.1f}'
    for cx in FACES:   # seams + button + peak copied from the bauble cap, same order (no shine anywhere)
        g = f'<g transform="translate({cx - 495 * S:.2f},0) scale({S:.5f})">'
        for m in re.finditer(r'<path d="(M495,28 Q[^"]+)" fill="none" stroke="#\w{6}" stroke-width="7" stroke-linecap="round"/>', svg):
            g += f'<path d="{m.group(1)}" fill="none" stroke="{sc}" stroke-width="7.2" stroke-linecap="round"/>'
        g += f'<circle cx="495" cy="30" r="24" fill="{sc}"/></g>'
        out.append(g)
    out.append(f'<path d="{gold}" fill="none" stroke="#C9A646" stroke-width="{8 * S:.2f}"/>')
    pk = re.search(r'<path d="(M225,219 [^"]+)" fill="(#\w{6})" stroke="#C9A646" stroke-width="7"/>', svg)
    for cx in FACES:   # peak gold edge kept >= 0.53 mm (7.2 x S = 6.43 px = 0.54 mm)
        out.append(f'<g transform="translate({cx - 495 * S:.2f},0) scale({S:.5f})"><path d="{pk.group(1)}" fill="{pk.group(2)}" stroke="#C9A646" stroke-width="7.2"/></g>')
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
    os.makedirs('out', exist_ok=True); base = f'out/{ref}-bauble-style-mug-{W}x{H}'
    render.make(out, base + '.png', W, H)
    pay = dict(position='front', x=.5, y=.5, scale=1, angle=0, blueprint_id=635, print_provider_id=94, variant_id=72180)
    des = dict(code=code, cap=capcol, **({'horse': horse} if horse else {}))
    json.dump(pay, open(base + '.payload.json', 'w')); json.dump(des, open(base + '.design.json', 'w'))
    f, nn = preflight.check('mug_harrier_11oz', base + '.png', base + '.svg', pay, des)
    print(ref, 'FAIL' if f else 'PASS', f, nn); return not f

if __name__ == '__main__':
    ok = [build(*it) for it in ITEMS]; sys.exit(0 if all(ok) else 1)
