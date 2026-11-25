import json, os, re, sys
sys.path.insert(0, '/tmp/claude-0/r1h/etsy/print_qa')
from playwright.sync_api import sync_playwright
import render, preflight, outline
OUT = '/tmp/claude-0/v3/out'
P1 = open('/tmp/claude-0/v3/horse_paths.txt').read().split('\n')[0]
CODE = 'ZANS-B-hoops-00843D-F5D130-plain-F5D130-00843D-contrast-C8102E-C8102E-HBK-R1'
SIZES = [('mug_harrier_11oz', 2475, 1155, 635, 94, 72180), ('mug_white_tss_11oz', 2582, 1120, 535, 6, 69010)]
jobs = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['PW_CHROMIUM']); pg = b.new_page()
    pg.goto('http://127.0.0.1:8765/mug-designer/'); pg.wait_for_timeout(1500)
    for sku, w, h, bp, pp, var in SIZES:
        svg = pg.evaluate("""([code,w,h]) => { const d = ZANS.fromCode(code); d.name = 'FACT TO FILE';
            const L = JSON.parse(JSON.stringify(MUG.logo)); for (const k of Object.keys(MUG.logo)) { MUG.logo[k].w_px = 760; MUG.logo[k].h_px = 84; }
            const spec = Object.assign({}, MUG, {width_px: w, height_px: h}); const s = ZANS.printFile(d, spec, 'Jost', LOGO); MUG.logo = L; return s; }""", [CODE, w, h])
        jobs.append((sku, w, h, bp, pp, var, svg))
    b.close()
for sku, w, h, bp, pp, var, svg in jobs:
    open(f'{OUT}/mug_{w}_raw.svg', 'w').write(svg)
    svg = re.sub(r'<style\b[^>]*>.*?</style>', '', svg, flags=re.S)
    # 1. line under the cap band >= 24 px (2 mm)
    svg = re.sub(r'(<rect x="0" y="[\d.]+" width="%d" height=")(\d+(?:\.\d+)?)(")' % w, lambda m: m.group(1) + str(max(float(m.group(2)), 24)) + m.group(3), svg)
    # 2. bitmap wordmark -> faithful vector logo: traced horse mark + 'ZANS RACING TOOLS' in Jost Bold (the font of the original strip)
    def logo(m):
        x, y, lw, lh = (float(v) for v in m.groups()[:4]); cy = y + lh / 2; cx = w / 2
        fs = 62; _, _, _, tw = outline.shape('ZANS RACING TOOLS', fs, 700, 2); mh = 96; mw = 850 * mh / 895; gap = 22
        k = 1.0   # text stays 62 px (>= 3.5 mm letters); the tab is widened to fit instead (TAB_W)   # fit inside the cream logo tab with 34 px (2.9 mm) each side
        fs, mh, gap = fs * k, mh * k, gap * k; _, _, _, tw = outline.shape('ZANS RACING TOOLS', fs, 700, 2 * k); mw = 850 * mh / 895
        tot = mw + gap + tw; x0 = cx - tot / 2
        return (f'<g data-safe="1" data-centre="x" data-label="ZANS logo" data-inside="logo tab"><g transform="translate({x0:.1f},{cy - mh / 2:.1f}) scale({mh / 895:.5f})"><path d="{P1}" fill="#1C1C1C"/></g>'
                f'<text x="{x0 + mw + gap:.1f}" y="{cy + fs * 0.35:.1f}" font-family="Jost" font-weight="700" font-size="{fs:.2f}" letter-spacing="{2 * k:.3f}" fill="#1C1C1C">ZANS RACING TOOLS</text></g>')
    n_img = len(re.findall(r'<image', svg))
    svg = re.sub(r'<image[^>]*?x="([\d.]+)"[^>]*?y="([\d.]+)"[^>]*?width="([\d.]+)"[^>]*?height="([\d.]+)"[^>]*?/?>(</image>)?', logo, svg)
    _, _, _, tw0 = outline.shape('ZANS RACING TOOLS', 62, 700, 2); TAB_W = max(783.5, 850 * 96 / 895 + 22 + tw0 + 2 * 34)
    # 3. logo tab centred on the wrap (was at the old 2700 px centre)
    tabs = re.findall(r'<rect x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)" rx="[\d.]+" fill="#FBF7F0"', svg)
    print(sku, 'images replaced', n_img, 'tabs', tabs[:3])
    open(f'{OUT}/mug_{w}_pre.svg', 'w').write(svg)

    svg = re.sub(r'<rect x="958\.2" y="([\d.]+)" width="783\.5"', lambda m: f'<rect data-safe="1" data-centre="x" data-label="logo tab" x="{w / 2 - TAB_W / 2:.1f}" y="{m.group(1)}" width="{TAB_W:.1f}"', svg)
    svg = svg.replace('<rect x="-428.6" y="-125" width="857.3" height="250" rx="125" fill="#FBF7F0"', '<rect data-safe="1" x="-428.6" y="-125" width="857.3" height="250" rx="125" fill="#FBF7F0"')
    # 4. name plates inside the 6 mm safe zone: the live layout ran them to 4.4 mm from the bottom edge
    capb = 156; top, bot = capb + 10, h - 6 * (w / ({'mug_harrier_11oz': 209.55, 'mug_white_tss_11oz': 218.6}[sku])) - 1
    def plate(m):
        sc = min(float(m.group(4)), (bot - top - 14 * 1.1) / 857.3); return f'<g transform="translate({m.group(1)},{(top + bot) / 2:.1f}) rotate({m.group(3)}) scale({sc:.4f})">'
    svg = re.sub(r'<g transform="translate\(([\d.]+),([\d.]+)\) rotate\((-?90)\) scale\(([\d.]+)\)">', plate, svg)
    svg = re.sub(r' (fill-)?opacity="0?\.\d+"', '', svg)
    base = f'{OUT}/fact-to-file-mug-{w}x{h}'
    render.make(svg, base + '.png', w, h)
    pay = dict(position='front', x=.5, y=.5, scale=1, angle=0, blueprint_id=bp, print_provider_id=pp, variant_id=var); design = dict(code=CODE)
    json.dump(pay, open(base + '.payload.json', 'w')); json.dump(design, open(base + '.design.json', 'w'))
    f, n = preflight.check(sku, base + '.png', base + '.svg', pay, design)
    print(sku, 'FAIL' if f else 'PASS', f, n)
