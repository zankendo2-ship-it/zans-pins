"""Alex, 21 Nov 2026 (photo of the real horse): the rider's cap is BLACK. Recolours the white helmet in the hub's opener v3 clip, frame by frame, changing nothing else.
python3 blackcap.py hub/opener-v3.mp4 hub/opener-v3-blackcap.mp4"""
import sys, subprocess, numpy as np, cv2, imageio_ffmpeg
src, out = sys.argv[1:3]; FF = imageio_ffmpeg.get_ffmpeg_exe(); W, H = 1080, 1920
raw = subprocess.run([FF, '-loglevel', 'error', '-i', src, '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3).copy(); enc = subprocess.Popen([FF, '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', '30', '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '14', out], stdin=subprocess.PIPE)
for i, f in enumerate(fr):
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV); white = ((hsv[..., 2] > 150) & (hsv[..., 1] < 70)).astype(np.uint8); white[1300:] = 0
    white = cv2.morphologyEx(white, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)); n, lab, st, cen = cv2.connectedComponentsWithStats(white)
    comps = [(st[k], k) for k in range(1, n) if st[k][4] > 250]; silks = max(comps, key=lambda c: c[0][4])            # the rider's silks: the biggest white shape
    sx, sy, sw, sh, _ = silks[0]; best = None
    for s, k in comps:                                                                                             # the helmet: a smaller white shape sitting just above the silks
        x, y, w, h, a = s
        if k != silks[1] and a < 12000 and y + h <= sy + 60 and y + h >= sy - 90 and x + w > sx - 40 and x < sx + sw + 40: best = (a, k) if best is None or a > best[0] else best
    if best is None: print('no cap found, frame', i); enc.stdin.write(f.tobytes()); continue
    cx, cy, cw, ch, _ = st[best[1]]; capm = (lab == best[1]).astype(np.uint8)
    brim = np.zeros_like(capm); y1 = min(cy + ch + 13, sy + 10); brim[cy:y1, max(0, cx - 30):cx + cw + 6] = ((hsv[cy:y1, max(0, cx - 30):cx + cw + 6, 2] > 120) & (hsv[cy:y1, max(0, cx - 30):cx + cw + 6, 1] < 90)).astype(np.uint8)   # the white peak under the cap
    capm = np.maximum(capm, brim)
    m = cv2.dilate(capm, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))); m = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 1.6)[..., None]
    g = f.astype(np.float32); dark = 14 + (g - g.min()) * 0.10                                                     # black silk, keeping a little of its own shine
    enc.stdin.write(np.clip(g * (1 - m) + dark * m, 0, 255).astype(np.uint8).tobytes())
enc.stdin.close(); enc.wait(); print('frames', len(fr))
