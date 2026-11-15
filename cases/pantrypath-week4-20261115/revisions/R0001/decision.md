# Executive decision memo — PantryPath (synthetic)

- **Decision question:** Which next action should the product lead take to address “soft week-four use” without overstating evidence?
- **Owner / status:** Fictional product lead; recommendation only, `RECOMMENDATION_PENDING_HUMAN`. No owner decision or execution approval has been supplied.
- **Revision:** `R0001`
- **Active claim IDs:** `C-01, C-02, C-03, C-04, C-05`
- **Recommendation:** Do not claim a retention win or promote the checklist. Propose a small, approved, moderated diagnostic of first-week setup and checklist comprehension; use findings to decide whether a larger controlled test is warranted. This is not permission to recruit or build.
- **Why:** Synthetic pilot week-four returns: 22/48 eligible checklist accounts vs 18/48 current flow (+8.3 percentage points descriptively); setup completion lower (26/48 vs 30/48) and support contacts higher (9 vs 5). Assignment and event definitions are missing, so selection/cohort differences could explain the contrast. Not causal or a market estimate. See `E-001`–`E-003`, `C-01`–`C-03`, CSV and receipt in `test-plan.md`.
- **Status quo:** Keep current flow; make no claim. Avoids immediate cost; leaves the complaint unanswered.
- **Stop / close:** Close the initiative and spend nothing. Defensible if decision-grade problem/capacity is unavailable; risks abandoning a useful intervention.
- **Active option — checklist polish:** 31/48 checklist accounts opened it; setup completion is lower, support higher, and return contrast confounded. Do not promote as a retention solution; test comprehension only.
- **Active option — simplify setup:** Recommended as a diagnostic, not a build. Compare a low-fidelity shorter setup with current flow in moderated tasks. CSV does not identify setup as cause. Ops estimate of two engineer-weeks is unverified.
- **Active option — partner promotion:** Defer. Partner segment, demand, proof, cost, and permission are unknown.
- **Product strategy:** Test task success and setup friction before feature release; preserve a current-flow comparator for any later controlled test. No deployment/recruitment before approval, metric contract, privacy review, and capacity check.
- **Communication strategy:** Internal: “The small synthetic pilot shows a descriptive difference, not proof. Test where first-week setup fails before choosing an intervention.” Cite `C-01`–`C-03`; do not call it lift. Partner audience/channel/barrier unknown; send nothing externally.
- **Critical evidence:** `E-001`/`E-002` CSV rows; `E-003` data-definition omissions and synthetic note; `E-004` GOV.UK “Choose relevant research activities” and “Work out participant numbers.” Guidance is method advice, not product evidence.
- **Unknowns:** Return event/window; assignment and cohort quality; user task/segment; outcome completeness; baseline; effect precision; cost/value; partner identity; authority and threshold.
- **Validation:** Stage 1: six approved users, same first-week task on current flow and prototype, counterbalanced. Primary denominator = every eligible started attempt, including abandonment, timeout, failure or missing; numerator = independently completed task without unplanned help. Report assistance/errors separately. Diagnostic stop rule: pause if <5/6 succeed on either flow or ≥2 encounter same critical blocker; not statistical evidence. Stage 2 only after approval and pre-registration of event, assignment, baseline, power/sample, cutoff; comparator = current flow; denominator = all eligible randomized accounts. GOV.UK says A/B tests generally require hundreds; this is not a power calculation. Proposed dates/guardrails in `test-plan.md`.
- **Owner decision / authorization:** `NOT PROVIDED`; `approvals.jsonl` empty. No action is authorized.
- **Next step:** Product lead defines return metric, deadline, target users, success threshold, authority, and research scope before separate approval for contact/build.
