"""Fixed (non-zooming) overlay for 1080x1920 TikTok videos, Alex's permanent strip rule:
ZANS gold metal strip top and bottom + CAP colour band directly under the top strip (thick, >=120 px) + SILKS band directly above the bottom strip.
Because it is laid over the finished video, the bands never shift with the slow zoom or the crossfades.
Usage: python3 templates/tiktok_overlay.py <post key in posts.json> <out.png>"""
import sys, os
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import silks_bands as sb
key, out = sys.argv[1], sys.argv[2]
P = sb.POSTS[key]; s = P['silks']; edge = sb.EDGE[P.get('metal', 'gold')]
W, H, STRIP, CAPBH, BH = 1080, 1920, 28, 126, 90
ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
d.rectangle([0, STRIP, W, STRIP + CAPBH], fill=s['cap']); d.rectangle([0, STRIP + CAPBH, W, STRIP + CAPBH + 5], fill=edge)
ov.paste(sb.silks_band(W, BH, s), (0, H - STRIP - BH)); d.rectangle([0, H - STRIP - BH - 6, W, H - STRIP - BH - 1], fill=edge)
ov.alpha_composite(Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets/metal-strip-28px-9x16.png')).convert('RGBA'))
ov.save(out)
