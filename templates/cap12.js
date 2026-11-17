const { chromium } = require('playwright');
const jobs=[ // file, style(green?), pattern button, c1, c2, cap, name, expected code
 ['art-nodrama.png',0,'Hoops','#FFFFFF','#1B2A5C','#C8102E','No Drama This End','ZBA-hoops-FFFFFF-1B2A5C-plain-C8102E'],
 ['art-jonbon.png',0,'Hoops','#0E6B3B','#F5D130','#FFFFFF','Jon Bon','ZBA-hoops-0E6B3B-F5D130-plain-FFFFFF'],
 ['art-billy.png',0,'Three big spots','#F5D130','#1C1C1C','#1C1C1C','Billy','ZBA-spot_diag-F5D130-1C1C1C-plain-1C1C1C'],
 ['art-conny-green.png',1,'Plain','#FFFFFF','#1C1C1C','#000000','Constitution Hill','ZBB-plain-FFFFFF-1C1C1C-plain-000000'],
 ['art-conny-white.png',0,'Plain','#FFFFFF','#1C1C1C','#000000','Constitution Hill','ZBA-plain-FFFFFF-1C1C1C-plain-000000'],
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
