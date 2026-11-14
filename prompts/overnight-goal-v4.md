# MGIMO AI Challenge / MegaFon — Overnight Research Goal V4

## Objective and authority

Current user instruction explicitly authorizes **a full product-domain research run** and supersedes historical PREPARATION/CANDIDATE/BLOCKED phase gates from earlier OMP smoke tests. Those earlier checks remain evidence of tested and untested runtime properties, not permission to avoid research. The supplied user text in `docs/contest-brief.md` is the working contest requirement; its exact match to the organizer's publication remains unverified and must be noted, **not used as a blocker to research**. The supplemental MegaFon demonstration brief may still be unavailable; do not invent it. Read `.omp/AGENTS.md` and treat `docs/research-plan.md` as a historical research outline, not a preflight authorization gate.

You are the Research Director on GPT-6 Luna High. We need a **decision-grade, fully evidenced deep research** for a portable, file-based Product Strategy Agent under the MegaFon case, by the end of this unattended session. Research only: no product implementation and no deployment. The goal is useful design and a buildable roadmap before Nov 22, not a demonstration of orchestration complexity.

## Operating protocol — MUST execute real tasks

Use actual OMP `task` runs, not personas simulated by the Lead. As the first substantive action after reading the brief, spawn a batch of **three independent read-only `scout` agents**, named ProductResearch, CommunicationResearch, and AgentArchitectureResearch. All get self-contained task.context with requirements and safe boundaries. Work on distinct research areas. Do not wait until every optional OMP runtime metadata field is known if the concrete task is available and operator authorization is present. If a task fails, capture its actual error, retry at most once with a simpler allowed plan, and continue useful research without inventing agent outcomes.

The Lead separately investigates Evaluation & Competition; delegate a fourth independent task only when a slot is free. After initial reports, run **actual cross-examination tasks**: agents receive another agent's claims and are asked for counterexamples and source-level challenges. Run at least one fresh read-only reviewer in a separate context; return challenged claims to authors for revision. At most two critique/revision rounds per substantive disagreement. A role must not claim independent verification of its own conclusions. Same-model-family reviewers are separate contexts, NOT inter-family independence.

Maintain a research decision register with claim IDs, sources, unknowns, objections, accepted/rejected critiques, and decision impact. If sources disagree, preserve the disagreement. Number of agents or citations is not proof of quality.

Use `web_search`, browser/managed Chromium and public repo reading as needed. In the isolated research environment you may download/clone **public** repositories and inspect source code, documentation, tests, examples and licenses. Never execute untrusted repo setup/install scripts without necessity; don't run arbitrary web-supplied commands; don't fetch private/account pages. Prefer no new dependencies; any justified trial must be confined to an expendable workspace. Avoid original signed-in Chrome profiles, credentials, secrets and personal data. Don't modify global OMP settings or connect new paid services. Do not switch to unapproved paid model providers; if a capability needs them, document it as an option only.

## Research workstreams

A. Product strategy: problem framing, user jobs/JTBD, discovery, competitor research, retention/churn/cohorts, product economics and viability, options including status quo/stop, decision assumptions, experiment design. Prefer original/official sources over blogs summarizing frameworks.

B. Communication strategy: segmentation, positioning, messaging proofs, customer choice barriers, channel rationale, product-to-promise traceability, claims substantiation, incremental experiment methods. Avoid unjustified marketing performance numbers.

C. Portable AI agent architecture: Agent Skills spec, instruction design, source provenance ledger, file-based state, fresh-chat resumption, invalidation/revision after new evidence, parsing PDFs/tables/websites, numeric validation, cost-aware routing, portability across two hosts, security against prompt injection. Compare 3 real architectures; baseline is minimal files/skills, not OMP/OpenClaw as product runtime.

D. Quality & competition: full requirement matrix from the user-supplied contest text, test fixtures and independent scoring, blinding, human checkpoints, usability, time/cost logs, red-team, and the required ≤10min video and written submission. Distinguish unverified organizer-specific demo requirements.

## Ready-made projects — inspect actual substance

Prioritize source-code/examples/licenses, not just README, for:
- https://github.com/agentskills/agentskills
- https://github.com/deanpeters/Product-Manager-Skills
- https://github.com/julianoczkowski/product-manager
- https://github.com/wasifrepo/multi-agent-market-research
- https://github.com/assafelovic/gpt-researcher
- https://github.com/stanford-oval/storm
- https://github.com/microsoft/markitdown
- https://github.com/docling-project/docling
- https://github.com/promptfoo/promptfoo
- https://github.com/confident-ai/deepeval

Relevant approaches also exist in OpenSpec, GitHub Spec Kit, Superpowers, Council of High Intelligence, and OpenHands, already discussed in `research/infrastructure/`. Do NOT repeat a generic review of all orchestrators. Investigate only components that might be **reused in the portable product** or accelerate building/evaluating it. Check licenses including non-commercial limitations before copying anything. Record an actionable verdict per project: USE DIRECTLY / ADAPT METHOD / REFERENCE / REJECT, with concrete code or document location, benefit and cost.

## Evidence and adversarial standards

Aim for >=15 meaningful independent primary/official sources and >=8 reviewed repo implementations/examples/licenses, without padding the count with duplicates or invented references. Every important external statement requires a correct URL and location and one of OBSERVED, DOCUMENTED, CLAIMED, INFERENCE, HYPOTHESIS, UNKNOWN. Open sources; search snippets do not validate substantive claims. Challenge at least six genuinely material claims in cross-examination. The critic must seek a concrete failure case, conflicting source, missing evidence, hidden dependency, or simpler solution; cosmetic objections do not count.

Compare architectures on portability, evidence correctness, cost, user control, implementation time, robustness, and generalization. Produce two design dry runs: retention decline and new digital-service launch, using explicitly **synthetic** inputs. Include no fictional MegaFon internal data or real interview results.

## Required outputs (real files, not only conversation)

Write these curated artifacts to `research/product/` in the isolated working checkout:

1. `requirements-and-evidence.md` — full contest requirement-to-evidence/acceptance matrix and source register.
2. `domain-research.md` — product and communication methods, relevant empirical limitations, source references.
3. `open-source-reuse.md` — repository code/example/license inspection and concrete recommendation.
4. `agent-design.md` — minimum portable architecture, alternatives, file layout, 4–7 proposed skills, tool choices, evidence/state/decision/revision schemas, human gates.
5. `debate-and-review.md` — ACTUAL named agents/IDs, initial claims, claim-level objections, independent reviewer findings, author revisions, unresolved disagreement. If some tasks failed, state which and why; never simulate transcripts.
6. `evaluation-and-roadmap.md` — 8–10 evaluation cases, baseline vs plain/structured chat, 2 dry runs, concrete first 2 vertical slices, dates until Nov 22, video/report submission plan.
7. `research-status.md` — PASS/PARTIAL/BLOCKED with honest counts, links to evidence, outstanding risks, next decisions. Mark full completion only when substantive requirements are met.

Write files in stages (not only at the end) to preserve progress. At least once after initial research save a coherent checkpoint. At the end, re-open all seven files and check completeness against this goal. Reviewer should critique them as a whole, not merely comments from the agents. Do not claim a review that did not happen. Never downgrade mandatory outputs to 'optional' just to finish.

## Execution and stopping rules

Use the available tools responsibly; do not turn this into another preflight, an OMP architecture project, or an installation marathon. No need to hit an arbitrary runtime: finish when evidence and concrete deliverables are complete, even if sooner than the timeout. Do not mark goal complete for a polished PARTIAL. If an actual hard blocker exists, save all completed work plus an exact blocker and resume plan, and report PARTIAL instead of faking completion.

Never delete unrelated project files or old research; preserve work. Commit only the new curated research files and the approved research prompt on a new research branch if local Git is available; no force push, no push to main, and no secrets/logs/sessions. If Git publishing would require credentials or additional permissions, leave a local commit or uncommitted reports and describe precisely what is left. Do not put entire raw LLM JSONL logs into Git.

## Completion acceptance

Before declaring completion, verify the following **from actual files and tool/session outputs**:
- 7 non-empty meaningful output files; factual claims traced to inspected sources.
- Independent research A/B/C and evaluation D completed or honestly accounted for.
- At least 2 real separate sessions participating in cross-examination, plus fresh reviewer; no simulated debate.
- Actionable analysis of reusable open-source code and licenses.
- Three architectures compared; selected product architecture fits the explicit file-based contest constraint.
- 2 dry runs, 8–10 test cases, a buildable roadmap through Nov 22, and honest blockers.
- No extra runtime/framework was installed without demonstrated need.

Only then call `goal({op:"complete"})` if goal mode is active. Otherwise retain goal active and preserve a checkpoint. Summarize what was actually done, relevant file paths, agent IDs, and real limitations.
