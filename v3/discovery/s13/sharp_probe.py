"""Exact finite checks of two-value moment certificates; DEVELOPMENT, GPT-6."""
from fractions import Fraction as F
from itertools import combinations
import hashlib, json, platform, time
from pathlib import Path

start=time.perf_counter_ns()
def d(r,z): return r+(1-r)*z
def h(r,z): return z/d(r,z)
laws=[]
for x,y in combinations([F(k,10) for k in range(1,11)],2):
    for w in (F(1,5),F(1,2),F(4,5)):
        laws.append([(x,w),(y,1-w)])
for x,y,z in combinations([F(k,10) for k in range(1,11)],3):
    laws.append([(x,F(2,5)),(y,F(1,5)),(z,F(2,5))])
identities=intervals=attainments=0
for law in laws:
    mu=sum(z*w for z,w in law)
    for s in (F(3,2),F(2),F(4)):
        nu=sum(w*h(s,z) for z,w in law)
        a=s*(mu-nu)/((s-1)*(1-nu))
        b=(s-mu/nu)/(s-1)
        assert 0<=a<=mu<=b<=1
        assert mu/b*h(s,b)==nu
        assert (1-mu)/(1-a)*h(s,a)+(mu-a)/(1-a)==nu
        for r in (F(1,4),F(1,2),F(1),F(3,2),F(3),F(8)):
            actual=sum(w*h(r,z) for z,w in law)
            lower=mu/d(r,b)
            upper=1-r*(1-mu)/d(r,a)
            assert min(lower,upper)<=actual<=max(lower,upper)
            assert (upper-lower)*(r-s)*(r-1)>=0
            intervals+=1
            Bb=(s-r)/((s-1)*d(r,b)**2)
            Cb=(r-1)*d(s,b)**2/((s-1)*d(r,b)**2)
            Ba=r*(s-r)/((s-1)*d(r,a)**2)
            Ca=r*(r-1)*d(s,a)**2/(s*(s-1)*d(r,a)**2)
            Aa=1-Ba-Ca
            assert Bb*mu+Cb*nu==lower
            assert Aa+Ba*mu+Ca*nu==upper
            attainments+=2
            for z in (F(0),a,F(1,2),b,F(1)):
                assert h(r,z)-Bb*z-Cb*h(s,z)==(r-s)*(r-1)*z*(z-b)**2/(d(r,b)**2*d(r,z)*d(s,z))
                assert h(r,z)-Aa-Ba*z-Ca*h(s,z)==r*(r-s)*(r-1)*(z-1)*(z-a)**2/(d(r,a)**2*d(r,z)*d(s,z))
                identities+=2
assert F(141,280)<F(113,224)<F(95,188)<F(51,100)<F(47,78)
print(json.dumps(dict(contributor="Codex (GPT-6)",status="PASS",
    scope="Finite exact development, not independent confirmation",
    laws=len(laws),interval_checks=intervals,endpoint_checks=attainments,
    rational_identities=identities,elapsed_ns=time.perf_counter_ns()-start,
    python=platform.python_version(),
    script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2))
