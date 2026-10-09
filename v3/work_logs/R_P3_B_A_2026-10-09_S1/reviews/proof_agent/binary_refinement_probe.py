"""Independently verify saved bound arithmetic; do not execute any new policy.

Logarithms are enclosed by the positive -log(1-x) series, independently of
the certificate generator's atanh implementation. Exact rational arithmetic
checks every saved refinement and unexecuted uniform rate option.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

FOLDER = Path(__file__).resolve().parent
LOG = FOLDER.parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def independent_log_k_ratio(k, terms=128):
    # log(k/(k-1)) = sum_{j>=1} (1/k)^j / j.
    x = F(1, k)
    power, lower = x, F(0)
    for j in range(1, terms + 1):
        lower += power / j
        power *= x
    return lower, lower + power / ((terms + 1) * (1 - x))


def main():
    certificate_path = FOLDER / "binary_potential_certificates_reviewed.json"
    certificate = json.loads(certificate_path.read_text())
    inputs_path = LOG / "development/service_comparison/run_001/result.json"
    inputs = json.loads(inputs_path.read_text())
    assert digest(inputs_path) == certificate["input_sha256"]
    assert digest(FOLDER / "binary_potential_certificates_reviewed.py") == certificate["program_sha256"]
    ln2_lower, ln2_upper = map(F, certificate["log2_enclosure"])
    independent_lower, independent_upper = independent_log_k_ratio(2)
    assert ln2_lower < independent_lower < independent_upper < ln2_upper
    ln4_upper = 2 * ln2_upper
    by_name = {arm["name"]: arm for arm in inputs["learner_arms"]}
    assert len(by_name) == len(certificate["executed_uniform_rows"]) == 20
    rows = []
    for row in certificate["executed_uniform_rows"]:
        arm = by_name[row["arm"]]
        t, b, s, h = arm["horizon"], arm["block_size"], arm["state_bits"], arm["contract"]["action_bits"]
        m, k = t // b, max(2, b - 1)
        alpha_lower, alpha_upper = map(F, row["alpha_enclosure"])
        ilower, iupper = independent_log_k_ratio(k)
        assert alpha_lower < F(b - 1, b) * k * ilower
        assert F(b - 1, b) * k * iupper < alpha_upper
        old_alpha = F(b - 1, b) * (1 + F(1, k))
        assert F(row["conservative_original_alpha"]) == old_alpha
        assert alpha_upper < old_alpha <= 1
        ell = min(arm["evaluation"]["fixed_expert_all_issued_losses"].values())
        assert row["retrospective_L_star"] == ell
        assert F(row["source_known_L_star_upper"]) == F(t, 2)
        state = F(0) if s is None else F((b - 1) * m * k, (1 << s) - 1)
        action = F(t - m, 1 << h)
        common = (b - 1) * k * ln4_upper + state + action
        expected = min(F(t - m), alpha_upper * ell + common)
        source_known = min(F(t - m), alpha_upper * F(t, 2) + common)
        beta_upper = alpha_upper * F(b, b - 1)
        brier_state = F(0) if s is None else F(b * m * k, (1 << s) - 1)
        brier = min(F(t), beta_upper * ell + b * k * ln4_upper + brier_state + F(2 * t, 1 << h))
        original = F(arm["evaluation"]["theorem_bounds"]["terminal_expectation_upper_clipped"])
        assert F(row["state_allowance"]) == state and F(row["action_allowance"]) == action
        assert F(row["refined_terminal_upper"]) == expected <= original
        assert F(row["source_known_terminal_upper"]) == source_known
        assert F(row["refined_brier_upper"]) == brier
        assert F(row["original_terminal_upper"]) == original
        assert F(row["bound_reduction"]) == original - expected
        assert row["policy_change"] is False
        assert row["observed_source_version"] == arm["contract"]["version"]
        assert row["refined_terminal_upper_decimal"] == float(expected)
        assert row["source_known_terminal_upper_decimal"] == float(source_known)
        rows.append({"arm": row["arm"], "retrospective_upper_decimal": float(expected),
                     "source_known_upper_decimal": float(source_known),
                     "all_exact_certificate_fields_match": True})
    candidates = certificate["unexecuted_rate_candidates"]
    assert [row["B"] for row in candidates] == [1 << j for j in range(1, 11)]
    adaptive_candidates = []
    for row in candidates:
        b, eta = row["B"], F(row["unexecuted_eta"])
        assert eta == F(2, b + 1) and 0 < eta < 1
        scalar_cap = 1 + eta / (2 * (1 - eta))
        assert F(b - 1, b) * scalar_cap == F(row["alpha_cap"]) == 1
        assert (b - 1) / eta == F(row["log_N_coefficient"]) == F(b * b - 1, 2)
        assert row["integer_correct_factor"] == b + 1 and row["integer_wrong_factor"] == b - 1
        hbound = 2 * b - 1
        adaptive_eta = F(2, hbound + 2)
        assert adaptive_eta * hbound / (2 * (1 - adaptive_eta)) == 1
        for tickets in (1, b + 1):
            pi = F(tickets, 2 * b)
            coefficient = 1 - pi + adaptive_eta * (1 - pi) ** 2 / (2 * hbound * (1 - adaptive_eta) * pi)
            assert coefficient <= 1
        denominator = (b + 1) * hbound * (hbound + 2)
        adaptive_candidates.append({"B": b, "H": hbound, "unexecuted_eta": str(adaptive_eta),
                                    "common_denominator": denominator,
                                    "common_denominator_bits": denominator.bit_length(),
                                    "comparator_coefficient_bound_pass": True})
    assert adaptive_candidates[-1]["common_denominator_bits"] == 33
    report = {"schema": "value_logic.selective_feedback.binary_refinement_independent_check.v1",
              "principal_time_credit_ns": 0,
              "certificate_sha256": digest(certificate_path),
              "input_sha256": digest(inputs_path),
              "program_sha256": certificate["program_sha256"],
              "independent_log_method": "128-term positive -log(1-x) series with rational geometric tail",
              "original_log_enclosures_strictly_contain_independent_enclosures": True,
              "executed_uniform_rows_verified": len(rows), "rows": rows,
              "uniform_unexecuted_rates_verified": len(candidates),
              "adaptive_unexecuted_rate_arithmetic": adaptive_candidates,
              "new_policy_executions": 0,
              "result": "PASS: same-policy refined certificates and separately labeled mathematical rate options."}
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
