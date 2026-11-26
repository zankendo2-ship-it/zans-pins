#!/usr/bin/env python3
"""Gate: may this item go to the owner? Exit 0 = OWNER_READY, 1 = not ready (reasons printed)."""
import hashlib, json, os, sys

ORDER = ["DRAFT", "SELF_CHECKED", "INDEPENDENT_REVIEW", "PASS", "OWNER_READY"]
REVIEWERS = {"claude", "chatgpt"}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check(manifest, base="."):
    """Return a list of reasons the item is NOT owner-ready (empty list = ready)."""
    why = []
    state = manifest.get("state")
    if state not in ORDER:
        return [f"state {state!r} is not one of {ORDER} (REVISE/BLOCKED are never owner-ready)"]
    art = manifest.get("artifact") or {}
    want = (art.get("sha256") or "").lower()
    if not (art.get("path") and art.get("ref") and want):
        why.append("artifact needs path, immutable ref (commit) and sha256")
    else:
        p = os.path.join(base, art["path"])
        if not os.path.exists(p):
            why.append(f"artifact file not found: {art['path']}")
        elif sha256_file(p) != want:
            why.append("artifact file hash does not match the manifest sha256")
    if not manifest.get("self_check", {}).get("tests_passed"):
        why.append("self-check: tests_passed is not true")
    if manifest.get("self_check", {}).get("placeholder") or manifest.get("placeholder"):
        why.append("item is a placeholder or partial work")
    seen = {}
    for r in manifest.get("reviews", []):
        who = str(r.get("reviewer", "")).lower()
        if who in REVIEWERS and r.get("verdict") == "PASS" and (r.get("sha256") or "").lower() == want:
            seen[who] = r.get("comment_id")
    for who in sorted(REVIEWERS - set(seen)):
        why.append(f"no PASS from {who} on this exact artifact hash")
    if state != "OWNER_READY":
        why.append(f"state is {state}, not OWNER_READY")
    return why


if __name__ == "__main__":
    m = json.load(open(sys.argv[1]))
    reasons = check(m, base=os.path.dirname(os.path.abspath(sys.argv[1])))
    if reasons:
        print("NOT OWNER-READY:\n- " + "\n- ".join(reasons))
        sys.exit(1)
    print("OWNER_READY: matching hash, both reviewers PASS")
