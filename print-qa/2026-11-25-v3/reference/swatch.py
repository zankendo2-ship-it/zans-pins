import json, re, os, sys
sys.path.insert(0, '/tmp/claude-0/r1h/etsy/print_qa')
import preflight
from playwright.sync_api import sync_playwright
OUT = '/tmp/claude-0/v3/out'; PK = '/tmp/claude-0/v3/pack'
def rl(h):
    v = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]; v = [x / 12.92 if x <= .03928 else ((x + .055) / 1.055) ** 2.4 for x in v]
    return .2126 * v[0] + .7152 * v[1] + .0722 * v[2]
con = lambda a, b: (max(rl(a), rl(b)) + .05) / (min(rl(a), rl(b)) + .05)
ITEMS = [('loussiemoo', 'Loussiemoo', 'ZBA-disc-F3B5C9-6CC24A-plain-F3B5C9', 'Silks bauble, pattern "disc" (spots). Code chosen by Alex on the designer 19 Nov; same pink/green as the approved Lossiemouth palette (Alex 21 Nov, rule 2A-13).'),
         ('zoo-olympios', 'Zoo Olympios', 'ZBA-spot_diag-F5D130-1C1C1C-plain-1C1C1C', 'Silks bauble, pattern "spot_diag". Code chosen by Alex on the designer 19 Nov (made-up name - the code IS the reference).'),
         ('rexs-romance', 'Rexs Romance', 'ZBA-plain-1C4FA0-FFFFFF-plain-FFFFFF', 'Silks bauble, plain body. Code chosen by Alex on the designer 19 Nov (made-up name - the code IS the reference).')]
html = []
for ref, name, code, note in ITEMS:
    _, pat, c1, c2, sl, cap = code.split('-'); c1, c2, cap = '#' + c1, '#' + c2, '#' + cap
    svg = open(f'{OUT}/{ref}-design-ink.svg').read(); used = sorted(set(x.upper() for x in re.findall(r'(?:fill|stroke)="(#[0-9A-Fa-f]{6})"', svg)))
    rows = [('Body (code colour 1)', c1, c1 in used), ('Pattern (code colour 2)', c2, c2 in used), ('Cap (code cap colour)', cap, cap in used)]
    derived = [(f'Cap shading x{f} (approved Cap A, Alex 5 Nov)', preflight.shade(cap, f)) for f in (0.7, 1.3, 1.25, 1.6) if preflight.shade(cap, f) in used]
    brand = [(f'Brand: {preflight.PALETTE["brand"][b].split(" (")[0]}', b) for b in preflight.PALETTE['brand'] if b in used]
    inkA = json.load(open(f'{OUT}/results.json'))
    ink_design = next(r[2] for r in inkA if r[0] == ref and r[1] == 'design')
    sw = lambda h: f'<span class=sw style="background:{h}"></span><code>{h}</code>'
    tr = ''.join(f'<tr><td>{a}</td><td>{sw(h)}</td><td>{sw(h)}</td><td>{"same - exact" if ok else "NOT USED"}</td></tr>' for a, h, ok in rows)
    tr += ''.join(f'<tr><td>{a}</td><td>-</td><td>{sw(h)}</td><td>derived by the approved rule</td></tr>' for a, h in derived)
    tr += ''.join(f'<tr><td>{a}</td><td>-</td><td>{sw(h)}</td><td>brand colour</td></tr>' for a, h in brand)
    dk = c1 if rl(c1) <= rl(c2) else c2
    letter = (f'<p><b>Lettering colour - Alex to choose:</b> the live designer writes the name in the design\'s darker colour {sw(dk)} = contrast {con(dk, "#F6F1E7"):.1f}:1 on the cream panel. '
              + (f'That is under 4.5:1 (hard to read when printed), so option A uses ZANS ink {sw("#1C1C1C")} ({con("#1C1C1C", "#F6F1E7"):.1f}:1).' if dk != ink_design else f'That reads fine, so option A keeps it; option B is ZANS ink {sw("#1C1C1C")} ({con("#1C1C1C", "#F6F1E7"):.1f}:1).')
              + ' No new shade is invented either way.</p>')
    html.append(f'<section><h2>{name}</h2><p class=n>{note}<br>Design code: <code>{code}</code></p><div class=row><img src="{OUT}/{ref}-design-ink.png"><img src="{OUT}/{ref}-brand-ink.png"></div>'
                f'<p class=cap>Left: option A lettering. Right: option B lettering (ZANS ink). Print files exactly as they would be sent: 990 x 990 px, sRGB, no overlays.</p>'
                f'<table><tr><th>Component</th><th>Reference (design code)</th><th>In the print file</th><th>Match</th></tr>{tr}</table>{letter}</section>')
page = ('<html><head><meta charset=utf-8><style>body{font:15px/1.4 sans-serif;background:#fff;color:#1C1C1C;margin:24px;width:1100px}h2{margin:0 0 4px}'
        'section{border-top:2px solid #ccc;padding:14px 0}.row img{width:420px;margin-right:18px;border:1px solid #ddd}.sw{display:inline-block;width:26px;height:18px;border:1px solid #555;vertical-align:middle;margin-right:6px}'
        'table{border-collapse:collapse;margin:8px 0}td,th{border:1px solid #bbb;padding:4px 8px;text-align:left}code{font-size:13px}.n,.cap{color:#444}</style></head><body>'
        '<h1>Bauble print files v3 - colour check per component</h1><p>Rule: the print file uses the design code\'s exact colours. Nothing deepened or lightened. Only extra colours: ZANS brand colours and the approved Cap A cap shading.</p>'
        + ''.join(html) + '</body></html>')
open(f'{PK}/swatches.html', 'w').write(page)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ['PW_CHROMIUM']); pg = b.new_page(viewport={'width': 1150, 'height': 800})
    pg.goto('file://' + f'{PK}/swatches.html'); pg.wait_for_timeout(800); pg.screenshot(path=f'{PK}/Bauble colour check v3.png', full_page=True); b.close()
