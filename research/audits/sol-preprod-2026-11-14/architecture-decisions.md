# Architecture decisions — предложено аудитом, не реализовано

Заданный baseline не менялся. Ниже решения для отдельного будущего implementation scope. Основания: [technical findings](technical-findings.md), [product review](product-review.md), [primary research register](research-findings.md). Формат — контекст, выбор, возражение, последствия и проверка, а не обещание работоспособности.

## ADR-01 — KEEP portable folder, CHANGE только хрупкие контракты

### Альтернативы

| Вариант | Польза | Риск/цена | Решение |
|---|---|---|---|
| A. Оставить текущую папку как есть | Нет новых зависимостей, inspectable outputs | Сохраняет P-01–P-04, T-01–T-06 и acceptance gaps | **CHANGE**: не выпускать unchanged как полностью accepted |
| B. Папка + ясный checkpoint/output contract; узкий deterministic helper только по доказанному отказу | Сохраняет portability и устраняет конкретные механизмы | Нужно проверить consistency на целевом host; manual discipline не гарантия | **KEEP/CHANGE**, рекомендуемый путь |
| C. Graph/workflow runtime + durable DB + постоянная панель моделей | Может формализовать concurrency/checkpoints и сложную оркестрацию | Setup, credentials, migrations, повтор действий при resume; нет measured benefit | **DEFER** до подтверждённой необходимости |
| D. Закрыть собственный workflow и использовать сильный B1 prompt | Снижает сопровождение при равном качестве | Теряется удобная история/сохранение, если они полезны | **DEFER** как честный результат value experiment; **KEEP** B1 как comparator |

**Решение:** B. Не требуется новый сервер, MCP или provider, чтобы исправить denominator и source entailment. **Контраргумент:** без deterministic publish tool дисциплина файлов может остаться ненадёжной. Ответ — сначала явно определить invariant и проверить прерывание; если ручной путь не проходит, добавить именно check/publish, не полномасштабный orchestrator.

**Acceptance:** новое дело проходит binary result contract и complete-checkpoint resume в разрешённой конфигурации. Никакой software choice не закрывает G-02 scope/video или human acceptance автоматически.

## ADR-02 — KEEP один canonical Skills tree

**Факт:** шесть local Skills имеют name/description, `.agents/skills/` поддерживается официальными Codex/Cursor docs (R-01/03/04). **Выбор:** одна каноническая копия; root route плюс explicit documented manual fallback, когда auto-use не доказан. Изменять trigger descriptions только по фактическому routing failure.

**CHANGE:** template/output contract должен согласовываться с правилами Skills, особенно standalone memo и experiment metric. Не добавлять отдельные «review», «economics», «memory» Skills только ради количества; сначала поместить узкую missing procedure в существующий момент работы.

**Контраргумент:** host-specific integration удобнее отдельного tree. Учитывать только если actual compatibility case не решается canonical path/manual invocation. Не поддерживать два источника истины ради гипотетического host.

**Acceptance:** normal host discovery и фактическое чтение нужного skill показаны отдельно; false-positive/false-negative trigger записаны. Listing alone не PASS workflow. Public docs — не доказательство локального запуска.

## ADR-03 — CHANGE complete-checkpoint protocol; DEFER автоматический publish до теста

**Проблема:** T-02/T-03. Current state/decision snapshots не покрывают общую публикацию и historical dependencies.

**Предложенный минимальный invariant:**

1. Один активный writer на дело. Reviewers — read-only; multiwriter не заявлять.
2. У checkpoint есть revision, parent и перечень artefacts/актуальных claim IDs. Existing immutable records не переписываются.
3. Decision/supporting outputs ссылаются на согласованную ревизию; прежняя версия изменённых dependencies либо полный diff доступна.
4. Незавершённая revision не current. Resume при отсутствующих/несовпадающих files/IDs останавливает использование новой версии и показывает conflict, не угадывает latest по дате.
5. Last complete checkpoint можно открыть из файлов без chat history. Правка делает новый checkpoint, а не перезаписывает историческое согласие.
6. Любая операция с внешним эффектом имеет самостоятельный human approval; checkpoint не означает exactly-once внешнего вызова.

**Trade-off:** full snapshots просты и inspectable для малого дела, но копируют больше данных; diffs компактнее, но усложняют восстановление. До конкурса — сохранить изменённые небольшие decision-support files, не создавать собственную event-sourcing платформу. При больших данных хранить версионные ссылки/оригиналы, а не бездумно копировать весь корпус.

**Acceptance:** interruption после каждой записи; old complete / new complete / explicit conflict — допустимы, silent mixed version — FAIL. Byte hashes могут подтвердить идентичность, не истинность источника. Windows/file-system publication semantics требуют actual check, не POSIX assumption.

## ADR-04 — CHANGE расчётные и evidence receipts; KEEP semantic review

**Проблема:** T-01/T-04 и P-04. **Выбор:** расчётный receipt хранит input locator/version, exact expression/query, cwd, permitted tool/version, result и status; source attempts имеют отдельные IDs/results. Если host telemetry недоступна — UNKNOWN, не выдуманная точность.

**Роли проверок:**

| Проверка | Что может установить | Чего не устанавливает |
|---|---|---|
| JSON/schema/ref checker | Parse, required fields, unique IDs, refs, successor graph/current selection | Поддержку смысла утверждения источником |
| Deterministic calculation | Верное вычисление по конкретным входам/формуле | Правильность события/знаменателя/атрибуции |
| Source-grounded independent review | Entailment, scope/date, counterevidence, unit semantics | OS permissions и успешность невидимых прошлых calls |
| Hash/manifest | Идентичность сохранённых bytes | Истинность или legal validity содержания |

**Минимум до конкурса:** исправить в будущих outputs конкретные semantics/receipt gaps, повторно проверить критичные основания. Bundled validator — после observed structural failure или повторяющегося ручного труда, не обязательная зависимость ради схемы.

**Acceptance:** corrupted JSON, duplicate ID, dangling source/evidence ref, cycle/неразрешённый current successor вызывают явный structural blocker. Семантически неверный, но открываемый source проверяется отдельно. Исторические недостающие receipts не реконструировать как оригиналы.

## ADR-05 — KEEP human-in-the-loop, CHANGE version-bound consent

**Факт:** current cases pending owner, C-010 требует подтверждения каждого будущего заказа; это доходит до всех inspected consumers. Реального обхода не установлено.

**Выбор:** recommendation ≠ decision ≠ approval to execute. Future approval привязано к decision revision, scope/action, relevant claims/terms и владельцу; изменившееся решающее основание требует re-approval. Hypothesis о stale-consent risk остаётся UNVERIFIED до сценария с прежде одобренным решением.

**Контраргумент:** добавление структуры consent усложняет file UX. Минимум — короткая читаемая запись с версией и action scope, не auth server. Инструкции не заменяют host permission boundary (R-14).

**Acceptance:** после изменения цены/региона/заказа старое согласие не запускает действие; no owner/no scope = explicit stop. Approved product direction не разрешает contact, spending или publication автоматически.

## ADR-06 — KEEP один lead; DEFER постоянный council/learned router

**Основание:** R-05/07, exploratory B1 близок к A; все нынешние auditors имеют одну exposed model. **Выбор:** optional specialist read-only reviewer на high-impact conflict/critical number/unsupported promise. Сначала independent conclusion по источникам, потом bounded cross-examination. Один writer интегрирует.

**Контраргумент:** одиночный lead может пропустить breadth. При нескольких независимых research slices делегировать, но просить source-backed findings и budget, не consensus. Reviewer не подменяет material human choice.

**Routing:** deterministic расчёт → permitted calculation tool; exact source verification → reader; missing permission/source → blocker/request owner, не model escalation; complex ambiguous synthesis → сильная доступная модель при явном trade-off. Learned router оправдан только log-backed task distribution и cost-quality measurements; RouteLLM paper abstract не достаточен для package adoption.

**Acceptance:** compare source-grounded second pass, optional reviewer и fixed lead при matched budget; keep если net verified corrections или measured savings, без новых critical errors. Не засчитывать повтор текста или model agreement.

## ADR-07 — DEFER OptiLLM; REJECT скрытый обязательный proxy

**Основание:** R/OSS inspection в research-findings: license и source/tests открыты; MoA padding дублирует первую completion, generic critique fallback может скрыть отсутствие реального review; полный host tool/stream contract не проверен. Это не vulnerability текущего продукта: OptiLLM не runtime dependency.

**Возможная польза:** отдельный inference-scaling experiment на задачах с проверяемым answer и budget, возможно cheaper model + selective escalation. **Риски:** latency/call multiplication, candidate correlation, provider secrets, tool semantics, deployment/dependencies и неполный usage accounting.

**Выбор:** до конкурса не интегрировать. После — один explicitly approved experimental approach и pinned version, только если direct/B1/source-recheck не справляются и есть измеримый выигрыш. Не использовать MoA как «три независимые модели».

**Acceptance:** preserved tool/stream IDs, recorded actual unique candidates/failures, truthful degraded status, полный наблюдаемый usage/time, no increased permissions, better accepted outcomes при бюджете. Все unavailable cost components UNKNOWN. Никакой запуск в этом аудите не выполнялся.

## ADR-08 — CHANGE продуктовый результат: concise decision package + outcomes

**Проблема:** P-03; документы полезны, но руководитель должен принимать решение без ручной сборки многих файлов.

**До конкурса:** один current decision memo: вопрос/владелец/status, альтернативы/отказы, critical facts с IDs+locators, аудитория/барьер/сообщение/proof/channel, validation summary/unknown prerequisites, следующее решение/trigger. Подробности в приложениях, не повтор всего корпуса.

**После конкурса:** обязательства/метрики/owner/due/сигнал пересмотра и фактический outcome с source. Без scheduler claim: можно запускать review вручную через fresh session; automatic monitoring — отдельная интеграция при потребности.

**Acceptance:** leader teach-back и genuine accepted-decision reversal; outcomes могут быть confirmed/revised/insufficient, не auto-positive. Если пользователь не понимает смысл, полнота файлов не считается продуктовым успехом.

## ADR-09 — CHANGE gate vocabulary и упаковку; KEEP честные UNKNOWN

**Выбор:** раздельные состояния prepared walkthrough, historical reported host execution, clean single-host acceptance, cross-host portability, submission. Current baseline doc drift T-06 не лечится одним общим PASS.

**Release:** owner adjudicates G-01; public-source safety policy не аттестует OS. Official brief/video/doc/jury access/submission G-02 завершаются отдельно. Optional portability не навязывается как organizer mandate.

**Acceptance:** два читателя получают одинаковый current status и next step; каждый PASS имеет artifact/result и границу. Не обещать zero cost: отсутствие отдельного сервера не делает модель/поиск/человека бесплатными.

## Триггеры пересмотра архитектуры

- Повторяемый missing critical source при правильном извлечении → сравнить lexical search с индексом; до этого **DEFER** RAG/vector DB.
- Реальный формат даёт critical extraction loss → проверить один parser по оригиналу и locator fidelity; до этого **DEFER** universal ingestion stack.
- Manual complete checkpoint не проходит interruption test → узкий publish/check helper; не сразу runtime.
- Несколько реальных writers/long-running jobs и восстановление между процессами → рассмотреть persistent engine после измерения нужды.
- B1 не хуже по решениям, а file recovery/verification не экономит работу → сократить artefacts/instructions либо честно закрыть самостоятельный product claim.
