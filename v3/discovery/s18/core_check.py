"""Exact development check specified in translated_core.md; no numeric solver."""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import hashlib
import json
import platform
import time

START = time.monotonic_ns()


def cross(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])


def hull(points):
    points = sorted(set(points))
    if len(points)<=1:
        return points
    lower, upper = [], []
    for p in points:
        while len(lower)>=2 and cross(lower[-2],lower[-1],p)<=0:
            lower.pop()
        lower.append(p)
    for p in reversed(points):
        while len(upper)>=2 and cross(upper[-2],upper[-1],p)<=0:
            upper.pop()
        upper.append(p)
    return lower[:-1]+upper[:-1]


def clipped(poly, a, b):
    if not poly:
        return []
    out = []
    for p,q in zip(poly,poly[1:]+poly[:1]):
        fp, fq = cross(a,b,p), cross(a,b,q)
        if fp>=0:
            out.append(p)
        if (fp<0<fq) or (fq<0<fp):
            ratio = fp/(fp-fq)
            out.append(tuple(p[j]+ratio*(q[j]-p[j]) for j in range(2)))
    return hull(out)


def intersect(a, b):
    assert len(b)>=3
    for u,v in zip(b,b[1:]+b[:1]):
        a = clipped(a,u,v)
    return a


centers = [(F(1),F(0)),(F(0),F(1)),(F(-1),F(0)),(F(0),F(-1))]
r = F(2,5)
regions = [[(a[0]+x*r,a[1]+y*r) for x,y in product((-1,1),repeat=2)]
           for a in centers]
assert all(len(hull(box))==4 for box in regions)
for i,j in combinations(range(4),2):
    assert not intersect(hull(regions[i]),hull(regions[j]))


def all_configs(ids):
    common = [(F(-2),F(-2)),(F(2),F(-2)),(F(2),F(2)),(F(-2),F(2))]
    n = 0
    record = []
    for config in product(*(regions[i] for i in ids)):
        actual = hull(config)
        assert len(actual)>=3
        common = intersect(common,actual)
        n += 1
        record.append([[str(x),str(y)] for x,y in actual])
    digest = hashlib.sha256(json.dumps(record,separators=(',',':')).encode()).hexdigest()
    return dict(regions=list(ids),configurations=n,
                intersection=[[str(x),str(y)] for x,y in common],
                actual_hulls_sha256=digest), common


full, polygon = all_configs(range(4))
expected = hull([(F(1,5),F(0)),(F(-1,5),F(0)),
                 (F(0),F(1,5)),(F(0),F(-1,5))])
assert polygon==expected, (polygon,expected)
triples = []
for ids in combinations(range(4),3):
    info, polygon = all_configs(ids)
    assert polygon==[]
    triples.append(info)
assert full['configurations']==256
assert sum(t['configurations'] for t in triples)==256

# Separate finite dual contradiction for E,N,W; support minima are exact
# corner minima, independent of the polygon intersection implementation.
normals = [(F(0),F(-1)),(F(1),F(1)),(F(-1),F(1))]
rhs = [max(min(h[0]*x+h[1]*y for x,y in regions[i]) for i in (0,1,2))
       for h in normals]
assert rhs==[F(-2,5),F(1,5),F(1,5)]
multipliers = (F(2),F(1),F(1))
assert all(sum(w*h[j] for w,h in zip(multipliers,normals))==0 for j in (0,1))
contradiction = sum(w*b for w,b in zip(multipliers,rhs))
assert contradiction==F(-2,5)

result = dict(status='PASS',attribution='Codex (GPT-6)',evidence='DEVELOPMENT',
              python=platform.python_version(),runtime_ns=time.monotonic_ns()-START,
              source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              centers=[[str(x),str(y)] for x,y in centers],square_halfside=str(r),
              nonempty_disjoint_full_dimensional_regions=True,
              full=full,triples=triples,
              triple_infeasibility=dict(normals=[[str(x),str(y)] for x,y in normals],
                                       rhs=list(map(str,rhs)),
                                       multipliers=list(map(str,multipliers)),
                                       resulting_rhs=str(contradiction)))
Path(__file__).with_name('core_result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(status=result['status'],runtime_ns=result['runtime_ns'],
                     total_corner_configurations=512,full_core=full['intersection'],
                     empty_triples=4,contradiction=str(contradiction))))
