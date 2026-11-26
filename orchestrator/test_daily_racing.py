import json

import pytest

import orchestrator.daily_racing as r
import orchestrator.orchestrate as o

TODAY = "2026-11-27"
ENV = {"ZANS_ORCH_ENABLED": "true", "ZANS_ORCH_ALLOWED_ACTORS": "zankendo2-ship-it", "GITHUB_ACTOR": "zankendo2-ship-it",
       "ZANS_ORCH_MAX_RUNS_PER_DAY": "3", "ZANS_ORCH_MAX_USD_PER_MONTH": "25", "ZANS_ORCH_MAX_USD_PER_RUN": "3",
       "ANTHROPIC_API_KEY": "k", "OPENAI_API_KEY": "k", "ANTHROPIC_MODEL": "claude-sonnet-5-5", "OPENAI_MODEL": "gpt-6.2-astra",
       "GITHUB_REF": "refs/heads/main", "ORCH_MODE": "live"}
BOT = {"login": "github-actions[bot]"}


def file_bytes(**kw):
    d = {"date": TODAY, "made_utc": "x", "picks": [], "table": [{"course": "Ascot", "time": "13:00", "ZANS": "A"}]}
    d.update(kw)
    return json.dumps(d).encode()


def good(e, t):
    return json.dumps({"ack": "ok", "verdict": "PASS", "reasons": ["r"], "fixes": []})


def setup(model_c="claude-sonnet-5-5", model_o="gpt-6.2-astra"):
    def claude(e, t):
        o.LAST_STOP["Claude"] = "end_turn"
        o.LAST_USAGE["Claude"] = (model_c, 3000, 300)
        return good(e, t)

    def openai(e, t):
        o.LAST_STOP["OpenAI"] = "stop"
        o.LAST_USAGE["OpenAI"] = (model_o, 3000, 300)
        return good(e, t)
    return claude, openai


def test_cap_is_under_80_cents_and_small_file_costs_cents():
    assert 0 < r.worst_case_usd() <= r.CAP_USD == 0.80
    assert o.usage_cost("claude-sonnet-5-5", 3000, 300) + o.usage_cost("gpt-6.2-astra", 3000, 300) < 0.10


@pytest.mark.parametrize("data", [b"x" * 70_000, b"\xff\xfe", b"[]", file_bytes(date="2026-11-26"),
                                  file_bytes(table=[]), file_bytes(notes="sk-" + "a" * 30)])
def test_bad_file_refused(data):
    with pytest.raises(r.Refuse):
        r.plan(data, [], ENV, TODAY)


def test_ledger_separate_racing_slot_shared_month_and_dedup():
    data = file_bytes()
    r.plan(data, [], ENV, TODAY)
    batch_slot = {"body": o.slot_tag("live", TODAY, "abc123", 0.3)}
    r.plan(data, [batch_slot], ENV, TODAY)              # a batch run today does NOT block the racing run
    h = r.fingerprint(data)[:16]
    with pytest.raises(r.Skip):                           # same file, attempted: no auto retry
        r.plan(data, [{"body": o.slot_tag("racing", TODAY, h, 0.7)}], ENV, TODAY)
    other = {"body": o.slot_tag("racing", TODAY, "deadbeef", 0.7)}
    with pytest.raises(o.Stop, match="already used"):
        r.plan(file_bytes(made_utc="y"), [other], ENV, TODAY)
    with pytest.raises(o.Stop, match="MONTH"):
        r.plan(data, [], {**ENV, "ZANS_ORCH_MAX_USD_PER_MONTH": "0.5"}, TODAY)
    # racing slots count against the shared month
    big = [{"body": o.slot_tag("racing", "2026-11-%02d" % d, "%x" % (d + 100), 1.0)} for d in range(1, 27)]
    with pytest.raises(o.Stop, match="MONTH"):
        r.plan(data, big, ENV, TODAY)


def test_e2e_two_calls_slot_first_settle_and_advisory_summary(monkeypatch):
    posted = []
    claude, openai = setup()
    v, h, reserve, bad = r.run(ENV, file_bytes(), [], TODAY, claude, openai, posted.append)
    assert not bad and set(v) == {"Claude", "ChatGPT"} and o.SLOT in posted[0] and ":racing:" in posted[0]
    assert "never changes a pick" in posted[1] and "HOLD" not in posted[1]
    sent = []
    monkeypatch.setattr(o, "gh", lambda env, m, path, body=None: sent.append(body["body"]) or {})
    o.settle(ENV, "r/r", "26", TODAY, h, reserve)
    assert sent and "OVERRUN" not in sent[0]


def test_failed_call_is_blocker_hold_and_never_retried():
    posted, calls = [], []
    claude, _ = setup()

    def boom(e, t):
        calls.append(1)
        raise OSError("net")
    v, h, reserve, bad = r.run(ENV, file_bytes(), [], TODAY, claude, boom, posted.append)
    assert bad and v["ChatGPT"]["verdict"] == "BLOCKER" and calls == [1] and o.RUN_COST["complete"] is False
    assert "HOLD" in posted[1]


def test_unverified_served_model_holds():
    posted = []
    claude, openai = setup(model_o="unverified:other")
    r.run(ENV, file_bytes(), [], TODAY, claude, openai, posted.append)
    assert o.RUN_COST["complete"] is False and "HOLD" in posted[1]


def test_mock_is_synthetic_and_reserves_nothing(monkeypatch):
    monkeypatch.setattr(o, "_post", lambda *a, **k: pytest.fail("network in mock"))
    posted = []
    v, h, reserve, bad = r.run({**ENV, "ORCH_MODE": "mock"}, file_bytes(), [], TODAY, r.mock_caller, r.mock_caller, posted.append)
    assert reserve == 0.0 and "SYNTHETIC MOCK" in posted[1]


def test_scheduled_main_reads_file_at_resolved_sha_and_exits_nonzero_on_failure(monkeypatch):
    seen, posts = [], []
    sha = "c" * 40
    monkeypatch.setattr(r.time, "strftime", lambda *a: TODAY)
    monkeypatch.setattr(o, "gh", lambda env, m, path, body=None: {"sha": sha} if m == "GET" else (posts.append(body["body"]) or {}))
    monkeypatch.setattr(o, "_get_bytes", lambda url, n: (seen.append(url), file_bytes())[1])
    monkeypatch.setattr(o, "comments_since", lambda *a: [])
    claude, _ = setup()

    def bad_openai(e, t):
        raise OSError("x")
    monkeypatch.setattr(o, "call_claude", claude)
    monkeypatch.setattr(o, "call_openai", bad_openai)
    env = {**ENV, "GITHUB_EVENT_NAME": "schedule", "ZANS_RACING_SCHEDULE": "true", "ORCH_ISSUE": "26",
           "GITHUB_REPOSITORY": "zankendo2-ship-it/zans-pins"}
    assert r.main(env) == 1
    assert seen == [f"https://raw.githubusercontent.com/zankendo2-ship-it/zans-pins/{sha}/racing-review/{TODAY}.json"]
    assert r.main({**env, "ZANS_RACING_SCHEDULE": "no"}) == 0   # schedule switch off = disabled, no call


def test_no_file_today_makes_zero_calls(monkeypatch):
    monkeypatch.setattr(o, "gh", lambda env, m, path, body=None: {"sha": "c" * 40})
    monkeypatch.setattr(o, "_get_bytes", lambda url, n: (_ for _ in ()).throw(OSError("404")))
    monkeypatch.setattr(o, "call_claude", lambda *a: pytest.fail("called"))
    env = {**ENV, "GITHUB_EVENT_NAME": "schedule", "ZANS_RACING_SCHEDULE": "true", "ORCH_ISSUE": "26", "GITHUB_REPOSITORY": "a/b"}
    assert r.main(env) == 0
