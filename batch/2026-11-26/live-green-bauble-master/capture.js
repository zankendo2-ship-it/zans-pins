// Captures the ACTUAL live racing green bauble print master from the website designer (style B), unchanged.
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 430, height: 900 } });
  await p.goto('https://www.zanshorseracing.co.uk/bauble-designer/', { waitUntil: 'networkidle' }); await p.waitForTimeout(1500);
  await p.locator('button', { hasText: 'STARRY NIGHT' }).first().click(); await p.waitForTimeout(400);
  await p.fill('#name', 'Dad'); await p.waitForTimeout(800);
  const r = await p.evaluate(async () => ({ code: ZANSBauble.code(), state: JSON.parse(JSON.stringify(S)), svg: printSVG(design(), 'pf'), png: await ZANSBauble.printFile(4), fix: ZANSBauble.PRINT_FIX || null }));
  const d = __dirname; fs.writeFileSync(path.join(d, 'LIVE-racing-green-bauble-DAD-print-master-990.svg'), r.svg);
  fs.writeFileSync(path.join(d, 'LIVE-racing-green-bauble-DAD-print-file-3960.png'), Buffer.from(r.png.split(',')[1], 'base64'));
  fs.writeFileSync(path.join(d, 'capture-info.json'), JSON.stringify({ captured_utc: new Date().toISOString(), url: 'https://www.zanshorseracing.co.uk/bauble-designer/', code: r.code, state: r.state, print_fix_marker: r.fix }, null, 1));
  console.log(r.code, r.svg.length, 'ring circles:', (r.svg.match(/<circle[^>]*fill="none"[^>]*>/g) || []), 'image:', /<image/.test(r.svg), 'filter:', /<filter/.test(r.svg)); await b.close(); })();
