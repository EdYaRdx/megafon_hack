# Repository architecture inventory and decisions

## Audit scope and observed baseline

Audit run for repository productization on the current branch at `7fd1ae68cd597c5a046de568d336f39791f25855`. The worktree was clean at inspection. Branch: `release/product-repository-20261114`; its upstream is not configured yet. `origin/main` is `7bbe59d37d4c1e13f0fd4453f7605e8d2f601d42`; the requested release branch was not present on origin before this work. No file moves or deletions are needed to reach the selected structure.

The tracked tree contains six canonical Skills, three reference documents, 137 case files, 14 documentation files, six prompt files, 136 research files, eight `.omp/` files, and root instructions/entrypoints. Counts are inventory observations, not quality or test results. The user-local `.omp/profiles/product-build.yml` was not read. No credentials, session dumps, private configuration, or raw OMP transcripts were opened.

Reviewed product contracts include the root `AGENTS.md`, all six Skill files, reference docs, template files and its revision/approval protocol, current example and case index, README/Quick Start/first-run prompt, research and audit indexes, repository ignore rules, root research launchers, relevant repository history and published Sol audit findings. Case inventory and published findings establish that examples are synthetic/QA/historical; they do not establish product-wide dynamic behavior.

## Keep / improve / archive / remove decisions

| Section | Decision | Evidence and rationale |
|---|---|---|
| `AGENTS.md`, `.agents/skills/` | **KEEP** | One canonical procedure for each of six workflow stages; root routing and evidence/approval boundaries are useful product contracts. No duplication or dependency on OMP. |
| `references/` | **KEEP** | Reusable source, evidence, metric and safety procedures; complements rather than duplicates the workflow Skills. |
| `cases/_template/` | **KEEP / IMPROVE** | It contains JSONL ledgers, state, immutable manifest/checkpoint selector and separate approvals. Improve discoverability via the new development guide; do not change historical semantics. |
| `cases/meal-planner-demo/` | **KEEP** | Most complete recommended synthetic example; limits and non-real evidence are explicitly documented. |
| Other `cases/` | **KEEP / LABEL** | QA fixtures, incomplete legacy case and historical synthetic outputs have audit/evaluation value. `cases/README.md` classifies them; age or incompleteness alone is not a deletion reason. |
| `docs/` | **IMPROVE** | Existing Quick Start, evaluation and status are useful, but architecture was only a pointer to another architecture file and the doc index omitted developer workflow. Make `architecture.md` canonical, retain the old path as a compatibility pointer, and add a developer guide/index. |
| `research/` | **ARCHIVE IN PLACE** | Dated research, audit decisions and negative results preserve evidence and provenance. `research/README.md` marks them historical/non-runtime and links current status. Do not edit reports retroactively. |
| `MGIMO_RESEARCH_TO_IMPLEMENTATION.md` | **ARCHIVE IN PLACE** | Historical rationale with its own origin history and no current user-facing setup role. Preserve provenance; the canonical current architecture is `docs/architecture.md`. |
| `prompts/overnight-*` | **ARCHIVE IN PLACE** | Research task prompts are not product workflow. They have historical links and research context; `prompts/first-run.md` remains the only onboarding prompt. |
| `START-OVERNIGHT-V3.txt`, `start-overnight-product-research-v3.cmd`, `.omp/` | **ARCHIVE IN PLACE** | Launcher references its OMP/config and repository path assumptions; history traces launcher files to the old research entrypoint. README and research index explicitly say not to use it for product setup. Moving/removing would risk historical reproducibility and provides no runtime benefit. Do not inspect private profile contents. |
| `START-HERE.txt` | **KEEP / LABEL** | Plain-text entrypoint is useful outside Markdown renderers; it is secondary to README and should point to Quick Start, not OMP research. |
| `docs/next-session-handoff.md`, `docs/research-plan.md`, `docs/release/` | **ARCHIVE IN PLACE** | Historical operations, initial plans, and release evidence contain old scopes/SHA and must not be silently rewritten. Index them as historical; current acceptance state remains in implementation-status/evaluation. |
| `.gitignore`, `.gitattributes` | **KEEP** | Ignore policy covers common credentials, private sessions, local state and generated files. It is not an allowlist or complete privacy scanner; use scoped review before publication. No ignore-policy change justified. |
| Redundant or unsupported files | **REMOVE: none** | No file was confirmed dead or without evidence/dependency value. Avoid speculative pruning. |

## Before / after information architecture

**Before:** product core at root (`AGENTS.md`, Skills, references, cases and prompts); `docs/` held useful pages but `architecture.md` was a short pointer while `submission-architecture.md` held the actual architecture. Research/audits and old OMP launchers were interspersed at root but already partly labelled. The developer/testing path and the distinction between product integrity checks and harness defects were not one navigable page.

**After (no moves):**

```text
README.md                  product overview and primary entrypoint
AGENTS.md                  product workflow contract
.agents/skills/            six canonical procedures
references/                reusable evidence/metric/safety methods
cases/
  _template/               new-case format and persistence contract
  meal-planner-demo/        recommended synthetic walkthrough
  <other cases>/           labeled historical cases and QA fixtures
prompts/first-run.md       first-case prompt
docs/
  quickstart.md             first actual workflow
  architecture.md           canonical system/data/revision architecture
  development.md            changes, evidence, compatibility, checks, review/release
  evaluation.md             evidence and technical-debt boundaries
  implementation-status.md  current acceptance snapshot
  submission-*.md           contest working contract and open gates
  repository-inventory.md   architecture choices and audit record
research/                  indexed historical evidence and audits
tools/check_repository.py  standard-library/Git repository-harness check
.omp/, START-OVERNIGHT*,    retained development/research history, not runtime
```

## Alternatives considered

1. **Leave the flat presentation as-is:** lowest path risk, but product docs remain harder to navigate and architecture authority remains split.
2. **Move product to a new subtree/repository and research to an archive:** clearer physical separation, but costly path changes and broken historical locators with no current execution need.
3. **Selected: stable product core plus explicit docs navigation and labeled history:** minimal path churn; architecture and development become findable while preserving historical evidence and portability.

## Technical assessment

**Strengths:** file-first and host-independent product data model; separations among instructions, methods, and case data; one canonical Skill per stage; explicit source/evidence/claim chain; alternatives and human gates; immutable revision manifests with explicit active claims; carefully separated approval scope; existing synthetic examples and audit artifacts.

**Confirmed organizational defects addressed:** the canonical architecture page was not substantive; `submission-architecture.md` was the actual spec, creating split authority. Developer changes, schema compatibility, checker scope and release procedure lacked a central guide. Research, OMP and legacy launchers required explicit archive labeling. No product contract, output or audit record was changed by this reorganization.

**Known product/harness debt:** F1–F5 targeted results are not accepted due to harness/checker defects; F6 has provenance limits; H02 is blocked; latest independent Sol acceptance sign-off is pending. The static Sol audit identifies bounded product/methodology findings and process/contest gates in its own scope; consult its [final verdict](../research/audits/sol-preprod-2026-11-14/final-verdict.md), [technical findings](../research/audits/sol-preprod-2026-11-14/technical-findings.md), and [product review](../research/audits/sol-preprod-2026-11-14/product-review.md). Those reports are not a current dynamic pass or release certification.

**Unverified:** host Skill discovery/adherence, clean-host workflow, cross-host portability, arbitrary crash recovery, complete provenance for prior sessions, full security properties, real user need/economics, and official MegaFon demo brief. No dynamic or H02 run was performed for this repository task.

**Unnecessary complexity rejected:** backend/database/UI/MCP/orchestrator, OMP runtime, package dependencies, CI badges and a second test framework. A single standard-library script is justified to catch malformed case JSON/JSONL and broken relative links in the product-facing docs without implying product acceptance.

## GitHub presentation

Suggested About description: **“A file-based product strategy AI agent for evidence-linked decisions, strategy, validation, and revision.”**

Suggested topics: `product-strategy`, `ai-agent`, `coding-assistant`, `decision-support`, `evidence-based`, `file-based`.

Repository About metadata was not changed; this task did not need to alter owner-controlled settings. No badges are warranted without working CI.
