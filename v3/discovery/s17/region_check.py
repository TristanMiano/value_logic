"""Exact boundary of a derived decision region; DEVELOPMENT, Codex (GPT-6)."""
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter_ns
import hashlib
import json
import platform
from checker_audit import plus, encode, checker, CHECKER

HERE=Path(__file__).resolve().parent
OUT=HERE/'region_result.json'
if OUT.exists():
    raise SystemExit('Refusing to overwrite an observed result.')
start=perf_counter_ns()
C=[[F(1,1025),F(0)],[F(0),F(9,10)]]
rad=[[F(1,10000),F(0)],[F(0),F(1,10000)]]
receipt=dict(schema='response-block-v1',source_id='s17-region-boundary',
             dimension=2,C_minus=encode(plus(C,rad,-1)),
             C_plus=encode(plus(C,rad)),V=[['1/2','1/2'],['1/2','1/2']],
             edit_squared='9',t_lower='10',t_upper='100',threshold='3/5')
result=checker.verify(receipt)
margin=F(3,5)-F(result['upper'])
assert result['verdict']=='below' and margin>0
minimum_lower_eigenvalue=F(1,9802)-F(1,10000)
cancel_bound=F(121,18)+F(81,200000)
assert minimum_lower_eigenvalue>0
assert cancel_bound<7
assert 10**2>=9*(1+10) and 100**2>=9*(1+100)
record=dict(status='PASS',R_interval=[32,99],E_interval=[7,9],receipt=receipt,
            result=result,margin=str(margin),cancelling_squared_norm_bound=str(cancel_bound),
            minimum_bracket_eigenvalue=str(minimum_lower_eigenvalue),
            elapsed_ns=perf_counter_ns()-start,python=platform.python_version(),
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            helper_sha256=hashlib.sha256((HERE/'checker_audit.py').read_bytes()).hexdigest(),
            checker_sha256=hashlib.sha256(CHECKER.read_bytes()).hexdigest(),
            scope='One boundary check; the continuum guarantee uses the separate monotonicity proof, not sampling.')
OUT.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(status=record['status'],upper=result['upper'],
                     upper_decimal=float(F(result['upper'])),margin=str(margin),
                     elapsed_ns=record['elapsed_ns'])))
