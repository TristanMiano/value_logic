"""Cold general-graph proof/cover screens with explicit failure logs."""
from pathlib import Path
import json
import subprocess
import sys
HERE=Path(__file__).resolve().parent;root=HERE/'gc01';design=json.loads((root/'design.json').read_text())
for case in design['cases']:
    name=case['name'];directory=root/name
    if(directory/'results.json').exists():continue
    if directory.exists():raise RuntimeError('Incomplete unit needs explicit disposition: '+name)
    index=1
    while(root/f'{name}_{index}.log').exists():index+=1
    with(root/f'{name}_{index}.log').open('w') as log:
        p=subprocess.run([sys.executable,'-B','-X',f'pycache_prefix={HERE/"unused_cache"}','-X','faulthandler',str(HERE/'graph_cover.py'),'run',str(root),name],stdout=log,stderr=subprocess.STDOUT)
    print(name,index,p.returncode,flush=True)
    if p.returncode:raise SystemExit(p.returncode)
