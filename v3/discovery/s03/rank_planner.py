"""Ordinary linear-matroid prefixes and rank-dependent decision values."""
from fractions import Fraction as F

def insert(basis,row):
    while row:
        p=row.bit_length()-1
        if p in basis:row^=basis[p]
        else:basis[p]=row;return True
    return False

def rank(rows):
    basis={}
    for row in rows:insert(basis,row)
    return len(basis)

def profile(rows,costs,d):
    assert len(rows)==len(costs) and type(d) is int and d>=0
    assert all(type(a) is int and 0<=a<1<<d for a in rows)
    assert all(isinstance(q,F) and q>=0 for q in costs)
    order=sorted(range(len(rows)),key=lambda j:(costs[j],j));basis={};chosen=[];cost=F(0)
    points=[dict(rank=0,cost=cost,success=F(1,1<<d),queries=())]
    for j in order:
        if insert(basis,rows[j]):
            chosen.append(j);cost+=costs[j]
            points.append(dict(rank=len(chosen),cost=cost,success=F(1,1<<(d-len(chosen))),queries=tuple(chosen)))
    return points

def best(points,lam=F(1)):
    assert isinstance(lam,F) and lam>=0
    return max(points,key=lambda p:(p['success']-lam*p['cost'],-p['cost']))

def completion(rows,labels,d):
    """Return one consistent assignment, including all elimination cost."""
    assert len(rows)==len(labels) and all(type(y) is int and y in (0,1) for y in labels)
    basis={}
    for row,y in zip(rows,labels):
        assert type(row) is int and 0<=row<1<<d
        while row:
            p=row.bit_length()-1
            if p in basis:
                other,b=basis[p];row^=other;y^=b
            else:basis[p]=(row,y);break
        if not row:assert y==0,'inconsistent labels'
    x=0
    for p,(row,y) in sorted(basis.items()):
        if ((row&x).bit_count()&1)!=y:x^=1<<p
    assert all(((row&x).bit_count()&1)==y for row,y in zip(rows,labels))
    return x
