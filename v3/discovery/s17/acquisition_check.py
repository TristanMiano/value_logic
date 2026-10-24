"""One exact acquisition-to-certificate check; DEVELOPMENT, Codex (GPT-6)."""
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter_ns
import hashlib
import json
import platform
from checker_audit import mm, transpose, plus, eye, encode, checker, CHECKER

HERE=Path(__file__).resolve().parent
OUT=HERE/'acquisition_result.json'
if OUT.exists():
    raise SystemExit('Refusing to overwrite an observed result.')
start=perf_counter_ns()
norm2=lambda x:mm(transpose(x),x)[0][0]
M=[[F(40),F(0),F(0)],[F(0),F(1,3),F(0)],[F(0),F(0),F(40)]]
queries=[]
# Prospective candidates: unregularized first-coordinate fit and rounded dual;
# exact second-coordinate ridge solution. No inverse is called in acquisition.
for name,z in [('e1',(1,0)),('e2',(0,1)),('e1+e2',(1,1))]:
    v=[[F(z[0])],[F(z[1])],[F(0)]]
    x=[[F(z[0],40)],[F(3*z[1],10)],[F(0)]]
    w=[[F(z[0],1600)],[F(9*z[1],10)],[F(0)]]
    Mx=mm(M,x)
    Mtw=mm(transpose(M),w)
    upper=norm2(plus(v,Mx,-1))+norm2(x)
    lower=2*mm(transpose(v),w)[0][0]-norm2(w)-norm2(Mtw)
    exact=F(z[0]**2,1601)+F(9*z[1]**2,10)  # Audit only, not used by adapter.
    assert lower<=exact<=upper
    queries.append(dict(name=name,z=list(z),x=encode(x),w=encode(w),
                        lower=str(lower),upper=str(upper),exact_audit=str(exact)))
mid=[(F(q['lower'])+F(q['upper']))/2 for q in queries]
err=[(F(q['upper'])-F(q['lower']))/2 for q in queries]
Chat=[[mid[0],(mid[2]-mid[0]-mid[1])/2],
      [(mid[2]-mid[0]-mid[1])/2,mid[1]]]
b12=sum(err,F(0))/2
delta=max(err[0]+b12,err[1]+b12)
assert delta==F(1,2560000)
rad=[[delta*F(i==j) for j in range(2)] for i in range(2)]
receipt=dict(schema='response-block-v1',source_id='s17-primal-dual-acquisition',
             dimension=2,C_minus=encode(plus(Chat,rad,-1)),
             C_plus=encode(plus(Chat,rad)),V=[['1/2','1/2'],['1/2','1/2']],
             edit_squared='9',t_lower='10',t_upper='100',threshold='3/5')
result=checker.verify(receipt)
assert result['verdict']=='below' and F(result['upper'])<F(3,5)
record=dict(status='PASS',source=encode(M),queries=queries,
            midpoint=encode(Chat),half_width=str(delta),receipt=receipt,result=result,
            acquisition_matvec_calls=6,acquisition_inverse_calls=0,
            elapsed_ns=perf_counter_ns()-start,python=platform.python_version(),
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            helper_sha256=hashlib.sha256((HERE/'checker_audit.py').read_bytes()).hexdigest(),
            checker_sha256=hashlib.sha256(CHECKER.read_bytes()).hexdigest(),
            scope='One constructed exact acquisition pipeline; counts are not an advantage over a strong solver or a complete price.')
OUT.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(status=record['status'],half_width=str(delta),
                     upper=result['upper'],upper_decimal=float(F(result['upper'])),
                     elapsed_ns=record['elapsed_ns'])))
