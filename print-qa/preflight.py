#!/usr/bin/env python3
"""ZANS print preflight - FAIL-CLOSED (exit 1 = the order must NOT be sent).
usage: preflight.py <sku> <print.png> [--master master.svg] [--payload payload.json]
Specs: print-qa/sku_specs.json. Checks: exact template px, >= 300 DPI at real size, sRGB IEC61966-2.1 ICC embedded,
lossless PNG, no transparency where the SKU has none (bleed, no halos), file size limit, master SVG has no bitmap,
no semi-transparency, no stroke under the SKU minimum, payload variant + placement (position/x/y/scale/angle) exact."""
import io, json, os, re, sys
from PIL import Image, ImageCms
SPECS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sku_specs.json')))

def check(sku, png, master=None, payload=None):
    fails, notes = [], []
    sp = SPECS.get(sku)
    if not sp or sku.startswith('_'): return [f'unknown SKU {sku} (not an approved template)'], notes
    W, H = sp['px']; mmw = sp['physical_mm'][0]
    try: im = Image.open(png); im.load()
    except Exception as e: return [f'cannot open print file: {e}'], notes
    if im.format != 'PNG': fails.append(f'format {im.format}, must be lossless PNG')
    if im.size != (W, H): fails.append(f'size {im.size[0]}x{im.size[1]} != template {W}x{H}')
    dpi = im.size[0] / (mmw / 25.4); notes.append(f'{dpi:.0f} DPI effective')
    if dpi < 299.5: fails.append(f'effective DPI {dpi:.0f} < 300')
    if os.path.getsize(png) > sp['max_bytes']: fails.append('file over provider size limit')
    icc = im.info.get('icc_profile')
    if not icc: fails.append('no ICC profile (needs sRGB IEC61966-2.1)')
    else:
        desc = ImageCms.getProfileDescription(ImageCms.ImageCmsProfile(io.BytesIO(icc))).strip()
        if 'srgb' not in desc.lower(): fails.append(f'ICC not sRGB: {desc}')
    if not sp['transparency'] and im.mode in ('RGBA', 'LA', 'P') and ('A' in im.getbands() or 'transparency' in im.info):
        a = im.convert('RGBA').getchannel('A')
        if a.getextrema()[0] < 255: fails.append('transparent pixels on a full-bleed product (edge halos / blank gaps)')
    if master:
        s = open(master, encoding='utf8').read()
        if re.search(r'<image\b', s): fails.append('master embeds a bitmap (<image>) - vector only')
        if re.search(r'(?<![-\w])opacity="0?\.\d+"|fill-opacity="0?\.\d+"|stroke-opacity="0?\.\d+"', s): fails.append('master has semi-transparency')
        if re.search(r'<(linearGradient|radialGradient|feGaussianBlur|feDropShadow)\b', s): fails.append('master has gradient / blur / shadow')
        m = re.search(r'viewBox="[\d.\-]+ [\d.\-]+ ([\d.]+) ', s); vb = float(m.group(1)) if m else W
        strokes = [float(x) for x in re.findall(r'stroke-width="([\d.]+)"', s) if float(x) > 0]
        if strokes:
            thin = min(strokes) / (vb / mmw)
            if thin < sp['min_stroke_mm'] - 0.01: fails.append(f'stroke {thin:.2f} mm < {sp["min_stroke_mm"]} mm')
    else: fails.append('no vector master supplied')
    if payload:
        p = json.load(open(payload)); pl = sp['placement']
        for k in ('position', 'x', 'y', 'scale', 'angle'):
            if p.get(k) != pl[k]: fails.append(f'placement {k}={p.get(k)!r}, approved {pl[k]!r}')
        if p.get('blueprint_id') != sp['printify_blueprint']: fails.append(f'blueprint {p.get("blueprint_id")} != {sp["printify_blueprint"]}')
        if p.get('variant_id') not in sp['variants']: fails.append(f'variant {p.get("variant_id")} not approved')
    return fails, notes

def main(a):
    if len(a) < 2: print(__doc__); return 2
    opt = lambda k: a[a.index(k) + 1] if k in a else None
    fails, notes = check(a[0], a[1], opt('--master'), opt('--payload'))
    print(('FAIL ' if fails else 'PASS ') + os.path.basename(a[1]) + ' | ' + '; '.join(fails + notes))
    return 1 if fails else 0
if __name__ == '__main__': sys.exit(main(sys.argv[1:]))
