"""Same-vector comparator check; DEVELOPMENT, Codex (GPT-6)."""
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter_ns
import hashlib
import json
import platform
from checker_audit import adj_inverse, mm, transpose, plus, eye, encode

HERE = Path(__file__).resolve().parent
out = HERE / 'vector_result.json'
if out.exists():
    raise SystemExit('Refusing to overwrite an observed result.')
start = perf_counter_ns()
u = [[F(1)], [F(1)]]  # v=u/sqrt(2); retain scaled vectors exactly.
M = [[F(3), F(0)], [F(0), F(1, 3)]]
M0 = [[F(3, 2), F(3, 2)], [F(1, 6), F(1, 6)]]
delta = [[F(-1, 100)] * 2, [F(-7, 100)] * 2]
N0 = plus(M0, delta)
resolvent = lambda a: adj_inverse(plus(eye(2), mm(a, transpose(a))))
C = resolvent(M)
C0 = resolvent(M0)
w, w0 = mm(C, u), mm(C0, u)
x, x0 = mm(transpose(M), w), mm(transpose(M0), w0)
assert w == w0 == [[F(1, 10)], [F(9, 10)]]
assert x == x0 == [[F(3, 10)], [F(3, 10)]]
gram = mm(transpose(delta), delta)
assert gram == [[F(1, 200)] * 2] * 2  # eigenvalues 0 and 1/100.
value = mm(transpose(u), mm(resolvent(N0), u))[0][0] / 2
assert value == F(229, 425) > F(1077, 2000)
assert C != C0
record = dict(status='PASS', source=encode(M), alternative=encode(M0),
              delta=encode(delta), alternative_edited=encode(N0),
              true_block=encode(C), alternative_block=encode(C0),
              common_residual_times_sqrt2=encode(w),
              common_coefficient_times_sqrt2=encode(x),
              edit_squared_operator_norm='1/100', edited_value=str(value),
              threshold='1077/2000', elapsed_ns=perf_counter_ns()-start,
              python=platform.python_version(),
              source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              helper_sha256=hashlib.sha256((HERE/'checker_audit.py').read_bytes()).hexdigest(),
              scope='Same-vector norm-only information counterexample, not an empirical speed comparison.')
out.write_text(json.dumps(record, indent=2)+'\n', encoding='utf-8', newline='\n')
print(json.dumps(dict(status='PASS', value=str(value), elapsed_ns=record['elapsed_ns'])))
