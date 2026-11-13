# Synthetic retention calculation check

**Date:** 2026-11-13  
**Scope:** Reproduce aggregate D30 retention for mature synthetic cohorts only. The fixture supplies counts, but the operational definitions of the D30 return event and `eligible_users` are `UNKNOWN`; this check validates arithmetic over the supplied fields only. Not MegaFon/customer data.  
**Input:** [`retention-calculation-input-20261113.json`](retention-calculation-input-20261113.json), a field-for-field projection of `cases/retention-demo/input/cohort-retention.csv` lines 2–7 with source path/line locators added. Source CSV remains authoritative.  
**Tool:** JSON reader with its `jq` query selector (`functions.read`, `?q=`). The query selects `period_mature == true`, groups by period, sums `d30_returned` and `eligible_users`, computes rates, and subtracts April from May in percentage points.

```jq
([.[] | select(.period_mature == true)]
 | group_by(.period)
 | map({period: .[0].period,
        returned: (map(.d30_returned) | add),
        eligible: (map(.eligible_users) | add),
        rate: (map(.d30_returned) | add) / (map(.eligible_users) | add)})) as $rates
| {periods: $rates, change_pp: (($rates[1].rate - $rates[0].rate) * 100)}
```

## Observed tool output

```json
{
  "periods": [
    {"period": "2026-04", "returned": 620, "eligible": 1000, "rate": 0.62},
    {"period": "2026-05", "returned": 380, "eligible": 1000, "rate": 0.38}
  ],
  "change_pp": -24
}
```

April D30 = 620/1000 = 62%; May D30 = 380/1000 = 38%; change = -24 percentage points. June (CSV lines 6–7; 10 observed days, immature, no D30 count) is absent from the result because the query filters to mature rows.

## Limits

- An internal JSON-reader jq run and two fresh OMP task runs verify deterministic arithmetic on this synthetic fixture. They do **not** verify that Cursor/Codex exposes or can run the tool, nor that the agent chooses the correct tool in an IDE.
- The JSON file is a manually maintained field-for-field projection and can drift; the source CSV remains authoritative. An initial projection omitted `days_observed` and `synthetic`; review caught this, the fixture was expanded to all seven source fields, and a reviewer confirmed rows 2–7 match.
- Synthetic arithmetic only. No inference about a real product, causal effect, or MegaFon outcome.
- The source defines neither the operational D30 return event nor who qualifies as `eligible_users`; both are `UNKNOWN`. Therefore the rates are arithmetic on fixture fields, not semantically validated product metrics.
- Model/provider, tokens, elapsed time, and cost: `UNKNOWN`.

## Independent review

Independent reviewers confirmed the source-field match and arithmetic. The first review caught the initial projection's omitted `days_observed` and `synthetic` fields; the fixture was expanded. A later review identified that the event/eligibility definitions were unspecified; after this report marked both `UNKNOWN`, a follow-up reviewer confirmed the correction and found no remaining issue. The saved output is a record of the `functions.read` jq run, not a separate execution log or evidence of IDE/agent-tool acceptance.

## Fresh-context skill smoke

A fresh OMP task read root `AGENTS.md` and `.agents/skills/evidence-research/SKILL.md`. It first tried `references/metrics.md` under the skill directory and then a nested `references/` directory; both lookups failed. After listing the project-root `references/` directory, it successfully read `references/metrics.md`, ran the separate `functions.read` jq query below, and did not edit case files or read this report.

```jq
map(select(.period_mature == true))
| group_by(.period)
| map({
    period: .[0].period,
    returned: (map(.d30_returned) | add),
    eligible_users: (map(.eligible_users) | add),
    rate_percent: ((map(.d30_returned) | add) / (map(.eligible_users) | add) * 100)
  })
| {periods: ., may_minus_april_percentage_points: (.[1].rate_percent - .[0].rate_percent)}
```

The task's observed result was April 620/1,000 = 62%, May 380/1,000 = 38%, difference = -24 percentage points. It cited CSV lines 2–5 and excluded June lines 6–7 because the cohorts were immature (10 days, no D30 result). Its limits note that channel mix differs, the aggregate change is non-causal, and this smoke verifies OMP/read-tool behavior only—not IDE acceptance.

This first smoke exposed an ambiguous reference path. The skill now explicitly says `references/metrics.md` is in the project root; the fresh post-fix smoke below verified the corrected route.

### Post-fix rerun

A new task context read `AGENTS.md`, the canonical evidence skill, and the project-root `references/metrics.md`; then read the source CSV and JSON projection and executed one jq query. The trace contains no failed reads or writes. The task did not read the earlier report.

```jq
[.[] | select(.period_mature == true)]
| group_by(.period)
| map({
    period: .[0].period,
    d30_returned: (map(.d30_returned) | add),
    eligible_users: (map(.eligible_users) | add),
    rate: (map(.d30_returned) | add) / (map(.eligible_users) | add)
  })
| . as $periods
| {
    periods: $periods,
    may_minus_april_percentage_points:
      ((($periods[] | select(.period == "2026-05") | .rate)
      - ($periods[] | select(.period == "2026-04") | .rate)) * 100)
  }
```

Observed output: April 620/1,000 = 0.62, May 380/1,000 = 0.38, and May-minus-April = -24 percentage points. It cites CSV rows 2–5 / JSON lines 2–5; June (rows 6–7, 10 observed days, null D30) is excluded. The task notes the channel mix changes sharply between months, so this aggregate comparison cannot isolate a cause. This remains OMP/read-tool behavior only, not IDE acceptance.

## Calculation-guidance tradeoff

- **Benefit:** requires decision-critical derived numbers to be rerunnable from located inputs, reducing silent arithmetic/denominator errors.
- **Cost:** one deterministic tool invocation and saving the input locators, query/formula, units, and output per critical result; time/token/cash cost is `UNKNOWN`.
- **Complexity:** one step in the existing evidence skill and its existing metrics reference; no code utility, service, or dependency added.
- **Test:** a fresh OMP task followed the canonical route and recalculated the synthetic aggregate. The first task exposed ambiguous reference-path wording; the second, after clarification, had no failed lookups. Neither establishes Cursor/Codex acceptance.
