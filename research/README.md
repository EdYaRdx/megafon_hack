# Research и development-only материалы

`research/` не является частью product runtime и не требуется для первого запуска. Здесь сохранены исходные исследования, design rationale, evaluation records и audits; исторические отчёты не редактировать задним числом. Содержимое считать рабочими материалами, а не автоматически актуальной спецификацией. Перед внешней публикацией требуется отдельная privacy review: поиск по ключам не гарантирует обнаружение личных/чувствительных данных.

## Навигация по коллекциям

| Путь | Класс | Использование |
|---|---|---|
| [`product/`](product/) | Product/domain research и дизайн | Источники и исследовательские синтезы, требования, agent design, оценки/roadmaps, debates и overnight audit. Это обоснование и история, не user evidence или runtime output. |
| [`sol-audit/`](sol-audit/) | Synthetic evaluation/dev records | Методика, fixtures F1–F3/F8/F9, run logs, reviews, adjudications и смежные результаты. Не путать старые exploratory scores с текущими F1–F5 targeted gate. |
| [`qualification/`](qualification/) | Host/infrastructure qualification | Historical preflight, host acceptance, blockers, official-demo availability и provenance records. Qualification статусы привязаны к своему scope/date. |
| [`audits/sol-preprod-2026-11-14/`](audits/sol-preprod-2026-11-14/) | Historical independent static audit | `CONDITIONAL` verdict; findings и roadmap относятся к статическому preprod scope, не dynamic Sol sign-off. Не переписывать. |
| [`infrastructure/`](infrastructure/) | Development environment/tool comparison | Исторический анализ OMP/DSH/моделей/инфраструктуры; не продуктовая зависимость и не текущая рекомендация запуска. |
| [`adversarial-audit/`](adversarial-audit/) | Historical challenge/report | Дебаты и проверки прежних сравнений; не новый независимый Sol acceptance. |

## Product runtime отдельно

Product runtime/первое использование определяются корневыми `AGENTS.md`, `.agents/skills/`, `references/`, `cases/_template/` и `prompts/first-run.md`. OMP-настройки и legacy research launcher находятся отдельно в `.omp/` и `start-overnight-product-research-v3.cmd`; не использовать их как пользовательский запуск.

Для текущих acceptance статусов см. [docs/implementation-status.md](../docs/implementation-status.md) и [docs/evaluation.md](../docs/evaluation.md).