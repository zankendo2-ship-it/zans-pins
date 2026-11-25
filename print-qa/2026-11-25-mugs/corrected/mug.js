const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('http://127.0.0.1:8765/mug-designer/');await p.waitForTimeout(1500);
for (const fixed of [false,true]){
const res=await p.evaluate(([fixed])=>{
 const d=ZANS.normalise({layout:'B',body:'hoops',c1:'#00843D',c2:'#F5D130',sleeves:'plain',cap:'contrast',k1:'#C8102E',k2:'#C8102E',name:'FACT TO FILE'});
 d.handlePick='Black'; d.ring=true; d.name='FACT TO FILE';
 const L=JSON.parse(JSON.stringify(MUG.logo));
 if(fixed){ for(const k of Object.keys(MUG.logo)){MUG.logo[k].w_px=560;MUG.logo[k].h_px=75;MUG.logo[k].y_px=930;} }
 const spec=Object.assign({},MUG,{width_px:2475,height_px:1155});
 let svg=ZANS.printFile(d,spec,'Jost',LOGO);
 MUG.logo=L;
 if(fixed){ // white line under the cap ring: at least 1.5 mm (about 24 px of 1155) 
   svg=svg.replace(/(<rect x="0" y="\d+(?:\.\d+)?" width="2475" height=")(\d+)(")/g,(m,a,h,c)=>a+Math.max(+h,24)+c); }
 return {svg,font:FONT,d:ZANS.toCode(d)};},[fixed]);
const q=await b.newPage({viewport:{width:2475,height:1155},deviceScaleFactor:2});
await q.setContent('<html><head><style>@font-face{font-family:Jost;font-weight:600 700;src:url(data:font/woff2;base64,'+res.font+')}body{margin:0}</style></head><body>'+res.svg+'</body></html>');
await q.waitForTimeout(1000);await q.screenshot({path:`mug-${fixed?'fixed':'now2x'}.png`});console.log(res.d);}
await b.close();})();
