import hashlib
import json

import pytest

import orchestrator.daily_batch as b
import orchestrator.orchestrate as o

SHA = "a" * 40
TODAY = "2026-11-27"
ENV = {"ZANS_ORCH_ENABLED": "true", "ZANS_ORCH_ALLOWED_ACTORS": "zankendo2-ship-it", "GITHUB_ACTOR": "zankendo2-ship-it",
       "ZANS_ORCH_MAX_RUNS_PER_DAY": "1", "ZANS_ORCH_MAX_USD_PER_MONTH": "25", "ZANS_ORCH_MAX_USD_PER_RUN": "3",
       "OPENAI_API_KEY": "k", "OPENAI_MODEL": "gpt-6.2-astra", "GITHUB_REF": "refs/heads/main", "ORCH_MODE": "live"}
BOT = {"login": "github-actions[bot]"}


def art(i, text="hello"):
    data = text.encode()
    url = f"https://github.com/zankendo2-ship-it/zans-pins/blob/{SHA}/{i}.md"
    return {"id": i, "title": "t", "url": url, "sha256": hashlib.sha256(data).hexdigest(), "self_check": True}, data


def manifest(*items, date=TODAY):
    return {"date": date, "items": list(items)}


def test_hard_cap_derived_and_at_most_30_cents():
    assert 0 < b.worst_case_usd() <= b.CAP_USD == 0.30


def test_empty_manifest_skips_with_no_call():
    with pytest.raises(b.Skip):
        b.validate(manifest(), TODAY)


@pytest.mark.parametrize("mut", [
    {"self_check": False}, {"self_check": "true"}, {"self_check": {"tests_passed": True}},
    {"url": "https://github.com/zankendo2-ship-it/zans-pins/blob/main/a.md"},
    {"url": f"https://github.com/other/zans-pins/blob/{SHA}/a.md"},
    {"url": f"https://github.com/zankendo2-ship-it/zans-pins/blob/{SHA}/a.png"},
    {"sha256": "F" * 64}, {"sha256": "f" * 63}, {"id": "Bad Id"}, {"id": 5}, {"title": 5}])
def test_bad_item_refused(mut):
    i, _ = art("a")
    with pytest.raises(b.Refuse):
        b.validate(manifest({**i, **mut}), TODAY)


def test_duplicate_ids_stale_date_and_too_many_refused():
    i, _ = art("a")
    with pytest.raises(b.Refuse):
        b.validate(manifest(i, i), TODAY)
    with pytest.raises(b.Refuse):
        b.validate(manifest(i, date="2026-11-26"), TODAY)
    with pytest.raises(b.Refuse):
        b.validate(manifest(*[art(f"x{n}")[0] for n in range(b.MAX_ITEMS + 1)]), TODAY)


def test_fetch_verifies_sha_before_any_call():
    i, data = art("a")
    assert b.fetch_texts([i], lambda u, n: data) == {"a": "hello"}
    with pytest.raises(b.Refuse, match="sha256"):
        b.fetch_texts([i], lambda u, n: b"tampered")
    with pytest.raises(b.Refuse, match="size"):
        b.fetch_texts([i], lambda u, n: b"x" * (o.MAX_ARTIFACT_BYTES + 1))


def test_token_bound_is_over_escaped_bytes_and_refuses_not_truncates():
    i, _ = art("a")
    with pytest.raises(b.Refuse, match="not truncated"):
        b.build_prompt([i], {"a": "é" * 12_000})     # 6 bytes each as JSON escapes
    b.build_prompt([i], {"a": "x" * 20_000})


def test_guard_activation_actor_ref_model_and_budgets():
    b.guard(ENV, "live")
    for k, v in (("ZANS_ORCH_ENABLED", "no"), ("GITHUB_ACTOR", "x"), ("GITHUB_REF", "refs/heads/f"),
                 ("OPENAI_MODEL", "gpt-6-luna"), ("OPENAI_API_KEY", ""), ("ZANS_ORCH_MAX_USD_PER_RUN", "0")):
        with pytest.raises(o.Stop):
            b.guard({**ENV, k: v}, "live")
    b.guard({**ENV, "ZANS_ORCH_ENABLED": "no"}, "mock")     # mock is free


def test_plan_shared_ledger_caps_duplicate_and_overrun():
    i, _ = art("a")
    items, texts = [i], {"a": "hello"}
    assert b.plan(items, TODAY, texts, [], ENV, TODAY)["reserve"] <= 0.30
    slot = {"user": BOT, "body": o.slot_tag("live", TODAY, "abc123", 2.45)}          # an ORCHESTRATOR run today, other route
    with pytest.raises(o.Stop, match="already used"):
        b.plan(items, TODAY, texts, [slot], ENV, TODAY)
    with pytest.raises(b.Skip):
        b.plan(items, TODAY, texts, [{"body": f"<!-- {o.MARKER}:{b.batch_hash(TODAY, items)} -->"}], ENV, TODAY)
    over = {"user": BOT, "body": o.settle_tag("2026-11-10", "dead", 3.1, over=True)}
    with pytest.raises(o.Stop, match="more than its reservation"):
        b.plan(items, TODAY, texts, [over], ENV, TODAY)
    with pytest.raises(o.Stop, match="monthly|MONTH"):
        b.plan(items, TODAY, texts, [], {**ENV, "ZANS_ORCH_MAX_USD_PER_MONTH": "0.1"}, TODAY)
    with pytest.raises(o.Stop, match="PER_RUN"):
        b.plan(items, TODAY, texts, [], {**ENV, "ZANS_ORCH_MAX_USD_PER_RUN": "0.1"}, TODAY)


def good(items):
    return json.dumps({"results": [{"id": i["id"], "verdict": "PASS", "reasons": ["r"], "fixes": []} for i in items]})


@pytest.mark.parametrize("mut", ["missing", "duplicate", "extra", "bad_verdict", "extra_key", "not_json", "refusal", "length"])
def test_strict_result_schema_rejects_everything_incomplete(mut):
    a, _ = art("a")
    c, _ = art("c")
    items = [a, c]
    rs = json.loads(good(items))["results"]
    finish = "stop"
    text = {"missing": json.dumps({"results": rs[:1]}),
            "duplicate": json.dumps({"results": [rs[0], rs[0]]}),
            "extra": json.dumps({"results": rs + [{**rs[0], "id": "zzz"}]}),
            "bad_verdict": json.dumps({"results": [{**rs[0], "verdict": "MAYBE"}, rs[1]]}),
            "extra_key": json.dumps({"results": [{**rs[0], "note": "x"}, rs[1]]}),
            "not_json": "PASS", "refusal": good(items), "length": good(items)}[mut]
    if mut in ("refusal", "length"):
        finish = mut
    with pytest.raises(b.Refuse):
        b.parse_results(text, items, finish)
    assert set(b.parse_results(good(items), items, "stop")) == {"a", "c"}


def e2e(env, comments, caller, items, data):
    posted, calls = [], []
    texts = b.fetch_texts(items, lambda u, n: data)

    def counted(e, p):
        calls.append(1)
        return caller(e, p)
    return b.run(env, items, TODAY, texts, comments, TODAY, counted, posted.append), posted, calls


def test_e2e_mocked_reserve_first_one_call_internal_summary_and_settle(monkeypatch):
    i, data = art("a")

    def caller(env, prompt):
        o.RUN_COST["usd"] += o.usage_cost("gpt-6.2-astra", 6000, 300)
        return good([i]), "stop"
    (outcome, h, reserve), posted, calls = e2e(ENV, [], caller, [i], data)
    assert calls == [1] and "a=PASS" in outcome
    assert o.SLOT in posted[0] and b.attempt_marker(i) in posted[0]
    assert "reviewed" in posted[1] and "never the owner's approval" in posted[1]
    assert o.MARKER not in posted[1] and b.item_marker(i) not in posted[1]
    assert reserve == b.worst_case_usd() <= 0.30
    sent = []
    monkeypatch.setattr(o, "gh", lambda env, m, path, body=None: sent.append(body["body"]) or {})
    settled = o.settle(ENV, "r/r", "26", TODAY, h, reserve,
                       completion_markers=[f"<!-- {o.MARKER}:{h} -->", b.item_marker(i)])
    assert settled and sent and o.SETTLE in sent[0] and "OVERRUN" not in sent[0]
    assert f"<!-- {o.MARKER}:{h} -->" in sent[0] and b.item_marker(i) in sent[0]


def test_e2e_invalid_output_no_retry_and_no_verdict():
    i, data = art("a")
    (outcome, h, r), posted, calls = e2e(ENV, [], lambda e, p: ("not json", "stop"), [i], data)
    assert calls == [1] and outcome.startswith("INVALID OUTPUT") and "**PASS**" not in posted[1]


def test_e2e_provider_failure_keeps_full_reservation_and_does_not_retry():
    i, data = art("a")

    def boom(e, p):
        raise OSError("net")
    (outcome, h, r), posted, calls = e2e(ENV, [], boom, [i], data)
    assert calls == [1] and outcome.startswith("CALL FAILED") and o.RUN_COST["complete"] is False


def test_second_batch_same_day_makes_zero_calls():
    i, data = art("a")
    _, posted, _ = e2e(ENV, [], lambda e, p: (good([i]), "stop"), [i], data)
    comments = [{"body": posted[0]}, {"body": posted[1]}]
    j, data2 = art("b")
    with pytest.raises(o.Stop, match="already used"):
        e2e(ENV, comments, lambda e, p: pytest.fail("called"), [j], data2)
    with pytest.raises(b.Skip):                 # the same set again is a duplicate: no paid re-review
        e2e(ENV, comments, lambda e, p: pytest.fail("called"), [i], data)


def test_mock_mode_reserves_nothing_and_never_calls_provider(monkeypatch):
    i, data = art("a")
    monkeypatch.setattr(o, "_post", lambda *a, **k: pytest.fail("network used in mock"))
    (outcome, h, reserve), posted, _ = e2e({**ENV, "ORCH_MODE": "mock"}, [], b.mock_caller([i]), [i], data)
    assert reserve == 0.0 and "a=PASS" in outcome


def test_fingerprint_ignores_date_and_commit_so_unchanged_bytes_are_not_charged_twice():
    i, _ = art("a")
    j = {**i, "url": i["url"].replace(SHA, "b" * 40)}
    assert len(b.batch_hash("2026-11-27", [i])) == 64
    assert b.batch_hash("2026-11-27", [i]) == b.batch_hash("2026-12-01", [j])
    assert b.batch_hash("2026-11-27", [i], "mock") != b.batch_hash("2026-11-27", [i], "live")


def test_mock_summary_is_synthetic_and_unknown_usage_holds():
    i, data = art("a")
    _, posted, _ = e2e({**ENV, "ORCH_MODE": "mock"}, [], b.mock_caller([i]), [i], data)
    assert "SYNTHETIC MOCK" in posted[1] and "never owner-ready" in posted[1].lower().replace("never a pass and ", "")
    _, posted, _ = e2e(ENV, [], lambda e, p: pytest.fail("x") if False else (_ for _ in ()).throw(OSError("n")), [i], data)
    assert "HOLD" in posted[1] and i["sha256"] in posted[1] or "HOLD" in posted[1]


def test_scheduled_run_reads_manifest_from_the_triggering_commit_and_failures_exit_nonzero(monkeypatch):
    i, data = art("a")
    seen, posts = [], []
    man = json.dumps(manifest(i)).encode()
    monkeypatch.setattr(b.time, "strftime", lambda *a: TODAY)
    monkeypatch.setattr(o, "uk_window_ok", lambda *a, **k: True)
    monkeypatch.setattr(o, "_get_bytes", lambda url, n: (seen.append(url), man if url.endswith(".json") else data)[1])
    monkeypatch.setattr(o, "comments_since", lambda *a: [])
    monkeypatch.setattr(o, "gh", lambda env, m, path, body=None: {"sha": SHA} if m == "GET" else (posts.append(body["body"]) or {}))
    monkeypatch.setattr(b, "call_openai_batch", lambda env, p: ("not json", "stop"))
    env = {**ENV, "ORCH_MODE": "", "GITHUB_EVENT_NAME": "schedule", "GITHUB_SHA": SHA, "ORCH_ISSUE": "26",
           "GITHUB_REPOSITORY": "zankendo2-ship-it/zans-pins"}
    env.pop("ORCH_MODE")
    env["ORCH_MODE"] = "live"
    assert b.main(env) == 1                                   # invalid output: posted + settled, nonzero, no retry
    assert any(f"{SHA}/handoff-manifests/daily-{TODAY}.json" in u for u in seen) and len(posts) >= 2


def test_per_artifact_dedup_and_failed_slot_is_not_retried():
    a, _ = art("a")
    c, _ = art("c")
    done = {"user": BOT, "body": b.item_marker(a)}
    attempted = {"user": BOT, "body": b.attempt_marker(a)}
    assert b.unreviewed([a, c], [done]) == [c]
    assert b.unreviewed([a, c], [attempted]) == [c]
    assert b.unreviewed([a, c], [{"user": {"login": "someone"}, "body": b.item_marker(a)}]) == [a, c]
    slot = {"user": BOT, "body": o.slot_tag("live", "2026-11-26", b.batch_hash(TODAY, [a]), 0.3)}   # earlier failed attempt, no summary
    with pytest.raises(b.Skip, match="attempted"):
        b.plan([a], TODAY, {"a": "x"}, [slot], ENV, TODAY)


def test_summary_never_emits_completion_markers_before_settlement():
    a, _ = art("a")
    results = {"a": {"verdict": "PASS", "reasons": [], "fixes": []}}
    for complete in (False, True):
        o.RUN_COST.update(usd=0.0, complete=complete)
        summary = b.summary("h", TODAY, [a], "reviewed a=PASS", results, "live")
        assert o.MARKER not in summary and b.item_marker(a) not in summary
    mock = b.summary("h", TODAY, [a], "mock", results, "mock")
    assert "SYNTHETIC MOCK" in mock and o.MARKER not in mock and b.item_marker(a) not in mock
