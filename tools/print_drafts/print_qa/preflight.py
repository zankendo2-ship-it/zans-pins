#!/usr/bin/env python3
"""ZANS print preflight v3 - FAIL-CLOSED (any failure, missing input or error = the order must NOT be sent).
usage: preflight.py <sku> <print.png> --master master.svg --payload payload.json --design design.json
Every input is mandatory. Checks:
 FILE      lossless PNG, exact template px, >= 300 DPI on BOTH axes, sRGB IEC61966-2.1 ICC, no transparency, size limit
 BINDING   <png>.prov.json made by render.py: renderer, px, sha256 of this PNG and of this master must match
 MASTER    parsed as XML (no DOCTYPE/entities): element + attribute ALLOWLIST (no <image>, <style>, <text>, <use>,
           filters, masks, gradients, style=, external refs, foreign namespaces), no opacity,
           strokes >= SKU minimum (transform scale applied)
 TEXT      text must be outlined (render.py does it); letter (cap) height >= min_text_mm, names >= min_name_mm
 LAYOUT    key content (outlined text, data-safe elements) inside the safe zone and out of any keep-out circle;
           names + data-centre elements centred within 0.5 mm
 COLOUR    every fill/stroke in the master is in the design's own code colours, its registry horse, the brand
           palette or an approved derived rule (palette.json); every colour covering >= 0.3% of the PNG is within
           6/255 per channel of one of those
 PAYLOAD   blueprint, provider, variant and placement (position/x/y/scale/angle) exactly as approved"""
import hashlib, io, json, math, os, re, sys
import xml.etree.ElementTree as ET
from PIL import Image, ImageCms
HERE = os.path.dirname(os.path.abspath(__file__))
SPECS = json.load(open(os.path.join(HERE, 'sku_specs.json')))
PALETTE = json.load(open(os.path.join(HERE, 'palette.json')))
SVGNS = 'http://www.w3.org/2000/svg'
TAGS = {'svg', 'g', 'defs', 'clipPath', 'rect', 'circle', 'ellipse', 'path', 'polygon', 'polyline', 'line', 'title', 'desc'}
ATTRS = {'id', 'x', 'y', 'width', 'height', 'viewBox', 'cx', 'cy', 'r', 'rx', 'ry', 'd', 'points', 'x1', 'y1', 'x2', 'y2',
         'fill', 'stroke', 'stroke-width', 'stroke-linecap', 'stroke-linejoin', 'stroke-miterlimit', 'transform', 'clip-path',
         'fill-rule', 'clip-rule', 'version', 'preserveAspectRatio'}
RENDERER = 'zans-print-qa/render.py v3'
CAP = 0.70  # Jost cap height / em (OS/2 sCapHeight 700 / 1000)
sha = lambda b: hashlib.sha256(b).hexdigest()

def norm(h):
    h = h.strip().upper()
    if re.fullmatch(r'#[0-9A-F]{3}', h): h = '#' + ''.join(c * 2 for c in h[1:])
    return h

def shade(h, f):  # identical to the bauble designer's shade()
    n = int(h[1:], 16); c = [n >> 16, (n >> 8) & 255, n & 255]
    c = [max(0, min(255, int(math.floor(v * f + 0.5)) if f < 1 else int(math.floor(v + (255 - v) * (f - 1) + 0.5)))) for v in c]
    return '#' + ''.join(f'{v:02X}' for v in c)

def allowed_colours(design):
    """design = {'code': buyer's design code, 'horse': registry key (optional), 'cap': cap hex (optional)}"""
    fails, brand = [], {norm(k) for k in PALETTE['brand']}
    ok = set(brand)
    code_cols = {norm('#' + h) for h in re.findall(r'(?<![0-9A-Fa-f])([0-9A-Fa-f]{6})(?![0-9A-Fa-f])', design.get('code') or '')}
    if not code_cols and not design.get('horse'): fails.append('no design colours (design code or registry horse) supplied')
    ok |= code_cols
    if design.get('horse'):
        h = PALETTE['horses'].get(design['horse'])
        if not h: fails.append(f'horse {design["horse"]!r} not in the approved palette registry')
        else:
            reg = {norm(v) for v in h['components'].values()}
            if code_cols - reg - brand: fails.append(f'design colours {sorted(code_cols - reg - brand)} differ from the approved {design["horse"]} silks')
            ok |= reg
    if design.get('cap'):
        cap = norm(design['cap'])
        if cap not in ok: fails.append(f'cap colour {cap} not in the design')
        ok |= {shade(cap, f) for f in PALETTE['derived_rules']['capA_shading']['factors']}
    return ok, fails

def tf_ops(t):
    if re.search(r'matrix|skew', t or ''): raise ValueError('matrix/skew transform not allowed in a print master')
    return re.findall(r'(translate|rotate|scale)\(([^)]*)\)', t or '')

def tscale(t):
    s = 1.0
    for op, a in tf_ops(t):
        if op == 'scale':
            v = [abs(float(x)) for x in re.split(r'[ ,]+', a.strip()) if x]; s *= math.sqrt(v[0] * (v[1] if len(v) > 1 else v[0]))
    return s

def apply_tf(pts, t):  # SVG order: the rightmost transform applies first
    for op, a in reversed(tf_ops(t)):
        v = [float(x) for x in re.split(r'[ ,]+', a.strip()) if x]
        if op == 'translate': pts = [(x + v[0], y + (v[1] if len(v) > 1 else 0)) for x, y in pts]
        elif op == 'scale': sy = v[1] if len(v) > 1 else v[0]; pts = [(x * v[0], y * sy) for x, y in pts]
        else:
            r = math.radians(v[0]); cx, cy = (v[1], v[2]) if len(v) > 2 else (0, 0)
            pts = [(cx + (x - cx) * math.cos(r) - (y - cy) * math.sin(r), cy + (x - cx) * math.sin(r) + (y - cy) * math.cos(r)) for x, y in pts]
    return pts

def elem_pts(e):
    t = e.tag.split('}')[-1]; g = lambda k: float(e.get(k, 0) or 0)
    if t == 'rect':
        x, y, w, h = g('x'), g('y'), g('width'), g('height'); r = min(g('rx'), w / 2, h / 2); k = r * (1 - 1 / math.sqrt(2))
        if e.get('stroke', 'none') != 'none': o = g('stroke-width') / 2; x, y, w, h, k = x - o, y - o, w + 2 * o, h + 2 * o, k + o * (1 - 1 / math.sqrt(2)) - o * 0  # stroke paints outside the box
        return [(x + k, y + k), (x + w - k, y + k), (x + k, y + h - k), (x + w - k, y + h - k), (x + w / 2, y), (x + w / 2, y + h), (x, y + h / 2), (x + w, y + h / 2)]
    if t == 'circle':
        cx, cy, r = g('cx'), g('cy'), g('r') + (g('stroke-width') / 2 if e.get('stroke', 'none') != 'none' else 0); return [(cx + r * math.cos(i * math.pi / 8), cy + r * math.sin(i * math.pi / 8)) for i in range(16)]
    if t == 'path':  # absolute coordinates only (outline.py writes M/L/Q/C/Z); relative commands are refused for key content
        d = e.get('d', '')
        if re.search(r'[mlhvcsqtaz](?=[^a-zA-Z]*\d)', d.replace('z', '')): raise ValueError('key-content path uses relative commands')
        n = [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?(?:[eE]-?\d+)?', d)]
        return list(zip(n[0::2], n[1::2]))
    return []

def check_master(sp, raw, W, H, design):
    fails, notes = [], []
    if re.search(rb'<!DOCTYPE|<!ENTITY|<\?xml-stylesheet', raw): return ['master has DOCTYPE/ENTITY/stylesheet (not allowed)'], notes, set()
    try: root = ET.fromstring(raw)
    except ET.ParseError as e: return [f'master is not valid XML: {e}'], notes, set()
    vb = [float(x) for x in re.split(r'[ ,]+', (root.get('viewBox') or f'0 0 {W} {H}').strip())]
    if vb[0] or vb[1] or abs(vb[2] / vb[3] - W / H) > 0.002: fails.append(f'master viewBox {vb} does not match the template')
    pxmm = vb[2] / sp['physical_mm'][0]; minstroke = sp['min_stroke_mm'] * pxmm
    ok_cols, f2 = allowed_colours(design); fails += f2
    used, key_pts, centre, n_text = set(), [], {}, [0]
    boxes, inside = {}, {}  # data-label boxes (inner edge of their border) and contents that must sit inside them
    def walk(e, tf, key, lab, ins=None):
        ns, tag = (e.tag[1:].split('}') if e.tag.startswith('{') else ('', e.tag))
        if ns != SVGNS: fails.append(f'element <{tag}> outside the SVG namespace'); return
        if tag == 'text': fails.append('live <text> in master - must be outlined so no font can change'); return
        if tag not in TAGS: fails.append(f'<{tag}> not allowed in a print master'); return
        for k, v in e.attrib.items():
            if k.startswith('{'): fails.append(f'namespaced attribute {k.split("}")[-1]} on <{tag}> (external refs not allowed)'); continue
            if k.startswith('data-'): continue
            if k not in ATTRS: fails.append(f'attribute {k}= not allowed on <{tag}>'); continue
            if k == 'clip-path' and not re.fullmatch(r'url\(#[\w-]+\)', v): fails.append(f'external clip-path {v}')
            if k in ('fill', 'stroke') and v != 'none':
                if not re.fullmatch(r'#[0-9A-Fa-f]{6}|#[0-9A-Fa-f]{3}', v.strip()): fails.append(f'{k}="{v}" is not a plain hex colour'); continue
                used.add(norm(v))
        t2 = (tf + ' ' + e.get('transform', '')).strip()
        sw = e.get('stroke-width')
        if sw and e.get('stroke', 'none') != 'none' and float(sw) > 0 and float(sw) * tscale(t2) < minstroke - 0.01:
            fails.append(f'stroke {float(sw) * tscale(t2) / pxmm:.2f} mm < {sp["min_stroke_mm"]} mm')
        if 'data-text' in e.attrib:
            n_text[0] += 1; cap = float(e.get('data-font-size', 0)) * tscale(t2) * CAP / pxmm
            role = e.get('data-role')   # 'logo' = lettering inside the ZANS brand mark (min_logo_text_mm, spec note says why)
            need = sp['min_name_mm'] if role == 'name' else sp.get('min_logo_text_mm', sp['min_text_mm']) if role == 'logo' else sp['min_text_mm']
            if cap < need - 0.01: fails.append(f'text "{e.get("data-text")}" letters {cap:.1f} mm tall < {need} mm')
        key = key or 'data-safe' in e.attrib or 'data-text' in e.attrib
        if e.get('data-centre') or e.get('data-role') == 'name':
            lab = e.get('data-label') or e.get('data-text') or e.get('id') or tag
        ins = e.get('data-inside') or ins
        if tag == 'rect' and e.get('data-label'):
            x, y = apply_tf([(float(e.get('x', 0)), float(e.get('y', 0)))], t2)[0]; sc = tscale(t2)
            sw = float(e.get('stroke-width', 0) or 0) if e.get('stroke', 'none') != 'none' else 0
            boxes[e.get('data-label')] = (x + sw / 2 * sc, y + sw / 2 * sc, x + (float(e.get('width')) - sw / 2) * sc, y + (float(e.get('height')) - sw / 2) * sc)
        if ins and tag == 'path': inside.setdefault(ins, []).extend(apply_tf(elem_pts(e), t2))
        if key and tag in ('path', 'rect', 'circle'):
            pts = apply_tf(elem_pts(e), t2); key_pts.extend(pts)
            if lab: centre.setdefault(lab, []).extend(pts)
        for c in e: walk(c, t2, key, lab, ins)
    # a <clipPath> nobody uses = a shape lost its clip (e.g. a cap printing as a raw rectangle); a url(#x) with no clipPath = same
    clip_ids = {e.get('id') for e in root.iter(f'{{{SVGNS}}}clipPath')}
    clip_refs = {m for e in root.iter() for m in re.findall(r'url\(#([\w-]+)\)', e.get('clip-path', ''))}
    for i in sorted(x for x in clip_ids - clip_refs if x): fails.append(f'clipPath #{i} is defined but nothing uses it - a shape has lost its clip')
    for i in sorted(clip_refs - clip_ids): fails.append(f'clip-path url(#{i}) points at no clipPath')
    try: walk(root, '', False, None)
    except (ValueError, TypeError) as e: fails.append(f'master geometry: {e}')
    for lab, pts in inside.items():
        if not pts: continue
        b = boxes.get(lab)
        if not b: fails.append(f'"{lab}" box not found for the text that must sit inside it'); continue
        out = max(max(b[0] - x, x - b[2], b[1] - y, y - b[3]) for x, y in pts) / pxmm
        if out > 0: fails.append(f'text runs {out:.1f} mm over the edge of the {lab}')
    bad = used - ok_cols
    if bad: fails.append(f'colours not in the design / registry / brand palette: {sorted(bad)}')
    s = sp['safe_mm'] * pxmm; cx0, cy0 = vb[2] / 2, vb[3] / 2
    inside = lambda x, y: (cx0 - math.hypot(x - cx0, y - cy0)) if sp['shape'] == 'circle' else min(x, y, vb[2] - x, vb[3] - y)
    if not key_pts: fails.append('no key content tagged (data-safe / outlined text) - layout cannot be checked')
    else:
        m = min(inside(x, y) for x, y in key_pts) / pxmm
        notes.append(f'key content {m:.1f} mm inside the edge (safe zone {sp["safe_mm"]} mm)')
        if m < sp['safe_mm'] - 0.05: fails.append(f'key content {m:.1f} mm from the edge, inside the {sp["safe_mm"]} mm unsafe band')
    ko = sp.get('keepout')
    if ko and key_pts:
        kx, ky, kr = ko['cx_mm'] * pxmm, ko['cy_mm'] * pxmm, ko['r_mm'] * pxmm
        if any(math.hypot(x - kx, y - ky) < kr for x, y in key_pts): fails.append(f'key content inside the {ko["r_mm"]} mm keep-out ({ko["why"]})')
    worst = 0.0
    for lab, pts in centre.items():
        xs = [p[0] for p in pts]; off = ((min(xs) + max(xs)) / 2 - cx0) / pxmm; worst = max(worst, abs(off))
        if abs(off) > 0.5: fails.append(f'"{lab}" {off:+.1f} mm off centre')
    notes.append(f'{len(used)} colours, all approved' if not bad else f'{len(used)} colours')
    notes.append(f'{len(centre)} centred items, worst {worst:.1f} mm; {n_text[0]} outlined texts')
    return fails, notes, ok_cols

def png_colours(im, ok_cols, tol=6, share=0.003):
    a = im.convert('RGB').resize((max(1, im.size[0] // 2), max(1, im.size[1] // 2)), Image.NEAREST)
    n = a.size[0] * a.size[1]; bad = []
    oks = [tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) for c in ok_cols]
    for cnt, c in sorted(a.getcolors(n), reverse=True):
        if cnt / n < share: break
        if not any(max(abs(c[i] - o[i]) for i in range(3)) <= tol for o in oks): bad.append(('#%02X%02X%02X' % c, f'{100 * cnt / n:.1f}%'))
    return bad

def check(sku, png, master=None, payload=None, design=None):
    fails, notes = [], []
    sp = SPECS.get(sku)
    if not sp or sku.startswith('_'): return [f'unknown SKU {sku} (not an approved template)'], notes
    for what, v in (('vector master', master), ('Printify payload', payload), ('design colours', design)):
        if not v: fails.append(f'no {what} supplied')
    if master and not os.path.exists(master): fails.append('vector master file missing')
    if fails: return fails, notes
    if isinstance(payload, str): payload = json.load(open(payload))
    if isinstance(design, str): design = json.load(open(design))
    W, H = sp['px']
    try: pb = open(png, 'rb').read(); im = Image.open(io.BytesIO(pb)); im.load()
    except Exception as e: return [f'cannot open print file: {e}'], notes
    if im.format != 'PNG': fails.append(f'format {im.format}, must be lossless PNG')
    if im.size != (W, H): fails.append(f'size {im.size[0]}x{im.size[1]} != template {W}x{H}')
    dx, dy = im.size[0] / (sp['physical_mm'][0] / 25.4), im.size[1] / (sp['physical_mm'][1] / 25.4)
    notes.append(f'{dx:.0f} x {dy:.0f} DPI')
    if min(dx, dy) < 299.5: fails.append(f'effective DPI {min(dx, dy):.0f} < 300 (width {dx:.0f}, height {dy:.0f})')
    if len(pb) > sp['max_bytes']: fails.append('file over provider size limit')
    icc = im.info.get('icc_profile')
    if not icc: fails.append('no ICC profile (needs sRGB IEC61966-2.1)')
    else:
        desc = ImageCms.getProfileDescription(ImageCms.ImageCmsProfile(io.BytesIO(icc))).strip()
        if 'srgb' not in desc.lower(): fails.append(f'ICC not sRGB: {desc}')
    if not sp['transparency'] and (im.mode in ('RGBA', 'LA', 'PA') or 'transparency' in im.info):
        if im.convert('RGBA').getchannel('A').getextrema()[0] < 255: fails.append('transparent pixels on a full-bleed product (edge halos / blank gaps)')
    mraw = open(master, 'rb').read()
    try:
        mf, mn, ok_cols = check_master(sp, mraw, W, H, design); fails += mf; notes += mn
        if ok_cols:
            bad = png_colours(im, ok_cols)
            if bad: fails.append(f'print file colours not in the approved set: {bad[:5]}')
    except Exception as e:
        fails.append(f'master check crashed: {e}')
    prov_f = png + '.prov.json'
    if not os.path.exists(prov_f): fails.append('no provenance sidecar (PNG not made by render.py from this master)')
    else:
        try: pv = json.load(open(prov_f))
        except Exception: pv = {}
        if not str(pv.get('renderer', '')).startswith(RENDERER): fails.append('PNG made by an unapproved renderer')
        if pv.get('png_sha256') != sha(pb): fails.append('PNG changed after it was rendered (hash mismatch)')
        if pv.get('master_sha256') != sha(mraw): fails.append('PNG was not rendered from this master (hash mismatch)')
        if pv.get('px') != [W, H]: fails.append('rendered at the wrong size')
    pl = sp['placement']
    for k in ('position', 'x', 'y', 'scale', 'angle'):
        if payload.get(k) != pl[k]: fails.append(f'placement {k}={payload.get(k)!r}, approved {pl[k]!r}')
    if payload.get('blueprint_id') != sp['printify_blueprint']: fails.append(f'blueprint {payload.get("blueprint_id")} != {sp["printify_blueprint"]}')
    if payload.get('print_provider_id') != sp['printify_provider']: fails.append(f'provider {payload.get("print_provider_id")} != {sp["printify_provider"]}')
    if payload.get('variant_id') not in sp['variants']: fails.append(f'variant {payload.get("variant_id")} not approved')
    return fails, notes

def main(a):
    if len(a) < 2: print(__doc__); return 2
    opt = lambda k: a[a.index(k) + 1] if k in a else None
    try: fails, notes = check(a[0], a[1], opt('--master'), opt('--payload'), opt('--design'))
    except Exception as e: fails, notes = [f'preflight crashed: {e}'], []
    print(('FAIL ' if fails else 'PASS ') + os.path.basename(a[1]) + ' | ' + '; '.join(fails + notes))
    return 1 if fails else 0
if __name__ == '__main__': sys.exit(main(sys.argv[1:]))
