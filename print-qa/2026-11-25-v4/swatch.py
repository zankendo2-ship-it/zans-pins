import re, json
from PIL import Image, ImageDraw, ImageFont
pairs=[('Loussiemoo','orig-loussiemoo.svg','out/loussiemoo-v4A.svg','out/loussiemoo-v4B.svg'),
 ('Zoo Olympios','orig-zoo-olympios.svg','out/zoo-olympios-v4A.svg','out/zoo-olympios-v4B.svg'),
 ('Rexs Romance','orig-rexs-romance.svg','out/rexs-romance-v4A.svg','out/rexs-romance-v4B.svg'),
 ('FACT TO FILE mug (Harrier)','orig-mug-2475.svg','out/fact-to-file-mug-2475x1155-v4.svg',None),
 ('FACT TO FILE mug (white)','orig-mug-2582.svg','out/fact-to-file-mug-2582x1120-v4.svg',None)]
def cols(f):
    s=open(f).read()
    return sorted({c.upper() for c in re.findall(r'(?:fill|stroke|stop-color)\s*[=:]\s*"?\s*(#[0-9A-Fa-f]{6})',s)})
def texts(f):
    s=open(f).read()
    t=[re.sub('<[^>]+>','',x).strip() for x in re.findall(r'<text[^>]*>(.*?)</text>',s,re.S)]
    t+= re.findall(r'data-text="([^"]+)"',s)+re.findall(r'aria-label="([^"]+)"',s)
    return [x for x in t if x]
rows=[];md=['# v4 colour + spelling check (original v corrected)\n']
for name,o,a,b in pairs:
    co=cols(o); ca=cols(a); cb=cols(b) if b else []
    md.append(f'## {name}\n')
    md.append(f'- original colours: {" ".join(co)}')
    md.append(f'- corrected A colours: {" ".join(ca)}  (added: {" ".join(sorted(set(ca)-set(co))) or "none"}; removed: {" ".join(sorted(set(co)-set(ca))) or "none"})')
    if b: md.append(f'- corrected B colours: {" ".join(cb)}  (added: {" ".join(sorted(set(cb)-set(co))) or "none"}; removed: {" ".join(sorted(set(co)-set(cb))) or "none"})')
    md.append(f'- original text: {texts(o)}')
    md.append(f'- corrected text: {texts(a)}'+(f' / B {texts(b)}' if b else ''))
    md.append('')
    rows.append((name,co,ca,cb))
open('pack/v4 colour and spelling check.md','w').write('\n'.join(md))
print('\n'.join(md))
