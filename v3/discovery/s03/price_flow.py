"""Expose bit-side min-cut witnesses; separate revision of flow_v2.exact."""
from collections import deque
from fractions import Fraction as F
from flow_v2 import scaled


def exact(terms, prices):
    den, demands, caps, supports = scaled(terms, prices)
    n, m = len(terms), len(prices)
    s = n + m; t = s + 1
    adj = [[] for _ in range(t + 1)]; edges = []; incidences = []
    def add(u, v, c):
        k = len(edges); edges.extend([[u, v, c], [v, u, 0]])
        adj[u].append(k); adj[v].append(k + 1); return k
    for e, d in enumerate(demands): add(s, e, d)
    big = 1 + sum(demands)
    for e, row in enumerate(supports):
        for i in row: incidences.append((e, i, add(e, n + i, big)))
    for i, c in enumerate(caps): add(n + i, t, c)
    while True:
        level = [-1] * (t + 1); level[s] = 0; queue = deque([s])
        while queue:
            u = queue.popleft()
            for k in adj[u]:
                _, v, c = edges[k]
                if c and level[v] < 0: level[v] = level[u] + 1; queue.append(v)
        if level[t] < 0: break
        current = [0] * (t + 1)
        def push(u, limit):
            if u == t: return limit
            while current[u] < len(adj[u]):
                k = adj[u][current[u]]; _, v, c = edges[k]
                if c and level[v] == level[u] + 1:
                    amount = push(v, min(c, limit))
                    if amount:
                        edges[k][2] -= amount; edges[k ^ 1][2] += amount
                        return amount
                current[u] += 1
            return 0
        while push(s, big): pass
    allocation = [(e, i, F(edges[k ^ 1][2], den)) for e, i, k in incidences if edges[k ^ 1][2]]
    bits = sum(1 << i for i in range(m) if level[n + i] >= 0)
    reward = sum((r for mask, r in terms if mask & bits == mask), F(0))
    cost = sum((q for i, q in enumerate(prices) if bits >> i & 1), F(0))
    value = reward - cost
    assert sum((r for _, r in terms), F(0)) - sum((a for _, _, a in allocation), F(0)) == value
    return allocation, dict(bits=bits, value=value)
