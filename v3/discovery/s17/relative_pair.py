"""Universal relative contrast certificate for two unit edits; DEVELOPMENT.

Codex (GPT-6). Numerical duals only propose coefficients. Three exact
projections remove the unbounded target-norm row. Seven predeclared shifts
are screened for exact positivity; all shift outcomes are preserved.
"""
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter_ns
import hashlib
import json
import platform

HERE=Path(__file__).resolve().parent
OUT=HERE/'relative_pair_result.json'
PROPOSAL=HERE/'paired_cert_result.json'
if OUT.exists():
    raise SystemExit('Refusing to overwrite observed evidence.')
start=perf_counter_ns()
proposal=json.loads(PROPOSAL.read_text())
y=list(map(F,proposal['multipliers']))
assert len(y)==17
y[0]=F(0)
y[1]=-y[3]-y[8]
y[4]=1-y[13]-y[14]
y[9]=-1-y[15]-y[16]

def form(*terms):
    out={}
    for sp,i,j,value in terms:
        key=(sp,min(i,j),max(i,j))
        out[key]=out.get(key,F(0))+F(value)
    return {key:v for key,v in out.items() if v}

def add(target,source,multiplier):
    for key,value in source.items():
        target[key]=target.get(key,F(0))+multiplier*value

# The target norm has no prescribed value. All nonzero right sides are s,
# the old ridge value, so the final constant multiplies s.
rows=[(form(('G',0,0,1)),F(0),'unused'),
      (form(('G',0,1,1)),F(1),'eq'),
      (form(('G',1,1,1),('H',0,0,1)),F(1),'eq')]
rs,us,xs,zs=[2,4],[3,5],[1,3],[2,4]
for r,u,x,z in zip(rs,us,xs,zs):
    rows += [(form(('G',1,0,1),('G',1,r,-1),('G',1,u,-1),('H',0,x,-1)),F(0),'eq'),
             (form(('G',0,r,1),('G',1,r,-1),('H',0,x,-1),('H',0,z,1)),F(0),'eq'),
             (form(('G',r,u,1),('H',x,z,-1)),F(0),'eq'),
             (form(('G',u,u,1),('H',x,x,-1)),F(0),'le'),
             (form(('H',z,z,1),('G',r,r,-1)),F(0),'le')]
for i in range(2):
    for j in range(2):
        rows.append((form(('G',rs[i],0,1),('G',rs[i],rs[j],-1),('G',rs[i],us[j],-1),
                          ('H',xs[i],xs[j],-1),('H',zs[i],xs[j],1)),F(0),'eq'))
slack={}
add(slack,form(('G',0,2,1),('G',0,4,-1)),F(-1))
constant=F(0)
for multiplier,(row,rhs,kind) in zip(y,rows):
    if kind=='le':
        assert multiplier>=0
    add(slack,row,multiplier)
    constant+=multiplier*rhs
assert all(value==0 for (sp,i,j),value in slack.items() if sp=='G' and i==0)

def matrix(space):
    out=[[F(0) for _ in range(5)] for _ in range(5)]
    offset=1 if space=='G' else 0
    for (sp,i,j),value in slack.items():
        if sp!=space or value==0:
            continue
        i-=offset; j-=offset
        assert i>=0 and j>=0
        if i==j:
            out[i][j]+=value
        else:
            out[i][j]+=value/2; out[j][i]+=value/2
    return out

def positivity(a,shift):
    a=[row[:] for row in a]
    for i in range(5):
        a[i][i]+=shift
    pivots=[]
    for k in range(5):
        pivot=a[k][k]
        pivots.append(str(pivot))
        if pivot<=0:
            return dict(positive=False,first_nonpositive=k,pivots=pivots)
        for i in range(k+1,5):
            for j in range(k+1,5):
                a[i][j]-=a[i][k]*a[k][j]/pivot
    return dict(positive=True,pivots=pivots)

SG,SH=matrix('G'),matrix('H')
trace_factor=F(23,2) # 1+4*a(1) < 1+4*(21/8)=23/2.
assert F(9,4)**2>5 # a(1)=(3+sqrt(5))/2 <21/8.
attempts=[]
for exponent in range(9,2,-1):
    shift=F(1,10**exponent)
    pg,ph=positivity(SG,shift),positivity(SH,shift)
    attempts.append(dict(shift=str(shift),output=pg,input=ph,
                         coefficient=str(constant+shift*trace_factor),
                         passed=pg['positive'] and ph['positive']))
valid=[row for row in attempts if row['passed']]
assert valid
chosen=valid[0]
coefficient=F(chosen['coefficient'])
assert coefficient<F(54,25)
# Scalar finite witness. For M=[a], N0=[a-1], N1=[a+1], the exact ratio is
# 4*a*(1+a*a)/(a**4+4). This is a lower witness, not the exact universal maximum.
a=F(63,40)
witness=4*a*(1+a*a)/(a**4+4)
assert F(21596,10000)<witness<coefficient
encode=lambda a:[[str(x) for x in row] for row in a]
record=dict(status='PASS',claim='For any finite real M and v and two edits of operator norm at most one, abs(F0-F1)<=(54/25)*F(M;v).',
            coefficient=str(coefficient),coefficient_decimal=float(coefficient),
            convenient_coefficient='54/25',unshifted_coefficient=str(constant),
            projected_multipliers=list(map(str,y)),output_slack=encode(SG),input_slack=encode(SH),
            trace_factor=str(trace_factor),shift_attempts=attempts,chosen=chosen,
            scalar_witness=dict(a=str(a),ratio=str(witness),ratio_decimal=float(witness)),
            elapsed_ns=perf_counter_ns()-start,python=platform.python_version(),
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            proposal_sha256=hashlib.sha256(PROPOSAL.read_bytes()).hexdigest(),
            scope='Exact universal certificate after deterministic coefficient construction; no proof of optimality or novelty, no independent confirmation.')
OUT.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(status='PASS',coefficient=float(coefficient),chosen_shift=chosen['shift'],
                     witness=float(witness),shift_outcomes=[(r['shift'],r['passed']) for r in attempts],
                     elapsed_ns=record['elapsed_ns'])))
