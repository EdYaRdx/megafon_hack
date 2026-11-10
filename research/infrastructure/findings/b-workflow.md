# Researcher B — workflow evidence

Дата проверки: 2026-11-10. Read-only исследователь; ниже исходный evidence report. VERIFIED ограничен явно описанными действиями.

# Материал для `findings/b-workflow.md`

## Краткие выводы

1. **Основной выбор для хакатона — минимальный OMP workflow без установки дополнительных workflow-плагинов**: короткий контракт → вертикальные срезы → независимое ревью → исправление → интеграционная проверка → повторное ревью исправлений. Это **[INFERENCE] рекомендация**, не результат эксперимента.
2. **Spec Kit и OpenSpec действительно имеют отдельную интеграцию Oh My Pi**, а не только поддержку исходного Pi. У Spec Kit ключ `omp`, у OpenSpec — `oh-my-pi`. **DOCUMENTED**, подтверждено документацией и исходниками.
3. **Если нужна формализованная spec-система, первый кандидат для квалификации — Spec Kit 1.3.3**: явные требования, зависимости задач, user-story slices, consistency analysis и convergence loop. **Не ставить одновременно с OpenSpec.**
4. **OpenSpec 1.17.0 — содержательный конкурент**, особенно для небольших изменений существующего продукта: proposal/delta specs/tasks/archive, простое восстановление по checkbox-состоянию. Независимое ревью и TDD не являются автоматически обеспеченными свойствами.
5. **BMAD шире задачи хакатона; Superpowers полезен как источник отдельных практик**, но их native OMP runtime-интеграция по прочитанным источникам **UNKNOWN**. Поддержку Pi нельзя выдавать за поддержку OMP.
6. Важное расхождение: **публичная OMP-документация Spec Kit описывает возможности `main`, которых нет в адаптере релиза 1.3.3**. Квалифицировать нужно pinned release, а не README плюс текущий сайт.
7. Ничего не устанавливалось, команды не запускались, настройки и файлы не изменялись. Практическая работоспособность всех интеграций — **UNKNOWN**, не VERIFIED.

---

## 1. Версии, даты, идентичность источников

**DOCUMENTED** ниже означает прочитанный официальный документ/исходник; опубликованные авторами результаты испытаний остаются **CLAIMED**, пока не воспроизведены.

| Система | Наблюдавшийся latest release | Дата в источнике | Статус и оговорки |
|---|---|---|---|
| GitHub Spec Kit | [v1.3.3](https://github.com/github/spec-kit/releases/tag/v1.3.3), `79cb423` | `2026-11-09` в [release commit/changelog](https://github.com/github/spec-kit/commit/79cb423c37bb9394bab7a66063c27dfa80b72fba); release UI: `09 Nov 20:40` | DOCUMENTED. На `main` уже есть изменения после релиза |
| Fission-AI OpenSpec | [v1.17.0](https://github.com/Fission-AI/OpenSpec/releases/tag/v1.17.0), `579fcac` | Release UI: `09 Nov 23:46`; год/таймзона в извлечённом release-тексте не показаны | DOCUMENTED версия и отображённая дата. Не превращать её в точный UTC timestamp |
| BMAD-METHOD | [v6.12.4](https://github.com/bmad-code-org/BMAD-METHOD/releases/tag/v6.12.4), `bab9082` | Release UI: `14 Oct 21:19`; год/таймзона не показаны | DOCUMENTED. [README](https://github.com/bmad-code-org/BMAD-METHOD) различает stable 6.12 и **v7 preview alpha**; ETA v7 — середина ноября 2026, это CLAIMED прогноз |
| obra/superpowers | [v7.0.2](https://github.com/obra/superpowers/releases/tag/v7.0.2), `22f0b46` | `2026-11-03` в [RELEASE-NOTES.md](https://github.com/obra/superpowers/blob/v7.0.2/RELEASE-NOTES.md) | DOCUMENTED. Release notes содержат заявления о собственных evals — CLAIMED, не локальное VERIFIED |

Все четыре целевых GitHub URL открыты именно под указанными владельцами. Указанный пользователем `github.github.com/spec-kit/integrations/omp.html` открыл официальную страницу Oh My Pi; её edit-link ведёт в `github/spec-kit`. README также использует домен `github.github.io/spec-kit`.

GitHub REST API для releases/tree вернул **HTTP 403 — FAILED для этого способа получения метаданных**. Альтернатива — официальные HTML releases, каталоги GitHub и raw-исходники — доступна; исследование не заблокировано.

---

## 2. Реальная OMP-интеграция и Windows

### Spec Kit: подтверждён отдельный адаптер OMP

Источники:

- [Официальная OMP-страница](https://github.github.com/spec-kit/integrations/omp.html).
- [Адаптер релиза 1.3.3](https://github.com/github/spec-kit/blob/v1.3.3/src/specify_cli/integrations/omp/__init__.py).
- [OMP-документация релиза](https://github.com/github/spec-kit/blob/v1.3.3/docs/integrations/omp.md).
- [Установка и Windows](https://github.github.io/spec-kit/installation.html).

**DOCUMENTED:**

- Интеграционный ключ — `omp`.
- Команды устанавливаются в `.omp/commands/*.md`, вызов — `/speckit.specify`, `/speckit.plan` и т. д.
- Адаптер запускает `omp --print`, передаёт prompt **позиционно**, модель через `--model`, JSON через `--mode json`, не `--output-format`.
- Интеграция объявлена `multi_install_safe`. Это безопасность совместной установки **интеграций Spec Kit**, а не обещание бесконфликтной совместимости с другими методологиями.
- Windows поддерживается без обязательного WSL; Windows default script variant — `ps`; доступны также `sh` и `py`.
- Python ≥3.11; `uv` рекомендован. Git нужен для source-install и отдельно для opt-in git extension, но не является обязательной основой feature-state.

**Критичное version drift:**

В релизе 1.3.3 `build_exec_args()` принимает `integration_args`/`integration_options`, но не добавляет их в argv. На [текущем `main`](https://github.com/github/spec-kit/blob/main/src/specify_cli/integrations/omp/__init__.py) уже есть их передача и валидация `profile`, `thinking`, `tools`.

Следовательно, пример сайта с per-step `profile`/`thinking`/`tools` **не считать контрактом версии 1.3.3**. Это не практический FAILED: расхождение обнаружено статическим чтением.

Сайт отдельно предупреждает: `tools: read` **не является read-only security boundary** — могут включаться discovered/extension tools.

### OpenSpec: отдельный OMP target тоже существует

Источники:

- [Supported tools](https://openspec.dev/docs/supported-tools).
- [Релизный `src/core/config.ts`](https://github.com/Fission-AI/OpenSpec/blob/v1.17.0/src/core/config.ts), строка 83.
- [Setup](https://openspec.dev/docs/setup), [Installation](https://openspec.dev/docs/installation).

**DOCUMENTED:**

```text
--tools oh-my-pi
skills:   .omp/skills/
commands: .omp/commands/
command:  /opsx-apply
```

В релизном коде отдельная запись:

```ts
{ name: 'Oh My Pi', value: 'oh-my-pi', available: true,
  successLabel: 'Oh My Pi', skillsDir: '.omp' }
```

Это генерация workflow-инструкций для OMP; не доказательство автоматической параллельной orchestration.

Windows документирован через PowerShell installer и standalone ZIP `openspec-windows-x64.zip`; npm-маршрут требует **Node ≥22.12.0**. В 1.17.0 заявлено исправление определения CPU в Windows PowerShell 5.1 — **DOCUMENTED release note / CLAIMED исправление**, локально не проверено.

### BMAD: Pi есть, отдельный OMP не найден

- [Pinned installer platform map](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.4/tools/installer/ide/platform-codes.yaml): `pi`, строки 277–282, пишет `.agents/skills`.
- Поиск `omp`/`oh-my-pi` в platform map и альтернативная проверка README/reference не обнаружили явного OMP target.
- Поэтому **native OMP adapter — UNKNOWN**, а не «поддерживается через Pi».
- [Pinned install guide](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.4/docs/start/install-bmad.md): Node ≥20.12, `uv` нужен для ряда skills, включая build; без него installer может завершиться с предупреждением.
- Windows end-to-end с OMP — **UNKNOWN**.

### Superpowers: native Pi package, не подтверждённый OMP package

- [README, Pi](https://github.com/obra/superpowers#pi): `pi install git:github.com/obra/superpowers`.
- [package.json 7.0.2](https://github.com/obra/superpowers/blob/v7.0.2/package.json): `pi.extensions`, `pi.skills`.
- [Pi extension](https://github.com/obra/superpowers/blob/v7.0.2/.pi/extensions/superpowers.ts): импорт API из **`@earendil-works/pi-coding-agent`**, bootstrap через `session_start`, `session_compact`, `context`.

Это другой package identity, чем OMP `@oh-my-pi/pi-coding-agent`. Совместимость extension API, загрузчика пакетов и tool mapping с OMP — **UNKNOWN**.

Release 7.0.2 документирует Windows fixes для Copilot hooks, Git Bash startup и путей helper scripts; это не VERIFIED Windows+OMP.

---

## 3. Команды и создаваемые артефакты

Команды ниже — **только описание будущей установки/работы**, не выполненные действия.

| Система | Установка/инициализация | Рабочие действия и реальные документированные артефакты |
|---|---|---|
| Spec Kit 1.3.3 | `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v1.3.3`; затем `specify init <project> --integration omp --script ps` | `/speckit.constitution`; `specify` → `spec.md`, requirements checklist; `plan` → `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/` по применимости; `tasks` → `tasks.md`; `analyze` → read-only report; `implement` → код/checkbox progress; `converge` → findings и при наличии gaps только **добавление задач** |
| OpenSpec 1.17.0 | npm-вариант: `npm install -g @fission-ai/openspec@1.17.0`; `openspec init --tools oh-my-pi` | `openspec/config.yaml`, `specs/`, `changes/`, OMP skills/commands; explore → ничего по умолчанию; propose → `changes/<name>/proposal.md`, delta specs, design/tasks; apply → код и task checkboxes; verify optional → report-only; archive → `changes/archive/YYYY-MM-DD-<name>/` и синхронизация main specs |
| BMAD 6.12.4 | `npx bmad-method@6.12.4 install`; отдельный OMP target не установлен источниками | `_bmad` — shared config/scripts, tool-specific skill trees; `bmad-spec` → `SPEC.md` и companions, optional `stories.yaml`; `bmad-prd` → `prd.md`, `addendum.md`, `.memlog.md`; architecture → `ARCHITECTURE-SPINE.md`; sprint planning → readiness verdict + `sprint-status.yaml`; build → код, implementation record, локальный commit, deferred-work record |
| Superpowers 7.0.2 | Документированный Pi-маршрут — `pi install git:github.com/obra/superpowers`; команда не pin-ит релиз | Skills/bootstrap; brainstorming → `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`; writing-plans → `docs/superpowers/plans/YYYY-MM-DD-<feature>.md`; SDD → git-ignored `.superpowers/sdd/<plan-workspace>/`, ledger `progress.md`, briefs/reports/review packages; worktrees и commits |

Источники деталей:

- Spec Kit: [Agentic SDD](https://github.github.io/spec-kit/reference/agentic-sdd.html), [plan template](https://github.com/github/spec-kit/blob/v1.3.3/templates/plan-template.md).
- OpenSpec: [Skill contracts](https://openspec.dev/docs/skills), [CLI](https://openspec.dev/docs/cli).
- BMAD: [planning paths](https://github.com/bmad-code-org/BMAD-METHOD/blob/V6.12/docs/plan/choose-a-planning-path.md), [build](https://github.com/bmad-code-org/BMAD-METHOD/blob/V6.12/docs/build/build-a-change.md). Ветка `V6.12` mutable; точный pinned install/review contract прочитан отдельно.
- Superpowers: [writing-plans 7.0.2](https://github.com/obra/superpowers/blob/v7.0.2/skills/writing-plans/SKILL.md), [SDD 7.0.2](https://github.com/obra/superpowers/blob/v7.0.2/skills/subagent-driven-development/SKILL.md).

**Не перепутать:** `openspec validate` проверяет структуру specs/changes, а не функциональную корректность приложения. `/speckit.checklist` проверяет качество требований, а не прохождение тестов продукта.

---

## 4. Сравнение workflow

Свойства систем — **DOCUMENTED инструкции**, не гарантия соблюдения моделью. Колонка минимального OMP — **[INFERENCE] предлагаемый процесс**.

| Аспект | Минимальный OMP | Spec Kit | OpenSpec | BMAD | Superpowers 7.0.2 |
|---|---|---|---|---|---|
| Discovery | Короткий read-only scout | `specify/clarify`; idea assessment отдельно | `explore`, ничего не пишет по умолчанию | Research/forge/brief, по потребности | Brainstorming + approval gate |
| Requirements/spec | Один короткий контракт | Constitution + feature spec | Proposal + capability delta specs | SPEC; PRD/UX/architecture по масштабу | Design doc |
| Decomposition | 2–3 end-to-end slices, interfaces/owners | Dependency phases, user stories, `[P]` | Tasks + artifact dependency graph | Stories/epics/sprint readiness | Independently testable tasks, exact files/tests |
| Parallel vertical slices | Только независимые файлы/контракты | Story-oriented; `[P]` — возможность, не доказательство runtime orchestration | Несколько changes возможно; scheduling не обеспечен | Story coordination; reviewers parallel | **SDD запрещает параллельных implementers**; отдельный parallel skill — не основание игнорировать запрет |
| TDD | Explicit RED/GREEN на рискованном поведении | Tests **optional**, если не запросить | Не обязательный default | QA есть; универсальный strict TDD не подтверждён | Strict RED–GREEN–REFACTOR |
| Independent review | Новый reviewer context, read-only | `analyze/converge` не требуют другого агента | `verify` optional и не гарантирует независимость | Независимые review layers + triage | Fresh task reviewer: spec + quality; final branch review |
| Evaluator–optimizer | Finding → fix → scoped re-review | `implement ↔ converge` | `verify → amend/apply` организует команда | Review → triage → fix/upstream correction | Явный bounded fix loop |
| Integration | Lead соединяет slices и проверяет общий путь | Общий plan/foundation, convergence | Main specs sync/archive; не замена code integration | Проверка combined stories, retrospective | Whole-branch review + finishing workflow |
| Re-review | Findings + fix diff, не новое безграничное ревью | Новый converge pass; независимость не встроена | Повтор verify, процесс задаёт команда | Повтор build со `status: done` идёт в review | Обязательный scoped re-review каждой fix round |
| Blockers | Не изобретать prerequisite/acceptance | Quality gates; unchecked checklist требует решения | Apply останавливается на ambiguity/error/missing artifacts | `patch / defer / decision needed` | NEEDS_CONTEXT/BLOCKED; часть ambiguity решается controller rulings |
| Context recovery | Contract + ledger + exact next action | Feature artifacts + `.specify/feature.json` | `tasks.md`: resume с первого unchecked | Implementation/story records, context artifacts | Ledger/briefs/reports; recovery после compaction |
| Stop criteria | AC + evidence + no unresolved blockers | `Converged`; не равно независимый sign-off | Tasks checked/archive readiness; archive допускает warning+confirmation | Review triage и acceptance, слабые specs исправлять upstream | До 5 fix rounds/task; затем findings могут быть **parked**, final review — одна fix wave |

### Существенные нюансы

- [Spec Kit tasks template 1.3.3](https://github.com/github/spec-kit/blob/v1.3.3/templates/tasks-template.md), строки 9–18: tests optional; `[P]` означает разные файлы без зависимостей. Поэтому нельзя писать «Spec Kit автоматически обеспечивает TDD и параллельных агентов».
- [Spec Kit quickstart](https://github.github.io/spec-kit/quickstart.html): active feature определяется `.specify/feature.json`, **не Git branch**. Переключение ветки само по себе feature не переключает — риск при параллельной работе.
- [OpenSpec profiles](https://openspec.dev/docs/profiles): core теперь **шесть workflows**, verify не включён по умолчанию. Старый обзор «три команды» неполон.
- [OpenSpec 1.17.0 release](https://github.com/Fission-AI/OpenSpec/releases/tag/v1.17.0): command files deprecated и планируются к удалению в 2.0; skills сохраняются.
- [Superpowers SDD](https://github.com/obra/superpowers/blob/v7.0.2/skills/subagent-driven-development/SKILL.md): fresh implementer/task, но **не параллельные implementers**; один reviewer совмещает spec и quality verdict. README-формулировка «two-stage review» не должна подменять текущий контракт двумя обязательными reviewer agents.
- [Fix loop](https://github.com/obra/superpowers/blob/v7.0.2/skills/subagent-driven-development/references/fix-loop.md): максимум пять раундов; [final review](https://github.com/obra/superpowers/blob/v7.0.2/skills/subagent-driven-development/references/final-review.md) — одна fix wave. «Workflow завершился» не означает «не осталось известных дефектов».
- [BMAD pinned review](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.4/docs/build/review-a-change.md): reviewers работают независимо, затем findings проверяются и маршрутизируются; авторы предупреждают, что на некоторых runtime reviewers могут перейти к последовательному выполнению или main context.

---

## 5. Плюсы, минусы, порог применения

Все пороги ниже — **[INFERENCE] рекомендации**.

| Вариант | Плюсы | Минусы/риск | Когда применять |
|---|---|---|---|
| Минимальный OMP | Нет нового installer/runtime слоя; управляемые роли; мало ceremony | Lead вручную удерживает AC, dependencies, recovery | Default для одного demo и нескольких slices |
| Spec Kit | Самая явная цепочка spec→plan→tasks→converge; отдельный OMP adapter; native Windows scripts | Артефактный overhead; tests optional; docs/main drift; feature-state collision | Несколько зависимых сценариев, стабильные требования, нужен traceability |
| OpenSpec | Компактные changes, delta specs, recovery по tasks; отдельный OMP target | Verify optional; глобальные profile settings; 2.0 command migration | Быстро меняющийся brownfield и небольшие последовательные changes |
| BMAD | Discovery, PRD/UX/architecture, независимые review lenses, upstream correction | Самый широкий процесс; alpha/stable split; native OMP UNKNOWN; автоматические commits | Несколько эпиков/команд, существенная coordination cost |
| Superpowers | Самые конкретные TDD/review/re-review/recovery инструкции | Native OMP UNKNOWN; mandatory gates/hooks; sequential implementers; может park findings | Команда осознанно выбирает всю методологию и квалифицировала harness |

**Выбор не «четыре системы вместе».** Для хакатона — минимальный OMP. Если эксперимент покажет необходимость spec framework — выбрать **один**: первым квалифицировать Spec Kit, OpenSpec оставить альтернативной веткой сравнения.

---

## 6. Риски конфликтов workflow-плагинов

1. **Два владельца одного процесса.** Spec Kit, OpenSpec и BMAD заведут разные spec/task/status источники истины; обновление одного не синхронизирует остальные.
2. **Auto-trigger и bootstrap.** Superpowers инжектирует правила на runtime events; это может повторно запускать brainstorming/planning вместо уже делегированной работы. В release notes есть реальные исправления подобного bootstrap-поведения, но OMP не квалифицирован.
3. **Разные semantics completion.** Checked task, `Converged`, archive, parked review finding и accepted epic — разные события.
4. **Запись за пределами ожидаемых Markdown.** Init/install создают `.omp`, `.specify`, `openspec`, `_bmad`, skills/scripts/config; Superpowers может создавать worktrees и commits. Текущему read-only контракту это не соответствует.
5. **Глобальные изменения.** OpenSpec profiles/delivery сохраняются per-machine; `openspec update` может предлагать upgrade CLI. Не считать это исключительно проектной операцией.
6. **Скрытые проверки/запуски.** Superpowers TDD/worktree/finishing и BMAD build могут инициировать tests/setup/commits. Для исследования они не запускались.
7. **Изоляция не следует из названия инструмента.** OMP `--tools` не полноценная граница доступа; нельзя основывать read-only assurance только на нём.
8. **Версии не pin-ятся автоматически.** `@latest`, `npx ... install` и `pi install git:...` без версии дают дрейф. Квалификация должна фиксировать CLI, templates/skills и commit.

---

## 7. Основной hackathon workflow: минимальный OMP

Это **план**, не разрешение писать продукт сейчас. До отдельного разрешения все будущие Markdown-артефакты остаются только в разрешённой исследовательской области.

| Шаг | Действие | Acceptance/gate |
|---|---|---|
| 1. Discovery | Lead формулирует пользовательскую цель, критерии жюри, доступные данные/инструменты; scouts исследуют только конкретные неизвестные | Есть evidence, unknowns и один выбранный demo path; никаких неподтверждённых prerequisite |
| 2. Contract | Один короткий документ: in/out scope, 5–8 проверяемых AC, примеры входа/выхода, ограничения, error/empty cases | Каждый AC наблюдаем; критические unknowns либо закрыты, либо явно блокируют |
| 3. Decompose | Сначала один walking skeleton; затем 2–3 вертикальных slices с owner, files, interfaces, test obligations, dependencies | Каждый slice даёт end-to-end поведение; shared schema/config назначены одному владельцу |
| 4. Implement | Параллель только для независимых ownership domains; в shared checkout не более одного писателя в файл | Нет конкурирующих edits; worker не меняет contract и не запускает собственных helpers/reviewers |
| 5. Evidence | После разрешения разработки — RED/GREEN для нового детерминированного поведения; worker возвращает изменения и требуемые проверки | Implementation claim не выдаётся за executed evidence |
| 6. Independent review | Свежий read-only reviewer получает contract, slice diff, interfaces; отдельно проверяет AC и качество | Findings с severity и `path:line`; отсутствие результатов — не автоматический approve |
| 7. Fix/re-review | Исправлять подтверждённые defects; re-review — findings + fix diff, включая новые регрессии | Каждый finding имеет addressed/refuted/blocked verdict; критичные нельзя просто park |
| 8. Integrate | Lead после всех slices выполняет разрешённые общие проверки один раз на собранном состоянии | Общий demo path и negative cases работают совместно; нет проверки половинчатого состояния |
| 9. Final gate | Независимый review интеграционных границ; затем evidence hand-off | Все AC покрыты, нет открытых critical/high, known limits явно указаны |

**Context recovery:** хранить contract, dependency/owner map, completed slices, findings, test evidence и точную следующую операцию. После compaction читать их, а не восстанавливать ход работы по памяти.

**Blocker contract:** статус → конкретный недостающий prerequisite → evidence → затронутые AC → доступная независимая работа. Нельзя подменять недостающий backend/mock данными и объявлять сценарий выполненным.

**Stop:** успешный demo path недостаточен без AC и интеграционного evidence. После двух безрезультатных fix/re-review циклов вернуться к requirements/interface/root cause; не продолжать бесконечное косметическое ревью.

---

## 8. План эксперимента Spec Kit vs OpenSpec

**Только план; установки, код и проверки не выполнялись.**

### Одинаковая задача

После согласования использовать изолированный маленький репозиторий:

> Импорт локального CSV с обращениями, проверка обязательных колонок, фильтр по категории, просмотр записи и экспорт отфильтрованного набора.

Фиксированные AC: valid import, missing-column rejection, корректная работа с quoted comma/Unicode, empty result, совпадение export с выбранным filter. Без сети, платных API и реальных персональных данных.

### Дизайн

- Две независимые копии одного baseline, одинаковые fixtures, stack и rubric.
- A: Spec Kit **1.3.3**, OMP integration `omp`, PowerShell scripts.
- B: OpenSpec **1.17.0**, target `oh-my-pi`.
- Отдельный optional baseline C: минимальный OMP, без framework.
- Одинаковые model/reasoning, permissions, число workers, stop conditions и человеческие ответы.
- Не использовать одновременно несколько spec frameworks и не добавлять Superpowers/BMAD.
- Отдельно измерять **default workflow** и **усиленный workflow с одинаковыми review/TDD требованиями**. Иначе Spec Kit optional tests и OpenSpec optional verify создадут нечестное сравнение.

### Последовательность

**A:** constitution → specify → clarify при необходимости → plan → tasks → analyze → implement → converge.

**B:** explore → propose → human review → apply → optional verify → archive. Для OMP команды `/opsx-explore`, `/opsx-propose`, `/opsx-apply`; verify сначала должен присутствовать в выбранном наборе workflows.

В обеих ветках:

1. Проверить происхождение/version и generated files.
2. Проверить распознавание OMP commands/skills без product edits.
3. Зафиксировать plan и одинаковые AC.
4. Проверить ownership/dependency decomposition.
5. После первой выполненной задачи преднамеренно начать свежую session и проверить recovery.
6. Провести одинаковое независимое blind review.
7. Выполнить один fix/re-review цикл.
8. Проверить итоговый общий сценарий и отсутствие неожиданных writes.

### Метрики и acceptance

| Область | Что записывать |
|---|---|
| Интеграция | Команды обнаружены; flags корректны; Windows paths/Unicode не ломаются |
| Требования | Доля AC в specs/tasks; придуманные требования; нерешённые ambiguity |
| Декомпозиция | End-to-end slices, dependency correctness, shared-file collisions |
| Recovery | Нет повторного выполнения completed tasks; корректный next task |
| Качество | Пройденные AC, regression defects, actionable review findings |
| Издержки | Время до согласованного плана/готового результата, turns/tokens при доступности, human interventions |
| Safety | Никаких unapproved installs/network/settings/commits; inventory созданных файлов |

**Проходит квалификацию:** все фиксированные AC, успешный recovery, нет critical/high findings, нет неожиданных writes. При равном качестве выигрывает вариант с меньшей coordination/context cost. Если оба framework не дают измеримой пользы против baseline — остаётся минимальный OMP.

---

## 9. Какие современные практики заимствовать — только по потребности

- **Независимые workers** — когда задачи реально разделяются по ownership; не ради числа агентов.
- **Evaluator–optimizer** — когда есть чёткая rubric и исправление измеримо; генератор и evaluator имеют разные роли.
- **Bounded scoped re-review** — когда исправления сами создают регрессии; не полное новое ревью каждого раунда.
- **Durable hand-off** — когда session compaction приводит к потере progress.
- **TDD/fixtures** — для детерминированных парсеров, validation, contracts и регрессий; не обещание проверить ими качество любого AI-ответа.

Первичные источники:

1. [Anthropic: Building effective agents](https://www.anthropic.com/research/building-effective-agents), опубликовано 2024-12-19; страница предупреждает об изменении tooling landscape. Документирует simplicity, independent parallel sections, orchestrator-workers, evaluator–optimizer и stopping conditions. Это источник паттернов, не основание устанавливать новый framework.
2. [Superpowers 7.0.2 SDD](https://github.com/obra/superpowers/blob/v7.0.2/skills/subagent-driven-development/SKILL.md), [re-review contract](https://github.com/obra/superpowers/blob/v7.0.2/skills/subagent-driven-development/re-review-prompt.md): конкретные brief/report/ledger и fix-diff review.
3. [BMAD 6.12.4 review](https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.4/docs/build/review-a-change.md): независимые lenses, проверка последствий findings и возврат к upstream spec при повторяющихся проблемах.

**Итог:** заимствовать понятные правила можно без установки полного пакета. Сейчас обоснован **минимальный OMP workflow**, а не стек из нескольких конкурирующих spec/methodology systems.