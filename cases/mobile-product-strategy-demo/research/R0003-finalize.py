"""Finalize the authorized existing draft. Publication uses unchanged shared gates."""
import datetime
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

case = Path(__file__).resolve().parents[1]
project = case.parents[1]
draft = case / 'drafts/r0003-independent-audit'
rev = case / 'revisions/R0003'
receipts = case / 'receipts'
views = ['options.md', 'decision.md', 'strategy-product.md', 'strategy-communication.md', 'test-plan.md', 'state.md']
active = [f'C-{i:03d}' for i in [1,2,3,4,5,6,7,8,9,11,12,13,14,17,18,19,20,22,23,25]]
active_text = ', '.join(active)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()

def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as f:
        if isinstance(data, str): f.write(data.rstrip()+'\n')
        else: json.dump(data, f, ensure_ascii=False, indent=2); f.write('\n')

def append(name, rows):
    path = case / name
    data = path.read_bytes()
    old = [json.loads(x) for x in data.splitlines()]
    key = 'approval_id' if name == 'approvals.jsonl' else 'id'
    ids = {r[key] for r in old}
    if any(r[key] in ids for r in rows) or (data and not data.endswith(b'\n')):
        raise RuntimeError('Unsafe append: '+name)
    with path.open('ab') as f:
        for row in rows: f.write((json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n').encode('utf-8'))

def change(text, old, new):
    if text.count(old) != 1: raise RuntimeError('Expected one saved block: '+old[:100])
    return text.replace(old, new, 1)

def parent_ok():
    base = json.loads((receipts/'R0003-recovery.json').read_bytes())
    if json.loads((case/'ACTIVE.json').read_bytes()) != {'revision_id':'R0002','manifest_sha256':base['base']['manifest_sha256']}:
        raise RuntimeError('Selected parent changed')
    for name, expected in base['history_sha256'].items():
        if sha(case/name) != expected: raise RuntimeError('Published history changed: '+name)
    return base

def shared(args, filename):
    argv = [sys.executable,'-B','-X','utf8',str(project/'tools/case_protocol.py'),*args]
    start = now()
    p = subprocess.run(argv,cwd=project,capture_output=True,text=True,encoding='utf-8')
    r = dict(command_argv=argv,cwd=str(project),started_at_utc=start,finished_at_utc=now(),runtime_version=sys.version,consumer_sha256=sha(project/'tools/case_protocol.py'),exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr)
    save(receipts/filename,r)
    print(p.stdout,end='')
    if p.stderr: print(p.stderr,file=sys.stderr,end='')
    if p.returncode: raise RuntimeError('Shared gate failed; stop without selection')
    return r

def finalized_strategy():
    text = (draft/'strategy.md').read_text(encoding='utf-8')
    text = change(text, '# Проактивная помощь семье — ограниченный пересмотр, DRAFT R0003', '# Проактивная помощь семье — пересмотренная стратегия R0003')
    text = change(text, 'Эта версия не опубликована.', 'R0003 финализирована по согласованному аналитическому scope; фактическую публикацию устанавливают selector и штатные receipts.')
    text = change(text, 'разрешения исполнения нет.', 'разрешения пилота/расходов/внешних действий нет. Решения PO и согласие на gated-публикацию: C-025, S-016 `inputs/R0003-owner-publication.md`, «Разрешённое действие», «Сохраняемые решения»; S-017 `drafts/r0003-independent-audit/owner-decision.md`, «Подготовка Q1», «Владельцы нескольких номеров», «Третий год».')
    text = text.replace('S-012 (`audit-input.md`)', 'S-012 (`drafts/r0003-independent-audit/audit-input.md`)')
    text = change(text, 'Это предложение объёма, не финансирование и не новая санкция исполнения.', 'PO согласовал ограниченный объём как направление дальнейшей проработки и разрешил внутренний план получения оценок/перечень ролей, данных и зависимостей. Бюджет и сотрудники не выделены; пилот/внешние контакты не разрешены. C-025; S-016/S-017, «Подготовка Q1» и «Сохраняемые решения».')
    text = text.replace('неактивный C-019', 'C-019')
    text = change(text, 'Недобор владельцев и числовой ориентир года3 требуют отдельных решений (§7–8).', 'PO принял недобор владельцев как незакрытый компромисс с сохранением цели; закрытие разрыва и реализацияC остаются будущими решениями. Ориентиры года3 остаются гипотезами (§7–8).')
    text = change(text, 'Решение PO не сохранено', 'В R0002 решение PO отсутствовало; теперь принят открытый компромисс с сохранением цели, C-025/S-016/S-017')
    text = change(text, '§7–8: принять явный недобор, запросить отдельную оценку C или пересмотреть ресурс/очередность; ничего не выбрано автоматически. C-021/E-016/E-017', '§7–8: PO осознанно принимает недобор1 000; цель2 000 сохранена, реализацияC не разрешена. Исторический C-021 заменён цепочкой C-024→C-025; E-016/E-017/E-022/E-023')
    text = change(text, 'Это минимальный предлагаемый к оценке и последующему финансированию результат.', 'Этот минимальный объём согласован PO как направление проработки; разрешено внутреннее планирование получения оценок. Финансирование и назначения не предоставлены (C-025/S-016/S-017).')
    text = change(text, 'Текущее поручение охватывает локальный DRAFT; не создаёт бюджет P0, сбор данных или запуск пилота', 'PO разрешил внутренний план получения оценок и перечень ролей/данных/зависимостей; не выделил бюджет/сотрудников и не разрешил сбор закрытых данных/контакты/пилот. Согласие на аналитическую публикацию проверяется отдельно')
    text = change(text, 'Варианты для PO: (а) явно принять недобор/отложить его закрытие при сохранённой цели как незакрытом обязательстве; (б) отдельно запросить оценку проблемы/воронкиC и цены устранения, не запускатьC; (в) пересмотреть ресурс/очередность и цели/срок с явным решением. Ни один не выбран.', 'PO осознанно принимает недобор1 000 как незакрытый компромисс приоритетаA, сохраняя цель2 000. РеализацияC сейчас не разрешена; отдельная оценка/закрытие разрыва и возможный пересмотр ресурса остаются будущими решениями. C-025; S-016 «Сохраняемые решения»; S-017 «Владельцы нескольких номеров».')
    text = text.replace('; C-021).', '; C-025).')
    text = change(text, 'канал — рассмотрение этого DRAFT;', 'канал — внутреннее рассмотрение стратегииR0003;')
    text = text.replace('`calculation-results.json`', '`drafts/r0003-independent-audit/calculation-results.json`')
    text = text.replace('`calculation-receipt.json`', '`drafts/r0003-independent-audit/calculation-receipt.json`')
    text = text.split('## 8. Конкретное решение PO и точка остановки')[0] + '''## 8. Решения PO, разрешённый scope и следующий этап

PO сохранил приоритетA и согласовал ограниченный объём Q1-P0 как направление проработки. Разрешены только внутренний план получения оценок и перечень ролей/данных/зависимостей из §5; бюджет не выделен, сотрудники не назначены, фактические часы/PM/ставки/даты/стоимость UNKNOWN до подтверждения. Реальный пилот и внешние контакты не разрешены. Само получение оценок также требует ресурса; лимит и конкретные владельцы ещё не определены. C-025; S-016 `inputs/R0003-owner-publication.md`, «Сохраняемые решения»; S-017 `drafts/r0003-independent-audit/owner-decision.md`, «Подготовка Q1».

PO осознанно принял недобор1 000 владельцев как открытый компромиссA, сохранил цель2 000 и не разрешил реализациюC. Закрытие разрыва остаётся будущим решением. Ориентиры года3 остаются гипотезами без утверждённого плана/траектории. Основания — C-025/S-016/S-017, разделы о владельцах и третьем годе; неизвестность траектории — C-018/E-020.

Согласие на финализацию и аналитическую публикацию R0003 дано только при успехе неизменённых штатных gates. Оно снимает прежнюю паузу публикации изS-015, сохраняя все ограничения исполнения. Отдельный approval аналитической публикации привязывается к точному complete-manifest SHA-256; его фактическую применимость/использование восстанавливать по approvals и receipts. Новая ревизия/hash, изменённый scope/действие или решающая предпосылка требуют нового применимого согласования. Это не approval пилота, расходов, найма, назначения людей, внешних коммуникаций или обработки закрытых данных и не host permission. C-025; S-016, «Разрешённое действие», «Ограничения и остановка».

Следующий этап после успешной публикации — конкурсная упаковка по отдельному конкретному поручению. Содержательную переработку/новое исследование/получение оценок/пилот автоматически не начинать. В конкурсных материалах сохранять различие целей, условной чувствительности и UNKNOWN; принятие компромисса не закрывает недобор, а публикация не подтверждает эффект или смету.
'''
    for bad in ['DRAFT', 'Ни один не выбран', 'Решение PO не сохранено', 'публикацию запрещает']:
        if bad in text: raise RuntimeError('Stale finalization text: '+bad)
    return text

def prepare():
    base = parent_ok()
    if rev.exists(): raise RuntimeError('R0003 already exists; stop, do not merge')
    if sha(draft/'strategy.md') != base['draft_sha256']['strategy.md']: raise RuntimeError('Draft basis changed')
    # Build every substantive output before any root-view handover.
    strategy = finalized_strategy()
    options = (case/'revisions/D0002/options.md').read_text(encoding='utf-8')
    options = options.replace('Выбор исследовательского приоритета R0002', 'Выбор исследовательского приоритета R0003')
    options = options.replace('C-015', 'C-017')
    options += '''\n## Сохранённые решения и границы R0003

Сравнение механизмов не менялось. PO согласовал ограниченную Q1-подготовку как направление проработки, разрешил внутренний план получения оценок/перечень ролей, данных и зависимостей; не выделил бюджет и сотрудников. Недобор владельцев1 000 принят как незакрытый компромисс при сохранении цели2 000; реализацияC сейчас не разрешена. Ориентиры года3 остаются гипотезами. C-025; S-016 `inputs/R0003-owner-publication.md`, «Сохраняемые решения»; S-017 `drafts/r0003-independent-audit/owner-decision.md`, соответствующие разделы.

Прежние числа условногоA не ранжируют ожидаемую прибыль и не являются собственным прогнозом: C-017/C-022/C-023; S-013 `drafts/r0003-independent-audit/calculation-results.json`, `kpi_reclassification`, `capacity_constraint`, `timing_profiles_not_forecasts`. Ограниченная Q1-подготовка, запускG1 и решениеG2 раздельны; затраты, PM и сроки UNKNOWN до подтверждения. Полная финализированная стратегия — `revisions/D0003/dependencies/strategy.md`, §3–8.
'''
    product = (case/'revisions/D0002/strategy-product.md').read_text(encoding='utf-8')
    product = product.replace('Продуктовая стратегия R0002', 'Продуктовая стратегия R0003')
    product = product.replace('Полный документ: `strategy.md`, части1–5;', 'Полный документ: `revisions/D0003/dependencies/strategy.md`, §1–8;')
    start = product.index('## Ресурс и экономика')
    product = product[:start] + '''## Ресурс, экономика и сохранённые решения

Ограниченный P0 согласован PO как направление проработки. Разрешено внутреннее планирование получения оценок и перечень ролей/данных/зависимостей; бюджет/сотрудники не выделены. Конечный пакетW1–W6, task-level входы для PM/сметы, зависимости и формулы дефицита — `revisions/D0003/dependencies/strategy.md`, §5. Часы/ставки/подтверждённая ёмкость/сроки UNKNOWN. C-003/C-019/C-025; S-001 PDF стр.11; S-016/S-017, «Сохраняемые решения»/«Подготовка Q1».

Собственный обоснованный прогнозA по пятиKPI UNKNOWN. ЦелиPDF и обычный прогноз источника отделены от чувствительности R0002 (C-017; S-001, стр.3,6,10; S-013 `drafts/r0003-independent-audit/calculation-results.json`, `kpi_reclassification`). GP_₽=279000000+500M+O−D, I отдельно. При условныхD1млн/O0 нужныM14000; условныеC88000 требуют взвешенной прибавки7/44=15,91п.п. и необходимого pbar_usual≤37/44≈84,09%. Вес — N_c по учтённым поздним cohort-month ячейкам, не общая доля платящих людей. Это не достаточное условие достижимости; реальная p_usual и устранимая ёмкость UNKNOWN. C-022; S-001, стр.9; S-013 `capacity_constraint` и `maximum_weighted_usual_paid_probability_fraction`. Квартальные M/GP/окупаемость UNKNOWN без времени эффекта и D/O/I; старое распределение предполагает одинаковоеΔ каждой ячейке, C-023/S-014, `calculations/R0002/calculate.py`, строки30,44–53.

PO принимает недобор1000 владельцев при сохранении цели2000 как незакрытый компромиссA; реализацияC сейчас не разрешена. Ориентиры года3 остаются гипотезами, траектория UNKNOWN. C-025/C-018; S-016/S-017, разделы о владельцах/годе3.

## Пересмотр и следующий шаг

P0/запускG1/следующий охватG2 — отдельные решения. При отсутствии входов доступны только разрешённые спецификация/внутренний план; пилот не готов. Применимость/клиентский исход/платёжный эффект различаются; SUCCESS/FAILURE/INCONCLUSIVE и защита — `test-plan.md`. Публикация аналитики не разрешает пилот/расход/контакт. После финализации следующий этап — конкурсная упаковка; дальнейшую переработку автоматически не начинать.
'''
    communication = (case/'revisions/D0002/strategy-communication.md').read_text(encoding='utf-8')
    communication = communication.replace('Коммуникационная стратегия R0002', 'Коммуникационная стратегия R0003')
    communication = communication.replace('Связный документ: `strategy.md`, часть2.', 'Связный документ: `revisions/D0003/dependencies/strategy.md`, §7; решения PO — §8.')
    communication = communication.replace('C-015', 'C-017/C-022/C-023')
    communication += '''\n## Текущее внутреннее сообщение PO и финансам

«A остаётся исследовательским приоритетом; согласовано только направление ограниченной подготовки и внутреннее планирование оценок. PM/стоимость/сроки/эффект неизвестны. Цель2000 владельцев сохранена с принятым открытым недобором1000; год3 — гипотезы». C-025/S-016/S-017: `inputs/R0003-owner-publication.md`, «Сохраняемые решения»; `drafts/r0003-independent-audit/owner-decision.md`, «Подготовка Q1», «Владельцы нескольких номеров», «Третий год». Канал — внутреннее рассмотрение стратегии и будущая конкурсная упаковка; барьер — риск принять целевой сценарий за подтверждённый прогноз. Подтверждение — точные ограничения решения и UNKNOWN, не эффект клиентов. Внешние сообщения не разрешены. Следующий шаг — конкурсные материалы по отдельному поручению, без автоматического пилота/плана финансирования.
'''
    plan = (case/'revisions/D0002/test-plan.md').read_text(encoding='utf-8')
    plan = plan.replace('План проверки A — R0002', 'План проверки A — R0003')
    plan = plan.replace('Основной документ: `strategy.md`, части1,3,5.', 'Основной документ: `revisions/D0003/dependencies/strategy.md`, §4–6.')
    plan += '''\n## Раздельные gates и решения PO в R0003

ОграниченныйP0 согласован только как направление подготовки; разрешены внутренний план получения оценок и перечень ролей/данных/зависимостей. Бюджет/назначения не предоставлены; реальные контакты/пилот/закрытые данные не разрешены. W1–W6 и нужные оценки — финальная стратегия§5. Числовые PM/ставки/стоимость/сроки остаютсяUNKNOWN. G1 отдельно решает конкретный запуск после готовности входов/ресурса/защиты; G2 отдельно рассматривает следующий ограниченный scope/доработку/продление/остановку по зрелым исходам и затратам. Квартал сам не разрешает расширение. C-019/C-020/C-025; S-001 PDF стр.10–11; S-016/S-017, «Подготовка Q1»/«Сохраняемые решения».

PO принял недобор1000 владельцев при сохранении цели2000; отдельная реализацияC не разрешена. Ориентиры года3 гипотетичны. Согласие на gated-публикацию аналитики не заменяет approval будущего исследования/расходов/пилота и host permissions. После публикации — остановка и конкурсная упаковка по отдельному поручению.

## Выполненная независимая арифметическая проверка

S-013, `drafts/r0003-independent-audit/calculation-receipt.json`: фактический argv/cwd/runtime, pinned hashes, exit0, полный stdout/stderr. `calculation-results.json` — `capacity_constraint`, `maximum_weighted_usual_paid_probability_fraction`, `timing_profiles_not_forecasts`, `kpi_reclassification`. УсловныеC88000/M14000 дают необходимое pbar_usual≤37/44≈84,09% с весами N_c по тем же cohort-month ячейкам; это не достаточное условие. Годовая сумма не идентифицирует кварталы: S-014, `calculations/R0002/calculate.py`, строки30,44–53, показывает неявное одинаковоеΔ. C-017/C-022/C-023. Нового клиентского исследования, расчёта реального эффекта или сметы не проводилось.
'''
    decision = f'''# Решение R0003 — A и ограниченная подготовка Q1

- **Decision owner / authority:** пользователь как Product Owner
- **Status:** DECIDED
- **Revision:** D0003
- **Parent revision:** D0002
- **Active claim IDs:** {active_text}
- **Selected direction:** A — проактивная помощь семье через подтверждённый риск и существующую передачу, исследовательский приоритет

## Решения и границы

PO сохранилA, согласовал ограниченныйQ1-P0 как направление дальнейшей проработки и разрешил внутренний план получения оценок/перечень ролей, данных и зависимостей. Бюджет не выделен, сотрудники не назначены, стоимость/трудоёмкость/срокиUNKNOWN. Недобор1000 владельцев принят как незакрытый компромиссA при сохранённой цели2000; реализацияC сейчас не разрешена. Год3 остаётся гипотезами без утверждённого плана. C-025; S-016 `inputs/R0003-owner-publication.md`, «Сохраняемые решения»; S-017 `drafts/r0003-independent-audit/owner-decision.md`, «Подготовка Q1», «Владельцы нескольких номеров», «Третий год».

Публикация аналитики разрешена только после штатных gates; это не approval пилота/расходов/контактов/закрытых данных/реального продукта. Отдельное согласование аналитической публикации имеет точный revision/hash/scope в approvals; текущую применимость будущих действий восстанавливать отдельно. Источник C-025/S-016, «Разрешённое действие», «Ограничения и остановка».

## Варианты и сильные возражения

A сохранён из-за решенияPO и конкретной гипотезы раннего сигнала с существующим действием, не доказанного максимума прибыли. Главный риск — пригодного устранимого случая мало либо помощь невозможна. B/общий кабинет отложен до пользы сверхA с тем же сигналом; риск дополнительного объёма без результата. C/свои номера остаётся будущим вопросом, не разрешённой реализацией; потенциальная лучшая экономикаUNKNOWN. СТАТУС-КВО сохраняет обычное обслуживание и разрывы, служит контролем/исходом при неготовностиA; пересмотрG1. Тарифный резерв вернётся при подтверждённой нехватке объёма с оценкой себестоимости/замещения. Остановка освобождает планируемый ресурс при неприменимости/неприемлемой цене; возврат при новых основаниях. Полное неизменное сравнение — `options.md` и `revisions/D0002/options.md`; C-001/C-007–C-009/C-013/C-014. Затраты и календарь альтернативUNKNOWN.

## Что пересмотрено и что ослаблено

Собственный прогнозA по всем пятиKPI UNKNOWN. Источник S-001 PDF стр.3,6,10 задаёт отдельные обычный прогноз/цели; R0002 чувствительность от целей их не заменяет. C-017/S-013 `drafts/r0003-independent-audit/calculation-results.json`, `kpi_reclassification`; полная таблица и контракты — `revisions/D0003/dependencies/strategy.md`, §3.

При условныхD1млн/O0 дляGP285млн от279млн и ставки500₽ нужныM14000 дополнительных оплаченных NUMBER-месяцев. УсловныеC88000 — не доказанная устранимая ёмкость: необходимое `pbar_usual≤1−14000/88000=37/44≈84,09%`, вес N_c по учтённым поздним cohort-month ячейкам; не общая доля платящих людей и не достаточное условие достижимости. Реальная исходная оплата/эффект/пригодностьUNKNOWN. C-022; S-001 PDF стр.9; S-013 `capacity_constraint`/`maximum_weighted_usual_paid_probability_fraction`, фактический receipt рядом.

Старые квартальные вклады требуют неявного постоянногоΔ по времени; без временного профиля и O/D/I квартальные M/GP/окупаемостьUNKNOWN. C-023/S-014 `calculations/R0002/calculate.py`, строки30,44–53; S-013 `timing_profiles_not_forecasts`. Год3 — C-018 UNKNOWN; историческое удвоение не имеет обоснованной траектории. Подробная проверка семи findings — финальная стратегия§2–7, без новых клиентских наблюдений.

## Подготовка, проверка и условия остановки

КонечныйP0 и входы для сметы — стратегия§5: W1–W6 по одному тарифному сценарию/причине. Нужны task-level часы, фондPM, ставки, подтверждённая доступность/очереди/зависимости и лимит самого оценивания; все числовые входыUNKNOWN. При недоступных обязательных системах — спецификация/явный blocker, не обещание пилота. C-003/C-019, S-001 PDF стр.11.

P0, G1/запуск и G2/следующий ограниченный охват — разные решения. Comparator — обычное обслуживание; назначение по семье, один индексный номер. `p_arm=индексные номера с подтверждённым ограничением из-за объёма в окне / все включённые индексные номера arm`; `Δ=p_usual−p_A`. Кандидат окна7суток, пригодность/набор/latency/зрелостьUNKNOWN доG1. Task success = верные завершения без помощи / все eligible started attempts, включая отказ/timeout/missing. Guardrails: ложные сигналы/все сигналы; жалобы/все назначенные семьи; ограничения других заранее включённых номеров/все такие номера; повторный расход/все подтверждённые eligible операции. Baseline/δ/метод/n/вред/надёжность/срокиUNKNOWN. SUCCESS→рассмотреть ограниченный следующийscope; FAILURE→пересмотр/доработка/стоп; INCONCLUSIVE→отдельное решение о цене донабора. Доступ после отзыва/двойной расход→немедленная остановка спорногоscope, сверка и подтверждённое исправление до нового решения. C-020; S-001 PDF стр.7–8,10–11; `test-plan.md`, §1–5 и «Раздельные gates».

## Сообщение, канал и следующий шаг

Организатору при актуальном риске: условный макет проверить разрешённый остаток и доступную передачу. Барьер позднего узнаванияC-007 — гипотеза; доказательство обещания — тариф, право, свежесть и конечный статус, ещё требуют проверки. Канал — существующий путь группы→проверка→передача→итог; участнику при приглашении — отдельные права/отзыв. S-001 PDF стр.1,5; C-001/C-012; `strategy-communication.md`. PO/финансам сейчас — внутреннее рассмотрение ограничений/UNKNOWN; следующее действие после публикации — конкурсная упаковка, без автоматической проработки стратегии или запуска.
'''
    state = f'''# Case state

Строки revision/claims ниже описывают содержимое ревизии, не подтверждение публикации.
До фактического post-selection `classify = CHECKPOINTED` это DRAFT; `VALIDATED_CANDIDATE` недостаточно.
Статус определяют настоящий `ACTIVE.json` и реальный classifier receipt, не выбор владельца или заголовок документа.

- Updated at: 2026-11-20, Europe/Moscow
- Case protocol: `checkpoint-v1`
- Active complete revision ID: D0003
- Parent revision ID: D0002
- Current stage: `DECISION_RESUME`
- Decision status: `DECIDED`
- Current evidence IDs: E-001, E-002, E-003, E-004, E-005, E-006, E-007, E-008, E-009, E-010, E-011, E-012, E-013, E-014, E-015, E-016, E-017, E-018, E-019, E-020, E-022, E-023
- Current claim IDs (active successors only; match manifest): {active_text}
- Superseded claim IDs → explicitly selected successor(s): C-010 → C-014; C-015 → C-017; C-016 → C-018; C-021 → C-024 → C-025
- Completed: ограниченный аудит и арифметика, финализация прежнего DRAFT без новых исследований, сохранённые решения PO и согласие на gated-публикацию
- Open questions: собственный прогнозA, причины/пригодность/устранимость/поток, реальная оплата/эффект/временной профиль, PM/ставки/доступность/стоимость/сроки, статистические параметры, возможные пилот/G2 и закрытие недобора владельцев, trajectory года3
- Blockers and limitations: фактические эффект/ресурс/сметаUNKNOWN; годовые цели/чувствительность не являются своим прогнозом; pilot/spend/contacts/real-product execution not approved as of this revision
- Next exact action: остановить содержательную работу после успешной публикации; следующий этап — конкурсная упаковка по отдельному конкретному поручению
- Human decision needed: будущие финансирование/назначения/входы/точный scopeG1/G2 и отдельная реализацияC; повторный выборA/принятие текущего компромисса не требуются
- Cost/time/call telemetry: UNKNOWN; actual command/runtime/timestamps in receipts; limit not specified; prior time/cost not reset

## Подтверждённое содержание решений

A сохранён; ограниченныйQ1-P0 согласован как направление проработки. Разрешены внутренний план получения оценок и перечень ролей/данных/зависимостей; денег/сотрудников не выделено, стоимость/PM/срокиUNKNOWN. PO принимает недобор1000 владельцев как незакрытый компромисс при сохранении цели2000; реализацияC не разрешена. Год3 — гипотезы. C-025; S-016 `inputs/R0003-owner-publication.md`, «Сохраняемые решения»; S-017 `drafts/r0003-independent-audit/owner-decision.md`, соответствующие разделы. Полные решения/ограничения — `decision.md` и `revisions/D0003/dependencies/strategy.md`, §8.

Собственный прогнозA UNKNOWN; условныеC88000/M14000 требуют необходимой взвешенной границы37/44≈84,09%, не доказывают достижимость. Кварталы/окупаемостьUNKNOWN без профиля эффекта/затрат. C-017/C-022/C-023; S-013 `drafts/r0003-independent-audit/calculation-results.json`, `capacity_constraint`, `timing_profiles_not_forecasts`; S-014 строки30,44–53. Числовой план года3UNKNOWN, C-018.

## Разрешения и продолжение

Согласие на gated-аналитическую публикацию этой ревизии дано S-016. Отдельную запись approval точного revision/hash/action/scope и текущую применимость исполнения восстанавливать из фактического `approvals.jsonl` и receipts; publication truth — реальный selector/классификатор. Публикация не даёт разрешения пилота/расходов/назначений/контактов/закрытых данных и host permissions. Изменение revision/hash/scope/решающего основания требует нового применимого approval.

Исторические drafts сохраняются: comparison наR0001 — старое ожидание выбора; r0002-family-priority — подготовительные дубликатыR0002; r0003-independent-audit — источник завершённого ограниченного пересмотра и прежних ограничений публикации, которые S-016 изменил только в scope аналитики. Не выбирать черновики по времени; в следующей сессии штатно восстановить этот checkpoint и отдельно inventory. История повреждённых locators S-015/E-021 сохранена; исправленная привязка S-017/E-023 используется C-025. Это техническая коррекция кодировки, не новое клиентское свидетельство.

Ошибки/попытки и реальные проверки — activity/receipts. R0001/R0002 не переписываются. Следующая работа — конкурсные материалы; новые исследования/переработку стратегии автоматически не начинать.
'''
    docs = dict(zip(views,[options,decision,product,communication,plan,state]))
    # No new claims may already exist; never overwrite history to finish a candidate.
    for name, reserved in [('sources.jsonl',['S-016','S-017']),('evidence.jsonl',['E-022','E-023']),('claims.jsonl',['C-025'])]:
        if {r['id'] for r in map(json.loads,(case/name).read_text(encoding='utf-8').splitlines())}.intersection(reserved): raise RuntimeError('Reserved IDs exist')
    headings = '; '.join(f'line{i}: {line.lstrip("# ")}' for i,line in enumerate((draft/'owner-decision.md').read_text(encoding='utf-8').splitlines(),1) if line.startswith('## '))
    sources = [dict(id='S-016',url='inputs/R0003-owner-publication.md',publisher='User acting as Product Owner',title='Authorization of finalization and gated analytical publication',published='2026-11-20; exact message timestamp UNKNOWN',version='Current owner message faithfully summarized',retrieved_at=now(),locator='Разрешённое действие; Сохраняемые решения; Ограничения и остановка',snapshot='inputs/R0003-owner-publication.md',sha256=sha(case/'inputs/R0003-owner-publication.md'),status='DOCUMENTED',limitations='Publication only after real gates; no new research, budget, staffing, pilot or external actions.'),dict(id='S-017',url='drafts/r0003-independent-audit/owner-decision.md',publisher='User acting as Product Owner',title='Corrected locators for unchanged saved owner decisions',published='2026-11-20; exact message timestamp UNKNOWN',version='Locator-only correction of S-015; original source bytes unchanged',retrieved_at=now(),locator=headings,snapshot='drafts/r0003-independent-audit/owner-decision.md',sha256=sha(draft/'owner-decision.md'),status='DOCUMENTED',limitations='Repairs question-mark corruption in S-015 locator without rewriting it. Historical publication hold superseded only by S-016; no new customer observation.')]
    evidence = [dict(id='E-022',source_id='S-016',locator='Разрешённое действие; Сохраняемые решения; Ограничения и остановка',summary='Owner authorizes faithful R0003 finalization/publication only via successful existing gates; retain Q1 limits, accepted open owner gap and hypothetical year3; stop on blocker or new substantive choice, then stop after success.',extraction_method='Read current owner instruction; save labeled summary',review_status='verified',limitations='Analytical publication authority only; no implementation/pilot/external action approval.'),dict(id='E-023',source_id='S-017',locator=headings,summary='Unchanged owner source confirms limited internal estimate planning without budget/staff, accepted1000 owner gap with2000 target retained/C deferred, hypothetical year3; prior publication hold is historical and now superseded by S-016.',extraction_method='Re-read saved source; derive exact headings/line locators from UTF-8 file; correct E-021 locator append-only',review_status='verified',limitations='Locator correction, not new product evidence. E-021 historical corrupted locator retained.')]
    claim = dict(id='C-025',text='PO retains A and limited Q1 preparation direction with internal estimate-plan/roles-data-dependencies permission only; no budget or staffing. PO knowingly accepts1000-owner shortfall as open compromise with2000 target retained and no C implementation now; year3 remains hypothetical. Latest owner decision authorizes faithful R0003 analytical publication only after real shared gates, superseding earlier publication hold.',status='DOCUMENTED',evidence_ids=['E-022','E-023'],valid_as_of='2026-11-20',limitations='No permission for pilot, spending, appointments, contacts, real-product changes or closed data. Separate exact-manifest publication approval; execution authority/host permissions remain distinct.',supersedes=['C-024'])
    append('sources.jsonl',sources); append('evidence.jsonl',evidence); append('claims.jsonl',[claim])
    append('activity.jsonl',[dict(id='ACT-038',date='2026-11-20',at_utc=now(),action='R0003_finalization_authorized',status='PREPARING',source='S-016',scope='Finalize existing chosen draft and saved owner decisions; no new substantive research or decision',correction='Question-mark encoding damage in S015/E021 locators found during read; unchanged primary source re-read, exact headings/lines recovered as S017/E023 append-only. C025 supersedesC024, resolves historical publication hold only.',base_receipt='receipts/R0003-recovery.json',remaining_seconds='UNKNOWN',monetary_guard='UNKNOWN',limit='Not specified')])
    rev.mkdir(parents=True,exist_ok=False)
    for name,text in docs.items(): save(rev/name,text)
    save(rev/'dependencies/strategy.md',strategy)
    # Preserve exact approved draft/decision sources and arithmetic; do not edit them.
    source_names = ['strategy.md','audit-input.md','owner-decision.md','calculate.py','calculation-results.json','calculation-receipt.json','owner-decision-receipt.json','verification-receipt.json']
    for name in source_names:
        target = rev/'dependencies/audit-source'/name
        target.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(draft/name,target)
    shutil.copyfile(case/'inputs/R0003-owner-publication.md',rev/'dependencies/owner-publication.md')
    # Every dependency actually used by the parent remains pinned; mutable root views excluded.
    parent = json.loads((case/'revisions/D0002/manifest.json').read_bytes())
    paths = {e['path'] for e in parent['files']}
    paths.update(f'revisions/D0002/{name}' for name in views)
    paths.add('revisions/D0002/manifest.json')
    paths.update(p.relative_to(case).as_posix() for p in rev.rglob('*') if p.is_file())
    paths.update((draft/name).relative_to(case).as_posix() for name in source_names)
    paths.update(['inputs/R0003-owner-publication.md','research/R0003-finalize.py','receipts/R0003-recovery.json'])
    manifest = dict(revision_id='R0003',parent_revision_id='R0002',parent_manifest_sha256=sha(case/'revisions/D0002/manifest.json'),status='COMPLETE',active_claim_ids=active,files=[dict(path=name,sha256=sha(case/name)) for name in sorted(paths)])
    save(rev/'manifest.json',manifest)
    # Approval is a later append-only record: avoid a hash cycle with the pinned prior prefix.
    approval = dict(approval_id='A-001',approver='User explicitly acting as Product Owner; current message saved as S-016',approved_at='2026-11-20; exact message timestamp UNKNOWN',recorded_at_utc=now(),action='publish_analytical_checkpoint_R0003',scope='Exact six R0003 snapshots, finalized strategy and manifest dependencies; copy current views and select R0003 only after successful unchanged pre-selection gate. No research, architecture changes, pilot, budget, staffing or external actions.',revision_id='R0003',manifest_sha256=sha(rev/'manifest.json'),basis_claim_ids=active,source_id='S-016',expires_at='NONE specified by owner',review_trigger='Any change to revision/manifest hash/action/scope/decisive basis or failed gate; stop for new owner decision if substantive choice required',conditions='Preserve R0001/R0002; successful actual check-candidate and post-selection classify; finalize approved draft faithfully; stop after publication. Host permissions separate.')
    append('approvals.jsonl',[approval])
    append('activity.jsonl',[dict(id='ACT-039',date='2026-11-20',at_utc=now(),action='R0003_snapshots_and_manifest_prepared',status='PREPARED',revision_id='R0003',manifest_sha256=sha(rev/'manifest.json'),parent_manifest_sha256=manifest['parent_manifest_sha256'],approval_id='A-001',detail='Six finalized snapshots saved once; source/report copies preserved, complete manifest hashed. Exact-manifest analytical publication approval appended separately after pinned prior approvals prefix, avoiding hash cycle. Root views/selector still selected parent; no pilot approval.',remaining_seconds='UNKNOWN',monetary_guard='UNKNOWN')])
    save(receipts/'R0003-prepare.json',dict(status='PREPARED',revision_id='R0003',manifest_sha256=sha(rev/'manifest.json'),parent_manifest_sha256=manifest['parent_manifest_sha256'],active_claim_ids=active,dependency_count=len(paths),approval=approval,root_views_unchanged={name:sha(case/name)==base['root_before_sha256'][name] for name in views},selector_unchanged=sha(case/'ACTIVE.json')==base['root_before_sha256']['ACTIVE.json'],remaining_seconds='UNKNOWN',monetary_guard='UNKNOWN'))
    print(json.dumps(dict(status='PREPARED',manifest_sha256=sha(rev/'manifest.json'),dependency_count=len(paths),active_claim_count=len(active))))

def gate():
    base = parent_ok()
    prepared = json.loads((receipts/'R0003-prepare.json').read_bytes())
    if prepared['manifest_sha256'] != sha(rev/'manifest.json'): raise RuntimeError('Prepared manifest changed')
    # Time/cost guard has no imposed limit; telemetry UNKNOWN, no invented remaining budget.
    # Exact byte copies, then unchanged tool. Failure stops without automatic selection/repair.
    for name in views: shutil.copyfile(rev/name,case/name)
    shutil.copyfile(rev/'dependencies/strategy.md',case/'strategy.md')
    result = shared(['check-candidate',str(case),'--revision','R0003'],'R0003-gate.json')
    selector = json.loads(result['stdout'])
    if selector.get('status')!='VALIDATED_CANDIDATE' or selector.get('revision_id')!='R0003' or selector.get('manifest_sha256')!=sha(rev/'manifest.json'): raise RuntimeError('Unexpected gate output')
    manifest = json.loads((rev/'manifest.json').read_bytes())
    save(receipts/'R0003-handover.json',dict(status='VALIDATED_CANDIDATE',selector=selector,parent_selector=json.loads((case/'ACTIVE.json').read_bytes()),gate_receipt_sha256=sha(receipts/'R0003-gate.json'),all_dependency_current_sha256={e['path']:sha(case/e['path']) for e in manifest['files']},root_views_sha256={name:sha(case/name) for name in views},strategy_sha256=sha(case/'strategy.md'),remaining_seconds='UNKNOWN',monetary_guard='UNKNOWN',copied_views=views))

def publish():
    base = parent_ok()
    handover = json.loads((receipts/'R0003-handover.json').read_bytes())
    actual = json.loads((receipts/'R0003-gate.json').read_bytes())
    selected = json.loads(actual['stdout'])
    if actual['exit_code']!=0 or sha(receipts/'R0003-gate.json')!=handover['gate_receipt_sha256'] or selected!=handover['selector'] or selected['manifest_sha256']!=sha(rev/'manifest.json'): raise RuntimeError('Matching actual gate absent')
    for name,h in handover['all_dependency_current_sha256'].items():
        if sha(case/name)!=h: raise RuntimeError('Dependency changed after gate: '+name)
    for name,h in handover['root_views_sha256'].items():
        if sha(case/name)!=h or (case/name).read_bytes()!=(rev/name).read_bytes(): raise RuntimeError('View changed after gate')
    if sha(case/'strategy.md')!=handover['strategy_sha256']: raise RuntimeError('Strategy view changed after gate')
    approvals = [json.loads(x) for x in (case/'approvals.jsonl').read_text(encoding='utf-8').splitlines()]
    matches = [a for a in approvals if a.get('approval_id')=='A-001' and a.get('revision_id')=='R0003' and a.get('manifest_sha256')==selected['manifest_sha256'] and a.get('action')=='publish_analytical_checkpoint_R0003']
    if len(matches)!=1: raise RuntimeError('Exact publication approval absent/ambiguous')
    # Selector is written last, using the unchanged tool's digest, not an invented one.
    (case/'ACTIVE.json').write_text(json.dumps(dict(revision_id='R0003',manifest_sha256=selected['manifest_sha256']),separators=(',',':'))+'\n',encoding='utf-8')
    r = shared(['classify',str(case)],'R0003-classify.json')
    if r['stdout'].strip()!='CHECKPOINTED': raise RuntimeError('Post-selection classification not CHECKPOINTED')
    for name,h in base['history_sha256'].items():
        if sha(case/name)!=h: raise RuntimeError('Published ancestors changed')
    for name,info in base['ledger_prefixes'].items():
        if hashlib.sha256((case/name).read_bytes()[:info['bytes']]).hexdigest()!=info['sha256']: raise RuntimeError('Historical ledger prefix changed')
    append('activity.jsonl',[dict(id='ACT-040',date='2026-11-20',at_utc=now(),action='R0003_publication',status='CHECKPOINTED',revision_id='R0003',manifest_sha256=selected['manifest_sha256'],parent_revision_id='R0002',parent_manifest_sha256=sha(case/'revisions/D0002/manifest.json'),approval_id='A-001',gate_receipt='receipts/R0003-gate.json',classify_receipt='receipts/R0003-classify.json',detail='Actual unchanged gate accepted; selector written last with its digest; real post-selection classifier CHECKPOINTED. R0001/R0002 and historical ledger prefixes preserved; new active set explicit in manifest/state/decision. No new research, architecture or external action. Analytical approval consumed for publication only; stop substantive work, next stage contest packaging.')])
    save(receipts/'R0003-completion.json',dict(status='CHECKPOINTED',revision_id='R0003',manifest_sha256=selected['manifest_sha256'],parent_revision_id='R0002',parent_manifest_sha256=sha(case/'revisions/D0002/manifest.json'),published_ancestor_files_checked=len(base['history_sha256']),ancestors_unchanged=True,historical_ledger_prefixes_preserved=True,all_six_views_byte_identical=True,approval_id='A-001',approval_scope='Analytical publication only; no pilot/budget/staff/contacts',strategy='revisions/D0003/dependencies/strategy.md',decision='revisions/D0003/decision.md',state='revisions/D0003/state.md',gate_receipt='receipts/R0003-gate.json',classify_receipt='receipts/R0003-classify.json',next_step='Stop; contest packaging by separate concrete instruction',telemetry='UNKNOWN'))
    print(json.dumps(dict(status='CHECKPOINTED',revision_id='R0003',manifest_sha256=selected['manifest_sha256'],ancestors_unchanged=True)))

if __name__ == '__main__':
    action = sys.argv[1]
    if action == 'prepare': prepare()
    elif action == 'gate': gate()
    elif action == 'publish': publish()
    else: raise RuntimeError('Unknown action')
