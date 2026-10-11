"""Standard continuous convex advice, then exact rational repair.

Codex (GPT-6), 2026-10-11. DEVELOPMENT. SciPy is advice, never a warrant.
"""
import math
import time
import numpy as np
from scipy.optimize import minimize
from bets_exchange import proposal,exchange


def float_stats(group,m):
    logs=[];derivatives=[]
    for eta_q in group.etas:
        eta=float(eta_q)
        value=group.positives*math.log1p(eta);slope=0.0
        for remaining,k,_ in group.trace:
            mu=min(1.0,(m-k)/remaining)
            value-=math.log1p(eta*mu)
            if mu<1:slope-=eta/(remaining+eta*(m-k))
        logs.append(value);derivatives.append(slope)
    maximum=max(logs);weights=[math.exp(v-maximum) for v in logs];normal=sum(weights)
    return maximum+math.log(normal/len(logs)),sum(w*d for w,d in zip(weights,derivatives))/normal


def rounded(groups,total,real):
    lows=[g.positives for g in groups];highs=[g.N for g in groups]
    if len(real)!=len(groups) or not all(math.isfinite(float(x)) for x in real):
        return proposal(groups,total,'proportional')
    def clip(shift):return [max(lo,min(hi,float(x)+shift)) for x,lo,hi in zip(real,lows,highs)]
    left=-max(highs)*2.0;right=max(highs)*2.0
    for _ in range(60):
        mid=(left+right)/2
        if sum(clip(mid))<total:left=mid
        else:right=mid
    vals=clip(right);ans=[int(x) for x in vals]
    while sum(ans)>total:
        i=max((i for i in range(len(groups)) if ans[i]>lows[i]),key=lambda i:ans[i]-vals[i]);ans[i]-=1
    while sum(ans)<total:
        i=max((i for i in range(len(groups)) if ans[i]<highs[i]),key=lambda i:vals[i]-ans[i]);ans[i]+=1
    return tuple(ans)


def numerical_profile(groups,total,stop_below=None):
    begin=time.perf_counter_ns();initial=proposal(groups,total,'proportional')
    if initial is None:
        got=exchange(groups,total);got['numerical']={'status':'hard_refutation','proposal_ns':time.perf_counter_ns()-begin};return got
    calls=0
    def objective(x):
        nonlocal calls
        calls+=1;out=[float_stats(g,m) for g,m in zip(groups,x)]
        return sum(v for v,d in out),np.array([d for v,d in out])
    # Remove fixed coordinates to avoid solver-specific all-fixed handling.
    free=[i for i,g in enumerate(groups) if g.positives<g.N]
    if not free or total in (sum(g.positives for g in groups),sum(g.N for g in groups)):
        integer=rounded(groups,total,initial);status='boundary';iterations=0;success=True
    else:
        fixed=[float(x) for x in initial]
        def reduced(x):
            allx=fixed.copy()
            for i,m in zip(free,x):allx[i]=m
            value,grad=objective(allx)
            return value,grad[free]
        remain=total-sum(initial[i] for i in range(len(groups)) if i not in free)
        res=minimize(reduced,np.array([initial[i] for i in free],dtype=float),jac=True,method='SLSQP',
                     bounds=[(groups[i].positives,groups[i].N) for i in free],
                     constraints=[{'type':'eq','fun':lambda x:sum(x)-remain,'jac':lambda x:np.ones(len(x))}],
                     options={'maxiter':150,'ftol':1e-10})
        real=fixed.copy()
        for i,m in zip(free,res.x):real[i]=m
        integer=rounded(groups,total,real);status=str(res.message);iterations=int(res.nit);success=bool(res.success)
    proposal_ns=time.perf_counter_ns()-begin
    got=exchange(groups,total,initial=integer,stop_below=stop_below)
    got['numerical']={'status':status,'reported_success':success,'iterations':iterations,'objective_calls':calls,'proposal_ns':proposal_ns}
    got['complete_profile_ns']=time.perf_counter_ns()-begin
    return got
