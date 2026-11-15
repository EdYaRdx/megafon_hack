# MGIMO / MegaFon Track 1 — contest-v1 integration report

**Status:** Integration worktree prepared; **not committed, promoted, pushed, merged, or submitted**. A local commit is blocked by the Windows bind mount: exact `chmod 644` was denied and an earlier commit draft would mark eight non-executable tracked docs `100755`. Two more tracked docs were edited afterward and were not part of that mode preview. No mode-changing commit was made. Current GitHub `main` and PR #5 cannot be checked from this clone.

## Repository state and ancestry

- Worktree at task start: clean; branch `test/mgimo-docker-20261115`; no staged or unstaged changes; no Git remote configured.
- Starting HEAD: `61b5ae9a4434792d6c0a4f48e61ccaee54eb637b` (`docs: record PantryPath commit status`). `e1adf315d5fecbdbce0994a233d70e1578229e72` is an ancestor. Reported baseline/PR commit objects are present locally; no fetch or GitHub verification was possible.
- **Tested HEAD:** `61b5ae9a4434792d6c0a4f48e61ccaee54eb637b` plus the current 14-path integration worktree listed below. Unit tests were rerun after the final documentation edits; current checker and whitespace-aware diff results are recorded below. No integration commit SHA exists because safe mode-preserving commit was blocked.
- Commit `04a2328199ccb90055432d97220c0e7e4c640aa1` (same SHA supplied for PR #5) is an ancestor, dated `2026-11-15T03:07:34+03:00`. Do not cherry-pick it or duplicate its code. The two later local commits are `0378d9748f4f851ef03c05eaceec3e5a845b7148` (protocol ledger-prefix fix) and `61b5ae9a4434792d6c0a4f48e61ccaee54eb637b` (PantryPath commit status). This local ancestry does not prove PR #5's live GitHub state.
- Relative to `e1adf31`, the pre-existing branch contains 58 changed paths, including checkpoint-v1 fixes/tests and the PantryPath R1/R2/R3 synthetic case and receipts. This integration adds user navigation/docs and this report; it does not edit the case, immutable revisions, ledgers, or receipts.
- Exact integration worktree files (12 tracked edits + 2 new): `README.md`, `cases/README.md`, `docs/README.md`, `docs/architecture.md`, `docs/clean-host-e2e-runbook.md`, `docs/demo-video-script.md`, `docs/development.md`, `docs/evaluation.md`, `docs/implementation-status.md`, `docs/quickstart.md`, `docs/submission-checklist.md`, `prompts/first-run.md`, `docs/pantrypath-demo.md`, `docs/release/contest-v1-integration.md`. No staged paths.

## Short inventory and product route

| Area | Current contents / disposition |
|---|---|
| User-facing product | `AGENTS.md`, six `.agents/skills/*/SKILL.md`, `references/`, `cases/_template/`, and `prompts/first-run.md`: portable instructions and case files; no runtime, OMP/Docker requirement, backend, UI, or package installation. |
| Deterministic maintenance | Standard-library `tools/case_protocol.py`, `tools/check_repository.py`, and `tests/test_case_protocol.py`; integrity/checker logic, not product runtime or host enforcement. |
| Canonical readable demo | `cases/pantrypath-week4-20261115/`, entered through [`PantryPath demo guide`](../pantrypath-demo.md); synthetic, unblinded, recommendation-only. The older `meal-planner-demo` is retained as historical, not a competing contest demo. |
| Research/development history | `research/` remains indexed and preserved; `.omp/`, overnight prompts and `start-overnight-product-research-v3.cmd` remain explicitly development/research-only. No file moves or deletions proposed. |
| Obsolete/duplicate entrypoints | No deletions. `cases/pantrypath-week4-20261115/README.md` is a template-copy text pinned as an R3 dependency; changing it would invalidate historical manifests. Use the linked demo guide and decision memo instead. |

User path: `README.md` → `docs/quickstart.md` → `prompts/first-run.md` → copied `cases/_template/` → case `decision.md`. Quick Start also links the resume/revise procedure and requires verification of selected revision, hashes, claims, approval and conflicts before continuing.

## Demo and immutable evidence

The PantryPath guide links the brief, input provenance, sources/evidence/claims, six options (explicit status quo and stop), decision, product and communications strategies, validation plan, calculations and R1→R2→R3 history. The banner distinguishes synthetic functional evidence from blind evaluation, real-user research, customer approval, multi-host certification, network testing and production security.

Protected case-file manifest: [`case-files.sha256`](../../research/qualification/pantrypath-r2-20261115/case-files.sha256), 41 files. It verified **41/41 before and after** this documentation work. Revision manifest SHA-256s (also listed in that manifest):

| Revision | Manifest SHA-256 | Meaning |
|---|---|---|
| R0001 | `be017727d3bcd6ebdd4190006f83b18d582b37d64b2df3e62703dc4415a71587` | Original selected synthetic checkpoint |
| R0002 | `5631937111e25f76b8996b5d31a58628696680dc8eafe2d8ba610a1a37eaf332` | Candidate with claimed capacity/date restriction; original classifier run failed and contemporaneous review was NO-GO |
| R0003 | `35373ca79dd0a0a59ab713e46860be2a52f67983504fbb11f338bb2f25e6e891` | Selected metadata/selection correction, not new research |

R2's recorded claim of a half-engineer-week cap through 2027-01-15 remains unverified. The alleged R1 sign-off is absent; no approval or external action exists. The R2 record documents rejection of the remembered approval. No historical failure was rewritten as a pass.

## Verification performed

| Command/scenario | Result and limit |
|---|---|
| `python3 -m unittest discover -s tests -v` | **PASS, 13/13**; includes fresh/legacy classification, parent/selector/hash checks, append-only JSONL growth and tampered/truncated prefix rejection. |
| Disposable PantryPath copies selecting R0001, R0002, R0003 | Each returned `CHECKPOINTED`; root selector/state/decision were aligned in the temporary copies only. |
| Disposable R1 copy with a changed historical `sources.jsonl` prefix | Rejected: `missing or hash-mismatched dependency: sources.jsonl`. |
| Disposable stale R1 approval record against selected R3 revision/hash | **Rejected for exact revision/hash mismatch**. The classifier still returns `CHECKPOINTED` because approvals are a workflow gate, not classifier enforcement. Saved R2 history independently records rejection of the remembered R1 approval; do not claim OS or model-level enforcement. |
| `sha256sum -c research/qualification/pantrypath-r2-20261115/case-files.sha256` | **PASS, 41/41** before and after the documentation edits; no PantryPath case files were edited. |
| `sha256sum -c research/qualification/pantrypath-r2-20261115/delivery-files.sha256` | **PASS, 6/6**; includes the case-file hash-list digest, R2 records and E2E receipt. |
| Repository checker / internal links | **PASS** (`153` Markdown files; indexed case JSON/JSONL syntax); file targets only, no fragment/external/schema checks. |
| All tracked JSON/JSONL syntax | **PASS** for 50 structured files when reading UTF-8 with BOM support. Four dated Codex R1/R2 research-case JSONL files contain a leading BOM; their bytes are preserved. |
| Secret/privacy pattern scan | **No credential, OAuth, email, or personal-path match** across 373 tracked/untracked non-ignored files. One case-insensitive `/Users/` false positive was ordinary `products/users/` prose; reviewed. Tracked filename scan found no raw session/transcript/`changes.jsonl` artifact (only `docs/next-session-handoff.md` matched). Auth stores were not read. Pattern scan is not full security certification. |
| Read-only newcomer route | **Walked** README → Quick Start → first-run prompt → template → PantryPath memo/demo guide. No template/example file was modified; this did not simulate a live host or model run. |
| Canonical sample classifier command | **PASS**, outputs `CHECKPOINTED` for PantryPath R3. |
| `git diff --check` | **FAIL in this CRLF working copy**: Git treats CR at EOL as trailing whitespace. Scoped `git -c core.whitespace=cr-at-eol diff --check` **PASS** without changing Git config. See exact line-ending note below; no content whitespace was suppressed. |
| File-mode commit gate | `git diff --summary` is empty only because `core.fileMode=false`; an earlier selective commit draft detected `100644 → 100755` for `README.md`, `cases/README.md`, `docs/README.md`, `docs/evaluation.md`, `docs/implementation-status.md`, `docs/quickstart.md`, `docs/submission-checklist.md`, and `prompts/first-run.md`. `docs/clean-host-e2e-runbook.md` and `docs/demo-video-script.md` were modified afterward and were not included in that draft. Exact `chmod 644` returned `Operation not permitted`; no commit was made. All changed paths need mode review on Windows. |

No full live-agent/product E2E, real-user study, network test, clean-host certification, or cross-host certification was run. No CI workflow was added; local standard-library checks provide the requested repeatable path without introducing CI/runtime dependencies.

## Review, risks, and contest readiness

Independent review: one read-only reviewer inspected the then-current product/docs and found one P2 broken link to this report; no other actionable findings. The targeted follow-up confirmed that link fixed and found no new issues in the report version then present. Subsequent documentation edits update the PantryPath demo/video path, stale gate wording, bind-mount blocker, host-transfer steps, and checklist disclosure; these exact final edits were not separately reviewed because the allowed full review and targeted follow-up were already used. No product code or case artifacts changed after review. Reviewers did not rerun tests; local results are recorded above.

- P0: none observed in the reviewed local change scope; this is not a security certification.
- P1: no confirmed local P1. Remote branch/PR state and jury access are unverified, not assumed safe or complete.
- P2: the local commit is blocked by bind-mount mode metadata; do not commit unintended executable bits. The earlier preview found eight, while two additional modified docs were not included in that preview; verify every changed path on Windows. The PantryPath root README is hash-pinned historical template text; do not edit it. Four dated research-case JSONL files have UTF-8 BOMs, preserved rather than rewritten. Host-side mode/CRLF review remains required.
- Historical baseline gates remain distinct: F1–F5 targeted results were NOT ACCEPTED, F6 had provenance limits, H02 was BLOCKED, and the latest independent Sol acceptance sign-off was PENDING in the dated 2026-11-14 snapshot. This consolidation's unit tests do not close those gates.
- Contest gaps: supplementary official MegaFon demo brief/provenance **UNKNOWN**; <=10-minute video not recorded; illustrated submission description/screenshots not finalized; jury access, final human acceptance and actual submission unconfirmed. No private data or organizer materials were accessed.

**Observed tools/time/cost:** Current writer runtime identifies as `openai-codex/gpt-6-luna`; model/provider billing and token telemetry are unavailable, so integration cost is `UNKNOWN`. The archived R2 process record names OMP `18.20.2`; its second fresh process took 510.84 seconds. That is not total R2 elapsed time or this integration's measured runtime. Current consolidation wall-clock/model-call totals were not instrumented. Reviewer model/usage is not assumed.

## File modes and line endings

`.gitattributes` uses `* text=auto`; `core.fileMode=false`; the bind mount reports mode `777`. Relative to `e1adf31`, five inherited mode deltas are recorded `100644 → 100755`: `cases/_template/README.md`, `docs/architecture.md`, `docs/development.md`, `tests/test_case_protocol.py`, `tools/case_protocol.py`. An earlier selective commit preview detected unwanted executable mode on the eight paths in the verification table. `docs/clean-host-e2e-runbook.md` and `docs/demo-video-script.md` were edited after that preview and their modes were not included. Exact `chmod 644` was denied with `Operation not permitted`; no permissions were changed and no commit was made. Git emitted CRLF-to-LF warnings on these ten modified docs: `README.md`, `cases/README.md`, `docs/README.md`, `docs/clean-host-e2e-runbook.md`, `docs/demo-video-script.md`, `docs/evaluation.md`, `docs/implementation-status.md`, `docs/quickstart.md`, `docs/submission-checklist.md`, `prompts/first-run.md`. The other two modified docs and all paths require host-side line-ending/mode review; two new Markdown files are LF. Plain `git diff --check` failed earlier on CRLF lines. The current post-edit `git -c core.whitespace=cr-at-eol diff --check` **passes**. Host review must inspect all 12 modified files, normalize only where needed, and avoid broad chmod/rewrite.

## Host-side promotion handoff — Windows repository owner

Do this only in the Windows clone with the owner's GitHub access; none of these actions were performed here.

1. The current branch history is committed through `61b5ae9`; the 14-path integration delta is **uncommitted**. A bundle alone omits this work. To transfer from the container, create a history bundle and a separate tracked-file patch: `git bundle create /workspace/contest-v1.bundle test/mgimo-docker-20261115` and `git diff --binary > /workspace/contest-v1-integration.patch`. Copy the patch plus new files `docs/pantrypath-demo.md` and `docs/release/contest-v1-integration.md` to the controlled Windows host location. Do not transfer runner/auth files or raw logs.
2. In the Windows clone, run `git fetch origin`, inspect actual `origin/main` and PR #5 state/checks in GitHub, then import history: `git fetch C:/transfer/contest-v1.bundle test/mgimo-docker-20261115:refs/heads/import/contest-v1`. Verify `e1adf31` ancestry and `04a2328199ccb90055432d97220c0e7e4c640aa1`; never cherry-pick/duplicate PR #5.
3. Create `integration/contest-v1` from `import/contest-v1`; apply the patch with `git apply --check` then `git apply`, and copy the two new Markdown files to their exact relative paths. Inspect mode and line endings for all 12 modified tracked files; normalize only observed unwanted differences. Review `git diff --name-status`, `git diff --summary`, `git diff --check`, and run all documented checks plus privacy scan. Commit there only after the diff contains no unintended executable bits or whitespace churn.
4. Merge freshly fetched `origin/main` into the integration branch without rewriting history; resolve conflicts without touching immutable PantryPath files. Push only that branch, open a PR to `main`, and verify its complete diff and required checks. Merge via GitHub UI after owner review; verify actual remote `main` SHA/tree. Close PR #5 only if GitHub evidence proves every PR #5 change is included in merged `main`; otherwise leave it open.

No claim that GitHub `main` changed is made here.
