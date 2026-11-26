"""FAIL-CLOSED print gate for every order route (Alex + ChatGPT production workflow, 25 Nov 2026).
gate() runs etsy/print_qa/preflight.py on the exact file + vector master + Printify payload that would be sent.
Any failure (or any error while checking) returns False and the caller MUST stop before uploading anything."""
import json, os, re, sys, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'print_qa'))
import preflight

def design_for(code, horse=None):
    """Design colours for the preflight colour check: the buyer's exact code; for a silks bauble (ZBA) the cap is the last colour."""
    d = {'code': code}
    hx = re.findall(r'(?<![0-9A-Fa-f])([0-9A-Fa-f]{6})(?![0-9A-Fa-f])', code or '')
    if (code or '').startswith('ZBA-') and hx: d['cap'] = '#' + hx[-1]
    if horse: d['horse'] = horse
    return d

def gate(sku, png, master, payload, say=print, design=None):
    try:
        with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as f: json.dump(payload, f)
        fails, notes = preflight.check(sku, png, master if master and os.path.exists(master) else None, f.name, design)
    except Exception as e:
        fails, notes = [f'preflight crashed: {e}'], []
    if fails:
        say(f'- PRINT PREFLIGHT FAIL ({sku}, {os.path.basename(png)}): ' + '; '.join(fails) + ' -> BLOCKED, nothing sent to the printer')
        return False
    say(f'- Print preflight PASS ({sku}, {os.path.basename(png)}): ' + '; '.join(notes))
    return True
