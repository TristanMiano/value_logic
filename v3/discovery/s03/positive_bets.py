"""Censored positive-production e-process and exact count profiling.

Codex (GPT-6), 2026-10-11. DEVELOPMENT. A local arithmetic kernel, not an
external proof checker or sampling-authority boundary. Each observe represents
one uniform draw chosen after group selection; Z=0 means no checked proof.
"""
from dataclasses import dataclass,field
from fractions import Fraction as F
import heapq


@dataclass
class Group:
    N: int
    etas: tuple = (F(1),)
    trace: list = field(default_factory=list)
    positives: int = 0
    cache: dict = field(default_factory=dict)
    evaluations: int = 0

    def __post_init__(self):
        if type(self.N) is not int or self.N<1:
            raise ValueError('population size')
        self.etas=tuple(F(v) for v in self.etas)
        if not self.etas or min(self.etas)<0:
            raise ValueError('nonnegative mixture bets')

    def observe(self,proved):
        if type(proved) is not int or proved not in (0,1) or len(self.trace)>=self.N:
            raise ValueError('one production indicator per draw')
        self.trace.append((self.N-len(self.trace),self.positives,proved))
        self.positives+=proved
        self.cache.clear()

    def wealth(self,m):
        if type(m) is not int or not self.positives<=m<=self.N:
            raise ValueError('hypothetical count')
        if m not in self.cache:
            parts=[]
            for eta in self.etas:
                val=F(1)
                for remaining,k,z in self.trace:
                    mu=min(F(1),F(m-k,remaining))
                    val*=(1+eta*z)/(1+eta*mu)
                parts.append(val)
            self.cache[m]=sum(parts,F())/len(parts)
            self.evaluations+=1
        return self.cache[m]

    def ratio(self,m):
        return self.wealth(m+1)/self.wealth(m)


def profile(groups,total):
    """Minimize product wealth over sum m<=total, m_g>=checked positives.

    Return None when hard receipts alone refute the total upper-count null.
    The exact null vector witness and ratio-choice work are retained.
    """
    if type(total) is not int or not 0<=total<=sum(g.N for g in groups):
        raise ValueError('total count upper bound')
    allocation=[g.positives for g in groups]
    if sum(allocation)>total:
        return None
    value=F(1);heap=[]
    for i,g in enumerate(groups):
        value*=g.wealth(allocation[i])
        if allocation[i]<g.N:
            heapq.heappush(heap,(g.ratio(allocation[i]),i))
    needed=total-sum(allocation)
    for _ in range(needed):
        ratio,i=heapq.heappop(heap)
        value*=ratio;allocation[i]+=1
        if allocation[i]<groups[i].N:
            heapq.heappush(heap,(groups[i].ratio(allocation[i]),i))
    assert value==product(g.wealth(m) for g,m in zip(groups,allocation))
    return value,tuple(allocation),needed


def product(vals):
    p=F(1)
    for x in vals:
        p*=x
    return p


def warrant(groups,target,alpha):
    result=profile(groups,target-1)
    return result is None or result[0]>=1/F(alpha),result
