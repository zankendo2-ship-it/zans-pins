#!/usr/bin/env python3
"""Independent RE-REVIEW of a corrected racing artifact (manual, main only, allowlisted actor).

Flow: a racing REVISE/REJECT opens a correction gate (run + correction id). The racing thread (a Claude session, no API
spend) fixes the sealed file and the receipt workflow records bound proof per fix: 'N=applied <commit> <path> <sha256>'.
That FIX receipt does NOT close the gate. This route then:
  1. finds the open gate and its bot-posted fix receipt (exact run + correction id; unknown/closed/mismatched = refused);
  2. requires every applied fix to name the SAME artifact path, re-fetches that file at the evidence commit and re-checks
     the sha256 (wrong bytes = refused, no call);
  3. runs the normal racing review (ONE Claude + ONE OpenAI call, same caps, shared daily slot, reservation + settlement)
     on those exact corrected bytes, with the full payload;
  4. closes the gate (and its ancestors) ONLY on a settled PASS/PASS. Anything else leaves it open, opens a new gate for
     the corrected file's own hash linked to its parent, and emits no completion marker.
Provider failure, unknown usage or an overrun never closes a gate. Mock mode = zero calls, plumbing only."""
import hashlib
import json
import os
import re
import sys
import time

import orchestrator.daily_racing as dr
import orchestrator.orchestrate as o

EVIDENCE_RE = re.compile(r"^- \s*(\d+)=applied\s+([0-9a-f]{40})\s+(\S+)\s+([0-9a-f]{64})\s*$", re.M | re.I)


class Refuse(Exception):
    pass


def fix_evidence(comments, run, cid):
    """The newest bot-posted fix receipt for this exact gate -> list of (item, commit, path, sha256)."""
    found = None
    for c in comments:
        if (c.get("user") or {}).get("login") != o.TRUSTED_SETTLER:
            continue
        b = c.get("body") or ""
        if f"<!-- {o.FIXED}:{run}:{cid} -->" in b:
            found = [(int(m.group(1)), m.group(2).lower(), m.group(3), m.group(4).lower()) for m in EVIDENCE_RE.finditer(b)]
    if not found:
        raise Refuse("no bot-posted fix receipt for this exact run + correction id (nothing applied to re-review)")
    paths = {x[2] for x in found}
    if len(paths) != 1:
        raise Refuse("applied fixes must all name one corrected artifact path")
    if len({(x[1], x[3]) for x in found}) != 1:
        raise Refuse("applied fixes must all point at the same corrected commit and file hash")
    return found


def corrected_bytes(evidence, getter):
    _, commit, path, digest = evidence[0]
    b = getter(commit, path)
    if hashlib.sha256(b).hexdigest() != digest:
        raise Refuse("the corrected file's bytes do not match the receipt's sha256")
    return b


def rereview(env, comments, run, cid, getter, source_getter, claude, openai, post):
    """Returns (closed: bool, verdicts, hash, reserve, bad). `getter(commit, path)` fetches corrected bytes."""
    mode = env.get("ORCH_MODE", "mock")
    if not o.SHA64_RE.fullmatch(run) or not o.SHA64_RE.fullmatch(cid):
        raise Refuse("run and correction must each be a full 64-hex id")
    if (run, cid) not in o.pending_corrections(comments):
        raise Refuse("no open correction gate with this exact run + correction id")
    ev = fix_evidence(comments, run, cid)
    data = corrected_bytes(ev, getter)
    if hashlib.sha256(data).hexdigest() == run:
        raise Refuse("the 'corrected' file is the very file that was reviewed (same hash); nothing was fixed")
    try:
        file_date = json.loads(data.decode("utf-8")).get("date", "")
    except (UnicodeDecodeError, ValueError):
        raise Refuse("corrected file is not UTF-8 JSON")
    today = time.strftime("%Y-%m-%d", time.gmtime())
    try:
        verdicts, h, reserve, bad = _run(env, data, comments, file_date, today, claude, openai, post, source_getter, (run, cid))
    except dr.Refuse as r:
        raise Refuse(str(r))
    passed = (mode == "live" and not bad and len(verdicts) == 2 and all(v["verdict"] == "PASS" for v in verdicts.values()))
    return passed, verdicts, h, reserve, bad


def _run(env, data, comments, file_date, today, claude, openai, post, source_getter, allow):
    """daily_racing.run with the file's own date for validation and the slot booked on today's UTC date."""
    mode = env.get("ORCH_MODE", "mock")
    p = dr.plan(data, comments, env, file_date, allow)
    if mode == "live":
        if source_getter is None:
            raise dr.Refuse("no source getter: pack bytes cannot be verified")
        dr.verify_sources(data, source_getter)
    if mode != "live":
        post(dr.summary(p, file_date, {}, mode))
        return {}, p["hash"], 0.0, False
    if o.runs_today(comments, today, "racing") >= o.day_cap(env, "racing"):
        raise o.Stop("STOPPED: the shared paid runs per UTC day are already used.")
    reserve = p["reserve"]
    o.RUN_COST.update(usd=0.0, complete=True)
    post(f"{o.slot_tag('racing', today, p['hash'], reserve)}\nZANS racing RE-REVIEW of corrected file ({p['hash']}), "
         f"worst case ${reserve:.2f}. If no summary follows, the run failed and the slot is used.\n\n"
         "---\n_Generated by [Claude Code](https://claude.ai/code)_")
    verdicts = {"Claude": dr.ask(env, "Claude", claude, p["prompt"])}
    if verdicts["Claude"]["verdict"] not in ("BLOCKER", "REJECT") and o.RUN_COST["complete"]:
        verdicts["ChatGPT"] = dr.ask(env, "OpenAI", openai, p["prompt"])
    post(dr.summary(p, file_date, verdicts, mode))
    bad = (len(verdicts) < 2 or any(v["verdict"] == "BLOCKER" for v in verdicts.values()) or not o.RUN_COST["complete"]
           or o.opens_gate(verdicts.values()))
    return verdicts, p["hash"], reserve, bad


def closing_body(run, cid, comments, h):
    chain = o.gate_chain(comments, run, cid)
    tags = "\n".join(f"<!-- {o.RECEIPT}:{r}:{c} -->" for r, c in chain)
    return (f"**Gate closed by independent re-review**: the corrected artifact (sha256 `{h}`) received PASS from both reviewers "
            f"in a settled run. Closed: {len(chain)} gate(s).\n{tags}\n\n---\n_Generated by [Claude Code](https://claude.ai/code)_")


def parent_body(new_hash, verdicts, run, cid):
    if not o.opens_gate(verdicts.values()):
        return None
    ncid = o.correction_id(o.gate_items(list(verdicts.values())))
    return (f"Re-review did not pass; a new gate opened for the corrected file and descends from the earlier one.\n"
            f"<!-- {o.PARENT}:{new_hash}:{ncid}:{run}:{cid} -->\n\n---\n_Generated by [Claude Code](https://claude.ai/code)_")


def main(env=None):
    env = dict(os.environ if env is None else env)
    mode = env.get("ORCH_MODE", "mock").strip()
    repo, issue = env.get("GITHUB_REPOSITORY", ""), env.get("ORCH_ISSUE", "").strip()
    run, cid = env.get("ORCH_RUN", "").strip().lower(), env.get("ORCH_CORRECTION", "").strip().lower()
    try:
        o.guard(env, mode)
        if issue != o.ALLOWED_ISSUE:
            raise o.Stop(f"REFUSED: only issue #{o.ALLOWED_ISSUE}.")
        today = time.strftime("%Y-%m-%d", time.gmtime())
        comments = o.comments_since(env, repo, issue, "2026-01-01T00:00:00Z")
        post = lambda body: o.gh(env, "POST", f"repos/{repo}/issues/{issue}/comments", {"body": body})  # noqa: E731
        getter = lambda commit, path: o._get_bytes(  # noqa: E731
            f"https://raw.githubusercontent.com/{repo}/{commit}/{path}", dr.MAX_FILE_BYTES + 1)
        srcget = lambda commit, path: o._get_bytes(dr.source_url(commit, path), dr.MAX_FILE_BYTES * 20)  # noqa: E731
        claude, openai = (o.call_claude, o.call_openai) if mode == "live" else (None, None)
        try:
            passed, verdicts, h, reserve, bad = rereview(env, comments, run, cid, getter, srcget, claude, openai, post)
        except Refuse as r:
            raise o.Stop("REFUSED: " + str(r))
        except dr.Skip as s:
            print("SKIPPED: " + str(s))
            return 0
        if mode == "live":
            markers = [f"<!-- {o.MARKER}:{h} -->"] if passed else []
            settled = o.settle(env, repo, issue, today, h, reserve, completion_markers=markers)
            if passed and settled:
                post(closing_body(run, cid, comments, h))
            else:
                pb = parent_body(h, verdicts, run, cid)
                if pb:
                    post(pb)
        print("done: re-review " + ("PASS/PASS, gate closed" if mode == "live" and passed else "gate stays open"))
        return 0 if (mode != "live" or passed) else 1
    except o.Stop as s:
        print(str(s))
        return 0 if s.args[0].startswith(("DISABLED", "SKIPPED")) else 1


if __name__ == "__main__":
    sys.exit(main())
