"""Cold process op01 stages; failures remain explicit and stop dependent work."""
from pathlib import Path
import json
import subprocess
import sys
HERE=Path(__file__).resolve().parent;root=HERE/'op02';design=json.loads((root/'design.json').read_text());mode=sys.argv[1]
cases=[c for c in design['cases'] if len(sys.argv)<3 or c['name']==sys.argv[2]]
for case in cases:
    for price,tau in case['duties']:
        label=f"{case['name']}_{price}_{tau}";pd=root/(label+'_policy')
        if mode in('build','check'):
            target=pd/('planning.json' if mode=='build' else 'checking.json')
            if target.exists():continue
            args=[mode,str(root),case['name'],str(price),str(tau)];jobs=[(label+'_'+mode,args)]
        else:
            jobs=[]
            for arm in design['arms']:
                output=root/(label+'_'+arm)
                if (output/'result.json').exists():continue
                if output.exists():raise RuntimeError('Incomplete physical acquisition requires explicit disposition: '+str(output))
                jobs.append((label+'_'+arm,['run',str(root),case['name'],str(price),str(tau),arm,str(output)]))
        for name,args in jobs:
            index=1
            while(root/f'{name}_{index}.log').exists():index+=1
            with(root/f'{name}_{index}.log').open('w') as log:
                p=subprocess.run([sys.executable,'-B','-X',f'pycache_prefix={HERE/"unused_cache"}','-X','faulthandler',str(HERE/'policy_safety.py'),*args],stdout=log,stderr=subprocess.STDOUT)
            print(name,index,p.returncode,flush=True)
            if p.returncode:raise SystemExit(p.returncode)

