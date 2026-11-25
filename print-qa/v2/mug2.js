const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('http://127.0.0.1:8765/mug-designer/');await p.waitForTimeout(1500);
const res=await p.evaluate(()=>{
 const d=ZANS.normalise({layout:'B',body:'hoops',c1:'#00843D',c2:'#F5D130',sleeves:'plain',cap:'contrast',k1:'#C8102E',k2:'#C8102E',name:'FACT TO FILE'});
 d.handlePick='Black'; d.ring=true; d.name='FACT TO FILE';
 const L=JSON.parse(JSON.stringify(MUG.logo));
 for(const k of Object.keys(MUG.logo)){MUG.logo[k].w_px=760;MUG.logo[k].h_px=84;}
 const spec=Object.assign({},MUG,{width_px:2475,height_px:1155});
 let svg=ZANS.printFile(d,spec,'Jost',LOGO); MUG.logo=L; return {svg,font:FONT};});
let svg=res.svg;
// 1. white line under the cap band at least 1.5 mm (24 px of 1155)
svg=svg.replace(/(<rect x="0" y="\d+(?:\.\d+)?" width="2475" height=")(\d+)(")/g,(m,a,h,c)=>a+Math.max(+h,24)+c);
// 2. bitmap logo -> vector text (no embedded raster)
const im=svg.match(/<image[^>]*>(<\/image>)?/g)||[]; console.log('images',im.length);
svg=svg.replace(/<image[^>]*?x="([\d.]+)"[^>]*?y="([\d.]+)"[^>]*?width="([\d.]+)"[^>]*?height="([\d.]+)"[^>]*?\/?>(<\/image>)?/g,(m,x,y,w,h)=>{const cx=+x+ +w/2, cy=+y+ +h/2;
 return `<text x="${cx}" y="${(cy+21).toFixed(1)}" text-anchor="middle" font-family="Jost" font-weight="700" font-size="58" letter-spacing="2" fill="#1C1C1C">ZANS RACING TOOLS</text>`;});
// 2b. logo strip centred on the wrap (it sat at x=1350, the centre of the old 2700 px canvas = 9.5 mm right of centre)
svg=svg.replace(/<rect x="958\.2" y="([\d.]+)" width="783\.5"/,(m,y)=>`<rect x="${(2475/2-783.5/2).toFixed(1)}" y="${y}" width="783.5"`).replace('<text x="1350" y="962.0"',`<text x="${2475/2}" y="962.0"`);
// 3. no semi-transparency
svg=svg.replace(/ opacity="0?\.\d+"/g,'').replace(/ fill-opacity="0?\.\d+"/g,'');
console.log('left images',(svg.match(/<image/g)||[]).length,'opacity',(svg.match(/opacity/g)||[]).length);
const fontcss='@font-face{font-family:Jost;font-weight:600 700;src:url(data:font/woff2;base64,'+res.font+')}';
fs.writeFileSync('mug-FACT-TO-FILE-master.svg',svg.replace('>',`><defs><style>${fontcss}</style></defs>`));
const q=await b.newPage({viewport:{width:2475,height:1155},deviceScaleFactor:1});
await q.setContent('<html><head><style>'+fontcss+'body{margin:0}</style></head><body>'+svg+'</body></html>');
await q.waitForTimeout(1000);await q.screenshot({path:'mug-raw.png'});await b.close();})();
