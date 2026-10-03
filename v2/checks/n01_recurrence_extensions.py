"""Exact finite probes for N01 recurrence B19-B27 and C5-C17.

Codex (GPT-6), October 3, 2026 UTC. These planning probes are not a native
producer. Finite enumerations corroborate, rather than replace, notebook
proofs over continuous parameters. Standard library and rational arithmetic.
"""

from fractions import Fraction as Q
from itertools import product
import json


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), Q(0))


def tail_cvar(losses, probabilities, alpha):
    """Independent upper-tail mass integration, including split atoms."""
    assert sum(probabilities) == 1 and 0 <= alpha < 1
    remaining = 1 - alpha
    total = Q(0)
    for loss, probability in sorted(zip(losses, probabilities), reverse=True):
        take = min(remaining, probability)
        total += take * loss
        remaining -= take
        if remaining == 0:
            break
    assert remaining == 0
    return total / (1 - alpha)


def threshold_cvar(losses, probabilities, alpha):
    return min(z + sum(p * max(loss - z, 0) for loss, p in
                       zip(losses, probabilities)) / (1 - alpha)
               for z in set(losses))


def parity_policies(cost=Q(3, 20)):
    """Execute each policy on each world; do not use derived value formulas."""
    worlds = list(product((0, 1), repeat=2))
    policies = {}
    for answer in (0, 1):
        policies[f"stop_{answer}"] = tuple(Q(answer != (x ^ y)) for x, y in worlds)
    for first in (0, 1):
        for branches in product((0, 1, "read"), repeat=2):
            losses = []
            for world in worlds:
                result = branches[world[first]]
                if result == "read":
                    losses.append(2 * cost)
                else:
                    losses.append(cost + Q(result != (world[0] ^ world[1])))
            policies[f"{first}_{branches}"] = tuple(losses)
    assert len(policies) == 20
    return policies


def distances(n, edges):
    """Floyd-Warshall; None denotes no path, and zero self paths are explicit."""
    d = [[Q(0) if i == j else None for j in range(n)] for i in range(n)]
    for u, v, w in edges:
        d[u][v] = w if d[u][v] is None else min(d[u][v], w)
    for k, i, j in product(range(n), repeat=3):
        if d[i][k] is not None and d[k][j] is not None:
            candidate = d[i][k] + d[k][j]
            if d[i][j] is None or candidate < d[i][j]:
                d[i][j] = candidate
    return d


def run():
    counts = {}
    # Convexity on each side of the active-bound kink proves that these
    # candidates are the complete continuum oracle for each tested s.
    for s in (Q(i, 120) for i in range(61)):
        xs = {Q(2, 3), Q(1), min(Q(1), max(Q(2, 3), 1 - s))}
        actual = max(2*x - 3 + 1/x + min(s, 1-x) for x in xs)
        formula = s*s/(1-s) if s <= Q(1, 4) else (
            s-Q(1, 6) if s <= Q(1, 3) else Q(1, 6))
        assert actual == formula
        node_actual = max(2*x-3+1/x+min(s, 1-x)
                          for x in (Q(2, 3), Q(5, 6), Q(1)))
        node_formula = max(Q(0), min(s, Q(1, 3))-Q(1, 6),
                           min(s, Q(1, 6))-Q(2, 15))
        assert node_actual == node_formula <= actual
        assert (node_actual <= Q(1, 20)) == (s <= Q(13, 60))
        assert (actual <= Q(1, 20)) == (s <= Q(1, 5))
    counts["amplitude_continuum_and_finite_grid_cases"] = 61

    # Actual fixed-grid error tables attain every endpoint contrast together.
    table_cases = 0
    for n, eta, slope in product((3, 6, 12), (Q(0), Q(1, 20), Q(1, 8)),
                                 (Q(0), Q(1, 8), Q(1))):
        e = [max(-eta, eta-slope*(1-Q(j, n))) for j in range(n+1)]
        assert all(abs(v) <= eta for v in e)
        assert all(abs(e[j+1]-e[j]) <= slope/n for j in range(n))
        assert all(e[-1]-e[j] == min(2*eta, slope*(1-Q(j, n)))
                   for j in range(n+1))
        table_cases += 1
    counts["simultaneous_finite_table_witnesses"] = table_cases

    # B22: validate constraints and potentials independently of closed bounds.
    for keep_a, keep_b in product((False, True), repeat=2):
        edges = [(7, j, Q(1, 8)) for j in range(7)]
        edges += [(j, 7, Q(1, 8)) for j in range(7)]
        edges += [(j, j+1, Q(1, 6)) for j in range(6)]
        edges += [(j+1, j, Q(1, 6)) for j in range(6)]
        if keep_a:
            edges.append((4, 6, Q(1, 5)))
        if keep_b:
            edges.append((4, 5, Q(1, 30)))
        d = distances(8, edges)
        assert all(d[j][j] == 0 for j in range(8))
        potential = [d[7][6]-d[j][6] for j in range(8)]
        assert potential[7] == 0
        assert all(potential[v]-potential[u] <= w for u, v, w in edges)
        assert all(potential[6]-potential[j] == d[j][6] for j in range(7))
        sharp = max(2*Q(j, 6)-3+1/Q(j, 6)+d[j][6] for j in (4, 5, 6))
        assert sharp == (Q(1, 30) if keep_a or keep_b else Q(1, 12))
    assert distances(2, [(0, 1, Q(-1)), (1, 0, Q(0))])[0][0] < 0
    counts["calibration_graph_presence_states"] = 4
    counts["calibration_graph_inconsistency_control"] = 1

    # B25's actual quality and comparative-loss bounds on rational contexts.
    for b in (Q(1, 9) + Q(7*i, 18*100) for i in range(101)):
        q = 1/(10*b)
        assert Q(0) <= q <= 1/(1+b) <= 1
        quality = 1-b*q+Q(1, 12)
        assert quality == Q(59, 60)
        regret = (1-b)*(q-1) + min(Q(1, 6), 1-q)
        assert regret <= Q(1, 50)
    counts["quality_policy_rational_context_checks"] = 101

    # B27: convergence of reports is insufficient with a discontinuous error.
    q = Q(1)
    for k in range(12):
        assert q == Q(2, 3) + Q(1, 3)*Q(1, 4)**k
        assert q > Q(2, 3)
        actual = 1-Q(1, 2)*q+Q(1, 2)*q+Q(1, 20)
        assert actual == Q(21, 20)
        q = (q + (1-q/2))/2
    assert Q(1)-Q(1, 20) == Q(19, 20)
    counts["discontinuous_calibration_execution_steps"] = 12

    # C5/C6: upper-tail integration is independent of the threshold formula.
    risk_cases = 0
    for t, alpha in product((Q(i, 20) for i in range(11)),
                            (Q(0), Q(1, 2), Q(3, 4), Q(9, 10))):
        values, probs = (Q(-1), Q(0), Q(1)), (t, 1-2*t, t)
        actual = tail_cvar(values, probs, alpha)
        assert actual == threshold_cvar(values, probs, alpha)
        if alpha >= Q(1, 2):
            assert actual == min(Q(1), t/(1-alpha))
        risk_cases += 1
    assert tail_cvar((Q(0), Q(1)), (Q(4, 5), Q(1, 5)), Q(3, 4)) == Q(4, 5)
    counts["tail_and_threshold_risk_comparisons"] = risk_cases + 1

    # C8-C11: simulate the actual update, rather than equilibrium identities.
    def raw(q, b, a):
        return tuple(max(Q(0), min(Q(1), a[i]-dot(b[i], q))) for i in range(2))

    bad_b = ((Q(1, 2), Q(2)), (Q(2), Q(1, 2)))
    for q in ((Q(2, 7), Q(2, 7)), (Q(2, 3), Q(0)), (Q(0), Q(2, 3))):
        assert raw(q, bad_b, (Q(1), Q(1))) == q
    assert raw((Q(0), Q(0)), bad_b, (Q(1), Q(1))) == (Q(1), Q(1))
    assert raw((Q(1), Q(1)), bad_b, (Q(1), Q(1))) == (Q(0), Q(0))
    b = ((Q(1), Q(1, 2)), (Q(1, 2), Q(1)))
    q = (Q(0), Q(0))
    for k in range(12):
        r = raw(q, b, (Q(1), Q(1)))
        actual_value = sum(r)+sum(q)/4
        assert actual_value-1 == Q(-1, 4)**k
        q = tuple(max(Q(0), min(Q(1), q[i]-(q[i]+dot(b[i], q)-1)/2))
                  for i in range(2))
    rotation = ((Q(0), Q(-1)), (Q(1), Q(0)))
    q = (Q(0), Q(0))
    visited = []
    for _ in range(4):
        visited.append(q)
        q = raw(q, rotation, (Q(0), Q(1)))
    assert len(set(visited)) == 4 and q == (Q(0), Q(0))
    counts["coupled_execution_controls"] = 6

    # C12-C14: direct edge inequalities and all binary version strings.
    h = (Q(3, 4), Q(0))
    assert 2-Q(5, 4) == h[0]-h[1]
    assert Q(1, 2)-Q(5, 4) == h[1]-h[0]
    switch_cases = 0
    for versions in product((0, 1), repeat=8):
        state, cost = 0, Q(0)
        potentials = ((Q(1), Q(0)), (Q(0), Q(1)))
        bound = potentials[versions[0]][state]
        switches = 0
        for t, version in enumerate(versions):
            if t and version != versions[t-1]:
                bound += potentials[version][state]-potentials[versions[t-1]][state]
                switches += 1
            target = 1-version
            step = Q(state != target)
            assert step == potentials[version][state]-potentials[version][target]
            cost += step
            state = target
        bound -= potentials[versions[-1]][state]
        assert cost == bound <= 1+switches
        switch_cases += 1
    counts["finite_execution_switch_sequences"] = switch_cases

    # C16-C17: execute all twenty policies and check risk by two algorithms.
    policies = parity_policies()
    pstar = (Q(9, 20), Q(1, 20), Q(1, 4), Q(1, 4))
    a_losses = (Q(3, 20), Q(23, 20), Q(3, 10), Q(3, 10))
    assert a_losses in policies.values()
    assert min(dot(l, pstar) for l in policies.values()) == Q(11, 40)
    assert all(dot(l, pstar) >= Q(3, 10) for l in policies.values() if l != a_losses)
    alphas = (Q(0), Q(1, 10), Q(1, 6), Q(1, 5), Q(9, 20), Q(9, 10))
    for alpha in alphas:
        risks = [tail_cvar(l, pstar, alpha) for l in policies.values()]
        assert risks == [threshold_cvar(l, pstar, alpha) for l in policies.values()]
        a_risk = tail_cvar(a_losses, pstar, alpha)
        assert min(risks) == (a_risk if alpha <= Q(1, 6) else Q(3, 10))
        if alpha <= Q(9, 20):
            assert a_risk == (Q(11, 40)-Q(3, 20)*alpha)/(1-alpha)
        for e, u in product((Q(0), Q(1, 40), Q(1, 20)),
                             (Q(1, 5), Q(1, 4), Q(3, 10))):
            p = (Q(1, 2)-e, e, u, Q(1, 2)-u)
            assert tail_cvar(a_losses, p, alpha) <= a_risk
        uniform = (Q(1, 4),)*4
        assert min(tail_cvar(l, uniform, alpha) for l in policies.values()) == Q(3, 10)
    assert dot(a_losses, (Q(0), Q(1, 2), Q(1, 4), Q(1, 4))) == Q(29, 40)
    counts["parity_policy_risk_comparisons"] = len(policies)*len(alphas)

    return {"status": "PASS", "scope": "finite exact planning probes, not F11",
            "counts": counts, "parity_mean_optimum": "11/40",
            "parity_risk_switch_alpha": "1/6"}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
