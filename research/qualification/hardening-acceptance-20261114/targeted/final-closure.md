# Final targeted closure after independent review

Date: 2026-11-14. Baseline/HEAD remains `98cd57ef8d0ba5e919c505466fa82f4e4653b9fe` in detached `megafon_hack-hardening-e2e`. No product source, Skills, historical cases, `main`, or feature branch were changed. No commit or push was created. PID 6568 was not terminated. No full E2E or paid call was made.

## Final verdict

**Product P0/P1: none confirmed by the independent review.** The reviewer reported no product-integrity P0/P1; findings F1–F5 are P1 issues in targeted test fixtures/harness/checker. F6 is a P2 calculation-receipt provenance issue. These findings block acceptance of the targeted QA changes and block using them as a release gate. They do not establish that the hardening product itself has a P1 defect.

**H02 remains BLOCKED as test-infrastructure coverage.** The old aggregate loss is confirmed; its cause is not. “Serialization caused the hang” remains unproven. New single-boundary attempts self-exited code 90 within their deadlines, but CIM identity was denied, so their result is `BLOCKED_IDENTITY_UNVERIFIED`; no cleanup command ran. The reviewer found a boundary-1 hardcode, non-atomic receipt writes, and missing trustworthy immediate process metadata in the harness. Do not use this H02 implementation to certify crash recovery.

**Targeted QA packet: NOT ACCEPTED / BLOCKED, per reviewer. Product pre-release merge: CONDITIONAL only as a separate owner decision.** Since no product P0/P1 was found, the review does not prove a product blocker. A limited pre-release merge of the already-reviewed product baseline may be considered only if the release owner accepts H02 as an explicit uncovered infrastructure gate and records that full acceptance is incomplete. The harness/checker edits from this closure should not be merged as verified fixes: F1–F5 remain open and must be corrected/re-reviewed before those tools are relied on. No approval to merge is given here.

The independent reviewer was the already-running task `01a1db10-f5b1-7be0-806f-64c8a3cec0de`; no additional reviewer was started. Final result `NOT_ACCEPTED_BLOCKED`, exact findings and independent commands are in [independent-review.md](../independent-review.md) and [independent-review.json](../independent-review.json). The reviewer did not inspect raw/private sessions, rerun full E2E, stop processes, or make paid calls.

## Review findings reconciled with evidence

| Reviewer finding | Reconciliation | Closure status |
|---|---|---|
| F1 P1: T01 R2 denominator is not operative | Confirmed. R2 retains the all-eligible-starts primary section and appends a contradictory completers-only note. The earlier boolean searched only for the phrase; distinct hashes do not prove a changed metric. | BLOCKER; T01 denominator test FAIL. Do not rely on candidate as a valid R2. |
| F2 P1: R2 manifest self-hash / nested dependency paths | Confirmed. `targeted-closure.ps1` enumerated the already-existing manifest and copied dependencies into an existing destination. Expected self-hash differs from actual manifest hash; dependency paths are misnested. | BLOCKER; candidate COMPLETE claim invalid. Do not patch/reseal it as if it passed. |
| F3 P1: H02 hardcoded identity check | Confirmed in current `run-one-boundary.ps1`: check still matches literal `-Boundary 1`; exception path also mislabels. Receipts show CIM denied and blocked identity. Boundary 2 earlier receipt has stale boundary-1 signal path and is historical evidence only. | BLOCKER; H02 identity/cleanup unverified. No process was stopped. |
| F4 P1: receipts are non-atomic | Confirmed. Both runner and checker write canonical receipts directly. Per-boundary receipts reduce cross-boundary loss but remain vulnerable to truncation. | BLOCKER for harness durability. |
| F5 P1: checker omits resume invariants | Confirmed. Current checker does not enforce parent manifest digest, unique complete-child/fork, exact claim-set equality or path containment. Positive/negative fixtures prove only note tolerance and operative-revision mismatch. | BLOCKER for using checker as complete resume validator. |
| F6 P2: T04 receipt overstates command execution | Confirmed. Totals and hash mutation reproduce independently, but `executed_command` is recorded as text while calculations are performed by separate inline statements and `exit_code=0` is assigned. | Values PASS as independently reproducible PowerShell aggregates; receipt provenance LIMITED. Not conversion. |

No reviewer finding alleges a product P0/P1. The original acceptance T03/T05/T06/T07/T08/T09 evidence remains scoped to its recorded runs; this closure did not repeat it. New-chat context provenance remains PARTIAL because host thread IDs show separate tasks but do not attest complete context/cache isolation.

## Targeted statuses

| Check | Final status |
|---|---|
| T01 full revisions | Prior acceptance evidence stands for R1→R2 preservation in LabSlot; new denominator subcheck **FAIL** (non-operative/contradictory R2 and invalid manifest). |
| T02/H02 | **BLOCKED**. Old forced-run aggregate absent; cause UNKNOWN. New one-boundary processes exited 90, but identity was unverified and receipts non-atomic. |
| T03 claim fork | Prior run PASS within its observed synthetic fixture; current checker is not a complete fork gate (F5). |
| T04 source mutation | **PASS for source hash, 18/13/6 aggregate computation and disposable-copy mutation; receipt provenance LIMITED (F6).** `orders/opens` is an aggregate ratio, not conversion. |
| T05 abandonment | Prior run PASS within observed fixture; no rerun. |
| T06 D30 | Prior run PASS within observed fixture; controlling definition remains UNKNOWN. |
| T07 stale approval | Prior run PASS for observed refusal; no rerun. |
| T08 clean case | Prior single-host run PASS; no rerun. |
| T09 new-chat | Prior resume evidence PASS for distinct tasks; isolation provenance PARTIAL. |
| Checker operational note | PASS, exit 0, 28 hashes match, receipt and fixture cross-checked. |
| Checker operative revision mismatch | CONFLICT, exit 1, receipt and fixture cross-checked. This does not establish the missing F5 invariants. |

## Changed files in this closure

Tracked product and historical files changed: **none**. Git remains detached at the baseline SHA; all additions are untracked under `acceptance/`.

Harness/checker edits (not accepted for merge):

- `acceptance/20261114-dynamic/verify-checkpoints.ps1`
- `acceptance/20261114-dynamic/run-one-boundary.ps1`
- `acceptance/20261114-dynamic/targeted-closure.ps1`

Procedures and decision records:

- `acceptance/20261114-dynamic/targeted/closure-report.md`
- `acceptance/20261114-dynamic/targeted/final-closure.md` (this verdict)
- `acceptance/20261114-dynamic/h02-manual-procedure.md`
- `acceptance/20261114-dynamic/independent-review.md`
- `acceptance/20261114-dynamic/independent-review.json`
- `acceptance/20261114-dynamic/targeted/t01-denominator.json`
- `acceptance/20261114-dynamic/targeted/t04-source-receipt.json`
- `acceptance/20261114-dynamic/receipts/checker-operational-note-final.json`
- `acceptance/20261114-dynamic/receipts/checker-operative-conflict-v2.json`
- `acceptance/20261114-dynamic/targeted/h02-boundary-01.json` (normalized failure summary)
- `acceptance/20261114-dynamic/targeted/h02-boundary-02.json` (stale signal path; exclude as current proof)
- `acceptance/20261114-dynamic/targeted/h02-boundary-03.json` (current bounded blocked observation)
- `acceptance/20261114-dynamic/targeted/t04/pilot-alerts-mutated.csv` (synthetic disposable copy)

The reviewer JSON contains its own full changed-review scope and commands. Other acceptance files from the earlier run predate this closure and were not edited in this step.

## Minimal reproduction and safe handoff

Read-only: `Get-Content -Raw -Encoding UTF8 acceptance/20261114-dynamic/independent-review.md`.

Checker positive: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File acceptance/20261114-dynamic/verify-checkpoints.ps1 -Case acceptance/20261114-dynamic/targeted/checker-operational -Label checker-operational-note-final` → PASS, exit 0, 28 hashes.

Checker negative: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File acceptance/20261114-dynamic/verify-checkpoints.ps1 -Case acceptance/20261114-dynamic/targeted/checker-operative-conflict -Label checker-operative-conflict-v2` → CONFLICT, exit 1.

T04 independent check command is in the review's “T04 source/disposable hash and aggregates” section. Expected original source SHA `39647f1023fb31484f0acf7db7fcadb99a605f108ccda4882a0a898f6c42d5e4`, totals `18/13/6`; disposable SHA `f11bf9f8217f1a7b700cf5c04ca884e2d2628051d6605cd3d16b6ff63c777e19`, generated `19`.

T01 reproduction commands are in reviewer sections 1, 4 and 5. They establish distinct hashes and expose the contradictory operative text/self-hash; they do not PASS denominator migration.

H02 procedure is intentionally BLOCKED in this host. Do not run the old 12-boundary loop. A future manual H02 retry requires verified immediate PID/start/parent/executable/command identity and a per-boundary durable receipt. On any metadata denial, leave the process running and preserve BLOCKED. Never stop PID 6568.

**Safe Git handoff:** keep this closure and all raw command receipts, native task readbacks, synthetic fault trees, mutated CSV and any ZIP/archive local and untracked. Do not publish raw TUI logs or the previous `mgimo-hardening-acceptance-20261114.zip` as a project artifact. If a review needs a shareable summary, publish only a separately redacted/reviewed Markdown summary and the minimal synthetic scripts/fixtures after correcting F1–F5 and rerunning their scoped review. This session created no branch, commit, tag, push or PR. Product pre-release merge, if considered, is a separate owner decision with H02 explicitly uncovered and no claim of full acceptance.
