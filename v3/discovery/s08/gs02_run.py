"""Freeze and execute gs02, preserving all retry prefixes."""
from datetime import datetime,timezone
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import time
HERE=Path(__file__).resolve().parent;ROOT=HERE/'gs02'
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
ROOT.mkdir(exist_ok=False);(ROOT/'impl.py').write_bytes((HERE/'graph_service2.py').read_bytes())
(ROOT/'declaration.md').write_bytes((HERE/'adaptive_graph.md').read_bytes())
cases=json.loads((HERE/'gs01/design.json').read_text())['cases'];arms=('greedy','adaptive_dual','ordinary_adaptive')
save(ROOT/'design.json',dict(stage='DEVELOPMENT',contributor='Codex (GPT-6)',created_utc=datetime.now(timezone.utc).isoformat(),cases=cases,arms=arms,
    source_sha256=sha(HERE/'graph_service2.py'),declaration_sha256=sha(HERE/'adaptive_graph.md'),
    dependencies={n:sha(HERE/n) for n in('graph_incremental.py','graph_service.py','graph_audits.py','g01.py','star_learning.py','action_audits.py')}))
results=[]
for case in cases:
    record=dict(name=case['name'],arms={},units={})
    for arm in arms:
        for attempt in range(1,5):
            unit=ROOT/f"{case['name']}_{arm}_{attempt}";begin=datetime.now(timezone.utc).isoformat();start=time.perf_counter_ns()
            with(ROOT/f'{unit.name}.txt').open('w') as out:
                try:code=subprocess.run([sys.executable,'-B','-X',f'pycache_prefix={HERE}/unused_cache','-X','faulthandler',str(HERE/'graph_service2.py'),str(unit),str(ROOT/'design.json'),case['name'],arm],stdout=out,stderr=out,timeout=90).returncode
                except subprocess.TimeoutExpired:code='timeout'
            with(ROOT/'processes.jsonl').open('a') as out:out.write(json.dumps(dict(case=case['name'],arm=arm,attempt=attempt,begin_utc=begin,end_utc=datetime.now(timezone.utc).isoformat(),wall_ns=time.perf_counter_ns()-start,returncode=code))+'\n')
            print(case['name'],arm,attempt,code,flush=True)
            if code==0:break
        else:raise RuntimeError('Repeated failure requires inspection')
        record['units'][arm]=unit.name;record['arms'][arm]=json.loads((unit/'result.json').read_text())
        save(ROOT/'progress.json',dict(completed=results,current=record))
    for key in('base_audit_fee','physical_audits','named_units','lower_bound_sum'):
        assert record['arms']['adaptive_dual'][key]==record['arms']['ordinary_adaptive'][key]
    results.append(record);save(ROOT/'results.json',dict(status='running',cases=results))
save(ROOT/'results.json',dict(status='complete',cases=results,failed_prefix_cost='Unknown unless a complete invoice survives; preserve every prefix and process record'))
