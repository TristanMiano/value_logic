"""Operational lower rejection receipt; Codex (GPT-6), DEVELOPMENT."""
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter_ns
import hashlib
import importlib.util
import json
import platform

HERE=Path(__file__).resolve().parent
OUT=HERE/'rejection_result.json'
CHECKER=HERE.parent/'s16'/'block_check.py'
if OUT.exists():
    raise SystemExit('Refusing to overwrite observed evidence.')
spec=importlib.util.spec_from_file_location('checker',CHECKER)
ck=importlib.util.module_from_spec(spec)
spec.loader.exec_module(ck)
start=perf_counter_ns()
cert=dict(schema='response-block-v1',source_id='s17-lower-rejection',dimension=2,
          C_minus=[['999/10000','0'],['0','8999/10000']],
          C_plus=[['1001/10000','0'],['0','9001/10000']],
          V=[['1/2','1/2'],['1/2','1/2']],edit_squared='1/100',
          t_lower='1/4',t_upper='1/4',threshold='23/50')
checked=ck.verify(cert)
assert checked['verdict']=='above'
assert F(checked['lower'])>=F(6070,13161)-F(1,8820)>F(23,50)
assert F(100,221)<F(23,50)
record=dict(status='PASS',certificate=cert,checked=checked,
            old_value_only_counterexample=dict(source='I_2',edit='I_2/10',old_value='1/2',new_value='100/221'),
            elapsed_ns=perf_counter_ns()-start,python=platform.python_version(),
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            checker_sha256=hashlib.sha256(CHECKER.read_bytes()).hexdigest(),
            scope='One exact rounded receipt and a different-information counterexample, not a benchmark or superiority over old-vector controls.')
OUT.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(status='PASS',lower=checked['lower'],elapsed_ns=record['elapsed_ns'])))
