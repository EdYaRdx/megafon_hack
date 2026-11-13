# Validation plan

This is a gated plan, not authorization to start research, contact patrons, spend, build, or communicate externally. The synthetic input prohibits those actions in this exercise (S-001, `input.md` / “Fixed follow-up answer”; E-002; C-002).

## Gate 0 — owner and scope (before any work)

- Learning/decision question: who can decide whether a six-week discovery/prototype is authorized, and what decision must that work resolve?
- Method/comparator: internal identification of the actual accountable owner and written scope/permissions; no user research or prototype. Comparator: current state is uncharacterized (`UNKNOWN`).
- Audience/sample: real decision owner, currently unidentified; sample `UNKNOWN`.
- Metric: authorization completeness = required scope fields explicitly confirmed / required scope fields. Required fields: owner, permitted activities, resources/cost, decision question, deadline, decision criteria, review gates. Denominator is seven listed fields; owner must confirm whether additional fields are required. This is a checklist-completion metric, not evidence of user demand.
- Window and threshold: `UNKNOWN`; owner must set before this gate begins. Do not proceed unless every required field is explicitly resolved and the owner authorizes next stage. No numerical outcome threshold is invented.
- Guardrails/action: if owner or permission absent, stop with no work. If complete, owner must separately approve each permitted next-stage activity.

## Gate 1 — problem and alternatives (only after explicit human approval)

- Learning question: is there a sufficiently evidenced patron problem related to due dates, and how does the current experience compare to candidate alternatives?
- Hypothesis/falsifier: some defined patron cohort experiences a problem that merits intervention; falsified for the scoped decision if permitted, credible evidence does not support a material problem under an owner-approved criterion. “Material” threshold is `UNKNOWN` and must be set by owner before collection.
- Method/comparator: first inspect existing, authorized aggregate usage/complaint records if available; compare observed baseline with owner-approved comparator/period. Those records are reported absent in synthetic input, so availability/access and method are `UNKNOWN`. Any new patron contact requires separate explicit approval, consent and safeguards; not authorized here. Do not build a prototype in this gate.
- Audience/sample and selection limits: relevant patron cohort and sample/frame `UNKNOWN`; define inclusion/exclusion, representativeness, missingness, duplicate handling, and selection limits before collection. No interviews or survey are currently authorized.
- Primary metric: due-date problem incidence = eligible borrow/loan records with an explicitly defined missed-return event / all eligible borrow/loan records in the defined cohort and observation window. Event definition, cohort, window, data source, baseline, and denominator availability are `UNKNOWN`; data owner must define and validate them before use. Do not compute without authorized data.
- Comparator/window/threshold: `UNKNOWN`; owner and data owner set comparable baseline/comparator, maturation window, and decision threshold before access or collection.
- Guardrails: data minimization and authorized access; missingness, duplicates, cohort maturity, alternative explanations, and any adverse patron effects must be assessed. Applicable privacy/consent review and permitted handling are `UNKNOWN`, not presumed satisfied.
- Owner/action: real decision owner `UNKNOWN`. No action until identified and explicit approvals recorded. If evidence supports a problem under pre-set criteria, owner may consider a distinct, separately approved feasibility stage. If it does not, stop/revisit status quo. If inconclusive or data quality fails, do not infer demand; owner decides whether to revise question or stop.

## Gate 2 — feasibility/solution comparison (only if separately approved)

- Learning question: can a candidate reminder approach be delivered safely and feasibly, and does it improve a meaningful outcome over status quo or an appropriate alternative?
- Hypothesis/falsifier: a specified candidate improves an owner-selected outcome without unacceptable guardrail harm; falsifier is no improvement or guardrail breach under pre-specified criteria. Neither candidate nor criterion is established.
- Method/comparator: compare SMS only if capability, cost, required reviews, and explicit human approvals are established; otherwise compare other authorized alternatives or stop. A prototype/build is expressly unauthorized in this exercise.
- Audience/sample, metric/formula/denominator, period, baseline, threshold, and data source: all `UNKNOWN`, to be determined and approved by owner and relevant data/operational owners before any experiment. Do not substitute message delivery/open rates for a user outcome without justification.
- Guardrails: define unwanted effects and applicable privacy/consent safeguards before any real-user test. No patron contact or external communication absent separate approval.
- Action: positive result permits only the next human decision, not launch; negative result stop/reconsider; inconclusive or unsafe result pause, investigate data/guardrail failure only if approved, otherwise stop. All paths require owner decision.
