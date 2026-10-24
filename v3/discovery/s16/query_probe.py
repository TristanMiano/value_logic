"""Exact DEVELOPMENT screen for task-directed old-value queries; Codex (GPT-6)."""
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter_ns
import hashlib
import json
import platform
from block_check import add,identity,inverse,mul,positive

here=Path(__file__).resolve().parent
out=here/'query_probe.json'
assert not out.exists(),'Preserve original evidence.'
start=perf_counter_ns()
def dot(x,y): return sum((a*b for a,b in zip(x,y)),F(0))
def mv(A,x): return [dot(row,x) for row in A]
def norm2(x): return dot(x,x)
def minus(x,y): return [a-b for a,b in zip(x,y)]
def scale(a,x): return [a*z for z in x]
def bound(c,z,qlo,qhi,E,t):
    assert t>0 and t*t>=E*(1+t)
    a=1+t; d=t-E-E/t
    assert d>0 and 0<=qlo<=qhi<=norm2(z)
    lower=a*qlo-norm2(minus(c,scale(a,z)))/d
    upper=a*qhi+a*norm2(minus(c,z))/d
    return max(F(0),lower),min(norm2(c),upper)

C=[[F(1,10),F(0)],[F(0),F(9,10)]]
forecast=[[F(12,100),F(3,100)],[F(3,100),F(85,100)]]
c=[F(3,5),F(4,5)]; E=F(1,100); t=F(1,4); a=1+t; d=t-E-E/t
I=identity(2)
zU=mv(inverse(add(I,forecast,d)),c)
zL=mv(inverse(add([[a*z for z in row] for row in I],forecast,-d)),c)
oracle_calls=[]
def old_value(z):
    oracle_calls.append([str(x) for x in z])
    return dot(z,mv(C,z))
qU=old_value(zU); qL=old_value(zL)
error=F(1,100000)
upper=bound(c,zU,qU-error,qU+error,E,t)[1]
lower=bound(c,zL,qL-error,qL+error,E,t)[0]
assert lower>F(14,25) and upper<F(2,3)
assert len(oracle_calls)==2

# Exact full-block identities and quadratic proposal defects.
AU=add(I,C,d); AL=add([[a*z for z in row] for row in I],C,-d)
zUstar=mv(inverse(AU),c); zLstar=mv(inverse(AL),c)
U=[[a*z for z in row] for row in mul(C,inverse(AU))]
L=mul(C,inverse(AL))
full_upper=dot(c,mv(U,c)); full_lower=dot(c,mv(L,c))
assert bound(c,zU,qU,qU,E,t)[1]-full_upper==a/d*dot(minus(zU,zUstar),mv(AU,minus(zU,zUstar)))
assert full_lower-bound(c,zL,qL,qL,E,t)[0]==a/d*dot(minus(zL,zLstar),mv(AL,minus(zL,zLstar)))

# One explicitly edited source: its Frobenius budget warrants the operator budget.
M=[[F(3),F(0)],[F(0),F(1,3)]]
edit=[[F(6,100),F(-3,100)],[F(2,100),F(5,100)]]
assert sum(z*z for row in edit for z in row)<=E
N=add(M,edit)
NT=[list(row) for row in zip(*N)]
SN=inverse(add(I,mul(N,NT)))
actual=dot(c,mv(SN,c))
assert lower<=actual<=upper

# Every arbitrary proposed vector remains sound; no forecast PSD premise is used.
checks=0
for i in range(-4,5):
    for j in range(-4,5):
        z=[F(i,3),F(j,4)]
        q=dot(z,mv(C,z))
        lo,hi=bound(c,z,q,q,E,t)
        assert lo<=full_lower<=full_upper<=hi
        assert lo<=actual<=hi
        checks+=1
result=dict(status='PASS',source='M=diag(3,1/3)',forecast=[[str(z) for z in row] for row in forecast],
            target=[str(z) for z in c],value_queries=oracle_calls,query_count=len(oracle_calls),
            interval_error=str(error),lower=str(lower),upper=str(upper),lower_float=float(lower),upper_float=float(upper),
            full_block_lower=str(full_lower),full_block_upper=str(full_upper),
            full_block_lower_float=float(full_lower),full_block_upper_float=float(full_upper),actual=str(actual),
            arbitrary_proposal_checks=checks,elapsed_ns=perf_counter_ns()-start,python=platform.python_version(),
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            helper_sha256=hashlib.sha256((here/'block_check.py').read_bytes()).hexdigest(),
            scope='Exact finite development example; old-query prices and forecast computation unmeasured; ordinary variational implementation ties.')
out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
