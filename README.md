# megafon_hack

Подготовка к MGIMO AI Challenge 2026, номинация «ИИ-проект», кейс МегаФона «Стратег Фабрики продуктов». Цель — качество, полезность и воспроизводимость конкурсного агента, а не развитие собственной инфраструктуры.

## Текущая стадия

**Project Bootstrap & Research Preparation. Продукт не реализован; предметное исследование ещё не запускалось.**

- Инфраструктурное исследование принято. Phase 1 подтвердила только ограниченный supervised single-writer путь на disposable CSV fixture; это не квалификация всех режимов OMP.
- **Полный оригинал кейса не предоставлен.** [contest-brief](docs/contest-brief.md) — явный BLOCKED status, не заполненное ТЗ. Без оригинала нельзя завершить кейс-специфичное исследование или перейти к продуктовой реализации.
- [Research profile](.omp/profiles/research.yml) — **CANDIDATE** до отдельного read-only scout smoke. Schema/metadata validation не равна runtime qualification.
- Default `yolo` текущего запуска не разрешение на автономные изменения. Bootstrap-файлы создаются в явно согласованном scope, не на основании permissive default.

## Навигация

| Файл / раздел | Назначение |
|---|---|
| [.omp/AGENTS.md](.omp/AGENTS.md) | Только Development System: стадии, безопасность, исследователи, review и будущая приёмка |
| [docs/contest-brief.md](docs/contest-brief.md) | Статус отсутствующего оригинала; позже — исключительно дословный текст организаторов |
| [docs/research-plan.md](docs/research-plan.md) | A–D workstreams, evidence/critique protocol, scout smoke, launch recipe и следующий Deep Research prompt |
| [.omp/profiles/research.yml](.omp/profiles/research.yml) | Новый read-only CANDIDATE overlay; не активируется автоматически |
| [.omp/profiles/qualification-supervised.yml](.omp/profiles/qualification-supervised.yml) | Неизменённый qualification baseline; другой режим, не база для бесконтрольного research |
| [Infrastructure recommendation](research/infrastructure/recommendation.md) | Принятые решения; не повторять обзор без новой конкретной потребности |
| [Qualification admission](research/qualification/next-step.md) | Практические результаты E10/E01 и пределы допуска |
| [Qualification blockers](research/qualification/blockers.md) | Abort/UI failure, plaintext local logs, отсутствие OS sandbox и прочие границы |
| [.gitignore](.gitignore) | Secrets, private sessions, logs и временные файлы; не security sandbox |

## Development System ≠ Contest Product

`.omp/`, infrastructure/qualification reports и локальные sessions — средства разработки. Contest Product будет переносимым файловым агентом согласно будущему проверенному ТЗ, без неявной зависимости от OMP/личных accounts/MCP.

Корневой `AGENTS.md` **не создаётся**: он зарезервирован для будущего конкурсного агента. Development instructions находятся только в `.omp/AGENTS.md`. Lead нового OMP-сеанса загружает их через native context discovery; task children получают существенные правила явно через shared `task.context`.

## Порядок продолжения

1. Получить полный оригинал кейса и сохранить дословно, отдельно зафиксировать provenance/полноту.
2. По отдельному разрешению выполнить [smoke одного scout](docs/research-plan.md) в disposable environment. Проверить actual model/high, child tool inventory, один public поиск, отсутствие mutation/exec/fallback и корректный lifecycle.
3. До допуска трёх concurrent researchers отдельно проверить read-only E02-lite; иначе работать последовательно с concurrency1 overlay.
4. Только затем — разрешённое Deep Research по A–D. Profile намеренно запрещает и Lead-запись: результаты в ответе, curated файлы — отдельным supervised writer-проходом.
5. Продуктовая реализация требует отдельного разрешения, утверждённых AC и независимых acceptance gates.

Команда запуска после prerequisites и полный следующий prompt сохранены в [research-plan](docs/research-plan.md). Не применять `--profile research` вместо `--config`: named profile имеет другую auth/config область. Не передавать `--yolo`, не добавлять новые extensions/MCP/providers.

Реальные secrets/PII не должны быть доступны исследователям. Private sessions хранить в ignored `.local/` либо вне repo; native JSONL/export могут содержать plaintext. При pending approval сначала Deny/Cancel, затем abort/settled check. Approvals/restrictedFolders/worktrees не являются OS-песочницей.
