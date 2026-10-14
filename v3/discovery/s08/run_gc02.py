"""Actual gc02 isolated acquisition processes; no silent prefix replay."""
from pathlib import Path
import json
import subprocess
import sys
HERE=Path(__file__).resolve().parent;root=HERE/'gc02';design=json.loads((root/'design.json').read_text())
overrides=json.loads((root/'attempts.json').read_text())['overrides'] if(root/'attempts.json').exists() else {}
for case in design['cases']:
    for arm in design['arms']:
        label=case['name']+'_'+arm;directory=root/overrides.get(label,{}).get('selected_directory',label)
        if(directory/'result.json').exists():continue
        if directory.exists():raise RuntimeError('Physical prefix needs explicit disposition: '+label)
        index=1
        while(root/f'{label}_{index}.log').exists():index+=1
        with(root/f'{label}_{index}.log').open('w') as log:
            p=subprocess.run([sys.executable,'-B','-X',f'pycache_prefix={HERE/"unused_cache"}','-X','faulthandler',str(HERE/'graph_cover_service.py'),'run',str(root),case['name'],arm,str(directory)],stdout=log,stderr=subprocess.STDOUT)
        print(label,index,p.returncode,flush=True)
        if p.returncode:raise SystemExit(p.returncode)

