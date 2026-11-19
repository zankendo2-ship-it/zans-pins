"""PASS/FAIL picture for the master mug: its outline (and the hole in the handle) drawn over Alex's real mug photo at the same angle.
python3 templates/master-mug/overlay.py <render.png from render.js at the photo's angle> <out.jpg>   (the real mug's box in the photo is fixed below)"""
import cv2, numpy as np, sys, os
H = os.path.dirname(os.path.abspath(__file__)); im = cv2.imread(H + '/../../reference/real-mug-fact-to-file.jpg')
X0, X1, Y0, Y1 = 88, 797, 168, 822                 # the real mug in the photo: handle's left edge, body's right edge, top of the rim, bottom of the base
a = (cv2.imread(sys.argv[1], cv2.IMREAD_UNCHANGED)[..., 3] > 40).astype(np.uint8); ys, xs = np.where(a); c = a[ys.min():ys.max()+1, xs.min():xs.max()+1]
c = cv2.resize(c, (X1 - X0 + 1, Y1 - Y0 + 1), interpolation=cv2.INTER_NEAREST); full = np.zeros(im.shape[:2], np.uint8); full[Y0:Y1+1, X0:X1+1] = c
cs, _ = cv2.findContours(full, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE); o = im.copy(); cv2.drawContours(o, cs, -1, (0, 255, 255), 3)
print('model box aspect', round(c.shape[1]/c.shape[0], 3), '(real', round((X1-X0+1)/(Y1-Y0+1), 3), ')'); cv2.imwrite(sys.argv[2], o, [cv2.IMWRITE_JPEG_QUALITY, 92])
