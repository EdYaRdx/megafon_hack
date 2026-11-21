"""Task-local receipts and publication; calls the unchanged shared gate."""
import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

CASE = Path(__file__).resolve().parents[2]
REPO = CASE.parents[1]
CASE_REL = CASE.relative_to(REPO).as_posix()
OUT = Path(__file__).resolve().parent
PARENT_HASH = 'aa6a57a28c1369258daa61ed25c214dff3fb86fa79ec89aae08fef472b387b8f'
SIX = ['options.md', 'decision.md', 'strategy-product.md', 'strategy-communication.md', 'test-plan.md', 'state.md']
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
def event(operation, result, details, retry_of=None):
    path = CASE / 'activity.jsonl'
    rows = [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]
    row = dict(id=f"A-{max(int(r['id'].split('-')[-1]) for r in rows)+1:03d}", recorded_at=datetime.now(timezone.utc).isoformat(), operation=operation, result=result, details=details, retry_of=retry_of, model='UNKNOWN', cost='UNKNOWN', elapsed_seconds='UNKNOWN')
    with path.open('ab') as stream:
        if path.stat().st_size and not path.read_bytes().endswith(b'\n'):
            stream.write(b'\n')
        stream.write((json.dumps(row, ensure_ascii=False) + '\n').encode('utf-8'))
    return row['id']
def run(name, args):
    argv = [sys.executable, '-B', '-X', 'utf8', *args]
    start = time.perf_counter()
    proc = subprocess.run(argv, cwd=REPO, capture_output=True, text=True, encoding='utf-8')
    receipt = dict(argv=argv, cwd=str(REPO), runtime=sys.version, recorded_at=datetime.now(timezone.utc).isoformat(), command_elapsed_seconds=time.perf_counter()-start, exit_code=proc.returncode, stdout=proc.stdout, stderr=proc.stderr)
    save(OUT / f'{name}-receipt.json', receipt)
    event(name, 'SUCCESS' if proc.returncode == 0 else 'FAILED', f'Actual argv/stdout/stderr/exit in research/D0003/{name}-receipt.json')
    if proc.returncode:
        print(proc.stdout, proc.stderr)
        raise SystemExit(proc.returncode)
    return receipt
mode = sys.argv[1]
if mode == 'restore':
    assert digest(CASE / 'revisions/D0002/manifest.json') == PARENT_HASH
    run('restore-classify', ['tools/case_protocol.py', 'classify', CASE_REL])
    receipt = run('restore-inventory', ['-m', 'tools.resume_context', CASE_REL])
    inventory = json.loads(receipt['stdout'])
    assert inventory['confirmed']['revision_id'] == 'D0002'
    assert inventory['unfinished']['drafts'] == [] and inventory['unfinished']['issues'] == []
    event('D0003 source review', 'SUCCESS', 'Restored D0002; activity A-033..A-036 inspected as gate/classifier/inventory/stop, not draft analysis. Read immutable snapshots, source/evidence/claim ledgers, user scope and choice. Reopened S-001 OCR p1/3/4/9/10/11 and original saved page images p3/9/11; financial table, rate and preliminary staffing visually checked. No external market numbers or field evidence added. Existing verified Python reused; stage time/money limit not set, remaining telemetry/guard UNKNOWN. Planning includes hashes, copies, shared gate and post-selection classify.')
elif mode == 'calculate':
    receipt = run('calculation', [f'{CASE_REL}/calculations/D0003/audit.py'])
    result = json.loads(receipt['stdout'])
    save(CASE / 'calculations/D0003/results.json', result)
    print(json.dumps({key:result[key] for key in ['gap_rub','required_additional_paid_number_months_if_C_O_zero','timing_scenarios']}, ensure_ascii=False, indent=2))
elif mode == 'build':
    receipt = run('build', [f'{CASE_REL}/research/D0003/build.py'])
    print(receipt['stdout'])
elif mode == 'qc':
    revision = CASE / 'revisions/D0003'
    active = json.loads((OUT / 'active-claims.json').read_text(encoding='utf-8'))
    decision_path = revision / 'decision.md'
    text = decision_path.read_text(encoding='utf-8')
    question = '- **Decision question:** достаточно ли оснований для финансовой цели и готовности следующего шага при сохранённом семейном направлении?'
    assert text.count(question) == 1
    assert '- **Revision:**' not in text
    controls = '\n'.join([
        question,
        '- **Decision owner / authority:** пользователь как руководитель продукта; S-002, inputs/user-scope.md, п. 2; S-007, inputs/user-review-D0003.md',
        '- **Status:** `DECIDED`',
        '- **Revision:** D0003',
        '- **Parent revision:** D0002',
        '- **Active claim IDs:** '+', '.join(active),
        '- **Selected direction:** помощь уже подключённым семьям сохраняется владельцем; экономический результат UNKNOWN; пилот и бюджет не одобрены',
    ])
    text = text.replace(question, controls, 1)
    old = '**Owner decision: DECIDED — приоритет помощи уже подключённым семьям; S-006, C-018.** Параметры B, масштаб и эффект остаются проверяемыми гипотезами (C-016, C-017). Альтернативы сохранены; числовые прогнозы и расчёты не перегенерированы. На момент D0002 пилот, бюджет, исследования с людьми, доступ к чувствительным данным и клиентская отправка не разрешены. В будущем текущие полномочия проверяются по отдельному approvals.jsonl для точного action/scope/revision/hash, а не по статусу DECIDED.'
    assert old in text
    text = text.replace(old, '**Owner decision: DECIDED — приоритет помощи уже подключённым семьям сохранён; S-007, C-018.** Механизм и клиентский эффект остаются гипотезами C-016/C-017; финансовое основание UNKNOWN C-019. Альтернативы сохранены, арифметика перепроверена отдельным запуском D0003 без перезаписи старого результата. На момент D0003 пилот, бюджет, исследования с людьми, чувствительные данные и клиентская отправка не разрешены. Будущие полномочия проверяются отдельно по точному action/scope/revision/hash и approvals/action receipts.')
    text = text.replace('C-002…C-021, C-016…C-020', 'C-002, C-003, C-004, C-005, C-021, C-016, C-019, C-020')
    decision_path.write_text(text,encoding='utf-8')
    for name in SIX:
        path = revision / name
        text = path.read_text(encoding='utf-8')
        text = text.replace('C-018–C-017','C-016, C-017, C-018')
        text = text.replace('C-007 и C-012 заменены C-018 и C-016','история C-007 → C-015 → C-018 и C-012 → C-016 сохранена')
        text = text.replace('В конце Q2 владелец решает о следующем охвате по клиентским исходам и отдельным данным об оплатах','В контрольной точке Q2 владелец рассматривает только фактически готовые материалы по клиентским исходам и оплатам; их готовность к этой дате не установлена')
        path.write_text(text,encoding='utf-8')
    shutil.copyfile(revision/'strategy-product.md', revision/'strategy.md')
    # Machine controls and preservation are checked before copying current views.
    decision = decision_path.read_text(encoding='utf-8')
    state = (revision/'state.md').read_text(encoding='utf-8')
    assert '- **Revision:** D0003\n' in decision and '- Active complete revision ID: D0003\n' in state
    assert '- **Active claim IDs:** '+', '.join(active)+'\n' in decision
    assert '- Current claim IDs (active successors only; match manifest): '+', '.join(active)+'\n' in state
    assert len(active) == len(set(active))
    preserved = []
    for rid in ['D0001','D0002']:
        manifest = json.loads((CASE/f'revisions/{rid}/manifest.json').read_text(encoding='utf-8'))
        for entry in manifest['files']:
            if entry['path'].startswith('revisions/'):
                assert digest(CASE/entry['path']) == entry['sha256'], entry['path']
                preserved.append(entry['path'])
    save(OUT/'quality-review.json',dict(status='PASSED',checks=['candidate controls agree with active set','prior revision snapshot hashes unchanged','strategy alias byte-identical','targeted content corrections reviewed'],prior_snapshots_checked=preserved,limitations='Document review and arithmetic only; no empirical effect/feasibility asserted',draft_correction='Initial draft paragraph helper consumed decision metadata. Detected before gate/current-view handover; restored exact controls in decision only, fixed helper source; corrected malformed claim shorthand and inherited stale calculation wording. No published revision changed.'))
    event('D0003 draft quality review', 'SUCCESS', 'Detected and corrected draft-only decision metadata loss before publication; restored controls, corrected affected claim ranges and inherited calculation wording without regenerating the package. No failed filesystem write or gate; source helper corrected. Actual checks in research/D0003/quality-review.json; previous snapshot hashes unchanged.')
    print('QUALITY_REVIEW_PASSED; selected views still D0002')
elif mode == 'prepare':
    assert digest(CASE / 'revisions/D0002/manifest.json') == PARENT_HASH
    selected = json.loads((CASE / 'ACTIVE.json').read_text(encoding='utf-8'))
    assert selected == {'revision_id':'D0002','manifest_sha256':PARENT_HASH}
    revision = CASE / 'revisions/D0003'
    assert all((revision / name).is_file() for name in SIX)
    active = json.loads((OUT / 'active-claims.json').read_text(encoding='utf-8'))
    source_rows = [json.loads(line) for line in (CASE/'sources.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
    for sid in ['S-007','S-008','S-009']:
        source = next(row for row in source_rows if row['id'] == sid)
        assert digest(CASE/source['snapshot']) == source['sha256'], sid
    for sid, detail in [
        ('S-001','Saved OCR p1/3/4/6/9/10/11 read; original saved page images 3/9/11 visually checked; numeric table/rate/staffing confirmed. No source update.'),
        ('S-002','inputs/user-scope.md read; educational numbers and no external operator substitutions confirmed.'),
        ('S-006','inputs/user-choice-D0002.md read; historical family choice and scope preserved.'),
        ('S-007','Current user instruction saved verbatim in inputs/user-review-D0003.md; authorizes critical review, retains direction, no pilot/budget.'),
        ('S-008','Actual calculation output parsed and saved; input hashes and prior arithmetic equality checked, exit 0; no empirical effect inferred.'),
        ('S-009','Pinned D0002 strategy/decision/state/options/communication/test snapshots read for affected conclusions; old snapshot hashes unchanged; corrections detailed in review.md.'),
    ]:
        event('D0003 source '+sid,'SUCCESS',detail)
    event('D0003 final preparation', 'SUCCESS', 'Six successor snapshots complete; unchanged alternatives/client flow retained. Documentary audit and actual arithmetic receipt saved; no empirical results, pilot, budget or client delivery. Actual remaining time/money and guard UNKNOWN, no stage limit assigned; proceeding with six copies, shared gate, selector and post-classifier. See research/D0003/review.md; prior bytes preserved.')
    parent = json.loads((CASE / 'revisions/D0002/manifest.json').read_text(encoding='utf-8'))
    deps = {entry['path'] for entry in parent['files'] if not entry['path'].startswith('revisions/')}
    deps.update(f'revisions/D0002/{name}' for name in SIX)
    deps.update(f'revisions/D0003/{name}' for name in SIX)
    deps.add('revisions/D0003/strategy.md')
    deps.update(['inputs/user-review-D0003.md','calculations/D0003/audit.py','calculations/D0003/results.json'])
    deps.update(p.relative_to(CASE).as_posix() for p in OUT.iterdir() if p.is_file() and p.name not in ['check-candidate-receipt.json','post-classify-receipt.json','post-inventory-receipt.json'])
    save(revision / 'manifest.json', dict(revision_id='D0003',parent_revision_id='D0002',parent_manifest_sha256=PARENT_HASH,status='COMPLETE',active_claim_ids=active,files=[dict(path=name,sha256=digest(CASE/name)) for name in sorted(deps)]))
    # Final handover; snapshots are the only generated prose, views receive bytes.
    for name in SIX:
        shutil.copyfile(revision / name, CASE / name)
    shutil.copyfile(revision / 'strategy.md', CASE / 'strategy.md')
    print('PREPARED; selector unchanged; shared gate required')
elif mode == 'gate':
    receipt = run('check-candidate', ['tools/case_protocol.py','check-candidate',CASE_REL,'--revision','D0003'])
    print(receipt['stdout'])
elif mode == 'select':
    receipt = json.loads((OUT / 'check-candidate-receipt.json').read_text(encoding='utf-8'))
    assert receipt['exit_code'] == 0
    result = json.loads(receipt['stdout'])
    assert result['status'] == 'VALIDATED_CANDIDATE'
    manifest_hash = digest(CASE / 'revisions/D0003/manifest.json')
    assert result['revision_id'] == 'D0003' and result['manifest_sha256'] == manifest_hash
    save(CASE / 'ACTIVE.json', dict(revision_id='D0003',manifest_sha256=manifest_hash))
    post = run('post-classify', ['tools/case_protocol.py','classify',CASE_REL])
    assert post['stdout'].strip() == 'CHECKPOINTED'
    inventory = run('post-inventory', ['-m','tools.resume_context',CASE_REL])
    parsed = json.loads(inventory['stdout'])
    assert parsed['confirmed']['revision_id'] == 'D0003'
    assert parsed['unfinished']['drafts'] == [] and parsed['unfinished']['issues'] == []
    event('D0003 completion', 'SUCCESS', 'Actual shared gate VALIDATED_CANDIDATE then actual selector D0003 then classifier CHECKPOINTED; inventory no drafts/issues. New activity hints are receipt events, not unpublished analysis. Direction retained by S-007; economic goal, effect, payback, timing and implementation feasibility remain unproven. No pilot/budget/customer contact. Full change record research/D0003/review.md.')
    print(json.dumps(dict(status='CHECKPOINTED',revision_id='D0003',manifest_sha256=manifest_hash), indent=2))
else:
    raise ValueError(mode)
