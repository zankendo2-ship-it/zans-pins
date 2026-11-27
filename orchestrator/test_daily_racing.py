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
    full = {**RACE, "confidence": 8, "second": None, "data_pick": "A", "agent_b": None, "gemini_api": None, "data_gap": False, "price_move": None,
            "rpr_pick": None, "rpr_reason": "none", "longshot": None}
    d["races"] = [dict(full)]
    with pytest.raises(r.Refuse, match="review detail"):
        r.validate(json.dumps(d).encode(), "2026-11-29")
    d["races"] = [{**full, **{k: None for k in r.V3_DETAIL_FIELDS}}]
    with pytest.raises(r.Refuse, match="no usable"):                       # a picked race with null reasons is a gap, not an answer
        r.validate(json.dumps(d).encode(), "2026-11-29")
    ok = {**full, "zans_reasons": "top rated on course form", "cautions": "none", "data_chance": 0.31, "best_price": 2.5,
          "second": "Blue Sky", "second_reason": None, "rpr_pick": "Alpha Star", "longshot": None, "longshot_reason": "no runner is priced at 15.00 or more"}
    d["races"] = [ok]
    r.validate(json.dumps(d).encode(), "2026-11-29")
    d["races"] = [{**ok, "cautions": ""}]
    with pytest.raises(r.Refuse, match="cautions"):
        r.validate(json.dumps(d).encode(), "2026-11-29")
    for bad, why in (({"second": None}, "second"), ({"rpr_pick": None, "rpr_reason": None}, "rpr_pick"),
                     ({"longshot": None, "longshot_reason": ""}, "longshot"), ({"best_price": None}, "best_price")):
        d["races"] = [{**ok, **bad}]
        with pytest.raises(r.Refuse, match=why):
            r.validate(json.dumps(d).encode(), "2026-11-29")
    d["races"] = [{**ok, "rpr_pick": None, "rpr_reason": "No runner has an RPR yet", "longshot": "Long Shot at 21.0", "longshot_reason": None}]
    r.validate(json.dumps(d).encode(), "2026-11-29")
    d["races"] = [{**full, **{k: None for k in r.V3_DETAIL_FIELDS}, "win_pick": None, "status": "no pick"}, ok | {"course": "B"}]
    r.validate(json.dumps(d).encode(), "2026-11-29")                      # an unpicked race may carry nulls
    r.validate(json.dumps({**d, "date": "2026-11-28", "frozen_at_utc": "2026-11-28T08:45:00Z", "races": [full]}).encode(), "2026-11-28")


def test_schema_v3_values_are_checked_not_just_present():
    d = json.loads(file_bytes(date="2026-11-29", frozen_at_utc="2026-11-29T08:45:00Z"))
    ok = {**RACE, "second": "Blue Sky", "data_pick": "A", "agent_b": None, "gemini_api": None, "data_gap": False, "price_move": None,
          "rpr_pick": "Alpha Star", "rpr_reason": None, "longshot": "Long Shot at 21.0", "zans_reasons": "top rated on course form",
          "cautions": "none", "data_chance": 0.31, "best_price": 2.5, "confidence": 8, "second_reason": None, "longshot_reason": None}

    def check(**chg):
        d["races"] = [{**ok, **chg}]
        r.validate(json.dumps(d).encode(), "2026-11-29")

    check()
    check(longshot={"name": "Long Shot", "price": 21.0})
    check(longshot="Long Shot 20/1")
    check(best_price="2.5")
    check(second="none", second_reason="only two runners were declared in this race")
    check(rpr_pick="none", rpr_reason="no runner in this race has an RPR yet")
    check(longshot="none", longshot_reason="no runner is priced at 14/1 or more")
    for chg, why in (({"second": "none"}, "second"), ({"second": "N/A"}, "second"), ({"second": "x", "second_reason": "short"}, "second"), ({"second": "B"}, "second"), ({"second": "N.A."}, "second"), ({"second": "Nobody", "second_reason": None, "second": "7"}, "second"),
                     ({"second": "none", "second_reason": "filler words"}, "second"), ({"rpr_pick": "A"}, "rpr_pick"),
                     ({"rpr_pick": "none", "rpr_reason": None}, "rpr_pick"), ({"rpr_pick": "-", "rpr_reason": "tbc"}, "rpr_pick"),
                     ({"longshot": "none"}, "longshot"), ({"longshot": "some horse"}, "longshot"), ({"longshot": "Rank 2 horse"}, "longshot"), ({"longshot": "Short Price at 9.0"}, "longshot"), ({"longshot": "Short Price 6/1"}, "longshot"), ({"longshot": "B at 21.0"}, "longshot"), ({"longshot": {"name": "", "price": 21.0}}, "longshot"),
                     ({"longshot": {"name": "Long Shot", "price": 0.5}}, "longshot"), ({"longshot": True}, "longshot"),
                     ({"best_price": True}, "best_price"), ({"best_price": "abc"}, "best_price"), ({"best_price": -2.0}, "best_price"),
                     ({"best_price": 1.0}, "best_price"), ({"best_price": float("inf")}, "best_price"),
                     ({"data_chance": "0.3"}, "data_chance"), ({"data_chance": True}, "data_chance"), ({"data_chance": 1.5}, "data_chance"),
                     ({"data_chance": -0.1}, "data_chance"), ({"data_chance": float("nan")}, "data_chance")):
        with pytest.raises(r.Refuse, match=why):
            check(**chg)
    check(sky_bet_price=None, best_price=None)             # no Sky price, nothing to compare
    for bad in ("8.5", True, float("nan"), float("inf"), -1, 11):
        with pytest.raises(r.Refuse, match="confidence"):
            check(confidence=bad)


PRICES = (b"course,time,horse,price,best_dec,status\nAscot,13:00,Alpha Star,2.5,2.5,RUNNER\nAscot,13:00,Blue Sky (IRE),4.0,4.0,RUNNER\nAscot,13:00,Long Shot,21.0,21.0,RUNNER\n"
          b"Ascot,13:00,Cee Dee,6.0,6.0,RUNNER\nAscot,13:00,Dee Ess,8.0,8.0,RUNNER\nAscot,13:00,Eff Gee,9.0,9.0,RUNNER\n")
V3RACE = {**RACE, "win_pick": "Alpha Star", "second": "Blue Sky 4.00 (23%)", "rpr_pick": "Alpha Star", "longshot": "Long Shot at 21.0",
          "sky_bet_price": 2.5, "best_price": 2.5, "second_reason": None, "longshot_reason": None}


def _v3(**chg):
    d = json.loads(file_bytes(date="2026-11-29", frozen_at_utc="2026-11-29T08:45:00Z"))
    d["races"] = [{**V3RACE, **chg}]
    return d


def test_v3_named_runners_must_be_declared_in_the_verified_prices_file():
    r.check_declared_runners(_v3(), PRICES)
    for chg in ({"second": "Imaginary Horse"}, {"rpr_pick": "Phantom Runner"}, {"win_pick": "Not Declared"}):
        with pytest.raises(r.Refuse, match="not a declared runner"):
            r.check_declared_runners(_v3(**chg), PRICES)


def test_declared_runner_check_reads_the_real_prices_columns():
    real = (b"course,off_time,horse,sl_dec,best_dec,bookie_terms,status\nAscot,13:00,Alpha Star,2.5,2.6,Sky Bet v2;2.6;3;1/5,RUNNER\n"
            b"Ascot,13:00,Blue Sky,4.0,4.5,Sky Bet v2;4.5;3;1/5,RUNNER\n")
    d = _v3(longshot=None, longshot_reason="no runner priced at 15.00 or more", best_price=2.6)
    r.check_declared_runners(d, real)
    with pytest.raises(r.Refuse, match="not a declared runner"):
        r.check_declared_runners(_v3(second="Imaginary Horse", longshot=None), real)


def test_longshot_price_must_match_a_price_in_the_verified_file():
    with pytest.raises(r.Refuse, match="longshot price 31.0 is not a price"):
        r.check_declared_runners(_v3(longshot="Long Shot at 31.0"), PRICES)
    lowfile = PRICES.replace(b"Long Shot,21.0,21.0,", b"Long Shot,3.0,3.0,")   # source row 3.00 must not accept a claimed 21.00
    with pytest.raises(r.Refuse):
        r.check_declared_runners(_v3(), lowfile)


def test_best_price_must_match_a_price_in_the_verified_file():
    with pytest.raises(r.Refuse, match="best_price 9.0 is not the best_dec price"):
        r.check_declared_runners(_v3(best_price=9.0), PRICES)


def test_missing_course_time_rows_fail_closed_unless_a_no_price_reason():
    with pytest.raises(r.Refuse, match="no rows in the verified prices file"):
        r.check_declared_runners(_v3(course="Elsewhere"), PRICES)
    r.check_declared_runners(_v3(course="Elsewhere", no_price_reason="meeting not on the price feed at any check"), PRICES)
    with pytest.raises(r.Refuse, match="no rows"):
        r.check_declared_runners(_v3(course="Elsewhere", no_price_reason="none"), PRICES)


def test_placeholder_win_pick_is_refused():
    for bad in ("none", "None", "tbc", "N/A"):
        with pytest.raises(r.Refuse, match="usable runner name"):
            r.check_declared_runners(_v3(win_pick=bad), PRICES)


def test_longshot_reason_cannot_bypass_a_qualifying_runner_in_the_file():
    with pytest.raises(r.Refuse, match="named qualifying longshot is required"):
        r.check_declared_runners(_v3(longshot=None, longshot_reason="no value in the outsiders today"), PRICES)
    small = b"course,time,horse,price,best_dec,status\nAscot,13:00,Alpha Star,2.5,2.5,RUNNER\nAscot,13:00,Blue Sky,4.0,4.0,RUNNER\nAscot,13:00,Long Shot,21.0,21.0,RUNNER\n"
    r.check_declared_runners(_v3(longshot=None, longshot_reason="field of three, longshot rule needs six"), small)


def test_non_runner_row_is_not_a_declared_runner_or_eligible_longshot():
    five = b"course,time,horse,price,best_dec,status\n" + b"".join(b"Ascot,13:00,Horse %s,%d.0,%d.0,RUNNER\n" % (n, 3 + i, 3 + i) for i, n in enumerate([b"Aa", b"Bb", b"Cc", b"Dd", b"Ee"]))
    withdrawn = five + b"Ascot,13:00,Long Shot,21.0,21.0,NONRUNNER\n"
    base = {"win_pick": "Horse Aa", "second": "Horse Bb 4.0", "rpr_pick": "Horse Aa", "sky_bet_price": 3.0, "best_price": 3.0}
    r.check_declared_runners(_v3(**{**base, "longshot": None, "longshot_reason": "no active runner priced at 15.00 or more"}), withdrawn)
    with pytest.raises(r.Refuse, match="non-runner"):
        r.check_declared_runners(_v3(**{**base, "longshot": "Long Shot at 21.0"}), withdrawn)
    with pytest.raises(r.Refuse, match="non-runner"):
        r.check_declared_runners(_v3(**{**base, "second": "Long Shot 21.0"}), withdrawn)


def test_no_pick_race_must_carry_no_selections():
    with pytest.raises(r.Refuse, match="no win_pick but names"):
        r.check_declared_runners(_v3(win_pick=None, second="Blue Sky 4.0"), PRICES)
    r.check_declared_runners(_v3(win_pick=None, second=None, rpr_pick=None, longshot=None), PRICES)


def test_prices_file_status_fails_closed():
    nocol = b"course,time,horse,price\nAscot,13:00,Alpha Star,2.5\n"
    with pytest.raises(r.Refuse, match="no 'status' column"):
        r.check_declared_runners(_v3(), nocol)
    for bad in (b"", b"MAYBE", b"runner-ish"):
        f = b"course,time,horse,price,status\nAscot,13:00,Alpha Star,2.5," + bad + b"\n"
        with pytest.raises(r.Refuse, match="blank or unknown status"):
            r.check_declared_runners(_v3(), f)
    ok = b"course,time,horse,price,status\nAscot,13:00,Alpha Star,2.5,RUNNER\nAscot,13:00,Blue Sky,4.0,NONRUNNER\n"
    with pytest.raises(r.Refuse, match="non-runner"):
        r.check_declared_runners(_v3(longshot=None, longshot_reason="field is two runners, no longshot"), ok)   # second = Blue Sky is the withdrawn one


SRC = (b"course,off_time,horse,sl_dec,best_dec,bookie_terms,status\n"
       b"Ascot,13:00,Alpha Star,2.5,2.6,Sky Bet v2;2.6;3;1/5|Paddy Power;2.7;3;1/5,RUNNER\n"
       b"Ascot,13:00,Blue Sky,4.0,4.5,Sky Bet v2;4.5;3;1/5,RUNNER\n"
       b"Ascot,13:00,Cee Dee,6.0,6.0,Sky Bet v2;6.0;3;1/5,RUNNER\nAscot,13:00,Dee Ess,8.0,8.0,Sky Bet v2;8.0;3;1/5,RUNNER\n"
       b"Ascot,13:00,Eff Gee,9.0,9.0,Sky Bet v2;9.0;3;1/5,RUNNER\n"
       b"Ascot,13:00,Long Shot,21.0,19.0,Sky Bet v2;17.0;3;1/5|Paddy Power;19.0;3;1/5,RUNNER\n")


def _v3s(**chg):
    return _v3(**{"best_price": 2.6, **chg})


def _ls(price, source, kind):
    return {"name": "Long Shot", "price": price, "price_source": source, "price_kind": kind}


def test_longshot_price_source_label_binds_to_its_own_column():
    n = "d0_0959.csv"
    r.check_declared_runners(_v3s(longshot=_ls(17.0, f"Sky Bet in {n}", "bookmaker")), SRC, n)
    r.check_declared_runners(_v3s(longshot=_ls(19.0, f"best bookmaker in {n}", "bookmaker")), SRC, n)
    with pytest.raises(r.Refuse, match="not held in the source column"):
        r.check_declared_runners(_v3s(longshot=_ls(19.0, f"Sky Bet in {n}", "bookmaker")), SRC, n)   # 19.00 is Paddy Power / best, not Sky
    with pytest.raises(r.Refuse, match="not held in the source column"):
        r.check_declared_runners(_v3s(longshot=_ls(21.0, f"best bookmaker in {n}", "bookmaker")), SRC, n)   # 21.00 is the SL quote
    with pytest.raises(r.Refuse, match="is quote_only"):
        r.check_declared_runners(_v3s(longshot=_ls(21.0, f"Sporting Life quote in {n}", "bookmaker")), SRC, n)
    with pytest.raises(r.Refuse, match="not the verified prices file"):
        r.check_declared_runners(_v3s(longshot=_ls(17.0, "Sky Bet in other.csv", "bookmaker")), SRC, n)
    with pytest.raises(r.Refuse, match="known label"):
        r.check_declared_runners(_v3s(longshot=_ls(17.0, f"Betfred in {n}", "bookmaker")), SRC, n)


def test_longshot_price_source_requires_explicit_kind():
    n = "d0_0959.csv"
    with pytest.raises(r.Refuse, match="requires an explicit price_kind"):
        r.check_declared_runners(_v3s(longshot={"name": "Long Shot", "price": 17.0, "price_source": f"Sky Bet in {n}"}), SRC, n)


def test_compact_longshot_kind_cannot_pass_a_quote_as_a_bookmaker_price():
    c = {"name": "Long Shot", "price": 21.0, "price_kind": "bookmaker"}      # compact file: no price_source
    with pytest.raises(r.Refuse, match="quote-only price cannot stand in"):
        r.check_declared_runners(_v3s(longshot=c), SRC)
    r.check_declared_runners(_v3s(longshot={**c, "price_kind": "quote_only"}), SRC)
    r.check_declared_runners(_v3s(longshot={**c, "price": 17.0}), SRC)


def test_best_price_is_bound_to_best_dec():
    r.check_declared_runners(_v3s(best_price=2.6, longshot=_ls(17.0, "Sky Bet in x.csv", "bookmaker")), SRC)
    with pytest.raises(r.Refuse, match="best_dec"):
        r.check_declared_runners(_v3s(best_price=2.5, longshot=_ls(17.0, "Sky Bet in x.csv", "bookmaker")), SRC)   # 2.5 is only the SL quote


def test_longshot_with_no_source_identity_is_refused():
    with pytest.raises(r.Refuse, match="neither price_source nor price_kind"):
        r.check_declared_runners(_v3s(longshot={"name": "Long Shot", "price": 17.0}), SRC)


def test_best_price_never_falls_back_to_another_column():
    noBest = b"course,off_time,horse,sl_dec,best_dec,bookie_terms,status\nAscot,13:00,Alpha Star,2.5,,,RUNNER\nAscot,13:00,Blue Sky,4.0,,,RUNNER\n"
    with pytest.raises(r.Refuse, match="no best_dec"):
        r.check_declared_runners(_v3(longshot=None, longshot_reason="single runner, no longshot", best_price=2.5), noBest)


def test_malformed_bookie_terms_are_refused():
    bad = b"course,off_time,horse,sl_dec,best_dec,bookie_terms,status\nAscot,13:00,Alpha Star,2.5,2.6,Sky Bet v2|Paddy Power;2.7,RUNNER\n"
    with pytest.raises(r.Refuse, match="malformed bookie_terms"):
        r.check_declared_runners(_v3(), bad)


# ---- immutable evidence ids (V3) ----
import hashlib as _hl

_REC = {"time": "13:00", "course": "Ascot", "horse": "Alpha Star", "win_angles": ["Won last time at this trip", "Trainer in form 4 from 9"],
        "win_caution": ["Up 5lb in the handicap"], "data_angles": ["Top speed figure"], "second": "Blue Sky 4.00 (23%)", "chance": 0.303,
        "data_chance": 0.31, "data_conf": 4, "rpr_pick": "Alpha Star", "rpr_reason": "Best RPR at trip", "price": 2.5, "going": "Good to Soft",
        "longshot": "Long Shot at 21.0", "data_gap": False, "drift_warning": False, "second_reason": None, "longshot_reason": None}
_COURSE = json.dumps({"picks": [_REC, {**_REC, "time": "14:00", "horse": "Other"}]}).encode()
_PR = (b"course,off_time,horse,sl_dec,best_dec,bookie_terms,status\n"
       b"Ascot,13:00,Alpha Star,2.5,2.6,Sky Bet v2;2.6;3;1/5|Paddy Power;2.7;3;1/5,RUNNER\n"
       b"Ascot,13:00,Long Shot,21.0,19.0,Sky Bet v2;17.0;3;1/5,RUNNER\n")
_ROW = {"course": "Ascot", "off_time": "13:00", "horse": "Alpha Star", "sl_dec": "2.5", "best_dec": "2.6",
        "bookie_terms": "Sky Bet v2;2.6;3;1/5|Paddy Power;2.7;3;1/5", "status": "RUNNER"}
_LROW = {"course": "Ascot", "off_time": "13:00", "horse": "Long Shot", "sl_dec": "21.0", "best_dec": "19.0",
         "bookie_terms": "Sky Bet v2;17.0;3;1/5", "status": "RUNNER"}
_FILES = {"c/ascot.json": _COURSE, "c/d0.csv": _PR}
_blob = lambda b: _hl.sha1(b"blob %d\0" % len(b) + b).hexdigest()


def _evd(**race):
    d = {"date": "2026-11-29", "racing_branch_commit": "abc", "racing_commit_original": "a" * 40, "prices_file": "c/d0.csv",
         "evidence_fields": sorted(r.EVIDENCE_FIELDS_REQUIRED), "reason_fields": list(r.REASON_FIELDS_REQUIRED),
         "evidence_map": {"pick_record_keys": dict(r.EVIDENCE_RECORD_KEYS)},
         "sources": [{"id": "S1", "path": "c/ascot.json", "origin_path": "o/ascot.json", "blob_sha1": _blob(_COURSE), "captured_utc": "2026-11-29T08:45:00Z"},
                     {"id": "S2", "path": "c/d0.csv", "origin_path": "o/d0.csv", "blob_sha1": _blob(_PR), "captured_utc": "2026-11-29T07:24:00Z"}],
         "races": [{"time": "13:00", "course": "Ascot", "win_pick": "Alpha Star", "confidence": 8, "zans_reasons": ["Won last time at this trip"],
                    "cautions": ["Up 5lb in the handicap"], "sky_bet_price": 2.6, "best_price": 2.6, "second": "Blue Sky 4.00 (23%)",
                    "rpr_pick": "Alpha Star", "zans_chance": 0.303, "data_chance": 0.31, "data_conf": 4, "price_at_pick": "2.50", "going": "Good to Soft",
                    "longshot": "Long Shot at 21.0", "second_reason": None, "longshot_reason": None, "data_gap": False, "drift_warning": False,
                    "evidence": {"id": "E1", "src": "S1", "pick_sha256": r._h(_REC), "price_src": "S2", "price_row_sha256": r._h(_ROW),
                                 "longshot_row_sha256": r._h(_LROW)}, **race}]}
    return d


def _ev(d=None, files=None):
    f = files or _FILES
    r.check_evidence(d or _evd(), lambda c, p: f[p])


def _chg(path, val):
    d = _evd()
    t = d
    for k in path[:-1]:
        t = t[k]
    t[path[-1]] = val
    return d


def _with_rec(**kw):
    rec = {**_REC, **{k: v for k, v in kw.items()}}
    rec = {k: v for k, v in rec.items() if v is not r}
    files = {**_FILES, "c/ascot.json": json.dumps({"picks": [rec]}).encode()}
    d = _evd()
    d["sources"][0]["blob_sha1"] = _blob(files["c/ascot.json"])
    d["races"][0]["evidence"]["pick_sha256"] = r._h(rec)
    return d, files


def test_evidence_ok_and_reasons_may_be_cut():
    _ev()
    _ev(_evd(zans_reasons=["Won last time at this trip\u2026"]))
    _ev(_evd(sky_bet_price=None, best_price=None, longshot=None, not_verified=["sky_bet_price", "best_price"],
             evidence={"id": "E1", "src": "S1", "pick_sha256": r._h(_REC)}))


def test_evidence_wrong_path_or_hash_or_missing_id_refused():
    for d, why in ((_chg(["races", 0, "evidence", "src"], "S9"), "not in sources"),
                   (_chg(["races", 0, "evidence", "pick_sha256"], "0" * 64), "pick_sha256 does not match"),
                   (_chg(["races", 0, "evidence", "pick_sha256"], r._h(_REC)[:12]), "full 64-hex"),
                   (_chg(["races", 0, "evidence"], None), "needs evidence"),
                   (_chg(["races", 0, "evidence", "price_row_sha256"], "0" * 64), "price_row_sha256 does not match"),
                   (_chg(["races", 0, "evidence", "price_row_sha256"], r._h(_ROW)[:12]), "full 64-hex"),
                   (_chg(["races", 0, "evidence", "longshot_row_sha256"], r._h(_ROW)), "longshot_row_sha256 does not match"),
                   (_chg(["races", 0, "evidence", "price_src"], "S1"), "price_src"),
                   (_chg(["races", 0, "evidence", "id"], ""), "needs evidence"),
                   (_chg(["races", 0, "evidence", "id"], "free text"), "needs evidence"),
                   (_chg(["sources", 0, "blob_sha1"], "0" * 40), "blob_sha1"),
                   (_chg(["racing_commit_original"], "short"), "racing_commit_original")):
        with pytest.raises(r.Refuse, match=why):
            _ev(d)
    with pytest.raises(r.Refuse, match="subset"):
        _ev(_evd(not_verified=["price_move"]))


def test_evidence_ids_must_be_unique_across_races():
    d = _evd()
    d["races"].append({**_copy_deep(d["races"][0]), "time": "14:00", "evidence": {**d["races"][0]["evidence"]}})
    with pytest.raises(r.Refuse, match="duplicate evidence id"):
        _ev(d)


def _copy_deep(x):
    return json.loads(json.dumps(x))


def test_evidence_schema_cannot_be_shrunk_to_skip_checks():
    for key in ("evidence_fields", "reason_fields"):
        d = _evd(zans_reasons=["Invented unsupported claim"])
        d[key] = d[key][1:]
        with pytest.raises(r.Refuse, match=key):
            _ev(d)
        d = _evd(); d.pop(key)
        with pytest.raises(r.Refuse, match=key):
            _ev(d)
    d = _evd(); d["evidence_map"]["pick_record_keys"]["zans_reasons"] = "other"
    with pytest.raises(r.Refuse, match="evidence_map"):
        _ev(d)
    d = _evd(); d["evidence_fields"] = d["evidence_fields"] + ["extra"]
    with pytest.raises(r.Refuse, match="evidence_fields"):
        _ev(d)


def test_evidence_wrong_runner_course_row_or_field_refused():
    with pytest.raises(r.Refuse, match="not the horse"):
        _ev(_evd(win_pick="Blue Sky"))
    with pytest.raises(r.Refuse, match="exact course and time"):
        _ev(_evd(course="Newbury"))                    # same time at another course: no record, no borrowed hash
    with pytest.raises(r.Refuse, match="exact course and time"):
        _ev(_evd(time="14:30"))
    d, f = _with_rec(course=r)                          # record without a course key: time alone is never enough
    with pytest.raises(r.Refuse, match="exact course and time"):
        _ev(d, f)
    d, f = _with_rec(horse=r)                           # record without any runner key
    with pytest.raises(r.Refuse, match="runner key is mandatory"):
        _ev(d, f)
    dup = json.dumps({"picks": [_REC, _REC]}).encode()
    with pytest.raises(r.Refuse, match="exact course and time"):
        d = _evd(); d["sources"][0]["blob_sha1"] = _blob(dup)
        _ev(d, {**_FILES, "c/ascot.json": dup})
    with pytest.raises(r.Refuse, match="row"):
        d = _evd(); bad = _PR.replace(b"Alpha Star", b"Blue Sky"); d["sources"][1]["blob_sha1"] = _blob(bad)
        _ev(d, {**_FILES, "c/d0.csv": bad})
    with pytest.raises(r.Refuse, match="best"):
        _ev(_evd(best_price=2.7))                      # 2.70 is Paddy Power, not best_dec
    with pytest.raises(r.Refuse, match="sky"):
        _ev(_evd(sky_bet_price=2.7))


def test_evidence_names_must_match_their_mapped_record_field_not_any_text():
    d, f = _with_rec(second="Dee Ess 8.00 (5%)", win_angles=["Won last time at this trip", "Blue Sky mentioned in a narrative"])
    with pytest.raises(r.Refuse, match="mapped hashed pick-record field 'second'"):
        _ev(d, f)
    d, f = _with_rec(rpr_pick="Dee Ess", win_angles=["Won last time at this trip", "Alpha Star mentioned in a narrative"])
    with pytest.raises(r.Refuse, match="mapped hashed pick-record field 'rpr_pick'"):
        _ev(d, f)


def test_evidence_boolean_fields_must_be_real_booleans():
    d, f = _with_rec(data_gap=True)
    d["races"][0]["data_gap"] = "false"
    with pytest.raises(r.Refuse, match="must be a boolean"):
        _ev(d, f)


def test_evidence_second_and_longshot_reasons_are_source_bound():
    sr = "Blue Sky has the stronger place profile on the supplied figures"
    lr = "Long Shot has the strongest recent speed figure in this field"
    d, f = _with_rec(second_reason=sr, longshot_reason=lr)
    d["races"][0]["second_reason"] = sr
    d["races"][0]["longshot_reason"] = lr
    _ev(d, f)
    d["races"][0]["second_reason"] = "the jockey is in great form this season"
    with pytest.raises(r.Refuse, match="second_reason text is not found"):
        _ev(d, f)


def test_evidence_typed_fields_must_match_the_hashed_record():
    for chg, why in (({"second": "Dee Ess 8.00 (5%)"}, "second"), ({"rpr_pick": "Cee Dee"}, "rpr_pick"), ({"zans_chance": 0.40}, "zans_chance"),
                     ({"data_chance": 0.5}, "data_chance"), ({"data_conf": 9}, "data_conf"), ({"price_at_pick": "3.10"}, "price_at_pick"),
                     ({"going": "Heavy"}, "going"), ({"data_gap": True}, "data_gap"), ({"drift_warning": True}, "drift_warning")):
        with pytest.raises(r.Refuse, match=why):
            _ev(_evd(**chg))
    _ev(_evd(zans_chance=0.3031, rpr_pick=None))        # tiny rounding / a withdrawn RPR pick (null) is fine
    _ev(_evd(zans_chance=0.40, not_verified=["zans_chance"]))   # flagged NOT VERIFIED = not claimed as verified


def test_evidence_pick_source_and_price_source_captured_strictly_before_off():
    with pytest.raises(r.Refuse, match="strictly before the off"):
        _ev(_chg(["sources", 0, "captured_utc"], "2026-11-29T08:45:00"))  # naive timestamps are not assumed to be UTC
    for si in (0, 1):
        for ts in ("2026-11-29T13:00:00Z", "2026-11-29T15:00:00Z", "nonsense", None):
            with pytest.raises(r.Refuse, match="strictly before the off"):
                _ev(_chg(["sources", si, "captured_utc"], ts))
    _ev(_chg(["sources", 0, "captured_utc"], "2026-11-29T12:59:00Z"))
    with pytest.raises(r.Refuse, match="after the off"):
        d = _evd(); d["races"][0]["evidence"]["price_captured_after_off"] = True
        _ev(d)


def test_evidence_summer_time_off_is_london_local():
    d = _chg(["date"], "2026-07-15")        # 13:00 BST = 12:00Z; 12:30Z capture is after the off
    d["sources"][1]["captured_utc"] = "2026-07-15T12:30:00Z"
    d["sources"][0]["captured_utc"] = "2026-07-15T08:00:00Z"
    with pytest.raises(r.Refuse, match="strictly before"):
        _ev(d)
    d["sources"][1]["captured_utc"] = "2026-07-15T11:30:00Z"
    _ev(d)


def test_evidence_plausible_but_unsupported_reason_refused():
    with pytest.raises(r.Refuse, match="unsupported reason"):
        _ev(_evd(zans_reasons=["Won last time at this trip", "Jockey has won 3 of 4 here"]))
    with pytest.raises(r.Refuse, match="unsupported reason"):
        _ev(_evd(cautions=["Never raced on soft"]))
    d, f = _with_rec(win_angles=None)
    with pytest.raises(r.Refuse, match="holds nothing"):
        _ev(_evd_with(d, zans_reasons=["Won last time"]), f)
    _ev(_evd(zans_reasons=["Won last time at this trip"], not_verified=["zans_reasons"], confidence_capped=6))   # flagged NOT VERIFIED = allowed


def _evd_with(d, **race):
    d["races"][0].update(race)
    return d


def test_evidence_unverified_reason_must_cap_confidence_at_six():
    with pytest.raises(r.Refuse, match="confidence_capped"):
        _ev(_evd(not_verified=["zans_reasons"]))
    with pytest.raises(r.Refuse, match="confidence_capped"):
        _ev(_evd(not_verified=["second"], confidence_capped=7))
    _ev(_evd(not_verified=["zans_reasons"], confidence_capped=6))
    _ev(_evd(not_verified=["zans_reasons"], confidence=5))      # already at or under the cap
    with pytest.raises(r.Refuse, match="confidence_capped"):
        _ev(_evd(not_verified=["zans_reasons"], confidence="8.5"))  # decimal confidence cannot bypass int() parsing
    _ev(_evd(not_verified=["zans_reasons"], confidence="8.5", confidence_capped=6))


def test_evidence_none_listed_is_verified_empty_only_when_the_record_key_is_empty():
    for empty in (None, "", []):
        d, f = _with_rec(win_angles=empty)
        _ev(_evd_with(d, zans_reasons="none listed"), f)
        d, f = _with_rec(win_angles=empty)
        _ev(_evd_with(d, zans_reasons=["none listed"]), f)
    d, f = _with_rec(win_angles=[])
    with pytest.raises(r.Refuse, match="holds nothing"):
        _ev(_evd_with(d, zans_reasons=["Won last time"]), f)               # invented reason on an empty record
    with pytest.raises(r.Refuse, match="holds content"):
        _ev(_evd(zans_reasons="none listed"))                                # hides real angles
    d, f = _with_rec(win_angles=r)
    with pytest.raises(r.Refuse, match="no such key"):
        _ev(_evd_with(d, zans_reasons="none listed"), f)                     # key absent is not verified-empty


def test_evidence_course_may_be_file_level_and_win_key_names_the_horse():
    rec = {k: v for k, v in _REC.items() if k not in ("course", "horse")}
    rec["win"] = "Alpha Star"
    for fc, ok in (("ascot", True), ("Ascot", True), ("newbury", False), (None, False)):
        doc = {"published_utc": "x", "picks": [rec]}
        if fc:
            doc["course"] = fc
        files = {**_FILES, "c/ascot.json": json.dumps(doc).encode()}
        d = _evd(); d["sources"][0]["blob_sha1"] = _blob(files["c/ascot.json"]); d["races"][0]["evidence"]["pick_sha256"] = r._h(rec)
        if ok:
            _ev(d, files)
        else:
            with pytest.raises(r.Refuse, match="exact course and time"):
                _ev(d, files)
    doc = {"course": "ascot", "picks": [{**rec, "win": "Blue Sky"}]}
    files = {**_FILES, "c/ascot.json": json.dumps(doc).encode()}
    d = _evd(); d["sources"][0]["blob_sha1"] = _blob(files["c/ascot.json"]); d["races"][0]["evidence"]["pick_sha256"] = r._h(doc["picks"][0])
    with pytest.raises(r.Refuse, match="not the horse"):
        _ev(d, files)
