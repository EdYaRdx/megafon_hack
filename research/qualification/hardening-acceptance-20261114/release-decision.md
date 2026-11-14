# Предрелизное решение

**Вердикт для этого checkout: `MERGE_BLOCKED`; продуктовый merge не разрешён этим решением.** Targeted review говорит, что условный pre-release baseline *может рассматриваться* владельцем отдельно, с явно открытым H02; это не approval и не разрешение на автоматический merge. Публикация audit-only пакета — отдельная операция и не означает merge в `main`.

## Зафиксированное состояние

- Hardening worktree `C:\Projects\GitHub\megafon_hack-hardening` HEAD ref resolves locally to `codex/mgimo-hardening-20261114` → `98cd57ef8d0ba5e919c505466fa82f4e4653b9fe`; E2E worktree HEAD is detached at the same SHA. Primary checkout HEAD points to `codex/megafon-mvp-file-agent` at `ff3c953975597de63deb99a8f094a99b4877c307`; local `main` ref is `e0151431f8992d145733f580731b8e472f2be354`. These are observed local `.git` ref files, not fresh Git commands or remote refs. `acceptance-report.md:9` records 311/311 tracked files unchanged in its test comparison.
- Git status, untracked/staged inventory, remote refs/auth, stage/push are not available through the permitted tools. This turn changed release docs and added the publication script only; pre-existing unrelated working-tree status remains UNKNOWN. Historical `preprod-report.md:8-13,46-47,63` describes an earlier checkout state, not current status.
- Полный E2E не повторялся. Ни процесс не завершался, ни платный API не вызывался.

## F1–F5: конкретные подтверждённые findings targeted harness

Все пять findings в `acceptance/20261114-dynamic/final-closure.md:17-24` — **P1 defects targeted fixture/harness/checker**, не подтверждённые product-runtime defects. Ссылка ниже указывает на review из sibling E2E checkout.

| ID | Подтверждённая ошибка и влияние | Минимальное исправление/гейт |
|---|---|---|
| F1 | T01 R2 `test-plan.md` сохраняет основной знаменатель всех eligible started attempts, а добавленная фраза «completers only» ему противоречит. Проверка искала только эту фразу; положительный boolean не доказывал смену operative metric. Неверный тест может ложно подтвердить изменение знаменателя. | Убрать противоречие; проверять operative section/ожидаемую формулу и негативные исходы, не одной подстрокой. Не переобъявлять текущую R2 кандидатом PASS. |
| F2 | `targeted-closure.ps1` захватывает существующий `manifest.json` в список файлов до записи нового manifest (самоссылочный hash, не совпадает); копирует зависимости в уже существующий destination, образуя `dependencies/dependencies/`. `COMPLETE` не подтверждён. | Не включать manifest самого себя в hash list; копировать в точный целевой dependency path без лишнего вложения; проверять все пути/hash и COMPLETE статус на независимой fixture. Не «чинить» исторический manifest задним числом. |
| F3 | `run-one-boundary.ps1` hardcode-ит `-Boundary 1` при проверке команды и помечает exception как boundary 1; другие номера не проверяются корректно. H02 evidence также не подтверждает process identity: CIM отказан, exit 90 сам по себе недостаточен. | Сравнивать с фактическим параметром boundary и маркировать его динамически; для H02 требовать проверенную идентичность процесса. До такой проверки оставить BLOCKED, не запускать cleanup по PID. |
| F4 | Boundary/checkpoint receipt записываются прямо в canonical path через `WriteAllText`/`Set-Content`; interruption может оставить усечённый receipt. | Писать временный соседний файл, валидировать и заменять атомарно; отдельно тестировать interruption. До исправления durability receipt не считать доказанной. |
| F5 | Checker не проверяет parent manifest digest, уникальность COMPLETE successor/fork, точное равенство active-claim sets, containment путей внутри case root. Имеющиеся positive/negative fixtures покрывают только operational note и operative revision mismatch. | Добавить минимальные fixtures на каждый пропуск и отказать при fork/hash/claim/path mismatch; PASS разрешать только после всех инвариантов. |

`F6` отдельно указан reviewer как P2: T04 receipt представляет строку как `executed_command` и задаёт `exit_code=0`, хотя литеральная команда не была исполнена именно так/статус не захвачен. Сводные числа независимо перепроверены в review: generated/opened/orders `18/13/6`, отношения `13/18`, `6/18`, `6/13`; это агрегатные отношения, не conversion. Не переименовывать F6 в F1–F5.

## Продуктовый runtime и H02

- Независимый targeted reviewer не обнаружил product-integrity P0/P1; final closure сообщает «no product P0/P1 confirmed». Это ограничено наблюдавшимися synthetic single-host tests и не является security certification или доказательством отсутствия всех дефектов (`final-closure.md:7,26`).
- Основные динамические проверки T01–T09 в acceptance report описаны как PASS в указанных узких сценариях; исходное итоговое состояние **CONDITIONAL**, не unconditional acceptance (`acceptance-report.md:3-5,19-41`).
- H02 остаётся **BLOCKED**. Исходный forced-replay aggregate отсутствует, причина зависания UNKNOWN (serialization — только inference); проверка identity новых boundary runs заблокирована отказом CIM; PID 6568 не останавливался (`acceptance-report.md:49-55`; `targeted/final-closure.md:9,21,33`). H02 не PASS.
- Independent Sol review: **PENDING** по `verdicts.json` и `sol-handoff.md:3`. Доступный `independent-review.md/json` — независимый targeted acceptance review, не заключение Sol. Подменять одно другим нельзя.
- Targeted QA пакет — `NOT ACCEPTED / BLOCKED`; harness/checker changes нельзя выдавать за принятые исправления. `final-closure.md:11` допускает, что владелец *может рассмотреть* отдельный conditional merge продуктового baseline, явно принимая открытый H02; это не рекомендация для текущего merge и не approval.

## Release-gate disposition

| Gate | Статус | Фактическое основание |
|---|---|---|
| Local baseline identity | CONFIRMED FROM LOCAL GIT METADATA | Hardening ref and E2E HEAD both point at `98cd57ef…`; this was verified by reading worktree/branch ref files. Not remote verification. |
| F1–F5 targeted harness | FAIL / BLOCKED | F1–F5 — перечисленные P1 дефекты, targeted QA NOT ACCEPTED. |
| Продуктовый P0/P1 в наблюдавшихся тестах | NONE CONFIRMED, ограниченный охват | Не экстраполировать на все хосты/условия и не считать доказательством security. |
| H02 | BLOCKED | Нет подтверждённой identity/cleanup; не запускать/останавливать неизвестный процесс. |
| Sol sign-off | PENDING | Handoff требует review; независимая targeted review не является Sol. |
| Секреты/PII | НЕ ПРОВЕРЕНО для publication package | В локальном предрелизном отчёте описан только ограниченный scan с исключениями; полный scan/allowlist этого нового пакета пока не выполнялся. |
| Локальные ветки, working tree и remote/auth | НЕ ПРОВЕРЕНО сейчас | Нет разрешённых Git/shell инструментов. Не заявлять существование ветки, push или удалённого commit. |
| Instructions и repeatability | PARTIAL | `README.md` описывает запуск; acceptance — single-host Codex/Pwsh, ограниченная воспроизводимость; произвольные host/crash timing не покрыты. |
| Доступность отчётов | SOURCE AVAILABLE LOCALLY | Источники прочитаны из указанного E2E checkout, но ещё не опубликованы в GitHub. |

## Решение и условия пересмотра

Сейчас продуктовый merge остаётся `MERGE_BLOCKED`: нет отдельного owner approval на conditional pre-release, H02 и Sol остаются открыты, а exact publication scope/security checks/remote branch status не проверены. Это решение не утверждает, что обнаружен продуктовый runtime P1. Рекомендация targeted reviewer разрешает только рассмотреть исключение; если владелец отдельно одобрит его, в решении и PR должны быть прямо указаны H02 BLOCKED, F1–F5 как open harness defects, отсутствие Sol sign-off и невозможность заявлять полную acceptance.

Audit-only публикация этих документов — отдельный scope. Публиковать только явный allowlist Markdown/JSON/docs; исключить raw sessions/JSONL, process dumps, private settings, credentials, сырые receipts/логи и непроверенные архивы. Новый package manifest должен показывать исходный путь/hash и непубликуемые данные. До получения проверенного Git handoff никакой push не заявляется.

### Источники

- `acceptance-report.md`: `Results`; `Blocked variant, errors and limits`.
- `independent-review.md`: `Findings F1–F6`; `Targeted checks`; `Limits and next action`.
- `independent-review.json`: `findings`, `targeted_checks`, `limitations`, `next_action`.
- `targeted/closure-report.md`: `H02 finding and disposition`; `Status and merge assessment`.
- `targeted/final-closure.md`: `Final verdict`; `Review findings reconciled with evidence`; `Targeted statuses`.
- `verdicts.json`, `sol-handoff.md`: итоговый статус и pending Sol review.
