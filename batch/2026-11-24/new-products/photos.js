const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const T = path.join(__dirname, '../../../templates'); const b64 = f => fs.readFileSync(f).toString('base64');
const font = (n, w, f) => `@font-face{font-family:'${n}';font-weight:${w};src:url(data:font/woff2;base64,${b64(path.join(T, 'fonts', f))})}`;
const W = 2700, H = 2025, S = 51; const metal = 'linear-gradient(90deg,#8a6a22,#f2cf5b 18%,#fff3c8 32%,#c9a13b 50%,#fff3c8 68%,#f2cf5b 82%,#8a6a22)';
const img = (n, v) => `data:image/png;base64,${b64(path.join(__dirname, 'work', `${n}-${v}.png`))}`;
const css = `${font('Jost', 600, 'jost-600.woff2')}${font('Jost', 700, 'jost-700.woff2')}*{box-sizing:border-box;margin:0}body{width:${W}px;height:${H}px;position:relative;overflow:hidden;font-family:Jost;background:#1F5A3D;color:#fff}
.m{position:absolute;left:0;right:0;height:${S}px;background:${metal};z-index:5}.badge{display:inline-block;background:#F2CF5B;color:#1C1C1C;font-weight:700;letter-spacing:6px;padding:18px 34px;border-radius:10px}`;
const strips = `<div class="m" style="top:0"></div><div class="m" style="bottom:0"></div>`;
const side = (n, v, eyebrow, big, sub, note) => `${strips}<img src="${img(n, v)}" style="position:absolute;left:0;top:0;width:${H}px;height:${H}px">
 <div style="position:absolute;left:${H}px;right:0;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center;padding:0 60px;text-align:center">
 <div style="font-weight:600;letter-spacing:8px;font-size:44px;color:#F2CF5B">${eyebrow}</div>
 <div style="font-weight:700;font-size:112px;line-height:1.02;margin:36px 0">${big}</div>
 <div><span class="badge" style="font-size:54px">FULLY<br>CUSTOMISED</span></div>
 <div style="font-weight:600;font-size:54px;line-height:1.25;margin-top:44px">${sub}</div>
 <div style="font-weight:600;font-size:38px;color:#E0D6C9;margin-top:40px">${note}</div></div>`;
const three = (n, name) => `${strips}<div style="position:absolute;left:0;right:0;top:${S + 50}px;text-align:center"><span class="badge" style="font-size:64px">FULLY CUSTOMISED</span>
 <div style="font-weight:700;font-size:104px;margin-top:30px">${name} IN YOUR OWN SILKS</div></div>
 ${['a', 'b', 'c'].map((v, i) => `<img src="${img(n, 'silks-' + v)}" style="position:absolute;left:${60 + i * 880}px;top:520px;width:820px;height:820px;border-radius:14px;border:8px solid #F3EDE5">`).join('')}
 <div style="position:absolute;left:0;right:0;top:1400px;text-align:center"><div style="font-weight:600;font-size:66px">Three examples. Yours is made in <span style="color:#F2CF5B">your colours</span>.</div>
 <div style="display:flex;justify-content:center;gap:50px;margin-top:60px">${['1 · PICK YOUR PATTERN', '2 · PICK YOUR TWO COLOURS', '3 · WE MAKE IT FOR YOU'].map(t => `<div style="border:5px solid #F2CF5B;border-radius:14px;padding:44px 40px;width:800px;font-weight:700;font-size:54px;letter-spacing:3px">${t}</div>`).join('')}</div>
 <div style="font-weight:600;font-size:50px;color:#E0D6C9;margin-top:56px">Hoops, spots, diamonds and more</div></div>`;
const PR = [['baby-bodysuit', 'BABY BODYSUIT'], ['kids-tee', "KIDS' T-SHIRT"], ['adult-tee', 'T-SHIRT'], ['patch', 'PATCH']];
(async () => { const b = await chromium.launch();
  for (const [n, name] of PR) { const pages = {
    '01-full-silks': side(n, 'silks-a', 'HORSE RACING GIFT', `${name}<br>IN YOUR SILKS`, 'Your own silks colours,<br>all over', 'Example colours shown'),
    '02-three-examples': three(n, name),
    '03-zans-design': side(n, 'zans', 'HORSE RACING GIFT', `${name}<br>ZANS DESIGN`, 'Your silks and your name<br>on the round ZANS design', 'Example design shown') };
    for (const [k, body] of Object.entries(pages)) { const p = await b.newPage({ viewport: { width: W, height: H } });
      await p.setContent(`<html><head><style>${css}</style></head><body>${body}</body></html>`); await p.waitForTimeout(300);
      await p.screenshot({ path: path.join(__dirname, `ZANS-${n}-${k}-2700x2025-DRAFT.jpg`), type: 'jpeg', quality: 90 }); await p.close(); } console.log(n); }
  await b.close(); })();
