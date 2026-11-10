# Phase 1 — решение и следующий шаг

## Ответ

**Да: OMP18.18.6 уже пригоден для проверенного supervised single-writer режима с контролем каждого tool approval и независимой приёмкой.** Практически квалифицирован RPC-ui путь с одним Codex Sol High writer, только native read/write/edit, ручными approvals и отдельным Lead execution после просмотра кода. Это не допуск исходного default-yolo сеанса и не утверждение, что любой TUI/CLI/headless запуск эквивалентен испытанному.

- E10 supervised gate: **PASS с ограничениями**; raw abort при pending approval — **FAIL**, требуется ручной dialog-cancel workaround.
- E01: **PASS**, 10 независимых tests и три real CLI smoke scenarios; source/frozen-input hashes проверены.
- Свежий same-family read-only reviewer: restricted supervised admission оправдан, подтверждённых CLI defects не найдено.
- Unattended, arbitrary execution, autonomous writing children, реальные секреты в workspace, непроверенные модели и parallel writers: **BLOCKED**.

Доказательства: [E10](e10-preflight.md), [E01](e01-results.md), [effective configuration](effective-configuration.md), [blockers](blockers.md). Полное первоначальное исследование не менялось.

## Минимальный следующий шаг — без реализации продукта

**Получить полное конкурсное ТЗ и в отдельном supervised запуске проверить profile/tool inventory перед планированием первого вертикального среза.** Сам продукт этой задачей не начинать. Никакие дополнительные фреймворки/сервисы для этого не нужны.

Project-local готовые файлы:

- `.omp/profiles/qualification-supervised.yml` — byte-identical копия реально испытанного `Q/workspace/.omp/config.yml` (SHA-256 `8535a5bc2f055de2accefd8571c34ab746f8c99cd6a514eace15b70817734ee3`). Файл **не активируется сам**: нужен явный --config.
- `.omp/mcp.json` — byte-identical копия испытанного project MCP config, OpenDesign disabled; global MCP registration не менялась.

Пример следующего ручного запуска **не выполнялся в конкурсном репозитории**:

```powershell
omp --config .omp/profiles/qualification-supervised.yml --model openai-codex/gpt-6.1-sol --thinking high --approval-mode always-ask --tools read,write,edit --no-extensions --no-skills --no-rules --no-context-files --no-lsp --no-title --max-time 12m --warn-cost 3 --max-cost 5
```

В начале убедиться: exact model/high, fallback=false, read/write/edit prompts, нет bash/eval/task/MCP. Смена cwd и UI требует проверки actual surface; TUI startup этой фазой не запускался. Сохранённый profile содержит machine-specific protected paths — не выдавать его за portable OS sandbox. Для нового workspace проверить canonical paths и target ownership; scope не расширять автоматически.

Пока --no-context-files включён, важные project constraints/полное ТЗ передавать явно; не предполагать скрытую загрузку AGENTS.md. Перед каждым последующим writer-run: фиксированные AC, owned paths, immutable evaluator; review proposed changes до Approve; не выдавать session-wide approvals; команды выполняет Lead только после просмотра source.

## Минимальная процедура остановки

Открытый approval сначала **Deny/Cancel**, затем abort и проверка settled/реальных файлов. При зависшем UI — остановить только известный PID worker OMP; не повторять неизвестные side effects. Этот manual порядок сработал в E10, raw abort alone — нет. Дальнейшая автоматизация допустима только после исправления/отдельного regression этой проблемы; больший timeout не исправление.

## Что сохранено и что не сделано

`Q=C:/Projects/mgimo-qualification-20261110-p1` сохранён локально: contract/tests/fixture/source, baseline Git, sanitized evidence, protocol adapter и metadata-only observer, native sessions. Это воспроизводимая test fixture вне Contest Product, не новая orchestration platform. Native JSONL содержит fake plaintext: не публиковать сырые сессии/exports, только sanitized summary. Fake/credentials не включены в repo profile.

Глобальные config/MCP/binary hashes не изменились; no installs, new providers, account linking, security weakening, publication или push. В fixture создан **один локальный baseline commit**, remote отсутствует; implementation остаётся untracked src/ для аудита. Конкурсный HEAD остался `17aa0db168366e7af61c2112c7ed65da83c864ac`; только qualification reports и project-local config добавлены как untracked. Итоговый Git/provenance снимок: `Q/evidence/final-scope.json`.

Инфраструктурная работа Phase1 завершена. E02–E09 и полный E10 не запускать автоматически; Contest Product не реализовывать без отдельной задачи.
