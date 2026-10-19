"""DEVELOPMENT screen of a candidate, not an asserted theorem."""
from itertools import product
from pathlib import Path
import hashlib
import json
import sys
import time
from parity_price_probe import all_invoice_functions,partitions

HERE=Path(__file__).resolve().parent


def panel(n):
    nw=1<<n
    potential=[0]*(1<<nw)
    for spec in product([-1,0,1],repeat=n):
        dim=spec.count(-1)
        if not dim:
            continue
        mask=sum(1<<x for x in range(nw)
                 if all(v==-1 or (x>>i&1)==v for i,v in enumerate(spec)))
        potential[mask]+=3 if dim==1 else -2*(-3)**(dim-2)
    for i in range(nw):
        bit=1<<i
        for w in range(1<<nw):
            if w&bit:
                potential[w]+=potential[w^bit]
    bank=partitions(all_invoice_functions((1,)*n,3))
    checks=0
    for w in sorted(range(1,1<<nw),key=int.bit_count):
        for program in bank:
            groups=[(c,s&w) for c,s in program if s&w]
            if len(groups)<2:
                continue
            rhs=sum(c*s.bit_count()+potential[s] for c,s in groups)
            checks+=1
            if potential[w]>rhs:
                return dict(n=n,status='counterexample',checks=checks,source_mask=w,
                            source_worlds=[x for x in range(nw) if w>>x&1],
                            lhs=potential[w],rhs=rhs,
                            groups=[dict(cost=c,mask=s,potential=potential[s]) for c,s in groups])
    return dict(n=n,status='no_counterexample_in_enumerated_panel',checks=checks,
                full_cube_potential=potential[-1],programs=len(bank))


def main():
    start=time.perf_counter_ns()
    results=[panel(n) for n in [3,4]]
    result=dict(status='COMPLETED',scope='DEVELOPMENT',contributor='Codex (GPT-6)',
                python=sys.version,elapsed_ns=time.perf_counter_ns()-start,
                hashes={p:hashlib.sha256((HERE/p).read_bytes()).hexdigest()
                        for p in ['face_potential_probe.py','parity_price_probe.py']},
                results=results,limitations='Tests the displayed Bellman potential only; '
                'a counterexample rejects that proof route, not the prefix construction.')
    (HERE/'face_potential_probe.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
