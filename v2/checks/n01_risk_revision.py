"""Exact planning probes for N01 recurrence C18-C24.

Codex (GPT-6), October 3, 2026 UTC. This is not the F11 producer.
Tail mass integration is compared to reference-knot stop-loss inequalities.
Enumerated probability grids corroborate the separate general proofs.
"""

from fractions import Fraction as Q
from itertools import product
import json

from .n01_recurrence_extensions import dot, parity_policies, tail_cvar


def compositions(total, size):
    if size == 1:
        yield (total,)
        return
    for head in range(total + 1):
        for rest in compositions(total - head, size - 1):
            yield (head,) + rest


def distribution(losses, probabilities):
    result = {}
    for loss, probability in zip(losses, probabilities):
        if probability:
            result[loss] = result.get(loss, Q(0)) + probability
    return result


def breakpoints(losses, probabilities):
    cumulative = Q(0)
    result = {Q(0)}
    for _, probability in sorted(distribution(losses, probabilities).items()):
        cumulative += probability
        if cumulative < 1:
            result.add(cumulative)
    return result


def all_level_gap(a, pa, b, pb):
    """CDF cells have fractional-linear gaps with constant derivative sign."""
    alphas = breakpoints(a, pa) | breakpoints(b, pb)
    endpoint = max(distribution(a, pa)) - max(distribution(b, pb))
    return max([endpoint] + [tail_cvar(a, pa, t) - tail_cvar(b, pb, t)
                             for t in alphas])


def stop_loss(losses, probabilities, threshold):
    return sum(p * max(loss - threshold, 0)
               for loss, p in zip(losses, probabilities))


def run():
    counts = {}
    c = Q(3, 20)
    policies = parity_policies(c)
    a = policies[f"0_{(0, 'read')}"]
    a_reverse = policies[f"0_{(1, 'read')}"]
    stop = policies["stop_0"]
    p = (Q(9, 20), Q(1, 20), Q(1, 4), Q(1, 4))
    q = (Q(1, 6), Q(0), Q(5, 12), Q(5, 12))
    assert dot(a, p) == dot(a, q) == Q(11, 40)
    assert tail_cvar(a, p, Q(1, 5)) == Q(49, 160)
    assert tail_cvar(a, q, Q(1, 5)) == Q(3, 10)
    assert tail_cvar(a, p, Q(9, 10)) == Q(29, 40)
    counts["equal_mean_different_risk_controls"] = 1

    delta = Q(1, 100)
    atom_losses = (c, 2*c, 1+c)
    pp = ((1-c)*delta, Q(0), 1-(1-c)*delta)
    pq = (Q(0), delta, 1-delta)
    for alpha in (Q(0), Q(1, 10), Q(1, 2), Q(9, 10)):
        assert tail_cvar(atom_losses, pp, alpha) == tail_cvar(atom_losses, pq, alpha)
    new_alpha = ((1-c)*delta+delta)/2
    assert tail_cvar(atom_losses, pp, new_alpha) > tail_cvar(atom_losses, pq, new_alpha)
    counts["fixed_risk_grid_counterexample"] = 1

    # All continuous alpha for each fixed finite distribution pair: the
    # CDF-cell oracle is independent of the stop-loss order construction.
    a_atoms = (Q(0), Q(3, 10), Q(1))
    b_atoms = (Q(3, 20), Q(3, 10), Q(23, 20))
    probability_grid = [tuple(Q(v, 6) for v in parts) for parts in compositions(6, 3)]
    order_cases = 0
    for pa, pb, allowance in product(probability_grid, probability_grid,
                                     (Q(0), Q(1, 5))):
        shifted = tuple(value + allowance for value in b_atoms)
        reference_knots = set(shifted)
        certified = all(stop_loss(a_atoms, pa, t) <= stop_loss(shifted, pb, t)
                        for t in reference_knots)
        actual = all_level_gap(a_atoms, pa, b_atoms, pb) <= allowance
        assert certified == actual
        order_cases += 1
    counts["reference_knot_vs_all_risk_order_cases"] = order_cases

    # C22: actual execution loss histograms agree despite a consequential edit.
    p_left = (Q(9, 20), Q(1, 20), Q(1, 5), Q(3, 10))
    p_right = (Q(9, 20), Q(1, 20), Q(3, 10), Q(1, 5))
    assert distribution(a, p_left) == distribution(a, p_right)
    assert dot(stop, p_left)-dot(a, p_left) == -Q(1, 40)
    assert dot(stop, p_right)-dot(a, p_right) == Q(3, 40)
    counts["old_full_loss_law_revision_counterexample"] = 1

    reconstruction_cases = 0
    for parts in compositions(5, 4):
        prior = tuple(Q(v, 5) for v in parts)
        means = dot(a, prior), dot(a_reverse, prior), dot(stop, prior)
        r = (means[0]+means[1]-4*c)/(1-2*c)
        d = means[0]-means[1]
        p00, p01 = (r-d)/2, (r+d)/2
        p10 = means[2]-p01
        recovered = (p00, p01, p10, 1-p00-p01-p10)
        # Compare every program's direct-execution expectation after recovery.
        assert recovered == prior
        assert all(dot(losses, prior) == dot(losses, recovered)
                   for losses in policies.values())
        reconstruction_cases += 1
    counts["full_policy_summary_reconstructions"] = reconstruction_cases

    alphas = (Q(0), Q(1, 11), Q(1, 10), Q(1, 4), Q(1, 2), Q(9, 10))
    lottery_cases = 0
    for weights, alpha in product(list(compositions(6, 3)), alphas):
        wa, wb, wc = (Q(v, 6) for v in weights)
        # At the equal prior, the entire lottery law depends only on wc.
        probs = ((wa+wb)/2, wc, (wa+wb)/2)
        optimum = min(Q(11, 10), 1/(1-alpha))
        assert tail_cvar((Q(0), Q(11, 10), Q(2)), probs, alpha) >= optimum
        lottery_cases += 1
    for alpha, prior0 in product(alphas, (Q(i, 10) for i in range(11))):
        optimum = min(Q(11, 10), 1/(1-alpha))
        if alpha <= Q(1, 11):
            # Fair A/B lottery, explicitly mixed over policy and input.
            probs = (prior0/2+(1-prior0)/2, (1-prior0)/2+prior0/2)
            assert tail_cvar((Q(0), Q(2)), probs, alpha) == optimum
        else:
            assert Q(11, 10) == optimum
    counts["robust_policy_lottery_witness_checks"] = lottery_cases

    for probability in (Q(0), Q(1, 1000), Q(1, 2), Q(1)):
        gap = all_level_gap((Q(0), Q(1)), (1-probability, probability),
                            (Q(3, 10),), (Q(1),))
        assert gap == (Q(7, 10) if probability else -Q(3, 10))
        assert (gap <= 0) == (probability == 0)
    counts["all_risk_numeric_discontinuity_cases"] = 4
    return {"status": "PASS", "scope": "finite planning probes, not F11",
            "counts": counts}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
