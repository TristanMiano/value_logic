"""Cold, explicitly logged pt01 development diagnostics."""
from pathlib import Path
import json
import subprocess
import sys
import policy_tradeoff as pt
root=pt.HERE/'pt01'
if not root.exists():
    root.mkdir();design=json.loads((pt.HERE/'op01/design.json').read_text());design['source_sha256']=pt.g01.sha(pt.__file__);design['physical_audits']=0
    pt.g01.save(root/'design.json',design);(root/'impl.py').write_bytes(Path(pt.__file__).read_bytes());(root/'declaration.md').write_bytes((pt.HERE/'policy_tradeoff.md').read_bytes())
design=json.loads((root/'design.json').read_text())
for case in design['cases']:
    for price,tau in case['duties']:
        label=f"{case['name']}_{price}_{tau}";directory=root/label
        if(directory/'results.json').exists():continue
        if directory.exists():raise RuntimeError('Incomplete diagnostic unit needs explicit disposition: '+label)
        index=1
        while(root/f'{label}_{index}.log').exists():index+=1
        with(root/f'{label}_{index}.log').open('w') as log:
            p=subprocess.run([sys.executable,'-B','-X',f'pycache_prefix={pt.HERE/"unused_cache"}','-X','faulthandler',str(pt.HERE/'policy_tradeoff.py'),str(root),case['name'],str(price),str(tau)],stdout=log,stderr=subprocess.STDOUT)
        print(label,index,p.returncode,flush=True)
        if p.returncode:raise SystemExit(p.returncode)
