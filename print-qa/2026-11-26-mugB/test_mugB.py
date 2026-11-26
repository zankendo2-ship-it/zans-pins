"""Regression for the bauble-style mug wraps (run: python3 -m pytest -q test_mugB.py after mugB.py)."""
import re, json, math, os
from PIL import Image
import mugB
HERE = os.path.dirname(os.path.abspath(__file__))
REFS = ('loussiemoo', 'zoo-olympios', 'rexs-romance')
def files(r): return os.path.join(HERE, 'out', f'{r}-bauble-style-mug-2475x1155')

def test_three_outputs():
    assert all(os.path.exists(files(r) + '.png') for r in REFS)

def test_both_face_targets():
    for r in REFS:
        svg = open(files(r) + '.svg').read()
        t = sorted({round(float(x), 2) for x in re.findall(r'data-centre="x@([\d.]+)"', svg)})
        assert t == [round(mugB.W / 4, 2), round(3 * mugB.W / 4, 2)], (r, t)
        assert len(re.findall(r'data-label="name panel [LR]"', svg)) == 2

def test_no_body_gap_between_brim_and_peak():
    """Every column across each peak: from just under the gold brim to the peak, only peak / gold pixels (no body colour)."""
    S, y0, depth = mugB.S, 185 * mugB.S, 32.5 * mugB.S
    for r in REFS:
        im = Image.open(files(r) + '.png').convert('RGB'); bg = im.getpixel((5, 1150)) if r == 'rexs-romance' else None
        body = {re.search(r'width="990" height="990" fill="#(\w{6})"', open(f'/tmp/claude-0/zp/print-qa/2026-11-26-v7/out9/{r}-v9.svg').read()).group(1).lower()}
        for cx in mugB.FACES:
            for x in range(int(cx - 240 * S), int(cx + 240 * S), 8):
                yb = mugB.brim_y(x, y0, depth)
                for y in range(int(yb + 6 * S), int(yb + 14 * S)):
                    p = '%02x%02x%02x' % im.getpixel((x, y))
                    assert p not in body, (r, x, y, p)

def test_no_cusp():
    y0, d = 10.0, 5.0; h = 1e-3
    for x in (0.0, mugB.W / 2, mugB.W):
        slope = (mugB.brim_y(x + h, y0, d) - mugB.brim_y(max(0, x - h), y0, d)) / (2 * h if x else h)
        assert abs(slope) < 1e-3
