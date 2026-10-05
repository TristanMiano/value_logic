"""Constructed positive calibration for F14's intervention measurement.

This network is compiled, never ordinarily trained, and is never evidence
about learned structure. It checks whether the protocol can recognize a
known approximate expected-cost interchange representation.
Contributor: ChatGPT (GPT-6 Astra Pro), F14.
"""
from __future__ import annotations

import math

import numpy as np

from . import neural as N


def compiled_cost_network() -> tuple[N.MLP, list[list[int]], float]:
    """Eight ReLU coordinates per cost, with a uniform probability bound.

    Approximate four univariate logarithms by secants on four geometric
    intervals. Each uses one always-positive affine input and three hinges.
    The other sixteen hidden coordinates have zero output weight.
    """
    w = np.zeros((4, 32), dtype=np.float64)
    b, v = np.zeros(32), np.zeros(32)
    beta, index = 0.0, 0
    role_subsets: list[list[int]] = [[], []]
    bounds = [0.0, 0.0]
    pieces = [
        (0, 1.0, np.array([0., 0., 1., 0.]), 0.0, 0.5, 2.0),
        (0, 1.0, np.array([0.125, 0.125, 0., 0.]), 0.5, 0.25, 0.75),
        (1, -1.0, np.array([0., 0., 0., 1.]), 0.0, 0.5, 2.0),
        (1, -1.0, np.array([-0.125, -0.125, 0., 0.]), 0.5, 0.25, 0.75),
    ]
    for role, sign, coefficients, offset, lower, upper in pieces:
        knots = np.geomspace(lower, upper, 5)
        slopes = np.diff(np.log(knots)) / np.diff(knots)
        # On [a,b], the secant underestimate is at most (b-a)^2/(8a^2).
        bounds[role] += max(float((right-left)**2/(8*left**2))
                            for left, right in zip(knots[:-1], knots[1:]))
        beta += sign * (math.log(lower)-slopes[0]*lower)
        for j in range(4):
            w[:, index] = coefficients
            b[index] = offset-(knots[j] if j else 0.0)
            v[index] = sign*(slopes[j]-slopes[j-1] if j else slopes[0])
            role_subsets[role].append(index)
            index += 1
    # Each log is underestimated. Logit error is the difference of two
    # nonnegative cost-log errors, not their sum. Sigmoid is 1/4-Lipschitz.
    probability_bound = max(bounds)/4 + 1e-12
    return N.MLP(w, b, v, float(beta)), role_subsets, probability_bound


def _swap(net, base, donor, subset):
    h = net.hidden(base)
    h[:, subset] = net.hidden(donor)[:, subset]
    return N.sigmoid(h @ net.v + net.beta)


def cancellation_witness():
    """A separate toy blocks interchange => ordinary-necessity overclaim.

    This is not the F14 training task, an ordinarily trained network, or a
    counterexample to its restricted intervention-relation claim.
    """
    base = np.linspace(-1, 1, 65)[:, None]
    donor = -base
    net = N.MLP(np.ones((1, 2)), np.ones(2), np.array([1., -1.]), 0.)
    ordinary = net.probability(base)
    role0 = _swap(net, base, donor, [0])
    role1 = _swap(net, base, donor, [1])
    jbase, jdonor = np.exp(base[:, 0]), np.exp(donor[:, 0])
    expected0, expected1 = jdonor/(jdonor+jbase), jbase/(jbase+jdonor)
    removed_pair = N.MLP(net.w.copy(), net.b.copy(), np.zeros(2), 0.)
    errors = [float(np.max(np.abs(role0-expected0))), float(np.max(np.abs(role1-expected1)))]
    ablation = float(np.max(np.abs(ordinary-removed_pair.probability(base))))
    effect = float(np.max(np.abs(role0-ordinary)))
    return {"evidence_type": "constructed_cancelling_pair_development_only",
            "original_F14_training_task": False, "ordinary_training_steps": 0,
            "ordinary_probability_max_error": float(np.max(np.abs(ordinary-0.5))),
            "per_role_interchange_max_errors": errors,
            "pair_removal_ordinary_effect_max": ablation,
            "isolated_intervention_effect_max": effect,
            "interchange_implies_ordinary_necessity": False,
            "passed": max(errors) <= 1e-12 and ablation == 0 and effect > 0.3}


def development_calibration(config=None, *, n=256):
    """Use a distinct DEVELOPMENT stream; no evaluation seed is accepted."""
    c = N.defaults() if config is None else config.get("neural", config)
    seed = c["development_seed"]
    net, subsets, error_bound = compiled_cost_network()
    rows, gauge_error = [], 0.0
    rng = N._rng(seed, 9000)
    permutation = rng.permutation(32)
    scales = np.exp(rng.uniform(math.log(0.125), math.log(8.0), 32))
    transformed = net.gauge(permutation, scales)
    inverse = np.argsort(permutation)
    for role in (0, 1):
        pairs, generation = N.make_pairs(c, seed, n, role, stream=9100+100*role)
        for stratum, (base, donor) in pairs.items():
            actual = _swap(net, base, donor, subsets[role])
            predicted = N.high_prediction(base, donor, role)
            gauged = _swap(transformed, base, donor, inverse[subsets[role]].tolist())
            maximum = float(np.max(np.abs(actual-predicted)))
            discrepancy = float(np.max(np.abs(gauged-actual)))
            gauge_error = max(gauge_error, discrepancy)
            rows.append({"role": role, "stratum": stratum, "n": n,
                         "mae": float(np.mean(np.abs(actual-predicted))),
                         "max_error": maximum,
                         "uniform_probability_bound": error_bound,
                         "bound_satisfied": maximum <= error_bound,
                         "generator_proposals": generation[stratum]["proposals_generated"]})
    cancellation = cancellation_witness()
    return {"evidence_type": "constructed_positive_development_only",
            "ordinary_training_steps": 0, "learned_structure_evidence": False,
            "seed": seed, "stream_namespace": "9000/9100/9200",
            "known_subsets": subsets, "rows": rows,
            "uniform_probability_bound": error_bound,
            "gauge_max_error": gauge_error,
            "cancellation_interpretation_witness": cancellation,
            "passed": all(r["bound_satisfied"] for r in rows)
                      and gauge_error <= c["gauge_tolerance"] and cancellation["passed"]}
