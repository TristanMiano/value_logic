"""Regression for output serialization repair; Codex (GPT-6), DEVELOPMENT."""
from decimal import Decimal
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter_ns
import hashlib
import importlib.util
import json
import platform
import sys

HERE=Path(__file__).resolve().parent
OUT=HERE/'format_repair_result.json'
SOURCE=HERE/'block_check_v2.py'
if OUT.exists():
    raise SystemExit('Refusing to overwrite observed evidence.')
spec=importlib.util.spec_from_file_location('repaired_checker',SOURCE)
ck=importlib.util.module_from_spec(spec)
spec.loader.exec_module(ck)
start=perf_counter_ns()
guard=sys.get_int_max_str_digits()
for n in (0,1,-1,2**15000+123456789,-2**15000):
    assert int(Decimal(ck.integer_text(n)))==n
base=json.loads((HERE/'format_result.json').read_text())['base_certificate']
B=ck.MAX_BITS
tmax=2**B-1
rows=[]
for tl in (2,tmax-1):
    cert=dict(base,t_lower=str(tl))
    checked=ck.verify(cert)
    numerator,denominator=checked['lower'].split('/')
    actual=F(int(Decimal(numerator)),int(Decimal(denominator)))
    C=F(cert['C_minus'][0][0]);E=F(cert['edit_squared'])
    expected=C/(1+tl-(tl-E-E/tl)*C)
    assert actual==expected and checked['verdict']=='unresolved' and checked['upper']=='1'
    rows.append(dict(t_lower_bits=tl.bit_length(),verdict=checked['verdict'],
                     exact_round_trip=True,lower_characters=len(checked['lower'])))
for name in ('rejection_result.json','partial_result.json'):
    prior=json.loads((HERE/name).read_text())
    cases=prior.get('cases',[prior])
    for r in cases:
        assert ck.verify(r['certificate'])==r['checked']
bad=dict(base,t_upper=ck.integer_text(2**(2*(B-2))))
try:
    ck.verify(bad)
    raise AssertionError('Oversized witness was accepted.')
except ck.InvalidCertificate:
    pass
assert sys.get_int_max_str_digits()==guard
record=dict(status='PASS',large_receipts=rows,integer_round_trips=5,ordinary_receipt_regressions=4,
            oversized_witness_rejected=True,process_digit_guard_unchanged=guard,
            elapsed_ns=perf_counter_ns()-start,python=platform.python_version(),
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            checker_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            original_checker_sha256=hashlib.sha256((HERE.parent/'s16'/'block_check.py').read_bytes()).hexdigest(),
            scope='Serialization repair only: same arithmetic, schema, input limits and verdicts; bounded-format incompleteness remains.')
OUT.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(status='PASS',large_receipts=rows,elapsed_ns=record['elapsed_ns'])))
