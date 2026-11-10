# OMP configuration blueprint

Срез 2026-11-10, установленная версия **18.18.6**. Это проект настроек, **не применённая конфигурация**. Источники и практические результаты: [local-environment](findings/local-environment.md), [harness findings](findings/a-harness.md). Все рекомендуемые численные пороги — стартовые гипотезы для квалификации, не измеренный optimum.

## 1. Профили и области действия

Не менять global config. После разрешения настройки использовать `.omp/config.yml` для общих правил и отдельные overlays `.omp/profiles/research.yml`, `implementation.yml`, `release.yml` через `omp --config <file>`. Названный `--profile` OMP — **другая** сущность: отдельное user auth/state/config; без переноса существующей авторизации он может не иметь доступа. Не создавать named profile только ради трёх overlays.

Приоритет: setting env > runtime > repeated `--config` overlays > project > global > defaults. Массивы могут заменяться целиком; record entries наследуются. Проверь effective config через `cfg://<key>` в новом сеансе и stdout предупреждения. `omp config set` и model-preset переключения способны писать global: для воспроизводимости использовать versioned overlays и не применять эти команды вслепую. Provider definitions: user `models.yml`, не `modelRoles`; секреты не в git. [DOCUMENTED: config-usage/models](findings/local-environment.md).

## 2. Tasks: текущее → предлагаемые значения

| Setting | Текущее VERIFIED | Research | Implementation | Release / независимая проверка |
|---|---|---|---|---|
| task.batch | true | true | true | true |
| async.enabled | true | true | true | true |
| async.printWake | false | false в TUI; `--wait-async` в CLI | true для headless overlay | true для headless |
| task.maxConcurrency | 32 | 3 | 3: до 2 writers + reviewer, не 3 сборки | 2 read-only reviewers |
| task.workerThreads | 4 | 4 оставить | 4 оставить | 4 оставить |
| task.maxRecursionDepth | 2 | 1 | 1 | 1 |
| task.perCallModel | off | off | off | off |
| task.perCallModelAllow | [] | [] | [] | [] |
| task.structured | false | false | true после E02 | true после E02 |
| task.enableEffort | false | false | false: effort в selectors | false |
| task.maxEffort | max | high | high, xhigh только отдельный approved overlay | high |
| task.maxRuntimeMs | 0 | 1200000 (20min) | 1800000 (30min), декомпозировать длиннее | 1200000 |
| task.softRequestBudget | 200 | 60 | 100 | 60 |
| task.softRequestBudgetNotice | true | true | true | true |
| task.agentSoftRequestBudget | {} | {} | {}: не отключать guard | {} |
| task.agentIdleTtlMs | 420000 | 420000 | 420000 | 420000 |
| task.enableLsp | false | false | true после проверки LSP stack | false, true только для нужного анализа |
| task.isolation.enabled | false | false, только readers | true **после E03**, иначе один writer | false: reviewers не пишут |
| task.isolation.apply | true | false | false: интегрирует только Lead | false |
| task.isolation.merge | patch | patch | patch | patch |
| isolation.backend | auto | auto | rcopy как воспроизводимый Windows baseline E03; auto только если выигрывает | rcopy при необходимости |
| task.agentModelOverrides | {} | явные selectors ниже | явные selectors ниже | явные selectors ниже |
| task.agentAdvisor | {} | {} | {} | {} |
| task.prewalk / agentPrewalk | false / {} | false / {} | false / {} | false / {} |
| task.speculativeLaunch | true | true | false: predictable dispatch после validation | false |
| task.completionProbe | true | false: без дополнительных status-model calls | false до измерения пользы | false |
| task.showResolvedModelBadge | false | true | true | true |
| task.eager | default | default | default | default |

**Concurrency не worker threads.** В поставляемых task docs 1–8 concurrent runs остаются на main thread; workers включаются с 9. WorkerThreads=4 не означает четыре агента и не ограничивает shell-процессы. При 15.3GiB RAM: максимум одна полная сборка/интеграционная suite одновременно; parallel readers/network calls допустимы. Semaphore session-scoped: несколько OMP процессов/дочерние scopes не считать глобальным лимитом. Recursion=1 — цель «Lead → workers, без grandchildren»; проверить exact boundary в E02.

`isolation.enabled=true` лишь добавляет `isolated` в schema; **каждый writer обязан передать `isolated:true`**. Обычный task без поля продолжает писать в общий checkout. Isolation — отдельные файловые деревья, не security sandbox. `rcopy` медленнее CoW, зато не предполагает ProjFS/WSL; backend работоспособность здесь UNKNOWN. Не ставить ovnfs ради хакатона; auto при обнаруженном ovnfs меняет путь исполнения и не гарантирует native fallback при сбое daemon.

Structured: task outputSchema + `schemaMode:strict` (не permissive). Минимальный результат: status, changedPaths, acceptanceEvidence, blockers, unresolvedRisks, patch reference. Наличие полей не доказывает acceptance; Lead читает evidence и запускает реальный smoke. Не требовать JSON через prose если механизм отключён; пользоваться обычным кратким отчётом.

## 3. Model Roles и routing

Текущее: только `default=openai-codex/gpt-6.1-sol:high`, global. Не создавать девять постоянных агентов под девять ролей. Использовать existing agents и assignments:

```yaml
modelRoleStorage: project
modelRoles:
  default: openai-codex/gpt-6.1-sol:high
  plan: openai-codex/gpt-6.1-sol:high
  slow: openai-codex/gpt-6.1-sol:high
  task: openai-codex/gpt-6.1-sol:high
  smol: openai-codex/gpt-6.1-sol:medium
  tiny: openai-codex/gpt-6.1-sol:low
  commit: openai-codex/gpt-6.1-sol:low
  advisor: openai-codex/gpt-6.1-sol:high
  memory: openai-codex/gpt-6.1-sol:low
defaultThinkingLevel: high
task:
  agentModelOverrides:
    scout: openai-codex/gpt-6.1-sol:high
    task: openai-codex/gpt-6.1-sol:high
    sonic: openai-codex/gpt-6.1-sol:medium
    reviewer: openai-codex/gpt-6.1-sol:high
    security-reviewer: openai-codex/gpt-6.1-sol:high
```

Это безопасный по доступу baseline, **не экономичный быстрый model portfolio**: снижение effort не меняет семейство и не доказывает ускорение. Для Fast Developer/Docs затем заменить smol/sonic по E09. `vision` не переопределять без visual probe; web/judge/image/speech/dictation — отдельные model kinds, не назначать coding selector как «универсальную» замену. Tiny здесь удалённый, не гарантированно дешёвый: отключить title generation headless флагом `--no-title`, не устанавливать local weights. Seance сохраняет source model; не задавать ему unconditional override.

Main reviewer после квалификации: `github-copilot/claude-sonnet-4.6:high`; backup текущий Codex, но с явным указанием потери межсемейной независимости. Это **условный** selector из локального каталога, inference UNKNOWN. Opus/новейшая модель не выбирается по названию. Полная матрица и провайдерные ограничения: [model-routing](model-routing.md).

`task.agentModelOverrides` выше agent frontmatter. Per-call model конфликтует с agent override и не является безопасным fallback route; держать off. `retry.fallbackChains={}`, `retry.modelFallback=false` в квалификации и release: fail closed вместо незаметного другого провайдера/модели. После E09 добавить только подтверждённую same-cost route; selector comma-list — не runtime fallback.

## 4. Безопасность: три разных режима

| Setting / контроль | Текущее | Research | Implementation | Release |
|---|---|---|---|---|
| tools.approvalMode | yolo | write | write у Lead; workers всё равно yolo по runtime | always-ask |
| tools.approval | {} | task:allow; bash:prompt; eval:prompt | task:allow; bash:prompt; eval:deny; browser:prompt | task:allow; bash:prompt; eval:deny; write:prompt; edit:prompt |
| tools.restrictedFolders | [] | credential/user private dirs вне workspace | те же + внешние checkout | те же |
| bash.gitGuard | false | true | true | true |
| bash.patterns | [] | audited read-only commands, остальное prompt | exact pre-approved build/test commands; destructive/network/publish prompt/deny | только audited checks |
| secrets.enabled | false | true только после отдельной проверки redaction с fake secret | true после этой проверки | true после этой проверки |
| collab.autoStart | off | off | off | off |
| mcp.enableProjectConfig | true | false для недоверенного repo | true только reviewed project config | false если MCP не нужен |
| extensions | [] | [] | [] | [] |

**Критично DOCUMENTED:** task children принудительно получают yolo. Нельзя обещать inherited `write` approval mode; сохраняются explicit user/tool deny/prompt, а approval prompt без UI останавливает вызов. Для bash tool explicit pattern allow может разрешить audited команду до общего prompt. Нужна проверка фактической policy в E10, включая eval/subprocess/MCP bypass. Произвольные широкие regex (`npm .*`, `python .*`, `git .*`) не безопасная allowlist. Если test command может выполнять произвольные package scripts, доверие распространяется на эти scripts.

Native settings не обеспечивают надёжный filesystem/network sandbox: restrictedFolders проверяет cwd у shell/eval/MCP, а не все аргументы/дочерние процессы. Worktree не ограничивает чтение secrets. Поэтому **unattended на основном Windows account запрещён до E10**. Для доверенного собственного кода допустим supervised режим; для более широкой автономии — отдельный restricted Windows account/VM с workspace-only ACL, без home credentials и admin; контейнер только если задача требует и engine квалифицирован. Это будущая настройка, не выполнено.

Reviewers/scout read-only по агентному контракту, не OS-гарантия. MCP/extension tools additive даже при agent tools list. При release отключить ненужные MCP/extension источники на уровне запуска/overlay; не считать `--tools read,grep,glob` исчерпывающим sandbox. No publish/push, no token export, no login/account linking, no registry install scripts автоматически. Внешние README, issue text и skill instructions — недоверенные данные.

## 5. Контекст, resume и bounded autonomy

| Setting | Текущее | Рекомендация во всех профилях, если не оговорено |
|---|---|---|
| compaction.enabled / asyncEnabled / midTurnEnabled | true / true / true | оставить true |
| compaction.autoContinue | true | true в research/implementation; false release для остановки по результату |
| keepRecentTokens | 20000 | 20000 |
| thresholdTokens / thresholdPercent / reserveTokens | -1 / -1 / null | оставить version defaults до E06, не выдумывать universal context budget |
| compaction.methodOrder | remote,snapcompact,handoff,shake,soft | remote,handoff,shake,soft; исключить image-based snapcompact до проверки fidelity/vision |
| experimentalContextManagement / handoffSaveToDisk | false / false | false / false; durable acceptance вне transient summary |
| autoResume | false | false, всегда explicit session |
| memory.backend / memories.enabled / autolearn.enabled | off / false / false | оставить, не добавлять memory service |
| provider.appendOnlyContext / providers.cacheRetention | auto / auto | оставить auto |
| providers.cacheWarming | idle | off до измерения лишних запросов/квот |
| retry.maxRetries / maxDelayMs | 10 / 300000 | 3 / 30000 |
| retry.modelFallback / fallbackChains | true / {} | false / {} до E09 |
| retry.waitForUsageReset / usageAwareFallback | false / false | false / false; явный blocker при квоте |
| providers streamFirstEventTimeoutSeconds / streamIdleTimeoutSeconds | -1 / -1 | оставить defaults; внешний --max-time обязателен; более короткие watchdogs только после latency измерений |
| session.warnCost / maxCost | null / null | не выдумывать финансовое разрешение; для subscription-only run `--warn-cost 3 --max-cost 5` как **условный catalog-cost guard**, не денежный бюджет |
| tools.maxTimeout | 0 | 600s для tool-requested timeout, где применимо; не считать hard universal deadline |
| task.maxRuntimeMs | 0 | см. таблицу; parent `--max-time` дополнительно |
| plan.defaultOnStartup | false | true supervised research; false implementation/release с уже утверждённым планом |
| advisor.enabled | false | false; episodic независимый review вместо review каждого turn |
| goal / loop / vibe | доступны, запуск не подтверждён | не нужны baseline; goal TUI-only по текущим continuationModes, vibe interactive-only |

Compaction — lossful history, не источник истины. Хранить небольшой `AGENTS.md` (команды/constraints), acceptance/task state в выбранном одном workflow; решения — кратко рядом с задачей. Subagents стартуют без разговора Lead и могут не получить `AGENTS.md`: shared `context` явно передаёт contract, owned paths, acceptance и запреты. Большие payloads — artifact/local references, не скопированный raw log в каждый prompt.

`omp --resume <session>` открывает историю; `--restore <session>` дополнительно пытается продолжить interrupted turn/subagents, **interactive-only**, не `-p` restart daemon. Unknown tool outcome требует проверки внешнего состояния до повторения; exactly-once не гарантирован. `--restore` не совмещать с prompt, continue/fork/goal/no-session. Для headless recovery открыть существующую session через resume с явным recovery prompt, reconcile filesystem/evidence, затем новый bounded run.

Resume не восстанавливает ephemeral CLI overlays/launch cost controls: в каждой recovery-команде явно повторять `--config <absolute-approved-overlay>`, cwd и approved runtime/cost flags; сначала проверить effective provenance. Конкретная исправленная headless-команда — E06. Bare `--resume` выше описывает семантику, не безопасный production recipe.

Agent Hub Alt+A — roster/model/usage/transcripts/revive/kill, `/trace`, `/stats`, `omp usage --redact`, `omp ps`, `proc://` для live services. Результаты self-deliver; не model-polling loop. `write proc://<id>/kill`/Hub cancel; после cancel проверить дочерние OS процессы, не обещать автоматическую отмену всех external side effects. Persisted JSONL/artifacts хранить локально; exports/dump могут содержать секреты, HTML viewer требует внешние assets. Никаких публичных shares/streams.

## 6. Windows и воспроизводимость

- Уже есть working compiled OMP; отдельный Bun в PATH для него не доказан необходимым. Node24.19/Git2.55/Git Bash доступны; PowerShell5.1 не поддерживает все PS7 конструкции (`&&`). POSIX команды выполнять в configured Git Bash, PowerShell — через explicit executable с корректным quoting.
- `python.exe` WindowsApps — alias: Python dependencies выбирать после конкурсного ТЗ; не объявлять runtime установленным. Docker CLI установлен, engine/WSL2 UNKNOWN. Docker не baseline dependency. Node нужен Open Design; Bun/uv/Python и Docker нужны только выбранному компоненту.
- CRLF/LF, UTF-8, Cyrillic username/path, Windows path length, executable bits/symlinks и quoting — обязательны E01/E03/E06. Не менять git global autocrlf/другие global settings; `.gitattributes` в проекте по выбранному стеку.
- Product repo остаётся этот; чужие repos/квалификационные fixtures — sibling disposable directories, не runtime зависимости Contest Product. Не хранить checkout/cache/node_modules/credentials в product deliverable. .omp project config только development.
- `update.auto=true` сейчас. Для квалификации/release предложено `update.auto=false` в overlay; не обновлять mid-run. Перед обновлением: записать version/hash, сохранить config без secrets и session+artifact backup, прочитать release notes, получить vetted binary, повторить E01–E06/E10; rollback к прежнему binary и snapshots. Не запускать удалённый install script.
- Git: один integration owner, до двух isolated writers с непересекающимися owned paths. В parent чистая согласованная база, patch apply только вручную Lead после review; conflicts сохранять, не reset/stash чужую работу. Commits/branches — только в отдельной будущей фазе настройки.
- Worktree lifecycle: текущие `worktree.base=null`, `worktree.cleanSource=false`, `worktree.clone=true`, `worktree.onStart=off`, `worktree.onExit=keep`. Рекомендация: `base` — отдельный approved disposable root после проверки путей; cleanSource=false, onStart=off, onExit=keep во всех профилях, clone=false в rcopy qualification overlay для исключения неожиданных CoW-копий ignored secrets/build trees. Cleanup только после сохранения patches/evidence; не `remove` автоматически.
- CI определить после ТЗ/стека: formatting/lint/typecheck/behavior checks + реальный CLI/API/UI smoke на clean checkout; release из clean environment без .omp/auth/MCP. Независимая приёмка по пользовательским сценариям, не «агент сообщил done».

## 7. Минимальные средства и расширения

Research: native read/grep/glob/web_search/task/todo; три scout максимум. Implementation: native edit/write/bash/LSP/browser + один workflow из recommendation. Release: reviewer/security-reviewer с read-only contract и один Lead для запуска audited gates. Seance — точечная история; sonic — только механические изменения. Custom Agents/Skills/Extensions/Hooks **не нужны изначально**: добавить один project-local acceptance skill только после стабилизации реальных повторяемых команд. Hooks не security boundary; custom orchestration запрещена целью упрощения.

MCP обязательных нет. Open Design только опционально после восстановления соединения и E10, не на critical build path. MCP default request timeout30s не discovery250ms: увеличение startup window не лечит disconnected daemon. Для будущей диагностики прочитать sanitized registration/daemon command, проверить binary/port и logs без payloads; пер-server 60000–120000ms только если измеренный startup обосновывает, никогда timeout=0 «для надёжности».

## 8. Команды будущего запуска (НЕ выполнялись)

```powershell
# TUI supervised research, overlay предварительно создан и проверен
omp --config .omp/profiles/research.yml --approval-mode write

# Уже утверждённая ограниченная задача; никакого implicit paid fallback
omp --config .omp/profiles/implementation.yml -p --mode json --wait-async --max-time 45m --warn-cost 3 --max-cost 5 --no-title "Execute the approved qualification slice; stop at acceptance or blocker"

# Просмотр и осознанное продолжение interrupted TUI session
omp --config .omp/profiles/implementation.yml --restore <session-id-or-path>

# Release: независимое чтение, исполняемые checks отдельно у Lead
omp --config .omp/profiles/release.yml --approval-mode always-ask
```

Эти команды documented и синтаксис сверялся с `omp --help`; сами сценарии не запускались. Overlay schema/policy, structured tasks, Windows isolation, cancellation и recovery — **UNKNOWN до E01–E06/E10**. Включать автономный профиль только после PASS, иначе supervised OMP с одним writer.

## 9. Capability checklist: функция → проверка → fallback

Описание/конфигурация/границы — DOCUMENTED в [A evidence](findings/a-harness.md) и bundled docs в local ledger. Ни одна будущая проверка ниже не объявляется выполненной.

| Функция: что даёт / нужна ли | Включение / граница | Как квалифицировать | Если отсутствует или ненадёжна |
|---|---|---|---|
| task/batch: blank-context workers; да | batch=true, complete shared context + per-item brief | E02: 3 результата с identity/overlap | один worker/inline Lead |
| Async: parent продолжает работу; да | async.enabled=true, CLI wait-async; print иначе отменяет jobs | E01/E02 delivery и exit | synchronous run с тем же timeout |
| Structured results: машинный contract; после E02 | structured=true, outputSchema, strict; permissive не acceptance | E02 malformed/schema-invalid case | plain evidence report, manual validation |
| Agent Hub: live roster/control; да в TUI | Alt+A, focus/transcript/revive/kill | E02/E06: observed model/state и cancel | proc/history/JSON events, оператор |
| Persistent/parked children: reuse контекста; да | idle TTL420000, message agent://; не perpetual process | E06 idle→park→revive без потери AC | fresh worker с durable brief |
| /vibe: director с persistent workers; нет baseline | /vibe TUI-only, исключает plan/goal и ряд session operations | отдельный E02/E06 variant, если потребуется | обычные task; не RPC-wrapper вокруг vibe |
| Agent Skills: task instructions по потребности; позднее | .omp/skills/name/SKILL.md; body on demand | discovery+вызов на безопасной задаче, inventory writes | короткий явный brief без skill |
| Custom Agents: tool/model defaults; не нужны сейчас | .omp/agents/name.md, frontmatter; additive tools остаются | E02 discovery/source precedence | bundled agents + explicit context |
| Model Roles: workload routing; да | modelRoles; defaults, plan/task/smol/advisor; roles не запускают modes сами | E09 actual resolved route/effort | exact current selector, fail closed |
| Per-call routing: модель на item; нет baseline | off/eval/on + grants; project не может выдать новые grants, override conflict | E09 identity/revival, no hidden fallback | agentModelOverrides/role overlay |
| Advisor: дополнительная critique; эпизодически | enabled + advisor role; strict backlog может ждать без cap | E05 usefulness vs requests, no mutating tools | fresh reviewer по milestone |
| /review: review prompt; да с явным лимитом | сам command не reviewer executor; возможен fan-out до16 | E05 seeded defects; явно максимум2 reviewers | direct bounded reviewer task |
| scout: read-only exploration; да | bundled, exact model override; не OS sandbox | E02 sources/counterexamples | Lead targeted reads |
| sonic: механика; да условно | bundled, @smol/override, не сложный design | E09 bounded diff+review | task на сильной модели |
| reviewer/security-reviewer: независимые lenses; да | bundled, read-only contract, отдельные contexts | E05 repro/false positives/security boundaries | Lead gates + явно потерянная независимость |
| seance: consult старой session; по нужде | sourceSession, saved model либо explicit; source не меняется | historical known fact без writes/контаминации | durable handoff, без притворного восстановления памяти |
| Hooks/Extensions: runtime integrations; нет baseline | code-bearing TS/JS, hooks через extension runtime; in-process | отдельный reviewed fixture, load/error/cancel | штатные tools/CI, не свой orchestrator |
| MCP: внешние tools; optional | reviewed .omp/mcp.json, exact per-tool policy/timeout | E10 metadata+deny mutation/cancel/logs | отключить сервер; native tools/manual visual work |
| CLI/RPC/ACP: automation/host integration; CLI да | print JSON; RPC не JSON-RPC; native omp acp | E01/E08 completion, stdout drain, cancel, resume | TUI/CLI, без второго bridge |
| Isolation/integration: отдельные изменения; после PASS | enabled + per-item isolated + apply=false | E03/E04 parent untouched/conflict/combined AC | single writer/manual integration |
| Compaction/context: долгие runs; да | enabled, thresholds default, durable AC вне summary | E06 /compact→следующее правильное действие | bounded slices, fresh session+handoff |
| Resume/restore: restart recovery; да после PASS | --resume история; --restore TUI interrupted work | E06 unknown outcomes и process reconciliation | supervised resume, сверить состояние вручную |
| Errors/hangs/cancel/budgets: bounded autonomy; обязательно | child/parent caps, retries3, explicit blocker | E06/E10 timeout/quota/failure/cancel | stop+operator, не бесконечный retry/fallback |
| Approval/safety/Windows: controlled execution; обязательно | explicit tool policies + OS boundary; native x64 не WSL prerequisite | E10 плюс E01/E03 paths/CRLF/process cleanup | supervised native OMP, никакой ложной sandbox-гарантии |

