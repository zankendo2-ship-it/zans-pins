"""Build the speed + icon assets for the ZANS website (docs/).

Run from the repo root:  python tools/seo-fixes/build_assets.py
- favicon.ico, apple-touch-icon.png, img/icon-192.png: square crop of img/zans-logo.png
  (the 'HORSE RACING' line is dropped because it can't be read at icon size)
- img/zans-logo-180.jpg: small header logo (the 385px PNG was loaded for a 60px slot)
- WebP copies of the big photos, plus a JPEG copy of the 920 KB silks-mugs-trio.png
- fonts/: self-hosted Jost, Source Sans 3 and IBM Plex Mono (SIL Open Font Licence),
  downloaded from Google Fonts, with metric-matched fallback faces in fonts/fonts.css
Originals are never changed or deleted (other pages and posts may link to them).
"""
import io, json, os, re, sys, urllib.request
from PIL import Image

DOCS = os.path.join(os.path.dirname(__file__), '..', '..', 'docs')
IMG = os.path.join(DOCS, 'img')
BG = (234, 225, 216)  # logo background


def save(im, path, fmt, **kw):
    im.save(path, fmt, **kw)
    print(f'  {os.path.relpath(path, DOCS):45} {os.path.getsize(path):>8} bytes')


def resize_w(im, w):
    return im if w >= im.size[0] else im.resize((w, round(im.size[1] * w / im.size[0])), Image.LANCZOS)


def icons():
    logo = Image.open(os.path.join(IMG, 'zans-logo.png')).convert('RGB')
    crop = logo.crop((0, 0, logo.size[0], 343))  # drop the small 'HORSE RACING' line
    side = max(crop.size) + 16
    sq = Image.new('RGB', (side, side), BG)
    sq.paste(crop, ((side - crop.size[0]) // 2, (side - crop.size[1]) // 2))
    save(sq.resize((192, 192), Image.LANCZOS), os.path.join(IMG, 'icon-192.png'), 'PNG', optimize=True)
    save(sq.resize((180, 180), Image.LANCZOS), os.path.join(DOCS, 'apple-touch-icon.png'), 'PNG', optimize=True)
    save(sq.resize((48, 48), Image.LANCZOS), os.path.join(DOCS, 'favicon.ico'), 'ICO', sizes=[(16, 16), (32, 32), (48, 48)])
    save(resize_w(logo, 180), os.path.join(IMG, 'zans-logo-180.jpg'), 'JPEG', quality=85, optimize=True, progressive=True)


def photos():
    hero = Image.open(os.path.join(IMG, 'silks-mugs-hero.jpg')).convert('RGB')
    for w in (600, 940):
        save(resize_w(hero, w), os.path.join(IMG, f'silks-mugs-hero-{w}.webp'), 'WEBP', quality=80, method=6)
    trio = Image.open(os.path.join(IMG, 'silks-mugs-trio.png')).convert('RGB')
    for w in (800, 1553):
        save(resize_w(trio, w), os.path.join(IMG, f'silks-mugs-trio-{w}.webp'), 'WEBP', quality=80, method=6)
    save(trio, os.path.join(IMG, 'silks-mugs-trio-1553.jpg'), 'JPEG', quality=85, optimize=True, progressive=True)
    for name in ('ascot-flat-beginner', 'ascot-flat-advanced', 'ascot-flat-pro',
                 'breeders-cup-beginner', 'breeders-cup-advanced', 'breeders-cup-pro'):
        im = Image.open(os.path.join(IMG, name + '.jpg')).convert('RGB')
        for w in (600, 1000):
            save(resize_w(im, w), os.path.join(IMG, f'{name}-{w}.webp'), 'WEBP', quality=80, method=6)
    seal = Image.open(os.path.join(IMG, 'limited-edition-seal.png'))
    save(seal, os.path.join(IMG, 'limited-edition-seal.webp'), 'WEBP', quality=85, method=6)


FONT_FILES = {
    'jost-latin': 'https://fonts.gstatic.com/s/jost/v20/92zatBhPNqw73oTd4jQmfxI.woff2',
    'jost-latin-ext': 'https://fonts.gstatic.com/s/jost/v20/92zatBhPNqw73ord4jQmfxIC7w.woff2',
    'source-sans-3-latin': 'https://fonts.gstatic.com/s/sourcesans3/v20/nwpStKy2OAdR1K-IwhWudF-R3w8aZejf5Hc.woff2',
    'source-sans-3-latin-ext': 'https://fonts.gstatic.com/s/sourcesans3/v20/nwpStKy2OAdR1K-IwhWudF-R3wEaZejf5HdF8Q.woff2',
    'ibm-plex-mono-500-latin': 'https://fonts.gstatic.com/s/ibmplexmono/v20/-F6qfjptAgt5VM-kVkqdyU8n3twJwlBFgsAXHNk.woff2',
    'ibm-plex-mono-500-latin-ext': 'https://fonts.gstatic.com/s/ibmplexmono/v20/-F6qfjptAgt5VM-kVkqdyU8n3twJwl5FgsAXHNlYzg.woff2',
}


def fonts():
    d = os.path.join(DOCS, 'fonts')
    os.makedirs(d, exist_ok=True)
    for name, url in FONT_FILES.items():
        p = os.path.join(d, name + '.woff2')
        if not os.path.exists(p):
            urllib.request.urlretrieve(url, p)
        print(f'  fonts/{name}.woff2 {os.path.getsize(p):>8} bytes')


if __name__ == '__main__':
    print('icons'); icons()
    print('photos'); photos()
    print('fonts'); fonts()
