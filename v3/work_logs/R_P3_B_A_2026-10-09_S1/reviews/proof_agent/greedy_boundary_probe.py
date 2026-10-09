"""Exact, exogenous-tape counterexamples to importing a mixture guarantee.

These are mathematical policy comparisons, not executions or selections of
P3-08. Public modular answers are independently evaluated only in this probe.
"""

from fractions import Fraction as F
import json


def fixed_mass(weights, losses, k):
    mass, n = sum(weights), len(weights)
    weighted = tuple(F(w) * (1 - F(loss, k)) for w, loss in zip(weights, losses))
    total = sum(weighted)
    scaled = tuple((mass - n) * value / total for value in weighted)
    base = [1 + x.numerator // x.denominator for x in scaled]
    remainder = mass - sum(base)
    return tuple(value + int(i < remainder) for i, value in enumerate(base))


def compare(n, blocks, actions, *, precision=None, action_bits=None):
    block, k = 4, 3
    weights = (1 if precision is None else 1 << precision,) * n
    greedy_loss = 0
    mixed_loss = F(0)
    full_expert_losses = [0] * n
    predictions = []
    probabilities = []
    for index in range(blocks):
        label = 1 - index % 2
        probability = F(sum(w * a for w, a in zip(weights, actions)), sum(weights))
        if action_bits is not None:
            scaled = probability * (1 << action_bits)
            probability = F(scaled.numerator // scaled.denominator, 1 << action_bits)
        greedy = int(probability > F(1, 2))
        predictions.append(greedy)
        probabilities.append(str(probability))
        greedy_loss += (block - 1) * int(greedy != label)
        mixed_loss += (block - 1) * (probability if label == 0 else 1 - probability)
        losses = tuple(int(a != label) for a in actions)
        full_expert_losses = [total + block * loss
                              for total, loss in zip(full_expert_losses, losses)]
        if precision is None:
            weights = tuple(w * (k - loss) for w, loss in zip(weights, losses))
        else:
            weights = fixed_mass(weights, losses, k)
    best = min(full_expert_losses)
    regret = greedy_loss - best
    # ln 2 < 7/10 follows from exp(7/10)>1+.7+.7^2/2+.7^3/6>2.
    assert n in (2, 4)
    ordinary_allowance_upper = F(9 * 7 * (n.bit_length() - 1), 10)
    state_allowance = F(0) if precision is None else F(3 * blocks * 3, (1 << precision) - 1)
    action_allowance = F(0) if action_bits is None else F(3 * blocks, 1 << action_bits)
    complete_upper = ordinary_allowance_upper + state_allowance + action_allowance
    assert regret > complete_upper
    assert predictions == [i % 2 for i in range(blocks)]
    return {"experts": n, "blocks": blocks, "block_size": block,
            "expert_actions_on_both_queries": actions,
            "state_bits": precision, "action_bits": action_bits,
            "greedy_tie_rule": "zero", "greedy_predictions": predictions,
            "issued_probabilities": probabilities,
            "greedy_terminal_loss": greedy_loss,
            "best_fixed_full_tape_loss": best, "greedy_regret": regret,
            "randomized_expected_terminal_loss": str(mixed_loss),
            "safe_rational_log_allowance": str(ordinary_allowance_upper),
            "state_allowance": str(state_allowance),
            "action_allowance": str(action_allowance),
            "complete_claimed_allowance_upper": str(complete_upper),
            "strict_counterexample": True}


def main():
    modular = {str(a): {"residue": pow(a, 8, 17), "answer": int(pow(a, 8, 17) == 1),
                        "four_expert_actions": (0, 1, a & 1, int(2 * a < 17))}
               for a in (1, 3, 2, 6)}
    assert (modular["1"]["answer"], modular["3"]["answer"]) == (1, 0)
    assert (modular["2"]["answer"], modular["6"]["answer"]) == (1, 0)
    assert modular["2"]["four_expert_actions"] == modular["6"]["four_expert_actions"] == (0, 1, 0, 1)
    original = compare(2, 8, (0, 1))
    assert original["randomized_expected_terminal_loss"] == "66/5"
    ordinary_four = compare(4, 16, (0, 1, 0, 1))
    assert ordinary_four["randomized_expected_terminal_loss"] == "132/5"
    report = {"schema": "value_logic.selective_feedback.greedy_boundary_probe.v1",
              "arithmetic": "Exact integers and Fraction; rational upper bounds for logarithms",
              "public_modular_verification": modular,
              "design_two_expert_case": original,
              "same_service_four_expert_case": ordinary_four,
              "same_service_fixed_state_case": compare(4, 16, (0, 1, 0, 1), precision=16, action_bits=16),
              "result": "PASS: all three greedy replacements violate the corresponding imported mixture bound."}
    print(json.dumps(report, indent=2) + "\n", end="")


if __name__ == "__main__":
    main()
