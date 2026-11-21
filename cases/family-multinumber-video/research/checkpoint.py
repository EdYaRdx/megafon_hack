"""Record actual tool receipts and package this case; shared gate is never replaced."""
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

CASE = Path(__file__).resolve().parents[1]
PROJECT = CASE.parents[1]
REL = CASE.relative_to(PROJECT).as_posix()
REV = CASE / 'revisions/D0001'
SNAPSHOTS = ['options.md','decision.md','strategy-product.md','strategy-communication.md','test-plan.md','state.md']

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def save_new(path, value):
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
def event(eid, operation, result, details):
    path = CASE / 'activity.jsonl'
    old = path.read_bytes()
    assert eid not in {json.loads(x).get('id') for x in old.splitlines() if x.strip()}
    row = dict(id=eid,recorded_at=datetime.now(timezone.utc).isoformat(),operation=operation,result=result,details=details,cost='UNKNOWN',elapsed_seconds='UNKNOWN',model='UNKNOWN')
    with path.open('ab') as stream:
        if old and not old.endswith(b'\n'):
            stream.write(b'\n')
        stream.write((json.dumps(row, ensure_ascii=False)+'\n').encode('utf-8'))
def run_receipt(args, path):
    result = subprocess.run(args, cwd=PROJECT, capture_output=True, text=True, encoding='utf-8')
    receipt = dict(command=args,cwd=str(PROJECT),executed_at=datetime.now(timezone.utc).isoformat(),exit_code=result.returncode,stdout=result.stdout,stderr=result.stderr)
    save_new(path,receipt)
    print(json.dumps(receipt,ensure_ascii=False,indent=2))
    return result

mode = sys.argv[1]
if mode == 'prepare':
    assert json.loads((CASE/'case-protocol.json').read_text())['checkpoint_state']=='CHECKPOINTING'
    assert not (CASE/'ACTIVE.json').exists()
    assert not (REV/'manifest.json').exists()
    assert all((REV/name).is_file() for name in SNAPSHOTS)
    old_results = (CASE/'calculations/results.json').read_bytes()
    calculation = run_receipt([sys.executable,'-B','-X','utf8',f'{REL}/calculations/run.py'],CASE/'research/calculation-receipt.json')
    if calculation.returncode:
        event('A-025','calculation receipt','FAILED','See research/calculation-receipt.json');sys.exit(calculation.returncode)
    assert old_results == (CASE/'calculations/results.json').read_bytes(), 'Repeated calculation changed result'
    assert json.loads(calculation.stdout)==json.loads(old_results)
    shutil.copyfile(REV/'strategy-product.md',REV/'strategy.md')
    event('A-025','prepare recommendation','SUCCESS','Six snapshots and five-part strategy complete; owner decision NOT PROVIDED; actual calculation repeat matches original results; no stage budget set, actual remaining time/money and guard UNKNOWN; preparation reserves remaining work for hashes, copies, shared gate, selector and classifier.')
    dependencies = [CASE/name for name in ['sources.jsonl','evidence.jsonl','claims.jsonl','activity.jsonl','approvals.jsonl']]
    for directory in ['inputs','sources','calculations']:
        dependencies.extend(p for p in (CASE/directory).rglob('*') if p.is_file())
    dependencies.extend(CASE/name for name in ['research/record.py','research/checkpoint.py','research/calculation-receipt.json'])
    dependencies.extend(REV/name for name in SNAPSHOTS+['strategy.md'])
    dependencies=sorted(set(dependencies))
    claims=[f'C-{i:03d}' for i in range(1,15)]
    manifest=dict(revision_id='D0001',parent_revision_id=None,status='COMPLETE',active_claim_ids=claims,files=[dict(path=p.relative_to(CASE).as_posix(),sha256=sha(p)) for p in dependencies])
    save_new(REV/'manifest.json',manifest)
    for name in SNAPSHOTS+['strategy.md']:
        shutil.copyfile(REV/name,CASE/name)
        assert (REV/name).read_bytes()==(CASE/name).read_bytes()
    print(json.dumps(dict(status='PREPARED_NOT_SELECTED',revision_id='D0001',file_count=len(dependencies),manifest_sha256=sha(REV/'manifest.json'),copied=SNAPSHOTS+['strategy.md'])))
elif mode == 'gate':
    assert not (CASE/'ACTIVE.json').exists()
    result=run_receipt([sys.executable,'-B','-X','utf8','tools/case_protocol.py','check-candidate',REL,'--revision','D0001'],CASE/'research/check-candidate-receipt.json')
    if result.returncode:
        event('A-026','shared pre-selection gate','FAILED','See research/check-candidate-receipt.json; STOP; selector not written');sys.exit(result.returncode)
    value=json.loads(result.stdout)
    assert value['status']=='VALIDATED_CANDIDATE'
    assert value['manifest_sha256']==sha(REV/'manifest.json')
    event('A-026','shared pre-selection gate','SUCCESS','VALIDATED_CANDIDATE; exact command/stdout/stderr/exit in research/check-candidate-receipt.json; real selector still absent')
elif mode == 'select':
    gate=json.loads((CASE/'research/check-candidate-receipt.json').read_text(encoding='utf-8'))
    assert gate['exit_code']==0
    value=json.loads(gate['stdout'])
    assert value['status']=='VALIDATED_CANDIDATE' and value['manifest_sha256']==sha(REV/'manifest.json')
    assert not (CASE/'ACTIVE.json').exists()
    save_new(CASE/'ACTIVE.json',dict(revision_id=value['revision_id'],manifest_sha256=value['manifest_sha256']))
    result=run_receipt([sys.executable,'-B','-X','utf8','tools/case_protocol.py','classify',REL],CASE/'research/post-selection-receipt.json')
    if result.returncode or result.stdout.strip()!='CHECKPOINTED':
        event('A-027','post-selection classifier','FAILED','See research/post-selection-receipt.json; STOP; do not repair immutable revision');sys.exit(1)
    marker=json.loads((CASE/'case-protocol.json').read_text())
    marker['checkpoint_state']='CHECKPOINTED'
    (CASE/'case-protocol.json').write_text(json.dumps(marker,indent=2)+'\n',encoding='utf-8')
    event('A-027','post-selection classifier','SUCCESS','CHECKPOINTED; marker set CHECKPOINTED after real success; owner choice and execution approval remain separate')
    print(json.dumps(dict(status='CHECKPOINTED',revision_id='D0001',manifest_sha256=value['manifest_sha256'])))
elif mode == 'inventory':
    result=run_receipt([sys.executable,'-B','-X','utf8','-m','tools.resume_context',REL],CASE/'research/resume-inventory-receipt.json')
    if result.returncode:
        event('A-028','resume inventory','FAILED','See research/resume-inventory-receipt.json');sys.exit(result.returncode)
    event('A-028','resume inventory','SUCCESS','Actual consumer inventory receipt saved; no owner choice inferred from drafts')
else:
    raise ValueError(mode)
