"""Graded, already-warranted lower receipts for a fixed finite value source.

Codex (GPT-6), 2026-10-12. DEVELOPMENT. None wealth means a hard-sum rejection.
"""
from fractions import Fraction as F


def wealth(lowers,N,T,eta):
    assert type(N) is int and N>0 and len(lowers)<=N and 0<=T<=N and eta>=0
    assert all(isinstance(z,F) and 0<=z<=1 for z in lowers)
    if sum(lowers)>T:return None
    k=F(0);value=F(1)
    for j,z in enumerate(lowers):
        mu=min(F(1),(T-k)/(N-j));value*=(1+eta*z)/(1+eta*mu);k+=z
    return value


def mixture(lowers,N,T,etas=(F(4),F(16))):
    assert etas
    values=[wealth(lowers,N,T,eta) for eta in etas]
    return None if values[0] is None else sum(values)/len(values)


def reject(lowers,N,T,alpha):
    assert 0<alpha<1
    value=mixture(lowers,N,T)
    return value is None or value>=1/alpha


def partial_polynomial(poly,known):
    assert all(type(i) is int and i>=0 and s in (-1,1) for i,s in known.items())
    fixed=sum(1<<i for i in known);negative=sum(1<<i for i,s in known.items() if s==-1);result={}
    for mask,c in poly.items():
        key=mask&~fixed;sign=-1 if (mask&negative).bit_count()%2 else 1
        result[key]=result.get(key,F(0))+sign*c
    return {mask:c for mask,c in result.items() if c}


def interval(poly,known):
    reduced=partial_polynomial(poly,known);center=reduced.get(0,F(0));radius=sum(abs(c) for mask,c in reduced.items() if mask)
    return center-radius,center+radius
