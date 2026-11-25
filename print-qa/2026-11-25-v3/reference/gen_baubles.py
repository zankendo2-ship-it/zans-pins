import json, os, sys
sys.path.insert(0, '/tmp/claude-0/r1h/etsy/print_qa')
from playwright.sync_api import sync_playwright
import render, preflight
OUT = '/tmp/claude-0/v3/out'
P1 = open('/tmp/claude-0/v3/horse_paths.txt').read().split('\n')[0]
ITEMS = [('loussiemoo', 'Loussiemoo', 'ZBA-disc-F3B5C9-6CC24A-plain-F3B5C9'),
         ('zoo-olympios', 'Zoo Olympios', 'ZBA-spot_diag-F5D130-1C1C1C-plain-1C1C1C'),
         ('rexs-romance', 'Rexs Romance', 'ZBA-plain-1C4FA0-FFFFFF-plain-FFFFFF')]
PAY = dict(position='front', x=.5, y=.5, scale=1, angle=0, blueprint_id=1676, print_provider_id=94, variant_id=115590)
res = []; jobs = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['PW_CHROMIUM']); pg = b.new_page()
    pg.goto('http://127.0.0.1:8765/bauble-designer/'); pg.wait_for_timeout(1500)
    pg.add_script_tag(content=open('/tmp/claude-0/v3/fixC.js').read()); pg.evaluate('h => window.__HORSE=[h]', P1)
    for mode in ('design', 'brand'):
        for ref, name, code in ITEMS:
            _, pat, c1, c2, sl, cap = code.split('-')
            svg, ink = pg.evaluate("""([m,pat,c1,c2,cap,name]) => { window.__INKMODE=m;
              Object.assign(S,{style:'A',pat,body:pat,allover:pat,c1,c2,capCol:cap,name,sleeves:'plain'});
              return [window.__master(), window.__ink(design())]; }""", [mode, pat, '#' + c1, '#' + c2, '#' + cap, name])
            jobs.append((ref, mode, code, cap, svg, ink))
    b.close()
for ref, mode, code, cap, svg, ink in jobs:
            base = f'{OUT}/{ref}-{mode}-ink'
            render.make(svg, base + '.png', 990, 990)
            design = dict(code=code, cap='#' + cap, horse='lossiemouth' if ref == 'loussiemoo' else None)
            if not design['horse']: design.pop('horse')
            json.dump(design, open(base + '.design.json', 'w')); json.dump(PAY, open(base + '.payload.json', 'w'))
            f, n = preflight.check('bauble_harrier', base + '.png', base + '.svg', PAY, design)
            res.append((ref, mode, ink, f, n)); print(ref, mode, ink, 'FAIL' if f else 'PASS', f, n)
json.dump(res, open(f'{OUT}/results.json', 'w'), indent=1)
