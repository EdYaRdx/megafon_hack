# Каталог кейсов

Ниже — назначение существующих папок. Заполненный кейс не обязательно является текущим рекомендуемым checkpoint или acceptance result. Для нового дела копируйте только [`_template/`](../cases/_template/); не редактируйте примеры.

| Кейс | Категория | Назначение и предел |
|---|---|---|
| [`meal-planner-demo/`](meal-planner-demo/) | **Рекомендуемый ознакомительный пример** | Самый связный синтетический workflow с brief/input, source/evidence/claims, options, decision, двумя стратегиями, test plan и R1/R2. Не user research и не продуктовый спрос. |
| [`retention-demo/`](retention-demo/) | Историческая демонстрация | Синтетическое дело с retention cohorts и revisions; определение D30/eligibility остаётся неопределённым в своём контексте. Не переиспользовать как одобренную метрику. |
| [`unseen-shelf-alerts-20261114/`](unseen-shelf-alerts-20261114/) | Историческая демонстрация / QA | Synthetic R1/R2; ratios — агрегаты записей, не conversions/causal outcome. Не считать новым clean checkpoint. |
| [`fresh-start-demo/`](fresh-start-demo/) | Историческая демонстрация | Созданное в OMP synthetic дело; не чистая acceptance-проверка coding assistant. |
| [`public-source-retention-smoke/`](public-source-retention-smoke/) | QA fixture | Одна static public-page попытка и synthetic retention; reviewer caveat по источнику сохраняется. Не host/site general acceptance. |
| [`retention-f1-demo/`](retention-f1-demo/) | QA fixture | Малый синтетический fixture для retention/cohort calculation; не кейс реальных данных. |
| [`service-launch-f3/`](service-launch-f3/) | QA fixture | Сценарные synthetic constraints/economics и alternatives; числа не подтверждают спрос или окупаемость. |
| [`source-injection-demo/`](source-injection-demo/) | QA fixture | Материал с недоверенной директивой для prompt/source-handling диагностики; не security certification. |
| [`resume-failure-demo/`](resume-failure-demo/) | QA fixture | Synthetic failure/resume scenario; failure fixture не означает успешную динамическую recovery проверку. |
| [`offer-terms-demo/`](offer-terms-demo/) | **Incomplete / legacy fixture** | Частичные synthetic offer terms и revisions; нет полного decision/strategy/test-plan checkpoint. Не показывать как complete strategy. |
| [`_template/`](../cases/_template/) | Новый кейс | Исходные файлы дела и документированный single-writer revision/approval protocol. Копировать в новый каталог, не заполнять шаблон прямо. |

Классификация говорит о природе файла, а не о том, пройдены ли новые F1–F5 targeted checks. См. [evaluation](../docs/evaluation.md) и [implementation status](../docs/implementation-status.md).
