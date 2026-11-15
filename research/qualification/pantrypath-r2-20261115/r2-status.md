# R2 process record — original parser failure; repaired protocol verifies chain

**Status:** The fresh OMP process generated the R2 decision candidate. Under the old classifier, R2 failed selection and its contemporaneous reviewer returned `NO-GO`. A later protocol fix accepts its parent annotations after checking them against the manifest; R0001, R0002 and R0003 now each classify `CHECKPOINTED` when selected on a disposable case copy. No R1/R2/R3 manifest or snapshot was rewritten.

## Fresh process and persistent history

- OMP executable: `/usr/local/bin/omp`, version `18.20.2`.
- First fresh process: empty session directory `/tmp/pantrypath-omp-r2-ru1k1R`, no `--continue`/`--resume` or transcript, `-p`, `--approval-mode=write`. It read the R2 input but its Bash/eval/hash/write calls were blocked: `requires approval but no interactive UI available`. No case files changed in that attempt.
- Second fresh process: empty session directory `/tmp/pantrypath-omp-r2-retry-eMNOxi`, no `--continue`/`--resume` or transcript; `--tools=read,edit,write,bash --approval-mode=write --auto-approve`. It ran for 510.84 seconds. It created and selected R0002.
- Session persistence: fresh session directories contain OMP session JSONL/`changes.jsonl` files, verified by listing filenames and sizes only. These raw session logs remain under `/tmp`; none are copied into Git.

## R2 candidate result

- R2 input: `r2-raw-addendum.md`, SHA-256 `0bc20d40288ec976174ae4d89590aca24bc3716b8af05260d56611f60f0ddffa`; remains outside the case as raw handoff. The candidate copied it to `cases/pantrypath-week4-20261115/sources/S-005-r2-addendum.md`.
- Handoff prompt: `handoff-prompt.md`, SHA-256 `e5d405344063df817e3a37dfd3e205b5c3b5709c7f42dc76cda0e963c01c3374`.
- Candidate R2 manifest SHA-256 `5631937111e25f76b8996b5d31a58628696680dc8eafe2d8ba610a1a37eaf332`; its 18 listed dependency hashes and selector-to-manifest hash match actual bytes. It says `COMPLETE`, but that label is not sufficient.
- Candidate meaning: claimed half-engineer-week cap through 2027-01-15 conditionally defers R1's diagnostic; partner copy remains blocked; no retention-win claim. R2 added E-005–E-007 and C-06–C-09, updated product/communication strategies and validation timing, and rejected the alleged remembered approval. `approvals.jsonl` remains empty; no approval was invented/appended.
- Original deterministic run raised `ProtocolError: root state does not declare revision and active claims`: R2 root and snapshots use `(parent R0001)` on selector lines, which the old parser rejected. The repaired parser recognizes this explicit form and verifies it against `parent_revision_id`; the isolated R1→R2→R3 replay passes with all historical snapshots unchanged.
- Fresh read-only R2 reviewer returned `NO-GO` under the old parser. That contemporaneous result remains part of history and is not represented as an as-run pass.
- No repair was made to R2 snapshots or its manifest; the parser changed, not the historical candidate files.

## R1 preservation and R2 recovery

- R2 appends caused the four R1 whole-file ledger hashes to differ because the original JSONL files had no final LF; a separator LF was added before new rows. Each R1 manifest hash matches the exact earlier row bytes without that separator. The old classifier compared full-file hashes only.
- The updated classifier verifies exact complete-JSON-object prefixes, with or without terminal LF, for the five append-only root ledgers; changed or truncated bytes inside a selected prefix still fail. Inline and separate parent annotations are accepted only when they match the manifest.
- In an isolated copy, each of R0001, R0002 and R0003 returned `CHECKPOINTED` when selected. The six snapshots and manifests remained byte-identical. CSV mutation and R1-prefix mutation were rejected; the approval ledger remains empty and R2 refuses to reuse the alleged R1 sign-off.
- A fresh independent read-only review after the fixes returned `PASS`, with no actionable defects; it checked prefix scope/boundaries, parent binding, unchanged history, and receipt wording. Earlier R3 reviewers returned `CONDITIONAL` over stale receipts.
- `case-files.sha256` now covers all 41 case files. `sha256sum -c` verified all 41; a separate set comparison confirmed every current file occurs exactly once.
- R2 raw input and verified handoff prompt remain separate from the case until the fresh R2 process read them. No new evidence was introduced for R3. No user research, build, recruitment, deployment, partner contact, or external message occurred.
- Handoff: `research/qualification/pantrypath-r2-20261115/HANDOFF.md`. R3 is a recommendation only; no approval record or external action is authorized.

## Handoff

The R2 process's original classifier run failed; the unchanged R2 revision is now selectable as `CHECKPOINTED` with the repaired parser. R3 is the currently selected `CHECKPOINTED` successor. The case is recommendation-only: no approval, external message, build, recruitment, deployment, GitHub push, PR, or contest submission occurred. The initial commit attempt failed because identity was unset; after the user provided a local identity, commit `0378d9748f4f851ef03c05eaceec3e5a845b7148` succeeded on `test/mgimo-docker-20261115`. No remote is configured.
