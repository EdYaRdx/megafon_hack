# Стратег Фабрики продуктов — MVP агента

Файловый AI-агент помогает руководителю цифрового продукта пройти путь от размытого вопроса до доказательной продуктовой и коммуникационной стратегии. Это папка с инструкциями, навыками, шаблоном дела и журналами доказательств; приложение, сервер, MCP и отдельный платный провайдер не требуются.

## Состояние

**File-based MVP with synthetic case exercises.** [`cases/meal-planner-demo/`](cases/meal-planner-demo/) covers local materials, a public method source, survey-denominator arithmetic, options and strategies. [`cases/fresh-start-demo/`](cases/fresh-start-demo/) was created in a fresh OMP context by following this README and `prompts/first-run.md`, then independently reviewed. Neither is a clean Cursor/Codex startup or real-user acceptance test. The official [MGIMO AI Challenge landing page](https://challenge.mgimo.ai/) says partner assignments are in the personal cabinet; the exact MegaFon demo file and its provenance remain `UNKNOWN` until an authorized team member supplies it ([availability note](research/qualification/official-demo-brief-availability.md)). Do not invent the brief or MegaFon data.

1. Открой эту папку в coding assistant с чтением локальных файлов. Начни с `AGENTS.md` и `.agents/skills/intake/SKILL.md`; OMP и отдельный runtime не нужны. Фактическое обнаружение Skills зависит от host и должно проверяться отдельно.
2. Скопируй `cases/_template/` в `cases/<короткий-id>/`, заполни `brief.md` и используй `prompts/first-run.md`.
3. Создавай outputs в новой папке дела. Для первого completion/revision следуй `cases/_template/README.md`; неполные revisions не восстанавливаются как текущие.
4. Проверяй `state.md`; рекомендация, decision и scoped approval — разные статусы. Для руководителя краткая запись `decision.md` обязана сообщать выбранное направление, альтернативы, product+communication strategy, основания, UNKNOWN, проверку, решение владельца и следующий шаг.

Историческая OMP research/dev инфраструктура находится в `.omp/`, `research/` и `start-overnight-product-research-v3.cmd`; она не входит в product first-use/runtime. См. [чистый E2E runbook](docs/clean-host-e2e-runbook.md).

Пример стартового запроса:

> Помоги решить, как снизить отток пользователей цифрового сервиса. Сначала уточни решение, срок и доступные данные. Не предполагай причину оттока. Сохраняй источники и неизвестное в `cases/churn/state.md` и журналах; до рекомендации предложи варианты, включая оставить как есть и остановить направление.

Пример иллюстрирует workflow, а не утверждает, что у МегаФона есть такой продукт или проблема.

## Что включено

- `AGENTS.md` — основная инструкция агенту и гейты качества.
- `.agents/skills/*/SKILL.md` — единственная каноническая копия intake, исследования доказательств, вариантов, стратегий, экспериментов и продолжения после паузы.
- `references/` — статусы утверждений, правила работы с источниками и метриками.
- `cases/_template/` — переносимый шаблон отдельного дела с раздельными фактами, гипотезами, решениями и состоянием.
- `prompts/first-run.md` — короткая команда для первого запуска.
- `research/product/` — исследовательские материалы и проектные решения; это обоснование дизайна, не результат работы MVP.

## Границы MVP

- Инструменты и доступы задаёт выбранная среда. Текст инструкций сам по себе не ограничивает права host и не является песочницей.
- Публичные источники и материалы, предоставленные пользователем; никаких закрытых данных МегаФона и секретов.
- Синтетические интервью и данные всегда помечаются как синтетические и не доказывают реальный спрос.
- Если модель/host не показывает расходы или точные вызовы, записывай `UNKNOWN`.
- Пока нет официального демо-брифа МегаФона, clean-host проверки, реальных пользовательских испытаний, измеренной полной стоимости, проверки во второй среде или записи видео. Архитектурный документ — подготовительный черновик, а не финальное измеренное описание.

## Подготовка к подаче

- [Архитектура и ограничения](docs/submission-architecture.md) — текущий, непрошедший чистый host acceptance снимок.
- [Сценарий видео до 10 минут](docs/demo-video-script.md) — план, не запись; требуется реальный capture и проверка нового чата в IDE.
- [Чек-лист подачи](docs/submission-checklist.md) — текущие проверки и блокеры.
- [Implementation status](docs/implementation-status.md) — проверенные результаты и следующие шаги.

Эти материалы не подтверждают запуск в Cursor/втором host, реальное исследование, фактическую стоимость или завершённое конкурсное видео.

История разработки OMP и инфраструктуры находится в `.omp/` и `research/infrastructure/`; это не runtime и не зависимость конкурсного продукта.
