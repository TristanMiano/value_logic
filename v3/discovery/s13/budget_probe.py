"""Development screen of two-denominator inspection budget; exact arithmetic."""
from pathlib import Path
from itertools import product
from fractions import Fraction as F
from collections import deque
import ast
import hashlib
import json
import random
import time

HERE = Path(__file__).resolve().parent
deps = [HERE/'edge_extension.py', HERE/'inspect_probe.py']
scope = {'deque': deque, 'COUNTS': {'cuts': 0}}
for path, names in [(deps[0], {'Flow'}), (deps[1], {'valid', 'solve'})]:
    tree = ast.parse(path.read_text(encoding='utf-8'))
    nodes = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names]
    assert {n.name for n in nodes} == names
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), scope)
solve, valid = scope['solve'], scope['valid']
rng = random.Random(202610212)


def main():
    started = time.perf_counter_ns()
    counts = dict(panels=0, plans=0, certificates=0, worlds=0, matching=0, tight_budget=0)
    for n in range(1, 6):
        for case in range(9):
            edges = sorted({tuple(rng.sample(range(n), 2)) for _ in range(n)}) if n > 1 else []
            units = [(rng.randrange(n), rng.randrange(2))] if case % 2 == 0 else []
            w = [tuple(F(rng.randrange(0, 10), 2) for _ in (0, 1)) for i in range(n)]
            q = [F(rng.randrange(0, 9), 4) for i in range(n)]
            predicted = tuple(rng.randrange(2) for i in range(n))
            certificates = [s for s in product((-1, 0, 1), repeat=n) if valid(s, edges, units)]
            B = min(sum(w[i][b] for i, b in enumerate(s) if b >= 0) for s in certificates)
            cp = min(sum(min(w[i][b], q[i]) if b == predicted[i] else w[i][b]
                         for i, b in enumerate(s) if b >= 0) for s in certificates)
            counts['certificates'] += len(certificates)
            for lam in (F(1, 10), F(1, 4), F(1, 2), F(3, 4), F(1)):
                d = [tuple(min(w[i][b], q[i]/lam) if b == predicted[i] else w[i][b]
                           for b in (0, 1)) for i in range(n)]
                value, signs = solve(d, edges, units)
                enumerated = min(sum(d[i][b] for i, b in enumerate(s) if b >= 0)
                                 for s in certificates)
                assert value == enumerated
                queried = [i for i, b in enumerate(signs) if b >= 0 and b == predicted[i]
                           and q[i]/lam < w[i][b]]
                written = [i for i, b in enumerate(signs) if b >= 0 and i not in queried]
                Q = sum(q[i] for i in queried)
                W = sum(w[i][signs[i]] for i in written)
                assert Q/lam+W == value <= B and Q <= lam*B
                for x in product((0, 1), repeat=n):
                    h = {i: x[i] for i in queried}
                    # Independent certificate enumeration of post-observation recourse.
                    recourse = min(sum(0 if h.get(i, -1) == b else w[i][b]
                                       for i, b in enumerate(s) if b >= 0) for s in certificates)
                    misses = sum(w[i][signs[i]] for i in queried if x[i] != signs[i])
                    cost = Q+recourse
                    assert cost <= (1+lam)*B
                    assert cost <= cp/lam+misses
                    if all(x[i] == predicted[i] for i in queried):
                        assert cost <= cp/lam
                        counts['matching'] += 1
                    if B and cost == (1+lam)*B: counts['tight_budget'] += 1
                    counts['worlds'] += 1
                counts['plans'] += 1
            counts['panels'] += 1
    # Just-above-threshold one-bit cases approach the claimed unavoidable factor.
    lower = []
    for lam in (F(1, 10), F(1, 4), F(1, 2), F(3, 4)):
        q = lam+(1-lam)/1000
        assert q < 1 and q+1 > 1+lam
        assert 1/q < 1/lam
        lower.append(dict(lam=str(lam), q=str(q), blind=1,
                          forced_matching_ratio=str(1/q), limiting_ratio=str(1/lam)))
    out = dict(status='PASS', contributor='Codex (GPT-6)', seed=202610212,
               counts=counts, cuts=scope['COUNTS']['cuts'], lower_examples=lower,
               elapsed_ns=time.perf_counter_ns()-started,
               source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               dependency_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in deps},
               scope='Finite rational certificate comparisons; distinct blind and predicted-certificate denominators.')
    (HERE/'budget_probe.json').write_text(json.dumps(out, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(out))


if __name__ == '__main__': main()
