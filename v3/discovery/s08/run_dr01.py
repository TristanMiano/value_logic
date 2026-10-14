"""Freeze and run explicit ordinary decision-region screen, with cold processes."""
from pathlib import Path
import json
import subprocess
import sys
import region_policy as rp
root=rp.HERE/'dr01'
if not root.exists():
    root.mkdir();design=json.loads((rp.HERE/'op01/design.json').read_text());design['source_sha256']=rp.g01.sha(rp.__file__);design['physical_audits']=0
    rp.g01.save(root/'design.json',design);(root/'impl.py').write_bytes(Path(rp.__file__).read_bytes());(root/'declaration.md').write_bytes((rp.HERE/'decision_regions.md').read_bytes())
design=json.loads((root/'design.json').read_text())
for case in design['cases']:
    for price,tau in case['duties']:
        label=f"{case['name']}_{price}_{tau}";directory=root/label
        if(directory/('screen.json' if len(case['weights'])==2 else 'checking.json')).exists():continue
        if directory.exists():raise RuntimeError('Preserve/dispose incomplete unit before retry: '+label)
        index=1
        while(root/f'{label}_{index}.log').exists():index+=1
        with(root/f'{label}_{index}.log').open('w') as log:
            p=subprocess.run([sys.executable,'-B','-X',f'pycache_prefix={rp.HERE/"unused_cache"}','-X','faulthandler',str(rp.HERE/'region_policy.py'),str(root),case['name'],str(price),str(tau)],stdout=log,stderr=subprocess.STDOUT)
        print(label,index,p.returncode,flush=True)
        if p.returncode:raise SystemExit(p.returncode)
