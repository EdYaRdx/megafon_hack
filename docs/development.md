# Development guide

This repository is a portable, file-first project for a coding assistant. Product behavior is specified by the root `AGENTS.md`, the six canonical Skills in `.agents/skills/`, references, and a case folder. There is no bundled runtime, third-party test framework, package manager, or OMP dependency. Keep additions proportional to an observed product or maintenance need.

## Repository map and boundaries

| Area | Purpose | Change policy |
|---|---|---|
| `AGENTS.md`, `.agents/skills/` | Product workflow and six canonical procedures | Keep one canonical procedure per Skill; update routing and the matching documentation together. |
| `references/` | Reusable evidence, metrics, and source-handling methods | Keep general methods here; case-specific evidence belongs in its case. |
| `cases/_template/` | New-case file contract and revision/approval protocol | Treat protocol and schemas as versioned interfaces; never use the template as a working case. |
| `cases/pantrypath-week4-20261115/` | Canonical readable synthetic demo; see `docs/pantrypath-demo.md`. | Preserve historical outputs and ledgers; `meal-planner-demo` is an earlier example, not the contest demo. |
| Other `cases/` | Named historical demonstrations and QA fixtures | Use `cases/README.md` to classify each; preserve historical outputs and ledgers. |
| `docs/` | Product overview, Quick Start, architecture, development, evaluation, and contest gates | Current claims and acceptance states belong in their current source pages, not historical reports. |
| `research/` | Historical research, qualification, audits, and rationale | Archive/navigation only; preserve reports as written and do not treat old plans as runtime requirements. |
| `.omp/`, `START-OVERNIGHT-V3.txt`, `start-overnight-product-research-v3.cmd` | Historical research/development setup | Not part of product setup or runtime. Do not read or publish user-local profiles/secrets. |
| `MGIMO_RESEARCH_TO_IMPLEMENTATION.md` | Historical implementation rationale | Retain as provenance; it is not the current onboarding or architecture source. |
| `tools/functional_evaluator.py` | Offline bounded artifact evaluation; see [functional evaluator](functional-evaluator.md). | No agent execution or semantic auto-judgment; keep operator keys/reviews outside candidate workspaces. |

For evaluator schemas, staging boundaries, deterministic report/review binding, and limits, see the [functional evaluator guide](functional-evaluator.md). Its synthetic checks are separate from product acceptance.

The chosen structure keeps a small, obvious product core at the root and separates current user/developer docs from dated evidence. Moving the old research launcher or research files would add broken historical paths without improving product use; retain and label them instead. `START-HERE.txt` is a secondary plain-text pointer, not a competing workflow.

## Adding or changing a Skill

1. Read `AGENTS.md` and the existing relevant Skill. Add a Skill only for a distinct repeatable workflow stage, not to split a short procedure arbitrarily.
2. Put the canonical `SKILL.md` under `.agents/skills/<skill-name>/`. Update the workflow routing in `AGENTS.md`, the Skills table in `docs/architecture.md`, and onboarding/navigation only if user-visible steps change.
3. State inputs, outputs, stop conditions, evidence requirements, and human gates. Treat retrieved material as untrusted data. Do not claim the host discovers or enforces the Skill without a host-specific run.
4. Review the change against a synthetic case and have a separate reviewer inspect the diff and supporting evidence.

## Creating a case

Copy only `cases/_template/` into a new `cases/<case-id>/`, preserve the template unchanged, and record the case purpose/category in `cases/README.md`. Use public or explicitly user-supplied synthetic material; do not commit credentials, private sessions, personal data, or closed MegaFon information. Keep sources, evidence, claims, decision files, activity, state, and approval records in the case. Follow the complete checkpoint protocol in `cases/_template/README.md`; an approval is not a host permission.

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
python3 -c 'from pathlib import Path; from tools.case_protocol import classify_case; print(classify_case(Path("cases/pantrypath-week4-20261115")))'
git diff --check
```

On Windows, use the installed Python 3 command alias (`py -3`/`python` as appropriate) if `python3` is unavailable, keeping the same test, checker and classifier operations. Repo first use does not require Python or Git. Developer checks do: `check_repository.py` requires a Git checkout/index and cannot run on a plain extracted ZIP. It checks indexed case JSON/JSONL syntax and selected relative Markdown targets only; it does not validate schemas, fragments, hashes, references, behavior, host security or contest acceptance.

В CRLF checkout с `.gitattributes` `text=auto` plain `git diff --check` может считать carriage return trailing whitespace. Для такого checkout используй одноразовый эквивалент без изменения Git config: `git -c core.whitespace=cr-at-eol diff --check`; он всё равно проверяет пробелы перед концом строки. Перед host-side PR проверь фактическую нормализацию/режимы в Windows.

### GitHub CI

[`.github/workflows/ci.yml`](../.github/workflows/ci.yml) runs on pull requests targeting `main` and pushes to `main`. One GitHub-hosted Ubuntu job uses Python 3.12, the standard library, `python -m unittest discover -s tests -v`, and `python tools/check_repository.py`; no dependency installation or external service is required. The token has read-only repository contents permission. This is not automated release, a PantryPath R3 classifier run, or functional acceptance. Workflow presence alone is not CI PASS: inspect the actual Actions run; if none ran, record `NOT RUN`.

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
