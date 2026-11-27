import asyncio, os, shutil
from playwright.async_api import async_playwright
V='/mnt/project-files/bauble-style-mugs-v3'
S=V+'/scene-photos'
FD='/mnt/attach/project-files/ascot-advanced-pro/shared-build/guide/fonts'
OUT='/tmp/claude-0/shots/out'; os.makedirs(OUT,exist_ok=True)
names=['Loussiemoo','Zoo Olympios','Rexs Romance']
CSS=f"""
@font-face{{font-family:Jost;font-weight:600;src:url('file://{FD}/Jost-600-normal.woff2')}}
@font-face{{font-family:Jost;font-weight:700;src:url('file://{FD}/Jost-700-normal.woff2')}}
*{{box-sizing:border-box;margin:0}}
body{{width:2700px;height:2025px;background:#0C3726;font-family:Jost;position:relative;overflow:hidden;color:#fff}}
.strip{{position:absolute;left:0;width:2700px;height:96px;background:linear-gradient(180deg,#E8CF7A,#C4A042 50%,#9C7B26);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:52px;letter-spacing:.28em;color:#0C3726}}
.top{{top:0}}.bot{{bottom:0}}
.h{{position:absolute;left:0;width:2700px;text-align:center;font-weight:700;color:#F2CA47;line-height:1}}
.w{{color:#fff}}
.pill{{position:absolute;left:50%;transform:translateX(-50%);background:linear-gradient(180deg,#E8CF7A,#C4A042);color:#0C3726;font-weight:700;border-radius:80px;padding:18px 60px;font-size:68px;white-space:nowrap}}
.frame{{position:absolute;border:10px solid #C4A042;border-radius:10px;overflow:hidden;background:#000}}
.frame img{{width:100%;height:100%;object-fit:cover;display:block}}
"""
def page(body): return f"<html><head><style>{CSS}</style></head><body><div class='strip top'>ZANS RACING</div>{body}<div class='strip bot'>ZANS RACING</div></body></html>"
def ph(n): return f"{S}/{n} mug - in the listing scene.jpg"
pages={}
# 1 cover (content inside centre 4:5: x 540-2160)
pages['01 cover']=page(f"""
<div class='h' style='top:130px;font-size:150px'>FULLY CUSTOMISED</div>
<div class='h w' style='top:300px;font-size:76px'>YOUR SILKS ON YOUR MUG</div>
<div class='frame' style='left:845px;top:420px;width:1010px;height:1262px'><img src='file://{ph("Loussiemoo")}'></div>
<div class='pill' style='top:1722px'>11oz WRAPAROUND PRINT</div>""")
# 2 three examples
fr=''.join(f"<div class='frame' style='left:{150+i*820}px;top:400px;width:760px;height:1100px'><img src='file://{ph(n)}'></div>" for i,n in enumerate(names))
pages['02 three examples']=page(f"""
<div class='h' style='top:130px;font-size:130px'>ANY SILKS. ANY NAME.</div>
<div class='h w' style='top:290px;font-size:70px'>FULLY CUSTOMISED TO YOUR COLOURS</div>{fr}
<div class='pill' style='top:1640px'>ALL FULL WRAPAROUND</div>""")
# 4 specs
rows=[('CAPACITY','11 oz  (330 ml)'),('SIZE','8.2 cm wide  x  9.6 cm high'),('MATERIAL','White ceramic'),('HANDLE + INSIDE','One of 9 colours'),('PRINT','Full wraparound')]
tr=''.join(f"<div style='position:absolute;left:640px;width:1420px;top:{470+i*190}px;height:150px;border-bottom:4px solid #C4A042;display:flex;justify-content:space-between;align-items:center;font-size:62px'><span style='color:#F2CA47;font-weight:700;letter-spacing:.05em'>{a}</span><span style='font-weight:600'>{b}</span></div>" for i,(a,b) in enumerate(rows))
pages['03 specs']=page(f"""<div class='h' style='top:130px;font-size:140px'>MUG DETAILS</div>
<div class='h w' style='top:300px;font-size:70px'>FULLY CUSTOMISED 11oz MUG</div>{tr}""")
open('pages.py','w').write('')
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome',args=['--no-sandbox']); pg=await b.new_page(viewport={'width':2700,'height':2025})
        for k,h in pages.items():
            open(f'{OUT}/{k}.html','w').write(h)
            await pg.goto(f'file://{OUT}/{k}.html'); await pg.wait_for_timeout(500)
            await pg.screenshot(path=f'{OUT}/ZANS silks mug - Etsy photo {k}.png')
        await b.close()
asyncio.run(main())
