// Code-drawn concept previews: silks tie pins and cufflinks. No supplier, no paid credits.
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const T = path.join(__dirname, '../../../templates'); const b64 = f => fs.readFileSync(f).toString('base64');
const font = (n, w, f) => `@font-face{font-family:'${n}';font-weight:${w};src:url(data:font/woff2;base64,${b64(path.join(T, 'fonts', f))})}`;
const METAL = 'linear-gradient(90deg,#8a6a22,#f2cf5b 18%,#fff3c8 32%,#c9a13b 50%,#fff3c8 68%,#f2cf5b 82%,#8a6a22)';
const PX = 22; // pixels per millimetre on the 2000x1500 image
const pat = {
  stripes: (a, b) => `<rect width="100" height="100" fill="${a}"/>` + [0, 2, 4].map(i => `<rect x="${10 + i * 16}" width="16" height="100" fill="${b}"/>`).join(''),
  hoops: (a, b) => `<rect width="100" height="100" fill="${a}"/>` + [0, 2, 4].map(i => `<rect y="${10 + i * 16}" width="100" height="16" fill="${b}"/>`).join(''),
  spots: (a, b) => `<rect width="100" height="100" fill="${a}"/>` + [[22, 24], [50, 24], [78, 24], [36, 50], [64, 50], [22, 76], [50, 76], [78, 76], [8, 50], [92, 50]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="8.5" fill="${b}"/>`).join(''),
  chevrons: (a, b) => `<rect width="100" height="100" fill="${a}"/>` + [8, 38, 68].map(y => `<path d="M0 ${y + 22} L50 ${y} L100 ${y + 22} L100 ${y + 36} L50 ${y + 14} L0 ${y + 36} Z" fill="${b}"/>`).join(''),
  diamonds: (a, b) => `<rect width="100" height="100" fill="${a}"/>` + [0, 1, 2, 3, 4].flatMap(r => [0, 1, 2, 3, 4].map(c => [c * 25 + (r % 2 ? 12.5 : 0), r * 25])).map(([x, y]) => `<path d="M${x} ${y - 11} L${x + 9} ${y} L${x} ${y + 11} L${x - 9} ${y} Z" fill="${b}"/>`).join(''),
  quartered: (a, b) => `<rect width="100" height="100" fill="${a}"/><rect width="50" height="50" fill="${b}"/><rect x="50" y="50" width="50" height="50" fill="${b}"/>`,
  blank: () => `<rect width="100" height="100" fill="#f4f4f2"/>` };
const D = [
  ['01', 'stripes', 'Emerald and white stripes', '#0E8F5B', '#FFFFFF', 'gold'],
  ['02', 'hoops', 'Red and white hoops', '#D5202B', '#FFFFFF', 'silver'],
  ['03', 'spots', 'Black with yellow spots', '#16161A', '#FFD21F', 'gold'],
  ['04', 'chevrons', 'Purple with white chevrons', '#5B2A86', '#FFFFFF', 'silver'],
  ['05', 'diamonds', 'Orange with sky-blue diamonds', '#FF8C1A', '#7FC8F0', 'gold'],
  ['06', 'quartered', 'Cream and chocolate quarters', '#F4E7C8', '#4A2A1A', 'gold'],
  ['00', 'blank', 'BLANK - shape and size only', '', '', 'gold']];
const RIM = { gold: ['#8a6a22', '#f2cf5b', '#fff3c8', '#c9a13b'], silver: ['#6f7377', '#c9ccd0', '#ffffff', '#a3a7ac'] };
let uid = 0;
function disc(mm, kind, a, b, metal, px = PX) { // round enamel face with a metal rim, drawn at true scale
  const d = mm * px, id = 'c' + (uid++), m = RIM[metal];
  return `<svg width="${d + 40}" height="${d + 40}" viewBox="-20 -20 ${d + 40} ${d + 40}" style="overflow:visible">
<defs><clipPath id="${id}"><circle cx="${d / 2}" cy="${d / 2}" r="${d / 2 - d * .07}"/></clipPath>
<linearGradient id="${id}m" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${m[2]}"/><stop offset=".35" stop-color="${m[1]}"/><stop offset=".7" stop-color="${m[0]}"/><stop offset="1" stop-color="${m[3]}"/></linearGradient>
<radialGradient id="${id}g" cx=".32" cy=".26" r=".75"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset=".35" stop-color="#fff" stop-opacity=".08"/><stop offset="1" stop-color="#000" stop-opacity=".22"/></radialGradient>
<filter id="${id}s" x="-40%" y="-40%" width="180%" height="180%"><feDropShadow dx="0" dy="${d * .05}" stdDeviation="${d * .045}" flood-opacity=".4"/></filter></defs>
<circle cx="${d / 2}" cy="${d / 2}" r="${d / 2}" fill="url(#${id}m)" filter="url(#${id}s)"/>
<g clip-path="url(#${id})"><g transform="scale(${d / 100})">${pat[kind](a, b)}</g><rect width="${d}" height="${d}" fill="url(#${id}g)"/></g>
<circle cx="${d / 2}" cy="${d / 2}" r="${d / 2 - d * .07}" fill="none" stroke="rgba(0,0,0,.28)" stroke-width="2"/></svg>`; }
function page([n, kind, name, a, b, metal]) { const m = RIM[metal];
  const mg = `linear-gradient(180deg,${m[0]},${m[1]} 30%,${m[2]} 50%,${m[1]} 70%,${m[0]})`, mh = `linear-gradient(90deg,${m[0]},${m[1]} 30%,${m[2]} 50%,${m[1]} 70%,${m[0]})`;
  const rule = mm => `<div style="width:${mm * PX}px;margin:6px auto 0;border-top:3px solid #1C1C1C;position:relative;height:14px"><i style="position:absolute;left:0;top:-9px;height:16px;border-left:3px solid #1C1C1C"></i><i style="position:absolute;right:0;top:-9px;height:16px;border-left:3px solid #1C1C1C"></i></div><div style="font:700 34px Jost;color:#1C1C1C">17 mm</div>`;
  const lab = t => `<div style="font:700 30px Jost;letter-spacing:5px;color:#5E574F">${t}</div>`;
  const card = (title, inner, w) => `<div style="width:${w}px;height:1010px;background:#F3EDE5;border:3px solid #C9BDAE;border-radius:26px;box-shadow:0 26px 60px rgba(0,0,0,.45);position:relative;text-align:center">
<div style="font:700 44px Jost;letter-spacing:8px;color:#1F5A3D;margin-top:36px">${title}</div><div style="height:4px;width:150px;margin:12px auto 0;background:${METAL}"></div>${inner}
<div style="position:absolute;left:0;right:0;bottom:28px;font:700 30px Jost;letter-spacing:7px;color:#1F5A3D">ZANS <span style="color:#8a6a22">·</span> RACING</div></div>`;
  const edge = (w) => `<div style="width:${w * PX}px;height:${17 * PX}px;background:${mh};border-radius:${PX}px;box-shadow:4px 6px 10px rgba(0,0,0,.25)"></div>`;
  // tie tack: face from the front, then a side view = face edge-on + thin sharp pin + separate butterfly clutch
  const pin = `<div style="margin-top:26px">${lab('FRONT')}<div style="margin-top:-6px">${disc(17, kind, a, b, metal)}</div><div style="margin-top:-18px">${rule(17)}</div></div>
<div style="margin-top:16px">${lab('SIDE: PIN + CLUTCH BACK')}<div style="display:flex;align-items:center;justify-content:center;margin-top:10px;height:${8.2 * PX}px">
<div style="transform:scale(.48);transform-origin:right center;margin-left:-${1.1 * PX}px">${edge(2.2)}</div>
<div style="width:${9 * PX}px;height:${0.9 * PX}px;background:${mg};clip-path:polygon(0 0,82% 0,100% 50%,82% 100%,0 100%)"></div>
<div style="width:${2.2 * PX}px"></div>
<svg width="${6 * PX}" height="${8 * PX}" viewBox="0 0 60 80"><defs><linearGradient id="k${n}" x1="0" x2="1"><stop offset="0" stop-color="${m[0]}"/><stop offset=".5" stop-color="${m[2]}"/><stop offset="1" stop-color="${m[0]}"/></linearGradient></defs>
<rect x="18" y="14" width="16" height="52" rx="5" fill="url(#k${n})" stroke="${m[0]}" stroke-width="1.5"/><path d="M34 22 Q58 6 54 30 Q52 38 34 36 Z" fill="url(#k${n})" stroke="${m[0]}" stroke-width="1.5"/><path d="M34 58 Q58 74 54 50 Q52 42 34 44 Z" fill="url(#k${n})" stroke="${m[0]}" stroke-width="1.5"/></svg></div></div>`;
  // cufflinks: one front-on, one side-on (face edge-on + post + swivel toggle)
  const link = `<div style="display:flex;justify-content:center;gap:36px;margin-top:26px">
<div>${lab('FRONT')}<div style="margin-top:-6px">${disc(17, kind, a, b, metal)}</div><div style="margin-top:-18px">${rule(17)}</div></div>
<div>${lab('SIDE')}<div style="display:flex;align-items:center;justify-content:center;height:${17 * PX + 40}px;margin-top:-6px">${edge(2.6)}
<div style="width:${9 * PX}px;height:${2.2 * PX}px;background:${mg}"></div>
<div style="width:${4.6 * PX}px;height:${15 * PX}px;border-radius:${2.3 * PX}px;background:${mh};box-shadow:4px 6px 10px rgba(0,0,0,.25)"></div></div>
<div style="font:700 30px Jost;color:#1C1C1C;margin-top:-12px">face · post · swivel bar</div></div></div>
<div style="margin-top:44px;font:700 40px Jost;letter-spacing:5px;color:#1F5A3D">SOLD AS A PAIR</div>
<div style="display:flex;justify-content:center;gap:40px;margin-top:6px">${[0, 1].map(() => `<div style="transform:scale(.42);margin:-${17 * PX * .29 + 12}px -${17 * PX * .29 + 12}px">${disc(17, kind, a, b, metal)}</div>`).join('')}</div>`;
  return `<html><head><style>${font('Jost', 600, 'jost-600.woff2')}${font('Jost', 700, 'jost-700.woff2')}*{box-sizing:border-box;margin:0}
body{width:2000px;height:1500px;position:relative;overflow:hidden;font-family:Jost;background:radial-gradient(ellipse at 50% 40%,#24684a,#143524)}
.s{position:absolute;left:0;right:0;height:38px;background:${METAL}}</style></head><body><div class="s" style="top:0"></div><div class="s" style="bottom:0"></div>
<div style="position:absolute;left:0;right:0;top:74px;text-align:center;font:700 92px Jost;letter-spacing:6px;color:#fff">SILKS TIE PIN &amp; CUFFLINKS</div>
<div style="position:absolute;left:0;right:0;top:196px;text-align:center;font:700 58px Jost;letter-spacing:4px;color:#F2CF5B">${n === '00' ? name : `DESIGN ${n} · ${name.toUpperCase()}`}</div>
<div style="position:absolute;left:150px;top:316px">${card('TIE PIN (TIE TACK)', pin, 700)}</div><div style="position:absolute;left:910px;top:316px">${card('CUFFLINKS', link, 940)}</div>
<div style="position:absolute;left:0;right:0;bottom:62px;text-align:center;font:600 34px Jost;letter-spacing:5px;color:#EAE2D8">CONCEPT PREVIEW · DRAWN AT TRUE 17 mm SCALE · NOT A PRODUCT PHOTO</div></body></html>`; }
// worn, at one shared scale: tie tack on a plain 8 cm tie, cufflink on a shirt cuff
function context([n, kind, name, a, b, metal]) { const S = 11; // px per mm
  return `<html><head><style>${font('Jost', 600, 'jost-600.woff2')}${font('Jost', 700, 'jost-700.woff2')}*{box-sizing:border-box;margin:0}
body{width:2000px;height:1500px;position:relative;overflow:hidden;font-family:Jost;background:radial-gradient(ellipse at 50% 40%,#24684a,#143524)}
.s{position:absolute;left:0;right:0;height:38px;background:${METAL}}.pane{position:absolute;top:316px;width:820px;height:1010px;border-radius:26px;overflow:hidden;box-shadow:0 26px 60px rgba(0,0,0,.45);border:3px solid #C9BDAE}
.cap{position:absolute;left:0;right:0;bottom:0;padding:18px 0 20px;background:rgba(243,237,229,.96);text-align:center;font:700 40px Jost;letter-spacing:3px;color:#1C1C1C}</style></head><body><div class="s" style="top:0"></div><div class="s" style="bottom:0"></div>
<div style="position:absolute;left:0;right:0;top:74px;text-align:center;font:700 92px Jost;letter-spacing:6px;color:#fff">HOW BIG IS IT WHEN WORN?</div>
<div style="position:absolute;left:0;right:0;top:196px;text-align:center;font:700 58px Jost;letter-spacing:4px;color:#F2CF5B">${n === '00' ? name : `DESIGN ${n} · ${name.toUpperCase()}`}</div>
<div class="pane" style="left:150px;background:linear-gradient(100deg,#fbfbf9,#e9e9e4)">
<div style="position:absolute;left:50%;top:0;width:6px;height:100%;margin-left:-3px;background:rgba(0,0,0,.06)"></div>
<svg style="position:absolute;left:0;top:0" width="820" height="1010"><defs><pattern id="w" width="18" height="18" patternTransform="rotate(45)" patternUnits="userSpaceOnUse"><rect width="18" height="18" fill="#2c2f36"/><rect width="18" height="5" fill="#363a43"/></pattern></defs>
<path d="M${410 - 30 * S / 2 - 40} -10 L${410 + 30 * S / 2 + 40} -10 L${410 + 80 * S / 2} 1010 L${410 - 80 * S / 2} 1010 Z" fill="url(#w)"/>
<path d="M${410 - 30 * S / 2 - 40} -10 L${410 - 80 * S / 2} 1010" stroke="rgba(0,0,0,.35)" stroke-width="6"/></svg>
<div style="position:absolute;left:50%;top:430px;transform:translateX(-50%)">${disc(17, kind, a, b, metal, S)}</div><div class="cap">17 mm tie pin on an 8 cm tie</div></div>
<div class="pane" style="left:1030px;background:linear-gradient(160deg,#3a3f4a,#22252c)">
<div style="position:absolute;left:-40px;top:300px;width:900px;height:${62 * S}px;transform:rotate(-7deg)">
<div style="position:absolute;left:0;top:${6 * S}px;width:330px;height:${50 * S}px;background:linear-gradient(180deg,#30343d,#1d2026)"></div>
<div style="position:absolute;left:300px;top:0;width:${68 * S / 1.6}px;height:${62 * S}px;background:linear-gradient(180deg,#ffffff,#e4e4df);border-radius:10px 26px 26px 10px;box-shadow:0 14px 30px rgba(0,0,0,.45)">
<div style="position:absolute;inset:16px;border:3px dashed rgba(0,0,0,.14);border-radius:6px 18px 18px 6px"></div>
<div style="position:absolute;right:${7 * S}px;top:50%;transform:translateY(-50%)">${disc(17, kind, a, b, metal, S)}</div></div>
<div style="position:absolute;left:${300 + 68 * S / 1.6 - 6}px;top:${14 * S}px;width:260px;height:${34 * S}px;background:linear-gradient(180deg,#e7c2a0,#cfa27c);border-radius:0 90px 90px 0"></div></div>
<div class="cap">17 mm cufflink on a shirt cuff</div></div>
<div style="position:absolute;left:0;right:0;bottom:62px;text-align:center;font:600 34px Jost;letter-spacing:5px;color:#EAE2D8">CONCEPT PREVIEW · TIE AND CUFF DRAWN TO THE SAME SCALE · NOT A PRODUCT PHOTO</div></body></html>`; }
(async () => { const b = await chromium.launch(); for (const d of D) { const slug = d[2].toLowerCase().replace(/ - .*/, '').replace(/[^a-z]+/g, '-').replace(/-$/, '');
  for (const [fn, tag] of [[page, 'CONCEPT'], [context, 'WORN-SCALE']]) { const p = await b.newPage({ viewport: { width: 2000, height: 1500 } }); await p.setContent(fn(d)); await p.waitForTimeout(250);
    const out = `ZANS-silks-tie-pin-cufflinks-${d[0]}-${slug}-${tag}-DRAFT-v2.jpg`; await p.screenshot({ path: path.join(__dirname, out), type: 'jpeg', quality: 93 }); await p.close(); console.log(out); } } await b.close(); })();
