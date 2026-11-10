# Сравнение инфраструктурных проектов

Проверено 2026-11-10. **DOCUMENTED** ниже означает источники/реализацию, а не успешную интеграцию. Рекомендации — архитектурный выбор. Полные ссылки, SHA, версии и ограничения в findings: [A](findings/a-harness.md), [B](findings/b-workflow.md), [C](findings/c-models-tools.md), [local VERIFIED/FAILED](findings/local-environment.md). Moving main не равен release; даты feed/UI не унифицируются без доказательств.

| Проект / наблюдавшаяся версия | Полезная возможность | Существенная граница | Выбор |
|---|---|---|---|
| [OMP 18.18.6](https://github.com/can1357/oh-my-pi/releases/tag/v18.18.6) | Task/async, persistent sessions, Hub, roles, native ACP/RPC, isolation | Children yolo; isolation не sandbox; headless lifecycle требует wait-async | **Основной harness**; версия VERIFIED локально |
| [OpenClaw 2026.11.3](https://github.com/openclaw/openclaw/releases/tag/v2026.11.3) | Always-on Gateway, schedules/events, remote channels | OMP custom acpx argv, E2E UNKNOWN; внешний harness вне sandbox; двойной lifecycle | **Не ставить сейчас**; только для реального внешнего trigger |
| [DeepSeek Harness 0.2.2-rc.1](https://github.com/deepseek-ai/deepseek-harness/releases/tag/dsh-v0.2.2-rc.1) | Cordis plugins, document/UI, SDK/ACP | Preview; ACP session/load отсутствует; master далеко от RC | Не менять working OMP; альтернативный harness по конкретной нужде |
| [OpenHands / Agent Canvas 1.38.0](https://github.com/OpenHands/OpenHands/releases/tag/v1.38.0) | UI/control plane, container/remote agent workspaces | Уже не прежний монолит; Docker/WSL/runtime qualification | Не нужен baseline |
| [OpenHands SDK 1.61.0](https://github.com/OpenHands/software-agent-sdk/releases/tag/v1.61.0) | Python/REST agents, persistence, delegation, structured FinishTool | Python≥3.12; версии tools/workspace/server согласовывать; Windows multi-container через WSL2 | Только если нужен programmatic container runtime |
| [Agent Platform](https://github.com/EdYaRdx/agent-platform) / local ref `1382b30` | Board/budgets/evidence/recovery principles | Public URL FAILED 404; local qualification gate пуст; прежний pilot не unattended proof | Заимствовать принципы, **не код control plane** |
| [Spec Kit 1.3.3](https://github.com/github/spec-kit/releases/tag/v1.3.3) | OMP integration `omp`, требования→plan→tasks→converge | Python/uv; tests optional; сайт уже описывает unreleased adapter flags | Первый formal SDD кандидат, только после E07 |
| [OpenSpec 1.17.0](https://github.com/Fission-AI/OpenSpec/releases/tag/v1.17.0) | OMP target `oh-my-pi`, delta specs/change tasks/archive | Verify optional; skills/commands migration к 2.0; global profile effects | Альтернатива для изменяющегося brownfield |
| [BMAD 6.12.4](https://github.com/bmad-code-org/BMAD-METHOD/releases/tag/v6.12.4) | Discovery/PRD/architecture/review lifecycle | Pi target не доказательство OMP; много process state; v7 alpha отдельно | Не устанавливать для хакатона |
| [Superpowers 7.0.2](https://github.com/obra/superpowers/releases/tag/v7.0.2) | TDD, fresh review, scoped fixes/re-review, handoff | Pi package API другой; SDD запрещает parallel implementers; OMP UNKNOWN | Заимствовать практики, не ставить bootstrap |
| [OpenDesign 0.27.1](https://github.com/nexu-io/open-design/releases/tag/open-design-v0.27.1) | Visual workspace, preview/export, MCP | Local MCP FAILED disconnected; write/delete/login tools; некоторые skills catalogue-only | Опционально под конкретный visual deliverable |
| [OptiLLM 0.4.1](https://github.com/algorithmicsuperintelligence/optillm/releases/tag/v0.4.1) | Inference-time reasoning techniques | Многократные upstream calls, tool/schema loss, Responses route не найден; debug Bearer logging в source | Не проксировать baseline coding loop |
| [Council 1.2.0](https://github.com/0xNyk/council-of-high-intelligence/releases/tag/v1.2.0) | Blind positions→cross-exam→Chairman | Main 38 commits ahead; simulated seats; detector не auth proof; большие call multipliers | Не ставить; точечный blind review средствами OMP |

## Workflow: окончательный выбор

**Сейчас — минимальный OMP workflow, без дополнительного spec package.** После конкурсного ТЗ: один contract с наблюдаемыми AC, один walking skeleton, затем 2–3 vertical slices, independent review, fix, scoped re-review, integration smoke, stop. Не два task ledgers.

**Spec Kit vs OpenSpec:** для нового проекта с несколькими стабильными требованиями первым квалифицировать Spec Kit; для частых компактных изменений существующей системы — OpenSpec. В E07 сравнить оба с native baseline; установить **один** только если он улучшит traceability/recovery/качество, а не число Markdown. [Официальная OMP integration](https://github.github.com/spec-kit/integrations/omp.html) реально существует, но site/main flags не переносить на pinned 1.3.3. Ни один framework не обеспечивает независимую приёмку автоматически.

## Optional tools: что дублируется

OMP task уже даёт execution fan-out и сбор результатов; Council добавляет debate protocol для одной decision boundary, не новый необходимый executor. OMP reviewer/advisor уже дают critique; OptiLLM добавляет upstream generations и proxy risk, а не гарантированное качество. Native browser/Mermaid/SVG достаточно для обычных материалов; OpenDesign нужен только когда его реальный visual workflow лучше. OMP native tools/LSP не требуют filesystem/GitHub/browser MCP-дубликатов.

## Стоимость архитектур

У OMP-only — текущая подписочная квота и время интеграции. OpenClaw добавляет Gateway uptime, обновления, логирование/секреты, plugins/acpx и дополнительные orchestration prompts. DSH/OpenHands добавляют второй agent runtime и qualification surface. Точные денежные operating costs UNKNOWN без deployment plan и измерений; бесплатная open-source лицензия не означает бесплатную эксплуатацию.
