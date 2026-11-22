> PRIVACY-SAFE DERIVATIVE D0001 of source R0001. Historical E2E/Resume belong to the original; export checks validate exported bytes only. No execution approval transfers. See EXPORT.md.

# Validation plan — B, design only; not ready to execute

Подготовленный план проверки выбранного B. Подготовку разрешил PO (C-009/E-008/S-006, inputs/owner-message-B-20261122.md, items 1–4); новый доступ/сбор, реальные контакты, расходы, продуктовые изменения и пилот запрещены. Это диагностическая сверка, не causal A/B experiment. Сейчас выполнена только ранее сохранённая арифметика synthetic CSV, не новая диагностика.

## Вопрос, гипотезы и решения
Вопрос: позволяют ли definition/eligibility/query/maturity/missingness и периоды сопоставимо интерпретировать агрегат января/февраля до выбора intervention?

Проверяемое предположение B: ограниченная сверка даст достаточно оснований различить composition pattern и несопоставимое измерение. Конкуренты: instrumentation/eligibility/window/cutoff changes; скрытые subgroup/behavioral changes. Первый класс дизайн способен выявить при наличии спецификации/query/changelog. Причинный эффект acquisition, UX-механизм, сезонность и экономическую ценность этот дизайн не устанавливает; две последовательные когорты не рандомизированы.

Falsifier направления B: требуемых материалов нет в допустимом scope либо определения нельзя привести к согласованному контракту без нового исследования. Тогда не продолжать автоматически: INCONCLUSIVE и решение PO остановить/ограничить/пересмотреть scope. Сохранение within-segment роста не опровергает возможный барьер UX; для C нужны самостоятельные свидетельства.

## Метод, comparator и отбор
Предложена документальная reconciliation на допустимых существующих материалах, если позднее отдельно разрешены. Материал: authoritative metric specification, versioned query/export, extract/cutoff date, instrumentation changelog и таблица missing/exclusions. Сейчас их наличие/доступность UNKNOWN, закрытые данные не запрашиваются.

Comparator — январь и февраль 2026 на одном owner-approved contract, отдельно paid/organic; secondary — февраль со структурой января. Все четыре переданные mature month×segment строки (S-002 строки 2–5) входят в synthetic review scope, не случайная выборка. Март (строки 6–7) проверяется как negative maturity/missingness case, не как D30 comparator. Дубликаты/исключения/отказы в доступе фиксируются, не скрываются post hoc.

Единица reconciliation — заранее перечисленный month×segment×metric-version с полным lineage. Единица retention должна быть утверждена как уникальный eligible user с deduplication, сейчас UNKNOWN. При смене query/контракта старую и новую версии не смешивать. Нет recruitment/assignment, респондентов и task-success attempts; соответствующая usability success rate здесь не применяется.

## Контракт метрики и формулы
Основной диагностический исход: контракт и сопоставимость ПОДТВЕРЖДЕНЫ / НЕСОВМЕСТИМЫ / НЕ УСТАНОВЛЕНЫ. Перед проверкой PO и владелец метрики должны выбрать authoritative cohort-entry event/time basis, return event и exact-day/fixed-window/after criterion, unit/dedup, eligibility, numerator/denominator, maturity/latency, cohort dates/common cutoff. Всё отсутствующее — UNKNOWN. Vendor default не заменяет решение владельца (C-004/C-006).

Количественный объект сверки — R(m,s)=100×U_return(m,s)/U_eligible(m,s), %, где числитель — уникальные eligible users с утверждённым return criterion, знаменатель — все утверждённые eligible users, достигшие требуемого интервала по общему cutoff/latency. Невозврат остаётся в знаменателе; unknown outcomes не считаются успехом, показываются отдельно; незрелые интервалы не получают нулевой D30. Правила exclusion/missing должны быть зафиксированы до доступа и одинаковы в comparator. При неизвестном контракте controlling R UNKNOWN; пока можно показать только буквально supplied returned_d30/eligible_users.

Pooled R(m)=100×Σ_s U_return(m,s)/Σ_s U_eligible(m,s); segment share w(m,s)=U_eligible(m,s)/Σ_s U_eligible(m,s). Secondary standardized R(Feb|Jan mix)=Σ_s w(Jan,s)×R(Feb,s). Δ_total=R_Feb−R_Jan, Δ_within=R(Feb|Jan mix)−R_Jan, Δ_mix=R_Feb−R(Feb|Jan mix), единицы п.п. Не усреднять row percentages без соответствующих весов.

Quality diagnostics: абсолютные discrepancies D_N=N_query−N_export (users), D_K=K_query−K_export (users), отдельно по каждой единице; completeness = units with fully documented required lineage / all prelisted eligible reconciliation units, доля. Непроверенные/незавершённые/missing единицы остаются в completeness denominator, не засчитываются complete. Полный список units/исключений утверждается до проверки; диагностические показатели не доказывают причинность. Допустимые count margins, completeness threshold и significance/precision criteria UNKNOWN — не подставлять нулевой tolerance или произвольный процент. До их согласования нельзя объявлять numerical PASS.

## Периоды, зрелость и воспроизводимость
CSV маркирует январь/февраль true/30 дней, март false/10 дней (C-003/E-004/S-002 строки 2–7). Это наблюдаемые поля, не утверждённая operational D30 window. Exact cohort-entry dates, timezone, day boundary, extraction date, common follow-up cutoff/latency и стабильность instrumentation UNKNOWN. Мартовские пустоты не нули и не основание календарного прогноза.

Период operational review, ответственные имена/capacity и дата следующего PO review UNKNOWN; PO/analytics устанавливают их до любого разрешённого доступа. Дедлайн подготовки 22 ноября 23:59 MSK не задаёт observation window или SLA исследования. Не придумываются длительность, sample size, power или uplift target.

Уже выполненное: C-001/C-002/E-002/E-003, S-002 inputs/cohorts.csv строки 2–5; S-004 analysis/cohort-results.json monthly/segments/descriptive_january_reference_decomposition. January 1100/2000=55%, February 1000/2000=50%; segment changes +5 п.п., paid share 50%→75%. Standardized February=0.5×40%+0.5×80%=60%, within +5 п.п., mix at February rates −10 п.п., net −5 п.п. Разложение descriptive, January-reference и order-dependent, не causal channel effect.

Исходный receipts/calculation-run-001.json: redacted historical argv, source cwd omitted; input SHA-256 b6db2059086921629565ed1947b5fa7c91607d8aa19576d3b20efdac7e423ebd, Python 3.12.14, exit 0, source stdout; source stderr omitted in export, script hash. Exact Fraction arithmetic, конечные displayed values, missing не нули. Успешный run не повторён. Выполнение proposed query reconciliation NOT RUN; при будущей смене допустимых inputs новый run потребует нового pinned receipt, не переписывать старый.

## Guardrails и исходы
- Guardrails: только согласованные synthetic/допустимые материалы; никаких закрытых данных/PII, контактов, расходов, кампаний/продукта/пилота. Проверять hashes/lineage, сохранять contradictions и версии; не исключать незрелость/missing ради красивого результата.
- Ресурсный guard: cap аналитических часов/расходов и срок UNKNOWN, PO определяет до старта; при отсутствии/превышении — остановка и новое решение, не автоматическое расширение.
- PASS диагностики: выбран authoritative contract, подтверждён общий comparison scope/lineage, выполнены заранее согласованные (пока UNKNOWN) numerical quality criteria, нет неразрешённых смысловых противоречий. Это успех измерительной сверки, не продукта. Analytics/reviewer представляют PO результат. Если mix pattern сохраняется, PO может отдельно выбрать economics E; удерживается causal uncertainty.
- REVISE/неуспех: incompatible contract/query/maturity либо discrepancies за будущими согласованными пределами. Analytics сохраняет версии и issue, PO решает о корректировке измерения; продуктовый вывод удерживается, без молчаливого исправления входов.
- STOP/вред: запрещённые данные/действия или выход за согласованный scope/cap; немедленно прекратить исполнение и вернуть PO решение. Новых доступов не добиваться обходом.
- INCONCLUSIVE: материалы отсутствуют, outcomes/thresholds/cutoff не определены или precision недостаточна. Не PASS и не доказательство отсутствия эффекта; PO выбирает остановку, сужение либо отдельное разрешённое уточнение.
- Новое product evidence: сопоставимые данные о конкретном барьере могут поддержать C, economic linkage — E. Это новое решение PO, не автоматический запуск.

Владелец решения — PO; proposed roles — metric owner, analytics, reviewer, конкретные имена UNKNOWN. До исполнения нужны утверждённые contract/thresholds/scope/ресурсный срок и отдельное action/scope/revision+manifest-hash approval плюс host permissions. Выбор B и разрешение подготовить этот план не являются таким approval. Проверенное сохранение плана не означает готовность или разрешение исполнения.
