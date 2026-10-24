"""Exact small DEVELOPMENT checks; Codex (GPT-6), 2026-10-24.
Question: do the transport identity, exact reuse ratio and approximate-solve
bound survive rational boundary/noncommuting examples? No timing advantage.
"""
from fractions import Fraction as F
from itertools import product
import hashlib
import json
from pathlib import Path
import platform
import time

t0 = time.perf_counter_ns()
def add(A, B): return [[a+b for a,b in zip(ar,br)] for ar,br in zip(A,B)]
def sub(A, B): return add(A, scale(B, -1))
def scale(A, s): return [[a*s for a in row] for row in A]
def tr(A): return [list(row) for row in zip(*A)]
def mul(A, B): return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def sq(v): return sum(row[0]**2 for row in v)
I = [[F(1),F(0)],[F(0),F(1)]]
def inv(A):
    a,b = A[0]; c,d = A[1]; det = a*d-b*c
    assert det > 0
    return [[d/det,-b/det],[-c/det,a/det]]
def optimum(M, y):
    G = add(I,mul(M,tr(M)))
    x = mul(inv(G),mul(M,y))
    r = sub(y,mul(tr(M),x))
    return x, sq(r)+sq(x), G, r
def objective(M,y,x): return sq(sub(y,mul(tr(M),x)))+sq(x)
def energy(v,G): return mul(tr(v),mul(G,v))[0][0]

vals = [F(-2),F(0),F(1,3),F(1),F(3)]
edits = [[[F(1),F(0)],[F(0),F(0)]],
         [[F(0),F(-1)],[F(1),F(0)]],
         [[F(9,25),F(12,25)],[F(12,25),F(16,25)]]]
ys = [[[F(1)],[F(0)]], [[F(1)],[F(2)]], [[F(0)],[F(0)]]]
offsets = [[[F(0)],[F(0)]], [[F(1,10)],[F(-1,5)]], [[F(2)],[F(1)]]]
counts = {"identities":0,"mean_bounds":0,"exact_reuse":0,"approx_reuse":0,"zero_data":0}
largest_exact = F(0)
for a,b,off in product(vals,vals,[F(0),F(1,2)]):
    M = [[a,off],[F(0),b]]
    for e, direction,y in product([F(0),F(1,10),F(1),F(3)],edits,ys):
        D = scale(direction,e); N = add(M,D); E=e*e; c=1+E/2; d2=E*(1+E/4)
        old,rM,GM,residual = optimum(M,y)
        new,rN,GN,_ = optimum(N,y)
        difference=sub(new,old)
        rhs=mul(inv(GN),sub(mul(D,residual),mul(N,mul(tr(D),old))))
        assert difference == rhs
        counts["identities"]+=1
        excess=energy(difference,GN)
        assert excess <= E*rM
        counts["mean_bounds"]+=1
        assert objective(N,y,old) == rN+excess <= c*c*rN
        counts["exact_reuse"]+=1
        if rN:
            largest_exact=max(largest_exact,(rN+excess)/(c*c*rN))
        else:
            counts["zero_data"]+=1
        for shift in offsets:
            x=add(old,shift)
            old_gap=objective(M,y,x)-rM
            assert old_gap == energy(shift,GM) >= 0
            if not rM:
                continue # Relative old-gap premise does not cover nonzero x here.
            delta=old_gap/rM
            ratio=objective(N,y,x)/rN
            base=c*c*(1+delta)+d2*delta
            positive=max(ratio-base,F(0))
            assert positive*positive <= 4*c*c*d2*delta*(1+delta)
            counts["approx_reuse"]+=1

# A noncommuting family attains the exact-solve constant, not only a limit.
sharp=[]
for e in [F(1,10),F(1),F(3)]:
    N=add(I,scale(edits[1],e)); y=ys[1]
    old,_,_,_=optimum(I,y); _,rN,_,_=optimum(N,y)
    ratio=objective(N,y,old)/rN
    assert ratio == (1+e*e/2)**2
    sharp.append({"e":str(e),"ratio":str(ratio)})

# The component-covariance-only shortcut fails for the symmetric model mixture.
e=F(1); y=F(30)
mixture_variance=1/(1+e*e)+e*e*y*y/(1+e*e)**2
assert mixture_variance > 1
assert mixture_variance <= (1+e*e*y*y)/(1+e*e)
result={"status":"PASS","counts":counts,"sharp_examples":sharp,
        "largest_normalized_exact_ratio":str(largest_exact),
        "mixture_variance":str(mixture_variance),
        "elapsed_ns":time.perf_counter_ns()-t0,"python":platform.python_version(),
        "source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_suffix(".json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
print(json.dumps(result))
