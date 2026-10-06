"""Two remaining concrete F16 boundaries, without rerunning the first probe.

The first large-denominator source had a small active optimum, so it did not
exercise a derived receipt bound beyond the external 256-bit input cap.
This supplement also checks the graded withdrawal helper at one valid and
one invalid retained-source point. No generated population or broad suite.
"""
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT))
from v2.checks import f06_inference_rules as K
from v2.checks import f07_soundness as A
from v2.verification import native, receipts
from v2.verification.model import Evidence, Query
from v2.verification.producer import produce
from v2.verification.reference import reference

output = HERE / 'supplement1.json'
if output.exists():
    raise SystemExit('Refusing to overwrite a retained attempt.')
records = []

source = Evidence(beta=0, gamma=Q(1, 2**255), revision='F16-active-large-denominator')
query = Query('T1')
outcome, semantic = produce(source, query), reference(source, query)
wire = receipts.make_receipt(source, query, outcome)
root = receipts.receive_receipt(source, query, wire)
assert root.budget == outcome.upper_bound == semantic.maximum == Q(255, 2**263)-Q(3, 32)
assert root.budget.denominator.bit_length() == 264
A.receive(native.context(source), outcome.proof, native.bound_request(native.context(source), 'T1', root.budget))
records.append({'name': 'derived_bound_exceeds_external_cap_without_rounding', 'status': 'PASS',
                'input_gamma': str(source.gamma), 'input_denominator_bits': source.gamma.denominator.bit_length(),
                'derived_bound': str(root.budget), 'derived_denominator_bits': root.budget.denominator.bit_length(),
                'current_external_request_budget': '0', 'receipt_accepted': True,
                'internal_exact_bound_request_accepted': True})

x, z = K.src('x'), K.num(0)
ctx = K.context(('x',), (K.Row(x, z), K.Row(x, K.num(1))), {'x': 0}, scope='F16-grade')
b = K.Builder(ctx, 'h'); left = b.rewrite(b.row(0), x, z); right = b.rewrite(b.row(1), x, z)
proof = b.proof(b.meet(left, right))
grade = A.grade_at(ctx, proof, (0,), {'x': 1})
assert grade['actual_difference'] == grade['bound'] == grade['penalty'] == grade['linear_penalty'] == 1
records.append({'name': 'graded_withdrawal_exact_point', 'status': 'PASS', 'withdrawn': [0],
                'point': {'x': '1'}, 'grade': {key: str(value) for key, value in grade.items()}})
try:
    A.grade_at(ctx, proof, (0,), {'x': 2})
except A.AuditError as error:
    records.append({'name': 'graded_helper_rejects_failed_retained_premise', 'status': 'PASS',
                    'point': {'x': '2'}, 'exception': type(error).__name__, 'message': str(error)})
else:
    raise AssertionError('Graded helper accepted a point violating a retained row.')

result = {'status': 'PASS', 'records': records,
          'probe_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'scope': 'Three targeted assertions resolving two concrete remaining boundaries; no first-probe repeat.'}
output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
print(json.dumps(result, sort_keys=True), flush=True)
