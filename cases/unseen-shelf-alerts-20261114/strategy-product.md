# Product strategy — R2 recommendation pending human approval

## Audience and job

**Hypothesis, not validated audience:** staff at independent bookstores may need to notice likely low stock and decide whether/how to replenish a title. Frequency, severity, current workflow, eligibility, buyer/user authority, and demand are `UNKNOWN` (brief.md:23–35; C-006). The six fictional active dashboard-user stores are a selected pilot sample, not representative users (S-003, `input/pilot-protocol.md:5–11`; E-002).

## Problem evidence and alternatives

Only a synthetic concept note establishes what the prototype is supposed to do: manual stock entry and a low-stock row (S-001, `input/concept-note.md:7–9`; E-001/C-001). The fixture has 18 alert records, 13 opens and six recorded orders within seven days (S-002, `input/pilot-alerts.csv:1–7`; E-003/C-002), but no randomization, comparator, stockout/lost-sales outcomes, or eligible-SKU denominator (S-003, `input/pilot-protocol.md:5–11`; E-002). The observed records cannot establish alert-caused orders or reduced stockouts (C-004). Staff's existing process and alternatives are `UNKNOWN`.

## Proposed product direction

**Provisional recommendation only:** retain the existing manual, read-only low-stock display as the scope boundary while a human owner considers authorizing bounded discovery and a usability/feasibility evaluation. Do not commit to automatic ordering or claim reduced stockouts. Any later change must show that a defined user task exists, the signal is trustworthy/actionable, and the owner approves a safe path. This is a proposed next step, not a selected sprint scope.

## Explicitly out of scope

No supplier integration, order submission, automated inventory updates, availability guarantees, customer/staff contact, data collection, live test, purchase, external release, or promotion is authorized. The R2 synthetic scenario constraint requires explicit human review and confirmation for every individual supplier order before submission; it does not authorize any order or establish demand (S-007, `input/revision-2-research-note.md:3–7`; E-007/C-010). Do not state “40% fewer stockouts” (S-004/E-004/C-003).

## Value, cost and revenue assumptions

Potential value—earlier awareness of a low-stock condition—is a hypothesis, not measured benefit. Lost sales, margin, willingness to use/pay, revenue, cost, effort, and delivery capacity are all `UNKNOWN`. No estimate or numeric target is inferred from the pilot.

## Evidence, hypotheses and unknowns

- `DOCUMENTED`: prototype boundary (C-001).
- `OBSERVED`: synthetic record totals/rates only (C-002); the 72.22% open ratio is 13 opened / 18 generated alert **records**, not stores/users.
- `CLAIMED`: 40% fewer stockouts (C-003), unsupported; vendor's 14/18 opens conflict with the CSV's 13/18 (C-009).
- `UNKNOWN`: prevalence/value of the problem, alert accuracy, causal effect, supplier feasibility, cost, user intent/consent, and suitable stockout definition (C-004/C-006).
- `DOCUMENTED`: GOV.UK advises discovery research about users, current tasks, problems and needs (C-007; S-005/E-005); this is methodology, not market evidence.

## Risks and strongest counterargument

Potential wrong/late/misleading alerts could cause wasted staff time or inappropriate replenishment; operational risk is unmeasured. A discovery step could delay an opportunity and small qualitative usability work would not prove stockout impact. The current synthetic selected pilot is not enough to settle either side. Human approval is required before consequential work.
