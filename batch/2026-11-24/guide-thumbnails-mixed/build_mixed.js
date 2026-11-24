const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const T = path.join(__dirname, '../../../templates'); const b64 = f => fs.readFileSync(f).toString('base64');
const font = (n, w, f) => `@font-face{font-family:'${n}';font-weight:${w};src:url(data:font/woff2;base64,${b64(path.join(T, 'fonts', f))})}`;
const meta = JSON.parse(fs.readFileSync('/tmp/gt/meta.json'));
const METAL = { Pro: ['#8a6a22', '#f2cf5b', '#fff3c8', '#c9a13b'], Advanced: ['#6f7377', '#c9ccd0', '#ffffff', '#a3a7ac'], Beginner: ['#6b3f1d', '#c98a4b', '#f3cfa6', '#a8642e'] };
const grad = m => `linear-gradient(90deg,${m[0]},${m[1]} 18%,${m[2]} 32%,${m[3]} 50%,${m[2]} 68%,${m[1]} 82%,${m[0]})`;
const SELL = {
  'SANDOWN JUMPS Advanced - 4622672428': [28, ['Every distance, every detail', 'Every main distance', 'Smart money and big prices', "Big-race winners' colours"]],
  'CHELTENHAM JUMPS Beginner - 4622511316': [18, ['Simple advice for every distance', 'The course map, explained', 'Jumps racing in pictures', 'Jockeys, trainers and colours']],
  'AINTREE JUMPS Pro - 4623069940': [135, ['Every finding tested twice', 'Price calibration and big prices', '2027 Aintree returner list', 'Findings register and case studies']] };
(async () => { const b = await chromium.launch();
  for (const key of Object.keys(SELL)) { const [, course, type, ed, id] = key.match(/^(.*?) (JUMPS|FLAT|ALL-WEATHER) (Beginner|Advanced|Pro) - (\d+)$/); const m = meta[key]; const [pages, lines] = SELL[key];
    const cov = `data:image/png;base64,${b64(`/tmp/gt/${key}-cover.png`)}`;
    const p = await b.newPage({ viewport: { width: 2700, height: 2025 } });
    await p.setContent(`<html><head><style>${font('Jost', 600, 'jost-600.woff2')}${font('Jost', 700, 'jost-700.woff2')}*{box-sizing:border-box;margin:0}
body{width:2700px;height:2025px;position:relative;overflow:hidden;font-family:Jost;background:radial-gradient(ellipse at 50% 50%,${m.centre},${m.edge} 90%);color:#fff}
.s{position:absolute;left:0;right:0;height:62px;background:${grad(METAL[ed])};z-index:9}.h{position:absolute;left:0;right:0;text-align:center;font-weight:700;line-height:1;white-space:nowrap;text-shadow:0 6px 18px rgba(0,0,0,.35)}
.pg{position:absolute;width:1040px;height:1262px;background:#EFE8DD;box-shadow:0 20px 50px rgba(0,0,0,.45)}</style></head><body>
<div class="s" style="top:0"></div><div class="s" style="bottom:0"></div>
<div class="h" style="top:78px;font-size:226px;color:${m.col}">${course}</div>
<div class="h" style="top:300px;font-size:134px;color:#F2CF5B">${type}</div>
<div class="h" style="top:438px;font-size:134px;color:#F2CF5B">RACECOURSE GUIDE</div>
<div class="pg" style="left:1150px;top:652px;transform:rotate(6.5deg)"></div><div class="pg" style="left:1132px;top:646px;transform:rotate(5deg)"></div>
<img src="${cov}" style="position:absolute;left:1108px;top:636px;width:1040px;height:1262px;transform:rotate(3.2deg);box-shadow:0 24px 60px rgba(0,0,0,.5)">
<img src="data:image/png;base64,${b64(`/tmp/gt/${key}-box.png`)}" style="position:absolute;left:560px;top:668px;width:530px;height:139px;border-radius:22px">
<div style="position:absolute;left:560px;top:860px;width:540px;font-weight:700;font-size:116px;line-height:1.04;text-shadow:0 5px 16px rgba(0,0,0,.4)">${lines[0]}</div>
<div style="position:absolute;left:556px;top:1636px;width:540px;padding:22px 0 24px;text-align:center;border-radius:26px;background:linear-gradient(90deg,#8a6a22,#f2cf5b 18%,#fff3c8 32%,#c9a13b 50%,#fff3c8 68%,#f2cf5b 82%,#8a6a22);box-shadow:0 10px 26px rgba(0,0,0,.45);font-weight:700;font-size:74px;letter-spacing:1px;line-height:1.06;color:#14301f">DIGITAL PDF<br>DOWNLOAD</div>
</body></html>`); await p.waitForTimeout(250);
    const out = `MIXED-${course}-${type}-${ed}-${id}-angled-cover-new-heading-v2.1.jpg`.replace(/ /g, '-');
    await p.screenshot({ path: path.join(__dirname, out), type: 'jpeg', quality: 95 }); await p.close(); console.log(out); }
  await b.close(); })();
