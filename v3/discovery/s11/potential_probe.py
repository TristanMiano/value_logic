"""Exact, small DEVELOPMENT screens for canonical policy-difference compression.

Codex (GPT-6). No external dependencies or stochastic floating-point decisions.
Run with --out PATH; existing outputs are never overwritten.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import random
import time


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def mul(K, v):
    return tuple(sum((x * y for x, y in zip(row, v)), F(0)) for row in K)


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


class Span:
    def __init__(self, n):
        self.n = n
        self.rows = []
        self.pivots = []
        self.reductions = 0

    def reduce(self, v):
        v = list(v)
        coeff = []
        for pivot, row in zip(self.pivots, self.rows):
            c = v[pivot]
            coeff.append(c)
            v = [x - c * y for x, y in zip(v, row)]
            self.reductions += 1
        return tuple(coeff), tuple(v)

    def insert(self, v):
        _, r = self.reduce(v)
        if not any(r):
            return False
        pivot = next(i for i, x in enumerate(r) if x)
        self.pivots.append(pivot)
        self.rows.append(tuple(x / r[pivot] for x in r))
        return True

    def coordinates(self, v):
        c, r = self.reduce(v)
        assert not any(r), (v, r)
        return c


def closure(generators, operations, n):
    span = Span(n)
    for v in generators:
        span.insert(v)
    pos = 0
    applications = 0
    while pos < len(span.rows):
        v = span.rows[pos]
        for op in operations:
            for K in op['K']:
                span.insert(mul(K, v))
                applications += 1
        pos += 1
    return span, applications


def transform(model, b):
    n = len(b)
    terminal = [sub(c, b) for c in model['terminal']]
    charges = []
    for op in model['operations']:
        expected_b = tuple(sum((mul(K, b)[i] for K in op['K']), F(0)) for i in range(n))
        charges.append(sub(add(op['q'], expected_b), b))
    return terminal, charges


def model_span(model, b):
    terminal, charges = transform(model, b)
    return closure(terminal + charges, model['operations'], len(b))


def evaluate(model, seed):
    n = len(model['terminal'][0])
    assert all(sum(sum(row) for row in (K[i] for K in op['K'])) == 1
               for op in model['operations'] for i in range(n))
    b = model['terminal'][0]
    span, applications = model_span(model, b)
    rng = random.Random(seed)
    baselines = [('zero', (F(0),) * n), ('pointwise_min', tuple(min(c[i] for c in model['terminal']) for i in range(n))),
                 ('arbitrary', tuple(F(rng.randrange(-5, 6)) for _ in range(n)))]
    baselines += [('terminal_' + str(i), c) for i, c in enumerate(model['terminal'])]
    dimensions = {}
    for name, potential in baselines:
        candidate, _ = model_span(model, potential)
        dimensions[name] = len(candidate.rows)
        for v in span.rows:
            candidate.coordinates(v)
        if name.startswith('terminal_'):
            assert len(candidate.rows) == len(span.rows)

    terminals, charges = transform(model, b)
    terminal_coeff = [span.coordinates(c) for c in terminals]
    charge_coeff = [span.coordinates(q) for q in charges]
    # B columns: K applied to each basis function, expressed in that basis.
    B = [[tuple(span.coordinates(mul(K, v)) for v in span.rows)
          for K in op['K']] for op in model['operations']]

    policies = {c: u for c, u in zip(model['terminal'], terminal_coeff)}
    horizon_counts = [len(policies)]
    comparisons = 0
    for horizon in (1, 2):
        old = list(policies.items())
        new = dict(policies)
        for e, op in enumerate(model['operations']):
            for children in product(old, repeat=len(op['K'])):
                direct = op['q']
                coeff = charge_coeff[e]
                for o, (v, alpha) in enumerate(children):
                    direct = add(direct, mul(op['K'][o], v))
                    continuation = tuple(sum((B[e][o][j][i] * alpha[j] for j in range(len(alpha))), F(0))
                                         for i in range(len(alpha)))
                    coeff = add(coeff, continuation)
                assert coeff == span.coordinates(sub(direct, b))
                new[direct] = coeff
                comparisons += 1
        policies = new
        horizon_counts.append(len(policies))

    for _ in range(5):
        p = tuple(F(rng.randrange(5), rng.randrange(1, 5)) for _ in range(n))
        z = tuple(dot(p, row) for row in span.rows)
        original = [dot(p, v) for v in policies]
        compressed = [dot(z, c) for c in policies.values()]
        assert all(x - dot(p, b) == y for x, y in zip(original, compressed))
        assert {i for i, x in enumerate(original) if x == min(original)} == {
            i for i, x in enumerate(compressed) if x == min(compressed)}

    policy_span = Span(n)
    for v in policies:
        policy_span.insert(sub(v, b))
    # A finite horizon may not yet generate the all-horizon invariant span.
    assert len(policy_span.rows) <= len(span.rows)
    return dict(name=model['name'], states=n, canonical_dimension=len(span.rows),
                baseline_dimensions=dimensions, horizon_policy_counts=horizon_counts,
                horizon_two_difference_rank=len(policy_span.rows), exact_recursion_checks=comparisons,
                basis_operator_applications=applications)


def deterministic(n, transition, observation, charge, outcomes=(0, 1)):
    Ks = []
    for o in outcomes:
        Ks.append(tuple(tuple(F(int(j == transition[i] and observation[i] == o)) for j in range(n)) for i in range(n)))
    return {'q': tuple(map(F, charge)), 'K': Ks}


def fixtures():
    # Irrelevant latent nuisance b is unchanged and unobserved by the operation.
    n = 8
    b = tuple(F(7 * (i // 2) ** 2) for i in range(n))
    c1 = tuple(b[i] + (1 if i % 2 else -1) for i in range(n))
    toggle = deterministic(n, [i ^ 1 for i in range(n)], [0] * n, [1] * n, (0,))
    reveal = deterministic(n, list(range(n)), [i % 2 for i in range(n)], [1] * n)
    yield {'name': 'irrelevant_common_nuisance', 'terminal': [b, c1], 'operations': [toggle, reveal]}
    change = deterministic(n, [(i + 2) % n for i in range(n)], [0] * n, [1] * n, (0,))
    yield {'name': 'changed_nuisance_operation', 'terminal': [b, c1], 'operations': [toggle, change]}
    yield {'name': 'all_zero', 'terminal': [(F(0),) * 3] * 2,
           'operations': [deterministic(3, [1, 2, 0], [0, 1, 0], [0] * 3)]}
    for m in (3, 5):
        n = 2 ** m
        scores = tuple(F(sum(1 if (i >> j) & 1 else -1 for j in range(m))) for i in range(n))
        ops = [deterministic(n, [i ^ (1 << j) for i in range(n)], [0] * n, [1] * n, (0,)) for j in range(m)]
        yield {'name': 'signed_flip_' + str(m), 'terminal': [(F(0),) * n, scores], 'operations': ops}


def random_model(rng, index):
    n = 2 + index % 5
    terminal = [tuple(F(rng.randrange(-3, 6)) for _ in range(n)) for _ in range(2)]
    operations = []
    for _ in range(2):
        raw = [[rng.randrange(4) for _ in range(2 * n)] for _ in range(n)]
        for row in raw:
            if not any(row):
                row[0] = 1
        Ks = [tuple(tuple(F(raw[i][o*n+j], sum(raw[i])) for j in range(n)) for i in range(n)) for o in range(2)]
        operations.append({'q': tuple(F(rng.randrange(4)) for _ in range(n)), 'K': Ks})
    return {'name': 'random_' + str(index), 'terminal': terminal, 'operations': operations}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    assert not args.out.exists(), 'Preserve prior evidence; use a fresh output path.'
    start = time.perf_counter_ns()
    rng = random.Random(20261015)
    models = list(fixtures()) + [random_model(rng, i) for i in range(20)]
    records = []
    for i, model in enumerate(models):
        try:
            row = evaluate(model, 1000 + i)
        except Exception as exc:
            args.out.with_suffix('.failure.json').write_text(json.dumps({'index': i, 'model': model, 'exception': repr(exc), 'completed': records}, default=str, indent=2) + '\n', encoding='utf-8', newline='\n')
            raise
        records.append(row)
        print(json.dumps(row), flush=True)
    result = dict(schema='s11_canonical_compression_development_v1', contributor='Codex (GPT-6)',
                  seed=20261015, source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  cases=records, exact_recursion_checks=sum(r['exact_recursion_checks'] for r in records),
                  elapsed_ns=time.perf_counter_ns()-start,
                  scope='Exact finite checks, not a proof, novelty claim, economic benefit or general learned-model guarantee.')
    args.out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')


if __name__ == '__main__':
    main()
