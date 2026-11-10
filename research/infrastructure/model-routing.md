# Model routing, доступ и стоимость

Дата: 2026-11-10. **Не применено, inference-сравнения не запускались.** Primary sources, exact metadata и риски: [C evidence](findings/c-models-tools.md); локальные результаты: [L02/L05–L07](findings/local-environment.md).

## 1. Выбранная стратегия

Сегодня единственный session-proven route — **`openai-codex/gpt-6.1-sol:high`**. Сохраняем качество Lead/Developer; не меняем модель ради красивой матрицы. Medium/low selectors допустимы по локальному каталогу, но конкретный quality/latency выигрыш **UNKNOWN**. Это стартовый fallback baseline, а не утверждение, что одна модель оптимальна для всех ролей.

Целевая конфигурация после E09: сильный Codex Lead/Developer + быстрый квалифицированный worker + different-family Copilot reviewer. Никаких paid Polza/direct API fallbacks без отдельного разрешения. Role comma-list выбирает доступный catalog match, а не повторяет неуспешный запрос; failover — `retry.fallbackChains` отдельно. Сейчас chain пуст, автоматическую смену модели выключить в квалификационном overlay.

## 2. Роли

| Роль / OMP mapping | Основной маршрут | Резерв / условная оптимизация | Подключение и quality gate |
|---|---|---|---|
| Lead / Architect → default, slow | Codex Sol high | Same route после reset; Copilot Sonnet high только после E09 | Existing OAuth; AC completeness, interface/root-cause choices, no invented scope |
| Researcher → scout | Codex Sol high | Sol medium для extraction; Sonnet high после gate | task.agentModelOverrides.scout; exact URL/version, evidence vs inference |
| Developer → task | Codex Sol high | Copilot Sonnet high после gate | task override; behavioral AC, минимальный diff, actual smoke |
| Fast Developer → sonic / smol | Sol medium (catalog candidate) | Sol high; Copilot Haiku low после gate | только механический scope, blind review обязателен |
| Reviewer → reviewer | Пока Sol high, свежий blind context | **Цель Sonnet high**, backup Sol high с маркировкой same-family | Не видеть авторский self-review до своего verdict; seeded defect detection + false positives |
| Security Reviewer → security-reviewer | Sol high, read-only | Sonnet high после gate | trust boundaries, secrets/egress, exploitability; не замена scanner/OS policy |
| Advisor → advisor | disabled; Sol high эпизодически | Sonnet high после gate | Нет per-turn runtime расходов по умолчанию; ценность — выявленный decision risk |
| Planning / Specification → plan | Sol high | Sonnet high после gate | testable AC, dependency graph, реальные blockers |
| Documentation → smol/commit либо обычная узкая задача | Sol low (catalog candidate) | Sol high; Copilot Haiku low после gate | Сверка с executed behavior; изменения API не додумывать |

Exact candidates: `openai-codex/gpt-6.1-sol:medium`, `openai-codex/gpt-6.1-sol:low`, `github-copilot/claude-sonnet-4.6:high`, `github-copilot/claude-haiku-4.5:low`. Локальный `omp models` показывает эти IDs и соответствующие effort levels; **adapter execution и quality UNKNOWN**. Это не гарантированные fallbacks. Не использовать fuzzy `opus`/`latest` для воспроизводимого опыта. Не подменять доступность будущих/старых model aliases именем из каталога.

`task.agentModelOverrides` закрепляет встроенные agents и имеет приоритет над frontmatter; perCallModel остаётся off. Native Model Roles не требуют создать отдельного persistent agent для каждой профессии. Independent-family review этого исследования **не выполнено**: entitlement/overage не доказаны. Read-only reviewer той же семьи — независимость контекста/автора, не model-family diversity.

## 3. Каналы, деньги и limits

| Канал | Подтверждённый источник / тариф | Что известно об этом аккаунте | Решение |
|---|---|---|---|
| ChatGPT Plus / Codex OAuth | [Plans](https://learn.chatgpt.com/docs/pricing.md): $20/month; [auth](https://learn.chatgpt.com/docs/auth.md), [credit eligibility](https://developers.openai.com/api/docs/guides/chatgpt-api-credits.md): sign-in и API billing различаются | OMP usage reports plan plus; cached windows, не гарантированное число tasks | Основной существующий доступ. **Plus не считать отдельными API-кредитами** |
| GitHub Copilot | [Billing](https://docs.github.com/en/copilot/concepts/billing-and-usage/individuals/billing): Pro $10/1500 AI credits, Pro+ $39/7000, Max $100/20000; credit=$0.01 | Cached OMP snapshot premium0/200. Возможно legacy scope, точный regime UNKNOWN | Сначала billing/entitlement gate, затем no-overage review probe |
| Direct OpenAI API Sol Standard | [Pricing](https://developers.openai.com/api/docs/pricing): ≤272K input $2 input/$10 output/$0.10 cache-read за 1M; >272K $4/$15/$0.20 | API key/project funding не исследовались | Только будущий платный канал по разрешению; не путать с OAuth |
| Polza | [API](https://polza.ai/docs/api-reference/introduction.md), публичный [catalog](https://polza.ai/api/v1/models?type=chat); RUB token pricing | Публичный GET successful; личный balance/auth/RPM/RPD UNKNOWN | Условный резерв после paid approval и protocol qualification |
| Local | [Ollama compatibility](https://docs.ollama.com/api/openai-compatibility), tools/JSON docs | Нет доказанных installed weights/GPU/работающего endpoint; RAM15.3GiB | Не baseline; возможны tiny/doc tasks после quality/resource tests |
| Иной API (Anthropic/Google/OpenRouter и др.) | Отдельные credentials/billing; OMP provider support не entitlement | Доступ/актуальный индивидуальный quote UNKNOWN | Нет незакрытой потребности; не добавлять подписки заранее |

Все цены DOCUMENTED на дату чтения, до налогов/курса/индивидуальных договоров и с применимостью конкретного канала. Нет измеренного cost-per-accepted-task. OMP catalog estimate **не Copilot subscription cost**. OMP task batch **не OpenAI Batch API** и не основание применять batch discount.

Copilot [models and pricing](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing) указывает token rates, например Sonnet4.6 $3/$15, Haiku4.5 $1/$5 за 1M input/output; это usage-billing rates, не стоимость подписки. [Legacy premium scope](https://docs.github.com/en/copilot/reference/copilot-billing/request-based-billing-legacy/copilot-requests) после 2026-06-01 отдельно описывает существующие annual планы. Ни multiplier, ни бесплатный вызов выбранной модели из `0/200` не следуют. Auth/политики OMP adapter отличать от [официального Copilot CLI auth](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/authenticate-copilot-cli).

## 4. Контекст, tools, structured и latency

- Локальный Codex catalog: Sol500K context/128K output. [Direct API specification](https://developers.openai.com/api/docs/models/gpt-6.1-sol) описывает другую API surface:1,050,000 total/922,000 input/128,000 output. **Не повышать OMP contextWindow до direct API значения**. Actual accepted max context UNKNOWN.
- Direct Sol tools требуют Responses API; strict structured output поддержка сервера не равна OMP task schema policy. `task.structured=true`, strict validation, refusals/incomplete handling — отдельные gates.
- Copilot models зависят от plan/client/policy, [supported models](https://docs.github.com/en/copilot/reference/ai-models/supported-models); OMP catalog не гарантирует tools/schema/effort прохождение именно этого adapter.
- Polza [Responses](https://polza.ai/docs/api-reference/responses/create.md): beta/stateless adapter, history/tool results передаются полностью. `previous_response_id`, conversation/store/background не дают OpenAI state semantics; cancel endpoints не эквивалентны. Sol tool roundtrip UNKNOWN.
- Local Ollama: частичная OpenAI compatibility, context зависит от model/runtime/memory; default FAQ4096 — не обещание нужного длинного контекста. Cloud structured output нельзя выводить из local docs.
- TTFT, total wall time, p50/p95, accepted work/minute и concurrency saturation **не измерялись**. 600s provider timeout не latency SLA. High effort может быть медленнее; численные ускорения не заявляются.

## 5. Polza: только предлагаемый OMP adapter

Официальная [Codex integration](https://polza.ai/docs/integracii/codex.md) показывает `https://polza.ai/api/v1/`, env `POLZA_API_KEY`, wire_api responses. **Codex TOML нельзя копировать в OMP config.**

Будущий custom OMP provider `polza` в user models.yml должен определить baseUrl `https://polza.ai/api/v1`, apiKey как **имя environment variable**, `api:openai-responses` либо `openai-completions` согласно model/probe, точные model id/context/output/cost и stateful opt-out для stateless gateway. Документированный OMP [provider schema](https://github.com/can1357/oh-my-pi/blob/main/docs/models.md) позволяет это спроектировать, но exact working selector/compat combination **UNKNOWN до E09**. Не публиковать непроверенный YAML как готовую совместимую настройку. Credentials не читать/сохранять в research.

| Polza catalog snapshot (RUB/1M tokens) | Input | Output | Условия |
|---|---:|---:|---|
| openai/gpt-6.1-sol | 121.7013 | 608.5065 | top_provider=openai/flex; tools advertised, не invocation proof |
| anthropic/claude-sonnet-4.6 | 365.1039 | 1825.5195 | top_provider=azure/global; условный независимый платный reviewer |
| google/gemini-3.5-flash | 90.03722963 | 540.22337775 | is_unofficial=true; **не рекомендован** |
| google/gemini-3.1-flash-lite | 15.00620494 | 90.03722963 | is_unofficial=true; **не рекомендован** |

Цены — provider-advertised snapshot, не индивидуальная котировка/будущий route. Закреплять официальный provider, `allow_fallbacks:false`, price ceiling после разрешения. Неофициальный route нельзя оправдывать низкой ценой: version/data-retention uncertainty. Polza account-management MCP с billing/key scopes для inference не нужен.

## 6. Gate перед любым новым model route

1. Catalog ID + source date; transport/API/tool/schema/effort support.
2. Подтвердить существующую auth без экспорта tokens; конкретный plan/client eligibility.
3. Выяснить quota units, model multiplier/AI-credit tariff, hard zero-overage boundary. UNKNOWN → не вызвать.
4. Только после разрешения: один bounded tool roundtrip, schema refusal/incomplete/cancel; затем одинаковые E09 tasks.
5. Сохранить actual model route, usage/cache/reasoning и charged amount/quota delta. Неизвестную стоимость не записывать нулём.
6. Новый primary только при не худших critical AC/security и меньшем accepted-task cost/time. Изменения семейства/версии — повторная квалификация.
