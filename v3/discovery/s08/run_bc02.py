"""Run frozen bc02 units or read-only reconstruction, retaining logs."""
from pathlib import Path
import json
import subprocess
import sys
HERE=Path(__file__).resolve().parent;root=HERE/'bc02';design=json.loads((root/'design.json').read_text());mode=sys.argv[1]
for case in design['cases']:
    for arm in design['arms']:
        label=case['name']+'_'+arm;done=root/(label+'_reconstruction.json') if mode=='check' else root/label/'result.json'
        if done.exists():continue
        index=1
        while(root/f'{label}_{mode}_{index}.log').exists():index+=1
        args=[str(HERE/'check_bc02.py'),case['name'],arm] if mode=='check' else[str(HERE/'budget_service.py'),'run',str(root),case['name'],arm,str(root/label)]
        with(root/f'{label}_{mode}_{index}.log').open('w') as log:
            p=subprocess.run([sys.executable,'-B','-X',f'pycache_prefix={HERE/"unused_cache"}','-X','faulthandler',*args],stdout=log,stderr=subprocess.STDOUT)
        print(label,mode,index,p.returncode,flush=True)
        if p.returncode:raise SystemExit(p.returncode)
