"""Prospective bounded compositional invoice screen, isolated process units."""
from datetime import datetime,timezone
from pathlib import Path
import hashlib
import json
import random
import subprocess
import sys
import time
HERE=Path(__file__).resolve().parent;ROOT=HERE/'ia01'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
ROOT.mkdir(exist_ok=False);(ROOT/'impl.py').write_bytes((HERE/'invoice_add.py').read_bytes())
small=[json.loads(p.read_text()) for p in sorted((HERE/'pi01').glob('*/result.json'))]
assert len(small)==16
cases=[dict(name=f"n{d['n']}r{d['repeat']}",costs=d['costs']) for d in sorted(small,key=lambda d:(d['n'],d['repeat']))]
rng=random.Random(8141501)
cases +=[dict(name=f'n{n}r{r}',costs=[rng.randrange(1,10) for _ in range(n)]) for n in (16,32,64) for r in range(2)]
save(ROOT/'design.json',dict(stage='DEVELOPMENT',contributor='Codex (GPT-6)',cases=cases,large_seed=8141501,
    created_utc=datetime.now(timezone.utc).isoformat(),node_cap=250000,apply_state_cap=2000000,
    per_attempt_wall_timeout_seconds=120,source_sha256=sha(HERE/'invoice_add.py'),declaration_sha256=sha(HERE/'paired_invoices.md'),
    dependencies={n:sha(HERE/n) for n in ('paired_invoices.py','invoice_completion.py','markov_paths.py','continuum_policy.py','g01.py')}))
results=[]
for case in cases:
    for attempt in range(1,5):
        unit=ROOT/f"{case['name']}a{attempt}";start=time.perf_counter_ns();begin=datetime.now(timezone.utc).isoformat()
        with (ROOT/f'{unit.name}.txt').open('w') as log:
            try:code=subprocess.run([sys.executable,'-B','-X',f'pycache_prefix={HERE}/unused_cache','-X','faulthandler',
                str(HERE/'invoice_add.py'),str(unit),json.dumps(case['costs'])],stdout=log,stderr=log,timeout=120).returncode
            except subprocess.TimeoutExpired:code='timeout'
        with (ROOT/'processes.jsonl').open('a') as log:log.write(json.dumps(dict(case=case['name'],attempt=attempt,
            begin_utc=begin,end_utc=datetime.now(timezone.utc).isoformat(),wall_ns=time.perf_counter_ns()-start,returncode=code))+'\n')
        print(case['name'],attempt,code,flush=True)
        if code==0:break
    else:raise RuntimeError('Repeated failures: inspect')
    results.append(dict(name=case['name'],unit=unit.name,result=json.loads((unit/'result.json').read_text())))
    save(ROOT/'results.json',dict(status='running',cases=results))
save(ROOT/'results.json',dict(status='complete',cases=results,failed_prefix_cost='unknown; see every process and prefix'))
