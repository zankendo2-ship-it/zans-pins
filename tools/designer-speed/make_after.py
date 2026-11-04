"""Build the faster mug designer page from the live one (nothing visible changes).

1. The Tailwind Play CDN script (compiles CSS on the visitor's phone) -> the same rules prebuilt with
   Tailwind CLI 3.4.17 (tw.min.css, built from this page's own classes), inlined where the CDN put its CSS.
2. three.min.js no longer holds up or slows the first paint: it is fetched and run just after the page's first paint,
   then the 3D preview starts.
3. The 3D mug redraws only while something changes (drag, turn, new design) instead of every frame forever.

Usage: python3 make_after.py <live index.html> <out.html> [A|B]
  A = prebuilt CSS where the CDN script was (default), B = at the end of <head>.
"""
import sys

src, out = sys.argv[1], sys.argv[2]
pos = sys.argv[3] if len(sys.argv) > 3 else "A"
s = open(src, encoding="utf-8").read()
css = open(__file__.rsplit("/", 1)[0] + "/tw.min.css", encoding="utf-8").read().strip()
tw = '<style id="zans-tw">' + css + "</style>"


def sub(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, (old[:60], n)
    s = s.replace(old, new)


cdn = '<script src="https://cdn.tailwindcss.com/3.4.17"></script>\n'
if pos == "A":
    sub(cdn, tw + "\n")
else:
    sub(cdn, "")
    note = ('<!-- Tailwind CSS is built into this page (no CDN). New Tailwind classes need a rebuild: '
            'python3 tools/designer-speed/swap_css.py docs/mug-designer/index.html (the designer-css workflow runs it after every push). -->\n')
    sub('</style>\n\n<div class="strip"></div>\n<div class="wrap">', '</style>\n' + note + tw + '\n\n<div class="strip"></div>\n<div class="wrap">')

# 2. three.js: fetched and run just after the page's first paint (no download competing with the page itself)
sub('<script src="three.min.js"></script>\n', '')
sub("init3D(); render(); priceUI(); target=faceAngle();",
    "render(); priceUI();\n"
    "function start3D(){ init3D(); render(); target=faceAngle(); wake(); }\n"
    "// The 3D library (three.min.js) is fetched and run just after the page's first paint, so it never holds up or\n"
    "// slows the first view. If it fails to load, init3D shows the flat-print message.\n"
    "function afterPaint(f){ requestAnimationFrame(()=>setTimeout(f,0)); }\n"
    "function load3D(){ const s=document.createElement('script'); s.src='three.min.js'; s.onload=s.onerror=()=>start3D(); document.head.appendChild(s); }\n"
    "if (document.readyState==='loading') document.addEventListener('DOMContentLoaded', ()=>afterPaint(load3D)); else afterPaint(load3D);")

# 3. draw on demand
sub("function loop(){ if(target!==null){ rotY+=(target-rotY)*0.08; if(Math.abs(target-rotY)<0.002) target=null; }\n"
    "  group.rotation.y=rotY; renderer.render(scene,camera); requestAnimationFrame(loop); }",
    "// Draw only while something is changing (saves phone battery). Anything that changes the mug calls wake().\n"
    "let raf=0, still=0;\n"
    "function wake(){ still=0; if(!raf && renderer && group) raf=requestAnimationFrame(loop); }\n"
    "// One drawing chain only: a direct call cancels any frame already booked (two chains = every frame drawn twice).\n"
    "function loop(){ cancelAnimationFrame(raf); raf=0; if(target!==null){ rotY+=(target-rotY)*0.08; if(Math.abs(target-rotY)<0.002) target=null; }\n"
    "  group.rotation.y=rotY; renderer.render(scene,camera);\n"
    "  if(target!==null || dragging || ++still<3) raf=requestAnimationFrame(loop); }")
sub("el.addEventListener('pointerdown',e=>{dragging=true;lastX=e.clientX;target=null;el.setPointerCapture(e.pointerId);});",
    "el.addEventListener('pointerdown',e=>{dragging=true;lastX=e.clientX;target=null;el.setPointerCapture(e.pointerId);wake();});")
sub("el.addEventListener('pointermove',e=>{if(!dragging)return; rotY+=(e.clientX-lastX)*0.012; lastX=e.clientX;});",
    "el.addEventListener('pointermove',e=>{if(!dragging)return; rotY+=(e.clientX-lastX)*0.012; lastX=e.clientX; wake();});")
sub("new ResizeObserver(size).observe(st); size(); loop();",
    "el.addEventListener('webglcontextrestored',wake);\n"
    "  ['pointerdown','keydown','input','change','click'].forEach(t=>document.addEventListener(t,wake,{capture:true,passive:true}));\n"
    "  new ResizeObserver(size).observe(st); size();")  # size() calls wake(), which books the first frame
sub("camera.aspect=w/h; camera.updateProjectionMatrix(); }",
    "camera.aspect=w/h; camera.updateProjectionMatrix(); wake(); }")
sub("tex.image=c; tex.needsUpdate=true; };", "tex.image=c; tex.needsUpdate=true; wake(); };")
sub("insideMat.color=hc; handleMat.color=hc; }\n  $('code').textContent=Z.toCode(d);",
    "insideMat.color=hc; handleMat.color=hc; wake(); }\n  $('code').textContent=Z.toCode(d);")
sub("target = rotY + (((faceAngle()-rotY)%(2*Math.PI))+3*Math.PI)%(2*Math.PI)-Math.PI; };",
    "target = rotY + (((faceAngle()-rotY)%(2*Math.PI))+3*Math.PI)%(2*Math.PI)-Math.PI; wake(); };")

open(out, "w", encoding="utf-8").write(s)
print("wrote", out, len(s), "chars, css position", pos)
