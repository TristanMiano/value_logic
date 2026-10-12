"""Reusable pair-error closure; ChatGPT (GPT-6 Astra Pro), DEVELOPMENT.

The graph weights are simultaneous upper bounds on disagreements of common
vertex error bits, not acquisition costs. Small-boundary implementation uses
Floyd-Warshall plus subset matching DP; it is exponential in boundary size.
The general minimum T-join problem also admits polynomial matching methods.
See parity_closure.md for the imported theorem and exact probability scope.
"""
from functools import lru_cache
import math


def boundary(edges):
    """Odd-degree vertices of an undirected edge multiset (GF(2))."""
    odd = set()
    for a, b in edges:
        for v in (a, b):
            if v in odd:
                odd.remove(v)
            else:
                odd.add(v)
    return tuple(sorted(odd))


class PairClosure:
    def __init__(self, n, pairs):
        if not isinstance(n, int) or n < 1:
            raise ValueError('n must be a positive integer')
        self.n = n
        self.pairs = []
        self.distance = [[math.inf] * n for _ in range(n)]
        self.paths = [[None] * n for _ in range(n)]
        for v in range(n):
            self.distance[v][v] = 0.0
            self.paths[v][v] = ()
        for a, b, p in pairs:
            if not (isinstance(a, int) and isinstance(b, int)
                    and 0 <= a < n and 0 <= b < n and a != b):
                raise ValueError('pair endpoints must be distinct vertex indices')
            p = float(p)
            if not math.isfinite(p) or not 0 <= p <= 1:
                raise ValueError('pair bounds must be finite probabilities')
            i = len(self.pairs)
            self.pairs.append((a, b, p))
            if p < self.distance[a][b]:
                self.distance[a][b] = self.distance[b][a] = p
                self.paths[a][b] = self.paths[b][a] = (i,)
        for k in range(n):
            for a in range(n):
                for b in range(n):
                    candidate = self.distance[a][k] + self.distance[k][b]
                    if candidate < self.distance[a][b]:
                        self.distance[a][b] = candidate
                        self.paths[a][b] = self.paths[a][k] + self.paths[k][b]

    def certificate(self, target):
        target = tuple(sorted(target))
        if len(target) % 2 or len(set(target)) != len(target):
            raise ValueError('target must contain distinct, evenly many vertices')
        if any(not isinstance(v, int) or not 0 <= v < self.n for v in target):
            raise ValueError('invalid target vertex')

        @lru_cache(None)
        def match(mask):
            if not mask:
                return 0.0, ()
            first = (mask & -mask).bit_length() - 1
            rest = mask ^ (1 << first)
            best = math.inf, ()
            for other in range(first + 1, len(target)):
                if not rest & (1 << other):
                    continue
                cost, chosen = match(rest ^ (1 << other))
                candidate = cost + self.distance[target[first]][target[other]]
                if candidate < best[0]:
                    best = candidate, chosen + ((target[first], target[other]),)
            return best

        cost, matched = match((1 << len(target)) - 1)
        if math.isinf(cost):
            return dict(target=list(target), error_upper=1.0, join_weight=None,
                        pair_indices=[], matching=[], supported=False)
        used = set()
        for a, b in matched:
            for i in self.paths[a][b]:
                if i in used:
                    used.remove(i)
                else:
                    used.add(i)
        used = sorted(used)
        join_weight = sum(self.pairs[i][2] for i in used)
        assert boundary((self.pairs[i][:2] for i in used)) == target
        assert abs(join_weight - cost) <= 1e-9
        return dict(target=list(target), error_upper=min(1.0, join_weight),
                    join_weight=join_weight, pair_indices=used,
                    matching=[list(pair) for pair in matched], supported=True)

    def bound(self, target):
        return self.certificate(target)['error_upper']
