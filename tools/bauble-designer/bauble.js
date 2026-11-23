/* ZANS silks bauble designer (page logic). Uses window.ZANS (silks engine). */
const Z = window.ZANS;
const $ = id => document.getElementById(id);
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const W = 990, R = 495, GOLD = '#C9A646', CREAM = '#F6F1E7', RGREEN = '#0F3B2C';
const JW = {"A":0.66,"B":0.558,"C":0.685,"D":0.68,"E":0.55,"F":0.5,"G":0.775,"H":0.715,"I":0.245,"J":0.24,"K":0.565,"L":0.45,"M":0.81,"N":0.775,"O":0.79,"P":0.548,"Q":0.79,"R":0.56,"S":0.548,"T":0.465,"U":0.626,"V":0.66,"W":0.99,"X":0.555,"Y":0.561,"Z":0.545,"0":0.6,"1":0.45,"2":0.569,"3":0.546,"4":0.583,"5":0.564,"6":0.576,"7":0.525,"8":0.546,"9":0.576," ":0.3,"'":0.285,".":0.3,"-":0.21,"&":0.675,"#":0.6};
const em = t => { let w = 0; for (const c of String(t).toUpperCase()) w += JW[c] || 0.8; return w; };
const f1 = n => Math.round(n * 10) / 10;
function shade(hex, f) { const n = parseInt(hex.slice(1), 16); const c = [n >> 16, (n >> 8) & 255, n & 255].map(v => Math.max(0, Math.min(255, Math.round(f < 1 ? v * f : v + (255 - v) * (f - 1))))); return '#' + c.map(v => v.toString(16).padStart(2, '0')).join(''); }
const lum = h => { const n = parseInt(h.slice(1), 16); return ((n >> 16) * 0.299 + ((n >> 8) & 255) * 0.587 + (n & 255) * 0.114) / 255; };
/* split a name into 1 or 2 lines and size it to fit width maxW, height maxH */
function fit(name, maxW, maxH, maxFs, ls) {
  const t = name.toUpperCase(), words = t.split(' ');
  const one = Math.min(maxFs, maxW / (em(t) + ls * t.length), maxH);
  let best = { lines: [t], fs: one };
  if (words.length > 1) for (let i = 1; i < words.length; i++) {
    const a = words.slice(0, i).join(' '), b = words.slice(i).join(' ');
    const fs = Math.min(maxFs, maxW / (Math.max(em(a) + ls * a.length, em(b) + ls * b.length)), maxH / 2.1);
    if (fs > best.fs * 1.12) best = { lines: [a, b], fs };
  }
  return best;
}
function jerseyAt(d, cx, cy, h, id) { const sc = h / 648; return `<g transform="translate(${f1(cx)},${f1(cy + 73.6 * sc)}) scale(${Math.round(sc * 1000) / 1000})">${Z.jersey(d, id)}</g>`; }
const scaleFor = p => (['quartered','halved','stripe','sash','large_diamond','triple_diamond','star','disc','cross','chevron','braces','seams','cross_belts'].includes(p) ? 0.55 : p === 'spot_diag' ? 0.4 : 1.15);

/* ---------- the two bauble designs (990 x 990 print, same on both sides) ---------- */
function capTop(cap) {           // Cap A (Alex 5 Nov): plain cap, seams, button, shine, darker peak, gold edges
  const lo = lum(cap) < 0.2, dark = lo ? shade(cap, 1.3) : shade(cap, 0.7), light = shade(cap, lo ? 1.6 : 1.25), by = 225;
  const crown = `<path d="M0,0 H${W} V${by - 40} Q${R},${by + 25} 0,${by - 40} Z" fill="${cap}"/>`;
  const seams = [-330, -150, 150, 330].map(dx => `<path d="M${R},28 Q${R + dx * 0.45},${f1(by * 0.35)} ${R + dx},${f1(by - 18 - Math.abs(dx) * 0.06)}" fill="none" stroke="${dark}" stroke-width="7" stroke-linecap="round"/>`).join('');
  const shine = `<path d="M${R - 300},${by - 70} Q${R - 230},70 ${R - 40},48" fill="none" stroke="${light}" stroke-width="16" stroke-linecap="round" opacity="0.7"/>`;
  const edge = `<path d="M0,${by - 40} Q${R},${by + 25} ${W},${by - 40}" fill="none" stroke="${GOLD}" stroke-width="8"/>`;
  const peak = `<path d="M${R - 270},${by - 6} Q${R},${by + 34} ${R + 270},${by - 6} Q${R + 250},${by + 70} ${R},${by + 78} Q${R - 250},${by + 70} ${R - 270},${by - 6} Z" fill="${dark}" stroke="${GOLD}" stroke-width="6"/>`;
  return crown + seams + shine + `<circle cx="${R}" cy="30" r="24" fill="${dark}"/>` + edge + peak;
}
function logoTab(cy, w) { return `<rect x="${R - w / 2 - 8}" y="${f1(cy - w * 0.0667 - 6)}" width="${w + 16}" height="${f1(w * 0.1333 + 12)}" rx="7" opacity="0.92" fill="${CREAM}"/><image href="${LOGO_WIDE}" x="${R - w / 2}" y="${f1(cy - w * 0.0667)}" width="${w}" height="${f1(w * 0.1333)}"/>`; }
function designA(d, id) {
  const pat = Z.fillPattern(d.allover, d.c1, d.c2, 0, 0, W, W, scaleFor(d.allover));
  const n = fit(d.name, 640, 210, 120, 0.03), ink = Z.darkOf(d);
  const h = n.lines.length * n.fs * 1.05 + 120, y = 545 - h / 2;
  let t = `<rect x="${R - 380}" y="${f1(y)}" width="760" height="${f1(h)}" rx="${f1(Math.min(90, h / 2))}" fill="${CREAM}" stroke="${GOLD}" stroke-width="12"/>`;
  n.lines.forEach((l, i) => { t += `<text x="${R}" y="${f1(y + 35 + n.fs * 0.86 + i * n.fs * 1.05)}" text-anchor="middle" font-family="Jost" font-weight="700" font-size="${f1(n.fs)}" letter-spacing="${f1(n.fs * 0.03)}" fill="${ink}">${esc(l)}</text>`; });
  t += `<text x="${R}" y="${f1(y + h - 34)}" text-anchor="middle" font-family="Jost" font-weight="600" font-size="32" letter-spacing="9.6" fill="${ink}">MERRY CHRISTMAS</text>`;
  return svgWrap(id, pat + capTop(d.capCol) + `<circle cx="${R}" cy="${R}" r="${R - 26}" fill="none" stroke="${GOLD}" stroke-width="14"/>` + t + logoTab(885, 165));
}
function designB(d, id) {
  const jd = Object.assign({}, d, { cap: 'contrast', k1: d.capCol, k2: d.capCol });
  const n = fit(d.name, 600, 150, 96, 0.04);
  let t = ''; const one = n.lines.length === 1, top = one ? 715 : 680;
  n.lines.forEach((l, i) => { t += `<text x="${R}" y="${f1(top + i * n.fs * 1.02)}" text-anchor="middle" font-family="Jost" font-weight="700" font-size="${f1(n.fs)}" letter-spacing="${f1(n.fs * 0.04)}" fill="${GOLD}">${esc(l)}</text>`; });
  const mc = `<text x="${R}" y="${one ? 795 : 830}" text-anchor="middle" font-family="Jost" font-weight="600" font-size="30" letter-spacing="9.6" fill="${GOLD}">MERRY CHRISTMAS</text>`;
  return svgWrap(id, `<defs><filter id="${id}ol" x="-15%" y="-15%" width="130%" height="130%"><feMorphology in="SourceAlpha" operator="dilate" radius="9" result="d"/><feFlood flood-color="${GOLD}"/><feComposite in2="d" operator="in" result="o"/><feMerge><feMergeNode in="o"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><rect width="${W}" height="${W}" fill="${RGREEN}"/><circle cx="${R}" cy="${R}" r="${R - 26}" fill="none" stroke="${GOLD}" stroke-width="8"/><circle cx="${R}" cy="${R}" r="${R - 44}" fill="none" stroke="${GOLD}" stroke-width="2"/>` + `<g filter="url(#${id}ol)">` + jerseyAt(jd, R, one ? 395 : 365, one ? 380 : 340, id + 'j') + '</g>' + t + mc + logoTab(one ? 885 : 905, 150));
}
function svgWrap(id, inner) { return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 ${W} ${W}" width="${W}" height="${W}"><defs><clipPath id="${id}c"><circle cx="${R}" cy="${R}" r="${R}"/></clipPath></defs><g clip-path="url(#${id}c)">${inner}</g></svg>`; }
function printSVG(d, id) { return S.style === 'A' ? designA(d, id) : designB(d, id); }

/* ---------- state ---------- */
// Christmas starting designs (Alex 5 Nov): Snow Dancer on the silks bauble, Starry Night on the racing green bauble.
// Names checked: no famous racehorse of either name. Colours: Christmas red, white, gold, racing green (never green + pink).
const DEF = {
  A: { pat: 'stars', body: 'stars', c1: '#C8102E', c2: '#FFFFFF', sleeves: 'plain', capCol: '#0E6B3B', name: 'Snow Dancer' },
  B: { pat: 'stars', body: 'stars', c1: '#1B2A5C', c2: '#F5D130', sleeves: 'plain', capCol: '#F5D130', name: 'Starry Night' } };
const untouched = () => Object.keys(DEF[S.style]).every(k => S[k] === DEF[S.style][k]);
const S = Object.assign({ style: 'A', view: 'flat', scene: 'soft' }, DEF.A);
function design() {
  const n = Z.checkName(S.name);
  const d = Z.normalise({ layout: 'B', body: S.style === 'A' ? S.pat : S.body, allover: S.pat, c1: S.c1, c2: S.c2, sleeves: S.sleeves, cap: 'contrast', k1: S.capCol, k2: S.capCol });
  if (S.style === 'B') d.body = S.body;
  d.capCol = S.capCol; d.name = n.ok ? n.text : 'YOUR NAME'; // a refused name is never drawn
  return d;
}
function code(d) { // ZANS bauble code: ZB<style>-<pattern>-<c1>-<c2>-<sleeves>-<cap colour>
  const hx = h => h.replace('#', '').toUpperCase();
  return ['ZB' + S.style, S.style === 'A' ? S.pat : S.body, hx(d.c1), hx(d.c2), S.style === 'A' ? 'plain' : S.sleeves, hx(S.capCol)].join('-');
}

/* ---------- controls ---------- */
function optBtn(html, pressed, onClick, label) { const b = document.createElement('button'); b.type = 'button'; b.className = 'opt p-2 text-left'; b.setAttribute('aria-pressed', pressed); b.innerHTML = html; if (label) b.setAttribute('aria-label', label); b.onclick = onClick; return b; }
function chip(text, pressed, onClick) { const b = optBtn(`<span class="text-sm font-semibold px-1">${esc(text)}</span>`, pressed, onClick); b.classList.add('py-1.5'); return b; }
function swatches(el, key) { el.innerHTML = ''; Object.entries(Z.COLOURS).forEach(([n, h]) => { const b = document.createElement('button'); b.type = 'button'; b.className = 'sw'; b.style.background = h; b.title = n; b.setAttribute('aria-label', n); b.setAttribute('aria-pressed', S[key].toUpperCase() === h.toUpperCase()); b.onclick = () => { S[key] = h; render(); }; el.appendChild(b); }); }
function miniA(p) { return `<svg viewBox="0 0 110 110" xmlns="http://www.w3.org/2000/svg"><clipPath id="ma${p}"><circle cx="55" cy="55" r="53"/></clipPath><g clip-path="url(#ma${p})">${Z.fillPattern(p, S.c1, S.c2, 0, 0, 110, 110, scaleFor(p) * 0.35)}<rect width="110" height="22" fill="${S.capCol}"/></g><circle cx="55" cy="55" r="53" fill="none" stroke="${GOLD}" stroke-width="3"/></svg>`; }
function miniB(p) { const d = Z.normalise({ layout: 'C', body: p, c1: S.c1, c2: S.c2, sleeves: S.sleeves, cap: 'contrast', k1: S.capCol, k2: S.capCol }); return `<svg viewBox="-290 -420 580 690" xmlns="http://www.w3.org/2000/svg">${Z.jersey(d, 'mb' + p)}</svg>`; }
// Popular colour schemes (Alex 6 Nov: the same as the mug designer, plus the two bauble photo designs first).
// Mug ring colour = bauble cap colour; no ring = cap in the second colour. Colours only, never names.
// Left out: the mug's "Pink, green spots" (no green + pink on ZANS presets - Juddmonte rule).
const PRESETS = [
  ['Red, white stars, green cap (Snow Dancer)','stars','#C8102E','#FFFFFF','#0E6B3B'],
  ['Navy, gold stars, gold cap (Starry Night)','stars','#1B2A5C','#F5D130','#F5D130'],
  ['Green and yellow hoops, white cap','hoops','#00843D','#F5D130','#FFFFFF'],
  ['White and dark blue diamonds, red cap','diamonds','#FFFFFF','#0B3A5E','#C8102E'],
  ['Yellow, white cap','plain','#F5D130','#1C1C1C','#FFFFFF'],
  ['All white, black cap','plain','#FFFFFF','#1C1C1C','#1C1C1C'],
  ['Yellow, three big black spots, black cap','spot_diag','#F5D130','#1C1C1C','#1C1C1C'],
  ['Yellow, black spots, black cap','spots','#F5D130','#1C1C1C','#1C1C1C'],
  ['Royal blue, white cap','plain','#1C4FA0','#FFFFFF','#FFFFFF'],
  ['Green, blue sash, blue cap','sash','#00843D','#1C4FA0','#1C4FA0'],
  ['Royal blue, orange discs, orange cap','disc','#1C4FA0','#E36414','#E36414'],
  ['Purple, white seams, white cap','seams','#5B2C83','#FFFFFF','#FFFFFF'],
  ['Mid blue, red cap','plain','#4A7FC1','#FFFFFF','#C8102E'],
  ['Green, red cap','plain','#00843D','#FFFFFF','#C8102E'],
  ['Red, white sashes, blue cap','sash','#C8102E','#FFFFFF','#1C4FA0'],
  ['Purple, white diamonds, white cap','large_diamond','#5B2A86','#FFFFFF','#FFFFFF'],
  ['Blue, white seams, white cap','seams','#1C4FA0','#FFFFFF','#FFFFFF'],
  ['Yellow, dark blue cross belts, dark blue cap','cross_belts','#F5D130','#1B2A5C','#1B2A5C'],
  ['Dark blue and yellow hoops, yellow cap','hoops','#1B2A5C','#F5D130','#F5D130'],
  ['Red, black stars, black cap','stars','#C8102E','#1C1C1C','#1C1C1C'],
  ['All grey, white cap','plain','#9AA0A6','#FFFFFF','#FFFFFF'],
  ['Green and yellow hoops, red cap','hoops','#0E6B3B','#F5D130','#C8102E'],
  ['Purple, yellow chevrons, black cap','chevrons','#5B2C83','#F5D130','#1C1C1C'],
  ['Dark blue, orange diagonals, orange cap','diagonal','#1B2A5C','#E36414','#E36414'],
  ['Royal blue and white check, red cap','checks','#1C4FA0','#FFFFFF','#C8102E'],
  ['Maroon, light blue hoops, light blue cap','hoops','#8B1E3F','#7FB7E3','#7FB7E3'],
  ['Emerald, white diamonds, white cap','diamonds','#0E6B3B','#FFFFFF','#FFFFFF']];
function renderControls() {
  const SB = $('styles'); SB.innerHTML = '';
  [['A', 'Silks bauble', 'Your silks all over, a jockey cap across the top, your name on a cream plate'], ['B', 'Racing green bauble', 'Racing green and gold, your jersey and cap, your name in gold, Merry Christmas']].forEach(([k, t, s]) => {
    const d = design(), u = untouched() ? DEF[k] : null; const svg = (k === 'A' ? designA : designB)(Object.assign({}, d, u ? { allover: u.pat, body: u.body, c1: u.c1, c2: u.c2, sleeves: u.sleeves, capCol: u.capCol, k1: u.capCol, k2: u.capCol, name: u.name.toUpperCase() } : { allover: S.pat, body: k === 'A' ? S.pat : S.body }), 'st' + k);
    SB.appendChild(optBtn(`<div class="mx-auto" style="max-width:120px">${svg}</div><div class="disp font-semibold mt-2">${t}</div><div class="hint text-sm">${s}</div>`, S.style === k, () => { if (S.style !== k) { if (untouched()) Object.assign(S, DEF[k]); else if (S.name === DEF[S.style].name) S.name = DEF[k].name; } S.style = k; render(); }));
  });
  const PR = $('presets'); PR.innerHTML = '';
  PRESETS.forEach(([lab, p, a, b, cap], i) => {
    const on = S.pat === p && S.c1.toUpperCase() === a && S.c2.toUpperCase() === b && S.capCol.toUpperCase() === cap;
    PR.appendChild(optBtn(`<div class="mini"><svg viewBox="0 0 110 110" xmlns="http://www.w3.org/2000/svg"><clipPath id="pr${i}"><circle cx="55" cy="55" r="53"/></clipPath><g clip-path="url(#pr${i})">${Z.fillPattern(p, a, b, 0, 0, 110, 110, scaleFor(p) * 0.35)}<rect width="110" height="22" fill="${cap}"/></g><circle cx="55" cy="55" r="53" fill="none" stroke="${GOLD}" stroke-width="3"/></svg></div><div class="text-xs font-semibold mt-1 text-center">${lab}</div>`, on, () => { Object.assign(S, { pat: p, body: p, c1: a, c2: b, capCol: cap }); render(); }, lab));
  });
  const P = $('patterns'); P.innerHTML = '';
  Z.ALLOVER /* Alex 6 Nov: same 25 patterns as the mug designer, both baubles */.forEach(p => P.appendChild(optBtn(`<div class="mini">${S.style === 'A' ? miniA(p) : miniB(p)}</div><div class="text-xs font-semibold mt-1 text-center">${Z.NAMES[p] || p}</div>`, (S.style === 'A' ? S.pat : S.body) === p, () => { S.pat = p; S.body = p; render(); }, Z.NAMES[p])));
  swatches($('c1'), 'c1'); swatches($('c2'), 'c2'); swatches($('capsw'), 'capCol');
  $('pick1').value = S.c1; $('pick2').value = S.c2; $('capcol').value = S.capCol;
  $('sleevestep').hidden = S.style !== 'B';
  const SL = $('sleeves'); SL.innerHTML = ''; Z.SLEEVES.forEach(p => SL.appendChild(chip(p === 'plain' ? 'Same as jersey' : Z.NAMES[p], S.sleeves === p, () => { S.sleeves = p; render(); })));
  if (document.activeElement !== $('name') && $('name').value !== S.name) $('name').value = S.name;
  $('count').textContent = `${(S.name || '').length}/28`;
}

/* ---------- Christmas tree scene ---------- */
const SCENES = { soft: { cx: 446, cy: 628, r: 263, label: 'Soft light' }, moody: { cx: 452, cy: 648, r: 298, label: 'Evening' } };
function treeScene(baubleSvg, scene) {   // Alex 5 Nov: must look like a real photo; round disc, no tab (matches Harrier's bauble)
  // Photos: AI-made for ZANS (FLUX.1 Krea) of a BLANK white round ceramic bauble on a tree, /img/bauble-tree-<scene>.jpg 880x1088.
  // The design is laid on the blank face with "multiply" so the photo's own light and shadow show through it.
  // The mask PNG keeps the ribbon and the hole on top of the design.
  const sc = SCENES[scene] || SCENES.soft, { cx, cy, r } = sc;
  const inner = baubleSvg.replace(/^<svg[^>]*>/, '').replace(/<\/svg>$/, '').replace(/id="([^"]+)"/g, 'id="tr$1"').replace(/url\(#([^)]+)\)/g, 'url(#tr$1)');
  return `<svg viewBox="0 0 880 1088" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" role="img" aria-label="Your bauble hanging on a Christmas tree">
  <defs><mask id="face" maskUnits="userSpaceOnUse" x="0" y="0" width="880" height="1088"><image href="/img/bauble-tree-${scene}-mask.png" x="0" y="0" width="880" height="1088"/></mask></defs>
  <image href="/img/bauble-tree-${scene}.jpg" x="0" y="0" width="880" height="1088"/>
  <g mask="url(#face)" style="mix-blend-mode:multiply"><g transform="translate(${cx - r},${cy - r}) scale(${Math.round(2 * r / 990 * 10000) / 10000})">${inner}</g></g>
  </svg>`;
}

/* Real Harrier bauble (Printify pictures 5 Nov): round disc, hole INSIDE the circle near the top, red ribbon, no tab. Preview only, never printed. */
const HANGER = '<svg class="hang" viewBox="0 -18 100 118" aria-hidden="true"><path d="M46.5 -18 L49.3 6.2 M53.5 -18 L50.7 6.2" stroke="#B3121F" stroke-width="1.5" stroke-linecap="round" fill="none"/><circle cx="50" cy="7" r="2.6" fill="#EFE8DE" stroke="rgba(0,0,0,.35)" stroke-width=".4"/><path d="M48.6 5.4 Q50 9.6 51.4 5.4" stroke="#B3121F" stroke-width="1.5" fill="none" stroke-linecap="round"/></svg>';

/* ---------- render ---------- */
function render() {
  renderControls();
  const cc = code(design()); if (S._copied !== cc) $('copied').textContent = '';
  const d = design(), svg = printSVG(d, 'pv');
  $('flat').innerHTML = svg + HANGER;
  $('ribbonname').textContent = S.style === 'A' ? 'Silks bauble' : 'Racing green bauble';
  $('etsyorder').href = S.style === 'A' ? 'https://www.etsy.com/listing/4611232428' : 'https://www.etsy.com/listing/4611213915';
  $('tree').innerHTML = treeScene(printSVG(d, 'tv'), S.scene);
  $('scsoft').setAttribute('aria-pressed', S.scene === 'soft'); $('scmoody').setAttribute('aria-pressed', S.scene === 'moody');
  $('code').textContent = code(d);
  const n = Z.checkName(S.name);
  $('nameerr').textContent = n.ok ? '' : n.error;
  $('problem').textContent = n.ok ? '' : 'Fix the name before ordering.';
  $('copy').disabled = !n.ok; $('copy').style.opacity = n.ok ? 1 : .45;
  $('vflat').setAttribute('aria-pressed', S.view === 'flat'); $('vtree').setAttribute('aria-pressed', S.view === 'tree');
  $('flatwrap').hidden = S.view !== 'flat'; $('treewrap').hidden = S.view !== 'tree';
  try { localStorage.setItem('zans_bauble_design_v2', JSON.stringify(S)); } catch (e) {}
}
try { const saved = JSON.parse(localStorage.getItem('zans_bauble_design_v2') || 'null'); if (saved) Object.assign(S, saved); } catch (e) {}
$('name').value = S.name;
$('name').addEventListener('input', e => { S.name = e.target.value; render(); });
$('pick1').addEventListener('input', e => { S.c1 = e.target.value.toUpperCase(); render(); });
$('pick2').addEventListener('input', e => { S.c2 = e.target.value.toUpperCase(); render(); });
$('capcol').addEventListener('input', e => { S.capCol = e.target.value.toUpperCase(); render(); });
$('swap').onclick = () => { [S.c1, S.c2] = [S.c2, S.c1]; render(); };
$('vflat').onclick = () => { S.view = 'flat'; render(); };
$('scsoft').onclick = () => { S.scene = 'soft'; render(); };
$('scmoody').onclick = () => { S.scene = 'moody'; render(); };
$('vtree').onclick = () => { S.view = 'tree'; render(); };
$('totree').onclick = () => { S.view = 'tree'; render(); $('preview').scrollIntoView({ behavior: 'smooth', block: 'start' }); };
$('copy').onclick = async () => { const t = $('code').textContent;
  try { await navigator.clipboard.writeText(t); S._copied = t; $('copied').textContent = 'Copied. Paste it into the Etsy box "Design code from our bauble designer".'; }
  catch (e) { const r = document.createRange(); r.selectNodeContents($('code')); const s = getSelection(); s.removeAllRanges(); s.addRange(r); S._copied = t; $('copied').textContent = 'Code selected. Copy it from your phone menu.'; } };
render();

/* ---------- print file (Alex 5 Nov: every designer prints at 2x oversample, like the mug order tool) ----------
   Harrier ceramic bauble print area is 990 x 990 px; we render 3960 x 3960 (4x, Alex 6 Nov "super high definition"; logo source 750 px wide stays sharp) with high-quality smoothing and
   Printify scales it down cleanly. Usage: await ZANSBauble.printFile() -> PNG data URL of the current design. */
window.ZANSBauble = {
  PRINT_PX: 990, OVERSAMPLE: 4,
  async printFile(scale = 4) {
    const px = 990 * scale; let svg = printSVG(design(), 'pf').replace(/width="990" height="990"/, `width="${px}" height="${px}"`).replace(' clip-path="url(#pfc)"', ''); // full square = bleed past the round edge
    // an SVG drawn as an image can't see the page's fonts, so embed Jost (same as the mug order tool)
    if (!this._font) { const buf = await (await fetch('/fonts/jost-latin.woff2')).arrayBuffer(); let bin = ''; new Uint8Array(buf).forEach(b => bin += String.fromCharCode(b)); this._font = btoa(bin); }
    svg = svg.replace('>', `><defs><style>@font-face{font-family:Jost;font-weight:100 900;src:url(data:font/woff2;base64,${this._font}) format('woff2')}</style></defs>`);
    const img = new Image(); img.decoding = 'sync';
    img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
    await img.decode();
    const c = document.createElement('canvas'); c.width = c.height = px;
    const g = c.getContext('2d'); g.imageSmoothingEnabled = true; g.imageSmoothingQuality = 'high';
    g.drawImage(img, 0, 0, px, px);
    return c.toDataURL('image/png');
  },
  code: () => code(design())
};

/* ---------- Christmas sparkles (Alex 5 Nov: "sparkles throughout the page ... glistening and christmassy") ----------
   One fixed canvas over the page with pointer-events off, so taps go straight through. Gold stars twinkle and drift
   slowly down. Every half second each star checks what is under it: over a button, box, colour, picture or the bauble
   it fades away, so sparkles never sit on the controls or the preview. Light on phones (40-80 stars, ~30 fps, stops when
   the tab is hidden). Reduce-motion: a still scatter, no movement. */
(function sparkles() {
  const cv = document.createElement('canvas'); cv.id = 'sparkles'; cv.setAttribute('aria-hidden', 'true');
  document.body.appendChild(cv);
  const ctx = cv.getContext('2d'); if (!ctx) return;
  const still = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  const COLS = ['#B8862B', '#C99A2E', '#D4A93A', '#A97A22'];
  const KEEP_CLEAR = 'p,h1,h2,.lbl,button,input,label,a,img,svg,canvas:not(#sparkles),select,.codebox,.ball,.tree,.opt,.xmasmsg,.zlogo';
  let W, H, dpr, stars = [];
  function size() {
    dpr = Math.min(window.devicePixelRatio || 1, 2); W = innerWidth; H = innerHeight;
    cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const n = Math.round(Math.min(90, Math.max(45, W * H / 6500)));
    stars = Array.from({ length: n }, () => ({ x: Math.random() * W, y: Math.random() * H, r: 4 + 14 * Math.random() ** 2.2, rot: Math.random() * .5 - .25,
      c: COLS[Math.random() * COLS.length | 0], ph: Math.random() * 6.28, sp: .5 + Math.random() * 1.1, dy: .04 + Math.random() * .14, ok: 1, vis: 1 }));
    check();
  }
  function check() {   // fade out stars that sit over anything people tap or look at
    cv.style.visibility = 'hidden';
    for (const s of stars) { const d = s.r * 1.6; s.ok = [[0, 0], [d, 0], [-d, 0], [0, d], [0, -d]].every(([dx, dy]) => { const el = document.elementFromPoint(s.x + dx, s.y + dy); return !(el && el.closest(KEEP_CLEAR)); }); }
    cv.style.visibility = '';
  }
  // Realistic glint: soft warm glow, thin light spikes that taper out, bright white core (pre-drawn once, then stamped)
  const SPR = {};
  function sprite(c) {
    if (SPR[c]) return SPR[c];
    const N = 128, m = N / 2, o = document.createElement('canvas'); o.width = o.height = N; const g = o.getContext('2d');
    let rg = g.createRadialGradient(m, m, 0, m, m, m * .55); rg.addColorStop(0, c + 'DD'); rg.addColorStop(.3, c + '66'); rg.addColorStop(1, c + '00');
    g.fillStyle = rg; g.fillRect(0, 0, N, N);
    const spike = (ang, len, wid, al) => { g.save(); g.translate(m, m); g.rotate(ang);
      const lg = g.createLinearGradient(-len, 0, len, 0); lg.addColorStop(0, c + '00'); lg.addColorStop(.42, c + Math.round(al * 255).toString(16).padStart(2, '0')); lg.addColorStop(.5, `rgba(255,250,225,${al})`); lg.addColorStop(.58, c + Math.round(al * 255).toString(16).padStart(2, '0')); lg.addColorStop(1, c + '00');
      g.fillStyle = lg; g.beginPath(); g.moveTo(-len, 0); g.lineTo(0, -wid); g.lineTo(len, 0); g.lineTo(0, wid); g.closePath(); g.fill(); g.restore(); };
    spike(0, m * .98, 2.6, 1); spike(Math.PI / 2, m * .98, 2.6, 1); spike(Math.PI / 4, m * .5, 1.6, .7); spike(-Math.PI / 4, m * .5, 1.6, .7);
    rg = g.createRadialGradient(m, m, 0, m, m, 9); rg.addColorStop(0, 'rgba(255,255,255,1)'); rg.addColorStop(.4, 'rgba(255,246,210,.9)'); rg.addColorStop(1, 'rgba(255,240,200,0)');
    g.fillStyle = rg; g.beginPath(); g.arc(m, m, 9, 0, 6.29); g.fill();
    return SPR[c] = o;
  }
  function star(x, y, r, a, c, rot) {
    const im = sprite(c), d = r * 4; ctx.globalAlpha = a;
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.drawImage(im, -d / 2, -d / 2, d, d); ctx.restore();
  }
  function draw(t) {
    ctx.clearRect(0, 0, W, H);
    for (const s of stars) {
      const tw = still ? .8 : .35 + .65 * Math.max(0, Math.sin(t / 1000 * s.sp + s.ph)) ** 4; // short bright glint, then rest
      s.vis += ((s.ok ? 1 : 0) - s.vis) * .15;
      if (!still) { s.y += s.dy; if (s.y > H + 10) { s.y = -10; s.x = Math.random() * W; } }
      const a = tw * s.vis; if (a > .03) star(s.x, s.y, s.r * (.55 + .45 * tw), a, s.c, s.rot + tw * .15);
    }
  }
  let last = 0, lastCheck = 0, raf = 0;
  function loop(t) { raf = requestAnimationFrame(loop); if (t - last < 33) return; last = t; if (t - lastCheck > 500) { lastCheck = t; check(); } draw(t); }
  size(); addEventListener('resize', () => { size(); if (still) draw(0); });
  if (still) { addEventListener('scroll', () => { check(); stars.forEach(s => s.vis = s.ok ? 1 : 0); draw(0); }, { passive: true }); stars.forEach(s => s.vis = s.ok ? 1 : 0); draw(0); return; }
  raf = requestAnimationFrame(loop);
  document.addEventListener('visibilitychange', () => { if (document.hidden) cancelAnimationFrame(raf); else raf = requestAnimationFrame(loop); });
})();
