# Development guide

This repository is a portable, file-first project for a coding assistant. Product behavior is specified by the root `AGENTS.md`, the six canonical Skills in `.agents/skills/`, references, and a case folder. There is no bundled runtime, test framework, package manager, CI, or OMP dependency. Keep additions proportional to an observed product or maintenance need.

## Repository map and boundaries

| Area | Purpose | Change policy |
|---|---|---|
| `AGENTS.md`, `.agents/skills/` | Product workflow and six canonical procedures | Keep one canonical procedure per Skill; update routing and the matching documentation together. |
| `references/` | Reusable evidence, metrics, and source-handling methods | Keep general methods here; case-specific evidence belongs in its case. |
| `cases/_template/` | New-case file contract and revision/approval protocol | Treat protocol and schemas as versioned interfaces; never use the template as a working case. |
| `cases/meal-planner-demo/` | Recommended synthetic end-to-end example | Keep synthetic labels and evidence limits visible. |
| Other `cases/` | Named historical demonstrations and QA fixtures | Use `cases/README.md` to classify each; preserve historical outputs and ledgers. |
| `docs/` | Product overview, Quick Start, architecture, development, evaluation, and contest gates | Current claims and acceptance states belong in their current source pages, not historical reports. |
| `research/` | Historical research, qualification, audits, and rationale | Archive/navigation only; preserve reports as written and do not treat old plans as runtime requirements. |
| `.omp/`, `START-OVERNIGHT-V3.txt`, `start-overnight-product-research-v3.cmd` | Historical research/development setup | Not part of product setup or runtime. Do not read or publish user-local profiles/secrets. |
| `MGIMO_RESEARCH_TO_IMPLEMENTATION.md` | Historical implementation rationale | Retain as provenance; it is not the current onboarding or architecture source. |

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

The explicit case-protocol classifier has focused synthetic regression tests: run `py -3 -m unittest discover -s tests` (Windows) or `python3 -m unittest discover -s tests` (macOS/Linux). It checks new/legacy classification, selector and manifest integrity, snapshot hashes, and active-claim agreement; it does not prove that a coding assistant follows the Skills.

## Evidence and provenance review

For each consequential claim, inspect the source itself and record an exact openable URL or repository path plus section/page/row/line locator, publisher/date/version where available, evidence status, confidence and limitations. Check that the cited material entails the claim, not just that a URL exists. Keep observed facts, documented statements, inferences, hypotheses, and unknowns distinct. For calculations preserve actual inputs, formula, units, denominator, missing-value rules, execution tool/version and result. If no execution occurred, write `NOT RUN`; do not reconstruct a fictitious receipt.

## Checks and fixtures

Run the standard-library repository integrity check after edits to Markdown, case JSON/JSONL, or navigation. It requires Python 3.9+ and Git; first use of the product does not require either.

PowerShell:

```powershell
py -3 tools/check_repository.py
```

macOS/Linux:

```sh
python3 tools/check_repository.py
```

This is a **repository/test-harness integrity check**, not a product test. It checks JSON/JSONL syntax only for case files already in the Git index, avoiding untracked user case data, and checks relative Markdown file targets in the current product/developer surface. Stage only sanitized new fixtures before checking them. It does not validate JSONL schemas, link fragments or external links, revision hashes, product behavior, host Skill discovery, security, or contest acceptance.

Update a fixture only when a real contract or product change requires it. Keep expected behavior and intentionally unknown fields explicit; fixture text must not turn into evidence of an executed test. Do not revise historical audit outputs to make them pass. Product behavior needs an appropriately scoped synthetic run and independent artifact review; dynamic checks that are unavailable remain `NOT RUN` or `BLOCKED`.

## Compatibility, review, branches, and releases

- Prefer additive changes. For incompatible case/revision changes, document the old/new format, migration path, rejection behavior, and fixture coverage before implementation. Never silently reinterpret existing approvals or immutable revisions.
- Work on a named feature/release branch from the agreed base; do not force-push or rewrite published history. Keep unrelated/user-owned files out of the change.
- Ask an independent read-only reviewer to inspect the actual diff, architecture choices, link/provenance changes, and limitations. Address material findings once; retain disagreements and evidence.
- Before release, check the exact staged file set, whitespace/errors, repository integrity check, historical-data preservation, privacy/secrets, current acceptance evidence, and remote branch state. A documentation check is not release approval.
- Tag/version only when a release owner approves the scope and public claims. No automated release or CI is configured. Contest submission, official brief verification, video, H02, and independent Sol acceptance are separate human/evidence gates.

## Current technical debt and release boundaries

See [Evaluation](evaluation.md) for the evidence-backed breakdown of known product risks, harness defects, unverified behavior, contest blockers, and deferred work. Current acceptance is limited: dynamic E2E **CONDITIONAL**; F1–F5 **NOT ACCEPTED** due to harness/checker defects; F6 has a provenance limitation; H02 **BLOCKED**; latest independent Sol acceptance sign-off **PENDING**. Clean-host and cross-host acceptance are not certified. Do not describe this repository as production-ready.
