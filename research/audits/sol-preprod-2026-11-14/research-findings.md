# Targeted deep research — решения, которые меняют продукт

## Граница исследования

Получено 2026-11-14 через public static reads/search. Не запускались OptiLLM, Polza, paid API, чужой код, installers или benchmark. Search snippets использовались только для discovery; итоговые опоры открыты. Ни vendor benchmark, ни paper result не переносится на этот продукт без local evaluation. Из-за разрешения создавать только восемь Markdown-отчётов source/evidence/claim register встроен сюда; продуктовые JSONL не пополнялись.

Вопросы выбраны по возможному изменению решения:

| Вопрос | Какой ответ меняет действие |
|---|---|
| Достаточны ли шесть file Skills без нового runtime? | Реальный discovery/use сбой потребует точной правки trigger/path, не второго skills tree |
| Нужны ли постоянные subagents? | Только net verified corrections / breadth gain при бюджете оправдывают дополнительные calls |
| Что маршрутизировать? | Детерминированные расчёты — инструменту; source/permission gap не исправляется более сильной моделью |
| Как сохранить/revise state? | Missing coherent checkpoint и historical dependencies требуют явного протокола, а не автоматического framework migration |
| Как не заменить исследование документами? | Покрытие decision-changing facts, проверки альтернатив и sensitivity важнее числа citations/files |
| Как доказать выигрыш над чатом? | Equal-budget B1 и реальные recovery/leader outcomes могут как оправдать workflow, так и потребовать его упрощения |
| Даст ли OptiLLM полезность? | Только локально измеренный gain и host/tool compatibility оправдают отдельный proxy; исходники дают конкретные риски |

## Открытый source register

Все статусы ниже — о содержании источника. Уверенность высокая в прочитанном тексте, но эмпирические результаты авторов не воспроизводились.

| ID / источник | Publisher, дата/версия и точный locator | Что поддерживает / ограничения |
|---|---|---|
| R-01 [Agent Skills specification](https://agentskills.io/specification) | Agent Skills; live docs без даты релиза; Directory structure, Frontmatter, Progressive disclosure, File references | `SKILL.md`, name/description, on-demand resources; `allowed-tools` experimental. Не capability/permission enforcement |
| R-02 [Skill creator practices](https://agentskills.io/skill-creation/best-practices) | Agent Skills, live docs; Refine with real execution; Add what the agent lacks; Match specificity to fragility; Provide defaults, not menus | Инструкции из реальных исправлений, concise procedures, trace evaluation, prescriptive fragile operations. Guidance, не сравнительный benchmark нашего набора |
| R-03 [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills) | OpenAI, live docs без publication date; How to use skills, Where Codex loads local skills, Best practices | Explicit/implicit invocation, `.agents/skills` traversal, description-based matching; docs не доказывают actual activation местных Skills |
| R-04 [Cursor Agent Skills](https://cursor.com/docs/skills) | Cursor, live docs; How skills work, Skill directories, Viewing skills | `.agents/skills/` и normal UI discovery; agent decides relevance. Совместимость формата не равна переносимости permissions/tools/state |
| R-05 [Multi-agent research system](https://www.anthropic.com/research/multi-agent-research-system) | Anthropic Engineering, 13.06.2025; Benefits; Prompt engineering; Effective evaluation; Production reliability; Appendix | Отдельные contexts помогают decomposable breadth-first research; высокая token overhead; нужны бюджет, чёткие slices, end-state evaluation. Internal vendor results CLAIMED, не внешний comparative proof |
| R-06 [Demystifying evals for AI agents](https://www.anthropic.com/research/demystifying-evals-for-ai-agents) | Anthropic Engineering, 09.01.2026; Structure of an evaluation; Types of graders; Capability vs regression; Evaluating research agents | Outcome ≠ финальное сообщение; trials, harness effects; code/model/human graders, groundedness+coverage+source quality, human calibration. Engineering guidance, не доказательство efficacy продукта |
| R-07 [Towards a Science of Scaling Agent Systems, v3](https://arxiv.org/html/2512.08296v3) | Kim et al., arXiv v3, 08.04.2026; Abstract, §§1, 3.1–3.2 | Controlled topology/model/tool/compute comparisons; architecture-task alignment, coordination tax, ограничения независимых aggregation. Preprint; нет продуктовых стратегий из этого repo. Не применять опубликованные thresholds как универсальный router |
| R-08 [RouteLLM](https://arxiv.org/abs/2406.18665) | Ong et al., arXiv 26.06.2024, прочитан abstract | Preference-trained strong/weak model routing может менять cost/quality trade-off. Только abstract-level evidence; не инспекция code/tests/license и не выбор пакета |
| R-09 [GOV.UK discovery](https://www.gov.uk/service-manual/user-research/user-research-in-discovery) | GDS/User research community, 18.11.2016; How to do…, Who to research with, Typical activities | Текущий task/process, наблюдение/данные/исследование разных пользователей до build. Government service method, не свидетельство спроса на ShelfSignal/meal-planner |
| R-10 [AAPOR Disclosure Standards](https://aapor.org/standards-and-ethics/disclosure-standards/) | AAPOR; displayed Code April 2021, page modified metadata 26.08.2026; III.A instrument/population/sample/precision/processing/limitations | Прозрачность методики нужна для независимой оценки, но сама не удостоверяет rigorous sample или demand |
| R-11 [AAPOR Transparency Initiative](https://aapor.org/standards-and-ethics/transparency-initiative/) | AAPOR, page modified metadata 21.09.2026; Items for Immediate Disclosure, items 3–12; FAQ “Will…quality…” | Современные AI disclosure, generated vs human responses, human validation, QC и limits. TI прямо не оценивает качество методов. Не смешивать обновлённую TI page с wording старой Disclosure page |
| R-12 [Green Book 2026](https://www.gov.uk/government/publications/the-green-book--2/the-green-book-2026) | HM Treasury; updated 28.10.2026; Business as usual, Selecting a shortlist, Sensitivity analysis and switching values | Fair BAU как benchmark, do-minimum vs ambitious options, чувствительность выбора. UK public appraisal, не нормативная российская коммерческая unit economics. Адаптировать вопросы, не копировать social discount/rates |
| R-13 [Trustworthy Experimentation: During-Experiment](https://www.microsoft.com/en-us/research/articles/patterns-of-trustworthy-experimentation-during-experiment-stage/) | Microsoft Research ExP, 25.01.2021; Capture Unexpected Effects; taxonomy table; Use Segments Stable during A/B Test; Measure Early/Often | Data-quality/OEC/diagnostics/guardrails различаются; post-treatment segmentation и repeated peeking требуют осторожности. Не основание автоматически выбирать длительность/threshold нашего теста |
| R-14 [OWASP LLM01:2025](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) | OWASP GenAI, version 2025, modified metadata 17.04.2025; Indirect injections; Prevention and Mitigation 1–7 | External content отделять, least privilege, high-risk human approval, deterministic output checks и adversarial tests. Не утверждает fool-proof prompt-only prevention |
| R-15 [LangGraph Persistence](https://docs.langchain.com/oss/python/langgraph/persistence) и [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) | LangChain, live docs без pinned version; Checkpointer vs store; MemorySaver…; Resuming interrupts | Persistence и durable storage различаются; node restarts from beginning, code before interrupt выполняется повторно. Framework не даёт exactly-once external actions автоматически; внедрение не выбрано |
| R-16 [MGIMO rules](https://challenge.mgimo.ai/rules) | МГИМО, ред.22.10.2026; §§3.2,4.1,5,6,7 | Organizer-level deadline/criteria/submission/rights; не authenticates MegaFon-specific brief |

### Claim register и решения

| Claim | Evidence | Статус, уверенность, decision implication |
|---|---|---|
| RC-01: existing canonical Skills layout соответствует документированному формату | R-01/03/04 + все local Skills | DOCUMENTED/OBSERVED_STATIC, высокая; **KEEP** один tree. Actual host use UNVERIFIED |
| RC-02: постоянный council не обоснован имеющимися результатами | R-05/07 + local F1/F2/F3/F9 limits | INFERENCE, средняя-высокая; **DEFER** always-on panel, **KEEP** bounded risk-triggered review |
| RC-03: host tool и model selection — разные проблемы | R-03/14 + T-01/G-01 | INFERENCE, высокая; capability/permission check раньше model escalation |
| RC-04: durable decision support требует coherent checkpoint и dependencies, не обязательно graph engine | T-02/T-03, R-15 | INFERENCE, высокая для need, UNKNOWN для лучшего implementation; **CHANGE** file protocol, **DEFER** runtime |
| RC-05: точный denominator и source entailment нельзя заменить citations/согласованием моделей | P-01/P-02/P-04 + R-10/11/13/14 | OBSERVED_STATIC/INFERENCE, высокая; semantic checks критичных claims до release |
| RC-06: экономическую рекомендацию следует проверять на переключающих параметрах | R-12 + F3 inputs | INFERENCE, высокая как полезный метод; no invented probabilities/NPV при missing inputs |
| RC-07: benefit over chat остаётся UNKNOWN | local F1/F2/F3/F9; R-06/07 | OBSERVED limits, высокая; claim только auditable workspace до matched proof |
| RC-08: OptiLLM может быть experiment arm, но не необходимый runtime/core reviewer | OSS inspection ниже | INFERENCE, высокая до конкурса; product-quality gain и tool compatibility UNKNOWN |

## Skills: минимальные изменения вместо разрастания

Шесть коротких Skills в baseline — достаточное разумное разбиение по моменту применения. Они не нуждаются в обязательном Python package только ради формата. R-01 советует resources on demand; R-02 — фактические trace corrections и инструмент только для fragile repeatability. Существующие known failures дают конкретные кандидаты:

- **CHANGE** experiment-design при семантической проверке denominator/temporal contract, не новые headings.
- **CHANGE** template/output gate для concise standalone memo, не второй стиль документа.
- **CHANGE** resume protocol: complete revision/active successor/current decision dependencies и explicit conflict stop.
- **KEEP** skill-first routing из root; test normal discovery отдельно от explicit manual read. Наличие `allowed-tools` не заменяет разрешения host.
- **REJECT** дублировать Skills в `.cursor/`/`.codex/` без наблюдённого compatibility дефекта; это создаёт вторую каноническую версию.

Acceptance должен показывать, что correct skill загружен и applied на ordinary task без имени skill в запросе; ручной вызов допустим как отдельно заявленный fallback. Не нужно доказывать магическую «автоактивацию» для работоспособности явно ручного режима, но нельзя заявлять её без следа.

## Subagents и independent review

R-05 обосновывает параллельную исследовательскую ширину; R-07 показывает обратные эффекты coordination и task dependence при matched compute. Вместе они не противоречат: эффект зависит от задачи, ресурсов и проверки aggregation. Три фактических reviewers этого аудита нужны по запросу пользователя, но не доказывают, что их надо постоянно поставлять в продукт.

Предлагаемый маршрут: один ответственный writer; optional read-only domain/source challenger при material contradiction, expensive irreversible choice, unsupported promise или fragile numeric threshold. Reviewer получает original question/constraints/sources без выбранной рекомендации; потом один cross-round по новым возражениям. Два раунда без нового evidence — stop, unresolved disagreement сохраняется. Засчитывать net verified corrections, не длину дебатов и не совпавшие выводы. Все текущие reviewer sessions показывают одну exposed model `openai-codex/gpt-6.1-sol`; diversity провайдеров/семейств не установлена.

## Research workflow и продуктовые стратегии

R-09/10/11 поддерживают проверку реального task/process, recruitment/instrument и прозрачности. R-12 добавляет neglected в MVP вопрос: **при каком допустимом cost/value/delay значении предпочитается другой вариант?** Если answer неизвестен, можно запросить диапазон у владельца и показать сценарий, но нельзя назвать discovery оптимальным просто потому, что launch не доказан.

Небольшой decision-research ledger должен содержать: вопрос → какие ответы меняют действие → allowed source → результат/unknown → affected claim/option → next action. Сначала supplied evidence, затем первоисточник и targeted disconfirming check. Stop при устойчивости выбора на обоснованных диапазонах, недоступности decisive evidence или исчерпании согласованного бюджета; последние два исхода дают условную рекомендацию, не бесконечное накопление документов.

Communication проверять на capability/terms и ситуации выбора, а не только на красивый wording. Internal-only memo правомерен при no-contact scope, но не является проверенным go-to-market. Для реального channel decision нужны наблюдаемый barrier, доступная audience и разрешённый тест; никакой синтетический собеседник не заменяет user evidence.

## State / revising accepted decisions

Не превращать Markdown в вторую платформу. Сначала определить authoring/recovery invariants: immutable IDs/history; complete revision boundary; active successor selected; version-bound approval; изменённые dependencies доступны исторически; uncertain external attempts не повторяются незаметно.

Manual last-complete snapshot плюс manifest может быть достаточен для одного writer, но это hypothesis до fault test. Если публикация нескольких файлов доказанно ломается, узкий standard-library check/publish инструмент предпочтительнее server/graph migration. Persistent store/graph runtime рассматривать только при многопроцессной координации или измеренном recovery failure, который минимальный контракт не устраняет. R-15 напоминает: RAM memory не durable, а resume может повторить code before interrupt; перенос framework не отменяет idempotency и human gates.

## Evaluation against ordinary LLM chat

R-06 различает transcript и реальный outcome; наличие final «saved» не доказывает сохранённые файлы. Local exploratory outputs не matched на model/tools/context/persistence, а F2 hardened run 47 читал full state/ledgers с готовыми выводами. Это полезная integration regression, не raw holdout. Claim training contamination не установлен.

Предлагаются два независимых результата:

1. **Capability acceptance:** binary material facts/critical arithmetic/promises/approval/state integrity + concise human-readable decision package.
2. **Value experiment:** B0/B1/A с одинаковой моделью/tools/raw inputs/budget; blinded outcomes и human teach-back; time includes setup, corrections и handoff. Recovery сравнивать при одинаковой возможности сохранить результат, не saved A против answer-only B.

На малом корпусе публиковать task-level outcomes и uncertainty, не population superiority. Coverage и unsupported claims считать вместе: отказ от всех содержательных утверждений не должен выигрывать оценку. Cost per accepted outcome включает observable model/search/tools/retries и human effort; actual invoice, estimate и UNKNOWN различаются. До конкурса достаточно narrow honest proof; широкое сравнение — после reliability gates.

## OptiLLM: адресная инспекция, не запуск

**Решение: DEFER integration; KEEP как кандидат offline/authorized post-contest evaluation arm.** OptiLLM оптимизирует inference, не заменяет source acquisition, evidence integrity, metric contract или approval.

### Что открыто

Текущий публичный репозиторий — [algorithmicsuperintelligence/optillm](https://github.com/algorithmicsuperintelligence/optillm). Старые codelion paths остаются в metadata; search fallback выдал сторонний fork/обобщение, которое **не использовано как proof**. Primary GitHub API/root затем открыт напрямую.

- [Repository metadata](https://api.github.com/repos/algorithmicsuperintelligence/optillm): API сообщил `archived:false`, `pushed_at:2026-11-02`; это признак активности, не качество поддержки.
- [README](https://raw.githubusercontent.com/algorithmicsuperintelligence/optillm/main/README.md), Selecting a technique, Combining techniques, Plugins, Security, Testing: OpenAI-compatible proxy, подходы/комбинации/router, отдельные external-action plugins. Рекламные «drop-in», «2–10x», «production ready» — **CLAIMED**, продуктовые преимущества не воспроизведены.
- [pyproject.toml](https://raw.githubusercontent.com/algorithmicsuperintelligence/optillm/main/pyproject.toml): version `0.4.1`, Python ≥3.10, default dependency set включает torch/transformers, Flask, LiteLLM, Selenium и др. Существование proxy-only пути в README учитывается; тяжёлый default не доказывает невозможность облегчённой сборки.
- [LICENSE](https://raw.githubusercontent.com/algorithmicsuperintelligence/optillm/main/LICENSE): Apache-2.0; redistribution §4 требует сохранить license/notices и отметить изменения. Это не полный license audit зависимостей/моделей.
- [optillm.py](https://raw.githubusercontent.com/algorithmicsuperintelligence/optillm/main/optillm.py): thin wrapper imports main.
- [moa.py](https://raw.githubusercontent.com/algorithmicsuperintelligence/optillm/main/optillm/moa.py), `mixture_of_agents`: initial provider request с `n=3`, sequential fallback, padding, critique/final synthesis. API listing отдал blob SHA `6f5f9ad7e63c2e67d65a01784d203d3022b77f89` для прочитанного main-пути.
- [tests/test_approaches.py](https://raw.githubusercontent.com/algorithmicsuperintelligence/optillm/main/tests/test_approaches.py): прочитаны MockClient/MockBadClient, signatures, basic calls, degraded-response и request-scoped MCTS tests. Basic mock calls не являются продуктовой оценкой MoA; не заявляется аудит всего suite или его PASS. API blob SHA `d5f78cb0786b2f53a80c8e8ec8a1d044df756cf4`.

Все main URLs moving. Перед reuse нужен pinned commit и полный dependency/license review; в этом аудите пакет **не выбран, не установлен и не исполнялся**.

### Механизмы, меняющие решение

1. `moa.py`, `if len(completions) < 3`: недостающие candidates добираются копией первого. Значит «три кандидата» не гарантируют три независимых результата. Это непосредственно прочитанный код, не observed provider failure.
2. При невалидной critique используется generic `All candidates show reasonable approaches…`. Такую строку нельзя считать реально выполненным independent review. Нет оснований переносить этот fallback в доказательный продукт.
3. MoA запросы в прочитанной функции передают system/user text и параметры generation, но не воспроизводят весь live tool workflow. Полную несовместимость proxy с tools из этого **не** выводим: требуется проверка выбранного approach/host, stream/tool-call IDs, permissions и usage aggregation.
4. Completion-token accumulation в функции — не полная стоимость всех provider inputs/retries/human work. Прокси нельзя использовать как shortcut к доказанному cost accounting.
5. Inference scaling не добывает отсутствующий metric contract, raw links или реальное человеческое согласие. Эти gap устраняются источником/владельцем, не sampling.

### Возможный полезный эксперимент после конкурса

Один frozen task set, direct single pass против обычного source-grounded second pass против **одного** выбранного OptiLLM approach; одинаковые источники и overall budget. Пропуск/дублирование candidates явно recorded, provider errors не превращаются в положительный verdict, полный usage/latency включая failed calls. Проверить tool/schema/stream contracts и отсутствие более высокого privilege. Считать verified corrections minus introduced errors и decision-changing omissions, не stylistic preference.

До измерения default **DEFER**. Постоянный OptiLLM server ради «масштаба нейротехнологий» — **REJECT**: добавляет отдельную эксплуатационную поверхность без доказанной пользы для текущих findings.

## Что остаётся UNKNOWN

Real-user decision quality, representative domain demand, cost per accepted outcome, automatic host skill use, crash recovery, cross-host equivalence, semantic judge calibration и выигрыш OptiLLM. Новые технологии не предлагаются как замена этих неизвестных. Конкретные решения/acceptance — [architecture-decisions.md](architecture-decisions.md) и [implementation-roadmap.md](implementation-roadmap.md).
