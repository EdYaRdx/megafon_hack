# Reusable case-template use check

**Date:** 2026-11-13  
**Fresh OMP task contexts:** initial smoke 45.3s; post-correction smoke 49.7s.  
**Model/provider, tokens, billing:** `UNKNOWN`; task durations are not human-active time.

## Scope and result

Two read-only task contexts applied `cases/_template/` to the same prompt-supplied fictional revision: 8/10 versus 2/12, 9/12, 1/12 across distinct synthetic cohorts, plus one attempted read of an absent local summary. Neither test modified the template or a case. The first smoke found three guidance gaps: no activity-event field guidance, no explicit `supersedes` shape in the claim example, and no rule for prompt-only material. The template/claim reference was then updated.

A fresh post-correction context confirmed the gaps are closed at the **guidance** level: event records include attempt/result, tool, errors/retries, `external_actions`, and available telemetry; successor links accept a scalar ID or array; prompt-only material cannot be given a fabricated path or presented as independently checked. The proposed transition keeps the synthetic reports separate, treats broad real-audience preference as `UNKNOWN`, retains the human gate, and records the exact missing-file error once.

## Limits

This is an answer-only template-use check, not a saved case, state-write E2E, or IDE acceptance. The actual prior claim ID, current state/decision and revision snapshots were intentionally outside the read set, so the tests cannot establish case-specific successor IDs or snapshot content. A case author must inspect those artifacts before revising. The first independent reviewer confirmed the template and smoke, but a follow-up review found that the resume skill mentioned source acquisition without explicitly including reads. The skill, template, claim guidance, and retention resume note were aligned to record every source acquisition/read result plus case-file edit/write failures and retries; an independent follow-up reviewer confirmed the correction. No fabricated journal entries were added.