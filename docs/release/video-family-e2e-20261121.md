# Видеокейс MGIMO / МегаФон — release-упаковка 21.11.2026

Статус: **release-упаковка готова к ручному review: smoke и штатные проверки PASS, два независимых финальных read-only review без actionable findings**. Окончательная конкурсная подача остаётся действием владельца после проверок записи, прав и доступа. Этот отчёт не подтверждает бизнес-эффект или новый live E2E.

## Основание и результат

- Ветка `release/video-family-e2e-20261121` от актуального `origin/main` `adbbc30` (PR #29 уже включён). Основная рабочая копия до этого оставалась на старой MVP-ветке; её незакоммиченные посторонние файлы не включаются.
- Вход: отдельное дело `family-multinumber-8c3e71a9`, **98 файлов, 6 501 901 байт**. Выполнены два независимых read-only source-review: CaseIntegrity и CasePrivacy. Ни один не запускал case helpers или тесты; их выводы ниже отделены от реальных CLI-проверок автора упаковки.
- Выход: [`cases/family-multinumber-video`](../../cases/family-multinumber-video/README.md), **D0001 → D0002 → D0003**, 98 сопоставленных артефактов + EXPORT и export-map. Из них 30 byte-identical; все PDF/PNG и OCR сохранены. 68 изменённых текстовых/control-файлов имеют самостоятельные hashes.
- Причина derivative: личный Windows-profile path в **22 исходных файлах**, включая pinned зависимости. Более широкое разрешение на раскрытие новых личных путей не предполагалось. Одного wrapper или удаления receipts недостаточно. Исходные R0001–R0003 не исправлялись и не отправляются в PR.
- [EXPORT](../../cases/family-multinumber-video/EXPORT.md) и [98-file export-map](../../cases/family-multinumber-video/export-map.json) фиксируют все соответствия, original/derivative hashes и точные границы 15 исторических ledger-prefix pins. Исторические hashes в тексте и stdout сохранены как source provenance, а не заменены якобы новыми результатами старого запуска.
- README ведёт к [маршруту по видео](../video-e2e.md), двум стратегиям, шести альтернативам, PDF, решению, расчётам, плану проверки и R0003. Прежний `mobile-product-strategy-demo` сохранён отдельно. Архитектура, Skills, протокол, CLI, tests и конфигурация продукта не менялись.

**Видео опубликовано:** [MGIMO_Hack_Demo_Final.mp4](https://drive.google.com/file/d/1kDBIVW_hgRwh2WnttYouUtfnlhtD27P_/view), длительность **9:58 по сообщению владельца**. Он подтвердил доступ к папке Google Drive по ссылке. По предоставленному URL открылась landing page с этим названием; воспроизведение, кадры, звук и фактический доступ жюри не проверялись. Ссылка добавлена только в release-документацию: derivative D0001–D0003, manifests и исходная история не менялись. Прежние замечания внутри сохранённого derivative об отсутствии URL относятся к моменту его упаковки.

## Целостность, восстановление и полнота

Штатные команды **актуального main** на неизменённом исходнике реально вернули:

```text
check-candidate <source-case> --revision R0003
  VALIDATED_CANDIDATE, manifest_sha256:
  90817278d2b39b8c29ea95a753ef55a16860d0f9db58903e71413e1fcaec67d6
classify <source-case>
  CHECKPOINTED
resume_context.inventory(<source-project>, <explicit-case>)
  CHECKPOINTED; confirmed R0003; drafts []; issues []
  hint: activity.jsonl changed or unpinned; unverified
```

`check-candidate` проверяет всю parent-chain и шесть root/snapshot пар; `classify` сам по себе не доказывает всю историю. Подтверждены R0001 → R0002 → R0003 и точные parent-manifest hashes. Все исходные manifest digests, производная цепочка и исторические префиксы — в export-map.

Исторический `research/R0003/restore-inventory-receipt.json` восстанавливает **R0002 до пересмотра**; `post-inventory-receipt.json` — R0003 после него. A-050…A-053 добавлены после закреплённого activity-префикса A-049; hint ожидаем и не скрыт. Это receipts завершения, не автоматически выбираемый draft. Исходные ошибки/retries A-004…A-016 сохранены. Свежий CLI inventory не является повторённым ответом модели в новом чате; успешный fresh-session Resume и запись видео — наблюдение владельца.

**Содержательный review:** R0001 — шесть путей и рекомендация без окончательного выбора; R0002 — PO выбрал B, помощь уже подключённым семьям; R0003 — критический пересмотр с сохранением направления. Решение, обе стратегии, пятичастный документ и план проверки присутствуют. Клиентский путь включает права/отзыв, несовместимый тариф, устаревшие сведения, отсутствие объёма, ошибку и подтверждённый итог. Коммуникация различает приглашение, условный сигнал, канал действия и подтверждение исполнения; готовые обещания эффекта не приписаны продукту.

Экономика: `GP=279000000+500M+O−C`; цель iff `500M+O−C≥6000000`. Только при условии C=O=0 необходимо M≥12000 дополнительных оплаченных номеро-месяцев. M/net O могут быть отрицательными, I отдельно. Верхние календарные оболочки 9/6/3 месяца и 1334/2000/4000 номеров — **не sample, охват или прогноз**. R0003 исправляет прогнозное прочтение reference, ресурсную уверенность и необоснованный минимум третьего года; не выдумывает арифметическую ошибку R0002.

План разделяет P0 причины/охват, P1 usability, P2 клиентский исход с назначением по семье и P3 оплату исходных когорт, включая выход из группы. Missing/failure/неоткликнувшиеся не исключаются ради результата; границы вреда и полномочий названы. При этом baseline/n/пороги, M/O/C/I, реальные частоты, критический путь, люди, даты и смета **UNKNOWN**. Нет собственного доказанного прогноза по пяти KPI и исполнимого утверждённого пилота. Это завершённый desk-пересмотр, **не полное эмпирическое бизнес-обоснование**. Следующее D1 о scope ограниченной диагностики не принято; пилот и бюджет не одобрены.

Исторический `brief.md` сохраняет intake/остановку R0002; он не текущий state. Историческая неточная shorthand-ссылка claims в R0002 исправлена в R0003, но старый текст не переписан. Текущую версию выбирает ACTIVE, не intake, mtime или последний журнал.

## Адресный privacy/security audit исходника

Независимый CasePrivacy проверил **все 98 файлов**: 86 текстовых, PDF, 11 PNG; все 11 страниц просмотрены, 11 OCR sidecars прочитаны, metadata/опасные PDF markers и PNG ancillary markers проверены статически. Полный индивидуальный inventory — `export-map.files[].source_path`. Это не полная DLP или сертификация безопасности PDF-парсера.

### P-01 — Medium privacy: личный профиль, 22 файла

Ниже **исходные** file/line/field locators; личное значение намеренно не воспроизводится. Для соответствующего derivative-файла используйте export-map (там есть D-переименование и добавленные provenance-строки).

| Исходный файл | Точный locator |
|---|---|
| `brief.md` | 7: путь исходного desktop PDF |
| `sources/S-001-reading.md` | 3: тот же путь |
| `activity.jsonl` | 23: A-023, details |
| `research/record.py` | 89: встроенная команда A-023 |
| `test-plan.md` | 62: executable исторического расчёта |
| `revisions/R0001/test-plan.md` | 52 |
| `revisions/R0002/test-plan.md` | 60 |
| `revisions/R0003/test-plan.md` | 62 |
| `research/calculation-receipt.json` | 3: command[0] |
| `research/check-candidate-receipt.json` | 3: command[0] |
| `research/post-selection-receipt.json` | 3: command[0] |
| `research/resume-inventory-receipt.json` | 3: command[0] |
| `research/R0002/check-candidate-receipt.json` | 3: command[0] |
| `research/R0002/post-selection-receipt.json` | 3: command[0] |
| `research/R0002/resume-inventory-receipt.json` | 3: command[0] |
| `research/R0003/build-receipt.json` | 3: argv[0] |
| `research/R0003/calculation-receipt.json` | 3: argv[0] |
| `research/R0003/check-candidate-receipt.json` | 3: argv[0] |
| `research/R0003/post-classify-receipt.json` | 3: argv[0] |
| `research/R0003/post-inventory-receipt.json` | 3: argv[0] |
| `research/R0003/restore-classify-receipt.json` | 3: argv[0] |
| `research/R0003/restore-inventory-receipt.json` | 3: argv[0] |

Решение: `<USER_HOME>` в отдельном derivative, без новых персональных раскрытий и без редактирования исходника. CaseIntegrity оценил это как HIGH **блокер original-byte публикации**, CasePrivacy — Medium privacy, не credential. Это разные оценки последствия; риск не скрыт и не выдан за компрометацию аккаунта.

### Остальные находки и ограничения

| ID / серьёзность | Точные свидетельства | Решение |
|---|---|---|
| P-02 / Low portability и раскрытие структуры workstation | cwd в 14 command receipts выше, строки 9/11/13; A-023; `research/record.py:89`; четыре `test-plan.md` | Checkout заменён `<WORKSPACE>`. Это исторические команды, не portable launch instructions |
| O-01 / Low operational hazard, не доказанная exploit-уязвимость | `calculations/run.py:69` пишет pinned results; `research/record.py:19` append; `checkpoint.py:31,49,61,85`; `R0002/revise.py:40,262–263`; `publish.py:30,65,85`; `R0003/build.py:36,147–149`; `control.py:21,34,81,88–89,138–139` | Генераторы сохранены как inert evidence; не запускать/импортировать при просмотре. Нет новых auto-hooks; replay только в disposable copy |
| I-02 / High integrity **при неправильной redaction** | ACTIVE; R0002/R0003 manifest parent fields; JSONL pins и source receipt stdout | Отдельные D manifests, собственные parent hashes, точные исторические префиксы; source receipts явно помечены, новые результаты вне case history |
| I-03 / Medium evidence limitation | Все сохранённые command receipts; `research/R0003/quality-review.json` | Неподписанные source records не являются независимой аттестацией исполнения. Свежие штатные проверки отделены ниже |
| Binary metadata / Low fingerprint, не PII/credential finding | PDF raw строки 401–402: Quartz/macOS Producer и creation/modification dates; catalog 398, trailer/document ID 1405 | PDF не переписан; Author/contact/JS/Launch/EmbeddedFiles/URI/forms/encryption markers в статическом просмотре не найдены |
| Временные файлы / no finding | Полный inventory; receipts, генераторы, OCR и render outputs относятся к истории | Caches/backups/посторонних временных payloads не выявлено; pinned файлы не удалялись |

Подтверждённых credentials, private keys, bearer tokens, email/телефонных контактов, приватных sharing/internal URLs и клиентских записей **не выявлено**. Внешние ссылки — публичные GOV.UK/Stripe method sources, сохранены атрибутированные пересказы, не полные сайты. Пустые поля/примерные placeholders будущих customer-полей не являются реальными абонентскими данными. Скрипты не показали download/install, credential harvesting, shell=True или обфусцированный payload. PNG-визуальный review не выявил данных аккаунта; marker-поиск не заменяет полный chunk/CRC parser.

## PDF и права — отдельно от security

SHA-256 PDF `558d2c665caa4f4954135c8bbfb69d791e398dcdc5b625d5ded7bdb2d0eb0fa5` **совпадает побайтово с уже включённым PDF прежнего демо**. Применено уже записанное [подтверждение владельца](../submission-checklist.md#публикация-основного-репозитория) о получении этих байтов непосредственно со страницы задания; нового права или лицензии этим PR не назначено. Source S-001/brief.md сохраняют прежнее UNKNOWN независимой provenance-проверки. Независимой сверки кабинета/версии нет. Фраза об использовании/адаптации на странице 1 PDF не объявляется общей лицензией на распространение. Не установлено нарушение; условия конкурсной передачи и правообладателя остаются проверкой владельца.

## Фактическая release-верификация

Новый [curated receipt](video-family-e2e-receipt.json) сохраняет фактические команды, stdout/stderr/exit и runtime CPython 3.12.14; executable/cwd обозначены placeholders. Это не raw host session и не изменённый source receipt.

| Проверка | Наблюдённый результат | Граница |
|---|---|---|
| D0003 check-candidate + classify | VALIDATED_CANDIDATE; CHECKPOINTED; digest `10b175b51789466e0b4858ff58c609149dd75d478db321b04c2a843677520626` | Полная ancestry/шесть root views и выбранная D-chain, не качество стратегии |
| Resume inventory | D0003; drafts/issues пусты; activity hint сохранён | Только CLI, не новый model/host acceptance |
| Relocated/ZIP-like copy | Без `.git` и исходного дела восстановлены те же confirmed/unfinished; case не изменён | Скопированы штатные tools, private profile/прежний checkout не нужны |
| Арифметика | Два фактических Python replay на disposable copy совпали с сохранёнными JSON | Первичный writer не запускался в оригинале/authoritative derivative; pinned bytes восстановлены только в disposable copy перед audit |
| Файлы и карта | 98/98 исходных и 131/131 прежнего demo unchanged; 100/100 derivative не изменены checks; 30 JSON/JSONL разобраны | Проверены все export hashes и 15 пар исторических prefix hashes; source/profile/credential-marker scan не полная DLP-гарантия |
| Штатный unittest suite | PASS: 121 tests за 69.542 s, OK (skipped=5), exit 0; CPython 3.12.14 / Windows | Пять symlink-privilege skips сохранены; новый live E2E/бизнес-эффект этим не подтверждены |
| Repository checker | PASS: 262 Markdown files; indexed case JSON/JSONL syntax; exit 0 | `python -B -X utf8 tools/check_repository.py`; targets/syntax, не fragments/внешние URLs/семантика. Новые 30 case JSON/JSONL отдельно разобраны smoke до включения в Git |

Никаких case mutation helpers в оригинале или authoritative derivative не запускалось. Исторические source hashes не выдаются за D hashes; source PASS не заменяет эти свежие результаты.

Команда suite: `python -B -X utf8 -m unittest discover -s tests -v` через проверенный executable. Raw вывод содержит реальные временные/profile пути и намеренно не копируется в Git. Первый системный `py -3.12` оказался нерабочим из-за отсутствующего `encodings`; использован уже установленный рабочий CPython 3.12.14 без установки или изменения policy. Ошибки подготовки текста (prewrite JS SyntaxError и неверный якорь отчёта) исправлены до финальных checks; исходник ими не менялся. Throwaway smoke launcher/его локальные baselines удалены после сохранения curated результата.

Независимый **ReleasePackageReview**: `correct`, findings none, confidence 0.92. Read-only source comparison проверил сохранение содержания, 98-file map, D-chain, все 15 исторических prefix mappings, шесть root views по recorded hashes, source receipt labeling и навигацию. Новых проверок/пересчёта hashes этот reviewer не запускал; фактический runtime smoke приведён отдельно выше.

Независимый **ReleasePrivacyReview**: findings `[]`, publication-blocking defects не выявлены. Проверены все **100 derivative-файлов** и изменённые release-документы, включая escaped receipts, snapshots, generators, map, OCR, PDF metadata и все PNG ancillary markers. Личных profile literals, credentials, private URLs, customer records, temp/raw sessions не найдено. Оставлены явно обозначенные Low PDF fingerprints и риск явного запуска mutation helpers; видео, права и доступ — owner gates. Review статический, не полная DLP/hostile-document гарантия; prior visual review/byte-continuity использованы как ограниченный контекст, а не выданы за новые замеры.

CaseIntegrity/CasePrivacy были отдельными исходными исследовательскими lanes; ReleasePackageReview/ReleasePrivacyReview — свежим review готовой упаковки. Ни один reviewer не редактировал исходник/продукт и не выполнял тесты; автор упаковки не заменял независимый review самосертификацией.

## Что должен подтвердить владелец

1. Просмотреть **саму запись**: правильное новое дело, безопасные кадры/пути/уведомления, отсутствие secrets, звук и возможность просмотра жюри. Ссылка теперь предоставлена; длительность 9:58 и доступ к папке по ссылке подтверждены владельцем, не независимым просмотром. Успех Resume на видео не перепроверялся новым model run.
2. Условия конкурсной передачи PDF и производных материалов, применимость актуальных требований и готовность команды принять их. Получение PDF уже owner-confirmed, отдельная лицензия/независимая organizer authentication не заявляется.
3. Доступ жюри к репозиторию и видео, Wiki/прочие внешние поверхности и требуемый документ/PDF/screenshots. Репозиторий при preflight **PRIVATE**; доступа жюри не проверяли. Смену visibility/доступов выполняет только владелец отдельно.
4. Human/product acceptance и окончательную подачу капитаном до 22.11.2026 23:59 МСК. Historical QA gates не превращены в PASS, отсутствующие model/call/total-time/billing данные нового дела остаются `UNKNOWN`; telemetry старого demo не переносится.

Эта упаковка не требует раскрывать личное имя или пересогласовывать продуктовую архитектуру. Никакого merge, force-push, изменения visibility/лицензии, релизного тега, продуктового запуска или конкурсной заявки не выполнялось.
