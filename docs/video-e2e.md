# Реальный видеокейс: помощь семье со связью

[**Быстро открыть задачу, пять KPI, входы и итоговые стратегии**](demos/megafon.md) · [Текущая готовность и доступы](release/submission-ready-20261122/README.md). Ниже — подробная навигация по исходной записи и ревизиям.

**Как выбрать первую продуктовую инициативу, если есть финансовая цель, несколько аудиторий и недостаточно данных об их проблемах?**

В учебном брифе «Связь для близких и собственных устройств» агент сравнил шесть направлений. Product Owner выбрал помощь уже подключённым семьям: ранний сигнал о низком остатке интернета и переход к существующей передаче объёма. После выбора подготовлены две стратегии и план проверки; при критическом пересмотре финансовая достижимость оставлена неизвестной, а история решения сохранена.

[**Смотреть видеодемонстрацию**](https://drive.google.com/file/d/1kDBIVW_hgRwh2WnttYouUtfnlhtD27P_/view) · [**Продуктовая стратегия**](../cases/family-multinumber-video/strategy-product.md) · [**Коммуникационная стратегия**](../cases/family-multinumber-video/strategy-communication.md) · [Решение](../cases/family-multinumber-video/decision.md)

Длительность **9:58 — по сообщению владельца**, независимо не измерена. Он подтвердил доступ к папке Drive по ссылке; содержательная проверка всей записи, звука и фактического просмотра жюри остаётся его ответственностью. [Подлинный кадр результата, 06:34](assets/strategy-result-from-video.png), получен из опубликованного видео, не сгенерирован.

## Открыть тот же этап, что на видео

В видео показаны исходные **R0001–R0003**. В GitHub лежит обезличенный derivative **D0001–D0003**; ссылки ниже ведут в эту опубликованную копию, а не в отсутствующие исходные R-файлы.

| Этап | Что проверить в опубликованных файлах |
|---|---|
| Естественный запрос, первый запуск и шесть Skills | [Уточнение задачи](../cases/family-multinumber-video/inputs/user-scope.md); шесть проектных Skills показаны в видео по сообщению владельца, их канонический состав — в [архитектуре](architecture.md) |
| Исследование 11-страничного PDF | [Бриф](../cases/family-multinumber-video/inputs/brief.pdf) · [Разбор с локаторами](../cases/family-multinumber-video/sources/S-001-reading.md) · [Источники](../cases/family-multinumber-video/sources.jsonl) |
| R0001 → D0001: сравнение шести альтернатив | [Варианты](../cases/family-multinumber-video/revisions/D0001/options.md) · [Рекомендация до выбора PO](../cases/family-multinumber-video/revisions/D0001/decision.md) |
| Выбор направления человеком | [Дословное решение PO](../cases/family-multinumber-video/inputs/user-choice-D0002.md) |
| R0002 → D0002: две стратегии и проверка | [Продуктовая](../cases/family-multinumber-video/revisions/D0002/strategy-product.md) · [Коммуникационная](../cases/family-multinumber-video/revisions/D0002/strategy-communication.md) · [План](../cases/family-multinumber-video/revisions/D0002/test-plan.md) |
| Resume R0002 в новом чате | [Сохранённый inventory перед пересмотром](../cases/family-multinumber-video/research/D0003/restore-inventory-receipt.json): восстанавливает стадию до пересмотра; преобразованный receipt явно помечен как исторический |
| R0003 → D0003: критический пересмотр | [Поручение](../cases/family-multinumber-video/inputs/user-review-D0003.md) · [Что изменено и почему](../cases/family-multinumber-video/research/D0003/review.md) |
| Актуальный итог | [Решение](../cases/family-multinumber-video/decision.md) · [Две стратегии](../cases/family-multinumber-video/README.md#результаты) · [План проверки](../cases/family-multinumber-video/test-plan.md) · [Состояние](../cases/family-multinumber-video/state.md) |

В этом деле **A — статус-кво, B — помощь семьям, C — собственные номера, D — начисления, E — общий кабинет, F — остановка инициативы**. Выбран B. Подходящий семье тариф, действующие права, свободный объём и своевременность сигнала остаются условиями помощи, а не свойствами уже реализованного сервиса.

## Что изменил R0003

Пересмотр сохранил направление, но усилил границы вывода:

- Сценарий без эффекта — reference, не прогноз и не гарантированный нижний предел.
- Предварительный ресурс не гарантирует готовность к Q2; числа третьего года — проект ориентира, не доказанный минимум.
- Помощь существующим семьям сама по себе не закрывает новые подключения, привлечение владельцев номеров и активацию новых групп.
- Пилот и бюджет не одобрены; следующим решением остаётся точный scope ограниченной диагностики D1.

Экономическая граница: `GP = 279 000 000 + 500M + O − C`; цель требует `500M + O − C ≥ 6 000 000`. Только при **условных C=O=0** необходимы **12 000 дополнительных оплаченных номеро-месяцев**. Это не семьи, не размер выборки и не подтверждённый прогноз. M и прочий чистый вклад O могут быть отрицательны; разработка I учитывается отдельно.

[Расчёт](../cases/family-multinumber-video/calculations/D0003/results.json) воспроизводит условную арифметику, но не устанавливает реальный эффект. Частоты причин, baseline, sample, пороги, M/O/C/I, смета и критический путь неизвестны. Дело завершает аналитический этап, не выдаёт его за проведённый клиентский эксперимент.

## Read-only проверка и продолжение

Для чтения результатов команды не нужны. Для проверки сохранённой копии из корня clone/ZIP используйте работающий **Python 3.12+** ([помощь с Windows](quickstart.md#если-команду-выполняет-оператор)); `python` ниже обозначает этот executable:

```sh
python -B tools/case_protocol.py check-candidate cases/family-multinumber-video --revision D0003
python -B tools/case_protocol.py classify cases/family-multinumber-video
python -B -m tools.resume_context cases/family-multinumber-video
```

Ожидаются `VALIDATED_CANDIDATE`, `CHECKPOINTED` и inventory с D0003. Отдельный activity hint относится к receipts A-050…A-053 после закреплённого префикса; он не выбирает новый draft. Реальные результаты release-проверок — в [оценке](evaluation.md).

Для нового чата:

```text
RESUME CASE cases/family-multinumber-video
Прочитай AGENTS.md, prompts/first-run.md и .agents/skills/resume-revise/SKILL.md.
Учти EXPORT.md этого дела. Проверь checkpoint, восстанови решение,
открытые вопросы и следующий шаг. Пока не меняй файлы и не начинай исследование.
```

Не запускайте исторические `research/**/*.py` и `calculations/run.py` в сохранённом примере: часть пишет case-файлы. Они оставлены как происхождение результата, не как процедура Resume.

## Происхождение и границы доказательств

Дело [`family-multinumber-video`](../cases/family-multinumber-video/README.md) и его [EXPORT](../cases/family-multinumber-video/EXPORT.md) / [карта преобразований](../cases/family-multinumber-video/export-map.json) сохраняют соответствие оригинала и derivative. PDF, 11 PNG и OCR сохранены побайтово; личные profile/checkout пути обезличены в текстах. Старые hashes и receipts описывают source-байты; новые проверки производной копии хранятся отдельно.

PDF совпадает с ранее включённым учебным документом; получение со страницы задания MGIMO подтверждено владельцем, не независимой сверкой кабинета или отдельной лицензией. Оператор вымышленный, числа учебные. Это отдельное дело от [прежнего prepared demo](archive/README.md#предыдущие-примеры).

В выбранных кадрах опубликованной записи виден Codex и UI-обозначение `GPT-6.1-Sol high`, а также ускорение `speed x10`. Это наблюдение интерфейса, не provider/API ID или billing export. Полные время, вызовы, токены и стоимость сессии не установлены. [Источник кадра и кроп](assets/README.md) · [Описание реализации для жюри](submission-description.md).
