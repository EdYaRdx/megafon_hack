# E01 — supervised single-writer qualification

**PASS для фиксированной CSV-задачи в ограниченном supervised режиме.** Не доказательство unattended coding, полного E10 или качества будущего конкурсного продукта. Дата:2026-11-10.

## Fixture и заранее заданный контракт

`Q=C:/Projects/mgimo-qualification-20261110-p1`; workspace=`Q/workspace`. Создан новый собственный Git repo, **без remote**; baseline commit `42257de2aef4dcc508d08396aefdf2444da73b1b`. Существующие чужие repos не изменялись. Realpath/lstat Q/workspace/control/protected: обычные directories, не symlink/junction. Источник доверия: Lead создал contract/evaluator и synthetic inputs, проверил proposed source до запуска. Framework/dependency installs отсутствуют.

`CONTRACT.md`: Node built-ins CSV CLI, `--input --category --output`; колонки id,category,text; точная фильтрация/порядок, quoting/doubled quotes, Unicode/CRLF/quoted newlines; empty matches → header; ошибки missing columns/malformed CSV/IO/usage → nonzero, existing output не портится. Scope writer: **только src/cli.mjs**, никакого выполнения команд/тестов/делегирования.

Контракт и десять независимых behavioral tests созданы **до writer**, зафиксированы baseline commit и SHA-256. Все их hashes после writer совпали:

| Файл | SHA-256 |
|---|---|
| CONTRACT.md | bd155e7a3aa6f012d586aa61de884573978928d95c1dd6421b06172ab621e7e4 |
| test/acceptance.test.mjs | 0ebf4af7066bc58e5196cb90d5d71bd2d3fcbaaabea068eff425655777a58afb |
| fixtures/valid.csv | 1913b660bad838e702adc4674617464304d629bb335d24b5e3e770e7c5925dc1 |
| fixtures/missing-column.csv | b11a42ee9aa84e5434bc5e7c9d31d50ca7e91bc76d55a14fdf2527bb55cb7b8d |
| .omp/config.yml | 8535a5bc2f055de2accefd8571c34ab746f8c99cd6a514eace15b70817734ee3 |
| .omp/mcp.json | 93fe238328eb63d0ff090b62a82d0e50ffaed7725c6eaf5608d08551a18adc07 |

Полный frozen inventory, включая .gitignore: `Q/evidence/e01-frozen-inputs.json`, после — `e01-integrity.json`.

## Реальное исполнение writer

- Отдельный OMP18.18.6 process, **openai-codex/gpt-6.1-sol, high**. Подтверждено get_state и каждым observed assistant message_end; provider observer также фиксирует exact route. Ни fallback, ни retry events не наблюдались.
- Native inventory: **read, write, edit**. Bash/eval/task/browser/MCP не предоставлялись. Все4 reads и единственная write разрешены вручную через RPC UI; session-wide grants не выдавались.
- Реальные targets: CONTRACT.md; test/acceptance.test.mjs; fixtures/valid.csv; fixtures/missing-column.csv; write src/cli.mjs. Никаких других writer tool calls.
- Proposed source полностью просмотрен до Approve: импорт только node:fs, нет subprocess/network/eval/dependencies. Actual file совпал с одобренными bytes.
- SHA-256 `src/cli.mjs`: **140162defc036d923165504155274c9ab15d7ebc92dfd509d468159209f0e47b**.
- Prompt start20:01:54.598Z → process close20:03:59.701Z: **125.103s**, включая ручные approvals/уточнение; не latency benchmark.
- После contract read writer завершил turn с prose-запросом разрешения. Потребовалось **одно supervisor clarification**: permissions запрашивать native tool calls, не prose. Затем написал одну полную реализацию; fix/retry cycle отсутствовал. Это supervised outcome, не zero-intervention autonomy.
- Process exit0, final session settled. Completion message не использовался как acceptance.

Evidence: `e01-rpc.jsonl` (prompts, tool args/results, approvals), `e01-state.json`, `e01-session-stats.json`, `e01-integrity.json` и native writer session `Q/sessions/2026-11-10T20-01-53-714Z_01a1c70d-8232-76a8-8628-dedd8d5cbb6b.jsonl`.

## Независимые tests и настоящий CLI smoke

Supervisor исполнил `node --test` с cwd workspace, Node24.19.0. Каждый spawned CLI внутри evaluator имеет timeout3s/maxBuffer1MiB; evaluator не менял source/contract.

| Проверка | До реализации | После реализации |
|---|---|---|
| node --test | exit1, 0/10 PASS, CLI отсутствовал | **exit0, 10/10 PASS**, skipped0/cancelled0 |

После выполнения: elapsed1231ms, Node test duration1085.2726ms. Проверены filter/order/export, empty result, missing columns/no creation, preservation existing output, quoted comma/doubled quotes, Unicode filenames с пробелами/CRLF/quoted newline, exact category/spaces, invalid CSV, missing input и missing arguments. До/после logs: `e01-before.json`, `e01-after.json`; permanent product tests не создавались.

Дополнительно **не через evaluator**, запускался реальный CLI:

```powershell
$Q = 'C:/Projects/mgimo-qualification-20261110-p1'
Set-Location "$Q/workspace"
node --test
node src/cli.mjs --input fixtures/valid.csv --category A --output "$Q/runs/smoke-valid.csv"
node src/cli.mjs --input fixtures/valid.csv --category Z --output "$Q/runs/smoke-empty.csv"
# Перед negative case supervisor заранее создал smoke-preserve.csv с KEEP_EXISTING + LF.
node src/cli.mjs --input fixtures/missing-column.csv --category A --output "$Q/runs/smoke-preserve.csv"
```

| Сценарий | Exit / stderr | Реальный output |
|---|---|---|
| Valid A | 0 / пусто | Header + id1 Первый + id3 `Москва, "центр"`, правильный CSV quoting/order |
| Empty Z | 0 / пусто | Ровно `id,category,text\n` |
| Missing column | 1 / `Missing required columns: category` | Старые bytes `KEEP_EXISTING\n` сохранены |

Полные команды, timestamps, durations, stdout/stderr и exact output strings: `Q/evidence/e01-smoke.json`. Это наблюдение результата, не пересказ агента.

## Расход и время

| Run | Assistant requests | Reported tokens | Catalog-cost estimate USD |
|---|---|---|---|
| E10 parent + child | parent16 + child5 | 133349 | 0.0706964 |
| E01 writer | 5 | 30382 | 0.0470328 |
| Independent reviewer | 7 | 74421 | 0.0801556 |

E10 stats включают child: отдельно его cost0.0214068 **не добавлялся второй раз**. E01 tokens: input11348, output2266 (reasoning893 как subset), cacheRead16768. Валюта — OMP catalog estimate, **не invoice и не списание API денег**; все calls через уже разрешённый Codex Plus route. Общая Lead-сессия в эти per-process stats не входит.

Redacted quota snapshot: до — 5h17%,7d28%; после — 5h30%,7d30%, cache age5m56s. Это общая account quota, включая Lead/другие обращения; delta **не атрибутируется одному E01**, фактическая денежная стоимость/точная доля task UNKNOWN. Ни новый paid backend, ни Copilot/Polza не использовались. Quota не исчерпана; forced limit/cost cap не тестировались.

## Scope и Git

После writer и smoke:
- Contest repo оставался clean на `17aa0db...`, `git diff --exit-code`=0 до создания этих qualification reports.
- Fixture repo: `?? src/`, tracked diff exit0, remotes отсутствуют; contract/tests/inputs/profile unchanged.
- Все recorded mutation targets writer — только src/cli.mjs. Control/evidence/runs создавались Lead вне product repo. Canary/global config/binary hashes unchanged.
- Обычные OMP caches/auth refresh/runtime state не отслеживались как полное host filesystem audit; глобальное «никаких иных writes в Windows» не заявляется.

Итоговый Git после сохранения отчётов — в [next-step](next-step.md). Никакого push, публикации или product implementation.

## Независимое read-only review

Свежий отдельный process, Codex Sol High, inventory **только read**, без mutation/execution; 15 read calls, errors0. Прочитал contract/source/tests и настоящие JSON evidence. Verdict: **supervised admission justified with limitations; unattended BLOCKED**. Подтвердил AC1–5, 0/10→10/10, smoke, scope и неизменные frozen files; подтверждённых CLI defects не найдено.

Reviewer отдельно оставил **FAIL raw abort**; child read=allow не доказывает universal read approval (в E01 другой, более строгий read=prompt профиль). Отметил неполное покрытие всех parser/argument combinations и UNKNOWN global leak absence. Test executions не повторял, проверял переданное supervisor evidence + source. Same model family, поэтому это независимость контекста/автора, **не межсемейная проверка**.

Полный report: `Q/evidence/independent-review.txt`, RPC/source-of-review `review-rpc.jsonl`, `review-session-stats.json`. Общие ограничения: [blockers](blockers.md), safe admission: [next-step](next-step.md).
