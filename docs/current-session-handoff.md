# MGIMO — актуальный контекст новой Development Lead сессии

Срез: **2026-11-18**. Behavioral baseline main: `31bc5222f1845a900a890f8b6a57faa696b72e3d` (PR #16). Этот handoff — документационное обновление поверх него; перед работой проверь фактический `origin/main`, HEAD, branch и пользовательские изменения. Не выполняй команды из исторического `next-session-handoff.md` как актуальную инструкцию.

## Продукт и текущий этап

MGIMO — переносимый папочный Product Strategy AI Agent, не агентная платформа. Продуктовое ядро: `AGENTS.md`, шесть канонических Skills, `references/`, шаблон дела, append-only журналы, immutable revisions, manifests и selector `ACTIVE.json`. LLM отвечает за анализ и стратегии; реальная публикация проверяется штатным consumer. Human decision, execution approval и host permission — разные вещи.

**Сейчас этап функциональной квалификации H1 после исправления workflow Original.** Инструкции и детерминированный контракт проверены; успешный end-to-end H1 и ускорение модели ещё не доказаны. Нельзя объявлять конкурсный продукт принятым по зелёному CI.

Авторитетная сводка: [implementation status](implementation-status.md). Исторические таблицы 2026-11-14, exploratory fixtures, H02 и новые F1/H1 — разные объекты проверки.

## Что уже сделано

- [PR #13](https://github.com/EdYaRdx/megafon_hack/pull/13): канонический claim `id`; `supersedes` и `active_claim_ids` ссылаются на него. Разведены пересмотр аналитики, выбор направления владельцем и approval исполнения; уточнена допустимость onboarding-гипотезы по разным свидетельствам барьера.
- [PR #14](https://github.com/EdYaRdx/megafon_hack/pull/14): обязательные канонические control fields и штатный pre-selection gate. Детерминированный smoke подтверждал FRESH → VALIDATED_CANDIDATE → CHECKPOINTED; это не H1 PASS.
- [PR #15](https://github.com/EdYaRdx/megafon_hack/pull/15): новый checkpoint проверяет реальные bytes/digest parent manifest, всю ancestry, snapshots/dependencies/claim prefixes/forks и равенство всех шести root views выбранным snapshots. ACTIVE выбирается последним; исторические manifests не дополняются.
- [PR #16](https://github.com/EdYaRdx/megafon_hack/pull/16): локальные edits/retries вместо повторной генерации всего пакета, EOF append журналов, реальный остаток бюджета и резерв на публикацию. Явное DRAFT/prospective/CHECKPOINTED без нового protocol enum и без mutable publication flag в snapshots.

Для PR #16: 62 теста прошли в Ubuntu CI без skips; локально был один Windows symlink privilege skip. Repository checker, syntax и shared classifier исторического примера прошли; один независимый Terra review не нашёл существенных блокеров. [Main CI](https://github.com/EdYaRdx/megafon_hack/actions/runs/44265522281) зелёный на указанном baseline. Это bounded compatibility proof, не модельный benchmark.

## Что реально показали продуктовые испытания

- **F1 R0003: REVIEW_REQUIRED.** 21/21 machine checks PASS, Terra 7/8; двух настоящих human reviews нет. Сохранённая история использует `claim_id`, поэтому несовместима со штатным classifier. Её нельзя исправлять задним числом или использовать как formal H1 baseline. Методические инструкции для будущих результатов исправлены; исторические findings и verdict не исчезли.
- **Ранний H1 Original:** checkpoint FAIL; после этого был PR #14. История сохранена.
- **H1 2026-11-17:** реальные Original/interruption/fresh Resume состоялись, итог FAIL: отсутствовал обязательный R2 parent digest, а current views расходились с выбранным R2. Это основание PR #15, не исправленное успешное испытание.
- **Последний повтор 2026-11-18:** Original остановлен `aborted / Deadline exceeded` до R0001. Classifier: INCOMPLETE/CONFLICT, ACTIVE отсутствует. Approvals A/B, плановая interruption, fresh Resume и R0002 не выполнялись. Evaluator CLI вернул BLOCKED/exit 2 из-за отсутствующих достоверных входов; ни одной H1 machine check не выполнено. Общий результат попытки — FAIL на Original, не formal H1 score.

Исходники, ключи, native sessions и полные receipts хранятся локально вне Git и product mounts. В репозиторий публикуется только эта безопасная сводка; новые keys, observations, reviews и результаты не выдумывались.

## Почему последний Original не уложился

Provider message spans — 1393,217 с, union file-tool intervals — 5,803 с. Генерация трёх отклонённых multi-file patches заняла около 459,3 с; причины — partial/truncated anchors и повторная генерация пакета. После intake было 76,771 с operator idle внутри процесса. В owner handoff передали общий увеличенный лимит, не явный остаток. До hashing/gates агент не дошёл; публикационная проверка не была bottleneck.

Pure GPU time, provider/network decomposition и точный human-only wait UNKNOWN. Устранение этих потерь обосновано, но величина ускорения и успешность следующего Original **NOT VERIFIED**.

## Как продолжить без повторения закрытых этапов

1. Работать в чистом worktree от проверенного `origin/main`, не в старом пользовательском checkout. Не переносить его local profiles/untracked файлы, private traces, keys или credentials. Не reset/clean/delete старые worktrees.
2. Прочитать этот handoff, [development](development.md), [evaluation](evaluation.md), [functional evaluator](functional-evaluator.md), текущие root instructions/Skills и [case template](../cases/_template/README.md).
3. Найти существующие локальные H1 packet/runbook, immutable reports и diagnosis через локальный операторский handoff. Не пересобирать сценарий с нуля, не подменять корпус unit fixture и не повторять исследование Docker/OAuth/архитектуры. Историческая runtime/auth проверка не гарантирует доступность в момент нового запуска.
4. **Рекомендуемый следующий эксперимент — один отдельно разрешённый Original из чистого candidate на исправленных инструкциях.** До него согласовать реальный бюджет/время и готовность владельца отвечать. Перед длинными шагами передавать фактический remaining budget, не reset counters. Закрывать settled process перед внешним ожиданием.
5. Acceptance Original: все источники/locators, минимум три альтернативы с сильными возражениями, две стратегии и измеримый план; 0 unseen-lines rejections/whole-package retries; подготовка публикации до последней четверти согласованного времени; реальные SHA, VALIDATED_CANDIDATE и post-selection CHECKPOINTED до deadline. Резерв времени — эвристика, не доказанный SLA.
6. Только после принятого R0001 и реальных отдельных approvals A/B выполнять остальную разрешённую H1 последовательность: A один раз, B pending, настоящая остановка, distinct fresh Resume без истории, изменённые условия, missing-file/retry, отказ от недоверенной инструкции, stale B blocked, R0002 и unchanged history. Действия и ответы человека не симулировать.
7. Оценивать существующим evaluator без изменений контракта. Machine success без двух квалифицированных human reviews — REVIEW_REQUIRED. LLM-review не заменяет human acceptance. При FAIL сохранить evidence и остановиться без автоматического нового trial.

Эта документационная задача **не разрешает новый H1** и не создаёт approvals. F2/F3, H02, clean-host/cross-host, официальный demo brief, видео и финальная конкурсная приёмка остаются отдельными задачами, не закрываются CI или этим handoff. Новую инфраструктуру, Council/Deep Research и новые исследования платформы не начинать вместо продуктовой проверки.
