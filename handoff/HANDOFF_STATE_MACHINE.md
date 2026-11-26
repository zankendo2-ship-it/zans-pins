# ZANS handoff state machine (canonical, from owner 26 Nov 2026)

Alex only receives a finished, independently reviewed final package. He is never sent drafts,
placeholders, internal disagreements, routine technical questions or repeated approval requests.

States, in order:

1. DRAFT - the owning thread is working.
2. SELF_CHECKED - the owning thread has checked the ACTUAL artifact: tests run, an immutable ref
   (commit + path), a sha256, and a phone-size visual check where it matters.
3. INDEPENDENT_REVIEW - posted on #26 (zans-pins) or #39 (racing) for the other reviewer.
4. REVISE - back to the owning thread. It is fixed privately, using the approved design constraints.
   BLOCKED means the item is waiting on something internal, and it stays internal.
5. PASS - both reviewers (Claude and ChatGPT) PASS the same artifact sha256.
6. OWNER_READY - only with a matching artifact hash and both PASS reviews. Only now may Alex see it.

Escalate to Alex only for a real business choice, new spending, an unavoidable account permission, or a
complete OWNER_READY package. If a change is unnecessary, keep the original and don't ask.
Physical sample gates and print gates are never bypassed.

Enforcement: `python handoff/owner_ready.py <manifest.json>` exits 0 only when the item may go to Alex.
See handoff/samples/ and handoff/tests/. Rules the script cannot enforce: ordinary Claude chats can
still send Alex a message, so each thread runs the check before posting a package, and the coordinator
re-verifies before relaying one.
