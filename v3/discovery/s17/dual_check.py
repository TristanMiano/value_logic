"""Focused exact screen of new Gram-dual identities; DEVELOPMENT, Codex (GPT-6)."""
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter_ns
import hashlib
import json
import platform
from checker_audit import adj_inverse, mm, transpose, plus, eye, encode

HERE = Path(__file__).resolve().parent
OUT = HERE/'dual_result.json'
if OUT.exists():
    raise SystemExit('Refusing to overwrite an observed result.')
start = perf_counter_ns()
scale = lambda a,s: [[s*v for v in row] for row in a]
dot = lambda a,b: mm(transpose(a),b)[0][0]
norm2 = lambda a: dot(a,a)
M = [[F(1),F(2)], [F(2),F(-1)], [F(1),F(1)]]
W = [[F(1),F(0)], [F(0),F(1)], [F(0),F(0)]]
c = [[F(3,5)],[F(4,5)]]
v = mm(W,c)
left = [[F(3,5)],[F(4,5)],[F(0)]]
right = [[F(5,13),F(12,13)]]
Delta = scale(mm(left,right),F(1,10))
assert norm2(left) == 1 and mm(right,transpose(right)) == [[F(1)]]
N = plus(M,Delta)
S = adj_inverse(plus(eye(3),mm(M,transpose(M))))
SN = adj_inverse(plus(eye(3),mm(N,transpose(N))))
R = mm(S,W)
X = mm(transpose(M),R)
C = mm(transpose(W),R)
Q = mm(transpose(R),R)
P = plus(Q,mm(C,C),-1)
r = mm(SN,v)
x = mm(transpose(N),r)
u = mm(Delta,x)
z = mm(transpose(Delta),r)
f = dot(v,r)
assert f == norm2(r)+norm2(x)
records = []
for E,t,eta in ((F(1,100),F(1,5),F(1,20)), (F(1,2),F(1),F(1))):
    assert E >= F(1,100)
    a = 1+t
    d = t-E-E/t
    assert d >= 0
    B = plus(scale(eye(2),a),scale(C,-d))
    alpha = mm(adj_inverse(B),c)
    w,b = mm(R,alpha),mm(X,alpha)
    lower = dot(c,mm(C,alpha))
    lower_terms = [norm2(plus(r,w,-1)), norm2(plus(x,scale(b,a),-1))/a,
                   t*norm2(plus(u,scale(w,a*E/t),-1))/(a*E),
                   (t/a)*(norm2(x)-norm2(u)/E), d*dot(alpha,mm(P,alpha))]
    assert all(q >= 0 for q in lower_terms)
    assert sum(lower_terms) == f-lower
    a = 1+eta
    b0 = 1+E+E/eta
    kappa = b0-a
    assert kappa >= 0
    B = plus(scale(eye(2),a),scale(C,kappa))
    alpha = scale(mm(adj_inverse(B),c),a)
    b = mm(X,alpha)
    q = plus(mm(W,plus(c,alpha,-1)),mm(R,alpha))
    upper_t = E*(1+eta)/eta
    upper_d = upper_t-E-E/upper_t
    upper = (1+upper_t)*dot(c,mm(C,mm(adj_inverse(plus(eye(2),scale(C,upper_d))),c)))
    upper_terms = [norm2(plus(x,b,-1)), norm2(plus(r,scale(q,a),-1))/a,
                   eta*norm2(plus(z,scale(b,a*E/eta)))/(a*E),
                   (eta/a)*(norm2(r)-norm2(z)/E), kappa*dot(alpha,mm(P,alpha))]
    assert all(q >= 0 for q in upper_terms)
    assert sum(upper_terms) == upper-f
    records.append(dict(E=str(E),t=str(t),eta=str(eta),upper_t=str(upper_t),
                        d=str(d),kappa=str(kappa),lower=str(lower),upper=str(upper),
                        lower_terms=list(map(str,lower_terms)),
                        upper_terms=list(map(str,upper_terms))))
record = dict(status='PASS',source=encode(M),delta=encode(Delta),W=encode(W),
              c=encode(c),C=encode(C),P=encode(P),actual=str(f),cases=records,
              elapsed_ns=perf_counter_ns()-start,python=platform.python_version(),
              source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              helper_sha256=hashlib.sha256((HERE/'checker_audit.py').read_bytes()).hexdigest(),
              scope='Two exact source cases, four square identities; finite development check only.')
OUT.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(status='PASS',identities=4,elapsed_ns=record['elapsed_ns'])))
