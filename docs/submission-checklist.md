# Конкурсная подача — checklist и текущие gates

Это checklist незавершённых действий, не заявление о приёмке или подаче. Рабочий конкурсный scope взят из [предоставленного contest brief](contest-brief.md); точное происхождение/актуальность относительно кабинета организатора не установлены.
Таблица сочетает текущие CI/F1/H1 сведения с явно сохранёнными historical dynamic acceptance gates 2026-11-14. Датированный [contest-v1 integration report](release/contest-v1-integration.md) не заменяет [текущий статус](implementation-status.md) и [handoff](current-session-handoff.md). Unit/CI PASS не закрывает product/host/contest acceptance.

## Текущие gates

| Пункт | Статус | Следующее подтверждение |
|---|---|---|
| Repository / CI | Проверенный merged main `afea4b8dfaf2cd59ef3ebbe0fa41955c859762ca`, PR #13–18 интегрированы; [CI success](https://github.com/EdYaRdx/megafon_hack/actions/runs/44356209988) | Deterministic compatibility не равна human acceptance/live demo; перед подачей сверить фактический HEAD/CI |
| F1 R0003 | REVIEW_REQUIRED: 21/21 machine PASS, Terra 7/8; исторический `claim_id` несовместим со shared classifier | Два квалифицированных human reviews отсутствуют; не менять старую историю и не использовать её formal H1 baseline |
| Последний отдельно разрешённый Resume-only | Genuine R1/исторический stop + fresh Resume на merged инструкциях: CHECKPOINTED R2;29/29 machine PASS, evaluator REVIEW_REQUIRED/exit3 | Retrospective mixed-version scope, не новый одно-версионный blind H1; два human reviews и проверка qualified restoration labels ещё нужны. Прежние FAIL сохранены |
| Dynamic E2E | **CONDITIONAL**, ограниченный single-host synthetic scope | Выполнить только разрешённую приёмку по конкретному утверждённому scope; не расширять claim без evidence |
| Targeted F1–F5 | **NOT ACCEPTED** — defect test harness/checker | Исправить и независимо проверить harness перед новыми зачётными выводами |
| F6 provenance | Ограничение provenance | Уточнить допустимый evidence/provenance claim по audit source |
| H02 | **BLOCKED** | Получить/зафиксировать отсутствующее доказательство или решение владельца; не подменять статус |
| Latest independent Sol acceptance sign-off | **PENDING** | Дождаться независимого sign-off по dynamic acceptance; historical preprod audit не замена |
| Official MegaFon demo brief | Нет в доступных материалах; public note указывает на личный кабинет | Уполномоченный капитан сверяет актуальный документ и передаёт по разрешённому каналу |
| Видео, документ/screenshots, доступ жюри, human acceptance, фактическая подача | Не подтверждены | Подготовить, просмотреть и проверить по актуальному brief; зафиксировать подачу отдельно от readiness |
| Подготовленный video/demo | Существующий script9:30 и PantryPath files доступны; текущий stock classify CHECKPOINTED | Это prepared synthetic artifact walkthrough, не новый live model run, запись или подача; приватный H1 не публиковать без разрешения |
| GitHub visibility / LICENSE | Проверка 2026-11-18T18:39Z: repository PRIVATE, GitHub `licenseInfo: null`; jury access NOT VERIFIED | Решение владельца о доступе жюри/visibility и лицензии; не делать репозиторий публичным и не назначать лицензию автоматически |

## Перед подачей

- [ ] Сверить официальный MegaFon brief, версию и сроки с уполномоченным аккаунтом; не использовать закрытые материалы без разрешения.
- [ ] Выбрать synthetic/public-data demo, пометить все synthetic элементы и хранить inputs/outputs раздельно.
- [ ] Провести требуемую приёмку на конкретном host и сохранить redacted evidence; отдельно назвать unobserved/blocked проверки.
- [ ] Исправить harness/checker defects до принятия targeted F1–F5 результатов; не объявлять эти результаты PASS задним числом.
- [ ] Закрыть H02 и получить latest independent Sol sign-off; статический historical preprod verdict не равен динамической приёмке.
- [ ] Проверить продуктовую рекомендацию, locators, denominators, три разных варианта, связанные стратегии и test plan.
- [ ] Записать и посмотреть видео (лимит по предоставленному brief — до 10 минут); не выдавать подготовленные repository outputs за live-generated.
- [ ] Подготовить полный документ/screenshots, host/model/tool list и фактическое время/затраты либо `UNKNOWN`; указать помощь человека и ошибки.
- [ ] Убедиться в jury access к репозиторию/материалам и проверить privacy/secret exposure отдельно. Локальный pattern scan не достаточен.
- [ ] Получить human acceptance и подтверждение фактической captain submission; это отдельные статусы.

Подробные доказательства и статус формулируются в [evaluation](evaluation.md) и [implementation status](implementation-status.md).
