# Реальный запуск из видеозаписи: семейная помощь

**Это отдельное дело от прежнего [подготовленного демо](contest-demo.md).** По сообщению владельца, на видео записаны первый запрос, чтение PDF, шесть альтернатив, выбор Product Owner, две стратегии R0002, Resume в новой сессии и критический пересмотр R0003. Реальна работа с агентом; оператор и показатели в брифе **учебные**, не реальные данные МегаФона.

В репозитории размещена **обозначенная обезличенная производная копия** [`cases/family-multinumber-video/`](../cases/family-multinumber-video/README.md), D0001 → D0002 → D0003. Она сохраняет аналитические результаты видео, но не выдаётся за исходные байты R0001–R0003. [EXPORT](../cases/family-multinumber-video/EXPORT.md), [карта SHA-256](../cases/family-multinumber-video/export-map.json) и [release-отчёт](release/video-family-e2e-20261121.md) объясняют изменения и проверки. Исходное дело не переписывалось; прежний демонстрационный кейс сохранён отдельно.

## Открыть тот же этап, что на видео

| Этап видео / оригинала | Сохранённый результат в репозитории |
|---|---|
| Задание и исследование PDF | [Исходный PDF](../cases/family-multinumber-video/inputs/brief.pdf), [уточнение задачи](../cases/family-multinumber-video/inputs/user-scope.md), [разбор PDF](../cases/family-multinumber-video/sources/S-001-reading.md), [источники](../cases/family-multinumber-video/sources.jsonl) |
| R0001: шесть альтернатив, выбор ещё за PO | [Варианты D0001](../cases/family-multinumber-video/revisions/D0001/options.md), [решение D0001](../cases/family-multinumber-video/revisions/D0001/decision.md) |
| Выбор PO и R0002: две стратегии | [Дословный выбор](../cases/family-multinumber-video/inputs/user-choice-D0002.md), [продуктовая стратегия D0002](../cases/family-multinumber-video/revisions/D0002/strategy-product.md), [коммуникационная D0002](../cases/family-multinumber-video/revisions/D0002/strategy-communication.md), [решение D0002](../cases/family-multinumber-video/revisions/D0002/decision.md) |
| Resume R0002 в новой сессии перед пересмотром | [Исторический inventory](../cases/family-multinumber-video/research/D0003/restore-inventory-receipt.json); это преобразованный source receipt, не новый запуск модели |
| Критический пересмотр R0003 | [Поручение](../cases/family-multinumber-video/inputs/user-review-D0003.md), [что изменено и почему](../cases/family-multinumber-video/research/D0003/review.md), [решение D0003](../cases/family-multinumber-video/revisions/D0003/decision.md) |
| Актуальный итог после пересмотра | [Продуктовая стратегия](../cases/family-multinumber-video/strategy-product.md), [коммуникационная стратегия](../cases/family-multinumber-video/strategy-communication.md), [пятичастный документ](../cases/family-multinumber-video/strategy.md), [план проверки](../cases/family-multinumber-video/test-plan.md), [состояние](../cases/family-multinumber-video/state.md) |

Обозначения вариантов этого дела: **A — статус-кво, B — помощь уже подключённым семьям, C — собственные номера, D — начисления, E — общий кабинет, F — остановка инициативы**. PO сохранил B. Не переносите буквы из прежнего демо: там другой CASE и иные обозначения.

## Что изменил R0003

Направление сохранено, но достижимость финансовой цели, эффект, окупаемость и сроки остаются `UNKNOWN`. Снято прочтение сценария без эффекта как прогноза или нижнего предела. Предварительный ресурс не гарантирует готовность к Q2. Числа третьего года — проект ориентира, не установленный минимум. Помощь существующим семьям не закрывает автоматически привлечение, новые подключения и активацию. Пилот и бюджет не одобрены.

Экономика: `GP = 279 000 000 + 500M + O − C`; до цели 285 млн ₽ нужно `500M + O − C ≥ 6 000 000`. Только при **условных C=O=0** необходимы **12 000 дополнительных оплаченных номеро-месяцев**. Это граница, не прогноз, не семьи и не размер выборки. M/O могут быть отрицательны; разработка I отдельно. [Детерминированный расчёт](../cases/family-multinumber-video/calculations/D0003/results.json) и [пояснение границ](../cases/family-multinumber-video/research/D0003/review.md) не доказывают реальный платёжный эффект.

Полнота документов не означает наличия эмпирических входов: частоты причин, M/O/C/I, baseline, sample, пороги, смета и критический путь неизвестны. Следующий шаг сохранённого дела — рассмотреть с руководителем комплект D1 об ограниченной диагностике P0/P1; это не автоматическое разрешение её выполнять.

## Read-only проверка и продолжение

Из корня clone или распакованного ZIP, с проверенным **Python 3.12+** ([Windows fallback](quickstart.md#если-команду-выполняет-оператор)); `python` ниже обозначает этот executable:

```sh
python -B tools/case_protocol.py check-candidate cases/family-multinumber-video --revision D0003
python -B tools/case_protocol.py classify cases/family-multinumber-video
python -B -m tools.resume_context cases/family-multinumber-video
```

Ожидаемые контракты: `VALIDATED_CANDIDATE`, `CHECKPOINTED`, inventory с выбранным D0003. Отдельный hint об append-only `activity.jsonl` ожидаем: после закреплённого префикса сохранены receipts A-050…A-053. Hint не выбирает более поздний draft; его нужно прочитать, а не скрыть. Проверки целостности не равны успешному ответу модели.

В новом чате Codex/Cursor:

```text
RESUME CASE cases/family-multinumber-video
Прочитай AGENTS.md, prompts/first-run.md, .agents/skills/resume-revise/SKILL.md
и cases/family-multinumber-video/EXPORT.md. Это производная копия видеокейса.
Проверь D0003, восстанови решение, неизвестное и точный следующий шаг.
Отдельно разбери activity hints. Не начинай новое исследование и не меняй историю.
```

**Не запускайте исторические `research/**/*.py` или `calculations/run.py` в сохранённом деле:** часть скриптов пишет snapshots, журналы, selector или results. Для просмотра/Resume нужны только штатные read-only команды выше. Арифметику release проверяет на временной копии, не переписывая исходник.

## Происхождение и границы доказательств

PDF SHA-256: `558d2c665caa4f4954135c8bbfb69d791e398dcdc5b625d5ded7bdb2d0eb0fa5` — побайтово тот же файл, что уже включён в прежний демо-кейс. [Подтверждение владельца о получении со страницы задания](submission-checklist.md#публикация-основного-репозитория) применимо к этим байтам; независимой сверки кабинета и отдельной лицензии на PDF нет. PDF и 11 PNG не изменены; пользовательские вводы не содержат клиентских данных.

Видео и успешный fresh-session Resume — **наблюдение владельца**. Сам видеофайл/URL для проверки не предоставлен в этом задании: здесь не подтверждаются его монтаж, длительность, отсутствие личных данных или фактическая доступность жюри. Новый live E2E модели при упаковке не выполнялся. Точная модель, полные время/вызовы/стоимость исходного запуска — `UNKNOWN`; command elapsed в receipts не заменяет эти данные.

Перед подачей владелец отдельно проверяет безопасную запись и её ссылку, требования к документам, условия передачи PDF, доступ жюри и выполняет конкурсную отправку. Этот PR не выполняет merge, смену visibility или подачу.
