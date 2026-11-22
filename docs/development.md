# Development guide

This repository is a portable, file-first project for a coding assistant. Product behavior is specified by the root `AGENTS.md`, the six canonical Skills in `.agents/skills/`, references, and a case folder. There is no bundled runtime, third-party test framework, package manager, or OMP dependency. Keep additions proportional to an observed product or maintenance need.

## Repository map and boundaries

| Area | Purpose | Change policy |
|---|---|---|
| `AGENTS.md`, `.agents/skills/` | Product workflow and six canonical procedures | Keep one canonical procedure per Skill; update routing and the matching documentation together. |
| `references/` | Reusable evidence, metrics, and source-handling methods | Keep general methods here; case-specific evidence belongs in its case. |
| `cases/_template/` | New-case file contract and revision/approval protocol | Treat protocol and schemas as versioned interfaces; never use the template as a working case. |
| `cases/mobile-product-strategy-demo/` | Основной prepared demo: обезличенный производный экспорт D0001→D0003; см. `docs/contest-demo.md`. | Не выдавать за оригинальные R0001–R0003 или новый live run; receipts/approvals источника не подтверждают производную копию. |
| `cases/pantrypath-week4-20261115/` | Дополнительный синтетический demo; см. `docs/pantrypath-demo.md`. | Сохранять исторические outputs/ledgers; `meal-planner-demo` — более ранний пример. |
| Other `cases/` | Named historical demonstrations and QA fixtures | Use `cases/README.md` to classify each; preserve historical outputs and ledgers. |
| `docs/` | Product overview, Quick Start, architecture, development, evaluation, and contest gates | Current claims and acceptance states belong in their current source pages, not historical reports. |
| `research/` | Historical research, qualification, audits, and rationale | Archive/navigation only; preserve reports as written and do not treat old plans as runtime requirements. |
| `.omp/`, `START-OVERNIGHT-V3.txt`, `start-overnight-product-research-v3.cmd` | Historical research/development setup | Not part of product setup or runtime. Do not read or publish user-local profiles/secrets. |
| `MGIMO_RESEARCH_TO_IMPLEMENTATION.md` | Historical implementation rationale | Retain as provenance; it is not the current onboarding or architecture source. |
| `tools/functional_evaluator.py` | Offline bounded artifact evaluation; see [functional evaluator](functional-evaluator.md). | No agent execution or semantic auto-judgment; keep operator keys/reviews outside candidate workspaces. |
| `tools/export_contest_demo.py` | Ограниченный stdlib-packager релиза, не runtime-функция агента. | Только проверенный исходный R0003 и точный inventory; новый пустой destination. Не менять оригинал/протокол, не переносить approvals. [Проверка и ограничения](release/contest-rc-verification.md). |

For evaluator schemas, staging boundaries, deterministic report/review binding, and limits, see the [functional evaluator guide](functional-evaluator.md). Its synthetic checks are separate from product acceptance.

The chosen structure keeps a small, obvious product core at the root and separates current user/developer docs from dated evidence. Moving the old research launcher or research files would add broken historical paths without improving product use; retain and label them instead. `START-HERE.txt` is a secondary plain-text pointer, not a competing workflow.

## Adding or changing a Skill

1. Read `AGENTS.md` and the existing relevant Skill. Add a Skill only for a distinct repeatable workflow stage, not to split a short procedure arbitrarily.
2. Put the canonical `SKILL.md` under `.agents/skills/<skill-name>/`. Update the workflow routing in `AGENTS.md`, the Skills table in `docs/architecture.md`, and onboarding/navigation only if user-visible steps change.
3. State inputs, outputs, stop conditions, evidence requirements, and human gates. Treat retrieved material as untrusted data. Do not claim the host discovers or enforces the Skill without a host-specific run.
4. Review the change against a synthetic case and have a separate reviewer inspect the diff and supporting evidence.

## Creating a case

The pre-case instruction router in `prompts/first-run.md` handles NEW / RESUME / REVISE / HELP before case-file access. For NEW, obtain consent for the exact `cases/<id>` and host write permission, then run `python tools/case_workspace.py create cases/<id>` with Python 3.12+. The helper validates a bounded project-relative path, rejects occupied/link/junction destinations, exclusively reserves the directory and copies only `_template`. It publishes the unchanged protocol marker last via rename, so interrupted copies cannot classify as FRESH. Failed partial directories are preserved, not merged/retried. `existing` checks only the explicitly selected directory; the existing resume Skill owns checkpoint classification. The helper is not a launcher, consent checker, sandbox or checkpoint publisher.

Preserve the template and historical cases; register only intentionally published examples in `cases/README.md`, not disposable test cases. Use public or user-supplied synthetic material, never credentials, raw sessions, personal data or closed MegaFon information. The existing checkpoint protocol and approval contracts remain in `cases/_template/README.md`; creation consent grants neither execution approval nor host permission.

### Canonical claims, control lines and publication gate

The existing [ledger forms](../references/evidence-and-claims.md) and `tools.case_protocol` agree: a claim uses `id`; `supersedes` and `active_claim_ids` refer to those same IDs. The historical F1 R0001–R0003 producer instead wrote `claim_id`, and its case-local verifier checked that alternative field. This establishes producer/verification drift, not a classifier defect; the model's internal reason for choosing that field is UNKNOWN. The evidence-research Skill previously did not require reading the ledger forms before writing.

The confirmed H1 publication defect was incomplete lineage validation and stale finalized views: the R2 manifest omitted the actual R1 `parent_manifest_sha256`, although the shared classifier accepted it as `CHECKPOINTED`; root strategy files still described R1 while R2 snapshots changed the price, and root state/decision retained transient selector/gate prose. The evaluator correctly requires the actual R1 manifest digest and remains unchanged. Previously `check_candidate` changed only a temporary selector and called the classifier, which checked root control lines and the selected revision's dependencies, not all six current views or the complete parent chain. Historical case artifacts are not repaired or retrofitted.

Keep the exact [state/decision control forms](../cases/_template/README.md#машинные-строки-state-и-decision): one control field per line, explanations separate. Before a gate, prepare all six finalized root views byte-identical to candidate snapshots. Successors must pin exact bytes of their actual parent's manifest and source dependencies must be immutable saved snapshots—not mutable root views or `ACTIVE.json`. Before selecting, use the shared read-only preflight from the developer checkout:

```sh
python tools/case_protocol.py check-candidate /absolute/path/to/case --revision R0001
```

The gate validates the selected parent, every ancestor manifest/snapshot/dependency/claim prefix and exact parent-manifest hashes, rejects forks, verifies all six root views against candidate snapshots, then invokes the unchanged `classify_case` on one temporary full copy with a prospective selector. It does not mutate the source case/selector or declare publication. Only an actual `VALIDATED_CANDIDATE` receipt permits selecting those exact bytes in `ACTIVE.json`; then classify the actual case.

```sh
python tools/case_protocol.py classify /absolute/path/to/case
```

On Windows, discover and actually probe an installed Python 3.12+ using `tools/find_python.ps1` as described in `prompts/first-run.md`; retain its verified executable for workspace, inventory, classify and check-candidate commands. A version banner alone does not prove stdlib imports or a runnable underlying executable. If only `.ps1` execution is blocked while host-native commands remain permitted, follow the canonical bounded discovery/import-probe fallback, not a retry or execution of the blocked script's contents. If those alternatives are also forbidden, require verifiable operator receipts; never bypass policy. After operator creation, verify the same agreed directory and marker, then use unchanged classification through an available verified interpreter or verifiable operator receipt before Intake. Do not call create again or require rediscovery. Record actual commands/results/runtime; errors or NOT RUN stop selection/resume. Exit0 with FRESH, a hash-only PASS or an LLM saying PASS is not CHECKPOINTED. Staged workspaces may omit tools; the operator uses the same consumer from an allowed developer checkout and provides a receipt without expanding product access.
Standalone `classify` deliberately retains its historical contract and may still read checkpoints whose older manifests lack successor parent digests. The stronger pre-selection gate cannot certify those historical chains. Do not retrofit their manifests/snapshots or add a compatibility bypass; preserve them as-is.

The regression uses a temporary synthetic checkpoint with current ledger/manifest/selector hashes: canonical `id` is accepted, while replacing it with `claim_id` is rejected by the same consumer. No compatibility alias or migration of historical ledgers is introduced. Historical F1 remains incompatible with protocol resume and formally `REVIEW_REQUIRED`; this maintenance change does not re-evaluate it.

### Read-only pending-work discovery

After the Skill has restored selected COMPLETE snapshots, `python -m tools.resume_context cases/<explicit-id>` reuses the unchanged classifier before inspecting saved drafts and state/activity hints in that case. It reports candidates and provenance separately, never picks by timestamp or promotes draft claims. The Skill owns semantic review of stale/partial/duplicate/conflicting text and the user's continue/ignore-without-delete/clarify choice. No new metadata, case migration or writes are required for discovery. Missing/unreadable sources leave uncertainty; lack of write permission does not prevent read-only recovery. Selected checkpoints and history remain unchanged. Record future unfinished work in existing drafts prose and append-only activity, not by changing snapshot control fields.

### Bounded drafting and publication status

The 2026-11-18 Original exhausted its owner-authorized 1500s window before R1.
Native provider message spans totalled 1393.217s, while unioned file-tool intervals took 5.803s.
Three rejected multi-file patches consumed about 459.3s of provider generation; partial/truncated anchors triggered `unseen_lines`, followed by regeneration of the document package.
These are observed trace costs, not a claim that all that time can be recovered or that provider latency equals pure model computation.

Root `AGENTS.md` now requires scoped edits/retries, append-only EOF writes, reuse of unchanged analysis and planning against the actual remaining budget.
When relaying an owner reply to a bounded runtime, the operator must supply remaining phase seconds and money from real telemetry, not repeat the original total or reset counters.
One quarter of the agreed phase time is a planning reserve for saving, hashing and both gates, not an enforced or benchmarked SLA.
Unknown telemetry stays `UNKNOWN`; a budget warning never permits skipping sources, alternatives, objections, strategies or validation.

The [template](../cases/_template/README.md#draft-и-checkpointed) separates working DRAFT, prospective control fields and published CHECKPOINTED without adding protocol states.
An owner choice does not activate R1. Keep first-draft controls empty until snapshot finalization and preserve the state's permanent conditional note in its snapshot.
No mutable publication flag is hashed into final prose: real `ACTIVE.json` and successful post-selection classification remain authoritative.
The existing template-consumer regression now rejects prospective roots, a complete unselected manifest and a gate-only candidate; only the real selector makes the unchanged consumer accept it.

For a separately authorized next Original, record a native timeline and require:
- actual remaining time/cost relayed after each owner pause, with no counter reset;
- zero `unseen_lines` rejections and no repeated multi-document retry for one bad anchor;
- saving/hash/gate preparation reached before the final quarter of its authorized phase budget;
- all existing substantive/evidence requirements, no invented owner/approval, and real `VALIDATED_CANDIDATE` then `CHECKPOINTED` before deadline;
- absent publication remains DRAFT/INCOMPLETE, not a resumable checkpoint; immutable history and approvals remain intact.

Unit tests validate consumer compatibility and fail-closed status, not the speed of a future model run. No new H1 or performance qualification is implied.

### Models, tools, services and costs

| Requirement | Supplied by | Verified boundary |
|---|---|---|
| Model/account and file read/write/edit tools | User's compatible host; Cursor/other coding assistants are workflow options | No embedded model, credentials, subscription or guarantee of automatic Skill discovery |
| Websites, documents and CSV/calculations | Permitted host tools and user-authorized inputs | No bundled crawler, OCR, RAG, database or product MCP service; unavailable formats need readable exports or UNKNOWN |
| Checkpoint verification | Python3.12+ stdlib and `tools/case_protocol.py`, or a real operator running it | Validates files/chain, not strategy quality, human authority or OS isolation |
| Git and repository checker | Developer checkout | Git is needed for clone/indexed maintenance checks, not plain ZIP analysis; no package manager/test service required |
| OMP/Docker/provider profiles | Optional operator-specific qualification setup, not product dependencies | Private profiles, sessions, keys and model history must not enter a normal manual test |
| Time and money | Owner's explicit allowance and actual host telemetry | No fixed product fee or universal monetary hard cap; soft request-stop estimates are not invoice guarantees; absent costs UNKNOWN |

Observed trial-specific model/cost figures and limits belong in the [historical engineering handoff of 18 November](current-session-handoff.md), not as a pricing promise or mandatory launcher. Current submission readiness is recorded [separately](release/submission-ready-20261122/README.md). Manual testing means a new case with the tester's own permission, not reuse of historical qualification approvals or evaluator answers.



## Changing schemas or revision protocol

Case JSONL records and the `manifest.json`/`ACTIVE.json` pair are interfaces, even though no generated schema package exists. Before changing them:

New cases carry `case-protocol.json` from the template with `protocol_id: "checkpoint-v1"`. `UNINITIALIZED` means no checkpoint has started only when there is no selector or revision artifact; change to `CHECKPOINTING` before writing the first revision file. Missing or ambiguous identity fails closed. Legacy handling is limited to the exact pre-protocol directories listed by the resume Skill; do not infer it from missing manifests.

- document the current fields, invariants, and consumer behavior in the template;
- identify every Skill, example, fixture, and saved case that reads or writes the affected fields;
- define migration and backward-compatibility behavior before editing historical data;
- add a new protocol/version marker only if consumers can use it to reject incompatible data safely;
- preserve immutable revisions, existing ledgers, and audit receipts; never silently retrofit old cases;
- test valid, missing, malformed, hash-mismatched, forked, and mixed-revision cases using synthetic fixtures where applicable;
- preserve the immutable JSONL record prefix across revisions; hash matching may accept only complete-record prefixes for the five append-only root ledgers, including a prior file ending without a final line-feed;
- add a regression test that appends records without changing the prior prefix, plus negative tests for changed/truncated prefixes and mismatched parent annotations.
- obtain independent review of the schema and migration plan.

A format/documentation-only change is not proof that an agent or host correctly enforces the contract. The repository checker validates JSON syntax and relative Markdown targets only; it does not validate semantic schemas, references between IDs, hashes, active revisions, evidence entailment, or approval scope.


## Evidence and provenance review

For each consequential claim, inspect the source itself and record an exact openable URL or repository path plus section/page/row/line locator, publisher/date/version where available, evidence status, confidence and limitations. Check that the cited material entails the claim, not just that a URL exists. Keep observed facts, documented statements, inferences, hypotheses, and unknowns distinct. For calculations preserve actual inputs, formula, units, denominator, missing-value rules, execution tool/version and result. If no execution occurred, write `NOT RUN`; do not reconstruct a fictitious receipt.



## Canonical repository checks

Run from the repository root with Python 3 and Git available. The classifier command is a deterministic synthetic-case check; it does not run a live agent or certify the host. The repository checker and unit tests do not establish product acceptance.

```sh
python3 -m unittest discover -s tests -v
python3 tools/check_repository.py
python3 tools/case_protocol.py classify cases/pantrypath-week4-20261115
git diff --check
```

For first-run changes, the narrow offline commands are `python -m unittest discover -s tests -p 'test_case_workspace.py' -v` and `python -m unittest discover -s tests -p 'test_case_protocol.py' -v`. They exercise filesystem boundaries and checkpoint consumers, not natural-language routing or automatic host discovery. Test the actual coding-assistant surface separately; see [First Run UX verification](release/first-run-ux-20261119.md) for observed live responses, review and limitations.

Runtime/resume regression coverage is in `tests/test_find_python.py` and `tests/test_resume_context.py`. PowerShell discovery tests use isolated command adapters for unavailable/broken installations and actual subprocess tests for quoting, timeouts and direct executable verification; they skip rather than install PowerShell on hosts without it. Resume tests use synthetic cases, including blocked writes, stale/partial candidates and immutable-byte comparisons. Valid JSONL EOF without a final newline remains valid; an empty drafts container is not itself pending work.

Verification on this Windows feature checkout: the full existing/new offline suite ran **110 tests, OK (5 symlink-privilege skips)** with the discovered CPython 3.12.14; actual Windows junction checks passed. `tools/check_repository.py` returned **PASS (158 Markdown files; indexed case JSON/JSONL syntax)**. No end-to-end model run, paid research or new H1/F1 agent evaluation was performed; the existing offline evaluator unit/regression tests were included in the requested suite.

Independent read-only review found two in-scope P2 issues: a probe-only encoding override could hide a broken inherited environment, and relative explicit paths/process CWD could disagree with PowerShell's location. Both were fixed. The final discovery-only suite then ran **19 tests, OK**, including real-process regressions for invalid inherited encoding, relative executable selection after Set-Location, and child CWD. The 110-test full run and bounded smoke preceded those fixes; unchanged non-discovery code was not rerun. Final static re-review: **correct, no actionable findings remain**. This is AI code review, not independent human product acceptance.

Bounded no-model smoke on 2026-11-19: Windows PowerShell 5.1 discovery skipped Store aliases, rejected an unusable launcher runtime, then selected installed CPython 3.12.14 through offline/no-download uv. That returned executable created one disposable case, exercised the unchanged candidate gate and classifier on synthetic R0001, and ran the inventory CLI over a saved draft. Inventory preserved all case bytes; the disposable case was removed. This is observed CLI execution, not live LLM E2E or a re-test of actual SlotPilot. SlotPilot's saved addendum is a user-reported discovery risk, not demonstrated data loss.

Limits: discovery is bounded to 24 subprocess attempts at five seconds each, supported PATH/project/launcher/uv sources and optional explicit executable; a missing permitted source may still require operator help. Timeout termination targets the immediate process, not an entire descendant process tree. Inventory is a non-atomic read of existing locations; semantic provenance, stale/duplicate/conflicting text and the Product Owner's choice remain the Skill/model's responsibility. No new model-behavior, automatic Skill discovery, privileged symlink/real ACL-denial, cross-host or strategy-quality qualification is claimed.

On Windows use the available Python3.12+ command in place of python3. Reading files and preliminary analysis need neither Python nor Git; publishing/resuming a canonical checkpoint requires the shared Python consumer or a real operator. The developer repository checker additionally requires a Git checkout/index and cannot run on a plain extracted ZIP. It checks indexed case JSON/JSONL syntax and selected relative Markdown targets only, not schemas, fragments, hashes, references, behavior, host security or contest acceptance.

В CRLF checkout с `.gitattributes` `text=auto` plain `git diff --check` может считать carriage return trailing whitespace. Для такого checkout используй одноразовый эквивалент без изменения Git config: `git -c core.whitespace=cr-at-eol diff --check`; он всё равно проверяет пробелы перед концом строки. Перед host-side PR проверь фактическую нормализацию/режимы в Windows.

### GitHub CI

[`.github/workflows/ci.yml`](../.github/workflows/ci.yml) runs on pull requests to **any base branch** (including stacked documentation PRs) and pushes to `main`. One GitHub-hosted Ubuntu job uses Python 3.12, the standard library, `python -m unittest discover -s tests -v`, and `python tools/check_repository.py`; no dependency installation or external service is required. The token has read-only repository contents permission; checkout does not persist credentials. This is not automated release, a PantryPath R3 classifier run, or functional acceptance. Workflow presence alone is not CI PASS: inspect the actual Actions run; if none ran, record `NOT RUN`.

## Fixture maintenance

Update a fixture only when a real contract or product change requires it. Keep expected behavior and intentionally unknown fields explicit; fixture text must not turn into evidence of an executed test. Do not revise historical audit outputs to make them pass. Product behavior needs an appropriately scoped synthetic run and independent artifact review; dynamic checks that are unavailable remain `NOT RUN` or `BLOCKED`.

## Compatibility, review, branches, and releases

- Prefer additive changes. For incompatible case/revision changes, document the old/new format, migration path, rejection behavior, and fixture coverage before implementation. Never silently reinterpret existing approvals or immutable revisions.
- Work on a named feature/release branch from the agreed base; do not force-push or rewrite published history. Keep unrelated/user-owned files out of the change.
- Ask an independent read-only reviewer to inspect the actual diff, architecture choices, link/provenance changes, and limitations. Address material findings once; retain disagreements and evidence.
- Before release, check the exact staged file set, whitespace/errors, repository integrity check, historical-data preservation, privacy/secrets, current acceptance evidence, and remote branch state. A documentation check is not release approval.
- Tag/version only when a release owner approves the scope and public claims. CI runs the bounded repository checks above; no automated release is configured. Contest submission, official brief verification, video, H02, and independent Sol acceptance are separate human/evidence gates.

## Current technical debt and release boundaries

See [Evaluation](evaluation.md) for known product risks, harness defects, unverified behavior and deferred work. The Dynamic E2E **CONDITIONAL**, F1–F5 **NOT ACCEPTED**, F6 provenance limitation, H02 **BLOCKED**, and pending Sol sign-off are statuses from the dated 2026-11-14 acceptance snapshot; this repository consolidation does not re-evaluate them. Current branch repository/protocol checks and their scope are in the [contest integration report](release/contest-v1-integration.md). Clean-host and cross-host acceptance remain uncertified; do not describe the repository as production-ready.
