const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const T = path.join(__dirname, '../../../templates'); const b64 = f => fs.readFileSync(f).toString('base64');
const font = (n, w, f) => `@font-face{font-family:'${n}';font-weight:${w};src:url(data:font/woff2;base64,${b64(path.join(T, 'fonts', f))})}`;
const meta = JSON.parse(fs.readFileSync('/tmp/gt/meta.json'));
const METAL = { Pro: ['#8a6a22', '#f2cf5b', '#fff3c8', '#c9a13b'], Advanced: ['#6f7377', '#c9ccd0', '#ffffff', '#a3a7ac'], Beginner: ['#6b3f1d', '#c98a4b', '#f3cfa6', '#a8642e'] };
const grad = m => `linear-gradient(90deg,${m[0]},${m[1]} 18%,${m[2]} 32%,${m[3]} 50%,${m[2]} 68%,${m[1]} 82%,${m[0]})`;
(async () => { const b = await chromium.launch();
  for (const key of Object.keys(meta)) { const mm = key.match(/^(.*?) (JUMPS|FLAT|ALL-WEATHER) (Beginner|Advanced|Pro) - (\d+)$/); const [, course, type, ed, id] = mm; const m = meta[key];
    const p = await b.newPage({ viewport: { width: 2700, height: 2025 } });
    await p.setContent(`<html><head><style>${font('Jost', 600, 'jost-600.woff2')}${font('Jost', 700, 'jost-700.woff2')}*{box-sizing:border-box;margin:0}
body{width:2700px;height:2025px;position:relative;overflow:hidden;font-family:Jost;text-align:center;background:radial-gradient(ellipse at 50% 50%,${m.centre},${m.edge} 90%)}
.s{position:absolute;left:0;right:0;height:62px;background:${grad(METAL[ed])}}.h{position:absolute;left:0;right:0;font-weight:700;line-height:1;white-space:nowrap;text-shadow:0 6px 18px rgba(0,0,0,.35)}</style></head><body>
<div class="s" style="top:0"></div><div class="s" style="bottom:0"></div>
<div class="h" style="top:112px;font-size:128px;color:${m.col}">${course} ${type}</div>
<div class="h" style="top:258px;font-size:128px;color:#F2CF5B">RACECOURSE GUIDE</div>
<img src="data:image/png;base64,${b64(`/tmp/gt/${key}-cover.png`)}" style="position:absolute;left:1005px;top:452px;width:690px;height:840px;box-shadow:0 22px 60px rgba(0,0,0,.5)">
<img src="data:image/png;base64,${b64(`/tmp/gt/${key}-box.png`)}" style="position:absolute;left:910px;top:1362px;width:880px;height:230px;border-radius:26px">
<div style="position:absolute;left:0;right:0;top:1668px;font-weight:600;font-size:92px;letter-spacing:12px;color:#F3EDE5">DIGITAL PDF DOWNLOAD</div>
</body></html>`); await p.waitForTimeout(200);
    const w = await p.evaluate(() => [...document.querySelectorAll('.h')].map(e => { const r = document.createRange(); r.selectNodeContents(e); return Math.round(r.getBoundingClientRect().width); }));
    const out = `${course}-${type}-${ed}-${id}-heading-racecourse-guide-strip-62px-${ed.toLowerCase()}.jpg`.replace(/ /g, '-');
    await p.screenshot({ path: path.join(__dirname, out), type: 'jpeg', quality: 95 }); await p.close(); console.log(out, w.join('/')); }
  await b.close(); })();
