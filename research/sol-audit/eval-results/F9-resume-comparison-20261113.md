# F9 resume/revision comparison — exploratory, single response per arm

**Date:** 2026-11-13. Frozen plan: `F9-resume-comparison-plan-20261113.md`. Sealed key: `research/sol-audit/fixtures/F9-resume-failure-key.md` (not provided to B0/B1). Candidate packet: `F9-resume-comparison-packet-20261113.md`.

## Runs and scores

| Arm | Output mode | Reviewer 1 | Reviewer 2 | Direct artifact score | Task duration |
|---|---|---:|---:|---:|---:|
| B0 ordinary chat | Proposed R2 response; no files written | 7/10 | 8/10 | — | 24.6 s |
| B1 structured prompt | Proposed R2 response; no files written | 10/10 | 9/10 | — | 39.0 s |
| A file-based agent | Saved R2 artifacts | 9/10* | 8/10* | 10/10 | 2m01s |

*Initial de-identified packet reviewers scored the abbreviated A artifact summary, which omitted the precise source locator and snapshot trace; those scores are not the final A result. A separate direct artifact review examined decision/state/claim/source/evidence/activity files and the task trace, verified exact R2 locators and no R1 snapshot writes, and scored A 10/10 across all five dimensions. This corrects the packet-evidence omission; it is not a third blinded comparison.

Reviewer score vectors (resume-only; lookup/source trail; claims/cohorts; history/state/next step; human gate): B0 `1,1,2,1,2` and `2,1,2,1,2`; B1 `2,2,2,2,2` and `2,1,2,2,2`; A direct `2,2,2,2,2`. B1 reviewers differed on whether its paragraph locator without the explicit input path was complete.

An independent audit found an incorrect transcription of Alpha's B0 vector in this report; it was corrected to `1,1,2,1,2`. A separate follow-up reviewer confirmed the corrected B0 vectors sum to 7/10 and 8/10 and found no remaining arithmetic or arm-mapping error.

## Trace and notable observation

B0 and B1 used separate fresh OMP contexts. Their tool histories show only the allowed R1 snapshots, notes, initial R1 ledger rows, and one read attempt of the absent summary; neither shows a read of current R2 files, key, skills, or root instructions, nor any writes. B1 independently produced claim IDs C-003/C-004/C-005 and S-003/E-002 matching the saved A IDs despite no logged read of the R2 ledger. This exact match is unexplained; the trace has no direct forbidden read, so it is not proof of leakage, but identifier independence cannot be established.

## Interpretation and limits

B1's response scored 9–10/10, B0 7–8/10, and the final saved A artifact set 10/10 on this five-point resume rubric. The result shows B1 can produce a strong proposed decision; only A's run actually saved state, source/evidence/claim records, event history, and a revised decision. B0/B1 persistence is untested. The response forms and evidence exposure differ, and A ran before the baselines; candidates were anonymized but not guaranteed blind because artifact form may reveal the condition. B0/B1 did not have isolated clean work folders; loader isolation was not independently verifiable. Model/provider/version equivalence, tokens, cost, and human-active time are `UNKNOWN`. Durations above are task runtime only. One response per condition, non-randomized, non-concurrent with A. Exploratory only; no causal, statistical, or superiority claim.