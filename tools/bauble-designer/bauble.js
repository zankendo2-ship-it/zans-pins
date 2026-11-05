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
function logoTab(cy, w) { return `<rect x="${R - w / 2 - 14}" y="${f1(cy - w * 0.0667 - 10)}" width="${w + 28}" height="${f1(w * 0.1333 + 20)}" rx="10" fill="${CREAM}"/><image href="${LOGO_WIDE}" x="${R - w / 2}" y="${f1(cy - w * 0.0667)}" width="${w}" height="${f1(w * 0.1333)}"/>`; }
function designA(d, id) {
  const pat = Z.fillPattern(d.allover, d.c1, d.c2, 0, 0, W, W, scaleFor(d.allover));
  const n = fit(d.name, 640, 210, 120, 0.03), ink = Z.darkOf(d);
  const h = n.lines.length * n.fs * 1.05 + 70, y = 560 - h / 2;
  let t = `<rect x="${R - 380}" y="${f1(y)}" width="760" height="${f1(h)}" rx="${f1(Math.min(90, h / 2))}" fill="${CREAM}" stroke="${GOLD}" stroke-width="12"/>`;
  n.lines.forEach((l, i) => { t += `<text x="${R}" y="${f1(y + 35 + n.fs * 0.86 + i * n.fs * 1.05)}" text-anchor="middle" font-family="Jost" font-weight="700" font-size="${f1(n.fs)}" letter-spacing="${f1(n.fs * 0.03)}" fill="${ink}">${esc(l)}</text>`; });
  return svgWrap(id, pat + capTop(d.capCol) + `<circle cx="${R}" cy="${R}" r="${R - 26}" fill="none" stroke="${GOLD}" stroke-width="14"/>` + t + logoTab(860, 280));
}
function designB(d, id) {
  const jd = Object.assign({}, d, { cap: 'contrast', k1: d.capCol, k2: d.capCol });
  const n = fit(d.name, 600, 150, 96, 0.04);
  let t = ''; const top = n.lines.length === 1 ? 770 : 735;
  n.lines.forEach((l, i) => { t += `<text x="${R}" y="${f1(top + i * n.fs * 1.02)}" text-anchor="middle" font-family="Jost" font-weight="700" font-size="${f1(n.fs)}" letter-spacing="${f1(n.fs * 0.04)}" fill="${GOLD}">${esc(l)}</text>`; });
  const mc = `<text x="${R}" y="${n.lines.length === 1 ? 860 : 875}" text-anchor="middle" font-family="Jost" font-weight="600" font-size="30" letter-spacing="9.6" fill="${GOLD}">MERRY CHRISTMAS</text>`;
  return svgWrap(id, `<defs><filter id="${id}ol" x="-15%" y="-15%" width="130%" height="130%"><feMorphology in="SourceAlpha" operator="dilate" radius="9" result="d"/><feFlood flood-color="${GOLD}"/><feComposite in2="d" operator="in" result="o"/><feMerge><feMergeNode in="o"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><rect width="${W}" height="${W}" fill="${RGREEN}"/><circle cx="${R}" cy="${R}" r="${R - 26}" fill="none" stroke="${GOLD}" stroke-width="8"/><circle cx="${R}" cy="${R}" r="${R - 44}" fill="none" stroke="${GOLD}" stroke-width="2"/>` + `<g filter="url(#${id}ol)">` + jerseyAt(jd, R, n.lines.length === 1 ? 430 : 400, n.lines.length === 1 ? 420 : 380, id + 'j') + '</g>' + t + mc);
}
function svgWrap(id, inner) { return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 ${W} ${W}" width="${W}" height="${W}"><defs><clipPath id="${id}c"><circle cx="${R}" cy="${R}" r="${R}"/></clipPath></defs><g clip-path="url(#${id}c)">${inner}</g></svg>`; }
function printSVG(d, id) { return S.style === 'A' ? designA(d, id) : designB(d, id); }

/* ---------- state ---------- */
const S = { style: 'A', pat: 'hoops', body: 'hoops', c1: '#0E6B3B', c2: '#F5D130', sleeves: 'plain', capCol: '#C8102E', name: 'Lucky Lady', view: 'flat' };
function design() {
  const n = Z.checkName(S.name);
  const d = Z.normalise({ layout: 'B', body: S.style === 'A' ? S.pat : S.body, allover: S.pat, c1: S.c1, c2: S.c2, sleeves: S.sleeves, cap: 'contrast', k1: S.capCol, k2: S.capCol });
  if (S.style === 'B') d.body = S.body;
  d.capCol = S.capCol; d.name = n.ok ? n.text : ((S.name || '').toUpperCase().slice(0, 28) || 'YOUR NAME');
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
const PRESETS = [['Green and yellow hoops, red cap','hoops','#0E6B3B','#F5D130','#C8102E'],['Purple, yellow chevrons, black cap','chevrons','#5B2C83','#F5D130','#1C1C1C'],['Dark blue, orange diagonals, orange cap','diagonal','#1B2A5C','#E36414','#E36414'],['Red, white stars, white cap','stars','#C8102E','#FFFFFF','#FFFFFF'],['Yellow, black spots, black cap','spots','#F5D130','#1C1C1C','#1C1C1C'],['Royal blue and white check, red cap','checks','#1C4FA0','#FFFFFF','#C8102E'],['Maroon, light blue hoops, light blue cap','hoops','#8B1E3F','#7FB7E3','#7FB7E3'],['Emerald, white diamonds, white cap','diamonds','#0E6B3B','#FFFFFF','#FFFFFF']];
function renderControls() {
  const SB = $('styles'); SB.innerHTML = '';
  [['A', 'Silks bauble', 'Your silks all over, a jockey cap across the top, your name on a cream plate'], ['B', 'Racing green bauble', 'Racing green and gold, your jersey and cap, your name in gold, Merry Christmas']].forEach(([k, t, s]) => {
    const d = design(); const svg = (k === 'A' ? designA : designB)(Object.assign({}, d, { allover: S.pat, body: k === 'A' ? S.pat : S.body }), 'st' + k);
    SB.appendChild(optBtn(`<div class="mx-auto" style="max-width:120px">${svg}</div><div class="disp font-semibold mt-2">${t}</div><div class="hint text-sm">${s}</div>`, S.style === k, () => { S.style = k; render(); }));
  });
  const PR = $('presets'); PR.innerHTML = '';
  PRESETS.forEach(([lab, p, a, b, cap], i) => {
    const on = S.pat === p && S.c1.toUpperCase() === a && S.c2.toUpperCase() === b && S.capCol.toUpperCase() === cap;
    PR.appendChild(optBtn(`<div class="mini"><svg viewBox="0 0 110 110" xmlns="http://www.w3.org/2000/svg"><clipPath id="pr${i}"><circle cx="55" cy="55" r="53"/></clipPath><g clip-path="url(#pr${i})">${Z.fillPattern(p, a, b, 0, 0, 110, 110, scaleFor(p) * 0.35)}<rect width="110" height="22" fill="${cap}"/></g><circle cx="55" cy="55" r="53" fill="none" stroke="${GOLD}" stroke-width="3"/></svg></div><div class="text-xs font-semibold mt-1 text-center">${lab}</div>`, on, () => { Object.assign(S, { pat: p, body: Z.BODY.includes(p) ? p : 'hoops', c1: a, c2: b, capCol: cap }); render(); }, lab));
  });
  const P = $('patterns'); P.innerHTML = '';
  (S.style === 'A' ? Z.ALLOVER : Z.BODY).forEach(p => P.appendChild(optBtn(`<div class="mini">${S.style === 'A' ? miniA(p) : miniB(p)}</div><div class="text-xs font-semibold mt-1 text-center">${Z.NAMES[p] || p}</div>`, (S.style === 'A' ? S.pat : S.body) === p, () => { if (S.style === 'A') { S.pat = p; if (Z.BODY.includes(p)) S.body = p; } else { S.body = p; if (Z.ALLOVER.includes(p)) S.pat = p; } render(); }, Z.NAMES[p])));
  swatches($('c1'), 'c1'); swatches($('c2'), 'c2'); swatches($('capsw'), 'capCol');
  $('pick1').value = S.c1; $('pick2').value = S.c2; $('capcol').value = S.capCol;
  $('sleevestep').hidden = S.style !== 'B';
  const SL = $('sleeves'); SL.innerHTML = ''; Z.SLEEVES.forEach(p => SL.appendChild(chip(p === 'plain' ? 'Same as jersey' : Z.NAMES[p], S.sleeves === p, () => { S.sleeves = p; render(); })));
  $('count').textContent = `${(S.name || '').length}/28`;
}

/* ---------- Christmas tree scene ---------- */
function treeScene(baubleSvg) {   // Alex 5 Nov: realistic tree, bauble life-size (7.5 cm) next to real decorations
  // Photo: AI-made for ZANS (FLUX.1 Krea), /img/bauble-tree-scene.jpg 864x1072. Our bauble hangs where the photo's red ball was.
  const cx = 608, cy = 576, r = 136, top = cy - r;
  const inner = baubleSvg.replace(/^<svg[^>]*>/, '').replace(/<\/svg>$/, '').replace(/id="([^"]+)"/g, 'id="tr$1"').replace(/url\(#([^)]+)\)/g, 'url(#tr$1)');
  const RIB = '#A3101C', RIB2 = '#D42A35';
  return `<svg viewBox="170 170 694 860" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" role="img" aria-label="Your bauble hanging on a real Christmas tree, shown life-size next to other decorations">
  <defs>
    <radialGradient id="glaze" cx="32%" cy="26%" r="80%"><stop offset="0" stop-color="#fff" stop-opacity=".42"/><stop offset=".22" stop-color="#fff" stop-opacity=".08"/><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".30"/></radialGradient>
    <linearGradient id="streak" x1="0" y1="0" x2="1" y2="1"><stop offset=".3" stop-color="#fff" stop-opacity="0"/><stop offset=".42" stop-color="#fff" stop-opacity=".22"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient>
    <linearGradient id="rib" x1="0" x2="1"><stop offset="0" stop-color="${RIB}"/><stop offset=".5" stop-color="${RIB2}"/><stop offset="1" stop-color="${RIB}"/></linearGradient>
    <filter id="shadow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur in="SourceAlpha" stdDeviation="10"/><feOffset dx="10" dy="16"/><feComponentTransfer><feFuncA type="linear" slope=".55"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <clipPath id="disc"><circle cx="${cx}" cy="${cy}" r="${r}"/></clipPath>
  </defs>
  <image href="/img/bauble-tree-scene.jpg" x="0" y="0" width="864" height="1072" preserveAspectRatio="xMidYMid slice"/>
  <g class="swing" style="transform-origin:605px 345px">
    <path d="M603,348 C597,380 596,412 600,${top + 20} M607,348 C613,380 614,412 610,${top + 20}" fill="none" stroke="url(#rib)" stroke-width="6" stroke-linecap="round"/><path d="M596,352 q9,-14 18,0" fill="none" stroke="${RIB}" stroke-width="6" stroke-linecap="round"/>
    <g filter="url(#shadow)">
      <circle cx="${cx + 5}" cy="${cy + 6}" r="${r}" fill="#CFC5B4"/>
      <g clip-path="url(#disc)"><g transform="translate(${cx - r},${cy - r}) scale(${f1(2 * r / 990 * 1000) / 1000})">${inner}</g>
        <rect x="${cx - r}" y="${cy - r}" width="${2 * r}" height="${2 * r}" fill="#FFB060" opacity=".07"/>
        <circle cx="${cx}" cy="${cy}" r="${r}" fill="url(#glaze)"/><rect x="${cx - r}" y="${cy - r}" width="${2 * r}" height="${2 * r}" fill="url(#streak)"/></g>
      <circle cx="${cx}" cy="${cy}" r="${r - 0.8}" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="1.6"/>
    </g>
    <circle cx="${cx}" cy="${top + 20}" r="8" fill="#14110E" stroke="#E8E0D0" stroke-width="2"/>
    <path d="M605,${top - 8} c-30,-26 -62,-14 -52,6 c8,14 36,8 52,-6 z M605,${top - 8} c30,-26 62,-14 52,6 c-8,14 -36,8 -52,-6 z" fill="url(#rib)" stroke="#7E0B15" stroke-width="1.5"/>
    <path d="M600,${top - 4} l-22,38 l12,-4 l6,12 z M610,${top - 4} l22,38 l-12,-4 l-6,12 z" fill="${RIB}" stroke="#7E0B15" stroke-width="1.2"/>
    <rect x="596" y="${top - 18}" width="18" height="18" rx="5" fill="${RIB2}" stroke="#7E0B15" stroke-width="1.5"/>
  </g></svg>`;
}

/* ---------- render ---------- */
function render() {
  renderControls();
  const d = design(), svg = printSVG(d, 'pv');
  $('flat').innerHTML = svg;
  $('ribbonname').textContent = S.style === 'A' ? 'Silks bauble' : 'Racing green bauble';
  $('tree').innerHTML = treeScene(printSVG(d, 'tv'));
  $('code').textContent = code(d);
  const n = Z.checkName(S.name);
  $('nameerr').textContent = n.ok ? '' : n.error;
  $('problem').textContent = n.ok ? '' : 'Fix the name before ordering.';
  $('copy').disabled = !n.ok; $('copy').style.opacity = n.ok ? 1 : .45;
  $('vflat').setAttribute('aria-pressed', S.view === 'flat'); $('vtree').setAttribute('aria-pressed', S.view === 'tree');
  $('flatwrap').hidden = S.view !== 'flat'; $('treewrap').hidden = S.view !== 'tree';
  try { localStorage.setItem('zans_bauble_design', JSON.stringify(S)); } catch (e) {}
}
try { const saved = JSON.parse(localStorage.getItem('zans_bauble_design') || 'null'); if (saved) Object.assign(S, saved); } catch (e) {}
$('name').value = S.name;
$('name').addEventListener('input', e => { S.name = e.target.value; render(); });
$('pick1').addEventListener('input', e => { S.c1 = e.target.value.toUpperCase(); render(); });
$('pick2').addEventListener('input', e => { S.c2 = e.target.value.toUpperCase(); render(); });
$('capcol').addEventListener('input', e => { S.capCol = e.target.value.toUpperCase(); render(); });
$('swap').onclick = () => { [S.c1, S.c2] = [S.c2, S.c1]; render(); };
$('vflat').onclick = () => { S.view = 'flat'; render(); };
$('vtree').onclick = () => { S.view = 'tree'; render(); };
$('totree').onclick = () => { S.view = 'tree'; render(); $('preview').scrollIntoView({ behavior: 'smooth', block: 'start' }); };
$('copy').onclick = async () => { const t = `${$('code').textContent}  |  ${design().name}`;
  try { await navigator.clipboard.writeText(t); $('copied').textContent = 'Copied. Paste it into the Etsy personalisation box.'; }
  catch (e) { const r = document.createRange(); r.selectNodeContents($('code')); const s = getSelection(); s.removeAllRanges(); s.addRange(r); $('copied').textContent = 'Code selected. Copy it from your phone menu.'; } };
render();
