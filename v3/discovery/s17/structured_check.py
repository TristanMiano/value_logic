"""Exact structured-update composition screen; DEVELOPMENT, Codex (GPT-6)."""
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter_ns
import hashlib
import json
import platform
from checker_audit import adj_inverse, mm, transpose, plus, eye, encode, checker, CHECKER

HERE=Path(__file__).resolve().parent
OUT=HERE/'structured_result.json'
if OUT.exists():
    raise SystemExit('Refusing to overwrite observed evidence.')
start=perf_counter_ns()
matrix=lambda rows:[[F(v) for v in row] for row in rows]
scale=lambda A,s:[[s*v for v in row] for row in A]
M=matrix([[3,1,0],[1,2,1],[0,1,2]])
M1=matrix([[0,1,0],[1,2,1],[0,1,2]])
H=matrix([[-9,-3],[-3,0]])
W=matrix([[1,0],[0,1],[0,0]])
u=matrix([[1],[1],[0]])
S=adj_inverse(plus(eye(3),mm(M,transpose(M))))
S1=adj_inverse(plus(eye(3),mm(M1,transpose(M1))))
C=mm(transpose(W),mm(S,W))
C1=mm(transpose(W),mm(S1,W))
assert C==scale(matrix([[2,-2],[-2,5]]),F(1,13))
assert C1==scale(matrix([[26,-8],[-8,11]]),F(1,37))
assert plus(mm(M1,transpose(M1)),mm(M,transpose(M)),-1)==mm(W,mm(H,transpose(W)))
assert adj_inverse(plus(adj_inverse(C),H))==C1
epsilon=F(1,10000)
Clo=plus(C,scale(eye(2),epsilon),-1)
Chi=plus(C,scale(eye(2),epsilon))
lo=adj_inverse(plus(adj_inverse(Clo),H))
hi=adj_inverse(plus(adj_inverse(Chi),H))
assert checker.positive(plus(C1,lo,-1)) and checker.positive(plus(hi,C1,-1))
receipt=dict(schema='response-block-v1',source_id='s17-structured-transport',dimension=2,
             C_minus=encode(lo),C_plus=encode(hi),V=[['1/2','1/2'],['1/2','1/2']],
             edit_squared='1/100',t_lower='11/100',t_upper='11/100',threshold='2/5')
result=checker.verify(receipt)
assert result['verdict']=='below'
P=plus(eye(3),scale(mm(u,transpose(u)),F(2,5)),-1)
Nalt=mm(P,M)
altS=adj_inverse(plus(eye(3),mm(Nalt,transpose(Nalt))))
alternative_value=mm(transpose(u),mm(altS,u))[0][0]/2
old_action_norm2=mm(transpose(u),mm(mm(M,transpose(M)),u))[0][0]/2
assert old_action_norm2==13
edit_squared=F(16,25)*old_action_norm2
assert edit_squared==F(208,25)<F(961,100)
assert alternative_value>=F(25,38)>F(2,5)
record=dict(status='PASS',M=encode(M),M1=encode(M1),W=encode(W),H=encode(H),
            C=encode(C),C1=encode(C1),old_bracket=[encode(Clo),encode(Chi)],
            receipt=receipt,result=result,
            alternative_source=encode(Nalt),alternative_value=str(alternative_value),
            alternative_edit_squared=str(edit_squared),norm_only_budget_squared='961/100',
            elapsed_ns=perf_counter_ns()-start,python=platform.python_version(),
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            helper_sha256=hashlib.sha256((HERE/'checker_audit.py').read_bytes()).hexdigest(),
            checker_sha256=hashlib.sha256(CHECKER.read_bytes()).hexdigest(),
            scope='One exact conditional composition of standard Schur transport and N16 bounds; no novelty, sharpness or economic superiority is inferred.')
OUT.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(status='PASS',upper=result['upper'],upper_decimal=float(F(result['upper'])),
                     alternative_value=str(alternative_value),elapsed_ns=record['elapsed_ns'])))
