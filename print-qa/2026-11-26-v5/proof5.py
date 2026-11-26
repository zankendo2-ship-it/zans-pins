import base64, os
from playwright.sync_api import sync_playwright
items=[('Loussiemoo','loussiemoo'),('Zoo Olympios','zoo-olympios'),('Rexs Romance','rexs-romance')]
def b64(p): return 'data:image/png;base64,'+base64.b64encode(open(p,'rb').read()).decode()
cells=''
for nm,ref in items:
    cells+=f'''<div class=row><div class=c><img src="{b64(f'/tmp/claude-0/r1h/etsy/orders/own-{ref}.png')}"><p>{nm} - ORIGINAL</p></div>
<div class=c><img src="{b64(f'out5/{ref}-v5C.png')}"><p>{nm} - CORRECTED v5</p></div></div>'''
html=f'''<html><head><style>@page{{size:A4;margin:10mm}} body{{font-family:sans-serif;font-size:9pt;margin:0}}
.row{{display:flex;gap:12mm;margin-bottom:4mm}} .c img{{width:74.9mm;height:74.9mm;clip-path:circle(50%)}} .c p{{margin:1mm 0}}
.bar{{width:50mm;height:3mm;background:#000;margin:1mm 0}}</style></head><body>
<b>ACTUAL-SIZE PROOF - print at 100% / "Actual size" (no fit-to-page). Each bauble face = 74.9 mm across (Harrier 990 px template).</b>
<div class=bar></div><div>&uarr; this bar must measure exactly 50 mm on paper; if not, the printer scaled the page.</div>
<p>v5: MERRY CHRISTMAS capitals 2.55 mm (weight 500), ZANS RACING TOOLS capitals 1.52 mm, peak gold edge 0.53 mm. Paper proof shows size/legibility only - colour and sharpness need the supplier's physical sample.</p>
{cells}</body></html>'''
open('pack5/proof.html','w').write(html)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ['PW_CHROMIUM']); q=b.new_page(); q.set_content(html); q.pdf(path='pack5/Baubles v5 actual size proof (print at 100%).pdf', format='A4', print_background=True, margin=dict(top='10mm',bottom='10mm',left='10mm',right='10mm')); b.close()
