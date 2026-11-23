const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const T = path.join(__dirname, '../../../templates'); const b64 = f => fs.readFileSync(f).toString('base64');
const font = (n, w, f) => `@font-face{font-family:'${n}';font-weight:${w};src:url(data:font/woff2;base64,${b64(path.join(T, 'fonts', f))})}`;
const metal = 'linear-gradient(90deg,#8a6a22,#f2cf5b 18%,#fff3c8 32%,#c9a13b 50%,#fff3c8 68%,#f2cf5b 82%,#8a6a22)';
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1000, height: 1500 } });
  await p.setContent(`<html><head><style>${font('Jost', 600, 'jost-600.woff2')}${font('Jost', 700, 'jost-700.woff2')}*{box-sizing:border-box;margin:0}body{width:1000px;height:1500px;position:relative;overflow:hidden;font-family:Jost;background:#1F5A3D}</style></head><body>
<div style="position:absolute;left:0;right:0;top:0;height:1040px;background:url(data:image/png;base64,${b64(path.join(T, 'scenes', 'silks-bauble.png'))}) center 35%/cover"></div>
<div style="position:absolute;left:0;right:0;top:0;height:20px;background:${metal}"></div><div style="position:absolute;left:0;right:0;top:1040px;height:16px;background:${metal}"></div><div style="position:absolute;left:0;right:0;bottom:0;height:20px;background:${metal}"></div>
<div style="position:absolute;left:60px;right:60px;top:1075px;text-align:center;color:#fff">
<div style="font-weight:600;letter-spacing:8px;font-size:30px;color:#F2CF5B">HORSE RACING CHRISTMAS GIFT</div>
<div style="font-weight:700;font-size:66px;line-height:1.05;margin-top:14px">YOUR SILKS.<br>YOUR HORSE'S NAME.</div>
<div style="font-weight:600;font-size:32px;margin-top:16px;color:#F3EDE5">Personalised racing silks bauble · any colours, any name</div>
<div style="font-weight:600;font-size:30px;margin-top:18px;color:#F2CF5B">UK: recommend ordering by Mon 7 Dec</div></div></body></html>`);
  await p.waitForTimeout(300); await p.screenshot({ path: path.join(__dirname, 'SAMPLE-PIN-silks-bauble-1000x1500-DRAFT.png') }); await b.close(); })();
