# Options and trade-offs — R2

Evidence basis: E-001–E-007; cited current claims C-001–C-004, C-006–C-010. All materials are synthetic. Costs, demand, base rates, owner, and delivery dates are `UNKNOWN`.

## A — `STATUS QUO`: keep the current read-only prototype unchanged

- **Audience/value:** The six fictional prototype stores retain manual on-hand entry and the low-stock row; no additional value beyond the existing display is evidenced (S-001, `input/concept-note.md:7–9`).
- **Change/cost:** No scope change; marginal cost and opportunity cost `UNKNOWN`.
- **Strongest objection:** Does not establish whether the signal is accurate or useful and does not address actual replenishment; user need is unverified (C-006).
- **Falsifier/revisit:** Evidence that a defined user task is unmet by the display and that a safe, measurable change is feasible.

## B — bounded read-only discovery and usability/feasibility validation (provisional recommendation)

- **Audience/value:** First learn about intended bookstore staff and their current stock-check/replenishment work; then, only if approved, test whether a low-stock display supports that task without ordering. GOV.UK discovery guidance supports learning users, current process, problems and needs, not product demand (S-005/E-005, methodology only).
- **Change/cost:** Next step is a human-gated discovery/test plan; no implementation, contact, data collection, supplier integration, or release authorized. Cost, schedule and capacity `UNKNOWN`.
- **Evidence/assumptions:** Current prototype is read-only (C-001). The fictional pilot contains 13/18 opened alert records and six recorded orders, but no causal stockout evidence (C-002/C-004). Assumes only that answering need/feasibility questions is useful; this itself requires owner approval.
- **Strongest objection:** A small usability exercise may be slow, selected, and fail to show commercial impact; current pilot may be enough to justify a focused build only if an owner already has independent evidence (none supplied).
- **Falsifier/revisit:** Revisit if approved discovery finds no important task, the signal is not actionable/trustworthy, or authorized data show no plausible relationship to the defined stockout outcome.

## C — supplier-order workflow (autonomous submission disallowed; human confirmation required)

- **Audience/value:** Could reduce manual reordering only if users want it and accurate availability, supplier integration, consent, and order authority exist; none is established (C-001/C-006). R2's synthetic constraint requires explicit human review and confirmation of every individual order before submission, even when urgent (S-007, `input/revision-2-research-note.md:3–7`; E-007/C-010).
- **Change/cost:** Any future workflow involving order submission cannot submit automatically; each order must wait for explicit human confirmation. A read-only display remains the current prototype boundary. Feasibility, cost, timeline, supplier coverage, and authority are `UNKNOWN`; the note authorizes no order, integration, build, or launch.
- **Evidence/assumptions:** Only a contributor proposal exists (S-001); no implementation estimate or impact evidence. The “40% fewer stockouts” claim is unsupported (C-003). Human review is a required workflow constraint, not evidence of demand or approval (C-010).
- **Strongest objection:** High-consequence mistaken orders/inventory errors and an unproven user need; the requested 40% benefit cannot be substantiated. Human confirmation may constrain speed, including for urgent alerts; this has not been tested.
- **Falsifier/revisit:** Do not scope unless an authorized owner establishes user need, supplier/technical feasibility, safeguards, permissions, and a credible controlled outcome evaluation; any submission path must preserve per-order confirmation.

## D — stop/close the replenishment direction

- **Audience/value:** Avoids continued effort if the need is absent, unsafe, or infeasible; benefit and avoided cost `UNKNOWN`.
- **Change/cost:** Stop further direction work; sunk/current effort and opportunity cost `UNKNOWN`.
- **Evidence/assumptions:** Current evidence is insufficient for an impact claim, but insufficiency does not prove lack of value (C-004/C-006).
- **Strongest objection:** Could abandon a real, consequential unmet need before adequate discovery.
- **Falsifier/revisit:** Reopen only if a decision owner authorizes evidence gathering that demonstrates a defined need and feasible, safe path.

## Trade-off

B is the least-commitment learning path, not a finding that demand exists or an authorization to contact anyone. A is the true no-change alternative; C is not supported for next-sprint commitment; D remains available if discovery or feasibility fails. A human owner must choose before any consequential work.
