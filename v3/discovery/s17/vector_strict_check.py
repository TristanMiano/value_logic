"""Full-rank strengthening of same-vector ambiguity; DEVELOPMENT, Codex (GPT-6)."""
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter_ns
import hashlib
import json
import platform
from checker_audit import adj_inverse, mm, transpose, plus, eye, encode

HERE = Path(__file__).resolve().parent
out = HERE/'vector_strict_result.json'
if out.exists():
    raise SystemExit('Refusing to overwrite an observed result.')
start = perf_counter_ns()
u = [[F(1)], [F(1)]]
M = [[F(3), F(0)], [F(0), F(1, 3)]]
M0 = [[F(3, 2), F(3, 2)], [F(1, 6), F(1, 6)]]
correction = [[F(9, 100), F(-9, 100)], [F(-1, 100), F(1, 100)]]
delta = [[F(-1, 100)]*2, [F(-7, 100)]*2]
alternative = plus(M0, correction)
new = plus(alternative, delta)
resolvent = lambda a: adj_inverse(plus(eye(2), mm(a, transpose(a))))
old_C = resolvent(M)
alternative_C = resolvent(alternative)
w = mm(old_C, u)
x = mm(transpose(M), w)
assert mm(alternative_C, u) == w
assert mm(transpose(alternative), w) == x
assert mm(correction, x) == [[F(0)], [F(0)]]
assert mm(transpose(correction), w) == [[F(0)], [F(0)]]
det = alternative[0][0]*alternative[1][1]-alternative[0][1]*alternative[1][0]
assert det == F(3, 50)  # full rank implies 0<resolvent<I.
assert mm(transpose(delta), delta) == [[F(1, 200)]*2]*2
value = mm(transpose(u), mm(resolvent(new), u))[0][0]/2
assert value > F(1077, 2000)
record = dict(status='PASS', source=encode(M), alternative=encode(alternative),
              correction=encode(correction), delta=encode(delta), edited=encode(new),
              determinant=str(det), alternative_block=encode(alternative_C),
              common_residual_times_sqrt2=encode(w),
              common_coefficient_times_sqrt2=encode(x),
              edited_value=str(value), threshold='1077/2000',
              margin=str(value-F(1077, 2000)), elapsed_ns=perf_counter_ns()-start,
              python=platform.python_version(),
              source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              helper_sha256=hashlib.sha256((HERE/'checker_audit.py').read_bytes()).hexdigest(),
              scope='Exact full-rank same-vector norm-only information counterexample.')
out.write_text(json.dumps(record, indent=2)+'\n', encoding='utf-8', newline='\n')
print(json.dumps(dict(status='PASS', value=str(value), decimal=float(value),
                     margin=str(value-F(1077, 2000)), elapsed_ns=record['elapsed_ns'])))
