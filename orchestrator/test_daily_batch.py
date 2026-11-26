import pytest
import orchestrator.daily_batch as b
import orchestrator.orchestrate as o

SHA = "a" * 40
URL = f"https://github.com/zankendo2-ship-it/zans-pins/blob/{SHA}/x.md"
ENV = {"ZANS_ORCH_MAX_RUNS_PER_DAY": "1", "ZANS_ORCH_MAX_USD_PER_MONTH": "25", "ZANS_ORCH_MAX_USD_PER_RUN": "3"}
BOT = {"login": "github-actions[bot]"}


def item(i="a", **kw):
    d = {"id": i, "title": "t", "url": URL, "sha256": "f" * 64, "self_check": {"tests_passed": True}}
    d.update(kw)
    return d


def test_hard_cap_derived_from_the_caps():
    assert 0 < b.worst_case_usd() <= b.CAP_USD


def test_empty_manifest_makes_no_call():
    with pytest.raises(b.Skip):
        b.plan({"items": []}, {}, [], ENV, "2026-11-27")


def test_unchecked_or_unpinned_item_is_refused_before_any_call():
    with pytest.raises(b.Refuse):
        b.plan({"items": [item(self_check={"tests_passed": False})]}, {"a": "x"}, [], ENV, "2026-11-27")
    with pytest.raises(b.Refuse):
        b.plan({"items": [item(url="https://github.com/x/y/blob/main/a.md")]}, {"a": "x"}, [], ENV, "2026-11-27")


def test_valid_batch_is_one_call_within_cap():
    p = b.plan({"items": [item("a"), item("b")]}, {"a": "text a", "b": "text b"}, [], ENV, "2026-11-27")
    assert p["reserve"] <= b.CAP_USD and p["body"]["max_completion_tokens"] == b.MAX_OUT_TOKENS
    assert p["body"]["model"] == b.MODEL and len(p["body"]["messages"]) == 1


def test_second_batch_same_day_stops():
    slot = {"body": o.slot_tag("live", "2026-11-27", "abc", 0.25), "user": BOT}
    with pytest.raises(o.Stop):
        b.plan({"items": [item()]}, {"a": "x"}, [slot], ENV, "2026-11-27")


def test_overrun_blocks_and_oversize_is_refused_not_truncated():
    slot = {"body": o.slot_tag("live", "2026-11-20", "abc", 0.25), "user": BOT}
    st = {"body": o.settle_tag("2026-11-20", "abc", 0.4, over=True), "user": BOT}
    with pytest.raises(o.Stop):
        b.plan({"items": [item()]}, {"a": "x"}, [slot, st], ENV, "2026-11-27")
    with pytest.raises(b.Refuse):
        b.plan({"items": [item()]}, {"a": "y" * (b.MAX_INPUT_CHARS + 1)}, [], ENV, "2026-11-27")


def test_more_than_six_items_refused():
    with pytest.raises(b.Refuse):
        b.plan({"items": [item(str(n)) for n in range(7)]}, {str(n): "x" for n in range(7)}, [], ENV, "2026-11-27")
