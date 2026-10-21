"""DEVELOPMENT exact finite screen; no application or timing comparison."""
from pathlib import Path
from itertools import combinations, product
import hashlib
import json
import random
import time

ROOT = Path(__file__).resolve().parent
RNG = random.Random(202610205)


def holds(world, clauses):
    return all(any(((world >> i) & 1) == b for i, b in clause) for clause in clauses)


def random_cnf(n):
    clauses = []
    for _ in range(RNG.randrange(0, 2*n+1)):
        indices = RNG.sample(range(n), RNG.choice((1, 2)))
        clauses.append(tuple((i, RNG.randrange(2)) for i in indices))
    return tuple(clauses)


def models(n, clauses):
    return {x for x in range(1 << n) if holds(x, clauses)}


def polar_compile(source, goal):
    clauses = set()
    for clause in goal:
        indices = tuple(i for i, _ in clause)
        patterns = {tuple((x >> i) & 1 for i in indices) for x in source}
        for pattern in patterns:
            # Falsification requires x_i XOR a_i = 1-b_i, hence forbidden
            # a_i=x_i XOR (1-b_i); the resulting literal is its complement.
            clauses.add(tuple(sorted((i, xbit ^ b) for (i, b), xbit in zip(clause, pattern))))
    return tuple(sorted(clauses))


def hull(n, source):
    clauses = []
    for size in (1, 2):
        for indices in combinations(range(n), size):
            observed = {tuple((x >> i) & 1 for i in indices) for x in source}
            for pattern in product(range(2), repeat=size):
                if pattern not in observed:
                    clauses.append(tuple((i, 1-b) for i, b in zip(indices, pattern)))
    return models(n, clauses)


def direct_permissions(source, available, good):
    return {a for a in available if all((x ^ a) in good for x in source)}


def encode(source):
    return sorted(source)


def run():
    began = time.perf_counter()
    stats = dict(panels=0, union_models=0, maximality_witnesses=0,
                 receipt_checks=0, strict_hull_relaxations=0,
                 strict_conditional_losses=0)
    first_nontrivial = None
    first_conditional = None
    for n in range(2, 7):
        full = set(range(1 << n))
        for _ in range(120):
            goal, availability = random_cnf(n), random_cnf(n)
            good, available = models(n, goal), models(n, availability)
            source = set()
            parts = []
            for _ in range(RNG.randrange(1, 5)):
                formula = random_cnf(n)
                part = models(n, formula)
                parts.append(formula)
                source.update(part)
            if not source:
                continue
            stats['panels'] += 1
            stats['union_models'] += len(parts)
            allowed = direct_permissions(source, available, good)
            first = polar_compile(source, goal)
            assert models(n, first) & available == allowed
            second = polar_compile(allowed, goal)
            closure = models(n, second)
            direct = {x for x in full if all((x ^ a) in good for a in allowed)}
            assert closure == direct and source <= closure
            assert direct_permissions(closure, available, good) == allowed
            binary_hull = hull(n, source)
            assert binary_hull <= closure
            assert models(n, polar_compile(direct_permissions(closure, available, good), goal)) == closure
            for x in full-closure:
                assert any((x ^ a) not in good for a in allowed)
                stats['maximality_witnesses'] += 1
            if binary_hull < closure:
                stats['strict_hull_relaxations'] += 1
                if first_nontrivial is None and 1 < len(allowed) < len(available):
                    first_nontrivial = dict(n=n, goal=goal, availability=availability,
                        source=encode(source), binary_hull=encode(binary_hull),
                        closure=encode(closure), allowed=encode(allowed))
            for i in range(n):
                for b in range(2):
                    sf = {x for x in source if ((x >> i) & 1) == b}
                    sw = {x for x in closure if ((x >> i) & 1) == b}
                    if not sf:
                        continue
                    af = direct_permissions(sf, available, good)
                    aw = direct_permissions(sw, available, good)
                    assert aw <= af
                    stats['receipt_checks'] += 1
                    if aw < af:
                        stats['strict_conditional_losses'] += 1
                        if first_conditional is None:
                            first_conditional = dict(n=n, goal=goal, availability=availability,
                                source=encode(source), closure=encode(closure), receipt=(i,b),
                                original_permissions=encode(af), retained_permissions=encode(aw))
    # Written example uses tuple order x,y,z, whereas integers use little-endian bits.
    goal = (((0,0),(1,0)), ((1,0),(2,0)))
    source = {0, 2, 1}
    allowed = direct_permissions(source, set(range(8)), models(3, goal))
    closure = models(3, polar_compile(allowed, goal))
    assert allowed == {0} and len(closure) == 5 and hull(3, source) == source
    assert first_nontrivial is not None and first_conditional is not None
    return dict(status='PASS', contributor='Codex (GPT-6)', seed=202610205,
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        statistics=stats, strict_nontrivial_example=first_nontrivial,
        conditional_loss_example=first_conditional,
        elapsed_seconds=time.perf_counter()-began,
        scope='Exact enumerated panels; no independent confirmation or arm runtime comparison')


if __name__ == '__main__':
    result = run()
    (ROOT/'closure_probe.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result))
