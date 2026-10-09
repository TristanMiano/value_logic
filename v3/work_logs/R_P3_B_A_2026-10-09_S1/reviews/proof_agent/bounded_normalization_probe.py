"""Independent exact enumeration of the fixed-mass normalization lemma.

This checks a mathematical integer map, not the root implementation. No
development population or private mathematical-query answers are generated.
"""

from fractions import Fraction as F
from itertools import product
import json


def compositions(total, length):
    if length == 1:
        yield (total,)
        return
    for first in range(1, total - length + 2):
        for tail in compositions(total - first, length - 1):
            yield (first,) + tail


def normalize(weights, losses, k):
    n = len(weights)
    mass = sum(weights)
    products = tuple(w * (k - ell) for w, ell in zip(weights, losses))
    total = sum(products)
    numerators = tuple((mass - n) * v for v in products)
    base = tuple(1 + numerator // total for numerator in numerators)
    remainder = mass - sum(base)
    result = tuple(value + int(i < remainder) for i, value in enumerate(base))
    return result, products, total, remainder, numerators


def enumeration():
    counts = []
    total_checked = 0
    for n, precision in ((2, 1), (2, 2), (3, 1), (3, 2), (4, 1)):
        mass = n * (1 << precision)
        retention = F(mass - n, mass)
        checked = 0
        worst_ratio = None
        largest_remainder = 0
        for weights in compositions(mass, n):
            for losses in product((0, 1), repeat=n):
                for k in (2, 3):
                    updated, values, total, remainder, numerators = normalize(weights, losses, k)
                    assert sum(updated) == mass and min(updated) >= 1
                    assert 0 <= remainder < n
                    assert max(updated) <= mass
                    assert max(numerators) <= mass * mass * k
                    for wi, vi in zip(updated, values):
                        ratio = F(wi * total, mass * vi)
                        assert ratio >= retention
                        worst_ratio = ratio if worst_ratio is None else min(worst_ratio, ratio)
                    largest_remainder = max(largest_remainder, remainder)
                    checked += 1
        counts.append({"experts": n, "precision": precision, "mass": mass,
                       "states_and_loss_vectors_checked": checked,
                       "retention_lower_bound": str(retention),
                       "minimum_observed_component_ratio": str(worst_ratio),
                       "largest_remainder": largest_remainder})
        total_checked += checked
    return total_checked, counts


def persistent_precision_loss():
    weights = (2, 2)
    mistakes = F(0)
    states = [weights]
    # b=2 gives one unbought round per block. Every true answer is zero.
    for _ in range(10):
        mistakes += F(weights[1], sum(weights))
        weights, *_ = normalize(weights, (0, 1), 2)
        states.append(weights)
    assert states[1:] == [(3, 1)] * 10
    assert mistakes == F(11, 4)
    return {"N": 2, "s": 1, "K": 2, "blocks": 10,
            "block_size": 2, "states": states,
            "perfect_expert_full_loss": "0",
            "expected_unbought_loss": str(mistakes),
            "old_constant_allowance": "2*ln(2), strictly less than 2",
            "old_bound_without_normalization_penalty_fails": mistakes > 2,
            "reason": "Positive minimum rounded expert mass persists forever."}


def main():
    checked, cases = enumeration()
    report = {
        "schema": "value_logic.selective_feedback.normalization_probe.v1",
        "arithmetic": "Exact Python integers and Fraction",
        "scope": "Finite map checks and one necessary-penalty witness",
        "total_cases": checked,
        "cases": cases,
        "precision_penalty_witness": persistent_precision_loss(),
        "result": "PASS: mass, positivity, component retention and finite numerator bounds hold in every enumerated case.",
    }
    print(json.dumps(report, indent=2) + "\n", end="")


if __name__ == "__main__":
    main()
