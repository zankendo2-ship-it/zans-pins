"""Regression for the bauble-style mug wraps. Repo-relative, run in a clean checkout:
   PW_CHROMIUM=<chrome> python3 mugB.py && python3 -m pytest -q test_mugB.py"""
import re, os
from PIL import Image
import mugB
HERE = os.path.dirname(os.path.abspath(__file__))
REFS = ('loussiemoo', 'zoo-olympios', 'rexs-romance')
def base(r): return os.path.join(HERE, 'out', f'{r}-bauble-style-mug-2475x1155')
def v9(r): return open(os.path.join(HERE, 'inputs', f'{r}-v9.svg')).read()
def near(a, b, tol=40): return sum(abs(x - y) for x, y in zip(a, b)) <= tol
def hexrgb(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))

def peak_interior_columns(r, im):
    """Every column across each peak, from just under the brim to just above the peak's own lower edge."""
    S, y0, depth = mugB.S, 185 * mugB.S, 32.5 * mugB.S
    for cx in mugB.FACES:
        for x in range(int(cx - 262 * S), int(cx + 262 * S) + 1):
            yt = mugB.brim_y(x, y0, depth) + 5 * S           # clear of the gold brim line
            yield x, int(yt), cx

def allowed(r):
    s = v9(r); pk = hexrgb(re.search(r'<path d="M225,219 [^"]+" fill="(#\w{6})"', s).group(1))
    return [pk, hexrgb('#C9A646')]

def gap_hits(r, im):
    ok = allowed(r); bad = []
    for x, y, cx in peak_interior_columns(r, im):
        if abs(x - cx) > 255 * mugB.S: continue
        p = im.getpixel((x, y))
        if not any(near(p, a) for a in ok): bad.append((x, y, p))
    return bad

def test_three_outputs():
    assert all(os.path.exists(base(r) + '.png') for r in REFS)

def test_both_face_targets():
    for r in REFS:
        svg = open(base(r) + '.svg').read()
        t = sorted({round(float(x), 2) for x in re.findall(r'data-centre="x@([\d.]+)"', svg)})
        assert t == [round(mugB.W / 4, 2), round(3 * mugB.W / 4, 2)], (r, t)
        assert len(re.findall(r'data-label="name panel [LR]"', svg)) == 2

def test_no_gap_every_column_peak_and_gold_only():
    for r in REFS:
        assert gap_hits(r, Image.open(base(r) + '.png').convert('RGB')) == [], r

def test_gap_check_catches_a_defective_fixture():
    """Deliberately defective: body-colour dots leak across the peak -> the check must fail."""
    for r in REFS:
        im = Image.open(base(r) + '.png').convert('RGB').copy()
        body = hexrgb(re.search(r'width="990" height="990" fill="(#\w{6})"', v9(r)).group(1))
        cx = mugB.FACES[0]; S, y0, depth = mugB.S, 185 * mugB.S, 32.5 * mugB.S
        for xx in range(int(cx) - 3, int(cx) + 4):
            yy = int(mugB.brim_y(xx, y0, depth) + 5 * S)
            for dy in range(-2, 3): im.putpixel((xx, yy + dy), body)
        assert gap_hits(r, im), r

def test_rendered_brim_is_smooth_at_the_joins():
    """On the rendered PNG: the gold brim line's y at each join (x = 0 / W/2 / W) differs by < 2 px from 12 px either side."""
    for r in REFS:
        im = Image.open(base(r) + '.png').convert('RGB'); gold = hexrgb('#C9A646')
        def gold_y(x):
            ys = [y for y in range(120, 280) if near(im.getpixel((x, y)), gold, 60)]
            return sum(ys) / len(ys)
        for xj in (mugB.W // 2, 12, mugB.W - 13):
            assert abs(gold_y(max(2, xj - 12)) - gold_y(min(mugB.W - 3, xj + 12))) < 2.0, (r, xj)

def test_button_clears_the_top_edge():
    for r in REFS:
        im = Image.open(base(r) + '.png').convert('RGB'); S = mugB.S
        for cx in mugB.FACES:
            col = [im.getpixel((int(cx), y)) for y in range(0, 120)]
            top = next(i for i, p in enumerate(col) if p != col[0])
            assert top / (mugB.W / mugB.MM) >= 6.0, (r, top)
