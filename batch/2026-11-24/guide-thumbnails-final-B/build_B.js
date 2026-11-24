const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const T = path.join(__dirname, '../../../templates'); const b64 = f => fs.readFileSync(f).toString('base64');
const font = (n, w, f) => `@font-face{font-family:'${n}';font-weight:${w};src:url(data:font/woff2;base64,${b64(path.join(T, 'fonts', f))})}`;
const meta = JSON.parse(fs.readFileSync('/tmp/gt/meta.json'));
const METAL = { Pro: ['#8a6a22', '#f2cf5b', '#fff3c8', '#c9a13b'], Advanced: ['#6f7377', '#c9ccd0', '#ffffff', '#a3a7ac'], Beginner: ['#6b3f1d', '#c98a4b', '#f3cfa6', '#a8642e'] };
const grad = m => `linear-gradient(90deg,${m[0]},${m[1]} 18%,${m[2]} 32%,${m[3]} 50%,${m[2]} 68%,${m[1]} 82%,${m[0]})`;
const LINE = { Beginner: 'COURSE MADE SIMPLE', Advanced: 'DEEPER COURSE INSIGHTS', Pro: 'DETAILED COURSE ANALYSIS' };
(async () => { const b = await chromium.launch();
  for (const key of (process.argv[2]==='all'?Object.keys(meta).sort():['AINTREE JUMPS Pro - 4623069940','CHELTENHAM JUMPS Beginner - 4622511316','SANDOWN JUMPS Advanced - 4622672428'])) { const [, course, type, ed, id] = key.match(/^(.*?) (JUMPS|FLAT|ALL-WEATHER) (Beginner|Advanced|Pro) - (\d+)$/); const m = meta[key]; const lines = [LINE[ed]];
    const cov = `data:image/png;base64,${b64(`/tmp/gt/${key}-cover.png`)}`;
    const p = await b.newPage({ viewport: { width: 2700, height: 2025 } });
    await p.setContent(`<html><head><style>${font('Jost', 600, 'jost-600.woff2')}${font('Jost', 700, 'jost-700.woff2')}*{box-sizing:border-box;margin:0}
body{width:2700px;height:2025px;position:relative;overflow:hidden;font-family:Jost;background:radial-gradient(ellipse at 50% 50%,${m.centre},${m.edge} 90%);color:#fff}
.s{position:absolute;left:0;right:0;height:62px;background:${grad(METAL[ed])};z-index:9}.h{position:absolute;left:0;right:0;text-align:center;font-weight:700;line-height:1;white-space:nowrap;text-shadow:0 6px 18px rgba(0,0,0,.35)}
.pg{position:absolute;width:947px;height:1150px;background:#EFE8DD;box-shadow:0 20px 50px rgba(0,0,0,.45)}</style></head><body>
<div class="s" style="top:0"></div><div class="s" style="bottom:0"></div>
<div class="h" style="top:84px;font-size:200px;color:${m.col}">${course}</div>
<div class="h" style="top:284px;font-size:112px;color:#F2CF5B">${type}</div>
<div class="h" style="top:398px;font-size:112px;color:#F2CF5B">RACECOURSE GUIDE</div>
<div class="h" style="top:540px;font-size:94px;color:#fff;letter-spacing:3px">${lines[0]}</div>
<div class="pg" style="left:912px;top:694px;transform:rotate(6.5deg)"></div><div class="pg" style="left:896px;top:688px;transform:rotate(5deg)"></div>
<img src="${cov}" style="position:absolute;left:876px;top:680px;width:947px;height:1150px;transform:rotate(3.2deg);box-shadow:0 24px 60px rgba(0,0,0,.5)">
<img src="data:image/png;base64,${b64(`/tmp/gt/${key}-box.png`)}" style="position:absolute;left:650px;top:1706px;width:480px;height:126px;border-radius:22px;box-shadow:0 10px 26px rgba(0,0,0,.45)">
<div style="position:absolute;left:1160px;top:1706px;width:890px;height:126px;line-height:126px;text-align:center;border-radius:26px;background:linear-gradient(90deg,#8a6a22,#f2cf5b 18%,#fff3c8 32%,#c9a13b 50%,#fff3c8 68%,#f2cf5b 82%,#8a6a22);box-shadow:0 10px 26px rgba(0,0,0,.45);font-weight:700;font-size:66px;letter-spacing:1px;color:#14301f">DIGITAL PDF DOWNLOAD</div>
</body></html>`); await p.waitForTimeout(250);
    const out = `${course}-${type}-${ed}-${id}-racecourse-guide-thumbnail-LAYOUT-B-DRAFT.jpg`.replace(/ /g, '-');
    await p.screenshot({ path: path.join(__dirname, out), type: 'jpeg', quality: 95 }); await p.close(); console.log(out); }
  await b.close(); })();
