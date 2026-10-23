# Derived from channel_lp.py SHA256 7c288a07287dc66821f9e5cf3e472ac0d5d533823b1d6575e845bcc282bdea8a
"""Development LP for binary channels with depth<=5, followed by exact checks.

No solver optimality flag is treated as an exact certificate by itself.
"""
from fractions import Fraction as F
from itertools import combinations
import hashlib,json,platform,sys
from pathlib import Path
from time import perf_counter_ns
import numpy as np
import scipy
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

HERE=Path(__file__).resolve().parent
OUT=HERE/'weight_channel.json'
RAW=HERE/'weight_channel_raw.json'
assert not OUT.exists() and not RAW.exists(), 'Preserve exposed evidence.'
start=perf_counter_ns()
n,d=7,5
states=[]
for k in range(d+1):
    for bits in combinations(range(n),k):
        mask=sum(1<<i for i in bits)
        for a in range(1<<k):
            value=sum(((a>>j)&1)<<i for j,i in enumerate(bits))
            states.append((mask,value))
state_index={s:i for i,s in enumerate(states)}
variables=[]
for mask,value in states:
    variables.extend([(mask,value,'accept'),(mask,value,'reject')])
    if mask.bit_count()<d:
        variables.extend((mask,value,j) for j in range(n) if not (mask>>j)&1)
a_index=len(variables)
variables.append(('a',))
rows=[{} for _ in range(len(states)+128)]
rhs=[F(0) for _ in rows]
rhs[0]=F(1)
def add(row,col,val):
    rows[row][col]=rows[row].get(col,F(0))+val
for col,var in enumerate(variables[:-1]):
    mask,value,action=var
    add(state_index[(mask,value)],col,F(1))
    if isinstance(action,int):
        for bit in (0,1):
            child=(mask|(1<<action),value|(bit<<action))
            add(state_index[child],col,F(-1))
    elif action=='accept':
        for x in range(128):
            if x&mask==value:
                add(len(states)+x,col,F(1))
def syndrome(x):
    s=0
    for i in range(n):
        if (x>>i)&1:
            s^=i+1
    return s
def weight(x):
    s=syndrome(x)
    c=x if s==0 else x^(1<<(s-1))
    return c.bit_count()
for x in range(128):
    row=len(states)+x
    add(row,a_index,F(-weight(x)))
    rhs[row]=F(0)
ii,jj,vv=[],[],[]
for i,row in enumerate(rows):
    for j,val in row.items():
        ii.append(i);jj.append(j);vv.append(float(val))
A=coo_matrix((vv,(ii,jj)),shape=(len(rows),len(variables))).tocsr()
c=np.zeros(len(variables));c[-1]=-1
res=linprog(c,A_eq=A,b_eq=[float(v) for v in rhs],bounds=(0,None),method='highs',
            options={'time_limit':45})
raw=dict(success=bool(res.success),status=int(res.status),message=res.message,
         source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         python=sys.version,numpy=np.__version__,scipy=scipy.__version__,platform=platform.platform(),
         elapsed_ns=perf_counter_ns()-start)
if res.x is not None:
    raw['primal']=res.x.tolist()
if res.eqlin.marginals is not None:
    raw['dual']=res.eqlin.marginals.tolist()
RAW.write_text(json.dumps(raw,separators=(',',':'))+'\n',encoding='utf-8')
assert res.success, res.message
primal=[F(float(v)).limit_denominator(1000000) for v in res.x]
dual=[F(float(v)).limit_denominator(1000000) for v in res.eqlin.marginals]
assert all(v>=0 for v in primal)
assert all(sum(val*primal[j] for j,val in row.items())==rhs[i]
           for i,row in enumerate(rows)), 'Rational primal not exact.'
at_y=[F(0) for _ in variables]
for i,row in enumerate(rows):
    for j,val in row.items():
        at_y[j]+=dual[i]*val
cost=[F(0) for _ in variables];cost[-1]=F(-1)
assert all(a<=b for a,b in zip(at_y,cost)), 'Rational dual infeasible.'
dual_value=sum(a*b for a,b in zip(rhs,dual))
assert dual_value==-primal[-1], 'Rational primal-dual gap.'
result=dict(status='PASS',classification='DEVELOPMENT; exact finite LP certificate',
            source_sha256=raw['source_sha256'],raw_sha256=hashlib.sha256(RAW.read_bytes()).hexdigest(),
            elapsed_ns=perf_counter_ns()-start,states=len(states),variables=len(variables),
            equations=len(rows),depth=d,a=str(primal[-1]),minimum_wrong_acceptance=str(3*primal[-1]),
            primal_nonzero=[dict(variable=list(variables[j]),value=str(v)) for j,v in enumerate(primal) if v],
            dual_nonzero=[dict(row=i,value=str(v)) for i,v in enumerate(dual) if v],
            exact_primal_feasible=True,exact_dual_feasible=True,exact_gap_zero=True,
            scope='Optimal depth-five channel with acceptance a*weight(Q(x)); count5/6 adapter.')
OUT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ('primal_nonzero','dual_nonzero')},indent=2))
