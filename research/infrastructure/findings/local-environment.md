# Локальные наблюдения и границы доказательств

Проверка: 2026-11-10. Исследование, не квалификация автономной разработки. Глобальные настройки не изменялись; сервисы не устанавливались, аккаунты не подключались, платные inference-вызовы отдельно не запускались. Исследовательские subagents используют существующий OMP и его квоты.

## Статусы

- **DOCUMENTED** — прочитана документация/реализация; не доказана работоспособность в этой среде.
- **VERIFIED** — выполнено конкретное действие, наблюдался указанный результат; статус не распространяется на соседние функции.
- **CLAIMED** — заявление автора/поставщика без достаточной технической проверки.
- **UNKNOWN** — данных недостаточно. **FAILED** — конкретная попытка завершилась ошибкой.
- Рекомендации и численные бюджеты — архитектурные решения, не benchmark-результаты.

## Практически наблюдалось

| ID | Действие / источник | Результат | Статус / граница |
|---|---|---|---|
| L01 | `omp --version`; `omp --help` | `omp/18.18.6`; CLI содержит `--restore`, `--wait-async`, `--max-time`, `--warn-cost`, `--max-cost`, `acp` | VERIFIED только версия/наличие CLI, не выполнение сценариев |
| L02 | `read cfg://`, `cfg://:651-731`; `cfg://modelRoles` | `default: openai-codex/gpt-6.1-sol:high`, источник global config; все остальные role assignments отсутствуют | VERIFIED effective settings |
| L03 | `cfg://task/maxConcurrency` и `cfg://task` | concurrency=32 (default), workers=4, batch=true, async=true, recursion=2, structured=false, perCallModel=off, maxRuntimeMs=0, softRequestBudget=200 | VERIFIED значения, не нагрузочная проверка |
| L04 | `cfg://tools/approvalMode`, `cfg://tools`, `cfg://task`, `cfg://secrets` | yolo (default), approval={}, restrictedFolders=[], isolation.enabled=false/apply=true/merge=patch; secrets.enabled=false | VERIFIED; не считать безопасным unattended-профилем |
| L05 | `omp usage --redact --no-extensions` | 1 Codex account, plan plus; 5h 2%, 7d 19%; 1 Copilot account, premium 0/200 monthly | VERIFIED отображение cached quota snapshot (возраст около 2–5 минут), не гарантии биллинга или model entitlement; проценты быстро устаревают |
| L06 | `omp models openai-codex --no-extensions` | 8 catalog rows; gpt-6.1-sol: context 500K, max-out 128K, low/medium/high/xhigh/max | VERIFIED каталог; серверный приём максимального контекста UNKNOWN |
| L07 | `omp models github-copilot --no-extensions` | 90 catalog rows, в т.ч. claude-sonnet-4.6, claude-haiku-4.5, claude-opus-4.6 и более новые семейства | VERIFIED каталог; каждый inference route UNKNOWN, не основание для автоматического fallback |
| L08 | `write xd://mcp__open_design_list_projects {}` | `MCP server not connected: open-design`, stage connect, retryable yes | FAILED текущая связь; прежний timeout не перезапускали для подтверждения |
| L09 | безопасная JSON-проекция `~/.omp/agent/mcp.json` | единственный server open-design, stdio, node.exe, 2 arguments, timeout/enabled не заданы | VERIFIED registration; args/env/credentials не экспортировались |
| L10 | PowerShell `Get-Command` и version commands | Node 24.19.0; Git 2.55.0.windows.5; gh 2.103.3; Windows PowerShell 5.1.26100.9711; Docker CLI 29.7.2 | VERIFIED binaries, Docker engine/WSL2/containers НЕ проверялись |
| L11 | `Get-CimInstance Win32_ComputerSystem` | 16 logical processors; около 15.3 GiB RAM | VERIFIED; основание ограничить реальные одновременные сборки |
| L12 | `Get-Command bun,pwsh,python` | bun/pwsh не найдены в проверенном PATH; python.exe указывает WindowsApps alias | VERIFIED discovery; рабочий Python interpreter UNKNOWN, alias не доказательство runtime |
| L13 | repo root `read .` | README.md, .gitattributes, .git; project-local .omp отсутствует | VERIFIED исходное состояние; продукт не реализовывался |
| L14 | текущая сессия и batch `task` с 3 scout | запущены три исследователя, результаты сохранены Lead отдельно | VERIFIED запуск; это не сценарий parallel writing/isolation/integration |

Первый комбинированный PowerShell version-запрос не выполнился из-за интерполяции `$` внешним shell; повтор через аргументный Bun subprocess дал L10–L11. Не свидетельствует о неисправности Windows/OMP.

## Остальные текущие значения

`advisor.enabled=false`; `task.enableLsp=false`; `task.enableEffort=false`; `task.agentModelOverrides={}`; `task.perCallModelAllow=[]`; `task.agentIdleTtlMs=420000`; `task.speculativeLaunch=true`; `task.completionProbe=true`; `task.softRequestBudgetNotice=true`.

`compaction.enabled=true`, `asyncEnabled=true`, `midTurnEnabled=true`, `autoContinue=true`, `keepRecentTokens=20000`, `thresholdTokens=-1`, `thresholdPercent=-1`, `reserveTokens=null`, `methodOrder=[remote,snapcompact,handoff,shake,soft]`, experimentalContextManagement=false. `memory.backend=off`, `memories.enabled=false`, `autolearn.enabled=false`, `autoResume=false`, `plan.defaultOnStartup=false`, `goal.continuationModes=[interactive]`.

`retry.maxRetries=10`, `retry.maxDelayMs=300000`, `retry.fallbackChains={}`, `retry.modelFallback=true`, `retry.usageAwareFallback=false`, `retry.waitForUsageReset=false`. `session.maxCost=null`, `session.warnCost=null`, `tools.maxTimeout=0`. `providers.cacheWarming=idle`, cacheRetention=auto; provider stream watchdogs=-1. `bash.gitGuard=false`, `bash.patterns=[]`; shellPath=Git Bash. `update.auto=true`, channel=stable. `mcp.startupTimeoutMs=250`, project config enabled. `collab.autoStart=off`; extensions=[]; disabledExtensions=[]; skills enabled with several discovery roots.

## Документация установленной версии (DOCUMENTED)

Снимок поставляемых документов прочитан через `omp://` при установленной 18.18.6. Публичные counterparts — [docs](https://github.com/can1357/oh-my-pi/tree/main/docs); main движется и не заменяет локальный снимок:

- [config-usage](https://github.com/can1357/oh-my-pi/blob/main/docs/config-usage.md): CLI overlay > project > global; env/runtime выше overlays. `.omp/config.yml`, `--config`, model roles в config.yml, provider definitions в user models.yml.
- [models](https://github.com/can1357/oh-my-pi/blob/main/docs/models.md): exact selectors; role comma-list — availability selection, НЕ runtime retry; retry.fallbackChains отдельно. Catalog costs — estimates.
- [task](https://github.com/can1357/oh-my-pi/blob/main/docs/tools/task.md): settings-dependent wire schema; structured strict/permissive; children force yolo; isolation opt-in per item; workers используются только начиная с 9 in-flight runs.
- [approval-mode](https://github.com/can1357/oh-my-pi/blob/main/docs/approval-mode.md): approvals не OS sandbox; restrictedFolders не парсят пути внутри shell/eval/MCP; tool denies сохраняются; неизвестный custom tool=exec, MCP tools=write независимо от annotations.
- [cli-reference](https://github.com/can1357/oh-my-pi/blob/main/docs/cli-reference.md): print default exits/cancels jobs; `--wait-async`; cost cap не отменяет in-flight перерасход.
- [compaction](https://github.com/can1357/oh-my-pi/blob/main/docs/compaction.md), [sessions](https://github.com/can1357/oh-my-pi/blob/main/docs/session-operations-export-share-fork-resume.md): compaction summary не полная память; restore interactive-only, unfinished tool outcomes могут быть unknown и повторяться.
- [vibe](https://github.com/can1357/oh-my-pi/blob/main/docs/vibe-mode.md): interactive-only, director не исполняет команды/правки; не замена headless orchestration.
- [MCP](https://github.com/can1357/oh-my-pi/blob/main/docs/mcp-config.md): request timeout по умолчанию 30000ms, discovery window 250ms — разные параметры. `OMP_MCP_TIMEOUT_MS` выше per-server timeout; 0 снимает deadline.
- [agents](https://github.com/can1357/oh-my-pi/blob/main/docs/task-agent-discovery.md), [skills](https://github.com/can1357/oh-my-pi/blob/main/docs/skills.md), [hooks](https://github.com/can1357/oh-my-pi/blob/main/docs/hooks.md), [extensions](https://github.com/can1357/oh-my-pi/blob/main/docs/extensions.md): code-bearing integrations выполняются in-process; agent tools lists не изолируют дополнительные MCP/extension tools.

Ни worktree isolation, ни crash recovery, ни ACP interoperability, ни доступ альтернативной модели здесь не объявляются VERIFIED.
