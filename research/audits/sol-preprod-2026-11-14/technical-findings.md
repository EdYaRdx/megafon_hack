# Technical findings

## Метод и severity

Read-only аудит доступных файлов; идентичность checkout заданному SHA не проверялась, Git запрещён. **P0 не установлен.** P1 ниже — существенные release/acceptance gates, а не найденные исполняемые уязвимости. P2 — конкретный дефект протокола, воспроизводимости или пользовательского контракта. Статический дефект можно подтвердить чтением; его предполагаемый runtime-исход остаётся **UNVERIFIED** до выполнения сценария.

Сокращение `H/` в локаторах означает `research/qualification/host-acceptance/codex-0.169.0/20261114-r1-r2/`. Остальные пути — от корня repo. Все предлагаемые исправления и regression checks — будущая работа, **продукт не исправлялся**. Независимые первичные результаты: ArchSecurity (A), ProductEvidence (B), ContestUX (C); итог перекрёстного разбора — [final-verdict.md](final-verdict.md).

## T-01 — P2: сохранённый calculation receipt не воспроизводит заявленную команду

- **Локатор:** `H/case/calculation-notes.md:8`, строка «Команда»; `references/metrics.md`, последний абзац; `H/case/activity.jsonl`, события CSV calculation / interruption / artifact writes.
- **Факт, OBSERVED_STATIC, высокая уверенность:** вместо полного PowerShell-выражения сохранено слово `вычислить`; путь указывает на прежний `cases/codex-e2e-run1-20261114/input/beta-survey.csv`, не на input экспортированного пакета. Metrics reference требует точную команду/query и сырой результат.
- **Механизм, INFERENCE:** другой оператор не может повторить именно успешный вызов по сохранённому receipt. Это особенно важно после сообщённых Python-not-found, case-insensitive `$N`/`$n` collision и неуспешной команды с output. Формулы и числа есть, но они не доказывают успешность конкретной команды.
- **Не установлено:** неверность финальных 20% / 62.5% / 12.5%. Эти отношения согласуются с supplied CSV; host replay здесь BLOCKED.
- **Влияние:** теряется проверяемость критичных чисел и доказательство tool verification для жюри.
- **Минимальное исправление:** в будущих run receipts сохранять точный успешный вызов, cwd/относительный путь, exit status и raw stdout. Для старого пакета честно обозначить missing receipt, не сочинять прошлую команду.
- **Regression:** в разрешённой среде выполнить сохранённый receipt на packaged CSV без переписывания логики; получить три отношения с правильными знаменателями и успешным status. Дополнительно воспроизвести unavailable interpreter, не выдавая его за successful calculation.
- **Независимость:** A4; B перепроверяет в cross-round. Unseen E-003 содержит существенно более полный Node receipt — положительный образец, не доказательство host portability.

## T-02 — P2: протокол не определяет целостную публикацию и отказ от mixed revision

- **Локатор:** `.agents/skills/resume-revise/SKILL.md`, первые два абзаца и update-state; `cases/_template/README.md`, абзац «При каждом пересмотре»; `docs/submission-architecture.md`, «Persistence and evidence». Исторический альтернативный дизайн: `research/sol-audit/architecture-decision.md`, «Рабочий контракт варианта A», пункты «Запись»/«Публикация».
- **Факт, OBSERVED_STATIC, высокая уверенность:** текущая процедура сохраняет decision/state snapshots и обновляет несколько независимых файлов, но не задаёт признак завершённой общей ревизии, complete-file manifest или правило отклонения несогласованного набора.
- **Механизм, INFERENCE:** остановка после нового claim/decision и до strategy/state может оставить чтение разных версий. Один писатель устраняет конкурентное редактирование, но не аварийную многофайловую публикацию. Исторические неуспешные hashline patches с «no files changed» не являются доказательством такого partial commit.
- **Контрдоказательство:** финальные inspected R2 связны; `H/case/activity.jsonl`, interruption/artifact writes, сообщает о восстановленных ошибках. Это не доказывает повреждения текущего state.
- **Влияние:** восстановление может повторить шаг или сохранить старое обещание; критично для ценности «продолжить без истории чата».
- **Минимальное исправление:** определить один complete checkpoint: parent/revision, набор обязательных файлов и finished marker; при resume несоответствие останавливает дальнейшее использование и возвращает к последнему полному набору. Полная staged revision + single pointer — вариант при подтверждённой необходимости, не требование внедрить framework.
- **Regression:** на новой тестовой копии прервать обновление после каждой записи successor, decision, options, обеих strategies, plan и state. Новый сеанс принимает только полный старый или полный новый checkpoint; не лечит конфликт угадыванием.
- **Статус:** отсутствие контракта подтверждено статически; crash-consistency test **BLOCKED/NOT RUN**. A2, independent B cross-review.

## T-03 — P2: historical decision ведёт к mutable dependencies

- **Локатор:** `H/case/revisions/decision-r1.md` → `options.md`; `H/case/revisions/` содержит только decision/state; `H/case/activity.jsonl`, R2 event сообщает обновление options/strategies/test-plan. Аналогичный минимальный snapshot contract — `cases/_template/README.md`.
- **Факт, OBSERVED_STATIC:** R1 options/обеих strategies/plan в пакете нет, текущие документы уже R2. Прошлый acceptance сам отметил REVISION-EVIDENCE-02.
- **Механизм, INFERENCE:** открытие старого основания не восстанавливает прежние обещания, альтернативы и знаменатели. Hash двух оставшихся файлов не восстанавливает отсутствующие dependencies.
- **Граница:** текущий minimum template не требует snapshot всех файлов, поэтому это ограничение полноты истории, не нарушение несуществующего правила и не полная потеря R1.
- **Влияние:** руководитель/аудитор не может точно восстановить принятое прежде решение и условия согласия.
- **Минимальное исправление:** в следующих revisions сохранять изменённые dependencies либо полный reconstructable diff и revision-specific ссылки. Не фабриковать отсутствующие R1 copies.
- **Regression:** после R2-изменения обещания и denominator открыть R1 и увидеть именно прежние значения, R2 — новые, с доступными источниками обеих версий.
- **Независимость:** A3 и независимое наблюдение B о пределах revisions; historical acceptance corroborates scope, не заменяет проверку.

## T-04 — P2: activity описывает фазы, а не отдельные попытки

- **Локатор:** `H/case/activity.jsonl`, события source reads, public methodology, interruption and resume, R2 resume; `.agents/skills/resume-revise/SKILL.md`, последний абзац; `cases/_template/README.md`, activity guidance.
- **Факт, OBSERVED_STATIC:** три input reads и failed directory read сгруппированы; первый и повторный public fetch объединены; interruption записан как случившийся до наполнения journals; R2 reads/writes/verification собраны в одном completion event.
- **Механизм, INFERENCE:** между результатом запроса и поздней записью существует неописанный промежуток. При file-only resume нельзя отличить все completed/failed/uncertain attempts и обосновать неизбежный повтор. Не доказаны скрытые вызовы или сокрытие ошибок.
- **Влияние:** недостоверна полнота retry/time/cost trail; трудно оценить сохранение прогресса.
- **Минимальное исправление:** индивидуальные attempt IDs и status attempt→result во время работы; при пропуске результата `UNKNOWN`, не реконструированное «success». Не требовать недоступную стоимость.
- **Regression:** прервать после ответа источника до анализа/записи результата; свежий сеанс раскрывает неопределённый исход и каждый повтор, не заявляет «ошибок нет».
- **Независимость:** A5; B cross-review. Unseen failure/retry events являются полезным контрпримером более точной детализации.

## T-05 — P2: START-HERE ведёт в исследовательскую инфраструктуру, не продукт

- **Локатор:** `START-HERE.txt`, prerequisites/start; `start-overnight-product-research-v3.cmd`, OMP invocation и Git publication; `README.md`, «Быстрый запуск»/«Границы MVP».
- **Факт, OBSERVED_STATIC:** START-HERE требует Windows, OMP authentication, конкретный путь, profiles и Git push permission. CMD выбирает Luna, `--no-skills`, многочасовой research и publication. Продуктовый README говорит о переносимой папке без OMP runtime.
- **Механизм, INFERENCE:** очевидная точка входа подменяет новый case чужим workflow, зависимостями и потенциальными внешними действиями. Launcher в аудите **не запускался**, расходы/push не наблюдались.
- **Влияние:** провал first-use UX, лишние доступы, риск демонстрировать не тот продукт.
- **Минимальное исправление:** единая root product entrypoint; исторический research launcher однозначно development-only вне пользовательского пути.
- **Regression:** незнакомый пользователь из exported folder создаёт новый case без OMP/profile/Git publication. Наблюдать фактический маршрут и помощь, не проверять только текст.
- **Независимость:** C-01, parent прочитал START-HERE/CMD/README; B cross-review.

## T-06 — P2: разные документы смешивают walkthrough, clean host и portability acceptance

- **Локатор:** `docs/submission-architecture.md`, «Models, services, and tools», говорит, что startup Cursor/Codex не наблюдался; `docs/submission-checklist.md:19` признаёт reported Codex R1/R2 PARTIAL PASS, `:395–397` требует оба hosts и говорит «No host E2E is claimed»; `docs/implementation-status.md`, Closure status; `docs/next-session-handoff.md`, Codex E2E provenance reconciliation.
- **Факт, OBSERVED_STATIC:** одновременно существуют разные текущие narratives и mandatory gates.
- **Механизм, INFERENCE:** пользователь должен самостоятельно восстанавливать хронологию; может ошибочно повторить всю проверку или объявить готовность по saved walkthrough.
- **Влияние:** неверные конкурсные claims и неопределённый следующий шаг.
- **Минимальное исправление:** одна current gate table: historical reported execution, saved-artifact review, clean single-host workflow, discovery/use, new-session resume, second-host portability, submission. Historical текст не переписывать в новую «истину».
- **Regression:** два независимых читателя одинаково определяют завершённые gates, next action и предел portability; then actual surface acceptance для выбранного host.
- **Независимость:** C-03, parent сверил противоречащие строки. Второй host — дополнительная portability-функция, не обязательное условие любого Codex-demo.

## P1 assurance gates — не исполняемые vulnerability findings

| ID | Точное основание и статус | Риск/минимальное действие | Regression/acceptance |
|---|---|---|---|
| G-01 | `docs/release/preprod-report.md`, Execution boundary / Release blocker; OBSERVED_STATIC: прежний автор записал FAIL и запрет публикации до process review. Сам инцидент HISTORICAL_REPORTED, конфигурация host UNKNOWN | Владелец релиза должен рассмотреть нарушение, зафиксировать допустимый execution profile и disposition. Настоящий аудит не отменяет старый gate автоматически | Под профилем no shell/eval запросить критичный расчёт: permitted tool либо verification blocker; sanitized attempted-call receipts показывают отсутствие запрещённых действий |
| G-02 | `docs/contest-brief.md`, «Что отправить»; checklist «Demo and deliverables»; current docs прямо указывают отсутствие verified official demo/video/final package | Сверить cabinet brief, провести сквозное демо, подготовить и проверить пакет; scope/rights — человек | Открываемые jury links, просмотренное видео ≤10 минут, полный doc, верный brief и подтверждённая подача |
| G-03 | `H/host-provenance.md`, Evidence limits, и `H/acceptance-review.md`, PARTIAL PASS; raw-call success/discovery не доказаны | Не принимать counts/skill paths за успешный clean-run; для operational claim нужен scoped acceptance evidence | Новая папка из template, novel inputs, разрешённые tools, точные receipts, реальные writes и fresh-session resume; model/version/assistance/UNKNOWN сохранены |

G-01 — governance gap, не доказательство повреждения репозитория или утечки. G-02/G-03 — отсутствие доказательства готовности, не доказательство неспособности продукта. Severity относится к unqualified release/contest acceptance.

## Матрица failure modes и фактически выполненного

| Failure mode | Текущая проверка | Результат / честный предел |
|---|---|---|
| Source/site prompt injection | Прочитаны source-injection memo, unseen vendor footer, root/security rules, F8 reports | Правила корректны; прошлый узкий F8 reported pass после targeted fix. Covert web/PDF injection и host enforcement **UNVERIFIED**, exploit не найден |
| Unsupported conclusions | Traced unseen 40%, 13/14 contradiction, method-vs-demand distinction; B/C независимое чтение | Core case withholding хорош; [P-04](product-review.md#p-04--p2-агрегат-ordersopens-превращён-в-условную-конверсию) — неверное status wording |
| Arithmetic/denominators | Reader jq arithmetic unseen + direct input inspection; source formula review | Суммы/деления согласованы, но семантика denominator ошибочна в P-01/P-02/P-04; host calculation receipt T-01 |
| State/history loss | Current active successors traced; revisions inventories | Текущие C-009/C-010 применены; T-02/T-03 показывают contract gaps, аварийный исход **NOT RUN** |
| Evidence/claims corruption | JSON-reader projections selected unseen/Codex ledgers | Parse/read success выбранных записей; не comprehensive all-repo schema/reference validation. Broken JSON, duplicate IDs, dangling refs, cycles и conflicting successors — будущие negative checks |
| Interrupted recovery | Historical Codex/F9 activity/report inspection | Сообщённое восстановление есть; нет настоящего kill-at-write-boundaries теста |
| Skills inconsistency | Все шесть + template + root | Нет конфликтующей canonical копии; P-03 template/output mismatch; refs root-relative host resolution требует actual check |
| Host dependence | README, architecture, Codex provenance, official Cursor/Codex documentation | Формат совместим документально; actual clean GUI/cross-host **BLOCKED/UNVERIFIED** |
| Unsupported safety guarantee | Root и security reference explicitly disclaim sandbox | Не найдено действующей гарантии OS isolation; process G-01 не закрыт |
| Human approval gates | Unseen C-010 traced до всех consuming outputs, Codex pending owner | Narrative gates есть; нет proof stale/reused approval rejection или real tool-gate enforcement |
| Clean startup/portability | Static onboarding/host checklist | T-05/T-06 подтверждены текстом; новое исполнение невозможно доступными средствами |

## Что не является дефектом

Append-only старый C-005 сам по себе не corruption: current consumers выбирают C-009. Отсутствие сервера/MCP/DB — сознательный scope. UNKNOWN threshold лучше выдуманного; draft не равен запущенному эксперименту. Совпадение reviewers не доказательство истинности. Старые ошибки уже исправленного case не объявлены текущими дефектами. Правила безопасности не дают OS isolation, и проект это прямо признаёт.

Полный regression programme и решение о минимальной реализации — [roadmap](implementation-roadmap.md) и [architecture-decisions](architecture-decisions.md).
