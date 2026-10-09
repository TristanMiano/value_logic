"""Exact finite P3-07 acquisition-value diagnostics; DEVELOPMENT.

The hidden object is a bounded service's completion rate, not an alternative
truth semantics. Success yields an acquired checked correct answer; failure
uses fallback. Rates and prices are explicit hypotheses for this witness.
This is not an executed performance profile or a hardware lower bound.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import argparse
import hashlib
import json

VERSION = "p307-acquisition-identification-witness-v1"


def binomial(n, p):
    return tuple(F(comb(n, k)) * p**k * (1-p)**(n-k) for k in range(n+1))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=False)
    low, high, cost, horizon = F(9,20), F(11,20), F(1,2), 128
    single_chi = (high-low)**2 / (low*(1-low))
    rows = []
    for n in range(129):
        p, q = binomial(n, low), binomial(n, high)
        tv = sum((abs(a-b) for a,b in zip(p,q)), F(0))/2
        chi = sum(((b-a)**2/a for a,b in zip(p,q)), F(0))
        # Product likelihood ratio factorization, with binomial count
        # sufficient for these exchangeable Bernoulli observations.
        assert chi == (1+single_chi)**n - 1
        assert 4*tv*tv <= chi
        accuracy = (1+tv)/2
        # Majority, with fair randomization of an even tie, attains equal
        # correctness in the two laws and the equal-prior optimum.
        correct_high = sum((q[k] for k in range(n+1) if 2*k > n), F(0))
        if n % 2 == 0:
            correct_high += q[n//2]/2
        assert correct_high == accuracy
        rows.append({"n":n,"total_variation":str(tv),
                     "chi_square":str(chi),"optimal_symmetric_accuracy":str(accuracy),
                     "profile_bill":str(n*cost)})
    required = next(r for r in rows if F(r["optimal_symmetric_accuracy"]) >= F(3,4))
    weak_required = next(r for r in rows if F(r["chi_square"]) >= 1)
    max_future_gain = horizon*(high-cost)
    affordable = int(max_future_gain/cost)
    assert F(required["profile_bill"]) > max_future_gain
    assert F(weak_required["profile_bill"]) > max_future_gain
    result = {
        "status":"PASS", "version":VERSION,
        "hypotheses":{"completion_low":str(low),"completion_high":str(high),
                      "attempt_cost":str(cost),"fallback_loss":"1","future_queries":horizon},
        "true_gain_per_future_query":{"low":str(low-cost),"high":str(high-cost)},
        "single_chi_square":str(single_chi),
        "minimum_n_from_chi_square_necessary_condition":weak_required["n"],
        "minimum_n_for_optimal_symmetric_three_quarter_accuracy":required["n"],
        "bill_at_exact_minimum":required["profile_bill"],
        "maximum_good_law_future_gross_gain":str(max_future_gain),
        "largest_affordable_fixed_sample_n":affordable,
        "best_sign_accuracy_at_affordable_n":rows[affordable]["optimal_symmetric_accuracy"],
        "perfect_diagnostic_witness":{"future_queries":4,"probe_cost":"1/2",
              "good_law_net_gain":"3/2","bad_law_net_gain":"-1/2",
              "prior_good_threshold_for_positive_expected_acquisition_value":"1/4"},
        "boundary":"Exact stipulated finite-law diagnostic. Fixed-size sign identification is stronger than safe abstention. No claim about arbitrary sequential policies or empirical service performance.",
        "source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (out/"rows.json").write_text(json.dumps(rows,indent=2)+"\n")
    (out/"result.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
