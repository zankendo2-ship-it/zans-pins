"""Mug v4 = the ORIGINAL FACT TO FILE designer artwork (as printed 2 Nov) with technical fixes only:
vector logo strip at the same size; logo tab centred on the 2475/2582 wrap (the designer left it at the old 2700 px centre);
name plates 3% smaller so they sit 6 mm inside the bottom edge (were 4.4 mm). Colours, layout, type untouched."""
import json, re, sys
sys.path.insert(0, '/tmp/claude-0/r1h/etsy/print_qa'); sys.path.insert(0, '/tmp/claude-0/v4')
import render, preflight, outline
P1 = open('/tmp/claude-0/v3/horse_paths.txt').read().split('\n')[0]
CODE = 'ZANS-B-hoops-00843D-F5D130-plain-F5D130-00843D-contrast-C8102E-C8102E-HBK-R1'
for sku, w, h, mm, bp, pp, var in (('mug_harrier_11oz', 2475, 1155, 209.55, 635, 94, 72180), ('mug_white_tss_11oz', 2582, 1120, 218.6, 535, 6, 69010)):
    s = open(f'orig-mug-{w}.svg').read(); pxmm = w / mm
    # logo: tab + bitmap -> same-size tab centred on the wrap + vector strip
    t = re.search(r'<rect x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)" rx="9" fill="#FBF7F0"/>', s)
    im = re.search(r'<image [^>]*x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)"[^>]*/>', s)
    tx, ty, tw, th = map(float, t.groups()); ix, iy, iw, ih = map(float, im.groups()); dx = w / 2 - (tx + tw / 2)
    from v4 import logo
    s = s.replace(t.group(0), f'<rect data-safe="1" data-centre="x" data-label="logo tab" x="{tx + dx:.2f}" y="{ty}" width="{tw}" height="{th}" rx="9" fill="#FBF7F0"/>')
    # the bitmap strip is drawn 'meet' inside its box: the 750x100 image fills 343 x 45.7
    bw = min(iw, ih * 7.5); bh = bw / 7.5
    s = s.replace(im.group(0), logo(ix + dx + (iw - bw) / 2, iy + (ih - bh) / 2, bw, bh))
    # name plates: scale so the outer edge is >= 6.2 mm from top/bottom edges and below the cap band
    def plate(m):
        cx, cy, rot, sc = float(m.group(1)), float(m.group(2)), m.group(3), float(m.group(4))
        half = (857.3 / 2 + 7) * sc; lim = h - 6.2 * pxmm
        if cy + half > lim:
            k = (lim - cy) / half; sc *= k
        return f'<g data-safe="1" transform="translate({cx},{cy}) rotate({rot}) scale({sc:.4f})">'
    s, n = re.subn(r'<g transform="translate\(([\d.]+),([\d.]+)\) rotate\((-?90)\) scale\(([\d.]+)\)">', plate, s); assert n == 2
    s = re.sub(r'<g data-text="(FACT|TO FILE)"', r'<g data-role="name" data-text="\1"', s)
    base = f'out5/fact-to-file-mug-{w}x{h}-v5'
    render.make(s, base + '.png', w, h)
    pay = dict(position='front', x=.5, y=.5, scale=1, angle=0, blueprint_id=bp, print_provider_id=pp, variant_id=var); des = dict(code=CODE)
    json.dump(pay, open(base + '.payload.json', 'w')); json.dump(des, open(base + '.design.json', 'w'))
    f, nn = preflight.check(sku, base + '.png', base + '.svg', pay, des); print(sku, 'FAIL' if f else 'PASS', f, nn)
