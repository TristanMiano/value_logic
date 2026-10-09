"""Exact finite checks of the block-feedback bridge, not a learning benchmark.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-09.
Independent, same-model, nonblind mathematical reconstruction. All labels in
this evaluator are private mathematical inputs; this is not a learner API.
"""

from fractions import Fraction as F
from itertools import product
import json


def normalized(weights):
    total = sum(weights)
    return tuple(w / total for w in weights)


def loss_vector(label):
    return (F(label != 0), F(label != 1))


def dot(left, right):
    return sum(a * b for a, b in zip(left, right))


def exact_block_path(labels, block_sizes, choices, eta=F(1, 2), weighted=False):
    """Return the actual unbought mixture loss and its sampled bridge target."""
    weights = (F(1), F(1))
    actual = F(0)
    sampled_target = F(0)
    offset = 0
    largest = max(size - 1 for size in block_sizes)
    for size, chosen in zip(block_sizes, choices):
        probabilities = normalized(weights)
        rows = tuple(loss_vector(y) for y in labels[offset:offset + size])
        actual += sum(dot(probabilities, row) for j, row in enumerate(rows)
                      if j != chosen)
        sample = rows[chosen]
        sampled_target += (size - 1) * dot(probabilities, sample)
        scale = F(size - 1, largest) if weighted and largest else F(1)
        weights = tuple(w * (1 - eta * scale * x)
                        for w, x in zip(weights, sample))
        offset += size
    return actual, sampled_target


def exhaustive_bridge(block_sizes, weighted=False):
    rounds = sum(block_sizes)
    paths_per_tape = 1
    for size in block_sizes:
        paths_per_tape *= size
    checked = 0
    nonpathwise = 0
    for labels in product((0, 1), repeat=rounds):
        actual_total = F(0)
        sampled_total = F(0)
        for choices in product(*(range(size) for size in block_sizes)):
            actual, sampled = exact_block_path(labels, block_sizes, choices,
                                              weighted=weighted)
            actual_total += actual
            sampled_total += sampled
            nonpathwise += actual != sampled
            checked += 1
        assert actual_total / paths_per_tape == sampled_total / paths_per_tape
    return {
        "block_sizes": block_sizes,
        "weighted_updates": weighted,
        "binary_tapes": 2 ** rounds,
        "selector_paths_per_tape": paths_per_tape,
        "paths_checked": checked,
        "paths_where_equality_fails_before_expectation": nonpathwise,
        "expected_bridge_equal_for_every_tape": True,
    }


def immediate_update_witness():
    # One fixed block, constant experts 0 and 1, labels (0,1), eta=1/2.
    actual_total = F(0)
    sampled_total = F(0)
    rows = (loss_vector(0), loss_vector(1))
    for chosen in (0, 1):
        weights = (F(1), F(1))
        for j, row in enumerate(rows):
            probabilities = normalized(weights)
            if j == chosen:
                sampled_total += dot(probabilities, row)
                weights = tuple(w * (1 - F(1, 2) * x)
                                for w, x in zip(weights, row))
            else:
                actual_total += dot(probabilities, row)
    actual, sampled = actual_total / 2, sampled_total / 2
    assert actual == F(7, 12) and sampled == F(1, 2)
    return {"actual_expected_unbought_loss": str(actual),
            "claimed_sample_bridge": str(sampled),
            "bridge_failed": actual > sampled}


def public_history_adaptation_witness():
    # The first query's answer is zero. The second query has answer one only
    # when the public first-round decision was BUY. There is one expert, 0.
    actual_total = sampled_total = all_issued_total = F(0)
    for chosen in (0, 1):
        labels = (0, int(chosen == 0))
        actual_total += sum(F(y) for j, y in enumerate(labels) if j != chosen)
        sampled_total += F(labels[chosen])
        all_issued_total += sum(F(y) for y in labels)
    actual = actual_total / 2
    sampled = sampled_total / 2
    all_issued = all_issued_total / 2
    assert (actual, sampled, all_issued) == (F(1, 2), F(0), F(1, 2))
    return {"actual_expected_unbought_loss": str(actual),
            "expected_selected_loss": str(sampled),
            "expected_all_issued_expert_loss": str(all_issued),
            "uniform_query_count": 1,
            "discounted_expert_loss": str(all_issued / 2),
            "bridge_failed": actual > sampled}


def random_hindsight_minimum_witness():
    totals = ((F(0), F(2)), (F(2), F(0)))
    minimum_of_expectations = min(sum(row[i] for row in totals) / 2
                                  for i in range(2))
    expectation_of_minimum = sum(min(row) for row in totals) / 2
    assert (minimum_of_expectations, expectation_of_minimum) == (F(1), F(0))
    return {"minimum_of_fixed_expert_expectations": str(minimum_of_expectations),
            "expected_random_hindsight_minimum": str(expectation_of_minimum),
            "cannot_swap": True}


def main():
    report = {
        "schema": "value_logic.selective_feedback.independent_bridge_probe.v1",
        "scope": "Finite arithmetic identities and separating counterexamples only.",
        "arithmetic": "Python Fraction; exhaustive selector expectations, no seeds.",
        "fixed_tape_equal_blocks": exhaustive_bridge((2, 2)),
        "fixed_tape_uneven_blocks": exhaustive_bridge((2, 3), weighted=True),
        "singleton_block_boundary": exhaustive_bridge((1, 2), weighted=True),
        "premature_update_counterexample": immediate_update_witness(),
        "adaptive_request_counterexample": public_history_adaptation_witness(),
        "random_hindsight_counterexample": random_hindsight_minimum_witness(),
        "result": "PASS: qualified identities hold; invalid extensions are separated.",
    }
    print(json.dumps(report, indent=2) + "\n", end="")


if __name__ == "__main__":
    main()
