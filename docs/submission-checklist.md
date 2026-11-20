# Конкурсная подача — checklist и текущие gates

Это checklist release candidate 20.11.2026, **не заявление о приёмке или подаче**. Основной prepared walkthrough — [мобильный кейс](contest-demo.md); PantryPath остаётся дополнительным. Официальность user-supplied PDF не установлена. [Открытая страница конкурса](https://challenge.mgimo.ai/), FAQ05, указывает на задания в личном кабинете; публичный дедлайн — 22.11.2026 23:59 МСК. В кабинет в рамках подготовки не заходили.

## Текущие release gates

| Пункт | Статус RC | Что требуется |
|---|---|---|
| Основание сборки | Ветка `release/mgimo-contest-rc-20261120` от `origin/main` `7c55792db7f5153e9f8e56e7f346200532baa400`; это provenance, не результат проверки | Фактический scope и результат интеграционной проверки фиксируются в [contest RC verification](release/contest-rc-verification.md); до записи результата PASS не заявлять |
| Мобильный walkthrough | R0001 исследование → R0002 выбор PO → R0003 аудит; исходный R0003 receipt содержит CHECKPOINTED | Не выдавать исходный receipt за новый release/host acceptance; проверить фактический пакет после интеграции |
| Публикация оригинального CASE | **BLOCKED — owner publication=hold**: личные пути в неизменяемой истории | Оригинал остаётся локально вне release-worktree, не входит в PR/clone; подготовлен отдельный derivative ниже. R0001–R0003 не редактировать |
| Публичный derivative CASE | Создан [`cases/mobile-product-strategy-demo`](../cases/mobile-product-strategy-demo/), независимая D0001–D0003, выбран D0003 от R0003 | [EXPORT](../cases/mobile-product-strategy-demo/EXPORT.md)/[export-map](../cases/mobile-product-strategy-demo/export-map.json) отделяют его от оригинала; фактический PASS — только по release verification, не исходным receipts |
| Официальный PDF | **UNKNOWN**; публичная страница не подтверждает происхождение примера | Уполномоченный капитан отдельно сверяет актуальное задание и допустимость распространения; не входить в кабинет автоматически |
| Описание решения | [Markdown для жюри](submission-description.md) подготовлен | PDF/скриншоты ещё не подтверждены; выполнить экспорт/просмотр отдельно, если требуются актуальным brief |
| Видео ≤10 минут | [Сценарий мобильного кейса](demo-video-script.md) подготовлен, запись **NOT CONFIRMED** | Записать/просмотреть, убрать личные пути и секреты; prepared walkthrough не называть live-run |
| Модели, инструменты, время, стоимость | [Demo evidence](release/demo-evidence.md) — отдельный источник | Называть только наблюдённые данные; отсутствующие call/time/cost telemetry — UNKNOWN |
| Human/product/host acceptance | Не закрываются Markdown, classifier или unit/CI | Отдельно зафиксировать фактическую приёмку и сохраняемые ограничения; прошлые результаты не переносить автоматически |
| Доступ жюри, visibility, LICENSE | Проверено: **PRIVATE**, `licenseInfo: null`; доступ жюри NOT VERIFIED. Старые Git-коммиты содержат персональный путь | Не делать текущий репозиторий публичным. После решения о правах — snapshot-архив без `.git` или новый history-free репозиторий; новая лицензия/очистка истории требуют решения владельца |
| Фактическая подача | **NOT CONFIRMED** | Отдельное подтверждение капитана; readiness не является submission |

## Сохранённые historical gates — не текущий acceptance

Ниже сохранены прежние CI/F1/H1 сведения и dynamic acceptance gates, включая провалы. Они не переоценивались в этой документационной правке. Датированный [contest-v1 report](release/contest-v1-integration.md), [implementation status](implementation-status.md), [handoff](current-session-handoff.md) и [evaluation](evaluation.md) сохраняют свой scope; их результаты нельзя переносить на RC.

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
- [ ] Сохранить выбранный hold: не включать полный mobile CASE в PR, не раскрывать имя профиля и не менять историю. Проверить безопасный readable walkthrough; full-case reproducibility для clone/жюри не заявлять. PantryPath — дополнительный.
- [ ] Провести требуемую приёмку на конкретном host и сохранить redacted evidence; отдельно назвать unobserved/blocked проверки.
- [ ] Исправить harness/checker defects до принятия targeted F1–F5 результатов; не объявлять эти результаты PASS задним числом.
- [ ] Закрыть H02 и получить latest independent Sol sign-off; статический historical preprod verdict не равен динамической приёмке.
- [ ] Проверить продуктовую рекомендацию, locators, denominators, три разных варианта, связанные стратегии и test plan.
- [ ] Записать и посмотреть видео (лимит по предоставленному brief — до 10 минут); не выдавать подготовленные repository outputs за live-generated.
- [ ] Проверить [описание для жюри](submission-description.md), подготовить требуемый PDF/screenshots отдельно; сверить [host/model/tools и затраты](release/demo-evidence.md), неизвестное оставить UNKNOWN; указать помощь человека и ошибки.
- [ ] Убедиться в jury access к репозиторию/материалам и проверить privacy/secret exposure отдельно. Локальный pattern scan не достаточен.
- [ ] Получить human acceptance и подтверждение фактической captain submission; это отдельные статусы.

Текущий результат RC фиксируется только в [release verification](release/contest-rc-verification.md). Исторические доказательства остаются в [evaluation](evaluation.md) и [implementation status](implementation-status.md). Ни этот checklist, ни старый план не означают закрытие gates.
