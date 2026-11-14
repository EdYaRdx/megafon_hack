# F9 resume-rule regression — answer-only transition proposal

**Date:** 2026-11-13  
**Task:** `ResumeLedgerRuleRegression`, fresh OMP task context, 35.0s task duration.  
**Model/provider, token count, billing:** `UNKNOWN`; duration is not human-active time.

## Scope

After the F9 artifact run exposed ambiguous claim supersession and incomplete error history, the canonical `.agents/skills/resume-revise/SKILL.md` now requires a new-ID successor with `supersedes`, an explicit current epistemic status, current `state.md`/decision pointers, and activity records for source failures and case-file edit failures/retries. `references/evidence-and-claims.md` defines these append-only semantics and prohibits backfilling an old row's `invalidated_by`.

A fresh task context was given only R1 snapshots, both synthetic notes, the initial R1 ledger records, the updated procedure, and one reserved missing path. It attempted the path once and returned a proposed R2 transition. The response kept cohorts separate, left C-001 narrow, documented the cohort-B counts, proposed a new `UNKNOWN` successor for the broad generalization, treated C-002 as historical without rewriting it, recorded the exact not-found result, and retained the human gate.

## Limits and review

This was **answer-only**. It did not edit or save any case artifact, and it is not a second state-write E2E, IDE/new-chat test, or B0/B1/A evaluation arm. An independent reviewer found the updated rules consistent with append-only records and the proposed transition accurate against the synthetic inputs, but flagged an ambiguous implementation-status sentence that could conflate this answer-only regression with the earlier artifact-writing F9 run. The status wording was revised to distinguish the saved artifact run from the proposal-only regression; a separate follow-up reviewer confirmed the clarification is accurate and the two reports align with their traces.

No real data, external action, or product decision. No causal or superiority claim.