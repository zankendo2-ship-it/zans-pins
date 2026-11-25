const {chromium}=require('playwright');const fs=require('fs');
const items=[['loussiemoo','disc','#F3B5C9','#6CC24A','#F3B5C9','Loussiemoo'],['zoo-olympios','spot_diag','#F5D130','#1C1C1C','#1C1C1C','Zoo Olympios'],['rexs-romance','plain','#1C4FA0','#FFFFFF','#FFFFFF','Rexs Romance']];
function deepen(h){let [r,g,b]=[1,3,5].map(i=>parseInt(h.substr(i,2),16)/255);const mx=Math.max(r,g,b),mn=Math.min(r,g,b);let l=(mx+mn)/2,s=0,hh=0;const dd=mx-mn;
 if(dd){s=l>.5?dd/(2-mx-mn):dd/(mx+mn);hh=mx==r?((g-b)/dd+(g<b?6:0)):mx==g?((b-r)/dd+2):((r-g)/dd+4);hh/=6;}
 if(s<0.05||l<0.35||l>0.97) return h; // leave black, white, greys and already-deep colours
 l=Math.max(0.35,l-0.12); s=Math.min(1,s+0.2);
 const q=l<.5?l*(1+s):l+s-l*s,p=2*l-q,f=t=>{t=(t+1)%1;return t<1/6?p+(q-p)*6*t:t<.5?q:t<2/3?p+(q-p)*(2/3-t)*6:p};
 return '#'+[hh+1/3,hh,hh-1/3].map(t=>Math.round(f(t)*255).toString(16).padStart(2,'0')).join('').toUpperCase();}
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('http://127.0.0.1:8765/bauble-designer/');await p.waitForTimeout(1500);
await p.addScriptTag({content:fs.readFileSync('fixA.js','utf8')});
for(const ver of ['A','B']) for(const [ref,pat,c1,c2,cap,name] of items){
 const C=ver==='A'?[c1,c2,cap]:[c1,c2,cap].map(deepen);
 const r=await p.evaluate(async([pat,c1,c2,cap,name])=>{Object.assign(S,{style:'A',pat,body:pat,c1,c2,capCol:cap,name,sleeves:'plain'});const u=await ZANSBauble.printFile(1);const svg=printSVG(design(),'m');return {u,svg,ink:__ink(design())};},[pat,...C,name]);
 fs.writeFileSync(`master-${ref}-${ver==='A'?'approved-colours':'deeper-colours'}.svg`,r.svg);fs.writeFileSync(`fixed-${ref}-${ver==='A'?'approved-colours':'deeper-colours'}.png`,Buffer.from(r.u.split(',')[1],'base64'));console.log(ref,ver,C.join(' '),'ink',r.ink);}
await b.close();})();
