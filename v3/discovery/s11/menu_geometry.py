"""DEVELOPMENT cardinality/parity repair classifier checks, Codex (GPT-6)."""
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import random


def matches(x,h):
    return all(v<0 or ((x>>j)&1)==v for j,v in enumerate(h))


def predicted_cardinality(mask,m,k,target,h):
    observed=[j for j,v in enumerate(h) if v>=0]
    unknown=[j for j in range(m) if j not in observed]
    t=k-sum(h[j] for j in observed);u=len(unknown)
    if not 0<=t<=u:return None
    V=[j for j in unknown if mask&(1<<j)]
    known=sum((1-2*h[j]) for j in observed if mask&(1<<j))
    if 0<t<u:
        if len(V) not in (0,u):return False
        change=known+(u-2*t if len(V)==u else 0)
    else:change=known+len(V)*(1 if t==0 else -1)
    return change==target-k


def case(index):
    m=(2,4,5,6)[index];r=min(2,m)
    histories=list(product((-1,0,1),repeat=r));worlds=list(range(2**m))
    counts={'cardinality_histories':0,'cardinality_mask_checks':0,'parity_mask_checks':0,'unreachable_histories':0}
    for k in range(m+1):
        source=[x for x in worlds if x.bit_count()==k]
        for h in histories:
            compatible=[x for x in source if matches(x,h)]
            if not compatible:counts['unreachable_histories']+=1;continue
            counts['cardinality_histories']+=1
            for target in range(m+1):
                for mask in worlds:
                    actual=all((x^mask).bit_count()==target for x in compatible)
                    assert predicted_cardinality(mask,m,k,target,h)==actual,(m,k,target,h,mask)
                    counts['cardinality_mask_checks']+=1
    rng=random.Random(27000+index);parity_cases=[]
    for panel in range(5):
        rows=[rng.randrange(1,2**m) for _ in range(min(m,3))]
        reference=rng.randrange(2**m);target_world=rng.randrange(2**m)
        syndrome=lambda x:tuple((x&a).bit_count()%2 for a in rows)
        c=syndrome(reference);d=syndrome(target_world)
        source=[x for x in worlds if syndrome(x)==c]
        for h in histories:
            compatible=[x for x in source if matches(x,h)]
            if not compatible:continue
            for mask in worlds:
                expected=syndrome(mask)==tuple(a^b for a,b in zip(c,d))
                actual=all(syndrome(x^mask)==d for x in compatible)
                assert expected==actual;counts['parity_mask_checks']+=1
        parity_cases.append({'rows':rows,'source_syndrome':c,'target_syndrome':d,'worlds':source})
    return {'contributor':'Codex (GPT-6)','status':'DEVELOPMENT','case':index,'m':m,'r':r,'counts':counts,
      'parity_panels':parity_cases,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'scope':'Exact finite classification of uniformly valid XOR masks; no optimizer or economic claim.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',type=int,required=True);p.add_argument('--out',required=True)
    a=p.parse_args();result=case(a.case)
    with open(a.out,'x',encoding='utf-8',newline='\n') as out:out.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('case','m','r','counts')}))
