# Metric-validation plan — not approved or ready to run

This is a concrete plan for defining a metric before any validation. It explicitly does **not** choose the meaning of D30, access data, launch a reminder, or authorize outreach/spend. The vendor documentation's alternatives are prompts for questions only. The saved synthetic revision note contains conflicting, explicitly non-authoritative requirement and dashboard-glossary excerpts (CL-05–07); neither is selected and no Mixpanel default controls.

## Gate 0 — metric contract (internal planning only)

1. **Question:** what product event and user outcome is the displayed “D30 retention” intended to represent, and which authoritative internal record governs? The owner must reconcile the conflicting fictional excerpts against that authority; if no authority is established, leave the definition UNKNOWN and do not choose either excerpt or a Mixpanel default. Owner and analytics/data steward must document: unit of analysis; cohort entry/birth event; return event(s); exact-day-30 vs through/after-day-30 criterion or another window; calendar vs rolling basis; numerator; denominator and eligibility; exclusions; event identity/deduplication/missing-event handling; aggregation; and source/version.
2. **Maturity:** document the exact observation window and a rule for excluding incomplete cohorts, based on data latency and the chosen criterion. Then freeze cohort dates and extract date. No rule or maturity is currently chosen.
3. **Comparator:** UNKNOWN. Owner must identify a valid reference period or randomized control and justify comparability before data review. Historical comparison alone cannot establish causality.
4. **Population/sample:** UNKNOWN. Define eligible audience, inclusion/exclusion, sampling/assignment, and minimum cohort requirements before extraction. No real-user contact.
5. **Metric:** candidate form only, not the selected definition: `unique eligible users who satisfy the owner-approved return event/criterion within the owner-approved D30 window / unique eligible cohort users with a fully matured opportunity to satisfy it` (unit: proportion of users; report numerator and denominator separately). Event, window, eligibility, cohort, and maturity are all UNKNOWN and must be filled and approved before use. This is a template, not the case's definition.
6. **Baseline / target / threshold / period:** all UNKNOWN. Owner must set decision-relevant baseline, minimum effect or other threshold, observation duration, and any sample/maturity rule before data access or analysis; do not invent a numeric threshold.
7. **Source and responsible roles:** data source/access authority and analyst UNKNOWN; name data steward and obtain approved access scope before any extraction. This exercise grants no access.

## Gate 1 — only after explicit human approval

- **Question/hypothesis:** does an owner-approved reminder change improve an explicitly named user outcome versus an approved comparator? Refuting outcome: no improvement or worse outcome under the pre-agreed threshold, or failed guardrails. User outcome and reminder capability currently UNKNOWN.
- **Method/comparator:** preferred causal design (e.g. randomized eligible-user control) is not selected; design, assignment unit, contamination controls, and comparator require owner/analytics approval. No experiment is authorized now.
- **Audience/sample:** UNKNOWN; define only from approved eligibility and sample plan. No outreach outside a separately approved product experience.
- **Primary metric:** use the approved formula above only after its blanks are resolved. Report raw numerator/denominator per arm and absolute/relative contrast only if the chosen design and data support it. No values exist.
- **Guardrails:** define before execution for unwanted notification burden/opt-outs, complaints, delivery failures, and any relevant user harm; definitions, data sources, and thresholds all UNKNOWN.
- **Period:** UNKNOWN until window, maturation, latency, and duration are approved.
- **Actions:** if threshold met and all guardrails pass, return to human product owner for a separate decision; do not auto-launch. If threshold missed, guardrail breached, data incomplete, or result inconclusive, do not proceed; investigate only within separately approved scope or stop. No outcome is presumed.
- **Strong alternative explanations/checks:** cohort maturity and completeness, seasonality, audience/channel/product mix, instrumentation changes, missing/duplicate events, concurrent changes, and selection effects must be assessed. Mixpanel's docs mention incomplete periods and cohort/aggregation rules (E-MP-03/E-MP-04), but do not resolve these for this product.
