# МегаФон — предметное исследование и Research Mode qualification

> **Архивный план исследовательской фазы.** PREPARATION/BLOCKED ниже — исторические квалификационные статусы, не запрет работы и не текущее состояние продукта. Текущий продукт: [архитектура](architecture.md), [видеокейс](video-e2e.md); [архивный индекс](archive/README.md).

**Статус: PREPARATION ONLY.** Полное исследование и scout smoke не запускались. `.omp/profiles/research.yml` — **CANDIDATE**, не VERIFIED. Полный оригинал кейса отсутствует: [contest-brief](contest-brief.md) BLOCKED. Bootstrap не подменяет этот prerequisite.

## 1. Scope и результат будущего исследования

Определить, какой Contest Product действительно решает оригинальный кейс лучше альтернатив и как независимо доказать качество. Не реализовывать агента, не выбирать product runtime/framework до требований. Сохранять разделение Development System/Contest Product из [.omp/AGENTS.md](../.omp/AGENTS.md).

До начала: полный verbatim brief с проверенной provenance; original constraints/rubric mapped без придуманных условий; PASS scout smoke; разрешение на Deep Research; только уже разрешённая Codex quota, без неизвестных доплат. При отсутствии оригинала допустима только подготовка вопросов/источников, не кейс-специфичный synthesis.

Выход будущей фазы: requirement/evidence/decision matrix, конкурирующие гипотезы, минимальная обоснованная архитектура переносимого агента, протокол оценки и план реализации после отдельного разрешения. Сначала результаты в ответе/parent artifacts; research profile намеренно запрещает запись и Lead. Curated Markdown сохранять отдельным supervised writer-проходом по согласованным путям, не включать write в исследователей и не публиковать raw sessions.

## 2. Исследовательские направления

Названия — временные workstreams, не постоянные custom agents. Вопросы ниже — план проверки, **не факты о ТЗ, бизнесе МегаФона или данных**.

| Направление | Вопросы | Ожидаемые доказательства | Критерий завершения |
|---|---|---|---|
| **A. Product Strategy & Discovery** | Кто пользователь/заказчик и какое решение он принимает? Какие JTBD, входы/выходы, workflow, pain points, бизнес-метрики и приоритеты действительно следуют из brief? Как различить сегментацию, value proposition, продуктовую гипотезу, validation и стратегическое решение? Какие альтернативы/ошибки опаснее всего? | Точные требования/цитаты из оригинала; официальные публичные материалы компании и подтверждённые отраслевые данные; примеры проверяемых decision artifacts; альтернативные гипотезы и counterevidence | У каждого обязательного сценария есть actor/input/decision/output/AC и source; никакая внутренняя метрика/данные компании не выдуманы; выбран минимальный demo path либо явно указан blocker |
| **B. Communications & Marketing** | Какие аудитории, цели, сообщения, tone-of-voice, каналы и KPI требуются? Как связать коммуникационную стратегию с продуктовой, а не генерировать generic copy? Какие ограничения доказательности, бренда, рекламы, персональных данных применимы? | Brief и опубликованные первичные brand/company материалы; релевантные нормативные первоисточники при применимости; структура message hierarchy/channel rationale; примеры плохих/хороших результатов по одинаковой rubric | Рекомендации трассируются к аудитории/цели/продуктовой гипотезе и evidence; утверждения/обещания проверяемы; критерии качества и запрещённые claims перечислены без выдуманной compliance-сертификации |
| **C. Agent Architecture, Knowledge & Tools** | Каковы реальный формат переносимых файлов, host/runtime, model/tools/network ограничения по ТЗ? Какие знания статические, версионируемые или требующие lookup? Нужны ли retrieval/tools вообще? Как управлять provenance, contradictions, uncertainty, prompt injection и missing input? | Original execution contract; сравнительная таблица минимальных вариантов; примеры input→reasoning procedure→artifact schema/error; источники знаний с лицензией/датой; trust boundaries; условия tool necessity | Есть минимальная архитектура без зависимости от OMP/личных accounts; каждый компонент необходим конкретному AC; fallback/abstention/ошибки определены, но код/прототип не написан |
| **D. Evaluation, Reliability & Competition** | Каковы точные критерии/формат судейства? Что означает полезная и фактически обоснованная стратегия? Какие deterministic, expert/rubric и adversarial проверки нужны? Как доказать воспроизводимость, переносимость, citation correctness, устойчивость к неполным/враждебным данным? | Original rubric; requirement→evaluation matrix; синтетические scenario designs/expected properties; blind A/B protocol и baseline; failure taxonomy, scoring definitions, repeated-run/latency/cost measurement plan | Все обязательные требования имеют независимый gate и evidence plan; критические ошибки/stop criteria определены; отсутствуют выдуманные benchmark scores и обещания победы; продукт можно будет принять без dev infrastructure |

Не делать большой обзор SDD/harness/model providers повторно: пользоваться принятым [infrastructure](../research/infrastructure/recommendation.md) и фактическим [qualification](../research/qualification/next-step.md). Новое инфраструктурное исследование — только при конкретном обнаруженном незакрытом требовании.

## 3. Протокол независимых позиций и пересмотра

1. **Independent Research.** Волна1: A/B/C, максимум3 bundled scouts; D после освобождения slot (может исследовать original rubric независимо от предложенной архитектуры). Все briefs получают одинаковый verbatim scope и safety contract. До blind report не читать peer conclusions. Output: claims, sources, альтернативы, uncertainties, опровержимый вывод, acceptance implications.
2. **Cross-Examination.** Lead передаёт каждому релевантный peer report и сильнейшую альтернативу через новый explicit task context. Для существенного разногласия: точная contested claim, исходная цитата/данные, контрпример/условия, что изменит решение. Не vote-counting по personas и не «три одинаковые модели согласились».
3. **Adversarial Review.** Освободить slot, свежий bundled read-only reviewer/scout без авторского self-approval. Атака на полноту brief, неподтверждённые предпосылки, generic recommendations, архитектурную сложность, переносимость, безопасность и evaluator leakage. Same-family independence указать явно; новую платную модель не подключать.
4. **Revision.** Авторы отвечают addressed/refuted/blocked, приводят источник и обновляют позицию. Не более2 раундов на спор; нерешённый существенный конфликт → upstream clarification/blocker, не скрытое снижение acceptance.
5. **Synthesis.** Lead сопоставляет evidence и варианты, сохраняет dissent/ограничения, принимает минимальное решение. Не считает количество citation доказательством качества. Остановка после complete traceability и закрытых существенных замечаний; без автоматического перехода к implementation.

Lead явно включает в `task.context`: цель/стадию, оригинальный scope, allowed public sources/paths, только read/grep/glob/web_search, отсутствие secrets/execution/writes/new providers, лимит делегирования и stop conditions. `.omp/AGENTS.md` не передаётся children автоматически; copy важных правил обязателен. Инвентарь дочерней сессии проверять отдельно от Lead.

## 4. Evidence contract и общий acceptance

Каждый значимый claim: ID → exact source URL/file+section → publisher → version/publication/access date → короткая цитата/данные → status DOCUMENTED/VERIFIED/CLAIMED/UNKNOWN/FAILED → applicability → implication → counterevidence. Gate statuses PASS/FAIL/BLOCKED отдельно. Источник search snippet обязательно открыть/проверить; ссылки без доступа отметить, не выдумывать содержание. Benchmarks/prices/company-specific facts без источника не использовать.

Исследование завершается, когда:

- Оригинальный brief полон, untouched и прослеживается; requirements не восстановлены из summaries.
- Для каждого обязательного requirement есть evidence, решение/альтернативы и будущий acceptance gate; существенные unknowns не замаскированы mock/fallback.
- Все направления A–D прошли cross-exam/revision; независимый review выполнен и критичные замечания закрыты либо честно блокируют конкретное решение.
- Архитектура проста/переносима, контуры dev/product разделены, стратегия не generic; no implementation в этой фазе.
- Расход/маршруты/лимиты и границы проверки указаны; raw sessions/secrets не вошли в curated output.

Предлагаемые outputs после отдельного согласования: один curated report на направление + общий evidence/decision ledger и synthesis; не создавать service/task DB, несколько spec systems или постоянные custom agents.

## 5. Research profile: назначение и ограничения

Кандидат [.omp/profiles/research.yml](../.omp/profiles/research.yml): Sol High для Lead/scout/reviewer; batch/async=true; concurrency3, workers0, recursion1; child timeout10min/request budget60; perCallModel off; generic writing task/sonic/seance отключены; structured=false до отдельной квалификации. Explicit read-only deny для write/edit/exec/brokered execution, shell/eval/LSP/browser/debug отключены. Task spawn требует operator approval, без session-wide grant.

Web: exact `modelRoles.web=openai-codex/gpt-6.1-sol`, `retry.fallbackChains.web=[]`; default web chain иначе может менять backend независимо от retry.modelFallback. `xai`/`xai-oauth` disabled, чтобы X-only query не подставлял новый grounded backend. Не использовать X-specific operators в smoke. Existing Codex OAuth — не отдельный OpenAI API. Catalog/metadata acceptance не доказательство search entitlement, поэтому search failure → BLOCKED, а не включение другого provider.

Native discovery сохранён для .omp/AGENTS.md и существующего project MCP suppression; foreign/plugin discovery отключён. Новых MCP/extensions нет; существующий open-design disabled в .omp/mcp.json, xdev=false. При смене cwd обязательно скопировать это suppression в disposable project и проверить actual inventory: один --tools не изолирует additive tools. `enabledProviders` не transport allowlist. Read-only и restrictedFolders не sandbox/конфиденциальность всех host files.

Lead тоже не имеет write/edit: full research отдаёт synthesis в ответе. Сохранение — отдельный разрешённый writer-проход; не ослаблять policy ради записи report или IRC. Runtime session/artifact writes harness остаются, это не agent mutation; хранить в ignored `.local/` или вне repo, не считать local JSONL секрето-безопасным.

## 6. Короткий qualification smoke одного scout — ТОЛЬКО ПЛАН

**Не выполнен.** Это prerequisite большого исследования, а не повтор E01. Разрешение на исполнение smoke должно быть отдельным. Не менять qualification-supervised.yml и global config.

### Начальные условия

- Новый одноразовый каталог вне contest/чужих repos, canonical path проверен, нет junction/symlink/настоящих secrets. Только фиктивный canary и публичный readme.
- Оператор помещает byte-identical candidate profile и существующий MCP-disabled config в disposable `.omp/`; добавляет одноразовую копию dev instructions для Lead. Зафиксировать hashes canary, profile/MCP/brief; outputs и sessions оставить вне tracked repo.
- Разрешён только существующий Codex route; проверить current quota без token exports. Parent и child model/high, web route/no-fallback inspect **до** search. UNKNOWN entitlement/доплата → STOP.
- Запустить отдельный supervised процесс, максимум **один scout**, parent max-time5min, child не дольше3min через отдельный disposable overlay `task.maxRuntimeMs:180000` + `task.softRequestBudget:12`. Не редактировать tracked candidate ради smoke.

### Процедура и обязательное evidence

| Шаг | Действие | PASS / FAIL |
|---|---|---|
| 1. Parent metadata | RPC get_state/эквивалентный observed UI: exact model/high, actual top-level inventory, context .omp/AGENTS.md; inspect effective cfg modelRoles/retry/task/tools | Нет write/edit/bash/eval/exec/browser/MCP; parent read/grep/glob/web_search/task и optional wait/todo. Не считать catalog proof inference |
| 2. Один bundled scout | Один task item, agent=scout, полные safety instructions; оператор approves только этот spawn. Зафиксировать agentSource/resolvedModel/resolvedThinkingLevel и actual latest child session_init.tools/mountedTools, а не prose агента | bundled, openai-codex/gpt-6.1-sol/high, один уровень, no executor/writer/delegation tools. Допустимы только read/grep/glob/web_search и inert completion yield при наличии |
| 3. Один public поиск | Ровно один `web_search` query `site:nodejs.org/api test runner`, небольшой limit; открыть один найденный официальный источник read | Есть наблюдённый tool roundtrip, реальные URLs/цитируемый раздел, provider/model из response; не подмена search response ответом памяти |
| 4. Отрицательный контроль | Оператор сверяет explicit deny и недоступность write/edit/exec в реальном child inventory; child не должен выдумывать вызовы отсутствующих tools. Только если runtime позволяет безопасно вызвать native policy-path — одна заранее санкционированная попытка записи dummy canary/безвредного исполнения **внутри fixture** | Подтверждены отсутствие этих callable surfaces и неизменный canary/fixture manifest; policy-path negative test помечается UNKNOWN, если фактически не выполнялся. Никакой общей OS sandbox гарантии |
| 5. Lifecycle/результат | Прочитать настоящий child transcript/tool results/structured metadata; дождаться result/settled, проверить errors и отсутствие лишних children, сравнить baseline canary/files | No unauthorized writes/exec, sources consistent, parent получил результат; idle/parked после completion не выдавать за работающую задачу. Голое get_subagents=[] не заменяет transcript |
| 6. Routing/расход/stop | Проверить все observed provider/model/effort, search details/failures, retry/fallback events, quota/cost estimates; отменить pending dialog до abort, закрыть тестовый process | Нет другого backend/fallback, retries bounded, no live child/process после закрытия. Любой неразрешённый маршрут или mutation → FAIL; missing evidence → UNKNOWN/BLOCKED |

**Evidence bundle:** versions/hash/commands/prompts, sanitized effective config, get_state и child session_init (без raw system/auth dumps), observed tool arguments/results, route/usage/error metadata, canary/file hashes, start/end/exit, curator verdict. Observer extensions/новые MCP для smoke не ставить. Если actual tool inventory нельзя подтвердить существующим UI/RPC/session_init без расширения — BLOCKED, не «агент сказал read-only».

**Admission:** один scout PASS только для испытанного маршрута/поверхности; concurrency3 ещё не VERIFIED. После него отдельно квалифицировать E02-lite:2–3 **read-only** scouts с независимыми публичными задачами, лимит/доставка/stop; без writing tests. До E02-lite использовать последовательные waves/concurrency1 runtime overlay. Profile остаётся CANDIDATE до соответствующего evidence; статус не повышать автоматически по metadata checks.

### Команда после smoke и перед большим исследованием

Из корня репозитория, только после полного оригинала и отдельного разрешения. В bootstrap эта команда **не выполнялась**:

```powershell
omp --config .omp/profiles/research.yml --model openai-codex/gpt-6.1-sol --thinking high --approval-mode always-ask --tools read,grep,glob,web_search,task,wait,todo --no-extensions --no-skills --no-rules --no-lsp --no-title --max-time 45m --warn-cost 3 --max-cost 5 --session-dir .local/omp/sessions
```

Не добавлять `--no-context-files`: он отключит .omp/AGENTS.md. Нет -e/--hook/--plugin-dir/--yolo. Для RPC inventory inspection вместо TUI — `--mode rpc-ui`, без отправки subject prompt до проверки. Headless только с `--wait-async`, но не использовать его как обход task approval: prompt без UI должен fail closed. `--config`, cwd и limits при resume передаются заново; --profile — другой механизм с отдельным auth, здесь не используется.

## 7. Следующий промпт Deep Research (после prerequisites)

```text
Ты — Principal AI Research Lead MGIMO / МегаФон. Сначала прочитай .omp/AGENTS.md,
docs/contest-brief.md и docs/research-plan.md. Не реализуй продукт.

До inference fan-out проверь: полный оригинал действительно сохранён дословно;
есть PASS одного scout для текущего research profile, фактической модели High,
read-only inventory и exact Codex web route без fallback. Для concurrency>1 нужен
отдельный PASS read-only E02-lite; иначе последовательно и concurrency1.
Если prerequisite отсутствует — назови конкретный BLOCKED и останови исследование,
не восстанавливай требования из памяти и не расширяй permissions/providers.

Выполни A Product Strategy & Discovery; B Communications & Marketing;
C Agent Architecture, Knowledge & Tools; D Evaluation, Reliability & Competition
по docs/research-plan.md. Максимум три одновременных read-only субагента, один
уровень делегирования, только существующие bundled агенты, полный safety contract
в каждом task.context. Сначала независимые позиции без чтения peer conclusions,
затем Cross-Examination → fresh Adversarial Review → до двух Revision rounds →
Synthesis. Сохрани существенное dissent и условия опровержения. Same-family
контекстную независимость не называй multivendor review.

Для каждого значимого claim дай точный primary source/версию/дату/цитату,
статус доказательства и applicability. Свяжи original requirements с findings,
альтернативами, решениями и будущими acceptance gates. Не придумывай данные
МегаФона, rubric, цены, доступ инструментов или benchmark results.

Не запускай shell/eval, installs, новые MCP/extensions/API, writing subagents,
push/publication. В profile запрещена и Lead-запись: верни curated reports,
evidence/decision matrix, минимальную архитектуру, evaluation plan, blockers и
следующий отдельно разрешаемый шаг в ответе. Сохранение файлов — отдельный
supervised writer-проход; не ослабляй research policies ради артефактов.
Остановись после синтеза, не переходи к продуктовой реализации.
```

## 8. Проверка самого bootstrap

Разрешённые изменения: .omp/AGENTS.md, docs/contest-brief.md (status BLOCKED до оригинала), README.md, .gitignore, .omp/profiles/research.yml и этот docs/research-plan.md. Последний — единственный дополнительный файл для явно запрошенного Research Plan/smoke/prompt. Корневой AGENTS.md, existing reports, qualification-supervised.yml и global config не изменять.

Безопасная проверка profile сейчас может загрузить YAML и получить RPC get_state без prompt/model calls. Это только schema/metadata evidence; не smoke scout/search, не основание для VERIFIED. Никаких новых installations или реальных секрета-проб в bootstrap.

Официальные contracts установленной18.18.6: `omp://context-files.md` (native AGENTS discovery и исключение для children), `omp://tools/task.md`, `omp://task-agent-discovery.md`, `omp://session.md` (session_init.tools), `omp://tools/web_search.md` (отдельная search chain), `omp://models.md`, `omp://cli-reference.md`. Публичные counterparts: [release docs](https://github.com/can1357/oh-my-pi/tree/v18.18.6/docs), [bundled scout](https://github.com/can1357/oh-my-pi/blob/v18.18.6/packages/coding-agent/src/prompts/agents/scout.md). DOCUMENTED поддержка не заменяет future runtime qualification.

### Выполненная безопасная metadata-проверка bootstrap

Запущен отдельный OMP18.18.6 с candidate profile и теми же tool/discovery flags, но `--mode rpc-ui --no-session --max-time 2m`; отправлены **только get_state и get_session_stats**, без prompt. Process exit0, warnings отсутствуют.

- Actual parent model: `openai-codex/gpt-6.1-sol`, thinking high.
- Actual parent inventory: **read, grep, glob, web_search, task, wait, todo**; write/edit/exec/MCP не показаны, xdev=false.
- Native `.omp/AGENTS.md` обнаружен в parent systemPrompt; `--no-context-files` не использовался.
- Stats: user/assistant messages0, toolCalls0, tokens0; agent_start/tool_execution_start отсутствуют; sessionFile отсутствует.
- `.gitignore` проверен через `git check-ignore --stdin`: secrets/session/cache examples исключаются; .env.example, tracked research/docs и project instructions/profile не исключаются. Dummy secret-файлы не создавались.

Это наблюдённая **metadata/startup проверка**, не квалификация scout/web search/deny-paths/concurrency. Дочерний agentSource, High, inventory и отсутствие fallback при запросе ещё не проверены. CANDIDATE сохраняется; Deep Research не запускалось. Текущая родительская bootstrap-сессия остаётся default-yolo с более широким набором инструментов; этот факт не переносится на исследовательский допуск.
