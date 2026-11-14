# Independent targeted acceptance review

Date: 2026-11-14 (Europe/Moscow)  
Scope: `verify-checkpoints.ps1`, `run-one-boundary.ps1`, `targeted-closure.ps1`, current targeted fixtures/receipts, original H02 receipts, `docs/clean-host-e2e-runbook.md`, and `.agents/skills/resume-revise/SKILL.md`.  
Review type: static review plus read-only recalculation/hash checks. No full E2E, private/raw session review, process termination, product mutation, or paid calls.

## Result

**NOT ACCEPTED / BLOCKED.** The operational-note positive and operative-revision conflict negative are supported by current receipts and match the current fixtures. T04 source metrics and disposable mutation reproduce. T01 does not establish a changed denominator: R2's operative section still specifies the R1 all-starts denominator, while an appended paragraph contradicts it. The R2 manifest also lists itself as a hashed file with a mismatching self-hash. H02 remains blocked by unverified process identity; the new boundary harness has a boundary-1 hardcode and writes receipts non-atomically.

## Findings

### F1 — T01 denominator change is contradictory and not operative (P1)

`targeted/t01-denominator/revisions/R0002/test-plan.md:13` still says the denominator is **all eligible started attempts**, including abandoned, timeout, failed, assisted, unfinished and missing outcomes. The appended note at line 58 says the fixture changes to completers only. Those statements conflict. The R2 check only searches for the phrase `completers only`, so its positive boolean does not prove the operative metric changed. R1 and R2 hashes are distinct, but the primary metric text remains R1's contract. Do not treat the T01 denominator version-separation check as passed.

### F2 — R2 manifest hashes itself and its self-hash mismatches (P1)

`targeted-closure.ps1:20` enumerates every existing file below R2 before writing the new manifest. On the current rerun fixture, `revisions/R0002/manifest.json` is included in `manifest.files`; its expected SHA-256 is `ffba21bbd8586d784fa0c14dcb5cfb78977f354ba3506c57be4d52bdc73ae130`, while the current manifest SHA-256 is `42345c93ab189bd9f1d50d0faef18a381e1949b286e9629c671832e875953435`. This is a self-referential, mismatching entry, so the manifest's `COMPLETE` label is not supported. The R2 dependencies are also nested under `dependencies/dependencies/`, rather than the expected single `dependencies/` level, as a result of copying into an already-created destination directory.

### F3 — H02 boundary identity validation is wrong for boundaries other than 1 (P1)

`run-one-boundary.ps1:26` checks the child command line for literal `-Boundary 1` even though the harness accepts `$Boundary`; line 41 also labels every exception receipt as boundary 1. The existing boundary-2 receipt identifies boundary 2 in the child command but points its signal argument at `h02-boundary-01.signal`, indicating that receipt belongs to an earlier harness version and must not be used as evidence for current code. The current script constructs a boundary-specific signal path, but the hardcoded identity comparison still blocks boundaries 2 and 3.

The current harness polls CIM for up to three seconds after launch, but does not capture a verified creation time, parent, executable, and command identity immediately from an independent source. CIM denial exits capture early. The recorded H02 receipts show `identity_confirmed=false`, CIM access denied, and `BLOCKED_IDENTITY_UNVERIFIED`; child exit 90 is not a PASS without identity attribution. No H02 rerun was attempted in this review.

### F4 — Boundary and checkpoint receipts are not atomic (P1)

`run-one-boundary.ps1:38,42` writes a final receipt directly with `File.WriteAllText`; a crash or interruption can leave a truncated receipt at the canonical per-boundary path. `verify-checkpoints.ps1:53` uses `Set-Content` directly for its receipt as well. The harness does not use a temporary sibling followed by an atomic replace/move. Timeout handling is conservative: it records a blocked result and does not terminate an identity-uncertain process. That avoids unsafe cleanup, but can leave a child process running after timeout; this limitation is recorded in the receipt and no process was stopped.

### F5 — Checkpoint checker does not enforce all resume-revise invariants (P1)

The checker verifies required snapshot entries, hashes for listed files, selector-to-selected-manifest hash, and selected root/snapshot revision and active-claim presence. However, it does not validate a selected manifest's `parent_manifest_sha256`, reject multiple COMPLETE children/forks, compare the root active claim set exactly with `active_claim_ids`, or ensure listed paths remain within the case root. The skill at `.agents/skills/resume-revise/SKILL.md` requires unique complete checkpoint recovery and verified parent/dependency hashes. The two checker fixtures cover only an operational note and an operative root revision mismatch; they do not cover these cases. Therefore checker PASS is useful but insufficient as a complete resume checkpoint gate.

### F6 — T04 values and mutation reproduce; receipt provenance overstates execution (P2)

The source hash is `39647f1023fb31484f0acf7db7fcadb99a605f108ccda4882a0a898f6c42d5e4`; the current source aggregates to generated 18, opened 13, orders 6, with ratios 13/18, 6/18, and 6/13. The disposable copy hash is `f11bf9f8217f1a7b700cf5c04ca884e2d2628051d6605cd3d16b6ff63c777e19`, and its generated total is 19. The original source was not modified. However, `targeted-closure.ps1:29-40` stores an `executed_command` string and hardcodes `exit_code=0` while computing via separate inline statements; it does not execute that literal recorded command or capture its actual exit status/stdout. The calculations reproduce, but the receipt should distinguish recorded command from actually invoked command.

## Targeted checks

- **Operational-note positive:** current fixture contains an operational note while keeping R0001 and C001-C008; `checker-operational-note-final.json` says PASS/exit 0, all 28 listed file hashes match, and its manifest hash matches the current fixture. Independent receipt/fixture check passed.
- **Operative-conflict negative:** current fixture state names R0002 while ACTIVE selects R0001; `checker-operative-conflict-v2.json` says CONFLICT/exit 1 and reports `Root state.md does not identify selected revision R0001`. Its manifest hash matches the current fixture. Independent receipt/fixture check passed.
- **T01:** hashes differ, R1 contains the all-eligible-started clause, R2 contains the appended `completers only` phrase, and R2 remains unselected. This detects byte-level separation but does not establish a changed operative denominator (F1/F2).
- **T04:** source-bound aggregates, source hash, disposable hash, and altered generated count reproduced as above.
- **H02:** existing original receipts are blocked on identity verification; the boundary-2 original receipt also contains a stale/mismatched boundary-1 signal path. No process was stopped or rerun.
- **Runbook:** `docs/clean-host-e2e-runbook.md` explicitly marks full clean-host E2E NOT RUN. This review does not change that status.

## Commands and exit statuses

All commands below were read-only PowerShell commands in `C:\Projects\GitHub\megafon_hack-hardening-e2e`; each returned exit code 0. Initial nested `powershell.exe -Command` quoting attempts were discarded: the first T01 and T04 wrappers exited 1 with parser errors, the second T01 wrapper exited 1, and the second T04 wrapper exited 0 but printed quoting/path errors without calculating results. Direct commands below then succeeded; no files were modified by those attempts.

1. T01 hash and wording check — exit 0:

```powershell
$ErrorActionPreference='Stop'; $t='acceptance/20261114-dynamic/targeted/t01-denominator'; $a=Get-FileHash -Algorithm SHA256 -LiteralPath "$t/revisions/R0001/test-plan.md"; $b=Get-FileHash -Algorithm SHA256 -LiteralPath "$t/revisions/R0002/test-plan.md"; $r1=Get-Content -Raw "$t/revisions/R0001/test-plan.md"; $r2=Get-Content -Raw "$t/revisions/R0002/test-plan.md"; [pscustomobject]@{R1=$a.Hash.ToLower();R2=$b.Hash.ToLower();Distinct=($a.Hash -ne $b.Hash);R1AllStarted=($r1 -match 'ALL eligible started');R2CompletersOnly=($r2 -match 'completers only');R2Unselected=((Get-Content -Raw "$t/ACTIVE.json") -notmatch 'R0002')} | ConvertTo-Json -Compress
```

2. T04 source/disposable hash and aggregates — exit 0:

```powershell
$ErrorActionPreference='Stop'; $s='cases/unseen-shelf-alerts-20261114/input/pilot-alerts.csv'; $d='acceptance/20261114-dynamic/targeted/t04/pilot-alerts-mutated.csv'; $rows=Import-Csv -LiteralPath $s; $g=($rows|Measure-Object alerts_generated -Sum).Sum; $o=($rows|Measure-Object alerts_opened -Sum).Sum; $n=($rows|Measure-Object orders_within_7d -Sum).Sum; $m=Import-Csv -LiteralPath $d; $mg=($m|Measure-Object alerts_generated -Sum).Sum; [pscustomobject]@{Source=(Get-FileHash -Algorithm SHA256 -LiteralPath $s).Hash.ToLower();Disposable=(Get-FileHash -Algorithm SHA256 -LiteralPath $d).Hash.ToLower();Generated=$g;Opened=$o;Orders=$n;OpenedPerGenerated=($o/$g);OrdersPerGenerated=($n/$g);OrdersPerOpened=($n/$o);MutatedGenerated=$mg} | ConvertTo-Json -Compress
```

3. Current positive/negative checker receipt-to-fixture cross-check — exit 0:

```powershell
$ErrorActionPreference='Stop'; $base='acceptance/20261114-dynamic'; $o=Get-Content -Raw "$base/receipts/checker-operational-note-final.json" | ConvertFrom-Json; $n=Get-Content -Raw "$base/receipts/checker-operative-conflict-v2.json" | ConvertFrom-Json; $om=Get-FileHash -Algorithm SHA256 -LiteralPath "$base/targeted/checker-operational/revisions/R0001/manifest.json"; $nm=Get-FileHash -Algorithm SHA256 -LiteralPath "$base/targeted/checker-operative-conflict/revisions/R0001/manifest.json"; $os=Get-Content -Raw "$base/targeted/checker-operational/state.md"; $ns=Get-Content -Raw "$base/targeted/checker-operative-conflict/state.md"; [pscustomobject]@{PositiveReceiptPass=($o.status -eq 'PASS' -and $o.exit_code -eq 0 -and @($o.issues).Count -eq 0);PositiveManifestCurrent=($o.selector.manifest_sha256 -eq $om.Hash.ToLower());PositiveNotePresent=($os -match 'Operational note: review heartbeat');NegativeReceiptConflict=($n.status -eq 'CONFLICT' -and $n.exit_code -eq 1 -and @($n.issues).Count -gt 0);NegativeManifestCurrent=($n.selector.manifest_sha256 -eq $nm.Hash.ToLower());NegativeHasOperativeRevisionMismatch=($ns -match '(?m)^- Active complete revision ID: R0002');PositiveCheckedFiles=@($o.checked).Count;NegativeCheckedFiles=@($n.checked).Count} | ConvertTo-Json -Compress
```

4. R2 manifest inventory and dependency nesting — exit 0:

```powershell
$m=Get-Content -Raw acceptance/20261114-dynamic/targeted/t01-denominator/revisions/R0002/manifest.json | ConvertFrom-Json; [pscustomobject]@{R2Files=@($m.files.path);DependencyFileCount=@($m.files | Where-Object path -Match '/dependencies/').Count;ManifestComplete=$m.status;Parent=$m.parent_revision_id;ParentHashPresent=[bool]$m.parent_manifest_sha256} | ConvertTo-Json -Depth 5
```

5. R2 manifest self-hash check — exit 0:

```powershell
$m=Get-Content -Raw acceptance/20261114-dynamic/targeted/t01-denominator/revisions/R0002/manifest.json | ConvertFrom-Json; $entry=@($m.files | Where-Object path -eq 'revisions/R0002/manifest.json')[0]; $actual=(Get-FileHash -Algorithm SHA256 -LiteralPath acceptance/20261114-dynamic/targeted/t01-denominator/revisions/R0002/manifest.json).Hash.ToLower(); [pscustomobject]@{SelfEntryPresent=([bool]$entry);ExpectedSelfHash=$entry.sha256;ActualManifestHash=$actual;SelfHashMatches=($entry.sha256 -eq $actual);R2Status=$m.status} | ConvertTo-Json -Compress
```

## Limits and next action

Only the requested targeted artifacts and the canonical resume skill were inspected. No full E2E or H02 harness rerun was performed; the recorded identity failure and current hardcoded boundary check make that rerun non-evidentiary until corrected. Current read-only review is complete, but acceptance remains blocked by F1-F5. Next action: correct the T01 operative denominator fixture and manifest construction, repair H02 identity/receipt handling, then add checker cases for parent hashes, forks, exact active-claim selection, and path containment before recording new targeted receipts.
