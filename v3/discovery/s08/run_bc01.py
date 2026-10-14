"""Isolated read-only planning screens, retain failed logs."""
from pathlib import Path
import json
import subprocess
import sys
import hashlib
HERE=Path(__file__).resolve().parent;root=HERE/'bc01';root.mkdir(exist_ok=True)
jobs=['stars']+[c['name'] for c in json.loads((HERE/'gc02/design.json').read_text())['cases']]
if not(root/'design.json').exists():
    (root/'impl.py').write_bytes((HERE/'budget_cover.py').read_bytes());(root/'declaration.md').write_bytes((HERE/'budget_cover.md').read_bytes())
    (root/'design.json').write_text(json.dumps(dict(stage='DEVELOPMENT',contributor='Codex (GPT-6)',jobs=jobs,physical_audits=0,source_sha256=hashlib.sha256((HERE/'budget_cover.py').read_bytes()).hexdigest()),indent=2)+'\n')
for job in jobs:
    if(root/f'{job}.json').exists():continue
    index=1
    while(root/f'{job}_{index}.log').exists():index+=1
    with(root/f'{job}_{index}.log').open('w') as log:
        p=subprocess.run([sys.executable,'-B','-X',f'pycache_prefix={HERE/"unused_cache"}','-X','faulthandler',str(HERE/'budget_cover.py'),job],stdout=log,stderr=subprocess.STDOUT)
    print(job,index,p.returncode,flush=True)
    if p.returncode:raise SystemExit(p.returncode)
