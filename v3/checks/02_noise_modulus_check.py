#!/usr/bin/env python3
"""P3-02 DEVELOPMENT: exact noise-modulus and coherent-center checks.

Prospective question: when is inverse-matrix error amplification sharp over
the entire normalized probability source, and when do source constraints make
it strictly loose? Fourteen rational regimes were selected to cover zero rank,
zero error, inverse-limited, source-limited and saturated cases, not a held-out
challenge. The formula and matching laws are proved separately in the review.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import resource
import time


HERE = Path(__file__).resolve().parent
DEPENDENCY = HERE / "02_probability_checks.py"
spec = importlib.util.spec_from_file_location("p3_02_exact_probability_probe", DEPENDENCY)
K = importlib.util.module_from_spec(spec)
spec.loader.exec_module(K)


def conditioning_case(delta, epsilon):
    delta, epsilon = Q(delta), Q(epsilon)
    assert delta >= 0 and epsilon >= 0
    l = ((Q(0), Q(1), Q(1)), (Q(0), Q(1), 1 + delta))
    one_p, np = K.simplex_rows(3, 0, 6)
    one_q, nq = K.simplex_rows(3, 3, 6)
    a, b = (one_p, one_q), (Q(1), Q(1))
    h, g = list(np + nq), [Q(0)] * 6
    for row in l:
        difference = tuple(row) + tuple(-x for x in row)
        h.extend((difference, tuple(-x for x in difference)))
        g.extend((2 * epsilon, 2 * epsilon))
    c = (Q(0), Q(0), Q(1), Q(0), Q(0), Q(-1))
    result = K.maximum(c, a, b, h, g)
    r = (Q(1) if delta == 0 else
         min(Q(1), 4 * epsilon / delta, (1 + 2 * epsilon) / (1 + delta)))
    assert result["value"] == r
    t = min(Q(0), 2 * epsilon - delta * r)
    p, q = (-t, 1 - r + t, r), (Q(0), Q(1), Q(0))
    assert min(p) >= 0 and sum(p) == 1
    lp, lq = tuple(K.dot(row, p) for row in l), tuple(K.dot(row, q) for row in l)
    shared = tuple((x + y) / 2 for x, y in zip(lp, lq))
    ep, eq = tuple(z - x for z, x in zip(shared, lp)), tuple(z - x for z, x in zip(shared, lq))
    assert all(abs(x) <= epsilon for x in ep + eq)
    assert p[2] - q[2] == r
    naive = Q(1, 2) if delta == 0 else min(Q(1, 2), 2 * epsilon / delta)
    assert r / 2 <= naive
    return {"delta": delta, "epsilon": epsilon, "radius": r / 2,
            "clipped_inverse_bound": naive, "inverse_bound_is_loose": r / 2 < naive,
            "exact_pair_lp": result, "analytic_matching_pair": (p, q),
            "shared_observation": shared, "paired_errors": (ep, eq)}


def coherent_centers():
    # Variables q1,q2,q3,r; source Delta_3 and 0<=r<=1 makes the LP compact.
    one, nq = K.simplex_rows(3, 0, 4)
    h = list(nq) + [(0, 0, 0, -1), (0, 0, 0, 1)]
    g = [Q(0)] * 4 + [Q(1)]
    for i in range(3):
        low, high = [Q(0)] * 4, [Q(0)] * 4
        low[i], low[3] = Q(1), Q(-1)
        high[i], high[3] = Q(-1), Q(-1)
        h.extend((tuple(low), tuple(high)))
        g.extend((Q(0), Q(-1)))
    cert = K.maximum((0, 0, 0, -1), (one,), (1,), h, g)
    assert cert["value"] == -Q(2, 3)
    assert cert["witness"] == (Q(1, 3), Q(1, 3), Q(1, 3), Q(2, 3))
    midpoint = (Q(1, 2),) * 3
    assert sum(midpoint) != 1
    # Scalar p1 can attain its midpoint with a compatible law.
    scalar_midpoint_law = (Q(1, 2), Q(1, 2), Q(0))
    assert min(scalar_midpoint_law) >= 0 and sum(scalar_midpoint_law) == 1
    return {"unrestricted_vector_center": midpoint, "unrestricted_radius": Q(1, 2),
            "compatible_radius": Q(2, 3), "compatible_center_certificate": cert,
            "scalar_target_midpoint_law": scalar_midpoint_law,
            "attribution": "Generic midpoint/compatible-center machinery and related simplex gaps are inherited phase-two reconstructions."}


def correlated_errors_and_incoherence():
    # p1,p2,b; an actual common bias, not an independent error box.
    a = ((1, 1, 0), (1, 0, 1), (0, 1, 1))
    b = (Q(1), Q(1, 2), Q(1, 2))
    h = ((-1, 0, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
    g = (Q(0), Q(0), Q(1, 4), Q(1, 4))
    joint = K.interval((1, 0, 0), a, b, h, g)
    assert joint["lower"] == joint["upper"] == Q(1, 2)
    one, nn = K.simplex_rows(2)
    box_h = nn + ((1, 0), (-1, 0), (0, 1), (0, -1))
    box_g = (Q(0), Q(0), Q(3, 4), -Q(1, 4), Q(3, 4), -Q(1, 4))
    box = K.interval((1, 0), (one,), (1,), box_h, box_g)
    assert (box["lower"], box["upper"]) == (Q(1, 4), Q(3, 4))
    # Incoherent observation (.9,.9) with .1 errors implies p_i>=.8.
    bad_h = nn + ((-1, 0), (0, -1))
    bad_g = (Q(0), Q(0), -Q(4, 5), -Q(4, 5))
    assert K.vertices((one,), (1,), bad_h, bad_g) == ()
    # The original-row certificate is 1*(p1+p2=1) plus both lower rows.
    contradiction = K.verify_upper_certificate(
        (Q(0), Q(0)), (one,), (Q(1),), K.matrix(bad_h), bad_g,
        (Q(1),), (Q(0), Q(0), Q(1), Q(1)), -Q(3, 5))
    assert contradiction
    rejected = False
    try:
        K.maximum((1, 0), (one,), (1,), bad_h, bad_g)
    except ValueError:
        rejected = True
    assert rejected
    # A negative inequality multiplier is not a sound upper-bound witness.
    invalid_multiplier_accepted = K.verify_upper_certificate(
        (Q(1),), (), (), ((Q(-1),),), (Q(0),), (), (Q(-1),), Q(0))
    assert not invalid_multiplier_accepted
    return {"actual_common_bias_interval": joint, "rectangularized_interval": box,
            "incoherent_observation_has_no_fiber": True,
            "infeasibility_certificate_zero_le_minus_three_fifths": contradiction,
            "empty_source_refused_by_extremum_producer": rejected,
            "negative_multiplier_accepted": invalid_multiplier_accepted}


def run():
    regimes = ((0, 0), (0, Q(1, 10)),
               (Q(1, 100), 0), (Q(1, 100), Q(1, 10000)), (Q(1, 100), Q(1, 100)),
               (1, Q(1, 10)), (1, Q(2, 5)), (1, Q(1, 2)),
               (2, Q(1, 10)), (2, Q(2, 5)), (2, 1),
               (10, Q(1, 10)), (10, Q(2, 5)), (10, 1))
    return {"status": "DEVELOPMENT", "passed": True,
            "contributor": "ChatGPT (GPT-6 Astra Pro)",
            "scope": "Fourteen exact finite noise regimes and two source/coherence boundaries; no final evaluation.",
            "conditioning_regimes": [conditioning_case(d, e) for d, e in regimes],
            "coherent_centers": coherent_centers(),
            "correlation_and_incoherence": correlated_errors_and_incoherence()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("Preserve existing development output; record a distinct run if needed.")
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
        "dependencies": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in (Path(__file__), DEPENDENCY)}}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(K.jsonable(result), indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "DEVELOPMENT", "passed": True, "regimes": len(result["conditioning_regimes"]),
                      "output": str(args.output), "elapsed_ns": result["execution"]["elapsed_ns"]}))


if __name__ == "__main__":
    main()
