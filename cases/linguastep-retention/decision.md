> PRIVACY-SAFE DERIVATIVE D0001 of source R0001. Historical E2E/Resume belong to the original; export checks validate exported bytes only. No execution approval transfers. See EXPORT.md.

# Decision summary — следующий шаг исследования

- **Decision question:** что исследовать после агрегатного снижения в учебной выгрузке LinguaStep?
- **Decision owner / authority:** Product Owner, имя UNKNOWN
- **Status:** `DECIDED`
- **Revision:** D0001
- **Active claim IDs:** C-001, C-002, C-003, C-004, C-005, C-006, C-007, C-009, C-010
- **Selected direction:** B выбран Product Owner: ограниченная сверка измерения retention и состава когорт; разрешена подготовка, не исполнение

Состав решения D0001: C-001…C-007, C-009, C-010; C-010 supersedes C-008. Выбор направления DECIDED не разрешает исполнение диагностики. Предыдущие байты memo сохранены в research/pre-po/decision.md. Состав и публикация проверяются штатным protocol gate и selector.

C-009/E-008/S-006, inputs/owner-message-B-20261122.md, opening choice, grounds и priority paragraph: PO выбрал B по тем же числам, приоритет definition/eligibility/maturity/query/missingness/period comparability. Авторизована подготовка стратегий и плана. Это нормализованная транскрипция из parent chat; не original message bytes, исходный timestamp UNKNOWN; read/recorded UTC в A-012.

C-001/E-002/S-002: inputs/cohorts.csv строки 2–5, eligible_users/returned_d30: январь (350+750)/(1000+1000)×100=55%; февраль (600+400)/(1500+500)×100=50%, −5 п.п. Paid 350/1000=35%→600/1500=40%, organic 750/1000=75%→400/500=80%, оба +5 п.п. Формула 100×Σreturned/Σeligible, единица %, разница п.п. Это отношения переданных счётчиков; decision-grade D30 UNKNOWN.

C-002/E-003/S-002, те же строки: paid share 1000/2000=50%→1500/2000=75%. При январских весах февральские отношения дают (1000/2000)×(600/1500)×100 + (1000/2000)×(400/500)×100 = 60%; within +5 п.п. и mix at Feb rates −10 п.п. = net −5 п.п. S-004 analysis/cohort-results.json → descriptive_january_reference_decomposition; receipts/calculation-run-001.json: исторический run: UTC, hashes, Python 3.12.14, exit 0; argv redacted, source cwd/stderr omitted. Это reference-dependent арифметика, не causal effect.

C-003/E-004/S-002, строки 6–7: март false/10 дней и пустые outcomes; не 0% и не зрелый D30. C-004/E-001/S-001 inputs/brief-source.md, абзац 4: события, eligibility, timezone, окно и instrumentation UNKNOWN; unit/deduplication, extraction date/common cutoff/latency тоже отсутствуют. C-007/E-005/S-004 monthly: unweighted mean reported percentages 55%→60% — другой показатель, pooled ratio нельзя заменить средним.

C-006/E-006/S-003: [Amplitude](https://www.amplitude.com/docs/analytics/charts/retention-analysis/retention-analysis-calculation), Return On or After → Overall retention и Return On. Методические различия определения и зрелости поддерживают запрос контракта; не определяют LinguaStep события и поведение. C-005: ухудшение продукта/причина не установлены; остаются composition, measurement changes и скрытые subsegments.

Явные альтернативы:

- A — СТАТУС-КВО: продукт/привлечение и месячный отчёт без отдельной диагностики. Сохраняет ресурс; сильное возражение — неизвестный контракт и риск пропустить проблему. Пересмотр на следующем зрелом обзоре, дата/допуск UNKNOWN.
- B — минимально сверить contract/query/counts, cutoff и composition. Условно предпочтителен (C-004/C-005/C-010); сильное возражение — задержка реального улучшения, входы/стоимость UNKNOWN.
- C — исследовать конкретный барьер paid-учебного опыта. Возможна пользовательская польза; сильное возражение — барьер не обнаружен, paid ratio вырос, causal basis отсутствует.
- D — остановить отдельную emergency-retention инициативу и освободить ресурс; продукт не закрывать. Возможна экономия; сильное возражение — скрытая проблема и measurement debt сохраняются, объём высвобождения UNKNOWN.
- E — исследовать экономику acquisition mix. Состав меняется; сильное возражение — costs/payments/learning linkage отсутствуют, смена каналов не обоснована.

Ресурсы, цепочки бизнес-ценности и условия потери предпочтительности подробно записаны один раз в options.md. Эффекты, выручка, затраты, часы, размер выборки и пороги UNKNOWN.

Выбранный процесс B описан в strategy-product.md: внутренние PO/analytics/product/acquisition роли получают versioned contract, lineage/count reconciliation, missingness и decision note. Условная ценность — уменьшить риск неверного распределения работ; выручка/избежанные затраты/стоимость/capacity UNKNOWN. Сильное возражение — задержка полезного вмешательства; scope ограничивается и возвращается PO при недоступных входах (C-010). Другие варианты выше не переписаны и не объявлены ошибочными.

Коммуникация (strategy-communication.md): внутренняя аудитория PO и команды перед следующим выбором; барьер «aggregate decline = product deterioration» — HYPOTHESIS, не измеренный факт. Сообщение: состав объясняет арифметику, comparability/causality UNKNOWN; нет обещания роста. Proposed канал — этот memo с test-plan/receipts для внутреннего review, без отправок/публикации. Независимое content review подтвердило соответствие scope, формулам и locators (receipts/content-review-source.json). Следующий шаг — восстановить выбранную ревизию в действительно новом чате без исследования заново.

План B (test-plan.md): документальная сверка, comparator январь/февраль на одном owner-approved contract отдельно paid/organic; secondary standardized February. Scope — четыре mature CSV строки 2–5; март строки 6–7 лишь maturity/missingness check. Controlling R=100×unique qualifying returned eligible users / all eligible users who reached the approved interval; events/unit/dedup/eligibility/criterion/timezone/cutoff/latency UNKNOWN, пока decision-grade R UNKNOWN. Невозвраты остаются в denominator, missing outcomes не считаются success. Pooled=100×Σreturned/Σeligible; standardized=Σ(Jan eligible_segment/Jan eligible_all × Feb R_segment). Это не randomized/causal test.

Основной исход диагностики: contract/comparability confirmed, incompatible либо not established. Quality counts D_N=N_query−N_export и D_K=K_query−K_export, users; completeness=fully documented units/all prelisted eligible review units, незавершённые/missing остаются в denominator. Допустимые discrepancy margins/completeness threshold/statistical precision UNKNOWN, владелец PO+metric owner должен определить до старта; zero margin не назначен. Operational dates/cap/resources UNKNOWN. CSV true/30 и false/10 — поля источника, не утверждённое D30 окно. Весь новый query review NOT RUN; исходный calculation receipt переиспользован.

PASS только при authoritative contract, comparability/lineage и заранее согласованных quality criteria — поддерживает следующий выбор PO, не успех продукта. Incompatible measurement/discrepancies → REVISE, удержать продуктовый вывод. Нет входов/порогов/precision → INCONCLUSIVE, PO сужает/останавливает/разрешает отдельное уточнение. Запрещённые данные/действия или выход за scope/cap → STOP. Guardrails: no closed data/contacts/spend/product changes/pilot, сохранять версии/hashes/противоречия. При подтверждённом mix PO может рассмотреть E; самостоятельное evidence барьера может поддержать C, даже без within-channel decline. Исполнения этой диагностики сейчас нет.

- **Owner decision:** `DECIDED` — B; exact scope по S-006/E-008/C-009, исходный timestamp UNKNOWN
- **Execution approval:** на момент D0001 выбор B разрешает подготовку, но не исполнение; для будущего действия требуется отдельное applicable action/scope/revision/hash approval, проверяемое по фактическому append-only журналу
- **Next step:** в действительно новом чате Codex восстановить D0001, выбор PO, pinned sources, UNKNOWN и следующий управленческий шаг; не выполнять диагностику и не создавать новую ревизию в рамках read-only Resume

Выбор PO уже получен; повторный вопрос не требуется. Следующее подтверждение E2E — настоящий новый чат Resume; UNKNOWN параметры исполнения определяются до любого будущего старта. Результат текущего чата не является таким Resume.

Это host-backed agent/tool attempt, не внешнее человеческое принятие. Успешная проверка операторского создания не является демонстрацией самостоятельного free-form NEW создания.
