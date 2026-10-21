"""DEVELOPMENT local inequality screen; all 3-bit invoice functions/subsets."""
from pathlib import Path
import hashlib
import importlib.util
import json
import time

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'s12/parity_price_probe.py'
spec=importlib.util.spec_from_file_location('invoice_enumerator',SOURCE)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
begun=time.perf_counter_ns()
n=3
bank=mod.all_invoice_functions((1,)*n,3)
edges=[(x,x^(1<<i)) for x in range(1<<n) for i in range(n) if not (x>>i&1)]
checks=0;tight=0;minimum=None;counterexample=None
for function in sorted(bank):
    for mask in range(1,1<<(1<<n)):
        fee=sum(c for x,c in enumerate(function) if mask>>x&1)
        removed=sum(1 for x,y in edges if mask>>x&1 and mask>>y&1 and function[x]!=function[y])
        checks+=1
        if removed:
            ratio=fee/removed
            if minimum is None or ratio<minimum['ratio']:
                minimum=dict(ratio=ratio,fee=fee,removed=removed,mask=mask,function=function)
            tight+=3*fee==7*removed
        if 3*fee<7*removed:
            counterexample=dict(mask=mask,function=function,fee=fee,removed=removed)
            break
    if counterexample:break
result=dict(status='COUNTEREXAMPLE' if counterexample else 'PASS',
            contributor='Codex (GPT-6)',scope='same-model finite local screen',
            n=n,cap=3,functions=len(bank),checks=checks,tight_cases=tight,
            minimum=minimum,counterexample=counterexample,
            elapsed_ns=time.perf_counter_ns()-begun,
            hashes={str(p.relative_to(HERE.parent)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in (Path(__file__),SOURCE)})
(HERE/'edge_probe.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result))
