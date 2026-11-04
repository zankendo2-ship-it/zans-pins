// Old v new mug designer, side by side in real Chrome (GitHub runner, internet on so the old page's Tailwind CDN loads).
// For every step of the designer it compares: computed CSS of every element, the full page picture (3D canvas masked),
// and the 3D mug picture once it has settled. It also checks the CDN's own CSS against our prebuilt CSS, counts how
// often the 3D mug is redrawn while nobody touches the page, and records console errors.
// Usage: node compare.cjs <outDir> name=url name=url ...   (first site = the reference, normally the live page)
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright-core');
const { PNG } = require('pngjs');
const pixelmatch = require('pixelmatch');

const out = process.argv[2];
const sites = process.argv.slice(3).map(a => { const i = a.indexOf('='); return { name: a.slice(0, i), url: a.slice(i + 1) }; });
fs.mkdirSync(out, { recursive: true });
const chromePath = ['/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', process.env.CHROME_PATH].find(p => p && fs.existsSync(p));

const VIEWPORTS = [
  { name: 'phone', width: 390, height: 844, isMobile: true, hasTouch: true },
  { name: 'tablet', width: 820, height: 1180, isMobile: true, hasTouch: true },
  { name: 'desktop', width: 1366, height: 900 },
].filter(v => !process.env.VPS || process.env.VPS.split(',').includes(v.name));

// Same clicks on every site. wait = ms to let the page (and the 3D turn) settle.
const STEPS = [
  { name: 'loaded', wait: 7000 },
  { name: 'preset 2', act: p => p.locator('#presets .opt').nth(1).click(), wait: 2500 },
  { name: 'pattern 5', act: p => p.locator('#patterns .opt').nth(4).click(), wait: 2500 },
  { name: 'main colour 4', act: p => p.locator('#c1 .sw').nth(3).click(), wait: 2500 },
  { name: 'second colour 7', act: p => p.locator('#c2 .sw').nth(6).click(), wait: 2500 },
  { name: 'swap colours', act: p => p.locator('#swap').click(), wait: 2500 },
  { name: 'type name', act: async p => { await p.locator('#name').fill('Midnight Runner'); }, wait: 2500 },
  { name: 'name too long', act: async p => { await p.locator('#name').fill('ABCDEFGHIJKLMNOPQRSTUVWXYZABCD'); }, wait: 2500 },
  { name: 'name back', act: async p => { await p.locator('#name').fill('Lucky Lady'); }, wait: 2500 },
  { name: 'handle colour 3', act: p => p.locator('#handles .opt').nth(2).click(), wait: 2500 },
  { name: 'ring on', act: p => p.locator('#ring').check(), wait: 2500 },
  { name: 'ring colour 2', act: p => p.locator('#ringsw .sw').nth(1).click(), wait: 2500 },
  { name: 'sync off', act: p => p.locator('#sync').uncheck({ force: true }), wait: 2500 },
  { name: 'turn it round', act: p => p.locator('#spin').click(), wait: 8000 },
  { name: 'drag mug', act: async p => {
      const c = p.locator('#stage canvas'); await c.scrollIntoViewIfNeeded(); const b = await c.boundingBox();
      if (!b) return 'no canvas';
      await p.mouse.move(b.x + b.width / 2, b.y + b.height / 2); await p.mouse.down();
      await p.mouse.move(b.x + b.width / 2 + 90, b.y + b.height / 2, { steps: 12 }); await p.mouse.up();
    }, wait: 6000 },
  { name: 'preset 1', act: p => p.locator('#presets .opt').nth(0).click(), wait: 2500 },
  { name: 'copy code', act: p => p.locator('#copy').click(), wait: 2500 },
  { name: 'scroll top', act: p => p.evaluate(() => window.scrollTo(0, 0)), wait: 2500 },
];

const INIT = () => {
  window.__draws = 0;
  for (const C of [window.WebGLRenderingContext, window.WebGL2RenderingContext]) {
    if (!C) continue;
    for (const f of ['drawElements', 'drawArrays']) { const o = C.prototype[f]; C.prototype[f] = function () { window.__draws++; return o.apply(this, arguments); }; }
  }
};

// Hash of every computed style property of every element in <body> (same order on every site).
const SNAP = () => {
  const els = [...document.body.querySelectorAll('*')];
  const props = [...getComputedStyle(document.body)];
  return {
    height: document.documentElement.scrollHeight,
    els: els.map(e => {
      const cs = getComputedStyle(e); let h = 2166136261;
      for (const p of props) { const v = cs.getPropertyValue(p); for (let i = 0; i < v.length; i++) { h ^= v.charCodeAt(i); h = Math.imul(h, 16777619); } h ^= 124; h = Math.imul(h, 16777619); }
      const r = e.getBoundingClientRect();
      return [e.tagName + (e.id ? '#' + e.id : '') + (typeof e.className === 'string' && e.className ? '.' + e.className.trim().split(/\s+/).join('.') : ''), h >>> 0, [r.x, r.y, r.width, r.height].map(n => Math.round(n * 10) / 10).join(',')];
    }),
    classes: [...new Set(els.flatMap(e => (typeof e.className === 'string' ? e.className.split(/\s+/) : [])).filter(Boolean))],
  };
};
const DETAIL = (i) => {
  const e = document.body.querySelectorAll('*')[i]; const cs = getComputedStyle(e); const o = {};
  for (const p of cs) o[p] = cs.getPropertyValue(p); return o;
};
const RULES = (which) => {
  // which: 'cdn' = the <style> the Tailwind CDN made, 'ours' = #zans-tw
  const styles = [...document.querySelectorAll('style')];
  const el = which === 'ours' ? document.getElementById('zans-tw') : styles.find(s => s.id !== 'zans-tw' && /--tw-|tailwindcss/.test(s.textContent) && !s.textContent.includes('Layout: two panes'));
  if (!el) return null;
  const list = [];
  const walk = (rules, pre) => { for (const r of rules) { if (r.cssRules && r.media) walk(r.cssRules, pre + '@media ' + r.media.mediaText + ' '); else if (r.selectorText) list.push([pre + r.selectorText, r.style.cssText]); } };
  walk(el.sheet.cssRules, '');
  const head = [...document.head.children].map((c, i) => `${i} ${c.tagName}${c.id ? '#' + c.id : ''}${c.src ? ' src=' + c.getAttribute('src') : ''}${c === el ? '  <== Tailwind CSS' : ''}${c.tagName === 'STYLE' && c !== el ? ' (' + c.textContent.trim().slice(0, 40).replace(/\s+/g, ' ') + ')' : ''}`);
  return { rules: list, head, text: el.textContent };
};

const saved = {};
function keep(key) { saved[key] = (saved[key] || 0) + 1; return saved[key] <= 3; } // at most 3 example pictures per kind
function pngDiff(a, b, file, key) {
  const A = PNG.sync.read(a), B = PNG.sync.read(b);
  if (A.width !== B.width || A.height !== B.height) return { sizeA: [A.width, A.height], sizeB: [B.width, B.height], diff: -1 };
  const D = new PNG({ width: A.width, height: A.height });
  const n = pixelmatch(A.data, B.data, D.data, A.width, A.height, { threshold: 0 });
  // visible = what a person could notice (pixelmatch's normal threshold); maxDelta = biggest colour step in any channel
  const visible = n ? pixelmatch(A.data, B.data, null, A.width, A.height, { threshold: 0.1 }) : 0;
  let maxDelta = 0; if (n) for (let i = 0; i < A.data.length; i++) { const d = Math.abs(A.data[i] - B.data[i]); if (d > maxDelta) maxDelta = d; }
  if (n > 0 && file && keep(key)) fs.writeFileSync(file, PNG.sync.write(D));
  return { diff: n, visible, maxDelta, size: [A.width, A.height] };
}

(async () => {
  const browser = await chromium.launch({ executablePath: chromePath, headless: true,
    args: ['--no-sandbox', '--enable-unsafe-swiftshader', '--use-angle=swiftshader', '--ignore-gpu-blocklist', '--font-render-hinting=none'] });
  const report = { chrome: browser.version(), sites, viewports: {} };
  const ref = sites[0].name;
  for (const vp of VIEWPORTS) {
    const R = report.viewports[vp.name] = { steps: [], errors: {}, idleDraws: {}, cssCheck: {} };
    const pages = {};
    for (const s of sites) {
      const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height }, isMobile: !!vp.isMobile, hasTouch: !!vp.hasTouch, deviceScaleFactor: 1 });
      await ctx.addInitScript(INIT);
      const p = await ctx.newPage(); R.errors[s.name] = [];
      p.on('pageerror', e => R.errors[s.name].push('pageerror: ' + e.message));
      p.on('console', m => { if (m.type() === 'error') R.errors[s.name].push('console: ' + m.text().slice(0, 200)); });
      p.on('requestfailed', r => R.errors[s.name].push('request failed: ' + r.url().slice(0, 120)));
      pages[s.name] = p;
    }
    await Promise.all(sites.map(s => pages[s.name].goto(s.url, { waitUntil: 'load' })));
    for (const st of STEPS) {
      const row = { step: st.name, vs: {} };
      for (const s of sites) { if (st.act) { try { const r = await st.act(pages[s.name]); if (r) row['note_' + s.name] = r; } catch (e) { row['fail_' + s.name] = String(e.message).slice(0, 160); } } }
      await pages[ref].waitForTimeout(st.wait);
      const snaps = {}, shots = {}, mugs = {};
      for (const s of sites) {
        const p = pages[s.name];
        snaps[s.name] = await p.evaluate(SNAP);
        shots[s.name] = await p.screenshot({ fullPage: true, mask: [p.locator('#stage canvas')], animations: 'disabled' });
        try { mugs[s.name] = await p.locator('#stage').screenshot(); } catch (e) { mugs[s.name] = null; }
      }
      const tag = `${vp.name}_${String(R.steps.length).padStart(2, '0')}_${st.name.replace(/\W+/g, '-')}`;
      if (['loaded', 'turn it round', 'scroll top'].includes(st.name)) fs.writeFileSync(path.join(out, `${tag}_${ref}.png`), shots[ref]);
      for (const s of sites.slice(1)) {
        const a = snaps[ref], b = snaps[s.name];
        const v = { heightRef: a.height, height: b.height, elements: [a.els.length, b.els.length], styleDiffs: [], moved: [] };
        if (a.els.length === b.els.length) {
          for (let i = 0; i < a.els.length; i++) {
            if (a.els[i][0] !== b.els[i][0]) { v.styleDiffs.push({ i, ref: a.els[i][0], other: b.els[i][0], note: 'different element' }); continue; }
            if (a.els[i][2] !== b.els[i][2]) v.moved.push({ i, el: a.els[i][0].slice(0, 80), ref: a.els[i][2], other: b.els[i][2] });
            if (a.els[i][1] !== b.els[i][1] && v.styleDiffs.length < 40) {
              const da = await pages[ref].evaluate(DETAIL, i), db = await pages[s.name].evaluate(DETAIL, i);
              const props = Object.keys(da).filter(k => da[k] !== db[k]).map(k => `${k}: ${da[k]} -> ${db[k]}`);
              v.styleDiffs.push({ i, el: a.els[i][0].slice(0, 100), props: props.slice(0, 12) });
            }
          }
        }
        v.moved = v.moved.slice(0, 20);
        v.page = pngDiff(shots[ref], shots[s.name], path.join(out, `${tag}_${s.name}_pagediff.png`), vp.name + s.name + 'page');
        v.mug = (mugs[ref] && mugs[s.name]) ? pngDiff(mugs[ref], mugs[s.name], path.join(out, `${tag}_${s.name}_mugdiff.png`), vp.name + s.name + 'mug') : 'no mug';
        if (v.page.diff !== 0 && keep(vp.name + s.name + 'pageshot')) { fs.writeFileSync(path.join(out, `${tag}_${s.name}.png`), shots[s.name]); fs.writeFileSync(path.join(out, `${tag}_${ref}_forpage.png`), shots[ref]); }
        if (v.mug && v.mug.diff && keep(vp.name + s.name + 'mugshot')) { fs.writeFileSync(path.join(out, `${tag}_${ref}_mug.png`), mugs[ref]); fs.writeFileSync(path.join(out, `${tag}_${s.name}_mug.png`), mugs[s.name]); }
        row.vs[s.name] = v;
      }
      // Tailwind classes the reference page actually shows, so we can check they are all in our CSS
      row.classesRef = snaps[ref].classes.length;
      R.allClasses = [...new Set([...(R.allClasses || []), ...snaps[ref].classes])];
      R.steps.push(row);
      console.log(vp.name, st.name, JSON.stringify(Object.fromEntries(Object.entries(row.vs).map(([k, v]) => [k, { css: v.styleDiffs.length, moved: v.moved.length, page: v.page.diff, mug: v.mug && v.mug.diff }]))));
    }
    // redraws while nobody touches the page (10 s)
    for (const s of sites) {
      const p = pages[s.name]; await p.evaluate(() => window.scrollTo(0, 0));
    }
    await pages[ref].waitForTimeout(3000);
    const d0 = {}; for (const s of sites) d0[s.name] = await pages[s.name].evaluate(() => window.__draws);
    await pages[ref].waitForTimeout(10000);
    for (const s of sites) R.idleDraws[s.name] = (await pages[s.name].evaluate(() => window.__draws)) - d0[s.name];
    // CSS check: every rule the CDN made must be in ours with the same declarations
    const cdn = await pages[ref].evaluate(RULES, 'cdn');
    if (cdn) {
      fs.writeFileSync(path.join(out, `${vp.name}_cdn_generated.css`), cdn.text);
      R.cdnHead = cdn.head;
      for (const s of sites.slice(1)) {
        const ours = await pages[s.name].evaluate(RULES, 'ours');
        if (!ours) { R.cssCheck[s.name] = 'no #zans-tw'; continue; }
        const om = new Map(ours.rules.map(([k, v]) => [k, v]));
        const cm = new Map(cdn.rules.map(([k, v]) => [k, v]));
        R.cssCheck[s.name] = {
          cdnRules: cdn.rules.length, ourRules: ours.rules.length,
          missingInOurs: cdn.rules.filter(([k]) => !om.has(k)).map(([k]) => k),
          differentDeclarations: cdn.rules.filter(([k, v]) => om.has(k) && om.get(k) !== v).map(([k, v]) => `${k} | cdn: ${v} | ours: ${om.get(k)}`).slice(0, 30),
          extraInOurs: ours.rules.filter(([k]) => !cm.has(k)).map(([k]) => k),
          orderSame: JSON.stringify(cdn.rules.map(r => r[0]).filter(k => om.has(k))) === JSON.stringify(ours.rules.map(r => r[0]).filter(k => cm.has(k))),
          head: ours.head,
        };
      }
    } else R.cdnHead = 'Tailwind CDN style not found on the reference page';
    for (const s of sites) await pages[s.name].context().close();
  }
  await browser.close();
  fs.writeFileSync(path.join(out, 'report.json'), JSON.stringify(report, null, 1));
  // short summary
  const L = [`# Mug designer: old v new (${new Date().toISOString().slice(0, 16)} UTC, ${report.chrome})`, ''];
  for (const [vn, R] of Object.entries(report.viewports)) {
    L.push(`## ${vn}`);
    for (const s of sites.slice(1)) {
      const steps = R.steps.map(r => r.vs[s.name]);
      const css = steps.reduce((t, v) => t + v.styleDiffs.length, 0), moved = steps.reduce((t, v) => t + v.moved.length, 0);
      const page = steps.filter(v => v.page.diff !== 0).length, mug = steps.filter(v => v.mug && v.mug.diff).length;
      const pageVis = steps.filter(v => v.page.diff === -1 || v.page.visible).length, mugVis = steps.filter(v => v.mug && v.mug.visible).length;
      const maxD = Math.max(0, ...steps.map(v => Math.max(v.page.maxDelta || 0, (v.mug && v.mug.maxDelta) || 0)));
      L.push(`- ${s.name} v ${ref}: ${R.steps.length} steps | style differences ${css} | elements moved ${moved} | page pictures different ${page} (visible ${pageVis}) | 3D mug pictures different ${mug} (visible ${mugVis}) | biggest colour step ${maxD}/255`);
      const c = R.cssCheck[s.name];
      if (c && typeof c === 'object') L.push(`  - CSS: CDN made ${c.cdnRules} rules, ours ${c.ourRules}; missing in ours ${c.missingInOurs.length}; different declarations ${c.differentDeclarations.length}; same order ${c.orderSame}`);
    }
    L.push(`- 3D redraws in 10 s with nobody touching the page: ${JSON.stringify(R.idleDraws)}`);
    L.push(`- errors: ${JSON.stringify(Object.fromEntries(Object.entries(R.errors).map(([k, v]) => [k, v.length])))}`);
    L.push('');
  }
  fs.writeFileSync(path.join(out, 'summary.md'), L.join('\n') + '\n');
  console.log(L.join('\n'));
})().catch(e => { console.error(e); process.exit(1); });
