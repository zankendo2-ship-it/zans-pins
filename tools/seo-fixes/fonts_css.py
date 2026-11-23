"""The @font-face block used by every ZANS page (inline) and by docs/fonts/fonts.css.

Self-hosted fonts load from our own domain (no extra connection to Google, no render-blocking
stylesheet). The '... Fallback' faces resize Arial / Courier New to the same width and line
height as the real fonts, so the page does not jump when the real fonts arrive (Lighthouse
measured layout shifts of 0.3 on the gift pages and the home page, all caused by font swaps).
Overrides measured with fontTools: English letter-frequency average width v Liberation Sans/Mono
(metric twins of Arial/Courier New), Jost at 500/600/700, Source Sans 3 at 400/600/700.
"""
LATIN = ('U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, '
         'U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD')
LATIN_EXT = ('U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, '
             'U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, '
             'U+2C60-2C7F, U+A720-A7FF')
REAL = [  # family, weight range, file stem
    ('Jost', '100 900', 'jost'),
    ('Source Sans 3', '200 900', 'source-sans-3'),
    ('IBM Plex Mono', '500', 'ibm-plex-mono-500'),
]
ARIAL = "local('Arial'),local('ArialMT'),local('Liberation Sans'),local('LiberationSans'),local('Arimo')"
ARIAL_B = ("local('Arial Bold'),local('Arial-BoldMT'),local('Liberation Sans Bold'),"
           "local('LiberationSans-Bold'),local('Arimo Bold'),local('Arimo-Bold')")
COURIER = "local('Courier New'),local('CourierNewPSMT'),local('Liberation Mono'),local('LiberationMono'),local('Cousine')"
FALLBACK = [  # family, weight range, src, size-adjust, ascent, descent (percent; line gap 0)
    ('Jost Fallback', '100 549', ARIAL, 99.92, 107.09, 37.53),
    ('Jost Fallback', '550 649', ARIAL_B, 94.99, 112.65, 39.48),
    ('Jost Fallback', '650 900', ARIAL_B, 97.8, 109.41, 38.34),
    ('Source Sans 3 Fallback', '100 499', ARIAL, 94.26, 108.64, 42.44),
    ('Source Sans 3 Fallback', '500 649', ARIAL_B, 89.76, 114.08, 44.56),
    ('Source Sans 3 Fallback', '650 900', ARIAL_B, 92.21, 111.05, 43.38),
    ('IBM Plex Mono Fallback', '100 900', COURIER, 99.98, 102.52, 27.5),
]
PRELOAD = ('<link rel="preload" href="/fonts/jost-latin.woff2" as="font" type="font/woff2" crossorigin>'
           '<link rel="preload" href="/fonts/source-sans-3-latin.woff2" as="font" type="font/woff2" crossorigin>')


def css():
    out = []
    for fam, wt, stem in REAL:
        for sub, rng in (('latin-ext', LATIN_EXT), ('latin', LATIN)):
            out.append(f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{wt};font-display:swap;"
                       f"src:url(/fonts/{stem}-{sub}.woff2) format('woff2');unicode-range:{rng}}}")
    for fam, wt, src, sa, asc, desc in FALLBACK:
        out.append(f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{wt};src:{src};"
                   f"size-adjust:{sa}%;ascent-override:{asc}%;descent-override:{desc}%;line-gap-override:0%}}")
    return '\n'.join(out)


if __name__ == '__main__':
    import os
    p = os.path.join(os.path.dirname(__file__), '..', '..', 'docs', 'fonts', 'fonts.css')
    with open(p, 'w', encoding='utf-8') as f:
        f.write('/* ZANS self-hosted fonts (SIL Open Font Licence, see OFL.txt) + metric-matched fallbacks */\n' + css() + '\n')
    print('wrote', p)
