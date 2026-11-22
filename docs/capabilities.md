# Возможности и доказательства

Эта матрица сопоставляет реализованный процесс с проверяемыми артефактами. Она не прогнозирует конкурсный балл. Срез: основной main после PR32/33, дополненный финальным PDF и конкурсной навигацией; runtime/Skills не изменялись. Два независимых учебных кейса дают 11 альтернатив, четыре стратегии и два плана проверки.

[Финальный PDF со скриншотами](MGIMO_FINAL_REPORT.pdf) · [текущая readiness-проверка](release/submission-ready-20261122/README.md). В PDF, стр.15, объединённая строка «NEW и уточнение задачи» относится к видеокейсу и механизму создания. Более узкий статус свободного NEW без операторской помощи указан ниже; он не повышен до полноценного независимого E2E. Pinned CI релизного aa4b23f в PDF сохранён как исторический, [опубликованный PDF-релиз 3005460](https://github.com/EdYaRdx/megafon_hack/actions/runs/45060829339) и [актуальный main CI](https://github.com/EdYaRdx/megafon_hack/actions?query=branch%3Amain) доступны отдельно.

## Как читать статусы

| Статус | Значение |
|---|---|
| VERIFIED | Есть конкретный E2E, сохранённый результат или выполненный тест указанного механизма. Область подтверждения приведена в строке; это не универсальная гарантия |
| IMPLEMENTED_NOT_E2E_TESTED | Процедура/код существует, но самостоятельный живой сценарий целиком не подтверждён. Есть точный сценарий использования ниже |
| HOST_DEPENDENT | Результат зависит от модели, инструментов, permissions или телеметрии host. Это не утверждение о встроенной интеграции или одинаковой работе всех сред |
| NOT_IMPLEMENTED | Нет соответствующей продуктовой процедуры/движка/интеграции. Возможность общего LLM или инструмент разработки не объявляется функцией продукта |

Основные доказательства: [семейный видеокейс](video-e2e.md), [LinguaStep D0001](../cases/linguastep-retention/README.md), [release receipts](release/final-20261122/README.md), [unit receipt Windows](release/final-20261122/unit-tests.json), [CI основного main](https://github.com/EdYaRdx/megafon_hack/actions?query=branch%3Amain).

Исторический оригинал LinguaStep R0001 прошёл модельный workflow и подтверждённый владельцем Resume нового чата; [receipt](release/final-20261122/source-resume-receipt.json) — ограниченная неподписанная транскрипция реальных tool outputs. D0001 имеет новые hashes и отдельно проверенные байты; его file inventory не объявлен новым live Resume. Видеокейс также owner-reported; сохранённые D-ревизии — производные исходных R-байтов.

## Маршруты и продуктовый результат

| Функция / статус | Ценность и механизм | Конкретная реализация | Проверка и граница |
|---|---|---|---|
| NEW — IMPLEMENTED_NOT_E2E_TESTED | Из свободной задачи предложить отдельный путь, получить согласие и безопасно скопировать шаблон | [first-run: NEW и помощь оператора](../prompts/first-run.md), [intake](../.agents/skills/intake/SKILL.md), [case_workspace](../tools/case_workspace.py) | tests/test_case_workspace.py: test_new_case_copies_exact_template_and_remains_fresh_not_checkpointed, test_cli_reports_real_results_and_nonzero_stop. Свободный NEW→создание без помощи оператора не доказан независимым retention E2E: там case создал оператор; первый вход видеокейса описан владельцем |
| RESUME — VERIFIED | Вернуться к подтверждённому решению без полного прежнего чата; отдельно показать незавершённое | [resume-revise](../.agents/skills/resume-revise/SKILL.md), [case_protocol](../tools/case_protocol.py), [resume_context](../tools/resume_context.py) | [Настоящий новый чат исходного R0001](release/final-20261122/source-resume-receipt.json); tests/test_resume_context.py: test_clean_r1_confirms_exact_selector_and_six_snapshots_without_writes. Ожидаемые revision/hash были даны; это procedural restore, не blind discovery |
| REVISE — VERIFIED | Пересмотреть затронутые основания и сохранить прежнюю версию | [resume-revise](../.agents/skills/resume-revise/SKILL.md), [claim conventions](../references/evidence-and-claims.md) | [Изменения семейного D0003](../cases/family-multinumber-video/research/D0003/review.md), [поручение PO](../cases/family-multinumber-video/inputs/user-review-D0003.md). Подтверждён desk-пересмотр, не получение новых клиентских данных |
| HELP — IMPLEMENTED_NOT_E2E_TESTED | Объяснить запуск/возможности без чтения и создания дел | [first-run: HELP](../prompts/first-run.md) | Процедура явно задана; отдельный live HELP E2E не сохранён |
| Уточнение задачи — VERIFIED | Выяснить цель, адресата, ограничения и только существенные вопросы | [intake](../.agents/skills/intake/SKILL.md), [AGENTS](../AGENTS.md) | [Семейный scope](../cases/family-multinumber-video/inputs/user-scope.md), [LinguaStep brief](../cases/linguastep-retention/context/brief.md). Неизвестные ресурсы не заменены выдуманными ответами |
| Разные альтернативы — VERIFIED | Выбрать между разными механизмами, статус-кво и остановкой со сильными возражениями | [options-decision](../.agents/skills/options-decision/SKILL.md) | [Шесть семейных вариантов](../cases/family-multinumber-video/options.md), [пять LinguaStep](../cases/linguastep-retention/options.md). Не назначены выдуманные ROI/баллы |
| Выбор PO — VERIFIED | Отделить рекомендацию модели от решения человека | [AGENTS: recommendation gates](../AGENTS.md), options-decision | [Семейный выбор](../cases/family-multinumber-video/inputs/user-choice-D0002.md), [выбор B LinguaStep](../cases/linguastep-retention/inputs/owner-message-B-20261122.md). Последний — нормализованная транскрипция, не original message bytes |
| Две связанные стратегии — VERIFIED | Согласовать аудиторию, ценность, обещание и канал с выбранным механизмом | [strategy-communication](../.agents/skills/strategy-communication/SKILL.md) | [Семейная продуктовая](../cases/family-multinumber-video/strategy-product.md) / [коммуникационная](../cases/family-multinumber-video/strategy-communication.md); [LinguaStep продуктовая](../cases/linguastep-retention/strategy-product.md) / [коммуникационная](../cases/linguastep-retention/strategy-communication.md). Стратегии подготовлены; сообщения/пилоты не запускались |
| Экспериментальный план — VERIFIED | Заранее определить comparator, метрики/знаменатели, период, вред и действия после исходов | [experiment-design](../.agents/skills/experiment-design/SKILL.md), [metrics](../references/metrics.md) | [Семейный P0–P3](../cases/family-multinumber-video/test-plan.md), [план B](../cases/linguastep-retention/test-plan.md). Проверен дизайн, не выполнение эксперимента; неопределённые сроки/n/пороги остаются UNKNOWN |
| Пользовательский путь и отказы — VERIFIED | Сделать стратегию применимой: кто действует, что проверяет и что происходит при ошибке | strategy-communication; [семейная стратегия](../cases/family-multinumber-video/strategy-product.md) | Описаны отзыв прав, устаревший остаток, неподходящий тариф и неизвестный статус передачи. Это дизайн сценария по брифу, не UX-исследование существующего интерфейса |

## Источники, данные и качество вывода

| Функция / статус | Ценность и механизм | Реализация | Доказательство / граница |
|---|---|---|---|
| PDF и изображения документа — VERIFIED | Извлечь заданные факты с точной страницей и сверить визуально | Host render/view/OCR + [evidence-research](../.agents/skills/evidence-research/SKILL.md) | [Чтение 11-страничного брифа](../cases/family-multinumber-video/sources/S-001-reading.md), [PDF](../cases/family-multinumber-video/inputs/brief.pdf), activity A-004…A-016. Продемонстрирован Windows fallback, не универсальный PDF parser |
| Произвольные форматы/инструменты чтения — HOST_DEPENDENT | Использовать доступный reader/render; при отказе запросить читаемый экспорт либо признать пробел | [first-run](../prompts/first-run.md), evidence-research, [quickstart](quickstart.md) | Репозиторий не устанавливает PDF/OCR/XLSX engine; arbitrary XLSX E2E отсутствует. Изображение, доступное модели, не автоматически проверенный факт |
| Web research и атрибуция — VERIFIED | Открыть разрешённый первичный источник, указать точный раздел, дату и область применимости | evidence-research; [source conventions](../references/evidence-and-claims.md) | [Amplitude method snapshot](../cases/linguastep-retention/sources/S-003-amplitude-text.txt), S-003/E-006 и [исторический HTTP receipt](../cases/linguastep-retention/receipts/public-source-run-001.json). Методика не доказывает спрос или причины поведения |
| Доступ к сети — HOST_DEPENDENT | Проверить источник через инструменты host, не выдумывать чтение при отказе | evidence-research, security-and-source-handling | [HTTP reachability](release/final-20261122/external-links.json) не доказывает воспроизведение видео или доступ жюри |
| CSV и воспроизводимый расчёт — VERIFIED | Учитывать знаменатели, веса, периоды и пропуски; сохранить исполняемый расчёт и receipt | [metrics](../references/metrics.md), [расчёт под CSV](../cases/linguastep-retention/analysis/calculate_cohorts.py) | [Реальный replay экспорта](release/final-20261122/export-calculation-replay.json), [CSV](../cases/linguastep-retention/inputs/cohorts.csv). Скрипт рассчитан на конкретный fixture, не generic BI engine |
| Неизвестное/причинность — VERIFIED | Не превращать aggregate decline в диагноз; отделить observed/inference/hypothesis/unknown | evidence-research, metrics, options-decision | [LinguaStep decision](../cases/linguastep-retention/decision.md): 55→50%, оба сегмента +5 п.п., fixed January mix 60%, mix term −10 п.п.; contract D30 UNKNOWN, decomposition noncausal |
| Противоречия и отсутствие источника — VERIFIED | Сохранить конкурирующие версии и ограничить вывод вместо выбора удобной заметки | evidence-research, resume-revise | [Исторический F9 failure/recovery](../research/sol-audit/eval-results/F9-resume-failure-20261113.md), [F9 comparison](../research/sol-audit/eval-results/F9-resume-comparison-20261113.md). Exploratory synthetic scope, не общий benchmark |
| Evidence и claims — VERIFIED | Проверить цепочку источник→извлечение→вывод; явно выбрать active claims и сохранять supersedes | [conventions](../references/evidence-and-claims.md), case_protocol | [LinguaStep sources](../cases/linguastep-retention/sources.jsonl), [evidence](../cases/linguastep-retention/evidence.jsonl), [claims](../cases/linguastep-retention/claims.jsonl). tests/test_case_protocol.py проверяет IDs/forks; hashes не проверяют смысл источника автоматически |
| Файловая память — VERIFIED | Сохранить основание, решение, версии и следующий шаг между чатами | state, snapshots, source/evidence/claim журналы; resume-revise | [R0001 Resume receipt](release/final-20261122/source-resume-receipt.json), [D0001 map](../cases/linguastep-retention/export-map.json). Прежний ответ модели не становится фактом |
| Семантический поиск / vector DB — NOT_IMPLEMENTED | Такой дополнительный retrieval-компонент не нужен для заявленного файлового workflow | Нет отдельного engine, embedding store или server | Файловая навигация не называется vector/RAG системой |

## Целостность и границы исполнения

| Функция / статус | Ценность и механизм | Реализация | Проверка / предел |
|---|---|---|---|
| SHA-256 и checkpoint — VERIFIED | Связать шесть snapshots, источники, parent и active set в одной проверяемой версии | [case_protocol](../tools/case_protocol.py), [checkpoint contract](../cases/_template/README.md) | [Family gate](release/final-20261122/family-final-hash-check.json), [LinguaStep gate](release/final-20261122/linguastep-export-gate.json) и [classify](release/final-20261122/linguastep-export-classify.json). VALIDATED_CANDIDATE и CHECKPOINTED — разные стадии |
| История/fail-closed — VERIFIED | Не смешивать snapshots и не выбирать claim по времени/порядку JSONL | resume-revise, case_protocol | tests/test_case_protocol.py: test_manifest_hash_mismatch_stops, test_unselected_claim_fork_is_rejected_even_if_parent_is_active, test_candidate_rejects_each_stale_current_view |
| Незавершённые дополнения — VERIFIED | Отдельно показать draft/hints, не сделать их активными автоматически | [resume_context](../tools/resume_context.py) | tests/test_resume_context.py: test_multiple_candidates_and_older_base_are_not_ranked_by_mtime, test_state_and_activity_only_hints_do_not_follow_saved_paths. Live случай без drafts подтверждён source Resume; многодрафтовый UI сценарий — только tests |
| Безопасное создание/повтор — VERIFIED | Не объединять занятый каталог, сохранить partial copy, отвергнуть traversal/links/junctions | [case_workspace](../tools/case_workspace.py), first-run | tests/test_case_workspace.py: test_occupied_directory_or_file_is_never_merged_or_overwritten, test_partial_copy_is_preserved_and_retry_cannot_merge. Не является exactly-once гарантией внешнего бизнес-действия |
| Разделение выбора и исполнения — VERIFIED | Сохранить явные запреты после выбора стратегии | [AGENTS](../AGENTS.md), source owner inputs обоих кейсов | Выбраны направления, но пилот/бюджет/контакты не разрешены и не запускались |
| Revision-bound approvals — IMPLEMENTED_NOT_E2E_TESTED | Отдельная запись action/scope/revision+manifest hash; изменённое основание требует нового согласования | [approval contract](../references/evidence-and-claims.md), [template](../cases/_template/README.md), [functional evaluator](../tools/functional_evaluator.py) | Существуют schema/procedure и offline checks; реальный цикл утверждение→внешнее действие→повтор не проведён в двух основных кейсах. Это не host permission/sandbox |
| Отказы и fallback — VERIFIED | Записать ошибку/retry и выбрать доступный разрешённый инструмент | [find_python](../tools/find_python.ps1), first-run, source activity | [PDF fallback](evaluation.md), [selected-case review/limits](release/final-20261122/README.md), tests/test_runtime_fallback.py. Не доказана crash-safety любого прерванного multi-file write |
| Полная атомарность / автоматическое crash recovery — NOT_IMPLEMENTED | Многофайловая публикация сокращает окно конфликта, но не является транзакцией | [Архитектурные ограничения](architecture.md) | Неполная ревизия блокирует продолжение; не чинится незаметно |
| Источники как недоверенные данные — HOST_DEPENDENT | Инструкции запрещают исполнять команды из источника и расширять доступ | [security rules](../references/security-and-source-handling.md), AGENTS | Требует соблюдения моделью/host; репозиторий не является OS sandbox и не гарантирует общую injection resistance |

## Шесть Skills — одна последовательность, шесть процедур

| Skill / статус | Вклад и проверяемый результат |
|---|---|
| [intake](../.agents/skills/intake/SKILL.md) — VERIFIED | Бриф, цель, границы, существенные вопросы; сохранённые brief/scope двух кейсов |
| [evidence-research](../.agents/skills/evidence-research/SKILL.md) — VERIFIED | Источники, сопоставление объяснений, locators/UNKNOWN; PDF и CSV/web кейсы |
| [options-decision](../.agents/skills/options-decision/SKILL.md) — VERIFIED | Разные варианты/возражения, рекомендация отдельно от PO; 6 и5 альтернатив |
| [strategy-communication](../.agents/skills/strategy-communication/SKILL.md) — VERIFIED | Связанные продуктовая и коммуникационная стратегии обоих кейсов |
| [experiment-design](../.agents/skills/experiment-design/SKILL.md) — VERIFIED | Validation design с comparator/знаменателями/guardrails; реальный эксперимент не запускался |
| [resume-revise](../.agents/skills/resume-revise/SKILL.md) — VERIFIED | Проверка версии, восстановление и targeted revise; source Resume и семейный D0003 |

VERIFIED здесь относится к содержанию процедур/сохранённым этапам и указанному scope доказательства. Автоматическое обнаружение/активация Skills во всех hosts — HOST_DEPENDENT. Шесть Skills не называются шестью агентами.

## Среды, измерения и дополнительные пункты ТЗ

| Возможность / статус | Реальное состояние и сценарий |
|---|---|
| Codex workflow — VERIFIED | Основной видеокейс и второй source-case новый чат; provider/API ID всей сессии UNKNOWN. Для чтения итогов достаточно Markdown, для проверки helpers нужен Python3.12+ |
| Cursor / другие coding assistants — HOST_DEPENDENT | Открыть ту же папку с моделью, файловым/web/exec доступом; прочитать AGENTS и canonical Skill, выполнить штатный gate. Cursor live E2E не проводился |
| Снятие времени/usage — HOST_DEPENDENT | Activity и receipts сохраняют доступные timestamps/errors/tools; model calls/tokens/direct bill и полное время дела UNKNOWN без host/provider exports |
| Инженерные измерения — VERIFIED | [Windows 121 tests/5 symlink skips](release/final-20261122/unit-tests.json); [CI release](https://github.com/EdYaRdx/megafon_hack/actions/runs/45050094992) — 121 tests/5 Windows-only skips. Пропуски дополняют друг друга. Это не скорость модели/задачи |
| Визуальный UX-аудит интерфейса — HOST_DEPENDENT | Host может передать screenshot; агент должен цитировать видимое и отличать гипотезу. Отдельной UX Skill, проверенного UI-audit E2E и измеренного usability-эффекта нет. Продемонстрирован только дизайн пути/отказов по брифу |
| Реальные интервью / модельные респонденты — NOT_IMPLEMENTED | Есть consent/privacy правила, но нет реализованного специализированного interview/respondent workflow и живого доказательства; синтетические ответы не подтверждают спрос |
| Аудио/видео как аналитический вход — NOT_IMPLEMENTED | Нет ingestion/transcription/video-analysis pipeline или E2E. Демонстрационное видео — запись работы, не вход модели для видеоанализа |
| MCP — NOT_IMPLEMENTED | [.omp/mcp.json](../.omp/mcp.json) содержит отключённый open-design для разработки; рабочая продуктовая MCP интеграция не заявлена |
| Hooks / product subagents — NOT_IMPLEMENTED | В runtime нет событийных hooks и субагентного orchestration. Независимые инженерные reviewers не являются функцией продукта |
| Мультимодельный router — NOT_IMPLEMENTED | Host выбирает модель; optional .omp profiles — разработка, не проверенный выбор моделей по задаче/цене |
| Мониторинг после решения — NOT_IMPLEMENTED | Возврат/пересмотр запускается запросом человека. Нет background service, polling источников, scheduler или автоматических уведомлений |
| Автоматический запуск пилота/расходов — NOT_IMPLEMENTED | Workflow выпускает стратегии и план, не автономный action executor; выполнение требует отдельного решения и host permissions |

## Реализовано, но не показано отдельным live E2E: точные сценарии

1. **HELP.** В новом чате: «Прочитай AGENTS.md и prompts/first-run.md. Объясни, как начать работу; файлы дел не открывай». Ожидаемый результат — помощь и один следующий шаг; нет create/read чужого case. Это инструкция проверки, не выполненный тест.
2. **Свободный NEW.** После чтения инструкций описать новую задачу без пути. Агент предлагает один безопасный CASE; только после вашего точного согласия helper возвращает CREATED. Это пример использования уже написанного маршрута, не третий E2E и не новый прогон этой работы.
3. **Отдельное approval исполнения.** На подтверждённой ревизии владелец отдельно задаёт точные action/scope/лимиты; запись связывается с revision/hash. При иной ревизии/основании требуется новое согласие. В этом репозитории нет внешнего исполнителя, так что такая запись сама по себе ничего не запускает.

[Краткий маршрут для жюри](for-jury.md) · [Архитектура](architecture.md) · [Историческая оценка и пределы](evaluation.md).
