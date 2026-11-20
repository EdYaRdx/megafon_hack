import datetime,hashlib,json,subprocess,sys
from pathlib import Path
here=Path(__file__).resolve().parent
case=here.parents[1]; project=case.parents[1]
command=[sys.executable,'-X','utf8',str(here/'calculate.py')]
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
p=subprocess.run(command,cwd=project,capture_output=True,text=True,encoding='utf-8')
receipt={'command_argv':command,'cwd':str(project),'started_at_utc':started,'finished_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runtime_version':sys.version,'script_sha256':hashlib.sha256((here/'calculate.py').read_bytes()).hexdigest(),'input_path':'inputs/R0002-scenario.json','input_sha256':hashlib.sha256((case/'inputs/R0002-scenario.json').read_bytes()).hexdigest(),'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'status':'PASS' if p.returncode==0 else 'FAILED'}
dest=here/('receipt.json' if p.returncode==0 else 'receipt-failed-'+datetime.datetime.now().strftime('%Y%m%dT%H%M%S')+'.json')
if dest.exists(): raise RuntimeError('Do not overwrite existing calculation receipt')
dest.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if p.returncode==0:
    result=json.loads(p.stdout)
    (here/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ['status','total_opportunity_number_months','required_extra_paid_number_months','required_weighted_average_gap_percentage_points','gp_rub_conditional','stress_gp_rub','no_effect_gp_rub_if_cost_incurred']},ensure_ascii=False))
else: print(p.stderr)
sys.exit(p.returncode)
