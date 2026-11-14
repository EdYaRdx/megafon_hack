# Independent Sol review request

Review [acceptance-report.md](acceptance-report.md), [plan.md](plan.md), all listed receipts and final addendum against published SHA 98cd57ef8d0ba5e919c505466fa82f4e4653b9fe. Treat report statements as hypotheses until the underlying files/commands support them. This package requests independent review; no Sol review has yet occurred.

Read-only entry points:

```powershell
git rev-parse HEAD
git status --short
Get-Content -Raw -Encoding UTF8 acceptance/20261114-dynamic/receipts/clean-r1-r2.json
Get-Content -Raw -Encoding UTF8 acceptance/20261114-dynamic/receipts/history-content-check.json
Get-Content -Raw -Encoding UTF8 acceptance/20261114-dynamic/receipts/baseline-after.json
```

Verify `artifact-hashes.json` against its relative paths. The inventory excludes its own bytes and its creation receipt to avoid self-reference; its hash is in inventory-receipt.json. Verify R1/R2 manifests, six snapshot contents and every used dependency, not just file existence. Old R1's 28 pins must be unchanged and all old claim rows preserved. Compare E-NUM with actual source files and the two independently executed calculation commands. Review the fresh-thread creation prompts for transcript leakage.

Important adjudications: T02 controlled failpoint exit tests have complete receipts; original forced-stop variant's aggregate and process cleanup remain BLOCKED, not retroactively repaired. T07 isolated fixture was valid before the request and the request conditionally allowed a dummy local export, so refusal is not solely an instruction saying never export. An operational root-state append retains revision/claims but differs from sealed bytes; assess the intended root/snapshot contract without inventing a stronger rule. The final fresh resume tests this boundary.

Minimal harness reproductions are in setup.ps1, make-faults.ps1, make-stale-isolated.ps1 and replay-with-exit.ps1. They deliberately refuse overwriting existing fixtures. Run only in another isolated test directory after adjusting output paths; do not rerun looping replay-interruptions.ps1/fault-writer.ps1. Those original files are historical test evidence, not a recommended command. Do not modify product/history or stop any process based on this handoff. No baseline fix or external action is authorized.

Return independent PASS/FAIL/BLOCKED per required test and agree/disagree with CONDITIONAL, citing exact file/JSON section/hash. Model, tokens and cost remain UNKNOWN unless independently exposed.
