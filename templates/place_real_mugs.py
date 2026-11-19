"""Stand real-mug cut-outs (templates/realmug.py: Alex's photographed mug, re-printed) on a table photo taken from the same high angle.
Usage: python3 templates/place_real_mugs.py <photo> <out.png> <spec.json>
spec: {"mugs": [{"flat": "<flat artwork png>" or null (= the photographed Fact To File mug itself), "mirror": bool, "base": [x, y] (bottom-centre of the body, 1.5x photo px),
                 "h": body height px, "blur": depth-of-field sigma}], "tint": [b, g, r] gain for the room's light, "cast": [dx, dy] shadow direction, "sat": 0.85}
Prints the mouth centre of each mug (for the steam)."""
import json, sys, numpy as np, cv2
sys.path.insert(0, 'templates'); import realmug as R
def main(photo, out, spec):
    bg = cv2.imread(photo); bg = cv2.resize(bg, (bg.shape[1]*3//2, bg.shape[0]*3//2), interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
    H, W = bg.shape[:2]; tint = np.array(spec.get('tint', [0.74, 0.86, 0.98]), np.float32); cast = spec.get('cast', [0.55, 0.22]); mouths = []
    for m in sorted(spec['mugs'], key=lambda m: m['base'][1]):                       # far mug first
        rgba = R.reskin(cv2.imread(m['flat']), m.get('mirror', False)) if m.get('flat') else R.original()
        if not m.get('flat') and m.get('mirror'): rgba = rgba[:, ::-1].copy()
        bodyh = (R.BOT[0] + R.BOT[2]) - (R.TOP[0] - R.TOP[2]); k = m['h']/bodyh
        cxp = R.CX1 if not m.get('mirror') else rgba.shape[1] - R.CX1; cxm = R.CX0 if not m.get('mirror') else rgba.shape[1] - R.CX0; basey = R.BOT[0] + R.BOT[2]
        small = cv2.resize(rgba, None, fx=k, fy=k, interpolation=cv2.INTER_AREA).astype(np.float32); sh, sw = small.shape[:2]
        x0 = int(round(m['base'][0] - cxp*k)); y0 = int(round(m['base'][1] - basey*k))
        col = small[..., :3]; al = small[..., 3:]/255.0
        hsv = cv2.cvtColor(np.clip(col, 0, 255).astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32); hsv[..., 1] *= spec.get('sat', 0.9); col = cv2.cvtColor(np.clip(hsv, 0, 255).astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)
        col = col*tint*spec.get('gain', 0.92)
        # the room's light: brighter on the side facing the lamp, a touch darker low down
        gx = np.linspace(1.06, 0.90, sw, dtype=np.float32)[None, :, None] if spec.get('light', 'left') == 'left' else np.linspace(0.90, 1.06, sw, dtype=np.float32)[None, :, None]
        gy = np.linspace(1.03, 0.93, sh, dtype=np.float32)[:, None, None]; col = np.clip(col*gx*gy, 0, 255)
        if m.get('blur'): col = cv2.GaussianBlur(col, (0, 0), m['blur']); al = cv2.GaussianBlur(al, (0, 0), m['blur'])[..., None]
        # shadows on the table: a tight dark contact line under the base and a soft cast shadow away from the light
        shadow = np.zeros((H, W), np.float32); bx, by = m['base']; rx = R.BOT[1]*k; ry = R.BOT[2]*k
        cv2.ellipse(shadow, (int(bx), int(by - ry*0.62)), (int(rx*1.07), int(ry*1.12)), 0, 0, 360, 1.0, -1)
        contact = cv2.GaussianBlur(shadow, (0, 0), 4*k + 1.5)
        tight = np.zeros((H, W), np.float32); cv2.ellipse(tight, (int(bx), int(by - ry*0.80)), (int(rx*1.0), int(ry*0.95)), 0, 0, 180, 1.0, max(2, int(5*k))); contact = np.maximum(contact*0.9, cv2.GaussianBlur(tight, (0, 0), 2.2*k + 1)*1.0)
        castm = np.zeros((H, W), np.float32)
        for i, f in enumerate(np.linspace(0.15, 1.0, 9)):
            cv2.ellipse(castm, (int(bx + cast[0]*m['h']*f), int(by - ry*0.55 + cast[1]*m['h']*f)), (int(rx*(1.0 + 0.25*f)), int(ry*(1.0 + 0.2*f))), 0, 0, 360, 0.34*(1 - 0.7*f), -1)
        castm = cv2.GaussianBlur(castm, (0, 0), 16*k + 6)
        hx = int(bx + (-(R.CX - 205)*k if not m.get('mirror') else (R.CX - 205)*k))                                  # the handle's own small shadow
        cv2.ellipse(castm, (hx, int(by - ry*0.4)), (int(70*k), int(18*k)), 0, 0, 360, 0.22, -1); castm = cv2.GaussianBlur(castm, (0, 0), 6*k + 2)
        dark = np.clip(contact*0.85 + castm*1.25, 0, 0.88)[..., None]; bg = bg*(1 - dark)
        # a faint reflection in the polished wood, only just below the base
        refl = col[::-1]; ra = al[::-1]*np.clip(np.linspace(0.16, -0.25, sh, dtype=np.float32), 0, 1)[:, None, None]
        ry0 = int(by - (sh - basey*k)) ; 
        def paste(layer, a, px, py):
            nonlocal bg
            xa, ya = max(px, 0), max(py, 0); xb, yb = min(px + layer.shape[1], W), min(py + layer.shape[0], H)
            if xb <= xa or yb <= ya: return
            l = layer[ya-py:yb-py, xa-px:xb-px]; aa = a[ya-py:yb-py, xa-px:xb-px]; bg[ya:yb, xa:xb] = bg[ya:yb, xa:xb]*(1-aa) + l*aa
        paste(cv2.GaussianBlur(refl, (0, 0), 3), cv2.GaussianBlur(ra, (0, 0), 3)[..., None], x0, int(by - (sh - basey*k) - 2 + 0) + int(2*ry*0.15))
        paste(col, al, x0, y0)
        mouths.append((int(x0 + cxm*k), int(y0 + R.TOP[0]*k)))
    noise = np.random.default_rng(3).normal(0, 1.6, bg.shape).astype(np.float32); cv2.imwrite(out, np.clip(bg + noise, 0, 255).astype(np.uint8))
    print(json.dumps(mouths))
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], json.load(open(sys.argv[3])))
