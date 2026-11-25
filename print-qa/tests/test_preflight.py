"""Regression tests: a defective print file must FAIL (be blocked). Run: python -m pytest -q print-qa/tests"""
import io, json, os, sys
import pytest
from PIL import Image, ImageCms
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import preflight
SRGB = ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()
GOOD_SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 990 990" width="990" height="990"><rect width="990" height="990" fill="#C8102E"/><circle cx="495" cy="495" r="200" fill="#FFF" stroke="#C9A646" stroke-width="20"/></svg>'

def png(tmp, size=(990, 990), mode='RGB', icc=True, alpha=255, fmt='PNG', name='p.png'):
    im = Image.new(mode, size, (200, 16, 46, alpha) if mode == 'RGBA' else (200, 16, 46))
    f = tmp / name; kw = {'icc_profile': SRGB} if icc else {}
    im.save(f, fmt, **kw); return str(f)
def svg(tmp, body=GOOD_SVG):
    f = tmp / 'm.svg'; f.write_text(body); return str(f)
def pay(tmp, **over):
    p = dict(position='front', x=0.5, y=0.5, scale=1, angle=0, blueprint_id=1676, variant_id=115590); p.update(over)
    f = tmp / 'pay.json'; f.write_text(json.dumps(p)); return str(f)

def run(*a): return preflight.check(*a)[0]

def test_good_bauble_passes(tmp_path):
    assert run('bauble_harrier', png(tmp_path), svg(tmp_path), pay(tmp_path)) == []
@pytest.mark.parametrize('kw,why', [
    (dict(size=(3960, 3960)), 'size'), (dict(size=(800, 800)), 'size'), (dict(icc=False), 'ICC'),
    (dict(mode='RGBA', alpha=120), 'transparent'), (dict(fmt='JPEG', name='p.jpg'), 'format')])
def test_bad_files_blocked(tmp_path, kw, why):
    f = run('bauble_harrier', png(tmp_path, **kw), svg(tmp_path), pay(tmp_path))
    assert any(why in x for x in f), f
@pytest.mark.parametrize('body,why', [
    (GOOD_SVG.replace('</svg>', '<image href="logo.png" x="0" y="0" width="10" height="10"/></svg>'), 'bitmap'),
    (GOOD_SVG.replace('fill="#FFF"', 'fill="#FFF" opacity="0.7"'), 'semi-transparency'),
    (GOOD_SVG.replace('stroke-width="20"', 'stroke-width="7"'), 'stroke'),
    (GOOD_SVG.replace('</svg>', '<defs><linearGradient id="g"/></defs></svg>'), 'gradient')])
def test_bad_masters_blocked(tmp_path, body, why):
    f = run('bauble_harrier', png(tmp_path), svg(tmp_path, body), pay(tmp_path))
    assert any(why in x for x in f), f
def test_no_master_blocked(tmp_path):
    assert any('master' in x for x in run('bauble_harrier', png(tmp_path), None, pay(tmp_path)))
@pytest.mark.parametrize('over,why', [(dict(x=0.52), 'placement x'), (dict(scale=1.1), 'placement scale'), (dict(angle=90), 'placement angle'),
                                       (dict(variant_id=1), 'variant'), (dict(blueprint_id=635), 'blueprint')])
def test_bad_payload_blocked(tmp_path, over, why):
    assert any(why in x for x in run('bauble_harrier', png(tmp_path), svg(tmp_path), pay(tmp_path, **over)))
def test_unknown_sku_blocked(tmp_path):
    assert run('mystery_mug', png(tmp_path), svg(tmp_path)) != []
def test_mug_template(tmp_path):
    assert run('mug_harrier_11oz', png(tmp_path, size=(2475, 1155)), svg(tmp_path, GOOD_SVG.replace('0 0 990 990', '0 0 2475 1155')),
               pay(tmp_path, blueprint_id=635, variant_id=72180)) == []
    assert any('size' in x for x in run('mug_harrier_11oz', png(tmp_path, size=(2700, 1050)), svg(tmp_path), None))
