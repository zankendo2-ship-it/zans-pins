# ZANS two-reviewer check (Claude + OpenAI): PILOT, OFF BY DEFAULT

**What it does:** you start it by hand. It works on issue #26 only. It reads the #26 checklist, the newest #26 comments and the TEXT files you link. Claude reviews first, then OpenAI, then up to 3 rounds where each sees the other's verdict. It posts **one** summary comment: AGREED, REJECTED, BLOCKER or NO AGREEMENT.

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
  - **1 live (paid) run per UTC day** to start with. Live needs `ZANS_ORCH_MAX_RUNS_PER_DAY` = `1` set explicitly; empty or invalid means 0 live runs. Raising the ceiling needs a code change and a review;
  - **owner budgets:** live needs `ZANS_ORCH_MAX_USD_PER_RUN` (Alex approved `3`) and `ZANS_ORCH_MAX_USD_PER_MONTH` (Alex approved `10`). Missing, zero, negative or non-finite (`nan`, `inf`) values refuse live. Every call is priced at $10 in / $50 out per million tokens, which is above every allowed model's 25 Nov list price:
    - **before the run**, the worst case is worked out. The run is refused if that is over the per-run budget, or if it plus this month's reservations is over the monthly budget;
    - the worst case is **reserved in the slot comment** before any paid call, so failed runs count against the month;
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
- **Dedup.** It skips a mode + task + artifact set it has already reviewed. Mock and live have separate keys, so a mock never blocks the live run.
- **Untrusted data.** Issue comments and artifacts go to the models inside untrusted-data markers, which the models are told to ignore instructions in. Any reply that isn't a valid verdict counts as BLOCKER, never PASS. That includes wrong field types, such as reasons not being a list of text.
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
   - `ZANS_ORCH_MAX_USD_PER_MONTH` = `10` (the monthly budget Alex approved; failed runs count);
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
