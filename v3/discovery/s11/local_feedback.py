"""DEVELOPMENT exact local feedback identities, Codex (GPT-6).

Array accesses model paid deterministic receipts; this is not a deployed service.
"""
from fractions import Fraction as F
from itertools import product,permutations
from pathlib import Path
import argparse
import hashlib
import json
import random
import time


def stopping(receipts,mode,Q,n):
    if mode=='sum':return sum(receipts.values())>=Q
    if mode=='two_sided':
        ones=sum(receipts.values());zeros=len(receipts)-ones
        return ones>=Q or zeros>=n-Q+1
    assert mode=='dnf'
    terms=(((0,1),(1,1)),((2,0),(3,1)),((1,0),(n-1,0)))
    return any(all(i in receipts and receipts[i]==v for i,v in term) for term in terms)


def run(world,order,fees,fallback,stop):
    receipts={};bill=F(0)
    for i in order:
        if stop(receipts):break
        receipts[i]=world[i];bill+=fees[i]
    hit=stop(receipts)
    if not hit:bill+=fallback
    return bill,receipts,hit


def adjacent_feedback(world,order,fees,bill,receipts,stop):
    observed=dict(receipts);length=len(receipts);extra=[]
    if length<len(order):
        i=order[length];observed[i]=world[i];extra.append(i)
    out=[]
    for j in range(len(order)-1):
        if j>=length:
            out.append(bill);continue
        a,b=order[j:j+2]
        prefix={i:observed[i] for i in order[:j]}
        assert not stop(prefix)
        A=int(stop(prefix|{a:observed[a]}));B=int(stop(prefix|{b:observed[b]}))
        out.append(bill-fees[a]*B+fees[b]*A)
    return out,extra


def block_feedback(world,blocks,order,fees,bill,receipts,hit,stop):
    if not hit:return None,dict(receipts),[],None
    final=order[len(receipts)-1]
    g=next(i for i,block in enumerate(blocks) if final in block)
    observed=dict(receipts);extra=[]
    for i in blocks[g]:
        if i not in observed:observed[i]=world[i];extra.append(i)
    prior={i:observed[i] for block in blocks[:g] for i in block}
    prior_bill=sum((fees[i] for i in prior),F(0))
    loss={}
    for perm in permutations(blocks[g]):
        r=dict(prior);cost=F(0)
        for i in perm:
            if stop(r):break
            r[i]=observed[i];cost+=fees[i]
        assert stop(r)
        loss[perm]=prior_bill+cost
    return g,observed,extra,loss


def case(index):
    settings=((4,1,'sum',1,2),(6,2,'sum',3,3),(7,1,'sum',4,3),
              (6,1,'two_sided',3,2),(7,1,'two_sided',5,3),(6,1,'dnf',0,3))
    n,K,mode,Q,b=settings[index];rng=random.Random(4200+index)
    fees=tuple(F(rng.randrange(1,9),2) for _ in range(n));fallback=F(7)
    blocks=[tuple(range(i,min(n,i+b))) for i in range(0,n,b)]
    order=[]
    for block in blocks:
        part=list(block);rng.shuffle(part);order+=part
    stop=lambda receipt:stopping(receipt,mode,Q,n)
    all_orders=list(product(*(list(permutations(block)) for block in blocks)))
    counts={'worlds':0,'adjacent_checks':0,'block_checks':0,'base_receipts':0,
            'adjacent_extra_receipts':0,'block_extra_receipts':0,'full_truth_extra_receipts':0,
            'base_fee':F(0),'adjacent_extra_fee':F(0),'block_extra_fee':F(0),'full_truth_extra_fee':F(0),
            'max_adjacent_extra':0,'max_block_extra':0}
    start=time.perf_counter_ns()
    for world in product(range(K+1),repeat=n):
        bill,receipts,hit=run(world,order,fees,fallback,stop)
        adjacent,extra=adjacent_feedback(world,order,fees,bill,receipts,stop)
        assert len(extra)<=1
        for j,value in enumerate(adjacent):
            swap=list(order);swap[j],swap[j+1]=swap[j+1],swap[j]
            assert run(world,swap,fees,fallback,stop)[0]==value,(index,world,j,value)
            counts['adjacent_checks']+=1
        g,observed,block_extra,loss=block_feedback(world,blocks,order,fees,bill,receipts,hit,stop)
        assert len(block_extra)<=b-1
        for parts in all_orders:
            alternative=[i for part in parts for i in part]
            predicted=bill if g is None else loss[parts[g]]
            actual,other_receipts,other_hit=run(world,alternative,fees,fallback,stop)
            assert actual==predicted,(index,world,parts,predicted,actual)
            if hit:
                other_final=alternative[len(other_receipts)-1]
                assert other_hit and other_final in blocks[g]
            counts['block_checks']+=1
        counts['worlds']+=1;counts['base_receipts']+=len(receipts)
        counts['adjacent_extra_receipts']+=len(extra);counts['block_extra_receipts']+=len(block_extra)
        missing=[i for i in order if i not in receipts]
        counts['full_truth_extra_receipts']+=len(missing);counts['base_fee']+=bill
        for key,ids in (('adjacent_extra_fee',extra),('block_extra_fee',block_extra),('full_truth_extra_fee',missing)):
            counts[key]+=sum((fees[i] for i in ids),F(0))
        counts['max_adjacent_extra']=max(counts['max_adjacent_extra'],len(extra))
        counts['max_block_extra']=max(counts['max_block_extra'],len(block_extra))
    stop2=lambda r:sum(r.values())>=1
    left=run((1,0),(0,1),(F(1),F(2)),F(0),stop2)
    right=run((1,1),(0,1),(F(1),F(2)),F(0),stop2)
    assert left==right
    alt=[run(x,(1,0),(F(1),F(2)),F(0),stop2)[0] for x in ((1,0),(1,1))]
    assert alt==[F(3),F(2)]
    return {'case':index,'n':n,'K':K,'mode':mode,'Q':Q,'block_size':b,'blocks':blocks,'base_order':order,
            'fees':list(map(str,fees)),'fallback':str(fallback),'product_policy_count':len(all_orders),
            'counts':{k:str(v) if isinstance(v,F) else v for k,v in counts.items()},
            'one_extra_lower_example':{'base_bill':'1','alternative_bills':list(map(str,alt))},
            'elapsed_ns':time.perf_counter_ns()-start,
            'scope':'Exact enumerated counterfactual receipt reconstruction, with simulated acquisition fees; no probabilistic source assumed.'}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--case',type=int,required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();assert not args.out.exists()
    result=case(args.case);result['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    with args.out.open('x',encoding='utf-8',newline='\n') as out:out.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('case','n','mode','product_policy_count','counts','elapsed_ns')}))


if __name__=='__main__':main()
