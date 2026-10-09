"""Small independent exact calculation; no imports from the candidate source.

Same-model, nonblind candidate prompt; mathematical reconstruction was completed
before reading the candidate source or evidence. All time is unmeasured and has
zero principal credit.
"""

from decimal import Decimal, getcontext
from fractions import Fraction
from math import comb
import json
from pathlib import Path

getcontext().prec = 65


def exact_accuracy(n):
    numerator = 2 * sum(
        comb(n, k) * 11**k * 9 ** (n - k)
        for k in range(n // 2 + 1, n + 1)
    )
    if n % 2 == 0:
        numerator += comb(n, n // 2) * 11 ** (n // 2) * 9 ** (n // 2)
    return Fraction(numerator, 2 * 20**n)


def decimal_string(value):
    return str(Decimal(value.numerator) / Decimal(value.denominator))


def main():
    accuracy = [exact_accuracy(n) for n in range(101)]
    threshold = Fraction(3, 4)
    minimum_n = next(n for n, value in enumerate(accuracy) if value >= threshold)
    selected_n = [0, 1, 12, 13, 17, 18, 42, 43, 44, 45, 46]
    p = Fraction(11, 20)
    single_chi = Fraction(4, 99)
    checks = {
        "all_smaller_n_fail_exact_comparison": all(
            accuracy[n] < threshold for n in range(minimum_n)
        ),
        "even_odd_plateaus_through_100": all(
            accuracy[2 * m] == accuracy[2 * m - 1] for m in range(1, 51)
        ),
        "odd_increment_identity_through_99": all(
            accuracy[2 * m + 1] - accuracy[2 * m]
            == (p - Fraction(1, 2)) * comb(2 * m, m) * (p * (1 - p)) ** m
            for m in range(50)
        ),
    }
    assert all(checks.values())
    result = {
        "review_provenance": {
            "same_model": True,
            "blind": False,
            "candidate_n_disclosed_by_prompt": 45,
            "reconstruction_before_source_read": True,
            "timing": "unmeasured",
            "principal_time_credit": 0,
        },
        "experiment": "fixed_n_iid_equal_prior_bernoulli_9_over_20_vs_11_over_20",
        "minimum_fixed_n_for_accuracy_at_least_3_over_4": minimum_n,
        "accuracy_selected": {
            str(n): {
                "fraction": str(accuracy[n]),
                "decimal": decimal_string(accuracy[n]),
                "at_least_3_over_4": accuracy[n] >= threshold,
            }
            for n in selected_n
        },
        "checks": checks,
        "single_sample_chi_square": str(single_chi),
        "product_chi_square_formula": "(103/99)**n - 1",
        "chi_square_necessary_sample_count": next(
            n for n in range(101) if (1 + single_chi) ** n >= 2
        ),
        "product_chi_square_selected": {
            str(n): decimal_string((1 + single_chi) ** n - 1) for n in [17, 18]
        },
        "minimum_qualifying_profile_cost": str(Fraction(1, 2) * minimum_n),
        "gross_gain_ceiling_H128": str(Fraction(1, 20) * 128),
        "net_gain_upper_at_minimum_n": str(
            Fraction(1, 20) * 128 - Fraction(1, 2) * minimum_n
        ),
        "gross_gain_at_threshold_accuracy": decimal_string(
            Fraction(1, 10) * 128 * (accuracy[minimum_n] - Fraction(1, 2))
        ),
        "scope": "No arbitrary sequential or adaptive lower-bound claim.",
    }
    output = Path(__file__).with_name("independent_results.json")
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
