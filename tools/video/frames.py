"""Test frames only: the hook screen and the snow end-card."""
import numpy as np
from PIL import Image
W, H = 1080, 1920
rng = np.random.default_rng(7)
FL = [(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(2.5, 7.5), rng.uniform(.5, 1.0)) for _ in range(150)]
def snow(img):
    a = np.asarray(img.convert('RGB')).astype(np.float32); h, w = a.shape[:2]
    ky, kx = np.mgrid[-20:21, -20:21].astype(np.float32)
    for (x, y, r, op) in FL:
        xi, yi = int(x) % w, int(y) % h
        if 20 <= xi < w-20 and 20 <= yi < h-20: a[yi-20:yi+21, xi-20:xi+21] += (np.exp(-(kx**2+ky**2)/(2*r*r))*255*op)[..., None]
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))
for k, crop in (('ombudsman', 1.0), ('lossiemouth', 1.0)):
    m = Image.open(f'v/scene-{k}.png').convert('RGB').resize((W, H), Image.LANCZOS).convert('RGBA')
    Image.alpha_composite(m, Image.open(f'v/{k}-hook.png').convert('RGBA')).convert('RGB').save(f'v/test-hook-{k}.png')
snow(Image.open('v/endcard.png')).save('v/test-endcard.png')
s = Image.new('RGB', (486*3, 864))
for i, f in enumerate(('test-hook-ombudsman', 'test-hook-lossiemouth', 'test-endcard')): s.paste(Image.open(f'v/{f}.png').resize((486, 864)), (486*i, 0))
s.save('v/tests.png')
