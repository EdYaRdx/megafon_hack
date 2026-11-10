# Phase 1 — effective configuration

Дата: 2026-11-10. **VERIFIED** означает конкретное наблюдение этой фазы, не полную безопасность OMP. Raw evidence и disposable fixture сохранены локально: `C:/Projects/mgimo-qualification-20261110-p1/` (далее `Q`). Конкурсный код не создавался.

## Исходный запуск Lead

- `omp --version`: **18.18.6**; Node **24.19.0**, Windows native x64.
- `read cfg://tools/approvalMode`: **yolo**, `source: default`, `default: yolo`.
- `cfg://tools`: approval={}, restrictedFolders=[], maxTimeout=0.
- `cfg://modelRoles`: `default=openai-codex/gpt-6.1-sol:high`, source global config.
- task: concurrency32, workers4, recursion2, runtime0, isolation off, perCallModel off; retry.modelFallback=true; session cost limits отсутствуют.
- Исследование правильно зафиксировало default, а не включённый нами флаг `--yolo`. Текущая родительская сессия по-прежнему yolo: её настройки **не изменялись**. Квалифицирован отдельный supervised процесс с явным local profile, не этот default-сеанс.
- Переменных `OMP_*`/`PI_*` в environment запуска test process не обнаружено; значения credentials/environment не экспортировались.

Доказательства: исходные `cfg://` tool outputs; `Q/evidence/baseline.json` содержит safe namespace snapshots и исходные hashes. Начальный Git конкурсного репозитория: `17aa0db168366e7af61c2112c7ed65da83c864ac`, clean `main...origin/main`.

## Реально использованные project-local настройки

Файл: `Q/workspace/.omp/config.yml`; не записан в global config. Native project discovery подтверждён `omp config get tools.approvalMode --json` с cwd fixture: always-ask. `omp config list --json` exit0 без warnings; отфильтрованный снимок `Q/evidence/effective-settings.json`. В запущенном preflight `read cfg://...` показал overlay provenance; actual provider/model/effort проверены через RPC get_state и message_end.

| Параметр | Реальное значение |
|---|---|
| Main/task/scout/reviewer route | openai-codex/gpt-6.1-sol:high |
| enabledProviders / enabledModels | только openai-codex / gpt-6.1-sol |
| approvalMode | always-ask |
| read / write / edit | prompt / prompt / prompt |
| bash / eval / browser / web_search | deny |
| task | prompt; отсутствовал в E01 tool inventory |
| maxConcurrency / workerThreads / recursion | 1 / 0 / 1 |
| child maxRuntimeMs / softRequestBudget | 180000 / 12 |
| perCallModel / modelFallback | off / false |
| isolation / auto-apply | false / false; параллельной записи не было |
| async / speculativeLaunch / completionProbe | false / false / false |
| retry.maxRetries / maxDelayMs | 1 / 5000 |
| session.warnCost / maxCost | 3 / 5, catalog estimates, не реальные API-бюджеты |
| secrets.enabled | true; только fake probe, project replace-mode rule |
| eval.js / eval.py / LSP / Skills | false / false / false / false |
| cacheWarming / advisor / memory | off / false / off |
| update.auto / startup.checkUpdate | false / false |
| worktree.cleanSource / clone / onStart / onExit | false / false / off / keep |
| tools.xdev / maxTimeout | false / 60 |
| MCP | project entry open-design enabled=false; MCP tools в inventory отсутствуют |

RestrictedFolders: `Q/protected`, `Q/control`, `Q/evidence`, конкурсный репозиторий, user `.omp`. Это prompts, **не deny-all-files-outside-workspace ACL**. Shell/eval способны обходить cwd-based restrictions, поэтому writer не получил эти инструменты вообще. Непроверенный OS containment не заявляется.

Два узких overlays в `Q/control/`:

- `preflight.yml`: read=allow, остальные политики наследуются; только finite canary/config probes. Child действительно получил yolo, сохранив explicit write prompt/bash deny. `Q/evidence/e10-child-proof.json` извлечён из настоящих toolResult его JSONL, не только из итогового текста.
- `review.yml`: read=allow, read-only inventory, разрешено читать evidence этой fixture; private/protected/repo paths остаются restricted. Только свежая независимая проверка.

## Точные launch controls

Общие args (абсолютные placeholders раскрываются через Q):

```text
omp --cwd Q/workspace --config Q/workspace/.omp/config.yml
  --model openai-codex/gpt-6.1-sol --thinking high --mode rpc-ui
  --no-extensions --no-skills --no-rules --no-context-files --no-lsp --no-title
  --max-time 12m --warn-cost 3 --max-cost 5 --session-dir Q/sessions
```

E10: дополнительно `--config Q/control/preflight.yml -e Q/control/provider-observer.mjs --tools read,write,edit,bash,task`.

E01: `-e Q/control/provider-observer.mjs --tools read,write,edit`. RPC get_state реально показал **ровно read/write/edit**. Supervisor вручную ответил на 4 read approvals и 1 write approval; session-wide grants/auto-approval отсутствуют.

Independent review: дополнительно `--config Q/control/review.yml -e Q/control/provider-observer.mjs --tools read`; actual inventory только read.

`provider-observer.mjs` — reviewed disposable instrumentation, не установленный плагин/сервис: пишет только time/model и boolean наличия fake/replacement, **не payload/headers/tokens**. `rpc-client.mjs` — finite JSONL test adapter с непрерывным drain stdout/stderr и request timeout30s, без автоматических approvals/scheduler/retries. Сохранены вне product repo для воспроизводимости. Явный `-e` загружает только этот observer несмотря на отключённый ambient discovery.

RPC process не запускал unattended workflow: каждую мутацию разрешал Lead, executable commands worker не имел. Supervisor исполнял только проверенный Node evaluator/CLI и Git metadata/создание baseline **собственного** fixture repo. No install, push, publication, new account/provider.

## Целостность global config и binary

До/после E10 и E01 hashes совпали:

| Файл | SHA-256 |
|---|---|
| user .omp/agent/config.yml | 5451c1e75f92e45dbbbd563153e99b9c92ecaf6ed01683b8eac6089136e99bed |
| user .omp/agent/mcp.json | cfe09da05c444e1550704a2bb974750e67fdbf185bf29ad12aaa3e893d22955f |
| installed omp.exe | dfb15c27cb2ea192a94761c26aa5cd4eed54b1e0a5a85c02938ab07d769bc8f7 |

Обычные OMP auth/cache/usage/session runtime writes не равны изменениям global config. Полный мониторинг всех файлов/сетевых обращений host не проводился; отсутствие произвольных изменений во всём Windows — **UNKNOWN**. Проверены конкретные config hashes, repo Git states, frozen fixture files, canaries и все наблюдённые worker tool targets.

## Сохранённая project-local копия для следующего запуска

После завершения проверок в конкурсный repo добавлены только `.omp/profiles/qualification-supervised.yml` и `.omp/mcp.json`, byte-identical испытанным fixture files. Их hashes совпали: profile `8535a5bc2f055de2accefd8571c34ab746f8c99cd6a514eace15b70817734ee3`, MCP `93fe238328eb63d0ff090b62a82d0e50ffaed7725c6eaf5608d08551a18adc07`. Evidence: `Q/evidence/project-profile-copy.json`.

Profile — явный `--config`, не автоматическое изменение текущего Lead или global defaults. Main-repo/TUI запуск с ним ещё не выполнялся; verified runtime results относятся к disposable workspace. Fake-secret rule/value не копировались в репозиторий. Перед новым cwd подтвердить actual inventory/policy; подробный следующий шаг — [next-step](next-step.md).
