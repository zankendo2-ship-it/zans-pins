// Capture bauble artwork from the website designer. Edit the jobs list: file, style (0 snow, 1 starry night), pattern, colour 1, colour 2, cap, name, expected design code.
// Usage: node templates/cap_baubles.js <out_dir>
const { chromium } = require('playwright');
const jobs=[
 ['art-gw.png',0,'Spots','#F3B5C9','#6CC24A','#F3B5C9','Gaelic Warrior','ZBA-spots-F3B5C9-6CC24A-plain-F3B5C9'],
 ['art-ftf.png',0,'Hoops','#0E8A4B','#F2C40F','#FFFFFF','Fact To File','ZBA-hoops-0E8A4B-F2C40F-plain-FFFFFF'],
 ['art-gd.png',0,'Plain','#D0202E','#1C1C1C','#D0202E','Grey Dawning','ZBA-plain-D0202E-1C1C1C-plain-D0202E'],
 ['art-ito.png',0,'Hoops','#0E8A4B','#F2C40F','#FFFFFF','Inothewayurthinkin','ZBA-hoops-0E8A4B-F2C40F-plain-FFFFFF'],
];
(async()=>{const b=await chromium.launch();
const setCol=(p,id,v)=>p.evaluate(([id,v])=>{const e=document.getElementById(id);e.value=v.toLowerCase();e.dispatchEvent(new Event('input',{bubbles:true}));e.dispatchEvent(new Event('change',{bubbles:true}));},[id,v]);
for(const [f,g,pat,c1,c2,cap,name,exp] of jobs){
 const p=await b.newPage({viewport:{width:430,height:900},deviceScaleFactor:5});
 await p.goto('https://www.zanshorseracing.co.uk/bauble-designer/',{waitUntil:'networkidle'});
 await p.locator('button',{hasText:g?'STARRY NIGHT':'SNOW'}).first().click();await p.waitForTimeout(300);
 await p.locator('button',{hasText:new RegExp('^'+pat+'$')}).first().click();await p.waitForTimeout(200);
 await setCol(p,'pick1',c1);await setCol(p,'pick2',c2);await setCol(p,'capcol',cap);await p.fill('#name',name);await p.waitForTimeout(700);
 const codes=await p.evaluate(()=>[...new Set(document.body.innerText.match(/ZB[AB]-[\w-]+/g)||[])]);
 await p.evaluate(()=>{const s=document.querySelector('svg');document.querySelectorAll('svg.hang').forEach(e=>e.style.display='none');
  for(let e=s.parentElement;e;e=e.parentElement){e.style.background='transparent';e.style.backgroundImage='none';e.style.boxShadow='none';e.style.border='0';}
  s.style.filter='none';document.querySelectorAll('body *').forEach(k=>{if(!(k.contains(s)||s.contains(k)||k===s))k.style.visibility='hidden';});
  const st=document.createElement('style');st.textContent='*::before,*::after{display:none!important}';document.head.appendChild(st);});
 await p.locator('svg').first().screenshot({path:process.argv[2]+'/'+f,omitBackground:true});
 console.log(f,codes.includes(exp)?'MATCH':'MISMATCH',codes.join(' '));await p.close();}
await b.close();})();
