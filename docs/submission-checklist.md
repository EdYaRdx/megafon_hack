# Конкурсная подача — checklist и текущие gates

Это checklist незавершённых действий, не заявление о приёмке или подаче. Рабочий конкурсный scope взят из [предоставленного contest brief](contest-brief.md); точное происхождение/актуальность относительно кабинета организатора не установлены.
Статусы dynamic acceptance ниже сохраняют evidence scope из 2026-11-14 baseline; свежие local repository/protocol checks, review и GitHub merge зафиксированы отдельно в [contest-v1 integration report](release/contest-v1-integration.md). Локальный unit-test PASS не закрывает acceptance/host/contest gates.

## Текущие gates

| Пункт | Статус | Следующее подтверждение |
|---|---|---|
| Product-first docs and repository checks | Local verification and independent read-only review are recorded in the [integration report](release/contest-v1-integration.md); PR #6 is merged to GitHub `main` | Local tests and classifier pass on the merged tree. No CI checks were configured. The CRLF-aware diff check has three retained, checksum-pinned historical whitespace findings; see the report. |
| Dynamic E2E | **CONDITIONAL**, ограниченный single-host synthetic scope | Выполнить только разрешённую приёмку по конкретному утверждённому scope; не расширять claim без evidence |
| Targeted F1–F5 | **NOT ACCEPTED** — defect test harness/checker | Исправить и независимо проверить harness перед новыми зачётными выводами |
| F6 provenance | Ограничение provenance | Уточнить допустимый evidence/provenance claim по audit source |
| H02 | **BLOCKED** | Получить/зафиксировать отсутствующее доказательство или решение владельца; не подменять статус |
| Latest independent Sol acceptance sign-off | **PENDING** | Дождаться независимого sign-off по dynamic acceptance; historical preprod audit не замена |
| Official MegaFon demo brief | Нет в доступных материалах; public note указывает на личный кабинет | Уполномоченный капитан сверяет актуальный документ и передаёт по разрешённому каналу |
| Видео, документ/screenshots, доступ жюри, human acceptance, фактическая подача | Не подтверждены | Подготовить, просмотреть и проверить по актуальному brief; зафиксировать подачу отдельно от readiness |
| GitHub visibility / LICENSE | Решение владельца | Проверить доступ жюри до конкурса; не менять visibility и не назначать лицензию без решения владельца |

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
