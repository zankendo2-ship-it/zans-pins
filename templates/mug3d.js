// The exact ZANS mug (the website designer's own 3D model of the Printify mug: 9.6 cm high x 8.2 cm wide, with the real print), rendered with a clear background.
// node templates/mug3d.js <out_dir> '<json>'
// job: [file, pattern, colour1, colour2, handleColour, name, "left"|"right", opts]
//   handleColour 'White' = the all-white mug (White Silks Mug listing).
//   opts (optional): { light: "fire"|"overcast"|"studio", tea: true|false, turn: radians the name panel is turned towards the camera (default 0.8), camY: camera height (default 1.5), ring: '#hex' = print the cap-colour ring round the top (false = no ring) }
const { chromium } = require('playwright'); const fs = require('fs');
const jobs = JSON.parse(process.argv[3]);
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  for (const [f, pat, c1, c2, handle, name, side, opts = {}] of jobs) {
    const p = await b.newPage({ viewport: { width: 430, height: 900 }, deviceScaleFactor: 2 });
    await p.goto('https://www.zanshorseracing.co.uk/mug-designer/', { waitUntil: 'networkidle' });
    const setCol = (id, v) => p.evaluate(([id, v]) => { const e = document.getElementById(id); e.value = v.toLowerCase(); e.dispatchEvent(new Event('input', { bubbles: true })); e.dispatchEvent(new Event('change', { bubbles: true })); }, [id, v]);
    await p.locator('button:visible', { hasText: new RegExp('^' + pat + '$') }).first().click(); await p.waitForTimeout(200);
    await setCol('pick1', c1); await setCol('pick2', c2);
    if (handle !== 'White') await p.locator('button:visible', { hasText: new RegExp('^' + handle + '$') }).first().click();
    if (opts.ring) { await p.evaluate(() => { const r = document.getElementById('ring'); if (!r.checked) r.click(); }); await setCol('capcol', opts.ring); } else if (opts.ring === false) await p.evaluate(() => { const r = document.getElementById('ring'); if (r.checked) r.click(); });
    await p.fill('#name', name); await p.waitForTimeout(1200);
    const code = await p.evaluate(() => [...new Set(document.body.innerText.match(/Z[A-Z]{2}-[\w-]+/g) || [])].join(' '));
    const url = await p.evaluate(([side, handle, o]) => { const N = 1800;
      if (handle === 'White') { handleMat.color.set('#ffffff'); insideMat.color.set('#ffffff'); }
      const light = o.light || 'studio';
      if (light !== 'studio') {                      // light the mug like its scene, not like a shop mock-up
        scene.children.filter(c => c.isLight).forEach(c => scene.remove(c));
        if (light === 'fire') {                      // fire behind the mugs: warm rim light from the back, dim warm fill from the room
          scene.add(new THREE.HemisphereLight(0xfff0de, 0x8a6c52, 0.80));   // bright enough that white stays white and the handle keeps its colour
          const back = new THREE.DirectionalLight(0xffc080, 0.45); back.position.set(0.6, 3.0, -6); scene.add(back);
          const sideL = new THREE.DirectionalLight(0xffe0c0, 0.22); sideL.position.set(-6, 2.5, 2); scene.add(sideL);
          const front = new THREE.DirectionalLight(0xfff2e4, 0.42); front.position.set(1.5, 3.5, 7); scene.add(front);
        } else {                                     // flat grey winter daylight from the whole sky
          scene.add(new THREE.HemisphereLight(0xeef3f8, 0x6f7068, 0.92));
          const sky = new THREE.DirectionalLight(0xffffff, 0.34); sky.position.set(-2, 8, 3); scene.add(sky);
          const front = new THREE.DirectionalLight(0xf4f7fa, 0.18); front.position.set(1, 2, 8); scene.add(front);
        }
      }
      if (o.handle !== 'model') {                    // matched to Alex's photo of the real mug (reference/real-mug-fact-to-file.jpg, 19 Nov 2026): a big round C handle, thick and glossy, and a rim in the handle colour
        const hc = handle === 'White' ? '#ffffff' : '#' + handleMat.color.getHexString();
        group.traverse(c => { if (!c.isMesh) return;
          if (c.material === handleMat) { c.geometry.dispose(); c.geometry = new THREE.TorusGeometry(0.62, 0.115, 28, 96, Math.PI); }
          else if (c.geometry.type === 'TorusGeometry') { c.geometry.dispose(); c.geometry = new THREE.TorusGeometry(0.992, 0.03, 16, 128); c.material = new THREE.MeshPhongMaterial({ color: hc, shininess: 90, specular: 0x777777 }); }
          else if (c.material.map) { c.material.shininess = 80; c.material.specular && c.material.specular.set(0x4a4a4a); } });
        handleMat.shininess = 90; handleMat.specular && handleMat.specular.set(0x777777);
      }
      if (o.tea !== false) {                         // a drink in the mug, as in Alex's own photo of the real mug
        const tea = new THREE.Mesh(new THREE.CircleGeometry(0.975, 96), new THREE.MeshPhongMaterial({ color: 0x5a3a24, shininess: 60, specular: 0x444444 }));
        tea.rotation.x = -Math.PI / 2; tea.position.y = 2.34 / 2 - (o.teaDrop === undefined ? 0.24 : o.teaDrop); group.add(tea);
      }
      renderer.setPixelRatio(1); renderer.setSize(N, N, false); camera.aspect = 1; camera.fov = 20; camera.position.set(0, o.camY === undefined ? 1.5 : o.camY, 9.4); camera.lookAt(0, 0, 0); camera.updateProjectionMatrix();
      tex.anisotropy = renderer.capabilities.getMaxAnisotropy(); tex.needsUpdate = true;
      const turn = o.turn === undefined ? 0.8 : o.turn;
      group.rotation.y = side === 'right' ? -turn : Math.PI + turn; renderer.render(scene, camera);
      return renderer.domElement.toDataURL('image/png'); }, [side, handle, opts]);
    fs.writeFileSync(process.argv[2] + '/' + f, Buffer.from(url.split(',')[1], 'base64')); console.log(f, code); await p.close(); }
  await b.close(); })();
