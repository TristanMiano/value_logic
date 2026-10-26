"""Bounded exact development probe of C1/C3; uses no numerical LP solver.

Enumerate every vertex of the four-dimensional interval example and check the
original nonlinear report semantics at each one. Also check a nontrivial affine
gauge example. Frozen before execution; outputs are development evidence only.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import hashlib
import json
import platform
import time

start = time.monotonic_ns()
rows = []
def add(a, b):
    rows.append((tuple(map(F, a)), F(b)))

# x=(p1,p2,t1,t2); p3=1-p1-p2. All constraints are a*x<=b.
add((-1,0,0,0),0)
add((0,-1,0,0),0)
add((1,1,0,0),1)
reports = ((0,2,F(19,10),F(21,10)),
           (1,2,F(29,10),F(31,10)),
           (1,3,F(59,10),F(61,10)))
for j,t,lo,hi in reports:
    a = [0]*4
    a[j],a[t] = -1,lo
    add(a,0)
    a = [0]*4
    a[j],a[t] = 1,-hi
    add(a,0)
add((1,1,0,F(99,10)),1)
add((-1,-1,0,-F(101,10)),-1)
add((0,0,-1,0),-F(1,11))
add((0,0,1,0),F(1,9))
add((0,0,0,-1),-F(1,21))
add((0,0,0,1),F(1,19))

def solve(selected):
    aug = [list(a)+[b] for a,b in selected]
    for j in range(4):
        pivot = next((i for i in range(j,4) if aug[i][j]),None)
        if pivot is None:
            return None
        aug[j],aug[pivot] = aug[pivot],aug[j]
        z = aug[j][j]
        aug[j] = [v/z for v in aug[j]]
        for i in range(4):
            if i != j:
                z = aug[i][j]
                aug[i] = [a-z*b for a,b in zip(aug[i],aug[j])]
    return tuple(aug[i][-1] for i in range(4))

vertices = set()
bases = 0
for ids in combinations(range(len(rows)),4):
    bases += 1
    x = solve([rows[i] for i in ids])
    if x is not None and all(sum(a*v for a,v in zip(row,x))<=b
                             for row,b in rows):
        vertices.add(x)
assert vertices
for p1,p2,t1,t2 in vertices:
    p3 = 1-p1-p2
    assert min(p1,p2,p3)>=0 and t1>0 and t2>0
    assert 9<=1/t1<=11 and 19<=1/t2<=21
    actual = (p1/t1,p2/t1,p2/t2,p3/t2)
    bounds = ((F(19,10),F(21,10)),(F(29,10),F(31,10)),
              (F(59,10),F(61,10)),(F(99,10),F(101,10)))
    assert all(lo<=v<=hi for v,(lo,hi) in zip(actual,bounds))

objective = lambda x: 1-2*x[0]-x[1]
low = min(vertices,key=objective)
high = max(vertices,key=objective)
assert objective(low)==F(1590,5921)>F(1,4)
assert objective(high)==F(670,2027)
assert low[:2] != high[:2]  # the target decision does not identify p.

# Different calibrations can preserve all reports with unknown offsets.
p = (F(1,5),F(3,10),F(1,2))
alpha = F(1,2)
pp = tuple(alpha*v+(1-alpha)/3 for v in p)
assert pp != p and sum(pp)==1
gauge_cases = []
for scale,offset,js in ((F(10),F(7),(0,1)),(F(20),F(-4),(1,2))):
    ss = scale/alpha
    bb = offset-scale*(1-alpha)/(3*alpha)
    old = tuple(scale*p[j]+offset for j in js)
    new = tuple(ss*pp[j]+bb for j in js)
    assert old==new
    gauge_cases.append(dict(scale=scale,offset=offset,
                            new_scale=ss,new_offset=bb,reports=old))

def strings(obj):
    if isinstance(obj,F):
        return str(obj)
    if isinstance(obj,dict):
        return {k:strings(v) for k,v in obj.items()}
    if isinstance(obj,(tuple,list)):
        return [strings(v) for v in obj]
    return obj

result = dict(status="pass",development=True,model="Codex (GPT-6)",
    inequalities=len(rows),candidate_bases=bases,vertices=len(vertices),
    lower=objective(low),upper=objective(high),lower_vertex=low,upper_vertex=high,
    strict_threshold=F(1,4),law_identified=False,gauge_cases=gauge_cases,
    source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    python=platform.python_version(),runtime_ns=time.monotonic_ns()-start,
    scope="one exact interval fixture and affine-gauge check; no economic measurement")
print(json.dumps(strings(result),indent=2))
