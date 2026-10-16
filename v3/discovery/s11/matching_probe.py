"""DEVELOPMENT sparse decomposition and weighted-tree screen, Codex (GPT-6)."""
import argparse
from itertools import product
import hashlib
import json
import math
from pathlib import Path
import random
import time

from banded_probe import execute,acquire
from local_feedback import stopping
from matching_core import MatchingTree,matching_orders,sparse_delta,logadd


def lse(values):
    total=-math.inf
    for value in values:total=logadd(total,value)
    return total


def case(index):
    start=time.perf_counter_ns();n=(5,7,8,9)[index]
    mode=('sum','two_sided','dnf','sum')[index];Q=(1,4,0,3)[index]
    stop=lambda r:stopping(r,mode,Q,n);fees=tuple(1+(j*3+index)%7 for j in range(n))
    family=matching_orders(n);tree=MatchingTree(n);rng=random.Random(18200+index)
    count=dict(decompositions=0,loss_entries=0,maximum_nonzero=0,partition_checks=0,conditional_checks=0)
    for world in product((0,1),repeat=n):
        for order,matching in family[::max(1,len(family)//3)]:
            actual,receipts,hit=execute(world,order,fees,stop)
            observed,extra=acquire(world,receipts,hit,n,1)
            deltas,reference,refhit=sparse_delta(observed,n,fees,stop)
            if not refhit:reference+=7
            assert len(deltas)<=2
            for candidate,edges in family:
                predicted=reference+sum(deltas.get(j,0) for j in edges)
                assert execute(world,candidate,fees,stop)[0]==predicted
                count['decompositions']+=1
            count['loss_entries']+=len(deltas)
            count['maximum_nonzero']=max(count['maximum_nonzero'],len(deltas))
    for _ in range(20):
        j=rng.randrange(n-1);tree.update(j,rng.uniform(-20,20))
        weights=[sum(tree.logweights[j] for j in edges) for _,edges in family]
        assert abs(tree.suffix(0)-lse(weights))<1e-9
        count['partition_checks']+=1
        for j in range(n-1):
            suffix=matching_orders(n-j)
            vals=[sum(tree.logweights[j+k] for k in edges) for _,edges in suffix]
            numerator=lse(v for v,(_,edges) in zip(vals,suffix) if 0 in edges)
            exact=math.exp(numerator-lse(vals))
            assert abs(tree.swap_probability(j)-exact)<1e-9
            count['conditional_checks']+=1
        for _ in range(5):
            sampled=tuple(tree.sample_lazy(rng))
            assert sampled in {order for order,edges in family}
    large=[]
    for size in (64,256,1024,4096):
        other=MatchingTree(size);setup=dict(other.counts)
        for j in (size//2,size//2+1):other.update(j,.1)
        update_products=other.counts['matrix_products']-setup['matrix_products']
        large.append({'n':size,'setup_products':setup['matrix_products'],'two_update_products':update_products,
                      'tree_matrix_slots':len(other.tree),'direct_dp_recurrence_steps_per_rebuild':size-1})
    return {'case':index,'n':n,'mode':mode,'Q':Q,'policies':len(family),'counts':count,
            'tree_counts':tree.counts,'scaling_probe':large,'elapsed_ns':time.perf_counter_ns()-start,
            'scope':'Finite exact cost identities and numerical partition/sampling probabilities. Operation categories are not interchangeable time or monetary prices.'}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--case',type=int,required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();assert not args.out.exists()
    result=case(args.case)
    result['source_hashes']={p:hashlib.sha256(Path(__file__).with_name(p).read_bytes()).hexdigest() for p in ('matching_core.py','matching_probe.py')}
    with args.out.open('x',encoding='utf-8',newline='\n') as out:out.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('case','n','policies','counts','scaling_probe','elapsed_ns')}))


if __name__=='__main__':main()
