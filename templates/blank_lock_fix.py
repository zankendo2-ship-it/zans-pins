"""Makes the locked-shape blank mug photo usable (19 Nov 2026): FLUX gave the back mug a white handle and both handles white roots; our real mug's
handle is black all the way to the body. Usage: python3 templates/blank_lock_fix.py  (reads/writes templates/scenes/pool/blank-mugs-11oz-lock-tree-fire*)"""
import numpy as np, cv2, os
H = os.path.dirname(os.path.abspath(__file__)) + '/scenes/pool/'
im = cv2.resize(cv2.imread(H + 'blank-mugs-11oz-lock-tree-fire-original.webp'), (1296, 2304), interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
hsv = cv2.cvtColor(im.astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32); V, Sa = hsv[..., 2], hsv[..., 1]; ys, xs = np.mgrid[0:2304, 0:1296].astype(np.float32)
def gloss(mask, streak=0.0):                      # black glaze that keeps the photo's own highlights; streak adds a soft highlight along the upper-left edge
    m = cv2.GaussianBlur(mask.astype(np.float32), (0, 0), 1.6)[..., None]
    black = np.clip((V - 205)/45, 0, 1)*175 + np.clip(V/255, 0, 1)*22 + 6
    if streak:
        core = cv2.erode(mask.astype(np.uint8), np.ones((9, 9), np.uint8)).astype(np.float32)
        edge = np.clip(core - np.roll(np.roll(core, 9, axis=0), 9, axis=1), 0, 1)             # the band just inside the upper-left edge
        black = black + cv2.GaussianBlur(edge, (0, 0), 3.5)*streak
    return m, np.repeat(black[..., None], 3, 2)
# back mug: the whole handle (white on the dark room), right of the body
box = (xs > 1074) & (xs < 1296) & (ys > 1050) & (ys < 1545)
m = ((V > 105) & (Sa < 70) & box).astype(np.uint8); m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)); m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (27, 27)))
n, lab, st, _ = cv2.connectedComponentsWithStats(m); m = (lab == 1 + np.argmax(st[1:, 4])); m = cv2.dilate(m.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
ell = lambda cx, cy, rx, ry: ((xs-cx)/rx)**2 + ((ys-cy)/ry)**2 <= 1
masks = [(m | ell(1056, 1128, 30, 36) | ell(1054, 1470, 32, 36), 70.0),                        # ...and its two roots on the body
         (ell(676, 1246, 42, 50) | ell(676, 1642, 44, 46), 0.0)]                                 # front mug: the two white stubs
res = im.copy()
for mk, st_ in masks:
    a, blk = gloss(mk, st_); res = res*(1-a) + blk*a
cv2.imwrite(H + 'blank-mugs-11oz-lock-tree-fire.jpg', np.clip(res, 0, 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 96])
