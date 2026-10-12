"""Adaptive Bayesian oracle and checked closure upper bounds; DEVELOPMENT."""
from fractions import Fraction as F
from functools import lru_cache
from acquire_flow import solve
from contrast_plan import coordinates


def conditional(poly,A,world):
    return sum(a*(-1 if (mask&world).bit_count()%2 else 1) for mask,a in poly.items() if mask&A==mask)


def adaptive(polys,prices):
    m=len(prices);actions={}
    @lru_cache(None)
    def V(A,world):
        stops=[conditional(p,A,world) for p in polys];value=max(stops);choice=('stop',stops.index(value))
        for i in range(m):
            bit=1<<i
            if A&bit:continue
            new=(V(A|bit,world)+V(A|bit,world|bit))/2-prices[i]
            if new>value:value=new;choice=('query',i)
        actions[f'{A}/{world}']=choice
        return value
    value=V(0,0);initial=max(p.get(0,F(0)) for p in polys)
    return dict(value=value,gain=value-initial,states=V.cache_info().currsize,actions=actions)


def closure_upper(polys,prices,baseline):
    masks=sorted(set(baseline)|set().union(*(p.keys() for p in polys))-{0})
    initial=max(p.get(0,F(0)) for p in polys);rows=[]
    for p in polys:
        terms=[(mask,abs(p.get(mask,F(0))-baseline.get(mask,F(0)))) for mask in masks]
        witness=solve(terms,prices);gap=initial-p.get(0,F(0))
        rows.append(dict(upper=witness['objective']-gap,witness=witness))
    return dict(upper=max(r['upper'] for r in rows),actions=rows)


def relaxation(polys,prices,baseline):
    masks=sorted((set(baseline)|set().union(*(p.keys() for p in polys)))-{0})
    codes,rank=coordinates(masks);unions={0}
    for mask in masks:unions|={u|mask for u in unions}
    initial=max(p.get(0,F(0)) for p in polys);total=F(0)
    for z in range(1<<rank):
        signs={mask:(-1 if (z&code).bit_count()%2 else 1) for mask,code in codes.items()};best=None
        for B in unions:
            price=sum(q for i,q in enumerate(prices) if B&(1<<i))
            for p in polys:
                value=p.get(0,F(0))-initial-price+sum((p.get(mask,F(0))-baseline.get(mask,F(0)))*signs[mask] for mask in masks if mask&B==mask)
                if best is None or value>best:best=value
        total+=best
    return dict(upper=total/(1<<rank),rank=rank,batches=len(unions))


def midpoint(polys):
    masks=set().union(*(p.keys() for p in polys))-{0}
    return {mask:(min(p.get(mask,F(0)) for p in polys)+max(p.get(mask,F(0)) for p in polys))/2 for mask in masks}
