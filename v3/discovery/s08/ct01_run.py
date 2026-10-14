"""Isolated conditional circuit-target screen, preserving all failed attempts."""
from datetime import datetime,timezone
from itertools import product
from pathlib import Path
import hashlib
import json
import random
import subprocess
import sys
import time
HERE=Path(__file__).resolve().parent;ROOT=HERE/'ct01'
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
ROOT.mkdir(exist_ok=False);(ROOT/'impl.py').write_bytes((HERE/'circuit_targets.py').read_bytes())
fees=random.Random(8141510);world_rng=random.Random(8141511);cases=[]
for n in(3,4,5,6,8,10):
    for repeat in range(2):
        worlds=list(product((0,1),repeat=n)) if n<=6 else[tuple(world_rng.randrange(2) for _ in range(n)) for _ in range(128)]
        cases.append(dict(name=f'n{n}r{repeat}',costs=[fees.randrange(1,10) for _ in range(n)],worlds=worlds))
save(ROOT/'design.json',dict(stage='DEVELOPMENT',contributor='Codex (GPT-6)',cases=cases,fee_seed=8141510,world_seed=8141511,
    source_sha256=sha(HERE/'circuit_targets.py'),declaration_sha256=sha(HERE/'circuit_targets.md'),created_utc=datetime.now(timezone.utc).isoformat(),physical_audits=0))
result=[]
for case in cases:
    for attempt in range(1,5):
        unit=ROOT/f"{case['name']}a{attempt}";begin=datetime.now(timezone.utc).isoformat();start=time.perf_counter_ns()
        with (ROOT/f'{unit.name}.txt').open('w') as out:
            try:code=subprocess.run([sys.executable,'-B','-X',f'pycache_prefix={HERE}/unused_cache','-X','faulthandler',str(HERE/'circuit_targets.py'),str(unit),str(ROOT/'design.json'),case['name']],stdout=out,stderr=out,timeout=90).returncode
            except subprocess.TimeoutExpired:code='timeout'
        with(ROOT/'processes.jsonl').open('a') as out:out.write(json.dumps(dict(case=case['name'],attempt=attempt,begin_utc=begin,
            end_utc=datetime.now(timezone.utc).isoformat(),wall_ns=time.perf_counter_ns()-start,returncode=code))+'\n')
        print(case['name'],attempt,code,flush=True)
        if code==0:break
    else:raise RuntimeError('Repeated failures require inspection')
    result.append(dict(name=case['name'],unit=unit.name,result=json.loads((unit/'result.json').read_text())));save(ROOT/'results.json',dict(status='running',cases=result))
save(ROOT/'results.json',dict(status='complete',cases=result))
