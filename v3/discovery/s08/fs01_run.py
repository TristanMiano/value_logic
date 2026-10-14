"""Freeze fs01, acquire actual geometry first, then execute isolated arms."""
from datetime import datetime,timezone
from pathlib import Path
import json
import random
import subprocess
import sys
import time
import frontier_service as fs
g01=fs.g01;HERE=Path(__file__).resolve().parent;ROOT=HERE/'fs01'
ROOT.mkdir(exist_ok=False);(ROOT/'impl.py').write_bytes((HERE/'frontier_service.py').read_bytes());(ROOT/'declaration.md').write_bytes((HERE/'frontier_service.md').read_bytes())
rng=random.Random(8141610);cases=[]
for old in json.loads((HERE/'rf01/design.json').read_text())['cases']:
    n=len(old['weights'])
    if n not in(1,3,6):continue
    W=sum(old['weights']);H=10*W
    cases.append(dict(name=old['name'],weights=old['weights'],fees=[rng.randrange(1,8) for _ in range(n+1)]+[10],H=H,
        seed=8141620+len(cases),duties=sorted(set((price,tau) for price in(H,H+W,H+2*W) for tau in(W,3*W//2,2*W)))))
arms=('frontier','ordinary_frontier','repair_minimax','full')
g01.save(ROOT/'design.json',dict(stage='DEVELOPMENT',contributor='Codex (GPT-6)',created_utc=datetime.now(timezone.utc).isoformat(),cases=cases,arms=arms,
    source_sha256=g01.sha(HERE/'frontier_service.py'),declaration_sha256=g01.sha(HERE/'frontier_service.md'),
    dependencies={n:g01.sha(HERE/n) for n in('replacement_frontier.py','g01.py','action_audits.py')}))
for case in cases:
    data=fs.source(case['weights'],case['fees'],case['H']);geometry=fs.acquire_geometry(data)
    g01.save(ROOT/f"{case['name']}_geometry.json",geometry)
    meter=fs.Meter();fs.admit(data,geometry,meter);g01.save(ROOT/f"{case['name']}_geometry_check.json",dict(checked=True,invoice=meter.record(),receipt=geometry['receipt']['identity']))
results=[]
for case in cases:
    record=dict(name=case['name'],arms={},units={})
    for arm in arms:
        for attempt in range(1,5):
            unit=ROOT/f"{case['name']}_{arm}_{attempt}";begin=datetime.now(timezone.utc).isoformat();start=time.perf_counter_ns()
            with(ROOT/f'{unit.name}.txt').open('w') as out:
                try:code=subprocess.run([sys.executable,'-B','-X',f'pycache_prefix={HERE}/unused_cache','-X','faulthandler',str(HERE/'frontier_service.py'),str(unit),str(ROOT/'design.json'),case['name'],arm],stdout=out,stderr=out,timeout=90).returncode
                except subprocess.TimeoutExpired:code='timeout'
            with(ROOT/'processes.jsonl').open('a') as out:out.write(json.dumps(dict(case=case['name'],arm=arm,attempt=attempt,begin_utc=begin,end_utc=datetime.now(timezone.utc).isoformat(),wall_ns=time.perf_counter_ns()-start,returncode=code))+'\n')
            print(case['name'],arm,attempt,code,flush=True)
            if code==0:break
        else:raise RuntimeError('Repeated failure requires inspection')
        record['units'][arm]=unit.name;record['arms'][arm]=json.loads((unit/'result.json').read_text())
        g01.save(ROOT/'progress.json',dict(completed=results,current=record))
    for key in('base_audit_fee','physical_audits','named_units'):
        assert record['arms']['frontier'][key]==record['arms']['ordinary_frontier'][key]
    results.append(record);g01.save(ROOT/'results.json',dict(status='running',cases=results))
g01.save(ROOT/'results.json',dict(status='complete',cases=results,physical_resolution_steps=6,complete_sat_calls=0,
    failed_prefix_cost='Unknown unless a complete invoice survives; preserve every prefix and process record'))
