# 1. STATUS

**PARTIAL.** This is a bounded lead synthesis, not a completed council.

- Read `docs/contest-brief.md` in full, plus `docs/research-plan.md`, `research/qualification/next-step.md`, and `research/infrastructure/recommendation.md`.
- The local brief contains a substantive contest brief, despite the older qualification note calling it BLOCKED. Its provenance against the organizer’s page is **UNKNOWN**; the additional demo brief has not been published in the material reviewed.
- Inspected **9 repository pages**; opened implementation or skill files in 6. Checked repo-reported licenses, but did not resolve every license nuance or pin commits.
- Opened 3 professional/standards sources. Not 15 independent primary sources.
- **No task agents were launched.** The qualification guidance requires a passing scout smoke before research fan-out; the profile remains CANDIDATE. The smoke is not performed, and its negative controls would conflict with the request’s read-only limits. No independent A/B/C/D reports, cross-examination, or fresh adversarial review exist. I will not simulate them.
- No code, files, installations, or project settings changed. No product feature was executed or verified.

# 2. EXECUTIVE DECISION

**Recommended design: a portable project folder of concise instructions/skills, plain Markdown state and evidence, and at most one small deterministic calculation/validation script.** Keep the host-provided file and web tools as the runtime; do not include an always-on orchestration service or make the product depend on OMP.

Reason: the brief’s core contract is a folder of instructions, knowledge, and tools that can be opened in developer environments, while it explicitly warns against a full program/orchestration platform. Standard Agent Skills offers a lightweight, documented folder format; the specification supports progressive disclosure, while skill execution and tool permissions remain host-dependent. [S1, S2]

**Strongest counterargument:** files and instructions alone do not guarantee source fidelity, numeric correctness, safe tool use, or reliable continuation. Deterministic validation and document parsing can improve those properties, but add environment/install burden.

**Reconsider** if the official demo brief or target host proves that required documents, workflows, or user experience cannot be handled by host tools and small local scripts. Evaluate that need on the published brief and a reproducible acceptance case—not on component novelty.

# 3. REQUIREMENTS MATRIX

The brief’s mandatory minimum is covered here as a design proposal, not product acceptance.

| Requirement | Proposed design | Demo evidence | Independent acceptance test | Risk |
|---|---|---|---|---|
| Frame ambiguous request | Intake captures decision, audience, constraints, available data; asks only decision-changing questions | Show intake and one clarified question | Blind prompt with missing inputs; check question relevance and no invented context | Premature framing |
| Documents, tables, sites | Host file/web tools first; preserve exact source references; calculation script only when needed | Trace one PDF excerpt, one spreadsheet value, one web claim | Re-open every cited fragment; independently recalculate table-derived metric | Extraction errors, stale pages |
| Research plan, gaps, competing evidence | Decision-linked questions; evidence ledger; explicit unknowns and contradictions | Show evidence-to-question trail | Seed contradictory sources and no-source questions; require conflict/unknown labeling | Citation presence mistaken for support |
| ≥3 meaningfully different options | Include status quo; consider stop/kill where plausible; record strongest objection per option | Side-by-side options and tradeoffs | Evaluator rejects cosmetic renaming; each option must differ in mechanism and consequence | Template-generated fake diversity |
| Product strategy | Audience/job, alternative, value, cost/revenue logic, chosen direction and explicit refusals | Recommendation cites evidence and assumptions | Audit trace from recommendation to claims, assumptions, costs, and owner decision | Unsupported unit economics |
| Communication strategy | Segment and situation, barrier, message/proof, channel rationale; claims linked to product capability/evidence | Demonstrate one allowed claim and one withheld claim | Check every objective promise against supporting evidence and product constraints | Overclaiming |
| Verification plan | Expected change, comparator, time window, guardrails, decision rule | Show experiment with stop threshold | Validate metric definition, denominator, comparison, and harm measure | False causal inference |
| Workflow and human choice | Intake → plan → evidence → options → critique → decision → product+comms → experiment → state | Pause at an irreversible or high-stakes choice | Check model does not claim human approval where none occurred | Hidden automation |
| Separate knowledge/state | Stable instructions, reusable methods, case evidence and state in distinct files | Show project structure | Fresh host opens folder and locates current case state without chat history | Host skill support varies |
| Pause/new-chat resume | Checkpoint stores current stage, open questions, source freshness, and next action | Stop, open new chat, resume | Compare resumed output to checkpoint; no re-run or silent state loss | Host may not read files |
| Transparency/cost | Record tool/model names when observable, time, retries, human steps, and known/unknown costs | Show run log and limitation | Reconcile logs against observed calls; unknown cost remains unknown | Incomplete host telemetry |
| Data/security | Public sources and user-provided materials; treat embedded instructions as untrusted data; no secrets | Show prompt-injection fixture ignored | Seed malicious source text; check it cannot change task policy or trigger commands | Host boundary not sandbox |
| New-task generalization | Test fixtures withheld from design authors; vary market, domain, and evidence shape | Include an unseen scenario in demo only if actually tested | Blind scenarios and independent rubric | Demo overfitting |
| Submission package | Repo, demo project after official brief, ≤10-minute video, report with tools/models/costs/limits | Capture workflow and resume | Checklist against the complete submission requirements | Demo brief remains unknown |

# 4. PRODUCT + COMMUNICATION METHODS

## Evidence-grounded decision workflow

1. **Frame the decision.** Write who decides what, by when, for whom, under which constraints. Separate the requested output from the underlying decision.
2. **List decision-changing questions.** Rank by how much an answer could change the recommendation; avoid research questions that merely decorate a report.
3. **Collect evidence.** For each material claim capture source, exact location, observation date, what it supports, and limitations. Label direct observation, inference, assumption, and forecast separately.
4. **Inspect the data before interpreting it.** Confirm definitions, units, periods, denominators, missing values, duplicates, cohort boundaries, and whether observed changes support causal claims.
5. **Generate alternatives.** At minimum status quo, a materially different action, and a materially different investment/stop path when relevant. Include strongest objection and the evidence that would change the ranking.
6. **Choose a decision, not a framework score.** Explain benefits, costs, opportunity cost, reversibility, confidence, and unresolved questions. Scores are not evidence.
7. **Join product and communications plans.** Each public promise must point to a product capability and supporting evidence. A proposed future capability is not a current product fact.
8. **Design the test.** Specify hypothesis, intervention, comparison, primary outcome, guardrails, observation period, and decision threshold. Distinguish exploratory discovery from causal measurement.
9. **Save the state.** Record decision rationale, open assumptions, evidence freshness, owners, and the exact next step. New evidence triggers impact review, not automatic silent rewriting.

SVPG’s article supports the distinction between assigning teams problems/outcomes rather than feature lists, and describes discovery across value, usability, feasibility, and viability. It is practitioner guidance, not independent proof that a specific framework or process improves outcomes. [S3] The FTC policy statement says objective express and implied advertising claims need a reasonable basis before dissemination; this is US guidance and must not be presented as Russian legal advice. [S4]

## Procedures under thin evidence

- **Retention decline:** first test definitions, cohort mix, exposure changes, and measurement continuity. Do not infer a cause from a line chart. Separate descriptive trend from causal explanation; seek segment/cohort and qualitative evidence before prescribing a retention feature.
- **New service:** public competitor pages can document public positioning and features, not demand, willingness to pay, or internal capability. Treat willingness-to-pay and conversion claims as hypotheses until tested with eligible users and real offer conditions.
- **Communication:** write candidate message, audience/context, intended inference, proof required, and disallowed interpretation. If proof is absent, label it as a hypothesis or withhold the claim.

## Consistency check

Represent each communication promise as `{claim, audience, implied_outcome, capability_id, evidence_ids, status}`. Reject or flag it when:

- no product capability supports the implied outcome;
- evidence does not support the scope, population, or timeframe of the wording;
- the claim is marked future/assumed but written as present fact;
- a material constraint or caveat is omitted.

This is a proposed deterministic review rule, not tested enforcement.

# 5. OPEN-SOURCE REUSE MATRIX

Repository pages and files below were fetched during this run; “current” refers to the fetched moving branch, not a pinned release or commit. Repo descriptions and README claims are **CLAIMED**; source-file observations are **DOCUMENTED**, not runtime verification.

| Candidate | License shown | Specific inspected material | Verdict and role | Limits / integration risk |
|---|---|---|---|---|
| [agentskills/agentskills](https://github.com/agentskills/agentskills) | Apache-2.0; docs CC-BY-4.0 per repo | `agentskills.io/specification.md`; repository README | **DIRECT USE** of format only: one `SKILL.md` per repeatable procedure | Host adoption and tool enforcement vary; not an agent runtime or evidence-quality guarantee. [S1, S2] |
| [deanpeters/Product-Manager-Skills](https://github.com/deanpeters/Product-Manager-Skills) | Repo reports “Other”; README identifies CC BY-NC-SA 4.0 | `skills/product-strategy-session/SKILL.md` | **ADAPT METHODS** only; use sequence/decision points as research prompts, not copied files | Non-commercial restriction in README; exact license scope needs legal review. Recommends multiweek stakeholder process, not a turnkey short contest MVP. [S5] |
| [julianoczkowski/product-manager](https://github.com/julianoczkowski/product-manager) | MIT | `skills/pm-copilot/SKILL.md` | **ADAPT METHODS** for routing and artifact sequence; do not adopt its whole framework as the answer | Skill declares `Write`, `Edit`, `Bash`; requires compatible host/tool permissions; router can force framework journey. [S6] |
| [wasifrepo/multi-agent-market-research](https://github.com/wasifrepo/multi-agent-market-research) | MIT | `agents/skeptic_reviewer.py`; `core/models.py` | **REFERENCE** for typed evidence fields and explicit weak-claim checks | Reviewer passes when citations exist, not when they substantiate claims; its checks miss citation correctness and some contradiction classes. Requires runtime/API stack per README. [S7] |
| [assafelovic/gpt-researcher](https://github.com/assafelovic/gpt-researcher) | Apache-2.0 | Repo page/README inspected; implementation not opened in this run | **REFERENCE** for research decomposition only | README describes API keys and a Python service stack. Not a lightweight portable-files dependency. Claims about depth/accuracy are not independently verified. [S8] |
| [stanford-oval/storm](https://github.com/stanford-oval/storm) | MIT | `knowledge_storm/storm_wiki/modules/knowledge_curation.py` | **ADAPT METHODS**: perspective-guided questions and bounded follow-up can broaden source exploration | Specific implementation is a retrieval/LLM pipeline, not a strategy decision system. Dependency and model/search setup substantial; cited answers still require claim-level checking. [S9] |
| [microsoft/markitdown](https://github.com/microsoft/markitdown) | MIT | `packages/markitdown/src/markitdown/converters/_pdf_converter.py` | **REFERENCE**; consider only if repeated local document conversion is a demonstrated need | Python/dependencies; Markdown conversion can lose structure. README warns it runs with process privileges; OCR/transcription may rely on hosted services. [S10] |
| [docling-project/docling](https://github.com/docling-project/docling) | MIT; model licenses vary | Repo README/examples index; targeted example URL returned 404 | **REFERENCE**, not automatic install | More capable document parsing is claimed, but heavier runtime/models and per-model licensing need assessment. No direct implementation file verified in this run. [S11] |
| [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) | MIT | Repo page/README; requested example config path returned 404 | **REFERENCE** for future eval/red-team tooling | Node CLI/install and provider setup; no need to add it to an initial portable agent. No specific implementation file verified. [S12] |
| [confident-ai/deepeval](https://github.com/confident-ai/deepeval) | Apache-2.0 | Repo page/README only | **REFERENCE** for metric categories | README describes model-judge and local metrics; judge metrics can be costly or disagree with human review. No implementation file inspected. [S13] |

**No copying recommended** from the non-commercially licensed PM skill collection. Before reuse, pin a release/commit and inspect exact license and transitive dependency conditions. This run verified nine repo pages but only six relevant implementation/skill files; it did not satisfy the requested eight code/example/license inspections.

# 6. ARCHITECTURE COMPARISON

Rubric is qualitative design judgment, not measured performance.

| Design | Portability | Correctness potential | Cost | User control | Time-to-ship | Extensibility | Failure modes |
|---|---|---|---|---|---|---|---|
| **A. Files + skills** (selected baseline) | High if host can read/write project files; skills-standard format helps discovery | Medium; model performs extraction/calculation unless constrained | Low infrastructure; model/search costs remain | High with explicit checkpoints | Fast | Medium | Host incompatibility, hallucinated calculations, state drift |
| **B. Files + targeted deterministic tools** | Medium; script/runtime must be installed | Higher for validated extraction, arithmetic, schema and consistency checks | Medium; dependencies and maintenance | High if scripts are inspectable and opt-in | Moderate | High | Parser edge cases, install friction, script errors |
| **C. Multi-agent/runtime platform** | Low-medium; orchestration, provider, and deployment coupling | Not inherently higher; needs additional coordination and end-to-end testing | Highest and variable | Lower unless explicit controls built | Slowest | High | Partial failures, hidden retries/cost, shared-source bias, state recovery complexity |

Select A, with only a narrowly scoped deterministic script if acceptance fixtures demonstrate a failure that A cannot safely handle. Do not include Docling, MarkItDown, Promptfoo, DeepEval, or a multi-agent runtime in the initial product merely because they exist.

## Proposed folder layout

```text
README.md
AGENTS.md                    # concise entrypoint, host-neutral where possible
skills/
  intake/SKILL.md
  evidence-research/SKILL.md
  options-decision/SKILL.md
  strategy-comms/SKILL.md
  experiment-design/SKILL.md
  resume-revise/SKILL.md
references/
  evidence-and-claims.md
  metric-definitions.md
schemas/
  case-state.schema.json
  evidence.schema.json
cases/<case-id>/
  brief.md
  evidence.md
  decision.md
  state.md
  sources/
scripts/                     # optional; only justified deterministic validation/calculation
```

Minimum run conditions: compatible file-reading/writing agent host; web access only if the case requires external sources; user-provided spreadsheet/PDF tools for those formats. No OMP, API provider, service, or parser package is a required dependency in this design. Host-specific permissions and capabilities must be documented; file-based instructions are not an OS sandbox.

## Workflow, human gates, degradation

`intake → plan → evidence → options → critique → decision → product+comms → experiment → state → resume/revise`

Mandatory human choice: clarify business constraints when missing; approve high-impact assumptions; select/authorize a recommended direction; approve external claims and experiments. If web access fails, proceed only with supplied/publicly cached evidence labeled accordingly. If a file cannot be parsed reliably, request an accessible excerpt or stop that analysis; do not silently infer its contents. If cost/host telemetry is unavailable, log **UNKNOWN**, not a fabricated estimate.

## Minimal record schemas

Examples are illustrative, not validated JSON Schema definitions.

```yaml
case_state:
  case_id: retention-demo
  stage: evidence
  updated_at: 2026-11-11
  next_action: obtain cohort definition
  open_questions: [Does the event definition change mid-period?]
  source_ids: [E-01]
  decision_status: pending-human-choice
```

```yaml
evidence:
  id: E-01
  source: https://example.org/report
  locator: "page 4, chart 2"
  accessed_at: 2026-11-11
  excerpt: "..."
  supports: [C-01]
  limitations: ["Aggregate data; no cohort breakdown"]
  freshness: "review-by: 2026-12-11"
```

```yaml
claim:
  id: C-01
  text: "Observed retention fell in the supplied period"
  type: observed
  evidence_ids: [E-01]
  confidence: medium
  status: documented
```

```yaml
assumption:
  id: A-01
  statement: "The event definition is stable"
  owner: human
  falsifier: "Event schema changed during the period"
  status: untested
```

```yaml
option:
  id: O-01
  mechanism: "Hold current experience; instrument cohorts"
  expected_benefit: "Reduce uncertainty before intervention"
  costs: ["Delay feature work"]
  objections: ["Does not immediately address a real decline"]
  assumptions: [A-01]
```

```yaml
strategy:
  audience_job: "Unknown pending evidence"
  product_direction: "Instrument and diagnose before prescribing"
  message: "Do not make a causal claim yet"
  proof_ids: [E-01]
  prohibited_promises: ["Guaranteed retention recovery"]
```

```yaml
decision:
  selected_option: O-01
  rationale_claims: [C-01]
  rejected_options: [O-02, O-03]
  human_approver: null
  review_trigger: "Validated cohort analysis or new causal evidence"
```

```yaml
experiment:
  hypothesis: "Variant X improves 30-day retained use"
  comparator: "Current experience"
  primary_metric: "Predefined eligible-user retention"
  guardrails: ["complaints", "uninstall rate"]
  window: "set after baseline and power analysis"
  threshold: "pre-register before launch"
```

```yaml
change_impact:
  new_evidence_ids: [E-02]
  invalidated_claim_ids: [C-01]
  affected_decisions: [decision-01]
  action: "re-evaluate; preserve prior version"
```

**Invalidation/freshness:** a new source never erases old evidence. Mark dependent claims stale when definitions, source versions, period, or population change; revisit linked options and decisions. A decision is revised only with an explicit reason and versioned record. “Retrieved at” does not imply “still true.”

# 7. AGENT DEBATE TRANSCRIPT SUMMARY

**Not conducted.** There are no A/B/C/D child session IDs, reports, or `agent://` transcripts. No cross-examination CLAIM IDs or fresh review exist.

Lead-only preliminary positions, not independent research:

- **A / product strategy:** start from the decision and outcome; separate observation, cause, and intervention; preserve status quo/stop alternatives.
- **B / communications:** every promise requires proof appropriate to its likely interpretation and a currently supported capability.
- **C / architecture:** files first; add parsers/calculators only for demonstrated acceptance gaps.
- **D / evaluation:** test on blind synthetic cases and hard negatives; check citation entailment and arithmetic, not citation presence alone.

A real council could change these positions. Outstanding dissent: file-only parsing and host-specific skill discovery are not proven sufficient for the eventual demonstration environment.

# 8. DESIGN DRY-RUNS

These are **synthetic design walkthroughs**, not executed agent results or company data.

## A. Synthetic retention decline

- **Input/unknowns:** an aggregate retention chart shows a decline; population, event definition, acquisition mix, release history, cohort windows, seasonality, and tracking changes are unknown.
- **Needed evidence:** event/metric definition and lineage; cohort-level data by acquisition/source/plan; release and campaign timeline; support themes; competitor/market context only if it can change the decision.
- **Options:** (1) status quo plus instrumentation/diagnosis; (2) targeted onboarding or service intervention if a segment-specific problem is established; (3) pause investment/close a segment if economics and strategic fit justify it.
- **Reproducible calculations:** retained users / eligible cohort by fixed interval; cohort-size and missingness checks; segment mix; uncertainty intervals or test design appropriate to available counts. A trend alone does not establish a cause.
- **Product/comms link:** do not promise “improved retention” publicly from an untested intervention. Explain the actual service change only if confirmed.
- **Decision now:** request cohort and instrumentation evidence; preserve alternative interventions. **Requires test:** causal impact of a product change.
- **New-chat state:** metric definitions, supplied data references, queries performed, exclusions, unresolved schema changes, options, next action.
- **Plausible error:** Simpson’s paradox or event-definition change mistaken for product deterioration. **Eval checks:** aggregate-vs-segment inconsistency; missing-period fixture; altered event definition; arithmetic fixture.

## B. Synthetic new digital service

- **Input/unknowns:** service concept is vague; target segment, job, price, distribution, costs, capability, and competitor choice are unknown.
- **Needed evidence:** public competitor product/pricing/terms pages; credible market estimates with definitions; direct discovery interviews or tests (not available from public pages); proposed delivery cost and internal capability supplied by user.
- **Options:** (1) do nothing/continue status quo; (2) narrow prototype/probe for one audience/job; (3) broader launch only if capability, economics, and demand evidence clear; (4) stop if the job or viable delivery case fails.
- **Reproducible calculations:** bottom-up reachable audience × eligible conversion × price, with sourced inputs/ranges; contribution per customer after variable costs; sensitivity to conversion and churn. Do not fabricate market share or willingness to pay.
- **Product/comms link:** promise only currently available capability and evidenced outcomes. Label future roadmap features clearly; avoid implying availability or performance.
- **Decision now:** select a low-cost learning test and specify falsification. **Requires test:** real conversion, willingness to pay, retention, and support burden.
- **New-chat state:** customer/problem hypotheses, public source URLs and timestamps, cost assumptions, option tradeoffs, experiment decision rules.
- **Plausible error:** competitor feature page interpreted as customer demand; optimistic conversion compounded into false TAM. **Eval checks:** public facts vs inference labeling; sensitivity arithmetic; absent pricing case; unsupported communications promise.

# 9. EVAL + BASELINE PLAN

No scores have been measured. Compare the proposed agent with **plain chat** and **structured chat using the same model, brief, permitted sources, time limit, and user inputs**. Randomize order; use blinded reviewers and a fixed rubric. Log elapsed time, observed tool calls, human minutes, model/search costs when observable, retries, and unresolved work. Repeat prompts where variability matters. Evaluators should not see which system produced an answer.

| Fixture | Required checks | Hard failure |
|---|---|---|
| 1. Retention decline, aggregate only | Clarify denominator/period; distinguish correlation from cause; present status quo and 2 different options | Claims a cause or intervention effect as fact |
| 2. Cohort mix shifts | Segment calculations and aggregation caveat | Misstates aggregate change as within-cohort change |
| 3. Spreadsheet with missing cells/units | Missingness, units, formulas, independent recomputation | Silent imputation or incorrect arithmetic |
| 4. Multi-page PDF with table | Page/table locator and extraction uncertainty | Cites wrong page/value as direct evidence |
| 5. Conflicting public sources | Version/date/context comparison and preserved contradiction | Silently chooses one source |
| 6. New-service launch with no demand data | Alternatives, uncertainty, test, product/comms consistency | Presents demand or willingness to pay as fact |
| 7. Malicious instructions embedded in a source | Treat source text as data; no policy/tool changes | Follows embedded instructions |
| 8. Resume in new chat | Reconstruct stage/decision/evidence from files; avoid duplicate work | Loses unresolved state or claims prior work without record |
| 9. New evidence contradicts a premise | Identify dependent claims/options/decision; preserve history | Updates conclusion without change-impact trail |
| 10. Unsupported numeric claim or marketing promise | Reject/qualify unless evidence supports exact wording | False “verified,” invented calculation, unsupported promise |

Metrics: requirement coverage; factual claim precision/entailment; source-locator correctness; fact/hypothesis separation; calculation accuracy; distinctness and objection quality of options; product/comms inconsistency rate; experiment completeness; resume/change-impact correctness; human intervention; time/cost. Hard failures should not be averaged away by prose quality.

Promptfoo and DeepEval are possible later references, not dependencies selected now. Both require implementation/evaluation choices; LLM-as-judge should supplement—not replace—human adjudication and deterministic checks. [S12, S13]

# 10. IMPLEMENTATION ROADMAP

Planning proposal to the stated November 22, 2026 deadline; not evidence of available engineering capacity.

| Timing | Scope | Observable DONE | Depends on |
|---|---|---|---|
| Day 1: first vertical slice | One synthetic retention case; intake, evidence ledger, three options, decision, checkpoint; no external dependencies | A fresh host session follows the files and produces traceable artifacts; human choices visible | Confirmed host and acceptance fixture |
| Day 2: eval-driven correction | Run fixtures 1–3 and 6 against plain/structured-chat baselines; fix observed material failures | Blind rubric and deterministic arithmetic checks show failure cases and corrections; no invented scores | Frozen fixture/rubric |
| Next: source and document handling | Test website, PDF, spreadsheet on public/synthetic inputs; add only necessary converter/calculator | Every material extracted value points to a locator; formulas independently recompute; uncertainty exposed | Target host and document fixtures |
| Next: state and change impact | New-chat resume and contradicted-source fixture | Resume and invalidation gates pass with versioned state | State schema |
| Next: portability | Test same folder in at least two permitted target environments if practical | Documented differences and successful core workflow in each claimed host | Host availability |
| After official demo brief | Build one public-data demo case; map every brief requirement to evidence and a test | No internal company data; all claims and sources auditable | Organizer’s additional brief |
| Final: video/report/buffer | Record ≤10-minute end-to-end run including pause/resume; document tools, model, cost, errors, human help, limitations | Replayable project and submission checklist complete | Acceptance gates closed |

Do not build an orchestration server, custom database, broad document-conversion stack, mandatory MCP integration, large skill catalog, or multi-agent council into the product without a demonstrated requirement.

# 11. SOURCE REGISTER

Checked November 11, 2026. Moving `main` branch links are not commit-pinned; claims about current repo metadata reflect the fetched pages.

- **S1 — Agent Skills specification**, [agentskills.io/specification](https://agentskills.io/specification). Format fields, directory structure, progressive disclosure, and validation guidance. **DOCUMENTED**. Does not guarantee every host implements the format.
- **S2 — Agent Skills repository**, [github.com/agentskills/agentskills](https://github.com/agentskills/agentskills), README/LICENSE and repository metadata. Repo reports Apache-2.0 code and CC-BY-4.0 docs. **DOCUMENTED**. Repo metadata not a runtime test.
- **S3 — SVPG, “Empowered Product Teams”**, [svpg.com/empowered-product-teams](https://www.svpg.com/empowered-product-teams/), published 2018-10-31, modified 2023-08-27; sections on discovery, strategy, teams. Supports problem/outcome framing and value/usability/feasibility/viability as practitioner model. **DOCUMENTED**. Not independent causal evaluation.
- **S4 — FTC, “Policy Statement Regarding Advertising Substantiation”**, [ftc.gov/legal-library/...](https://www.ftc.gov/legal-library/browse/ftc-policy-statement-regarding-advertising-substantiation), dated 1984-11-23. Supports prior reasonable basis for objective express/implied US advertising claims. **DOCUMENTED**. Jurisdiction-specific; not a substitute for local legal review.
- **S5 — Product Manager Skills**, [repository](https://github.com/deanpeters/Product-Manager-Skills), `skills/product-strategy-session/SKILL.md`; repo reports “Other” license and README states CC BY-NC-SA 4.0. Workflow includes positioning, discovery, solution exploration, prioritization, stakeholder alignment. **DOCUMENTED**. Author’s “battle-tested” claims are **CLAIMED**; avoid copying absent license resolution.
- **S6 — Product Manager Copilot**, [repository](https://github.com/julianoczkowski/product-manager), `skills/pm-copilot/SKILL.md`, MIT. Router reads shared framework/journey, directs to stage skills, produces artifacts. **DOCUMENTED**. Declares write/edit/bash tools and is framework-specific.
- **S7 — Multi-Agent Market Research**, [repository](https://github.com/wasifrepo/multi-agent-market-research), MIT; `agents/skeptic_reviewer.py`, `core/models.py`. Citation-presence gate, one contradiction rule, typed citation/source fields observed in source. **DOCUMENTED**. Gate can pass unsupported-but-cited claims.
- **S8 — GPT Researcher**, [repository](https://github.com/assafelovic/gpt-researcher), Apache-2.0 per repo page. README describes planner/executor research and API/service setup. **CLAIMED** for performance; this run did not inspect implementation.
- **S9 — STORM**, [repository](https://github.com/stanford-oval/storm), MIT; `knowledge_storm/storm_wiki/modules/knowledge_curation.py`. Observed bounded simulated question loop, query generation, retrieval, and response assembly. **DOCUMENTED**. The code itself includes a “top 1 snippet” simplification; not a citation-accuracy guarantee.
- **S10 — MarkItDown**, [repository](https://github.com/microsoft/markitdown), MIT; `packages/markitdown/src/markitdown/converters/_pdf_converter.py`. Source includes PDF table extraction and layout heuristics. README states multiple format support, optional dependencies, and process-privilege warning. **DOCUMENTED**. Conversion fidelity not tested here.
- **S11 — Docling**, [repository](https://github.com/docling-project/docling), MIT per repo/README; repo README describes PDF layout/table/OCR support and notes individual model licenses. **CLAIMED** capabilities; targeted example URL was unavailable (404), no implementation inspected.
- **S12 — Promptfoo**, [repository](https://github.com/promptfoo/promptfoo), MIT per repo. README describes eval and red-team CLI; specific requested example path was unavailable (404), no implementation inspected. **CLAIMED**.
- **S13 — DeepEval**, [repository](https://github.com/confident-ai/deepeval), Apache-2.0 per repo. README lists LLM-judge and other metrics; no metric implementation inspected. **CLAIMED**.

# 12. UNKNOWNS / BLOCKERS / NEXT DECISIONS

1. **Independent council and review:** blocked pending a project-approved PASS scout smoke and actual child-runtime inventory. No session IDs exist. Do not treat this lead synthesis as independent cross-examination.
2. **Depth targets:** 15 primary sources, 8 inspected code/example/license locations, and independent initial positions/revisions remain incomplete. Current evidence does not justify FULL status.
3. **Demo brief/provenance:** organizer-side verification and additional demo brief are **UNKNOWN**. Obtain the published brief, preserve the original unchanged, and record source/version/hash before final requirement mapping.
4. **Target host:** exact host, supported skill format, file/web tools, spreadsheet/PDF behavior, route, and cost telemetry remain **UNKNOWN**. Do not claim portability or runtime success until tested.
5. **Legal and data constraints:** FTC source is US-specific. Confirm applicable jurisdiction and privacy/advertising requirements before implementation or publication.
6. **Next concrete decision:** qualify one read-only scout using the project’s documented procedure in a separate authorized run. Then conduct A/B/C independent research, D afterward, cross-examination, and a fresh review. Until then, use this architecture and eval plan as hypotheses, not accepted research findings.
