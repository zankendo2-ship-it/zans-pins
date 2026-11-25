# ZANS two-reviewer check (Claude + OpenAI): PILOT, OFF BY DEFAULT

**What it does:** you start it by hand. It reads issue #26 and the file links you give it. Claude reviews first, then OpenAI, then up to 3 rounds where each sees the other's verdict. It posts **one** summary comment: AGREED, REJECTED, BLOCKER or NO AGREEMENT.

**What it never does:** deploy, publish, list, post to social, order, or spend beyond its capped API calls. Agreement between the two reviewers is **not** Alex's approval.

## Safety built in
- **Manual start only** (`workflow_dispatch`). There are no comment, push or schedule triggers, so it cannot start itself. Its summary comment is posted with `GITHUB_TOKEN`, which GitHub does not let start other workflows.
- **Off by default.** Live (paid) runs only happen when the repository variable `ZANS_ORCH_ENABLED` is `true`. The free `mock` run works while it is off, so it can be tested first.
- **Allowlist.** The person starting it must be listed in `ZANS_ORCH_ALLOWED_ACTORS`.
- **Immutable inputs.** Artifact links must be pinned to a 40-character commit SHA.
- **Hard caps in the code.** Provider budgets are alerts, not guaranteed stops, so these are enforced before any call:
  - 3 rounds;
  - 6 API requests per run;
  - 1,500 output tokens per call;
  - 120 s per call;
  - 10 min per run;
  - **5 runs per day** (a repo variable can only lower this);
  - **estimated input of 120k tokens per run**; anything over is refused before any call;
  - **up to 6 files, 60 KB per text file, 120 KB in total**. Images are passed by link only, never uploaded;
  - 24k characters of issue context;
  - files only from `zankendo2-ship-it` repos;
  - one run at a time (concurrency lock).
- **Shared context.** Every review loads `orchestrator/ZANS_RULES.md` (the shared project rules and quality standards), the #26 issue body (the open checklist), the newest #26 comments, and the text of the pinned files.
- **Dedup.** It skips a task + artifact set it has already reviewed (hash marker in the summary).
- **Untrusted data.** Issue comments and artifacts go to the models inside untrusted-data markers, which the models are told to ignore instructions in. Any reply that isn't a valid verdict counts as BLOCKER, never PASS.
- **No secrets or comment text in logs.** Keys are only passed in `live` mode and are never printed. The job has `contents: read` and `issues: write` only.
- **Dry-run first.** `mock` mode makes no model calls. The 23 tests run before every review.

## Activation order (agreed 25 Nov)
- Keep `ZANS_ORCH_ENABLED` = `false` until ChatGPT has approved this code AND a free `mock` run has passed.
- Keys go ONLY into encrypted GitHub secrets. Never put them in code, comments or either chat. This repo is public.

## Alex's setup steps
1. Merge this PR into `main`. GitHub only offers manual workflows that are on the default branch.
2. Repo **Settings > Secrets and variables > Actions > Secrets**: add `ANTHROPIC_API_KEY` and `OPENAI_API_KEY`. Never paste keys in chat or issues.
3. Same page, **Variables**:
   - `ZANS_ORCH_ALLOWED_ACTORS` = your GitHub username;
   - `ANTHROPIC_MODEL` and `OPENAI_MODEL` = the model names you're paying for;
   - `ZANS_ORCH_ENABLED` = `true`.
4. Set a monthly spending limit in both API dashboards (Anthropic Console, OpenAI Platform).
5. **Actions > ZANS two-reviewer check > Run workflow.** Try `mock` first, then `live`.

**Kill switch:** set `ZANS_ORCH_ENABLED` to `false`, or press Disable workflow in the Actions tab.

## Cost estimate (a guide, not a promise)
Each live run is at most 6 calls of roughly 8k input tokens and up to 1.5k output tokens each. That's about 50k input and 9k output tokens per run at the cap, usually less. At typical list prices this is a few tens of pence per run on mid-tier models, and more on top-tier models. Check current prices on each provider's pricing page; this is an estimate, not a quote.

Reviewing long documents or code costs more than a short check. The token cap above is the hard ceiling per run, and the 5-runs-a-day cap limits daily use.

## Next phase (not in this PR)
This pilot is started by a button press. The goal is fully automatic Claude <-> ChatGPT review on #26 comments. That needs an `issue_comment` trigger restricted to trusted authors, a loop guard (ignore the orchestrator's own comments), and the same caps. It will be proposed as a separate PR once the pilot has run cleanly.

## Caveats
- This repo is **public**: anything the reviewers write in the summary comment is public too.
- Workflow runs count toward the repo's GitHub Actions minutes. Each run is about 1-2 minutes.
- The existing hourly ChatGPT review stays as the fallback.
