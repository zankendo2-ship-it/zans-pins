const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const T = path.join(__dirname, '../../../templates'); const b64 = f => fs.readFileSync(f).toString('base64');
const font = (n, w, f) => `@font-face{font-family:'${n}';font-weight:${w};src:url(data:font/woff2;base64,${b64(path.join(T, 'fonts', f))})}`;
const P = f => `data:image/png;base64,${b64(f)}`;
const mum = P(path.join(T, 'scenes', 'mum-green-tree-bells.png'));
const scene = P(path.join(T, 'scenes', 'silks-bauble.png'));
const ex = P(path.join(__dirname, '../../2026-11-22/free-silks-design/example-bauble-your-horse.png'));
const css = `${font('Jost', 600, 'jost-600.woff2')}${font('Jost', 700, 'jost-700.woff2')}*{box-sizing:border-box;margin:0}body{width:1080px;height:1920px;position:relative;overflow:hidden;font-family:Jost;background:#1F5A3D;color:#fff;text-align:center}
.big{position:absolute;left:50px;right:50px;font-weight:700;line-height:1.02;text-shadow:0 4px 24px rgba(0,0,0,.45)}`;
const stars = s => `<div style="font-size:${s}px;letter-spacing:${s / 6}px;color:#F2CF5B;line-height:1">★★★★★</div>`;
const endbg = `data:image/png;base64,${b64('/tmp/endg/etsy-review-9x16-end.png')}`;
const F = {
 r: `<div style="position:absolute;inset:0;background:#0d1a12"></div><img src="${scene}" style="position:absolute;left:0;top:330px;width:1080px;height:1920px">
  <div style="position:absolute;left:0;right:0;top:0;height:860px;background:linear-gradient(rgb(13,26,18) 78%,transparent)"></div>
  <div style="position:absolute;left:0;right:0;top:350px">${stars(120)}</div>
  <div class="big" style="top:500px;font-size:92px">“Love this item for our Christmas tree”</div>
  <div style="position:absolute;left:0;right:0;top:730px;font-weight:600;font-size:40px;color:#E0D6C9">Verified Etsy Buyer</div>`,
 e: `<img src="${ex}" style="position:absolute;left:115px;top:520px;width:850px;border-radius:50%;border:8px solid #F2CF5B">
  <div class="big" style="top:340px;font-size:112px;color:#F2CF5B">ANY COLOURS</div>
  <div class="big" style="top:1420px;font-size:112px">ANY NAME</div><div style="position:absolute;left:0;right:0;top:1550px;font-weight:600;letter-spacing:8px;font-size:34px;color:#E0D6C9">DESIGN PREVIEW</div>`,
 g: `<div style="position:absolute;inset:0;background:url(${mum}) center/cover"></div>
  <div style="position:absolute;left:0;right:0;top:0;height:620px;background:linear-gradient(rgba(8,24,16,.85) 45%,transparent)"></div>
  <div style="position:absolute;left:0;right:0;bottom:0;height:560px;background:linear-gradient(transparent,rgba(8,24,16,.88) 60%)"></div>
  <div class="big" style="top:370px;font-size:70px;white-space:nowrap">PERSONALISED FOR THEM</div>
  <div class="big" style="top:1470px;font-size:64px;color:#F2CF5B">DESIGN YOURS · LINK IN BIO</div><div style="position:absolute;left:0;right:0;top:1400px;font-weight:600;letter-spacing:8px;font-size:34px;color:#E0D6C9;text-shadow:0 2px 10px #000">DESIGN EXAMPLE</div>`,
 end: `<div style="position:absolute;inset:0;background:url(${endbg}) center/cover"></div><div style="position:absolute;left:230px;width:620px;top:1215px;height:190px;background:rgb(42,98,71);box-shadow:0 0 50px 45px rgb(42,98,71)"></div><div style="position:absolute;left:0;right:0;top:1250px;font-weight:700;font-size:76px;letter-spacing:6px;color:#F2CF5B">LINK IN BIO</div>`,
};
(async () => { const b = await chromium.launch(); for (const [k, v] of Object.entries(F)) { const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.setContent(`<html><head><style>${css}</style></head><body>${v}</body></html>`); await p.waitForTimeout(250); await p.screenshot({ path: `/tmp/r5-${k}.png` }); await p.close(); } await b.close(); })();
