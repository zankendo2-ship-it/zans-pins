"""Writes the master mug's handle path into mug.json: one continuous oval D. Two short straight arms leave the wall square-on, joined by half an ellipse.
python3 templates/master-mug/handle_path.py <top cm> <bottom cm> <reach cm> <arm cm>"""
import json, math, sys, os, re
p = os.path.dirname(os.path.abspath(__file__)) + '/mug.json'; m = json.load(open(p)); top, bot, reach, arm = map(float, sys.argv[1:5])
cy, ry, rx = (top + bot)/2, (top - bot)/2, reach - arm; n = 28
pts = [[0.35, top], [0.0, top], [-arm*0.5, top]] + [[-arm - rx*math.sin(math.pi*i/n), cy + ry*math.cos(math.pi*i/n)] for i in range(n + 1)] + [[-arm*0.5, bot], [0.0, bot], [0.35, bot]]
m['handle']['path'] = [[round(x, 3), round(y, 3)] for x, y in pts]; m['handle']['reach'] = reach + m['handle']['thick']/2
s = json.dumps(m, indent=1); s = re.sub(r'\[\s+(-?[\d.]+),\s+(-?[\d.]+)\s+\]', r'[\1, \2]', s); open(p, 'w').write(s + '\n')
