# Evidence and claim conventions

## Statuses

- `OBSERVED` — непосредственно увидено в материале или воспроизводимом расчёте; укажи, что именно наблюдалось.
- `DOCUMENTED` — явно написано в указанном источнике; это не автоматически означает, что источник независим или применим.
- `CLAIMED` — утверждение организации/собеседника, которое отдельно не проверено.
- `INFERENCE` — вывод из перечисленных доказательств с явным объяснением связи.
- `HYPOTHESIS` — предположение, требующее проверки.
- `UNKNOWN` — сведений недостаточно или они недоступны.

## JSONL records

Одна JSON-объект запись на строку, UTF-8. ID неизменяемы; исправление добавляет новую запись и ссылку на заменяемую, а не переписывает историю.

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
{"id":"C-001","text":"Проверяемое утверждение","status":"DOCUMENTED","evidence_ids":["E-001"],"valid_as_of":"2026-01-02","limitations":"...","invalidated_by":[]}
```

Не копируй длинные фрагменты. Хэш подтверждает идентичность сохранённого файла, не достоверность содержания и не качество извлечения. Для критической цифры сверяй преобразование с оригиналом.
