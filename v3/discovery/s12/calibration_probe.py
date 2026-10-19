"""s12 DEVELOPMENT: exact fixed-relation admission and acquisition accounting.

Codex (GPT-6). Stdlib only. This is finite arithmetic, not deployment evidence.
Run once; preserve this source and the resulting evidence unchanged.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import platform
import time


def maximum_marginal(n):
    return F(n ** n, (n + 1) ** (n + 1))


def graph_law(p, biased=False):
    """Return distribution of (error, alternative bill, direct bill).

    The first path's partner bit is inverted, so the complete circulation
    model is false on every assignment. The u-cut relation fails iff err=1.
    """
    out = defaultdict(F)
    for err in (0, 1):
        ep = p if err else 1 - p
        zs = [((err, err, err), F(1))] if biased else [
            (z, F(1, 8)) for z in product((0, 1), repeat=3)]
        for z, zp in zs:
            target = (sum(z) % 2) ^ err
            x = [target]
            for j in range(3):
                x.extend((z[j], z[j] ^ (j == 0)))
            edges = [(0, 1), (0, 2), (2, 1), (0, 3),
                     (3, 1), (0, 4), (4, 1)]
            syndrome = [0] * 5
            for bit, (u, v) in zip(x, edges):
                syndrome[u] ^= bit
                syndrome[v] ^= bit
            assert any(syndrome)
            assert ((sum(z) % 2) != target) == bool(err)
            # Separate H=2 episodes. Every marker differs from its data edge.
            alternative = sum(1 + bit for bit in z)
            direct = 100 + target
            assert alternative <= 6 and direct - alternative >= 94
            out[(err, alternative, direct)] += ep * zp
    assert sum(out.values()) == 1
    return [(state, prob) for state, prob in out.items() if prob]


def enumerate_service(law, n, m):
    risk = F(0)
    any_error = F(0)
    difference = F(0)
    cases = 0
    for sample in product(law, repeat=n + m):
        prob = F(1)
        for _, mass in sample:
            prob *= mass
        states = [state for state, _ in sample]
        admitted = all(state[0] == 0 for state in states[:n])
        # Training are requested tasks: exact route is owed by both methods.
        surcharge = sum(state[1] for state in states[:n])
        saving = sum(state[2] - state[1] for state in states[n:]) if admitted else 0
        risk += prob * (admitted and bool(states[n][0]))
        any_error += prob * (admitted and any(state[0] for state in states[n:]))
        difference += prob * (surcharge - saving)
        cases += 1
    return risk, any_error, difference, cases


def main():
    started = time.perf_counter()
    alpha, delta = F(1, 100), F(1, 20)
    n_marginal = next(n for n in range(1000) if maximum_marginal(n) <= alpha)
    n_confidence = next(n for n in range(1000) if (1 - alpha) ** n <= delta)
    assert n_marginal == 37 and n_confidence == 299
    assert maximum_marginal(36) > alpha
    assert F(99, 100) ** 298 > delta
    scenarios, assignments = 0, 0
    for biased in (False, True):
        for p in map(F, [0, F(1, 4), F(1, 2), F(3, 4), 1]):
            law = graph_law(p, biased)
            mu_a = sum(prob * s[1] for s, prob in law)
            mu_gap = sum(prob * (s[2] - s[1]) for s, prob in law)
            assert mu_a == (3 + 3 * p if biased else F(9, 2))
            assert mu_gap == (97 - 3 * p if biased else 96)
            for n in range(3):
                for m in (1, 2):
                    risk, any_error, difference, cases = enumerate_service(law, n, m)
                    admit = (1 - p) ** n
                    assert risk == p * admit
                    assert any_error == admit * (1 - (1 - p) ** m)
                    assert difference == n * mu_a - m * mu_gap * admit
                    assert risk <= maximum_marginal(n)
                    assert difference <= 6 * n - 94 * m * admit
                    scenarios += 1
                    assignments += cases
    # Extremal exchangeable error laws: exactly j errors, uniform positions.
    exchangeable = 0
    for n in range(8):
        for j in range(n + 2):
            patterns = [s for s in product((0, 1), repeat=n + 1) if sum(s) == j]
            risk = F(sum(not any(s[:n]) and s[n] for s in patterns), len(patterns))
            assert risk <= F(1, n + 1)
            if j == 1:
                assert risk == F(1, n + 1)
            exchangeable += 1
    break_even = []
    for n in (37, 299):
        conservative = next(m for m in range(100) if 6*n - 94*m < 0)
        fair_law = next(m for m in range(100) if F(9, 2)*n - 96*m < 0)
        break_even.append({"N": n, "conservative_future_tasks": conservative,
                           "fair_law_future_tasks": fair_law})
    assert [r["conservative_future_tasks"] for r in break_even] == [3, 20]
    assert [r["fair_law_future_tasks"] for r in break_even] == [2, 15]
    result = {
        "status": "PASS", "contributor": "Codex (GPT-6)",
        "scope": "DEVELOPMENT finite exact arithmetic; not population performance",
        "python": platform.python_version(), "marginal_1pct_N": n_marginal,
        "confidence_1pct_95pct_N": n_confidence,
        "iid_scenarios": scenarios, "iid_joint_assignments": assignments,
        "exchangeable_extreme_laws": exchangeable,
        "break_even_at_p_zero": break_even,
        "elapsed_seconds": time.perf_counter() - started,
    }
    Path(__file__).with_suffix('.json').write_text(
        json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
