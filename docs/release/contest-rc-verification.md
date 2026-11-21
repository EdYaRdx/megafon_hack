# Contest RC — 2026-11-20

Статус: **RC подготовлен для ручного review; окончательная конкурсная подача BLOCKED**. Это датированный release report, не новый продуктовый benchmark или human acceptance. Результаты ниже отделяют исходную историю, производный экспорт и проверки релиза.

**Актуализация 21.11.2026:** последующий аудит доступной истории не выявил подтверждённых секретов; владелец допускает обычные исторические пути/Git author metadata и подтвердил получение PDF со страницы задания MGIMO. Прежний запрет PUBLIC только из-за путей снят; [текущие условия и ограничения](../submission-checklist.md#публикация-основного-репозитория). Ниже сохранены результаты и provenance прежнего прогона, не новая приёмка и не лицензия на PDF.

## Основание и разрешения

- Отдельный worktree/ветка `release/mgimo-contest-rc-20261120` создан от обновлённого `origin/main` `7c55792db7f5153e9f8e56e7f346200532baa400`. Исходные рабочие каталоги и тестовые копии не редактировались.
- Владелец запретил раскрытие имени профиля/персональных локальных путей, затем явно разрешил исследовать и подготовить обезличенный **производный** экспорт с отдельной hash-chain. Оригинальные R0001–R0003 и receipts не редактируются, их доказательства не подменяются.
- GitHub API `gh repo view EdYaRdx/megafon_hack --json visibility,licenseInfo,url`: на момент preflight репозиторий **PRIVATE**, `licenseInfo: null`. Видимость и лицензия не менялись; доступ жюри не проверен. PR не является публичной публикацией или конкурсной отправкой.
- Независимый privacy-review нашёл персональный путь в унаследованном `.omp/profiles/qualification-supervised.yml`. В текущем дереве он заменён более широким запретом `C:/Users`; профиль не активировался, глобальные настройки не менялись. Старые Git-коммиты содержат прежние bytes. Историю не переписывали; последующий аудит оценил путь как LOW privacy, не credential, а владелец разрешил такую историческую метаинформацию к публикации.

## Официальность брифа — BLOCKED

[Страница организатора](https://challenge.mgimo.ai/), открыта 20.11.2026: раздел «ИИ-проект», «Как участвовать» и FAQ05 отсылают к заданию в личном кабинете. FAQ07: до 22.11.2026, 23:59 МСК. Публичная страница не подтверждает идентичность предоставленного PDF текущему брифу трека. В кабинет и пользовательские браузерные сессии не входили.

В исходном `inputs/provenance.json`: `organizer_original_independently_verified=false`, автор/дата UNKNOWN. PDF SHA-256 `558d2c665caa4f4954135c8bbfb69d791e398dcdc5b625d5ded7bdb2d0eb0fa5`; стр.1 — вымышленный оператор, стр.3 — учебные числа. **Не заявляется, что официальный бриф проверен.** Капитану нужны разрешённые свидетельства из кабинета: название/версия/дата/ссылка, совпадение файла или объяснение отличий, права на распространение PDF и производных материалов. FAQ12 о передаче прав организатору также требует осознанного решения команды; новую лицензию автоматически не назначали.

## Состав и границы демонстрационного пакета

[Публичный по составу кейс](../../cases/mobile-product-strategy-demo/README.md) содержит исходный учебный PDF и 11 PNG/TXT, обе стратегии и пятичастный документ, альтернативы, PO-вводы, расчёты, curated ledgers, историю черновиков и checkpoint-зависимости. Он подготовлен для публикации в PR, но не является подтверждением внешней доступности.

- **D0001–D0003 — не оригинальные R0001–R0003.** [EXPORT.md](../../cases/mobile-product-strategy-demo/EXPORT.md) объясняет преобразования; [export-map.json](../../cases/mobile-product-strategy-demo/export-map.json) содержит соответствия путей/исходных и производных hashes. Исторические названия R в содержательном тексте относятся к исходной работе.
- Штатный `checkpoint-v1`, classifier, Skills и продуктовый протокол не менялись. Пересчитаны только manifests/parent chain/selector производной копии, control IDs, revision-directory locators и обезличенные зависимости; Markdown снабжён предупреждением. Содержательные решения/неизвестное сохранены, оригинальный R0003 не правился ради PASS.
- D0003 manifest: `07247dbb5e77d01d7f679e0b67ce21bb2efd2a2a397fc9798ab15c168c868d7d`. Исходный R0003: `8b23176b2975081d58721a1dd1cb695899caa29c5496a7ad8e44420cd820ced5`. Это разные цепочки.
- Исторические receipts дополнены `export_notice`: их команды, timestamps, hashes, PASS/approval относятся только к источнику. Для redacted файла проверяют **export hash** в карте; исходный hash в старом receipt не должен совпадать с redacted bytes. Карта — запись преобразования автора, не независимая аутентификация закрытого оригинала.
- Source approvals не связывают D0001–D0003 и не разрешают пилот/расходы/назначения/контакты. Команда экспорта не выдаёт разрешения на продуктовый запуск.
- Сохраняется closure manifests всех трёх стадий; drafts нужны для неослеплённого Resume и различения дубликатов/старых оснований. Два неприкреплённых helper-скрипта публикации не экспортируются; pinned scripts оставлены как inert historical dependencies. **Не запускать** `research/*`, `record_review.py`, `run.py` для воспроизведения Resume: они пишут исторические файлы. Для арифметики запускать только читающие `calculate.py`.
- Не включены оригинальная персональная копия, raw host sessions, credentials, локальные профили, `.local/` receipts/промежуточные экспорты, caches/`__pycache__`, временные скрипты. `cases/** -text` сохраняет точные байты checkpoint при Git checkout на Windows.

## Воспроизведение штатного Resume

Из корня клона/ZIP получите реально работающий Python3.12+ по [Quick Start](../quickstart.md). На Windows используйте сохранённый `$Python` из `tools/find_python.ps1`; `python` ниже — обозначение этого проверенного executable.

```sh
python tools/case_protocol.py check-candidate cases/mobile-product-strategy-demo --revision D0003
python tools/case_protocol.py classify cases/mobile-product-strategy-demo
python -m tools.resume_context cases/mobile-product-strategy-demo
```

В новом чате Codex/Cursor явно прочитайте `AGENTS.md`, `prompts/first-run.md` и `.agents/skills/resume-revise/SKILL.md`, затем:

```text
RESUME CASE cases/mobile-product-strategy-demo
Это производная демонстрационная копия, не оригинальные R0001–R0003.
Сначала проверь checkpoint; восстанови D0003 из шести snapshots и listed dependencies.
Отдельно классифицируй сохранённые drafts; не выбирай их по времени.
Не запускай новое исследование и не переноси approvals источника на эту копию.
```

Fresh-chat Resume оригинала — пользовательское исходное наблюдение, не повторённый release-прогон модели. Здесь проверяются CLI/файлы производной копии; новый live Codex/Cursor E2E и автоматическое обнаружение Skills не приписываются этому запуску.

Для повторной упаковки из **отдельно разрешённого приватного оригинала**: `python -m tools.export_contest_demo <private-source-case> <new-empty-destination>`. Packager принимает только проверенный исходный checkpoint и inventory131 файла, отклоняет занятый destination, не меняет source и не устанавливает зависимости. Для обычного Resume исходный приватный путь/профиль не нужен.

## Проверки

| Проверка | Текущий результат | Граница |
|---|---|---|
| Export source gate/chain, независимая D-chain и classify | PASS при реальном выполнении exporter, D0003 CHECKPOINTED | Целостность/совместимость, не содержание/официальность/host acceptance |
| Исходные файлы | 131/131 unchanged, повторная сверка каждого source hash и inventory | [Curated receipt](contest-rc-receipt.json), `summary` и карта128 source→export entries |
| Полный существующий unittest suite + release-регрессия | PASS: 121 tests, OK, 5 skipped; 102.842 s, CPython3.12.14/Windows | Пять symlink-privilege skips сохранены; реальный Windows junction regression exporter прошёл |
| `tools/check_repository.py` | PASS: 218 Markdown files; indexed case JSON/JSONL syntax; exit0 | Targets/syntax, не schema/hash/fragment/external URL/семантика/host validation |
| Relocated/ZIP-like Resume, inventory и read-only сохранность | PASS: без `.git` и приватного оригинала восстановлен D0003; все шесть snapshots совпадают; 3 draft-каталога обнаружены отдельно | CLI, не новый model run; 131 export-файл не изменён |
| Replay трёх расчётов | PASS: parsed JSON outputs совпадают с сохранёнными результатами для исходной арифметики, R0002 и аудита | Только deterministic arithmetic, не эмпирический эффект |
| Повторный экспорт/отказ overwrite | PASS: 131/131 файла повторного экспорта идентичны; занятый destination отклонён без изменения результата | Ограниченная reproducibility проверка packager |
| Privacy/secret review | PASS в указанном scope: имя профиля/личные пути в export не найдены; унаследованное раскрытие в текущем дереве исправлено | AI review + plaintext/JSON/UTF-16 проверки, не полный DLP; последующий аудит и решение владельца — в актуализации выше |
| Независимые AI reviews | ExportReview и ReleasePrivacyReview: после исправлений actionable findings отсутствуют | Не human/product acceptance |
| Сборка документации | Отдельного site/PDF builder нет; Markdown проверяется repository checker | Видео/PDF/screenshots не созданы этим запуском |

Фактические CLI результаты сохранены в [curated receipt](contest-rc-receipt.json); путь executable обезличен, версия CPython 3.12.14 сохранена. Это не raw host session. Все 43 JSON/JSONL export-файла разобраны; source/export fingerprints сохранены, содержательная история оригинала не менялась.

Независимые review выявили два исправленных дефекта: P2 alias/junction destination мог перенаправить экспорт внутрь source (добавлены canonical resolution, inventory-set guard и регрессия с реальным junction/symlink); P1 baseline-профиль содержал личный путь (текущее дерево исправлено, исторический блокер выше сохранён). Повторные статические review выполнены отдельно и не заменяют tests/human acceptance.

Ошибки подготовки: один локальный patch exporter получил parser warning и был исправлен до запуска; первый throwaway verification launcher завершился SyntaxError из-за передачи кавычек PowerShell, после чего использован запуск файла. Это не провалы штатного classifier/расчётов; ни источник, ни опубликованная D-chain этими попытками не менялись. Исходные ошибки OCR/source access не стёрты: см. demo evidence.

Финальные команды: `python -X utf8 -m unittest discover -s tests -v` и `python -X utf8 tools/check_repository.py` через ранее проверенный executable; оба exit0. Полный тестовый вывод содержит машинозависимые временные пути и намеренно не публикуется; выше сохранены наблюдённые итог/пропуски/scope. Дополнительного site/PDF build в проекте нет.

## Время, расходы и инструменты

[Demo evidence](demo-evidence.md) разделяет elapsed, длительности Python, PO-действия, инструменты и UNKNOWN model/billing telemetry. Не переносить модель/затраты текущей разработки OMP на исходный demo. OMP — инструмент разработки и release-review, **не runtime/зависимость конкурсного агента**. Packager — release-only Python stdlib; для продукта нет новых архитектурных компонентов или тяжёлых зависимостей.

## Решения и материалы человека перед подачей

1. Подтвердить официальный бриф/версию и допустимость распространения учебного PDF/derivatives.
2. Предоставить безопасный usage/billing export demo или принять явно UNKNOWN costs/model/time; не отправлять credentials/raw sessions. Данные труда PO/автора отдельно.
3. Записать и проверить видео ≤10 минут по [сценарию](../demo-video-script.md), подготовить требуемые реальные screenshots/PDF либо документ по ссылке. Markdown-описание уже есть; запись и скриншоты не выдуманы.
4. Проверить доступ жюри к основному репозиторию/документу/видео и условия конкурсной передачи. Смену visibility выполняет владелец отдельно; очистка истории только из-за обычных путей не требуется, лицензия автоматически не назначается.
5. Выполнить human acceptance и фактическую подачу капитаном. Старые неуспехи/ограничения evaluation не превращаются в новый PASS.

Merge, смена видимости, создание релизного тега и конкурсная отправка не выполняются.
