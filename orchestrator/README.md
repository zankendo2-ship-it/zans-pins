# ZANS two-reviewer check (Claude + OpenAI): PILOT, OFF BY DEFAULT

**What it does:** you start it by hand. It works on issue #26 only. It reads the #26 checklist, the newest #26 comments and the TEXT files you link. Claude reviews first, then OpenAI, then up to 3 rounds where each sees the other's verdict. It posts **one** summary comment: AGREED (both PASS), AGREED REVISE (both want changes: it stops at once and lists the combined fixes, no paid re-review until a new revision is pinned), REJECTED, BLOCKER or NO AGREEMENT (the stricter verdict, REVISE, stands).

**What it is:** a manual, text-only exchange of verdicts. It never edits files, never reviews artwork, images or video, and never applies corrections by itself.

**What it never does:** deploy, publish, list, post to social, order, or spend beyond its capped API calls. Agreement between the two reviewers is **not** Alex's approval.

## Safety built in
- **Manual start only** (`workflow_dispatch`). There are no comment, push or schedule triggers, so it cannot start itself. Its summary comment is posted with `GITHUB_TOKEN`, which GitHub does not let start other workflows.
- **Off by default.** Live (paid) runs only happen when the repository variable `ZANS_ORCH_ENABLED` is `true`. The free `mock` run works while it is off, so it can be tested first.
- **Allowlist.** The person starting it must be listed in `ZANS_ORCH_ALLOWED_ACTORS`.
- **Immutable inputs.** Artifact links must be pinned to a 40-character commit SHA.
- **Issue #26 only.** Any other issue number is refused before anything is read.
- **Text files only, fail closed.** These API calls cannot see images, video or rendered designs, so there is no visual PASS. Image, video, SVG, HTML and PDF links are refused. Review a design through a text report, such as a preflight JSON or MD file.
- **Hard caps in the code.** Provider budgets are alerts, not guaranteed stops, so these are enforced before any call:
  - 3 rounds, and 6 API requests per run;
  - the first REJECT or BLOCKER stops the run at once, so the other reviewer is not called;
  - 1,500 output tokens per call, 120 s per call, 10 min per run;
  - **a shared daily count of paid runs across manual/live, products, racing and retro routes.** Alex's rule of 26 Nov was ONE batched run a day. On 27 Nov 05:30 UTC he asked for MORE than one a day while setting up and fixing issues, so the code ceiling is TEMPORARILY 6 (`MAX_LIVE_RUNS_PER_DAY`; it was 3 earlier on 27 Nov, raised after Alex said at 11:28 UTC to keep using paid runs until everything is done, one line, marked TEMPORARY; set it back to 1 after set-up). USD 2.45 is reserved up front per run, then settled at measured cost. Live needs `ZANS_ORCH_MAX_RUNS_PER_DAY` set explicitly (1 to 6); empty or invalid means 0 live runs;
  - **owner budgets:** live needs `ZANS_ORCH_MAX_USD_PER_RUN` (Alex approved `3`) and `ZANS_ORCH_MAX_USD_PER_MONTH` (set by Alex himself; this PR never changes it). Missing, zero, negative or non-finite (`nan`, `inf`) values refuse live. Every call is priced at $10 in / $50 out per million tokens, which is above every allowed model's 25 Nov list price:
    - **before the run**, the worst case is worked out. The run is refused if that is over the per-run budget, or if it plus this month's reservations is over the monthly budget;
    - the full hard-cap worst run (**$2.45**) is **reserved in the slot comment** before any paid call, whatever the estimate, so failed runs count against the month;
    - **after the run** (finished or stopped by a cap), the workflow posts a settle comment with the measured cost: provider-reported tokens x list price x 1.25. The month then counts that measured amount even if it is above the reservation (flagged as an overrun that blocks further live runs). A run with any call missing usage data, an unknown model price, or a crash is never settled and keeps the full $2.45. Only settle comments by `github-actions[bot]` count;
    - each call is also held to that reserve (the smaller of $2.45 and the per-run budget);
    - **before every call**, the actual input so far plus this call, with the output of all 6 calls reserved, must still fit the per-run budget;
    - the hard caps put the largest possible run at **$2.45**;
  - **live only from `main`**, only with the checked models (`claude-sonnet-5-5`; `gpt-6.2-astra` or `gpt-6-luna`);
  - the **run slot is reserved** with a marker comment on #26 **before any paid call**. Failed or cancelled runs still use their slot;
  - **input bound of 200k tokens per run**, counted as **the JSON-escaped bytes actually sent + 500 per call**. These are never fewer than the UTF-8 bytes, and a token is at least one byte, so this cannot undercount Unicode, control characters or code. Reviewer verdict text is cut down to plain printable ASCII, so its size is fixed. It is counted on every actual call, including the other reviewer's verdict. The worst case is checked before the first call, and the run stops if the real total would go over;
  - up to 6 files, 60 KB per file and 120 KB in total. In practice the bound limits files to a few KB: **the first live test uses a small synthetic text file**;
  - 6k characters of recent comments;
  - files only from `zankendo2-ship-it` repos;
  - one run at a time (concurrency lock).
- **Shared context.** Every review loads `orchestrator/ZANS_RULES.md` (the shared rules) and the **#26 issue body (the canonical checklist) as its own section, in full**. It is never cut by the comment cap; if it is over 14k characters the run is refused. It also loads the newest #26 comments and the text of the pinned files.
- **Dedup.** A full 64-hex fingerprint and the pre-call slot prevent a retry of an unchanged paid artifact set, even after a failed attempt or on a later day. Mock and live have separate keys, so a mock never blocks the live run. Completion markers are emitted only in the trusted settlement comment after known, non-overrun usage; unknown usage, overrun or failed settlement never marks an artifact complete.
- **Untrusted data.** Issue comments and artifacts go to the models inside untrusted-data markers, which the models are told to ignore instructions in. Any reply that isn't a valid verdict counts as BLOCKER, never PASS. That includes wrong field types, such as reasons not being a list of text.
- **Correction routing limitation.** The current workflow does not implement a private Claude-thread handoff or receipt. Its GitHub summary is public on #26; corrections must be relayed manually until a tested internal route is added. Do not claim private routing or automatic re-review.
- **No secrets or comment text in logs.** Keys are only passed in `live` mode and are never printed. The job has `contents: read` and `issues: write` only.
- **Mock is labelled synthetic.** `mock` mode makes no model calls. Its summary says SYNTHETIC MOCK, zero paid API calls, and that it gives no verdict on the files.
- **Pinned supply chain.** No third-party actions: a plain `git` checkout of the exact commit on the pinned `ubuntu-24.04` image. The test dependencies are installed with `--require-hashes`. The tests run before every review.

## Activation order (agreed 25 Nov)
- Keep `ZANS_ORCH_ENABLED` = `false` until ChatGPT has approved this code AND a free `mock` run has passed.
- Keys go ONLY into encrypted GitHub secrets. Never put them in code, comments or either chat. This repo is public.

## Alex's setup steps (in this order)
1. Merge this PR into `main`. GitHub only offers manual workflows that are on the default branch.
2. Repo **Settings > Secrets and variables > Actions > Secrets**: add `ANTHROPIC_API_KEY` and `OPENAI_API_KEY`. Never paste keys in chat or issues.
3. Same page, **Variables**:
   - `ZANS_ORCH_ALLOWED_ACTORS` = your GitHub username;
   - `ANTHROPIC_MODEL` and `OPENAI_MODEL` = the model names.
   - Do **not** set `ZANS_ORCH_ENABLED` yet.
4. Set a monthly spending limit or alert in both API dashboards (Anthropic Console, OpenAI Platform). These can lag or only warn, so they are **alerts, not a guaranteed hard stop**. The code's own refusals are `ZANS_ORCH_MAX_USD_PER_RUN` and `ZANS_ORCH_MAX_USD_PER_MONTH`.
5. **Actions > ZANS two-reviewer check > Run workflow** with mode `mock`. It runs while switched off and costs nothing.
6. Only after ChatGPT and Claude both PASS the mock result, and Alex has approved a budget, set:
   - `ZANS_ORCH_MAX_RUNS_PER_DAY` = `1`;
   - `ZANS_ORCH_MAX_USD_PER_RUN` = `3` (the per-run budget Alex approved);
   - `ZANS_ORCH_MAX_USD_PER_MONTH` = Alex sets this himself (failed runs count; no value is mandated here);
   - `ZANS_ORCH_ENABLED` = `true`.

   Then run one `live` test on a small synthetic text file. If the first call rejects a model setting, the run stops as BLOCKER (never PASS). That first call is the model compatibility check.

**Kill switch:** set `ZANS_ORCH_ENABLED` to `false`, or press Disable workflow in the Actions tab.

## Cost (an estimate, NOT a hard ceiling)
The code bounds tokens and refuses any run whose worst case is over `ZANS_ORCH_MAX_USD_PER_RUN`, or would take this month's reservations over `ZANS_ORCH_MAX_USD_PER_MONTH`, and re-checks the per-run budget before every call. That worst case uses the cautious $10 / $50 price for every call.

The largest possible run at the hard caps is $2.45 at those cautious prices. With the #26 checklist and a small file it is lower (about $1.10). A typical run costs far less: Claude Sonnet 5.5 is $2 / $10 per million tokens and gpt-6.2-astra is $8 / $40 (list prices, 25 Nov).

Real billing depends on each provider's own token count and current price. The dashboards are alerts, not guaranteed stops.

## Next phase (not in this PR)
This pilot is started by a button press. The goal is fully automatic Claude <-> ChatGPT review on #26 comments. That needs an `issue_comment` trigger restricted to trusted authors, a loop guard (ignore the orchestrator's own comments), and the same caps. It will be proposed as a separate PR once the pilot has run cleanly.

## Caveats
- This repo is **public**: anything the reviewers write in the summary comment is public too.
- Workflow runs count toward the repo's GitHub Actions minutes. Each run is about 1-2 minutes.
- The existing hourly ChatGPT review stays as the fallback.


## Correction handling (all paid routes)
- Any REVISE or REJECT (manual run: AGREED REVISE, NO AGREEMENT, STOPPED: rejected; daily batch, racing, retro: any reviewer verdict) opens a **correction gate** in the bot-posted summary, lists every fix (or the reasons, or a placeholder if none were given), and posts NO completion marker for that run. In the daily batch only PASSing items are marked complete.
- The gate blocks every paid route (manual, batch, racing, retro) until the 'ZANS correction receipt' workflow posts a bot-authored receipt with exactly one decision per fix, numbered 1 to N: `N=applied <40-hex commit> <changed path> <sha256 of that file at the commit>` (the commit must exist here, must have changed that path, and the file must hash to the stated value; one corrected file may back several fixes, whether it truly fixes them is decided by the independent re-review, not the receipt). A receipt with any applied fix does NOT close the gate: it posts a 'fix receipt' and the **ZANS racing re-review** workflow then runs an independent Claude + OpenAI review of exactly those corrected bytes (same caps, shared daily slot) and closes the gate, and its ancestor gates, only on a settled PASS/PASS. A receipt with only rejections closes the gate at once. or `N=rejected <reason of 10+ characters>`.
- **Automatic routing of fixes to a Claude thread and automatic re-review are NOT built: BLOCKED.** The gate is the enforced stop: paid runs stay stopped after a REVISE until a person closes it with evidence. Alex's decision 27 Nov: the route need not be private.

### Known limitation: one GitHub login
Alex, Claude and ChatGPT all act through the same GitHub login, so comments cannot prove who wrote them. The gate therefore never trusts a human-authored comment: a gate opens only from a `github-actions[bot]` comment and closes only from a `github-actions[bot]` receipt posted by the receipt workflow (main branch, allowlisted login), and an `applied` decision must name a commit that exists in this repo. This stops an ordinary comment from impersonating a correction or a receipt. It does NOT prove that a Claude revision was made by Claude, and the receipt workflow is manual: this is not an automatic correction-to-Claude-to-OpenAI loop and must not be described as one. A signed receipt would need a repository secret that only the owner can create; none is configured.

## Correction loop status (27 Nov, updated)
- **Automatic re-review after a receipt** (OFF by default). If the owner sets the repository variable `ZANS_ORCH_AUTO_REREVIEW` to `mock` or `live`, the `ZANS correction receipt` workflow runs the independent re-review in the same job right after posting a receipt that has at least one applied fix. It uses the same code, actor allowlist, kill switch, daily ceiling, monthly cap, no-retry guard and closure rule as the manual workflow; API keys are only passed when the variable is `live`. Unset = manual, as before.
- **A rejection-only receipt can no longer close a gate.** It posts a `zans-orch-rejected` marker, the gate stays open and every paid route stays blocked until a changed file passes a PASS/PASS re-review (or the owner decides how to close it).
- The re-review prompt carries every original gate item with its disposition and each reviewer must state `ITEM N: RESOLVED` per item; the gate (and its ancestors) closes only inside the settlement comment of a settled PASS/PASS.
- **Chunked review for full detail.** A file too big for one call is split by race into at most 3 prompts, each with the full header and the full detail of its races (nothing truncated). Each chunk is reviewed by both providers; the worst verdict wins; a reviewer that missed a chunk is a BLOCKER. The per-call input cap stays 30,000 tokens; cost scales with the chunk count (worst-case reservation up to 3x). A file that fits one prompt is sent exactly as before.
- Racing files dated 2026-11-28 or later must carry the V2 fields (explicit null allowed) and a data-gap pick must be capped at confidence 6. From 2026-11-29 every race also carries `zans_reasons`, `cautions`, `best_price`, `data_chance` (explicit null allowed on a race with no pick) and every picked race must have usable `zans_reasons`, `cautions` and `data_chance`, or the file is refused before any call.
