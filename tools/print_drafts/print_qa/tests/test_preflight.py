"""preflight v3: every check has a NEGATIVE test (the defect must be BLOCKED) next to the good files passing.
Run: python -m pytest -q etsy/print_qa/tests"""
import hashlib, json, os, re, shutil, sys
import pytest
from PIL import Image, ImageCms
HERE = os.path.dirname(os.path.abspath(__file__)); QA = os.path.dirname(HERE); FX = os.path.join(QA, 'fixtures')
sys.path.insert(0, QA)
import preflight
SRGB = ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()
sha = lambda b: hashlib.sha256(b).hexdigest()
SKU = {'good_bauble': 'bauble_harrier', 'good_mug': 'mug_harrier_11oz'}

def kit(tmp, name='good_bauble'):
    """copy a good print kit (png, master, sidecar, payload, design) into tmp; returns dict of paths"""
    k = {}
    for ext in ('png', 'svg', 'png.prov.json', 'payload.json', 'design.json'):
        shutil.copy(os.path.join(FX, f'{name}.{ext}'), tmp / f'{name}.{ext}'); k[ext] = str(tmp / f'{name}.{ext}')
    k['sku'] = SKU[name]; return k
def run(k, **over):
    a = dict(png=k['png'], master=k['svg'], payload=k['payload.json'], design=k['design.json']); a.update(over)
    return preflight.check(k['sku'], a['png'], a['master'], a['payload'], a['design'])[0]
def reseal(k):
    """attacker-style: rewrite the sidecar so ONLY the check under test can fail"""
    p = json.load(open(k['png.prov.json'])); p['png_sha256'] = sha(open(k['png'], 'rb').read()); p['master_sha256'] = sha(open(k['svg'], 'rb').read())
    json.dump(p, open(k['png.prov.json'], 'w'))
def edit_master(k, f):
    s = open(k['svg'], encoding='utf8').read(); s2 = f(s); assert s2 != s, 'mutation did not apply'
    open(k['svg'], 'w', encoding='utf8').write(s2); reseal(k)
def has(fails, why): return any(why in x for x in fails)

@pytest.mark.parametrize('name', ['good_bauble', 'good_mug'])
def test_good_kits_pass(tmp_path, name):
    assert run(kit(tmp_path, name)) == []

# ---------- mandatory inputs ----------
@pytest.mark.parametrize('field,why', [('master', 'vector master'), ('payload', 'Printify payload'), ('design', 'design colours')])
def test_missing_input_blocked(tmp_path, field, why):
    assert has(run(kit(tmp_path), **{field: None}), why)
def test_unknown_sku_blocked(tmp_path):
    k = kit(tmp_path); k['sku'] = 'mystery_mug'; assert has(run(k), 'unknown SKU')

# ---------- file ----------
def _png(k, im, **kw):
    im.save(k['png'], **kw); reseal(k)
@pytest.mark.parametrize('mut,why', [
    (lambda im: (im.resize((3960, 3960)), {'icc_profile': SRGB}), 'size'),
    (lambda im: (Image.frombytes('RGB', im.size, im.tobytes()), {}), 'ICC'),
    (lambda im: (im.convert('RGBA'), {'icc_profile': SRGB, '_alpha': True}), 'transparent'),
    (lambda im: (im, {'format': 'JPEG', 'icc_profile': SRGB}), 'format')])
def test_bad_png_blocked(tmp_path, mut, why):
    k = kit(tmp_path); im = Image.open(k['png']).convert('RGB'); im2, kw = mut(im)
    if kw.pop('_alpha', False): im2.putpixel((0, 0), (0, 0, 0, 100))
    _png(k, im2, **kw); assert has(run(k), why)
def test_dpi_checked_on_height_too(tmp_path, monkeypatch):
    k = kit(tmp_path); sp = dict(preflight.SPECS['bauble_harrier']); sp['physical_mm'] = [74.9, 90.0]
    monkeypatch.setitem(preflight.SPECS, 'bauble_harrier', sp)
    assert has(run(k), 'height')

# ---------- binding / provenance ----------
def test_png_changed_after_render_blocked(tmp_path):
    k = kit(tmp_path); im = Image.open(k['png']); im.putpixel((500, 500), (1, 2, 3)); im.save(k['png'], icc_profile=SRGB)
    assert has(run(k), 'PNG changed after it was rendered')
def test_png_not_from_this_master_blocked(tmp_path):
    k = kit(tmp_path); open(k['svg'], 'a').write('\n'); assert has(run(k), 'not rendered from this master')
def test_no_sidecar_blocked(tmp_path):
    k = kit(tmp_path); os.remove(k['png.prov.json']); assert has(run(k), 'no provenance sidecar')
def test_unapproved_renderer_blocked(tmp_path):
    k = kit(tmp_path); p = json.load(open(k['png.prov.json'])); p['renderer'] = 'canvas toDataURL'; json.dump(p, open(k['png.prov.json'], 'w'))
    assert has(run(k), 'unapproved renderer')

# ---------- master allowlist ----------
@pytest.mark.parametrize('mut,why', [
    (lambda s: s.replace('</svg>', '<image href="logo.png" x="0" y="0" width="10" height="10"/></svg>'), '<image>'),
    (lambda s: s.replace('</svg>', '<use href="#x"/></svg>'), '<use>'),
    (lambda s: s.replace('</svg>', '<style>path{fill:#000;opacity:.5}</style></svg>'), '<style>'),
    (lambda s: s.replace('</svg>', '<text x="1" y="1">HI</text></svg>'), 'live <text>'),
    (lambda s: s.replace('</svg>', '<filter id="b"><feGaussianBlur stdDeviation="3"/></filter></svg>'), '<filter>'),
    (lambda s: s.replace('</svg>', '<linearGradient id="g"/></svg>'), '<linearGradient>'),
    (lambda s: s.replace('</svg>', '<mask id="m"/></svg>'), '<mask>'),
    (lambda s: s.replace('</svg>', '<foo:bar xmlns:foo="urn:x"/></svg>'), 'outside the SVG namespace'),
    (lambda s: s.replace('<path ', '<path style="opacity:.5" ', 1), 'style='),
    (lambda s: s.replace('<path ', '<path opacity="0.6" ', 1), 'opacity='),
    (lambda s: s.replace('<path ', '<path fill-opacity="0.6" ', 1), 'fill-opacity='),
    (lambda s: s.replace('<path ', '<path filter="url(#b)" ', 1), 'filter='),
    (lambda s: s.replace('<path ', '<path xlink:href="http://evil/x.png" ', 1), 'namespaced attribute'),
    (lambda s: re.sub(r'fill="#[0-9A-Fa-f]{6}"', 'fill="url(#g)"', s, count=1), 'not a plain hex colour'),
    (lambda s: s.replace('<path ', '<path clip-path="url(http://x/#c)" ', 1), 'clip-path'),
    (lambda s: '<?xml version="1.0"?><!DOCTYPE svg [<!ENTITY x SYSTEM "file:///etc/passwd">]>' + s, 'DOCTYPE'),
    (lambda s: s.replace('stroke-width="16"', 'stroke-width="4"', 1), 'stroke'),
    (lambda s: re.sub(r'<g transform="translate\(([^)]*)\) scale\(([\d.]+)\)">', r'<g transform="translate(\1) matrix(1,0,0,1,0,0) scale(\2)">', s, count=1), 'matrix')])
def test_bad_master_blocked(tmp_path, mut, why):
    k = kit(tmp_path); edit_master(k, mut); assert has(run(k), why)

# ---------- text ----------
def test_small_name_blocked(tmp_path):
    k = kit(tmp_path); edit_master(k, lambda s: re.sub(r'(data-text="REXS" data-font-size=")[\d.]+', r'\g<1>60', s)); assert has(run(k), 'letters')
def test_small_secondary_text_blocked(tmp_path):
    k = kit(tmp_path); edit_master(k, lambda s: re.sub(r'(data-text="MERRY CHRISTMAS" data-font-size=")[\d.]+', r'\g<1>40', s)); assert has(run(k), 'MERRY CHRISTMAS')
def test_mug_small_name_blocked(tmp_path):
    k = kit(tmp_path, 'good_mug'); edit_master(k, lambda s: re.sub(r'(data-text="FACT" data-font-size=")[\d.]+', r'\g<1>30', s)); assert has(run(k), 'FACT')  # 30 px = ~1.8 mm letters

# ---------- layout ----------
def test_key_content_near_edge_blocked(tmp_path):  # logo tab moved down to the rim
    k = kit(tmp_path); edit_master(k, lambda s: s.replace('data-label="ZANS logo"', 'data-label="ZANS logo" transform="translate(0,90)"')); assert has(run(k), 'unsafe band')
def test_key_content_in_hole_keepout_blocked(tmp_path):
    k = kit(tmp_path); edit_master(k, lambda s: s.replace('data-label="ZANS logo"', 'data-label="ZANS logo" transform="translate(0,-700)"')); assert has(run(k), 'keep-out')
def test_off_centre_panel_blocked(tmp_path):  # the 25 Nov complaint: name box off centre
    k = kit(tmp_path); edit_master(k, lambda s: s.replace('data-label="name panel" x="115"', 'data-label="name panel" x="140"')); assert has(run(k), 'name panel')
def test_off_centre_mug_logo_blocked(tmp_path):  # the 2 Nov mug: logo strip 9.5 mm right of centre
    k = kit(tmp_path, 'good_mug'); edit_master(k, lambda s: re.sub(r'data-label="logo tab" x="([\d.]+)"', lambda m: f'data-label="logo tab" x="{float(m.group(1)) + 112:.1f}"', s)); assert has(run(k), 'logo tab')
def test_untagged_master_blocked(tmp_path):
    k = kit(tmp_path); edit_master(k, lambda s: re.sub(r' data-(safe|text|centre|role|label)="[^"]*"', '', s)); assert has(run(k), 'no key content')

# ---------- colour (owner mandate: no wrong shades) ----------
def test_deepened_design_colour_in_master_blocked(tmp_path):  # the rejected v2 'deeper colours'
    k = kit(tmp_path); edit_master(k, lambda s: s.replace('#1C4FA0', '#1B4B98')); assert has(run(k), 'not in the design')
def test_wrong_shade_in_png_blocked(tmp_path):
    k = kit(tmp_path); im = Image.open(k['png']).convert('RGB'); px = im.load()
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            if px[x, y] == (0x1C, 0x4F, 0xA0): px[x, y] = (0x24, 0x57, 0x0F)
    _png(k, im, icc_profile=SRGB); assert has(run(k), 'print file colours not in the approved set')
def test_design_code_mismatch_blocked(tmp_path):  # file drawn in other colours than the buyer's code
    k = kit(tmp_path); d = json.load(open(k['design.json'])); d['code'] = 'ZBA-plain-1E50A2-FFFFFF-plain-FFFFFF'; json.dump(d, open(k['design.json'], 'w'))
    assert has(run(k), 'not in the design')
def test_registry_horse_wrong_shade_blocked(tmp_path):
    k = kit(tmp_path); d = {'code': 'ZBA-disc-F5B8CC-6CC24A-plain-F5B8CC', 'cap': '#F5B8CC', 'horse': 'lossiemouth'}; json.dump(d, open(k['design.json'], 'w'))
    assert has(run(k), 'differ from the approved lossiemouth silks')
def test_unknown_registry_horse_blocked(tmp_path):
    k = kit(tmp_path); d = json.load(open(k['design.json'])); d['horse'] = 'not_a_horse'; json.dump(d, open(k['design.json'], 'w'))
    assert has(run(k), 'not in the approved palette registry')

# ---------- payload ----------
@pytest.mark.parametrize('over,why', [(dict(x=0.52), 'placement x'), (dict(scale=1.1), 'placement scale'), (dict(angle=90), 'placement angle'),
    (dict(position='back'), 'placement position'), (dict(variant_id=1), 'variant'), (dict(blueprint_id=635), 'blueprint'),
    (dict(print_provider_id=6), 'provider'), (dict(print_provider_id=None), 'provider')])
def test_bad_payload_blocked(tmp_path, over, why):
    k = kit(tmp_path); p = json.load(open(k['payload.json'])); p.update(over); json.dump(p, open(k['payload.json'], 'w'))
    assert has(run(k), why)

def test_cli_exit_code(tmp_path):
    k = kit(tmp_path)
    assert preflight.main(['bauble_harrier', k['png'], '--master', k['svg'], '--payload', k['payload.json'], '--design', k['design.json']]) == 0
    assert preflight.main(['bauble_harrier', k['png'], '--master', k['svg']]) == 1
def test_name_running_over_panel_blocked(tmp_path):  # e.g. a long name forced too big for the cream panel
    k = kit(tmp_path); edit_master(k, lambda s: s.replace('data-label="name panel" x="115"', 'data-label="name panel" x="265"').replace('width="760"', 'width="460"', 1))
    assert has(run(k), 'over the edge of the name panel')

def test_orphaned_clip_blocked(tmp_path):  # code chat 25 Nov: master regex stripped the cap's clip-path, cap printed as a rectangle
    k = kit(tmp_path); edit_master(k, lambda s: s.replace('<defs>', '<defs><clipPath id="capc"><rect x="0" y="0" width="10" height="10"/></clipPath>', 1) if '<defs>' in s else s.replace('>', '><defs><clipPath id="capc"><rect x="0" y="0" width="10" height="10"/></clipPath></defs>', 1))
    assert has(run(k), 'nothing uses it')
def test_dangling_clip_ref_blocked(tmp_path):
    k = kit(tmp_path); edit_master(k, lambda s: s.replace('<rect ', '<rect clip-path="url(#gone)" ', 1))
    assert has(run(k), 'points at no clipPath')


# --- owner waiver (Alex 26 Nov 11:02: "keep the logo the original size please") ---
def _w(**k):
    w = dict(value=0.68, by='Alex', source='cmsg_017LpptpymmcJZuGHLNRtGrsWh1B1WDPh3cT1yyLN6NSHm', at='2026-11-26T11:02Z'); w.update(k)
    return {'owner_waivers': {'logo_text_mm': w}}

def test_waiver_valid():
    import preflight
    assert preflight.owner_waiver(_w(), 'logo_text_mm')['value'] == 0.68

def test_waiver_rejects_non_alex_or_bad_source():
    import preflight
    assert preflight.owner_waiver(_w(by='ChatGPT'), 'logo_text_mm') is None
    assert preflight.owner_waiver(_w(source='issue-26'), 'logo_text_mm') is None
    assert preflight.owner_waiver(_w(at='today'), 'logo_text_mm') is None

def test_waiver_floor_and_scope():
    import preflight
    assert preflight.owner_waiver(_w(value=0.3), 'logo_text_mm') is None      # never below 0.6 mm
    assert preflight.owner_waiver({'owner_waivers': {'min_name_mm': _w()['owner_waivers']['logo_text_mm']}}, 'min_name_mm') is None   # only the logo can be waived
    assert preflight.owner_waiver({}, 'logo_text_mm') is None


# --- cap seam regression (26 Nov: shine drawn over the seam cut it on Rexs Romance / Zoo Olympios) ---
V = '/tmp/claude-0/zp/print-qa/2026-11-26-v{0}/out{0}/{1}-v{0}.svg'
def test_cap_shine_over_seam_fails():
    import preflight, os, pytest
    p = V.format(7, 'rexs-romance')
    if not os.path.exists(p): pytest.skip('v7 master not here')
    assert preflight.cap_seam_check(open(p, 'rb').read())

def test_cap_shine_under_seams_passes():
    import preflight
    raw = b'<path d="M195,155 Q265,70 455,48" stroke="#fff"/><path d="M495,28 Q346.5,78.8 165,187.2" fill="none" stroke="#B3B3B3" stroke-width="7" stroke-linecap="round"/>'
    assert preflight.cap_seam_check(raw) == []
    bad = raw.split(b'/>', 1)[1] + raw.split(b'/>', 1)[0] + b'/>'
    assert preflight.cap_seam_check(bad)


# --- no outer ring on any bauble (Alex, non-negotiable, 26 Nov) ---
def test_edge_ring_fails_and_ring_free_passes():
    import preflight
    bad = b'<circle cx="495" cy="495" r="469" fill="none" stroke="#C9A646" stroke-width="14"/>'
    assert preflight.edge_ring_check(bad, 990, 990)
    assert preflight.edge_ring_check(b'<circle cx="495" cy="30" r="24" fill="#aa7f8d"/>', 990, 990) == []
    import glob
    for f in glob.glob('/tmp/claude-0/zp/print-qa/2026-11-26-v7/out9/*-v9.svg'):
        assert preflight.edge_ring_check(open(f, 'rb').read(), 990, 990) == [], f

def test_raster_ring_catches_any_shape():
    import preflight
    from PIL import Image, ImageDraw
    def base():
        im = Image.new('RGB', (990, 990), '#1C4FA0'); ImageDraw.Draw(im).rectangle((0, 0, 990, 200), fill='#FFFFFF'); return im
    assert preflight.raster_ring(base()) is None
    a = base(); ImageDraw.Draw(a).ellipse((20, 20, 970, 970), outline='#C9A646', width=14); assert preflight.raster_ring(a)          # stroked ring
    b = base(); dr = ImageDraw.Draw(b); dr.ellipse((15, 15, 975, 975), fill='#C9A646'); dr.ellipse((35, 35, 955, 955), fill='#1C4FA0'); assert preflight.raster_ring(b)   # filled annulus
    c = base(); ImageDraw.Draw(c).ellipse((25, 30, 965, 960), outline='#C9A646', width=14); assert preflight.raster_ring(c)          # slightly squashed / shifted ellipse
    d = base(); ImageDraw.Draw(d).regular_polygon((495, 495, 470), 64, outline='#C9A646', width=14); assert preflight.raster_ring(d)   # path / polygon ring
