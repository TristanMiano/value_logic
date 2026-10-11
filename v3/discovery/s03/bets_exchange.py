"""Exact exchange certificate from a fallible count-allocation proposal.

Codex (GPT-6), 2026-10-11. DEVELOPMENT. Uses simple O(G) neighbor scans.
"""
from fractions import Fraction as F
from positive_bets import product


def proposal(groups,total,kind='trace'):
    lows=[g.positives for g in groups];highs=[g.N for g in groups]
    if sum(lows)>total:return None
    if kind not in ('trace','proportional'):
        raise ValueError('proposal kind')
    if kind=='proportional':
        slopes=[g.N for g in groups];offsets=[0]*len(groups)
    else:
        slopes=[len(g.trace) for g in groups]
        offsets=[(-g.N+sum(g.N-rem+k for rem,k,z in g.trace)/len(g.trace)) if g.trace else 0 for g in groups]
    # Unsampled groups have constant wealth. Allocate to them only after all
    # sampled groups have exhausted their capacity under the trace heuristic.
    active=[i for i,s in enumerate(slopes) if s]
    target=min(total,sum(highs[i] for i in active)+sum(lows[i] for i in range(len(groups)) if i not in active))
    def vals(c):
        return [max(lo,min(hi,c*s+b)) if s else float(lo) for lo,hi,s,b in zip(lows,highs,slopes,offsets)]
    left,right=0.0,1.0
    while sum(vals(right))<target:right*=2
    for _ in range(60):
        mid=(left+right)/2
        if sum(vals(mid))<target:left=mid
        else:right=mid
    real=vals(right);allocation=[max(lo,min(hi,int(v))) for v,lo,hi in zip(real,lows,highs)]
    # Float proposal is never trusted. Repair integer feasibility, then the
    # rational exchange certificate decides whether it is optimal.
    while sum(allocation)>total:
        i=max((i for i in range(len(groups)) if allocation[i]>lows[i]),key=lambda i:allocation[i]-real[i])
        allocation[i]-=1
    while sum(allocation)<total:
        i=max((i for i in range(len(groups)) if allocation[i]<highs[i]),key=lambda i:real[i]-allocation[i])
        allocation[i]+=1
    return tuple(allocation)


def exchange(groups,total,initial=None,kind='trace',stop_below=None):
    if type(total) is not int or not 0<=total<=sum(g.N for g in groups):
        raise ValueError('total')
    if sum(g.positives for g in groups)>total:
        return {'status':'hard_refutation','value':None,'allocation':None,'exchanges':0,'neighbor_scans':0,'initial':None}
    alloc=list(initial if initial is not None else proposal(groups,total,kind))
    if len(alloc)!=len(groups) or sum(alloc)!=total or any(type(m) is not int or not g.positives<=m<=g.N for g,m in zip(groups,alloc)):
        raise ValueError('feasible count proposal required')
    start=tuple(alloc);value=product(g.wealth(m) for g,m in zip(groups,alloc));moves=scans=0
    while True:
        if stop_below is not None and value<F(stop_below):
            return {'status':'counterexample','value':value,'allocation':tuple(alloc),'exchanges':moves,'neighbor_scans':scans,'initial':start}
        chosen=[];unselected=[]
        for i,(g,m) in enumerate(zip(groups,alloc)):
            scans+=1
            if m>g.positives:chosen.append((g.ratio(m-1),i,m-1))
            if m<g.N:unselected.append((g.ratio(m),i,m))
        if not chosen or not unselected or max(chosen)[0]<=min(unselected)[0]:
            assert value==product(g.wealth(m) for g,m in zip(groups,alloc))
            return {'status':'optimal','value':value,'allocation':tuple(alloc),'exchanges':moves,'neighbor_scans':scans,'initial':start}
        r,g,_=max(chosen);p,h,_=min(unselected)
        assert g!=h and p<r
        alloc[g]-=1;alloc[h]+=1;value*=p/r;moves+=1
