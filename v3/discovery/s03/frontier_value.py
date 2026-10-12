"""Finite frontier composition with priced ordinary initializers; DEVELOPMENT."""
from fractions import Fraction as F
from functools import lru_cache
from adaptive_value import conditional,closure_upper,midpoint
from contrast_plan import coordinates


def substitute(poly,A,world):
    p={}
    for mask,a in poly.items():
        key=mask&~A;value=a*(-1 if (mask&A&world).bit_count()%2 else 1)
        p[key]=p.get(key,F(0))+value
    return {mask:a for mask,a in p.items() if a}


def perfect_information(polys):
    masks=sorted(set().union(*(p.keys() for p in polys))-{0});codes,rank=coordinates(masks);total=F(0)
    for z in range(1<<rank):
        total+=max(p.get(0,F(0))+sum(p.get(mask,F(0))*(-1 if (code&z).bit_count()%2 else 1) for mask,code in codes.items()) for p in polys)
    return total/(1<<rank)


def frontier(polys,prices,depth,kind):
    m=len(prices);proof={};init_count=0
    @lru_cache(None)
    def initial(A,world):
        nonlocal init_count
        init_count+=1;p=[substitute(row,A,world) for row in polys];stop=max(row.get(0,F(0)) for row in p)
        if A==(1<<m)-1:return stop,stop
        if kind=='coefficient':upper=max(row.get(0,F(0))+sum(abs(a) for mask,a in row.items() if mask) for row in p)
        elif kind=='perfect_info':upper=max(stop,perfect_information(p)-min(q for i,q in enumerate(prices) if not A&(1<<i)))
        else:
            assert kind=='closure'
            incumbent=max(range(len(p)),key=lambda a:p[a].get(0,F(0)))
            baselines=[midpoint(p),{mask:a for mask,a in p[incumbent].items() if mask}]
            upper=stop+min(closure_upper(p,prices,b)['upper'] for b in baselines)
        assert upper>=stop
        return stop,upper
    @lru_cache(None)
    def visit(A,world,h):
        stop,cap=initial(A,world);L,U=stop,cap;policy=('stop',None)
        if h and A!=(1<<m)-1:
            U=stop
            for j in range(m):
                bit=1<<j
                if A&bit:continue
                lp,up=visit(A|bit,world,h-1);ln,un=visit(A|bit,world|bit,h-1)
                lo=(lp+ln)/2-prices[j];hi=(up+un)/2-prices[j]
                if lo>L:L=lo;policy=('query',j)
                U=max(U,hi)
            U=min(U,cap)
        assert L<=U
        proof[f'{A}/{world}/{h}']=dict(lower=L,upper=U,policy=policy)
        return L,U
    L,U=visit(0,0,depth)
    return dict(lower=L,upper=U,states=visit.cache_info().currsize,initializer_states=init_count,proof=proof)
