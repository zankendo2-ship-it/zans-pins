const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const T = path.join(__dirname, '../../../templates'); const b64 = f => fs.readFileSync(f).toString('base64');
const font = (n, w, f) => `@font-face{font-family:'${n}';font-weight:${w};src:url(data:font/woff2;base64,${b64(path.join(T, 'fonts', f))})}`;
const metal = 'linear-gradient(90deg,#8a6a22,#f2cf5b 18%,#fff3c8 32%,#c9a13b 50%,#fff3c8 68%,#f2cf5b 82%,#8a6a22)';
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 2700, height: 2025 } });
  await p.setContent(`<html><head><style>${font('Jost', 600, 'jost-600.woff2')}${font('Jost', 700, 'jost-700.woff2')}*{box-sizing:border-box;margin:0}body{width:2700px;height:2025px;position:relative;overflow:hidden;font-family:Jost;color:#fff;text-align:center}</style></head><body>
<img src="data:image/png;base64,${b64('/tmp/mf/crop.png')}" style="position:absolute;inset:0;width:2700px;height:2025px;filter:brightness(1.3) contrast(1.05)">
<div style="position:absolute;left:0;right:0;top:0;height:640px;background:linear-gradient(rgba(10,30,20,.88) 55%,transparent)"></div>
<div style="position:absolute;left:0;right:0;top:0;height:51px;background:${metal}"></div><div style="position:absolute;left:0;right:0;bottom:0;height:51px;background:${metal}"></div>
<div style="position:absolute;left:540px;width:1620px;top:110px">
<span style="display:inline-block;border:5px solid #F2CF5B;color:#F2CF5B;font-weight:600;letter-spacing:10px;font-size:52px;padding:10px 34px">PERSONALISED SILKS MUG</span>
<div style="font-weight:700;font-size:128px;line-height:1.02;margin-top:26px">YOUR NAME.<br><span style="color:#F2CF5B">YOUR COLOURS.</span></div></div>
</body></html>`); await p.waitForTimeout(300);
  await p.screenshot({ path: path.join(__dirname, 'SILKS-MUG-photo1-replacement-2700x2025-DRAFT.jpg'), type: 'jpeg', quality: 92 }); await b.close(); })();
