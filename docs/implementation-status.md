# Implementation status

**Updated:** 2026-11-13  
**Active stage:** Stage A — vertical slice  
**Working baseline:** `codex/megafon-mvp-file-agent` at `3675280` (`feat: add file-first product strategy MVP workflow`)  
**Latest verified artifact revision:** `cases/meal-planner-demo/`, revision 2 synthetic case; reviewer and independent context-recovery check completed. **Product acceptance:** still incomplete; host runtime tests not run.

## Repository and safety audit

- Current branch is the dedicated MVP branch and tracks `origin/codex/megafon-mvp-file-agent`; it is based on the successive `codex/sol-audit` and `codex/product-research-v4` work. These branch refs are present locally/remotely. `main` is a separate, older research snapshot; the feature branch is 67 changed paths / +2,163 −93 versus local `main` at audit time.
- Existing user changes are preserved: staged `MGIMO_RESEARCH_TO_IMPLEMENTATION.md` and untracked `.omp/profiles/product-build.yml`. Neither is part of this implementation. No branch switch, reset, cleanup, or user-file edit performed.
- `docs/contest-brief.md` was read in full as the working contract. Exact organizer provenance and the additional MegaFon demo brief remain `UNKNOWN`; neither blocks this explicitly authorized implementation.
- No real MegaFon/customer data or secrets are used. The retention example is explicitly synthetic.

## Requirement inventory

| Requirement | Existing component | Evidence checked | Missing step | Priority |
|---|---|---|---|---|
| Intake and decision-relevant questions | `.agents/skills/intake/`, `cases/meal-planner-demo/brief.md` | New ambiguous service-launch brief records owner/audience unknowns and four decision-changing questions | Fresh host run; collect human answers only if authorized | P0 |
| Documents, tables, permitted websites; traceable evidence | `.agents/skills/evidence-research/`, `cases/meal-planner-demo/` journals/input | Read concept note and synthetic CSV; opened GOV.UK page; checked relevant content and section locator; source/evidence/claim links parsed | Clean-host replay; independently review citations and formats beyond Markdown/CSV | P0 |
| ≥3 distinct options, status quo/stop, strong objections | `cases/meal-planner-demo/options.md` | Four distinct paths: status quo, discovery/prototype, paid launch, stop; each has a counterargument and revisit condition | Independent acceptance of strategic distinctness against contest brief | P0 |
| Product + communication strategy and validation | `strategy-product.md`, `strategy-communication.md`, `test-plan.md` | Strategies are linked; no unsupported public promise; plan states comparator, measures/denominators, time, decision gates, guardrails | Human/independent review; no real experiment is authorized or run | P0 |
| Pause/resume/revise | `.agents/skills/resume-revise/`, case revisions and append-only journals | Same-session revision processed; an independent read-only OMP context recovered the saved revision-2 state, next action, and unknowns without chat history | Fresh chat in a supported IDE and real new-data revision | P0 |
| Portability / skill discovery | root `AGENTS.md`, canonical `.agents/skills/*/SKILL.md`, README | File-based workflow and skill format exist; skill source instructions reviewed | Verify discovery in supported hosts; clean launch in two hosts | P1 |
| Research integrity / security | `references/*`, `AGENTS.md` | Provenance, status labels, untrusted-source and human gates inspected | Adversarial fixture and observed host-permission test | P1 |
| Reproducible calculations / state safety | CSV + claim/evidence journals | Ratios recalculated: 24/120=20%, 15/24=62.5%, 15/120=12.5%; no population extrapolation; revision history preserved | Repeat in fresh host; identify whether deterministic calculation tooling is needed | P1 |
| Comparative evaluation | `research/sol-audit/evaluation-plan.md`, Luna/Sol research | Protocol and constraints exist; prior product runs are not claimed | Matched B0/B1/A execution with comparable inputs, tools, telemetry and independent review | P1 |
| Submission package | README, two synthetic cases, research notes | New case and limitations are documented; no official partner demo, video or final architecture/cost report | Recheck official brief; clean run; write report/video script; record ≤10 min video; submission checklist | P1 |

## Implemented vs. described vs. verified

 - **Implemented as repository files:** six skills in `.agents/skills/`; evidence/security/metrics references; reusable template; synthetic retention and meal-planner cases with source/evidence/claim journals, options, decision drafts, strategies, validation plans, activity and state.
 - **Described but not demonstrated:** autonomous step selection, host UI skill loading, cancel/stop UX, new-chat resume/revision, multi-format ingestion, trustworthy host isolation, cost transparency and comparative benefit.
 - **Evidence presently checked:** contest contract, branch graph/status/diff, core skills/instructions, opened GOV.UK discovery page and relevant content, and a new synthetic case using a local concept note, CSV, exact URL/section, claim/evidence links, four alternatives, aligned strategies and gated validation plan. JSONL journals were parsed; calculations manually recomputed.
- **Resume/revision evidence:** revision 1 decision/state preserved; revision 2 processed a new synthetic note, retained counterexamples, and left real demand UNKNOWN. An independent OMP task context reconstructed current state and exact next step from files only (PASS); that does not prove a new-chat run in Cursor/Codex.

## Current defects / risks

1. Product README now links a new case but does not imply host acceptance or real-world validity.
2. Canonical skills have moved from root `skills/` to `.agents/skills/`, the project-level location documented by Cursor and Codex. Discovery is supported by their docs; actual IDE loading remains unverified. Do not retain duplicate copies.
3. No runtime/CLI exists. This is not yet a defect: add one only if the slice demonstrates a concrete correctness or resume failure.
4. No official MegaFon demo brief, actual product data, observed costs, or second host run is available.

Next: test skill loading and state restoration in a clean new host session. Then run the matched B0/B1/A cases from the saved Sol/Luna protocol; preserve the user's staged/untracked files when checkpointing.
