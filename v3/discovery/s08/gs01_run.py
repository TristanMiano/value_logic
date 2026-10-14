"""Freeze and execute gs01 with isolated, preserved stochastic retries."""
from datetime import datetime,timezone
from pathlib import Path
import hashlib
import json
import random
import subprocess
import sys
import time
HERE=Path(__file__).resolve().parent;ROOT=HERE/'gs01'
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
ROOT.mkdir(exist_ok=False);(ROOT/'impl.py').write_bytes((HERE/'graph_service.py').read_bytes())
(ROOT/'declaration.md').write_bytes((HERE/'graph_service.md').read_bytes())
(ROOT/'graph_audits.py').write_bytes((HERE/'graph_audits.py').read_bytes())
rng=random.Random(8141570);cases=[]
for n in(16,64,256):
    path=[(i,i+1) for i in range(n-1)]
    options=dict(path=path,star=[(0,i) for i in range(1,n)],cycle=sorted(set(path+[(0,n-1)])),
        sparse=sorted(set(path+[(i,j) for i in range(n) for j in range(i+1,n) if rng.randrange(n)<2])))
    for shape,edges in options.items():cases.append(dict(name=f'n{n}_{shape}',costs=[rng.randrange(1,10) for i in range(n)],edges=edges,seed=8141580+len(cases)))
arms=('primal_dual','ordinary_dual','greedy','full')
save(ROOT/'design.json',dict(stage='DEVELOPMENT',contributor='Codex (GPT-6)',created_utc=datetime.now(timezone.utc).isoformat(),cases=cases,arms=arms,
    source_sha256=sha(HERE/'graph_service.py'),declaration_sha256=sha(HERE/'graph_service.md'),
    dependencies={n:sha(HERE/n) for n in('graph_audits.py','g01.py','star_learning.py','action_audits.py')}))
results=[]
for case in cases:
    record=dict(name=case['name'],arms={},units={})
    for arm in arms:
        for attempt in range(1,5):
            unit=ROOT/f"{case['name']}_{arm}_{attempt}";begin=datetime.now(timezone.utc).isoformat();start=time.perf_counter_ns()
            with(ROOT/f'{unit.name}.txt').open('w') as out:
                try:code=subprocess.run([sys.executable,'-B','-X',f'pycache_prefix={HERE}/unused_cache','-X','faulthandler',str(HERE/'graph_service.py'),str(unit),str(ROOT/'design.json'),case['name'],arm],stdout=out,stderr=out,timeout=90).returncode
                except subprocess.TimeoutExpired:code='timeout'
            with(ROOT/'processes.jsonl').open('a') as out:out.write(json.dumps(dict(case=case['name'],arm=arm,attempt=attempt,begin_utc=begin,end_utc=datetime.now(timezone.utc).isoformat(),wall_ns=time.perf_counter_ns()-start,returncode=code))+'\n')
            print(case['name'],arm,attempt,code,flush=True)
            if code==0:break
        else:raise RuntimeError('Repeated failure requires inspection')
        record['units'][arm]=unit.name;record['arms'][arm]=json.loads((unit/'result.json').read_text())
        save(ROOT/'progress.json',dict(completed=results,current=record))
    for key in('base_audit_fee','physical_audits','named_units','lower_bound_sum'):
        assert record['arms']['primal_dual'][key]==record['arms']['ordinary_dual'][key]
    results.append(record);save(ROOT/'results.json',dict(status='running',cases=results))
save(ROOT/'results.json',dict(status='complete',cases=results,failed_prefix_cost='Unknown unless a complete invoice survives; preserve every prefix and process record'))
