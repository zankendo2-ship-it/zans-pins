const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const T = path.join(__dirname, '../../../templates'); const b64 = f => fs.readFileSync(f).toString('base64');
const font = (n, w, f) => `@font-face{font-family:'${n}';font-weight:${w};src:url(data:font/woff2;base64,${b64(path.join(T, 'fonts', f))})}`;
const metal = 'linear-gradient(90deg,#8a6a22,#f2cf5b 18%,#fff3c8 32%,#c9a13b 50%,#fff3c8 68%,#f2cf5b 82%,#8a6a22)';
const W = 1080, H = 1350;
const html = `<html><head><style>${font('Jost', 600, 'jost-600.woff2')}${font('Jost', 700, 'jost-700.woff2')}
*{box-sizing:border-box;margin:0}body{width:${W}px;height:${H}px;background:#1F5A3D;font-family:'Jost';color:#fff;position:relative;overflow:hidden}
.m{position:absolute;left:0;right:0;height:14px;background:${metal}}.t{top:0}.b{bottom:0}
.frame{position:absolute;inset:36px;border:2px solid #F2CF5B;border-radius:6px}
.in{position:absolute;inset:36px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 60px}
.eye{font-weight:600;letter-spacing:5px;font-size:26px;color:#F2CF5B;margin-bottom:26px}
.ph{width:700px;height:687px;border-radius:14px;border:8px solid #f7f3ea;box-shadow:0 14px 40px rgba(0,0,0,.45);overflow:hidden;margin-bottom:34px}.ph img{width:100%;display:block}
.stars{font-size:64px;letter-spacing:10px;color:#F2CF5B;line-height:1;margin-bottom:22px}
h1{font-weight:700;font-size:58px;line-height:1.12;margin-bottom:22px}
.by{font-weight:600;font-size:30px;color:#EAE2D8;letter-spacing:1px}</style></head><body><div class="m t"></div><div class="m b"></div><div class="frame"></div>
<div class="in"><div class="eye">A CUSTOMER REVIEW</div><div class="ph"><img src="data:image/png;base64,${b64(path.join(__dirname, 'review-photo-crop.png'))}"></div>
<div class="stars">★★★★★</div><h1>“Love this item for our Christmas tree”</h1><div class="by">Verified Etsy Buyer</div></div></body></html>`;
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: W, height: H } }); await p.setContent(html); await p.waitForTimeout(300);
  await p.screenshot({ path: path.join(__dirname, 'ETSY-REVIEW-slide1-1080x1350-DRAFT.png') }); await b.close(); })();
