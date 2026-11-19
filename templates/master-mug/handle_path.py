"""Writes the master mug's handle path into mug.json: a D made of two arms and two quarter-circles. python3 templates/master-mug/handle_path.py <top cm> <bottom cm> <reach cm> <corner radius cm>"""
import json, math, sys, os
p = os.path.dirname(os.path.abspath(__file__)) + '/mug.json'; m = json.load(open(p)); top, bot, reach, r = map(float, sys.argv[1:5]); out = -reach
q = [i*math.pi/2/6 for i in range(7)]
pts = [[0.3, top], [-0.4, top]] + [[out + r - r*math.sin(a), top - r + r*math.cos(a)] for a in q] + ([[out, (top + bot)/2]] if top - bot - 2*r > 0.3 else []) + [[out + r - r*math.cos(a), bot + r - r*math.sin(a)] for a in q] + [[-0.4, bot], [0.3, bot]]
m['handle']['path'] = [[round(x, 3), round(y, 3)] for x, y in pts]; m['handle']['reach'] = reach + m['handle']['thick']/2
s = json.dumps(m, indent=1); import re; s = re.sub(r'\[\s+(-?[\d.]+),\s+(-?[\d.]+)\s+\]', r'[\1, \2]', s); open(p, 'w').write(s + '\n')
