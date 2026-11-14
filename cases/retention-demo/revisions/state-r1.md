# Case state

- Updated at: 2026-11-13 (Moscow date; exact local time not captured)
- Revision: 1
- Current stage: `DECISION_DRAFT`
- Decision status: `HUMAN_REVIEW_REQUIRED`
- Completed: synthetic intake; opened two public methodology pages; recalculated the cohort fixture; recorded claims, limitations, options, draft product/communication strategies, and a gated validation plan.
- Evidence/claim IDs added: `S-001..S-003`, `E-001..E-007`, `C-001..C-007`.
- Open questions: real metric/event definition; real cohort source and completeness; acquisition/release/instrumentation changes; audience and owner; unit economics; meaningful decision threshold; authorized test conditions.
- Blockers and limitations: all operational data are fictional; no causal product mechanism is identified; no real company data or partner brief was accessed; recommendation is not approved for implementation or publication.
- Next exact action: for a real case, obtain the decision owner's metric/event contract and source cohort export with channel, cohort age, interval completeness, and provenance; independently recompute before replacing any synthetic claim.
- Human decision needed: yes, before real data ingestion, direction selection, product intervention, experiment, or outward-facing communication.
- Cost/time/call telemetry: no paid model/API request was made; public-source lookup occurred but external metering is `UNKNOWN`; authoring time is `UNKNOWN`.

## Resume note

The next session must re-read the brief and this state, then verify whether new input is real or synthetic. Do not carry the synthetic 62%/38% values into a real decision. If an event definition or source period changes, add new evidence/claim records with new IDs; link each successor to replaced claims using `supersedes`, and update the current state/decision to identify active successor IDs. Snapshot the prior decision/state before editing and append an `activity.jsonl` event for every source-acquisition/read attempt and its result, plus case-file write/edit failures and retries. Do not rewrite this revision's history.
