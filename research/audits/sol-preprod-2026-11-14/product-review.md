# Product review — решение, а не количество документов

## Вывод

Существующий продукт — inspectable file-based decision-support workflow. Он хорошо удерживает неопределённость, отвергает неподтверждённые обещания и сохраняет основания следующего шага. **Не доказано**, что он самостоятельно проводит глубокое рыночное исследование, улучшает реальные решения руководителя или дешевле сильного структурированного чата.

Это не вывод о бесполезности. Хорошие synthetic outputs полезны для regression testing; они не заменяют real-product evidence и human acceptance. Изученные substantive cases и границы — [inventory](inventory.md). Ниже подтверждены **статические P2-дефекты**; результат реального эксперимента не заявляется. `H/` = `research/qualification/host-acceptance/codex-0.169.0/20261114-r1-r2/`.

## P-01 — P2: success denominator отбрасывает abandonment

**Локатор:** `H/case/test-plan.md:6`, Primary metric. Contract: `.agents/skills/experiment-design/SKILL.md`, точный denominator и качество данных; `references/metrics.md`, missing/exclusions.

**Факт, OBSERVED_STATIC, высокая уверенность:** task success делится на eligible participants, **завершивших задачу с прототипом**, а не начавших её. Abandonment перечислен среди guardrails, но это не исправляет estimand основной метрики.

**Механизм, INFERENCE:** участники, которым прототип слишком труден и которые прекратили задачу, исключаются из знаменателя; сравнение conditional-on-completion может предпочесть более трудный вариант. Иллюстрация — вымышленный набор с двумя успешными завершениями и остальными отказами: success among completers может выглядеть идеальным, при плохом overall task success. Это логический counterexample, не наблюдённый study result.

**Влияние:** неправильный продуктовый выбор по biased success и слабая методология перед жюри. **Минимальное исправление:** заранее определить единицу participant/attempt и включить все eligible started attempts в основной denominator; assistance/abandonment отдельно; одинаковые правила для comparator. Не выдумывать владельца/порог.

**Regression, NOT RUN:** подать dataset с success, failures, assisted completion и abandonment. Основная метрика учитывает все eligible starts, только unaided-valid success в числителе, не удаляет отказавшихся как «пропуски». Дать те же правила текущему способу.

**Контрдоказательство:** план явно draft/not authorized и требует правил пропусков до старта. Не найдено ошибочного real study. Более корректный existing pattern: `cases/unseen-shelf-alerts-20261114/test-plan.md`, все eligible tasks attempted. Первичный reviewer B-01; независимое A/C cross-check см. final verdict.

## P-02 — P2: D30 определён заранее, хотя metric contract UNKNOWN

**Локатор:** `cases/retention-demo/test-plan.md:10`, Primary output; `cases/retention-demo/state.md`, Open questions/Blockers; `brief.md`, intake. Не путать с `cases/retention-f1-demo/metric.md`, где отдельный synthetic contract определён.

**Факт, OBSERVED_STATIC:** текущие state/decision оставляют D30 event/eligibility неизвестными, но план выбирает `Return On or After` — на 30-й день **или позже**. Для позднего возврата нет одинакового конечного cutoff/follow-up horizon.

**Механизм, INFERENCE:** exact-day D30, days 24–30 и on-or-after D30 — разные величины. Даже после согласования имени event этот выбор уже меняет metric; «достиг day 30» не даёт старой и новой когорте одинаковую возможность вернуться позже.

**Влияние:** незаметная подмена измеряемого результата и несопоставимые cohorts. Не опровергает текущую арифметику supplied synthetic 62%/38%.

**Минимальное исправление:** return criterion, time basis и cutoff оставить UNKNOWN до решения accountable analytics/product owner; формулу связать с согласованным contract, не vendor default. `cases/public-source-retention-smoke/test-plan.md`, Gate 0, уже даёт более осторожный образец.

**Regression, NOT RUN:** contract «активный день в дни 24–30», пользователь вернулся только на day 45. Он не retained по этому contract. Для on-or-after варианта отдельно задать и одинаково применять follow-up cutoff и maturity. Не выбирать одно определение из публичной vendor docs.

**Источник:** B непосредственно открыл [Amplitude, Return On / Return On or After](https://www.amplitude.com/docs/analytics/charts/retention-analysis/retention-analysis-calculation); документация различает варианты, но не определяет metric этого продукта. Parent напрямую проверил противоречие в local files. Высокая уверенность в static mismatch, dynamic calculation NOT RUN.

## P-03 — P2: standalone decision memo не выполняет собственный output contract

**Локаторы:** `cases/_template/decision.md`, поля status→review; `cases/meal-planner-demo/decision.md:5–10`; `cases/retention-demo/decision.md:5–11`; `cases/public-source-retention-smoke/decision.md`, Decision question and evidence; `cases/unseen-shelf-alerts-20261114/decision.md:11–15`.

**Контракт:** root `AGENTS.md`, Recommendation gates, требует critical source IDs + точные locators в кратком memo. `options-decision` требует явно перечислить альтернативы; `strategy-communication` — audience/moment/barrier/message/proof/channel в каждом memo; `experiment-design` — formula/denominator также в memo.

**Факт, OBSERVED_STATIC:** template decision не содержит communication/validation summary. В meal/retention memo не перечислены все альтернативы и преимущественно даны claim IDs вместо точных source locators. Unseen лучше показывает варианты и raw locators, но communication/validation package всё равно остаётся в соседних файлах. Current public-source memo отсылает к CL/E IDs, не давая прежний точный URL/section.

**Механизм, INFERENCE:** отправленная отдельно руководителю записка требует ручной сборки контекста; presence соседних файлов не исполняет обещанный standalone output. Это UX/контрактный дефект, не доказанная ложность рекомендации.

**Минимальное исправление:** синхронизировать template и publication gate с уже существующим контрактом: короткие варианты/отказы, critical facts с точными locator, внутреннее сообщение и канал, metric/comparator/unknown prerequisites, следующий human choice. Полные приложения оставить отдельно, не копировать всё исследование в memo.

**Regression, NOT RUN:** независимый руководитель получает только decision.md и называет альтернативы, решающее основание, где проверить цифру/условие, внутреннее сообщение, следующую проверку и критерий пересмотра. Если нужен соседний файл для критичного смысла — test fails; открываемые ссылки для подробной проверки допустимы.

**Независимость:** B-03; C проверяет контракт в cross-round. Уверенность высокая, влияние P2 из-за отсутствия наблюдённой ошибки пользователя.

## P-04 — P2: агрегат orders/opens превращён в условную конверсию

**Локатор:** `docs/implementation-status.md:75`, New unseen synthetic workflow: «6/13 opened records with an order record (46.15%)» и «6/18 with an order record». Inputs: `cases/unseen-shelf-alerts-20261114/input/pilot-alerts.csv:1–7`; protocol bullets о counts; E-003.

**Факт, OBSERVED_STATIC:** CSV даёт store-level суммы alert_generated, alert_opened и orders_within_7d, но не join `alert_id → open → order`, не one-order-per-alert counting rule. Dividing order records by opened alert records не устанавливает число opened alerts with order.

**Механизм, INFERENCE:** у S1 два открытых alert и один order могут совпадать либо не совпадать; store aggregates одинаковы. Значит conditional conversion неидентифицируема. Детерминированный reader query аудитора подтверждает деление 6/13, **не** поддержку его интерпретации. Ошибка семантическая, не арифметическая.

**Влияние:** статус проекта завышает качество evidence и может привести к ложному обещанию funnel performance. Core decision осторожнее, не использует это как causal/stockout proof.

**Минимальное исправление:** назвать их raw counts и ratio of aggregate record counts, не conversion. Настоящая конверсия требует linked units, dedupe и attribution window. Не дописывать отсутствующие raw данные.

**Regression, NOT RUN:** два alert-level synthetic datasets с одинаковыми store aggregates и различным overlap open/order. Из агрегата агент должен оставить conditional conversion UNKNOWN, сохранив верные totals.

**Независимость:** C-02, parent проверил CSV/protocol/status; A/B cross-review. Высокая уверенность в unsupported wording.

## Оценка реальной продуктовой глубины

| Измерение | Что действительно показывают файлы | Недоказанное / нужная проверка |
|---|---|---|
| Decision-focused intake | Решение, владелец, ограничения, unknowns; вопросы связаны с next step | Codex input уже содержит intake и research questions; способность самостоятельно выбрать существенное уточнение требует novel sparse brief |
| Глубина исследования | Проверка supplied claims, exact locators, vendor contradiction, открытая методика | Внешние источники в основных делах преимущественно methodology, не рынок/поведение/экономика; нужен разрешённый public-domain decision case |
| Альтернативы | Status quo, learning, launch/build, close различаются; objections есть | Нужен кейс, где два реализуемых active paths конкурируют по value/cost, а не только очевидно небезопасный launch |
| Рекомендации | Условная discovery/measurement рекомендация обоснованно не равна launch approval | Положительная ценность discovery не установлена при UNKNOWN стоимости/задержке; нужен explicit decision sensitivity |
| Экономика | Не придумана; F3 сохраняет paid shop-months, не shops/payback/demand | Реальная unit economics, opportunity cost, budget/time sensitivity отсутствуют; это gap доказательства, не повод заполнить фиктивные значения |
| Коммуникации | Обещания не превышают capability; внутренний memo вместо запрещённой рекламы | Не показана validated go-to-market/channel strategy; нужен реальный public offer case с доказанными terms/target context |
| Эксперименты | Comparator/guardrails/inconclusive ветка, owner gates, NOT READY честно | P-01/P-02 показывают, что наличие headings не гарантирует корректный estimand |
| Revision | C-009 supersedes C-005; C-010 меняет ordering constraint; separate fictional cohorts не pooled | Нет убедительного accepted-decision reversal с новым economic/price fact и re-approval; неизменная рекомендация сама по себе не ошибка |
| После принятия | Owner/trigger поля и state сохраняют следующий шаг | Основные cases всё ещё pending human; нет observed obligation completion, outcome review, overdue escalation или retire decision |
| Product-leader UX | Читаемые Markdown и visible unknowns, текущая next action | T-05/T-06/P-03; нет observed teach-back/decision task completion, активного времени/числа исправлений |

## Почему предыдущий PASS не закрывает findings

`H/acceptance-review.md` делает сильное ограничение PARTIAL PASS и признаёт неполный R1 diff. Однако таблица «План проверки» называет его PASS как draft и итог не находит P1/P2 содержательных ошибок. **P-01 уточняет этот вывод:** draft может корректно блокировать запуск, но содержать biased metric. Эти утверждения не взаимоисключающи. Аналогично корректные final ratios не закрывают T-01 provenance receipt.

В `research/product/overnight-audit-2026-11-14.md` описан независимый pass unseen artifacts; **P-04 касается status summary**, а не ошибки current case recommendation. Source→claim entailment требуется проверять и в summaries, не только ledgers.

## Чего не следует объявлять дефектом

- UNKNOWN sample/threshold/owner — корректно, когда отсутствуют данные и запуск запрещён.
- Synthetic interviews не реальны, и проект в изученных кейсах не скрывает это.
- Неизменная рекомендация при новых фактах может быть правильной: меняется допустимый protocol/constraint.
- Отсутствие external campaign при запрете контактов — соблюдение scope, не неработающая strategy.
- Нет real-market data — не доказательство неспособности найти их в разрешённом другом brief.
- Все текущие claims нельзя считать false из-за append-only исторического C-005: current state явно выбирает successor.

## Минимальная проверка ценности против чата

Предложение, не выполненный эксперимент. В [roadmap](implementation-roadmap.md) это отдельный acceptance, не метрика «число файлов».

1. Новый frozen corpus: один sparse brief с decision-changing fact; один достаточный для активного выбора кейс; один accepted-decision reversal. Старые inputs/keys/ledgers/scores не доступны кандидату.
2. B0 обычный чат, B1 сильный structured prompt, A folder workflow; одна модель/host/tools и заранее одинаковый time/resource budget. Persistence оценивается только если все arms могут реально сохранить/передать результат; active human handoff time включено.
3. Критичные факты, denominator, locators, promises, approval и integrity — бинарные gates. Затем blinded subject-matter rubric и teach-back руководителя; LLM judge — вспомогательная сортировка, не окончательная истина.
4. Считать coverage decision-changing facts, unsupported material claims, net corrected decisions, user time, interventions, fresh-session recovery, observed cost per accepted case. При нулевом accepted count cost/result N/A; unavailable billing UNKNOWN. Не обещать статистический эффект малого корпуса.
5. Решение KEEP только если файлы дают наблюдаемую пользу восстановления/проверки либо better decisions при приемлемых затратах. Если B1 сопоставим — честно позиционировать продукт как auditable workspace, не superior strategist.
