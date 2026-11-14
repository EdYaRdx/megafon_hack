# Blind review 2 — F1

Reviewed anonymized output text against the fixture and sealed key; run mapping withheld. Same eight dimensions as `review-1.md`.

| Output | Score | Dimensions 1–8 | Critical errors |
|---|---:|---|---|
| run-17 | 2/8 | 1,0,1,0,0,0,0,0 | None identified |
| run-28 | 8/8 | 1,1,1,1,1,1,1,1 | None identified |
| run-43 | 7/8 | 1,1,1,0,1,1,1,1 | None identified |

Evidence: `run-17.md:3` distinguishes D7 and causality but lacks denominators, concrete source locators, alternatives, communication and validation. `run-28.md:15–27` matches `cohorts.csv:2–6`, separates D7 using `metric.md:7–8`, and gives source row locators, alternatives and complete validation (`:29–58`). `run-43.md:7–14` calculates correctly and identifies uncertainty; `:18–37` gives options and test details, but no explicit input paths/row locators.

Scores are limited to the supplied text and synthetic inputs; no real-world causal or statistical conclusion.