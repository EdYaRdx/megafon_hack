> PRIVACY-SAFE DERIVATIVE D0001 of source R0001. Historical E2E/Resume belong to the original; export checks validate exported bytes only. No execution approval transfers. See EXPORT.md.

# Evidence review — DRAFT before PO choice

Рабочие C-001…C-008 пока не выбраны в complete revision. Источники и извлечения — sources/evidence/claims.jsonl.

## Контракт
S-001, inputs/brief-source.md, абзац 4 (C-004/E-001): start/return event, eligibility, timezone, окно и изменения инструментации UNKNOWN. Также отсутствуют unit/deduplication, extraction date, common cutoff и latency/maturity rule. eligible_users и returned_d30 — известные переданные знаменатель и числитель; UNKNOWN относится к их операционному определению, не наличию счётчиков.

S-002, inputs/cohorts.csv строки 2–5: зрелость true/30 дней по выгрузке, независимо не подтверждена. Строки 6–7: false/10 дней, outcomes пусты; не 0% (C-003/E-004). Март не включён в расчёт.

S-003: https://www.amplitude.com/docs/analytics/charts/retention-analysis/retention-analysis-calculation, разделы Return On or After → Overall retention и Return On. Методика различает критерии возврата и учитывает завершённость интервала (C-006/E-006). Никакое vendor definition не принято за определение LinguaStep. В оригинале сохранены raw HTML и parsed text. В экспорте оставлены parsed text и сокращённые historical receipts/public-source-run-001.json, receipts/public-extraction-001.json; raw HTML исключён.

## Реальный расчёт
receipts/calculation-run-001.json содержит исторические argv (redacted в экспорте), исходный cwd не опубликован; Python 3.12.14, UTC start/end, exit=0, сохранённый source stdout; source stderr omitted в экспорте, hashes source/script. analysis/calculate_cohorts.py читает pinned CSV, не вручную переписанные массивы. Input SHA-256: b6db2059086921629565ed1947b5fa7c91607d8aa19576d3b20efdac7e423ebd.

| Срез | Январь returned/eligible | Февраль returned/eligible | Изменение |
|---|---:|---:|---:|
| Все переданные зрелые строки | 1100/2000 = 55% | 1000/2000 = 50% | −5 п.п. |
| paid | 350/1000 = 35% | 600/1500 = 40% | +5 п.п. |
| organic | 750/1000 = 75% | 400/500 = 80% | +5 п.п. |

C-001/E-002/S-002, строки 2–5 eligible_users,returned_d30; S-004 analysis/cohort-results.json → monthly,segments. Формула: 100×Σreturned_d30/Σeligible_users; единица %, разница п.п. Это отношения счётчиков, не decision-grade D30.

C-002/E-003: paid share 1000/2000=50% → 1500/2000=75%. При январских весах февральские отношения: 0.5×40%+0.5×80%=60%; within=60−55=+5 п.п., mix at Feb rates=50−60=−10 п.п.; итого −5 п.п. S-002 строки 2–5 и S-004 descriptive_january_reference_decomposition. Reference-dependent accounting identity, не causal attribution.

C-007/E-005: unweighted mean reported percentages (35+75)/2=55% → (40+80)/2=60%, иной estimand. S-002 строки 2–5 reported_retention_percent; S-004 monthly/formulas. Exact Fraction arithmetic; отображённые значения конечные, округление не влияет. Проверены уникальность month/segment, положительные знаменатели, 0≤числитель≤знаменатель, совпадение row percentages. Пустоты не заменены нулём. Статистическая неопределённость и перенос на другие когорты не оценены.

## Объяснения и различающие сведения
Наблюдение: агрегатный count ratio ниже, оба segment ratios выше, вырос вес paid (C-001/C-002). INFERENCE C-005: composition объясняет арифметику; качество канала, мотивы и ухудшение продукта не установлены.

Сильный конкурент — несопоставимое измерение: eligibility/events/dedup/window/cutoff либо instrumentation. UNKNOWN, прямого свидетельства ошибки нет. Различат существующие specification/query/changelog и reconciliation на общем cutoff.

Ещё конкурент — скрытый учебный барьер внутри subsegments, компенсированный другими пользователями. HYPOTHESIS без локального подтверждения; не ранжируем по распространённости. Различат заранее определённые сопоставимые срезы и behavioral diagnostics после metric contract. Интервью или синтетические респонденты не проводились.

## Одно минимальное следующее исследование — только предложение
B: ограниченная сверка существующих metric specification, query/export и instrumentation changelog за январь/февраль. Проверить contract parity, counts, зрелость, common cutoff; comparator — январь/февраль на одном контракте, затем pooled/within-segment ratios.

Если contract/counts не сверяются — отложить продуктовый выбор и решить вопрос измерения. Если всё сверяется и mix pattern сохраняется — рассмотреть economics E, без автоматической смены каналов. Если выявлено сопоставимое within-segment deterioration — рассмотреть C. Владелец данных, доступность, срок, стоимость и порог существенности UNKNOWN; согласовать до старта. Данные сейчас не запрашивались и не собирались. C-008 — условная рекомендация, не решение PO.
