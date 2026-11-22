# Второй учебный кейс — LinguaStep

**Почему общий retention снизился, хотя оба сегмента выросли?** На новой синтетической задаче агент связал бриф, CSV и веб-методику, сравнил пять направлений и после выбора PO подготовил две стратегии ограниченной диагностики и план проверки.

[**Продуктовая стратегия**](../../cases/linguastep-retention/strategy-product.md) · [**Коммуникационная стратегия**](../../cases/linguastep-retention/strategy-communication.md) · [**План проверки**](../../cases/linguastep-retention/test-plan.md)

## Входы и исследование

[Исходный учебный документ](../../cases/linguastep-retention/inputs/brief-source.md) · [CSV когорт](../../cases/linguastep-retention/inputs/cohorts.csv) · [сохранённая публичная методика Amplitude](../../cases/linguastep-retention/sources/S-003-amplitude-text.txt) · [sources](../../cases/linguastep-retention/sources.jsonl) / [evidence](../../cases/linguastep-retention/evidence.jsonl) / [claims](../../cases/linguastep-retention/claims.jsonl). Методика помогает определить измерение, но не устанавливает причины поведения.

## Результат расчёта и выбор человека

По CSV, строки 2–5: январь 1100/2000=55%, февраль 1000/2000=50%. Paid 35→40%, organic 75→80%; доля paid 50→75%. При январской структуре февраль=0,5×40%+0,5×80%=60%. Декомпозиция +5 п.п. внутри сегментов и −10 п.п. состава даёт −5 п.п. агрегата. [Расчётный результат](../../cases/linguastep-retention/analysis/cohort-results.json) и [реальный replay](../release/final-20261122/export-calculation-replay.json). Незрелая мартовская когорта и пропуски не заменены нулями. Это описательная арифметика, не доказательство причинности; операционный контракт D30 UNKNOWN.

[Пять альтернатив с возражениями](../../cases/linguastep-retention/options.md): статус-кво, сверка измерения/когорт, UX paid, остановка срочной инициативы и экономика привлечения. [Реальный выбор PO B](../../cases/linguastep-retention/inputs/owner-message-B-20261122.md) — сначала проверить D30, eligibility, зрелость, запрос и сопоставимость периодов. Это выбор аналитического направления, не изменение продукта или бюджета.

Продуктовая стратегия задаёт внутренних пользователей результата, процесс и роли сверки. Коммуникационная объясняет неопределённость без ложного диагноза «retention продукта ухудшился». План фиксирует comparator, воспроизводимые расчёты и условия STOP/REVISE. [Итоговое решение](../../cases/linguastep-retention/decision.md). Реальные данные, контакты, расходы и запуск эксперимента не разрешены и не выполнялись.

## Resume и публичные результаты

Исходный R0001 прошёл checkpoint и подтверждённый владельцем Resume в настоящем новом чате: [ограниченный неподписанный receipt](../release/final-20261122/source-resume-receipt.json). Ожидаемые revision/hash были даны, это не blind discovery.

[Публичная папка D0001](../../cases/linguastep-retention/README.md) — отдельный privacy-safe экспорт с новыми hashes: [происхождение](../../cases/linguastep-retention/EXPORT.md), [manifest](../../cases/linguastep-retention/revisions/D0001/manifest.json), [gate](../release/final-20261122/linguastep-export-gate.json), [classify](../release/final-20261122/linguastep-export-classify.json). Проверка этих байтов не является повторным модельным E2E. Дело первоначально создал оператор; свободный NEW этим прогоном не квалифицирован.

[Основной демонстрационный проект МегаФона](megafon.md) · [финальная готовность](../release/submission-ready-20261122/README.md) · [PDF](../MGIMO_FINAL_REPORT.pdf).
