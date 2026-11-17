---
name: resume-revise
description: Продолжи дело из файлов и оцени влияние новых данных на старые выводы и решения.
---

# Resume and revise

## Classify the case before reading mutable roots
Before reading or writing any case file, explicitly resolve exactly one user-specified active directory `cases/<case-id>/`. If absent or ambiguous, ask for the exact case path and stop; do not select by scanning neighboring contents, timestamps, example names, or guessing. All case files—including `brief.md`, `README.md`, `case-protocol.json`, `ACTIVE.json`, `state.md`, ledgers, and revisions—are relative to this CASE root. The marker is only `cases/<case-id>/case-protocol.json`, never a repository/workspace-root marker. Shared `AGENTS.md`, `.agents/skills/`, prompts, and references remain project-root relative. “Root” below always means CASE root for case files.

Explicitly select the same directory again in a fresh/resumed session. Follow the classification below before reading mutable case-root files. A missing marker for an explicitly selected case follows only the fail-closed/legacy rules below; never fall back to the project root or another case.

For a new case copied from `cases/_template/`, first read its root `case-protocol.json`. It must contain the supported `protocol_id: "checkpoint-v1"` and `checkpoint_state` of `UNINITIALIZED`, `CHECKPOINTING`, or `CHECKPOINTED`. Missing, malformed, unsupported, or ambiguous identity is `INCOMPLETE/CONFLICT` and means stop; missing `ACTIVE.json` never makes a case legacy.

- `UNINITIALIZED` with no `ACTIVE.json`, no revision manifest, and no files under `revisions/` is a fresh case. Intake/root working files may be populated; no saved decision checkpoint exists yet.
- Before writing any first-revision snapshot, change the marker to `CHECKPOINTING`. If the selector or any revision artifact then exists without one unique verified complete checkpoint, stop with `INCOMPLETE/CONFLICT`.
- A complete checkpoint is accepted only by the manifest/selector/hash/claim checks below. After the complete selector is verified, the marker may be set to `CHECKPOINTED`; a valid selector remains authoritative if a crash leaves the marker at `CHECKPOINTING`.
- A missing marker is eligible for legacy handling only for the exact pre-protocol case directories enumerated below, and only when no `ACTIVE.json` or revision manifest exists. Existing legacy snapshots may be read under their historical limitations; they are not certified complete. Any other missing-marker case, or any legacy-listed case with a selector/manifest but no valid new-protocol identity, is `INCOMPLETE/CONFLICT`. Do not infer legacy from timestamps, filenames, or absent files.

Bounded pre-protocol legacy directories: `fresh-start-demo`, `meal-planner-demo`, `offer-terms-demo`, `public-source-retention-smoke`, `resume-failure-demo`, `retention-demo`, `retention-f1-demo`, `service-launch-f3`, `source-injection-demo`, and `unseen-shelf-alerts-20261114`. This list identifies historical format only; it does not make an incomplete case complete or authorize edits to its history.

For a `checkpoint-v1` case, read root `ACTIVE.json` as the explicit active-revision selector. It must name a revision ID and SHA-256 matching that revision's `manifest.json`; verify manifest status and every listed file hash before using it. Root `state.md` and `decision.md` must name the same selected revision and active claims. Use only that revision's six snapshots (`options.md`, `decision.md`, `strategy-product.md`, `strategy-communication.md`, `test-plan.md`, `state.md`) plus listed immutable dependencies. A successor manifest is written and verified before `ACTIVE.json` selects it; update the selector last. A missing/torn/mismatched selector, inconsistent root state/decision, missing/hash-mismatched file, or multiple complete children is `INCOMPLETE/CONFLICT`. Stop; do not mix files or infer from timestamps/JSONL order. Recover manually from the prior immutable complete snapshot after verifying it. Legacy cases are limited to the explicit allowlist above and follow their existing state without retroactive certification.

Claim selection is explicit: use only `active_claim_ids` listed in the complete manifest and repeated in current state/decision. `supersedes` records graph edges, not an automatic winner. If two descendants compete and the active selection is missing or inconsistent, stop for owner/reviewer resolution.
Аналитический вывод можно пересмотреть при новых свидетельствах или обнаружении слабости прежнего основания: добавь append-only successor claim с новым `id` и `supersedes` (включая `UNKNOWN` или снижение уверенности) и явно выбери актуальные claims в новой immutable revision. Не выдумывай независимый результат и не меняй исторические записи. Пересмотр вывода сам по себе не меняет принятое продуктовое направление: предложение агента не является выбором владельца.

Смена принятого продуктового направления требует явного решения владельца. Исполнение выбранного направления — отдельный вопрос: перед сверкой, экспериментом или внешним действием проверь отдельное approval record, применимое именно к этому действию/объёму и revision ID с SHA-256 complete manifest. Любая новая revision/hash, изменённое действие/объём, истёкшее approval или изменившаяся решающая предпосылка исключают повторное использование: запроси новое human approval; при отсутствии применимого approval останови это исполнение, а не документирование аналитического вывода. Никакое approval, предложение или checkpoint не даёт host permissions.

Before preparing a new checkpoint, read the exact machine-control lines in `cases/_template/README.md` and preserve them in root `state.md`/`decision.md` and their snapshots. Labels and punctuation are part of the contract: one field per line, no trailing prose or period; do not paraphrase the revision/active-claim labels. Keep explanations separate. Use the verified parent and explicit claim selection, not timestamps or JSONL order.

Create a new immutable revision ID, prepare all six final root Markdown views byte-identical to their snapshots, and hash every saved snapshot and immutable decision dependency (saved source snapshots, inputs and ledgers actually used; never mutable root views or `ACTIVE.json`).
For every successor, include `parent_manifest_sha256` computed from the exact bytes of the verified selected parent's saved `manifest.json`; root revisions may omit it or use `null`.
Write the manifest last with `status: "COMPLETE"` only after verifying completeness and hashes.

**Before selecting it in the real `ACTIVE.json`, require an actual successful `python tools/case_protocol.py check-candidate <CASE> --revision <ID>` receipt from the shared developer tool.**
The gate validates the actual selected parent, all ancestor hashes/snapshots/dependencies/claim prefixes and forks, all six root views, then checks a temporary copy with the proposed selector using unchanged `classify_case`.
`VALIDATED_CANDIDATE` does not mean the real case is published.
Use its computed selector digest without changing verified files, select last, then require `python tools/case_protocol.py classify <CASE>` to return `CHECKPOINTED`.
Only then claim compatibility and continue protocol resume.

Keep final state/decision focused on the decision, claims, business obligations and next step; publication truth belongs in the actual selector and external/append-only receipts, not transient `ACTIVE old`/`NOT RUN`/`NOT PUBLISHED` prose.
A candidate is not successful until real post-selection classification passes.

If the shared tool is outside the product's allowed workspace/tools, ask the operator for these actual receipts; never reach outside the boundary or invent a call. Missing access/receipt is `NOT RUN` and stops selection; any error is `INCOMPLETE/CONFLICT`, not a successful checkpoint. Preserve rejected/history artifacts, and do not replace this gate with a hash-only or case-specific verifier. Do not silently repair a published revision. These checks create no execution approval or host permission.

For legacy cases, retain existing append-only rules: do not rewrite prior files/journal entries; add new successor claims and explicitly select them in current state/decision. Do not retrofit a manifest or approval onto historical work.

Update state with work read, differences, claims revised, unknowns and one exact next action. In `activity.jsonl`, record each source attempt/result and case-file write/edit failures/retries. Unknown attempt outcomes remain `UNKNOWN`.
