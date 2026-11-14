# F9 — fresh-context resume with contradictory input and failed lookup

**Date:** 2026-11-13  
**Run:** `ResumeFailureFreshContext`; OMP fresh task context, 2m01s elapsed according to task record. This is not an IDE/new-chat acceptance test.  
**Model/provider, token count, and cost:** `UNKNOWN`. Elapsed task time is not human time.

## Scenario and observed result

Synthetic case `cases/resume-failure-demo/` starts at decision/state revision 1 with a fictional cohort-A note and an unresolved local source path. The fresh context read the saved state and prior snapshots, attempted `cases/resume-failure-demo/input/commissioned-study-summary.md` once, and received `Path ... not found`. It did not retry or invent contents. The new fictional cohort-B note conflicts in direction with cohort A; the run kept the cohorts separate, recorded S-003/E-002 and C-004, retained C-001 as cohort-A-only, and concluded the broad preference claim is not established. It revised the posture to status quo plus bounded internal preparation pending human review; no external action occurred.

Revision-1 decision/state snapshots remain present. Revision 2 records the failed lookup, added evidence and claims, human gate, and next action. The run transcript shows one stale-anchor edit failure followed by a fresh read and successful correction; the original activity record did not mention that edit error.

## Independent review and corrections

Two independent first-pass reviewers found P2 issues:

- **Claim status:** C-003 linked `supersedes: C-002`, but old C-002 remained `INFERENCE` with `invalidated_by: []`, leaving current status ambiguous to a raw-ledger consumer.
- **Activity fidelity:** the event described the missing-file read accurately but said “No other errors observed,” omitting the stale-anchor edit failure and successful retry visible in the task trace.

Correction preserved C-002 as an immutable historical record and appended C-005 with status `UNKNOWN`, explicitly superseding C-002 as the current decision-facing claim. Decision and state now identify C-005. The activity record now includes both the one failed read and the stale-anchor edit failure/retry. A separate reviewer rechecked the revised claims, decision, state, event and transcript; verdict **correct**, no P0/P1/P2. That reviewer notes snapshot preservation is supported by the transcript and event record, not independently proven by a content hash.

## Limits

A single A-workflow diagnostic, synthetic input only. No matched B0/B1 comparison for this resume scenario, live user data, real study, IDE host, or GUI startup. No causal or superiority claim. Human criteria and real-world action remain pending; no pilot was approved.