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
  diamonds: (a, b) => `<rect width="100" height="100" fill="${a}"/>` + [[25, 25], [75, 25], [50, 50], [25, 75], [75, 75], [0, 50], [100, 50], [50, 0], [50, 100]].map(([x, y]) => `<path d="M${x} ${y - 17} L${x + 17} ${y} L${x} ${y + 17} L${x - 17} ${y} Z" fill="${b}"/>`).join(''),
  quartered: (a, b) => `<rect width="100" height="100" fill="${a}"/><rect width="50" height="50" fill="${b}"/><rect x="50" y="50" width="50" height="50" fill="${b}"/>`,
  blank: () => `<rect width="100" height="100" fill="#f4f4f2"/>` };
const D = [
  ['01', 'stripes', 'Emerald and white stripes', '#0E8F5B', '#FFFFFF', 'gold'],
  ['02', 'hoops', 'Red and white hoops', '#D5202B', '#FFFFFF', 'silver'],
  ['03', 'spots', 'Black with yellow spots', '#16161A', '#FFD21F', 'gold'],
  ['04', 'chevrons', 'Purple with white chevrons', '#5B2A86', '#FFFFFF', 'silver'],
  ['05', 'diamonds', 'Orange and sky-blue diamonds', '#FF8C1A', '#7FC8F0', 'gold'],
  ['06', 'quartered', 'Cream and chocolate quarters', '#F4E7C8', '#4A2A1A', 'gold'],
  ['00', 'blank', 'BLANK - shape and size only', '', '', 'gold']];
const RIM = { gold: ['#8a6a22', '#f2cf5b', '#fff3c8', '#c9a13b'], silver: ['#6f7377', '#c9ccd0', '#ffffff', '#a3a7ac'] };
let uid = 0;
function disc(mm, kind, a, b, metal) { // round enamel face with a metal rim, drawn at true scale
  const d = mm * PX, id = 'c' + (uid++), m = RIM[metal];
  return `<svg width="${d + 40}" height="${d + 40}" viewBox="-20 -20 ${d + 40} ${d + 40}" style="overflow:visible">
<defs><clipPath id="${id}"><circle cx="${d / 2}" cy="${d / 2}" r="${d / 2 - d * .07}"/></clipPath>
<linearGradient id="${id}m" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${m[2]}"/><stop offset=".35" stop-color="${m[1]}"/><stop offset=".7" stop-color="${m[0]}"/><stop offset="1" stop-color="${m[3]}"/></linearGradient>
<radialGradient id="${id}g" cx=".32" cy=".26" r=".75"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset=".35" stop-color="#fff" stop-opacity=".08"/><stop offset="1" stop-color="#000" stop-opacity=".22"/></radialGradient>
<filter id="${id}s" x="-40%" y="-40%" width="180%" height="180%"><feDropShadow dx="0" dy="${d * .05}" stdDeviation="${d * .045}" flood-opacity=".4"/></filter></defs>
<circle cx="${d / 2}" cy="${d / 2}" r="${d / 2}" fill="url(#${id}m)" filter="url(#${id}s)"/>
<g clip-path="url(#${id})"><g transform="scale(${d / 100})">${pat[kind](a, b)}</g><rect width="${d}" height="${d}" fill="url(#${id}g)"/></g>
<circle cx="${d / 2}" cy="${d / 2}" r="${d / 2 - d * .07}" fill="none" stroke="rgba(0,0,0,.28)" stroke-width="2"/></svg>`; }
function page([n, kind, name, a, b, metal]) { const m = RIM[metal];
  const mgrad = `linear-gradient(90deg,${m[0]},${m[1]} 30%,${m[2]} 50%,${m[1]} 70%,${m[0]})`;
  const rule = mm => `<div style="width:${mm * PX}px;margin:14px auto 0;border-top:3px solid #1C1C1C;position:relative;height:16px"><i style="position:absolute;left:0;top:-9px;height:16px;border-left:3px solid #1C1C1C"></i><i style="position:absolute;right:0;top:-9px;height:16px;border-left:3px solid #1C1C1C"></i></div><div style="font:600 30px 'IBM Plex Mono',monospace;color:#1C1C1C;margin-top:2px">${mm} mm</div>`;
  const card = (title, inner, w) => `<div style="width:${w}px;height:1010px;background:#F3EDE5;border:3px solid #C9BDAE;border-radius:26px;box-shadow:0 26px 60px rgba(0,0,0,.45);position:relative;text-align:center">
<div style="font:700 44px Jost;letter-spacing:8px;color:#1F5A3D;margin-top:44px">${title}</div><div style="height:4px;width:150px;margin:14px auto 0;background:${METAL}"></div>${inner}
<div style="position:absolute;left:0;right:0;bottom:34px;font:700 30px Jost;letter-spacing:7px;color:#1F5A3D">ZANS <span style="color:#8a6a22">·</span> RACING</div></div>`;
  const pin = `<div style="position:relative;height:640px;margin-top:40px"><div style="position:absolute;left:50%;top:${17 * PX / 2 + 20}px;width:${1.2 * PX}px;height:${15 * PX}px;margin-left:${-0.6 * PX}px;background:${mgrad};border-radius:0 0 ${PX}px ${PX}px;box-shadow:6px 8px 12px rgba(0,0,0,.25)"></div>
<div style="position:absolute;left:50%;top:0;transform:translateX(-50%)">${disc(17, kind, a, b, metal)}</div>
<div style="position:absolute;left:50%;top:${21.5 * PX}px;transform:translateX(-50%);width:${7 * PX}px;height:${4.2 * PX}px;border-radius:${1.2 * PX}px;background:${mgrad};box-shadow:0 8px 14px rgba(0,0,0,.3)"></div>
<div style="position:absolute;left:0;right:0;top:${27 * PX}px">${rule(17)}</div></div>`;
  const link = `<div style="position:relative;height:640px;margin-top:40px"><div style="display:flex;justify-content:center;gap:${6 * PX}px;padding-top:10px">${[0, 1].map(() => `<div style="position:relative">${disc(17, kind, a, b, metal)}</div>`).join('')}</div>
<div style="display:flex;justify-content:center;gap:${6 * PX}px;margin-top:6px">${[0, 1].map(() => `<div style="width:${17 * PX + 40}px;text-align:center"><div style="width:${2 * PX}px;height:${3 * PX}px;margin:0 auto;background:${mgrad};box-shadow:5px 6px 10px rgba(0,0,0,.25)"></div><div style="width:${12 * PX}px;height:${3.6 * PX}px;margin:0 auto;border-radius:${1.8 * PX}px;background:${mgrad};box-shadow:0 8px 14px rgba(0,0,0,.3)"></div></div>`).join('')}</div>
<div style="margin-top:14px">${rule(17)}</div><div style="font:600 24px Jost;color:#5E574F;margin-top:2px">face shown front-on, swivel bar shown below</div></div>`;
  return `<html><head><style>${font('Jost', 600, 'jost-600.woff2')}${font('Jost', 700, 'jost-700.woff2')}*{box-sizing:border-box;margin:0}
body{width:2000px;height:1500px;position:relative;overflow:hidden;font-family:Jost;background:radial-gradient(ellipse at 50% 40%,#24684a,#143524)}
.s{position:absolute;left:0;right:0;height:38px;background:${METAL}}</style></head><body><div class="s" style="top:0"></div><div class="s" style="bottom:0"></div>
<div style="position:absolute;left:0;right:0;top:74px;text-align:center;font:700 92px Jost;letter-spacing:6px;color:#fff">SILKS TIE PIN &amp; CUFFLINKS</div>
<div style="position:absolute;left:0;right:0;top:196px;text-align:center;font:700 58px Jost;letter-spacing:4px;color:#F2CF5B">${n === '00' ? name : `DESIGN ${n} · ${name.toUpperCase()}`}</div>
<div style="position:absolute;left:150px;top:316px">${card('TIE PIN', pin, 700)}</div><div style="position:absolute;left:910px;top:316px">${card('CUFFLINKS', link, 940)}</div>
<div style="position:absolute;left:0;right:0;bottom:62px;text-align:center;font:600 34px Jost;letter-spacing:5px;color:#EAE2D8">CONCEPT PREVIEW · DRAWN AT TRUE 17 mm SCALE · NOT A PRODUCT PHOTO</div></body></html>`; }
(async () => { const b = await chromium.launch(); for (const d of D) { const p = await b.newPage({ viewport: { width: 2000, height: 1500 } }); await p.setContent(page(d)); await p.waitForTimeout(250);
  const out = `ZANS-silks-tie-pin-cufflinks-${d[0]}-${d[2].toLowerCase().replace(/ - .*/, '').replace(/[^a-z]+/g, '-').replace(/-$/, '')}-CONCEPT-DRAFT.jpg`;
  await p.screenshot({ path: path.join(__dirname, out), type: 'jpeg', quality: 93 }); await p.close(); console.log(out); } await b.close(); })();
