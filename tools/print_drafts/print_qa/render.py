"""The ONE way a print PNG is made: outlined vector master -> Chromium at the exact template pixels -> lossless PNG
with sRGB IEC61966-2.1 embedded -> provenance sidecar <png>.prov.json binding the PNG to its master.
preflight refuses a PNG whose sidecar is missing or whose hashes do not match.
usage: render.py master.svg out.png WIDTH HEIGHT   (outlines any <text> first)"""
import hashlib, io, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from outline import outline_svg
RENDERER = 'zans-print-qa/render.py v3 (chromium, outlined master, deviceScaleFactor 1)'
sha = lambda b: hashlib.sha256(b).hexdigest()

def to_png(svg, w, h):
    from playwright.sync_api import sync_playwright
    from PIL import Image, ImageCms
    with sync_playwright() as p:
        kw = {'executable_path': os.environ['PW_CHROMIUM']} if os.environ.get('PW_CHROMIUM') else {}
        b = p.chromium.launch(**kw); q = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
        q.set_content('<html><head><style>html,body{margin:0;padding:0}svg{display:block}</style></head><body>' + svg + '</body></html>')
        q.wait_for_timeout(300); raw = q.screenshot(clip={'x': 0, 'y': 0, 'width': w, 'height': h}); b.close()
    bio = io.BytesIO()
    Image.open(io.BytesIO(raw)).convert('RGB').save(bio, 'PNG', icc_profile=ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes())
    return bio.getvalue()

def make(svg, png_path, w, h, master_path=None, extra=None):
    """Outline, render, write PNG + master + sidecar. Returns (png_path, master_path)."""
    m = outline_svg(svg); mb = m.encode('utf8')
    master_path = master_path or png_path[:-4] + '.svg'
    open(master_path, 'wb').write(mb)
    png = to_png(m, w, h); open(png_path, 'wb').write(png)
    prov = dict(renderer=RENDERER, px=[w, h], master=os.path.basename(master_path), master_sha256=sha(mb), png_sha256=sha(png),
                made_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), **(extra or {}))
    json.dump(prov, open(png_path + '.prov.json', 'w'), indent=1)
    return png_path, master_path

if __name__ == '__main__':
    make(open(sys.argv[1], encoding='utf8').read(), sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
