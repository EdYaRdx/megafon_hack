import datetime
import hashlib
import json
from pathlib import Path

case = Path(__file__).resolve().parents[1]
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
notes_path = case/'research/notes.json'
notes = json.loads(notes_path.read_text(encoding='utf-8'))
sources = [dict(id='S-001',url='inputs/Пример брифа.pdf',publisher='UNKNOWN; provided by user',title='Пример брифа.pdf',published='UNKNOWN',version='user-supplied PDF, 11 pages',retrieved_at=now,locator='стр. 1–11; таблица стр. 3, экономика стр. 9, ресурс стр. 11',snapshot='inputs/Пример брифа.pdf',sha256=digest(case/'inputs/Пример брифа.pdf'),status='OBSERVED',limitations='Все показатели учебные; автор и соответствие оригиналу организатора независимо не установлены. Происхождение: inputs/provenance.json')]
for s in notes['sources']:
    sources.append({**{k:v for k,v in s.items() if k not in ['note','limits']},'version':s['published'],'retrieved_at':now,'snapshot':'research/notes.json','snapshot_locator':s['id'],'sha256':digest(notes_path),'status':'DOCUMENTED','limitations':s['limits']+' Сохранена заметка извлечения, не оригинал страницы.'})
sources.append(dict(id='S-008',url='calculations/results.json',publisher='local deterministic Python calculation',title='Разрывы и границы учебного расчёта',published=now,version='calculate.py; receipt.json records exact command and runtime',retrieved_at=now,locator='table; target_minus_no_change; family_net_additions; activity; profit_boundary',snapshot='calculations/results.json',sha256=digest(case/'calculations/results.json'),status='OBSERVED',limitations='Проверяет арифметику, не прогноз спроса или причинный эффект; inputs and hashes in calculations/receipt.json'))
evidence = [
 dict(id='E-001',source_id='S-001',locator='стр. 1–2, Связь для близких и собственных устройств; Что подготовить',summary='Оператор вымышленный, два сегмента, уже существуют распределение общего пакета и переключение своих номеров; решения Q1/Q2; требуется один документ из пяти частей.',extraction_method='Windows.Media.Ocr ru + visual page 1',review_status='verified',limitations='Частоты проблем и клиентские истории не заданы.'),
 dict(id='E-002',source_id='S-001',locator='стр. 3, Рынок и исходные показатели, таблица все пять строк и определения активности/активации',summary='Учебные базы и четыре колонки показателей; метрики семей и владельцев различаются; знаменатель активации включает все созданные группы, включая непринятые приглашения.',extraction_method='OCR; numeric column order verified visually on rendered page 3',review_status='verified',limitations='План и прогноз без изменений — условия задания, не наблюдаемый эффект продукта.'),
 dict(id='E-003',source_id='S-001',locator='стр. 11, Кто нужен / Что известно в начале работы',summary='Разработка Q2: предварительно три человеко-месяца; по половине ставки дизайнера и аналитика не выделены; один человеко-месяц проверки не подтверждён.',extraction_method='OCR + visual page 11',review_status='verified',limitations='Нет ставки труда, сметы, состава команды и подтверждения зависимостей.'),
 dict(id='E-004',source_id='S-001',locator='стр. 9, Как рассчитать прибыль и окупаемость',summary='База 279 млн руб., цель 285 млн руб.; 500 руб. за дополнительный оплаченный номеро-месяц; учитывать только месяцы в плановом году; разработку считать отдельно.',extraction_method='OCR + visual page 9',review_status='verified',limitations='Это учебная ставка, не ARPU, выручка или маржа реального оператора.'),
]
for eid,sid in [('E-005','S-002'),('E-006','S-003'),('E-007','S-004'),('E-008','S-005'),('E-009','S-006'),('E-010','S-007')]:
    s = next(x for x in notes['sources'] if x['id']==sid)
    evidence.append(dict(id=eid,source_id=sid,locator=s['locator'],summary=s['note'],extraction_method='web open of specified primary-source section; analyst paraphrase in research/notes.json',review_status='verified',limitations=s['limits']))
evidence.append(dict(id='E-011',source_id='S-008',locator='target_minus_no_change; family_net_additions; activity; profit_boundary; calculations/receipt.json stdout',summary='Расчёт успешно выполнен: до целей +6 млн руб., +3000 активных семей, +4000 подключённых семей, +1000 владельцев, +15 п.п. активации; 12000 дополнительных оплаченных номеро-месяцев при нулевых других вкладах и новых прямых расходах.',extraction_method='Python 3.12, calculate.py reading pinned PDF-derived text; receipt PASS exit 0',review_status='verified',limitations='Нет оценки эффекта и стоимости; интервалы и окупаемость UNKNOWN.'))
claims = [
 ('C-001','В брифе два сегмента; распределение общего пакета и переключение своих номеров уже есть.','DOCUMENTED',['E-001'],'Новые экраны сами по себе не создают новую базовую операцию.'),
 ('C-002','Все исходные показатели PDF учебные; цели и прогноз без изменений не доказывают эффект инициативы.','DOCUMENTED',['E-002','E-004'],'Применимость к реальному оператору не установлена.'),
 ('C-003','Ресурс первого запуска не подтверждён целиком; три человеко-месяца разработки — предварительный объём, не три разработчика на квартал.','DOCUMENTED',['E-003'],'Оценка трудоёмкости вариантов и стоимость UNKNOWN.'),
 ('C-004','Плановые разрывы составляют 6 млн руб., 3000 активных семей, 4000 подключённых семей, 1000 владельцев и 15 п.п. активации.','OBSERVED',['E-011'],'Это арифметика учебных колонок, не установленный вклад выбранной проблемы.'),
 ('C-005','Для +6 млн руб. только за счёт удержания требуется 12000 дополнительных оплаченных номеро-месяцев в плановом году при отсутствии других вкладов и новых прямых расходов.','OBSERVED',['E-004','E-011'],'Новые прямые расходы повышают границу; дополнительный платёж без контрфактуала не равен удержанию.'),
 ('C-006','Частота, тяжесть и своевременная устранимость причин у клиентов учебного оператора неизвестны.','UNKNOWN',['E-001','E-002'],'Ни число обращений без знаменателя, ни внешний перечень причин не устанавливают распространённость.'),
 ('C-007','Своевременный сигнал с переходом к существующей операции может уменьшать предотвратимые ограничения семейного интернета.','HYPOTHESIS',['E-001','E-006','E-008'],'Эффект и пригодный триггер UNKNOWN; в банковском исследовании часть ранних предупреждений не помогала.'),
 ('C-008','Общий кабинет требует самостоятельного сравнения с тем же сигналом и существующей операцией, если нужно оправдать дополнительные затраты именно на кабинет.','INFERENCE',['E-001','E-007','E-008'],'Наличие сервиса у конкурента не доказывает превосходства.'),
 ('C-009','При неоплате собственных номеров предупреждение или автопополнение являются отдельными механизмами; они не устраняют разряд батареи или проблемы покрытия.','INFERENCE',['E-001','E-009','E-010'],'Приоритет, спрос, разрешения и техническая доступность UNKNOWN.'),
 ('C-010','Минимальный следующий диагностический шаг должен различить исчерпание пакета, неоплату, непонятные начисления и недоступность устройства до выбора первого сегмента.','INFERENCE',['E-001','E-010'],'Это аналитическое предложение; доступ к данным и исследование с людьми не разрешены.'),
 ('C-011','Для 8000 активных при 12000 подключённых доля активных должна быть 66,67%; один рост подключений с 8000 до 12000 при 62,5% даёт 2500 из требуемых 3000 дополнительных активных.','OBSERVED',['E-011'],'Декомпозиция тождества не устанавливает причину роста.'),
 ('C-012','Правила ролей другого оператора нельзя переносить вместо отзывного согласия, заданного учебным брифом.','INFERENCE',['E-001','E-005'],'Требования брифа управляют дизайном этого дела; юридическое заключение не выполнялось.')
]
claim_rows = [dict(id=i,text=t,status=s,evidence_ids=e,valid_as_of='2026-11-20',limitations=l,supersedes=[]) for i,t,s,e,l in claims]
for filename,objects in [('sources.jsonl',sources),('evidence.jsonl',evidence),('claims.jsonl',claim_rows)]:
    path=case/filename
    if path.read_bytes().strip():
        raise RuntimeError(f'Refusing duplicate initial ledger write: {filename}')
    with path.open('ab') as f:
        for obj in objects:
            f.write((json.dumps(obj,ensure_ascii=False,separators=(',',':'))+'\n').encode('utf-8'))
print(json.dumps({'sources':len(sources),'evidence':len(evidence),'claims':len(claim_rows)},ensure_ascii=False))
