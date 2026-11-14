# Шаблон продуктового дела

Скопируй `_template/` в новый каталог `cases/<case-id>/`. Заполни brief известными данными и пометь неизвестное. Не помещай сюда секреты и закрытые материалы.

- `sources.jsonl` — источники и locators.
- `evidence.jsonl` — извлечённые подтверждения и их ограничения.
- `claims.jsonl` — тезисы, статусы и связи с evidence ID.
- `activity.jsonl` — попытки/результаты, инструменты, ошибки/повторы и доступные время/расходы.
- `approvals.jsonl` — отдельные записи human approval; пустой журнал означает отсутствие approval.
- `state.md` — этап и ссылка на единственную активную полную ревизию.
- Остальные Markdown-файлы — альтернативы, решение, две связанные стратегии и план проверки.

## Revision protocol (single writer)

Revision IDs are immutable, e.g. `R0001`, `R0002`; each manifest names exactly one parent or `null`. For each revision create `revisions/<id>/` and save exact copies of `options.md`, `decision.md`, `strategy-product.md`, `strategy-communication.md`, `test-plan.md`, and `state.md`. In its `manifest.json`, list the revision ID, parent ID, `status`, explicit `active_claim_ids`, and relative path + SHA-256 for every snapshot and every decision dependency used (inputs/source snapshots and relevant ledgers). Keep source material and append-only ledgers unchanged; snapshot all dependencies needed to reconstruct that decision.
Example manifest shape (hash values are actual lowercase SHA-256 hex digests computed from saved bytes; paths are relative to the case root):

```json
{
  "revision_id": "R0001",
  "parent_revision_id": null,
  "status": "COMPLETE",
  "active_claim_ids": [],
  "files": [
    {"path": "revisions/R0001/options.md", "sha256": "<computed-sha256>"},
    {"path": "revisions/R0001/decision.md", "sha256": "<computed-sha256>"},
    {"path": "revisions/R0001/strategy-product.md", "sha256": "<computed-sha256>"},
    {"path": "revisions/R0001/strategy-communication.md", "sha256": "<computed-sha256>"},
    {"path": "revisions/R0001/test-plan.md", "sha256": "<computed-sha256>"},
    {"path": "revisions/R0001/state.md", "sha256": "<computed-sha256>"},
    {"path": "input/<decision-dependency>", "sha256": "<computed-sha256>"}
  ]
}
```

This is a format illustration, not a complete revision or valid evidence; replace every example path/value with the actual complete dependency set and computed hash. Hash the final manifest bytes separately for root `ACTIVE.json`; do not include the manifest's own hash inside itself. `ACTIVE.json` is a small mutable selector and is not part of the revision manifest.

Write all snapshots first. Verify the file list, active claims and hashes, then write `manifest.json` last with `status: "COMPLETE"`. The root `state.md` snapshot includes the revision ID and active claims but not the manifest hash (avoiding a self-referential hash). A missing manifest, a non-COMPLETE status, a missing/hash-mismatched file, or inconsistent claim selection means INCOMPLETE/CONFLICT; never resume by combining root files with a partial revision. Never overwrite a revision folder or manufacture a missing historical artifact.

Publish in this order: update root `state.md` and `decision.md` to the verified successor, then write root `ACTIVE.json` last. It contains the selected `revision_id` and SHA-256 of that revision's manifest. It is a mutable selector outside the revision manifest; atomic replacement is not assumed. Until root files begin changing, the previous selector remains usable. If a crash leaves root files and selector disagreeing, or `ACTIVE.json` is missing/torn/mismatched, stop with `CONFLICT`; manually restore the prior immutable complete snapshot or finish selection only after re-verifying all files. A verified successor is not current until selected. Do not infer a successor from timestamps or leaf order. No atomic `CURRENT` pointer or helper is required.
Example `ACTIVE.json`:

```json
{"revision_id":"R0001","manifest_sha256":"<sha256-of-complete-manifest-bytes>"}
```

This selector is written outside the checkpoint hash set to avoid circular hashing. Revision snapshots do not contain the selector hash.

## Approval and claims

Append approvals to `approvals.jsonl`, separate from decision/revision history. Required fields: unique approval ID, approver/authority, timestamp, exact action, scope and limits, revision ID, SHA-256 of that revision's complete manifest, basis/claim IDs, expiry/review trigger, conditions. Any revision/hash, action, scope, or decisive-premise change requires new approval. Do not transfer approval. Missing/ambiguous authority or mismatch means STOP. This is a human workflow contract, not host permission enforcement.
Approval record shape (one JSON object per line in append-only `approvals.jsonl`):

```json
{"approval_id":"A-001","approver":"<name and authority>","approved_at":"<timestamp>","action":"<exact action>","scope":"<limits and included objects>","revision_id":"R0001","manifest_sha256":"<computed-sha256>","basis_claim_ids":[],"expires_at":"<timestamp or NONE>","review_trigger":"<event or date>","conditions":"<conditions or NONE>"}
```

Never copy an example approval into a real case or treat a blank/template record as consent.

`supersedes` does not select a claim. List exact active claim IDs in the complete manifest and repeat them in current state/decision. JSONL order, dates and “latest row” MUST NOT select the winner. For unresolved successor forks, mark the candidate INCOMPLETE/CONFLICT.

Each `activity.jsonl` row is a JSON event. Give source reads/requests individual attempt IDs and result status. Record failed writes/edits and retries. Use `UNKNOWN` for unknown outcomes/telemetry; do not backfill fabricated history.

For any critical calculation see `test-plan.md` and `references/metrics.md`. Store an execution receipt with the exact command actually run, cwd, input path and SHA-256, tool/runtime version, exit status, raw stdout/stderr, result, units, formula, rounding, missing/error rules. Failed commands are failed receipts, not successful calculations. If no tool ran, mark `NOT RUN`; never invent a command after the fact.
