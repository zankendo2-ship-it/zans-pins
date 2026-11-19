const { chromium } = require('playwright'); const fs = require('fs');
const jobs = JSON.parse(process.argv[3]);
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  for (const [f, pat, c1, c2, handle, name, ring] of jobs) {
    const p = await b.newPage({ viewport: { width: 430, height: 900 }, deviceScaleFactor: 2 });
    await p.goto('https://www.zanshorseracing.co.uk/mug-designer/', { waitUntil: 'networkidle' });
    const setCol = (id, v) => p.evaluate(([id, v]) => { const e = document.getElementById(id); e.value = v.toLowerCase(); e.dispatchEvent(new Event('input', { bubbles: true })); e.dispatchEvent(new Event('change', { bubbles: true })); }, [id, v]);
    await p.locator('button:visible', { hasText: new RegExp('^' + pat + '$') }).first().click(); await p.waitForTimeout(200);
    await setCol('pick1', c1); await setCol('pick2', c2);
    await p.locator('button:visible', { hasText: new RegExp('^' + handle + '$') }).first().click();
    if (ring) { await p.evaluate(() => { const r = document.getElementById('ring'); if (!r.checked) r.click(); }); await setCol('capcol', ring); }
    await p.fill('#name', name); await p.waitForTimeout(1200);
    const r = await p.evaluate(() => { const i = tex.image; const c = document.createElement('canvas'); c.width = i.width; c.height = i.height; c.getContext('2d').drawImage(i, 0, 0); return { url: c.toDataURL('image/png'), w: i.width, h: i.height, flipY: tex.flipY, rep: [tex.repeat.x, tex.repeat.y], off: [tex.offset.x, tex.offset.y], wrapS: tex.wrapS }; });
    fs.writeFileSync(process.argv[2] + '/' + f, Buffer.from(r.url.split(',')[1], 'base64')); console.log(f, r.w, r.h, r.flipY, r.rep, r.off, r.wrapS); await p.close(); }
  await b.close(); })();
