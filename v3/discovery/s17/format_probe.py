"""Finite-format and output availability screen; Codex (GPT-6), DEVELOPMENT."""
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter_ns
import hashlib
import importlib.util
import json
import platform
import sys

HERE=Path(__file__).resolve().parent
OUT=HERE/'format_result.json'
CHECKER=HERE.parent/'s16'/'block_check.py'
if OUT.exists():
    raise SystemExit('Refusing to overwrite observed evidence.')
spec=importlib.util.spec_from_file_location('checker',CHECKER)
ck=importlib.util.module_from_spec(spec)
spec.loader.exec_module(ck)
start=perf_counter_ns()
B=ck.MAX_BITS
v=2**(B-2)
C=F(v+1,2*v+1)
E=F(v-1,v)
tmax=2**B-1
assert (1/C-1)>E and (v*v-1)>tmax
cert=dict(schema='response-block-v1',source_id='s17-format-limit',dimension=1,
          C_minus=[[str(C)]],C_plus=[[str(C)]],V=[['1']],
          edit_squared=str(E),t_lower='2',t_upper=str(tmax),threshold='1')
outcomes=[]
for name,tl in [('small_lower',2),('large_lower',tmax-1)]:
    attempt=dict(cert,t_lower=str(tl))
    try:
        checked=ck.verify(attempt)
        outcomes.append(dict(case=name,status='returned',verdict=checked['verdict'],
                             lower_character_count=len(checked['lower'])))
        assert checked['verdict']=='unresolved'
    except ValueError as ex:
        outcomes.append(dict(case=name,status='ValueError',message=str(ex)))
big_t=v*v
a=1+big_t
d=big_t-E-E/big_t
upper=a*C/(1+d*C)
assert upper<1 and big_t.bit_length()>B
record=dict(status='OBSERVED',input_bit_cap=B,python_decimal_digit_limit=sys.get_int_max_str_digits(),
            base_certificate=cert,outcomes=outcomes,required_upper_parameter_greater_than_bits=(v*v-1).bit_length(),
            mathematical_witness_parameter_bits=big_t.bit_length(),mathematical_witness_upper_below_one=True,
            elapsed_ns=perf_counter_ns()-start,python=platform.python_version(),
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            checker_sha256=hashlib.sha256(CHECKER.read_bytes()).hexdigest(),
            scope='One exact finite-format incompleteness example; observed large-output availability behavior, no false approval asserted.')
OUT.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(outcomes=outcomes,required_bits=record['required_upper_parameter_greater_than_bits'],elapsed_ns=record['elapsed_ns'])))
