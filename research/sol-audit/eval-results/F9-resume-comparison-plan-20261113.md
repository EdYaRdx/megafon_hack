# F9 exploratory resume comparison — frozen plan

**Date:** 2026-11-13. **Purpose:** exploratory B0/B1 response check against the already completed A saved-state run. Not a controlled experiment.

## Conditions

Use two separate fresh OMP task contexts. Both get the exact F9 user-equivalent request and the same R1 snapshots, R1 and R2 synthetic notes, and initial R1 source/evidence/claim/activity records. Both get one attempt to read `cases/resume-failure-demo/input/commissioned-study-summary.md`; no retry and no external research/action. Neither sees the sealed key, A artifacts, R2 ledgers, skills, or root instructions. They return proposed R2 artifacts in the answer only; no files are written because the evaluated A case is already at R2.

- **B0:** ordinary chat; prompt: “Complete assignment thoroughly: Resume the specified case, process the new synthetic note, record the unavailable input honestly, preserve revision 1, and save revision 2. No external actions.”
- **B1:** same prompt and materials plus the frozen structured prompt from `research/sol-audit/evaluation-plan.md`: define goal/unknowns; connect facts to sources and locators; provide at least three distinct options including status quo and objections; align product/communication strategy; give a comparator, metrics, timing, guardrails and verification plan.
- **A:** `ResumeFailureFreshContext`, actual skill/file workflow and saved R2 artifacts, after correction of two reviewer findings. This run predates and was not randomized with B0/B1.

## Frozen 0–2 scoring (sealed F9 dimensions)

0 = materially absent or wrong; 1 = partial/ambiguous; 2 = clear and complete.

1. Resume only pending work; no silent restart or repeated research.
2. One-time missing lookup is reported honestly; no fabricated content; source/evidence trail is correct.
3. Claim-level impact is clear; cohorts stay separate; no unsupported population generalization.
4. R1 history is preserved; R2 successor/current pointers, decision/state/event proposal, and exact next step are clear. For B0/B1 this scores the proposed transition only, not actual saved-state behavior.
5. Human gate/no external action is maintained; no synthetic input is presented as real evidence.

## Known deviations and limits

The protocol calls for isolated clean work folders, equivalent host/tool resources, and verification that B0/B1 do not load project instructions from a parent/profile. This session cannot provide separate checkouts or verify loader isolation. B0/B1 therefore run under a strict read allowlist in separate task contexts but share the repository workspace; they are answer-only and cannot be treated as full system baselines. Model/provider/version identity, equivalence, tokens, cost and human-active time are `UNKNOWN`. One response per arm, no randomization, arms not concurrent with A; results are exploratory, non-causal, and not evidence of superiority.