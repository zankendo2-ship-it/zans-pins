"""Apply the 4 Nov 2026 search + speed fixes to the ZANS website pages in docs/.

python tools/seo-fixes/apply_fixes.py        (safe to run twice: every step checks first)
Each step asserts it found exactly what it expected, so a page that has changed shape
fails loudly instead of being edited wrongly.
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from fonts_css import css as font_css, PRELOAD

DOCS = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', 'docs'))
SITE = 'https://www.zanshorseracing.co.uk'
HOME = ['index.html']
GIFT = ['horse-racing-gifts/index.html', 'gifts-for-racehorse-owners/index.html', 'racing-syndicate-gifts/index.html']
OLD = ['ascot-racecourse-guide/index.html', 'breeders-cup-guide/index.html', 'articles/ascot-draw-bias/index.html',
       'articles/breeders-cup-uk-times/index.html', 'articles/going-explained/index.html']
DESIGNER = ['mug-designer/index.html']
ALL_STATIC = HOME + GIFT + OLD

ICONS = ('<link rel="icon" href="/favicon.ico" sizes="48x48">'
         '<link rel="icon" href="/img/icon-192.png" type="image/png" sizes="192x192">'
         '<link rel="apple-touch-icon" href="/apple-touch-icon.png">')
SITE_NAME = 'ZANS Racing Tools &amp; Gifts'
EXTRA_CSS = ('picture{display:contents}'
             '.flinks{line-height:1.9}.flinks a{color:inherit;text-decoration:underline;text-underline-offset:2px}')
FONT_BLOCK = PRELOAD + '<style id="zans-fonts">' + font_css() + EXTRA_CSS + '</style>'

ORG = {
    "@type": "Organization", "@id": SITE + "/#organization",
    "name": "ZANS Racing Tools & Gifts", "alternateName": ["ZANS Racing", "ZANS Horse Racing"],
    "url": SITE + "/", "logo": SITE + "/img/zans-logo.png",
    "description": "Horse racing guides, tools and personalised racing gifts for UK and Irish racing fans.",
    "address": {"@type": "PostalAddress", "addressLocality": "Leicester", "addressCountry": "GB"},
    "sameAs": [
        "https://www.etsy.com/uk/shop/ZANSRacingTools",
        "https://www.pinterest.com/zanshorseracing/",
        "https://www.instagram.com/zanshorseracing/",
        "https://www.facebook.com/1334837319720038",
        "https://www.tiktok.com/@zansracingtools",
        "https://x.com/zansracing",
        "https://www.youtube.com/channel/UCqwYTr5QYgwcxPIc-dbaX_Q",
    ],
}
WEBSITE = {
    "@type": "WebSite", "@id": SITE + "/#website",
    "name": "ZANS Racing Tools & Gifts", "alternateName": ["ZANS Racing", "ZANS Horse Racing"],
    "url": SITE + "/", "inLanguage": "en-GB", "publisher": {"@id": SITE + "/#organization"},
}
FOOTER_LINKS = ('<p class="flinks"><a href="/horse-racing-gifts/">Horse racing gifts</a> · '
                '<a href="/mug-designer/">Silks mug designer</a> · '
                '<a href="/gifts-for-racehorse-owners/">Gifts for racehorse owners</a> · '
                '<a href="/racing-syndicate-gifts/">Racing syndicate gifts</a> · '
                '<a href="/ascot-racecourse-guide/">Ascot racecourse guide</a> · '
                '<a href="/articles/ascot-draw-bias/">Ascot draw bias</a> · '
                '<a href="/articles/going-explained/">The going explained</a> · '
                '<a href="/breeders-cup-guide/">Breeders&#39; Cup guide</a></p>')
ARTICLE_IMAGE = {
    'articles/ascot-draw-bias/index.html': '/img/ascot-flat-beginner.jpg',
    'articles/going-explained/index.html': '/img/ascot-flat-beginner.jpg',
    'articles/breeders-cup-uk-times/index.html': '/img/breeders-cup-beginner.jpg',
}
OG_IMAGE_FIX = {  # Ascot pages were sharing the Breeders' Cup picture
    'ascot-racecourse-guide/index.html': '/img/ascot-flat-beginner.jpg',
    'articles/ascot-draw-bias/index.html': '/img/ascot-flat-beginner.jpg',
    'articles/going-explained/index.html': '/img/ascot-flat-beginner.jpg',
}
TODAY = '2026-11-04'

log = []


def sub1(s, pat, rep, page, what, count=1, flags=0):
    new, n = re.subn(pat, rep, s, flags=flags)
    if n != count:
        raise SystemExit(f'{page}: {what}: expected {count} match(es), found {n}')
    log.append(f'{page}: {what}')
    return new


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + '</script>'


def fix_icons(s, p):
    if 'apple-touch-icon' in s:
        return s
    return sub1(s, r'<link rel="icon" href="[^"]*zans-logo\.png">', ICONS, p, 'square favicon set')


def fix_fonts(s, p):
    if 'id="zans-fonts"' in s:
        return s
    s = sub1(s, r'<link rel="preconnect" href="https://fonts\.googleapis\.com">\s*'
                r'(<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>\s*)?', '', p,
             'drop Google Fonts preconnects')
    s = sub1(s, r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?[^"]*">',
             lambda m: FONT_BLOCK, p, 'self-hosted fonts + fallback faces')
    for var, fam in (('display', 'Jost'), ('body', 'Source Sans 3'), ('mono', 'IBM Plex Mono')):
        s = sub1(s, rf"--{var}:'{re.escape(fam)}',", f"--{var}:'{fam}','{fam} Fallback',", p,
                 f'--{var} fallback face')
    return s


def fix_site_name(s, p):
    if 'og:site_name' in s:
        return s
    return sub1(s, r'(<meta property="og:url" content="[^"]*">)',
                lambda m: m.group(1) + f'<meta property="og:site_name" content="{SITE_NAME}">', p, 'og:site_name')


def fix_org(s, p, home=False):
    pat = r'<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "Organization".*?</script>'
    if '"@id": "' + SITE + '/#organization"' in s:
        return s
    obj = {"@context": "https://schema.org", "@graph": [ORG, WEBSITE]} if home else dict({"@context": "https://schema.org"}, **ORG)
    return sub1(s, pat, lambda m: ld(obj), p, 'Organization' + (' + WebSite (site name)' if home else '') + ' schema', flags=re.S)


def fix_article(s, p):
    m = re.search(r'<script type="application/ld\+json">(\{"@context": "https://schema\.org", "@type": "Article".*?)</script>', s, re.S)
    if not m:
        raise SystemExit(f'{p}: no Article schema')
    a = json.loads(m.group(1))
    if 'image' in a:
        return s
    a['image'] = SITE + ARTICLE_IMAGE[p]
    a['dateModified'] = TODAY
    a['author'] = {"@type": "Organization", "name": "ZANS Racing Tools & Gifts", "url": SITE + "/"}
    a['publisher'] = {"@id": SITE + "/#organization"}
    log.append(f'{p}: Article schema image/dateModified/publisher')
    return s.replace(m.group(0), ld(a))


def fix_old_page(s, p):
    if 'id="tonight"' in s:
        s = sub1(s, r'<div class="tonight" id="tonight">.*?</script>', '', p,
                 'remove expired Breeders\' Cup "starts TONIGHT" banner', flags=re.S)
    if '<nav><a href="/horse-racing-gifts/">' not in s:
        s = sub1(s, r'<nav><a href="/#breeders-cup">',
                 '<nav><a href="/horse-racing-gifts/">Gifts</a><a href="/mug-designer/">Silks mugs</a><a href="/#breeders-cup">',
                 p, 'nav: add Gifts + Silks mugs (same as home page)')
    if p in OG_IMAGE_FIX:
        s = sub1(s, r'<meta property="og:image" content="[^"]*breeders-cup-beginner\.jpg">',
                 f'<meta property="og:image" content="{SITE}{OG_IMAGE_FIX[p]}">', p, 'share image: Ascot, not Breeders\' Cup')
    return s


def fix_footer(s, p):
    if 'class="flinks"' in s:
        return s
    return sub1(s, r'<footer><div class="in">', '<footer><div class="in">' + FOOTER_LINKS, p, 'footer links to every main page')


def fix_header_logo(s, p):
    return sub1(s, r'(<img src=")/?img/zans-logo\.png(")', r'\1/img/zans-logo-180.jpg\2', p, 'header logo 111 KB -> 8 KB') \
        if re.search(r'<img src="/?img/zans-logo\.png"', s) else s


def picture(tag, sources, sizes):
    srcset = ', '.join(f'/img/{f} {w}w' for f, w in sources)
    return f'<picture><source type="image/webp" srcset="{srcset}" sizes="{sizes}">{tag}</picture>'


def fix_images(s, p):
    if '<picture>' in s:
        return s
    def wrap(pattern, sources, sizes, what, edit=None, count=None):
        nonlocal s
        found = re.findall(pattern, s)
        if count is not None and len(found) != count:
            raise SystemExit(f'{p}: {what}: expected {count}, found {len(found)}')
        for tag in found:
            new = tag
            new = re.sub(r'src="img/', 'src="/img/', new)
            if edit:
                new = edit(new)
            s = s.replace(tag, picture(new, sources, sizes), 1)
            log.append(f'{p}: {what}')
    hero_sizes_home = '(max-width: 592px) calc(100vw - 32px), 560px'
    hero_sizes_gift = '(max-width: 900px) calc(100vw - 32px), 500px'
    hero_src = [('silks-mugs-hero-600.webp', 600), ('silks-mugs-hero-940.webp', 940)]
    if p == 'index.html':
        wrap(r'<img src="img/silks-mugs-hero\.jpg"[^>]*>', hero_src, hero_sizes_home,
             'mug photo: WebP 97 KB (was 247 KB), loads first (it is the main picture)',
             edit=lambda t: t.replace(' loading="lazy"', ' fetchpriority="high"'), count=1)
    if p in ('horse-racing-gifts/index.html', 'gifts-for-racehorse-owners/index.html'):
        wrap(r'<img src="/img/silks-mugs-hero\.jpg"[^>]*>', hero_src, hero_sizes_gift, 'mug photo: WebP 97 KB (was 247 KB)', count=1)
    trio_src = [('silks-mugs-trio-800.webp', 800), ('silks-mugs-trio-1553.webp', 1553)]
    trio_jpg = lambda t: t.replace('/img/silks-mugs-trio.png', '/img/silks-mugs-trio-1553.jpg')
    if p == 'horse-racing-gifts/index.html':
        wrap(r'<img src="/img/silks-mugs-trio\.png"[^>]*>', trio_src, '(max-width: 1060px) calc(100vw - 32px), 1028px',
             'three mugs photo: WebP 49 KB (was 920 KB PNG)', edit=trio_jpg, count=1)
    if p == 'racing-syndicate-gifts/index.html':
        wrap(r'<img src="/img/silks-mugs-trio\.png"[^>]*>', trio_src, hero_sizes_gift,
             'three mugs photo: WebP 49 KB (was 920 KB PNG)', edit=trio_jpg, count=1)
    cover_sizes = '(max-width: 700px) calc(100vw - 32px), 360px'
    first = {'ascot-racecourse-guide/index.html': 'ascot-flat-beginner', 'breeders-cup-guide/index.html': 'breeders-cup-beginner'}
    for name in ('ascot-flat-beginner', 'ascot-flat-advanced', 'ascot-flat-pro',
                 'breeders-cup-beginner', 'breeders-cup-advanced', 'breeders-cup-pro'):
        edit = None
        if first.get(p) == name:  # top of the page: do not lazy-load the main picture
            edit = lambda t: t.replace(' loading="lazy"', ' fetchpriority="high"')
        wrap(rf'<img src="/?img/{name}\.jpg"[^>]*>', [(f'{name}-600.webp', 600), (f'{name}-1000.webp', 1000)],
             cover_sizes, f'{name} cover: WebP', edit=edit)
    if p == 'breeders-cup-guide/index.html':
        wrap(r'<img class="seal" src="/img/limited-edition-seal\.png"[^>]*>', [('limited-edition-seal.webp', 360)],
             '220px', 'gold seal: WebP 35 KB (was 218 KB)', count=1)
    return s


def fix_designer(s, p):
    s = fix_icons(s, p)
    s = fix_fonts(s, p)
    s = fix_site_name(s, p)
    if '<a href="/" aria-label="ZANS Racing home"><img class="zlogo"' not in s:
        s = sub1(s, r'(<img class="zlogo" [^>]*>)', r'<a href="/" aria-label="ZANS Racing home">\1</a>', p, 'logo links to home page')
    return s


def main():
    for p in ALL_STATIC + DESIGNER:
        path = os.path.join(DOCS, p)
        s0 = s = open(path, encoding='utf-8').read()
        if p in DESIGNER:
            s = fix_designer(s, p)
        else:
            s = fix_icons(s, p)
            s = fix_fonts(s, p)
            s = fix_site_name(s, p)
            if p in HOME:
                s = fix_org(s, p, home=True)
            if p in OLD:
                s = fix_org(s, p)
                s = fix_old_page(s, p)
            if p in ARTICLE_IMAGE:
                s = fix_article(s, p)
            s = fix_footer(s, p)
            s = fix_header_logo(s, p)
            s = fix_images(s, p)
        if s != s0:
            open(path, 'w', encoding='utf-8').write(s)
    print('\n'.join(log))


if __name__ == '__main__':
    main()
