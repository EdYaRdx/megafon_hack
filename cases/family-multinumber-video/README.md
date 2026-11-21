# Видеокейс: помощь уже подключённым семьям

**Обезличенная производная копия реального запуска из видеозаписи, не исходная история.** Исходные R0001–R0003 сопоставлены самостоятельной цепочке D0001–D0003. Реальна сессия агента; оператор и исходные числа учебные. Видео и fresh-session Resume подтверждены сообщением владельца, не новым просмотром записи при упаковке.

[Маршрут по этапам видео](../../docs/video-e2e.md) · [Происхождение и ограничения](EXPORT.md) · [Карта SHA-256](export-map.json) · [Release-аудит и проверки](../../docs/release/video-family-e2e-20261121.md)

## Результаты

- [Актуальное решение D0003](decision.md), [состояние](state.md) и [selector](ACTIVE.json).
- [Продуктовая стратегия](strategy-product.md), [коммуникационная стратегия](strategy-communication.md), [пятичастный документ](strategy.md), [план проверки](test-plan.md).
- [Шесть альтернатив](options.md), [выбор PO](inputs/user-choice-D0002.md), [исходный PDF](inputs/brief.pdf).
- [Две стратегии до пересмотра, D0002: продукт](revisions/D0002/strategy-product.md) и [коммуникации](revisions/D0002/strategy-communication.md).
- [Поручение критического пересмотра](inputs/user-review-D0003.md), [изменения и основания D0003](research/D0003/review.md), [расчёт](calculations/D0003/results.json).
- [D0001: исследование](revisions/D0001/decision.md) → [D0002: выбор](revisions/D0002/decision.md) → [D0003: пересмотр](revisions/D0003/decision.md).

Выбран B — узкая помощь уже подключённым семьям; пилот/бюджет не одобрены. Экономический эффект, достижимость цели, окупаемость и сроки UNKNOWN. Следующее управленческое решение D1 о диагностике ещё не принято.

## Продолжение без изменения истории

Из корня проекта, проверенным Python 3.12+: `python -B tools/case_protocol.py classify cases/family-multinumber-video` и `python -B -m tools.resume_context cases/family-multinumber-video`. Полный порядок и команда для нового чата — в [маршруте](../../docs/video-e2e.md#read-only-проверка-и-продолжение). Ожидаемый activity hint относится к последующим receipts, не выбирает новый draft.

Исторические scripts и receipts сохранены как артефакты происхождения. **Не запускайте `research/**/*.py` и `calculations/run.py` в этом деле**: они могут писать защищённые файлы. Старые hashes и PASS внутри истории относятся к оригиналу; для derivative используйте export-map и новые release-проверки. Ни публикация, ни выбор направления не разрешают пилот, расходы или контакт с клиентами.
