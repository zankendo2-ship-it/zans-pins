"""Small Google/Bing fixes for the live site (run on a checkout of the live branch).

1. Footer: add 'Silks bauble designer' after 'Silks mug designer' on every public page
   that has the footer link row but not the bauble link (the home page already has it).
2. Mug designer: add the bauble designer to its 'Gifts for racehorse owners and
   syndicates' link line.
3. Sitemap: lastmod = the day each page last changed (git, or today when this script
   changed it), and the bauble share photo as the bauble page's image.

(IndexNow for Bing already runs on its own: .github/workflows/indexnow.yml sends every
sitemap URL whenever docs/sitemap.xml changes, with the key file docs/ebca91f5....txt.)

Usage: python3 bauble_links_sitemap.py <live checkout>
Prints what it changed. Safe to run twice.
"""
import datetime as dt
import os
import re
import subprocess
import sys

root = sys.argv[1]
docs = os.path.join(root, 'docs')
today = dt.date.today().isoformat()
changed = set()

MUG = '<a href="/mug-designer/">Silks mug designer</a>'
BAUBLE = '<a href="/bauble-designer/">Silks bauble designer</a>'


def page_files():
    for dirpath, _, files in os.walk(docs):
        if 'index.html' in files:
            yield os.path.join(dirpath, 'index.html')


for path in page_files():
    rel = os.path.relpath(path, root)
    html = open(path, encoding='utf-8').read()
    if 'noindex' in html[:5000]:
        continue
    new = html
    m = re.search(r'<p class="flinks">.*?</p>', new, re.S)
    if m and 'href="/bauble-designer/"' not in m.group(0) and MUG in m.group(0):
        row = m.group(0).replace(MUG, MUG + ' · ' + BAUBLE, 1)
        new = new[:m.start()] + row + new[m.end():]
    if rel == os.path.join('docs', 'mug-designer', 'index.html'):
        link = ('<a style="color:var(--ink);text-decoration:underline" href="/horse-racing-gifts/">'
                'All horse racing gifts</a>')
        add = (' · <a style="color:var(--ink);text-decoration:underline" href="/bauble-designer/">'
               'Silks Christmas bauble designer</a>')
        if link in new and 'href="/bauble-designer/"' not in new:
            new = new.replace(link, link + add, 1)
    if new != html:
        open(path, 'w', encoding='utf-8').write(new)
        changed.add(rel)
        print('links  ', rel)

def last_change(rel):
    dirty = subprocess.run(['git', '-C', root, 'diff', '--quiet', 'HEAD', '--', rel]).returncode != 0
    if rel in changed or dirty:
        return today
    out = subprocess.run(['git', '-C', root, 'log', '-1', '--format=%cs', '--', rel],
                         capture_output=True, text=True).stdout.strip()
    return out or today


sm_path = os.path.join(docs, 'sitemap.xml')
sm = open(sm_path, encoding='utf-8').read()
new_sm = sm
for loc in re.findall(r'<loc>(https://www\.zanshorseracing\.co\.uk/[^<]*)</loc>', sm):
    if '/img/' in loc:
        continue
    page = loc.replace('https://www.zanshorseracing.co.uk/', '')
    rel = os.path.join('docs', page, 'index.html') if page else os.path.join('docs', 'index.html')
    if not os.path.exists(os.path.join(root, rel)):
        print('MISSING page for', loc)
        continue
    want = last_change(rel)
    pat = re.compile(r'(<url><loc>' + re.escape(loc) + r'</loc><lastmod>)([0-9-]+)(</lastmod>)')
    mm = pat.search(new_sm)
    if mm and mm.group(2) != want:
        new_sm = new_sm[:mm.start(2)] + want + new_sm[mm.end(2):]
        print('lastmod', loc, mm.group(2), '->', want)
img = 'https://www.zanshorseracing.co.uk/img/zans-bauble-share.jpg'
bpat = re.compile(r'(<url><loc>https://www\.zanshorseracing\.co\.uk/bauble-designer/</loc>.*?)(</url>)', re.S)
bm = bpat.search(new_sm)
if bm and '<image:image>' not in bm.group(1) and os.path.exists(os.path.join(docs, 'img', 'zans-bauble-share.jpg')):
    new_sm = new_sm[:bm.end(1)] + f'<image:image><image:loc>{img}</image:loc></image:image>' + new_sm[bm.end(1):]
    print('image   bauble-designer ->', img)
if new_sm != sm:
    open(sm_path, 'w', encoding='utf-8').write(new_sm)
