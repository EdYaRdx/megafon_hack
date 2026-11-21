# История инженерных испытаний

Сохранённая часть прежнего evaluation: отрицательные исходы и ограничения не переоценены. [Текущие доказательства](../evaluation.md) относятся к новому видеокейсу и его release.

## Текущая квалификация — 2026-11-18

**Исторический срез, не текущая дата release.** Точные версии, хронология и ссылки: [handoff 18.11](../current-session-handoff.md), [implementation status](../implementation-status.md), [чек-лист с прежними gates](../submission-checklist.md).

| Испытание | Сохранённый результат |
|---|---|
| F1 R0003 | **REVIEW_REQUIRED:** 21/21 machine PASS, Terra 7/8, нет двух qualifying human reviews. Исторический `claim_id` несовместим со штатным classifier; историю не мигрировали |
| Ранний H1 Original | Checkpoint **FAIL**; последующие исправления предназначены для будущих результатов |
| H1 17.11 | Реальные Original/interruption/fresh Resume, итог **FAIL**: parent digest R2 отсутствовал, current views расходились |
| Ранний repeat 18.11 | **FAIL** на `Deadline exceeded` Original; R1 INCOMPLETE/CONFLICT, ACTIVE отсутствует; A/B/interruption/Resume NOT RUN, evaluator BLOCKED/exit2 без H1 checks |
| Trial на PR #17 | Original R1 CHECKPOINTED, реальный выбор и отдельные approvals, A once; первый fresh Resume оставил R2 incomplete по deadline, полный trial **FAIL** |
| Отдельно разрешённый Resume-only после PR #18 | На новой копии genuine R1 получен CHECKPOINTED R2, 29/29 machine PASS, evaluator **REVIEW_REQUIRED/exit3**; реальные missing→retry, блокировка старого B, нет повтора A |

Последний результат — retrospective mixed-version engineering qualification, **не новый blind/single-version full H1 PASS**. Семь H1 semantic checks документально поддержаны, context_restored qualified/partial из-за нормализованных labels. LLM review стратегий не нашёл P1/P2 в своём scope; reviewer model/effort UNKNOWN, двух genuine human reviews нет. Локальный операторский пакет вне Git не раскрывается как raw session. Поздний успех не переписывает прежние FAIL.

## Acceptance snapshot — 2026-11-14 baseline

**Исторический baseline.** Его версии и evidence references сохранены в [implementation status](../implementation-status.md), [Codex R1/R2 review](../../research/qualification/host-acceptance/codex-0.169.0/20261114-r1-r2/acceptance-review.md) и [Sol final verdict](../../research/audits/sol-preprod-2026-11-14/final-verdict.md).

| Проверка | Исторический статус и предел |
|---|---|
| Dynamic E2E | **CONDITIONAL**, ограниченный synthetic single-host scope; не full clean-host или contest acceptance |
| Targeted F1–F5 | **NOT ACCEPTED** из-за defects test harness/checker; exploratory fixtures не заменяют принятые результаты |
| F6 | **PROVENANCE LIMITATION**, не PASS и не установленный дефект продукта |
| H02 | **BLOCKED**; не закрыт текущей документацией или release smoke |
| Latest independent Sol dynamic sign-off | **PENDING**; статический preprod verdict не заменяет sign-off |
| Product P0/P1 | Не подтверждены в reviewed scope, не доказано отсутствие вне scope |
| Clean-host / cross-host | Не сертифицированы |
| Официальный brief в материалах того среза | Не был представлен; позднее подтверждение владельца приведено выше, прошлое наблюдение не переписано |

### Не смешивать статусы Sol

[Sol preprod audit](../../research/audits/sol-preprod-2026-11-14/final-verdict.md) — исторический **статический** CONDITIONAL, не latest independent dynamic acceptance. [Preprod process report](../release/preprod-report.md) — отдельная датированная запись. Имена reviewer/модели не следует выдавать за genuine human review.

### Имеющиеся локальные свидетельства и пределы

[Codex acceptance review](../../research/qualification/host-acceptance/codex-0.169.0/20261114-r1-r2/acceptance-review.md) дал **PARTIAL PASS** по saved artifacts и пользовательской provenance summary без проверки raw session. [F1–F3 evaluation plan](../../research/sol-audit/evaluation-plan.md) содержит исторические fixtures/процедуры, не accepted F1–F5 results. [Clean-host runbook](../clean-host-e2e-runbook.md) — процедура, не выполненный тест. [Brief availability note](../../research/qualification/official-demo-brief-availability.md) описывает публичную страницу на 13.11, не содержимое личного кабинета.

### Ограничения исследования

Учебные/user-supplied материалы и методические источники не устанавливают реальный спрос, unit economics, причинность или production readiness. Отсутствие видео и official brief в старых срезах — историческая граница, не актуальное утверждение, что новой записи нет.

### Риски, дефекты и незакрытые границы

#### Известные product risks / findings

Sol audit сохранил scoped P2 findings: abandonment в task-success denominator, преждевременные D30 semantics, неполный memo/locator contract, unsupported orders/opens interpretation. Оригинальные основания: [technical findings](../../research/audits/sol-preprod-2026-11-14/technical-findings.md), [product review](../../research/audits/sol-preprod-2026-11-14/product-review.md). Этот документационный release не исправляет старые outputs и не переоценивает эти findings.

#### Test infrastructure defects

Исторические targeted F1–F5 остаются NOT ACCEPTED, F6 ограничен provenance. Современный repository checker подтверждает свой targets/syntax scope, не schema correctness, hashes всех дел, semantic references или поведение host.

#### Непроверенное поведение

H02 BLOCKED и отсутствие независимой полной host/human acceptance не закрыты. Новых paid trials, массовых экспериментов, fault injection и full clean-host E2E в этой документационной задаче не запускали.

#### Конкурсные blockers

Историческое отсутствие official brief/видео не переносится в текущий release: owner-confirmed происхождение PDF и существующая видеоссылка приведены выше. Актуальные внешние gates — права передачи, безопасная запись, доступ жюри, требуемые PDF/screenshots, human acceptance и подача; отсутствие подтверждения не означает FAIL проведённого CLI smoke.

#### Отложенные улучшения

Новые claims по targeted acceptance потребуют исправленной и независимо принятой процедуры; claims по full H1/H02/переносимости — отдельных разрешённых испытаний и соответствующего review. Исторические материалы не ремонтируют задним числом. [Development guide](../development.md) разделяет product tests и harness checks; [research index](../../research/README.md) хранит датированную историю.

## Historical planning record — canonical-claims maintenance

Это сохранённый смысл прежнего плана, **не текущий запуск или allowance**. Более поздние фактические результаты перечислены в срезе 18.11; старые checkpoints/key/reports не мигрировали.

### A. Fresh-session F1 history restoration smoke — not formal H1

Планировалось read-only восстановление точной F1 history в новой явно разрешённой сессии без chat replay. Штатный classifier должен остановиться на известном `claim_id`, а не «исправить» историю. Только отдельное разрешение на historical inspection позволяет разобрать snapshots, successor chain и сохранённый STOP. Такой smoke не проверяет все H1 изменения/ошибки/действия и не означает formal H1 PASS.

### B. Formal H1 — new independent synthetic case

План требует отдельного синтетического дела из шаблона, заранее замороженных источников и typed expected facts; реальных Original/interruption/fresh Resume без истории; изменения условий и недоверенной директивы; actual missing→retry; сохранённой истории, применимых approvals и отсутствия повтора завершённого действия. Наблюдения и ключ предоставляет оператор вне candidate. Полный 13-fact контракт и восемь semantic checks — в [functional evaluator](../functional-evaluator.md). Без двух настоящих независимых human reviews, связанных с evaluation digest, machine success остаётся REVIEW_REQUIRED.

Новый trial требует отдельного разрешения. Этот план не объявлен выполненным в настоящем документационном release и не является H02/crash-safety/host-isolation certification.
