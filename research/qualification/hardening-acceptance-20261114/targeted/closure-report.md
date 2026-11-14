# Targeted acceptance closure

Baseline remains `98cd57ef8d0ba5e919c505466fa82f4e4653b9fe`. No full E2E rerun, product/skill/history edits, paid calls, commit, push or feature-branch change. All additions remain untracked under `acceptance/20261114-dynamic/`.

## H02 finding and disposition

**Confirmed test-infrastructure defects:** the prior runner launched a child without durably journaling child identity at creation, accumulated all observations in memory until the end, and had no overall timeout around finalization. `replay-interruptions.ps1` shows per-boundary loop timeouts but no whole-run/final-write timeout; the saved PID diagnostic has no pre-launch PID receipt. At all 12 observed boundary messages, the final aggregate receipt is absent. This establishes missing/late per-boundary evidence and unsafe cleanup provenance; it does **not** prove serialization was the cause of the hang. Serialization remains an unconfirmed inference. The old loop reported stop messages and success-shaped text, but no reliable immediate process receipt per boundary.

Changed [run-one-boundary.ps1](run-one-boundary.ps1) to run exactly one boundary per invocation, bound identity observation and child wait, persist a separate receipt, and never terminate a process. It records expected executable/command/parent/start time and checks PID metadata if CIM returns it. If metadata cannot be read, result is BLOCKED and the process is left alone. Receipts are ordinary direct writes, not atomic replace; do not claim stronger crash durability.

Three one-boundary runs were attempted. Boundary 1 child exited 90; CIM access denied; original implementation serialized a FileInfo object as the signal and produced a 98MB receipt. That receipt was reduced to a 554-byte summary; this does not conceal the error, which is described here. Boundaries 2 and 3 each exited 90 within the 12-second deadline, with individual 1.2KB receipts and correct signal strings. Identity checks were **BLOCKED** because CIM access was denied. No Stop-Process was called. **H02 identity/cleanup remains BLOCKED.** OMP-specific shell integration is unavailable in this environment; PowerShell fallback is real, not a claimed OMP execution.

Do not use `Stop-Process` based on PID alone. Exact future manual stop rule and PowerShell test procedure are in [H02 procedure](h02-manual-procedure.md). Keep the pre-existing PID 6568 untouched.

## Checker contract and regression

The canonical skill requires selected manifest ID/hash/status and every immutable listed file hash; root `state.md` and `decision.md` must agree with the selected revision and active claims. It does not require root state bytes to equal the sealed state snapshot, so equality incorrectly rejected an operational note. Changed [verify-checkpoints.ps1](verify-checkpoints.ps1) to keep exact SHA checks for manifest-pinned snapshots/dependencies but check root operative revision and active-claim declarations semantically. Unknown/missing selector, operative revision mismatch, claim mismatch and hash failures remain conflicts.

Executed: PowerShell checker on a valid R1 case with an appended operational note returned **PASS, exit 0, 28 hashes** (`receipts/checker-operational-note-final.json`). A root operative revision changed while selector remains R1 returned **CONFLICT, exit 1** (`receipts/checker-operative-conflict-v2.json`). This positive/negative pair avoids incorrectly requiring byte-equal root state; immutable snapshot hashes are still checked.

## T01 and T04

T01 used separate `targeted/t01-denominator/` copy. R1 `test-plan.md` SHA-256 `ac87df36d79e71801d2ea00099f1709761b26620ae1ef453d99c2ec24d4be547` retains all eligible started attempts, including abandonment/missing. R2 candidate SHA-256 `15968547efcfe1e883c5f9487ef4d792902244c10ec65c38fab3808dafe42cc7` explicitly uses completers-only. Content and hash differ. This proves historical-contract separation for a candidate; it is not published/selected as a product recommendation. Inputs and old case are untouched. Receipt: `targeted/t01-denominator.json`.

T04 executed the runbook command against original `cases/unseen-shelf-alerts-20261114/input/pilot-alerts.csv`, SHA-256 `39647f1023fb31484f0acf7db7fcadb99a605f108ccda4882a0a898f6c42d5e4`, PowerShell 5.1.26100.9818, exit 0. Totals generated=18, opened=13, orders=6; aggregate ratios opened/generated=13/18, orders/generated=6/18, orders/opened=6/13. **orders/opens is not conversion.** Disposable copy only changed generated 18→19; SHA changed to `f11bf9f8217f1a7b700cf5c04ca884e2d2628051d6605cd3d16b6ff63c777e19`. Full literal command and results: [T04 receipt](targeted/t04-source-receipt.json); disposable bytes: [mutated copy](targeted/t04/pilot-alerts-mutated.csv).

## New-chat provenance

Native Codex task/thread IDs and creation/read metadata are host-generated evidence of separate tasks. The prior acceptance retained create-thread results and observer logs. Full context isolation is **PARTIAL**: the runtime inherits the same workspace, and there is no host attestation here that context/cache state is isolated. No raw private session was exported or committed.

## Status and merge assessment

T01 targeted denominator separation **PASS**; T04 source hash/calculation/disposable mutation **PASS**; checker positive and negative regressions **PASS**. T02/H02 improved runner **BLOCKED** for identity metadata because this shell denies CIM. Original H02 aggregate cause **UNKNOWN**; it must not be called serialization without evidence. New-chat provenance **PARTIAL**. Prior T03/T05/T06/T07/T08/T09 evidence stands within the original report's stated scope; no full-suite repeat was performed. Overall targeted closure **PARTIAL/BLOCKED for H02**, not full acceptance PASS.

An independent read-only Codex review was requested at `targeted/independent-review-create.json`; its outcome is pending unless `independent-review.md` exists. **Do not merge harness/checker changes until that reviewer returns and H02 identity/receipt behavior is resolved or explicitly accepted as blocked by the merge owner.** No merge approval is implied by this packet.
