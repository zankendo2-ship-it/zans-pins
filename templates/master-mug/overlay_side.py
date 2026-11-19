"""The master mug's side-on outline drawn over the supplier's 11oz photo (reference/mug-shape-11oz-alex-2026-11-19.jpg, handle on the left).
python3 templates/master-mug/overlay_side.py <side render.png (az 0, el about 3, long lens, no shadow)> <out.jpg>
Scaled by one number so the body widths match, lined up on the body's right edge and the base."""
import cv2, numpy as np, sys, os
H = os.path.dirname(os.path.abspath(__file__)); im = cv2.imread(H + '/../../reference/mug-shape-11oz-alex-2026-11-19.jpg'); h, w = im.shape[:2]
BX0, BX1, BY1 = 277, 731, 1340                      # supplier mug: body's left edge, right edge, bottom of the base
a = (cv2.imread(sys.argv[1], cv2.IMREAD_UNCHANGED)[..., 3] > 40).astype(np.uint8); ys, xs = np.where(a); row = a[(ys.min() + ys.max())//2 + int((ys.max() - ys.min())*0.42)]   # a row low on the body, below the handle
bx = np.where(row > 0)[0]; k = (BX1 - BX0)/(bx.max() - bx.min()); M = np.float32([[k, 0, BX1 - k*bx.max()], [0, k, BY1 - k*ys.max()]])
b = cv2.warpAffine(a, M, (w, h), flags=cv2.INTER_NEAREST); cs, _ = cv2.findContours(b, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE); o = im.copy(); cv2.drawContours(o, cs, -1, (0, 200, 255), 3)
cv2.imwrite(sys.argv[2], o[560:1460], [cv2.IMWRITE_JPEG_QUALITY, 92])
