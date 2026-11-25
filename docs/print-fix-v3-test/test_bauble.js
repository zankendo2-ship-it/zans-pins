const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch(); const p = await b.newPage(); const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto('http://127.0.0.1:8765/bauble-designer-v2/', { waitUntil: 'load' }); await p.waitForTimeout(1500);
  const out = {};
  for (const [ref, name, pat, c1, c2, cap] of [['loussiemoo', 'Loussiemoo', 'disc', '#F3B5C9', '#6CC24A', '#F3B5C9'], ['zoo-olympios', 'Zoo Olympios', 'spot_diag', '#F5D130', '#1C1C1C', '#1C1C1C'], ['rexs-romance', 'Rexs Romance', 'plain', '#1C4FA0', '#FFFFFF', '#FFFFFF']]) {
    const r = await p.evaluate(async ([pat, c1, c2, cap, name]) => { Object.assign(S, { style: 'A', pat, body: pat, allover: pat, c1, c2, capCol: cap, name, sleeves: 'plain' });
      const m = ZANSBauble.printMaster(); const url = await ZANSBauble.printFile(1); const i = new Image(); i.src = url; await i.decode();
      return { m, w: i.width, h: i.height, url, code: ZANSBauble.code() }; }, [pat, c1, c2, cap, name]);
    fs.writeFileSync(`${process.argv[2]}/v2-${ref}.svg`, r.m); fs.writeFileSync(`${process.argv[2]}/v2-${ref}.png`, Buffer.from(r.url.split(',')[1], 'base64'));
    const m = r.m; out[ref] = { code: r.code, png: [r.w, r.h], svg_len: m.length, has_image: /<image/.test(m), has_style: /<style/.test(m), has_opacity: /opacity=/.test(m), has_filter: /<filter/.test(m), has_clip: /clip-path=/.test(m),
      min_stroke: Math.min(...[...m.matchAll(/stroke-width="([\d.]+)"/g)].map(x => +x[1])), fills: [...new Set([...m.matchAll(/(?:fill|stroke)="(#[0-9A-Fa-f]{6})"/g)].map(x => x[1].toUpperCase()))] }; }
  console.log(JSON.stringify(out, null, 1), 'errors:', errs); await b.close(); })();
