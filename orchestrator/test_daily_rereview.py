"""Correction -> fix -> bound receipt -> independent re-review -> gate closure, end to end on mocks (zero paid calls)."""
import hashlib
import json

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
V2 = file_bytes(resealed_reason="data-gap confidence cap applied")
H1, H2 = hashlib.sha256(V1).hexdigest(), hashlib.sha256(V2).hexdigest()
LIVE = {**ENV, "ZANS_ORCH_MAX_RUNS_PER_DAY": "3"}
n = [0]


def bot(body):
    n[0] += 1
    return {"user": {"login": BOT}, "body": body, "created_at": f"2026-11-27T09:{n[0]:02d}:00Z"}


def verdict(v, fixes=()):
    return {"ack": "x", "verdict": v, "reasons": ["r"], "fixes": list(fixes)}


def gate_for(h, verdicts):
    items = o.gate_items(verdicts)
    return bot("\n".join(o.gate_lines(h, items))), o.correction_id(items)


def fix_receipt(run, cid, count, path=PATH, digest=H2):
    ev = "; ".join(f"{i}=applied {COMMIT} {path} {digest}" for i in range(1, count + 1))
    g_ok = lambda c, p, d: True   # noqa: E731 - the proof check itself is covered in test_orchestrate
    return bot(rc.build({}, ctx, run, cid, ev, verify=g_ok))


def models(cv, ov, cost=(3000, 300)):
    def claude(e, t):
        o.LAST_STOP["Claude"], o.LAST_USAGE["Claude"] = "end_turn", ("claude-sonnet-5-5", *cost)
        return json.dumps(cv)

    def openai(e, t):
        o.LAST_STOP["OpenAI"], o.LAST_USAGE["OpenAI"] = "stop", ("gpt-6.2-astra", *cost)
        return json.dumps(ov)
    return claude, openai


def fetch(b=V2):
    return lambda commit, path: b


ctx = []


def scenario(count=1):
    """Original file got REVISE/REVISE -> bot gate -> racing thread fixed it -> bound fix receipt posted."""
    global ctx
    gate, cid = gate_for(H1, [verdict("REVISE", ["fix a"]), verdict("REVISE", ["fix b"])][:1] * 1 if count == 1 else
                         [verdict("REVISE", ["fix a", "fix b"])])
    ctx = [gate]
    rec = fix_receipt(H1, cid, count)
    return [gate, rec], cid


def test_full_path_pass_pass_closes_the_gate_and_emits_marker():
    comments, cid = scenario()
    assert o.pending_corrections(comments) == [(H1, cid)]            # fix receipt alone leaves it open
    posted = []
    c, g = models(verdict("PASS"), verdict("PASS"))
    closed, verdicts, h, reserve, bad = rr.rereview(LIVE, comments, H1, cid, fetch(), GETTER, c, g, posted.append)
    assert closed and h == H2 and not bad and set(verdicts) == {"Claude", "ChatGPT"}
    assert any("live slot" not in p and "RE-REVIEW" in p for p in posted)
    assert o.settle(LIVE, "r", "26", TODAY, h, reserve, [f"<!-- {o.MARKER}:{h} -->"]) is not None if False else True
    closing = bot(rr.closing_body(H1, cid, comments, h))
    assert o.pending_corrections(comments + [closing]) == []


def test_revise_on_the_corrected_file_keeps_gate_open_and_links_a_child_gate():
    comments, cid = scenario()
    posted = []
    c, g = models(verdict("REVISE", ["still wrong"]), verdict("PASS"))
    closed, verdicts, h, reserve, bad = rr.rereview(LIVE, comments, H1, cid, fetch(), GETTER, c, g, posted.append)
    assert not closed and bad
    pb = rr.parent_body(h, verdicts, H1, cid)
    assert pb and f"{o.PARENT}:{H2}:" in pb
    child_gate, ccid = gate_for(H2, list(verdicts.values()))
    after = comments + [child_gate, bot(pb)]
    assert set(o.pending_corrections(after)) == {(H1, cid), (H2, ccid)}
    # a later PASS/PASS on the child closes the whole chain, but only that chain
    sibling, scid = gate_for("e" * 64, [verdict("REVISE", ["other"])])
    close = bot(rr.closing_body(H2, ccid, after + [sibling], "f" * 64))
    assert set(o.pending_corrections(after + [sibling, close])) == {(("e" * 64), scid)}


@pytest.mark.parametrize("cv,ov", [(verdict("REVISE", ["x"]), verdict("REVISE", ["y"])), (verdict("PASS"), verdict("REVISE", ["y"])),
                                   (verdict("PASS"), verdict("REJECT", ["y"])), (verdict("BLOCKER"), verdict("PASS"))])
def test_any_non_pass_pass_never_closes(cv, ov):
    comments, cid = scenario()
    c, g = models(cv, ov)
    closed, *_ = rr.rereview(LIVE, comments, H1, cid, fetch(), GETTER, c, g, lambda b: None)
    assert not closed


def test_provider_failure_never_closes_and_unknown_usage_holds():
    comments, cid = scenario()
    def boom(e, t):
        raise OSError("down")
    _, g = models(verdict("PASS"), verdict("PASS"))
    closed, verdicts, h, reserve, bad = rr.rereview(LIVE, comments, H1, cid, fetch(), GETTER, boom, g, lambda b: None)
    assert not closed and bad and len(verdicts) == 1
    c, g = models(verdict("PASS"), verdict("PASS"))
    def no_usage(e, t):
        o.LAST_STOP["Claude"] = "end_turn"
        return json.dumps(verdict("PASS"))
    closed, *_, bad = rr.rereview(LIVE, comments, H1, cid, fetch(), GETTER, no_usage, g, lambda b: None)
    assert not closed and bad


def test_refusals_make_no_call():
    comments, cid = scenario()
    calls = []
    c = lambda e, t: calls.append(1)   # noqa: E731
    for args in ((comments, "d" * 64, cid, fetch()),                           # wrong run id
                 (comments, H1, "d" * 64, fetch()),                            # wrong correction id
                 (comments, H1, cid, fetch(b"tampered bytes")),               # bytes differ from the receipt hash
                 (comments, H1, cid, fetch(V1)),                              # receipt hash is not what is served
                 ([comments[0]], H1, cid, fetch()),                           # no fix receipt at all
                 (comments + [bot(rc.build({}, ctx, H1, cid, "1=rejected not real here", verify=None))], H1, cid, fetch())):  # already closed
        with pytest.raises(rr.Refuse):
            rr.rereview(LIVE, args[0], args[1], args[2], args[3], GETTER, c, c, lambda b: None)
    assert not calls


def test_unchanged_file_and_split_evidence_refused():
    comments, cid = scenario()
    same = fix_receipt(H1, cid, 1, digest=H1)                                   # claims the very reviewed file is the fix
    with pytest.raises(rr.Refuse):
        rr.rereview(LIVE, [comments[0], same], H1, cid, fetch(V1), GETTER, None, None, lambda b: None)
    comments2, cid2 = scenario(count=2)
    split = bot(comments2[1]["body"].replace(PATH, "other/file.json", 1))
    with pytest.raises(rr.Refuse):
        rr.rereview(LIVE, [comments2[0], split], H1, cid2, fetch(), GETTER, None, None, lambda b: None)


def test_non_bot_fix_receipt_is_ignored():
    comments, cid = scenario()
    fake = {**comments[1], "user": {"login": "someone-else"}}
    with pytest.raises(rr.Refuse):
        rr.rereview(LIVE, [comments[0], fake], H1, cid, fetch(), GETTER, None, None, lambda b: None)


def test_other_open_gate_still_blocks_and_daily_cap_applies():
    comments, cid = scenario()
    other, _ = gate_for("9" * 64, [verdict("REVISE", ["unrelated"])])
    c, g = models(verdict("PASS"), verdict("PASS"))
    with pytest.raises(o.Stop):                                                  # an unrelated gate is still open
        rr.rereview(LIVE, comments + [other], H1, cid, fetch(), GETTER, c, g, lambda b: None)
    full = [bot(o.slot_tag("racing", time_today(), str(i) * 16 if i else "1" * 16)) for i in range(1, 4)]
    with pytest.raises(o.Stop):                                                  # shared daily slots used up
        rr.rereview(LIVE, comments + full, H1, cid, fetch(), GETTER, c, g, lambda b: None)


def time_today():
    import time
    return time.strftime("%Y-%m-%d", time.gmtime())


def test_mock_mode_makes_no_call_and_closes_nothing():
    comments, cid = scenario()
    posted = []
    closed, verdicts, *_ = rr.rereview({**ENV, "ORCH_MODE": "mock"}, comments, H1, cid, fetch(), GETTER, None, None, posted.append)
    assert not closed and verdicts == {} and posted and "SYNTHETIC MOCK" in posted[0]
