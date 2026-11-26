# v5 print-check drafts approval (one-shot)

Only after Alex says yes to Q1 **in his own words**:
1. Copy `tools/print_drafts/approval.TEMPLATE.json` to `tools/print_drafts/approval.json`. No other keys.
2. `run_id` = `v5drafts-<YYYYMMDD>-<NN>` (new number every time; a used run_id is refused).
3. `approved_by` = `Alex`, `approved_at` = UTC time of his yes, `source` = the cmsg_ id of HIS message.
4. Commit that file ALONE (added in that commit) and push to `zans-social-notes (zans-pins)`.
   That push is the only thing that starts `.github/workflows/print-drafts.yml`.

The run never publishes, orders, retries a POST or deletes. Deleting the drafts needs Alex's separate yes.

Repo secrets the workflow needs (zans-pins): `PRINTIFY_API_KEY`, and `PRINT_DRAFTS_ADDRESS` = the UK delivery address as one JSON
object (first_name, last_name, address1, city, zip, country "GB") used only for the postage quote. The address is never committed.
Tests: `python -m pytest -q tools/print_drafts/print_qa/tests`.
