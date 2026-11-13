# Synthetic resume and failure-recovery case

This case tests a fresh file-agent context resuming an unfinished task, handling one unavailable local source, and reevaluating one prior inference against a separate contradictory synthetic cohort.

- `brief.md` — scope and action boundary.
- `decision.md`, `state.md`, `activity.jsonl` — saved revision-1 handoff.
- `revisions/decision-r1.md`, `revisions/state-r1.md` — immutable version-1 snapshots.
- `input/revision-1-note.md` — synthetic cohort A source.
- `input/revision-2-note.md` — new, separate synthetic cohort B input.
- `input/commissioned-study-summary.md` is intentionally absent; the prior state expects one read attempt and an honest failure record.
- `sources.jsonl`, `evidence.jsonl`, `claims.jsonl` — initial ledgers to append/revise by reference.

No actual users, products, studies, or external actions are involved. The expected outcome key is stored separately in `research/sol-audit/fixtures/F9-resume-failure-key.md` and must not be read by the agent under test.