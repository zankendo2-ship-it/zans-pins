import asyncio
from playwright.async_api import async_playwright
S='/tmp/claude-0/sp'
FD='/mnt/attach/project-files/ascot-advanced-pro/shared-build/guide/fonts'
CSS=f"""@font-face{{font-family:Jost;font-weight:700;src:url('file://{FD}/Jost-700-normal.woff2')}}
*{{box-sizing:border-box;margin:0}}body{{width:1080px;height:1920px;background:#0C3726;font-family:Jost;font-weight:700;position:relative;overflow:hidden;color:#fff;text-align:center}}
.strip{{position:absolute;left:0;width:1080px;height:70px;background:linear-gradient(180deg,#E8CF7A,#C4A042 50%,#9C7B26);color:#0C3726;font-size:36px;letter-spacing:.28em;line-height:70px}}
.t{{top:0}}.b{{bottom:0}}.h{{position:absolute;left:60px;width:960px;color:#F2CA47;line-height:1.05}}.w{{color:#fff}}
.f{{position:absolute;left:60px;width:960px;border:8px solid #C4A042;overflow:hidden}}.f img{{width:100%;height:100%;object-fit:cover}}"""
def pg(b): return f"<html><head><style>{CSS}</style></head><body><div class='strip t'>ZANS RACING</div>{b}<div class='strip b'>ZANS RACING</div></body></html>"
im=lambda n:f"<div class='f' style='top:380px;height:1200px'><img src='file://{S}/{n} mug - in the listing scene.jpg'></div>"
sc={
'1 hook (0-3s)':f"<div class='h' style='top:140px;font-size:110px'>YOUR SILKS.<br>ON A MUG.</div>"+im('Lossiemoo')+"<div class='h w' style='top:1640px;font-size:70px'>FULLY CUSTOMISED</div>",
'2 examples (3-7s)':f"<div class='h' style='top:140px;font-size:100px'>ANY COLOURS.<br>ANY NAME.</div>"+im('Zoo Olympios')+"<div class='h w' style='top:1640px;font-size:70px'>YOUR DESIGN, YOUR MUG</div>",
'3 more (7-11s)':f"<div class='h' style='top:140px;font-size:100px'>MAKE IT<br>YOURS</div>"+im('Lossiemoo')+"<div class='h w' style='top:1640px;font-size:70px'>11oz FULL WRAPAROUND</div>",
'4 end card (11-15s)':"<div class='h' style='top:560px;font-size:104px'>AVAILABLE NOW</div><div class='h w' style='top:760px;font-size:68px'>at zanshorseracing.co.uk</div><div class='h w' style='top:930px;font-size:52px'>Also on Etsy: ZANS Racing</div>",
}
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux64/chrome',args=['--no-sandbox']);g=await b.new_page(viewport={'width':1080,'height':1920})
    for k,h in sc.items():
      open('/tmp/claude-0/shots/v.html','w').write(pg(h));await g.goto('file:///tmp/claude-0/shots/v.html');await g.wait_for_timeout(400)
      await g.screenshot(path=f'/tmp/claude-0/shots/out/ZANS silks mug - video scene {k}.png')
    await b.close()
asyncio.run(m())
