const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] }); const p = await b.newPage(); const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto('http://127.0.0.1:8765/mug-designer-v2/', { waitUntil: 'load' }); await p.waitForTimeout(2500); await p.evaluate(() => document.fonts.load('700 62px Jost'));
  const out = {};
  for (const [w, h] of [[2475, 1155], [2582, 1120]]) {
    const m = await p.evaluate(([w, h]) => { const d = ZANS.fromCode('ZANS-B-hoops-00843D-F5D130-plain-F5D130-00843D-contrast-C8102E-C8102E-HBK-R1'); d.name = 'FACT TO FILE'; return ZANS.printMaster(d, Object.assign({}, MUG, { width_px: w, height_px: h }), 'Jost', LOGO); }, [w, h]);
    fs.writeFileSync(`${process.argv[2]}/v2-mug-${w}.svg`, m);
    out[w] = { len: m.length, has_image: /<image/.test(m), has_style: /<style/.test(m), has_opacity: /opacity=/.test(m), rects: (m.match(/<rect[^>]*>/g) || []).slice(-5), groups: (m.match(/<g transform[^>]*>/g) || []), text: (m.match(/<text[^>]*>[^<]*/g) || []).map(t => t.slice(0, 200)) }; }
  console.log(JSON.stringify(out, null, 1), 'errors:', errs); await b.close(); })();
