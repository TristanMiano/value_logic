#!/usr/bin/env python3
"""P3-02 DEVELOPMENT: exact finite probability-information probes.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-07.
This small rational vertex enumerator is an independent arithmetic probe, not
a replacement for the unchanged native kernel or a general LP service. Every
reported extremum has a feasible endpoint and an independently rechecked
nonnegative-multiplier upper certificate. Only explicit compact polytopes with
independent equality rows are admitted by these fixtures.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction as Q
import hashlib
from itertools import combinations
import json
from pathlib import Path
import platform
import resource
import time


def dot(a, b):
    if len(a) != len(b):
        raise ValueError("Vector dimensions differ.")
    return sum((x * y for x, y in zip(a, b)), Q(0))


def matrix(rows):
    return tuple(tuple(Q(x) for x in row) for row in rows)


def solve_square(rows, rhs):
    """Exact Gauss-Jordan solve; singular systems have no returned solution."""
    n = len(rows)
    if len(rhs) != n or any(len(row) != n for row in rows):
        raise ValueError("A square coefficient system is required.")
    a = [[Q(x) for x in row] + [Q(b)] for row, b in zip(rows, rhs)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j]), None)
        if pivot is None:
            return None
        a[j], a[pivot] = a[pivot], a[j]
        factor = a[j][j]
        a[j] = [x / factor for x in a[j]]
        for i in range(n):
            if i != j and a[i][j]:
                factor = a[i][j]
                a[i] = [x - factor * y for x, y in zip(a[i], a[j])]
    return tuple(row[-1] for row in a)


def simplex_rows(n, start=0, width=None):
    width = width or n
    one = [Q(0)] * width
    nonnegative = []
    for i in range(start, start + n):
        one[i] = Q(1)
        row = [Q(0)] * width
        row[i] = Q(-1)
        nonnegative.append(tuple(row))
    return tuple(one), tuple(nonnegative)


def feasible(x, a, b, h, g):
    return all(dot(row, x) == value for row, value in zip(a, b)) and all(
        dot(row, x) <= value for row, value in zip(h, g)
    )


def vertices(a, b, h, g):
    """Enumerate bases of a declared compact polytope, retaining exact points."""
    a, h = matrix(a), matrix(h)
    b, g = tuple(map(Q, b)), tuple(map(Q, g))
    n = len(a[0] if a else h[0])
    if len(a) > n or len(a) != len(b) or len(h) != len(g):
        raise ValueError("Malformed fixture constraints.")
    points = set()
    for active in combinations(range(len(h)), n - len(a)):
        rows = a + tuple(h[i] for i in active)
        rhs = b + tuple(g[i] for i in active)
        x = solve_square(rows, rhs)
        if x is not None and feasible(x, a, b, h, g):
            points.add(x)
    return tuple(sorted(points))


def verify_upper_certificate(c, a, b, h, g, lam, mu, value):
    """Arithmetic-only verifier; it does not inspect a vertex search result."""
    n = len(c)
    if len(lam) != len(a) or len(mu) != len(h) or any(v < 0 for v in mu):
        return False
    combined = tuple(
        sum((lam[i] * a[i][j] for i in range(len(a))), Q(0))
        + sum((mu[i] * h[i][j] for i in range(len(h))), Q(0))
        for j in range(n)
    )
    return combined == tuple(c) and dot(lam, b) + dot(mu, g) == value


def maximum(c, a, b, h, g, points=None):
    c, a, b, h, g = tuple(map(Q, c)), matrix(a), tuple(map(Q, b)), matrix(h), tuple(map(Q, g))
    points = vertices(a, b, h, g) if points is None else points
    if not points:
        raise ValueError("No feasible vertex; these fixtures require a nonempty compact source.")
    value, witness = max((dot(c, p), p) for p in points)
    active = [i for i, row in enumerate(h) if dot(row, witness) == g[i]]
    n = len(c)
    for indices in combinations(active, n - len(a)):
        basis = a + tuple(h[i] for i in indices)
        weights = solve_square(tuple(zip(*basis)), c)
        if weights is None or any(w < 0 for w in weights[len(a):]):
            continue
        lam = weights[:len(a)]
        mu = [Q(0)] * len(h)
        for index, weight in zip(indices, weights[len(a):]):
            mu[index] = weight
        if verify_upper_certificate(c, a, b, h, g, lam, mu, value):
            assert feasible(witness, a, b, h, g)
            assert dot(c, witness) == value
            return {
                "value": value, "witness": witness,
                "equalities": a, "equality_rhs": b,
                "inequalities": h, "inequality_rhs": g,
                "objective": c, "lambda": lam, "mu": tuple(mu),
                "dual_certificate_valid": True,
            }
    raise AssertionError("No matching checked dual certificate for the proposed optimum.")


def interval(c, a, b, h, g):
    points = vertices(a, b, h, g)
    upper = maximum(c, a, b, h, g, points)
    neg = maximum(tuple(-Q(x) for x in c), a, b, h, g, points)
    return {"lower": -neg["value"], "upper": upper["value"],
            "lower_via_negation": neg, "upper_certificate": upper,
            "vertex_count": len(points)}


def sharp_probability_and_dependence():
    one, nonnegative = simplex_rows(3)
    result = interval((0, 0, 1), (one, (0, 1, 2)), (1, Q(1, 2)), nonnegative, (0, 0, 0))
    assert (result["lower"], result["upper"]) == (0, Q(1, 4))
    # The target is uncertain but a 3/10 fallback is worse throughout the fiber.
    assert result["upper"] < Q(3, 10)
    assert result["lower"] < Q(1, 8) < result["upper"]
    one4, n4 = simplex_rows(4)
    marginals = (one4, (0, 0, 1, 1), (0, 1, 0, 1))
    joint = interval((0, 1, 1, 1), marginals, (1, Q(1, 2), Q(1, 2)), n4, (0,) * 4)
    assert (joint["lower"], joint["upper"]) == (Q(1, 2), 1)
    # State order (K=1,A), (K=1,not A), (K=3,A), (K=3,not A).
    stake = interval((1, 0, 1, 0), (one4, (1, 1, 0, 0), (1, 0, 3, 0)),
                     (1, Q(1, 2), 1), n4, (0,) * 4)
    assert (stake["lower"], stake["upper"]) == (Q(1, 3), Q(2, 3))
    return {"singleton": result, "missing_joint_dependence": joint, "known_random_stakes": stake}


def brier_row(q):
    q = tuple(map(Q, q))
    n = len(q)
    assert sum(q) == 1 and min(q) >= 0
    return tuple(sum((q[j] - int(i == j)) ** 2 for j in range(n)) for i in range(n))


def score_calibration():
    n = 3
    uniform = (Q(1, n),) * n
    reports = (uniform,) + tuple(tuple(Q(int(i == j)) for i in range(n)) for j in range(n))
    rows = tuple(brier_row(q) for q in reports)
    difference = tuple(tuple(x - z for x, z in zip(row, rows[0])) for row in rows[1:])
    law, scale, offset = (Q(1, 6), Q(1, 3), Q(1, 2)), Q(3), Q(5)
    values = tuple(offset + scale * dot(row, law) for row in rows)
    assert values == (7, 10, 9, 8)
    lifted = solve_square(difference, tuple(v - values[0] for v in values[1:]))
    assert lifted is not None
    decoded_scale = sum(lifted)
    decoded = tuple(x / decoded_scale for x in lifted)
    decoded_offset = values[0] - dot(rows[0], lifted)
    assert (decoded, decoded_scale, decoded_offset) == (law, scale, offset)
    realized_decodings = []
    for outcome in range(n):
        transcript = tuple(offset + scale * row[outcome] for row in rows)
        x = solve_square(difference, tuple(v - transcript[0] for v in transcript[1:]))
        p = tuple(z / sum(x) for z in x)
        expected = tuple(Q(int(i == outcome)) for i in range(n))
        assert p == expected
        realized_decodings.append({"outcome": outcome, "raw_scores": transcript, "decoded_empirical_law": p})
    return {"reports": reports, "loss_rows": rows, "risk_values": values,
            "recovered_law": decoded, "recovered_scale": decoded_scale,
            "recovered_offset": decoded_offset,
            "semantic_hostile_case": realized_decodings}


def noisy_scale_interval():
    # x=s*p, unknown common positive s; observed vector (2,1).
    h = ((-1, 0), (1, 0), (0, -1), (0, 1))
    g = (-Q(3, 2), Q(5, 2), -Q(3, 4), Q(5, 4))
    points = vertices((), (), h, g)
    ratios = tuple((p[0] / sum(p), p) for p in points)
    lower, upper = min(ratios), max(ratios)
    assert lower[0] == Q(6, 11) and upper[0] == Q(10, 13)
    low_cert = maximum((-5, 6), (), (), h, g, points)
    high_cert = maximum((3, -10), (), (), h, g, points)
    assert low_cert["value"] == high_cert["value"] == 0
    midpoint = (lower[0] + upper[0]) / 2
    radius = (upper[0] - lower[0]) / 2
    normalized_observation = Q(2, 3)
    naive_error = max(normalized_observation - lower[0], upper[0] - normalized_observation)
    assert (midpoint, radius, naive_error) == (Q(94, 143), Q(16, 143), Q(4, 33))
    assert naive_error > radius
    # Feasible scale is bounded away from zero by the original value constraints.
    scale_bounds = interval((1, 1), (), (), h, g)
    assert scale_bounds["lower"] == Q(9, 4)
    known_scale = interval((Q(1, 3), 0), ((1, 1),), (3,), h, g)
    assert (known_scale["lower"], known_scale["upper"]) == (Q(7, 12), Q(3, 4))
    return {"lower_endpoint": lower, "upper_endpoint": upper,
            "ratio_lower_affine_certificate": low_cert,
            "ratio_upper_affine_certificate": high_cert,
            "scale_bounds": scale_bounds, "midpoint": midpoint, "radius": radius,
            "normalized_observation": normalized_observation,
            "normalization_worst_error": naive_error,
            "separately_known_scale_three": known_scale}


def jsonable(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, dict):
        return {key: jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [jsonable(item) for item in value]
    return value


def run():
    return {
        "status": "DEVELOPMENT", "passed": True,
        "contributor": "ChatGPT (GPT-6 Astra Pro)",
        "scope": "Finite rational fixtures; exact vertices plus independently checked dual arithmetic; no final challenge.",
        "sharp_probability_and_dependence": sharp_probability_and_dependence(),
        "score_calibration": score_calibration(),
        "noisy_scale_interval": noisy_scale_interval(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("Preserve the existing run; choose an explicitly recorded new development run path.")
    started_utc = datetime.now(timezone.utc).isoformat()
    started_ns = time.monotonic_ns()
    usage_before = resource.getrusage(resource.RUSAGE_SELF)
    result = run()
    ended_ns = time.monotonic_ns()
    usage_after = resource.getrusage(resource.RUSAGE_SELF)
    result["execution"] = {
        "started_utc": started_utc, "ended_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_ns": ended_ns - started_ns,
        "cpu_user_seconds": usage_after.ru_utime - usage_before.ru_utime,
        "cpu_system_seconds": usage_after.ru_stime - usage_before.ru_stime,
        "python": platform.python_version(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(jsonable(result), indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "DEVELOPMENT", "passed": True, "output": str(args.output),
                      "elapsed_ns": result["execution"]["elapsed_ns"]}))


if __name__ == "__main__":
    main()
