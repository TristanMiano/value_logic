"""Development-only finite-field scope verification and retirement counterexample."""
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import platform
from time import perf_counter_ns

start = perf_counter_ns()
q = 5
polys = list(product(range(q), repeat=3))
values = {p: tuple(sum(c * x**i for i, c in enumerate(p)) % q
                   for x in range(q)) for p in polys}
spaces = [('zero', None), ('full', None), ('vertical', None)] + [('slope', s) for s in range(q)]

def inside(a, b, space):
    kind, s = space
    if kind == 'full':
        return True
    if kind == 'zero':
        return a == b == 0
    if kind == 'vertical':
        return a == 0
    return (b - s*a) % q == 0

claims = 0
false_claims = 0
max_false_roots = 0
for p, r, space in product(polys, polys, spaces):
    roots = sum(inside(a, b, space) for a, b in zip(values[p], values[r]))
    claims += 1
    if roots != q:
        false_claims += 1
        assert roots <= 2
        max_false_roots = max(max_false_roots, roots)

# Every monic quadratic with a root pair is a false polynomial identity.
roots_claims = [frozenset((a, b)) for a in range(q) for b in range(a, q)]
first = frozenset((0, 1))
roots_claims.remove(first)
roots_claims.insert(0, first)
seeds = list(product(range(q), repeat=2))
retired_false = 0
continued_false = 0
true_prefixes = 0
for seed in seeds:
    # Genuine, possibly changing, full/rank-one scope proposals reveal only accept.
    for p in polys[:7]:
        assert all(inside(values[p][x], (3*values[p][x]) % q, ('slope', 3)) for x in seed)
        true_prefixes += 1
    retired_false += all(x in first for x in seed)
    continued_false += any(all(x in roots for x in seed) for roots in roots_claims)
assert retired_false == 4
assert continued_false == 25

result = dict(status='PASS', model='Codex (GPT-6)', python=platform.python_version(),
    source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
    field=q, degree=2, secret_points=2, fixed_claims=claims,
    false_claims=false_claims, maximum_false_root_count=max_false_roots,
    genuine_prefix_checks=true_prefixes, seeds=len(seeds),
    lifetime_error_with_retirement=str(Fraction(retired_false, len(seeds))),
    error_when_reusing_after_rejection=str(Fraction(continued_false, len(seeds))),
    scope='All two-coordinate univariate degree-at-most-two polynomials over F5, all eight linear subspaces; not a general proof or cost benchmark.',
    elapsed_ns=perf_counter_ns()-start)
Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
print(json.dumps(result, indent=2))
