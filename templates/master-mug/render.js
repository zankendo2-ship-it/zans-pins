// THE ZANS MASTER MUG (locked 19 Nov 2026). One 3D model of our real 11oz mug; every mug picture wraps the print onto THIS model.
// Never edit the shape per video. Dimensions are in mug.json (cm). Usage:
//   node templates/master-mug/render.js <out.png> '<json>'
//   json: { flat: "templates/mug-flats/x.png" | null (plain white), handle: "#0a0a0a", inside: "#0a0a0a", drink: true|false,
//           az: degrees the handle is turned from pointing left (0 = handle straight left, + = towards the camera), el: camera height in degrees,
//           fov: 28, w: 1600, h: 1600, light: "studio"|"fire", shadow: true|false (soft contact shadow under the mug), fill: 0.9 (how much of the frame the mug fills; above 1 zooms in), cx, cy, cz: the point the camera looks at, in cm (default the middle of the mug) }
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const out = process.argv[2]; const o = JSON.parse(process.argv[3] || '{}'); const M = JSON.parse(fs.readFileSync(path.join(__dirname, 'mug.json'), 'utf8'));
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const W = o.w || 1600, H = o.h || 1600; const p = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  await p.setContent('<body style="margin:0;background:transparent"></body>'); await p.addScriptTag({ path: path.join(__dirname, 'three.min.js') });
  const flat = o.flat ? 'data:image/png;base64,' + fs.readFileSync(o.flat).toString('base64') : null;
  const url = await p.evaluate(async ([M, o, flat, W, H]) => {
    const T = THREE; const R = M.diameter / 2, HT = M.height, wall = M.wall, e = M.baseEdge;
    const r = new T.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true }); r.setSize(W, H); r.setPixelRatio(2); r.outputEncoding = T.sRGBEncoding; r.toneMapping = T.ACESFilmicToneMapping; r.toneMappingExposure = o.exposure || 1.05; document.body.appendChild(r.domElement);
    const sc = new T.Scene();
    // the room the glaze reflects: soft boxes, so the gloss looks like a photo and not a flat render
    const env = new T.Scene(); env.background = new T.Color(o.light === 'fire' ? 0x1a120c : 0x9a9a9a);   // studio: a bright, even room, so the white glaze is white and shades smoothly
    const panel = (x, y, z, w, h, col, k) => { const m = new T.Mesh(new T.PlaneGeometry(w, h), new T.MeshBasicMaterial({ color: new T.Color(col).multiplyScalar(k), side: T.DoubleSide })); m.position.set(x, y, z); m.lookAt(0, 0, 0); env.add(m); };
    if (o.light === 'fire') { panel(-30, 25, 30, 30, 40, 0xfff1dc, 5); panel(40, 8, 10, 18, 22, 0xff9a45, 6); panel(0, 50, 0, 60, 60, 0xffe6c8, 1.6); panel(-20, 5, -40, 50, 30, 0xffc890, 1.2); }
    else { panel(-34, 34, 34, 60, 60, 0xffffff, 2.6); panel(44, 22, 18, 30, 50, 0xffffff, 1.6); panel(0, 60, 0, 120, 120, 0xffffff, 1.4); panel(-26, 16, 40, 18, 70, 0xffffff, 3.2); }   // the last one is a tall strip light: the glaze's highlight line
    const pm = new T.PMREMGenerator(r); sc.environment = pm.fromScene(env, o.light === 'fire' ? 0.03 : 0.16).texture;
    const glaze = (col, extra = {}) => new T.MeshPhysicalMaterial(Object.assign({ color: col, roughness: 0.16, metalness: 0, clearcoat: 1, clearcoatRoughness: 0.06, envMapIntensity: 1 }, extra));
    const mug = new T.Group(); sc.add(mug);
    // print texture: the flat artwork is the whole way round, starting and ending at the handle
    let wallMat = glaze('#ffffff');
    if (flat) { const img = await new Promise(res => { const i = new Image(); i.onload = () => res(i); i.src = flat; });
      const c = document.createElement('canvas'); c.width = 3015; c.height = 1250; const g = c.getContext('2d'); g.fillStyle = '#fff'; g.fillRect(0, 0, c.width, c.height);
      const y0 = c.height*(1 - M.printTop), y1 = c.height*(1 - M.printBottom); g.drawImage(img, 0, 20, img.width, 1080, 0, y0, c.width, y1 - y0);
      const tx = new T.CanvasTexture(c); tx.encoding = T.sRGBEncoding; tx.anisotropy = 16; wallMat = glaze('#ffffff', { map: tx }); }
    const lathe = (pts, mat) => { const m = new T.Mesh(new T.LatheGeometry(pts.map(q => new T.Vector2(q[0], q[1])), 160), mat); mug.add(m); return m; };
    const arc = (cx, cy, rad, a0, a1, n = 10) => Array.from({ length: n + 1 }, (_, i) => { const a = a0 + (a1 - a0)*i/n; return [cx + rad*Math.cos(a), cy + rad*Math.sin(a)]; });
    const rimR = wall/2, wallTop = HT - rimR;
    const wallGeo = new T.CylinderGeometry(R, R, wallTop - e, 160, 1, true, -Math.PI/2, Math.PI*2); wallGeo.translate(0, (wallTop + e)/2, 0);
    // the cylinder's v runs over the wall only; the print canvas is laid over the whole height, so shift v to match
    const uv = wallGeo.attributes.uv; for (let i = 0; i < uv.count; i++) uv.setY(i, (e + uv.getY(i)*(wallTop - e))/HT); mug.add(new T.Mesh(wallGeo, wallMat));
    lathe([[0, 0], [R - e, 0], ...arc(R - e, e, e, -Math.PI/2, 0)], glaze('#ffffff'));                                   // flat base with a small rounded edge
    const dark = glaze(o.inside || '#0a0a0a', { roughness: 0.42, clearcoat: 0.35, clearcoatRoughness: 0.35, envMapIntensity: o.light === 'fire' ? 0.45 : 0.25 });   // a soft sheen inside, no mirror-sharp reflections of the lights
    lathe([...arc(R - rimR, wallTop, rimR, 0, Math.PI), [R - wall, 0.7], [0, 0.7]], Object.assign(dark, { side: T.DoubleSide }));     // rim and inside
    if (o.drink !== false) { const d = new T.Mesh(new T.CircleGeometry(R - wall - 0.02, 96), new T.MeshPhysicalMaterial({ color: o.drinkColour || '#3a2416', roughness: 0.25, clearcoat: 0.6, envMapIntensity: 0.35 })); d.rotation.x = -Math.PI/2; d.position.y = HT - M.drinkBelowRim; mug.add(d); }
    // the handle: one smooth D-shaped strap with a moulded fillet where it meets the body at both ends
    const hp = M.handle.path.map(q => new T.Vector3(-R + q[0], q[1], 0)); const curve = new T.CatmullRomCurve3(hp, false, 'centripetal');
    const N = 220, S = 48, pos = [], idx = [];
    for (let i = 0; i <= N; i++) { const t = i/N; const c = curve.getPointAt(t), tg = curve.getTangentAt(t); const nrm = new T.Vector3(-tg.y, tg.x, 0).normalize(); const bin = new T.Vector3(0, 0, 1);
      const outD = Math.max(0, -(c.x + R)); const k = Math.max(0, 1 - outD/M.handle.filletLength); const fil = M.handle.fillet*k*k*k;   // fillet: the strap swells smoothly into the wall over the last few millimetres, like moulded ceramic
      for (let j = 0; j <= S; j++) { const a = j/S*Math.PI*2; const v = c.clone().addScaledVector(nrm, Math.cos(a)*(M.handle.thick/2 + fil)).addScaledVector(bin, Math.sin(a)*(M.handle.width/2 + fil)); pos.push(v.x, v.y, v.z); } }
    for (let i = 0; i < N; i++) for (let j = 0; j < S; j++) { const a = i*(S + 1) + j, c2 = a + S + 1; idx.push(a, c2, a + 1, a + 1, c2, c2 + 1); }
    const hg = new T.BufferGeometry(); hg.setAttribute('position', new T.Float32BufferAttribute(pos, 3)); hg.setIndex(idx); hg.computeVertexNormals();
    mug.add(new T.Mesh(hg, Object.assign(glaze(o.handle || '#0a0a0a', { roughness: 0.14, envMapIntensity: o.light === 'fire' ? 0.5 : 0.28 }), { side: T.DoubleSide })));
    mug.rotation.y = (o.az || 0)*Math.PI/180;
    if (o.shadow !== false) {                       // a soft contact shadow on the table, so the mug stands instead of floating
      const c = document.createElement('canvas'); c.width = c.height = 256; const g = c.getContext('2d'); const gr = g.createRadialGradient(128, 128, 40, 128, 128, 126);
      gr.addColorStop(0, 'rgba(0,0,0,0.55)'); gr.addColorStop(0.55, 'rgba(0,0,0,0.28)'); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(0, 0, 256, 256);
      const sh = new T.Mesh(new T.PlaneGeometry(M.diameter*1.75, M.diameter*1.75), new T.MeshBasicMaterial({ map: new T.CanvasTexture(c), transparent: true, depthWrite: false })); sh.rotation.x = -Math.PI/2; sh.position.set(0.5, 0.01, -0.2); sc.add(sh); }
    // camera: looks at the middle of the mug from `el` degrees above; the mug fills `fill` of the frame
    const fov = o.fov || 28, el = (o.el == null ? 12 : o.el)*Math.PI/180; const cam = new T.PerspectiveCamera(fov, W/H, 1, 500);
    const span = Math.max(HT, M.diameter + M.handle.reach)*1.12; const dist = span/2/Math.tan(fov*Math.PI/360)/(o.fill || 0.9);
    const tgt = new T.Vector3(o.cx || 0, o.cy == null ? HT/2 : o.cy, o.cz || 0); cam.position.set(tgt.x, tgt.y + dist*Math.sin(el), dist*Math.cos(el)); cam.lookAt(tgt);
    r.render(sc, cam); return r.domElement.toDataURL('image/png');
  }, [M, o, flat, W, H]);
  fs.writeFileSync(out, Buffer.from(url.split(',')[1], 'base64')); await b.close(); console.log('master mug ->', out);
})();
