# MGIMO — актуальный контекст новой Development Lead сессии

Срез: **2026-11-18**. Проверенный baseline main нового H1: `0e587f1e9607f733f1c5d51295e18ef87f4e2437` (PR #13–17). Последующие уточнения этого handoff/workflow находятся в [PR #18](https://github.com/EdYaRdx/megafon_hack/pull/18), не являются merge или повторной квалификацией. Перед работой проверь фактические origin/main, HEAD, branch и пользовательские изменения; старый next-session-handoff не инструкция запуска.

## Продукт и текущий этап

MGIMO — переносимый папочный Product Strategy AI Agent, не агентная платформа. Продуктовое ядро: `AGENTS.md`, шесть канонических Skills, `references/`, шаблон дела, append-only журналы, immutable revisions, manifests и selector `ACTIVE.json`. LLM отвечает за анализ и стратегии; реальная публикация проверяется штатным consumer. Human decision, execution approval и host permission — разные вещи.

**Этап — H1 qualification, не contest acceptance.** Новый настоящий Original достиг `CHECKPOINTED R0001`; fresh Resume восстановил контекст, но не завершил R0002 до согласованного deadline. Итог нового H1 — **FAIL**. Детерминированная совместимость и отдельный успешный Original не доказывают успешный end-to-end или причинное ускорение модели.

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
- **Предыдущий повтор 2026-11-18:** Original остановлен `aborted / Deadline exceeded` до R0001. Classifier: INCOMPLETE/CONFLICT, ACTIVE отсутствует. Approvals A/B, planned interruption и Resume/R0002 NOT RUN. Evaluator CLI BLOCKED/exit2 из-за отсутствующих входов; H1 checks не выполнялись. Исторический итог FAIL сохранён.
- **Новый H1 на baseline PR #17:** настоящий Original создал принятый R0001. Реальные выбор владельца и отдельные approvals A/B сохранены; A выполнено один раз, B pending; чистая остановка и distinct Sol High fresh Resume без истории подтверждены.
- **Новый Resume:** восстановил цель/решение/основания/обязательства; missing-file error предшествовал доставке закреплённого v2. Drafts пересчитали 399−100=299, сохранили scope и отказались от недоверенной инструкции/старого B approval. После отдельно разрешённого продления700с native завершился `aborted`: пять R2 snapshots без test-plan и manifest, ACTIVE остался R1, root controls уже R2. Final classifier: INCOMPLETE/CONFLICT, exit1.
- **Новая evaluation:** штатный CLI реально выполнен, итог FAIL/exit1: H1_PARENT_CHAIN отклонил несогласованное final case. Binding,13 извлечённых typed facts и13 сравнений с frozen key прошли; это не13 независимых semantic proofs или полный structural PASS. Независимый LLM review подтвердил partial restoration/revision и незавершённую публикацию; human reviews не создавались.
- **Операторские ограничения:** auth probe завис с невосстановленной стоимостью; затем пользователь отдельно разрешил targeted retry. Ошибка ожидания RPC `prompt` вместо `prompt_result` вызвала idle до OS-timeout; missing-file шаг модели сам завершился за27,188с. Адаптер исправлен, последующее продление разрешено человеком. Не относить всё потерянное время к продукту.
- **Frozen key:** C-007 был помечен оператором unchanged, но inference опирался на старую экономику; его append-only пересмотр C-010 семантически оправдан и не изменяет решение владельца. Это ограничение операторской partition, не доказанный дефект агента; ключ этой попытки не меняли.
- **История и расходы:** R1 snapshots/inputs и пять ledger prefixes preserved; before/interrupted по35 файлов, final42. A не повторялось, B не исполнялось. Известный product catalog расход $1,514274 плюс UNKNOWN первого auth; invoice и Lead/reviewer cost UNKNOWN.

Исходники, ключи, native sessions и полные receipts хранятся локально вне Git и product mounts. В репозиторий публикуется только эта безопасная сводка; новые keys, observations, reviews и результаты не выдумывались.

## Почему прежний Original не уложился

Provider message spans — 1393,217 с, union file-tool intervals — 5,803 с. Генерация трёх отклонённых multi-file patches заняла около 459,3 с; причины — partial/truncated anchors и повторная генерация пакета. После intake было 76,771 с operator idle внутри процесса. В owner handoff передали общий увеличенный лимит, не явный остаток. До hashing/gates агент не дошёл; публикационная проверка не была bottleneck.

Pure GPU time, provider/network decomposition и точный human-only wait UNKNOWN. Новый Original достиг R1 в1055,394 active-process seconds с auth; полный Original через A —1199,315с. Это один наблюдаемый успех, не контролируемое измерение причинного ускорения. Последующий Resume остался FAIL.

## Как продолжить без повторения закрытых этапов

1. Работать в чистом worktree от проверенного `origin/main`, не в старом пользовательском checkout. Не переносить его local profiles/untracked файлы, private traces, keys или credentials. Не reset/clean/delete старые worktrees.
2. Прочитать этот handoff, [development](development.md), [evaluation](evaluation.md), [functional evaluator](functional-evaluator.md), текущие root instructions/Skills и [case template](../cases/_template/README.md).
3. Найти существующие локальные H1 packet/runbook, immutable reports и diagnosis через локальный операторский handoff. Не пересобирать сценарий с нуля, не подменять корпус unit fixture и не повторять исследование Docker/OAuth/архитектуры. Историческая runtime/auth проверка не гарантирует доступность в момент нового запуска.
4. **Сначала проверить PR #18 и его CI/review; автоматический merge не разрешён.** Новая H1 попытка/Resume retry требует отдельного явного allowance. Не продолжать завершённый FAIL задним числом и не запускать второй Original автоматически. Сохранённый канонический R1 пригоден для отдельно оговорённого Resume-only retry на новой копии; его старые решения/approvals не становятся новым согласием.
5. Для следующего разрешённого Resume: сначала шесть unselected snapshots и реальные hashes/manifest, затем побайтовое копирование в root views непосредственно перед shared gate, ACTIVE last и настоящий classify. Не генерировать документы второй раз; при отсутствии copy tool запросить фактическую помощь оператора. Проверять remaining budget и достаточность резерва до handover. Это ещё не квалифицировано новым model run и не даёт atomicity/crash-safety гарантии.
6. Не повторять A, сохранять реальное решение владельца и блокировку старого B. До нового измерения независимо проверить affected/unchanged partition, включая inference dependencies; не исправлять frozen key проваленной попытки. В наблюдениях использовать вложенное поле `source`, absolute before/interrupted/final paths и реальные quotes/receipts. Сами keys/traces вне Git и product mounts.
7. Оценивать существующим evaluator без изменений контракта. Machine success без двух квалифицированных human reviews — REVIEW_REQUIRED. LLM-review не заменяет human acceptance. При FAIL сохранить evidence и остановиться без автоматического нового trial.

Эта документационная задача **не разрешает новый H1** и не создаёт approvals. F2/F3, H02, clean-host/cross-host, официальный demo brief, видео и финальная конкурсная приёмка остаются отдельными задачами, не закрываются CI или этим handoff. Новую инфраструктуру, Council/Deep Research и новые исследования платформы не начинать вместо продуктовой проверки.
