# Quick Start

Запуск — это открытие папки проекта в coding assistant, а не установка отдельного приложения. OMP, provider API, MCP, платная услуга и зависимости пакетов для первого использования не требуются.

## Требования host

- Coding assistant с чтением/изменением файлов проекта и сохранением в пользовательской папке дела.
- Cursor, Codex, OMP или другой совместимый host могут использовать те же файлы; обнаружение `.agents/skills/`, инструменты и формат запросов зависят от host.
- Web access нужен только для разрешённых сетевых источников; расчётный инструмент — только для воспроизводимых вычислений. Если инструмент отсутствует, оставь `NOT RUN`.
- Host/model, permissions, telemetry, model usage/cost and sandbox are host-controlled; repo neither installs nor confines them. Docker/OMP не нужны для продукта.

Не добавляй секреты, закрытые материалы, credentials или персональные данные. Не запускай внешние действия без отдельного разрешения; текстовые approvals не ограничивают host.

## Создать дело

Из корня репозитория создайте копию шаблона (пример в PowerShell):

```powershell
Copy-Item -Recurse .\cases\_template .\cases\churn-review
```

macOS/Linux:

```sh
cp -R cases/_template cases/churn-review
```

Не копируйте существующий кейс и не меняйте файлы в `_template/`. В `cases/churn-review/brief.md` запишите решение, которое предстоит принять, владельца, аудиторию, ожидаемый срок, доступные материалы, ограничения и неизвестные. Создайте `input/` и положите туда разрешённые пользовательские материалы:

```powershell
New-Item -ItemType Directory .\cases\churn-review\input
```

```sh
mkdir -p cases/churn-review/input
```

## Первый запуск и результат

1. Открой корень репозитория в Cursor, Codex, OMP или совместимом coding assistant.
2. Прочитай `AGENTS.md`, новый `brief.md`, `cases/<case-id>/README.md` и `.agents/skills/intake/SKILL.md`.
3. Отправь [`prompts/first-run.md`](../prompts/first-run.md) как рабочую инструкцию. Записывай unknowns как `UNKNOWN`.
4. Работай только в копии `cases/_template/`; сохраняй evidence IDs, точные locators, альтернативы, обе стратегии, план и решение в новом деле.
5. Подготовь краткий decision memo с основными claim IDs и ссылками на источники/locators. Окончательный memo — `decision.md`.

Пример готового memo и навигация по его основаниям: [PantryPath demo guide](pantrypath-demo.md). Копируй только шаблон, не пример.

## Resume / revise

На паузе сохраняй завершённое, открытые вопросы, ошибки/повторы и один точный следующий шаг в `state.md`/`activity.jsonl`. До чтения изменяемых корневых решений прочитай [resume-revise Skill](../.agents/skills/resume-revise/SKILL.md), выбранный `ACTIVE.json`, его revision manifest и связанный `state.md`. Проверь revision/parent, manifest + все зависимости, exact active claims и наличие approval, привязанного к точным action/scope/revision/hash. Изменившаяся ревизия, decisive premise, срок или scope делает approval stale. При конфликте selector/root, hash mismatch, fork или неоднозначных claims — STOP `INCOMPLETE/CONFLICT`; не смешивай revisions и не выполняй внешние действия.

Синтетический [PantryPath R1→R2→R3 history](pantrypath-demo.md) показывает исправленную классификацию исторических revisions без изменения их файлов; это не разрешение переносить approval.
