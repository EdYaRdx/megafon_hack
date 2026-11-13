# Case state — current

- Updated at: 2026-11-13 (Moscow date; exact local time not captured)
- Revision: 2
- Current stage: `DECISION_DRAFT`
- Decision status: `HUMAN_REVIEW_REQUIRED`
- Completed: synthetic intake and public-method review; decision-critical mature-cohort calculation run through an internal JSON-reader jq tool and two fresh OMP task contexts; source rows and arithmetic independently reviewed; claim successor recorded.
- Current source IDs: `S-001..S-003`.
- Current evidence IDs: `E-001..E-008`.
- Current claim IDs (active successors only): `C-002..C-008`.
- Superseded claim IDs → successor IDs: `C-001` → `C-008`.
- Open questions: operational definition of D30 return event and eligibility; real cohort source and completeness; acquisition/release/instrumentation changes; audience and owner; unit economics; meaningful decision threshold; authorized test conditions.
- Blockers and limitations: all input counts are fictional; this is arithmetic over supplied fields only; operational definitions remain `UNKNOWN`; channel mix differs between periods; no causal product mechanism is established; no real company data or partner brief was accessed; recommendation remains unapproved.
- Source/read failures and case-file edit/write failures or retries recorded in `activity.jsonl`: first OMP smoke had two failed nested metrics-reference lookups before finding the project-root reference; a lookup of the absent `revisions/` directory failed before R1 snapshots were created. Case-source reads succeeded; no case-file write/edit failures occurred.
- Next exact action: for a real case, obtain the decision owner's metric/event and eligibility contract plus source cohort export with channel, cohort age, interval completeness, and provenance; verify eligibility definitions and independently recompute before replacing synthetic claims.
- Human decision needed: yes, before real data ingestion, direction selection, product intervention, experiment, or outward-facing communication.
- Cost/time/call telemetry: provider-call, token, billing, and exact elapsed-time details are `UNKNOWN`.

## Revision 2 note

Before this update, exact revision-1 state and decision were preserved in `revisions/state-r1.md` and `revisions/decision-r1.md`. This revision adds `E-008` and active successor `C-008` (supersedes `C-001`); the recommendation remains unchanged and human review is still required. Calculation outputs and limitations are in `../../research/sol-audit/eval-results/retention-calculation-20261113.md`.
