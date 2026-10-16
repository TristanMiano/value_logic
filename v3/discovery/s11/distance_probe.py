"""DEVELOPMENT cheap distance-feedback screen, Codex (GPT-6)."""
from itertools import permutations,product
from pathlib import Path
import argparse
import hashlib
import json
import time

from banded_probe import execute,replay


def inversion(order):
    return sum(a>b for i,a in enumerate(order) for b in order[i+1:])


def footrule(order):return sum(abs(t-i) for t,i in enumerate(order))


def case(index):
    n,k=((5,1),(6,2),(7,3))[index];start=time.perf_counter_ns()
    full=list(permutations(range(n)));counts={};lower={}
    for name,metric,budget in (('kendall',inversion,k),('footrule',footrule,2*k)):
        family=[p for p in full if metric(p)<=budget]
        for i in range(n):
            for j in range(i+1,n):
                minimum=min(metric(p) for p in full if p.index(j)<p.index(i))
                assert minimum==(j-i)*(1 if name=='kendall' else 2)
        checks=0;maxextra=0
        bases=tuple(dict.fromkeys((tuple(range(n)),family[len(family)//3],family[-1])))
        fees=tuple(1+j%4 for j in range(n));stop=lambda r:sum(r.values())>=1
        for world in product((0,1),repeat=n):
            for base in bases:
                bill,receipts,hit=execute(world,base,fees,stop)
                end=min(n,max(receipts)+k+1) if hit else n
                extra=[i for i in range(end) if i not in receipts]
                assert len(extra)<=(k if base==tuple(range(n)) else 2*k)
                observed=receipts|{i:world[i] for i in extra}
                for p in family:
                    assert replay(observed,p,fees,stop)==execute(world,p,fees,stop)[0]
                    checks+=1
                maxextra=max(maxextra,len(extra))
        counts[name]={'policies':len(family),'replays':checks,'max_extra':maxextra,'pair_minimum_checks':n*(n-1)//2}
        # A separate untruncated witness attains the 2k lower bound.
        L=2;i=L+k-1;nn=i+k+1;world=[0]*nn;world[i]=1
        base=list(range(nn));base.pop(i);base.insert(L-1,i)
        assert metric(base)<=budget
        fees=tuple(1 for _ in range(nn));actual=execute(world,base,fees,stop)
        missing=[j for j in range(i+k+1) if j not in actual[1]]
        assert len(missing)==2*k
        for j in missing:
            order=list(range(nn))
            if j>i:order.pop(j);order.insert(i,j)
            assert metric(order)<=budget and order.index(j)<order.index(i)
            changed=list(world);changed[j]=1
            assert execute(changed,base,fees,stop)==actual
            assert execute(changed,order,fees,stop)[0]<execute(world,order,fees,stop)[0]
        lower[name]={'n':nn,'necessary_extra':len(missing),'executed':base}
    return {'case':index,'n':n,'k':k,'counts':counts,'lower':lower,'elapsed_ns':time.perf_counter_ns()-start,
            'scope':'All small permutations and binary worlds, three selected executing orders; explicit larger lower construction.'}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--case',type=int,required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();assert not args.out.exists()
    result=case(args.case);result['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    with args.out.open('x',encoding='utf-8',newline='\n') as out:out.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':main()
