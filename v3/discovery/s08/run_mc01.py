from pathlib import Path
import json
import subprocess
import sys
HERE=Path(__file__).resolve().parent;root=HERE/'mc01';design=json.loads((root/'design.json').read_text())
for case in design['cases']:
    name=case['name']
    if(root/f'{name}.json').exists():continue
    index=1
    while(root/f'{name}_{index}.log').exists():index+=1
    with(root/f'{name}_{index}.log').open('w') as log:
        p=subprocess.run([sys.executable,'-B','-X',f'pycache_prefix={HERE/"unused_cache"}','-X','faulthandler',str(HERE/'matroid_cover.py'),name],stdout=log,stderr=subprocess.STDOUT)
    print(name,index,p.returncode,flush=True)
    if p.returncode:raise SystemExit(p.returncode)
