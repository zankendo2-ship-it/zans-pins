// v3 bauble print design (25 Nov, after ChatGPT REVISE 7169706069/7169718295):
// exact design colours (no deepening), approved panel width 760, panel centred on R, name >= 6 mm letters,
// MERRY CHRISTMAS >= 3.5 mm letters, no thin edge ring, no opacity, strokes >= 20 px (1.5 mm),
// traced vector horse logo (pending Alex approval) instead of the bitmap, full-square bleed master.
function hex2rgb(h){const n=parseInt(h.slice(1),16);return [n>>16,(n>>8)&255,n&255];}
function rl(h){return hex2rgb(h).map(v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)}).reduce((a,v,i)=>a+v*[.2126,.7152,.0722][i],0);}
function contrast(a,b){const x=rl(a),y=rl(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05);}
// lettering colour: the design's own darker colour (what the live designer uses) when it reads at >= 4.5:1 on cream,
// otherwise ZANS brand ink. Never an invented shade. __INKMODE='brand' forces brand ink.
function inkFor(d){const c=Z.darkOf(d); if(window.__INKMODE==='brand') return '#1C1C1C'; return contrast(c,CREAM)>=4.5?c:'#1C1C1C';}
function horseMark(cx,cy,hgt){const s=hgt/895, w=850*s, pad=14, tw=w+2*pad, th=hgt+2*pad;
  return `<g data-safe="1" data-centre="x" data-label="ZANS horse logo"><rect x="${f1(cx-tw/2)}" y="${f1(cy-th/2)}" width="${f1(tw)}" height="${f1(th)}" rx="16" fill="${CREAM}" stroke="${GOLD}" stroke-width="20"/>`+
  `<g transform="translate(${f1(cx-w/2)},${f1(cy-hgt/2)}) scale(${s.toFixed(5)})"><path d="${window.__HORSE[0]}" fill="#1C1C1C"/></g></g>`;}
designA = function(d,id){
  const pat=Z.fillPattern(d.allover,d.c1,d.c2,0,0,W,W,scaleFor(d.allover));
  const n=fit(d.name,640,240,170,0.02), ink=inkFor(d); const fs=n.fs;
  const h=n.lines.length*fs*1.0+66+95, y=R-h/2;
  let t=`<rect data-safe="1" data-centre="x" data-label="name panel" x="${R-380}" y="${f1(y)}" width="760" height="${f1(h)}" rx="${f1(Math.min(90,h/2))}" fill="${CREAM}" stroke="${GOLD}" stroke-width="20"/>`;
  n.lines.forEach((l,i)=>{t+=`<text data-role="name" data-inside="name panel" x="${R}" y="${f1(y+28+fs*0.78+i*fs*1.0)}" text-anchor="middle" font-family="Jost" font-weight="700" font-size="${f1(fs)}" letter-spacing="${f1(fs*0.02)}" fill="${ink}">${esc(l)}</text>`;});
  t+=`<text data-centre="x" data-inside="name panel" x="${R}" y="${f1(y+h-40)}" text-anchor="middle" font-family="Jost" font-weight="700" font-size="66" letter-spacing="1.3" fill="${ink}">MERRY CHRISTMAS</text>`;
  return svgWrap(id,pat+capTop(d.capCol)+t+horseMark(R,y+h+20+89,150));
};
const __capTop=capTop;
capTop=function(c){return __capTop(c).replace(/ opacity="0?\.\d+"/g,'').replace(/stroke-width="(\d+(?:\.\d+)?)"/g,(m,w)=>`stroke-width="${Math.max(+w,20)}"`);};
window.__ink=inkFor;
window.__master=function(){return printSVG(design(),'m').replace(' clip-path="url(#mc)"','').replace(/ clip-path="url\(#[\w]+c\)"/,'');};
