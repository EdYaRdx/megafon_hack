# Repository inventory и план навигации

Снимок по доступным файлам/деревьям; Git status, current branch/HEAD и remote не проверялись. Базовые Git SHA и branch в задаче — ожидаемые, не результат локальной сверки. Секреты или личные данные этим инвентарём не сертифицированы.

| Область | Роль | Навигационное решение |
|---|---|---|
| Product core: `AGENTS.md`, `.agents/skills/`, `references/`, `cases/_template/`, `prompts/first-run.md` | Инструкции, 6 canonical Skills, evidence/metrics/safety guidance, шаблон дела, первый запрос | Оставить как runtime; не дублировать Skills |
| Первое использование: `README.md`, `START-HERE.txt`, `docs/quickstart.md` | Позиционирование и запуск нового case | README и START-HERE вести на один Quick Start; явно исключить OMP |
| Cases: `cases/` | Подготовленный пример, QA fixtures, исторические outputs, template | Категории и назначение указаны в [cases index](../cases/README.md); не перемещать старые папки без анализа path/protocol |
| Contest docs: `docs/contest-brief.md`, `docs/submission-checklist.md`, `docs/demo-video-script.md` | User-provided working contract и незавершённые deliverables | Не выдавать brief provenance/video/submission за проверенные |
| Product docs: `docs/` | Quickstart, architecture, evaluation, status, navigation, runbook | Использовать docs index; единая текущая точка статуса — implementation-status |
| Research/dev-only: `research/` | Product research, synthetic evals, qualification, infrastructure, historical audits | Сохранить дерево/доказательную историю; добавить индекс, не делать runtime prerequisite |
| OMP/legacy: `.omp/`, `start-overnight-product-research-v3.cmd` | Историческая development/research конфигурация и launcher | Оставить на месте для воспроизводимости; пометить development-only. Не открывать user-local profile для polish |
| Hygiene: `.gitignore`, `.gitattributes` | Ignore secrets/local runtime; normalize text | Статически прочитаны; правила не менялись. `.gitignore` не игнорирует весь `.omp/`; пользовательский `.omp/profiles/product-build.yml` не читать и не staging. Полного secret/PII scan нет |

## Наблюдаемые риски навигации

- Ранее README/START-HERE смешивали product use с OMP research history и старым acceptance language; обновлены оба entrypoint.
- Ранее submission architecture, implementation status, checklist и handoff содержали взаимно несогласованные и исторические acceptance statements; см. current status/evaluation. Historical audit/release files сохранены.
- `docs/next-session-handoff.md` и `docs/clean-host-e2e-runbook.md` — старые операционные записи с устаревшими SHA/путями; они не являются источником текущего baseline. Handoff теперь маркируется историческим; runbook требует отдельно сверять scope/commit до использования.
- `.gitignore` исключает `.omp` local state, распространённые credential patterns, raw session dumps, local artifacts/logs и OS metadata, но не заменяет explicit allowlist; `.omp/profiles/product-build.yml` — пользовательский файл, не читать/не staging. `.gitattributes` включает `text=auto`. Полного privacy scan нет.
- Legacy launcher не перемещён: его OMP/profile/Git пути и относительные предпосылки историчны; перемещение могло бы сломать воспроизводимость.

## План и выполненные действия

1. Сначала классифицировать product/runtime, onboarding, contest docs, research/dev-only и legacy. — Выполнено.
2. Исправить entrypoint и сделать docs/cases/research индексы; сохранить исторические папки. — Выполнено для навигации.
3. Привести статус/architecture/submission docs к текущему evidence и явно отделить planned procedures от observed results. — Выполнено в текущих docs; старые audit/release reports оставлены.
4. Проверить относительные ссылки, новые Quick Start пути и cross-document status. — Выполнена статическая проверка доступными read/glob; shell/Git/тесты не выполнялись.

Не выполнялись перемещения/удаления, изменение product Skills/protocol, изменение ignore rules, внешняя публикация или полный privacy scan.
