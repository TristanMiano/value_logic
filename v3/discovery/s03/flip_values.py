"""Finite Boolean-flip value advice and sharp deterministic box regret.

Codex (GPT-6), 2026-10-12. DEVELOPMENT. Acquisition/semantics are external.
None denotes immediate terminal action 0; a tuple is a flip set then action 1.
"""
from fractions import Fraction as F


def top(values,H):
    ordered=sorted(range(len(values)),key=lambda i:(-values[i],i))[:H]
    return tuple(sorted(i for i in ordered if values[i]>0))


def cost(means,prices,J):
    return F(0) if J is None else sum(means)-2*sum(means[i] for i in J)+sum(prices[i] for i in J)


def advise(means,prices,H):
    J=top([2*m-q for m,q in zip(means,prices)],H)
    return None if cost(means,prices,J)>=0 else J


def regret(lower,upper,prices,H,J):
    m=len(lower)
    assert len(upper)==len(prices)==m and type(H) is int and 0<=H<=m
    assert all(F(-1)<=l<=u<=F(1) and q>=0 for l,u,q in zip(lower,upper,prices))
    assert J is None or (len(set(J))==len(J)<=H and all(type(i) is int and 0<=i<m for i in J))
    if J is None:
        K=top([l+u-q for l,u,q in zip(lower,upper,prices)],H)
        bound=-sum(lower)+sum(lower[i]+upper[i]-prices[i] for i in K)
        if bound<=0:return F(0),None,tuple(lower)
        means=tuple(upper[i] if i in K else lower[i] for i in range(m))
        return bound,K,means
    J=set(J);qj=sum(prices[i] for i in J)
    A=sum(upper[i] if i not in J else -lower[i] for i in range(m))+qj
    K=top([2*(lower[i] if i in J else upper[i])-prices[i] for i in range(m)],H)
    B=qj-2*sum(lower[i] for i in J)+sum(2*(lower[i] if i in J else upper[i])-prices[i] for i in K)
    if A>B:return A,None,tuple(lower[i] if i in J else upper[i] for i in range(m))
    means=tuple(upper[i] if i in K and i not in J else lower[i] for i in range(m))
    return B,K,means
