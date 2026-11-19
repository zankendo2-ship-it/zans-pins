"""Print our flat mug artwork onto BLANK photoreal mugs in a FLUX photo, the same way the baubles are made (Alex, 19 Nov 2026:
"create one that looks exactly the same and then put the print on it like you did the bauble"). The photo supplies the mug (straight sides, black handle,
rim and inside), its light, gloss and shadows; we only lay the print on the white glaze.
Usage: python3 templates/wrapmug.py <blank photo> <out.png> <spec.json>
spec: {"mugs": [{"flat": png, "top": [cx, cy, rx, ry], "bot": [cx, cy, rx, ry]  (rim and base ellipses in 1296x2304 px),
                 "handle": "right"|"left", "uh": handle angle in radians (about 1.35 = at the edge, turned a little to the camera),
                 "t0": 0.03, "t1": 0.93 (how far down the print runs), "behind": [index of a mug standing in front of this one]}]}"""
import json, sys, numpy as np, cv2
TEX_W, TEX_H, PPR = 3015.0, 1125.0, 480.0
def geom(m, h, w):
    (cx0, cy0, rx0, ry0), (cx1, cy1, rx1, ry1) = m['top'], m['bot']; ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    E = lambda t: (cx0+(cx1-cx0)*t, cy0+(cy1-cy0)*t, rx0+(rx1-rx0)*t, ry0+(ry1-ry0)*t)
    def fy(t):
        cx, cy, rx, ry = E(t); return cy + ry*np.sqrt(np.clip(1-((xs-cx)/rx)**2, 0, None))
    lo = np.zeros((h, w), np.float32); hi = np.ones((h, w), np.float32)
    for _ in range(24):
        mid = (lo+hi)/2; go = ys > fy(mid); lo = np.where(go, mid, lo); hi = np.where(go, hi, mid)
    t = (lo+hi)/2; cx, cy, rx, ry = E(t); d = (xs-cx)/rx
    valid = (ys >= fy(0.0)) & (ys <= fy(1.0)) & (np.abs(d) < 0.997)
    return t, np.arcsin(np.clip(d, -1, 1)), valid
def main(photo, out, spec):
    im = cv2.imread(photo); im = cv2.resize(im, (1296, 2304), interpolation=cv2.INTER_LANCZOS4)
    if spec.get('mirror'): im = im[:, ::-1].copy()                                                  # the same room seen the other way round: handles on the left
    im = im.astype(np.float32); h, w = im.shape[:2]; res = im.copy()
    hsv = cv2.cvtColor(im.astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32)
    glaze = np.clip((hsv[..., 2]-34)/22, 0, 1)                                                    # the white glaze, lit or in shadow, but not the black handle or rim
    G = [geom(m, h, w) for m in spec['mugs']]
    for i, m in enumerate(spec['mugs']):
        t, u, valid = G[i]; flat = cv2.imread(m['flat']).astype(np.float32); t0, t1 = m.get('t0', 0.03), m.get('t1', 0.93); uh = m.get('uh', 1.35)
        ty = (20 + (t-t0)/(t1-t0)*(1100-20))/TEX_H
        x = TEX_W - (uh - u)*PPR if m.get('handle', 'right') == 'right' else (u + uh)*PPR
        art = cv2.remap(flat, ((x % TEX_W)).astype(np.float32), (ty*TEX_H).astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        ref = m.get('white', 232.0); lum = cv2.cvtColor(im.astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32)
        tintless = np.repeat(lum[..., None], 3, axis=2)*0.55 + im*0.45                             # keep most of the room's warm cast, not all of it
        hs = cv2.cvtColor(np.clip(art, 0, 255).astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32); hs[..., 1] *= spec.get('sat', 0.9); art = cv2.cvtColor(hs.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)
        shade = np.clip(tintless/ref, 0, 1.25); printed = np.clip(art*shade, 0, 255)
        gl = np.clip((lum-238)/14, 0, 1)[..., None]; printed = printed*(1-gl) + 255*gl               # the photo's own highlights stay on top of the print
        a = (valid & (t >= t0) & (t <= t1)).astype(np.float32)
        for j in m.get('behind', []):                                                               # never print on the part hidden by a mug in front
            tj, uj, vj = G[j]; mj = spec['mugs'][j]; ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
            top = ((xs-mj['top'][0])/mj['top'][2])**2 + ((ys-mj['top'][1])/mj['top'][3])**2 <= 1
            a *= 1 - (vj | top).astype(np.float32)
        a = cv2.GaussianBlur(a, (0, 0), 1.2)*glaze; a = a[..., None]
        res = res*(1-a) + printed*a
    cv2.imwrite(out, np.clip(res, 0, 255).astype(np.uint8))
if __name__ == '__main__': main(sys.argv[1], sys.argv[2], json.load(open(sys.argv[3])))
