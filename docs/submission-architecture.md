# Архитектура и ограничения

**Тип продукта:** project folder для coding assistant. Файлы содержат инструкции и данные дела; исполняемый workflow runtime не встроен. Шесть канонических Skills находятся в `.agents/skills/<name>/SKILL.md`; общего или host-specific дублирующего дерева нет.

## Маршрутизация Skills

Корневой [`AGENTS.md`](../AGENTS.md) задаёт порядок, safety/evidence правила и переадресует к единственной процедуре соответствующего этапа:

| Этап | Канонический Skill | Результат |
|---|---|---|
| Уточнение задачи | [`intake`](../.agents/skills/intake/SKILL.md) | Решение, владелец, аудитория, срок, границы, unknowns |
| Источники и доказательства | [`evidence-research`](../.agents/skills/evidence-research/SKILL.md) | Source locators, evidence, claims и пробелы |
| Варианты и выбор | [`options-decision`](../.agents/skills/options-decision/SKILL.md) | Не менее трёх реальных вариантов с возражениями |
| Product + communication strategy | [`strategy-communication`](../.agents/skills/strategy-communication/SKILL.md) | Согласованное направление, аудитория и проверяемое обещание |
| Проверка | [`experiment-design`](../.agents/skills/experiment-design/SKILL.md) | Comparator, метрики, знаменатели, период и guardrails |
| Пауза/изменение данных | [`resume-revise`](../.agents/skills/resume-revise/SKILL.md) | Проверенное восстановление и новая ревизия |

Это routing по проектным инструкциям, не кодовый router. Host может не обнаружить Skill, иметь другой набор инструментов или иначе следовать файлам; это требует отдельной host-проверки.

## Data flow и доказательства

```mermaid
flowchart LR
  Q[Brief и материалы] --> I[intake]
  I --> S[Source records]
  S --> E[Evidence]
  E --> C[Claims]
  C --> O[Options и decision]
  O --> P[Product strategy]
  P --> M[Communication strategy]
  M --> T[Test plan]
  T --> H[Human decision / approval]
  H --> R[Revision и state]
  R --> E
```

Путь **Source → Evidence → Claim → Decision** хранит происхождение и контекст вывода. Наличие URL не означает, что он поддерживает тезис. У существенного claim должны быть source/evidence IDs, точный locator и ограничения.

| Статус | Значение |
|---|---|
| `OBSERVED` | Непосредственно наблюдаемое в доступном материале/событии; синтетический scope отмечается отдельно |
| `DOCUMENTED` | Утверждение или правило, опубликованное в указанном документе; не обязательно проверено в реальном мире |
| `INFERENCE` | Вывод из явно названных оснований; не прямое наблюдение |
| `HYPOTHESIS` | Проверяемое предположение, не установленный факт |
| `UNKNOWN` | Данных недостаточно, источник/инструмент недоступен либо исход не проверен |

`CLAIMED` может встречаться в старых/локальных схемах, но не заменяет перечисленные выше различения. Сохраняйте конфликтующие периоды, определения и источники отдельно.

## Варианты, стратегия и проверка

До рекомендации сравниваются минимум три качественно разные действия; обычно это конкретный status quo, ограниченная проверка/изменение и остановка/закрытие. Для каждого нужны последствия, компромиссы и сильное возражение. Это не три формулировки одного решения.

Product strategy описывает аудиторию/задачу, ценность, направление, отказы и связь пользы с затратами/доходом. Communication strategy выводится из выбранного продукта: кому, в какой ситуации и с каким барьером сообщать; какое обещание подтверждено; какие доказательства и каналы уместны. Необоснованное обещание остаётся гипотезой или исключается.

План проверки называет предполагаемое изменение, comparator, аудиторию/выборку, числитель и знаменатель, период и зрелость когорты, защитные метрики, порог/действие и условие пересмотра. Неизвестная формула, определение события, порог или цена остаются `UNKNOWN`, не подставляются догадкой. Расчётный receipt содержит реально использованные входы/locators, формулу, единицы, способ исполнения и результат; если команда не запускалась, это `NOT RUN`.

## File protocol: revisions и active claims

- Запись дела отделена от template, методических `references/` и постоянных Skills. JSONL журналы источников, доказательств, claims и активности не переписывают историю.
- Каждая новая revision имеет уникальный immutable ID и одного parent. Сохраняются точные snapshots решения, вариантов, обеих стратегий, test plan, state и decision dependencies, нужных для восстановления.
- `manifest.json` перечисляет snapshots/dependencies, их SHA-256, revision/parent, `COMPLETE` status и explicit `active_claim_ids`. Проверка manifest и перечисленных hash обязательна перед использованием checkpoint.
- После подготовки полных файлов manifest записывается последним. Root `state.md` и `decision.md` переводятся на проверенный checkpoint, `ACTIVE.json` записывается последним как selector по revision ID + manifest SHA-256.
- Selector не assumed atomic. Неполный manifest, hash mismatch, неопределённая ветка или несогласованность root state/decision/selector означает `INCOMPLETE`/`CONFLICT`: остановиться, не смешивать ревизии и вручную восстановить прежний полный снимок. Timestamps и порядок листьев не выбирают текущую ревизию.
- Successor claim выбирается только явным списком active claims в COMPLETE manifest и согласованными `state.md`/`decision.md`. `supersedes` и порядок строк JSONL не выбирают claim; неоднозначный fork блокирует рекомендацию.
- Human approval — отдельная append-only запись, привязанная к точному action, scope, revision ID, полному manifest hash и основанию. Изменение revision/hash/action/scope/решающего основания требует нового одобрения. Approval не расширяет host permissions и не технически enforced.

Legacy кейсы без такого протокола сохраняют исторические ограничения; недостающие снимки не реконструируются задним числом.

## Host, переносимость и безопасность

Не поставляются и не фиксируются модель, provider, биллинг, host, skill loader, OS permissions или расчётный tool. Product runtime не требует OMP. `.omp/`, research launchers и исследовательские профили не являются runtime-зависимостями.

Папка — формат переносимых материалов, не гарантия одинакового запуска между hosts. Реальный доступ к файлам/сети/командам определяет host. Инструкции к недоверенному содержимому предписывают считать его данными, а не командами, но не создают OS isolation. Останавливайтесь перед реальным контактом, расходами, чувствительными данными, публикацией или запуском; требуется отдельное человеческое разрешение.

Acceptance status и локаторы доказательств — в [evaluation](evaluation.md) и [implementation status](implementation-status.md); текущий динамический runbook — [clean-host E2E](clean-host-e2e-runbook.md).