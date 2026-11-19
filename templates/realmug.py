"""Build a mug picture from Alex's photo of the REAL mug (reference/real-mug-fact-to-file.jpg): the real handle, rim, inside, drink, gloss and shading are kept,
and only the printed wrap is swapped for another design's flat artwork (from templates/mug_flat.js). Returns RGBA cut-outs.
geometry of the mug in the photo (952x1183): the body is a cone between two ellipses."""
import numpy as np, cv2
REF = 'reference/real-mug-fact-to-file.jpg'
CX = 534.5; TOP = (285.0, 261.0, 118.0); BOT = (742.0, 159.0, 81.0)      # (cy, rx, ry) of the rim and the base
def ell(t): return TOP[0] + (BOT[0]-TOP[0])*t, TOP[1] + (BOT[1]-TOP[1])*t, TOP[2] + (BOT[2]-TOP[2])*t
def uv_map(h=1183, w=952):
    """for every pixel on the front of the body: t (0 rim .. 1 base) and u (angle, -pi/2 left edge .. +pi/2 right edge)."""
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32); lo = np.zeros((h, w), np.float32); hi = np.ones((h, w), np.float32)
    def front_y(t):
        cy, rx, ry = ell(t); s = np.clip(1 - ((xs-CX)/rx)**2, 0, None); return cy + ry*np.sqrt(s), np.abs(xs-CX) <= rx
    y0, in0 = front_y(0.0); y1, in1 = front_y(1.0)
    for _ in range(26):
        mid = (lo+hi)/2; ym, _ = front_y(mid); go = ys > ym; lo = np.where(go, mid, lo); hi = np.where(go, hi, mid)
    t = (lo+hi)/2; cy, rx, ry = ell(t); d = (xs-CX)/rx
    valid = (ys >= y0) & (ys <= y1 + 0.5) & (np.abs(d) < 0.995) & in0
    # pixels beside the base ellipse but inside the cone sides
    return t, np.arcsin(np.clip(d, -1, 1)), valid
T_PTS = [0.0, 0.009, 0.182, 0.31, 0.43, 0.55, 0.65, 0.745, 0.827, 0.911, 0.979, 1.0]          # measured on the photo: where each hoop starts down the mug
Y_PTS = [30, 38, 168, 262, 373, 486, 597, 710, 821, 934, 1045, 1080]                       # the same edges in the flat artwork (1125 rows)
U0, X0, PX_PER_RAD, TEX_W = -0.936, 172.0, 436.0, 3015.0                                   # the name panel's left edge: angle on the photo, column in the artwork
def tex_coords(t, u, mirror=False):
    """flat-artwork coordinates (0..1) for each body pixel. mirror = the other side of the handle (the cut-out is flipped left to right afterwards)."""
    ty = np.interp(t, T_PTS, Y_PTS)/1125.0; x = X0 + (u - U0)*PX_PER_RAD
    if mirror: x = TEX_W - x
    return (x/TEX_W) % 1.0, ty
def sample(flat, tx, ty):
    H, W = flat.shape[:2]; mx = (tx*W).astype(np.float32); my = (ty*H).astype(np.float32)
    return cv2.remap(flat, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

def body_mask(h=1183, w=952):
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32); m = np.zeros((h, w), bool)
    for t in np.linspace(0, 1, 500):
        cy, rx, ry = ell(t); m |= ((xs-CX)/rx)**2 + ((ys-cy)/ry)**2 <= 1
    return m
def cutout():
    """alpha for the whole real mug (body + handle, hole open), from the photo."""
    im = cv2.imread(REF); h, w = im.shape[:2]; body = body_mask(h, w); g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    gc = np.zeros((h, w), np.uint8); cv2.grabCut(im, gc, (70, 150, 750, 690), np.zeros((1, 65)), np.zeros((1, 65)), 6, cv2.GC_INIT_WITH_RECT)
    fg = ((gc == 1) | (gc == 3)); left = np.zeros((h, w), bool); left[290:730, 60:350] = True
    bright = ((g > 135) & left & ~body).astype(np.uint8)
    hole = cv2.morphologyEx(bright, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41)))      # the big bright gap inside the handle, not the thin white lugs
    n, lab, st, cen = cv2.connectedComponentsWithStats(hole); best = min(range(1, n), key=lambda i: abs(cen[i][0]-205) + abs(cen[i][1]-500)); hole = lab == best
    hole = cv2.dilate(hole.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))).astype(bool)
    dark = cv2.morphologyEx((g < 100).astype(np.uint8), cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))).astype(bool)
    n, lab, st, _ = cv2.connectedComponentsWithStats((dark & left & ~body).astype(np.uint8)); hand = lab == (1 + np.argmax(st[1:, cv2.CC_STAT_AREA]))
    ring = cv2.morphologyEx((hand | hole).astype(np.uint8), cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31))).astype(bool) & ~hole   # handle with its highlights
    xs = np.mgrid[0:h, 0:w][1]; lugs = fg & left & ~hole & (xs > 262) & cv2.dilate(ring.astype(np.uint8), np.ones((41, 41), np.uint8)).astype(bool)        # white joins between handle and body
    m = (body | ring | lugs).astype(np.uint8)*255
    return cv2.GaussianBlur(m, (0, 0), 1.2)
def _shade(im, valid, t):
    """the real light on the body, from the photo alone: each pixel's brightness against the usual brightness of its own colour (red, yellow, green or white), smoothed."""
    hsv = cv2.cvtColor(im.astype(np.uint8), cv2.COLOR_BGR2HSV); H, S, V = [hsv[..., i].astype(np.float32) for i in range(3)]
    L = cv2.cvtColor(im.astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32); cls = np.full(L.shape, -1)
    cls[(S < 60) & (V > 120)] = 0; cls[(S >= 60) & ((H < 10) | (H > 165))] = 1; cls[(S >= 60) & (H >= 15) & (H <= 38)] = 2; cls[(S >= 60) & (H >= 39) & (H <= 95)] = 3
    rel = np.zeros_like(L); wgt = np.zeros_like(L); zone = valid & (t > 0.03) & (t < 0.97)
    for c in range(4):
        m = (cls == c) & zone
        if m.sum() < 200: continue
        core = cv2.erode(m.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool); med = np.median(L[core]) if core.sum() else np.median(L[m])
        rel[core] = L[core]/med; wgt[core] = 1
    sm = cv2.GaussianBlur(rel*wgt, (0, 0), 10)/np.maximum(cv2.GaussianBlur(wgt, (0, 0), 10), 1e-3)
    white = np.median(im[(cls == 0) & zone], axis=0)/255.0                        # the photo's white balance and exposure on a white part of the print
    hi = ((V > 232) & (S < 45) & zone & (cls != 0)).astype(np.float32); hi = cv2.GaussianBlur(hi, (0, 0), 1.2)   # real specular glints on the coloured glaze
    return sm, white, hi
def reskin(flat_new, mirror=False):
    """the real mug with another design printed on it: only the wrap changes; handle, rim, inside, drink and the light are the photo's own."""
    im = cv2.imread(REF).astype(np.float32); t, u, valid = uv_map(); txn, tyn = tex_coords(t, u, mirror); new = sample(flat_new, txn, tyn).astype(np.float32)
    sm, white, hi = _shade(im, valid, t)
    out = np.clip(new*white[None, None, :]*sm[..., None], 0, 255); out = out*(1-hi[..., None]*0.85) + 255*hi[..., None]*0.85
    grain = im - cv2.GaussianBlur(im, (0, 0), 1.0); out = np.clip(out + grain*0.6, 0, 255)                      # the photo's own fine noise, so the wrap is not cleaner than the rest
    a = cv2.GaussianBlur((valid & (t > 0.014) & (t < 0.985)).astype(np.float32), (0, 0), 1.3)[..., None]
    res = (im*(1-a) + out*a).astype(np.uint8); rgba = np.dstack([res, cutout()])
    return rgba[:, ::-1].copy() if mirror else rgba
def original():
    return np.dstack([cv2.imread(REF), cutout()])
