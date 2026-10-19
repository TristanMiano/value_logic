"""DEVELOPMENT: immutable-source lineage versus direct current-world progression."""
from collections import deque
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import random
import sys
import time
from permission_probe import graph, holds, projections
from map_probe import source_edges

HERE = Path(__file__).resolve().parent


class Lineage:
    def __init__(self, n, clauses):
        self.n = n
        sat, self.reach, initial = graph(n, clauses)
        assert sat
        self.edges = source_edges(n, clauses)
        self.forced = 0
        self.records = [(i % n, 0) for i in range(2*n)]
        self.cache = {}
        self.stats = dict(forced_literals=0, edge_visits=0, writes=0,
                          observations=0, base_pairs=0, pattern_visits=0)
        self.propagate([lit for lit in range(2*n) if initial >> lit & 1])

    def propagate(self, seeds):
        queue = deque(seeds)
        while queue:
            lit = queue.popleft()
            if self.forced >> lit & 1:
                continue
            if self.forced >> (lit ^ 1) & 1:
                return False
            self.forced |= 1 << lit
            self.stats['forced_literals'] += 1
            for dest in self.edges[lit]:
                self.stats['edge_visits'] += 1
                queue.append(dest)
        return True

    def apply(self, updates):
        old = list(self.records)
        for dest, source, sign in updates:
            if source is None:
                self.records[dest] = (None, sign)
            else:
                origin, shift = old[source]
                self.records[dest] = (origin, shift ^ sign)
            self.stats['writes'] += 1

    def observe(self, i, bit):
        self.stats['observations'] += 1
        origin, sign = self.records[i]
        if origin is None:
            return bit == sign
        return self.propagate([2*origin+(bit ^ sign)])

    def project(self, scope):
        origins = tuple(sorted({self.records[i][0] for i in scope
                                if self.records[i][0] is not None}))
        if origins not in self.cache:
            if not origins:
                self.cache[origins] = [()]
            else:
                target = [tuple(2*i for i in origins)]
                _, patterns = projections(self.n, target, self.reach, 0)[0]
                # The reachability test includes each assumption's closure;
                # include the initial backbone separately for empty/fixed pairs.
                self.cache[origins] = patterns
            self.stats['base_pairs'] += 1
        answer = set()
        for bits in self.cache[origins]:
            self.stats['pattern_visits'] += 1
            if any(self.forced >> (2*i+1-b) & 1 for i, b in zip(origins, bits)):
                continue
            values = dict(zip(origins, bits))
            answer.add(tuple(sign if origin is None else values[origin] ^ sign
                             for origin, sign in [self.records[i] for i in scope]))
        return answer


def apply_world(world, updates):
    result = world
    for dest, source, sign in updates:
        value = sign if source is None else ((world >> source) & 1) ^ sign
        result = (result & ~(1 << dest)) | (value << dest)
    return result


def main():
    begun = time.perf_counter_ns()
    rng = random.Random(120031)
    totals = dict(fixtures=0, steps=0, projections=0, counterfactual_receipts=0,
                  contradictory_receipts=0, forced_literals=0, edge_visits=0,
                  writes=0, observations=0, base_pairs=0, pattern_visits=0)
    for trial in range(64):
        n = 2+trial % 5
        planted = rng.randrange(1 << n)
        pool = [(2*i+a, 2*j+b) for i, j in combinations(range(n), 2)
                for a, b in product([0, 1], repeat=2)
                if holds([(2*i+a, 2*j+b)], planted)]
        source = rng.sample(pool, min(len(pool), n+trial % (n+1)))
        worlds = [x for x in range(1 << n) if holds(source, x)]
        pairs = {x: x | (x << n) for x in worlds}
        actual = planted | (planted << n)
        state = Lineage(n, source)
        for step in range(64):
            dests = rng.sample(list(range(n, 2*n)), 1+step % n)
            updates = [(dest, None if rng.randrange(5)==0 else rng.randrange(2*n),
                        rng.randrange(2)) for dest in dests]
            state.apply(updates)
            pairs = {x: apply_world(y, updates) for x, y in pairs.items()}
            actual = apply_world(actual, updates)
            if step % 4 == 0:
                i = rng.randrange(2*n)
                bit = actual >> i & 1
                assert state.observe(i, bit)
                pairs = {x: y for x, y in pairs.items() if y >> i & 1 == bit}
                assert pairs
            expected_forced = sum(1 << (2*i+b) for i in range(n) for b in [0, 1]
                                  if all(x >> i & 1 == b for x in pairs))
            assert state.forced == expected_forced, (trial, step)
            for size in [1, 2]:
                for scope in combinations(range(2*n), size):
                    truth = {tuple(y >> i & 1 for i in scope) for y in pairs.values()}
                    assert state.project(scope) == truth, (trial, step, scope)
                    totals['projections'] += 1
            # Preview both outcomes on the current source, without corrupting
            # the main monotone stream on an impossible hypothetical branch.
            for i in range(2*n):
                for bit in [0, 1]:
                    origin, sign = state.records[i]
                    possible = (bit == sign if origin is None else
                                not (state.forced >> (2*origin+1-(bit ^ sign)) & 1))
                    truth = any(y >> i & 1 == bit for y in pairs.values())
                    assert possible == truth
                    totals['counterfactual_receipts'] += 1
                    totals['contradictory_receipts'] += int(not possible)
            totals['steps'] += 1
        assert state.stats['forced_literals'] <= n
        assert state.stats['edge_visits'] <= sum(map(len, state.edges))
        for key, value in state.stats.items():
            totals[key] += value
        totals['fixtures'] += 1
    result = dict(status='PASS', scope='DEVELOPMENT', contributor='Codex (GPT-6)',
                  seed=120031, python=sys.version, totals=totals,
                  elapsed_ns=time.perf_counter_ns()-begun,
                  hashes={p: hashlib.sha256((HERE/p).read_bytes()).hexdigest()
                          for p in ['lineage_probe.py', 'map_probe.py', 'permission_probe.py']},
                  limitations='Finite semantics and per-stream amortization checks; no '
                              'complete runtime, physical-query, or economic advantage claim.')
    (HERE/'lineage_probe.json').write_bytes((json.dumps(result, indent=2)+'\n').encode())
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
