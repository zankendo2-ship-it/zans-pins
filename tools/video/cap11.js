const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const setCol = (p,id,v)=>p.evaluate(([id,v])=>{const e=document.getElementById(id); e.value=v; e.dispatchEvent(new Event('input',{bubbles:true})); e.dispatchEvent(new Event('change',{bubbles:true}));},[id,v]);
  const jobs = [
    ['art-ombudsman.png', async p=>{ await p.locator('button',{hasText:'Royal blue, white cap'}).first().click(); await p.fill('#name','Ombudsman'); }],
    ['art-lossiemouth.png', async p=>{ await p.locator('button',{hasText:/^Large spots$/}).first().click(); await p.waitForTimeout(300);
        await setCol(p,'pick1','#F3B5C9'); await setCol(p,'pick2','#6CC24A'); await setCol(p,'capcol','#F3B5C9'); await p.fill('#name','Lossiemouth'); }],
  ];
  for (const [f,setup] of jobs) {
    const p = await b.newPage({ viewport:{width:430,height:900}, deviceScaleFactor:5 });
    await p.goto('https://www.zanshorseracing.co.uk/bauble-designer/',{waitUntil:'networkidle'});
    await setup(p); await p.waitForTimeout(700);
    await p.evaluate(()=>{ const s=document.querySelector('svg');
      document.querySelectorAll('svg.hang').forEach(e=>e.style.display='none');
      for(let e=s.parentElement;e;e=e.parentElement){e.style.background='transparent';e.style.backgroundImage='none';e.style.boxShadow='none';e.style.border='0';}
      s.style.filter='none'; document.querySelectorAll('body *').forEach(k=>{ if(!(k.contains(s)||s.contains(k)||k===s)) k.style.visibility='hidden'; });
      const st=document.createElement('style'); st.textContent='*::before,*::after{display:none!important}'; document.head.appendChild(st); });
    await p.locator('svg').first().screenshot({path:'assets/'+f, omitBackground:true});
    await p.close();
  }
  await b.close();
})();
