# Evaluation и доказательства

**Границы среза:** продуктовые gate statuses ниже дословно описывают принятую evaluation snapshot от 2026-11-14, а не текущую версию branch; исходные SHA/branch/audit reference сохранены для provenance. Текущие детерминированные проверки repository и checkpoint-protocol отдельно перечислены в [contest integration report](release/contest-v1-integration.md). Их результат не переписывает прошлые F1–F5/H02/Sol/clean-host/real-user gates и не является product, security или host certification.

## Acceptance snapshot — 2026-11-14 baseline

| Проверка | Статус | Что именно означает |
|---|---|---|
| Dynamic E2E | **CONDITIONAL** | Только ограниченный single-host synthetic scope. Это не full clean-host, не общая host acceptance и не product/contest acceptance. |
| Targeted F1–F5 | **NOT ACCEPTED** | Не считать результаты подтверждением product behavior: выявлены дефекты test harness/checker. Требуется исправить тестовую процедуру до нового зачётного вывода; повторные прогоны не выполнялись здесь. |
| F6 | **PROVENANCE LIMITATION** | Ограничение происхождения/подтверждаемости данных; не превращать в продуктовый PASS или дефект, пока provenance gap не закрыт. |
| H02 | **BLOCKED** | В текущем baseline этот gate не пройден; недостающую причину/доказательство не домысливать. |
| Sol acceptance | **PENDING** | Ожидается latest independent sign-off для динамической приёмки. |
| Product findings | P0/P1 не подтверждены в рассмотренном scope | Не означает полного аудита безопасности или отсутствия дефектов вне scope. |
| Clean-host / cross-host portability | Не сертифицированы | Формат и Skills документированы, но фактическую переносимость это не доказывает. |
| Официальный MegaFon demo brief | Не представлен в доступных материалах | Нельзя заключать, что organizer его не опубликовал: локальная заметка сообщает, что задание доступно в личном кабинете. |

### Не смешивать статусы Sol

`research/audits/sol-preprod-2026-11-14/` — **исторический статический preprod audit** со статусом CONDITIONAL. Он не является latest independent Sol acceptance sign-off по dynamic E2E; этот sign-off остаётся **PENDING**. `docs/release/preprod-report.md` — отдельный исторический release/process отчёт с собственными ограничениям и gate. Ни один документ нельзя переименовывать в текущую динамическую приёмку.

## Имеющиеся локальные свидетельства и пределы

- [Codex R1/R2 acceptance review](../research/qualification/host-acceptance/codex-0.169.0/20261114-r1-r2/acceptance-review.md) классифицирует сохранённый synthetic run как **PARTIAL PASS**. Источником является пакет saved artifacts и пользовательская provenance summary; raw session logs не представлены/не проверялись в указанном review. Это не доказывает automatic Skill activation, успешность каждого host call, clean-host reproducibility или общий E2E PASS.
- [Preprod audit verdict](../research/audits/sol-preprod-2026-11-14/final-verdict.md) — статический независимый аудит своего scope, **CONDITIONAL**; не runtime test.
- [F1–F3 synthetic evaluation plan/results](../research/sol-audit/evaluation-plan.md) — исторические fixtures и исследовательские прогоны, не приемлемые результаты F1–F5 этого нового targeted acceptance gate.
- [Clean-host runbook](clean-host-e2e-runbook.md) задаёт процедуры, но строки `NOT RUN`/будущие проверки не являются результатами.
- [Официальный brief availability note](../research/qualification/official-demo-brief-availability.md) фиксирует публичную страницу MGIMO Challenge на 2026-11-13: текст говорит о partner assignment в личном кабинете; проверенная публичная страница не раскрывала сам MegaFon brief. Личный кабинет не открывался; содержимое/версия задания неизвестны.

## Ограничения исследования

Примеры и прогоны основаны на synthetic/user-supplied материалах и ограниченном наборе публичных методических источников. Они не устанавливают реальный спрос, поведение клиентов, unit economics, причинность, безопасность host, полную стоимость, преимущество перед обычным чатом или production readiness. Не подтверждены полный clean-host acceptance, cross-host portability, official demo workflow, видео и подача. План теста не равен выполненному тесту.
## Риски, дефекты и незакрытые границы

### Известные product risks / findings

- Независимый исторический Sol preprod audit описал ограниченные P2 product/method findings: неучёт eligible starters с abandonment в draft task-success denominator; преждевременная фиксация retention D30 semantics; неполное concise memo/source locator contract; unsupported interpretation of orders/opens as conditional conversion. Locators, caveats и reviewer challenge — в [technical findings](../research/audits/sol-preprod-2026-11-14/technical-findings.md), [product review](../research/audits/sol-preprod-2026-11-14/product-review.md) и [final verdict](../research/audits/sol-preprod-2026-11-14/final-verdict.md). Эти scoped findings не исправлялись этим repository documentation change; старые output/ledgers не менялись.
- В reviewed scope нет подтверждённых product P0/P1. Это ограниченное наблюдение, не доказательство отсутствия дефектов вне scope или security certification.

### Test infrastructure defects

- Targeted F1–F5 — **NOT ACCEPTED** из-за defects test harness/checker. Сохранённые exploratory результаты не подменяют этот gate. Исправления harness и повторные accepted runs не входят в эту структуру/doc change.
- F6 ограничен provenance; точный status и открытые границы — в [implementation status](implementation-status.md).
- Новый `tools/check_repository.py` проверяет только синтаксис JSON/JSONL в `cases/` и existence относительных Markdown targets в указанном product/developer scope. Его PASS не говорит о продуктовой функциональности, schema correctness, hashes, semantic references или поведении host.

### Непроверенное поведение

- Dynamic E2E остаётся **CONDITIONAL** только в ограниченном synthetic single-host scope; H02 **BLOCKED**; latest independent Sol acceptance sign-off **PENDING**.
- Clean-host acceptance, cross-host portability, автоматическое обнаружение/исполнение Skills, arbitrary interrupted-write recovery, общая injection resistance и enforced least privilege не сертифицированы.
- В рамках этой repository задачи full E2E, H02, paid research, массовые agent experiments, host acceptance и fault injection не запускались.

### Конкурсные blockers

- Официальный supplementary MegaFon demo brief и его provenance/version не проверены; доступные project records сообщают о задании в личном кабинете, который не открывался.
- Видео, полный submission package, human acceptance и факт подачи не подтверждены. Contest checklist остаётся отдельным gate; отсутствие этих подтверждений не означает, что organizer не публиковал brief.

### Отложенные улучшения

- Исправить и независимо принять F1–F5 harness/checker до новых выводов.
- Снять F6 provenance limitation и закрыть H02; получить latest independent Sol acceptance sign-off.
- Получить разрешённый clean-host proof; проверить cross-host только если заявляется portability.
- Разрешить scope-specific product findings из Sol audit до изменения затронутых product contracts; не менять старые outputs задним числом.
- Утвердить case schema/versioning and migration contract перед любым несовместимым изменением.

См. [development guide](development.md) для разграничения product tests и harness checks. Ни одна из перечисленных deferred items не обозначена как завершённая этим изменением.

Для актуальных gates см. [implementation status](implementation-status.md); для классификации всех исторических материалов см. [research index](../research/README.md).
