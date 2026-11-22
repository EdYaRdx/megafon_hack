> PRIVACY-SAFE DERIVATIVE D0001 of source R0001. Historical E2E/Resume belong to the original; export checks validate exported bytes only. No execution approval transfers. See EXPORT.md.

# Decision summary — следующий шаг исследования

- **Decision question:** что исследовать после агрегатного снижения в учебной выгрузке LinguaStep?
- **Decision owner / authority:** Product Owner, имя UNKNOWN
- **Status:** `RECOMMENDATION_PENDING_HUMAN`
- **Revision:**
- **Active claim IDs:**
- **Selected direction:** не выбрано; B условно рекомендован агентом

Первый рабочий DRAFT. Рабочие claims C-001…C-008 не являются selected active set. Complete checkpoint отсутствует. Стратегии и полный validation plan пока не разработаны: остановка на реальном PO gate по заданию.

C-001/E-002/S-002: inputs/cohorts.csv строки 2–5, eligible_users/returned_d30: январь (350+750)/(1000+1000)×100=55%; февраль (600+400)/(1500+500)×100=50%, −5 п.п. Paid 350/1000=35%→600/1500=40%, organic 750/1000=75%→400/500=80%, оба +5 п.п. Формула 100×Σreturned/Σeligible, единица %, разница п.п. Это отношения переданных счётчиков; decision-grade D30 UNKNOWN.

C-002/E-003/S-002, те же строки: paid share 1000/2000=50%→1500/2000=75%. При январских весах февральские отношения дают 60%; within +5 п.п. и mix at Feb rates −10 п.п. = net −5 п.п. S-004 analysis/cohort-results.json → descriptive_january_reference_decomposition; receipts/calculation-run-001.json: исторический run: UTC, hashes, Python 3.12.14, exit 0; argv redacted, source cwd/stderr omitted. Это reference-dependent арифметика, не causal effect.

C-003/E-004/S-002, строки 6–7: март false/10 дней и пустые outcomes; не 0% и не зрелый D30. C-004/E-001/S-001 inputs/brief-source.md, абзац 4: события, eligibility, timezone, окно и instrumentation UNKNOWN; unit/deduplication, extraction date/common cutoff/latency тоже отсутствуют. C-007/E-005/S-004 monthly: unweighted mean reported percentages 55%→60% — другой показатель, pooled ratio нельзя заменить средним.

C-006/E-006/S-003: [Amplitude](https://www.amplitude.com/docs/analytics/charts/retention-analysis/retention-analysis-calculation), Return On or After → Overall retention и Return On. Методические различия определения и зрелости поддерживают запрос контракта; не определяют LinguaStep события и поведение. C-005: ухудшение продукта/причина не установлены; остаются composition, measurement changes и скрытые subsegments.

Явные альтернативы:

- A — СТАТУС-КВО: продукт/привлечение и месячный отчёт без отдельной диагностики. Сохраняет ресурс; сильное возражение — неизвестный контракт и риск пропустить проблему. Пересмотр на следующем зрелом обзоре, дата/допуск UNKNOWN.
- B — минимально сверить contract/query/counts, cutoff и composition. Условно предпочтителен (C-004/C-005/C-008); сильное возражение — задержка реального улучшения, входы/стоимость UNKNOWN.
- C — исследовать конкретный барьер paid-учебного опыта. Возможна пользовательская польза; сильное возражение — барьер не обнаружен, paid ratio вырос, causal basis отсутствует.
- D — остановить отдельную emergency-retention инициативу и освободить ресурс; продукт не закрывать. Возможна экономия; сильное возражение — скрытая проблема и measurement debt сохраняются, объём высвобождения UNKNOWN.
- E — исследовать экономику acquisition mix. Состав меняется; сильное возражение — costs/payments/learning linkage отсутствуют, смена каналов не обоснована.

Ресурсы, цепочки бизнес-ценности и условия потери предпочтительности подробно записаны один раз в options.md. Эффекты, выручка, затраты, часы, размер выборки и пороги UNKNOWN.

Минимальный предложенный B сравнивает существующие январь/февраль на одном contract/cutoff. Если contract/counts не сверяются — продуктовый вывод отложить; если pattern сохраняется — рассмотреть E; если выявлено сопоставимое within-segment deterioration — C. Это предложение, не выполненное исследование. Владелец/доступность/срок/порог существенности UNKNOWN, определить до старта. Обе стратегии и полный validation plan следуют только после PO choice; причинное вмешательство, comparator эксперимента, sample и guardrails пока не выбраны.

- **Owner decision:** `NOT PROVIDED`
- **Execution approval:** не предоставлено на этой стадии; требуется отдельный applicable action/scope/revision/hash record, не вывод агента
- **Next step:** получить фактический выбор PO A/B/C/D/E или новое ограничение, затем читать следующий канонический Skill; не запускать сбор, контакты, расходы или эксперимент

Вопрос PO: **Какой следующий шаг выбираете: B — проверить измерение и состав (рекомендация), A — сохранить текущую работу, C — исследовать учебный барьер, D — остановить emergency-направление или E — изучить экономику привлечения?**

Это host-backed agent/tool attempt, не внешнее человеческое принятие. Успешная проверка операторского создания не является демонстрацией самостоятельного free-form NEW создания.
