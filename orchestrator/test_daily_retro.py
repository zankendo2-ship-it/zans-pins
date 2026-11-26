import hashlib
import json

import pytest

import orchestrator.daily_retro as r
import orchestrator.orchestrate as o

TODAY = "2026-11-26"
ENV = {"ZANS_ORCH_ENABLED": "true", "ZANS_ORCH_ALLOWED_ACTORS": "zankendo2-ship-it", "GITHUB_ACTOR": "zankendo2-ship-it",
       "ZANS_ORCH_MAX_RUNS_PER_DAY": "3", "ZANS_ORCH_MAX_USD_PER_MONTH": "25", "ZANS_ORCH_MAX_USD_PER_RUN": "3",
       "ANTHROPIC_API_KEY": "k", "OPENAI_API_KEY": "k", "ANTHROPIC_MODEL": "claude-sonnet-5-5", "OPENAI_MODEL": "gpt-6.2-astra",
       "GITHUB_REF": "refs/heads/main", "ORCH_MODE": "live", "GITHUB_EVENT_NAME": "workflow_dispatch"}


def data(n=8000):
    return ("2026-11-26 retrospective. " + "race line\n" * 2000)[:n].encode()


def sha(d):
    return hashlib.sha256(d).hexdigest()


def verdict(v="PASS"):
    return json.dumps({"ack": "ok", "verdict": v, "reasons": ["r"], "fixes": []})


def callers(c1="PASS", o2="REVISE", c3="PASS", model_c="claude-sonnet-5-5"):
    calls, seq = [], {"Claude": [c1, c3], "OpenAI": [o2]}

    def make(who, stopv, model):
        def f(e, t):
            calls.append(who)
            o.LAST_STOP[who] = stopv
            o.LAST_USAGE[who] = (model, 4000, 400)
            return verdict(seq[who].pop(0))
        return f
    return calls, make("Claude", "end_turn", model_c), make("OpenAI", "stop", "gpt-6.2-astra")


def test_reserve_is_bounded_and_cheap_in_reality():
    d = data(10000)
    assert r.worst_case_usd(d.decode()) <= r.CAP_USD == 0.60
    assert o.usage_cost("claude-sonnet-5-5", 4000, 400) * 2 + o.usage_cost("gpt-6.2-astra", 4000, 400) < 0.15


@pytest.mark.parametrize("d,s", [(data(), "0" * 64), (data(), "xyz"), (data(10_001), None), (b"\xff\xfe", None),
                                 (b"no date here", None), (b"2026-11-26 sk-" + b"a" * 30, None)])
def test_validate_refuses(d, s):
    with pytest.raises(r.Refuse):
        r.validate(d, s if s is not None else sha(d))


def test_plan_rules_one_slot_date_lock_and_month():
    d = data()
    r.plan(d, sha(d), [], ENV, TODAY)
    with pytest.raises(o.Stop, match="only for"):
        r.plan(d, sha(d), [], ENV, "2026-11-27")
    h = sha(d)[:16]
    with pytest.raises(o.Stop, match="already attempted"):
        r.plan(d, sha(d), [{"body": o.slot_tag("retro", TODAY, h, 0.5)}], ENV, TODAY)
    d2 = data(7000)
    with pytest.raises(o.Stop, match="already used"):
        r.plan(d2, sha(d2), [{"body": o.slot_tag("retro", TODAY, "deadbeef", 0.5)}], ENV, TODAY)
    # does NOT use or block the other routes' daily runs
    r.plan(d, sha(d), [{"body": o.slot_tag("live", TODAY, "abc123", 2.45)}, {"body": o.slot_tag("racing", TODAY, "beef", 0.7)}], ENV, TODAY)
    big = [{"body": o.slot_tag("live", "2026-11-%02d" % n, "%x" % (n + 100), 1.0)} for n in range(1, 26)]
    with pytest.raises(o.Stop, match="MONTH"):
        r.plan(d, sha(d), big, ENV, TODAY)
    with pytest.raises(o.Stop, match="PER_RUN"):
        r.plan(d, sha(d), [], {**ENV, "ZANS_ORCH_MAX_USD_PER_RUN": "0.3"}, TODAY)


def test_mock_free_ignores_ledger_and_date():
    d = data()
    posted = []
    env = {**ENV, "ORCH_MODE": "mock", "ZANS_ORCH_MAX_USD_PER_MONTH": "0.01"}
    v, h, reserve, bad = r.run(env, d, sha(d), [{"body": o.slot_tag("retro", TODAY, "ab", 1)}], "2026-12-01", None, None, posted.append)
    assert v == {} and reserve == 0.0 and "SYNTHETIC MOCK" in posted[0] and o.SLOT not in posted[0]


def test_live_three_calls_in_order_slot_first_exact_replies_and_marker():
    d = data()
    calls, c, oa = callers()
    posted = []
    steps, h, reserve, bad = r.run(ENV, d, sha(d), [], TODAY, c, oa, posted.append)
    assert calls == ["Claude", "OpenAI", "Claude"] and not bad and set(steps) == {1, 2, 3}
    assert o.SLOT in posted[0] and f"<!-- {o.MARKER}:{h} -->" in posted[1]
    assert "1. Claude" in posted[1] and "2. ChatGPT: challenge: REVISE" in posted[1] and "3. Claude" in posted[1]


@pytest.mark.parametrize("c1,expected", [("REJECT", ["Claude"]), ("BLOCKER", ["Claude"])])
def test_stop_on_first_reject_or_blocker(c1, expected):
    d = data()
    calls, c, oa = callers(c1=c1)
    posted = []
    steps, h, reserve, bad = r.run(ENV, d, sha(d), [], TODAY, c, oa, posted.append)
    assert calls == expected and bad and "HOLD" in posted[1] and f"<!-- {o.MARKER}:" not in posted[1]


def test_openai_reject_stops_third_call_and_unknown_model_holds():
    d = data()
    calls, c, oa = callers(o2="REJECT")
    steps, *_ = r.run(ENV, d, sha(d), [], TODAY, c, oa, [].append)
    assert calls == ["Claude", "OpenAI"] and set(steps) == {1, 2}
    calls, c, oa = callers(model_c="unverified:x")
    posted = []
    r.run(ENV, d, sha(d), [], TODAY, c, oa, posted.append)
    assert calls == ["Claude"] and o.RUN_COST["complete"] is False and "HOLD" in posted[1]


def test_main_refuses_schedule_and_runs_dispatch_end_to_end(monkeypatch):
    d = data()
    assert r.main({**ENV, "GITHUB_EVENT_NAME": "schedule", "ORCH_ISSUE": "26"}) == 1
    posts, settles = [], []
    sha_c = "c" * 40
    monkeypatch.setattr(r.time, "strftime", lambda *a: TODAY)
    monkeypatch.setattr(o, "gh", lambda env, m, path, body=None: {"sha": sha_c} if m == "GET" else (posts.append(body["body"]) or {}))
    monkeypatch.setattr(o, "_get_bytes", lambda url, limit: d if sha_c in url and url.endswith(r.PATH) else pytest.fail(url))
    monkeypatch.setattr(o, "comments_since", lambda *a, **k: [])
    monkeypatch.setattr(o, "settle", lambda *a: settles.append(a))
    calls, c, oa = callers()
    monkeypatch.setattr(o, "call_claude", c)
    monkeypatch.setattr(o, "call_openai", oa)
    env = {**ENV, "ORCH_ISSUE": "26", "GITHUB_REPOSITORY": "zankendo2-ship-it/zans-pins", "RETRO_SHA256": sha(d)}
    assert r.main(env) == 0 and calls == ["Claude", "OpenAI", "Claude"] and len(posts) == 2 and len(settles) == 1
    assert r.main({**env, "RETRO_SHA256": "0" * 64}) == 1       # wrong typed hash: refused, no call
