# ZANS two-reviewer check (Claude + OpenAI): PILOT, OFF BY DEFAULT

**What it does:** you start it by hand. It reads issue #26 and the file links you give it. Claude reviews first, then OpenAI, then up to 3 rounds where each sees the other's verdict. It posts **one** summary comment: AGREED, REJECTED, BLOCKER or NO AGREEMENT.

**What it never does:** deploy, publish, list, post to social, order, or spend beyond its capped API calls. Agreement between the two reviewers is **not** Alex's approval.

## Safety built in
- **Manual start only** (`workflow_dispatch`). There are no comment, push or schedule triggers, so it cannot start itself. Its summary comment is posted with `GITHUB_TOKEN`, which GitHub does not let start other workflows.
- **Off by default.** It only runs when the repository variable `ZANS_ORCH_ENABLED` is `true`.
- **Allowlist.** The person starting it must be listed in `ZANS_ORCH_ALLOWED_ACTORS`.
- **Immutable inputs.** Artifact links must be pinned to a 40-character commit SHA.
- **Caps:**
  - 3 rounds;
  - 6 API requests;
  - 1,500 output tokens per call;
  - 120 s per call;
  - 10 min per run;
  - 24k characters of issue context;
  - one run at a time (concurrency lock).
- **Dedup.** It skips a task + artifact set it has already reviewed (hash marker in the summary).
- **Untrusted data.** Issue comments and artifacts go to the models inside untrusted-data markers, which the models are told to ignore instructions in. Any reply that isn't a valid verdict counts as BLOCKER, never PASS.
- **No secrets or comment text in logs.** Keys are only passed in `live` mode and are never printed. The job has `contents: read` and `issues: write` only.
- **Dry-run first.** `mock` mode makes no model calls. The 23 tests run before every review.

## Alex's setup steps (only when you decide to switch it on)
1. Merge this PR into `main`. GitHub only offers manual workflows that are on the default branch.
2. Repo **Settings > Secrets and variables > Actions > Secrets**: add `ANTHROPIC_API_KEY` and `OPENAI_API_KEY`. Never paste keys in chat or issues.
3. Same page, **Variables**:
   - `ZANS_ORCH_ALLOWED_ACTORS` = your GitHub username;
   - `ANTHROPIC_MODEL` and `OPENAI_MODEL` = the model names you're paying for;
   - `ZANS_ORCH_ENABLED` = `true`.
4. Set a monthly spending limit in both API dashboards (Anthropic Console, OpenAI Platform).
5. **Actions > ZANS two-reviewer check > Run workflow.** Try `mock` first, then `live`.

**Kill switch:** set `ZANS_ORCH_ENABLED` to `false`, or press Disable workflow in the Actions tab.

## Cost estimate
Each live run is at most 6 calls of roughly 8k input tokens and up to 1.5k output tokens each. That's about 50k input and 9k output tokens per run at the cap, usually less. At typical list prices this is a few tens of pence per run on mid-tier models, and more on top-tier models. Check current prices on each provider's pricing page; this is an estimate, not a quote.

## Caveats
- This repo is **public**: anything the reviewers write in the summary comment is public too.
- Workflow runs count toward the repo's GitHub Actions minutes. Each run is about 1-2 minutes.
- The existing hourly ChatGPT review stays as the fallback.
