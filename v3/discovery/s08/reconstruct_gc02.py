"""Cold gc02 reconstruction; preserve all diagnostic failures."""
from pathlib import Path
import json
import subprocess
import sys
HERE=Path(__file__).resolve().parent;root=HERE/'gc02';design=json.loads((root/'design.json').read_text())
jobs=[(case['name'],arm,False) for case in design['cases'] for arm in design['arms']]+[('n32_clique','scan',True)]
for name,arm,prefix in jobs:
    label=name+'_'+arm+('_failed_prefix' if prefix else'')
    if(root/f'{label}_reconstruction.json').exists():continue
    index=1
    while(root/f'{label}_reconstruction_{index}.log').exists():index+=1
    args=[name,arm]+(['prefix'] if prefix else[])
    with(root/f'{label}_reconstruction_{index}.log').open('w') as log:
        p=subprocess.run([sys.executable,'-B','-X',f'pycache_prefix={HERE/"unused_cache"}','-X','faulthandler',str(HERE/'check_gc02.py'),*args],stdout=log,stderr=subprocess.STDOUT)
    print(label,index,p.returncode,flush=True)
    if p.returncode:raise SystemExit(p.returncode)
