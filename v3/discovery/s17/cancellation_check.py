"""Exact constructed cancellation decision; DEVELOPMENT, Codex (GPT-6)."""
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter_ns
import hashlib
import json
import platform
from checker_audit import adj_inverse, mm, transpose, plus, eye, encode, det, checker, CHECKER

HERE=Path(__file__).resolve().parent
OUT=HERE/'cancellation_result.json'
if OUT.exists():
    raise SystemExit('Refusing to overwrite an observed result.')
start=perf_counter_ns()
scale=lambda A,s:[[s*v for v in row] for row in A]
norm2=lambda x:mm(transpose(x),x)[0][0]
M=[[F(40),F(0)],[F(0),F(1,3)]]
u=[[F(1)],[F(1)]]
C=adj_inverse(plus(eye(2),mm(M,transpose(M))))
w0=mm(C,u)
x0=mm(transpose(M),w0)
s=mm(transpose(u),w0)[0][0]/2
m=norm2(w0)/2
q=norm2(x0)/2
assert q==s-m>0
A0=scale(mm(plus(u,w0,-1),transpose(x0)),1/(2*q))
a=[[w0[1][0]],[-w0[0][0]]]
b=[[x0[1][0]],[-x0[0][0]]]
A=plus(A0,scale(mm(a,transpose(b)),F(1,10)))
assert mm(A,x0)==plus(u,w0,-1)
assert mm(transpose(A),w0)==x0
assert det(A)==q/5>0
AS=adj_inverse(plus(eye(2),mm(A,transpose(A))))
assert mm(AS,u)==w0
assert mm(transpose(A),mm(AS,u))==x0
Atu=mm(transpose(A),u)
Delta=scale(mm(u,transpose(Atu)),F(-1,2))
N=plus(A,Delta)
edit_squared=norm2(Atu)/2
assert edit_squared==(1-s)**2/q+q*(w0[1][0]-w0[0][0])**2/100
assert edit_squared<9
assert mm(transpose(N),u)==[[F(0)],[F(0)]]
NS=adj_inverse(plus(eye(2),mm(N,transpose(N))))
actual=mm(transpose(u),mm(NS,u))[0][0]/2
assert actual==1
width=F(1,10000)
receipt=dict(schema='response-block-v1',source_id='s17-anisotropic-constructed-example',
             dimension=2,C_minus=encode(plus(C,scale(eye(2),width),-1)),
             C_plus=encode(plus(C,scale(eye(2),width))),
             V=[['1/2','1/2'],['1/2','1/2']],edit_squared='9',
             t_lower='10',t_upper='100',threshold='3/5')
result=checker.verify(receipt)
assert result['verdict']=='below'
assert F(result['upper'])<F(3,5)
record=dict(status='PASS',source=encode(M),C=encode(C),s=str(s),m=str(m),q=str(q),
            old_residual_times_sqrt2=encode(w0),old_optimizer_times_sqrt2=encode(x0),
            alternative=encode(A),alternative_determinant=str(det(A)),
            alternative_block=encode(AS),delta=encode(Delta),edited=encode(N),
            alternative_edit_squared=str(edit_squared),alternative_value=str(actual),
            receipt=receipt,result=result,margin=str(F(3,5)-F(result['upper'])),
            elapsed_ns=perf_counter_ns()-start,python=platform.python_version(),
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            helper_sha256=hashlib.sha256((HERE/'checker_audit.py').read_bytes()).hexdigest(),
            checker_sha256=hashlib.sha256(CHECKER.read_bytes()).hexdigest(),
            scope='One algebraically selected exact capability example; no empirical fee, runtime advantage or transfer claim.')
OUT.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(status='PASS',upper=result['upper'],upper_decimal=float(F(result['upper'])),
                     alternative_value=str(actual),edit_squared_decimal=float(edit_squared),
                     margin=record['margin'],elapsed_ns=record['elapsed_ns'])))
