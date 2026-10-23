"""Exact finite conditional-margin screens; not deployment validation."""
from decimal import Decimal, localcontext
from fractions import Fraction as F
from itertools import product
from math import comb
import hashlib
import json
from pathlib import Path
from time import perf_counter_ns

HERE = Path(__file__).resolve().parent
OUT = HERE/'conditional_probe.json'
assert not OUT.exists(), 'Preserve exposed evidence.'
start = perf_counter_ns()

def compositions(n, k):
    if k == 1:
        yield (n,)
    else:
        for a in range(n+1):
            for rest in compositions(n-a,k-1):
                yield (a,)+rest

n, unresolved = 1500, 30
num = sum(comb(n,j)*3**j*97**(n-j) for j in range(unresolved+1))
den = 100**n
alpha = F(num,den)
assert alpha < F(1,20)
with localcontext() as ctx:
    ctx.prec = 40
    decimal_alpha = str(Decimal(alpha.numerator)/Decimal(alpha.denominator))

# Every labelled partition of a four-point line into three nonempty classes.
# 0=good release, 1=bad release, 2=outside. Exact pointwise envelope equality.
envelopes = 0
for points in [(0,1,2,3),(0,2,4,9),(0,1,10,30)]:
    for labels in product(range(3),repeat=4):
        if set(labels) != {0,1,2}:
            continue
        for eps, lam in product([F(0),F(1,10),F(1,2),F(1)],
                                [F(0),F(1,10),F(1,3),F(2)]):
            h = [-eps,1-eps,F(0)]
            for i,x in enumerate(points):
                db = min(abs(x-y) for y,l in zip(points,labels) if l==1)
                do = min(abs(x-y) for y,l in zip(points,labels) if l==2)
                actual = max(h[l]-lam*abs(x-y) for y,l in zip(points,labels))
                receipt = max(1-eps-lam*db,-eps,-lam*do)
                assert actual == receipt
                envelopes += 1

# All grid transports for a three-point metric, including unprotected source
# mass in bad AND outside states. Distances G->B=b, G->O=o, B->O=|b-o|,
# with an equilateral metric when equal, so no distinct coincident points.
transport_checks = 0
sharp = []
for b,o in [(1,1),(2,1),(4,1),(4,2),(1,2),(1,4)]:
    c = ((0,b,o),(b,0,abs(b-o) or b),(o,abs(b-o) or b,0))
    for source in compositions(6,3):
        p = F(source[1]+source[2],6)
        for rows in product(*(list(compositions(count,3)) for count in source)):
            cost = sum(F(rows[i][j],6)*c[i][j] for i in range(3) for j in range(3))
            qbad = sum(F(rows[i][1],6) for i in range(3))
            qoutside = sum(F(rows[i][2],6) for i in range(3))
            eps = p+cost/b
            release_lower = 1-p-cost/o
            assert 1-qoutside >= release_lower
            if eps <= min(1,F(o,b)) and release_lower > 0:
                assert qbad/(1-qoutside) <= eps
                transport_checks += 1
    for p in [F(0),F(1,100),F(1,10)]:
        for rho in [F(0),F(1,100),F(1,10)]:
            eps = p+rho/b
            if eps <= min(1,F(o,b)) and 1-p-rho/o > 0:
                # Source at G,B; move rho/b protected mass to B.
                assert rho/b <= 1-p
                assert (rho/b)*b == rho
                sharp.append(dict(b=b,o=o,p=str(p),rho=str(rho),risk=str(eps)))

result = dict(status='PASS',classification='DEVELOPMENT; finite exact screens',
              source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              elapsed_ns=perf_counter_ns()-start,envelope_equalities=envelopes,
              conditional_transport_checks=transport_checks,sharp_receipt_witnesses=sharp,
              calibration=dict(N=n,certified=n-unresolved,p0='3/100',
                  exact_numerator=str(alpha.numerator),exact_denominator=str(alpha.denominator),
                  decimal_alpha=decimal_alpha,below_005=True),
              example=dict(joint_bound='13/100',release_floor='47/100',
                  separate_ratio='13/47',relative_bound_reduction='53/100',
                  unresolved=30,observed_error_reduction=None,computation_saving=None))
OUT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in
                 ('sharp_receipt_witnesses','calibration')},indent=2))
print('Exact calibration failure upper:',decimal_alpha)
