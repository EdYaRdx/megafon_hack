# Clean-host E2E and regression runbook

Status: **NOT RUN in this session**. This is an exact acceptance procedure, not evidence of a PASS. No shell, Git, host UI, model, or product runtime was available. Use a disposable copy/worktree of the reviewed feature checkpoint; never run fault injection against the only case copy. Do not use OMP or paid providers as product runtime.

## Environment and evidence

- Host: record OS, coding-assistant product/version, model identifier if exposed, skills discovery result, permissions, and whether shell/calculation tools are available. `UNKNOWN` is valid.
- Start from a clean checkout/archive of the feature branch and a new copy of `cases/_template/`; preserve tool logs without credentials/raw private sessions.
- Record each test's input file hashes, exact commands, exit code, stdout/stderr, created files, active revision/hash and reviewer. Hash command in PowerShell: `Get-FileHash -Algorithm SHA256 -LiteralPath <path>`.
- Use only synthetic fixtures and public sources. No real user contact, spend, launch, submission, or private MegaFon material.

## R1 → R2 historical reconstruction

1. Inspect the historical Codex acceptance package without editing it: R1 decision references R2 `options.md`; compare its revision folder inventory with current R2 options/strategies/plan.
2. Expected result: classify R1 as historically incomplete for those dependencies. Do **not** invent/recreate its missing outputs. New protocol should preserve all such files in future checkpoints.
3. On a new synthetic case, create R1 complete manifest, then R2 with changed options and test-plan denominator. Verify R1 opens its original versions and R2 opens its updated versions; every listed source/dependency hash matches.
4. PASS only when both snapshots and pinned dependencies are readable and distinct where changed. Historical Codex R1 cannot pass step 3 because those files do not exist.

## Interrupted write

1. Create a fresh case, complete R1 and set root `state.md`/`decision.md` to R1 revision ID and active claims. Write root `ACTIVE.json` with R1 ID + complete-manifest SHA-256.
2. Begin R2 in a separate revision folder. Interrupt after each required snapshot and dependency copy, and again after files but before `manifest.json`; do not write a COMPLETE manifest.
3. Start a fresh chat/process and follow `resume-revise`. Expected: R1 remains current; partial R2 is INCOMPLETE and ignored, with no mixed R1/R2 files.
4. Repeat with a complete verified R2 manifest but interrupt before touching root `state.md`, `decision.md`, or `ACTIVE.json`. Expected: R1 remains selected; verified R2 is not current.
5. Interrupt after changing either root state/decision but before the remaining file and selector are consistent; then separately interrupt while writing `ACTIVE.json`. Expected: explicit CONFLICT (never silently claim R1 remains current); recover manually from the prior immutable R1 snapshot. Atomic replacement is not assumed.
6. PASS requires observed filesystem results for each boundary. File instructions alone are not a PASS. If these failures show manual protocol cannot satisfy the invariant, then—and only then—scope a small deterministic check/publish helper.

## Claim fork / order independence

1. In a synthetic JSONL, include C-002 and two successors C-003/C-005, then select C-005 in the complete manifest and state/decision.
2. Reverse JSONL line order without changing records or active selection. Expected active claim remains C-005.
3. Remove the explicit active selection or list both incompatible successors. Expected INCOMPLETE/CONFLICT, not an automatic winner.
4. For the StudyTrack historical case, verify `C-005` is explicitly selected and `C-003` is explanatory. Do not call the present decision wrong.

## Source mutation and receipt

For a new scratch case using `cases/unseen-shelf-alerts-20261114/input/pilot-alerts.csv`, first record the source hash:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath .\cases\unseen-shelf-alerts-20261114\input\pilot-alerts.csv
```

Run a source-bound calculation in PowerShell (record the literal command, current directory, `$PSVersionTable.PSVersion`, exit status and raw output in the case receipt):

```powershell
$rows = Import-Csv -LiteralPath .\cases\unseen-shelf-alerts-20261114\input\pilot-alerts.csv
$generated = ($rows | Measure-Object -Property alerts_generated -Sum).Sum
$opened = ($rows | Measure-Object -Property alerts_opened -Sum).Sum
$orders = ($rows | Measure-Object -Property orders_within_7d -Sum).Sum
[pscustomobject]@{ generated=$generated; opened=$opened; orders=$orders; opened_per_generated=($opened/$generated); orders_per_generated=($orders/$generated); orders_per_opened=($orders/$opened) } | ConvertTo-Json -Compress
```

Expected values for this supplied synthetic CSV: generated=18, opened=13, orders=6; ratios 13/18, 6/18, 6/13. They are ratios of aggregate record counts, not conversions. Mutate one value in a disposable copy and verify old revision hash mismatch or a new revision with a newly captured hash and recalculated result. Never mutate the historical case input.

## Abandonment denominator

Use deterministic synthetic attempts: 2 unaided successes, 1 assisted completion, 1 failure, 2 abandonments, 1 timeout, and 1 missing outcome; all 8 eligible attempts started. Expected primary unaided task success is 2/8 (25%), not 2/2 among completers. Report other outcomes separately with denominator 8; missing outcome is not success. Apply identical eligibility/exclusion logic to comparator. A run using the case's old wording is NOT a pass; only verify the future protocol/implementation behavior.

## D30 incompatibility

Use two synthetic contracts: (A) any qualifying event in days 1–30 with mature eligible cohort; (B) a named event exactly on calendar day 30 among calendar cohort signups. Include one user returning only on day 45 and one user active on day 10 but not day 30. Expected: do not pool; A/B outputs differ and controlling definition stays UNKNOWN until authority chooses. If testing on-or-after, define one shared follow-up cutoff and cohort maturity first. No vendor default is the product contract.

## Stale approval

1. Record an approval for a clearly synthetic action/scope bound to R1 ID and exact COMPLETE manifest SHA-256; preserve its ledger row.
2. Create R2 with changed scope or decisive premise/hash. Attempt to use R1 approval for R2.
3. Expected workflow decision: STOP, approval mismatch; require a distinct approval naming R2/hash/action/scope. Verify no host action occurred; instruction-only behavior is not a security enforcement test.

## Fresh blank case

1. Copy only `cases/_template/` to a new case ID and provide a novel synthetic brief not found in existing cases. Do not copy solved answers or prefill ledgers.
2. Open the repository in the target assistant, record normal skill discovery/use separately from any manual fallback. Follow intake, research, options, both strategies, test-plan, decision, and revision skills as needed.
3. Confirm the user receives a comprehensible decision memo, 3+ distinct options (status quo and stop where applicable), traced evidence/UNKNOWNs, aligned product/communication strategy, valid metric contract or honest blocker, and exact next human choice. Check created files, receipts, approvals and revision completeness from disk.
4. Save state, start a genuinely new chat/process with no transcript handoff, and verify file-only resume. Do not call OMP-context work a clean-host PASS.

## Run result table (fill only from actual execution)

| Check | Status | Artifact/command/result | Limits |
|---|---|---|---|
| R1 → R2 snapshots | NOT RUN | | Historical R1 dependencies absent |
| interrupted writes | NOT RUN | | No runtime/fault injection here |
| claim fork/order | NOT RUN | | Historical C-005 selection statically inspected |
| CSV hash/recalculation | NOT RUN | | No command executed here |
| abandonment denominator | NOT RUN | | Scenario specified only |
| D30 incompatibility | NOT RUN | | Scenario specified only |
| stale approval | NOT RUN | | No host gate enforcement observed |
| blank case/new-chat resume | NOT RUN | | No clean-host runtime available |

## Git checkpoint / PR handoff (not executed here)

Run from PowerShell only after independent review and local inspection. These commands do not change `main`; do not force-push. User-reported branch/start checkpoint: `codex/mgimo-hardening-20261114`, `8fc5f737bf4e506bc3683b9d468092858632ead3` (not independently verified in this session).

```powershell
$expectedBranch = 'codex/mgimo-hardening-20261114'
$startSha = '8fc5f737bf4e506bc3683b9d468092858632ead3'
if ((git branch --show-current) -ne $expectedBranch) { throw "Wrong branch; stop." }
git merge-base --is-ancestor $startSha HEAD
if ($LASTEXITCODE -ne 0) { throw "Expected start checkpoint is not an ancestor; stop." }
git status --short --branch
git diff --check
```

Inspect status and diffs; do not stage user-owned/unrelated changes. Stage only the reviewed files:

```powershell
git add -- AGENTS.md START-HERE.txt README.md references/evidence-and-claims.md references/metrics.md `
  .agents/skills/resume-revise/SKILL.md .agents/skills/experiment-design/SKILL.md `
  cases/_template/README.md cases/_template/decision.md cases/_template/state.md `
  cases/_template/test-plan.md cases/_template/approvals.jsonl cases/retention-demo/test-plan.md `
  docs/submission-architecture.md docs/submission-checklist.md docs/implementation-status.md docs/clean-host-e2e-runbook.md `
  research/product/hardening-triage-2026-11-14.md
git diff --cached --check
git diff --cached --stat
```

Review the staged diff and staged paths. If unrelated content is staged, stop and unstage only those known unrelated paths after inspection. Then create a local checkpoint and publish the feature branch/PR only with authorized credentials:

```powershell
git commit -m "fix: harden file-agent revisions and evidence"
git push -u origin codex/mgimo-hardening-20261114
gh pr create --base main --head codex/mgimo-hardening-20261114 --title "Harden file-agent revisions and evidence" --body "Implements complete file checkpoints, revision-bound approvals, metric/source receipt contracts, and product first-use routing. Dynamic clean-host regressions remain pending; see docs/clean-host-e2e-runbook.md."
```

Verify actual command exit statuses and record commit/PR URLs. If Git/GitHub credentials are unavailable, preserve local files and report the exact blocker; never force-push or switch/publish to `main`.
