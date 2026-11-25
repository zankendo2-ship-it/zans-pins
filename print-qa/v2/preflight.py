#!/usr/bin/env python3
"""ZANS print preflight - FAIL-CLOSED. Exit code 1 (and 'FAIL') if any check fails; order scripts must stop on it.
usage: preflight.py <product> <print.png> [<master.svg>]
Checks (Alex's POD spec 25 Nov + ZANS rules): exact template pixels, >= 300 DPI at real size, sRGB ICC embedded,
no transparency (full bleed, no edge halos), master SVG has no embedded bitmap and no semi-transparency."""
import io, re, sys
from PIL import Image, ImageCms
TEMPLATES = {  # product: (px w, px h, physical width mm)
    'bauble_harrier': (990, 990, 74.9),          # Printify bp 1676, Harrier (pp 94), 2.95" round ceramic
    'mug_harrier_11oz': (2475, 1155, 209.55),     # Printify bp 635, Harrier (pp 94), 11oz accent mug wrap
    'mug_white_tss_11oz': (2582, 1120, 218.6),   # Printify bp 535, T Shirt and Sons (pp 6), white 11oz
}
def main(a):
    prod, png = a[0], a[1]; svg = a[2] if len(a) > 2 else None
    fails, notes = [], []
    if prod not in TEMPLATES: print('FAIL unknown product', prod); return 1
    W, H, mm = TEMPLATES[prod]; im = Image.open(png)
    if im.size != (W, H): fails.append(f'size {im.size} != template {(W, H)}')
    dpi = im.size[0] / (mm / 25.4); notes.append(f'effective {dpi:.0f} DPI')
    if dpi < 299.5: fails.append(f'effective DPI {dpi:.0f} < 300')
    icc = im.info.get('icc_profile')
    if not icc: fails.append('no ICC profile')
    else:
        desc = ImageCms.getProfileDescription(ImageCms.ImageCmsProfile(io.BytesIO(icc))).strip()
        notes.append(f'ICC {desc}')
        if 'srgb' not in desc.lower(): fails.append(f'ICC is not sRGB ({desc})')
    if im.mode in ('RGBA', 'LA') or 'transparency' in im.info:
        if im.mode in ('RGBA', 'LA') and im.getchannel('A').getextrema()[0] < 255: fails.append('transparent pixels (needs full bleed, no halos)')
    if svg:
        s = open(svg, encoding='utf8').read()
        if re.search(r'<image\b', s): fails.append('master SVG embeds a bitmap (<image>)')
        if re.search(r'(?<![-\w])opacity="0?\.\d+"|fill-opacity="0?\.\d+"', s): fails.append('master SVG has semi-transparency')
        thin = [float(x) for x in re.findall(r'stroke-width="([\d.]+)"', s) if 0 < float(x)]
        px_per_mm = W / mm
        if thin and min(thin) / px_per_mm < 1.0: fails.append(f'thinnest stroke {min(thin)/px_per_mm:.2f} mm < 1.0 mm')
    print(('FAIL ' if fails else 'PASS ') + png, '|', '; '.join(fails + notes)); return 1 if fails else 0
if __name__ == '__main__': sys.exit(main(sys.argv[1:]))
