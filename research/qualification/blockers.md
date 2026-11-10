# Phase 1 — blockers, failures, unknowns

Дата:2026-11-10. **Нет блокера для проверенного узкого supervised single-writer пути.** Есть обязательные ограничения; полный E10/unattended не приняты. Не интерпретировать статус E01 PASS как снятие этих ограничений.

| ID | Статус | Факт / влияние | Наименьшее исправление или безопасный fallback |
|---|---|---|---|
| B01 | FAIL | RPC abort при pending approval не ответил за30s. Original response пришёл после45.344s только после cancel UI | Supervised: сначала Deny/Cancel dialog, затем abort/settled check; это реально сработало за42ms после cancel. Для unattended нужен исправленный runtime/host handling и отдельный regression, не маскировка большим timeout |
| B02 | FAIL для log secrecy | Native JSONL содержит raw fake. Provider redaction не означает sanitization local storage; диагностический вывод Lead также показал fake | Только fake/несекретные workspace данные; JSONL/export не публиковать. Для реальных секретов нужен отдельный storage/log redaction qualification. Не копировать auth в fixture |
| B03 | BLOCKED | OS containment не создан/не квалифицирован. Read/write approvals/restrictedFolders/worktree — не sandbox | Не давать worker shell/eval/network/MCP; ручные per-call approvals; исполнять только проверенный Lead код. Для untrusted/unattended — отдельная OS boundary, но не устанавливать сейчас |
| B04 | UNKNOWN | 429/retry exhaustion, hard cost cap, full timeout/crash recovery, kill process tree, symlink/host escape не проверены | Не заявлять общий E10/E06 PASS. Отдельная phase только при реальной потребности; текущий scope не использует эти пути |
| B05 | UNKNOWN | Точная денежная стоимость/доля quota одной задачи не устанавливается catalog estimate и shared account snapshot | Existing Codex only, quotas наблюдать; никаких paid fallbacks/new providers. В report неизвестное не заменено нулём |
| B06 | Ограничение независимости | Reviewer fresh-context той же Codex семьи, read-only; разные семьи не вызывались | Принимать как контекстно независимую проверку + deterministic evaluator, не multivendor review. Дополнительную платную модель не подключать |
| B07 | Ограничение покрытия | 10 tests покрывают AC1–5, но не все combinations/parser branches; fixture мала и trusted | Не экстраполировать на сложный Contest Product. Для каждой product slice свои независимые acceptance/negative tests и реальный smoke |
| B08 | Наблюдённая human intervention | Writer после первого чтения спросил approval в prose и остановился | Один clarification: вызвать native read/write и дождаться UI. Дальше scope не расширялся; не заявлять zero-intervention autonomy |

## Не блокируют эту фазу

- OpenClaw/OpenDesign/Spec Kit/OpenSpec/BMAD/Superpowers/OptiLLM/Council не нужны и не подключались.
- Docker/WSL/Python/Bun installation не понадобились: native OMP binary и существующего Node достаточно.
- E02/E03 parallel writers/isolation не запускались; безусловный single-writer enforced tool inventory и процессной последовательностью.
- Полное конкурсное ТЗ ещё отсутствует. Это блокер реализации продукта, **не завершения qualification**.

## Решение

Можно использовать OMP только с указанными supervised controls. Нельзя переносить допуск на исходный yolo/default session, autonomous writing subagents, произвольный shell или реальные secrets. Переход к Contest Product автоматически не выполняется. Подробные evidence: [E10](e10-preflight.md), [E01](e01-results.md), [configuration](effective-configuration.md).
