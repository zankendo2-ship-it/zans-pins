// The exact ZANS mug (the website designer's own 3D model of the Printify mug, with the real print), rendered with a clear background.
// node mug3d.js <out_dir> '<json>'   job: [file, pattern, colour1, colour2, handleColour, name, "left"|"right"]
const { chromium } = require('playwright'); const fs = require('fs');
const jobs = JSON.parse(process.argv[3]);
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  for (const [f, pat, c1, c2, handle, name, side] of jobs) {   // handle 'White' = the all-white mug (White Silks Mug listing)
    const p = await b.newPage({ viewport: { width: 430, height: 900 }, deviceScaleFactor: 2 });
    await p.goto('https://www.zanshorseracing.co.uk/mug-designer/', { waitUntil: 'networkidle' });
    const setCol = (id, v) => p.evaluate(([id, v]) => { const e = document.getElementById(id); e.value = v.toLowerCase(); e.dispatchEvent(new Event('input', { bubbles: true })); e.dispatchEvent(new Event('change', { bubbles: true })); }, [id, v]);
    await p.locator('button:visible', { hasText: new RegExp('^' + pat + '$') }).first().click(); await p.waitForTimeout(200);
    await setCol('pick1', c1); await setCol('pick2', c2);
    if (handle !== 'White') await p.locator('button:visible', { hasText: new RegExp('^' + handle + '$') }).first().click();
    await p.fill('#name', name); await p.waitForTimeout(1200);
    const code = await p.evaluate(() => [...new Set(document.body.innerText.match(/Z[A-Z]{2}-[\w-]+/g) || [])].join(' '));
    const url = await p.evaluate(([side, handle]) => { const N = 1800; if (handle === 'White') { handleMat.color.set('#ffffff'); insideMat.color.set('#ffffff'); }
      renderer.setPixelRatio(1); renderer.setSize(N, N, false); camera.aspect = 1; camera.fov = 20; camera.position.set(0, 2.5, 9.2); camera.lookAt(0, 0, 0); camera.updateProjectionMatrix();
      tex.anisotropy = renderer.capabilities.getMaxAnisotropy(); tex.needsUpdate = true;
      group.rotation.y = side === 'right' ? -0.5 : Math.PI + 0.5; renderer.render(scene, camera);
      return renderer.domElement.toDataURL('image/png'); }, [side, handle]);
    fs.writeFileSync(process.argv[2] + '/' + f, Buffer.from(url.split(',')[1], 'base64')); console.log(f, code); await p.close(); }
  await b.close(); })();
