"""Exact small-network values retaining censored row intervals.

ChatGPT (GPT-6 Astra Pro), 2026-10-12. DEVELOPMENT. See row_flow.md.
Successive shortest augmentations use rational Bellman-Ford; final primal
flow and residual potentials are independently checkable. This is a small
reference implementation, not a strongly polynomial or tuned solver.
"""
from fractions import Fraction as F


class RowFlow:
    def __init__(self, size, intervals, epsilon, weights=None):
        if not isinstance(size, int) or size < 1:
            raise ValueError('Positive support size required')
        self.size = size
        self.intervals = tuple(tuple(pair) for pair in intervals)
        if not self.intervals:
            raise ValueError('At least one retained row is required')
        for lo, hi in self.intervals:
            if not isinstance(lo, int) or not isinstance(hi, int) or not 0 <= lo <= hi < size:
                raise ValueError('Invalid retained interval')
        self.epsilon = F(epsilon)
        if not 0 <= self.epsilon <= 1:
            raise ValueError('Radius outside [0,1]')
        if weights is None:
            weights = [F(1, len(self.intervals))]*len(self.intervals)
        self.weights = tuple(map(F, weights))
        if (len(self.weights) != len(self.intervals)
                or any(w < 0 for w in self.weights) or sum(self.weights) != 1):
            raise ValueError('Invalid row weights')
        self.source = 0
        self.row_start = 1
        self.state_start = self.row_start + len(self.intervals)
        self.sink = self.state_start + size
        self.nodes = self.sink + 1

    def arcs(self, payoff):
        g = tuple(map(F, payoff))
        if len(g) != self.size:
            raise ValueError('One payoff per support point required')
        arcs = []
        for i, ((lo, hi), weight) in enumerate(zip(self.intervals, self.weights)):
            row = self.row_start+i
            arcs.append((self.source, row, weight, F(0)))
            for h in range(lo, hi+1):
                arcs.append((row, self.state_start+h, weight, F(0)))
        for h in range(self.size-1):
            a, b = self.state_start+h, self.state_start+h+1
            arcs.extend(((a, b, self.epsilon, F(0)),
                         (b, a, self.epsilon, F(0))))
        for h, value in enumerate(g):
            arcs.append((self.state_start+h, self.sink, F(1), value))
        return arcs

    def minimum(self, payoff):
        arcs = self.arcs(payoff)
        flow = [F(0)]*len(arcs)
        sent = F(0)
        augmentations = relaxations = 0

        def residual():
            edges = []
            for index, ((u, v, cap, cost), used) in enumerate(zip(arcs, flow)):
                if used < cap:
                    edges.append((u, v, cap-used, cost, index, 1))
                if used > 0:
                    edges.append((v, u, used, -cost, index, -1))
            return edges

        while sent < 1:
            edges = residual()
            distance = [None]*self.nodes
            distance[self.source] = F(0)
            previous = [None]*self.nodes
            for iteration in range(self.nodes):
                changed = False
                for edge in edges:
                    u, v, cap, cost, index, direction = edge
                    if distance[u] is None:
                        continue
                    proposal = distance[u] + cost
                    if distance[v] is None or proposal < distance[v]:
                        distance[v] = proposal
                        previous[v] = edge
                        changed = True
                        relaxations += 1
                if not changed:
                    break
                if iteration == self.nodes-1:
                    raise ArithmeticError('Negative residual cycle in augmentation')
            if distance[self.sink] is None:
                raise ArithmeticError('Required unit flow became infeasible')
            path, seen = [], set()
            node = self.sink
            while node != self.source:
                if node in seen or previous[node] is None:
                    raise ArithmeticError('Invalid shortest-path predecessor chain')
                seen.add(node)
                edge = previous[node]
                path.append(edge)
                node = edge[0]
            amount = min(1-sent, *(edge[2] for edge in path))
            for u, v, cap, cost, index, direction in path:
                flow[index] += direction*amount
            sent += amount
            augmentations += 1

        # Distances from an implicit zero-cost supersource to all vertices
        # furnish a reduced-cost certificate on every residual component.
        potentials = [F(0)]*self.nodes
        edges = residual()
        for iteration in range(self.nodes):
            changed = False
            for u, v, cap, cost, index, direction in edges:
                proposal = potentials[u]+cost
                if proposal < potentials[v]:
                    potentials[v] = proposal
                    changed = True
                    relaxations += 1
            if not changed:
                break
            if iteration == self.nodes-1:
                raise ArithmeticError('Final flow has a negative residual cycle')
        value = sum(used*cost for used, (_, _, _, cost) in zip(flow, arcs))
        q, p = [F(0)]*self.size, [F(0)]*self.size
        for used, (u, v, cap, cost) in zip(flow, arcs):
            if self.row_start <= u < self.state_start and self.state_start <= v < self.sink:
                q[v-self.state_start] += used
            if self.state_start <= u < self.sink and v == self.sink:
                p[u-self.state_start] += used
        answer = dict(value=str(value), flow=list(map(str, flow)),
                      potentials=list(map(str, potentials)),
                      empirical_mixture=list(map(str, q)), probability=list(map(str, p)),
                      nodes=self.nodes, arcs=len(arcs), augmentations=augmentations,
                      relaxations=relaxations)
        if not self.verify(payoff, answer):
            raise ArithmeticError('Exact final certificate rejected')
        return answer

    def verify(self, payoff, answer):
        arcs = self.arcs(payoff)
        flow, potentials = list(map(F, answer['flow'])), list(map(F, answer['potentials']))
        if len(flow) != len(arcs) or len(potentials) != self.nodes:
            return False
        balance = [F(0)]*self.nodes
        value = F(0)
        for used, (u, v, cap, cost) in zip(flow, arcs):
            if not 0 <= used <= cap:
                return False
            balance[u] -= used
            balance[v] += used
            value += used*cost
            reduced = cost+potentials[u]-potentials[v]
            if (used < cap and reduced < 0) or (used > 0 and reduced > 0):
                return False
        return (value == F(answer['value'])
                and balance[self.source] == -1 and balance[self.sink] == 1
                and all(balance[j] == 0 for j in range(1, self.sink)))

    def interval(self, payoff):
        g = tuple(map(F, payoff))
        low = self.minimum(g)
        negative = self.minimum(tuple(-v for v in g))
        return dict(lower=low['value'], upper=str(-F(negative['value'])),
                    lower_certificate=low, negative_upper_certificate=negative)
