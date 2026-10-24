"""Exact algebra and coefficient enclosures for the all-radius diameter.

Codex (GPT-6), DEVELOPMENT. Five rational radii; symbolic identities are
checked before any decimal display. No SDP or random numerical screens.
"""
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter_ns
import hashlib
import json
import platform
import sympy as sy

HERE=Path(__file__).resolve().parent
OUT=HERE/'pair_radius_result.json'
if OUT.exists():
    raise SystemExit('Refusing to overwrite observed evidence.')
start=perf_counter_ns()
a,e,q,z,E=sy.symbols('a e q z E', positive=True)
P=q**3+(1+2*E)*q**2-(1+8*E+3*E**2)*q-(1+E)**2
k=1+a*e-a*a
l=a*a+a*e-1
D=(1+(a-e)**2)*(1+(a+e)**2)
g=4*a*e*(1+a*a)/D
expressions={
 'spectral_stationarity':l*(1+(a-e)**2)**2-k*(1+(a+e)**2)**2-2*P.subs({q:a*a,E:e*e}),
 'scalar_derivative':sy.diff(g,a)*D**2/(4*e)+P.subs({q:a*a,E:e*e}),
 'at_one':P.subs(q,1)+8*E+4*E**2,
 'at_E':P.subs(q,E)+8*E**2+3*E+1,
 'positive_boundary':P.subs({q:z,E:(z-1)**2/z})-(z-1)*(z+1)**2/z**2,
}
identities={name:sy.cancel(value)==0 for name,value in expressions.items()}
assert all(identities.values())

def polynomial(q,E):
    return q**3+(1+2*E)*q*q-(1+8*E+3*E*E)*q-(1+E)**2

rows=[]
for radius in map(F,('1/10','1/2','1','2','10')):
    energy=radius*radius
    qlo,qhi=max(F(1),energy),energy+2
    assert polynomial(qlo,energy)<0<polynomial(qhi,energy)
    for _ in range(160):
        mid=(qlo+qhi)/2
        if polynomial(mid,energy)<0:
            qlo=mid
        else:
            qhi=mid
    alo,ahi=max(F(1),radius),radius+1
    for _ in range(120):
        mid=(alo+ahi)/2
        if mid*mid<qlo:
            alo=mid
        elif mid*mid>qhi:
            ahi=mid
        else:
            break
    assert alo*alo<qlo<qhi<ahi*ahi
    assert 1+alo*radius-ahi*ahi>0
    assert alo*alo+alo*radius-1>0
    numerator=lambda x:4*x*radius*(1+x*x)
    denominator=lambda x:(1+(x-radius)**2)*(1+(x+radius)**2)
    glo=numerator(alo)/denominator(ahi)
    ghi=numerator(ahi)/denominator(alo)
    assert 0<ghi-glo<F(1,10**25)
    rows.append(dict(radius=str(radius),q_interval=list(map(str,(qlo,qhi))),
                     a_interval=list(map(str,(alo,ahi))),
                     coefficient_interval=list(map(str,(glo,ghi))),
                     coefficient_decimal=float((glo+ghi)/2),
                     interval_width=str(ghi-glo)))

# A compact exact ordinary certificate for e=1. Rational t,u are obtained
# from a rational approximation to the scalar witness. A quadratic with
# nonpositive discriminant proves g-R(lambda)>=0 for every real lambda.
unit=rows[2]
alo,ahi=map(F,unit['a_interval'])
candidate_a=F(int((alo+ahi)/2*10**10),10**10)
candidate_g=F(int(F(unit['coefficient_interval'][1])*10**12)+1,10**12)
ka=1+candidate_a-candidate_a*candidate_a
la=candidate_a*candidate_a+candidate_a-1
aa,bb=candidate_a-1,candidate_a+1
h2=candidate_g*ka*la
h1=candidate_g*(aa*la+bb*ka)-candidate_a*(la-ka)
h0=candidate_g*aa*bb-candidate_a*(bb-aa)
disc=h1*h1-4*h2*h0
assert ka>0 and la>0 and h2>0 and disc<0
previous=json.loads((HERE/'relative_pair_result.json').read_text())
assert candidate_g<F(previous['coefficient'])
assert F(previous['scalar_witness']['ratio'])<F(unit['coefficient_interval'][0])
record=dict(status='PASS',identities=identities,radii=rows,
            unit_rational_certificate=dict(a=str(candidate_a),coefficient=str(candidate_g),
              coefficient_decimal=float(candidate_g),quadratic=list(map(str,(h0,h1,h2))),
              discriminant=str(disc),previous_coefficient=previous['coefficient']),
            elapsed_ns=perf_counter_ns()-start,
            versions=dict(python=platform.python_version(),sympy=sy.__version__),
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            dependency_sha256=hashlib.sha256((HERE/'relative_pair_result.json').read_bytes()).hexdigest(),
            scope='Exact symbolic identities, five rational enclosures, and one rational spectral certificate; not independent confirmation or novelty evidence.')
OUT.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(status='PASS',identities=identities,
      coefficients=[(row['radius'],row['coefficient_decimal']) for row in rows],
      rational_coefficient=str(candidate_g),elapsed_ns=record['elapsed_ns'])))
