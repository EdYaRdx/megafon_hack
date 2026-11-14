# Inventory — независимый pre-production audit

Дата: 2026-11-14. Объект: «Стратег Фабрики продуктов», EdYaRdx/megafon_hack. Заданный пользователем immutable baseline: `7bbe59d37d4c1e13f0fd4453f7605e8d2f601d42`; заданная ветка: `audit/sol-preprod-20261114`. Это идентификаторы задания, не результат проверки HEAD: Git не использовался. Чтение относится к доступному checkout; его побайтовое соответствие SHA **UNVERIFIED**. Продукт не изменялся. Новые отчёты создаются только в этой папке.

## 1. Задача и границы

Проверить, помогает ли переносимая папка агента получать и пересматривать обоснованные продуктовые решения, и определить доказанные дефекты, пределы демонстрации и программу развития. Владелец итогового решения — пользователь/команда; срок подачи проверен по публичному регламенту: 22 ноября 2026, 23:59 МСК. Аудит не является разрешением публикации, исследования людей или запуска продукта.

Доступны `read`, `glob`, `grep`, `web_search`, реальные read-only task reviewers, `write` для отчётов, средства управления задачей. Shell/eval/browser/GUI/продуктовый runtime отсутствуют в используемом наборе. Разрешённый JSON-reader выполняет jq-фильтры; это отдельная проверка данных аудитором, не запуск агента в Codex/Cursor. Git, платные API, OptiLLM, Polza, installs, конфигурации и личные хранилища не использовались. Raw sessions/credentials не копировались.

`OBSERVED_STATIC` означает непосредственно прочитанный файл/текст. `CHECKED_DATA` — указанный успешный детерминированный запрос reader. `HISTORICAL_REPORTED` — сохранённое описание прежнего запуска, не его повтор. `INFERENCE` — механизм/оценка. `BLOCKED/UNVERIFIED` — динамическая проверка недоступна. VERIFIED не используется без уточнения предмета проверки.

## 2. Полная карта структуры

Корень перечислен через directory read. Поддеревья cases, references, docs, research и skills перечислены отдельно; первоначальная объединённая glob-выдача достигла лимита 200, поэтому cases и остальные исследовательские деревья перечислены самостоятельными запросами. Не заявляется прочтение каждого исторического файла целиком.

| Компонент | Состав и назначение | Глубина проверки |
|---|---|---|
| `AGENTS.md` | Product mission, start/resume, workflow, evidence, human gates, cost/done | Полный текст, сопоставление с шестью Skills и шаблоном |
| `.agents/skills/` | `intake`, `evidence-research`, `options-decision`, `strategy-communication`, `experiment-design`, `resume-revise`; по одному `SKILL.md` | Все шесть прочитаны полностью через `skill://`; metadata и процедуры наблюдаемы, host discovery не запускался |
| `references/` | `evidence-and-claims.md`, `metrics.md`, `security-and-source-handling.md` | Все полностью; статусы, ID/supersedes, расчётные требования, границы безопасности |
| `cases/_template/` | README, brief, options, decision, product/communication strategy, test-plan, state, четыре пустых JSONL | Все непустые файлы прочитаны; пустые ledgers — намеренный чистый старт |
| `cases/` | Десять именованных учебных/диагностических дел, перечислены ниже | Структура полностью; глубокая проверка выбранных сквозных дел и specialist review, остальные как fixture/history |
| `docs/` | contest-brief, submission-checklist, submission-architecture, demo-video-script, implementation-status, next-session-handoff, research-plan, release/preprod-report | Конкурсный текст, архитектура, видео, release/provenance прочитаны; большие status/checklist/handoff — релевантные разделы и specialist review; research-plan — исторический план, не активный запрет |
| `prompts/` | first-run, research-smoke, overnight-research, overnight-product-research-v2/v3, overnight-goal-v4 | Структура; first-run полностью; исторические overnight-задания не runtime продукта |
| `research/sol-audit/` | architecture-decision, critical-review, research-methods, open-source-decisions, evaluation-plan, implementation-roadmap; fixtures F1/F2/F3/F8/F9; eval-results | Архитектура, методы, критика и evaluation полностью/релевантные разделы; adjudication и failure reports прочитаны; specialist проверяет связанные runs |
| `research/product/` | requirements-and-evidence, domain-research, agent-design, open-source-reuse, evaluation-and-roadmap, debate-and-review, research-status, overnight-research-v3, overnight-audit | Структура; research-status и overnight findings; предыдущие авторские исследования — историческая доказательная база, не независимая истина |
| `research/adversarial-audit/` | report, verification, deliberation | report/verification прочитаны; история критики Sol/Luna и trade-offs |
| `research/qualification/` | brief availability, effective configuration, e01/e10, blockers/next-step; host-acceptance Codex | Полный текущий Codex provenance/acceptance, source/evidence/claim ledgers и activity; исторические qualification — контекст, не нынешний veto |
| `research/infrastructure/` | architecture-options, comparison, experiments, routing, OMP config, recommendation/review, findings A/B/C/local | Структура и исторические ссылки; не runtime-зависимость, не повторялась квалификация OMP |
| `MGIMO_RESEARCH_TO_IMPLEMENTATION.md` | Cutover к file-first MVP, три PARTIAL FULL runs, условия добавления инструментов | Прочитаны решение, доказательства, ограничения, roadmap/source map |
| `README.md`, `START-HERE.txt`, `START-OVERNIGHT-V3.txt`, launcher | README — продукт; START-HERE и CMD — историческое unattended research/publication | README, START-HERE и CMD полностью; обнаружен конфликт входных маршрутов, см. technical-findings |
| `.omp/` | Development policy/profiles/MCP configuration | Политика получена в контексте; локальные профили/секреты не читались, runtime не аттестован |
| `.git`, ignore/attributes | Метаданные checkout и правила публикации | Git-операций и исследования содержимого `.git` нет; secret scan/статус индекса не заявляются |

## 3. Cases и что они действительно показывают

Все найденные продуктовые кейсы — **synthetic** или фиксированные искусственные fixtures. Реального пользовательского исследования/реальных продуктовых данных МегаФона в изученных делах не установлено. Публичный методический источник не превращает synthetic case в полевое исследование.

| Case | Материалы/покрытие | Доказательная граница |
|---|---|---|
| `retention-demo` | CSV, публичные методические заметки, R1 snapshots, текущая R2, successor C-008 | Арифметика supplied fields исторически проверялась; D30 event/eligibility остаются UNKNOWN (`state.md`, Open questions) |
| `retention-f1-demo` | `cohorts.csv`, `metric.md`, brief; зрелый D30 против D7, смена состава | Отдельный искусственный контракт D30 уже определён; не переносить UNKNOWN из retention-demo на F1 |
| `offer-terms-demo` | promo HTML, terms v2/v3 Markdown, ledgers | Конфликт цены/лимита/регионов/effective dates; это не настоящий PDF-ingestion test |
| `service-launch-f3` | constraints, economics CSV, fictional alternatives HTML | Условная экономика, не спрос; сценарный потолок бюджета не фактическая затрата |
| `source-injection-demo` | Явно adversarial Markdown memo, brief | F8 проверял один распознаваемый локальный payload; не web/PDF/host sandbox |
| `resume-failure-demo` | R1/R2 notes, отсутствующий source, claims C-002/C-003/C-005, snapshots | История показывает найденные и исправленные ошибки claim/event; не аварийная транзакционная сохранность |
| `meal-planner-demo` | Fictional survey, concept, method source, R1/R2 snapshots, текущая R3 | Неодинаковые cohorts не pooled; рекомендация не меняется, реальные audience/economics UNKNOWN |
| `fresh-start-demo` | Fictional library task, заполненный workflow | Исторический fresh OMP context, не независимый clean GUI-host run |
| `public-source-retention-smoke` | Live Mixpanel guidance, conflict/revision, ledgers | Публичное vendor-определение не принято за продуктовый metric contract; ошибка в примере источника раскрыта |
| `unseen-shelf-alerts-20261114` | Six-store CSV, protocol, vendor HTML с injection, GOV.UK method, R2 order-confirmation constraint, revisions | Изучены decision/state/четыре журнала/input protocol+CSV/plan/communication; корректный активный C-009 вместо C-005, C-010 ограничен synthetic scope; это не доказательство causal impact |
| Codex acceptance `…/20261114-r1-r2/case/` | Копия meal-planner raw inputs, AAPOR, R1/R2 outputs и snapshots | Отдельная упаковка synthetic host exercise, не новый независимый рыночный кейс |

## 4. Provenance и лестница доказательств

| Утверждение | Что непосредственно подтверждено сейчас | Чего это не доказывает |
|---|---|---|
| Есть file-based агент | Прочитаны инструкции, шаблон, журналы и содержательные outputs | Не самостоятельное приложение; host предоставляет модель и инструменты |
| Есть все шесть Skills | Полные тексты и matching имена | Автоматическое обнаружение/активацию в целевом host |
| Есть источники и пересмотр | В unseen source→evidence→claim ссылки, C-009 supersedes C-005, current state/decision явно выбирают successor | Все случаи повреждения JSONL, fork/supersession conflict или interrupted writes |
| Codex R1/R2 выполнены | `host-provenance.md`, разделы R1/R2: разные Session IDs, версии 0.166.0/0.169.0, reported counts 22/7 exec, hashes | Raw logs отсутствуют; это пользовательская диагностическая сводка, не свежий trace audit. Сам путь каталога 0.169.0 не версия R1 |
| Независимый acceptance PARTIAL PASS | Сохранённый `acceptance-review.md` с методикой, проверками и ограничениями | Автоматическую активацию Skills, byte-identical прошлое или одинаковую повторяемость |
| F1/F2/F3/F8/F9 проверялись | Сохранены конкретные runs/reviews/adjudications, включая отрицательные результаты | Matched causal преимущество; одинаковость model/provider/tools не установлена |
| Безопасность обеспечена | Правила явно отказываются от sandbox-гарантии | Устойчивость к injection во всех форматах/реальный least privilege |
| Продукт дешёвый | Нет bundled provider/server; расходы часто честно UNKNOWN | Нулевую полную стоимость моделей, поиска, retries, человека |
| Готов конкурсный пакет | Есть draft architecture, checklist, video run sheet | Видео, organizer-specific demo, human acceptance и отправку |

## 5. История технических решений и расхождений

1. `research/product/agent-design.md` — ранний file-first дизайн; `research/sol-audit/architecture-decision.md`, «Рабочий контракт варианта A», предлагал `current.json`, целые ревизии и узкий CLI publish/check.
2. `research/adversarial-audit/report.md` и `verification.md` V3–V6 — возражения против лишнего runtime, напоминание о lost approval, mixed revisions и неполном бинарном acceptance.
3. `MGIMO_RESEARCH_TO_IMPLEMENTATION.md`, «Решение для реализации» — фактическое решение оставить файлы и добавить инструмент лишь после воспроизводимого дефекта. Текущие `docs/submission-architecture.md`, «Persistence and evidence»/«Architecture tradeoffs», подтверждают отсутствие deterministic runtime/validator. Исторический план CLI не выдаётся за реализованную функцию.
4. `canonical-skill-routing-20261113.md` — исторически root route не требовал чтения skill; исправление теперь видно в AGENTS. Это закрытая проблема, не новый текущий дефект.
5. F8 run 1 — несуществующий §1 и неправильная интерпретация отсутствующего denominator; follow-up целевой и подсказанный, не доказательство причинного улучшения.
6. F9 — исправлены пропущенная ошибка записи и неоднозначность текущего claim. Current files сохраняют историю; остаётся пробел общей публикации. Branching successors C-003/C-005 к C-002 проверены: state/decision явно выбирают C-005; действующего дефекта consumer не установлено.
7. `docs/release/preprod-report.md`, «Execution boundary», и unseen activity фиксируют прошлые нарушения процесса shell. В этом аудите они не повторялись; это не найденный exploit продукта.

## 6. Собственные проверки данных

Успешно выполнены JSON-reader jq projection для unseen `sources.jsonl`, `evidence.jsonl`, `claims.jsonl` и Codex `sources.jsonl`, `evidence.jsonl`, `claims.jsonl`. В этих выдачах подтверждены читаемость записей и перечисленные IDs; **не** полный schema/cross-reference/secret audit всего repo. Activity просмотрены текстом, не заявлен comprehensive parser run.

Независимый reader-расчёт по вручную переписанным и сверенным шести CSV-строкам unseen case:

```text
select(.id=="E-003") |
{generated:([3,3,3,3,3,3]|add), opened:([2,3,1,2,3,2]|add), orders:([1,2,0,1,1,1]|add)} |
.+{opened_per_generated:(.opened/.generated), orders_per_generated:(.orders/.generated), orders_per_opened:(.orders/.opened)}
```

Запрос выполнен через `read` selector на `cases/unseen-shelf-alerts-20261114/evidence.jsonl`. Output: generated 18, opened 13, orders 6; ratios 0.7222222222222222, 0.3333333333333333, 0.46153846153846156. Это проверка суммы/деления с ручной транскрипцией, не независимый CSV-parser, не outcome attribution. Результаты согласованы с E-003. Первый jq-запрос ошибочно применил `map` к отдельному JSONL object; получил `Cannot index string with string ("id")`, затем заменён на per-record projection. Ошибка аудитора раскрыта, файл не менялся.

## 7. Внешняя конкурсная provenance

Повторно открыты [landing](https://challenge.mgimo.ai/) («ИИ-проект», «Как участвовать», FAQ 05/07) и [регламент](https://challenge.mgimo.ai/rules), редакция 22.10.2026, §§3.2, 4.1, 5, 6, 7. Подтверждены cabinet-only assignments, срок, captain submission, четыре критерия по 10 баллов и условия прав. **Не подтверждено** точное совпадение `docs/contest-brief.md` с файлом кабинета и содержание дополнительного демо. Локальный текст используется как пользовательский рабочий контракт; неизвестность provenance не останавливала исследование.

## 8. Где искать результаты

[Технические findings](technical-findings.md), [продуктовое ревью](product-review.md), [contest gaps](contest-gap-analysis.md), [адресный ресерч](research-findings.md), [архитектурные решения](architecture-decisions.md), [roadmap](implementation-roadmap.md), [итог и независимая перепроверка](final-verdict.md). Пределы reviewer independence и cross-examination фиксируются в итоговом отчёте, отдельно от исторических self-reports.
