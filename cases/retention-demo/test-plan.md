# Validation plan — gated

This is a design draft, not an authorized experiment. No real users or company data were contacted or processed.

## Stage 1: measurement and cohort diagnostic

- **Question:** does the apparent aggregate decline remain after applying one documented event definition and comparing only mature, fixed-window cohorts with channel mix shown?
- **Method / comparison:** independently recompute aggregate and segment rates from a versioned export; compare like-for-like periods, report observed aggregate and channel-standardized values; inspect event lineage and completeness.
- **Population:** eligible new users for the agreed product and date window; real inclusion/exclusion rules are `UNKNOWN`.
- **Primary output:** mature D30 `Return On or After` rate = unique eligible users triggering the agreed return event on or after day 30 / eligible users whose cohort reached day 30. The event and units must be approved first.
- **Period:** at least two fully mature, comparable cohort windows; exact dates depend on the real metric contract.
- **Decision threshold:** `UNKNOWN` until the owner defines a material change and confirms economic relevance. No causal action should follow from this diagnostic alone.
- **Guardrails:** missingness, duplicate users, join rate, event-definition/version changes, cohort maturity, channel attribution, complaints/cancellations if supplied.
- **Action:** if measurement is unreliable, repair the data contract and rerun; if a within-segment decline remains, conduct user/problem discovery before choosing a mechanism; if the drop disappears after mix/maturity correction, do not launch a feature solely on the aggregate trend.

## Stage 2: optional controlled intervention (requires new evidence and approval)

- **Question / hypothesis:** only after discovery names a specific friction, does a corresponding reversible change improve mature D30 retention for the affected segment versus current experience?
- **Comparison:** randomized treatment and concurrent control if feasible; otherwise record the strongest valid comparison and its limitations.
- **Population / sample:** eligible users in the affected stable segment. Sample size, power, enrollment window, allocation, and minimum detectable effect are `UNKNOWN` until baseline counts and the owner threshold are available.
- **Primary metric:** pre-agreed mature D30 rate with fixed event definition and denominator.
- **Period:** enroll for a predeclared window and wait through the complete D30 maturity interval; no early stopping on an unplanned favorable result.
- **Decision threshold:** owner sets a minimum meaningful effect after costs/economics are known; do not invent it from this fixture.
- **Guardrails:** crash/error rate, cancellations, complaints/support contacts, data quality, and segment-specific harm. Owners set stop tolerances before launch.
- **Approvals required:** product owner, experiment/data owner, and privacy/security review as applicable. No automatic launch or spend.
