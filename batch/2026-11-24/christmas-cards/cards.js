const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const T = path.join(__dirname, '../../../templates'); const b64 = f => fs.readFileSync(f).toString('base64');
const font = (n, w, f) => `@font-face{font-family:'${n}';font-weight:${w};src:url(data:font/woff2;base64,${b64(path.join(T, 'fonts', f))})}`;
const img = f => `data:image/${f.endsWith('png') ? 'png' : 'webp'};base64,${b64(path.join(__dirname, 'scenes', f))}`;
const metal = 'linear-gradient(90deg,#8a6a22,#f2cf5b 18%,#fff3c8 32%,#c9a13b 50%,#fff3c8 68%,#f2cf5b 82%,#8a6a22)';
const base = `${font('Jost', 600, 'jost-600.woff2')}${font('Jost', 700, 'jost-700.woff2')}*{box-sizing:border-box;margin:0}body{width:1500px;height:2100px;position:relative;overflow:hidden;font-family:'Jost'}
.bg{position:absolute;inset:0;background-size:cover;background-position:center}.serif{font-family:'Liberation Serif','FreeSerif',serif}`;
const cards = {
'1-flying-finish': `<div class="bg" style="background-image:url(${img('finish2.png')})"></div>
<div style="position:absolute;left:0;right:0;bottom:0;height:900px;background:linear-gradient(transparent,rgba(10,30,20,.88) 55%)"></div>
<div style="position:absolute;left:90px;right:90px;bottom:120px;color:#fff;text-align:center">
<div class="serif" style="font-style:italic;font-size:210px;line-height:.95">Merry Christmas</div>
<div style="font-weight:600;letter-spacing:12px;font-size:50px;color:#F2CF5B;margin-top:34px">AND A FLYING FINISH TO THE YEAR</div></div>`,
'2-winning-post': `<div class="bg" style="background-image:url(${img('post.webp')})"></div>
<div style="position:absolute;left:0;right:0;top:70px;text-align:center;color:#fff">
<div style="font-weight:600;letter-spacing:16px;font-size:46px;color:#FFE9A8">MERRY CHRISTMAS</div>
<div class="serif" style="font-weight:700;font-size:130px;line-height:1;margin-top:10px;text-shadow:0 4px 30px rgba(0,20,50,.5)">First past the post</div></div>`,
'3-christmas-jumper': `<div style="position:absolute;inset:0;background:#F3EDE5"></div>
<div style="position:absolute;left:90px;right:90px;top:90px;height:1500px;background-image:url(${img('jumper.webp')});background-size:cover;background-position:center 40%;box-shadow:0 14px 50px rgba(0,0,0,.28)"></div>
<div style="position:absolute;left:90px;right:90px;top:1650px;text-align:center;color:#1F5A3D">
<div style="font-weight:700;font-size:112px;line-height:1.02">CHRISTMAS JUMPER?</div>
<div class="serif" style="font-style:italic;font-size:92px;color:#B3202A;margin-top:14px">I'd rather wear my silks.</div></div>`,
'4-boxing-day': `<div style="position:absolute;inset:0;background:#1F5A3D"></div>
<div style="position:absolute;left:0;right:0;top:0;height:1500px;background-image:url(${img('boxing.webp')});background-size:cover;background-position:center 30%"></div>
<div style="position:absolute;left:0;right:0;top:1500px;height:26px;background:${metal}"></div>
<div style="position:absolute;left:0;right:0;bottom:0;height:26px;background:${metal}"></div>
<div style="position:absolute;left:0;right:0;top:1610px;text-align:center;color:#fff">
<div style="font-weight:700;font-size:205px;line-height:.9;letter-spacing:4px;white-space:nowrap;color:#F2CF5B">BOXING DAY</div>
<div class="serif" style="font-style:italic;font-size:86px;margin-top:26px">The best day of Christmas</div></div>`,
'5-photo-finish': `<div class="bg" style="background-image:url(${img('reindeer.webp')})"></div>
<div style="position:absolute;left:90px;top:110px;transform:rotate(-5deg);border:12px solid #fff;color:#fff;padding:8px 44px;font-weight:700;font-size:150px;letter-spacing:8px;line-height:1.1">PHOTO FINISH</div>
<div style="position:absolute;left:0;right:0;bottom:0;height:520px;background:linear-gradient(transparent,rgba(0,0,0,.75))"></div>
<div style="position:absolute;left:0;right:0;bottom:120px;text-align:center;color:#fff">
<div class="serif" style="font-style:italic;font-size:130px">Rudolph, by a nose.</div>
<div style="font-weight:600;letter-spacing:14px;font-size:52px;color:#F2CF5B;margin-top:18px">MERRY CHRISTMAS</div></div>`,
'6-stewards-enquiry': `<div style="position:absolute;inset:0;background:#F3EDE5"></div>
<div style="position:absolute;left:0;right:0;top:0;height:26px;background:${metal}"></div><div style="position:absolute;left:0;right:0;bottom:0;height:26px;background:${metal}"></div>
<div style="position:absolute;left:110px;right:110px;top:150px;bottom:150px;border:8px solid #1C1C1C;padding:70px 50px;text-align:center;color:#1C1C1C">
<div style="font-weight:600;letter-spacing:14px;font-size:44px">OFFICIAL NOTICE · 25 DEC</div>
<div style="height:8px;background:#1C1C1C;margin:44px 0"></div>
<div style="font-weight:700;font-size:176px;line-height:.92;color:#B3202A">STEWARDS' ENQUIRY</div>
<div class="serif" style="font-style:italic;font-size:110px;margin-top:50px">Naughty or nice?</div>
<div style="height:4px;background:#1C1C1C;margin:50px 120px"></div>
<div style="font-weight:600;font-size:60px;line-height:1.4">After viewing the evidence,<br>the stewards found:</div>
<div style="display:inline-block;margin-top:50px;background:#1F5A3D;color:#F2CF5B;font-weight:700;font-size:150px;letter-spacing:10px;padding:6px 70px">NICE</div>
<div style="font-weight:700;font-size:66px;margin-top:50px">RESULT STANDS.<br>PRESENTS UNALTERED.</div>
<div class="serif" style="font-style:italic;font-size:66px;margin-top:44px;color:#5E574F">Merry Christmas</div></div>`,
};
for (const k of ['a', 'b', 'c']) cards[`7-your-own-silks-example-${k}`] = `<div class="bg" style="background-image:url(${img(`silks-${k}.png`)})"></div>
<div style="position:absolute;left:0;right:0;top:0;height:26px;background:${metal}"></div><div style="position:absolute;left:0;right:0;bottom:0;height:26px;background:${metal}"></div>
<div style="position:absolute;left:0;right:0;top:26px;height:330px;background:linear-gradient(rgba(243,237,229,.97) 80%,transparent)"></div><div style="position:absolute;left:0;right:0;top:64px;text-align:center;color:#1F5A3D">
<div style="font-weight:600;letter-spacing:14px;font-size:42px">MERRY CHRISTMAS FROM</div>
<div style="font-weight:700;font-size:136px;line-height:1.05;margin-top:2px">${{ a: 'THE SYNDICATE', b: 'GRANDAD', c: 'TEAM LUCKY' }[k]}</div></div>
<div style="position:absolute;left:0;right:0;bottom:0;height:560px;background:linear-gradient(transparent,rgba(20,50,35,.85) 60%)"></div>
<div style="position:absolute;left:0;right:0;bottom:110px;text-align:center;color:#fff">
<div class="serif" style="font-style:italic;font-size:120px">Your colours. Your Christmas.</div></div>`;

const full = f => `<div class="bg" style="background-image:url(${img(f)})"></div>`;
const shade = (pos, h, a = .8) => `<div style="position:absolute;left:0;right:0;${pos}:0;height:${h}px;background:linear-gradient(${pos === 'bottom' ? 'transparent' : `rgba(8,20,14,${a}) 30%`},${pos === 'bottom' ? `rgba(8,20,14,${a}) 60%` : 'transparent'})"></div>`;
Object.assign(cards, {
'8-stable-door': `${full('stable.webp')}${shade('bottom', 520)}
<div style="position:absolute;left:0;right:0;bottom:110px;text-align:center;color:#fff"><div class="serif" style="font-style:italic;font-size:150px;line-height:1">Merry Christmas</div>
<div style="font-weight:600;letter-spacing:14px;font-size:50px;color:#F2CF5B;margin-top:22px">FROM EVERYONE AT THE YARD</div></div>`,
'9-santa-hat': `${full('santahat.webp')}
<div style="position:absolute;left:0;right:0;top:70px;text-align:center"><div style="display:inline-block;background:#C8102E;color:#fff;font-weight:700;font-size:150px;line-height:1;padding:22px 60px;transform:rotate(-2deg);box-shadow:0 10px 30px rgba(0,0,0,.25)">HO HO HORSE</div></div>
${shade('bottom', 380, .7)}<div style="position:absolute;left:0;right:0;bottom:90px;text-align:center;color:#fff;font-weight:600;letter-spacing:12px;font-size:52px">MERRY CHRISTMAS</div>`,
'10-fireside': `${full('fireside.webp')}${shade('bottom', 620, .85)}
<div style="position:absolute;left:90px;right:90px;bottom:110px;color:#fff"><div class="serif" style="font-size:118px;line-height:1.05;font-weight:700">Boots off.<br>Feet up.</div>
<div class="serif" style="font-style:italic;font-size:92px;color:#F2CF5B;margin-top:20px">Back in the saddle Boxing Day.</div></div>`,
'11-robin': `${full('robin.webp')}
<div style="position:absolute;left:0;right:0;top:150px;text-align:center;color:#5a2b22"><div class="serif" style="font-style:italic;font-size:170px;line-height:1">Season's Greetings</div>
<div style="font-weight:600;letter-spacing:14px;font-size:44px;margin-top:26px">FROM THE RAILS</div></div>`,
'12-gingerbread-stakes': `<div style="position:absolute;inset:0;background:#B3202A"></div>
<div style="position:absolute;left:80px;right:80px;top:330px;bottom:80px;background-image:url(${img('gingerbread.webp')});background-size:cover;background-position:center;border:14px solid #fff"></div>
<div style="position:absolute;left:0;right:0;top:70px;text-align:center;color:#fff"><div style="font-weight:700;font-size:98px;line-height:1;white-space:nowrap">THE GINGERBREAD STAKES</div>
<div class="serif" style="font-style:italic;font-size:70px;margin-top:10px;color:#FFE9A8">They're off, and they're delicious</div></div>`,
'13-lucky-horseshoe': `${full('horseshoe.webp')}${shade('top', 420, .75)}
<div style="position:absolute;left:0;right:0;top:80px;text-align:center;color:#F2CF5B"><div style="font-weight:700;font-size:128px;letter-spacing:6px;line-height:1">GOOD LUCK</div></div>
${shade('bottom', 460, .8)}<div style="position:absolute;left:0;right:0;bottom:100px;text-align:center;color:#fff"><div class="serif" style="font-style:italic;font-size:118px">and a Merry Christmas</div></div>`,
'14-snow-globe': `${full('globe.webp')}
<div style="position:absolute;left:0;right:0;top:110px;text-align:center;color:#3a2a22"><div style="font-weight:600;letter-spacing:16px;font-size:46px">LET IT</div>
<div style="font-weight:700;font-size:240px;line-height:.95;letter-spacing:10px">SNOW</div></div>`,
'15-silks-stockings': `${full('stockings.webp')}
<div style="position:absolute;left:0;right:0;top:0;height:330px;background:#F3EDE5"></div><div style="position:absolute;left:0;right:0;top:330px;height:14px;background:${metal}"></div><div style="position:absolute;left:0;right:0;top:66px;text-align:center;color:#1F5A3D"><div style="font-weight:700;font-size:84px;line-height:1.12">THE STOCKINGS WERE HUNG<br>IN THEIR COLOURS WITH CARE</div></div>`,
'16-parade-ring-tree': `${full('tree.webp')}
<div style="position:absolute;left:0;right:0;top:90px;text-align:center;color:#fff"><div class="serif" style="font-size:150px;line-height:1;font-weight:700">Merry &amp; Bright</div></div>
${shade('bottom', 420, .8)}<div style="position:absolute;left:0;right:0;bottom:100px;text-align:center;color:#F2CF5B;font-weight:600;letter-spacing:12px;font-size:50px">CHRISTMAS AT THE RACES</div>`,
'17-all-i-want': `${full('noses.webp')}${shade('bottom', 520, .9)}
<div style="position:absolute;left:0;right:0;bottom:90px;text-align:center;color:#fff"><div class="serif" style="font-style:italic;font-size:124px;line-height:1.05">All I want for Christmas<br>is you</div></div>`,
'18-morning-gallops': `${full('gallops.webp')}
<div style="position:absolute;left:0;right:0;top:120px;text-align:center;color:#fff;text-shadow:0 3px 24px rgba(90,30,10,.55)"><div style="font-weight:600;letter-spacing:18px;font-size:48px">PEACE ON THE GALLOPS</div>
<div class="serif" style="font-style:italic;font-size:170px;line-height:1;margin-top:16px">Merry Christmas</div></div>`,
'19-christmas-day-racecard': `<div style="position:absolute;inset:0;background:#1F5A3D"></div>
<div style="position:absolute;left:0;right:0;top:0;height:26px;background:${metal}"></div><div style="position:absolute;left:0;right:0;bottom:0;height:26px;background:${metal}"></div>
<div style="position:absolute;left:100px;right:100px;top:120px;color:#fff">
<div style="font-weight:600;letter-spacing:14px;font-size:44px;color:#F2CF5B">TODAY'S CARD · 25 DECEMBER</div>
<div style="font-weight:700;font-size:168px;line-height:.95;margin-top:16px">CHRISTMAS<br>DAY RUNNERS</div>
<div style="height:8px;background:${metal};margin:50px 0 30px"></div>
${[['7:00', 'The Early Riser Stakes', 'Kids up. No going back.'], ['10:30', 'The Wrapping Paper Chase', 'Soft, torn in places.'], ['1:15', 'The Turkey Handicap', 'Top weight: Dad\'s plate.'], ['3:00', 'The King\'s Speech Hurdle', 'Hold-up tactics on the sofa.'], ['4:30', 'The Sofa Sprint', 'Five furlongs to the good chair.'], ['8:00', 'The Leftovers Plate', 'Stayers only.']].map(r => `<div style="display:flex;gap:40px;align-items:baseline;padding:26px 0;border-bottom:3px solid rgba(242,207,91,.35)"><div style="font-weight:700;font-size:74px;color:#F2CF5B;width:210px">${r[0]}</div><div><div style="font-weight:700;font-size:72px;line-height:1.05">${r[1]}</div><div class="serif" style="font-style:italic;font-size:54px;color:#E0D6C9;margin-top:6px">${r[2]}</div></div></div>`).join('')}
<div class="serif" style="font-style:italic;font-size:84px;text-align:center;margin-top:60px;color:#F2CF5B">Merry Christmas</div></div>`,
'20-going-report': `<div style="position:absolute;inset:0;background:#EAE2D8"></div>
<div style="position:absolute;left:0;top:0;bottom:0;width:150px;background:#B3202A"></div>
<div style="position:absolute;left:230px;right:90px;top:170px;color:#1C1C1C">
<div style="font-weight:600;letter-spacing:14px;font-size:44px;color:#5E574F">CHRISTMAS GOING REPORT</div>
<div style="font-weight:700;font-size:270px;line-height:.9;margin-top:40px;color:#1F5A3D">GOING:</div>
<div style="font-weight:700;font-size:270px;line-height:.9;color:#B3202A">MERRY</div>
<div class="serif" style="font-style:italic;font-size:124px;margin-top:40px">(mulled in places)</div>
<div style="height:8px;background:#1C1C1C;margin:90px 0 50px;width:300px"></div>
<div style="font-weight:600;font-size:70px;line-height:1.4">Stalls: by the fridge.<br>Rail: moved for the tree.<br>Watering: yes, please.</div>
<div class="serif" style="font-style:italic;font-size:100px;margin-top:90px;color:#1F5A3D">Merry Christmas</div></div>`,
});
(async () => { const b = await chromium.launch();
  for (const [n, body] of Object.entries(cards)) { const p = await b.newPage({ viewport: { width: 1500, height: 2100 } });
    await p.setContent(`<html><head><style>${base}</style></head><body>${body}</body></html>`); await p.waitForTimeout(300);
    await p.screenshot({ path: path.join(__dirname, `ZANS-christmas-card-${n}-DRAFT.png`) }); await p.close(); console.log(n); }
  await b.close(); })();
