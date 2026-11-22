# Демонстрационный проект — МегаФон

**Как выбрать первую инициативу для семей и владельцев нескольких номеров?** Агент изучил учебный PDF, сопоставил шесть направлений, получил выбор Product Owner и подготовил две связанные стратегии и план P0–P3. После Resume в новом чате критический Revise уточнил экономику и условия следующего решения.

[**Продуктовая стратегия**](../../cases/family-multinumber-video/strategy-product.md) · [**Коммуникационная стратегия**](../../cases/family-multinumber-video/strategy-communication.md) · [**План проверки**](../../cases/family-multinumber-video/test-plan.md) · [**Видео**](https://drive.google.com/file/d/1kDBIVW_hgRwh2WnttYouUtfnlhtD27P_/view)

## 1. Задача руководителя

Исходный вопрос: развивать сервис для семей и людей с несколькими номерами, но «пока не понимаем, на ком сосредоточиться и что лучше предложить клиентам». [Сохранённый исходный запрос](../../cases/family-multinumber-video/brief.md#запрос-пользователя) и [границы от PO](../../cases/family-multinumber-video/inputs/user-scope.md) доступны отдельно.

Пять KPI учебного планового года — условия задания, не результат работы агента (S-001, [PDF, стр.3](../../cases/family-multinumber-video/inputs/brief.pdf#page=3); [проверенное извлечение](../../cases/family-multinumber-video/sources/S-001-reading.md)):

| KPI | Без изменений | Цель |
|---|---:|---:|
| Валовая прибыль | 279 млн ₽ | ≥285 млн ₽ |
| Активные семейные группы за последний месяц | 5 000 | ≥8 000 |
| Подключённые семейные группы на конец года | 8 000 | ≥12 000 |
| Подключённые владельцы нескольких номеров | 1 000 | ≥2 000 |
| Активация новых групп Q4 за 14 дней | 45% | ≥60% |

В брифе уже есть передача свободного интернета и переключение собственных номеров. Спрос, причины потери связи, эффект и доступность ресурсов ещё нужно подтвердить. Семьи и владельцы номеров — разные единицы: [контекст и сравнение сегментов](../../cases/family-multinumber-video/brief.md#пользователи-и-контекст).

## 2. Что получил и исследовал агент

[Учебный PDF, 11 страниц](../../cases/family-multinumber-video/inputs/brief.pdf), исходный запрос и ограничения выше. Исследование сохранило [источники](../../cases/family-multinumber-video/sources.jsonl), [evidence](../../cases/family-multinumber-video/evidence.jsonl), [claims](../../cases/family-multinumber-video/claims.jsonl) и [первый аналитический вывод](../../cases/family-multinumber-video/revisions/D0001/decision.md). GOV.UK/Stripe использованы как методика; они не доказывают локальный спрос. Только учебные и разрешённые открытые материалы.

## 3. Шесть вариантов и решение PO

A — статус-кво; B — ранняя помощь подключённым семьям; C — собственные номера; D — понятные начисления; E — общий кабинет; F — остановка новой разработки. [Полное сравнение, ресурсы и сильные возражения](../../cases/family-multinumber-video/options.md).

**PO выбрал B для дальнейшей проработки.** Доступная передача даёт конкретный механизм проверки; неоплата, отсутствие общего объёма и превосходство C/D по реальному ущербу могут опровергнуть приоритет B. Сначала нужно сравнить масштаб причин. [Дословный выбор и поручение](../../cases/family-multinumber-video/inputs/user-choice-D0002.md) разрешают подготовку стратегий, но не пилот, бюджет или сообщения клиентам.

## 4. Итоговые материалы

| Результат | Где открыть |
|---|---|
| Аудитория, ценность, путь и отказы | [Продуктовая стратегия D0003](../../cases/family-multinumber-video/strategy-product.md) |
| Обещание, подтверждение, каналы и примеры сообщений | [Коммуникационная стратегия D0003](../../cases/family-multinumber-video/strategy-communication.md#сообщение-подтверждение-и-следующий-шаг) |
| P0 — причины; P1 — понятность; P2 — клиентская польза; P3 — оплаты | [План с comparator, метриками/знаменателями и условиями решений](../../cases/family-multinumber-video/test-plan.md) |
| Финансовая модель и возражения | [Проверенная экономика](../../cases/family-multinumber-video/research/D0003/review.md#проверенная-экономика-и-предел-вывода) · [сохранённые расчёты](../../cases/family-multinumber-video/calculations/D0003/results.json) |
| Выбор, неизвестное и следующий управленческий шаг | [Решение](../../cases/family-multinumber-video/decision.md) · [состояние](../../cases/family-multinumber-video/state.md) |

Только при условных C=O=0 разрыв 6 млн ₽ соответствует 12 000 дополнительным оплаченным номеро-месяцам. Это не прогноз эффекта B. Дизайн P0–P3 подготовлен; сами исследования/пилот NOT RUN. Следующий шаг — отдельное согласование scope диагностики D1.

## 5. Продолжение работы

[Исторический Resume перед пересмотром](../../cases/family-multinumber-video/research/D0003/restore-inventory-receipt.json) восстановил выбор B и ограничения. [Что изменил критический Revise](../../cases/family-multinumber-video/research/D0003/review.md#что-изменено-относительно-d0002): сценарий без эффекта перестал читаться как прогноз, календарь — как гарантия, цели третьего года — как обязательный минимум. Направление сохранено, старые версии не удалены: [D0001](../../cases/family-multinumber-video/revisions/D0001/decision.md) → [D0002](../../cases/family-multinumber-video/revisions/D0002/decision.md) → [D0003](../../cases/family-multinumber-video/revisions/D0003/decision.md).

## 6. Как посмотреть процесс

[Видео](https://drive.google.com/file/d/1kDBIVW_hgRwh2WnttYouUtfnlhtD27P_/view): около 04:50 — альтернативы, 06:34 — стратегии до пересмотра, 06:50–07:20 — новый чат/Resume. Это ориентиры выборочных кадров, не утверждение полного просмотра. [Все этапы и команда Resume](../video-e2e.md). Доступ Drive anyone / reader проверен; полный безопасный просмотр остаётся за владельцем.

## 7. Проверяемость

[Папка дела](../../cases/family-multinumber-video/README.md) сохраняет самостоятельную обезличенную D0001–D0003 историю исходного видеокейса R0001–R0003. [EXPORT](../../cases/family-multinumber-video/EXPORT.md), [export-map](../../cases/family-multinumber-video/export-map.json), [manifest D0003](../../cases/family-multinumber-video/revisions/D0003/manifest.json) и [актуальная готовность/receipts](../release/submission-ready-20261122/README.md) позволяют сверить происхождение и hashes. Hash подтверждает байты, не бизнес-эффект.

Эта входная страница находится вне защищённого дела: его README включён в export-map и сохранён без изменений. [Финальный PDF](../MGIMO_FINAL_REPORT.pdf) · [второй кейс LinguaStep](linguastep.md) · [маршрут для жюри](../for-jury.md).
