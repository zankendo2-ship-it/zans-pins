"""v5 print-fix DRAFTS (Alex's Q1, 26 Nov 2026): 5 HIDDEN Printify draft products of the gated v5 files, so both
reviewers can see Printify's own mock-ups, plus a UK postage quote. NEVER publishes, orders, retries blindly or deletes.

v3 safety (ChatGPT #26 7185568999 + 7185972203):
- Runs ONLY from .github/workflows/print-drafts.yml (zans-pins) on a PUSH to zans-social-notes whose commit adds the approval file
  (no workflow_dispatch). The approval is ONE-SHOT: the workflow commits + pushes tools/print_drafts/reports/<run_id>/CONSUMED
  before any API call; a run_id that was ever consumed is BLOCKED.
- Approval is bound to the fixed shop, Alex's own message id, the run id and the SHA-256 of all five print files, and is
  validated before any path is built. Every other check (hashes, payloads, print gate) also runs before the first call.
- Before EVERY POST the pending intent is checkpointed DURABLY (state.json committed + pushed). A failed push stops the run.
- Any non-2xx, timed-out, malformed or unexpected answer to a POST = AMBIGUOUS: stop at once, no retry, reconcile by hand.
- Nothing is ever adopted. If any product already carries this run's marker, or the product list cannot be read in full
  (missing pagination fields / over 40 pages), the run stops before creating anything.
- An upload counts only if Printify's record matches the file (24-hex id, image/png, exact width x height, byte size).
- Readback (GET only, retried for delayed visibility) must show: same id, exact blueprint + provider, one print area whose
  variant_ids == [variant], one 'front' placeholder, one image == our upload at x .5 / y .5 / scale 1 / angle 0, exactly
  one enabled variant, not external / locked / visible-on-a-channel.
- Credentials go only to api.printify.com; redirects are refused; mock-ups are fetched from images.printify.com without
  credentials and must be a real decodable JPEG/PNG of at least 300 px. Quotes keep only whitelisted integer fields.
- Logs carry status codes and categories only: never response text, URLs, the address or keys.
Exit: 0 COMPLETE | 2 INCOMPLETE / STOPPED | 3 BLOCKED before any API call."""
import base64, hashlib, io, json, os, re, struct, subprocess, sys, time, urllib.error, urllib.request

TOOL = os.path.dirname(os.path.abspath(__file__))                    # zans-pins tools/print_drafts
ROOT = os.path.dirname(os.path.dirname(TOOL))
sys.path.insert(0, TOOL)
O = os.path.join(TOOL, 'orders')
APPROVAL_REL = 'tools/print_drafts/approval.json'
APPROVAL = os.path.join(ROOT, APPROVAL_REL)
OUT_ROOT = os.path.join(TOOL, 'reports')
SHOP = '7066921'                                   # the ZANS Printify shop; fixed, the approval must name the same
BRANCH = 'refs/heads/zans-social-notes'
ITEMS = [  # (label, file stem, sku, blueprint, provider, variant)
    ('Loussiemoo bauble', 'qa-v5-loussiemoo', 'bauble_harrier', 1676, 94, 115590),
    ('Zoo Olympios bauble', 'qa-v5-zoo-olympios', 'bauble_harrier', 1676, 94, 115590),
    ('Rexs Romance bauble', 'qa-v5-rexs-romance', 'bauble_harrier', 1676, 94, 115590),
    ('FACT TO FILE mug black (Harrier)', 'qa-v5-fact-to-file-mug-2475x1155', 'mug_harrier_11oz', 635, 94, 72180),
    ('FACT TO FILE mug white (T Shirt and Sons)', 'qa-v5-fact-to-file-mug-2582x1120', 'mug_white_tss_11oz', 535, 6, 69010)]
API = 'https://api.printify.com/v1/'
ALLOW = [('POST', r'uploads/images\.json'), ('POST', r'shops/{shop}/products\.json'), ('GET', r'shops/{shop}/products/[0-9a-f]{24}\.json'),
         ('GET', r'shops/{shop}/products\.json\?limit=50&page=\d{1,2}'), ('POST', r'shops/{shop}/orders/shipping\.json')]
MOCK_HOST = 'https://images.printify.com/'
QUOTE_KEYS = ('standard', 'priority', 'express', 'economy', 'printify_express')
HEX24 = re.compile(r'[0-9a-f]{24}')
PLACE = {'position': 'front', 'x': 0.5, 'y': 0.5, 'scale': 1, 'angle': 0}


class Stop(Exception):
    pass


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def png_size(p):
    b = open(p, 'rb').read(24)
    if b[:8] != b'\x89PNG\r\n\x1a\n': raise Stop('print file is not a PNG')
    return struct.unpack('>II', b[16:24])


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        raise urllib.error.URLError('redirect refused')


_OPENER = urllib.request.build_opener(_NoRedirect)


def _urllib(method, url, body, headers):
    r = urllib.request.Request(url, data=body, method=method, headers=headers)
    try:
        with _OPENER.open(r, timeout=120) as x:
            return x.status, x.read()
    except urllib.error.HTTPError as e:
        return e.code, b''


class Api:
    def __init__(self, key, transport=None):
        self.key, self.transport = key, transport or _urllib
        self.allow = [(m, re.compile(p.replace('{shop}', SHOP) + r'$')) for m, p in ALLOW]

    def call(self, method, path, body=None):
        if not any(m == method and rx.match(path) for m, rx in self.allow):
            raise Stop(f'endpoint not allowed: {method} {path.split("?")[0]}')
        try:
            st, raw = self.transport(method, API + path, json.dumps(body).encode() if body is not None else None,
                                     {'Authorization': 'Bearer ' + self.key, 'Content-Type': 'application/json', 'User-Agent': 'ZANS'})
        except Exception as e:          # timeout / reset / redirect = UNCLEAR
            return None, ('unclear', type(e).__name__)
        try:
            return st, (json.loads(raw) if raw else None)
        except ValueError:
            return st, None

    def image(self, url):
        if not (isinstance(url, str) and url.startswith(MOCK_HOST)):
            return None, None
        try:
            return self.transport('GET', url, None, {'User-Agent': 'ZANS'})   # no credentials to the image host
        except Exception:
            return None, None


def ok2(st):
    return isinstance(st, int) and 200 <= st < 300


def real_image(raw):
    try:
        from PIL import Image
        im = Image.open(io.BytesIO(raw)); im.verify()
        im = Image.open(io.BytesIO(raw)); return im.format in ('JPEG', 'PNG') and min(im.size) >= 300
    except Exception:
        return False


def git_checkpoint(paths, msg):
    """Durable checkpoint: commit + push. False = not durable -> the caller stops."""
    try:
        subprocess.run(['git', 'add', '-A', *paths], cwd=ROOT, check=True, capture_output=True)
        if subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=ROOT).returncode == 0:
            return True
        subprocess.run(['git', 'commit', '-q', '-m', msg], cwd=ROOT, check=True, capture_output=True)
        for _ in range(3):
            if subprocess.run(['git', 'push', '-q'], cwd=ROOT, capture_output=True).returncode == 0:
                return True
            subprocess.run(['git', 'pull', '--rebase', '-q'], cwd=ROOT, capture_output=True); time.sleep(3)
    except Exception:
        pass
    return False


def load_approval(path, env, triggered_by_approval):
    """Validate the approval BEFORE anything else (no path is built from unvalidated data)."""
    if env.get('GITHUB_EVENT_NAME') != 'push' or env.get('GITHUB_REF') != BRANCH:
        raise Stop('only a push to the fixed branch may run this (no dispatch, no other branch)')
    if not triggered_by_approval:
        raise Stop('the triggering commit did not add the approval file')
    if not os.path.exists(path):
        raise Stop('no owner approval file')
    ap = json.load(open(path))
    if set(ap) != {'run_id', 'shop', 'approved_by', 'approved_at', 'source', 'files'}:
        raise Stop('approval fields are not exactly the expected set')
    if not (isinstance(ap['run_id'], str) and re.fullmatch(r'v5drafts-\d{8}-\d{2}', ap['run_id'])):
        raise Stop('bad run_id')
    if ap['shop'] != SHOP:
        raise Stop('approval names a different shop')
    if ap['approved_by'] != 'Alex':
        raise Stop('approval must be Alex')
    if not (isinstance(ap['source'], str) and re.fullmatch(r'cmsg_[0-9A-Za-z]{20,60}', ap['source'])):
        raise Stop('approval must cite Alex\'s own message id')
    if not (isinstance(ap['approved_at'], str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}Z', ap['approved_at'])):
        raise Stop('bad approved_at')
    if not isinstance(ap['files'], dict) or set(ap['files']) != {s for _, s, *_ in ITEMS}:
        raise Stop('approval does not list exactly the five files')
    if os.path.exists(os.path.join(OUT_ROOT, ap['run_id'], 'CONSUMED')) or os.path.exists(os.path.join(OUT_ROOT, ap['run_id'], 'state.json')):
        raise Stop('this approval was already used (one-shot)')
    return ap


def preflight_files(ap, say, gate=None):
    if gate is None:
        from print_gate import gate
    files = {}
    for lab, stem, sku, bp, pp, var in ITEMS:
        png = os.path.join(O, stem + '.png')
        if sha(png) != ap['files'][stem]:
            raise Stop(f'{stem}: file changed since approval (sha256 mismatch)')
        pay = json.load(open(os.path.join(O, stem + '.payload.json')))
        want = dict(PLACE, blueprint_id=bp, print_provider_id=pp, variant_id=var)
        if pay != want:
            raise Stop(f'{stem}: payload differs from the reviewed one')
        if not gate(sku, png, os.path.join(O, stem + '.svg'), pay, say, json.load(open(os.path.join(O, stem + '.design.json')))):
            raise Stop(f'{stem}: print gate failed')
        w, h = png_size(png)
        files[stem] = {'payload': pay, 'w': w, 'h': h, 'bytes': os.path.getsize(png)}
    return files


def marker(run_id, stem):
    return f'[zans-v5 {run_id} {stem}]'


def products_with_marker(api, prefix):
    """Full product list; fails closed on any missing pagination field or more than 40 pages."""
    hits, page = [], 1
    while True:
        st, d = api.call('GET', f'shops/{SHOP}/products.json?limit=50&page={page}')
        if not ok2(st) or not isinstance(d, dict) or not isinstance(d.get('data'), list) or not isinstance(d.get('last_page'), int):
            raise Stop('product list could not be read in full')
        if d['last_page'] > 40:
            raise Stop('product list over 40 pages - check by hand')
        hits += [p.get('id') for p in d['data'] if isinstance(p, dict) and prefix in str(p.get('title') or '')]
        if page >= d['last_page']:
            return hits
        page += 1


def upload_ok(up, f):
    return (isinstance(up, dict) and isinstance(up.get('id'), str) and HEX24.fullmatch(up['id'])
            and up.get('mime_type') == 'image/png' and up.get('width') == f['w'] and up.get('height') == f['h']
            and up.get('size') == f['bytes'])


def readback_problems(full, pid, bp, pp, var, upload_id):
    if not isinstance(full, dict): return ['no product body']
    p = []
    if full.get('id') != pid: p.append('id')
    if full.get('blueprint_id') != bp or full.get('print_provider_id') != pp: p.append('blueprint/provider')
    if full.get('external') or full.get('is_locked') is not False: p.append('published/locked')
    if full.get('visible') not in (False, None): p.append('visible')
    en = [v.get('id') for v in full.get('variants') or [] if isinstance(v, dict) and v.get('is_enabled')]
    if en != [var]: p.append('enabled variants')
    areas = full.get('print_areas') or []
    if len(areas) != 1 or areas[0].get('variant_ids') != [var]: p.append('print areas')
    else:
        ph = areas[0].get('placeholders') or []
        if len(ph) != 1 or ph[0].get('position') != 'front': p.append('placeholders')
        else:
            im = ph[0].get('images') or []
            if len(im) != 1 or im[0].get('id') != upload_id: p.append('image is not our upload')
            elif any(abs(float(im[0].get(k, -99)) - float(PLACE[k])) > 1e-9 for k in ('x', 'y', 'scale', 'angle')): p.append('placement')
    return p


def run(env, key, address, api=None, say=print, gate=None, checkpoint=git_checkpoint, sleep=time.sleep,
        approval_path=APPROVAL, triggered_by_approval=False):
    try:
        ap = load_approval(approval_path, env, triggered_by_approval)
        files = preflight_files(ap, say, gate)
    except Stop as e:
        say(f'BLOCKED before any API call: {e}'); return 3
    out = os.path.join(OUT_ROOT, ap['run_id']); os.makedirs(out, exist_ok=True)
    sp = os.path.join(out, 'state.json')
    state = {'run_id': ap['run_id'], 'shop': SHOP, 'source': ap['source'], 'status': 'STARTING', 'items': {}}

    def save(msg):
        with open(sp + '.tmp', 'w') as f:
            json.dump(state, f, indent=1); f.flush(); os.fsync(f.fileno())
        os.replace(sp + '.tmp', sp)
        if not checkpoint([out], f'print drafts {ap["run_id"]}: {msg}'):
            raise Stop('durable checkpoint (git push) failed')
    open(os.path.join(out, 'CONSUMED'), 'w').write(ap['run_id'] + '\n')
    api = api or Api(key)
    try:
        save('approval consumed')
        if products_with_marker(api, f'[zans-v5 {ap["run_id"]} '):
            raise Stop('products with this run marker already exist - reconcile by hand')
        for lab, stem, sku, bp, pp, var in ITEMS:
            it = state['items'][stem] = {'item': lab}; f = files[stem]
            it['pending'] = 'upload'; save(f'{stem} upload pending')
            st, up = api.call('POST', 'uploads/images.json', {'file_name': f'{stem}-{ap["run_id"]}.png',
                              'contents': base64.b64encode(open(os.path.join(O, stem + '.png'), 'rb').read()).decode()})
            if not ok2(st) or not upload_ok(up, f):
                it['ambiguous'] = f'upload ({st})'; save(f'{stem} upload AMBIGUOUS')
                raise Stop(f'{stem}: upload answer was not a clean match ({st}) - reconcile by hand, no retry')
            it['upload'] = up['id']; it['pending'] = 'product'; save(f'{stem} upload ok, product pending')
            st, pr = api.call('POST', f'shops/{SHOP}/products.json', {
                'title': f'DRAFT v5 print check - {lab} (do not publish) {marker(ap["run_id"], stem)}',
                'description': 'Hidden draft for print-fix mock-up review. Not for sale.',
                'blueprint_id': bp, 'print_provider_id': pp, 'variants': [{'id': var, 'price': 9999, 'is_enabled': True}],
                'print_areas': [{'variant_ids': [var], 'placeholders': [{'position': 'front', 'images': [
                    {'id': it['upload'], 'x': PLACE['x'], 'y': PLACE['y'], 'scale': PLACE['scale'], 'angle': PLACE['angle']}]}]}]})
            if not ok2(st) or not isinstance(pr, dict) or not HEX24.fullmatch(str(pr.get('id'))):
                it['ambiguous'] = f'product ({st})'; save(f'{stem} product AMBIGUOUS')
                raise Stop(f'{stem}: product answer was not clean ({st}) - reconcile by hand, no retry')
            it['product'] = pr['id']; it['pending'] = None; save(f'{stem} product made')
            full, probs = None, ['not visible yet']
            for _ in range(5):                                   # GET only: safe to repeat for delayed visibility
                sleep(6); st, full = api.call('GET', f'shops/{SHOP}/products/{it["product"]}.json')
                probs = readback_problems(full, it['product'], bp, pp, var, it['upload']) if ok2(st) else ['not visible yet']
                if probs != ['not visible yet']: break
            if probs:
                it['readback'] = probs; save(f'{stem} readback FAIL')
                raise Stop(f'{stem}: readback FAIL ({", ".join(probs)})')
            it['readback'] = 'OK'
            cost = next((v.get('cost') for v in full['variants'] if v.get('id') == var), None)
            it['cost_cents'] = cost if isinstance(cost, int) else None
            it['mockups'] = []
            for n, im in enumerate([i for i in full.get('images') or [] if isinstance(i, dict) and var in (i.get('variant_ids') or [])][:6]):
                st, raw = api.image(im.get('src'))
                if ok2(st) and isinstance(raw, (bytes, bytearray)) and real_image(raw):
                    view = re.sub(r'[^a-z0-9-]', '', str(im.get('position') or 'view').lower())[:20] or 'view'
                    fn = f'{stem}-mockup-{n + 1}-{view}.jpg'; open(os.path.join(out, fn), 'wb').write(raw); it['mockups'].append(fn)
            it['pending'] = 'quote'; save(f'{stem} quote pending')
            st, q = api.call('POST', f'shops/{SHOP}/orders/shipping.json',
                             {'line_items': [{'product_id': it['product'], 'variant_id': var, 'quantity': 1}], 'address_to': address})
            quote = {k: q[k] for k in QUOTE_KEYS if isinstance(q, dict) and isinstance(q.get(k), int) and 0 <= q[k] < 100000} if ok2(st) else {}
            it['postage_cents'] = quote or None; it['pending'] = None
            it['complete'] = bool(it['mockups']) and bool(quote) and it['cost_cents'] is not None
            save(f'{stem} done')
            say(f'- {lab}: draft {it["product"]} readback OK, cost {it["cost_cents"]}, postage {it["postage_cents"]}, '
                f'{len(it["mockups"])} mock-ups{"" if it["complete"] else " - INCOMPLETE"}')
    except Stop as e:
        state['status'] = 'STOPPED'; state['stop'] = str(e)[:200]
        try: save('STOPPED')
        except Stop: pass
        say(f'STOPPED: {e}. Nothing deleted or retried.'); return 2
    done = all(state['items'].get(s, {}).get('complete') for _, s, *_ in ITEMS)
    state['status'] = 'COMPLETE' if done else 'INCOMPLETE - missing mock-up, cost or postage'
    try:
        save(state['status'])
    except Stop as e:
        say(f'STOPPED: {e}'); return 2
    say(f'Status: {state["status"]}. Drafts KEPT. Nothing published, ordered or deleted.')
    return 0 if done else 2


def approval_in_trigger_commit():
    sha_ = os.environ.get('GITHUB_SHA', '')
    try:
        r = subprocess.run(['git', 'diff-tree', '--no-commit-id', '--name-status', '-r', sha_], cwd=ROOT, capture_output=True, text=True, check=True)
        return any(l.split('\t')[-1] == APPROVAL_REL and l[0] == 'A' for l in r.stdout.splitlines())
    except Exception:
        return False


if __name__ == '__main__':
    try:                                   # delivery address = repo secret PRINT_DRAFTS_ADDRESS (JSON); never in the repo or logs
        addr = json.loads(os.environ.get('PRINT_DRAFTS_ADDRESS') or '')
        assert isinstance(addr, dict) and addr.get('country')
    except Exception:
        print('BLOCKED before any API call: secret PRINT_DRAFTS_ADDRESS missing or not valid JSON'); sys.exit(3)
    sys.exit(run(dict(os.environ), os.environ.get('PRINTIFY_API_KEY', '').strip(), addr,
                 triggered_by_approval=approval_in_trigger_commit()))
