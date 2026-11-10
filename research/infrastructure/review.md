Дата ревью: 2026-11-10. Read-only reviewer; сохранено Lead без изменения вердикта.

# Независимое ревью инфраструктурного исследования

## Вердикт

**Исследование принято после исправления одной подтверждённой находки P1. Открытых подтверждённых дефектов не осталось.** Рекомендация OMP-only соразмерна задаче; материалы не выдают configuration blueprint за квалифицированную автономную систему.

**Overall correctness:** correct.  
**Уверенность:** 0.91.

Это вердикт **на исследование**, не на runtime qualification. E01–E10 остаются планируемыми испытаниями.

## Scope и выполненные проверки

Прочитаны полностью все десять заданных документов:

- recommendation.md, comparison.md, architecture-options.md;
- omp-configuration.md, model-routing.md, experiments.md;
- findings/local-environment.md, a-harness.md, b-workflow.md, c-models-tools.md.

Проверены согласованность рекомендаций, настройки и границы безопасности, model routing, recursion, isolation/recovery, Windows, цены и no-paid boundaries, версии/идентичность источников, полнота E01–E10.

**Охват13 проектов присутствует:** OMP, OpenClaw, DeepSeek Harness, OpenHands/Canvas, OpenHands SDK, Agent Platform, Spec Kit, OpenSpec, BMAD, Superpowers, OpenDesign, OptiLLM, Council.

Основные результаты:

- Capability checklist OMP содержит назначение, способ включения, ограничения, qualification и fallback.
- Current и recommended settings разделены; неприменённые настройки не объявлены VERIFIED.
- Child-yolo, additive MCP/extensions, ограничения shell-only правил и отсутствие OS sandbox описаны явно.
- Routing precedence и recursion boundary согласованы с pinned source; recursion1 запрещает task-spawn на первом дочернем уровне.
- Наличие Windows binaries не приравнено к готовности Docker/Python/WSL/isolation.
- Подписки, API billing, catalog estimates и cached quota не смешаны; неизвестные Copilot entitlement/overage блокируют альтернативные вызовы.
- Во всех E01–E10 присутствуют prerequisites, действия/команды, PASS/FAIL, метрики, evidence и decision. E08 корректно оставлен условным.
- Буквальных truncation/omission markers в сохранённых findings не найдено. Длинные строки прочитаны через `:raw`; конец A findings присутствует.

Файлы не изменялись. Установки, config changes, inference/API probes, логины, push, build/tests/formatters не выполнялись.

## Подтверждённый дефект и closure

### P1 — Повторно передавайте утверждённые настройки при headless recovery

**Путь:** `research/infrastructure/experiments.md:90`.  
**Уверенность:** 0.99.  
**Статус:** исправлен; scoped re-review PASS по тексту.

**Initial:** первоначальная команда E06 запускала `omp --resume ...` без approved `--config` и исходных cost flags. Возобновление истории не восстанавливает process-local overlays. Поэтому recovery терял ограничения профиля — существенно при зафиксированных текущих настройках `yolo`, concurrency32, выключенной isolation и включённом model fallback.

**Доказательства:**

- [OMP18.18.6 settings.md:13–25](https://github.com/can1357/oh-my-pi/blob/v18.18.6/docs/settings.md#L13-L25): CLI overlays и runtime overrides не сохраняются.
- [main.ts:1968–2000](https://github.com/can1357/oh-my-pi/blob/v18.18.6/packages/coding-agent/src/main.ts#L1968-L2000): новый процесс получает overlays из текущего `parsedArgs.config`, cost limits — из текущих launch arguments.

**Fixed:** Lead добавил абсолютный approved overlay, fixture cwd, cost guards, `--no-title`, проверку effective policy/provenance до работы и предупреждение о невосстановлении launch controls.

Исправленная строка прочитана полностью. Дополнительное предупреждение в `research/infrastructure/omp-configuration.md:131` согласовано с E06. **Дефект закрыт статически; runtime recovery не запускался.**

## Scoped re-review дополнительных правок

- **E08:** candidate argv JSON и custom session commands имеют оговорку moving-main/not-pinned/UNKNOWN. Пример согласуется с прочитанной acpx documentation, но не выдаётся за подтверждённую поддержку backend0.19.4.
- **`omp-configuration.md:143`:** current/recommended worktree lifecycle разделены; автоматическое удаление workspace не предлагается. `clone=false` ограничивает clone-first поведение, **не является sandbox или квалификацией task isolation**. Перенос ignored caches при включённом clone подтверждается [OMP18.18.6 CLI reference](https://github.com/can1357/oh-my-pi/blob/v18.18.6/docs/cli-reference.md#worktree-clones).

Новых подтверждённых дефектов в этих правках не найдено.

## Потенциальные риски и недостающие эксперименты

Это **не дефекты исследования** и не требование проводить запрещённые сейчас испытания.

1. **Windows isolation/cancel/recovery остаются UNKNOWN.** Документирование backend/lifecycle не доказывает работу в данной среде.
2. **OMP→acpx→OpenClaw E2E остаётся UNKNOWN.** Совместимость протоколов не доказывает completion, tree cancel, restart и result delivery.
3. **Межсемейный routing не квалифицирован.** Catalog IDs и cached quota не подтверждают entitlement, adapter interoperability или отсутствие доплат.
4. **Moving-source reproducibility ограничена.** Drift обозначен; перед будущими запусками нужны предусмотренные snapshots/hashes и проверка pinned help/schema.
5. **E01–E10 пока только планы.** Их отсутствие не препятствует завершению исследования, но запрещает объявлять unattended runtime готовым.

Эти ограничения уже отражены в материалах. Продуктовый код, установки и дополнительные orchestrators для принятия исследования не требуются.

## Источники независимых spot checks

Помимо локальных документов непосредственно прочитаны:

- [OMP18.18.6 task contract](https://github.com/can1357/oh-my-pi/blob/v18.18.6/docs/tools/task.md), [approval contract](https://github.com/can1357/oh-my-pi/blob/v18.18.6/docs/approval-mode.md), [restore semantics](https://github.com/can1357/oh-my-pi/blob/v18.18.6/docs/session-operations-export-share-fork-resume.md#cli---restore), settings и соответствующие участки source.
- [Spec Kit1.3.3 OMP adapter](https://github.com/github/spec-kit/blob/v1.3.3/src/specify_cli/integrations/omp/__init__.py): integration options действительно не добавляются в argv.
- [OpenSpec1.17.0 registry](https://github.com/Fission-AI/OpenSpec/blob/v1.17.0/src/core/config.ts#L83): отдельный `oh-my-pi` target существует.
- [Copilot billing](https://docs.github.com/en/copilot/concepts/billing-and-usage/individuals/billing) и [Sol specification/pricing](https://developers.openai.com/api/docs/models/gpt-6.1-sol): существенные приведённые тарифы и ограничения подтверждаются.
- [Polza Responses](https://polza.ai/docs/api-reference/responses/create.md): beta/stateless и преобразование в Chat Completions подтверждаются.
- [OptiLLM0.4.1 server.py](https://github.com/algorithmicsuperintelligence/optillm/blob/v0.4.1/optillm/server.py#L1009): debug-логирование Bearer присутствует.
- [acpx custom agents, moving main](https://github.com/openclaw/acpx/blob/main/docs/custom-agents.md): structured Windows argv и custom session commands документированы.

Это статические DOCUMENTED-проверки, не проверка выполнения интеграций.

## Реальная независимость и пределы

Ревью выполнено отдельным reviewer в свежем контексте, **той же модельной семьи**. Это независимость контекста и проверяющего, не multivendor/model-family review. Альтернативная модель не выбиралась: entitlement/overage неизвестны, платные расходы не разрешены.

Локальные VERIFIED-наблюдения Lead оценены как переданные evidence, а не повторены самостоятельно. Не каждая внешняя строка исследования независимо перепроверена; spot checks охватили существенные настройки, безопасность, pricing и protocol claims.

**Итог:** исследование завершено и пригодно как основание для отдельно разрешённой qualification-фазы. Runtime readiness этим ревью не установлена.

## Проверка целостности артефактов Lead

До сохранения этого отчёта выполнен локальный read-only анализ Markdown: все 10 ожидаемых исходных документов присутствуют, 10 разделов E01–E10, отсутствуют broken relative file links (review.md проверяется после сохранения) и буквальные truncation markers. Это проверка документов, не runtime qualification. CLI metadata smoke: omp --version/--help, models, usage --redact, acp --help; OpenDesign metadata call FAILED connect. Ни один E01–E10 не запускался.
