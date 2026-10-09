"""Audit only the named saved acquisition artifacts with independent formulas.

Does not execute/import the candidate source or update any pre-existing evidence.
Writes its report only beside this review script. All time is unmeasured and has
zero principal credit. This is same-model and not candidate-blind.
"""

from decimal import Decimal, getcontext
from fractions import Fraction as F
from hashlib import sha256
from math import comb
from pathlib import Path
import json

getcontext().prec = 65
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
SOURCE = ROOT / "v3/checks/07_acquisition_boundary.py"
EVIDENCE = ROOT / "v3/work_logs/P3_07_2026-10-09_S1/development/acquisition_boundary_v1"


def independent_accuracy(n):
    whole = sum(comb(n, k) * 11**k * 9 ** (n-k) for k in range(n//2+1, n+1))
    tie = comb(n, n//2) * 99 ** (n//2) if n % 2 == 0 else 0
    return F(2*whole + tie, 2*20**n)


def as_decimal(value):
    return str(Decimal(value.numerator) / Decimal(value.denominator))


def main():
    blobs = {path: path.read_bytes() for path in [SOURCE, EVIDENCE / "result.json", EVIDENCE / "rows.json"]}
    hashes = {
        str(path.relative_to(ROOT)): {"sha256": sha256(data).hexdigest(), "bytes": len(data)}
        for path, data in blobs.items()
    }
    result = json.loads(blobs[EVIDENCE / "result.json"])
    rows = json.loads(blobs[EVIDENCE / "rows.json"])
    checks = []
    errors = []

    def check(name, condition):
        checks.append({"name": name, "pass": bool(condition)})
        if not condition:
            errors.append(name)

    check("saved_source_hash_matches_current_source_bytes", result["source_sha256"] == sha256(blobs[SOURCE]).hexdigest())
    check("rows_are_exactly_n_0_through_128_in_order", [row["n"] for row in rows] == list(range(129)))
    exact = [independent_accuracy(n) for n in range(129)]
    row_errors = []
    for row in rows:
        n = row["n"]
        expected = {
            "total_variation": 2*exact[n]-1,
            "chi_square": F(103,99)**n-1,
            "optimal_symmetric_accuracy": exact[n],
            "profile_bill": F(n,2),
        }
        for field, value in expected.items():
            if F(row[field]) != value:
                row_errors.append({"n": n, "field": field, "stored": row[field], "expected": str(value)})
    check("all_129_rows_match_independent_exact_formulas_for_all_four_fields", not row_errors)
    check("all_saved_rows_satisfy_four_tv_squared_at_most_chi_square", all(4*F(r["total_variation"])**2 <= F(r["chi_square"]) for r in rows))
    expected_n = next(n for n, a in enumerate(exact) if a >= F(3,4))
    expected_weak = next(n for n in range(129) if F(103,99)**n >= 2)
    gross = F(128,20)
    affordable = gross // F(1,2)
    expected_fields = {
        "status": "PASS",
        "version": "p307-acquisition-identification-witness-v1",
        "hypotheses": {"completion_low": "9/20", "completion_high": "11/20", "attempt_cost": "1/2", "fallback_loss": "1", "future_queries": 128},
        "true_gain_per_future_query": {"low": "-1/20", "high": "1/20"},
        "single_chi_square": "4/99",
        "minimum_n_from_chi_square_necessary_condition": expected_weak,
        "minimum_n_for_optimal_symmetric_three_quarter_accuracy": expected_n,
        "bill_at_exact_minimum": str(F(expected_n,2)),
        "maximum_good_law_future_gross_gain": str(gross),
        "largest_affordable_fixed_sample_n": affordable,
        "best_sign_accuracy_at_affordable_n": str(max(exact[:affordable+1])),
    }
    for field, expected in expected_fields.items():
        check("result_field_" + field, result[field] == expected)
    check("chi_necessary_bill_exceeds_gross_bound", F(expected_weak,2) > gross)
    check("exact_minimum_bill_exceeds_gross_bound", F(expected_n,2) > gross)
    check("boundary_explicitly_excludes_arbitrary_sequential_policies", "No claim about arbitrary sequential policies" in result["boundary"])
    check("boundary_explicitly_excludes_empirical_service_performance", "empirical service performance" in result["boundary"])

    perfect = result["perfect_diagnostic_witness"]
    perfect_h = perfect["future_queries"]
    probe_cost = F(perfect["probe_cost"])
    separate_extremal_gross = F(perfect_h,2)
    # These are conditional consistency checks for an explicitly separate,
    # fully diagnostic witness, not assertions about the .45/.55 experiment.
    check("perfect_witness_good_gain_consistent_with_separate_per_query_gain_one_half", F(perfect["good_law_net_gain"]) == separate_extremal_gross-probe_cost)
    check("perfect_witness_bad_gain_consistent_with_abstention_after_probe", F(perfect["bad_law_net_gain"]) == -probe_cost)
    check("perfect_witness_prior_threshold_consistent_with_separate_extremal_gross", F(perfect["prior_good_threshold_for_positive_expected_acquisition_value"]) == probe_cost/separate_extremal_gross)

    report = {
        "status": "PASS_CORE_WITH_NESTED_WITNESS_SCOPE_LIMITATION" if not errors else "FAIL",
        "provenance": {"same_model": True, "candidate_blind": False, "core_derivation_completed_before_source_read": True, "timing": "unmeasured", "principal_time_credit": 0, "candidate_source_executed": False},
        "checks": checks,
        "errors": errors,
        "row_errors": row_errors,
        "hashes": hashes,
        "core_values": {"exact_minimum_n": expected_n, "chi_square_necessary_minimum_n": expected_weak, "accuracy_n44": as_decimal(exact[44]), "accuracy_n45": as_decimal(exact[45]), "bill_at_n45": str(F(45,2)), "maximum_good_law_gross_H128": str(gross), "net_upper_bound_at_n45": str(gross-F(45,2)), "largest_affordable_fixed_n": affordable, "best_accuracy_at_affordable_n": as_decimal(exact[affordable])},
        "limitations": [
            "Fixed deterministic n, equal-prior IID Bernoulli .45/.55 sign identification only; no arbitrary sequential or adaptive sample-cost lower bound.",
            "The perfect_diagnostic_witness is written as literal metadata without separate law parameters or computation/assertions. Its figures are consistent with a separate witness having good-law per-future-query gain 1/2 and perfect diagnostics, but not with inheritance of the surrounding .45/.55 laws. The surrounding writeup must establish the separate witness.",
            "The optional symmetric-payoff calculation in independent_derivation.md is expressly hypothetical and does not describe source's service-versus-abstention payoff convention; source-specific expected equal-prior gain is recorded below."
        ],
        "source_specific_equal_prior_service_or_abstain_economics": {
            "gross_formula_under_symmetric_classification_accuracy_A": "H*(high-cost)*(A-1/2)",
            "gross_at_n45_H128": as_decimal(F(128,20)*(exact[45]-F(1,2))),
            "perfect_information_prior_average_gross_ceiling_H128": "16/5",
            "lawwise_gross_ceiling_H128": "32/5",
            "perfect_diagnostic_H4_good_net_if_using_top_level_high_law": str(F(perfect_h,20)-probe_cost),
            "perfect_diagnostic_H4_bad_net_with_abstention": str(-probe_cost),
        },
    }
    (HERE / "source_hashes.json").write_text(json.dumps(hashes, indent=2)+"\n", encoding="utf-8")
    (HERE / "saved_evidence_audit.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "checks_passed": sum(c["pass"] for c in checks), "checks_total": len(checks), "errors": errors, "row_errors": row_errors, "core_values": report["core_values"], "source_specific_equal_prior_service_or_abstain_economics": report["source_specific_equal_prior_service_or_abstain_economics"]}, indent=2))


if __name__ == "__main__":
    main()
