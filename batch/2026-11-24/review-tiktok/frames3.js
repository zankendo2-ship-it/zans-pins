const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const T = path.join(__dirname, '../../../templates'); const b64 = f => fs.readFileSync(f).toString('base64');
const font = (n, w, f) => `@font-face{font-family:'${n}';font-weight:${w};src:url(data:font/woff2;base64,${b64(path.join(T, 'fonts', f))})}`;
const P = f => `data:image/png;base64,${b64(f)}`;
const mum = P(path.join(T, 'scenes', 'mum-green-tree-bells.png'));
const gd = P(path.join(T, 'scenes', 'grandad-green-twilight-course.png'));
const scene = P(path.join(T, 'scenes', 'silks-bauble.png'));
const ex = P(path.join(__dirname, '../../2026-11-22/free-silks-design/example-bauble-your-horse.png'));
const css = `${font('Jost', 600, 'jost-600.woff2')}${font('Jost', 700, 'jost-700.woff2')}*{box-sizing:border-box;margin:0}body{width:1080px;height:1920px;position:relative;overflow:hidden;font-family:Jost;background:#1F5A3D;color:#fff;text-align:center}
.big{position:absolute;left:50px;right:50px;font-weight:700;line-height:1.02;text-shadow:0 4px 24px rgba(0,0,0,.45)}`;
const stars = s => `<div style="font-size:${s}px;letter-spacing:${s / 6}px;color:#F2CF5B;line-height:1">★★★★★</div>`;
const endbg = `data:image/png;base64,${b64('/tmp/endg/etsy-review-9x16-end.png')}`;
const C = 'position:absolute;left:195px;width:690px;';
const F = {
 r: `<div style="position:absolute;inset:0;background:#0d1a12"></div><img src="${mum}" style="position:absolute;left:0;top:330px;width:1080px;height:1920px">
  <div style="position:absolute;left:0;right:0;top:0;height:920px;background:linear-gradient(rgb(13,26,18) 80%,transparent)"></div>
  <div style="${C}top:335px">${stars(104)}</div>
  <div class="big" style="${C}top:465px;font-size:82px;left:195px;right:auto">“Love this item for our Christmas tree”</div>
  <div style="${C}top:770px;font-weight:600;font-size:40px;color:#E0D6C9">Etsy review ★★★★★</div>
  <div style="${C}top:850px;font-weight:600;letter-spacing:8px;font-size:32px;color:#E0D6C9;text-shadow:0 2px 10px #000">DESIGN EXAMPLE</div>`,
 e: `<img src="${ex}" style="position:absolute;left:220px;top:470px;width:640px;border-radius:50%;border:8px solid #F2CF5B">
  <div class="big" style="${C}top:335px;font-size:92px;color:#F2CF5B;left:195px;right:auto">ANY COLOURS</div>
  <div class="big" style="${C}top:1160px;font-size:92px;left:195px;right:auto">ANY NAME</div><div style="${C}top:1290px;font-weight:600;letter-spacing:8px;font-size:34px;color:#E0D6C9">DESIGN PREVIEW</div>`,
 g: `<div style="position:absolute;inset:0;background:#0b1626"></div><img src="${gd}" style="position:absolute;left:0;top:-130px;width:1080px;height:1920px">
  <div style="position:absolute;left:0;right:0;top:0;height:700px;background:linear-gradient(rgba(8,24,16,.88) 55%,transparent)"></div>
  <div style="position:absolute;left:0;right:0;bottom:0;height:900px;background:linear-gradient(transparent,rgba(8,24,16,.9) 35%)"></div>
  <div class="big" style="${C}top:330px;font-size:84px;left:195px;right:auto;line-height:1.06">PERSONALISED<br>FOR THEM</div>
  <div style="${C}top:1238px;font-weight:600;letter-spacing:8px;font-size:32px;color:#E0D6C9;text-shadow:0 2px 10px #000">DESIGN EXAMPLE</div>
  <div class="big" style="${C}top:1292px;font-size:64px;color:#F2CF5B;left:195px;right:auto;line-height:1.05">DESIGN YOURS<br>LINK IN BIO</div>`,
 end: `<div style="position:absolute;inset:0;background:url(${endbg}) center/cover"></div>
  <div style="position:absolute;left:0;right:0;top:26px;height:54px;background:rgb(28,28,28)"></div>
  <div style="position:absolute;left:40px;width:1000px;top:1010px;height:440px;background:rgb(42,98,71);box-shadow:0 0 40px 36px rgb(42,98,71)"></div>
  <div class="big" style="${C}top:1030px;font-size:70px;left:195px;right:auto;line-height:1.1;text-shadow:none">WISHING YOU A<br>MERRY CHRISTMAS</div>
  <div style="${C}top:1235px;font-weight:700;font-size:72px;letter-spacing:6px;color:#F2CF5B">LINK IN BIO</div>`,
};
(async () => { const b = await chromium.launch(); for (const [k, v] of Object.entries(F)) { const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.setContent(`<html><head><style>${css}</style></head><body>${v}</body></html>`); await p.waitForTimeout(250); await p.screenshot({ path: `/tmp/r72-${k}.png` }); await p.close(); } await b.close(); })();
