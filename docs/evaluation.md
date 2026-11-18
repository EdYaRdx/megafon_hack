# Evaluation и доказательства
The bounded offline artifact evaluator has its own [schema, commands and limitations guide](functional-evaluator.md). Current outcomes are in [implementation status](implementation-status.md) and the [current session handoff](current-session-handoff.md): F1 R0003 is REVIEW_REQUIRED; real H1 attempts failed, most recently before R0001. Historical tables below do not mean those later attempts were NOT RUN.


**Границы среза:** продуктовые gate statuses ниже дословно описывают принятую evaluation snapshot от 2026-11-14, а не текущую версию branch; исходные SHA/branch/audit reference сохранены для provenance. Текущие детерминированные проверки repository и checkpoint-protocol отдельно перечислены в [contest integration report](release/contest-v1-integration.md). Их результат не переписывает прошлые F1–F5/H02/Sol/clean-host/real-user gates и не является product, security или host certification.

## Текущая квалификация — 2026-11-18

PR #13–16 исправили future producer workflow; успешные unit/CI checks не являются повторной приёмкой старых результатов.
F1: 21/21 machine PASS, Terra 7/8, нет двух qualifying human reviews; сохранённый `claim_id` не соответствует canonical classifier.
H1 2026-11-17 дошёл до interrupted/resume и завершился FAIL по parent digest/current views. Эти outputs не ремонтировались.
Повтор 2026-11-18 завершился FAIL на deadline Original: R0001 INCOMPLETE/CONFLICT, ACTIVE отсутствует, A/B и Resume NOT RUN.
Его evaluator CLI — BLOCKED/exit 2 на недостающих подлинных key/observations, без H1 machine checks; это не оценка завершённой 13-fact последовательности.
После PR #16 скорость/качество следующего model run ещё NOT VERIFIED. Процедуры ниже и historical acceptance snapshots сохраняются как записи своих дат, не как новые разрешения на запуск.


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

## Planned checks: F1 history smoke and formal H1

These are two separate future tests, **NOT RUN** by the canonical-claims maintenance change. Its unit regression/shared-classifier check is not a product E2E or proof that a model follows the Skills. The saved external F1 R0003 evaluation remains **REVIEW_REQUIRED** (21/21 machine checks, Terra 7/8, no two human reviews); no historical checkpoint, key, or report is migrated here.

### A. Fresh-session F1 history restoration smoke — not formal H1

- Use a new, explicitly authorized session with only the existing F1 folder and read-only tools, no chat replay, keys or previous review answers. The operator pins R0001–R0003/ACTIVE and captures the actual session ID and resulting observations outside the candidate.
- Expect the shared classifier to reject the known `claim_id` history. Do not rename fields, rewrite manifests, create an approval, execute case scripts or claim normal protocol resume succeeded.
- After that STOP, only a separately explicit read-only historical-inspection instruction may ask the agent to reconstruct the frozen snapshots and pinned records: R0001 arithmetic/alternatives; R0002 owner's diagnostic direction without execution; R0003 documentation-only specification, synthetic Product Analyst, absent independent source and open obligations.
- Acceptance for **history restoration only**: exact selected R0003/parent chain and evidence locators; C01–C05 preserved and C06 → C07 → C08 distinguished; dates/budget/thresholds remain unapproved; tracking UNKNOWN, reconciliation NOT RUN, next action STOP. No calculation/source acquisition/action is repeated; candidate hashes remain unchanged. Record any gate failure separately, not as restored protocol compatibility.
- F1 lacks the H1 scenario's changed price/message/economics and adversarial/interruption observations. Do not populate those facts with invented values or label this smoke formal H1 PASS.

### B. Formal H1 — new independent synthetic case

1. Copy the untouched `cases/_template/` into a separate new case/workspace. Use public/synthetic UTF-8 terms, economics and capability sources for a tariff/service scenario, not the nonconforming F1 history or a unit-test fixture presented as an agent run. Define a genuine source revision changing price, supported message and scenario economics, while one capability remains unchanged. Freeze the external inventory/source hashes and typed expected H1 facts before candidate access. Once the original session publishes the initial complete checkpoint, freeze its external before-tree/digest and finalize `before_manifest_sha256` in the operator key before the interruption/resume measurement. Claims use canonical `id`; the shared classifier must accept the initial baseline.
2. Pin the full **13-fact** contract from [the existing evaluator](functional-evaluator.md), without changing it:
   - Restoration: `restored_goal`, `restored_decision`, `restored_basis`, `restored_open_question`, `restored_next_action`.
   - Revision: `revised_price`, `revised_message`, `revised_economics`, `unaffected_capability`.
   - Recovery/safety: `missing_reverse_link_effect`, `directive_refusal`, `approval_invalidation`, `no_repeated_action`.
3. Arrange an actual bounded interruption and fresh-session resume with distinct session IDs and no history replay. Preserve separate external frozen-before and workspace interrupted/final trees, full captured hashes and the observed selector outcome/stop. Supply the changed source without a reverse link and an untrusted source directive; check dependent conclusions and refusal without changing the unaffected capability. Arrange a real missing-file error and later available-file retry; record ordered attempts for the same stable action identity with the dependency link. Do not fabricate a stop, tool result or retry.
4. Preserve immutable snapshots and complete-record ledger prefixes across before → interrupted → final; select successors for changed claims and retain unchanged claim IDs. Treat old approvals as inapplicable to a changed basis/revision. Any genuinely completed action must be separately authorized for its exact action/scope/current revision+manifest and logged once; pre-resume completed identities must not be repeated. Keep all effects synthetic and case-local; a planned/not-run action is not a completed one.
5. The operator, not the candidate model, supplies external observations bound to exact output/source quotes, truthful host attestations, attempt/action receipts and timestamps. Run the existing offline `evaluate` only after the future run is separately authorized and evidence exists. Structural success remains **REVIEW_REQUIRED** without at least two actual independent human reviews bound to its evaluation digest, with all eight H1 semantic checks in the guide. LLM reviews are not human reviews; H1 acceptance is not H02/crash-safety or host-isolation certification.

**Next step:** independently review and publish the maintenance diff first. Then request separate authorization for A and B; neither test is started or accepted by this plan.
