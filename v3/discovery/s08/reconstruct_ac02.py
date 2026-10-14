"""Isolated ac02 reconstruction with preserved failure logs."""
from pathlib import Path
import json
import subprocess
import sys
HERE=Path(__file__).resolve().parent;root=HERE/'ac02';design=json.loads((root/'design.json').read_text())
for case in design['cases']:
    for arm in design['arms']:
        label=case['name']+'_'+arm
        if(root/(label+'_reconstruction.json')).exists():continue
        index=1
        while(root/f'{label}_reconstruction_{index}.log').exists():index+=1
        with(root/f'{label}_reconstruction_{index}.log').open('w') as log:
            p=subprocess.run([sys.executable,'-B','-X',f'pycache_prefix={HERE/"unused_cache"}','-X','faulthandler',str(HERE/'check_ac02.py'),case['name'],arm],stdout=log,stderr=subprocess.STDOUT)
        print(label,index,p.returncode,flush=True)
        if p.returncode:raise SystemExit(p.returncode)
