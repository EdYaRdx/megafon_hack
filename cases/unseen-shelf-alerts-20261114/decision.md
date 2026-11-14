# Decision record — R2 pause

- Status: `RECOMMENDATION_PENDING_HUMAN`; no decision made or action authorized.
- Decision owner: `UNKNOWN` (brief says no specific owner is identified).
- Date: 2026-11-14.
- Revision: R2.
- Decision requested: choose an appropriate reversible next step for the next sprint; actual sprint plan/date `UNKNOWN`.
- Provisional recommendation: Option B, bounded read-only discovery/test planning, only after human approval. This is not an owner decision.
- Current evidence IDs: E-001–E-007.
- Current claim IDs (successor IDs only): C-001–C-004, C-006–C-010. Superseded: C-005 → C-009.
- Options considered: A `STATUS QUO` keep the existing read-only prototype unchanged; B bounded discovery/usability and feasibility work; C supplier-order workflow subject to mandatory per-order human confirmation before submission; D stop/close replenishment work. Full trade-offs and strongest objections: `options.md`.
- Basis: prototype is manually entered and read-only (S-001, `input/concept-note.md:7–9`; E-001/C-001). In the synthetic six-store, 18-alert, two-week pilot, 13/18 alert records opened and six orders were recorded within seven days (S-002, `input/pilot-alerts.csv:1–7`; S-003, `input/pilot-protocol.md:5–11`; E-002/E-003/C-002); alert opens/orders do not establish causal stockout reduction (C-004). Vendor export claims 40% fewer stockouts without evidence and reports 14/18 opens, contradicting the CSV’s 13/18 (S-004, `input/vendor-export.html:6–8`; E-004; C-003/C-009). Therefore refuse the 40% claim as unsupported. GOV.UK discovery advice is methodological, not demand evidence (S-005 URL, “User research in discovery”; E-005/C-007). New R2 scenario constraint requires explicit human review and confirmation of each individual order before submission; it disallows autonomous submission but establishes neither demand nor approval (S-007, `input/revision-2-research-note.md:3–7`; E-007/C-010).
- Rejected/not selected for recommendation: A leaves need and usefulness unexamined; C lacks demand/impact evidence, supplier integration, estimate, consent, or order authority, and any future supplier-order submission must require per-order human confirmation (C-010); D risks ending a direction before need is assessed. These are not owner decisions.
- Assumptions accepted by the owner: none.
- Conditions to proceed/change: owner identified and approves next step; agree operational stockout definition, eligible store/SKU frame, comparator, data access, baseline/decision threshold, safeguards and permissions before test. All currently `UNKNOWN`.
- Review date/trigger: `UNKNOWN`; revisit at the next human decision on scope/authorization.
- External actions: none authorized; no contact, collection, purchases, supplier integration, build, launch, or publication.
