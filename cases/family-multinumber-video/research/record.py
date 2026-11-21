"""Append the actual source/evidence/claim and attempt records once; never rewrite journals."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOW = datetime.now(timezone.utc).isoformat()
def digest(rel):
    return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
def append(name, rows):
    path = ROOT / name
    old = path.read_bytes()
    existing = [json.loads(x) for x in old.splitlines() if x.strip()]
    ids = {r.get('id') for r in existing}
    assert all(r['id'] not in ids for r in rows), 'Refuse duplicate IDs'
    payload = (b'\n' if old and not old.endswith(b'\n') else b'')
    payload += ''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows).encode('utf-8')
    with path.open('ab') as stream:
        stream.write(payload)

source_specs = [
 ('S-001','inputs/brief.pdf',None,'Пользователь; автор PDF UNKNOWN','Связь для близких и собственных устройств','с. 1–11','UNKNOWN','visual full-page review Windows.Data.Pdf + view_image; Windows.Media.Ocr ru secondary','Все числа учебные; происхождение независимо не сверено; OCR с. 3 пропускает часть знаков в колонке плана, непроверенные OCR-ячейки не используются'),
 ('S-002','inputs/user-scope.md',None,'Пользователь, руководитель продукта','Подтверждение постановки','пункты 1–2','2026-11-21','user message saved verbatim','Подтверждение scope, не выбор направления и не approval запуска'),
 ('S-003','sources/S-003-method.md','https://www.gov.uk/service-manual/measuring-success/usability-benchmarking-a-website-or-whole-service','GOV.UK User research community','Usability benchmarking a website or whole service','Choosing tasks to test; What to measure; Analyse the data; Running future rounds of benchmarking','2018-08-06','web open + verified paraphrase','Локальный snapshot — проверенный пересказ, не полный HTML. Только методика, не эффект телеком-продукта'),
 ('S-004','sources/S-004-method.md','https://www.gov.uk/service-manual/measuring-success/measuring-completion-rate','GOV.UK Performance analysis community','Measuring completion rate','Calculate completion rate; When a transaction has failed; Measure completion rates for assisted digital support','2016-03-31; updated 2021-02-19','web open + verified paraphrase','Проверенный пересказ; общая исходная метрика допускает помощь, в нашем task-success помощь выделена отдельно'),
 ('S-005','sources/S-005-method.md','https://docs.stripe.com/api/idempotent_requests','Stripe','Idempotent requests','абзацы о повторе и сохранении результатов; веб-строки 16–23','UNKNOWN','web open + verified paraphrase','Механизм другого API; не подтверждает возможностей оператора; рекомендации установки на странице проигнорированы'),
]
sources=[]
for sid,snap,url,pub,title,loc,published,method,limits in source_specs:
    sources.append(dict(id=sid,url=url,local_path=snap,publisher=pub,title=title,published=published,version='provided file' if sid=='S-001' else 'retrieved version',retrieved_at=NOW,locator=loc,snapshot=snap,sha256=digest(snap),status='DOCUMENTED',extraction_method=method,limitations=limits))
append('sources.jsonl',sources)
e_specs=[
 ('E-001','S-001','inputs/brief.pdf, с. 1, «Связь для близких и собственных устройств»','Вымышленный оператор; две аудитории и необходимость выбрать первый сценарий; плановый год и третий год.'),
 ('E-002','S-001','inputs/brief.pdf, с. 1 «Как люди пользуются связью сегодня», с. 5 «Покажите весь путь»','Передача интернета и переключение номеров уже существуют; совместимость тарифа, остаток, полномочия, отдельные разрешения и подтверждение операции обязательны.'),
 ('E-003','S-001','inputs/brief.pdf, с. 3 «Рынок и исходные показатели», таблица и определения; с. 6','Доступные базы 100 тыс. домохозяйств / 40 тыс. владельцев; пять KPI и разные единицы; знаменатель 14-дневной активации — все созданные группы зрелой когорты.'),
 ('E-004','S-001','inputs/brief.pdf, с. 4 «Обоснуйте первый приоритет», последние абзацы; с. 6 «От предложения до подключения»','Частоты причин и истории конкретных клиентов не даны; числовой разбивки по каналам нет. Причины / спрос / предотвратимость неизвестны.'),
 ('E-005','S-001','inputs/brief.pdf, с. 9 «Как рассчитать прибыль и окупаемость»','База 279 млн, цель 285 млн; ставка 500 руб. за дополнительный оплаченный месяц номера; новые прямые расходы вычитаются; инвестиции и удержание проверяются отдельно.'),
 ('E-006','S-001','inputs/brief.pdf, с. 1, с. 10 таблица кварталов, с. 11 таблица ресурсов и «Что делать при отклонении от плана»','Q1 — решение о пилоте, Q2 — расширение / доработка / остановка; на Q2 предварительно 3 человеко-месяца разработчиков; дизайн и аналитика по 0,5 ставки не выделены, тестирование 1 человеко-месяц не подтверждено. Отзыв доступа и двойная операция требуют остановки.'),
 ('E-007','S-002','inputs/user-scope.md, пункты 1–2','Пользователь подтвердил учебные данные / KPI, отсутствие дополнений, свою роль руководителя продукта и сохранение окончательного выбора за собой.'),
 ('E-008','S-003','https://www.gov.uk/service-manual/measuring-success/usability-benchmarking-a-website-or-whole-service#what-to-measure; также Choosing tasks to test / Analyse the data','Методика поддерживает реалистичные задачи с правильным результатом, наблюдение успеха, времени и отказа и анализ причин неудач.'),
 ('E-009','S-004','https://www.gov.uk/service-manual/measuring-success/measuring-completion-rate#calculate-completion-rate; #measure-completion-rates-for-assisted-digital-support','Знаменатель включает начатые неудачные и частичные транзакции; помощь можно измерять отдельно. Самостоятельный успех — явная адаптация нашего контракта.'),
 ('E-010','S-005','https://docs.stripe.com/api/idempotent_requests, абзацы 16–23 веб-представления','Ключ повторной операции — пример предотвращения повторного исполнения в другом API; гарантии имеют ограничения и требуют проверки в системе оператора.'),
 ('E-011','S-001','calculations/results.json; calculations/run.py; inputs/brief.pdf, с. 3,9; sources/S-001-ocr/page-03.txt, page-09.txt','Запущенный Python 3.12.14 проверил hash PDF и входы OCR, сверенные визуально; результаты: 6 млн руб. разрыв, 12000 номеро-месяцев при C=O=0, +4000 семей / +1000 владельцев / +3000 активных / +15 п.п. к сценарию без изменений. При 12000 групп и прежних 62,5% активности получаются 7500 активных, а не 8000.'),
]
evidence=[dict(id=eid,source_id=sid,locator=loc,summary=summary,extraction_method='deterministic Python + visually checked machine OCR' if eid=='E-011' else ('web source inspection' if sid in {'S-003','S-004','S-005'} else 'visual full-page review' if sid=='S-001' else 'user statement'),review_status='verified',limitations='Учебный контекст; методика не доказывает эффект. Для производных чисел см. расчётный receipt.') for eid,sid,loc,summary in e_specs]
append('evidence.jsonl',evidence)
c_specs=[
 ('C-001','DOCUMENTED',['E-001','E-003'],'Кейс вымышленный, числа учебные; рыночные показатели реальных операторов не применяются.'),
 ('C-002','DOCUMENTED',['E-001','E-003'],'Семьи и владельцы собственных номеров — разные сценарии и единицы; размер доступной базы не устанавливает превосходство механизма.'),
 ('C-003','DOCUMENTED',['E-002'],'Первый кандидат может использовать существующую передачу интернета, но только при тарифной совместимости, достаточном остатке, полномочиях и разрешениях; успех требует подтверждения биллинга.'),
 ('C-004','UNKNOWN',['E-004'],'Частота причин, своевременная устранимость, спрос, воронки и преимущество семей перед владельцами по предотвращаемому ущербу неизвестны.'),
 ('C-005','DOCUMENTED',['E-001','E-006'],'Учебная стратегия требует года, ориентира на третий год и решений руководителя по итогам Q1/Q2.'),
 ('C-006','DOCUMENTED',['E-006'],'Разработка ограничена предварительными тремя человеко-месяцами Q2; достаточность, ставки и необходимые дизайн/аналитика/тестирование не подтверждены.'),
 ('C-007','DOCUMENTED',['E-007'],'Пользователь — владелец окончательного решения; разрешены исследование и рекомендация учебного кейса, направление и исполнение не выбраны.'),
 ('C-008','DOCUMENTED',['E-003','E-005'],'Сценарий без изменений: 279 млн руб., 5000 активных групп, 8000 подключённых семейных групп, 1000 владельцев, 45% 14-дневной активации; цели: 285 млн / 8000 / 12000 / 2000 / 60%.'),
 ('C-009','OBSERVED',['E-011'],'Разрыв 6 млн руб. при ставке 500 руб. требует 12000 дополнительных оплаченных номеро-месяцев при C=O=0; цель по семьям выше базового сценария на 4000 групп. Это границы, не прогноз спроса или удержания.'),
 ('C-010','INFERENCE',['E-008','E-009'],'Проверка самостоятельного выполнения задачи должна учитывать все eligible started attempts, отказы и неудачи; удобство проверяется отдельно от клиентского и денежного исхода.'),
 ('C-011','INFERENCE',['E-010','E-002','E-006'],'Повтор, неизвестный результат и отзыв доступа необходимо проверять до пилота; описание идемпотентности Stripe не подтверждает гарантии оператора.'),
 ('C-012','INFERENCE',['E-001','E-002','E-003','E-004','E-006'],'Узкая помощь уже подключённым семьям через своевременный сигнал и существующую передачу — условный первый кандидат, связанный с семейными KPI. Предпочтение предварительное: частоты проблем, достигаемый эффект и стоимость неизвестны; до выбора пилота нужна сравнительная диагностика с собственными номерами и начислениями.'),
 ('C-013','UNKNOWN',['E-004','E-005','E-011'],'Численного прогноза эффекта, затрат, нужного размера выборки и окупаемости по материалам нет. Меньше недельных перебоев не означает дополнительные платные номеро-месяцы.'),
 ('C-014','INFERENCE',['E-003','E-005','E-011'],'До данных базовый рабочий прогноз сохраняет условные показатели без изменений; при пилоте без эффекта прибыль становится 279 млн минус новые прямые расходы. Цели остаются целями, не предсказанием.'),
]
append('claims.jsonl',[dict(id=cid,text=txt,status=status,evidence_ids=eids,valid_as_of='2026-11-21',limitations='Рекомендация условна; см. locators в evidence.jsonl и решающих документах',supersedes=[]) for cid,status,eids,txt in c_specs])

events=[
 ('A-001','user consent','SUCCESS','Пользователь согласовал cases/family-multinumber-video и указал локальный PDF.',None),
 ('A-002','create','SUCCESS','Python -B tools/case_workspace.py create cases/family-multinumber-video; cwd project; exit 0; stdout CREATED; stderr empty.',None),
 ('A-003','classify','SUCCESS','Прочитан marker checkpoint-v1/UNINITIALIZED; Python -B tools/case_protocol.py classify cases/family-multinumber-video; exit 0; stdout FRESH; stderr empty.',None),
 ('A-004','PDF dependencies probe','FAILED','Первый python -c importlib.util probe: NameError name pypdf is not defined из-за передачи кавычек; exit 1.',None),
 ('A-005','PDF dependencies probe stdin','SUCCESS','Повтор через stdin: pypdf/pdfplumber/fitz/reportlab false; pdftoppm/pdfinfo/mutool не найдены. Ничего не установлено.','A-004'),
 ('A-006','CUA inventory','LIMITED','Browser access host unavailable; native app inventory available.',None),
 ('A-007','CUA Yandex read','FAILED','getApp window 35129448: window is minimized.',None),
 ('A-008','CUA Explorer read','FAILED','getApp window 10749364: window is minimized.',None),
 ('A-009','CUA launch Yandex','UNKNOWN','launch_app completed, inventory remained same; no successful PDF read.','A-007'),
 ('A-010','CUA Yandex retry','FAILED','getApp window 35129448 still minimized; CUA completion_summary issued.','A-009'),
 ('A-011','Node PDF packages','UNAVAILABLE','pdfjs-dist, pdf-parse, @oai/artifact-tool imports unavailable; no installation.',None),
 ('A-012','WinRT PDF metadata','SUCCESS','Windows.Data.Pdf loaded source, PageCount 11; no installation.',None),
 ('A-013','WinRT render','FAILED','AsTask overload with 1 argument not found; render directory created, no PNG successfully reported.',None),
 ('A-014','WinRT render retry','SUCCESS','Reflection selected non-generic IAsyncAction AsTask; rendered all 11 pages to sources/S-001-pages; exit 0; source SHA256 558d2c665caa4f4954135c8bbfb69d791e398dcdc5b625d5ded7bdb2d0eb0fa5.','A-013'),
 ('A-015','visual source read','SUCCESS','view_image opened all 11 complete pages in batches 1–4,5–8,9–11; findings in sources/S-001-reading.md.',None),
 ('A-016','source copy and intake save','SUCCESS','Copied user PDF to inputs/brief.pdf; matching source/copy SHA256; apply_patch saved brief/state/reading notes.',None),
 ('A-017','scope response','SUCCESS','Owner confirmed educational case, unchanged brief KPIs, no additional data; inputs/user-scope.md saved.',None),
 ('A-018','web methodology search','SUCCESS','Queries for GOV.UK usability, Microsoft experimental units, Stripe idempotency; no actual-operator KPI used.',None),
 ('A-019','source S-003 web open','SUCCESS','Opened GOV.UK usability benchmarking; inspected Choosing tasks / What to measure / Analyse / future rounds; saved verified paraphrase.',None),
 ('A-020','source S-004 web open','SUCCESS','Opened GOV.UK Measuring completion rate; inspected denominator and assisted support sections; saved verified paraphrase.',None),
 ('A-021','source S-005 web open','SUCCESS','Opened Stripe Idempotent requests paragraphs 16–23; no install/API call performed; saved verified paraphrase.',None),
 ('A-022','Windows OCR','SUCCESS','Windows.Media.Ocr ru on Windows NT 10.0.26200.0; all 11 rendered pages -> sources/S-001-ocr; table estimate/no-change/target cells visually checked; plan cell OCR omission noted.',None),
 ('A-023','critical calculations','SUCCESS','Exact executed command: & <USER_HOME>/AppData/Roaming/uv/python/cpython-3.12-windows-x86_64-none/python.exe -B -X utf8 cases/family-multinumber-video/calculations/run.py; cwd <WORKSPACE>; exit 0; stderr empty; full stdout JSON equals calculations/results.json; version/inputs/hashes/formulas/units/rounding/missing rules inside result.',None),
 ('A-024','evidence record','SUCCESS','Initial sources/evidence/claims recorded append-only by research/record.py; user-scope and method notes saved; errors/retries retained.',None),
]
append('activity.jsonl',[dict(id=aid,recorded_at=NOW,event_time='UNKNOWN',operation=op,result=status,details=detail,retry_of=retry,model='UNKNOWN',cost='UNKNOWN',elapsed_seconds='UNKNOWN') for aid,op,status,detail,retry in events])
print(json.dumps({'status':'APPENDED','sources':len(sources),'evidence':len(evidence),'claims':len(c_specs),'activity':len(events),'recorded_at':NOW}))
