const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const T = path.join(__dirname, '../../../templates'); const b64 = f => fs.readFileSync(f).toString('base64');
const font = (n, w, f) => `@font-face{font-family:'${n}';font-weight:${w};src:url(data:font/woff2;base64,${b64(path.join(T, 'fonts', f))})}`;
const metal = 'linear-gradient(90deg,#8a6a22,#f2cf5b 18%,#fff3c8 32%,#c9a13b 50%,#fff3c8 68%,#f2cf5b 82%,#8a6a22)';
const html = (W, H, s) => `<html><head><style>${font('Jost', 600, 'jost-600.woff2')}${font('Jost', 700, 'jost-700.woff2')}${font('SS', 400, 'source-sans-3-400.woff2')}${font('SS', 600, 'source-sans-3-600.woff2')}
*{box-sizing:border-box;margin:0}body{width:${W}px;height:${H}px;background:#1F5A3D;font-family:'Jost';color:#fff;position:relative;overflow:hidden}
.m{position:absolute;left:0;right:0;height:${26 * s}px;background:${metal}}.t{top:0}.b{bottom:0}
.frame{position:absolute;inset:${70 * s}px;border:${3 * s}px solid #F2CF5B;border-radius:${10 * s}px}
.in{position:absolute;inset:${70 * s}px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 ${110 * s}px}
img{width:${440 * s}px;border-radius:${14 * s}px;margin-bottom:${46 * s}px}
.eye{font-weight:600;letter-spacing:${8 * s}px;font-size:${46 * s}px;color:#F2CF5B;margin-bottom:${26 * s}px}
h1{font-weight:700;font-size:${205 * s}px;line-height:1.02;text-transform:uppercase;margin-bottom:${40 * s}px}
.rule{width:${260 * s}px;height:${6 * s}px;background:${metal};margin-bottom:${40 * s}px}
p{font-family:'Jost';font-weight:600;font-size:${92 * s}px;line-height:1.22;max-width:${2100 * s}px}
p b{color:#F2CF5B;font-weight:700}</style></head><body><div class="m t"></div><div class="m b"></div><div class="frame"></div>
<div class="in"><img src="data:image/png;base64,${b64(path.join(T, 'assets', 'zans-logo.png'))}"><div class="eye">PERSONALISED RACING SILKS</div>
<h1>Can't find your silks?</h1><div class="rule"></div><p>Contact me and I'll design them for you<br><b>free of charge</b></p></div></body></html>`;
(async () => { const b = await chromium.launch();
  for (const [n, W, H, s] of [['CANT-FIND-YOUR-SILKS-etsy-photo-2700x2025-DRAFT.png', 2700, 2025, 1], ['CANT-FIND-YOUR-SILKS-square-2000x2000-DRAFT.png', 2000, 2000, 0.74], ['CANT-FIND-YOUR-SILKS-social-1080x1350-DRAFT.png', 1080, 1350, 0.5]]) {
    const p = await b.newPage({ viewport: { width: W, height: H } }); await p.setContent(html(W, H, s)); await p.waitForTimeout(300);
    await p.screenshot({ path: path.join(__dirname, n) }); await p.close(); console.log(n); }
  await b.close(); })();
