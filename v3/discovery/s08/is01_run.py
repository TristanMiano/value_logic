"""Frozen paid invoice-service development, isolated attempts with retained logs."""
from datetime import datetime,timezone
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import time
HERE=Path(__file__).resolve().parent;ROOT=HERE/'is01'
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
ROOT.mkdir(exist_ok=False);(ROOT/'impl.py').write_bytes((HERE/'invoice_service.py').read_bytes())
old=json.loads((HERE/'ct01/design.json').read_text())['cases'];cases=[]
for case in old:
    for r in(2,8):cases.append(dict(name=case['name']+f'p{r}',costs=case['costs'],r=r,seed=8141520+len(cases)))
arms=('replay','circuit','ordinary_circuit','on_policy')
save(ROOT/'design.json',dict(stage='DEVELOPMENT',contributor='Codex (GPT-6)',cases=cases,arms=arms,requests=256,calibration_requests=128,
    created_utc=datetime.now(timezone.utc).isoformat(),source_sha256=sha(HERE/'invoice_service.py'),declaration_sha256=sha(HERE/'invoice_service.md'),
    dependencies={n:sha(HERE/n) for n in('circuit_targets.py','invoice_syntax.py','check_invoice_syntax.py','invoice_bandit.py',
        'invoice_completion.py','markov_paths.py','markov_service.py','star_learning.py','paired_invoices.py','continuum_policy.py','g01.py','action_audits.py')}))
results=[]
for case in cases:
    record=dict(name=case['name'],arms={},units={})
    for arm in arms:
        for attempt in range(1,5):
            unit=ROOT/f"{case['name']}_{arm}_{attempt}";begin=datetime.now(timezone.utc).isoformat();start=time.perf_counter_ns()
            with(ROOT/f'{unit.name}.txt').open('w') as out:
                try:code=subprocess.run([sys.executable,'-B','-X',f'pycache_prefix={HERE}/unused_cache','-X','faulthandler',str(HERE/'invoice_service.py'),str(unit),str(ROOT/'design.json'),case['name'],arm],stdout=out,stderr=out,timeout=90).returncode
                except subprocess.TimeoutExpired:code='timeout'
            with(ROOT/'processes.jsonl').open('a') as out:out.write(json.dumps(dict(case=case['name'],arm=arm,attempt=attempt,
                begin_utc=begin,end_utc=datetime.now(timezone.utc).isoformat(),wall_ns=time.perf_counter_ns()-start,returncode=code))+'\n')
            print(case['name'],arm,attempt,code,flush=True)
            if code==0:break
        else:raise RuntimeError('Repeated failures require inspection')
        record['units'][arm]=unit.name;record['arms'][arm]=json.loads((unit/'result.json').read_text())
        save(ROOT/'progress.json',dict(completed=results,current=record))
    for key in('base_audit_fee','physical_audits','named_units','action_fee','pilot_fee','selected_policies','final_choice','sums'):
        assert record['arms']['circuit'][key]==record['arms']['ordinary_circuit'][key]
    for key in('action_fee','selected_policies','final_choice','sums'):
        assert record['arms']['replay'][key]==record['arms']['circuit'][key]
    results.append(record);save(ROOT/'results.json',dict(status='running',cases=results))
save(ROOT/'results.json',dict(status='complete',cases=results,failed_prefix_cost='Unknown wherever no complete invoice survived; preserve all process records and prefixes'))
