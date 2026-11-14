# План закрытия F1–F5 / H02

Статус по доступному independent review: F1–F5 — открытые P1 defects тестовых fixtures/harness/checker; H02 **BLOCKED**. Ниже — минимальные дальнейшие действия, не выполненные в этой сессии. Исторические результаты не переписывать; полный E2E не повторять.

| Finding | Минимальное действие | Доказательство для закрытия |
|---|---|---|
| F1 | Исправить T01 fixture так, чтобы operative denominator, а не добавленная contradictory note, отражал заявленный вариант; заменить substring-only assertion. | Проверка основных требований/формулы и отличающихся исходов; показать отрицание старого operative wording. |
| F2 | Пересобрать isolated R2 manifest без self-entry и с dependency paths одного уровня; не изменять старую fixture/report. | Независимый полный путь/hash check, выбранный parent и COMPLETE manifest без self-reference. |
| F3 | Убрать boundary-1 hardcode и неверное exception label; не запускать H02 пока не подтверждается identity. | Статическая проверка parameterized boundary; отдельный безопасный one-boundary result с проверенной PID/start/parent/executable/command identity. Если метаданные denied — BLOCKED, процесс оставить работающим. |
| F4 | Записывать receipt во временный sibling, валидировать, затем заменять; не утверждать atomicity сверх возможностей используемого механизма. | Interruption case подтверждает либо старую целую receipt, либо новую целую receipt, но не усечённую canonical. |
| F5 | Добавить отдельные checker fixtures: bad parent hash, competing COMPLETE children/fork, exact active claim-set mismatch, traversal/out-of-root path. | Каждый конфликт отвергнут; допустимый selected chain проходит. |
| H02 | Не завершать PID 6568 и не повторять looping forced-replay harness. Сначала одобрить bounded procedure, удостовериться в identity receipts; неопределённая identity означает BLOCKED. | Отдельный безопасный bounded run с точным process attribution и receipt; иначе оставить H02 BLOCKED. |

**Общее завершение:** сохранить каждый новый прогон отдельно; прежние receipts/manifest не исправлять на месте. Получить независимое re-review targeted changes; Sol handoff пока PENDING, Codex independent review не является Sol sign-off. Не включать неподтверждённые harness repairs в публикацию как PASS.

**Scope и безопасность публикации:** включать только перечисленные review/docs и machine-readable finding JSON после явной проверки allowlist. Raw Codex/OMP transcripts/session JSONL, process dumps, private settings, credentials, все непроверенные receipts/logs/fixtures остаются локально. Не заявлять полный secret/PII scan без проверки точного staged diff. Merge продуктового baseline — отдельное решение владельца; данный план не одобряет merge.
