"""Exact finite belief control and normalized deterministic quotient.

Codex (GPT-6), 2026-10-12. DEVELOPMENT; ordinary control/abstraction kernels.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache


@dataclass(frozen=True)
class System:
    terminal:tuple
    cost:tuple
    obs:tuple
    dest:tuple

    def validate(self):
        n=len(self.terminal);assert n>0
        a=len(self.terminal[0]);e=len(self.cost[0]);assert a>0
        assert len(self.cost)==len(self.obs)==len(self.dest)==n
        for x in range(n):
            assert len(self.terminal[x])==a
            assert len(self.cost[x])==len(self.obs[x])==len(self.dest[x])==e
            assert all(isinstance(v,F) for v in self.terminal[x]+self.cost[x])
            assert all(type(y) is int and 0<=y<n for y in self.dest[x])
            assert all(type(o) is int for o in self.obs[x])


def solve(system,belief,horizon):
    system.validate();n=len(system.terminal);a=len(system.terminal[0]);e=len(system.cost[0])
    assert len(belief)==n and all(isinstance(p,F) and p>=0 for p in belief) and sum(belief)==1
    assert type(horizon) is int and horizon>=0
    @lru_cache(None)
    def visit(b,h):
        active=[(x,p) for x,p in enumerate(b) if p]
        choices=[(sum(p*system.terminal[x][j] for x,p in active),'a'+str(j)) for j in range(a)]
        if h:
            for j in range(e):
                value=sum(p*system.cost[x][j] for x,p in active);branches={}
                for x,p in active:
                    o,y=system.obs[x][j],system.dest[x][j]
                    if o not in branches:branches[o]=[F(0)]*n
                    branches[o][y]+=p
                for masses in branches.values():
                    total=sum(masses);posterior=tuple(p/total for p in masses)
                    value+=total*visit(posterior,h-1)[0]
                choices.append((value,'e'+str(j)))
        best=min(v for v,_ in choices)
        return best,tuple(k for v,k in choices if v==best)
    value,choices=visit(tuple(belief),horizon)
    return value,choices,visit.cache_info().currsize


def normalize(system):
    system.validate();base=tuple(min(row) for row in system.terminal)
    r=tuple(tuple(v-base[x] for v in row) for x,row in enumerate(system.terminal))
    q=tuple(tuple(v+base[system.dest[x][j]]-base[x] for j,v in enumerate(row)) for x,row in enumerate(system.cost))
    return System(r,q,system.obs,system.dest),base


def classify(keys):
    ids={};result=[]
    for k in keys:
        if k not in ids:ids[k]=len(ids)
        result.append(ids[k])
    return tuple(result)


def quotient(system):
    norm,base=normalize(system);n=len(base);blocks=classify(norm.terminal)
    history=[len(set(blocks))]
    while True:
        keys=[(blocks[x],tuple((norm.cost[x][e],norm.obs[x][e],blocks[norm.dest[x][e]]) for e in range(len(norm.cost[x])))) for x in range(n)]
        new=classify(keys);history.append(len(set(new)))
        if new==blocks:break
        blocks=new
    representatives=[blocks.index(k) for k in range(max(blocks)+1)]
    reduced=System(tuple(norm.terminal[x] for x in representatives),tuple(norm.cost[x] for x in representatives),
                   tuple(norm.obs[x] for x in representatives),tuple(tuple(blocks[y] for y in norm.dest[x]) for x in representatives))
    reduced.validate()
    return reduced,blocks,base,history


def aggregate(belief,blocks):
    masses=[F(0)]*(max(blocks)+1)
    for x,p in enumerate(belief):masses[blocks[x]]+=p
    return tuple(masses)
