# Evidence and claim conventions

## Statuses

- `OBSERVED` — непосредственно увидено в материале или воспроизводимом расчёте; укажи, что именно наблюдалось.
- `DOCUMENTED` — явно написано в указанном источнике; это не автоматически означает, что источник независим или применим.
- `CLAIMED` — утверждение организации/собеседника, которое отдельно не проверено.
- `INFERENCE` — вывод из перечисленных доказательств с явным объяснением связи.
- `HYPOTHESIS` — предположение, требующее проверки.
- `UNKNOWN` — сведений недостаточно или они недоступны.

## JSONL records

IDs in historical JSONL rows are immutable. A `supersedes` edge records history; it does not select a current claim. Every complete revision MUST list `active_claim_ids` explicitly in its manifest and current `state.md` and `decision.md`. Consumers MUST use that selection, never line order, timestamps, or “last row wins.” Each active claim must exist and must not itself be superseded by another active claim. If two successors are plausible and neither is explicitly selected, or the active set conflicts with the graph, stop and report `INCOMPLETE/CONFLICT`; do not resolve by recency.

`source`:

```json
{"id":"S-001","url":"https://example.org/page","publisher":"Publisher","title":"Title","published":"2026-01-01","version":"v1","retrieved_at":"2026-01-02","locator":"section / page / table","snapshot":"sources/S-001.txt","sha256":"...","status":"OBSERVED","limitations":"..."}
```

`evidence`:

```json
{"id":"E-001","source_id":"S-001","locator":"section / page / row","summary":"Кратко перескажи релевантный фрагмент","extraction_method":"manual|host|parser+version","review_status":"verified|unverified","limitations":"..."}
```

`claim`:

```json
{"id":"C-001","text":"Проверяемое утверждение","status":"DOCUMENTED","evidence_ids":["E-001"],"valid_as_of":"2026-01-02","limitations":"...","supersedes":[]}
```

Не копируй длинные фрагменты. Хэш подтверждает идентичность сохранённого файла, не достоверность содержания и не качество извлечения. Для критической цифры сверяй преобразование с оригиналом.
При пересмотре сохрани связь «старый claim → successor» в записи, текущем состоянии и решении. `invalidated_by` не дописывай задним числом в append-only журнал. При ветвлении разрешены несколько successors, но active selection обязателен; unresolved fork блокирует рекомендацию.

## Revision-specific approval

Approval is a separate append-only record, not a decision status. Each record MUST identify approver, exact action, scope/limits, revision ID, complete-manifest SHA-256, decision/claim basis, timestamp, expiry or review trigger, and conditions. A changed revision, manifest hash, action, scope, or relevant premise requires a new approval. Missing/mismatched/expired approval means STOP. Approval text is not host-level authorization or a security boundary.

## Revision checkpoints

Every revision has an immutable ID, parent revision (or `null` for first), complete file snapshots for `options.md`, `decision.md`, both strategies, `test-plan.md`, and `state.md`, explicit `active_claim_ids`, and SHA-256 entries for every snapshot and every external dependency used by the decision (including source/input files and relevant ledgers).

Write snapshots first and `manifest.json` last. Only a manifest with `status: "COMPLETE"` and matching hashes for every listed file is a checkpoint. An interrupted revision lacking that final manifest is `INCOMPLETE` and MUST NOT be resumed or treated as current. Resume only the unique complete descendant chain from the last checkpoint; missing/mismatched files or multiple complete children are `CONFLICT` and require human inspection. Do not infer current state from modification time or JSONL order. No `CURRENT` pointer is required. Preserve incomplete folders for diagnosis; never repair them into COMPLETE by assumption.

Old cases without complete manifests remain historical artifacts, not new-protocol checkpoints. Do not fabricate missing snapshots or approvals.

In `activity.jsonl` record each source attempt/result and each case-file write/edit failure/retry. If outcome is unknown, state `UNKNOWN`; do not reconstruct success.
