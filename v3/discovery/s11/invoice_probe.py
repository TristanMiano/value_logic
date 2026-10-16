"""DEVELOPMENT invoice degree and logical support ranks, Codex (GPT-6)."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
from collections import Counter
import argparse
import hashlib
import json
import math
import random


def walsh(values):
    out=list(values);step=1
    while step<len(out):
        for base in range(0,len(out),2*step):
            for j in range(step):
                a,b=out[base+j],out[base+j+step];out[base+j]=a+b;out[base+j+step]=a-b
        step*=2
    return out


def tree(available,cap,rng):
    if not cap or not available or rng.randrange(5)==0:return None
    j=rng.choice(available);rest=[i for i in available if i!=j]
    return (j,tree(rest,cap-1,rng),tree(rest,cap-1,rng))


def invoice(policy,x,fees):
    total=0
    while policy is not None:
        j,a,b=policy;total+=fees[j];policy=b if x&(1<<j) else a
    return total


def rank(rows):
    pivots={}
    for raw in rows:
        row=list(map(F,raw))
        for pivot,basis in sorted(pivots.items()):
            if row[pivot]:
                scale=row[pivot];row=[x-scale*y for x,y in zip(row,basis)]
        nonzero=next((i for i,v in enumerate(row) if v),None)
        if nonzero is not None:
            scale=row[nonzero];pivots[nonzero]=[x/scale for x in row]
    return len(pivots)


def span(generators):
    values={0}
    for g in generators:values|={x^g for x in values}
    return sorted(values)


def code_ranks(n,code,offset=0):
    words=list(range(2**n));dual=[v for v in words if all((v&x).bit_count()%2==0 for x in code)]
    leaders={}
    for v in words:
        key=min(v^u for u in dual);leaders[key]=min(leaders.get(key,n+1),v.bit_count())
    radius=max(leaders.values());records=[]
    for degree in range(n):
        chars=[s for s in words if s.bit_count()<=degree]
        rows=[[(-1)**((s&(x^offset)).bit_count()%2) for x in code] for s in chars]
        actual=rank(rows);expected=sum(d<=degree for d in leaders.values())
        assert actual==expected
        records.append({'cap':degree+1,'rank':actual,'identified':actual==len(code)})
    return {'n':n,'world_count':len(code),'offset':offset,'dual_size':len(dual),'dual_covering_radius':radius,
            'cap_ranks':records,'first_identifying_cap':next((v['cap'] for v in records if v['identified']),None)}


def case(index):
    n=(2,3,4,6,7)[index];rng=random.Random(28000+index);fees=[1+(3*j%7) for j in range(n)]
    counts={'random_trees':0,'invoice_event_degree_checks':0,'parity_distribution_checks':0,'basis_purchase_checks':0}
    records=[]
    if index<4:
        for H in range(1,n+1):
            for trial in range(16):
                policy=tree(list(range(n)),H,rng);values=[invoice(policy,x,fees) for x in range(2**n)]
                coeff=walsh(values);assert all(v==0 for s,v in enumerate(coeff) if s.bit_count()>=H)
                for value in set(values):
                    event_coeff=walsh([int(v==value) for v in values])
                    assert all(v==0 for s,v in enumerate(event_coeff) if s.bit_count()>=H)
                    counts['invoice_event_degree_checks']+=1
                even=Counter(values[x] for x in range(2**n) if x.bit_count()%2==0)
                odd=Counter(values[x] for x in range(2**n) if x.bit_count()%2==1)
                assert even==odd;counts['parity_distribution_checks']+=1;counts['random_trees']+=1
                records.append({'cap':H,'tree':policy,'invoices':values})
            for S in range(1,2**n):
                if S.bit_count()>=H:continue
                j=next(j for j in range(n) if not S&(1<<j));base=sum(fees[i] for i in range(n) if S&(1<<i))
                values=[base+fees[j]*int((S&x).bit_count()%2==0) for x in range(2**n)]
                coeff=walsh(values)
                assert coeff[S]==fees[j]*2**(n-1)
                assert all(v==0 for s,v in enumerate(coeff) if s not in (0,S))
                counts['basis_purchase_checks']+=1
        full=code_ranks(n,list(range(2**n)));assert full['first_identifying_cap'] is None
        parity=code_ranks(n,[x for x in range(2**n) if x.bit_count()%2==0],1)
        assert parity['first_identifying_cap']==n//2+1
        repetition=code_ranks(n,[0,2**n-1]);assert repetition['first_identifying_cap']==2
        proper=[x for x in range(2**n) if x!=0]
        rows=[[(-1)**((s&x).bit_count()%2) for x in proper] for s in range(2**n-1)]
        assert rank(rows)==len(proper)
        code_results={'full':full,'parity_affine':parity,'repetition':repetition,'proper_support_rank':len(proper)}
    else:
        generators=[sum(((column>>bit)&1)<<j for j,column in enumerate(range(1,8))) for bit in range(3)]
        simplex=code_ranks(7,span(generators));assert simplex['first_identifying_cap']==2
        code_results={'all_nonzero_latent_parities':simplex}
    terminal={'predictable_base':sum(fees),'even_invoice_with_terminal_fee':sum(fees)+1,'odd_invoice_with_terminal_fee':sum(fees)}
    return {'contributor':'Codex (GPT-6)','status':'DEVELOPMENT','case':index,'n':n,'fees':fees,'seed':28000+index,
      'counts':counts,'code_results':code_results,'random_tree_records':records,'terminal_fee_boundary':terminal,
      'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'scope':'Exact finite invoice-degree checks and restricted-character ranks. No new sampled source or cheap full-law-learning claim.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',type=int,required=True);p.add_argument('--out',required=True)
    a=p.parse_args();result=case(a.case)
    with open(a.out,'x',encoding='utf-8',newline='\n') as out:out.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('case','n','counts','code_results')}))
