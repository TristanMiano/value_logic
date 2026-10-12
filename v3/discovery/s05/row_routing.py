"""Cheap exact membership checks for the interval-row Kolmogorov source.

ChatGPT (GPT-6 Astra Pro), 2026-10-12. DEVELOPMENT. See value_routing.md.
The checker uses all interval cut conditions via a range-add/max sweep.
The small main probe compares it with an independent exact max-flow routine;
it does not evaluate new source rows or claim a new max-flow theorem.
"""
from collections import deque
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
from random import Random

from cdf_sweep import CDFSweep
from row_flow import RowFlow


class _RangeMaximum:
    def __init__(self, size):
        self.size = size
        self.maximum = [None] * (4*size)
        self.argument = [None] * (4*size)
        self.lazy = [F(0)] * (4*size)
        self.visits = 0

    def _apply(self, node, amount):
        if self.maximum[node] is not None:
            self.maximum[node] += amount
            self.lazy[node] += amount

    def _push(self, node):
        amount = self.lazy[node]
        if amount:
            self._apply(2*node, amount)
            self._apply(2*node+1, amount)
            self.lazy[node] = F(0)

    def _pull(self, node):
        children = [c for c in (2*node, 2*node+1)
                    if self.maximum[c] is not None]
        if not children:
            self.maximum[node] = self.argument[node] = None
            return
        child = max(children, key=lambda c: (self.maximum[c], -self.argument[c]))
        self.maximum[node] = self.maximum[child]
        self.argument[node] = self.argument[child]

    def activate(self, index, value):
        def visit(node, lo, hi):
            self.visits += 1
            if lo == hi:
                self.maximum[node] = value
                self.argument[node] = index
                self.lazy[node] = F(0)
                return
            self._push(node)
            mid = (lo+hi)//2
            if index <= mid:
                visit(2*node, lo, mid)
            else:
                visit(2*node+1, mid+1, hi)
            self._pull(node)
        visit(1, 0, self.size-1)

    def add(self, first, last, amount):
        if not amount:
            return
        def visit(node, lo, hi):
            self.visits += 1
            if first <= lo and hi <= last:
                self._apply(node, amount)
                return
            self._push(node)
            mid = (lo+hi)//2
            if first <= mid:
                visit(2*node, lo, mid)
            if last > mid:
                visit(2*node+1, mid+1, hi)
            self._pull(node)
        visit(1, 0, self.size-1)

    def largest(self):
        return self.maximum[1], self.argument[1]


class RowRouter:
    def __init__(self, size, intervals, epsilon, weights=None):
        # Reuse the source constructor's exact scope and input validation.
        source = RowFlow(size, intervals, epsilon, weights)
        self.size = source.size
        self.intervals = source.intervals
        self.epsilon = source.epsilon
        self.weights = source.weights
        self.ending = [[] for _ in range(size)]
        for (lo, hi), weight in zip(self.intervals, self.weights):
            self.ending[hi].append((lo, weight))

    def bands(self):
        """The pointwise CDF relaxation, retaining exact rational arithmetic."""
        lower, upper = [], []
        begins, ends = [F(0)]*self.size, [F(0)]*self.size
        for (lo, hi), weight in zip(self.intervals, self.weights):
            begins[lo] += weight
            ends[hi] += weight
        certain, possible = F(0), F(0)
        for j in range(self.size-1):
            certain += ends[j]
            possible += begins[j]
            lower.append(max(F(0), certain-self.epsilon))
            upper.append(min(F(1), possible+self.epsilon))
        return lower, upper

    def check(self, probability):
        p = tuple(map(F, probability))
        if len(p) != self.size or any(x < 0 for x in p) or sum(p) != 1:
            raise ValueError('A normalized nonnegative candidate is required')
        tree = _RangeMaximum(self.size)
        worst, witness = None, None
        trace = []
        for b in range(self.size):
            tree.activate(b, -self.epsilon*int(b > 0))
            for lo, weight in self.ending[b]:
                tree.add(0, lo, weight)
            tree.add(0, b, -p[b])
            value, a = tree.largest()
            deficit = value-self.epsilon*int(b < self.size-1)
            trace.append(dict(right=b, left=a, maximum_deficit=str(deficit)))
            if worst is None or deficit > worst:
                worst, witness = deficit, (a, b)
        a, b = witness
        forced = sum(w for (lo, hi), w in zip(self.intervals, self.weights)
                     if a <= lo and hi <= b)
        available = sum(p[a:b+1])+self.epsilon*(int(a > 0)+int(b < self.size-1))
        assert forced-available == worst
        return dict(feasible=worst <= 0, maximum_deficit=str(worst),
                    witness=dict(interval=[a, b], forced_mass=str(forced),
                                 available_mass=str(available)),
                    sweep=trace,
                    operations=dict(tree_node_visits=tree.visits,
                                    right_endpoints=self.size,
                                    row_prefix_updates=len(self.intervals),
                                    represented_intervals=self.size*(self.size+1)//2))

    def route(self, payoff):
        """Contract payoff plateaus, then certify each cheap extremum if possible.

        A failed candidate is inconclusive about equality of optimal values:
        a different cheap-layer optimizer may belong to the row source.
        """
        g = tuple(map(F, payoff))
        if len(g) != self.size:
            raise ValueError('One payoff per support point is required')
        compressed, mapping = [], []
        for value in g:
            if not compressed or value != compressed[-1]:
                compressed.append(value)
            mapping.append(len(compressed)-1)
        intervals = [(mapping[lo], mapping[hi]) for lo, hi in self.intervals]
        router = RowRouter(len(compressed), intervals, self.epsilon, self.weights)
        lower, upper = router.bands()
        answer = CDFSweep(lower, upper).interval(compressed)
        monotone = (all(a <= b for a, b in zip(compressed, compressed[1:]))
                    or all(a >= b for a, b in zip(compressed, compressed[1:])))
        interior = sum(w for (lo, hi), w in zip(intervals, self.weights)
                       if 0 < lo and hi < len(compressed)-1)
        equal_sources = interior <= 2*self.epsilon
        route = dict(lower=answer['lower'], upper=answer['upper'],
                     original_size=self.size, compressed_size=len(compressed),
                     mapping=mapping, compressed_payoff=list(map(str, compressed)),
                     compressed_intervals=list(map(list, intervals)),
                     monotone_payoff=monotone,
                     source_equality_certified_by_interior_mass=equal_sources,
                     interior_row_mass=str(interior),
                     cheap_certificates=answer)
        for side, key in (('lower', 'lower_certificate'),
                          ('upper', 'negative_upper_certificate')):
            if monotone or equal_sources:
                route[side+'_equality_certified'] = True
                route[side+'_route'] = 'monotone' if monotone else 'interior_mass'
            else:
                check = router.check(answer[key]['probability'])
                route[side+'_equality_certified'] = check['feasible']
                route[side+'_route'] = 'candidate_membership'
                route[side+'_membership'] = check
        return route


def _all_interval_deficits(router, probability):
    p = list(map(F, probability))
    return max(sum(w for (lo, hi), w in zip(router.intervals, router.weights)
                   if a <= lo and hi <= b)
               - sum(p[a:b+1])
               - router.epsilon*(int(a > 0)+int(b < router.size-1))
               for a in range(router.size) for b in range(a, router.size))


def _fixed_probability_maxflow(router, probability):
    """Independent small exact BFS augmentations with fixed sink capacities."""
    source = RowFlow(router.size, router.intervals, router.epsilon, router.weights)
    arcs = source.arcs([F(0)]*router.size)
    capacities = [dict() for _ in range(source.nodes)]
    p = list(map(F, probability))
    for u, v, capacity, cost in arcs:
        if v == source.sink:
            capacity = p[u-source.state_start]
        capacities[u][v] = capacities[u].get(v, F(0))+capacity
        capacities[v].setdefault(u, F(0))
    total = F(0)
    while True:
        previous = {source.source: None}
        queue = deque([source.source])
        while queue and source.sink not in previous:
            u = queue.popleft()
            for v, capacity in capacities[u].items():
                if capacity > 0 and v not in previous:
                    previous[v] = u
                    queue.append(v)
        if source.sink not in previous:
            break
        path, v = [], source.sink
        while previous[v] is not None:
            u = previous[v]
            path.append((u, v))
            v = u
        amount = min(capacities[u][v] for u, v in path)
        for u, v in path:
            capacities[u][v] -= amount
            capacities[v][u] += amount
        total += amount
    return total


def main():
    cases = []
    for epsilon in (F(0), F(1, 8), F(1, 4)):
        cases.append((3, [(0, 2), (1, 1)], epsilon, None,
                      [F(1, 2), F(0), F(1, 2)]))
    rng = Random(5012)
    for _ in range(21):
        size, rows = rng.randint(2, 5), rng.randint(2, 4)
        intervals = [tuple(sorted((rng.randrange(size), rng.randrange(size))))
                     for _ in range(rows)]
        masses = [rng.randint(1, 4) for _ in range(rows)]
        weights = [F(x, sum(masses)) for x in masses]
        cells = [rng.randint(0, 4) for _ in range(size)]
        if not any(cells):
            cells[0] = 1
        p = [F(x, sum(cells)) for x in cells]
        epsilon = rng.choice((F(0), F(1, 8), F(1, 3)))
        cases.append((size, intervals, epsilon, weights, p))
    feasibility = []
    for size, intervals, epsilon, weights, p in cases:
        router = RowRouter(size, intervals, epsilon, weights)
        answer = router.check(p)
        deficit = _all_interval_deficits(router, p)
        flow = _fixed_probability_maxflow(router, p)
        assert F(answer['maximum_deficit']) == deficit
        assert answer['feasible'] == (flow == 1)
        feasibility.append(dict(size=size, intervals=list(map(list, intervals)),
                                weights=list(map(str, router.weights)),
                                epsilon=str(epsilon), probability=list(map(str, p)),
                                answer=answer, exact_maxflow=str(flow)))

    examples = [
        (3, [(0, 2), (1, 1)], F(0), [0, 1, 2]),
        (3, [(0, 2), (1, 1)], F(0), [0, 1, 0]),
        (3, [(0, 2), (1, 1)], F(1, 8), [0, 1, 0]),
        (5, [(0, 4), (1, 3)], F(0), [0, 1, 1, 1, 0]),
        (5, [(0, 3), (1, 4)], F(0), [2, -1, -1, 3, 0]),
        (5, [(0, 4), (2, 2)], F(1, 2), [1, 0, 0, 2, -1]),
    ]
    routing = []
    for size, intervals, epsilon, g in examples:
        router = RowRouter(size, intervals, epsilon)
        routed = router.route(g)
        exact = RowFlow(size, intervals, epsilon).interval(g)
        coarse = RowFlow(routed['compressed_size'], routed['compressed_intervals'],
                         epsilon).interval(routed['compressed_payoff'])
        assert exact['lower'] == coarse['lower']
        assert exact['upper'] == coarse['upper']
        for side in ('lower', 'upper'):
            if routed[side+'_equality_certified']:
                assert routed[side] == exact[side]
        routing.append(dict(intervals=list(map(list, intervals)), epsilon=str(epsilon),
                            payoff=g, route=routed,
                            exact_row_interval=[exact['lower'], exact['upper']],
                            exact_compressed_interval=[coarse['lower'], coarse['upper']]))

    directory = Path(__file__).resolve().parent
    dependencies = [Path(__file__).resolve(), directory/'row_flow.py',
                    directory/'cdf_sweep.py']
    result = dict(status='DEVELOPMENT', contributor='ChatGPT (GPT-6 Astra Pro)',
                  command=['python', 'v3/discovery/s05/row_routing.py'],
                  new_source_evaluations=0,
                  scope='Exact interval-row source only; proposed-candidate rejection '
                        'does not establish an optimal-value gap. Synthetic checks '
                        'are not a confirmation campaign.',
                  sources={str(p.relative_to(directory.parent.parent.parent)):
                           hashlib.sha256(p.read_bytes()).hexdigest() for p in dependencies},
                  feasibility_cases=len(feasibility), routing_cases=len(routing),
                  feasibility=feasibility, routing=routing)
    target = directory/'row_routing_results.json'
    target.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(feasibility_cases=len(feasibility),
                          routing_cases=len(routing),
                          certified_endpoints=sum(x['route'][side+'_equality_certified']
                                                  for x in routing for side in ('lower', 'upper')),
                          output=str(target.relative_to(directory.parent.parent.parent)))))


if __name__ == '__main__':
    main()
