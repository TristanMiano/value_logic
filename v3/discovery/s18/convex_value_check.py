"""Frozen finite check specified in convex_values.md, Codex (GPT-6).

The cross/hull routines reuse the core_check.py construction; not independent.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import platform
import time

START = time.monotonic_ns()
COUNTS = dict(hulls=0, polygon_queries=0, edge_projections=0)


def cross(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])


def hull(points):
    COUNTS['hulls'] += 1
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


def distance(poly, target):
    COUNTS['polygon_queries'] += 1
    if len(poly)>=3 and all(cross(a,b,target)>=0
                           for a,b in zip(poly,poly[1:]+poly[:1])):
        return F(0), target
    options = []
    for a,b in zip(poly,poly[1:]+poly[:1]):
        COUNTS['edge_projections'] += 1
        edge = tuple(b[j]-a[j] for j in (0,1))
        denom = sum(v*v for v in edge)
        t = sum(edge[j]*(target[j]-a[j]) for j in (0,1))/denom
        t = max(F(0),min(F(1),t))
        z = tuple(a[j]+t*edge[j] for j in (0,1))
        options.append((sum((z[j]-target[j])**2 for j in (0,1)),z))
    return min(options)


centers = [(F(1),F(0)),(F(0),F(1)),(F(-1),F(0)),(F(0),F(-1))]
corners = [(F(2*x,5),F(2*y,5)) for x,y in product((-1,1),repeat=2)]
regions = [[tuple(a[j]+c[j] for j in (0,1)) for c in corners] for a in centers]
all_hulls = [hull(config) for config in product(*regions)]
ordinary = [hull([tuple(a[j]+c[j] for j in (0,1)) for a in centers])
            for c in corners]
core = hull([(F(1,5),F(0)),(F(-1,5),F(0)),
             (F(0),F(1,5)),(F(0),F(-1,5))])
targets = [(F(0),F(0)),(F(1,2),F(0)),(F(2),F(1))]
records = []
for q in targets:
    full = [distance(p,q)[0] for p in all_hulls]
    small = [distance(p,q)[0] for p in ordinary]
    value, action = distance(core,q)
    assert max(full)==max(small)
    assert max(full)<=value
    records.append(dict(target=list(map(str,q)),
                        independent_corner_max=str(max(full)),
                        common_corner_values=list(map(str,small)),
                        common_corner_max=str(max(small)),
                        common_core_cost=str(value),
                        common_core_action=list(map(str,action))))
assert records[1]['independent_corner_max']=='9/200'
assert records[1]['common_core_cost']=='9/100'
assert records[2]['independent_corner_max']=='98/25'
result = dict(status='PASS',evidence='DEVELOPMENT',attribution='Codex (GPT-6)',
              python=platform.python_version(),runtime_ns=time.monotonic_ns()-START,
              source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              reused_kernel_source_sha256=hashlib.sha256(
                  Path(__file__).with_name('core_check.py').read_bytes()).hexdigest(),
              records=records,counts=COUNTS,
              independent_configurations=len(all_hulls),ordinary_configurations=len(ordinary),
              new_source_calls=0,
              warning='Finite development check; ordinary same-corner method ties')
Path(__file__).with_name('convex_value_result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
