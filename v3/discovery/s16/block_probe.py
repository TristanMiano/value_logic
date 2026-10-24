"""Meaningful exact checks of the conditional block certificate, not a proof of its theorem."""
import copy
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import platform
from time import perf_counter_ns
from block_check import verify,InvalidCertificate,positive,add,identity,mul,inverse,weighted_trace

here=Path(__file__).resolve().parent
out=here/'block_probe.json'
assert not out.exists(),'Preserve original evidence.'
start=perf_counter_ns()
data=json.loads((here/'block_receipt.json').read_text())
rounded=verify(data)
assert rounded['verdict']=='below'
assert F(rounded['lower'])>F(461,1000) and F(rounded['upper'])<F(538,1000)
assert F(rounded['upper'])-F(rounded['lower'])<F(767,10000)
exact=copy.deepcopy(data)
exact['C_minus']=exact['C_plus']=[['1/10','0'],['0','9/10']]
answer=verify(exact)
assert F(answer['upper'])==F(867127945275459,1611861132384100)
assert F(answer['lower'])==F(618573873750,1340748094907)

# A different, non-diagonal true response inside the very same rounded receipt.
trueC=[[F(100003,1000000),F(4,1000000)],[F(4,1000000),F(899997,1000000)]]
lo=[[F(x) for x in row] for row in data['C_minus']]
hi=[[F(x) for x in row] for row in data['C_plus']]
assert positive(add(trueC,lo,-1)) and positive(add(hi,trueC,-1))
inside=copy.deepcopy(data)
inside['C_minus']=inside['C_plus']=[[str(x) for x in row] for row in trueC]
inside_result=verify(inside)
assert F(rounded['lower'])<=F(inside_result['lower'])
assert F(inside_result['upper'])<=F(rounded['upper'])

# Exact rectangular edited sources independently exercise the reported interval.
source_cases=0
for n,m in [(1,1),(2,2),(2,3),(3,2)]:
    for seed in range(1,5):
        M=[[F((i+2)*(j+seed+1)%7-3,3) for j in range(m)] for i in range(n)]
        # Add enough diagonal information to make C strictly below I when possible.
        if n>m: continue # This checker version deliberately excludes an eigenvalue1.
        for i in range(n): M[i][i]+=2
        def gram(A):
            return [[sum((A[i][k]*A[j][k] for k in range(m)),F(0)) for j in range(n)] for i in range(n)]
        C=inverse(add(identity(n),gram(M)))
        if not positive(add(identity(n),C,-1),True): continue
        edit=[[F(0) for _ in range(m)] for _ in range(n)]
        edit[0][0]=F(1,10)
        N=[[a+b for a,b in zip(row,other)] for row,other in zip(M,edit)]
        SN=inverse(add(identity(n),gram(N)))
        V=[[F(i==j,n) for j in range(n)] for i in range(n)]
        case=dict(schema='response-block-v1',source_id=f'exact-source-{n}-{m}-{seed}',dimension=n,
                  C_minus=[[str(x) for x in row] for row in C],C_plus=[[str(x) for x in row] for row in C],
                  V=[[str(x) for x in row] for row in V],edit_squared='1/100',
                  t_lower='1/5',t_upper='1/5',threshold='1/2')
        result=verify(case)
        actual=weighted_trace(V,SN)
        assert F(result['lower'])<=actual<=F(result['upper'])
        source_cases+=1

# Zero edits, equality abstention, and the necessary scalar cap.
zero=copy.deepcopy(exact); zero.update(edit_squared='0',t_lower='0',t_upper='0',threshold='1/2')
assert verify(zero)['verdict']=='unresolved'
large=copy.deepcopy(exact); large.update(edit_squared='4',t_lower='5',t_upper='5',threshold='1')
assert verify(large)['upper']=='1' and verify(large)['verdict']=='unresolved'

invalid=[]
def rejected(name,change):
    obj=copy.deepcopy(data); change(obj)
    try: verify(obj)
    except InvalidCertificate: invalid.append(name)
    else: raise AssertionError(f'Accepted invalid certificate: {name}')
rejected('signed task',lambda o:o.update(V=[['2','0'],['0','-1']]))
rejected('non-symmetric task',lambda o:o.update(V=[['1/2','1/2'],['0','1/2']]))
rejected('zero pivot with nonzero off diagonal',lambda o:o.update(V=[['0','1'],['1','1']]))
rejected('bad cap',lambda o:o.update(t_upper='1/100'))
rejected('negative edit',lambda o:o.update(edit_squared='-1'))
rejected('reversed bounds',lambda o:o.update(C_minus=o['C_plus'],C_plus=o['C_minus']))
rejected('float input',lambda o:o.update(edit_squared=.01))
rejected('nonpositive lower',lambda o:o.update(C_minus=[['0','0'],['0','9/10']]))
rejected('unit upper endpoint',lambda o:o.update(C_plus=[['1','0'],['0','9/10']]))
rejected('unbounded dimension',lambda o:o.update(dimension=17))
rejected('extra field',lambda o:o.update(trust_me=True))
rejected('non-unit trace',lambda o:o.update(V=[['1','0'],['0','1']]))
result=dict(status='PASS',rounded_result=rounded,exact_result=answer,inside_result=inside_result,
            exact_source_cases=source_cases,rejected_cases=invalid,
            elapsed_ns=perf_counter_ns()-start,python=platform.python_version(),
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            checker_sha256=hashlib.sha256((here/'block_check.py').read_bytes()).hexdigest(),
            scope='Conditional exact arithmetic and finite tests, not source-warrant verification or independent confirmation.')
out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
