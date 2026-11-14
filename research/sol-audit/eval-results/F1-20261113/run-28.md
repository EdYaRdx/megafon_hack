# Anonymized F1 response 28

**Clarification applied before recommendation:** “We are deciding whether to spend next sprint on an onboarding redesign. Tracking changes and causes of the acquisition-mix shift are unknown.”

## Decision for 2026-11-14

**Do not commit next sprint to a broad onboarding redesign on this evidence.** First verify the D30 tracking and acquisition mix; if those checks support a product problem, use a narrower, reversible test rather than treating the aggregate decline as proof that onboarding caused it.

No implementation or user contact is authorized. Any action below is a recommendation, not something that has occurred.

## What the supplied data says

**Facts** — the four D30 rows are mature for this exercise, and D30 means at least one active day during days 24–30 after signup. The latest,all row is D7 and is not comparable to D30.

|Cohort / locator in `cohorts.csv`|Calculation|D30 retention|
|---|---:|---:|
|old, direct (row 2)|80 / 100|80%|
|old, partner (row 3)|60 / 100|60%|
|old, overall (rows 2–3)|(80 + 60) / (100 + 100)|70%|
|new, direct (row 4)|44 / 50|88%|
|new, partner (row 5)|93 / 150|62%|
|new, overall (rows 4–5)|(44 + 93) / (50 + 150)|68.5%|
|latest,all (row 6)|35 / 100|35% at D7; not comparable|

The observed mature-cohort overall change is **−1.5 percentage points** (68.5% − 70%). But the channel mix changed: direct is 50% of the old cohort and 25% of the new one. Within the supplied channel rows, direct is **+8 pp** and partner **+2 pp**. Applying the new within-channel rates to the old 50/50 mix gives 75%; applying the old rates to the new 25/75 mix gives 65%. This illustrates how mix can move the aggregate independently of within-channel rates; it does **not** establish why mix changed or what caused retention outcomes.

**Unknowns:** tracking or instrumentation changes, the cause of the mix shift, within-channel user experience, acquisition cost, user harm, release history, interview evidence, and a decision threshold. The supplied data does not establish a causal onboarding problem or whether the observed differences are meaningful for a decision.

## Options and trade-offs

1. **Commit next sprint to a broad onboarding redesign.**
   *Objection:* the aggregate difference is small, channel-level rates are higher in the new cohort, and neither tracking comparability nor causality is established. A redesign could spend the sprint on the wrong problem.

2. **Diagnose measurement and mix first — recommended.**
   Reconcile the D30 event definition and instrumentation/version history across cohorts; investigate the acquisition-mix change and compare like with like.
   *Objection:* diagnosis may delay a product change, and it may not identify a fix within one sprint.

3. **After those checks, run a narrow, reversible onboarding test.**
   Test one specified change against the existing experience, with a concurrent comparator and pre-set success and guardrail criteria.
   *Objection:* a narrow test may not answer whether a broader redesign would work; D30 results require waiting for enrolled users to mature.

4. **Maintain the current experience or stop the redesign direction.**
   This avoids spending on an unsupported intervention; stopping is reasonable if the diagnostic work finds no credible, actionable onboarding issue.
   *Objection:* it leaves any real onboarding problem unresolved and does not itself explain the aggregate movement.

## Product and communication approach

For the next sprint, prioritize measurement and mix diagnosis over a broad redesign. Do not present the aggregate decline as evidence that onboarding caused it. If a specific, actionable issue emerges, define the smallest testable product change and keep it reversible.

For internal communication, report the row-level rates, cohort definitions, mix shift, and unknowns together. Clearly label the D7 result as non-comparable to D30. Do not describe a diagnosis, redesign, test, or user communication as completed.

## Validation plan if a test is proposed

- **Comparator:** concurrent randomized control receiving the current experience, versus the specified onboarding change. Confirm measurement comparability before interpreting results.
- **Primary metric and denominator:** D30 retention as defined in `metric.md`: unique eligible cohort members with at least one active day on days 24–30 after signup, divided by all eligible members in the assigned group. Report each group’s numerator, denominator, and rate; show channel composition and results by channel as well as overall.
- **Timing:** enroll during the test, then evaluate only after each included cohort has completed days 24–30 and the data is available. Do not substitute D7 for a D30 readout.
- **Guardrails:** verify event instrumentation and eligibility are consistent between groups; monitor channel composition and any defined user-harm indicators. The packet supplies no guardrail thresholds, so set them before launch rather than infer them from these data.
- **Decision rule:** set a minimum worthwhile D30 improvement and guardrail limits before the test. Continue or expand only if the pre-set criteria are met; otherwise retain the current experience or revisit the diagnosis. No threshold can be derived from the supplied inputs.