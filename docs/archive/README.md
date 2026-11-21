# Технический архив и состав репозитория

Это вторичный справочник, **не маршрут первого запуска**. Пользовательские входы: [запуск](../quickstart.md), [видеокейс](../video-e2e.md), [архитектура](../architecture.md), [описание для жюри](../submission-description.md), [проверенные результаты](../evaluation.md).

## Решение по информационной архитектуре

Зафиксировано перед финальной редактурой 21.11.2026: README — ценность и четыре входа; пользовательские docs — запуск → видеокейс → архитектура → описание для жюри → результаты; исторические планы, аудиты и handoff — только этот вторичный раздел. Главный пример — `family-multinumber-video`, не прежний prepared demo.

Архив выделен **навигацией**, а не массовым переносом файлов. Исходные пути сохраняются для исторических locators и ссылок. Даты, старые FAIL/UNKNOWN и планы ниже не являются текущим статусом готовности документации.

## A — необходимые текущему продукту

| Материалы | Роль |
|---|---|
| [README](../../README.md), [docs index](../README.md), [Quick Start](../quickstart.md), [видеокейс](../video-e2e.md), [архитектура](../architecture.md), [описание для жюри](../submission-description.md), [оценка](../evaluation.md), [карта](../repository-guide.md) | Текущая пользовательская документация |
| [AGENTS](../../AGENTS.md), [Skills](../../.agents/skills/), [references](../../references/), [first-run](../../prompts/first-run.md) | Канонический процесс агента; этим release не меняется |
| [Шаблон дела](../../cases/_template/README.md), [каталог дел](../../cases/README.md), [основное дело](../../cases/family-multinumber-video/README.md) целиком | Новый CASE и проверяемый результат; manifests, снимки, журналы, inputs и export-map не вырезаются |
| [tools](../../tools/), [tests](../../tests/), [.github/workflows](../../.github/workflows/) | Helpers, воспроизводимость и CI; Python stdlib, без нового сервиса |
| [Development](../development.md), [offline evaluator](../functional-evaluator.md), [submission checklist](../submission-checklist.md) | Технические команды, контракт оценки и ручная передача |
| [START-HERE](../../START-HERE.txt), [submission-architecture](../submission-architecture.md) | Короткие указатели на канонические документы |

## B — полезные технические архивы

| Группа / все проверенные entrypoints | Что сохраняется |
|---|---|
| [Release reports](../release/) | Все датированные release/integration/аудит материалы: `preprod-report`, `contest-v1-integration`, `contest-rc-verification`, `contest-rc-receipt`, `demo-evidence`, `first-run-ux`, `product-grade-audit`, `product-strategy-quality`, `runtime-intake-recovery`, `video-family-e2e` и его curated receipt; файлы с датами сохраняют свой scope |
| [Текущий на момент записи handoff](../current-session-handoff.md), [ранний handoff](../next-session-handoff.md) | Операционные срезы для прежних сессий, не следующий шаг нового пользователя |
| [Research plan](../research-plan.md), [implementation status](../implementation-status.md), [старый inventory](../repository-inventory.md), [MGIMO_RESEARCH_TO_IMPLEMENTATION](../../MGIMO_RESEARCH_TO_IMPLEMENTATION.md) | История решений и разработки; не актуальная архитектура или разрешение выполнять старые команды |
| [Research index](../../research/README.md): [qualification](../../research/qualification/), [infrastructure](../../research/infrastructure/), [product](../../research/product/), [sol-audit](../../research/sol-audit/), [adversarial-audit](../../research/adversarial-audit/), [audits](../../research/audits/) | Сохранённые положительные/отрицательные испытания, исследовательские решения и границы доказательств |
| [Clean-host runbook](../clean-host-e2e-runbook.md) | Процедура старых испытаний; не доказательство, что каждый перечисленный host уже проверен |
| [Рабочий текст contest brief](../contest-brief.md) | Предоставленный конкурсный контекст; независимая сверка версии организатора не заявляется |
| [.omp](../../.omp/), research/overnight prompts в [prompts](../../prompts/) | Среда разработки и история исследовательских запусков; не runtime продукта |

Отдельно сохранены [прежний checklist](submission-checklist-20261121.md) и [история инженерных испытаний](evaluation-history-20261121.md). Текущие документы ссылаются на них как на архив, не как на незавершённый план продукта.

### Предыдущие примеры

- [Prepared mobile walkthrough](../contest-demo.md) и [`mobile-product-strategy-demo`](../../cases/mobile-product-strategy-demo/README.md) — отдельная D-цепочка, не дело из нового видео.
- [PantryPath](../pantrypath-demo.md) и [traceability addendum](../pantrypath-r3-traceability-addendum.md) — дополнительное синтетическое упражнение.
- Остальные исторические примеры и QA-фикстуры перечислены в [каталоге](../../cases/README.md). Они не используются как шаблон новой задачи и не удаляются.

## C — устаревшие подготовительные файлы: кандидаты, не удаление

| Файл | Почему устарел | Проверенные зависимости и безопасное решение |
|---|---|---|
| [START-OVERNIGHT-V3.txt](../../START-OVERNIGHT-V3.txt), [start-overnight-product-research-v3.cmd](../../start-overnight-product-research-v3.cmd) | Старый исследовательский запуск OMP; CMD способен делать commit/push в исследовательскую ветку. Не пользовательский старт | Ссылки в START-HERE, development, repository-inventory, research index; launcher зависит от относительного cwd, `.omp/profiles`, overnight prompt и contest brief. **Не запускать и не переносить без адаптации путей**. Удаление пары возможно отдельной правкой с обновлением этих references; здесь оставлена архивная копия на месте |
| [demo-video-script.md](../demo-video-script.md) | Storyboard 9:30 до нового реального видео; больше не задача «записать видео» | Входящие ссылки из media guide, documentation-todo, старых release/аудитов. Оставлен архивный баннер; удалить/перенести можно только вместе с разрешённой коррекцией входящих ссылок |
| [demo-media-guide.md](../demo-media-guide.md) | Прежний производственный план медиа | Зависит от storyboard; упоминается старым аудитом/картой. Текущие настоящий кадр и источник — [assets](../assets/README.md); план сохранён отдельно, без продвижения в пользовательском маршруте |
| [documentation-todo.md](../documentation-todo.md) | Снимок недостающих материалов до записи; прежний NOT CONFIRMED не актуальный статус видео | Ссылается на предыдущие планы, brief и checklist. Текущие материалы перечислены в docs index; файл помечен историческим, а не используется как активный backlog |

**Результат dependency-review:** прямые текстовые ссылки на эту C-группу есть в исторических документах; бесследное удаление сделало бы их неверными. Продуктовые `tools`, `tests`, Skills и references не требуют запуска overnight launcher. В этом PR нет удаления, переименования или массовой правки Git-истории. Предложение для отдельной чистки — удалить C-группу только после обновления всех входящих ссылок и повторной проверки замыкания; B сохранить.

## Неприкосновенные данные

Все сохранённые case-файлы, их manifests, snapshots, ledgers и export-map остаются побайтовыми. Даже неприкреплённый к checkpoint README видеокейса указан в export-map, поэтому для актуализации навигации меняется внешний walkthrough, не карта происхождения. Вспомогательные case scripts — inert evidence: их нельзя запускать ради чтения или Resume. Локальные видео, raw sessions, credentials, caches и пользовательские профили в Git не включаются.
