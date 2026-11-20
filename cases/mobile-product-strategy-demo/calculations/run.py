"""Execute calculate.py and retain the actual command, outputs and hashes."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

here = Path(__file__).resolve().parent
case = here.parent
project = case.parents[1]
script = here / 'calculate.py'
command = [sys.executable, '-X', 'utf8', str(script)]
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
process = subprocess.run(command, cwd=project, capture_output=True, text=True, encoding='utf-8')
receipt = {
 'started_at_utc':started,'finished_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'command_argv':command,'cwd':str(project),'runtime_version':sys.version,
 'script_path':str(script),'script_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),
 'input_path':str(case / 'inputs/Пример брифа.pdf'),
 'input_sha256':hashlib.sha256((case / 'inputs/Пример брифа.pdf').read_bytes()).hexdigest(),
 'exit_code':process.returncode,'stdout':process.stdout,'stderr':process.stderr,
 'status':'PASS' if process.returncode == 0 else 'FAILED'
}
filename = 'receipt.json' if process.returncode == 0 else 'receipt-failed-'+datetime.datetime.now().strftime('%Y%m%dT%H%M%S')+'.json'
(here/filename).write_text(json.dumps(receipt, ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if process.returncode == 0:
    parsed = json.loads(process.stdout)
    (here/'results.json').write_text(json.dumps(parsed,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':receipt['status'],'receipt':str(here/filename),'exit_code':process.returncode},ensure_ascii=False))
if process.returncode:
    print(process.stderr)
sys.exit(process.returncode)
