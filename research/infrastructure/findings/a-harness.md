# Researcher A — harness evidence

Дата проверки: 2026-11-10. Read-only исследователь; ниже evidence report. Main и pinned release различаются.

## Summary

**Рекомендация: OMP-only как исходная инфраструктура квалификационных экспериментов.** У OMP уже есть делегирование, фоновые задачи, сохраняемые дочерние сессии, Agent Hub, model routing, structured results и native ACP. OpenClaw оправдан **не ради дополнительных агентов**, а при реальной потребности в постоянно работающем Gateway, расписаниях, внешних событиях и управлении через каналы.

Ключевые результаты:

- **DOCUMENTED:** OMP имеет собственный ACP server — это не только декларация совместимости и не обязательный сторонний адаптер.
- **UNKNOWN:** готовая квалифицированная связка OpenClaw→OMP отсутствует в исследованных источниках. Рабочий кандидат — custom acpx agent, запускающий `omp acp`; совместимость требует отдельного E2E.
- **DOCUMENTED:** `task.structured=false` по умолчанию; наличие `output` у agent definition само по себе не гарантирует typed result. Для строгого контракта нужен structured run и `schemaMode: strict`.
- **DOCUMENTED:** persistent/restorable agent ≠ непрерывно работающий процесс. Обычный resume восстанавливает историю; специальный `--restore` продолжает некоторые прерванные задачи, но только интерактивно и с ограничениями.
- **DOCUMENTED:** workspace isolation OMP и ACP OpenClaw **не являются OS security sandbox**.
- **FAILED:** публичный URL прежней платформы возвращает 404. Однако найден локальный checkout; его архитектура исследована без запуска.
- Новых runtime-экспериментов, установок, логинов, API-вызовов моделей и проверок не проводилось. **VERIFIED здесь нет**, кроме переданного Lead результата `omp --version = 18.18.6`.

## Версии и идентичность

| Компонент | Наблюдаемый release / SHA | Ограничение |
|---|---|---|
| OMP | [v18.18.6](https://github.com/can1357/oh-my-pi/releases/tag/v18.18.6), `9058ab9d229663e229e2867824ba6df6f21e9e59`; feed: `2026-11-09T23:30:49Z` | Release page показывает 58 commits до `main`; ниже отдельно отмечены moving-main документы |
| OpenClaw | [v2026.11.3](https://github.com/openclaw/openclaw/releases/tag/v2026.11.3), `847611dcaa3bf0e2783335f961dd1fd0580e4d9f` | Номер содержит 11.3, публикация — 10 ноября; страница показывает 18:53, feed — 19:13:09Z. Не считать номер датой публикации. `main` далеко впереди release |
| DSH | [dsh-v0.2.2-rc.1](https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.2.2-rc.1), `66491b05e3f05ad35bcdd4f6cd7ed26041d9e3db`, `2026-11-04T13:07:14Z` | **Pre-release**, 811 commits до `master`; текущие README не доказывают наличие всего описанного в RC |
| OpenHands / Agent Canvas | [v1.38.0](https://github.com/OpenHands/OpenHands/releases/tag/v1.38.0), `e14b76cca01a71597cee242c202eed730e745ce3`, 10 ноября | Теперь репозиторий прежде всего Agent Canvas; старые обзоры монолитного OpenHands могут быть неприменимы |
| Software Agent SDK | [v1.61.0](https://github.com/OpenHands/software-agent-sdk/releases/tag/v1.61.0), `a2ffb6ec21a6216edc9fc4b4739c076847f87e04`, 9 ноября | Версии SDK/tools/workspace/server следует согласовывать |
| Прежняя платформа | Локальный `.git/refs/heads/main`: `1382b301c8c8a94d7b2290e2112beec320e97c7e` | Это ref checkout, не доказательство чистоты working tree; публичный release UNKNOWN |

Проверка идентичности DSH: исходный `https://www.deepseek.com/harness/en/` ведёт на canonical **`https://www.deepseek.com/en/harness/`**, откуда опубликована ссылка именно на `deepseek-ai/deepseek-harness`.

---

## Report: OMP — существенные возможности и ограничения

Все утверждения этого раздела — **DOCUMENTED**, не практическая квалификация.

### Делегирование и lifecycle

| Область | Что действительно предусмотрено | Ограничение / следствие |
|---|---|---|
| Task/batch | `task.batch=true`: `{context,tasks:[{agent?,task,solutionSpace,…}]}`; одна независимая дочерняя сессия на item | `context` обязателен; `agent` задаётся **внутри item**, не сверху. Дочерний brief должен быть самодостаточным |
| Async | При `async.enabled=true` обычные items регистрируются как отдельные background jobs; результаты доставляются родителю | Agent frontmatter `blocking:true` делает конкретный item синхронным; batch может быть смешанным |
| Structured | `task.structured=true` включает `yield`, `outputSchema`, `schemaMode`; agent-level `structured:true` позволяет opt-in при выключенном глобальном setting | Default — **false**. Eval `agent()`/`workpool()` всегда structured. Default `permissive` может принять schema-invalid payload после исчерпания повторов с предупреждением |
| Приоритет schema | Item `outputSchema` → agent `output` → parent schema | Схема применяется только к structured run. Для машинного acceptance нужен `strict`, проверка статуса и error, а не только JSON sidecar |
| Артефакты | `<id>.jsonl` — история; `<id>.md` — результат; `<id>.json` — structured data; `agent://id/key/index` — извлечение | JSON sidecar сохраняется даже для schema-invalid data: наличие файла не означает успех |
| Keep-alive | После завершения agent становится `idle`; через `task.agentIdleTtlMs=420000` паркуется, освобождая live session | `0` отключает parking. `write agent://id` продолжает/оживляет agent; это новый turn, не повтор исходного вызова |
| Hub | `Alt+A`: roster, lineage, activity, usage, transcript, steering; `r` revive, `x` kill | `/agents` — **другой** экран: definitions/settings, не live roster. Advisor rows — read-only, без message/revive/kill |
| Cancel | `proc://job/kill` отменяет run; kept-alive agent может остаться resumable. Explicit Hub/RPC kill освобождает session и пишет tombstone | Kill не равен удалению истории; последующий message/revive может открыть свежий экземпляр с прежним transcript |
| Resume | `--resume`, `--continue`, Hub scan находят сохранённую историю и parked descendants | Восстановление истории само по себе не продолжает незавершённую работу |

Источники: [task reference](https://github.com/can1357/oh-my-pi/blob/main/docs/tools/task.md), [release settings.ts:271–542](https://github.com/can1357/oh-my-pi/blob/v18.18.6/packages/coding-agent/src/task/settings.ts#L271-L542), [release Agent Hub](https://github.com/can1357/oh-my-pi/blob/v18.18.6/docs/agent-hub.md).

### Restore и Vibe: особенно важные границы

**`--restore`:** сначала восстанавливает подходящие unfinished children, затем interrupted main turn. Требуются persisted child transcript и `session_init`; явно killed дети исключаются. В документации восстановление unfinished children ограничено **неизолированными** дочерними сессиями. Незавершённые tool calls получают `outcome unknown`; полностью оборванный batch может выполняться снова. Это **не exactly-once execution**.

`--restore` — interactive-only, без prompt; несовместим с `--continue`, `--fork`, imports, `--goal`, `--no-session`.

Источник: [release session operations:477–513](https://github.com/can1357/oh-my-pi/blob/v18.18.6/docs/session-operations-export-share-fork-resume.md#cli---restore).

**Vibe** — интерактивный director mode, не headless orchestration API:

- Parent получает `read`, optional `todo` и `vibe_spawn/send/wait/kill/list`; искать, исполнять и редактировать должны workers.
- `fast` → **bundled** `sonic` → `@smol`; `good` → **bundled** `task` → `@task`. Одноимённые custom definitions эти tiers не заменяют.
- Workers начинают с пустой беседы; conversation директора им не передаётся.
- Resume восстанавливает завершённых workers как idle/parked; interrupted worker turns автоматически не продолжаются.
- Exit отменяет workers; switch session приостанавливает scope иначе, без tombstone.
- Несовместим с active **и paused** plan/goal; блокирует new/delete/fork/move/handoff и reset-style loop.

Источник: [release vibe-mode.md](https://github.com/can1357/oh-my-pi/blob/v18.18.6/docs/vibe-mode.md).

### Agents, skills, модели, advisor и review

**Definitions:** user `~/.omp/agent/agents/*.md`, project `.omp/agents/*.md`. Frontmatter: `name`, `description`, `tools`, `spawns`, `model`, thinking, `output`, `structured`, `blocking`, `autoloadSkills`, `prewalk`, `advisor`.

Приоритет discovery: ближайшие project agents → user → extension roots → разрешённые Claude marketplace roots → bundled; **first-wins по точному имени**, без слияния definition. `.claude/agents`, `.codex/agents`, `.gemini/agents` напрямую намеренно не импортируются.

**Bundled source содержит шесть definitions:** `scout`, `reviewer`, `security-reviewer`, `seance`, `task`, `sonic`. Часть overview-документов перечисляет пять, пропуская `seance`. Последний — read-only консультант по сохранённой чужой сессии, с урезанной discovery/tool surface.

Источники: [discovery contract](https://github.com/can1357/oh-my-pi/blob/main/docs/task-agent-discovery.md), [release agents.ts:45–77](https://github.com/can1357/oh-my-pi/blob/v18.18.6/packages/coding-agent/src/task/agents.ts#L45-L77).

**Model routing:**

1. `task.agentModelOverrides[name]`;
2. agent frontmatter `model`;
3. parent active/default fallback.

Role aliases разрешаются через `modelRoles`; доступны custom roles. Изменение role mapping влияет на последующие launches, не переключает здорового уже работающего worker.

`task.perCallModel = off | eval | on`, default **off**:

- Exact `provider/model-id[@upstream][:level]`, не fuzzy/glob/role alias.
- Project settings могут только сузить разрешение, не включить его и не предоставить новые grants.
- `task.perCallModelAllow` дополнительно сужает операторские grants.
- При `agentModelOverrides` per-call model — **конфликт**, а не override.
- Per-call worker не должен автоматически уходить на другую модель: fallback/promotion/prewalk отключаются; revival повторно проверяет текущие grants.
- Но maintenance calls, включая compaction/advisor, **не покрыты** этим main-loop model gate. Нельзя трактовать его как полный финансовый/provider boundary.

**Skills:** metadata в prompt, body по `skill://`; стандартный layout `skills/<name>/SKILL.md`, не рекурсивный. `autoloadSkills` берёт skills из parent; неизвестные имена игнорируются. `tools:[]` у agent не является полным запретом расширений: MCP/extension/custom tools могут оставаться additive.

**Контекст:** task children отбрасывают файлы с именем **`AGENTS.md`**, но получают sticky `RULES.md`; существенные ограничения надо явно включать в delegation context либо подходящие shared rules. Нативные project settings ищутся от cwd иначе, чем nearest-ancestor context/agent discovery — не путать эти механизмы.

Источники: [routing/per-call details](https://github.com/can1357/oh-my-pi/blob/main/docs/task-agent-discovery.md#per-call-model), [skills](https://github.com/can1357/oh-my-pi/blob/main/docs/skills.md), [release context files](https://github.com/can1357/oh-my-pi/blob/v18.18.6/docs/context-files.md).

**Advisor:** отдельный reviewer runtime, default disabled; `advisor.enabled`, `modelRoles.advisor`, `WATCHDOG.md`/`WATCHDOG.yml`, per-agent `task.agentAdvisor`. Это **не approval authority**. Default tools read/grep/glob, но roster может разрешать mutating tools. `advisor.syncBacklog:strict` допускает ожидание **без wall-clock cap**; headless final-review drain также имеет особую strict-семантику.

**`/review`:** команда сама не запускает reviewer — возвращает main prompt с указанием вызвать `task`. Fan-out зависит от diff, до 16 reviewers. Bundled reviewer имеет `output`, но не `structured:true`; при default task settings результат остаётся текстом. Review — мнение модели, не независимая verification.

Источники: [advisor](https://github.com/can1357/oh-my-pi/blob/main/docs/advisor-watchdog.md), [review internals:515–563](https://github.com/can1357/oh-my-pi/blob/main/docs/slash-command-internals.md#15-bundled-command-note-review).

### Isolation, merge, limits, hangs

- `task.isolation.enabled=false` — это gate; даже после включения item должен содержать `isolated:true`.
- `task.isolation.apply=true` по умолчанию; `merge=patch`. Для экспериментов разумно **retain artifacts, без auto-apply** — рекомендация, не выполненное изменение.
- Нужен Git repo; uncommitted baseline ограничен **1 GiB**.
- Isolated keep-alive agent сохраняет workspace при idle/parking; release захватывает изменения и очищает handle.
- Branch integration в исходнике — **последовательный cherry-pick**, остановка при первом конфликте, без stash рабочего дерева. UI description `merge --no-ff` в settings устарел.
- `auto` может выбрать ovnfs, если executable найден; после его выбора ошибка ovnfs не переключает run молча на native backend.
- Ни отдельный checkout, ни ProjFS не ограничивают ambient filesystem/network доступ внешних программ.

Источники: [task isolation reference](https://github.com/can1357/oh-my-pi/blob/main/docs/tools/task.md), [release worktree.ts:1049–1097](https://github.com/can1357/oh-my-pi/blob/v18.18.6/packages/coding-agent/src/task/worktree.ts#L1049-L1097).

Ограничения из source/docs, **не локальный cfg**:

| Setting / механизм | Значение / смысл |
|---|---|
| `task.maxConcurrency` | Default 32; `0` unlimited; semaphore scope — session/task tool, не универсальный глобальный лимит дерева |
| `task.workerThreads` | Default 4; **1–8 concurrent runs остаются на main thread**; workers добавляются от 9, затем 18/36/72; SDK embedding не использует этот CLI механизм |
| `task.maxRecursionDepth` | Default 2; negative unlimited; на границе убирается recursive task capability |
| `task.maxRuntimeMs` | Default **0**, wall-clock cap выключен |
| `task.softRequestBudget` | Default 200, scout/sonic ceiling 100; exact-name override может поднять/отключить |
| Budget exhaustion | Notice на budget; на 1.5× остановка свободного turn и forced wrap-up; source допускает ещё 5 requests до hard abort |
| `async.maxJobs` | Default 100 running jobs; queued/parked slots не занимают |
| `session.maxCost` / `--max-cost` | Прекращает новые запросы по catalog-priced spend; in-flight запрос может превысить ceiling |
| Stream watchdogs | `providers.streamFirstEventTimeoutSeconds`, `streamIdleTimeoutSeconds`: `-1` provider defaults, `0` disabled |
| Tool timeout | `tools.maxTimeout=0` означает отсутствие settings cap, не обязательный deadline каждого вызова |

Источники: [release task settings](https://github.com/can1357/oh-my-pi/blob/v18.18.6/packages/coding-agent/src/task/settings.ts), [executor budget implementation](https://github.com/can1357/oh-my-pi/blob/main/packages/coding-agent/src/task/executor.ts#L192-L248), [settings reference](https://github.com/can1357/oh-my-pi/blob/main/docs/settings.md).

**Известные пути бесконечного/долгого ожидания:** выключенные runtime/watchdog deadlines; `advisor.syncBacklog:strict`; MCP `timeout:0`; print MCP readiness при `OMP_MCP_TIMEOUT_MS=0`; RPC consumer, который оставил stdout открытым, но перестал читать. Это не гипотетический общий «агент может зависнуть», а документированные границы.

### CLI, RPC, ACP, extensions и Windows

**CLI:** TUI; `-p` one-shot; `--mode json`; SDK; `--mode rpc`; `omp acp`. Print без `--wait-async`/`async.printWake` не следует использовать как durable background orchestrator: фоновые jobs отменяются при выходе. `--restore` и Vibe не являются headless interfaces.

**RPC:** собственный JSONL protocol, **не JSON-RPC 2.0**. ACK `prompt` означает admission, а не окончание работы; существуют `prompt_result` и `session_settled`. Есть subagent subscriptions/control. V2 позволяет chunked logical frames до 64 MiB; stdout надо непрерывно читать.

**Native ACP действительно реализован:** в закреплённом release `AcpAgent.initialize()` объявляет `loadSession`, list/fork/resume/close, HTTP/SSE MCP, embedded context/images; существуют соответствующие handlers, model/config control, cancel и steering. `acp-mode.ts` поднимает stdio NDJSON connection и отделяет diagnostics от protocol stdout.

Источники: [RPC](https://github.com/can1357/oh-my-pi/blob/main/docs/rpc.md), [release ACP capabilities:1029–1079](https://github.com/can1357/oh-my-pi/blob/v18.18.6/packages/coding-agent/src/modes/acp/acp-agent.ts#L1029-L1079), [ACP startup source](https://github.com/can1357/oh-my-pi/blob/main/packages/coding-agent/src/modes/acp/acp-mode.ts).

**Approval:** default yolo. Headless children принудительно получают `tools.approvalMode:yolo`, но explicit deny/prompt сохраняются; prompt без UI завершается отказом. Approval — не containment. `bash.patterns` не контролирует shell, запущенный через eval. Ограниченный built-in tool list также не равен чистой capabilities boundary.

**Extensions:** TS/JS factory, tools/commands/events/context injection. `--hook` сейчас alias extension; legacy HookRunner — не основной runtime. Hooks могут блокировать/переписывать вызовы и routing; импортируемый код работает с полномочиями процесса, в том числе `pi.exec()` доступен во время load. Для нового integration не строить вторую систему legacy hooks.

**MCP:** native `.omp/mcp.json`, user `~/.omp/agent/mcp.json`; stdio/HTTP/SSE. Default request timeout 30s; `OMP_MCP_TIMEOUT_MS` выше server timeout; `0` отключает deadline. Parent connections переиспользуются children без независимого proxy deadline.

Источники: [approval](https://github.com/can1357/oh-my-pi/blob/main/docs/approval-mode.md), [hooks](https://github.com/can1357/oh-my-pi/blob/main/docs/hooks.md), [extensions](https://github.com/can1357/oh-my-pi/blob/main/docs/extensions.md), [MCP](https://github.com/can1357/oh-my-pi/blob/main/docs/mcp-config.md).

**Windows:**

- Native Windows поддерживается; Bun package route документирует **Bun ≥1.4.4**, существует compiled binary. WSL не является общим обязательным условием OMP.
- Embedded non-PTY bash не требует считать Git Bash основной runtime; external commands и Git всё равно зависят от доступных executable.
- Windows cancellation не эквивалентен POSIX catchable TERM; native cleanup имеет платформенные grace windows.
- ProjFS требует загружаемый `ProjectedFSLib.dll`; x64-under-ARM64 emulation явно отклоняется.
- Block-clone source уточняет **ReFS/Dev Drive**; NTFS может отказать, несмотря на более широкое описание в UI.
- Наличие backend в enum не доказывает доступность на машине.

Источники: [release README](https://github.com/can1357/oh-my-pi/blob/v18.18.6/README.md), [native shell/process](https://github.com/can1357/oh-my-pi/blob/main/docs/natives-shell-pty-process.md), [ProjFS](https://github.com/can1357/oh-my-pi/blob/v18.18.6/crates/pi-iso/src/projfs.rs), [block clone](https://github.com/can1357/oh-my-pi/blob/v18.18.6/crates/pi-iso/src/windows_block_clone.rs).

---

## OpenClaw и конкретно OpenClaw→OMP

### Что добавляет OpenClaw

**DOCUMENTED:**

- Один long-lived Gateway — control plane sessions/tools/events/channels; WS default `127.0.0.1:18789`.
- Durable schedules/events, run history и restart reconciliation; Gateway должен работать, чтобы schedule исполнялся.
- Native subagent sessions, configurable nesting, completion announce chain, cascade stop.
- Native children default: `maxConcurrent=8` на immediate parent session, `maxChildrenPerAgent=5`, `maxSpawnDepth=5`; вложенные controllers имеют собственные execution budgets.
- После restart восстанавливается eligible root requester, **не независимо каждый старый child**. Сохранённая запись не доказывает живого исполнителя.
- Interrupted effects не exactly-once: перед повтором требуется reconciliation.
- ACP — отдельный external-harness runtime через plugin `@openclaw/acpx`, не тот же путь, что native OpenClaw subagents.

Источники: [Gateway architecture](https://docs.openclaw.ai/concepts/architecture), [automations runtime](https://docs.openclaw.ai/automation/cron-jobs/how-it-works), [nesting](https://docs.openclaw.ai/tools/subagents/nesting), [recovery/stopping](https://docs.openclaw.ai/tools/subagents/operations).

### Есть ли OMP adapter

**Да — native ACP server внутри OMP. Нет доказательства отдельного официального first-class OpenClaw OMP profile.**

- В исследованных OpenClaw harness lists **`omp` не указан**; `pi` относится к другому проекту, не доказывает OMP integration.
- acpx поддерживает custom named agents. Кандидат launch — структурированный argv `["<absolute omp executable>","acp"]`; на Windows custom raw command string не поддерживается, требуется `argv`.
- Помимо acpx alias нужны OpenClaw ACP enablement, healthy backend, allowed agent mapping и policy admission.
- OpenClaw release package фиксирует `acpx=0.19.4`; moving `openclaw/acpx/main` может иметь новые profiles, которых нет в этой версии.
- Найден сторонний [`jiwangyihao/omp-acp`](https://github.com/jiwangyihao/omp-acp): отдельный ACP→OMP RPC bridge, MPL-2.0; README ссылается на fork OMP и сообщает injected extension, удаляющий ask. Это **не официальный OpenClaw adapter**, и при наличии native ACP добавляет ненужный translation layer. Не рекомендован исходным вариантом.

Источники: [OpenClaw quickstart/targets](https://docs.openclaw.ai/tools/acp-agents/quickstart), [setup](https://docs.openclaw.ai/tools/acp-agents-setup), [custom acpx agents](https://github.com/openclaw/acpx/blob/main/docs/custom-agents.md), [Windows argv/config](https://github.com/openclaw/acpx/blob/main/docs/config.md), [pinned package.json](https://github.com/openclaw/openclaw/blob/v2026.11.3/package.json#L2395).

**UNKNOWN до E2E:** create→prompt→cancel→resume→model control→background-result delivery для конкретной пары OpenClaw/acpx/OMP; propagation cancel к OMP grandchildren; поведение при Gateway/process restart. Наличие ACP methods с обеих сторон этого не доказывает.

### Security / Windows

ACP harness запускается **на host вне OpenClaw sandbox**. Sandboxed requester не может просто породить host ACP; `sandbox:"require"` для ACP не поддерживается. Gateway контролирует admission/ownership/delivery, но не ambient tools внешнего harness.

OpenClaw — один trust boundary на Gateway, не hostile multi-tenant isolation.

Pinned release Node engine: **`>=24.16.0 <25 || >=26.1.0`**. Текущая документация отдельно рекомендует более свежие security patch versions. Windows docs теперь включают native CLI/Tauri и Windows Hub с app-owned WSL Gateway; старое универсальное «только WSL2» неверно. Но это moving docs, не обещание всех этих путей закреплённого release.

Источники: [ACP sandbox boundary](https://docs.openclaw.ai/tools/acp-agents/delivery#sandbox-compatibility), [security model](https://docs.openclaw.ai/gateway/security), [Windows](https://docs.openclaw.ai/platforms/windows).

---

## DSH: что реально доступно

**DOCUMENTED:** open-source MIT developer preview, Cordis plugin architecture; Web/Desktop, headless/SDK/ACP profiles, subagents и scheduled-task plugins. Официальный source прямо предупреждает о breaking changes и отсутствии security audit.

- Node CLI в закреплённом RC требует **Node ≥24.9.0**.
- Текущий ACP launcher: **`dsh --profile acp`**, не вымышленный отдельный public `dsh-acp` binary.
- ACP поддерживает persistent list/resume/close, concurrent independent sessions, model/effort config, MCP, prompt/cancel.
- Намеренно **нет** `session/load`, transcript replay, ACP fork/delete, extra dirs, interactive elicitation, terminal/client filesystem delegation.
- `authenticate` возвращает success без собственной authentication: предполагается trusted stdio controller.
- acpx `main` уже имеет реальный профиль **`deepseek-harness` → `dsh --profile acp`**. Но в исследованном OpenClaw quickstart список отстаёт; присутствие этого profile в установленном pinned backend — UNKNOWN.
- OpenClaw delivery guide местами требует `session/load`, тогда как актуальный acpx DSH profile описывает предпочтение `session/resume`. **Нужно квалифицировать конкретные версии**, не переносить общий resume-текст буквально.

Источники: [DSH ACP contract](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/acp/acp/README.md), [CLI](https://github.com/deepseek-ai/deepseek-harness/blob/master/apps/cli/README.md), [acpx DSH profile](https://github.com/openclaw/acpx/blob/main/agents/DeepSeekHarness.md), [safety](https://github.com/deepseek-ai/deepseek-harness/blob/master/SAFETY.md).

**Официальный `subagent_codex` — другой механизм:** один fresh native Codex process/thread/turn, без follow-up/resume; workspace родителя, результат без полного tool transcript/diff. `permissionMode=never` означает no human approvals, **sandbox override отсутствует** — действует native Codex policy. Current bundle поставляет pinned payload; старый pilot с host Codex CLI нельзя автоматически считать проверкой нынешней упаковки.

Источник: [DSH Codex provider contract](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/subagent/subagent-codex/README.md).

**Не переносить:** Cordis composition/plugin manager, ещё один agent loop/scheduler и собственный ACP bridge ради повторения уже имеющихся OMP возможностей. DSH оставить альтернативным harness для отдельного A/B, если важны его document/UI/plugin workflows.

---

## Прежняя Agent Platform: локальные находки

Публичная доступность **FAILED/404**; локальные исходники доступны. Корень ниже обозначен `../agent-platform/`.

### Files

- `README.md:1–175` — честная status matrix и разделение execution planes.
- `docs/architecture.md:1–42` — board/controller/budget/workflow/verification/MCP и recovery limitations.
- `agent_platform/workflow.py:112–400` — workflow state и immutable contracts; файл около 245 KB.
- `agent_platform/integration.py:134–300` — immutable integration evidence/proposal; не merge authority.
- `agent_platform/verification.py:35–94` — exact-type qualification checks.
- `agent_platform/native_execution.py:48–63,418–438` — qualification contract и gate.
- `pilots/codex-developer-e2e/README.md:1–80`, `evidence.json:1–80` — ограниченная provenance прежнего E2E.
- `docs/operations/dsh-native-codex-pilot.md:1–150` — DSH `0.2.1-rc.2`, Codex `0.163.0`, supervised pilot.

### Выводы

**DOCUMENTED/source:** это custom control plane, не универсальный harness: SQLite Task Board, reservations/budgets, immutable proposal/workflow journals, Git evidence, independent verifier, Proof Pack, DSH MCP bridge.

**Критический source факт:** `_CUSTOM_MXC_QUALIFICATION = None` в `native_execution.py:63`; production runner admission требует attested qualification. Нельзя включать managed Developer, просто скопировав код. Пустой test-runner registry сам по себе не вся логика — существует gated Windows MXC path, но qualification отсутствует.

**CLAIMED с сохранённым evidence:** один DSH-native duration formatter pilot сообщает 12/12 PASS. `evidence.json` явно отделяет operator-reported delegation/sandbox от внешнего acceptance; полного child transcript нет. Это не VERIFIED в текущем исследовании и не квалификация Platform Controller, budgets, trusted checks, unattended recovery или reviewer/fix loop.

**Что сохранить как идеи:** явное отделение model claims от verification; неизвестные usage/outcome не превращать в zero/success; snapshot-bound acceptance; не повторять неопределённые side effects автоматически.

**Что не переносить в начальную архитектуру:** custom scheduler/board/workflow/budget ledger, D4 promotion/F2 integration machinery, MXC backend и общий Proof Pack framework. Они дублируют зрелые части harness и добавляют собственную qualification/recovery проблему. Существующие ограничения раздельных SQLite stores и ручной recovery прямо документированы.

---

## OpenHands: актуальная альтернатива

**DOCUMENTED:** сейчас два основных слоя:

1. **Software Agent SDK / Agent Server** — Python agent behavior, tools, conversations, workspace, REST/WS; browser-compatible TS client.
2. **Agent Canvas** — UI/backend control; scheduling/webhooks принадлежат отдельному `OpenHands/automation`.

SDK имеет реальные примеры persistence, async interrupt→PAUSED→resume, delegation, routing, MCP, hooks, condenser, structured `FinishTool.response_schema`. Это доступные implementation examples, **не выполненные нами проверки**.

Требования:

- SDK v1.61.0: **Python ≥3.12**.
- Canvas local stack: **Node ≥24 + uv**.
- Local unsandboxed mode даёт agent host filesystem access.
- Windows Docker quickstart предусмотрен; per-conversation multi-container runtime требует **WSL2 + Docker integration**, native Windows host этим runtime не поддерживается.
- SDK/tools следует закреплять одной версией.

Источники: [repository boundaries](https://github.com/OpenHands/software-agent-sdk#repository-boundaries), [architecture](https://docs.openhands.dev/sdk/arch/overview), [pinned Python requirement](https://github.com/OpenHands/software-agent-sdk/blob/v1.61.0/openhands-sdk/pyproject.toml#L1-L7), [Windows Canvas](https://github.com/OpenHands/OpenHands/blob/main/README.windows.md), [examples](https://github.com/OpenHands/software-agent-sdk/tree/main/examples/01_standalone_sdk).

**Рекомендация:** рассматривать OpenHands, когда нужны programmatic Python/REST agents и container workspaces как основной deployment contract. Для текущей исследовательской задачи это смена стека, а не необходимое дополнение к OMP.

---

## Architecture: boring comparison и условия добавления OpenClaw

| Вариант | Когда разумен | Главная цена / граница |
|---|---|---|
| **OMP-only** | Интерактивная работа, ограниченные parallel lanes, human steering/review, CLI/RPC automation | Надо квалифицировать restore/cancel/isolation; нет необходимости строить второй control plane |
| **OpenClaw + OMP** | Реально нужны always-on triggers, расписания, chat-channel control и persistent bindings | Gateway + plugin + acpx + OMP; custom alias, двойной lifecycle, host ACP вне sandbox |
| **OpenClaw + DSH** | Те же внешние triggers плюс специфические DSH document/plugin workflows | Preview API churn, version skew; ограниченный ACP UX и resume contract |
| **OpenHands SDK/Canvas** | Python/REST integration, remote/container execution, multi-user developer UI | Другой runtime/deployment stack; Docker/WSL и согласование package versions |

**Рекомендуемый исходный контур:** один OMP owner → небольшое число самодостаточных specialist tasks → сохранённые transcripts/results → отдельное операторское принятие результата. Один writer на конкретный shared checkout; для параллельных изменений — отдельные retained workspaces, без автоматического применения результата. Не строить собственную БД orchestration до обнаружения конкретного незакрытого требования.

**Добавлять OpenClaw только если одновременно выполнено:**

1. Есть конкретный внешний trigger/channel/schedule, которого действительно недостаточно запускать оператором.
2. Нужен постоянно работающий Gateway и есть владелец его lifecycle.

3. Закреплена совместимая тройка OpenClaw/acpx/OMP либо DSH.
4. Отдельно квалифицированы prompt completion, cancel дерева, resume после restart, result delivery и model selection.
5. Host execution boundary принята явно; «ACP» не используется как синоним sandbox.
6. Orchestration ownership остаётся одним: OpenClaw управляет внешним заданием, OMP — внутренними workers; не создавать взаимно рекурсивные две команды агентов.

Это рекомендации для следующей квалификации, не выполненные изменения и не заявление production readiness.