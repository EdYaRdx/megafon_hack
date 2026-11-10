# Рекомендация и порядок настройки

Срез:2026-11-10. **Решение: OMP-only + минимальный workflow + существующий Codex OAuth.** Никаких установок/изменения global config в этом исследовании. Это исследованный configuration blueprint и план испытаний, не готовая квалифицированная автономная система.

## Executive summary

1. OMP18.18.6 уже установлен; default `openai-codex/gpt-6.1-sol:high`. Native task/async/persistent children/Hub/roles/CLI/RPC/ACP покрывают основную development coordination. [VERIFIED metadata, DOCUMENTED capabilities](findings/local-environment.md).
2. Сейчас опасно включать unattended: yolo, isolation off, runtime/cost limits отсутствуют; task children принудительно yolo даже при более строгом Lead mode. Worktree и approvals не sandbox. [Configuration](omp-configuration.md).
3. **OpenClaw не нужен сейчас.** Его доказанная добавка — Gateway/внешние события/расписания/каналы, не лучшее coding качество. OpenClaw→OMP ACP E2E UNKNOWN; не заменять этим фактом поддержку протокола. [Варианты](architecture-options.md).
4. **Не устанавливать Spec Kit и OpenSpec сейчас.** Сначала native contract→vertical slices→independent review→fix/re-review→integration smoke. Если нужен формальный SDD, первым квалифицировать Spec Kit1.3.3; OpenSpec1.17.0 — альтернатива для change-heavy brownfield. Сайт Spec Kit описывает unreleased adapter options: pin release. [Сравнение](comparison.md), [B evidence](findings/b-workflow.md).
5. Ролевое распределение — сильный Codex Lead/Developer, квалифицируемый быстрый worker, условный Copilot Sonnet reviewer. Альтернативная модель/семейство сейчас не вызваны: billing regime/overage UNKNOWN. Plus не API credits; OMP prices не стоимость Copilot подписки. [Models](model-routing.md).
6. OpenDesign optional для конкретных visual deliverables; MCP connection сейчас FAILED. Council/OptiLLM/BMAD/Superpowers/OpenHands/DSH/custom Agent Platform **не включать в baseline**: дополнительная runtime/process/security поверхность без доказанного выигрыша.

## Инструменты по режимам

| Режим | Что включать | Что не требуется |
|---|---|---|
| Исследование | native read/grep/glob/web_search/task/todo, до3 scout | MCP, plugins, scheduler, memory service |
| Реализация после qualification | edit/write/bash/LSP/browser по стеку; ≤2 isolated writers, Lead integration | second orchestrator, persistent professional-role swarm |
| Независимая проверка/release | reviewer/security-reviewer, deterministic gates, actual CLI/API/UI smoke на clean snapshot | self-reported done как acceptance; automatic patch apply |
| По конкретной нужде | один SDD package, OpenDesign, episodic advisor; OpenClaw лишь trigger/channel requirement | установка «на всякий случай» |

Skills: изначально0 новых. После появления повторяемой acceptance procedure — один project-local skill, без собственного framework. MCP: обязательных0, не дублировать filesystem/GitHub/browser tools. Extensions/Hooks:0 новых; code-bearing plugins выполнять как user-trusted code, не считать security policy. Seance — для конкретного historical context, sonic — механические изменения, не архитектурные решения.

## Оптимальные стартовые settings

Рекомендация, не benchmark optimum: batch/async=true; maxConcurrency3; workerThreads4 оставить (workers включаются только от9); recursion1; perCallModel off; agent overrides явные; child runtime20–30min; soft budget60 research/100 implementation; structured strict после E02; isolation enabled + **isolated:true у каждого writer** после E03; apply=false, patch merge. Lead approval write/explicit execution policies, OS-restricted workspace до unattended. Advisor/prewalk/extra memory off; fallback fail closed; parent max-time45min + wait-async. Полная current→recommended матрица, YAML model roles и launch commands: [omp-configuration](omp-configuration.md).

## Пошаговый план последующей настройки

Все шаги ниже — **будущие**, не выполнены.

1. **Согласовать выполнение qualification, не продукта.** Начать с disposable CSV fixture и existing subscription route. Выделить no-overage boundary; никаких новых subscriptions/API без доказанной потребности.
2. **Зафиксировать окружение.** OMP18.18.6/runtime/binary hashes; rollback binary и sanitized config/session backup. Отключить auto-update только в будущих overlays; не обновлять посреди квалификации. Bun/uv/Python/Docker не ставить без выбранного компонента.
3. **Создать project-local overlays из blueprint.** research/implementation/release, без global changes/auth migration. Новый сеанс читает `cfg://` для provenance; убедиться, что загружена требуемая schema и deny/prompt policy.
4. **Проверить permissions до автономии.** E10 preflight с canary/fake secret, child-yolo, eval/MCP escape paths. Для unattended — restricted OS account/VM/ACL и no private home credentials. При неудаче supervised один writer.
5. **E01–E02:** один end-to-end CLI slice; затем3 read-only parallel slices+strict schema. Наблюдать Hub/events, runtime, usage, actual smoke.
6. **E03–E04:** два isolated writers на Windows rcopy, retained patch, manual Lead integration, conflict handling и full combined AC. До PASS не писать параллельно в общий checkout.
7. **E05–E06:** blind review/fix/re-review, cancel, crash/resume/restore/compaction с unknown outcome reconciliation. Утверждение о recovery только для испытанных путей.
8. **E09:** billing/entitlement Copilot, затем same-task quality/tool/schema/latency comparison. Different-family reviewer только после доказанного существующего allowance без uncertain charges. Paid Polza/API — отдельное решение.
9. **E07 при необходимости:** один pinned Spec Kit vs OpenSpec vs native baseline. Выбрать ровно один, если лучше качество/traceability/recovery при приемлемом overhead. Native baseline побеждает при равенстве.
10. **CI/release contract:** после будущего ТЗ определить stack-specific gates и clean runner. Release из product-only checkout без .omp/MCP/auth; проверять реальные пользовательские сценарии, обработку ошибок и переносимость.
11. **Опциональные сервисы:** OpenDesign сначала connection/security/read-only metadata, затем visual qualification; OpenClaw только при реальном trigger и PASS E08. Не включать их в critical build chain.
12. **Остановить инфраструктурную работу** после admission gates; получить полное конкурсное ТЗ и только по отдельной задаче начинать Contest Product.

## Риски и открытые вопросы

| Вопрос / риск | Текущий статус | Как закрыть / влияние |
|---|---|---|
| Полное конкурсное ТЗ/формат запуска/сроки | UNKNOWN | Определит product runtime и CI; сейчас не проектировать конкурсного агента |
| Реальная model entitlement и Copilot billing | UNKNOWN; quota report/catalog VERIFIED | E09 zero-overage gate; пока Codex only |
| Windows isolation/merge/kill/recovery | DOCUMENTED, не квалифицировано | E03/E04/E06; single writer fallback |
| Полноценная host isolation/secrets protection | Не обеспечивается native approvals | E10+OS boundary; без этого только supervised |
| OMP version/main drift | Есть documented расхождения и moving sources | Фиксировать installed18.18.6/source SHA, перепроверить перед изменениями |
| Polza Sol tools/Responses semantics | UNKNOWN interoperability | Paid approval+E09; не скрытый fallback |
| OpenDesign daemon | FAILED connection | Опциональная диагностика, не блокер baseline |
| OpenClaw ACP tree cancel/resume | UNKNOWN | Только условный E08 |
| Docker engine/WSL/Python/Bun PATH | Не доказана готовность | Не вводить ненужные runtime dependencies |
| Review independence | Fresh-context same family доступен; different family не проверена | Явное ограничение, не симулировать diversity |

## Первый конкретный следующий шаг

**Отдельная задача на E10 preflight и E01 в disposable fixture:** создать reviewed local overlays и синтетический CSV contract, проверить existing Codex allowance и безопасные permissions, затем один bounded run. Без OpenClaw/новых API/contest code. До разрешения выполнения ничего не устанавливать и настройки не менять.

## Навигация и доказательства

[Comparison](comparison.md) · [Architecture](architecture-options.md) · [OMP blueprint](omp-configuration.md) · [Model routing](model-routing.md) · [10 experiments](experiments.md) · [Independent review](review.md).

Исследовательские findings сохраняют exact sources, версии и статусы; рекомендации не повышают DOCUMENTED до VERIFIED. Практические квалификационные результаты появятся только после исполнения отдельной фазы.
