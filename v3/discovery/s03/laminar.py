"""Exact laminar count and product-pair value source. DEVELOPMENT.

Codex (GPT-6), 2026-10-11. Ordinary tree DP; no statistical acquisition here.
Costs are exact Fraction values. Structural input is a balanced binary tree.
"""
from dataclasses import dataclass
from fractions import Fraction
import heapq


class Conflict(ValueError):
    pass


@dataclass
class Node:
    children: tuple
    parent: int | None
    leaf: int | None
    size: int
    lower: int
    upper: int


class CountTree:
    def __init__(self, n, bounds=None, allowed=None):
        if type(n) is not int or n < 1:
            raise ValueError('positive integer size required')
        self.n, self.nodes, self.leaf_node = n, [], {}

        def build(start, stop, parent):
            v = len(self.nodes)
            self.nodes.append(Node((), parent, start if stop-start == 1 else None,
                                   stop-start, 0, stop-start))
            if stop-start == 1:
                self.leaf_node[start] = v
            else:
                mid = (start+stop)//2
                self.nodes[v].children = (build(start,mid,v),build(mid,stop,v))
            return v
        build(0,n,None)
        for v, interval in (bounds or {}).items():
            if type(v) is not int or not 0 <= v < len(self.nodes):
                raise ValueError('node identity')
            lo,hi = interval
            if type(lo) is not int or type(hi) is not int or not 0 <= lo <= hi <= self.nodes[v].size:
                raise ValueError('count interval')
            self.nodes[v].lower, self.nodes[v].upper = lo,hi
        self.allowed = [set((0,1)) for _ in range(n)]
        if allowed is not None:
            if len(allowed) != n:
                raise ValueError('allowed size')
            for i, values in enumerate(allowed):
                if any(type(x) is not int or x not in (0,1) for x in values):
                    raise ValueError('Boolean domain')
                self.allowed[i] = set(values)
        self.lo, self.hi = [0]*len(self.nodes), [0]*len(self.nodes)
        self.child_lo, self.child_hi = [0]*len(self.nodes), [0]*len(self.nodes)
        for v in reversed(range(len(self.nodes))):
            self._recompute(v)
        self.version = 0

    def _recompute(self,v):
        node = self.nodes[v]
        if node.leaf is not None:
            vals=self.allowed[node.leaf]
            low,high=(min(vals),max(vals)) if vals else (1,0)
        else:
            if any(self.lo[c] > self.hi[c] for c in node.children):
                self.lo[v], self.hi[v] = 1,0
                return
            low=sum(self.lo[c] for c in node.children)
            high=sum(self.hi[c] for c in node.children)
            self.child_lo[v],self.child_hi[v]=low,high
        self.lo[v],self.hi[v]=max(node.lower,low),min(node.upper,high)

    def set_allowed(self,index,values,parent_version):
        if type(parent_version) is not int or parent_version != self.version or type(index) is not int or not 0 <= index < self.n:
            raise ValueError('version/index')
        values=list(values)
        if any(type(x) is not int or x not in (0,1) for x in values):
            raise ValueError('Boolean domain')
        vals=set(values)
        self.allowed[index]=vals
        v=self.leaf_node[index]; steps=0
        while v is not None:
            self._recompute(v);steps+=1;v=self.nodes[v].parent
        self.version+=1
        return steps

    def interval(self,v):
        if type(v) is not int or not 0 <= v < len(self.nodes):
            raise ValueError('node identity')
        if self.lo[0] > self.hi[0]:
            raise Conflict('empty source')
        path=[];current=v
        while self.nodes[current].parent is not None:
            path.append(current);current=self.nodes[current].parent
        a,b=self.lo[0],self.hi[0]
        for c in reversed(path):
            p=self.nodes[c].parent
            a,b=max(self.lo[c],a-(self.child_hi[p]-self.hi[c])),min(self.hi[c],b-(self.child_lo[p]-self.lo[c]))
        return a,b,len(path)+1

    def descendants(self,v):
        node=self.nodes[v]
        if node.leaf is not None:
            return [node.leaf]
        return [i for c in node.children for i in self.descendants(c)]

    def feasible(self,x):
        if len(x)!=self.n or any(a not in self.allowed[i] for i,a in enumerate(x)):
            return False
        counts=[0]*len(self.nodes)
        for v in reversed(range(len(self.nodes))):
            node=self.nodes[v]
            counts[v]=x[node.leaf] if node.leaf is not None else sum(counts[c] for c in node.children)
            if not node.lower <= counts[v] <= node.upper:
                return False
        return True


def minimize(tree,pairs,weights):
    """Return (exact value, base witness, current witness, merge-item work)."""
    if len(pairs)!=tree.n or len(weights)!=tree.n:
        raise ValueError('objective size')
    local=[]
    for i,ps in enumerate(pairs):
        if any(len(p)!=2 or any(type(x) is not int or x not in (0,1) for x in p) for p in ps):
            raise ValueError('pair relation')
        options={}
        for x in tree.allowed[i]:
            choices=[(Fraction(weights[i])*z,z) for a,z in ps if a==x]
            if choices:
                options[x]=min(choices)
        local.append(options)
    work=0

    def recurse(v):
        nonlocal work
        node=tree.nodes[v]
        if node.leaf is not None:
            i=node.leaf
            opts={x:r for x,r in local[i].items() if node.lower<=x<=node.upper}
            if not opts:
                raise Conflict('empty leaf pair source')
            low,high=min(opts),max(opts)
            increments=[] if low==high else [(opts[1][0]-opts[0][0],i)]
            return low,high,opts[low][0],{i:low},increments
        parts=[recurse(c) for c in node.children]
        low,high=sum(p[0] for p in parts),sum(p[1] for p in parts)
        cost=sum((p[2] for p in parts),Fraction())
        chosen={i:x for p in parts for i,x in p[3].items()}
        increments=list(heapq.merge(*(p[4] for p in parts)))
        work+=len(increments)
        newlo,newhi=max(low,node.lower),min(high,node.upper)
        if newlo>newhi:
            raise Conflict('empty nested-count source')
        for delta,i in increments[:newlo-low]:
            cost+=delta;chosen[i]=1
        return newlo,newhi,cost,chosen,increments[newlo-low:newhi-low]
    _,_,cost,chosen,increments=recurse(0)
    for delta,i in increments:
        if delta >= 0:
            break
        cost+=delta;chosen[i]=1
    x=tuple(chosen[i] for i in range(tree.n))
    z=tuple(local[i][x[i]][1] for i in range(tree.n))
    assert tree.feasible(x)
    assert all((a,b) in pairs[i] for i,(a,b) in enumerate(zip(x,z)))
    assert cost==sum((Fraction(w)*b for w,b in zip(weights,z)),Fraction())
    return cost,x,z,work


def endpoints(tree,pairs,weights):
    lower=minimize(tree,pairs,weights)
    neg=minimize(tree,pairs,[-Fraction(w) for w in weights])
    upper=(-neg[0],neg[1],neg[2],neg[3])
    return lower,upper
