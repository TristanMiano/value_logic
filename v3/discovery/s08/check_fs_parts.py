"""Isolate larger read-only checks by arm and duty; preserve every failure."""
from pathlib import Path
import json
import subprocess
import sys
import g01
HERE=Path(__file__).resolve().parent;ROOT=HERE/'fs01';design=json.loads((ROOT/'design.json').read_text());results=json.loads((ROOT/'results.json').read_text())
for case in design['cases']:
    if len(case['weights'])!=6:continue
    record=next(c for c in results['cases'] if c['name']==case['name']);answers={}
    for arm in design['arms']:
        parts=[]
        for price,tau in case['duties']:
            stem=f"{case['name']}_{arm}_{price}_{tau}"
            for attempt in range(1,5):
                with(ROOT/f'{stem}_check{attempt}.txt').open('w') as out:
                    code=subprocess.run([sys.executable,'-B','-X',f'pycache_prefix={HERE}/unused_cache','-X','faulthandler',str(HERE/'check_fs01.py'),case['name'],arm,str(price),str(tau)],stdout=out,stderr=out).returncode
                print(stem,attempt,code,flush=True)
                if code==0:break
            else:raise RuntimeError('Repeated checking failure')
            parts.append(json.loads((ROOT/f'{stem}_reconstruction.json').read_text())['arms'][arm])
        total={k:sum(p[k] for p in parts) for k in('outputs','fee','physical_receipts','named_service_units','compatible_cost_worlds')}
        saved=record['arms'][arm];assert(total['outputs'],total['fee'],total['physical_receipts'],total['named_service_units']+saved['setup_units'])==tuple(saved[k] for k in('outputs','base_audit_fee','physical_audits','named_units'))
        requests=[r for p in parts for r in p['requests']];assert len(requests)==len(set(requests))==total['outputs']
        total['trace_sha256']=parts[0]['trace_sha256'];assert all(p['trace_sha256']==total['trace_sha256'] for p in parts);answers[arm]=total
    g01.save(ROOT/f"{case['name']}_reconstruction.json",dict(status='checked',arms=answers,method='Union of disjoint arm/duty cold-process checks',physical_new_audits=0))
