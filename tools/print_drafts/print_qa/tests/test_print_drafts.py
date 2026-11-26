"""Mocked tests for etsy/print_drafts.py v3 (ChatGPT #26 7185568999 + 7185972203): no network, fake Printify, fake git."""
import base64, io, json, os, struct, sys
import pytest
from PIL import Image
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
import print_drafts as D

SHOP = D.SHOP
GATE_OK = lambda *a, **k: True
ENV = {'GITHUB_EVENT_NAME': 'push', 'GITHUB_REF': D.BRANCH}
RUN = 'v5drafts-20261126-01'
SECRET_ADDR = {'zip': 'ZZ9 9ZZ', 'address1': '1 Secret Lane'}


def jpeg(w=600, h=600):
    b = io.BytesIO(); Image.new('RGB', (w, h), (20, 90, 40)).save(b, 'JPEG'); return b.getvalue()


def approval(tmp, **over):
    ap = {'run_id': RUN, 'shop': SHOP, 'approved_by': 'Alex', 'approved_at': '2026-11-26T08:00Z',
          'source': 'cmsg_017LpptpymmcJZuGHLNRtGrsTEST0000000000', 'files': {s: D.sha(os.path.join(D.O, s + '.png')) for _, s, *_ in D.ITEMS}}
    ap.update(over); p = tmp / 'approval.json'; p.write_text(json.dumps(ap)); return str(p)


class Fake:
    """Printify stand-in. fail = {(kind, n): 'timeout'|status|'junk'} kind = upload|product|get|list|ship|image; n = 1-based."""
    def __init__(self, fail=None, existing=None, published=False, no_mock=False, mock=None, hidden_gets=0, wrong_image=False,
                 upload_lie=False, list_body=None, quote=b'{"standard": 359, "express": 899, "note": "a@b.com"}'):
        self.fail = fail or {}; self.products = dict(existing or {}); self.calls = []; self.n = {}; self.headers = []
        self.published, self.no_mock, self.mock = published, no_mock, mock
        self.hidden_gets, self.wrong_image, self.upload_lie, self.list_body, self.quote = hidden_gets, wrong_image, upload_lie, list_body, quote

    def kind(self, m, url):
        if url.startswith(D.MOCK_HOST): return 'image'
        if 'uploads/images' in url: return 'upload'
        if url.endswith('/products.json') and m == 'POST': return 'product'
        if 'products.json?' in url: return 'list'
        if 'shipping' in url: return 'ship'
        return 'get'

    def __call__(self, m, url, body, headers):
        k = self.kind(m, url); self.n[k] = self.n.get(k, 0) + 1; self.calls.append((m, k)); self.headers.append((k, dict(headers)))
        f = self.fail.get((k, self.n[k]))
        if f == 'timeout': raise TimeoutError('timed out')
        if f == 'junk': return 200, b'not json <html>'
        if f: return f, b''
        if k == 'upload':
            raw = base64.b64decode(json.loads(body)['contents']); w, h = struct.unpack('>II', raw[16:24])
            return 201, json.dumps({'id': f'{self.n[k]:024x}', 'mime_type': 'image/png', 'width': w, 'height': h + (1 if self.upload_lie else 0),
                                    'size': len(raw)}).encode()
        if k == 'product':
            b = json.loads(body); pid = f'{len(self.products) + 1:024x}'.replace('0', 'a', 1)
            self.products[pid] = b; return 200, json.dumps({'id': pid}).encode()
        if k == 'list':
            if self.list_body is not None: return 200, self.list_body
            return 200, json.dumps({'data': [{'id': i, 'title': p['title']} for i, p in self.products.items()], 'last_page': 1}).encode()
        if k == 'get':
            if self.hidden_gets > 0:
                self.hidden_gets -= 1; return 404, b''
            pid = url.rsplit('/', 1)[1][:-5]; b = self.products[pid]; var = b['variants'][0]['id']
            areas = json.loads(json.dumps(b['print_areas']))
            if self.wrong_image: areas[0]['placeholders'][0]['images'][0]['id'] = 'f' * 24
            return 200, json.dumps({'id': pid, 'blueprint_id': b['blueprint_id'], 'print_provider_id': b['print_provider_id'],
                                    'external': {'id': 'etsy'} if self.published else None, 'is_locked': False, 'visible': False,
                                    'variants': [{'id': var, 'is_enabled': True, 'cost': 736}, {'id': 1, 'is_enabled': False}],
                                    'print_areas': areas,
                                    'images': [] if self.no_mock else [{'src': D.MOCK_HOST + 'mockup/x.jpg', 'variant_ids': [var], 'position': 'front'}]}).encode()
        if k == 'ship': return 200, self.quote
        if k == 'image': return 200, self.mock if self.mock is not None else jpeg()


class Git:
    def __init__(self, fail_at=None): self.n = 0; self.fail_at = fail_at; self.msgs = []
    def __call__(self, paths, msg):
        self.n += 1; self.msgs.append(msg); return self.n != self.fail_at


@pytest.fixture(autouse=True)
def out_root(tmp_path, monkeypatch):
    monkeypatch.setattr(D, 'OUT_ROOT', str(tmp_path / 'out'))


def go(tmp, fake, ap=None, env=ENV, git=None, trig=True, gate=GATE_OK, logs=None):
    api = D.Api('SECRETKEY', transport=fake)
    say = (lambda *a: logs.append(' '.join(map(str, a)))) if logs is not None else (lambda *a: None)
    return D.run(dict(env), 'SECRETKEY', SECRET_ADDR, api=api, say=say, gate=gate, checkpoint=git or Git(), sleep=lambda s: None,
                 approval_path=ap or approval(tmp), triggered_by_approval=trig)


def state(tmp):
    return json.load(open(tmp / 'out' / RUN / 'state.json'))


def test_complete_run(tmp_path):
    f = Fake(); g = Git(); assert go(tmp_path, f, git=g) == 0
    s = state(tmp_path); assert s['status'] == 'COMPLETE' and len(f.products) == 5
    assert all(i['readback'] == 'OK' and i['mockups'] and i['postage_cents'] and i['cost_cents'] == 736 for i in s['items'].values())
    assert {m for m, _ in f.calls} <= {'GET', 'POST'} and g.msgs[0].endswith('approval consumed')
    assert all(it['postage_cents'] == {'standard': 359, 'express': 899} for it in s['items'].values())   # whitelist only


def test_pending_intent_checkpointed_before_every_post(tmp_path):
    order = []
    class F(Fake):
        def __call__(s, m, url, body, headers):
            if m == 'POST': order.append(('post', s.kind(m, url)))
            return Fake.__call__(s, m, url, body, headers)
    class G(Git):
        def __call__(s, paths, msg): order.append(('save', msg.split(': ', 1)[1])); return True
    assert go(tmp_path, F(), git=G()) == 0
    for i, (k, v) in enumerate(order):
        if k == 'post': assert order[i - 1][0] == 'save' and 'pending' in order[i - 1][1]


# --- blocked before any API call ---
@pytest.mark.parametrize('env', [{'GITHUB_EVENT_NAME': 'workflow_dispatch', 'GITHUB_REF': D.BRANCH},
                                 {'GITHUB_EVENT_NAME': 'push', 'GITHUB_REF': 'refs/heads/main'}, {}])
def test_stale_dispatch_or_wrong_ref_blocks(tmp_path, env):
    f = Fake(); assert go(tmp_path, f, env=env) == 3 and f.calls == []


def test_approval_not_in_trigger_commit_blocks(tmp_path):
    f = Fake(); assert go(tmp_path, f, trig=False) == 3 and f.calls == []


@pytest.mark.parametrize('over', [{'shop': '999'}, {'approved_by': 'Alex (test)'}, {'source': 'chatgpt said yes'}, {'run_id': '../../etc'},
                                  {'approved_at': 'today'}, {'files': {}}, {'extra': 1}, {'files': {s: 'x' * 64 for _, s, *_ in D.ITEMS}}])
def test_bad_approval_blocks(tmp_path, over):
    f = Fake(); assert go(tmp_path, f, ap=approval(tmp_path, **over)) == 3 and f.calls == []


def test_missing_approval_blocks(tmp_path):
    f = Fake(); assert go(tmp_path, f, ap=str(tmp_path / 'none.json')) == 3 and f.calls == []


def test_gate_fail_blocks(tmp_path):
    f = Fake(); assert go(tmp_path, f, gate=lambda *a, **k: False) == 3 and f.calls == []


def test_one_shot_replay_blocks(tmp_path):
    f = Fake(); assert go(tmp_path, f) == 0; n = len(f.calls)
    assert go(tmp_path, f) == 3 and len(f.calls) == n
    os.remove(tmp_path / 'out' / RUN / 'state.json')          # CONSUMED alone still blocks
    assert go(tmp_path, f) == 3 and len(f.calls) == n


# --- stops, no retry ---
def test_failed_state_push_stops_before_any_call(tmp_path):
    f = Fake(); assert go(tmp_path, f, git=Git(fail_at=1)) == 2 and f.calls == []
    assert os.path.exists(tmp_path / 'out' / RUN / 'CONSUMED')


def test_failed_push_mid_run_stops_before_next_post(tmp_path):
    f = Fake(); assert go(tmp_path, f, git=Git(fail_at=3)) == 2      # 1 consumed, 2 upload pending, 3 product pending
    assert f.n.get('upload') == 1 and 'product' not in f.n


def test_marker_already_exists_stops(tmp_path):
    ex = {'b' * 24: {'title': f'old {D.marker(RUN, "qa-v5-loussiemoo")}'}}
    f = Fake(existing=ex); assert go(tmp_path, f) == 2 and 'upload' not in f.n


@pytest.mark.parametrize('body', [b'{"data": []}', b'{"last_page": 1}', b'{"data": [], "last_page": 41}', b'oops'])
def test_pagination_missing_or_huge_fails_closed(tmp_path, body):
    f = Fake(list_body=body); assert go(tmp_path, f) == 2 and 'upload' not in f.n


@pytest.mark.parametrize('fail', ['timeout', 500, 'junk'])
def test_ambiguous_upload_stops_no_retry(tmp_path, fail):
    f = Fake(fail={('upload', 1): fail}); assert go(tmp_path, f) == 2
    s = state(tmp_path); it = s['items']['qa-v5-loussiemoo']
    assert f.n['upload'] == 1 and it['pending'] == 'upload' and it['ambiguous'] and s['status'] == 'STOPPED'


def test_upload_record_mismatch_is_ambiguous(tmp_path):
    f = Fake(upload_lie=True); assert go(tmp_path, f) == 2 and 'product' not in f.n


def test_crash_after_upload_product_timeout_keeps_intent(tmp_path):
    f = Fake(fail={('product', 2): 'timeout'}); assert go(tmp_path, f) == 2
    it = state(tmp_path)['items']['qa-v5-zoo-olympios']
    assert it['upload'] and it['pending'] == 'product' and f.n['product'] == 2 and f.n['upload'] == 2


def test_delayed_visibility_retries_get_only(tmp_path):
    f = Fake(hidden_gets=3); assert go(tmp_path, f) == 0 and f.n['product'] == 5


def test_never_visible_stops(tmp_path):
    f = Fake(hidden_gets=99); assert go(tmp_path, f) == 2 and f.n['product'] == 1


def test_wrong_image_on_readback_stops(tmp_path):
    f = Fake(wrong_image=True); assert go(tmp_path, f) == 2 and 'image is not our upload' in state(tmp_path)['stop']


def test_published_readback_stops(tmp_path):
    f = Fake(published=True); assert go(tmp_path, f) == 2 and 'published' in state(tmp_path)['stop']


def test_fake_jpeg_bytes_not_a_mockup(tmp_path):
    f = Fake(mock=b'JPEGDATA'); assert go(tmp_path, f) == 2
    assert state(tmp_path)['status'].startswith('INCOMPLETE') and not os.listdir(tmp_path / 'out' / RUN) == []
    assert all(not i['mockups'] for i in state(tmp_path)['items'].values())


def test_tiny_image_not_a_mockup(tmp_path):
    f = Fake(mock=jpeg(100, 100)); assert go(tmp_path, f) == 2


def test_missing_mockup_is_incomplete(tmp_path):
    f = Fake(no_mock=True); assert go(tmp_path, f) == 2 and state(tmp_path)['status'].startswith('INCOMPLETE')


@pytest.mark.parametrize('q', [b'{"standard": "359"}', b'{"standard": -1}', b'[]', b'junk'])
def test_malformed_quote_is_incomplete(tmp_path, q):
    f = Fake(quote=q); assert go(tmp_path, f) == 2
    assert all(i['postage_cents'] is None for i in state(tmp_path)['items'].values())


# --- network safety ---
def test_endpoint_allowlist():
    api = D.Api('k', transport=Fake())
    for m, p in [('DELETE', f'shops/{SHOP}/products/{"a" * 24}.json'), ('POST', f'shops/{SHOP}/products/{"a" * 24}/publish.json'),
                 ('POST', f'shops/{SHOP}/orders.json'), ('POST', 'shops/999/products.json'), ('GET', f'shops/{SHOP}/products/../x.json'),
                 ('GET', f'shops/{SHOP}/products.json?limit=50&page=1&x=1')]:
        with pytest.raises(D.Stop): api.call(m, p)
    assert api.image('https://evil.example/x.jpg') == (None, None)


def test_no_credentials_to_image_host(tmp_path):
    f = Fake(); assert go(tmp_path, f) == 0
    assert all('Authorization' not in h for k, h in f.headers if k == 'image')
    assert all(h.get('Authorization') == 'Bearer SECRETKEY' for k, h in f.headers if k != 'image')


def test_redirect_refused():
    import urllib.request
    with pytest.raises(Exception):
        D._NoRedirect().redirect_request(urllib.request.Request('https://api.printify.com/v1/x'), None, 302, 'Found', {}, 'https://evil.example/')


def test_logs_and_state_carry_no_secrets_or_address(tmp_path):
    logs = []; f = Fake(fail={('ship', 2): 400}); go(tmp_path, f, logs=logs)
    blob = json.dumps(state(tmp_path)) + '\n'.join(logs)
    for s in ('SECRETKEY', 'ZZ9 9ZZ', 'Secret Lane', 'a@b.com', 'api.printify.com'):
        assert s not in blob


def test_workflow_is_push_only_and_reports_real_exit_code():
    wf = open(os.path.join(D.ROOT, '.github', 'workflows', 'print-drafts.yml')).read()
    assert 'workflow_dispatch' not in wf and D.APPROVAL_REL in wf and 'zans-social-notes' in wf
    assert 'concurrency' in wf and 'always()' in wf and '|| echo' not in wf and 'rc=$?' in wf
    assert not os.path.exists(D.APPROVAL), 'approval file must only be added after Alex says yes'


def test_no_address_or_order_ids_in_public_tool():
    import re as _re
    for dp, _, fs in os.walk(D.TOOL):
        for f in fs:
            if f.endswith(('.py', '.json', '.md', '.yml')) and f != os.path.basename(__file__):
                txt = open(os.path.join(dp, f), errors='ignore').read()
                assert not _re.search(r'\b42[0-9]{8}\b', txt), f
