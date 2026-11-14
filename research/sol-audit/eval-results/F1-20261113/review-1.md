# Blind review 1 — F1

Reviewed anonymized output text against the fixture and sealed key; run mapping withheld.

| Output | Score | Dimensions 1–8 | Critical errors |
|---|---:|---|---|
| run-17 | 2/8 | 1,0,1,0,0,0,0,0 | None identified |
| run-28 | 8/8 | 1,1,1,1,1,1,1,1 | None identified |
| run-43 | 7/8 | 1,1,1,0,1,1,1,1 | None identified |

Evidence: `run-17.md:1–2` gives aggregate rates, D7 separation and uncertainty but lacks segment arithmetic, locators, alternatives, strategy and validation. `run-28.md:15–27` has correct calculations and concrete cohort row locators; `:29–44` options/objections; `:46–58` communication and test plan. `run-43.md:7–14` has correct calculations and uncertainty; `:16–37` options, strategy and validation, but no explicit supplied source paths/concrete row locators. Inputs: `cohorts.csv:2–6`, `metric.md:3–8`.

Scores assess response text only. No causal inference or significance claim was validated beyond the synthetic fixture.