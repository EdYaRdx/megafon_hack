# Конкурсная подача — checklist и текущие gates

Актуализация 21.11.2026: **реальный запуск из видеозаписи — отдельный [видеокейс](video-e2e.md)**; прежний [prepared walkthrough](contest-demo.md) сохранён, PantryPath остаётся дополнительным. Видео и fresh-session Resume сообщены владельцем; сам файл/URL и доступ жюри здесь не проверены. [Отчёт текущей упаковки](release/video-family-e2e-20261121.md) отделён от исторического RC ниже. Получение PDF непосредственно со страницы задания MGIMO AI Challenge подтверждено владельцем. [Открытая страница конкурса](https://challenge.mgimo.ai/), FAQ05, указывает на задания в личном кабинете; опубликованный дедлайн — 22.11.2026 23:59 МСК. Независимая проверка кабинета/версии не проводилась. Это checklist, не заявление о подаче.

## Публикация основного репозитория

- **Решение владельца, 21.11.2026:** готовить к публичной конкурсной передаче существующий `EdYaRdx/megafon_hack`; обычные исторические пути и Git author metadata допускаются к публикации. Обязательная очистка истории или новый history-free репозиторий не требуются. Секреты, raw sessions и новые неразрешённые персональные данные этим не разрешены.
- **Независимый read-only аудит, 20.11.2026:** на main `d920f75c814176973d184fd367bb7c0add41cb99` проверены все доступные remote refs (25 branches, 26 PR heads, tags отсутствуют), локальные дополнительные/unreachable объекты и 41/41 доступных Actions logs; подтверждённых секретов не выявлено. Gitleaks 8.30.1 по доступной удалённой истории: exit0, findings0. Исторический Windows-profile path оценён как LOW privacy, не credential.
- **Граница аудита:** pattern scans не полная DLP-гарантия. Не исключены скрытые/удалённые server refs, внешние clones, недоступные прежние logs и произвольная конфиденциальная информация; Wiki включён в metadata, но его содержимое не просмотрено. При реальной утечке сначала отозвать credential: [рекомендации GitHub](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository).
- **PDF:** [происхождение подтверждено владельцем](contest-demo.md#источники-и-официальность), не независимой проверкой кабинета. Отдельная лицензия на PDF не установлена и не назначается этим PR; учитывать условия конкурса и правообладателя, не обещать неограниченное распространение.
- **Перед внешним доступом:** владелец проверяет Wiki и условия передачи материалов, отдельно меняет visibility и проверяет открытие/clone глазами жюри. На 21.11.2026 репозиторий PRIVATE, доступ жюри NOT VERIFIED; этот PR не меняет visibility, доступы или лицензию и не выполняет подачу.


## Текущие release gates

| Пункт | Статус RC | Что требуется |
|---|---|---|
| Реальный видео-E2E, 21.11.2026 | [`family-multinumber-video`](../cases/family-multinumber-video/README.md): отдельный D0001–D0003 от нового дела R0001–R0003 | Исходник не изменяется и не загружается; персональные пути обезличены в derivative. [Точные находки и фактические проверки](release/video-family-e2e-20261121.md); не смешивать со старым RC/D-кейсом |
| Основание сборки | Ветка `release/mgimo-contest-rc-20261120` от `origin/main` `7c55792db7f5153e9f8e56e7f346200532baa400`; это provenance, не результат проверки | Фактический scope и результат интеграционной проверки фиксируются в [contest RC verification](release/contest-rc-verification.md); до записи результата PASS не заявлять |
| Мобильный walkthrough | R0001 исследование → R0002 выбор PO → R0003 аудит; исходный R0003 receipt содержит CHECKPOINTED | Не выдавать исходный receipt за новый release/host acceptance; проверить фактический пакет после интеграции |
| Оригинальный CASE | Локальный R0001–R0003 не входит в основной репозиторий; его прежний publication=hold не является запретом PUBLIC для репозитория | Не переносить оригинал в этот PR и не редактировать R0001–R0003; для демонстрации использовать отдельный derivative |
| Публичный derivative CASE | Создан [`cases/mobile-product-strategy-demo`](../cases/mobile-product-strategy-demo/), независимая D0001–D0003, выбран D0003 от R0003 | [EXPORT](../cases/mobile-product-strategy-demo/EXPORT.md)/[export-map](../cases/mobile-product-strategy-demo/export-map.json) отделяют его от оригинала; фактический PASS — только по release verification, не исходным receipts |
| Происхождение PDF | **OWNER-CONFIRMED, 21.11.2026:** получен непосредственно со страницы задания MGIMO AI Challenge | Не выдавать подтверждение владельца за независимую сверку версии или отдельную лицензию на PDF |
| Описание решения | [Markdown для жюри](submission-description.md) подготовлен | PDF/скриншоты ещё не подтверждены; выполнить экспорт/просмотр отдельно, если требуются актуальным brief |
| Видео ≤10 минут | [Видеодемонстрация](https://drive.google.com/file/d/1kDBIVW_hgRwh2WnttYouUtfnlhtD27P_/view), **9:58 по сообщению владельца**; доступ к папке по ссылке подтверждён им. [Маршрут по результатам](video-e2e.md) | Кадры, звук, приватность записи и доступ жюри проверяет владелец; открытие landing page и CLI-проверки не заменяют просмотр видео |
| Модели, инструменты, время, стоимость | Для нового видео-дела — [текущий отчёт](release/video-family-e2e-20261121.md); [demo evidence](release/demo-evidence.md) относится только к прежнему делу | Называть только наблюдённые данные; отсутствующие call/time/cost telemetry — UNKNOWN; не переносить billing между делами |
| Human/product/host acceptance | Не закрываются Markdown, classifier или unit/CI | Отдельно зафиксировать фактическую приёмку и сохраняемые ограничения; прошлые результаты не переносить автоматически |
| Доступ жюри, visibility, LICENSE | На 21.11.2026 **PRIVATE**, `licenseInfo: null`; доступ жюри NOT VERIFIED; условия публикации — выше | Владелец отдельно выполняет смену visibility и проверку доступа; не назначать лицензию автоматически |
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
| GitHub visibility / LICENSE | Проверка 2026-11-18T18:39Z: repository PRIVATE, GitHub `licenseInfo: null`; jury access NOT VERIFIED | Исторический срез; текущее решение о публикации и ограничения аудита приведены выше, лицензия автоматически не назначается |

## Перед подачей

- [ ] Проверить актуальные требования и сроки конкурса, условия использования PDF и производных материалов; получение PDF со страницы задания уже подтверждено владельцем, отдельная лицензия не заявляется.
- [ ] Не включать локальные оригиналы обоих дел и не менять их историю. Для видео использовать `family-multinumber-video` D0001–D0003; `mobile-product-strategy-demo` D0001–D0003 — другое, прежнее дело; PantryPath — дополнительный пример.
- [ ] Провести требуемую приёмку на конкретном host и сохранить redacted evidence; отдельно назвать unobserved/blocked проверки.
- [ ] Исправить harness/checker defects до принятия targeted F1–F5 результатов; не объявлять эти результаты PASS задним числом.
- [ ] Закрыть H02 и получить latest independent Sol sign-off; статический historical preprod verdict не равен динамической приёмке.
- [ ] Проверить продуктовую рекомендацию, locators, denominators, три разных варианта, связанные стратегии и test plan.
- [ ] Просмотреть уже записанный по сообщению владельца новый E2E, проверить лимит до 10 минут, приватность и ссылку; не подменять проверку записи prepared outputs или CLI-прогоном.
- [ ] Проверить [описание для жюри](submission-description.md), подготовить требуемый PDF/screenshots отдельно; сверить [host/model/tools и затраты](release/demo-evidence.md), неизвестное оставить UNKNOWN; указать помощь человека и ошибки.
- [ ] Владельцу проверить Wiki, отдельно изменить visibility и убедиться в jury access к репозиторию/материалам. Не принимать pattern scan за гарантию отсутствия любых секретов.
- [ ] Получить human acceptance и подтверждение фактической captain submission; это отдельные статусы.

Результат новой видео-упаковки — в [отчёте 21.11.2026](release/video-family-e2e-20261121.md). Прежний RC зафиксирован отдельно в [release verification](release/contest-rc-verification.md); другие исторические доказательства — в [evaluation](evaluation.md) и [implementation status](implementation-status.md). Ни этот checklist, ни старые планы не означают закрытие gates.
