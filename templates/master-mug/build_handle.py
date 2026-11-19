"""Builds the master mug's handle as ONE blended surface: the handle strap and the mug wall are joined with a smooth moulded fillet (no cut end,
no flare, no ring), the way glazed ceramic looks. Writes handle_mesh.json for render.js.  python3 templates/master-mug/build_handle.py
(needs numpy + scikit-image; run it only when mug.json's handle changes, then get a new all-angles sign-off)"""
import json, os, base64, numpy as np
from skimage import measure
H = os.path.dirname(os.path.abspath(__file__)); M = json.load(open(H + '/mug.json')); R = M['diameter']/2; hd = M['handle']; K = hd.get('blend', 0.55)   # K = how far the fillet spreads, cm
path = np.array([[-R + x, y] for x, y in hd['path']], np.float32)
# dense polyline through the path points
t = np.linspace(0, 1, len(path)); tt = np.linspace(0, 1, 500); line = np.stack([np.interp(tt, t, path[:, 0]), np.interp(tt, t, path[:, 1])], 1)
step = 0.035; xs = np.arange(-R - hd['reach'] - 0.9, -R + 0.75, step); ys = np.arange(min(path[:, 1]) - 1.6, max(path[:, 1]) + 1.6, step); zs = np.arange(-hd['width']/2 - 1.0, hd['width']/2 + 1.0, step)
X, Y, Z = np.meshgrid(xs, ys, zs, indexing='ij'); Zs = Z*hd['thick']/hd['width']                      # squash across, so the strap is wider than it is thick
d2 = np.full(X.shape, 1e9, np.float32)
for i in range(0, len(line), 2): d2 = np.minimum(d2, (X - line[i, 0])**2 + (Y - line[i, 1])**2 + Zs**2)
tube = np.sqrt(d2) - hd['thick']/2; cyl = np.sqrt(X**2 + Z**2) - R
h = np.clip(K - np.abs(tube - cyl), 0, None)/K; f = np.minimum(tube, cyl) - h*h*K/4                 # smooth union: the fillet
v, faces, n, _ = measure.marching_cubes(f, 0.0, spacing=(step, step, step)); v += np.array([xs[0], ys[0], zs[0]], np.float32)
# keep the strap and its fillet only; the plain wall is drawn by render.js (with the print on it)
def tube_at(p):
    d = np.full(len(p), 1e9, np.float32)
    for i in range(0, len(line), 2): d = np.minimum(d, (p[:, 0] - line[i, 0])**2 + (p[:, 1] - line[i, 1])**2 + (p[:, 2]*hd['thick']/hd['width'])**2)
    return np.sqrt(d) - hd['thick']/2
tv = tube_at(v); rad = np.sqrt(v[:, 0]**2 + v[:, 2]**2); keep_v = (tv < K*1.35) & (rad > R - 0.03); keep_f = keep_v[faces].all(1); faces = faces[keep_f]
used = np.unique(faces); remap = -np.ones(len(v), np.int64); remap[used] = np.arange(len(used)); v, n, faces = v[used], n[used], remap[faces]
n = -n; v = v + n*0.004                                                                              # outward normals; lift a hair off the wall so nothing flickers
al = np.clip((np.sqrt(v[:, 0]**2 + v[:, 2]**2) - R - 0.03)/0.03 + 0.5, 0, 1)                       # black glaze wherever the surface has lifted more than about 0.3 mm off the wall; render.js cuts at 0.5
json.dump({'count': int(len(v)), 'tris': int(len(faces)), 'pos': base64.b64encode(v.astype(np.float32).tobytes()).decode(), 'nrm': base64.b64encode(n.astype(np.float32).tobytes()).decode(),
           'idx': base64.b64encode(faces.astype(np.uint32).tobytes()).decode(), 'alpha': base64.b64encode(al.astype(np.float32).tobytes()).decode()}, open(H + '/handle_mesh.json', 'w'))
print('handle mesh:', len(v), 'points,', len(faces), 'triangles')
