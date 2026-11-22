# Evaluation и доказательства

Дополнительный срез 22.11.2026: [второй учебный кейс LinguaStep, источник подтверждения нового чата и отдельные проверки privacy-safe экспорта](release/final-20261122/README.md). [Итоговые release-проверки](release/final-20261122/RELEASE_RESULTS.md) не переоценивают прежние FAIL и не являются новым live E2E.

## Текущий срез — 2026-11-22

В основном репозитории доступны два независимых учебных кейса: 11 альтернатив, четыре стратегии и два плана проверки. Исходный LinguaStep R0001 прошёл новый чат Resume; публичный D0001 отдельно прошёл файловые проверки. Основной main `385e1d2` до добавления финального PDF имеет [CI SUCCESS](https://github.com/EdYaRdx/megafon_hack/actions/runs/45055668569): 121 тест, **116 passed + 5 Windows-only skipped**, 0 failures/errors; repository checker PASS, 302 Markdown-файла. [Актуальные main runs](https://github.com/EdYaRdx/megafon_hack/actions?query=branch%3Amain) показывают последующие документационные commits.

[Финальная submission readiness](release/submission-ready-20261122/README.md) отдельно фиксирует текущий Windows suite, классификацию обоих checkpoint, проверку приложенного PDF, ссылок/anchors, Mermaid и новых документов. [PDF «Ромашка MISIS»](MGIMO_FINAL_REPORT.pdf) включён без изменения байтов. Ссылки PDF на `ed42fef` и CI релизного `aa4b23f` — намеренные исторические срезы; они не объявляются свежим CI main. Нового E2E, интервью или пилота при этой упаковке не выполнялось.

## Исторический проверенный release — 2026-11-21

**Основной продуктовый пример — [реальный видеокейс семейной помощи](video-e2e.md), не прежний prepared demo.** Его release-упаковка прошла файловые/CLI-проверки; полный результат работы в новом чате на видео подтверждён владельцем. Это разные классы доказательств: ни CI, ни запись одного учебного кейса не доказывают бизнес-эффект, полную host qualification или независимую human acceptance.

| Уровень | Подтверждённый результат | Точный источник / граница |
|---|---|---|
| Детерминированные release-проверки | D0003: `VALIDATED_CANDIDATE` → `CHECKPOINTED`; inventory без drafts/issues; перенесённая копия без `.git` даёт тот же результат; два arithmetic replay совпали с сохранёнными JSON | [Curated receipt](release/video-family-e2e-receipt.json), `commands`, `relocated_without_git`, `arithmetic_replays_match_saved_json`; не новый live model E2E |
| Unit tests и repository checker | Windows, CPython 3.12.14: 121 tests / 69.542 s / `OK (skipped=5)` / exit 0; checker PASS, 262 Markdown files | [Фактическая release-верификация](release/video-family-e2e-20261121.md#фактическая-release-верификация); пять symlink-privilege skips, не продуктовая приёмка |
| CI интегрированной упаковки PR #30 | Unit tests + Repository checker: SUCCESS на `0f27bef` | [CI run](https://github.com/EdYaRdx/megafon_hack/actions/runs/44939925462); не измерение качества модели |
| E2E, наблюдавшийся владельцем | Естественный запрос, первый вход/проверка шести Skills, PDF, шесть альтернатив, выбор PO, стратегии R0002, fresh-session Resume и критический R0003 | [Видео](https://drive.google.com/file/d/1kDBIVW_hgRwh2WnttYouUtfnlhtD27P_/view), 9:58 **по владельцу**; полный независимый просмотр/повтор не выполнен, raw session не опубликована |
| Выборочные кадры видео | На 300 s — Codex TUI, UI-метка `GPT-6.1-Sol high`; на 410 s — запрос Resume и `speed x10` | Та же запись; наблюдения отдельных кадров при release-подготовке, не точный provider/API model ID, billing или полный E2E verdict |
| Сохранённые результаты дела | D0001–D0003, вводы человека, sources/evidence/claims, две стратегии, план проверки, отчёт пересмотра | [Навигация по артефактам](video-e2e.md#открыть-тот-же-этап-что-на-видео); преобразованные source receipts не выдаются за новые CLI-прогоны |
| Независимые статические reviews | ReleasePackageReview: `correct`, findings none; ReleasePrivacyReview: findings `[]` | [Release-отчёт](release/video-family-e2e-20261121.md#фактическая-release-верификация); ограниченный read-only scope упаковки, не runtime/security certification |
| Бизнес/полевая проверка | **UNKNOWN / NOT RUN:** спрос, причинный эффект, GP, окупаемость, сроки, M/O/C/I; пилот и бюджет не одобрены | [Текущее состояние](../cases/family-multinumber-video/state.md), [пересмотр](../cases/family-multinumber-video/research/D0003/review.md) |

Это доказательства **указанного release и указанных команд**, не результат новых тестов этой документационной правки. Предыдущие испытания и их исходы доступны отдельно в [техническом архиве](archive/evaluation-history-20261121.md).

## Что именно проверено в видеокейсе

### Целостность и восстановление

Опубликована отдельная обезличенная производная копия [`cases/family-multinumber-video`](../cases/family-multinumber-video/README.md): D0001 → D0002 → D0003. [EXPORT](../cases/family-multinumber-video/EXPORT.md) и [export-map](../cases/family-multinumber-video/export-map.json) фиксируют 98 сопоставленных исходных файлов, собственные D manifests и 15 исторических ledger-prefix mappings. Она сохраняет результаты, но **не является исходными байтами R0001–R0003**.

Свежие release-команды сохранены в [receipt](release/video-family-e2e-receipt.json):

- `commands[label="derivative gate"]`: `VALIDATED_CANDIDATE`, D0003 digest `10b175b51789466e0b4858ff58c609149dd75d478db321b04c2a843677520626`;
- `derivative classify`: `CHECKPOINTED`;
- `derivative resume inventory` и `relocated no-git resume inventory`: выбран D0003, drafts/issues пусты;
- activity hint видим и ожидаем: A-050…A-053 добавлены после закреплённого A-049 и описывают завершение, не автоматически выбранный draft;
- `source_unchanged_files=98`, `existing_demo_unchanged_files=131`, `derivative_unchanged_by_checks_files=100`; `json_jsonl_files_parsed=30`.

`check-candidate` проверяет ancestry и шесть root/snapshot пар; один `classify` не следует выдавать за полную проверку истории. CLI inventory не восстанавливает рассуждение модели и не доказывает cross-host E2E. Неподписанные исторические source records не являются независимой аттестацией исполнения.

### Аналитический результат и его границы

В D0001 есть шесть направлений; в [сохранённом решении PO](../cases/family-multinumber-video/inputs/user-choice-D0002.md) выбран **B — помощь уже подключённым семьям**, не обозначение B прежнего demo. D0002 содержит две стратегии; [D0003 review](../cases/family-multinumber-video/research/D0003/review.md#что-изменено-относительно-d0002) показывает критический пересмотр без удаления прошлых ревизий.

Пересмотр снял прогнозное прочтение сценария без эффекта, необоснованную ресурсно-календарную уверенность и обязательность минимума третьего года. Он **не выдумывает арифметическую ошибку D0002** и не утверждает, что выбранное направление доказанно выгодно или бесперспективно.

Учебная граница: `GP = 279 000 000 + 500M + O − C`; цель требует `500M + O − C ≥ 6 000 000`. При **условных C=O=0** — 12 000 дополнительных оплаченных номеро-месяцев. Это не семьи, не sample, не прогноз; M/O могут быть отрицательными, I отдельно. Release replay обоих расчётов выполнен **на временной копии**; результаты совпали с сохранёнными JSON ([receipt](release/video-family-e2e-receipt.json), два последних `commands`). Исторические writers не запускались в оригинале или authoritative derivative.

План разделяет P0 диагностику, P1 usability, P2 клиентский исход с назначением по семье и P3 оплату исходных когорт. Наличие плана не означает его выполнения. Реальные частоты причин, baseline/n/пороги, M/O/C/I, люди, даты и смета UNKNOWN. Следующий D1 об ограниченной диагностике ещё не принят; `approvals.jsonl` пуст, пилот/бюджет/контакты с клиентами не разрешены.

### Ошибки, вмешательство человека, время и стоимость

- [Activity A-004…A-016](../cases/family-multinumber-video/activity.jsonl): NameError из-за кавычек, отсутствующие PDF dependencies, недоступный browser access и minimized CUA windows, неудачный WinRT AsTask overload; сохранены retry links. Успешный путь — WinRT render 11 страниц → визуальное чтение → дополнительный OCR. ПО не устанавливалось.
- A-042: draft metadata loss обнаружена и исправлена до публикации; это не failed published checkpoint. [Release-отчёт](release/video-family-e2e-20261121.md#фактическая-release-верификация) также фиксирует нерабочий системный `py -3.12` (`encodings`) и использование уже установленного рабочего Python без смены policy.
- Человек предоставил бриф, согласовал точный CASE, определил учебный scope, выбрал B, запретил пилот/бюджет и поручил критический пересмотр ([вводы](video-e2e.md#открыть-тот-же-этап-что-на-видео)). Эти решения не являются независимыми human reviews. Отсутствие любой иной операторской помощи не установлено.
- На выборочном кадре наблюдается Codex и UI-метка модели; точные host version/provider/API model ID/reasoning полной сессии, calls/tokens/billing, общий elapsed и активное время PO — **UNKNOWN** ([state](../cases/family-multinumber-video/state.md), «Cost/time/call telemetry»). Исходное `model: UNKNOWN` не переписано. 9:58 — owner-reported длительность видео с ускоренным фрагментом; время Python-команды и suite не равно времени решения или model compute. Телеметрия прежнего demo не переносится.

### Статические reviews и происхождение

[Source/privacy reviews и финальные package/privacy reviews](release/video-family-e2e-20261121.md) проверяли конкретные файлы и упаковку. Исходный личный profile prefix в 22 файлах стал причиной отдельного derivative, а не публикации оригинальных байтов; значения путей не воспроизводятся. PDF, 11 PNG и OCR сохранены побайтово. Не выявленные в review credentials/клиентские записи не означают полной DLP или hostile-document гарантии.

PDF SHA-256 `558d2c665caa4f4954135c8bbfb69d791e398dcdc5b625d5ded7bdb2d0eb0fa5` совпадает с прежним demo. [Получение этих байтов со страницы задания подтверждено владельцем](submission-checklist.md#публикация-основного-репозитория); независимой сверки кабинета/версии и отдельной лицензии нет. Видео опубликовано, [подлинный кадр результата](assets/README.md) добавлен из него. Старые «видео не предоставлено» внутри case history относятся к моменту упаковки. Полный безопасный просмотр, права передачи, доступ жюри и факт подачи — отдельные действия владельца.

## Что не следует заключать

- Нет контролируемого доказательства ускорения, экономии, преимущества над обычным чатом или причинного улучшения решений.
- Нет полевой валидации спроса, финансового результата, окупаемости или готового утверждённого пилота.
- Нет общей clean-host/cross-host certification, гарантии автоматической активации Skills, arbitrary interrupted-write recovery, injection resistance или enforced least privilege.
- Unit/CI PASS и reviews упаковки не являются human/product/security/contest acceptance. Формальный offline evaluator оценивает сохранённые артефакты по [своему контракту](functional-evaluator.md), а не запускает агента.

## Исторические испытания

[История квалификации и прежние планы](archive/evaluation-history-20261121.md) сохраняет FAIL/BLOCKED/REVIEW_REQUIRED, ограничения harness и границы прошлых H1/F1–F6/H02. Они не переименованы в PASS и не заменены новым CI. Это отдельные scope испытаний, не оценка готовности новой документации. [Технический архив](archive/README.md).
