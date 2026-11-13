# Implementation status

**Updated:** 2026-11-14  
**Active stage:** Stage E — exploratory evaluation; final-output contracts hardened and natural-prompt F2 regression reviewed  
**Working baseline:** `codex/megafon-mvp-file-agent`; evidence checkpoint `1931943` (`eval: record retention, launch, and resume trials`)  
**Latest artifacts:** meal-planner revision 3; F1/F2/F3 comparisons and F2 hardening runs 44/45/47 reviewed. Run 47 scored 6/8 in two blind reviews, no P0. **Product acceptance:** incomplete.

## Repository and safety audit

- Current branch `codex/megafon-mvp-file-agent` is one commit ahead of `origin/codex/megafon-mvp-file-agent` at audit snapshot; earlier commits include product research and Sol audit. No branch switch or history rewrite was performed.
- The previously staged `MGIMO_RESEARCH_TO_IMPLEMENTATION.md` is now present in upstream checkpoint `984b529`; it was not included in `ba8817b`. `.omp/profiles/product-build.yml` remains the user's untracked file and is excluded from this work.
- `docs/contest-brief.md` was read in full as the working contract. Exact organizer provenance and the additional MegaFon demo brief remain `UNKNOWN`; neither blocks this explicitly authorized implementation.
- No real MegaFon/customer data or secrets are used. The retention example is explicitly synthetic.

## Requirement inventory

| Requirement | Existing component | Evidence checked | Missing step | Priority |
|---|---|---|---|---|
| Intake and decision-relevant questions | `.agents/skills/intake/`, `cases/meal-planner-demo/brief.md` | New ambiguous service-launch brief records owner/audience unknowns and four decision-changing questions | Fresh host run; collect human answers only if authorized | P0 |
| Documents, tables, permitted websites; traceable evidence | `.agents/skills/evidence-research/`, `cases/meal-planner-demo/` journals/input | Read concept note and synthetic CSV; opened GOV.UK page; checked relevant content and section locator; source/evidence/claim links parsed | Clean-host replay; independently review citations and formats beyond Markdown/CSV | P0 |
| ≥3 distinct options, status quo/stop, strong objections | `cases/meal-planner-demo/options.md` | Four distinct paths: status quo, discovery/prototype, paid launch, stop; each has a counterargument and revisit condition | Independent acceptance of strategic distinctness against contest brief | P0 |
| Product + communication strategy and validation | `strategy-product.md`, `strategy-communication.md`, `test-plan.md` | Strategies are linked; no unsupported public promise; plan states comparator, measures/denominators, time, decision gates, guardrails | Human/independent review; no real experiment is authorized or run | P0 |
| Pause/resume/revise | `.agents/skills/resume-revise/`, case revisions and append-only journals | Fresh OMP task context resumed from saved revision-2 files; revision 2 preserved verbatim, revision-3 synthetic input linked to separate source/evidence/claims, and new decision/state/journal appended. Independent reviewer checked artifacts and flagged a source-locator defect; corrected from the input’s exact rows. | New-chat Cursor/Codex resume; actual user-supplied-data revision and IDE state recovery; final locator correction not separately re-reviewed | P0 |
| Portability / skill discovery | root `AGENTS.md`, canonical `.agents/skills/*/SKILL.md`, README | Cursor and Codex official docs specify `.agents/skills/`; project files were opened manually in OMP tasks | GUI/IDE startup tool is unavailable here; clean Cursor and second-host skill listing/startup remain unverified | P1 |
| Research integrity / security | `references/*`, `AGENTS.md` | Provenance, status labels, untrusted-source and human gates inspected | Adversarial fixture and observed host-permission test | P1 |
| Reproducible calculations / state safety | CSV + claim/evidence journals | Ratios recalculated: 24/120=20%, 15/24=62.5%, 15/120=12.5%; no population extrapolation; revision history preserved | Repeat in fresh host; identify whether deterministic calculation tooling is needed | P1 |
| Comparative evaluation | Sol/Luna protocol; F1/F2/F3 synthetic fixtures and F2 targeted hardening runs | F1 B0/B1/A 2/8, 8/8, 7/8; F2 3/8, 5/8, 5/8; F3 7/8, 7/8, 8/8. F2 run 44 integration 6/8; run 45 6/8 in both reviews; run 47 natural prompt 6/8 in both reviews. One answer per run; exploratory only. | Human review; model/resource equivalence; calculation-tool reproduction; no causal or superiority claim |
| Submission package | README, two synthetic cases, research notes | New case and limitations are documented; no official partner demo, video or final architecture/cost report | Recheck official brief; clean run; write report/video script; record ≤10 min video; submission checklist | P1 |

## Implemented vs. described vs. verified

 - **Implemented as repository files:** six skills in `.agents/skills/`; evidence/security/metrics references; reusable template; synthetic retention, meal-planner, conflicting-terms and service-launch cases; source/evidence/claim journals, options, strategies, validation plans, activity and state.
 - **Described but not demonstrated:** autonomous step selection; actual IDE skill loading; cancel/stop UX; new-chat IDE resume/revision; multi-format ingestion; host isolation; cost transparency; comparative benefit.
 - **Evidence presently checked:** contest brief, branch baseline, skills and source rules; GOV.UK discovery page content/locator; F2 conflicting terms and locators; F2 JSONL records and critical dates/prices/regions/caps; F3 synthetic input locators. F1 rates and F3 threshold arithmetic were checked against fixture inputs and blind reviews; no calculation tool execution was available.
 - **Resume/revision evidence:** revision 1/2 preserved; revision 2 was processed in the authoring session; revision 3 was resumed and processed by a fresh OMP task context using saved files only. Revision-2 state/decision preserved verbatim; revision-3 source/evidence/claims segregated, recommendation reevaluated, and event appended. Independent reviewer found an off-by-one row-locator error; it was corrected against the opened input table (rows 7–8). No repeated public research or pooling. This is not a Cursor/Codex new-chat test.
 - **Evaluation evidence:** F1 B0/B1/A scored 2/8, 8/8, 7/8; F2 3/8, 5/8, 5/8; F3 7/8, 7/8, 8/8. F2 run 44 was integration-adjudicated 6/8 (blind 6/8 and 7/8); run 45 scored 6/8 in both reviews; natural-prompt run 47 scored 6/8 in both reviews. Run 47 includes source IDs/locators, explicit status quo/stop, communication fields and a formula/denominator; communication and validation remain partial because audience/barrier/channel and operational test inputs are unknown. One synthetic response per run; model/provider, resources, human time, tokens and billing unknown. No P0 reported.

## Current defects / risks

1. README contains a second synthetic case, not a clean host/product acceptance result.
2. Skills use documented Cursor/Codex project path `.agents/skills/`; actual host UI discovery was not exercised.
3. Current tool surface provides file/read/search/task operations, but no Cursor/Codex GUI or computer-use launch. A real IDE startup and new-chat test cannot be observed in this session; manually reading the files in OMP is not an equivalent pass.
4. No official MegaFon demo brief, real product data, observed billing, second-host run, or video package is available.

Next: checkpoint the tightened Agent Skills and F2 run-47 evidence. Keep clean IDE startup/resume, human scoring, model/cost controls, calculation-tool reproduction, and video package as blockers. F1/F3 arithmetic was not run through a calculation tool; run-47's test plan correctly remains not ready pending owner-set sample, period, baseline, thresholds, and approval.
