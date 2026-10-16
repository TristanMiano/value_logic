"""DEVELOPMENT bounded-displacement feedback screen. Codex (GPT-6)."""
import argparse
from functools import lru_cache
from itertools import permutations, product
from pathlib import Path
import hashlib
import json
import time

from local_feedback import stopping


def automaton(n,d):
    layers=[{0}];edges={}
    for t in range(n):
        following=set()
        required=(1<<max(0,t+1-d))-1
        for mask in layers[-1]:
            choices=[]
            for j in range(max(0,t-d),min(n,t+d+1)):
                if mask>>j&1:continue
                after=mask|(1<<j)
                if after&required!=required:continue
                choices.append((j,after));following.add(after)
            edges[mask]=choices
        layers.append(following)
    @lru_cache(None)
    def paths(mask):
        if mask==(1<<n)-1:return ((),)
        return tuple((j,)+suffix for j,after in edges[mask] for suffix in paths(after))
    return layers,edges,paths(0)


def execute(values,order,fees,stop,fallback=7):
    receipts={};cost=0
    for j in order:
        if stop(receipts):break
        receipts[j]=values[j];cost+=fees[j]
    hit=stop(receipts)
    if not hit:cost+=fallback
    return cost,receipts,hit


def acquire(values,receipts,hit,n,d):
    if not hit:return dict(receipts),[]
    end=min(n,max(receipts)+2*d)
    extra=[j for j in range(end) if j not in receipts]
    return receipts|{j:values[j] for j in extra},extra


def replay(observed,order,fees,stop,fallback=7):
    receipts={};cost=0
    for j in order:
        if stop(receipts):break
        assert j in observed,('missing receipt',j,order,receipts,observed)
        receipts[j]=observed[j];cost+=fees[j]
    if not stop(receipts):cost+=fallback
    return cost


def necessity(d):
    L=2;i=L+d-1;n=i+2*d
    world=[0]*n;world[i]=1
    executed=list(range(n));executed.pop(i);executed.insert(L-1,i)
    fees=tuple(1+j%3 for j in range(n));stop=lambda r:sum(r.values())>=1
    actual=execute(world,executed,fees,stop)
    observed,missing=acquire(world,actual[1],True,n,d)
    assert len(missing)==3*d-1
    witnesses=[]
    for j in missing:
        order=list(range(n))
        if j>i:
            if j-i<=d:order[i],order[j]=order[j],order[i]
            else:order[i:i+2*d]=order[i+d:i+2*d]+order[i:i+d]
        assert all(abs(position-item)<=d for position,item in enumerate(order))
        assert order.index(j)<order.index(i)
        altered=list(world);altered[j]=1
        assert execute(altered,executed,fees,stop)==actual
        before=execute(world,order,fees,stop)[0]
        after=execute(altered,order,fees,stop)[0]
        assert after<before
        witnesses.append({'unobserved':j,'order':order,'bills':[before,after]})
    return {'d':d,'n':n,'executed_order':executed,'observed':actual[1],
            'necessary_missing_count':len(missing),'witnesses':witnesses}


def case(index):
    settings=((5,1,'sum',1),(6,2,'sum',2),(7,2,'two_sided',4),(6,2,'dnf',0),(7,3,'sum',3))
    n,d,mode,Q=settings[index];start=time.perf_counter_ns()
    layers,edges,orders=automaton(n,d)
    brute=tuple(p for p in permutations(range(n)) if all(abs(t-i)<=d for t,i in enumerate(p)))
    assert set(orders)==set(brute)
    fees=tuple((j*5+index)%9 for j in range(n));stop=lambda r:stopping(r,mode,Q,n)
    identity=tuple(range(n));bases=tuple(dict.fromkeys((identity,orders[0],orders[len(orders)//3],orders[-1])))
    counters=dict(worlds=0,replays=0,edge_checks=0,range_checks=0,base_receipts=0,
                  local_extra=0,full_extra=0,local_extra_fee=0,full_extra_fee=0,
                  max_reference_extra=0,max_general_extra=0)
    for world in product((0,1),repeat=n):
        bills={p:execute(world,p,fees,stop)[0] for p in orders}
        ref=bills[identity]
        assert all(abs(value-ref)<=d*max(fees) for value in bills.values())
        assert max(bills.values())-min(bills.values())<=2*d*max(fees)
        counters['range_checks']+=len(orders)
        for base in bases:
            bill,receipts,hit=execute(world,base,fees,stop)
            known,extra=acquire(world,receipts,hit,n,d)
            bound=2*d-1 if base==identity else 3*d-1
            assert len(extra)<=bound
            key='max_reference_extra' if base==identity else 'max_general_extra'
            counters[key]=max(counters[key],len(extra))
            for order in orders:
                assert replay(known,order,fees,stop)==bills[order]
                counters['replays']+=1
            for mask,choices in edges.items():
                # A known certificate makes unknown acquired values irrelevant.
                known_prefix={j:known[j] for j in known if mask>>j&1}
                if stop(known_prefix):predicted_stop=True
                else:
                    assert all(j in known for j in range(n) if mask>>j&1)
                    predicted_stop=stop(known_prefix)
                actual_stop=stop({j:world[j] for j in range(n) if mask>>j&1})
                assert predicted_stop==actual_stop
                for j,after in choices:
                    assert (0 if predicted_stop else fees[j])==(0 if actual_stop else fees[j])
                    counters['edge_checks']+=1
            missing=[j for j in range(n) if j not in receipts]
            counters['base_receipts']+=len(receipts)
            counters['local_extra']+=len(extra);counters['full_extra']+=len(missing)
            counters['local_extra_fee']+=sum(fees[j] for j in extra)
            counters['full_extra_fee']+=sum(fees[j] for j in missing)
        counters['worlds']+=1
    return {'case':index,'n':n,'d':d,'mode':mode,'Q':Q,'fees':fees,
            'policy_count':len(orders),'state_count':sum(map(len,layers)),
            'edge_count':sum(map(len,edges.values())),'executed_orders':bases,
            'counts':counters,'lower_constructions':[necessity(k) for k in (1,2,3)],
            'elapsed_ns':time.perf_counter_ns()-start,
            'scope':'Exhaustive binary worlds and candidate policies, four or fewer selected executed orders; numerical fees are simulated.'}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--case',type=int,required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();assert not args.out.exists()
    result=case(args.case);result['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    with args.out.open('x',encoding='utf-8',newline='\n') as out:out.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('case','policy_count','state_count','edge_count','counts','elapsed_ns')}))


if __name__=='__main__':main()
