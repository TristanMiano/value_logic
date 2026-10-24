"""One noncommuting second-block screen; DEVELOPMENT, Codex (GPT-6)."""
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter_ns
import hashlib
import json
import platform
from checker_audit import adj_inverse, mm, transpose, plus, eye, det, encode

HERE=Path(__file__).resolve().parent
OUT=HERE/'second_result.json'
if OUT.exists():
    raise SystemExit('Refusing to overwrite an observed result.')
start=perf_counter_ns()
scale=lambda a,s:[[s*v for v in row] for row in a]
dot=lambda a,b:mm(transpose(a),b)[0][0]
outer=lambda a,b:mm(a,transpose(b))
def pd(a):
    return a==transpose(a) and all(det([row[:i] for row in a[:i]])>0 for i in range(1,len(a)+1))

C=[[F(1,4),F(0)],[F(0),F(1,2)]]
W=eye(2)+[[F(0),F(0)],[F(0),F(0)]]
R=C+[[F(1,4),F(1,16)],[F(0),F(1,4)]]
Q=mm(transpose(R),R)
T=plus(C,Q,-1)
P=plus(Q,mm(C,C),-1)
assert pd(C) and pd(plus(eye(2),C,-1)) and pd(P) and pd(T)
assert mm(C,Q)!=mm(Q,C)
alpha=[[F(1)],[F(0)]]
A=plus(scale(C,2),Q)  # E=t=1, a=2, d=-1.
c=mm(adj_inverse(C),mm(A,alpha))
assert c==[[F(5,2)],[F(1,32)]]
norm=dot(c,c)
v=mm(W,c)
w=mm(R,alpha)
m=dot(alpha,mm(Q,alpha))
q=dot(alpha,mm(T,alpha))
assert m==q==F(1,8)
lower=dot(c,mm(C,alpha))/norm
assert lower==F(640,6401) and lower>F(49,500)
old_s=dot(c,mm(C,c))/norm
old_m=dot(c,mm(mm(C,C),c))/norm
# C-only lower endpoint is its cap: m0/s <= 1/2 < (1+h)/(2+h).
assert old_m<=old_s/2
# sqrt(5)>2236/1000, so this rational upper enclosure of the
# C-only sharp lower endpoint is already below the chosen threshold.
root_low=F(559,250)
assert root_low**2<5
core_lower_upper=old_s*(3-root_low)/2
assert core_lower_upper<F(49,500)

old_action=plus(W,R,-1)
base_gram=mm(mm(old_action,adj_inverse(T)),transpose(old_action))
projector=plus(eye(4),mm(mm(R,adj_inverse(Q)),transpose(R)),-1)
assert mm(projector,projector)==projector
assert mm(projector,R)==[[F(0),F(0)] for _ in range(4)]
mx=mm(old_action,alpha)
cross=scale(plus(outer(mx,w),outer(w,mx)),1/m)
delta_gram=scale(outer(w,w),1/m)
b=plus(v,plus(scale(mm(W,alpha),2),w),-1)
assert mm(transpose(R),b)==[[F(0)],[F(0)]]
assert dot(b,b)>0
records=[]
previous=F(2)
for L in (1,4,16,64):
    gram=plus(base_gram,scale(projector,F(L*L)))
    old_inverse=adj_inverse(plus(eye(4),gram))
    assert mm(old_inverse,W)==R
    edited=plus(plus(gram,cross),delta_gram)
    normal=plus(eye(4),edited)
    assert pd(normal)
    assert mm(normal,w)==plus(v,b,-1)
    inverse=adj_inverse(normal)
    value=dot(v,mm(inverse,v))/norm
    gap=value-lower
    exact_gap=dot(b,mm(inverse,b))/norm
    envelope=dot(b,b)/(norm*L*L)
    assert 0<gap==exact_gap<envelope
    assert value<previous
    previous=value
    records.append(dict(L=L,value=str(value),gap=str(gap),
                        gap_upper=str(envelope),source_gram=encode(gram),
                        edited_gram=encode(edited)))
record=dict(status='PASS',C=encode(C),Q=encode(Q),R=encode(R),
            unnormalized_c=encode(c),target_norm_squared=str(norm),
            lower_infimum=str(lower),threshold='49/500',
            core_lower_upper_enclosure=str(core_lower_upper),cases=records,
            elapsed_ns=perf_counter_ns()-start,python=platform.python_version(),
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            helper_sha256=hashlib.sha256((HERE/'checker_audit.py').read_bytes()).hexdigest(),
            scope='One noncommuting C,Q example and four exact members of a derived limiting sequence; realization and sharpness use second_block.md.')
OUT.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(status=record['status'],lower=str(lower),
                     values=[float(F(r['value'])) for r in records],
                     elapsed_ns=record['elapsed_ns'])))
