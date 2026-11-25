// Corrected bauble design A (25 Nov print fix): centred panel, no edge ring, bigger bold text, high-contrast ink.
function hex2rgb(h){const n=parseInt(h.slice(1),16);return [n>>16,(n>>8)&255,n&255];}
function rl(h){return hex2rgb(h).map(v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)}).reduce((a,v,i)=>a+v*[.2126,.7152,.0722][i],0);}
function contrast(a,b){const x=rl(a),y=rl(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05);}
function inkFor(d){let ink=Z.darkOf(d);let f=1;while(contrast(ink,CREAM)<7&&f>0.05){f-=0.05;ink=shade(Z.darkOf(d),f);}return ink;}
designA = function(d,id){
  const pat=Z.fillPattern(d.allover,d.c1,d.c2,0,0,W,W,scaleFor(d.allover));
  const n=fit(d.name,560,230,170,0.02), ink=inkFor(d);
  const h=Math.min(350,n.lines.length*n.fs*1.05+125), y=R-h/2;
  let t=`<rect x="${R-320}" y="${f1(y)}" width="640" height="${f1(h)}" rx="${f1(Math.min(80,h/2))}" fill="${CREAM}" stroke="${GOLD}" stroke-width="18"/>`;
  n.lines.forEach((l,i)=>{t+=`<text x="${R}" y="${f1(y+30+n.fs*0.86+i*n.fs*1.05)}" text-anchor="middle" font-family="Jost" font-weight="700" font-size="${f1(n.fs)}" letter-spacing="${f1(n.fs*0.02)}" fill="${ink}">${esc(l)}</text>`;});
  t+=`<text x="${R}" y="${f1(y+h-36)}" text-anchor="middle" font-family="Jost" font-weight="700" font-size="46" letter-spacing="5" fill="${ink}">MERRY CHRISTMAS</text>`;
  return svgWrap(id,pat+capTop(d.capCol)+t+logoTab(845,280));
};
window.__ink=inkFor;
