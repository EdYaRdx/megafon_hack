# Стратег Фабрики продуктов

**Файловый AI-агент для продуктовых решений:** от размытого запроса и разрозненных материалов — к проверяемым основаниям, вариантам и согласованным продуктовой и коммуникационной стратегиям. Это переносимая папка проекта с инструкциями, шестью Skills, шаблоном дела и журналами; не отдельное приложение или сервис.

## Что делает агент

Агент помогает уточнить решение и его границы, исследовать разрешённые материалы, связать источники с утверждениями и неизвестным, сравнить варианты, сформировать рекомендацию и план проверки. После паузы он продолжает работу по сохранённым файлам и пересматривает выводы при новых данных. Человек сохраняет решение о существенных действиях.

В отличие от обычного чата, результат сохраняется как структурированное дело с проверяемыми связями и историей ревизий, а не только как ответ в переписке. Возможности: точные source locators; раздельные статусы доказательств; минимум три содержательно разных варианта, включая статус-кво и остановку; связанные стратегии продукта и коммуникации; метрики с comparator, знаменателями, периодом и guardrails; сохранение ревизий, оснований и состояния.

## Быстрый старт

Требуется совместимый coding assistant с доступом к папке и созданию/редактированию файлов. Модель, доступ к сайтам, локальным файлам, расчётным инструментам и обнаружение Skills зависят от host. В репозитории нет обязательного runtime, сервера, базы данных, MCP или установки пакетов.

1. Откройте корень репозитория в coding assistant.
2. Прочитайте [`AGENTS.md`](AGENTS.md), затем [`docs/quickstart.md`](docs/quickstart.md).
3. Скопируйте [`cases/_template/`](cases/_template/) в новый каталог `cases/<case-id>/`; заполните `brief.md` известным и отметьте неизвестное.
4. Следуйте [`prompts/first-run.md`](prompts/first-run.md) и сохраняйте работу только в новом деле.

**OMP не требуется для использования продукта.** Не запускайте `start-overnight-product-research-v3.cmd`: это исторический development/research launcher.

## Каноническая демонстрация

[`PantryPath synthetic case`](docs/pantrypath-demo.md) — единственный рекомендуемый для оценки полный demo: brief, synthetic inputs, evidence/claim links, шесть вариантов, решение, связанные стратегии и validation design, calculation receipt и R1→R2→R3 checkpoint history. R3 is recommendation-only; no customer research, action or approval. Подробные границы и все исходные файлы — в entrypoint. Старый [`meal-planner-demo`](cases/meal-planner-demo/README.md) остаётся historical ознакомительным примером, не вторым contest demo.

## Статус и пределы

Протокол `checkpoint-v1` теперь имеет исправления для legacy identity, JSONL-prefix hashes и immutable history; смотрите [актуальный integration report](docs/release/contest-v1-integration.md) для выполненных проверок этой ветки. Это не меняет исторические acceptance gates автоматически и не является host certification: synthetic functional E2E ≠ blind evaluation, real-user research, multi-host certification, customer approval, network testing или production security. Organizer supplementary demo brief, video and completed submission remain unverified/unknown. [`Implementation status`](docs/implementation-status.md) сохраняет разные scope и evidence.

## Документы и примеры

- [Документация](docs/README.md) · [Quick Start](docs/quickstart.md) · [Архитектура](docs/architecture.md) · [Разработка](docs/development.md)
- [Оценка и доказательства](docs/evaluation.md) · [Submission checklist](docs/submission-checklist.md) · [Integration release report](docs/release/contest-v1-integration.md)
- [Каталог кейсов](cases/README.md) · [Research/dev-only индекс](research/README.md)

## Для разработчиков и исследователей

`research/`, `.omp/` и `start-overnight-product-research-v3.cmd` относятся к разработке, аудиту и исследовательской истории, не к product runtime или первому запуску. См. [research index](research/README.md). Не запускайте legacy launcher как Quick Start; не публикуйте сырые сессии, секреты или личные данные.
