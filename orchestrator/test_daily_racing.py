import json

import pytest

import orchestrator.daily_racing as r
import orchestrator.orchestrate as o

TODAY = "2026-11-27"
ENV = {"ZANS_ORCH_ENABLED": "true", "ZANS_ORCH_ALLOWED_ACTORS": "zankendo2-ship-it", "GITHUB_ACTOR": "zankendo2-ship-it",
       "ZANS_ORCH_MAX_RUNS_PER_DAY": "1", "ZANS_ORCH_MAX_USD_PER_MONTH": "25", "ZANS_ORCH_MAX_USD_PER_RUN": "3",
       "ANTHROPIC_API_KEY": "k", "OPENAI_API_KEY": "k", "ANTHROPIC_MODEL": "claude-sonnet-5-5", "OPENAI_MODEL": "gpt-6.2-astra",
       "GITHUB_REF": "refs/heads/main", "ORCH_MODE": "live"}
BOT = {"login": "github-actions[bot]"}


RACE = {"time": "13:00", "course": "Ascot", "win_pick": "A", "confidence": "8", "status": "RUNNER", "sky_bet_price": 2.5,
        "best_price": 2.5, "no_sky_price": False, "data_pick": "A", "agent_b": None, "gemini_api": None}


import hashlib
SRCS = {"sent/3_d0_morning_0845/predictions.json": b'{"p": 1}', "sent/3_d0_morning_0845/betslip.json": b'{"b": 2}',
        "reports/price_stages/2026-11-27/d0_0815.csv": b"course,time,horse,price\nAscot,13:00,A,2.5\n"}
PRICE_PATH = "reports/price_stages/2026-11-27/d0_0815.csv"
SOURCES = [{"path": k, "sha256": hashlib.sha256(v).hexdigest()} for k, v in SRCS.items()]
GETTER = lambda commit, path: SRCS[path]   # noqa: E731


def file_bytes(**kw):
    d = {"date": TODAY, "frozen_at_utc": TODAY + "T08:45:00Z", "built_utc": TODAY + "T08:50:00Z", "pack": "3_d0_morning_0845",
          "pack_manifest_combined_sha256": r.combined_sha256(SOURCES), "racing_branch_commit": "b" * 40,
          "prices_file": PRICE_PATH, "sources": SOURCES, "races": [RACE]}
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
                                  file_bytes(races=[]), file_bytes(notes="sk-" + "a" * 30),
                                  file_bytes(pack=""), file_bytes(frozen_at_utc=5), file_bytes(frozen_at_utc="2026-11-25T08:45:00Z"),
                                  file_bytes(pack_manifest_combined_sha256="xyz"), file_bytes(racing_branch_commit=""),
                                  file_bytes(races=[RACE, {**RACE, "course": "ascot"}]),
                                  file_bytes(races=[{"course": "Ascot"}]),
                                  file_bytes(races=[{k: v for k, v in RACE.items() if k != "win_pick"}]),
                                  file_bytes(races=[{k: v for k, v in RACE.items() if k != "sky_bet_price"}])])
def test_bad_file_refused(data):
    with pytest.raises(r.Refuse):
        r.plan(data, [], ENV, TODAY)


def test_empty_picks_make_no_call():
    with pytest.raises(r.Skip):
        r.plan(file_bytes(races=[{**RACE, "win_pick": None, "status": "no pick"}]), [], ENV, TODAY)


ONE = {**ENV, "ZANS_ORCH_MAX_RUNS_PER_DAY": "1"}   # owner hard cap: one shared paid slot per UTC day


def test_global_paid_slot_blocks_products_and_racing_cross_route():
    data = file_bytes()
    batch_slot = {"user": BOT, "body": o.slot_tag("live", TODAY, "b" * 64, 0.3)}
    with pytest.raises(o.Stop, match="shared one paid run"):
        r.plan(data, [batch_slot], ONE, TODAY)
    h = r.fingerprint(data)
    assert len(h) == 64
    with pytest.raises(r.Skip):
        r.plan(data, [{"user": BOT, "body": o.slot_tag("racing", TODAY, h, 0.7)}], ONE, TODAY)
    racing_slot = {"user": BOT, "body": o.slot_tag("racing", TODAY, "c" * 64, 0.7)}
    with pytest.raises(o.Stop, match="shared one paid run"):
        r.plan(file_bytes(frozen_at_utc=TODAY + "T08:46:00Z"), [racing_slot], ONE, TODAY)
    import orchestrator.daily_batch as b
    with pytest.raises(o.Stop, match="shared one paid run"):
        b.plan([{"id": "a", "url": "u", "sha256": "f" * 64}], TODAY, {"a": "x"}, [racing_slot], ONE, TODAY)
    with pytest.raises(o.Stop, match="MONTH"):
        r.plan(data, [], {**ONE, "ZANS_ORCH_MAX_USD_PER_MONTH": "0.5"}, TODAY)
    big = [{"user": BOT, "body": o.slot_tag("racing", "2026-11-%02d" % d, "%064x" % (d + 100), 1.0)} for d in range(1, 27)]
    with pytest.raises(o.Stop, match="MONTH"):
        r.plan(data, big, ONE, TODAY)


def test_e2e_two_calls_slot_first_settle_and_advisory_summary(monkeypatch):
    posted = []
    claude, openai = setup()
    v, h, reserve, bad = r.run(ENV, file_bytes(), [], TODAY, claude, openai, posted.append, GETTER)
    assert not bad and set(v) == {"Claude", "ChatGPT"} and o.SLOT in posted[0] and ":racing:" in posted[0]
    assert len(h) == 64 and h in posted[0]
    assert "never changes a pick" in posted[1] and "HOLD" not in posted[1] and "INDEPENDENT calls" in posted[1]
    assert o.MARKER not in posted[1]
    sent = []
    monkeypatch.setattr(o, "gh", lambda env, m, path, body=None: sent.append(body["body"]) or {})
    settled = o.settle(ENV, "r/r", "26", TODAY, h, reserve,
                       completion_markers=[f"<!-- {o.MARKER}:{h} -->"])
    assert settled and sent and "OVERRUN" not in sent[0] and f"<!-- {o.MARKER}:{h} -->" in sent[0]


def test_first_failure_stops_before_the_second_provider_and_holds():
    posted, calls = [], []

    def boom(e, t):
        calls.append("claude")
        raise OSError("net")
    _, openai = setup()
    o2 = lambda e, t: calls.append("openai") or openai(e, t)   # noqa: E731
    v, h, reserve, bad = r.run(ENV, file_bytes(), [], TODAY, boom, o2, posted.append, GETTER)
    assert bad and set(v) == {"Claude"} and calls == ["claude"] and o.RUN_COST["complete"] is False
    assert "HOLD" in posted[1] and f"<!-- {o.MARKER}:" not in posted[1]
    posted2 = []
    claude, bad_openai = setup()[0], (lambda e, t: (_ for _ in ()).throw(OSError("x")))
    v, h, reserve, bad = r.run(ENV, file_bytes(), [], TODAY, claude, bad_openai, posted2.append, GETTER)
    assert bad and v["ChatGPT"]["verdict"] == "BLOCKER" and "HOLD" in posted2[1]


def test_unverified_served_model_holds():
    posted = []
    claude, openai = setup(model_c="unverified:other")
    v, *_ = r.run(ENV, file_bytes(), [], TODAY, claude, openai, posted.append, GETTER)
    assert o.RUN_COST["complete"] is False and "HOLD" in posted[1] and set(v) == {"Claude"}   # second provider not called


def test_mock_is_synthetic_and_reserves_nothing(monkeypatch):
    monkeypatch.setattr(o, "_post", lambda *a, **k: pytest.fail("network in mock"))
    posted = []
    v, h, reserve, bad = r.run({**ENV, "ORCH_MODE": "mock"}, file_bytes(), [], TODAY, None, None, posted.append, GETTER)
    assert reserve == 0.0 and v == {} and len(posted) == 1 and "SYNTHETIC MOCK" in posted[0]
    assert o.SLOT not in posted[0] and f"<!-- {o.MARKER}" not in posted[0]     # no slot, no dedup marker


def test_scheduled_main_reads_file_at_resolved_sha_and_exits_nonzero_on_failure(monkeypatch):
    seen, posts = [], []
    sha = "c" * 40
    monkeypatch.setattr(r.time, "strftime", lambda *a: TODAY)
    monkeypatch.setattr(o, "uk_window_ok", lambda *a, **k: True)
    monkeypatch.setattr(o, "gh", lambda env, m, path, body=None: {"sha": sha} if m == "GET" else (posts.append(body["body"]) or {}))
    def fetch(url, n):
        for path, body in SRCS.items():     # pack source files, fetched at the commit named in the sealed file
            if url == f"https://raw.githubusercontent.com/zankendo2-ship-it/zans-pins/{'b' * 40}/{path}":
                return body
        seen.append(url)
        return file_bytes()
    monkeypatch.setattr(o, "_get_bytes", fetch)
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


def test_dst_gate_runs_only_the_cron_entry_inside_the_uk_window():
    from datetime import datetime, timezone
    u = lambda *a: datetime(*a, tzinfo=timezone.utc)   # noqa: E731
    assert o.uk_window_ok(*r.UK_WINDOW, now_utc=u(2026, 11, 27, 8, 55))        # winter: 08:55 UTC = 08:55 UK
    assert not o.uk_window_ok(*r.UK_WINDOW, now_utc=u(2026, 11, 27, 7, 55))    # winter: the summer line is skipped
    assert o.uk_window_ok(*r.UK_WINDOW, now_utc=u(2027, 6, 15, 7, 55))         # summer: 07:55 UTC = 08:55 BST
    assert not o.uk_window_ok(*r.UK_WINDOW, now_utc=u(2027, 6, 15, 8, 55))     # summer: the winter line is skipped
    import orchestrator.daily_batch as b
    assert o.uk_window_ok(*b.UK_WINDOW, now_utc=u(2026, 11, 27, 9, 10)) and not o.uk_window_ok(*b.UK_WINDOW, now_utc=u(2027, 6, 15, 9, 10))


def test_scheduled_run_outside_window_makes_no_call(monkeypatch):
    monkeypatch.setattr(o, "uk_window_ok", lambda *a, **k: False)
    monkeypatch.setattr(o, "call_claude", lambda *a: pytest.fail("called"))
    env = {**ENV, "GITHUB_EVENT_NAME": "schedule", "ZANS_RACING_SCHEDULE": "true", "ORCH_ISSUE": "26", "GITHUB_REPOSITORY": "a/b"}
    assert r.main(env) == 0


def test_claude_reject_makes_no_second_call():
    calls, posted = [], []
    claude, openai = setup()
    rej = lambda e, t: (claude(e, t), json.dumps({"ack": "ok", "verdict": "REJECT", "reasons": ["bad"], "fixes": []}))[1]  # noqa: E731
    v, h, reserve, bad = r.run(ENV, file_bytes(), [], TODAY, rej, lambda e, t: calls.append("openai") or openai(e, t), posted.append, GETTER)
    assert calls == [] and set(v) == {"Claude"} and bad


def test_mock_ignores_paid_ledger_caps_and_slots(monkeypatch):
    import orchestrator.daily_batch as b
    full = [{"user": BOT, "body": o.slot_tag("racing", TODAY, "deadbeef", 0.7)}, {"user": BOT, "body": o.slot_tag("live", TODAY, "abc123", 0.3)}]
    big = [{"user": BOT, "body": o.slot_tag("racing", "2026-11-%02d" % d, "%064x" % (d + 100), 1.0)} for d in range(1, 27)]
    env = {**ENV, "ORCH_MODE": "mock", "ZANS_ORCH_MAX_USD_PER_MONTH": "0.1"}
    p = r.plan(file_bytes(), full + big, env, TODAY)
    assert p["hash"] and p["prompt"]
    b.plan([{"id": "a", "url": "u", "sha256": "f" * 64}], TODAY, {"a": "x"}, full + big, env, TODAY)
    with pytest.raises(o.Stop):                                   # live is still blocked by the same ledger
        r.plan(file_bytes(), full + big, {**env, "ORCH_MODE": "live"}, TODAY)


def test_real_racing_exporter_fixture_passes_consumer_offline_zero_provider_calls():
    import pathlib
    raw = pathlib.Path(__file__).with_name("fixtures").joinpath("racing_2026-11-26.json").read_bytes()
    boom = lambda *a, **k: pytest.fail("provider call in an offline mock")   # noqa: E731
    posted = []
    env = {**ENV, "ORCH_MODE": "mock"}
    v, h, reserve, bad = r.run(env, raw, [], "2026-11-26", boom, boom, posted.append, GETTER)
    assert v == {} and len(posted) == 1 and "SYNTHETIC MOCK" in posted[0]
    p = r.plan(raw, [], env, "2026-11-26")
    assert len(json.loads(raw)["races"]) == 35 and p["prompt"]


def test_mock_main_real_fixture_no_provider_calls(monkeypatch):
    import pathlib
    raw = pathlib.Path(__file__).with_name("fixtures").joinpath("racing_2026-11-26.json").read_bytes()
    posts = []
    monkeypatch.setattr(r.time, "strftime", lambda *a: "2026-11-26")
    monkeypatch.setattr(o, "gh", lambda env, m, path, body=None: {"sha": "c" * 40} if m == "GET" else (posts.append(body["body"]) or {}))
    monkeypatch.setattr(o, "_get_bytes", lambda url, n: raw)
    monkeypatch.setattr(o, "comments_since", lambda *a: [])
    monkeypatch.setattr(o, "call_claude", lambda *a: pytest.fail("paid provider called in mock"))
    monkeypatch.setattr(o, "call_openai", lambda *a: pytest.fail("paid provider called in mock"))
    env = {**ENV, "ORCH_MODE": "mock", "ZANS_ORCH_ENABLED": "false", "ORCH_ISSUE": "26",
           "GITHUB_REPOSITORY": "zankendo2-ship-it/zans-pins", "GITHUB_EVENT_NAME": "workflow_dispatch"}
    assert r.main(env) == 0
    assert len(posts) == 1 and "SYNTHETIC MOCK" in posts[0] and o.SLOT not in posts[0]


def test_source_url_uses_the_pinned_racing_data_repository():
    assert r.source_url("a" * 40, "reports/predictions/x.json") == (
        "https://raw.githubusercontent.com/zankendo2-ship-it/zans-pins/"
        + "a" * 40 + "/reports/predictions/x.json"
    )


def test_source_bytes_and_combined_hash_are_verified_before_any_slot():
    assert r.verify_sources(file_bytes(), GETTER) == 3
    for bad in (file_bytes(sources=None), file_bytes(sources=[]),
                file_bytes(pack_manifest_combined_sha256="0" * 64),
                file_bytes(sources=[{**SOURCES[0], "sha256": "0" * 64}, SOURCES[1]]),
                file_bytes(sources=[{**SOURCES[0], "path": "../x"}, SOURCES[1]]),
                file_bytes(prices_file="reports/price_stages/unsealed.csv"),
                file_bytes(sources=[SOURCES[0], SOURCES[0]])):
        with pytest.raises(r.Refuse):
            r.verify_sources(bad, GETTER)
    with pytest.raises(r.Refuse):
        r.verify_sources(file_bytes(), lambda c, p: b"tampered")
    posted = []
    with pytest.raises(r.Refuse):   # live run with tampered bytes: refused before the slot comment, zero calls
        r.run(ENV, file_bytes(), [], TODAY, None, None, posted.append, lambda c, p: b"tampered")
    assert posted == []


def test_revise_opens_a_gate_and_is_not_complete():
    claude, openai = setup()
    def revise(e, t):
        o.LAST_STOP["OpenAI"] = "stop"
        o.LAST_USAGE["OpenAI"] = ("gpt-6.2-astra", 3000, 300)
        return json.dumps({"ack": "x", "verdict": "REVISE", "reasons": ["bad"], "fixes": ["fix the pick"]})
    posted = []
    verdicts, h, reserve, bad = r.run(ENV, file_bytes(), [], TODAY, claude, revise, posted.append, GETTER)
    assert bad and f"{o.CORRECTION}:{h}:" in posted[-1] and "1 fixes" in posted[-1]
    gate = {"user": {"login": o.TRUSTED_SETTLER}, "body": posted[-1], "created_at": "2026-11-27T05:00:00Z"}
    with pytest.raises(o.Stop, match="correction gate"):
        o.require_no_pending_corrections([gate])


def test_review_task_demands_a_short_reply_under_the_output_cap():
    # 27 Nov live run 45982259588: a long Claude reply hit max_tokens (BLOCKER). The prompt must ask for brevity.
    assert "KEEP THE REPLY SHORT" in r.REVIEW_TASK and "at most 6 reasons" in r.REVIEW_TASK


V2_ROW = {**RACE, "second": None, "agent_b": "A", "data_gap": False, "price_move": None, "rpr_pick": "A", "rpr_reason": "r", "longshot": None}


def test_schema_v2_files_need_every_reviewable_field_or_explicit_null():
    day = "2026-11-28"
    ok = file_bytes(date=day, frozen_at_utc=day + "T08:45:00Z", races=[V2_ROW])
    assert r.validate(ok, day)
    for drop in r.V2_RACE_FIELDS:
        row = {k: v for k, v in V2_ROW.items() if k != drop}
        with pytest.raises(r.Refuse):
            r.validate(file_bytes(date=day, frozen_at_utc=day + "T08:45:00Z", races=[row]), day)
    gap = {**V2_ROW, "data_gap": True, "confidence": "8"}
    with pytest.raises(r.Refuse):                                   # uncapped data-gap pick
        r.validate(file_bytes(date=day, frozen_at_utc=day + "T08:45:00Z", races=[gap]), day)
    assert r.validate(file_bytes(date=day, frozen_at_utc=day + "T08:45:00Z", races=[{**gap, "confidence_capped": 6}]), day)
    # earlier-dated files (27 Nov) keep the old schema
    assert r.validate(file_bytes(), TODAY)


def big_file(n=40, reason=900, **kw):
    rows = [{**RACE, "course": f"C{i}", "time": f"13:{i:02d}", "zans_reasons": f"r{i} " + "x" * reason, "cautions": f"c{i}"} for i in range(n)]
    return file_bytes(races=rows, **kw)


def test_big_file_is_split_by_race_nothing_dropped_each_prompt_under_the_cap():
    data = big_file()
    text = r.validate(data, TODAY)
    ps = r.build_prompts(text)
    n = len(ps)
    assert 2 <= n <= r.MAX_CHUNKS
    seen = []
    for i, p in enumerate(ps, 1):
        assert r._bound(p) <= r.MAX_INPUT_TOKENS and f"chunk {i} of {n}" in p and "CHUNKED REVIEW" in p
        seen += [x for x in range(40) if f'"course": "C{x}"' in p]
    assert sorted(seen) == list(range(40))                       # every race exactly once
    assert all(f"r{x} " + "x" * 900 in "".join(ps) for x in range(40))   # full per-race detail kept, no truncation
    one = r.build_prompts(r.validate(file_bytes(), TODAY))
    assert len(one) == 1 and "CHUNKED" not in one[0]            # small file: identical single prompt as before


def test_chunk_cap_and_oversize_row_refused():
    with pytest.raises(r.Refuse):
        r.build_prompts(r.validate(big_file(n=60, reason=1400), TODAY))   # needs more than 3 chunks
    row = {**RACE, "zans_reasons": "y" * 40_000}
    with pytest.raises((r.Refuse, o.Stop)):
        r.build_prompts(json.dumps({**json.loads(file_bytes()), "races": [row]}))


def test_chunked_run_reserves_per_chunk_calls_each_chunk_both_providers_and_merges_worst():
    data = big_file()
    n = len(r.build_prompts(r.validate(data, TODAY)))
    posted, calls = [], []
    claude, openai = setup()
    c2 = lambda e, t: calls.append("c") or claude(e, t)    # noqa: E731
    o2 = lambda e, t: calls.append("o") or openai(e, t)    # noqa: E731
    v, h, reserve, bad = r.run(ENV, data, [], TODAY, c2, o2, posted.append, GETTER)
    assert not bad and calls == ["c", "o"] * n and reserve == r.worst_case_usd(n) <= r.CAP_USD * n
    assert set(v) == {"Claude", "ChatGPT"} and f"worst case ${reserve:.2f}" in posted[0]
    # worst verdict wins; a reviewer that skipped a chunk can never PASS
    a = {"ack": "a", "verdict": "PASS", "reasons": ["ok"], "fixes": []}
    b = {"ack": "b", "verdict": "REVISE", "reasons": ["bad"], "fixes": ["f1", "f1", "f2", "f3", "f4"]}
    m = r.merge([a, b], 2)
    assert m["verdict"] == "REVISE" and m["fixes"] == ["f1", "f2", "f3"] and m["reasons"] == ["[1/2] ok", "[2/2] bad"]
    assert r.merge([a], 2)["verdict"] == "BLOCKER"


def test_chunked_failure_in_a_later_chunk_stops_and_holds():
    data = big_file()
    claude, openai = setup()
    seen = []

    def flaky(e, t):
        seen.append(1)
        if len(seen) == 2:
            raise OSError("net")
        return claude(e, t)
    v, h, reserve, bad = r.run(ENV, data, [], TODAY, flaky, openai, [].append, GETTER)
    assert bad and v["Claude"]["verdict"] == "BLOCKER"


def test_schema_v3_needs_review_detail_or_explicit_null_from_29_nov():
    d = json.loads(file_bytes(date="2026-11-29", frozen_at_utc="2026-11-29T08:45:00Z"))
    full = {**RACE, "second": None, "data_pick": "A", "agent_b": None, "gemini_api": None, "data_gap": False, "price_move": None,
            "rpr_pick": None, "rpr_reason": "none", "longshot": None}
    d["races"] = [dict(full)]
    with pytest.raises(r.Refuse, match="review detail"):
        r.validate(json.dumps(d).encode(), "2026-11-29")
    d["races"] = [{**full, **{k: None for k in r.V3_DETAIL_FIELDS}}]
    with pytest.raises(r.Refuse, match="no usable"):                       # a picked race with null reasons is a gap, not an answer
        r.validate(json.dumps(d).encode(), "2026-11-29")
    ok = {**full, "zans_reasons": "top rated on course form", "cautions": "none", "data_chance": 0.31, "best_price": None}
    d["races"] = [ok]
    r.validate(json.dumps(d).encode(), "2026-11-29")
    d["races"] = [{**ok, "cautions": ""}]
    with pytest.raises(r.Refuse, match="cautions"):
        r.validate(json.dumps(d).encode(), "2026-11-29")
    d["races"] = [{**full, **{k: None for k in r.V3_DETAIL_FIELDS}, "win_pick": None, "status": "no pick"}, ok | {"course": "B"}]
    r.validate(json.dumps(d).encode(), "2026-11-29")                      # an unpicked race may carry nulls
    r.validate(json.dumps({**d, "date": "2026-11-28", "frozen_at_utc": "2026-11-28T08:45:00Z", "races": [full]}).encode(), "2026-11-28")
