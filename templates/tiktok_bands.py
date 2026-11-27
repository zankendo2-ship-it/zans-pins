"""Silks bands for 1080x1920 TikTok cards (Alex's standing rule): the CAP colour as a band directly under the top metal strip,
the SILKS colours (with pattern) as a band directly above the bottom metal strip. Usage: python3 templates/tiktok_bands.py <post key in posts.json> <card1.png> [card2.png ...]
Run after the cards are rendered and before the video is built; the video build adds the metal strips on top."""
import sys, os, json
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import silks_bands as sb
NOCAP = '--no-cap' in sys.argv; sys.argv = [a for a in sys.argv if a != '--no-cap']
key = sys.argv[1]; P = sb.POSTS[key]; s = P['silks']; edge = sb.EDGE[P.get('metal', 'gold')]
STRIP, BH = 28, 90
for f in sys.argv[2:]:
    im = Image.open(f).convert('RGB'); W, H = im.size; d = ImageDraw.Draw(im)
    if not NOCAP: d.rectangle([0, STRIP, W, STRIP + BH], fill=s['cap']); d.rectangle([0, STRIP + BH, W, STRIP + BH + 5], fill=edge)
    im.paste(sb.silks_band(W, BH, s), (0, H - STRIP - BH)); d.rectangle([0, H - STRIP - BH - 6, W, H - STRIP - BH - 1], fill=edge)
    im.save(f)
