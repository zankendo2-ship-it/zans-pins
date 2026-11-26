import hashlib, os, sys, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from owner_ready import check


def make(tmp, content=b"art", **kw):
    p = os.path.join(tmp, "a.png"); open(p, "wb").write(content)
    h = hashlib.sha256(content).hexdigest()
    m = {"state": "OWNER_READY", "artifact": {"path": "a.png", "ref": "abc1234", "sha256": h},
         "self_check": {"tests_passed": True},
         "reviews": [{"reviewer": "claude", "verdict": "PASS", "sha256": h},
                     {"reviewer": "chatgpt", "verdict": "PASS", "sha256": h}]}
    m.update(kw); return m, h


def test_ready():
    with tempfile.TemporaryDirectory() as t:
        assert check(make(t)[0], t) == []


def test_one_reviewer_missing():
    with tempfile.TemporaryDirectory() as t:
        m, _ = make(t); m["reviews"].pop()
        assert any("chatgpt" in r for r in check(m, t))


def test_review_on_old_hash():
    with tempfile.TemporaryDirectory() as t:
        m, _ = make(t); m["reviews"][1]["sha256"] = "0" * 64
        assert any("chatgpt" in r for r in check(m, t))


def test_file_changed_after_review():
    with tempfile.TemporaryDirectory() as t:
        m, _ = make(t); open(os.path.join(t, "a.png"), "wb").write(b"changed")
        assert any("does not match" in r for r in check(m, t))


def test_placeholder_and_revise_blocked():
    with tempfile.TemporaryDirectory() as t:
        assert check(make(t, placeholder=True)[0], t)
        assert check(make(t, state="REVISE")[0], t)
        assert check(make(t, state="INDEPENDENT_REVIEW")[0], t)
