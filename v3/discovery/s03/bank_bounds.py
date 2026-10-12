"""Rational PAC-Bayes lower certificates; floating posterior advice only.

Codex (GPT-6), 2026-10-12. DEVELOPMENT. See policy_bank.md for source contract.
"""
from fractions import Fraction as F
from functools import lru_cache
import math


def reduced_log(r,n):
    assert 1<=r<=2 and n>=1
    z=(r-1)/(r+1);power=z;total=F(0)
    for k in range(n):total+=2*power/(2*k+1);power*=z*z
    tail=2*power/((2*n+1)*(1-z*z))
    return total,total+tail


@lru_cache(None)
def log_interval(x,n=16):
    assert isinstance(x,F) and x>0
    k=x.numerator.bit_length()-x.denominator.bit_length();r=x/(F(2)**k)
    if r<1:k-=1;r*=2
    if r>=2:k+=1;r/=2
    lo,hi=reduced_log(r,n);a,b=reduced_log(F(2),n)
    return (lo+k*a,hi+k*b) if k>=0 else (lo+k*b,hi+k*a)


def certificate(sums,t,Q,P,lam,alpha):
    assert type(t) is int and t>0 and len(sums)==len(Q)==len(P)
    assert all(isinstance(x,F) for x in list(sums)+list(Q)+list(P)+[lam,alpha])
    assert all(0<=s<=t for s in sums) and all(q>=0 for q in Q) and all(p>0 for p in P)
    assert sum(Q)==sum(P)==1 and lam>0 and 0<alpha<1
    kl_upper=sum(q*log_interval(q/p)[1] for q,p in zip(Q,P) if q)
    assert kl_upper>=0
    empirical=sum(q*s for q,s in zip(Q,sums))/t
    lower=empirical-(kl_upper+log_interval(1/alpha)[1])/(lam*t)-lam/8
    return {'lower':max(F(0),lower),'unclipped_lower':lower,'empirical_lower_mean':empirical,'kl_upper':kl_upper}


def propose(sums,P,lam,denominator=1<<20):
    assert denominator>0
    logits=[math.log(float(p))+float(lam*s) for p,s in zip(P,sums)];scale=max(logits)
    weights=[math.exp(x-scale) for x in logits];total=sum(weights)
    raw=[denominator*w/total for w in weights];counts=[int(x) for x in raw]
    remainder=denominator-sum(counts);assert 0<=remainder<=len(counts)
    order=sorted(range(len(counts)),key=lambda i:(-(raw[i]-counts[i]),i))
    for i in order[:remainder]:counts[i]+=1
    return tuple(F(n,denominator) for n in counts)
