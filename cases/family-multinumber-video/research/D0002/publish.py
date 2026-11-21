"""Package successor and run the unchanged shared gate; never alter prior history."""
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PROJECT=ROOT.parents[1]
REL=ROOT.relative_to(PROJECT).as_posix()
OLD=ROOT/'revisions/D0001'
NEW=ROOT/'revisions/D0002'
OUT=ROOT/'research/D0002'
PARENT_SHA='7cca0ed8ea388e56cdcc01b24aa4e896e62174b9283d0a265a3f47a4cdcf5c5d'
NAMES=['options.md','decision.md','strategy-product.md','strategy-communication.md','test-plan.md','state.md']
ACTIVE=[f'C-{i:03d}' for i in range(1,7)]+[f'C-{i:03d}' for i in range(8,12)]+['C-013','C-014','C-015','C-016','C-017']
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def save_new(path,value):
    with path.open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def event(eid,operation,result,details):
    p=ROOT/'activity.jsonl';old=p.read_bytes()
    assert eid not in {json.loads(x).get('id') for x in old.splitlines() if x.strip()}
    row=dict(id=eid,recorded_at=datetime.now(timezone.utc).isoformat(),operation=operation,result=result,details=details,cost='UNKNOWN',elapsed_seconds='UNKNOWN',model='UNKNOWN')
    with p.open('ab') as f:
        if old and not old.endswith(b'\n'):f.write(b'\n')
        f.write((json.dumps(row,ensure_ascii=False)+'\n').encode('utf-8'))
def run(args,file):
    result=subprocess.run(args,cwd=PROJECT,capture_output=True,text=True,encoding='utf-8')
    receipt=dict(command=args,cwd=str(PROJECT),executed_at=datetime.now(timezone.utc).isoformat(),exit_code=result.returncode,stdout=result.stdout,stderr=result.stderr)
    save_new(OUT/file,receipt)
    print(json.dumps(receipt,ensure_ascii=False,indent=2))
    return result
def block(text,start,end):return text.split(start,1)[1].split(end,1)[0]

mode=sys.argv[1]
if mode=='prepare':
    assert sha(OLD/'manifest.json')==PARENT_SHA
    old_manifest=json.loads((OLD/'manifest.json').read_text())
    assert json.loads((ROOT/'ACTIVE.json').read_text())==dict(revision_id='D0001',manifest_sha256=PARENT_SHA)
    for entry in old_manifest['files']:
        if entry['path'].startswith('revisions/D0001/'):
            assert sha(ROOT/entry['path'])==entry['sha256'],'Historical snapshot changed'
    assert all((ROOT/name).read_bytes()==(OLD/name).read_bytes() for name in NAMES),'Old root views changed too early'
    old_product=(OLD/'strategy-product.md').read_text(encoding='utf-8')
    product=(NEW/'strategy-product.md').read_text(encoding='utf-8')
    assert block(old_product,'## 3. Польза для клиента и прибыль оператора','## 4. Стратегический выбор, прогноз и план по кварталам')==block(product,'## 3. Польза для клиента и прибыль оператора','## 4. Стратегический выбор, прогноз и план по кварталам')
    assert block(old_product,'### Все пять KPI: цель, рабочий прогноз и менее благоприятный исход','## 5. Ресурсы, риски и решение руководителя')==block(product,'### Все пять KPI: цель, рабочий прогноз и менее благоприятный исход','## 5. Ресурсы, риски и решение руководителя')
    old_options=(OLD/'options.md').read_text(encoding='utf-8').replace('C-007','C-015').replace('C-012','C-016')
    options=(NEW/'options.md').read_text(encoding='utf-8')
    assert block(old_options,'## Сравнение на одинаковом горизонте','## Рекомендация и ближайшее опровержение')==block(options,'## Сравнение на одинаковом горизонте','## Рекомендация и ближайшее опровержение')
    assert all((NEW/name).is_file() for name in NAMES)
    for name in ['calculations/run.py','calculations/results.json','research/calculation-receipt.json']:
        assert sha(ROOT/name)==next(e['sha256'] for e in old_manifest['files'] if e['path']==name),'Unchanged numerical dependency modified'
    shutil.copyfile(NEW/'strategy-product.md',NEW/'strategy.md')
    event('A-032','D0002 final preparation','SUCCESS','Prior D0001 snapshot bytes verified unchanged; economics, KPI/forecast/quarter sections and alternative table compared with inherited references and unchanged; no rerun or invented numbers. Owner choice explicit. No assigned stage time/money limit; actual remaining telemetry and guard UNKNOWN. Work reserved for hashes, copies, unchanged shared gate, selector/classifier and restoration check. Brief mutable view updated to S-006.')
    deps=[ROOT/e['path'] for e in old_manifest['files'] if not e['path'].startswith('revisions/')]
    deps += [ROOT/'inputs/user-choice-D0002.md',OUT/'revise.py',OUT/'publish.py']
    deps += [NEW/name for name in NAMES+['strategy.md']]
    deps=sorted(set(deps))
    manifest=dict(revision_id='D0002',parent_revision_id='D0001',parent_manifest_sha256=sha(OLD/'manifest.json'),status='COMPLETE',active_claim_ids=ACTIVE,files=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p)) for p in deps])
    save_new(NEW/'manifest.json',manifest)
    for name in NAMES+['strategy.md']:
        shutil.copyfile(NEW/name,ROOT/name)
        assert (NEW/name).read_bytes()==(ROOT/name).read_bytes()
    receipt=dict(status='PREPARED_NOT_SELECTED',revision_id='D0002',parent_revision_id='D0001',parent_manifest_sha256=PARENT_SHA,manifest_sha256=sha(NEW/'manifest.json'),copied=NAMES+['strategy.md'],dependency_count=len(deps),unchanged_checks=['prior snapshots','economics','all five KPI and forecast/quarter sections','comparison table except inherited claim references','calculation script/results/receipt'])
    save_new(OUT/'preparation-receipt.json',receipt)
    print(json.dumps(receipt,ensure_ascii=False,indent=2))
elif mode=='gate':
    assert json.loads((ROOT/'ACTIVE.json').read_text())['revision_id']=='D0001'
    result=run([sys.executable,'-B','-X','utf8','tools/case_protocol.py','check-candidate',REL,'--revision','D0002'],'check-candidate-receipt.json')
    if result.returncode:
        event('A-033','D0002 shared gate','FAILED','See research/D0002/check-candidate-receipt.json; STOP, do not select or repair history');sys.exit(result.returncode)
    gate=json.loads(result.stdout)
    assert gate['status']=='VALIDATED_CANDIDATE' and gate['manifest_sha256']==sha(NEW/'manifest.json')
    # No pinned dependency changes between gate and selector; log gate only after successful selection.
elif mode=='select':
    stored=json.loads((OUT/'check-candidate-receipt.json').read_text(encoding='utf-8'))
    assert stored['exit_code']==0
    gate=json.loads(stored['stdout'])
    assert gate['status']=='VALIDATED_CANDIDATE' and gate['manifest_sha256']==sha(NEW/'manifest.json')
    assert json.loads((ROOT/'ACTIVE.json').read_text())==dict(revision_id='D0001',manifest_sha256=PARENT_SHA)
    selector=dict(revision_id='D0002',manifest_sha256=gate['manifest_sha256'])
    (ROOT/'ACTIVE.json').write_text(json.dumps(selector,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    result=run([sys.executable,'-B','-X','utf8','tools/case_protocol.py','classify',REL],'post-selection-receipt.json')
    if result.returncode or result.stdout.strip()!='CHECKPOINTED':
        event('A-034','D0002 post-selection','FAILED','See research/D0002/post-selection-receipt.json; STOP; do not repair immutable history');sys.exit(1)
    event('A-033','D0002 shared gate','SUCCESS','Actual unchanged tool returned VALIDATED_CANDIDATE; exact command/stdout/stderr/exit in research/D0002/check-candidate-receipt.json; selector written only after success')
    event('A-034','D0002 post-selection','SUCCESS','Actual classifier returned CHECKPOINTED; owner family priority DECIDED, no pilot/budget/comms approval; stop after completed handover per S-006')
    print(json.dumps(dict(status='CHECKPOINTED',**selector),ensure_ascii=False))
elif mode=='inventory':
    result=run([sys.executable,'-B','-X','utf8','-m','tools.resume_context',REL],'resume-inventory-receipt.json')
    if result.returncode:
        event('A-035','D0002 restore check','FAILED','See research/D0002/resume-inventory-receipt.json');sys.exit(result.returncode)
    event('A-035','D0002 restore check','SUCCESS','Read-only consumer inventory receipt saved; result to inspect separately from owner decision; no external action initiated')
else:raise ValueError(mode)
