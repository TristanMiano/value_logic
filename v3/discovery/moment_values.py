"""Depth-indexed value moments for finite Boolean observations.

Codex (GPT-6), 2026-10-12. DEVELOPMENT. Supplied moments must be realizable;
coordinate bounds alone do not authenticate their common probability source.
"""
from fractions import Fraction as F
from functools import lru_cache


def masks(m,degree):return tuple(k for k in range(1<<m) if k.bit_count()<=degree)


def acquire_from_table(counts,m,degree):
    assert len(counts)==1<<m and all(w>=0 for w in counts) and sum(counts)>0
    total=sum(counts)
    return {mask:F(sum(w*(1 if (x&mask).bit_count()%2==0 else -1) for x,w in enumerate(counts)),total) for mask in masks(m,degree)}


def plan(moments,m,terminal,prices,horizon,available=None):
    assert type(horizon) is int and horizon>=0 and len(prices)==m
    assert all(q>=0 for q in prices) and all(len(row)==m+1 for row in terminal)
    required={h:masks(m,min(m,h+1)) for h in range(horizon+1)}
    assert all(k in moments for k in required[horizon]) and moments[0]==1
    if available is None:available=(1<<m)-1
    assert 0<=available<(1<<m)
    skipped=0
    @lru_cache(None)
    def solve(vals,h,allowed):
        nonlocal skipped
        mu=dict(zip(required[h],vals))
        choices=[(row[0]+sum(row[i+1]*mu[1<<i] for i in range(m)),'a'+str(a)) for a,row in enumerate(terminal)]
        if h:
            for j in range(m):
                if not allowed&(1<<j):continue
                value=prices[j]
                for o in (1,-1):
                    den=1+o*mu[1<<j];assert den>=0
                    if den==0:skipped+=1;continue
                    child=tuple((mu[k]+o*mu[k^(1<<j)])/den for k in required[h-1])
                    value+=(den/2)*solve(child,h-1,allowed^(1<<j))[0]
                choices.append((value,'e'+str(j)))
        best=min(v for v,_ in choices)
        return best,tuple(k for v,k in choices if v==best)
    value,choices=solve(tuple(moments[k] for k in required[horizon]),horizon,available)
    return {'value':value,'first_choices':choices,'beliefs':solve.cache_info().currsize,'zero_branches_skipped':skipped,'retained_features':len(required[horizon])}
