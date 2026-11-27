const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const T = path.join(__dirname, '../../../templates'); const b64 = f => fs.readFileSync(f).toString('base64');
const font = (n, w, f) => `@font-face{font-family:'${n}';font-weight:${w};src:url(data:font/woff2;base64,${b64(path.join(T, 'fonts', f))})}`;
const img = f => `data:image/${f.endsWith('png') ? 'png' : 'webp'};base64,${b64(path.join(__dirname, 'scenes', f))}`;
const css = `${font('Jost', 600, 'jost-600.woff2')}${font('Jost', 700, 'jost-700.woff2')}*{box-sizing:border-box;margin:0}body{width:1080px;height:1920px;position:relative;overflow:hidden;font-family:Jost;color:#fff;text-align:center;background:#111}
.bg{position:absolute;inset:0;background-size:cover;background-position:center}.sh{position:absolute;left:0;right:0}
.t{position:absolute;left:50px;right:50px;font-weight:700;line-height:.98;text-shadow:0 4px 30px rgba(0,0,0,.7)}.k{position:absolute;left:0;right:0;font-weight:600;letter-spacing:10px;font-size:44px;text-shadow:0 2px 14px rgba(0,0,0,.8)}`;
const top = `<div class="sh" style="top:0;height:900px;background:linear-gradient(rgba(0,0,0,.72) 45%,transparent)"></div>`;
const bot = `<div class="sh" style="bottom:0;height:900px;background:linear-gradient(transparent,rgba(0,0,0,.78) 55%)"></div>`;
const sets = JSON.parse(fs.readFileSync(path.join(__dirname, process.argv[2])));
(async () => { const b = await chromium.launch(); for (const [k, v] of Object.entries(sets.frames)) { const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  const body = v.bg ? `<div class="bg" style="background-image:url(${img(v.bg)});${v.dy !== undefined ? 'background-repeat:no-repeat;background-color:#cfd1d3;background-size:1080px 1920px;background-position:0 ' + v.dy + 'px' : ''}"></div>${v.pos === 'top' ? top : bot}${v.dy !== undefined ? `<div style="position:absolute;left:0;right:0;top:0;height:${v.dy + 200}px;background:linear-gradient(rgb(34,34,34) ${v.dy - 40}px,rgba(34,34,34,0))"></div>` : ''}` : `<div class="bg" style="background:${sets.colour}"></div>`;
  await p.setContent(`<html><head><style>${css}</style></head><body>${body}${v.html.replace(/ACC/g, sets.accent)}</body></html>`); await p.waitForTimeout(250); await p.screenshot({ path: path.join(__dirname, `${sets.key}-${k}.png`) }); await p.close(); } await b.close(); })();
