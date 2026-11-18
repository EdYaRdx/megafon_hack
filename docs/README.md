# Документация

Здесь собраны инструкции по использованию проекта, демонстрационный пример и технические материалы. Для знакомства с продуктом начните с [главной страницы](../README.md).

## Начните здесь

| Раздел | Что внутри |
|---|---|
| [Быстрый старт](quickstart.md) | Создать первое дело, получить результат, продолжить после паузы |
| [Демонстрация PantryPath](pantrypath-demo.md) | Исходная задача, альтернативы, стратегии, проверка расчётов и три ревизии |
| [Архитектура](architecture.md) | Компоненты, движение данных, состояние и восстановление |
| [Каталог кейсов](../cases/README.md) | Шаблон, демонстрационный проект и прочие примеры |
| [Инструкция первого запуска](../prompts/first-run.md) | Рабочий текст для новой задачи |

## Правила и методика

- [Правила процесса](../AGENTS.md) — этапы работы и требования к источникам и решениям.
- [Шаблон дела](../cases/_template/README.md) — файлы задачи, проверяемые версии и согласование действий.
- [Справочные материалы](../references/) — метрики, источники, проверка утверждений.
- [Работа с внешними материалами](../references/security-and-source-handling.md) — границы использования данных.

## Разработка и сопровождение

Эти документы **не нужны для первого использования**. Они сохраняют проверяемые результаты и техническую историю проекта.

- [Разработка и проверки](development.md).
- [Оценка и ограничения](evaluation.md).
- [Текущее состояние](implementation-status.md).
- [Контекст Development Lead](current-session-handoff.md) — текущие F1/H1 gates, интегрированные исправления и следующий внешний шаг; не пользовательский launcher и не разрешение нового прогона.
- [Процедура проверки в новой среде](clean-host-e2e-runbook.md).

## Конкурс и недостающие материалы

- [Рабочий текст конкурсного задания](contest-brief.md).
- [Проверочный список подачи](submission-checklist.md) и [сценарий видео](demo-video-script.md).
- [План недостающих материалов](documentation-todo.md) — конкурсные доказательства и необязательные материалы для презентации.

## Архив и служебные материалы

- [Датированный Contest v1 integration report](release/contest-v1-integration.md) — исторический release record своего scope, не текущая инструкция запуска или приёмка H1.
- [Исследовательский архив](../research/README.md).

## Карта документов проекта

| Класс | Статус | Основные материалы | Как использовать |
|---|---|---|---|
| **PRODUCT** | CANONICAL | Корневой [README](../README.md) | Задача, возможности, первый запуск и границы продукта. |
| **USER GUIDE** | CANONICAL | [Быстрый старт](quickstart.md), [`prompts/first-run.md`](../prompts/first-run.md) | Единственный текущий workflow нового дела и продолжения; не исследовательские launchers. |
| **DEMO** | REFERENCE | [PantryPath](pantrypath-demo.md), [traceability addendum](pantrypath-r3-traceability-addendum.md) | Подготовленный синтетический разбор; не live-run или human approval. |
| **RUNTIME CONTRACT** | CANONICAL | `AGENTS.md`, шесть `.agents/skills/`, `references/`, [шаблон дела](../cases/_template/README.md), `tools/case_protocol.py` | Канонические процедуры и consumer; текстовые правила не обеспечивают права ОС. |
| **DEVELOPER** | CANONICAL по своей теме | [Архитектура](architecture.md), [разработка](development.md), [оценка](evaluation.md), [evaluator contract](functional-evaluator.md), [статус](implementation-status.md), [handoff](current-session-handoff.md) | Инженерные сведения, текущие scoped результаты и проверки; не обещание общей сертификации. |
| **CONTEST / HOST** | REFERENCE | [Рабочий brief](contest-brief.md), [подача](submission-checklist.md), [видео](demo-video-script.md), [план материалов](documentation-todo.md), [host runbook](clean-host-e2e-runbook.md) | Подготовка и будущие процедуры; наличие документа не подтверждает исполнение или официальный provenance. |
| **ARCHIVE** | HISTORICAL | Датированные `research/`; `docs/release/`, `docs/repository-inventory.md`, `docs/next-session-handoff.md`, `docs/research-plan.md`; исторические/QA-кейсы | Сохранять прежние результаты с датой и scope; не считать текущим разрешением или инструкцией. |
| **INTERNAL HISTORY** | HISTORICAL | `MGIMO_RESEARCH_TO_IMPLEMENTATION.md`, `prompts/overnight*`, `prompts/research-smoke.md`, `START-OVERNIGHT-V3.txt`, `start-overnight-product-research-v3.cmd` | Исследовательские процедуры, не launcher продукта; сохраняют свой scope и историю. |
| **DEVELOPMENT RULES** | CANONICAL по своей области | Применимые инструкции разработки в `.omp/` | Не пользовательская зависимость продукта. Действующие инструкции репозитория не становятся устаревшими из-за этой классификации; приватные профили/секреты не копировать. |

CANONICAL означает актуальный источник по конкретной теме, REFERENCE — пояснение/пример, HISTORICAL — сохранённую запись прошлого. OBSOLETE применяется только к подтверждённо заменённой роли; возраст файла не основание его удаления. Совместимые указатели ниже остаются REFERENCE, а не второй спецификацией.

`START-HERE.txt` — прежняя краткая инструкция; актуальный путь — README → Quick Start. `docs/submission-architecture.md` сохранён как совместимая ссылка на каноническую архитектуру. Архивные документы не переписываются задним числом и сохраняют даты и scope своих проверок.
