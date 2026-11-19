"""PASS/FAIL picture for the master mug: its outline (and the hole in the handle) drawn over Alex's real mug photo at the same angle.
python3 templates/master-mug/overlay.py <render.png from render.js at the photo's angle> <out.jpg> [blend.jpg]
The render is scaled by ONE number (same in both directions) so its height matches the real mug's, and centred on it; nothing is stretched to fit.
Photo angle: {"az":26,"el":36,"fov":54,"fill":0.75}"""
import cv2, numpy as np, sys, os
H = os.path.dirname(os.path.abspath(__file__)); im = cv2.imread(H + '/../../reference/real-mug-fact-to-file.jpg'); h, w = im.shape[:2]
X0, X1, Y0, Y1 = 89, 797, 168, 823                 # the real mug in the photo: handle's left edge, body's right edge, top of the rim, bottom of the base
a = cv2.imread(sys.argv[1], cv2.IMREAD_UNCHANGED); m = (a[..., 3] > 40).astype(np.uint8); ys, xs = np.where(m); k = (Y1 - Y0 + 1)/(ys.max() - ys.min() + 1)
M = np.float32([[k, 0, (X0 + X1)/2 - k*(xs.min() + xs.max())/2], [0, k, (Y0 + Y1)/2 - k*(ys.min() + ys.max())/2]])
b = cv2.warpAffine(m, M, (w, h), flags=cv2.INTER_NEAREST); cs, _ = cv2.findContours(b, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE); o = im.copy(); cv2.drawContours(o, cs, -1, (0, 255, 255), 3)
ys, xs = np.where(b); print('model box', xs.min(), xs.max(), ys.min(), ys.max(), '| real box', X0, X1, Y0, Y1, '| width differs by', round(100*((xs.max()-xs.min())/(X1-X0) - 1), 1), '%')
cv2.imwrite(sys.argv[2], o, [cv2.IMWRITE_JPEG_QUALITY, 92])
if len(sys.argv) > 3:
    c = cv2.warpAffine(a, M, (w, h), flags=cv2.INTER_AREA).astype(np.float32); kk = c[..., 3:]/255.0*0.5; cv2.imwrite(sys.argv[3], (im*(1 - kk) + c[..., :3]*kk).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 92])
