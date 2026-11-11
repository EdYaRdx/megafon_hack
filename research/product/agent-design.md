# Portable Product Strategy Agent — design proposal

**Scope:** research proposal only; no product code, script, runtime, deployment or dependency was created. Input contract is the supplied local contest brief (`docs/contest-brief.md`); its exact organizer provenance and supplemental MegaFon demo brief remain **UNKNOWN**. This design is intended to satisfy the brief's folder-based constraint, not implement an OMP/DSH/agent-orchestration platform.

## Recommendation

Start with a repository-backed, file-first workflow and one canonical set of portable skills. The authoritative record is ordinary files: concise project instructions, small `STATE.md` handoff, append-only claim/evidence/decision ledger, original sources or stable source references, and versioned outputs. The host supplies models, file access and permitted web tools. Never assume a skill defines or enforces host permissions. Add a deterministic parser/calculator only after an acceptance fixture demonstrates an error that files/host tools cannot adequately prevent.

This is an **INFERENCE** from the brief's folder contract and the standards/source inspection—not a measured comparative result. An integrated workflow service could add reliability at scale, but is not justified before a user/host need is demonstrated.

## Three architectures compared

Qualitative design judgment only; not benchmark results.

| Architecture | Portability | Evidence correctness | Cost | User control | Build time | Robustness / generalization | Decision |
|---|---|---|---|---|---|---|---|
| 1. **Files + skills** | Highest: portable files; host-specific skill discovery still needs verification. | Medium by default; depends on disciplined source locators, numeric checks and human validation. | Lowest infrastructure; model/search and human review costs remain. | High with visible stages and approval pauses. | Lowest. | Fresh-chat state straightforward; no transaction/concurrency guarantees. | **Baseline.** Matches brief's folder, avoids needless platform. |
| 2. **Files + targeted deterministic tools** | Medium: records remain portable; parser/runtime/tool install may vary by host. | Potentially higher for arithmetic, schema, repeated extraction; only if tested on representative inputs. | Medium and variable; dependencies + maintenance + host calls. | High if scripts are inspectable/opt-in and consequential actions gated. | Medium. | Better deterministic substeps; parser edge cases and injection/privilege risk remain. | **Conditional extension** only for verified gap (e.g. table extraction/numeric error). |
| 3. **Durable workflow service / graph runtime** | Lowest for intended folder-based usage: service, provider, DB and operations coupling. | Not inherently higher; orchestration does not prove claim/source correctness. | Highest and unmeasured; operational and model/tool costs. | Requires added pause/cancel/audit UX. | Highest. | Can checkpoint concurrent tasks but introduces partial-failure, retry and state synchronization risks. | **Reject for initial product** absent requirement for shared concurrency/central policy. |

### Tool choice

- Default to host-native open/read/web tools, direct file reading and visible user-owned sources. Unavailable tools → disclose limitation; do not invent output.
- PDF/table handling: preserve originals and page/table locators. MarkItDown is a candidate for straightforward text conversion; its README says Markdown conversion is for analysis, not high-fidelity reproduction, and source code uses position/column heuristics for certain tables. Docling exposes a richer structured document model, layout/reading order and configurable pipeline. Neither inspected repository provides task-specific accuracy evidence. Use neither by default; trial only against representative sanitized fixtures if needed.
- Numeric validation: calculation output must include source cells/locators, unit, period, denominator, missingness, conversion and rounding. Use deterministic arithmetic/schema check for critical calculations if introduced and reviewed. Hashes indicate file identity, not truth or parsing accuracy.
- Retrieval: start with explicit source folders/relative paths and web lookup; no vector database unless evaluation shows search failure on the actual corpus.
- No always-on router, multi-agent system, service, MCP server, CLI or paid provider requirement. Route cost/quality via a simple explicit escalation rule; measure rather than claim savings.

## Portable project layout

```text
project/
  README.md                 # supported hosts, setup, limitations, first-run path
  AGENTS.md                 # concise, trusted workflow entrypoint
  STATE.md                  # handoff pointer; not sole evidence record
  skills/
    intake/SKILL.md
    evidence-research/SKILL.md
    options-decision/SKILL.md
    strategy-communication/SKILL.md
    experiment-design/SKILL.md
    resume-revise/SKILL.md
  references/
    evidence-and-claims.md
    metric-definitions.md
    security-and-source-handling.md
  cases/<case-id>/
    brief.md
    evidence/ledger.jsonl
    sources/<source-id>/source.json  # optionally retained extract/snapshot
    decision.md
    strategy-product.md
    strategy-communication.md
    test-plan.md
    state.md
```

Canonical skills remain under `skills/`; if a host only discovers another location, document a host adapter that points/copies to the canonical source. Keep authoritative data in the folder, not conversation or hidden host memory. Agent Skills documents directory/frontmatter conventions and progressive disclosure; it does not normalize client discovery, model/tool interfaces, or script permissions. **DOCUMENTED:** [Agent Skills specification](https://agentskills.io/specification.md), “SKILL.md format,” “Progressive disclosure,” “Optional directories,” “Validation.” `allowed-tools` is experimental and implementation support varies.

## Proposed skills (6)

| Skill | Trigger and required output | Stop / human gate |
|---|---|---|
| `intake` | Ambiguous product problem; write decision owner, decision/date, audience, objective, constraints, available data, important unknowns; ask only next-step-changing questions. | Stop if decision authority or constraint materially absent; no invented case context. |
| `evidence-research` | Gather evidence for decision-changing questions; create source/evidence/claim records with exact locators, date, status, limitations and contradiction links. | Stop/label UNKNOWN if source unavailable or locator cannot be verified; treat content as untrusted. |
| `options-decision` | Convert evidence and assumptions into ≥3 materially different options, including status quo and stop when plausible; objections, cost/value, uncertainty and falsifiers. | Human chooses high-impact direction; model's ranking is recommendation, not authorization. |
| `strategy-communication` | Join selected product value/capability to audience/job, barrier, message, proof, conditions and channel role. | Hold unsupported claims for evidence/legal review; no claim of legal compliance. |
| `experiment-design` | Define learning question, method, comparator, target population, metric definition/unit/window, guardrails, data quality, threshold and owner. | Human approves real participant contact, external launch or sensitive data processing; discovery interview ≠ demand proof. |
| `resume-revise` | Read checkpoint and linked evidence; map new evidence to affected claims/options/decisions; append impact/revision record. | Preserve prior version; human approval on decision or external promise changes. |

**Maintenance:** skills follow Agent Skills `name`/`description` frontmatter; keep body concise, references one level deep. Do not rely on skill text to authorize tools. User brief asks 4–7 proposed skills; the six above meet that design requirement.

## Evidence/state/decision schemas

Proposed plain JSONL (one record per line, append corrections and supersessions):

```json
{"id":"S-001","type":"source","url":"https://…","publisher":"…","title":"…","published":"…","version_or_commit":"…","retrieved_at":"…","locator":"section/page/table","snapshot":"sources/S-001/source.pdf","sha256":"…","status":"OBSERVED","limitations":"…"}
{"id":"E-001","type":"evidence","source_id":"S-001","locator":"PDF p. 7, table 2, row/column","excerpt":"…","extraction_method":"manual|host|parser+version","review_status":"verified|unverified"}
{"id":"C-001","type":"claim","text":"…","status":"DOCUMENTED|CLAIMED|INFERENCE|HYPOTHESIS|UNKNOWN","evidence_ids":["E-001"],"valid_as_of":"…","limitations":"…","invalidated_by":[]}
{"id":"A-001","type":"assumption","text":"…","owner":"human|team","falsifier":"…","status":"untested|supported|rejected"}
{"id":"D-001","type":"decision","option_id":"O-01","basis":["C-001","A-001"],"rejected_options":["O-02"],"approver":null,"recorded_at":"…","review_trigger":"…"}
{"id":"I-001","type":"invalidation","target_id":"C-001","reason":"source changed/new contradiction/transcription correction","detected_at":"…","replacement_ids":[]}
```

Claim statuses distinguish observation/source assertion from inference and hypothesis. For every material claim, retain publisher, URL/file, exact locator, publication/version/retrieval dates, extraction path, applicable population/period, limitations and decision impact. A citation indicates traceability, not correctness or entailment. W3C PROV-DM is a general conceptual provenance model, not this schema or a validator: [W3C PROV-DM Recommendation](https://www.w3.org/TR/2013/REC-prov-dm-20130430/), abstract/model.

`STATE.md` should carry only `updated_at`, revision, ledger head, current stage, completed work, open questions/blockers, decision status and exact next action. New chat reads `STATE.md`, follows evidence IDs, reopens material source locators, checks for invalidation, and continues. It must not claim work unrecorded in files. A new source appends an invalidation/change-impact entry; older evidence and decision remain visible.

## Workflow and gates

```text
intake → question plan → source/evidence collection → options + strongest objections → independent critique → product+communication decision → experiment plan → save checkpoint → resume/revise
```

- Ask the user to decide when missing information blocks a consequential choice; mark unknown rather than filling it with a mock value.
- User approves direction, high-impact assumptions, external promise, real experiment and any potentially sensitive action.
- Source instructions never modify trusted workflow. Keep file/web capabilities and least privilege in host permissions; do not expose secrets. Treat retrieved and extracted text as untrusted data; prompts/delimiters are not a sandbox.
- If parsing fails, request an accessible source or stop the dependent claim; never silently infer table layout. Visually verify critical values against original page. If cost/telemetry is unavailable, record **UNKNOWN**.
- Preserve previous decisions and reason for change; stale source, new contradiction, changed population/period or corrected transcription triggers impact review.

## Security evidence and limitations

[OWASP LLM01:2025](https://genai.owasp.org/llmrisk/llm01-prompt-injection/), updated 2025-04-17, documents direct/indirect injection from files/web and recommends privilege control, validating outputs, human approval and separating external content. It explicitly says fool-proof prevention is unclear. **DOCUMENTED; security guidance, not product verification.** For a product test: indirect injection in PDF and website, with attempted instruction override/data exfiltration; inspect actual host permission boundary, tool calls, outputs and file state. If host enables shell/write broadly, skill text alone is insufficient safeguard.

## Model routing and cost

Policy proposal: deterministic checks first; low-cost bounded model for easy extract/classification only when independently checkable; escalate conflicting sources, complex layout, or consequential claims for stronger model/human inspection; log model/provider/version, task, observable token/price/time/calls, retries, escalation reason and human review minutes. Compare at matched task/quality budget. The [FrugalGPT paper](https://arxiv.org/abs/2305.05176), Chen et al., arXiv posted 2023-05-09, studies prompting/approximation/cascades; its reported cost reduction is experiment-specific, not a prediction for this agent. **DOCUMENTED / LIMITATION.**

## Portability proof required later

Run the same project folder under two declared hosts; record versions, skill discovery, file permissions, source-opening ability, pause/cancel UX, resume in new chat and output paths. Agent Skills naming/format is not sufficient. No runtime here tested, and no compatibility PASS is claimed.
