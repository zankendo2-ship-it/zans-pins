const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const T = path.join(__dirname, '../../../templates'); const b64 = f => fs.readFileSync(f).toString('base64');
const font = (n, w, f) => `@font-face{font-family:'${n}';font-weight:${w};src:url(data:font/woff2;base64,${b64(path.join(T, 'fonts', f))})}`;
const photo = `data:image/png;base64,${b64(path.join(__dirname, '../../2026-11-22/etsy-review-post/review-photo-crop.png'))}`;
const css = `${font('Jost', 600, 'jost-600.woff2')}${font('Jost', 700, 'jost-700.woff2')}*{box-sizing:border-box;margin:0}body{width:1080px;height:1920px;position:relative;overflow:hidden;font-family:Jost;background:#1F5A3D;color:#fff;text-align:center}`;
const stars = s => `<div style="font-size:${s}px;letter-spacing:${s / 6}px;color:#F2CF5B;line-height:1">★★★★★</div>`;
const F = {
 a0: `<img src="${photo}" style="position:absolute;left:40px;top:470px;width:1000px;border-radius:18px;border:8px solid #F3EDE5">`,
 a: `<img src="${photo}" style="position:absolute;left:40px;top:470px;width:1000px;border-radius:18px;border:8px solid #F3EDE5">
  <div style="position:absolute;left:0;right:0;top:330px">${stars(120)}</div>
  <div style="position:absolute;left:0;right:0;top:1490px;font-weight:700;font-size:74px;letter-spacing:4px">FIVE STARS ON ETSY</div>`,
 b: `<div style="position:absolute;left:0;right:0;top:350px;font-weight:600;font-size:40px;letter-spacing:8px;color:#F2CF5B">A CUSTOMER REVIEW</div>
  <img src="${photo}" style="position:absolute;left:210px;top:430px;width:660px;border-radius:14px;border:6px solid #F3EDE5">
  <div style="position:absolute;left:0;right:0;top:1110px">${stars(88)}</div>
  <div style="position:absolute;left:70px;right:70px;top:1230px;font-weight:700;font-size:82px;line-height:1.12">“Love this item for our Christmas tree”</div>
  <div style="position:absolute;left:0;right:0;top:1470px;font-weight:600;font-size:40px;color:#E0D6C9">Verified Etsy Buyer</div>`,
};
(async () => { const b = await chromium.launch(); for (const [k, v] of Object.entries(F)) { const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.setContent(`<html><head><style>${css}</style></head><body>${v}</body></html>`); await p.waitForTimeout(250); await p.screenshot({ path: `/tmp/rv-${k}.png` }); await p.close(); } await b.close(); })();
