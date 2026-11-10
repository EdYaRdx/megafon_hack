# Researcher C — models and tools evidence

Дата проверки: 2026-11-10. Read-only исследователь; ниже evidence report. Main и pinned release различаются.

## Summary

Для `findings/c-models-tools.md`: сохранять текущий Codex/OMP как базовый маршрут. **Единственный session-proven selector — `openai-codex/gpt-6.1-sol:high`.** Другую модель/семейство не вызывал. Файлы не изменял; генерацию, установки, логины, проверки аккаунтов и credential stores не выполнял.

Критичные находки:

1. **GPT-6.1 Sol требует Responses API для tool calling.** Поэтому обычный Chat Completions proxy — не гарантированно совместимый агентный backend.
2. **Polza Responses — beta/stateless адаптер поверх Chat Completions**, а не полная реализация OpenAI Responses. Совместимость конкретно с GPT-6.1 Sol tools — **UNKNOWN**, несмотря на объявленные capabilities.
3. **OpenDesign README «read-only by default» расходится с MCP-реализацией:** сервер публикует также запись, удаление, генерацию и начало cloud login.
4. **OptiLLM v0.4.1 сохраняет debug-логирование Bearer token в `server.py:1009`**, хотя release исправляет другую утечку MCP secrets.
5. **Council действительно предписывает отдельные вызовы, спор и Chairman**, но допускает полностью симулированные места; обнаружение CLI не подтверждает auth, entitlement или модельное разнообразие.

## Report

### Статусы доказательств

- **DOCUMENTED** — прочитана официальная документация/реализация; не означает работоспособность здесь.
- **VERIFIED** — наблюдалось практически; ниже ограничено текущей сессией/результатами Lead и публичным GET каталога.
- **CLAIMED** — маркетинговое/benchmark-обещание автора.
- **UNKNOWN** — не установлено.
- **FAILED** — конкретное неудавшееся действие.

### Компактная evidence matrix

| Канал/проект | Auth, доступ, деньги | Контекст, tools, structured, latency | Вывод |
|---|---|---|---|
| **OMP → Codex** | **VERIFIED, передано Lead:** OMP 18.18.6; redacted usage сообщает plan `plus`, 2%/5h и 19%/7d. Единственный session-proven selector: `openai-codex/gpt-6.1-sol:high`. Это не доказательство прямого API-доступа. | Работа текущей сессии наблюдается; точный фактический context cap, JSON Schema enforcement и latency — **UNKNOWN**. `structured=false` в локальной конфигурации нельзя превращать в обещание structured output. | Использовать текущий маршрут; не менять конфигурацию ради исследования. |
| **ChatGPT Plus / signed-in Codex** | **DOCUMENTED:** $20/месяц; subscription sign-in и API key — разные режимы оплаты. Plus не получает API credits по описанной программе Pro/Business. [Plans](https://learn.chatgpt.com/docs/pricing.md), [auth](https://learn.chatgpt.com/docs/auth.md), [API-credit eligibility](https://developers.openai.com/api/docs/guides/chatgpt-api-credits.md). | Оценка для Sol: 15–160 local messages/5h, **не фиксированный лимит**; local/cloud делят allowance, возможен недельный лимит. Docs указывают 500K default context Sol в Codex/Work, но это не измерение OMP. Latency/SLA здесь **UNKNOWN**. | Не оценивать число включённых задач через API token prices; использовать redacted usage/reset info. |
| **Прямой OpenAI API** | **DOCUMENTED:** project API key/service account; собственные права и billing. Sol Standard, ≤272K input: **$2 input / $10 output / $0.10 cached input за 1M tokens**; cache writes 30m $2.50. >272K: $4/$15/$0.20. [API pricing](https://developers.openai.com/api/docs/pricing), [keys](https://developers.openai.com/api/docs/guides/api-keys.md). Доступ этого аккаунта **UNKNOWN**. | Sol: 1,050,000 context, 922,000 maximum input, 128,000 output; `low/medium/high/xhigh/max`, **нет `none`**. Streaming/structured supported; **tools только через Responses**. [Model specification](https://developers.openai.com/api/docs/models/gpt-6.1-sol). | Платные вызовы не делать. Прямой API тариф не приписывать подписочному OMP. |
| **GitHub Copilot** | **VERIFIED, Lead:** cached account snapshot `premium 0/200 monthly`; catalog содержит `github-copilot/claude-sonnet-4.6`, `github-copilot/claude-haiku-4.5`, `github-copilot/claude-opus-4.6`; inference не выполнялся. **DOCUMENTED:** нынешняя публичная billing-модель — AI credits, 1 credit=$0.01. Pro $10 → 1,500 credits; Pro+ $39 → 7,000; Max $100 → 20,000. [Billing](https://docs.github.com/en/copilot/concepts/billing-and-usage/individuals/billing). | Models зависят от plan, client и policies. Некоторые поддерживают 1M context/configurable reasoning; не все. Catalog ≠ entitlement, capability ≠ проверенный OMP adapter. [Supported models](https://docs.github.com/en/copilot/reference/ai-models/supported-models). Latency/strict JSON через текущий adapter **UNKNOWN**. | Cached `0/200` не согласовывать автоматически с современной публичной схемой. Нужна идентификация конкретного billing regime; без этого independent-family запуск не разрешать. |
| **Polza** | **DOCUMENTED:** `https://polza.ai/api/v1`, Bearer API key; публичный `/models` не требует auth. [Introduction](https://polza.ai/docs/api-reference/introduction.md), [models](https://polza.ai/docs/api-reference/models/list.md). **VERIFIED:** публичный GET каталога получен; auth/inference/balance не проверялись. | Tools/structured зависят от модели/провайдера. Timeout 600s — **не latency SLA**. RPM/RPD зависят от модели/организации/провайдера; конкретные account limits **UNKNOWN**. Responses beta/stateless, внутренне преобразуется в Chat Completions. | Только условный backend. Не включать через догадки об endpoint или «полную OpenAI compatibility». |
| **Local/Ollama** | **DOCUMENTED:** local `http://localhost:11434/v1/`, SDK key игнорируется. Remote cloud — отдельный ключ/доступ. [Compatibility](https://docs.ollama.com/api/openai-compatibility). Установленные веса, лицензии, GPU/RAM, endpoint здесь **UNKNOWN**. | Local tool calling и JSON Schema документированы; OpenAI API реализован **частично**. FAQ указывает default 4096 context; увеличенный cap зависит от настроек/модели/памяти. Cloud structured outputs сейчас не поддержаны. [Tools](https://docs.ollama.com/capabilities/tool-calling), [JSON](https://docs.ollama.com/capabilities/structured-outputs), [FAQ](https://docs.ollama.com/faq). | Не «бесплатная готовая замена»: стоимость оборудования/времени и качество неизвестны. Никаких pull/download/install сейчас. |
| **OpenDesign** | **DOCUMENTED:** Apache-2.0 local-first workspace; внешние CLI, BYOK или cloud billing. **FAILED, Lead:** `list_projects` → `MCP server not connected: open-design`. | Реальные preview/export/MCP реализации существуют; качества генерации и end-to-end экспорта здесь не проверяли. MCP source содержит операции записи/удаления/запуска. | Не подключать ради исследования инфраструктуры; потенциально полезен позже для визуальной демонстрации. |
| **OptiLLM** | **DOCUMENTED:** Apache-2.0 inference proxy, стоимость upstream calls остаётся; local inference тоже требует ресурсы. | Multi-request reasoning, не замена модели/подписки. Tools/JSON не сохраняются автоматически всеми techniques; streaming может быть синтетическим после окончания upstream. | Не ставить между OMP и Codex по умолчанию. |
| **Council** | **DOCUMENTED:** MIT skill/protocol для host agents и внешних CLI/API; собственных бесплатных inference credits не предоставляет. | Independent analyses → cross-examination → final stances → отдельный Chairman; возможны retries/enforcement и simulated fallback. | Заимствовать протокол проверки решений; не вводить второй orchestrator без отдельной необходимости. |

**Copilot pricing trap.** В нынешней официальной таблице Sonnet 4.6: $3 input/$15 output за 1M tokens; Haiku 4.5: $1/$5. Это ставки списания usage, **не стоимость подписки и не гарантия доступного бесплатного вызова**. Legacy premium-request documentation распространяется только на оставшиеся существующие annual Pro/Pro+ plans после 2026-06-01. Публичное наличие новых моделей не определяет режим конкретного аккаунта.  
Источники: [models/pricing](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing), [legacy scope](https://docs.github.com/en/copilot/reference/copilot-billing/request-based-billing-legacy/copilot-requests).

**Auth Copilot:** OAuth либо поддерживаемые environment tokens; classic PAT не поддержан; fine-grained PAT требует `Copilot Requests`. BYOK использует оплату провайдера независимо от GitHub auth. Это документация, не основание читать tokens/credential stores. [Official auth](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/authenticate-copilot-cli).

### Polza: точная конфигурация, цены и несовместимости

**DOCUMENTED, не применялось:**

```toml
model_provider = "polza"
model = "openai/gpt-6.1-sol"
model_reasoning_effort = "high"

[model_providers.polza]
name = "Polza.ai"
base_url = "https://polza.ai/api/v1/"
env_key = "POLZA_API_KEY"
wire_api = "responses"
```

Секция provider/URL/env/wire взята из [официальной Codex integration](https://polza.ai/docs/integracii/codex.md); модель заменена на реально присутствующий публичный ID. **Это кандидат для Codex CLI, не подтверждённая конфигурация OMP.** Точный OMP provider selector для Polza — **UNKNOWN**.

Фактические routes:

- `POST https://polza.ai/api/v1/chat/completions`
- `POST https://polza.ai/api/v1/responses`
- `POST https://polza.ai/api/v1/responses/compact`

Не подставлять `api.polza.ai` по поисковой выдаче: прочитанные официальные integration/API docs указывают `polza.ai/api`.

**Ограничения Responses:** beta, stateless; всю историю и tool results повторять в `input`; `previous_response_id`, `conversation`, `store`, `background` не реализуют соответствующую OpenAI-семантику; нет GET/DELETE/cancel response endpoints. [Responses contract](https://polza.ai/docs/api-reference/responses/create.md).

**Критическое расхождение:** OpenAI требует Responses для Sol tools; Polza превращает свой Responses в Chat Completions и при этом каталог Sol объявляет `tools`. Прохождение полного tool roundtrip через выбранного Polza provider — **UNKNOWN**, не VERIFIED.

Публичный каталог `https://polza.ai/api/v1/models?type=chat` вернул:

| API model ID | `top_provider` | RUB/1M input → output | Context/output cap | Ограничение |
|---|---|---:|---:|---|
| `openai/gpt-6.1-sol` | `openai/flex` | 121.7013 → 608.5065 | 1,050,000 / 128,000 | Объявлены tools/structured; execution не проверен |
| `anthropic/claude-sonnet-4.6` | `azure/global` | 365.1039 → 1825.5195 | 1,000,000 / 128,000 | Объявлены tools/structured; платный условный кандидат |
| `google/gemini-3.5-flash` | `bananalab` | 90.03722963 → 540.22337775 | 1,048,576 / 65,536 | **`is_unofficial:true`** |
| `google/gemini-3.1-flash-lite` | `bananalab` | 15.00620494 → 90.03722963 | 1,048,576 / 65,536 | **`is_unofficial:true`** |

Это **DOCUMENTED provider-advertised metadata/prices**, практически подтверждено только получение публичного JSON. Не account quote, не гарантия цены будущего маршрута/long-context tier. Страница models местами описывает старые поля RUB/token, тогда как фактический JSON явно содержит `*_per_million` и `currency:"RUB"` — единицы не смешивать.

Неофициальные провайдеры по умолчанию выключены, `provider.only` запрет не обходит; metadata catalog может содержать то, что ключу недоступно. Polza прямо признаёт ограниченность проверки хранения данных и риск другого поведения/версии модели. [Unofficial providers](https://polza.ai/docs/gaidy/unofficial-providers.md).

[Provider routing](https://polza.ai/docs/gaidy/provider-selection.md) документирует `provider.only`, `allow_fallbacks:false`, `max_price` и alias:

```text
anthropic/claude-sonnet-4.6@reasoning_effort=high&allow_fallbacks=false
```

Alias и одноимённый body parameter одновременно дают 400. Для воспроизводимого исследования provider следует закреплять после получения его точного ID, не полагаться на меняющийся `top_provider`.

### Роли и selectors: предложение, не изменение настроек

При `perCallModel=off` эти роли — разделение задач/контекста, **не уже включённый per-role routing**.

Обозначения:

- **A:** `openai-codex/gpt-6.1-sol:high` — единственный session-proven.
- **B:** `openai-codex/gpt-6.1-sol:low` — только кандидат; API поддерживает `low`, но конкретный OMP selector/подписочный вызов не проверен.
- **C:** `github-copilot/claude-sonnet-4.6` — каталог подтверждён Lead, invocation/entitlement/overage не проверены.
- **D:** `github-copilot/claude-haiku-4.5` — те же условия.
- Thinking для C/D через текущий OMP adapter — **UNKNOWN**; не приписывать suffix `:high` без подтверждения adapter contract.

| Роль | Сейчас | Условный резерв/оптимизация | Quality gate |
|---|---|---|---|
| Lead | A, high | При исчерпании — ждать reset; другой backend не включать автоматически | Полнота критериев, источники, бюджет, финальный синтез |
| Researcher | A, high | B для простого извлечения после квалификации | Точный URL/версия; факт отдельно от inference |
| Developer | A, high | C только при доказанном уже включённом entitlement без overage | Минимальный diff, следование существующим conventions |
| Fast Developer | A, high; небольшая задача | B; затем D при тех же billing gates | Узкая правка; обязательный отдельный review |
| Reviewer | A, отдельный blind context | C как different-family **только после gates** | Контрпример, регрессии, конкретные file/line findings |
| Security | A, high, read-only | C после gates; не считать модель security scanner | Trust boundaries, secrets, egress, destructive paths |
| Advisor | A только по явному запросу | C после gates | Альтернативы и критерии опровержения; без exec |
| Planning | A, high | B для механического разбиения | Dependency graph, достижимые acceptance criteria |
| Docs | A | B или D после квалификации | Документ соответствует фактическому поведению |

**Независимый review другой семьёй сейчас не запускать:** каталожные C/D есть, но cached `0/200` не доказывает свободный остаток для конкретного selector, multiplier и отсутствие overage. При недоступности C сделать отдельный blind same-family review A и честно указать, что независимости семей нет. Polza платный маршрут не является бесплатным резервом; local different-family — только если существующие веса/работоспособность уже доказаны.

### OpenDesign: identity, реализация и безопасность

**Identity/version:** именно [`nexu-io/open-design`](https://github.com/nexu-io/open-design), OpenDesign workspace, Apache-2.0. Последний опубликованный release в прочитанной ленте: [`open-design-v0.27.1`](https://github.com/nexu-io/open-design/releases/tag/open-design-v0.27.1), commit **`b83646f4afb9b21b415d98c4d073477d077d7943`**. Release относится к дню проверки; feed `2026-11-10T07:33:57Z` — время feed entry/update, не следует выдавать его за точное время публикации: release page отдельно показывает `10 Nov 03:03`. Будущих относительно проверки releases в прочитанной ленте нет.

**Architecture:** UI/desktop → local daemon → существующий code-agent CLI либо API/cloud runtime. Agent loop, tool permissions, context/resume делегируются CLI; наличие adapter не подтверждает CLI auth. [Adapter contract](https://github.com/nexu-io/open-design/blob/main/docs/agent-adapters.md).

**MCP setup документирован:** `od mcp install <agent>`, preview `--print/--dry-run`, предпочтительно client-specific snippet с абсолютными путями из Settings. Это меняет config; **сейчас не выполнять**. Native Windows поддерживается; macOS `/usr/bin/od` collision не переносить на Windows.

**Важное расхождение README/source:**

- README утверждает read-only default.
- [`mcp.ts:611–815`](https://github.com/nexu-io/open-design/blob/b83646f4afb9b21b415d98c4d073477d077d7943/apps/daemon/src/mcp.ts#L611-L815) содержит `write_file`, `delete_file`, `delete_project`, `create_project`, `start_run`, cloud-login action.
- [`mcp.ts:2019–2021`](https://github.com/nexu-io/open-design/blob/b83646f4afb9b21b415d98c4d073477d077d7943/apps/daemon/src/mcp.ts#L2019-L2021) возвращает **весь `TOOL_DEFS`**, не read-only filtered list.
- `delete_project` требует explicit project + `confirm:true`, но это не security boundary вместо client policy.

Следовательно, **не считать MCP подключение inherently read-only**. Loopback/SSRF protection не запрещает destructive tools и не sandbox’ит внутреннего CLI.

**Diagrams vs implementation:**

- [`skills/hand-drawn-diagrams/SKILL.md`](https://github.com/nexu-io/open-design/blob/b83646f4afb9b21b415d98c4d073477d077d7943/skills/hand-drawn-diagrams/SKILL.md) обещает Excalidraw/SVG/PNG, но прямо сообщает: это **catalogue advertisement**, полный upstream bundle надо устанавливать отдельно. Не встроенный проверенный генератор диаграмм.
- [`skills/frontend-slides/SKILL.md`](https://github.com/nexu-io/open-design/blob/main/skills/frontend-slides/SKILL.md) имеет такую же catalogue-only оговорку.
- При этом собственный deck export действительно реализован: [`deck-export.ts:154–188`](https://github.com/nexu-io/open-design/blob/b83646f4afb9b21b415d98c4d073477d077d7943/apps/daemon/src/deck-export.ts#L154-L188) собирает **screenshot-based PPTX**, один raster image на slide — не editable text. Отдельный `editable` renderer mode объявлен в интерфейсе; его качество/полнота не проверены.

**Когда не добавлять:** пока нужны Markdown findings/простые Mermaid/SVG, нет подключённого MCP и задачи на presentation artifact. Cloud credits/referral offers в release — **CLAIMED commercial offer**, не entitlement пользователя.

### OptiLLM: реальные multi-request/cost/compatibility risks

Версия: [`v0.4.1`](https://github.com/algorithmicsuperintelligence/optillm/releases/tag/v0.4.1), **2026-11-02T05:00:25Z**, commit `f74e6787573a7935b6689837bee9a93a8b0fa440`. Не future release.

**Implementation evidence:**

- [`server.py:415–445`](https://github.com/algorithmicsuperintelligence/optillm/blob/v0.4.1/optillm/server.py#L415-L445): `none` preserves original multi-turn/tool messages and request parameters.
- [`moa.py`](https://github.com/algorithmicsuperintelligence/optillm/blob/v0.4.1/optillm/moa.py): initial `n=3`, затем critique, затем final synthesis, **все на том же `model`**. Обычно 3 HTTP requests, но 5 generated outputs; при отказе `n` — failed attempt + 3 singles + critique + final. Это не автоматически different-family debate.
- MOA использует `max_tokens`/`temperature`; tools/response schema не передаются в показанные calls. Префикс `moa-` не сохраняет агентную совместимость автоматически.
- [`server.py:1000–1038`](https://github.com/algorithmicsuperintelligence/optillm/blob/v0.4.1/optillm/server.py#L1000-L1038): upstream calls **не streamed**; клиентский SSE создаётся после завершения. Нельзя ожидать обычного upstream TTFT.
- Route search обнаружил `/v1/chat/completions`, legacy `/v1/completions`, `/v1/models`, `/health`; `/v1/responses` route в этом server не найден. Поэтому Sol tools через этот proxy — неподходящий default.
- [`json_plugin.py:24–38,54–84,150–158`](https://github.com/algorithmicsuperintelligence/optillm/blob/v0.4.1/optillm/plugins/json_plugin.py): загружает отдельный HF `Qwen/Qwen2.5-Coder-0.5B-Instruct`, преобразует schema через ограниченный mapping. Это **не прозрачное принуждение upstream модели соблюдать произвольный JSON Schema**; может означать download/локальную память и смену модели.
- `&` — последовательные техники, `|` — параллельные; входы/outputs и context повторяются. **[INFERENCE]** стоимость считать суммой всех upstream input/output/cache/tool charges, а не одним исходным запросом; latency оценивать по critical path.

**Security:**

Release 0.4.1 отключает unsandboxed `executecode` по умолчанию и исправляет MCP env/header value logging. Но pinned [`server.py:1009`](https://github.com/algorithmicsuperintelligence/optillm/blob/f74e6787573a7935b6689837bee9a93a8b0fa440/optillm/server.py#L1009) всё ещё содержит:

```python
logger.debug(f"Intercepted Bearer Token: {bearer_token}")
```

`server.py:872` также debug-логирует request body. Не включать DEBUG на реальных секретах/чувствительных prompts. README описывает остаточный DNS-rebinding gap URL fetcher; firewall/egress boundary остаётся необходимым.

Обещания «2–10x accuracy», «production ready» — **CLAIMED**, не результат нашего эксперимента.

**Когда не добавлять:** agentic tools/strict schema, жёсткий latency budget, неизвестная стоимость подписочного канала, простые задачи. Возможная будущая область — чистые reasoning tasks с фиксированным budget и сравнением против direct baseline.

### Council: вызовы, спор, синтез; отличие от OMP tasks

Версия: [`v1.2.0`](https://github.com/0xNyk/council-of-high-intelligence/releases/tag/v1.2.0), **2026-07-04T07:13:48Z**, commit `79c349bdbbb02b6c58c7f108734410e703dc71ca`. Прочитанный `main` на release page **38 commits ahead**; не выдавать все main-находки за release behavior.

[`SKILL.codex.md`](https://github.com/0xNyk/council-of-high-intelligence/blob/main/SKILL.codex.md) предписывает:

1. Отдельный `spawn_agent` на место, blind-first analysis.
2. Cross-examination с masked identities и требованием назвать конкретную ошибку перед сменой позиции.
3. Final stance, confidence-weighted tally, сохранение dissent.
4. **Отдельный Chairman**, не участвовавший в deliberation; single-provider fallback разрешён.
5. Retries/enforcement dispatches; `[Simulated]` degraded seats; при live<2 — fully simulated council.

Внешние места могут вызывать Codex/Gemini/Cursor CLI, Ollama или OpenAI-compatible HTTP. Это **executable instructions для host**, не доказательство реально произошедших независимых вызовов.

Особенно опасен [`detect-providers.sh`](https://github.com/0xNyk/council-of-high-intelligence/blob/main/scripts/detect-providers.sh):

- `anthropic` объявлен available **безусловно** как host runtime;
- Codex/Gemini/Cursor определяются по binary/version;
- defaults модели hardcoded;
- наличие env key/catalog reachability не подтверждает inference entitlement.

Поэтому автоматический detector нельзя использовать как доказательство бесплатного multivendor access; на Codex-host безусловное «Anthropic available» особенно вводит в заблуждение.

**Стоимость:** full 18-seat Codex protocol с отдельным restatement gate + 3 rounds + Chairman ≈ **73 seat/Chairman dispatches до retries/enforcement** — **[INFERENCE]** из протокола, не измерение HTTP requests. Default panel может быть triad, а не все 18. Family diversity требует реальных разных моделей, а не разных персон.

**Отличие от OMP tasks:** OMP task decomposition разделяет исполнимую работу/файлы и собирает результаты; Council многократно обсуждает **одну decision boundary**, добавляя opposition, voting, Chairman и audit transcript. OMP может реализовать подобную процедуру без установки Council; смена personas внутри одной семьи не создаёт независимого model-family review.

**Когда не добавлять:** фактические lookup, обратимые решения, deadline-sensitive coding, недостаточно доказанного свободного entitlement. Для этого исследования достаточно blind review + explicit counterargument/kill criteria.

### MCP least privilege и будущие qualification gates

**DOCUMENTED:** актуальная прочитанная MCP security guidance — версия **2026-07-28**: [security best practices](https://modelcontextprotocol.io/specification/2026-07-28/basic/security_best_practices). Требует минимизации прав, согласия на local execution, ограничения FS/network, audience validation; token passthrough запрещён.

Предлагаемая политика, **не применялась**:

- Allowlist конкретных read tools, project IDs и директорий; не весь filesystem/home.
- Отсечь generation/write/delete/login/billing/key-management tools на client/policy уровне; annotations — hints, не ACL.
- Local subprocess считать кодом с правами пользователя; не использовать auto-download `npx -y`/curl-install.
- Loopback binding не заменяет auth, Origin validation и sandbox.
- Не передавать GitHub/Codex credentials произвольным MCP/proxy.
- Отключать ненужные серверы: tool schemas расходуют context; [Codex docs прямо рекомендуют ограничить MCP surface](https://learn.chatgpt.com/docs/pricing.md).
- Polza MCP — **управление аккаунтом**, а не нужный inference transport: [`https://polza.ai/api/mcp`](https://polza.ai/docs/gaidy/mcp.md) имеет scopes вплоть до `billing.danger` («списание с карты без подтверждения»). **Сейчас не подключать даже read-only preset:** задача не требует accounts/keys/billing metadata.

**Квалификационные эксперименты пока только план:**

1. Подтвердить exact selector, adapter transport, существующий allowance, multiplier/billing regime, zero-overage boundary; при UNKNOWN не запускать.
2. Проверить один read-only tool roundtrip с правильным `call_id`; затем несколько calls, отказ и truncation.
3. Проверить strict schema отдельно от JSON mode: nested objects/arrays, required/additionalProperties, refusal/incomplete handling; валидировать локально, не доверять слову `strict`.
4. Измерить TTFT и total latency p50/p95, tokens/reasoning/cache, все внутренние requests и фактические списания; limit concurrency отдельно от OMP worker count.
5. Для proxy/Council сравнить с direct baseline на одинаковых задачах и budget; остановить при tool/schema regressions, несанкционированном fallback, отсутствии выигрыша.
6. Different-family review разрешать только после доказательства существующего свободного entitlement; до этого — blind same-family review с явной маркировкой.

**Методологическая оговорка:** локальный OMP `batch=true` не доказывает использование OpenAI Batch API и не даёт основания применять его 50%-discount pricing. API context limits, подписочные окна, OMP prompt budget и model knowledge cutoff — разные величины.