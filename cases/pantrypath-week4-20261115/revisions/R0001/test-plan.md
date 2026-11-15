# Validation plan — design only, not authorized

- **Question:** Do users who already plan meals online encounter a recurring first-week setup barrier that a shorter setup flow removes without more errors or help?
- **Hypothesis/falsifier:** `C-05`: shorter setup improves independent task success. No repeated actionable blocker or more critical errors/assistance falsifies the proposed direction.
- **Comparator:** Stage 1 moderated paired diagnostic: same task on current flow vs low-fidelity shorter-setup prototype, counterbalanced. Stage 2 controlled product test only after approval; current flow comparator and assignment/power plan pre-registered.
- **Audience/eligibility:** Proposed adults currently using an online weekly meal planner, consented; recruitment frame and representativeness unknown. No contact authorized. Stage 1 target six (qualitative diagnostic, not prevalence).
- **Primary metric (Stage 1):** unit = eligible started task attempt; eligible = meets criteria and consents; start = begins fixed task; numerator = completes predefined weekly-plan task without unplanned help; denominator = all eligible starts, including abandonment, timeout, failure, and missing outcome. Report success, assistance, errors, abandonment, timeout, and missing counts/rates on that denominator.
- **Outcome handling:** paired per-participant attempts; missing/technical failures reported; exclude only a prelisted platform-wide outage, consistently and separately for both conditions.
- **Window/dates:** proposed sessions 2026-11-18–20; synthesis 2026-11-23, conditional on owner/privacy/safeguards approval. Stage 2 dates unknown until metric and power plan exist.
- **Diagnostic threshold/stop:** continue only if at least 5/6 independently complete each flow and no repeated critical blocker; pause if fewer than 5/6 succeed on either flow or ≥2 hit same critical blocker. Triage threshold, not statistical evidence. Stage 2 effect threshold `UNKNOWN`; owner must define before sample/power/launch.
- **Guardrails:** consent and withdrawal; avoid sensitive food/health details; no external claims; stop for privacy/safety issue, misleading task, or material accessibility failure. Accessibility criteria/participants need owner review.
- **Stage 2 prerequisites:** define return event/window, cohort entry, deduplication, eligibility, maturity/cutoff, baseline, assignment, missingness and threshold. Denominator = all eligible randomized accounts; retain non-starts and report missing separately, never exclude post hoc. Sample size/power `UNKNOWN`. GOV.UK says A/B testing generally requires hundreds to yield clear findings; not a power calculation.
- **Data/source:** synthetic CSV `inputs/pilot-summary.csv`, SHA-256 `ecd78a589a5f7d17fd6b131dc9331b54e39cd8ab855270a95b66a023983577a4`; see `sources.jsonl`. No real users/events.
- **Owner/approval:** fictional product lead unidentified; no approval. No recruitment, build, deployment, or partner contact.
- **Actions:** repeated blocker and no guardrail issue → propose scoped prototype and preregistration; no repeated blocker → preserve current flow or close; safety/accessibility failure → stop/remediate before further research.

## Calculation receipt (executed)

- Purpose: descriptive rate calculation only; no causal/significance test.
- Exact command, CWD `/workspace`:

```sh
sha256sum cases/pantrypath-week4-20261115/inputs/pilot-summary.csv && python3 - <<'PY'
import csv
path = "cases/pantrypath-week4-20261115/inputs/pilot-summary.csv"
with open(path, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
for row in rows:
    eligible = int(row["eligible_accounts"])
    started = int(row["started_week1"])
    completed = int(row["completed_setup"])
    returned = int(row["returned_week4"])
    opened = int(row["checklist_opened"])
    print(f'{row["arm"]}: setup={completed}/{eligible}={completed/eligible:.3f}; week4_return_eligible={returned}/{eligible}={returned/eligible:.3f}; week4_return_starters={returned}/{started}={returned/started:.3f}; checklist_open={opened}/{eligible}={opened/eligible:.3f}')
delta = (int(rows[1]["returned_week4"])/int(rows[1]["eligible_accounts"]) - int(rows[0]["returned_week4"])/int(rows[0]["eligible_accounts"])) * 100
print(f"descriptive week4-return difference={delta:.1f} percentage points")
PY
```

- Runtime Python 3.13.5; exit 0. Raw stdout: SHA-256 `ecd78a589a5f7d17fd6b131dc9331b54e39cd8ab855270a95b66a023983577a4`; current flow: setup 30/48=0.625; return/eligible 18/48=0.375; return/starters 18/44=0.409; checklist open 0/48=0.000. Prep checklist: setup 26/48=0.542; return/eligible 22/48=0.458; return/starters 22/43=0.512; checklist open 31/48=0.646. Difference = +8.3 percentage points (checklist minus current).
- Formula: each count/eligible (started-only return shown secondarily); difference `(22/48 − 18/48) × 100`, rounded to one decimal point. No imputation. CSV labels and denominator are not validated product contracts.
- First shell invocation failed at parse time due quoting (`bash` syntax error); it generated no results. Successful retry above; both attempts recorded in activity log.
