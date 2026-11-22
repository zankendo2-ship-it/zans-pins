const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const T = path.join(__dirname, '../../../templates'); const b64 = f => fs.readFileSync(f).toString('base64');
const font = (n, w, f) => `@font-face{font-family:'${n}';font-weight:${w};src:url(data:font/woff2;base64,${b64(path.join(T, 'fonts', f))})}`;
const metal = 'linear-gradient(90deg,#8a6a22,#f2cf5b 18%,#fff3c8 32%,#c9a13b 50%,#fff3c8 68%,#f2cf5b 82%,#8a6a22)';
const EX = `data:image/png;base64,${b64(path.join(__dirname, 'example-bauble-your-horse.png'))}`, LOGO = `data:image/png;base64,${b64(path.join(T, 'assets', 'zans-logo.png'))}`;
const css = (W, H, s) => `${font('Jost', 600, 'jost-600.woff2')}${font('Jost', 700, 'jost-700.woff2')}
*{box-sizing:border-box;margin:0}body{width:${W}px;height:${H}px;background:#1F5A3D;font-family:'Jost';color:#fff;position:relative;overflow:hidden}
.m{position:absolute;left:0;right:0;height:${26 * s}px;background:${metal}}.t{top:0}.b{bottom:0}
.frame{position:absolute;inset:${70 * s}px;border:${3 * s}px solid #F2CF5B;border-radius:${10 * s}px}
.in{position:absolute;inset:${70 * s}px;display:flex;align-items:center;justify-content:center;text-align:center;padding:0 ${90 * s}px;gap:${90 * s}px}
.col{display:flex;flex-direction:column;align-items:center}
.logo{width:${300 * s}px;border-radius:${14 * s}px;margin-bottom:${36 * s}px}
.eye{font-weight:600;letter-spacing:${8 * s}px;font-size:${46 * s}px;color:#F2CF5B;margin-bottom:${26 * s}px;text-transform:uppercase}
h1{font-weight:700;line-height:1.02;text-transform:uppercase;margin-bottom:${36 * s}px}
.rule{width:${260 * s}px;height:${6 * s}px;background:${metal};margin-bottom:${36 * s}px}
p{font-weight:600;line-height:1.22}p b{color:#F2CF5B;font-weight:700}
.disc{border-radius:50%;overflow:hidden;box-shadow:0 ${18 * s}px ${50 * s}px rgba(0,0,0,.45);border:${10 * s}px solid #f7f3ea;flex:none}
.disc img{width:104%;margin:-2%;display:block}`;
const etsy = (W, H, s) => `<html><head><style>${css(W, H, s)}h1{font-size:${150 * s}px}p{font-size:${72 * s}px}</style></head><body><div class="m t"></div><div class="m b"></div><div class="frame"></div>
<div class="in"><div class="disc" style="width:${1000 * s}px;height:${1000 * s}px"><img src="${EX}"></div><div class="col" style="flex:1"><img class="logo" src="${LOGO}"><div class="eye">Personalised racing silks</div>
<h1>Can't find<br>your silks?</h1><div class="rule"></div><p>Contact me and I'll design them for you<br><b>free of charge</b></p></div></div></body></html>`;
const slide2 = (W, H, s) => `<html><head><style>${css(W, H, s)}.in{flex-direction:column;gap:${50 * s}px}h1{font-size:${120 * s}px;margin-bottom:0}p{font-size:${64 * s}px}</style></head><body><div class="m t"></div><div class="m b"></div><div class="frame"></div>
<div class="in"><div class="eye" style="margin:0">An example</div><div class="disc" style="width:${1250 * s}px;height:${1250 * s}px"><img src="${EX}"></div><h1>Your silks, drawn for you</h1><p>Your colours. <b>Your horse's name.</b></p></div></body></html>`;
(async () => { const b = await chromium.launch();
  for (const [n, W, H, s, f] of [['CANT-FIND-YOUR-SILKS-etsy-photo-with-example-2700x2025-DRAFT.png', 2700, 2025, 1, etsy], ['CANT-FIND-YOUR-SILKS-slide2-example-1080x1350-DRAFT.png', 1080, 1350, 0.5, slide2]]) {
    const p = await b.newPage({ viewport: { width: W, height: H } }); await p.setContent(f(W, H, s)); await p.waitForTimeout(300);
    await p.screenshot({ path: path.join(__dirname, n) }); await p.close(); console.log(n); }
  await b.close(); })();
