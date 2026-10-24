"""Finite rational ambiguity witness; DEVELOPMENT, Codex (GPT-6)."""
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter_ns
import hashlib
import json
import platform
from checker_audit import adj_inverse, mm, transpose, plus, eye, encode

HERE=Path(__file__).resolve().parent
out=HERE/'control_witness.json'
if out.exists():
    raise SystemExit('Refusing to overwrite an observed result.')
start=perf_counter_ns()
M=[[F(5,3)],[F(-4,3)]]
N=[[F(119,75)],[F(-209,150)]]
old=adj_inverse(plus(eye(2),mm(M,transpose(M))))
new=adj_inverse(plus(eye(2),mm(N,transpose(N))))
w=[[row[0]] for row in old]
delta=plus(N,M,-1)
E=mm(transpose(delta),delta)[0][0]
assert w==[[F(1,2)],[F(2,5)]]
assert mm(transpose(w),w)[0][0]==F(41,100)
assert E==F(1,100)
assert new[0][0]==F(66181,122825)>F(1077,2000)
record=dict(status='PASS',M=encode(M),N=encode(N),old_resolvent=encode(old),
            new_resolvent=encode(new),old_value='1/2',old_residual_moment='41/100',
            edit_squared=str(E),edited_value=str(new[0][0]),threshold='1077/2000',
            elapsed_ns=perf_counter_ns()-start,python=platform.python_version(),
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            helper_sha256=hashlib.sha256((HERE/'checker_audit.py').read_bytes()).hexdigest(),
            scope='Exact finite feasible counterexample to a decision based only on s,m and the norm budget; not a new universal theorem.')
out.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(status='PASS',edited_value=float(new[0][0]),elapsed_ns=record['elapsed_ns'])))
