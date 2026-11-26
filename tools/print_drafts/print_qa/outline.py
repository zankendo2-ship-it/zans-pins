"""Turn every <text> in a print master into outlined <path> glyphs (no fonts, no CSS left in the file).
Shaping: HarfBuzz (kerning + ligatures) on the self-hosted Jost variable font at the text's weight.
text-anchor start/middle/end is honoured; letter-spacing is added between letters but NOT after the last one,
so middle-anchored names sit exactly on the centre line.
Each outlined text becomes <g data-text="..." data-font-size=".." data-cap-mm-src="font-size"> so preflight can
measure letter height. usage: outline.py in.svg out.svg"""
import html, io, os, re, sys
import uharfbuzz as hb
from fontTools.ttLib import TTFont
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, 'fonts', 'jost-latin.woff2')
_face = None

def face():
    global _face
    if _face is None:
        f = TTFont(FONT); f.flavor = None; b = io.BytesIO(); f.save(b)
        _face = hb.Face(b.getvalue())
    return _face

class Pen:
    def __init__(s, sc, ox, oy): s.d, s.sc, s.ox, s.oy = [], sc, ox, oy
    def p(s, x, y): return f'{s.ox + x * s.sc:.2f},{s.oy - y * s.sc:.2f}'
    def moveTo(s, a): s.d.append('M' + s.p(*a))
    def lineTo(s, a): s.d.append('L' + s.p(*a))
    def qCurveTo(s, *a):
        pts = list(a)
        while len(pts) > 2:  # implied on-curve points between off-curve pairs
            c, n = pts[0], pts[1]; m = ((c[0] + n[0]) / 2, (c[1] + n[1]) / 2)
            s.d.append('Q' + s.p(*c) + ' ' + s.p(*m)); pts = pts[1:]
        s.d.append('Q' + s.p(*pts[0]) + ' ' + s.p(*pts[1]))
    def curveTo(s, a, b, c): s.d.append('C' + s.p(*a) + ' ' + s.p(*b) + ' ' + s.p(*c))
    def closePath(s): s.d.append('Z')
    endPath = closePath

def shape(txt, size, weight, ls):
    fc = face(); font = hb.Font(fc); font.set_variations({'wght': float(weight)})
    upem = fc.upem; buf = hb.Buffer(); buf.add_str(txt); buf.guess_segment_properties()
    hb.shape(font, buf, {'kern': True, 'liga': True})
    sc = size / upem; glyphs, x = [], 0.0
    infos, pos = buf.glyph_infos, buf.glyph_positions
    for i, (gi, gp) in enumerate(zip(infos, pos)):
        glyphs.append((gi.codepoint, x + gp.x_offset * sc, gp.y_offset * sc))
        x += gp.x_advance * sc + (ls if i < len(infos) - 1 else 0)
    return font, sc, glyphs, x

def outline_text(attrs, txt):
    g = lambda k, d=None: (re.search(rf'\b{k}="([^"]*)"', attrs) or [None, d])[1]
    size = float(g('font-size', 16)); weight = float(g('font-weight', 400)); ls = float(g('letter-spacing', 0) or 0)
    x0, y0 = float(g('x', 0)), float(g('y', 0)); anchor = g('text-anchor', 'start'); fill = g('fill', '#000000')
    font, sc, glyphs, width = shape(txt, size, weight, ls)
    x0 -= {'middle': width / 2, 'end': width}.get(anchor, 0)
    d = []
    for gid, gx, gy in glyphs:
        pen = Pen(sc, x0 + gx, y0 - gy); font.draw_glyph_with_pen(gid, pen); d += pen.d
    tr = g('transform'); t = f' transform="{tr}"' if tr else ''
    t += ''.join(f' {k}="{v}"' for k, v in re.findall(r'\b(data-[\w-]+)="([^"]*)"', attrs) if k not in ('data-text', 'data-font-size'))
    return (f'<g data-text="{html.escape(txt, quote=True)}" data-font-size="{size:g}"{t}>'
            f'<path d="{"".join(d)}" fill="{fill}"/></g>')

def outline_svg(s):
    s = re.sub(r'<style\b[^>]*>.*?</style>', '', s, flags=re.S)  # font CSS no longer needed once outlined
    return re.sub(r'<text\b([^>]*)>(.*?)</text>', lambda m: outline_text(m.group(1), html.unescape(re.sub(r'<[^>]+>', '', m.group(2)))), s, flags=re.S)

if __name__ == '__main__':
    open(sys.argv[2], 'w').write(outline_svg(open(sys.argv[1], encoding='utf8').read()))
