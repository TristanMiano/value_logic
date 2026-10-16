"""DEVELOPMENT evidence-enabled safe output revisions on chains, Codex (GPT-6)."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import random
from logical_chain import SIGNS,ALL,admissible
from query_flip import matches


def compile_menu(relations,h):
    m=len(relations)+1;r=len(h)
    allowed=[{h[i]} if i<r and h[i] else set(SIGNS) for i in range(m)]
    left=[set() for _ in range(m)];right=[set() for _ in range(m)];left[0]=allowed[0]
    work={'pair_checks':0,'menu_checks':0}
    for i in range(1,m):
        for x in allowed[i]:
            for y in left[i-1]:
                work['pair_checks']+=1
                if (y,x) in relations[i-1]:left[i].add(x)
    right[-1]=allowed[-1]
    for i in range(m-2,-1,-1):
        for x in allowed[i]:
            for y in right[i+1]:
                work['pair_checks']+=1
                if (x,y) in relations[i]:right[i].add(x)
    if not left[-1]:return None,[],work
    projections=[];menus=[]
    for i,relation in enumerate(relations):
        projection={(x,y) for x,y in relation if x in left[i] and y in right[i+1]}
        projections.append(projection);menu=set()
        for a,b in product((0,1),repeat=2):
            valid=True
            for x,y in projection:
                work['menu_checks']+=1
                if ((-1)**a*x,(-1)**b*y) not in relation:valid=False;break
            if valid:menu.add((a,b))
        menus.append(menu)
    return menus,projections,work


def valid_mask(mask,menu,m):
    return all(((mask>>i)&1,(mask>>(i+1))&1) in allowed for i,allowed in enumerate(menu))


def mask_optimum(x,w,f,k,menu):
    values={(None,0):(F(0),0)};extensions=0
    for i,truth in enumerate(x):
        nxt={}
        for (previous,count),(cost,mask) in values.items():
            for b in (0,1):
                if count+b>k or (i and (previous,b) not in menu[i-1]):continue
                extensions+=1;candidate=cost+w[i]*truth*(1-2*b)+f[i]*b
                key=b,count+b
                if key not in nxt or candidate<nxt[key][0]:nxt[key]=(candidate,mask|(b<<i))
        values=nxt
    assert values,'Identity mask must be permitted'
    value,mask=min(values.values())
    return value,mask,extensions


def comparator(x,w,f,q,H,menus):
    best=F(0);choice=('stop0',);work=0
    for h,menu in menus.items():
        used=sum(v!=0 for v in h)
        if menu is None or used>H or not matches(x[:len(q)],h):continue
        value,mask,extensions=mask_optimum(x,w,f,H-used,menu);work+=extensions
        value+=sum((q[j] for j,v in enumerate(h) if v),F(0))
        if value<best:best=value;choice=('stop1',h,mask)
    return best,choice,work


def unrestricted(x,w,f,q,H,relations,menus):
    m=len(x);r=len(q);work={'states':0,'query_options':0,'flip_options':0}
    @lru_cache(None)
    def solve(h,mask,budget):
        work['states']+=1;best=F(0)
        if valid_mask(mask,menus[h],m):
            best=min(best,sum((w[i]*x[i]*(-1 if mask&(1<<i) else 1) for i in range(m)),F(0)))
        if budget:
            for j in range(r):
                if h[j]:continue
                child=tuple(x[j] if i==j else h[i] for i in range(r))
                work['query_options']+=1;best=min(best,q[j]+solve(child,mask,budget-1))
            for i in range(m):
                work['flip_options']+=1;best=min(best,f[i]+solve(h,mask^(1<<i),budget-1))
        return best
    return solve((0,)*r,0,H),work


def case(index):
    settings=[(2,1,2),(4,1,2),(5,2,3),(6,2,4),(5,0,7),(41,3,5)]
    m,r,H=settings[index]
    relation_menu=[ALL,ALL-{(1,-1)},ALL-{(1,1)},{(-1,-1),(1,1)},{(-1,1),(1,-1)}]
    relations=[set(relation_menu[(i+index)%5]) for i in range(m-1)]
    if index==0:relations=[ALL-{(1,-1)}]
    rng=random.Random(24000+index)
    w=tuple(F(rng.randrange(-3,4)) for _ in range(m))
    f=tuple(F(rng.randrange(4),4) for _ in range(m));q=tuple(F(rng.randrange(1,4),4) for _ in range(r))
    if index==0:w=(F(1),F(1));f=(F(0),F(0));q=(F(1,4),)
    menus={};counts={'histories':0,'unreachable_histories':0,'pair_checks':0,'menu_checks':0,
                    'mask_universal_checks':0,'point_source_planners':0,'unrestricted_states':0,'mask_dp_extensions':0}
    worlds=[x for x in product(SIGNS,repeat=m) if admissible(x,relations)] if m<10 else None
    for h in product((-1,0,1),repeat=r):
        menu,projection,work=compile_menu(relations,h);menus[h]=menu;counts['histories']+=1
        for k,v in work.items():counts[k]+=v
        if menu is None:counts['unreachable_histories']+=1
        if worlds is not None:
            compatible=[x for x in worlds if matches(x[:r],h)]
            assert bool(compatible)==(menu is not None)
            if compatible:
                for i in range(m-1):assert projection[i]=={(x[i],x[i+1]) for x in compatible}
                for mask in range(2**m):
                    checked=all(admissible(tuple(v*(-1 if mask&(1<<i) else 1) for i,v in enumerate(x)),relations) for x in compatible)
                    assert valid_mask(mask,menu,m)==checked
                    counts['mask_universal_checks']+=1
    if worlds is None:
        # One explicitly generated compatible point, not an exhaustive 41-bit scan.
        x=[-1]
        for relation in relations:x.append(next(v for v in SIGNS if (x[-1],v) in relation))
        worlds=[tuple(x)]
    results=[]
    for x in worlds:
        answer,choice,work=comparator(x,w,f,q,H,menus);counts['mask_dp_extensions']+=work
        counts['point_source_planners']+=1
        if m<10:
            control,cnt=unrestricted(x,w,f,q,H,relations,menus)
            assert answer==control,(x,answer,control);counts['unrestricted_states']+=cnt['states']
        results.append({'truth':x,'value':str(answer),'choice':choice})
    example=None
    if index==0:
        assert [F(v['value']) for v in results]==[F(-2),F(-7,4),F(0)]
        policy_cost={(-1,-1):F(-7,8),(-1,1):F(-5,8),(1,1):F(1,4)}
        regrets=[policy_cost[tuple(v['truth'])]-F(v['value']) for v in results]
        assert regrets==[F(9,8),F(9,8),F(1,4)]
        example={'queried_controller_regrets':list(map(str,regrets)),
                 'no_query_minimax_regret':'7/4','queried_feasible_upper':'9/8',
                 'initial_masks':[mask for mask in range(4) if valid_mask(mask,menus[(0,)],2)],
                 'after_negative_query_masks':[mask for mask in range(4) if valid_mask(mask,menus[(-1,)],2)],
                 'after_positive_query_masks':[mask for mask in range(4) if valid_mask(mask,menus[(1,)],2)]}
    return {'contributor':'Codex (GPT-6)','status':'DEVELOPMENT','case':index,'m':m,'r':r,'H':H,
       'weights':list(map(str,w)),'flip_fee':list(map(str,f)),'query_fee':list(map(str,q)),
       'relations':[sorted(s) for s in relations],'menus':[{ 'history':h,'relations':None if menu is None else [sorted(s) for s in menu]} for h,menu in menus.items()],
       'counts':counts,'point_source_comparators':results,'worked_example':example,
       'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       'dependency_hashes':{name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() for name in ('logical_chain.py','query_flip.py')},
       'scope':'Menu universal-feasibility identities and comparator query-normal form, finite checks. No optimized full controller yet.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',type=int,required=True);p.add_argument('--out',required=True)
    a=p.parse_args();result=case(a.case)
    with open(a.out,'x',encoding='utf-8',newline='\n') as out:out.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('case','m','r','H','counts','worked_example')}))
