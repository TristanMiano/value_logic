"""DEVELOPMENT structural screen; no edits to earlier executed sources."""
from itertools import combinations,product
from pathlib import Path
import hashlib
import json
import sys
import time
from parity_price_probe import all_invoice_functions,partitions

HERE=Path(__file__).resolve().parent


def binary_sources(n):
    full=(1<<(1<<n))-1
    states={full}
    for size in [1,2]:
        for scope in combinations(range(n),size):
            for values in product([0,1],repeat=size):
                bad=sum(1<<x for x in range(1<<n)
                        if all((x>>i&1)==v for i,v in zip(scope,values)))
                clause=full^bad
                states.update([w&clause for w in states])
    return states


def faces(n):
    answer=[]
    for spec in product([-1,0,1],repeat=n):
        dim=spec.count(-1)
        if dim:
            mask=sum(1<<x for x in range(1<<n)
                     if all(v==-1 or (x>>i&1)==v for i,v in enumerate(spec)))
            answer.append((mask,3 if dim==1 else -2*(-3)**(dim-2)))
    return answer


def panel(n):
    started=time.perf_counter_ns()
    states=binary_sources(n)
    assert len(states)<=300000, 'Prospective source-count limit'
    cube_faces=faces(n)
    potential={w:sum(a for s,a in cube_faces if w&s==s) for w in states}
    bank=partitions(all_invoice_functions((1,)*n,3))
    # The structural characterization requires every observation cell and
    # every source intersection to be in the compiled binary relation class.
    assert all(s in states for p in bank for _,s in p)
    checks=0
    for w in sorted(states,key=lambda x:(x.bit_count(),x)):
        if not w:
            continue
        for program in bank:
            groups=[(c,s&w) for c,s in program if s&w]
            if len(groups)<2:
                continue
            rhs=sum(c*s.bit_count()+potential[s] for c,s in groups)
            checks+=1
            if potential[w]>rhs:
                return dict(n=n,status='reachable_counterexample',states=len(states),
                            checks=checks,source_mask=w,lhs=potential[w],rhs=rhs,
                            source_worlds=[x for x in range(1<<n) if w>>x&1],
                            groups=[dict(cost=c,mask=s,potential=potential[s]) for c,s in groups],
                            elapsed_ns=time.perf_counter_ns()-started)
            if checks%100000==0 and time.perf_counter_ns()-started>55000000000:
                return dict(n=n,status='time_cap',states=len(states),checks=checks,
                            elapsed_ns=time.perf_counter_ns()-started)
    return dict(n=n,status='no_counterexample_in_enumerated_panel',states=len(states),
                checks=checks,programs=len(bank),full_cube_potential=potential[max(states)],
                elapsed_ns=time.perf_counter_ns()-started)


def main():
    started=time.perf_counter_ns()
    rows=[]
    for n in [3,4,5]:
        rows.append(panel(n))
        print(json.dumps(rows[-1]),flush=True)
        if rows[-1]['status']=='reachable_counterexample':
            break
    result=dict(status='COMPLETED',scope='DEVELOPMENT',contributor='Codex (GPT-6)',
                python=sys.version,elapsed_ns=time.perf_counter_ns()-started,
                hashes={p:hashlib.sha256((HERE/p).read_bytes()).hexdigest()
                        for p in ['reachable_probe.py','parity_price_probe.py']},
                results=rows,limits=dict(max_sources=300000,seconds_per_panel=55),
                limitations='Finite screening of reachable source characterization and a '
                'candidate lower bound. Counterexamples reject the proposed potential; '
                'they do not refute the prefix upper bound or prove a better full-cube policy.')
    (HERE/'reachable_probe.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())


if __name__=='__main__':
    main()
