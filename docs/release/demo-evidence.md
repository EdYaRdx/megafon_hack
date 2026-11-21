# Demo evidence: R0001–R0003

**Локальный оригинал R0001–R0003 не входит в основной репозиторий и не изменяется.** Его сохранённый publication=hold относится к исходному CASE, не является запретом PUBLIC для репозитория. Актуальное [решение владельца и ограничения аудита](../submission-checklist.md#публикация-основного-репозитория) заменяют прежние рекомендации о запрете публикации обычных исторических путей. Ниже — датированный preflight, не новая приёмка.

**Обезличенный derivative: VERIFIED — bounded packaging feasibility.** Фактические gate/classify прошли для `cases/mobile-product-strategy-demo`, независимой цепочки D0001–D0003. Окончательный D0003 digest: `07247dbb5e77d01d7f679e0b67ce21bb2efd2a2a397fc9798ab15c168c868d7d`; каноническое source→export соответствие — `export-map.json`. Это не human/billing/host acceptance и не подтверждение организаторского provenance. Итоговые tests, Resume и replay расчётов — в [release verification](contest-rc-verification.md).

Граница проверена чтением публичного derivative `cases/mobile-product-strategy-demo/EXPORT.md`, строки 3–11: оригинал не редактировался/не опубликован, derivative имеет новые hashes; `export-map.json` сопоставляет source/export bytes. Redacted historical receipts помечены `export_notice` и не являются новым PASS. Все исходные locators ниже относятся к локальному оригиналу R0001–R0003; в публичном derivative разрешать их через export-map, не считать исходные digests hashes преобразованных файлов. Исходные approvals не связывают D0001–D0003. PDF/PNG не изменены; получение PDF со страницы задания подтверждено владельцем 21.11.2026, отдельная лицензия не установлена.

Дата read-only preflight: 2026-11-20. Относительные исходные locators ниже относятся к локальному оригиналу `cases/mobile-product-strategy-fdadbbcb`; его абсолютное размещение для публичного отчёта не требуется. Это отчёт о сохранённых артефактах. Во время preflight demo-скрипты не исполнялись, case не менялся, private host sessions/auth/secrets не читались. Позднейшие фактические release-проверки отделены в verification.

## Что подтверждается

- OBSERVED: `ACTIVE.json` выбирает R0003, digest `8b23176b2975081d58721a1dd1cb695899caa29c5496a7ad8e44420cd820ced5`. `receipts/R0003-classify.json`, `stdout`, содержит CHECKPOINTED, exit 0; `R0003-gate.json`, `stdout`, VALIDATED_CANDIDATE. Это исторические receipts, не текущий PASS перенесённой копии.
- DOCUMENTED: `receipts/R0003-completion.json`, `ancestors_unchanged`, `historical_ledger_prefixes_preserved`, `approval_scope` фиксируют сохранение предков и только аналитическую публикацию. Не подтверждают продуктовый эффект, пилот, бюджет или готовность к запуску.
- Цепочка manifest: R0001 `7b97ae92c708880da11e53ba9c59089190bf53eed70a65d9d51c6d0f7d78cbf9` → R0002 `824eb11ef01cdb64792f8ebc5d5262b6b37e143bbc9582f5b49466c96c5df3c3` → R0003 выше (`revisions/R000{1,2,3}/manifest.json`, `parent_revision_id`, `parent_manifest_sha256`).

## Время, compute и расходы

Времена UTC, взяты из полей receipts, не из filesystem mtime. Строка date=2026-11-20 в activity не означает точное время каждого действия; часть UTC-событий приходится на 19 ноября. Записанное время события/receipt нельзя превращать во время работы модели или человека.

| Наблюдение | Подтверждённое время | Ограничение |
|---|---|---|
| Копирование PDF | `inputs/provenance.json: copied_at_utc` = 2026-11-19T22:20:39.4291588Z | Это не начало всей сессии |
| Начальный расчёт | `calculations/receipt.json: started_at_utc` 22:27:25.653533 → `finished_at_utc` 22:27:25.842210, 19 ноября | Разница 0.188677 s; процесс Python, не model compute |
| Расчёт R0002 | `calculations/R0002/receipt.json` 23:04:19.944656 → 23:04:20.095566, 19 ноября | 0.150910 s; не elapsed всей ревизии |
| Независимая арифметика | `drafts/r0003-independent-audit/calculation-receipt.json` 23:53:45.308962 → 23:53:45.473210, 19 ноября | 0.164248 s; не клиентское исследование |
| Аудит сохранён / integrity | `activity.jsonl: ACT-035` 00:00:22.186078 / `ACT-036` 00:01:15.311000, 20 ноября | Время записи, не длительность аудита |
| PO-решения записаны | `ACT-037` 00:06:31.232205 | Точный timestamp сообщения PO UNKNOWN |
| Финализация / публикация | `ACT-038` 02:34:08.499728 / `ACT-040` 02:34:54.664284 | Промежуток не равен model compute |

Разницы трёх расчётов вычислены детерминированно по UTC microseconds в JS при подготовке отчёта. Между копированием PDF и ACT-040 около **4 ч 14 мин 15 с** (15255.235 s при миллисекундной точности Date.parse). Это только elapsed между двумя наблюдаемыми маркерами: включает ожидание PO/паузы, исключает предшествующую работу и ничего не говорит о человеко-часах или скорости относительно ручной работы.

**UNKNOWN:** точная модель/провайдер demo, model compute, число вызовов, billed input/output/cached tokens, тариф, итоговая стоимость, активное время PO, общий бюджет и remaining monetary/time guard. Основания: `activity.jsonl: ACT-001, ACT-026, ACT-035–040`; `receipts/R0003-completion.json: telemetry`; раздел учёта `drafts/po-priorities-comparison/review.md`. Подписочная цена, guessed tokens и модель текущего release-сеанса не заменяют эти данные. Заявление журналов «нет платных внешних действий» не означает нулевую стоимость модели/инфраструктуры; подтверждающий billing receipt отсутствует.

## Человеческие решения и границы

- `ACT-001, ACT-007, ACT-011`: разрешены точный case path, создание и копирование пользовательского PDF; host escalation — разрешение доступа, не продуктовый выбор.
- `ACT-015`: вопросы о приоритетах первоначально без наблюдаемого ответа; R0001 сохраняет аналитическое воздержание (`ACT-028`).
- `drafts/po-priorities-comparison/review.md`, ввод и §5: PO уточнил GP ≥285 млн и семейную активность при выборе семейного направления; сам сегмент ещё не выбран.
- `inputs/R0002-owner-decision.md`; `ACT-030–032`: A выбран как исследовательский приоритет, не пилот/расходы/коммуникации.
- `drafts/r0003-independent-audit/{audit-input.md,owner-decision.md,review.md}`; `ACT-035–037`: ограниченный критический пересмотр и решения PO сначала оставлены DRAFT; это не параллельный действующий checkpoint.
- `inputs/R0003-owner-publication.md`; `approvals.jsonl: A-001`: отдельное разрешение exact-manifest аналитической публикации R0003. `approved_at` прямо говорит exact message timestamp UNKNOWN. Scope исключает research execution, pilot, budget, staffing и внешние действия.

## Фактически использованные demo-инструменты

DOCUMENTED по `activity.jsonl` (не утверждение о запуске в текущем release):

- ACT-002–007: PowerShell metadata, попытка `find_python.ps1` заблокирована policy; native `uv python find` offline с access-denied и разрешённой повторной попыткой; существующий Python 3.12, штатный `tools/case_workspace.py`. Policy не менялась, установка не заявлена.
- ACT-008–014: metadata/probes PDF-зависимостей; Windows.Data.Pdf, Windows.Media.Ocr ru, 11 PNG/TXT. `inputs/brief-extracted/render-receipt.json: exit_code=-1073741819`: аварийное завершение не PASS. Отдельно описана проверка сохранённых outputs/изображений.
- ACT-016–023: web search для discovery, открытие публичных MTS/T2 и FCA; локаторы и URL находятся в `sources.jsonl: S-002–S-007` и `research/notes.json`. FCA screenshot провалился (Cache miss); использовался открытый текст, не непрочитанные таблицы. Не было доступа к личным кабинетам/оплате.
- ACT-024–025, ACT-030, ACT-034: локальная Python-арифметика, запись curated ledgers, hash pins; это не реальные интервью, telemetry оператора или эксперимент. `calculations/*/receipt.json: runtime_version` и начальный receipt: Python 3.12.14.
- ACT-026–040, `receipts/*`: чтение/запись документов, apply_patch, штатный `case_protocol.py` recovery/check-candidate/classify, snapshots и selector-last. Exact host API names/model billing в полном объёме UNKNOWN.

**Разделение:** OMP используется для разработки/упаковки release, не runtime конкурсного продукта. Текущие read/bash/eval/write инструменты этого preflight и текущая Windows-среда не доказывают, что demo запускалось через OMP или с текущей моделью. Никакие текущие инструменты не добавлены задним числом в demo inventory.

## Privacy / public packaging: блокирующий вывод

OBSERVED личное имя присутствует в pinned байтах локального case. Ниже сохранены точные file/field locators, но личные значения заменены на `<profile>`; это обезличивание только отчёта, не source case и не его истории.

| Case-файл | Locator / данные | Pin |
|---|---|---|
| `inputs/provenance.json` | `original_path`: `C:/Users/<profile>/Downloads/Пример брифа.pdf` | R0001–R0003 files[] |
| `calculations/receipt.json`, `calculations/R0002/receipt.json` | `command_argv[0]`: `C:/Users/<profile>/AppData/Roaming/uv/python/…/python.exe` | files[] |
| `drafts/r0003-independent-audit/calculation-receipt.json`, `owner-decision-receipt.json`, `verification-receipt.json` | command/runtime receipts, вложенные command_argv | R0003 files[] |
| Те же три receipts под `revisions/R0003/dependencies/audit-source/` | byte-preserved copies | R0003 files[] |
| `receipts/R0003-recovery.json` | вложенные команды с user-profile executable | R0003 files[] |
| `receipts/{classify-R0001,gate-R0001,R0002-base-classify,R0002-classify,R0002-gate,R0003-classify,R0003-gate}.json`; `drafts/po-priorities-comparison/recovery-receipt.json` | command_argv, личный runtime path | Не входят в union manifests files[]; исторические supporting receipts |

Машинозависимы также cwd/script/input пути `<WORKSPACE>/…`, native Windows OCR и локальный session_id render receipt. Их наличие не требует прежнего user profile для чтения/hash-check, но не позволяет обещать portable rerun сохранённых команд.

**Нельзя молча redaction/нормализовать pinned файлы, пересоздать manifests или заменить историю:** это разрушит R0001–R0003/digests. Владелец уже отклонил публичную упаковку полного case; повторное разрешение раскрыть имя не запрашивается. Возможная будущая передача неизменяемого case требует отдельно авторизованного непубличного канала и прав на PDF/PO-ввод. Безопасный обезличенный пример нельзя выдавать за эту же историю. Исключение только «очевидно временных» receipts тоже недопустимо, если они pinned.

PDF preflight: прочитаны сохранённые OCR-тексты страниц 1–11. Стр.1 говорит «вымышленного мобильного оператора», стр.3 — «Все числа учебные»; реальные корпоративные метрики из этого не следуют. Участники/клиентские телефоны/реальная customer telemetry в прочитанном тексте не обнаружены. Это ограниченная проверка, не DLP-сертификат: OCR не покрывает надёжно каждый пиксель/вложение. Без исполнения demo-кода просмотрены доступные plaintext PDF metadata tokens: CreationDate/ModDate `D:20261118221532Z00'00'`, Producer с macOS; readable Author/Title в таком просмотре не найдены. Это не полная верификация metadata/embedded objects и не доказательство отсутствия персональных данных. `inputs/provenance.json` прямо фиксирует author/published_at UNKNOWN, organizer_original_independently_verified=false. Дата metadata не подтверждает автора/организатора. Разрешение копировать локальный PDF не равно лицензии публичного распространения. По публичному сайту challenge.mgimo.ai задания выдаются в кабинете (FAQ05); организаторский provenance этого PDF не подтверждён, кабинет не открывался.

## Минимальный dependency closure и Resume

**Точный manifest-level closure:** union `files[].path` трёх manifests плюс сами три manifests, с дедупликацией путей: **90 файлов**. Это минимальное множество для сохранения всех явно pinned зависимостей трёх ревизий, но не само по себе полный Resume UX. У union могут быть разные исторические hashes одного append-only ledger: сохранять текущие целые файлы, не обрезать до старого digest; prefix semantics должен проверять штатный protocol. Нельзя требовать, чтобы текущий полный ledger имел hash каждого исторического префикса.

Closure компактно, без неявных исключений:

- `activity.jsonl`, `approvals.jsonl`, `claims.jsonl`, `evidence.jsonl`, `sources.jsonl`.
- Все файлы `revisions/R0001/`, `revisions/R0002/`, `revisions/R0003/`, включая manifests, dependencies и `R0003/dependencies/audit-source/` (ровно существующее дерево).
- `inputs/Пример брифа.pdf`, `inputs/provenance.json`, `inputs/R0002-owner-decision.md`, `inputs/R0002-scenario.json`, `inputs/R0003-owner-publication.md`.
- `inputs/brief-extracted/page-01`…`page-11` каждое `.png` и `.txt`, плюс `render-command.txt`, `render-receipt.json`.
- `calculations/{calculate.py,run.py,results.json,receipt.json}` и те же четыре файла `calculations/R0002/`.
- `research/{notes.json,record_evidence.py,R0002-record.py,R0003-finalize.py}`.
- `receipts/R0003-recovery.json`.
- `drafts/r0003-independent-audit/{audit-input.md,calculate.py,calculation-receipt.json,calculation-results.json,owner-decision-receipt.json,owner-decision.md,strategy.md,verification-receipt.json}`.

**Добавить для рабочего checkpoint/Resume:** `ACTIVE.json`, `case-protocol.json`, текущие root `options.md`, `decision.md`, `strategy-product.md`, `strategy-communication.md`, `test-plan.md`, `state.md`; root `strategy.md`, `brief.md` и `README.md` для человеческого чтения. Они не заменяют immutable snapshots. Сохранить `receipts/` целиком как доказательства gate/classify/completion/handover (не исполняемые команды).

**Добавить для неослеплённого Resume по ссылкам и истории черновиков:** целиком все три `drafts/` папки, включая reviews, `before.json`, `state.md`, `record_review.py` и `po-priorities-comparison/recovery-receipt.json`. В частности verification receipt ссылается на исходные protected hashes; review объясняет, почему старый DRAFT не является текущей базой. Старые reviews сознательно содержат исторический статус R0001/R0002 — не переименовывать их в действующие решения по mtime. Вне 90-file union `research/checkpoint.py` и `research/R0002-checkpoint.py` — вспомогательные исторические scripts, не manifest requirement; для архивной полноты можно сохранить inert, запускать не нужно. В обследованном дереве не выявлены cache/temp каталоги, которые требовалось бы копировать; нельзя считать `drafts`, PNG или receipt временными только по названию.

Минимальный manifest closure выведен чтением JSON, не выполнением protocol. Actual Resume использует штатные release `tools/case_workspace.py`/`tools/case_protocol.py` и их зависимости вне case. Совместимость, read-only перенос в ZIP-like каталог и replay проверены отдельно — см. [release verification](contest-rc-verification.md); это не новый model/host acceptance.

## Что получить от человека перед окончательной заявкой

1. Для возможной непубличной передачи — отдельно авторизованный канал, получатели и права на PDF, производные PNG/TXT и точные PO-вводы; при необходимости согласование владельца/юриста. Публичное раскрытие имени не запрашивается: действует publication=hold, CASE исключён из safe PR. Историю не переписывать.
2. Подтверждение организаторского происхождения/применимости brief и разрешения использовать/передавать его; публичная страница и metadata этого не дают.
3. Provider usage/billing export только для этого demo, без credentials и raw host sessions: exact model ID, интервалы запросов, billed input/output/cached tokens, валюта/тариф/стоимость и attribution границы. Если нет — оставить UNKNOWN.
4. Учёт активного труда PO/автора, начала/конца/пауз и состава ручных действий, если требуется заявить человеко-часы. Не выводить их из elapsed.
5. Применимые contest disclosure/AI/tool/данные правила и разрешённый канал передачи. Не выдавать отсутствие замеченных secrets за полный security clearance.
6. Если требуется продуктовый запуск, отдельные PO решения/реальные данные и бюджет; текущий A-001 разрешает только аналитический checkpoint, не эти действия.

Этот preflight был read-only; source case сохранён без изменений. Результаты последующих tests/CLI не подменяют исторические receipts и опубликованы отдельно в verification.
