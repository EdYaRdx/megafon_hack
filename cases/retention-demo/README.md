# Synthetic retention case — MVP slice

This is a fictional, self-contained demonstration of the file-first workflow. It is not MegaFon data, a real customer problem, or a validated business recommendation. The supplied cohort table is synthetic and exists only to exercise denominator, cohort-mix, missingness, claim-trace, option, and checkpoint handling.

Read `brief.md` and `state.md` first. Recheck source/evidence/claim links before relying on the recommendation. It is a draft for human review; it does not authorize a product change, user contact, experiment, or external communication.

## Artifacts

- `input/cohort-retention.csv` — synthetic cohort fixture.
- `sources.jsonl`, `evidence.jsonl`, `claims.jsonl` — source and reasoning trace.
- `options.md`, `decision.md` — distinct paths and recommended next step.
- `strategy-product.md`, `strategy-communication.md`, `test-plan.md` — linked strategy and gated validation plan.
- `activity.jsonl`, `state.md` — activity, open questions, and resume point.
- `revisions/state-r1.md`, `revisions/decision-r1.md` — exact revision-1 snapshots; current revision 2 adds E-008 and successor claim C-008.
- [`retention calculation check`](../../research/sol-audit/eval-results/retention-calculation-20261113.md) — jq query/output and limitations; arithmetic on synthetic fields only, not IDE acceptance.

Public-source snapshots are short notes with exact page locators, not full-page reproductions. A snapshot hash records those stored note bytes, not the source's truth.
