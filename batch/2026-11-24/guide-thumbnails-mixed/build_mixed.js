const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const T = path.join(__dirname, '../../../templates'); const b64 = f => fs.readFileSync(f).toString('base64');
const font = (n, w, f) => `@font-face{font-family:'${n}';font-weight:${w};src:url(data:font/woff2;base64,${b64(path.join(T, 'fonts', f))})}`;
const meta = JSON.parse(fs.readFileSync('/tmp/gt/meta.json'));
const METAL = { Pro: ['#8a6a22', '#f2cf5b', '#fff3c8', '#c9a13b'], Advanced: ['#6f7377', '#c9ccd0', '#ffffff', '#a3a7ac'], Beginner: ['#6b3f1d', '#c98a4b', '#f3cfa6', '#a8642e'] };
const grad = m => `linear-gradient(90deg,${m[0]},${m[1]} 18%,${m[2]} 32%,${m[3]} 50%,${m[2]} 68%,${m[1]} 82%,${m[0]})`;
const SELL = {
  'SANDOWN JUMPS Advanced - 4622672428': [28, ['Value and over-bet points', 'Every main distance', 'Smart money and big prices', "Big-race winners' colours"]],
  'CHELTENHAM JUMPS Beginner - 4622511316': [18, ['Simple advice for every main distance', 'The course map, explained', 'Jumps racing in pictures', 'Jockeys, trainers and colours']],
  'AINTREE JUMPS Pro - 4623069940': [135, ['Every finding tested twice', 'Price calibration and big prices', '2027 Aintree returner list', 'Findings register and case studies']] };
(async () => { const b = await chromium.launch();
  for (const key of Object.keys(SELL)) { const [, course, type, ed, id] = key.match(/^(.*?) (JUMPS|FLAT|ALL-WEATHER) (Beginner|Advanced|Pro) - (\d+)$/); const m = meta[key]; const [pages, lines] = SELL[key];
    const cov = `data:image/png;base64,${b64(`/tmp/gt/${key}-cover.png`)}`;
    const p = await b.newPage({ viewport: { width: 2700, height: 2025 } });
    await p.setContent(`<html><head><style>${font('Jost', 600, 'jost-600.woff2')}${font('Jost', 700, 'jost-700.woff2')}*{box-sizing:border-box;margin:0}
body{width:2700px;height:2025px;position:relative;overflow:hidden;font-family:Jost;background:radial-gradient(ellipse at 50% 50%,${m.centre},${m.edge} 90%);color:#fff}
.s{position:absolute;left:0;right:0;height:62px;background:${grad(METAL[ed])};z-index:9}.h{position:absolute;left:0;right:0;text-align:center;font-weight:700;line-height:1;white-space:nowrap;text-shadow:0 6px 18px rgba(0,0,0,.35)}
.pg{position:absolute;width:820px;height:996px;background:#EFE8DD;box-shadow:0 20px 50px rgba(0,0,0,.45)}</style></head><body>
<div class="s" style="top:0"></div><div class="s" style="bottom:0"></div>
<div class="h" style="top:78px;font-size:226px;color:${m.col}">${course}</div>
<div class="h" style="top:300px;font-size:134px;color:#F2CF5B">${type}</div>
<div class="h" style="top:438px;font-size:134px;color:#F2CF5B">RACECOURSE GUIDE</div>
<div class="pg" style="left:1352px;top:742px;transform:rotate(6.5deg)"></div><div class="pg" style="left:1334px;top:734px;transform:rotate(5deg)"></div>
<img src="${cov}" style="position:absolute;left:1308px;top:724px;width:820px;height:996px;transform:rotate(3.2deg);box-shadow:0 24px 60px rgba(0,0,0,.5)">
<img src="data:image/png;base64,${b64(`/tmp/gt/${key}-box.png`)}" style="position:absolute;left:580px;top:700px;width:660px;height:172px;border-radius:22px">
<div style="position:absolute;left:580px;top:940px;width:690px;font-weight:600;font-size:50px;line-height:1.28">${lines.map(l => `<div style="display:flex;gap:18px;margin-bottom:14px"><span style="color:#F2CF5B">✓</span><span>${l}</span></div>`).join('')}</div>
<div style="position:absolute;left:580px;top:1560px;width:700px;white-space:nowrap;font-weight:700;font-size:37px;letter-spacing:3px;color:#F2CF5B">${pages} PAGES · COLOUR + PRINT</div>
<div style="position:absolute;left:580px;top:1650px;width:720px;font-weight:600;font-size:66px;letter-spacing:6px;line-height:1.12;color:#F3EDE5">DIGITAL PDF<br>DOWNLOAD</div>
</body></html>`); await p.waitForTimeout(250);
    const out = `MIXED-${course}-${type}-${ed}-${id}-angled-cover-new-heading.jpg`.replace(/ /g, '-');
    await p.screenshot({ path: path.join(__dirname, out), type: 'jpeg', quality: 95 }); await p.close(); console.log(out); }
  await b.close(); })();
