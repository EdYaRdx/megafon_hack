# Anonymized F1 response 43

**Clarification before recommendation:** “Retention fell” does not specify the decision to make. The supplied clarification makes the immediate decision whether to spend next sprint on an onboarding redesign; tracking changes and causes of the acquisition-mix shift remain unknown.

## What the data show

The synthetic metric defines D30 retention as the share of eligible cohort members with at least one active day on days 24–30. The four channel-specific rows are mature D30 cohorts; `latest,all` is D7 and is not comparable.

|Cohort|Direct|Partner|All channels|
|---|---:|---:|---:|
|Old|80/100 = 80%|60/100 = 60%|140/200 = 70%|
|New|44/50 = 88%|93/150 = 62%|137/200 = 68.5%|

The aggregate is down 1.5 percentage points, while both observed channel rates are higher. The channel mix also changed: direct went from 100/200 (50%) to 50/200 (25%). This is consistent with a mix explanation for the aggregate decline, but does **not** establish why the mix changed or prove that onboarding did or did not affect retention. Tracking history, within-channel experience, causes, and a decision threshold are unknown.

## Options

1. **Commit next sprint to a full onboarding redesign — not recommended on current evidence.** Potentially addresses friction if onboarding is the cause, but no supplied evidence identifies an onboarding problem. Strong objection: the apparent aggregate decline may reflect composition or measurement, and the redesign could spend a sprint on the wrong cause. Reconsider if measurement is validated and evidence identifies a remediable onboarding issue.
2. **First diagnose measurement and acquisition mix — recommended next step.** Preserve the current experience while checking metric/event definitions and tracking changes, then investigate the channel-mix shift and compare mature cohorts within channel. This is the most decision-relevant response to the observed aggregate/channel difference. Cost, timing, and likely findings are unknown; the diagnosis may not identify a cause.
3. **After data validation, run a narrower reversible onboarding test.** Could test a specific, evidenced onboarding friction with less commitment than a full redesign. At present, no friction, test change, or expected benefit is established; do not treat this as authorization to launch or contact users.
4. **Maintain status quo without diagnosis, or stop retention work.** Avoids sprint investment, but leaves the metric and mix questions unresolved. Stopping is reasonable only if the human decision owner concludes retention is no longer a priority; no such rationale is supplied.

## Linked product and communication strategy

For now, the product choice is **not to promise an onboarding fix**: the supplied evidence does not show that onboarding caused the change. The immediate audience is the product decision-maker deciding next sprint’s allocation. Message: “The aggregate D30 rate is slightly lower, but the observed channel rates are higher and the channel mix changed; cause and tracking history are unknown.” Its basis is the metric contract and cohort counts above; it should not be reframed as proof that mix caused the decline. Use this in the internal sprint decision, with the next step being a measurement/mix review. No external or user-facing claim is supported.

If a later test is justified, first identify the specific audience, friction, proposed product change, and evidence for each. Any message about that change should describe only what it actually offers and under what conditions.

## Validation and next state

**Question:** Is the aggregate D30 movement explained by a measurement change, acquisition composition, or a within-channel change that points to an onboarding problem?

**Next check:** Review instrumentation/version history and metric implementation; verify eligibility, numerators, denominators, windows, and channel definitions for both mature periods; then compare like-for-like channel cohorts and investigate mix changes. Current counts are small in some cells (50 eligible direct in the new cohort), and no uncertainty estimates are supplied, so avoid treating these point estimates as conclusive.

If a specific onboarding issue is then supported, design a human-approved, reversible comparison against the current experience among the relevant eligible audience. Define the primary outcome as mature D30 retained / eligible members, with the same days 24–30 definition and channel-stratified reporting; use only complete mature cohorts and document exclusions. Set the minimum worthwhile effect, sample/period, and decision threshold **before** testing, based on decision-owner judgment; these values cannot be derived from the packet. Guardrails should include instrumentation integrity and relevant harms, which must be specified before any test. If the effect does not meet the pre-set threshold or guardrails fail, do not scale; if it does, return to the human owner for a decision. No test or external action is authorized now.

**Next state (2026-11-14):** Recommendation is to defer the full redesign commitment and first diagnose measurement and mix. Decision owner: product lead (not identified by name). Status: recommendation for human decision, not approval. Revisit when the measurement/mix review is complete or new onboarding evidence becomes available; change course if validated evidence identifies a material onboarding-specific opportunity.