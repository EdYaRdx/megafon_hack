# Contest gap analysis

## Источник требований

**Организатор проверен напрямую:** [MGIMO landing](https://challenge.mgimo.ai/), «ИИ-проект», «Как участвовать», FAQ 05/07; [регламент](https://challenge.mgimo.ai/rules), редакция 22.10.2026, §§3.2, 4.1, 5.1–5.2, 6.2–6.4, 7.5–7.7. Получено 2026-11-14.

Подтверждены срок **22.11.2026, 23:59 МСК**, подача капитаном в кабинете, возможность замены до срока, задания в кабинете, четыре критерия и максимум десять баллов по каждому. Номинационные уточнения публикуются вместе с заданием (§7.6).

**Пользовательский рабочий контракт:** `docs/contest-brief.md` — подробное задание «Стратег Фабрики продуктов». Оно разрешено как scope, прочитано полностью. Точное совпадение с organizer original, обновления и дополнительный MegaFon demo brief **UNKNOWN**. Ни публичная landing, ни общий регламент не подтверждают отдельно обязательное видео ≤10 минут и все MegaFon-specific поля. Здесь они проверяются как supplied contract, не выдуманное official wording. Cabinet/account не открывались, credentials не запрашивались.

## Обязательная функциональность по supplied contract

`H/` = `research/qualification/host-acceptance/codex-0.169.0/20261114-r1-r2/`.

| Требование | Артефакт и наблюдаемое покрытие | Gap / gate |
|---|---|---|
| Уточнить размытую задачу | intake Skill, brief/state; fresh-start и Codex intake | Inputs часто уже содержат вопросы/ответы intake. Независимый sparse-brief сценарий без подсказок не доказан |
| Документы, таблицы, сайты | Markdown, CSV, HTML; public GOV.UK/AAPOR/Mixpanel citations | Не заявлять PDF/XLSX/audio/image capability без actual input test; webpage read не равно самостоятельный поиск |
| План от decision-changing questions | evidence-research п.1, brief open questions | Исследовательская инициатива и stop policy недостаточно доказаны в обычном clean host |
| Traceable evidence | Четыре журнала, source locators, current successors | Selected chains статически связны; T-01 receipt, T-04 attempt completeness; не full integrity validator |
| ≥3 разные альтернативы + status quo | В полноценных options есть status quo/discovery/launch/close | P-03: не все итоговые memo перечисляют их; held-out active-action alternatives не доказаны |
| Продуктовая стратегия | Audience/job, capability, alternatives, unknown economics | Реальный value/cost/revenue business case отсутствует; условная discovery-рекомендация не economic optimum |
| Коммуникационная стратегия | Обещания ограничены capability; внутренний memo | Нет validated customer positioning/channel choice; P-03 handoff gap |
| План проверки | Formula, comparator, guardrails, unknown prerequisites | P-01 completion denominator, P-02 premature retention definition; draft не launch-ready |
| Агент сам ведёт workflow | Root route и шесть canonical Skills | Output completeness/path mentions не доказывают automatic skill activation или самостоятельную постановку шага |
| Human participation | Pending owner, explicit external-action prohibition | Narrative gates наблюдаемы; version-bound approval и rejection stale consent не проверялись |
| Разделение знаний/state | Root instructions, references, inputs, ledgers, revisions | Архитектурно правильно, но current root START-HERE ведёт в dev infrastructure (T-05) |
| Продолжение после перерыва | Сохранённые R1/R2, Codex distinct-session summary | New-session execution исторически reported; arbitrary interrupted-write recovery UNVERIFIED (T-02/T-03) |
| Прозрачность действий/стоимости | Activity честно раскрывает ошибки и UNKNOWN | Полная стоимость пригодного результата и human-active time неизвестны; phase summary не полный receipt |
| Без hidden setup | README file-first | Clean single-host acceptance не установлен; T-05/T-06 мешают first use |
| Безопасность/разрешённые данные | Public/synthetic restrictions, no sandbox claim | Реальные host permissions, covert injection, секреты всего пакета не аттестованы |

## Дополнительный уровень: что можно честно заявлять

| Возможность | Текущая граница |
|---|---|
| Interview preparation / model respondents | Synthetic counts отмечены; реальные consented interviews не показаны. Не claim real demand |
| Изображения/audio/video | Нет проверенного workflow; **NOT DEMONSTRATED**, не обязательное внедрение до срока |
| Анализ UI/user journeys | Task-plan есть, но анализ реального интерфейса с visual locators не показан |
| Анализ данных | Synthetic arithmetic/cohort-mix reasoning есть; calculation tool зависит от host, receipts неполны |
| Поддержка принятого решения | Owner/review trigger поля есть; accepted-decision outcomes/overdue commitments не демонстрировались |
| Revising decisions | Новые constraints/counterexamples применены; полноценный reversal ранее принятой ставки не показан |
| Routing | Процедурная маршрутизация Skills есть; measured model/tool routing и error recovery не доказаны |
| Skills / hooks / subagents | Шесть Skills реализованы как файлы. Исторические dev task reviewers — не packaged product subagent feature. Hooks отсутствуют, это не дефект само по себе |
| MCP / CLI integrations | Product-specific runtime не включён и не нужен для минимального file-folder scope |
| Knowledge navigation | Files/IDs/lexical read; current successor в отдельных кейсах; semantic search не реализован и пока не обоснован |
| Failure recovery | Исторические error disclosures и исправления; нет fault-injection acceptance |
| Portability | Стандартные пути подтверждены docs, actual cross-host continuation UNKNOWN |
| Сравнение с baseline | Есть exploratory F1–F3/F9; matched performance/cost advantage UNKNOWN |

Число агентов, хуков или технологий не является самостоятельной ценностью: это прямо соответствует supplied brief. Не рекомендуется заполнять дополнительные возможности ради перечня.

## Submission package

| Артефакт | Состояние доказательств | Acceptance перед подачей |
|---|---|---|
| Доступный repo/архив | Доступен локальный checkout; remote/jury access здесь не проверялись и Git запрещён | Капитан/владелец проверяет link/access и exact submitted snapshot отдельно от этого аудита |
| Демонстрационный проект | Несколько synthetic cases и saved strategies | Сверить official demo brief/version; freeze raw inputs; не выдавать prepared outputs за live generation |
| Видео ≤10 минут | `docs/demo-video-script.md` — **план, не запись** | Реальная capture в выбранном host, genuine pause/new-session resume; просмотр полного файла, проверка длины и доступа |
| PDF/документ со screenshots | `docs/submission-architecture.md` — draft, есть stale claims | Architecture, модели/tools, ключевые инструкции, реализованные extras, время/расходы/ошибки/помощь и ограничения на одной current version |
| Human product acceptance | Основные решения pending | Назначенный владелец подтверждает результат/границы; это не разрешает внешние действия автоматически |
| Подача | Подтверждения в изученных материалах нет | Captain submit через кабинет; сохранить подтверждение последней версии до deadline |

G-02 — **P1 submission gate**. Отсутствие видео не делает аналитическую рекомендацию ложной, но не позволяет считать supplied package завершённым.

## Четыре критерия жюри — без выдуманных баллов

| Критерий | Доказанная сильная сторона | Главный риск оценки | Максимально полезный следующий proof |
|---|---|---|---|
| Проработанность | Осторожные claims, разные варианты, противопоставление vendor/CSV, запрет unsupported promises | Методические страницы вместо глубокого domain research; flawed denominator/metric; memo не самодостаточен | Исправленные P-01–P-04 + novel decision case с decisive evidence и ясным trade-off |
| Масштаб использования нейротехнологий | Skills, адаптивный анализ, tool-oriented инструкции | Нельзя засчитать dev reviewers как product subagents; routing/автономность не наблюдались | Показать агентом выбранное следующее действие и его проверенный результат; не добавлять framework ради novelty |
| Имплементация | Папка inspectable, saved state, исторические Codex R1/R2 | Prepared walkthrough не clean execution; interruption и host portability не доказаны | Авторизованный clean single-host end-to-end + genuine new session и controlled failure |
| Качество | Явные unknowns, источники и human gates | First-use T-05, conflicting T-06, unknown effort/cost, нет leader teach-back | Наблюдение незнакомого оператора, короткий decision memo, truthful run receipt |

Прогноз баллов отсутствует: нет независимого jury scoring, verified nomination-specific updates и полного demo package.

## Три раздельных acceptance-сферы

1. **Prepared synthetic walkthrough:** допустим с явной маркировкой prepared/synthetic, limitations и исправлением ошибочных summary claims. Показывает структуру и конкретные основания, не live execution.
2. **Clean single-host product acceptance:** новый case, raw inputs, actual reads/calculation/writes, permitted tools, genuine file-based continuation и error receipts. Codex summary даёт частичную historical provenance, не закрывает этот gate полностью.
3. **Cross-host portability:** второй host продолжает тот же case без chat history и публикует согласованную новую ревизию. Дополнительная функция; не обязательна для честно ограниченного single-host demo. Если сохраняется project-defined двуххостовый gate checklist, его нужно пройти либо явно пересмотреть scope, а не молча объявить PASS.

## Rights и release process

[Регламент §§6.2–6.3](https://challenge.mgimo.ai/rules) описывает отчуждение исключительных прав при отправке. Это существенное решение капитана/правообладателей. Не делается юридический вывод, что любые OSS dependencies запрещены; сторонние права, лицензии и собственные материалы нужно различать. Нельзя обещать отчуждение прав, которыми команда не владеет. Default DEFER новых пакетов снижает дополнительную юридическую и операционную поверхность.

`docs/release/preprod-report.md`, Execution boundary/Release blocker, содержит прежний процессный FAIL. G-01 требует owner disposition, а не вечного запрета публикации. Историческая ошибка authentication не доказывает нынешнее отсутствие доступа; этот аудит текущие remote права не проверял.

## Приоритет до 22 ноября

Сначала official scope и release-process disposition; затем P-01–P-04/T-01/T-05/T-06 и честный clean single-host proof; затем финальный case/video/doc/доступ и подача. Широкие платформы, новые providers, OptiLLM и второй host без обещания portability — не на критическом пути. Подробные приоритеты/effort/acceptance — [implementation-roadmap.md](implementation-roadmap.md).
