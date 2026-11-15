# MGIMO / MegaFon Track 1 — Contest v1 integration review

**Record date:** 2026-11-16 (Europe/Moscow), before the integration PR was created. This is a point-in-time acceptance record; PR checks, review, and merge state are not inferred here.

## Repository and integration scope

- Primary checkout: `C:\Projects\GitHub\megafon_hack`, on `codex/megafon-mvp-file-agent`. It contains pre-existing untracked `.omp/profiles/product-build.yml` and `tatus -sb`; they were left untouched.
- Integration worktree: `C:\Projects\GitHub\megafon_hack-release-review`, branch `integration/contest-v1-20261115`; the release work was performed there. Starting integration commit: `038ea1b0809949a0d1ce39e5a90f943e70f8992d`.
- Fetched `origin/main` is `e1adf315d5fecbdbce0994a233d70e1578229e72`, an ancestor of the integration branch. PR #5 (`fix/a02-protocol-identity-20261115`) is open and mergeable at the time of this record. The integration includes its `04a2328` commit and follow-up regression fixes; do not duplicate it.
- The integration adds checkpoint-v1 classification and regression coverage, a synthetic PantryPath example with R1/R2/R3 history, and one canonical navigation route through README → Quick Start → first-run prompt → case template → PantryPath guide.
- Canonical product materials are `AGENTS.md`, `.agents/skills/*/SKILL.md`, `references/`, `cases/_template/`, and `prompts/first-run.md`. `tools/case_protocol.py` and `tools/check_repository.py` are deterministic maintenance utilities. OMP/Docker are development/test tools, not product dependencies.
- PantryPath is synthetic and recommendation-only. Its case files retain the evidence, uncertainty, and earlier rejected/checkpoint states; this example is not evidence of actual customer demand.

## Confirmed Windows integrity issue and fix

With system `core.autocrlf=true`, Git converted hash-pinned case text to CRLF in the Windows worktree. The classifier hashes raw bytes, so the R3 manifest check failed; direct checks found 25/41 case file hash mismatches and 6/6 delivery hash mismatches before the fix. Git object bytes themselves matched the recorded LF digests.

The release adds scoped `-text` rules in `.gitattributes` for all `cases/**` plus the PantryPath R2 delivery directory and E2E receipt. The affected worktree files were restored byte-for-byte from their existing Git blobs; no historical snapshot, manifest, or audit result was edited. Afterward the PantryPath classifier returned `CHECKPOINTED`, the case checksum list passed 41/41, and the delivery checksum list passed 6/6.

## Acceptance performed

- `python -m unittest discover -s tests -v`: PASS, 13/13.
- `python tools/check_repository.py`: PASS, 153 Markdown files and indexed case JSON/JSONL syntax. Its scope excludes hash, link-fragment, external-link, schema, product, and host validation.
- PantryPath classifier: PASS, `CHECKPOINTED` for the selected R3 revision.
- PantryPath `case-files.sha256`: PASS, 41/41, including the R1/R2/R3 manifests and snapshots; `delivery-files.sha256`: PASS, 6/6.
- `git -c core.whitespace=cr-at-eol diff --check`: reports three historical whitespace findings in `cases/pantrypath-week4-20261115/brief.md`, `cases/pantrypath-week4-20261115/sources/S-005-r2-addendum.md`, and `research/qualification/pantrypath-r2-20261115/r2-raw-addendum.md`. They are checksum-pinned; exact bytes were verified and retained. The command is therefore **not a full PASS**. The remaining reported findings are a trailing blank line and trailing spaces in these historical files.
- `git diff --summary origin/main...HEAD`: release additions use mode `100644`; no executable-bit changes were observed. `.gitattributes` disables line-ending conversion only for exact-byte case/delivery artifacts.
- A repository-wide tracked-file scan found no credential-pattern matches. The artifact-name scan found only the pre-existing `docs/next-session-handoff.md`; inspection confirmed it is historical operating guidance, not a raw session. This is a scoped screening, not a security certification.

## Limits

No clean-host or cross-host acceptance, live model product E2E, real-user research, network test, production security review, jury-access check, or contest submission was performed. Existing dated audit gates remain at their recorded states; this release's unit tests do not close them. The synthetic PantryPath case makes no claim of real demand. No credentials or private organizer materials were accessed.

## Follow-up

Use the integration PR as the live source for checks, review, merge result, and final `main` SHA. Preserve the primary checkout's two untracked items. Do not rewrite or line-normalize the checksum-pinned PantryPath history.
