# Metric checks

Before comparing metrics, freeze the event contract, unit of analysis, numerator, denominator, eligible population, observation window, cohort maturity/cutoff, and extract date.

For task success, use all pre-defined eligible started attempts as the primary denominator. Include abandoned, timed-out, failed and unfinished attempts; report these outcomes separately. Missing outcomes remain in the denominator and are not silently counted as successes. Any exclusions must be defined before collection and applied identically to each comparator arm.

For D30/retention, do not select a definition from the label or a vendor default. Require an owner-approved cohort-entry event/time basis, return event and criterion, unit/deduplication rule, eligibility, numerator/denominator, maturity/latency rule, cohort dates, and common follow-up cutoff. Exact-day, fixed-window, and after-day definitions are separate metrics; incompatible definitions must not be pooled. Until the controlling contract is authoritative, mark the metric UNKNOWN and do not calculate a decision-grade D30.

Do not describe `orders / opens` or similar aggregate count ratios as conversion unless event-level linked units, deduplication/cardinality, and attribution window are defined and available. Preserve raw counts and label the ratio literally; conditional conversion remains UNKNOWN without the linkage.

Check:

- whether periods and cohort maturity are comparable;
- whether audience, acquisition channels, tariff, or instrumentation changed;
- how missing values, duplicates, returns, abandonment, and exclusions were handled;
- what the result means for users and business, not just the chart;
- what alternative explanations remain.

For a critical derived value, run a deterministic available tool against the pinned source file, not manually copied number arrays. Record source path/locator and SHA-256, exact command/query actually executed, working directory, tool/runtime version, exit status, stdout/stderr, result and units, formula, rounding, and missing/error rules. Preserve failed attempts as failed; if no executable tool is available, label the calculation `NOT RUN`/unverified and do not present mental arithmetic as reproducible evidence. Do not send confidential data to an external calculator. Aggregated dynamics do not establish causality.
