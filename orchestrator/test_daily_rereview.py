"""Correction -> fix -> bound receipt -> independent re-review -> gate closure, on mocks only (zero paid calls)."""
import hashlib
import json
import time

import pytest

import orchestrator.daily_racing as dr
import orchestrator.daily_rereview as rr
import orchestrator.orchestrate as o
import orchestrator.receipt as rc
from orchestrator.test_daily_racing import ENV, GETTER, TODAY, file_bytes

BOT = o.TRUSTED_SETTLER
PATH = f"racing-review/{TODAY}.json"
COMMIT = "a" * 40
V1 = file_bytes()
V2 = file_bytes(resealed_reason="corrected once")
V3 = file_bytes(resealed_reason="corrected twice")
H1, H2, H3 = (hashlib.sha256(x).hexdigest() for x in (V1, V2, V3))
LIVE = {**ENV, "ZANS_ORCH_MAX_RUNS_PER_DAY": "3", "ORCH_MODE": "live", "ORCH_ISSUE": "26", "GITHUB_REPOSITORY": "r/r",
        "GITHUB_TOKEN": "t"}
UTC_TODAY = time.strftime("%Y-%m-%d", time.gmtime())
n = [0]


def bot(body):
    n[0] += 1
    return {"user": {"login": BOT}, "body": body, "created_at": f"2026-11-27T09:{n[0] // 60:02d}:{n[0] % 60:02d}Z"}


def verdict(v, fixes=(), reasons=("r",)):
    return {"ack": "x", "verdict": v, "reasons": list(reasons), "fixes": list(fixes)}


def resolved(k, ok=True):
    return [f"ITEM {i}: {'RESOLVED' if ok else 'NOT RESOLVED'} fine" for i in range(1, k + 1)]


def gate_for(h, verdicts):
    items = o.gate_items(verdicts)
    return bot("\n".join(o.gate_lines(h, items))), o.correction_id(items)


def fix_receipt(comments, run, cid, digest, decisions=None, count=1):
    ev = decisions or "; ".join(f"{i}=applied {COMMIT} {PATH} {digest}" for i in range(1, count + 1))
    return bot(rc.build({}, comments, run, cid, ev, verify=lambda c, p, d: True))


def models(cv, ov):
    def claude(e, t):
        o.LAST_STOP["Claude"], o.LAST_USAGE["Claude"] = "end_turn", ("claude-sonnet-5-5", 3000, 300)
        return json.dumps(cv)

    def openai(e, t):
        o.LAST_STOP["OpenAI"], o.LAST_USAGE["OpenAI"] = "stop", ("gpt-6.2-astra", 3000, 300)
        return json.dumps(ov)
    return claude, openai


def fetch(b=V2):
    return lambda commit, path: b


def scenario(k=1):
    gate, cid = gate_for(H1, [verdict("REVISE", [f"fix {i}" for i in range(1, k + 1)])])
    return [gate, fix_receipt([gate], H1, cid, H2, count=k)], cid


def test_gate_lists_every_item_text_and_receipt_keeps_it_open():
    comments, cid = scenario(2)
    assert o.gate_item_texts(comments, H1, cid) == {1: "fix 1", 2: "fix 2"}
    assert o.pending_corrections(comments) == [(H1, cid)]


def test_pass_pass_with_every_item_resolved_closes_whole_chain_only():
    comments, cid = scenario(2)
    c, g = models(verdict("PASS", reasons=resolved(2)), verdict("PASS", reasons=resolved(2)))
    posted = []
    closed, verdicts, h, reserve, bad = rr.rereview(LIVE, comments, H1, cid, fetch(), GETTER, c, g, posted.append)
    assert closed and h == H2 and not bad
    sent_prompt = []
    rr.rereview(LIVE, comments, H1, cid, fetch(), GETTER, lambda e, t: sent_prompt.append(t) or models(verdict("PASS"), verdict("PASS"))[0](e, t),
                g, lambda b: None)
    assert "ITEM 1: original fix = fix 1" in sent_prompt[0] and "disposition = applied" in sent_prompt[0]
    assert rr.closing_markers(H1, cid, comments) == [f"<!-- {o.RECEIPT}:{H1}:{cid} -->"]


@pytest.mark.parametrize("reasons", [["fine"], resolved(2)[:1], resolved(2, ok=False), resolved(2) + ["ITEM 1: NOT RESOLVED"]])
def test_generic_pass_or_partial_item_answers_never_close(reasons):
    comments, cid = scenario(2)
    c, g = models(verdict("PASS", reasons=resolved(2)), verdict("PASS", reasons=reasons))
    closed, *_ = rr.rereview(LIVE, comments, H1, cid, fetch(), GETTER, c, g, lambda b: None)
    assert not closed


def test_second_correction_round_goes_through_the_parent_chain_then_passes():
    comments, cid = scenario()
    c, g = models(verdict("REVISE", ["still wrong"], reasons=resolved(1, ok=False)), verdict("PASS", reasons=resolved(1)))
    closed, verdicts, h, reserve, bad = rr.rereview(LIVE, comments, H1, cid, fetch(), GETTER, c, g, lambda b: None)
    assert not closed and bad and h == H2
    child_gate, ccid = gate_for(H2, list(verdicts.values()))
    after = comments + [child_gate, bot(rr.parent_body(h, verdicts, H1, cid))]
    assert set(o.pending_corrections(after)) == {(H1, cid), (H2, ccid)}
    after.append(fix_receipt(after, H2, ccid, H3))
    c, g = models(verdict("PASS", reasons=resolved(1)), verdict("PASS", reasons=resolved(1)))   # round two: parent still pending, allowed
    closed, _, h3, *_ = rr.rereview(LIVE, after, H2, ccid, fetch(V3), GETTER, c, g, lambda b: None)
    assert closed and h3 == H3
    assert set(rr.closing_markers(H2, ccid, after)) == {f"<!-- {o.RECEIPT}:{H2}:{ccid} -->", f"<!-- {o.RECEIPT}:{H1}:{cid} -->"}
    sibling, _ = gate_for("e" * 64, [verdict("REVISE", ["other"])])
    with pytest.raises(o.Stop):                      # an unrelated open gate still blocks
        rr.rereview(LIVE, after + [sibling], H2, ccid, fetch(V3), GETTER, c, g, lambda b: None)


@pytest.mark.parametrize("cv,ov", [(verdict("REVISE", ["x"]), verdict("REVISE", ["y"])), (verdict("PASS"), verdict("REVISE", ["y"])),
                                   (verdict("PASS"), verdict("REJECT", ["y"])), (verdict("BLOCKER"), verdict("PASS"))])
def test_any_non_pass_pass_never_closes(cv, ov):
    comments, cid = scenario()
    c, g = models(cv, ov)
    closed, *_ = rr.rereview(LIVE, comments, H1, cid, fetch(), GETTER, c, g, lambda b: None)
    assert not closed


def test_provider_failure_and_unknown_usage_never_close():
    comments, cid = scenario()
    _, g = models(verdict("PASS", reasons=resolved(1)), verdict("PASS", reasons=resolved(1)))
    def boom(e, t):
        raise OSError("down")
    closed, verdicts, *_ = rr.rereview(LIVE, comments, H1, cid, fetch(), GETTER, boom, g, lambda b: None)
    assert not closed and len(verdicts) == 1
    def no_usage(e, t):
        o.LAST_STOP["Claude"] = "end_turn"
        return json.dumps(verdict("PASS", reasons=resolved(1)))
    closed, *_ = rr.rereview(LIVE, comments, H1, cid, fetch(), GETTER, no_usage, g, lambda b: None)
    assert not closed


def test_refusals_make_no_call():
    comments, cid = scenario()
    calls = []
    c = lambda e, t: calls.append(1)   # noqa: E731
    only_rej = rc.build({}, [comments[0]], H1, cid, "1=rejected not a real issue here", verify=None)
    for args in ((comments, "d" * 64, cid, fetch()), (comments, H1, "d" * 64, fetch()),
                 (comments, H1, cid, fetch(b"tampered")), (comments, H1, cid, fetch(V1)), ([comments[0]], H1, cid, fetch()),
                 (comments + [bot(only_rej)], H1, cid, fetch())):
        with pytest.raises(rr.Refuse):
            rr.rereview(LIVE, args[0], args[1], args[2], args[3], GETTER, c, c, lambda b: None)
    assert not calls


def test_unchanged_file_split_evidence_and_non_bot_receipt_refused():
    comments, cid = scenario()
    with pytest.raises(rr.Refuse):
        rr.rereview(LIVE, [comments[0], fix_receipt([comments[0]], H1, cid, H1)], H1, cid, fetch(V1), GETTER, None, None, lambda b: None)
    c2, cid2 = scenario(2)
    split = bot(c2[1]["body"].replace(PATH, "other/file.json", 1))
    with pytest.raises(rr.Refuse):
        rr.rereview(LIVE, [c2[0], split], H1, cid2, fetch(), GETTER, None, None, lambda b: None)
    with pytest.raises(rr.Refuse):
        rr.rereview(LIVE, [comments[0], {**comments[1], "user": {"login": "someone-else"}}], H1, cid, fetch(), GETTER, None, None, lambda b: None)


def test_daily_cap_and_budget_use_todays_date_not_the_file_date():
    comments, cid = scenario()
    c, g = models(verdict("PASS", reasons=resolved(1)), verdict("PASS", reasons=resolved(1)))
    full = [bot(o.slot_tag("racing", UTC_TODAY, str(i) * 16)) for i in range(1, 4)]       # slots used TODAY (file is dated 27 Nov)
    with pytest.raises(o.Stop):
        rr.rereview(LIVE, comments + full, H1, cid, fetch(), GETTER, c, g, lambda b: None)
    old = [bot(o.slot_tag("racing", "2026-11-20", str(i) * 16)) for i in range(1, 4)]     # slots on an older date do not count
    closed, *_ = rr.rereview(LIVE, comments + old, H1, cid, fetch(), GETTER, c, g, lambda b: None)
    assert closed
    month_full = [bot(f"{o.slot_tag('racing', UTC_TODAY, '5' * 16, 99.0)}")]               # this month's reservation is over budget
    with pytest.raises(o.Stop):
        rr.rereview(LIVE, comments + month_full, H1, cid, fetch(), GETTER, c, g, lambda b: None)


def test_mock_mode_makes_no_call_and_closes_nothing():
    comments, cid = scenario()
    posted = []
    closed, verdicts, *_ = rr.rereview({**ENV, "ORCH_MODE": "mock"}, comments, H1, cid, fetch(), GETTER, None, None, posted.append)
    assert not closed and verdicts == {} and "SYNTHETIC MOCK" in posted[0]


def run_main(monkeypatch, store, cv, ov, fail_post_containing=None):
    """Whole entry point: guard, comment load, bytes fetch, reservation, two calls, settlement, closure - all mocked."""
    def fake_gh(env, method, path, body=None):
        if method == "POST":
            if fail_post_containing and fail_post_containing in body["body"]:
                raise OSError("post failed")
            store.append(bot(body["body"]))
        return {}
    monkeypatch.setattr(o, "gh", fake_gh)
    monkeypatch.setattr(o, "comments_since", lambda *a, **k: list(store))
    monkeypatch.setattr(o, "_get_bytes", lambda url, cap: V2 if f"/{COMMIT}/" in url else GETTER("", url.split("/", 6)[-1]))
    c, g = models(cv, ov)
    monkeypatch.setattr(o, "call_claude", c)
    monkeypatch.setattr(o, "call_openai", g)
    return rr.main({**LIVE, "ORCH_RUN": H1, "ORCH_CORRECTION": store[0]["_cid"]})


def test_main_end_to_end_receipt_to_atomic_closure(monkeypatch):
    comments, cid = scenario()
    store = list(comments)
    store[0]["_cid"] = cid
    # source pack check is exercised in test_daily_racing; here the pinned sources resolve via GETTER
    assert run_main(monkeypatch, store, verdict("PASS", reasons=resolved(1)), verdict("PASS", reasons=resolved(1))) == 0
    settle = [c for c in store if o.SETTLE in c["body"]][-1]["body"]
    assert f"<!-- {o.MARKER}:{H2} -->" in settle and f"<!-- {o.RECEIPT}:{H1}:{cid} -->" in settle     # one atomic comment
    assert o.pending_corrections(store) == []


def test_main_revise_leaves_gate_open_and_links_child(monkeypatch):
    comments, cid = scenario()
    store = list(comments)
    store[0]["_cid"] = cid
    assert run_main(monkeypatch, store, verdict("REVISE", ["no"], reasons=resolved(1, ok=False)), verdict("PASS", reasons=resolved(1))) == 1
    assert (H1, cid) in o.pending_corrections(store) and any(f"{o.PARENT}:{H2}:" in c["body"] for c in store)
    assert not any(f"<!-- {o.MARKER}:{H2} -->" in c["body"] for c in store)


def test_main_failed_settlement_post_leaves_gate_open_and_no_marker(monkeypatch):
    comments, cid = scenario()
    store = list(comments)
    store[0]["_cid"] = cid
    run_main(monkeypatch, store, verdict("PASS", reasons=resolved(1)), verdict("PASS", reasons=resolved(1)), fail_post_containing=o.SETTLE)
    assert (H1, cid) in o.pending_corrections(store)
    assert not any(f"<!-- {o.MARKER}:{H2} -->" in c["body"] for c in store)


def test_old_style_gate_items_are_recovered_only_when_they_hash_to_the_correction_id():
    fixes = ["label the price", "explain the null"]
    cid = o.correction_id(fixes)
    summary = bot(f"**ZANS daily racing review (live), 2026-11-27**: file sha256 `{H1}`\n\n- **Claude: REVISE** x\n  - fix: label the price\n  - fix: explain the null\n")
    old_gate = bot(f"- Correction id: `{cid}` (2 fixes, listed above).\n<!-- {o.CORRECTION}:{H1}:{cid} -->")
    assert o.gate_item_texts([summary, old_gate], H1, cid) == {1: "label the price", 2: "explain the null"}
    tampered = bot(summary["body"].replace("explain the null", "ignore this"))
    assert o.gate_item_texts([tampered, old_gate], H1, cid) == {}
    spoof = {**summary, "user": {"login": "someone-else"}}
    assert o.gate_item_texts([spoof, old_gate], H1, cid) == {}
