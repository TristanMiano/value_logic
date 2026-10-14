"""Isolated units; all failures retained under author stochastic-retry authority."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib
import json
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent;ROOT=HERE/'ib02'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
ROOT.mkdir(exist_ok=False);(ROOT/'impl.py').write_bytes((HERE/'pruned_bandit.py').read_bytes())
design=json.loads((HERE/'cs01/design.json').read_text())
save(ROOT/'design.json',dict(stage='DEVELOPMENT',contributor='Codex (GPT-6)',created_utc=datetime.now(timezone.utc).isoformat(),
    cases=design['cases'],requests=1024,arm='ordinary_invoice',exposure='same exposed cs01 rows',
    source_sha256=sha(HERE/'pruned_bandit.py'),declaration_sha256=sha(HERE/'pruned_bandit.md'),
    dependencies={n:sha(HERE/n) for n in ('invoice_bandit.py','invoice_syntax.py','check_invoice_syntax.py','invoice_completion.py','markov_paths.py','markov_service.py','star_learning.py','g01.py','action_audits.py','continuum_policy.py')}))
result=dict(status='running',cases=[])
for case in design['cases']:
    for attempt in range(1,5):
        unit=ROOT/f"{case['name']}_{attempt}";begin=datetime.now(timezone.utc).isoformat();start=time.perf_counter_ns()
        with (ROOT/f"{unit.name}.txt").open('w') as log:
            try:
                proc=subprocess.run([sys.executable,'-B','-X',f'pycache_prefix={HERE}/unused_cache','-X','faulthandler',
                    str(HERE/'pruned_bandit.py'),str(unit),case['name']],stdout=log,stderr=log,timeout=60)
                code=proc.returncode
            except subprocess.TimeoutExpired:code='timeout'
        with (ROOT/'processes.jsonl').open('a') as log:log.write(json.dumps(dict(case=case['name'],attempt=attempt,
            begin_utc=begin,end_utc=datetime.now(timezone.utc).isoformat(),wall_ns=time.perf_counter_ns()-start,returncode=code))+'\n')
        print(case['name'],attempt,code,flush=True)
        if code==0:break
    else:raise RuntimeError('Four failures require explicit inspection')
    result['cases'].append(dict(name=case['name'],unit=unit.name,ordinary_invoice=json.loads((unit/'result.json').read_text())))
    save(ROOT/'results.json',result)
result.update(status='complete',completed_utc=datetime.now(timezone.utc).isoformat());save(ROOT/'results.json',result)

