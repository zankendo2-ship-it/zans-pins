const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const T = path.join(__dirname, '../../../templates'); const b64 = f => fs.readFileSync(f).toString('base64');
const font = (n, w, f) => `@font-face{font-family:'${n}';font-weight:${w};src:url(data:font/woff2;base64,${b64(path.join(T, 'fonts', f))})}`;
(async () => { const b = await chromium.launch(); const dir = process.argv[2];
  for (const f of fs.readdirSync(dir).filter(x => x.endsWith('.jpg') && !x.startsWith('breeders'))) { const p = await b.newPage({ viewport: { width: 1000, height: 750 } });
    await p.setContent(`<html><head><style>${font('Jost', 700, 'jost-700.woff2')}*{margin:0}body{width:1000px;height:750px;position:relative;overflow:hidden;font-family:Jost}</style></head><body>
<img src="data:image/jpeg;base64,${b64(path.join(dir, f))}" style="position:absolute;inset:0;width:1000px;height:750px">
<div style="position:absolute;left:222px;top:545px;background:#F3EDE5;color:#1C1C1C;font-weight:700;font-size:30px;letter-spacing:3px;padding:8px 20px;border-radius:8px;border:3px solid #F2CF5B;box-shadow:0 4px 14px rgba(0,0,0,.35)">DIGITAL PDF</div>
<div style="position:absolute;left:222px;top:616px;color:#fff;font-weight:700;font-size:21px;letter-spacing:1px">NOTHING IS POSTED</div>
</body></html>`); await p.waitForTimeout(150);
    await p.screenshot({ path: path.join(__dirname, f.replace('.jpg', '-DIGITAL-PDF-label-1000x750-DRAFT.jpg')), type: 'jpeg', quality: 92 }); await p.close(); }
  await b.close(); })();
