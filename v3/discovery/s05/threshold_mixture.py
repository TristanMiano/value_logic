#!/usr/bin/env python3
"""Small deterministic width probe for threshold_mixture.md.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-12. DEVELOPMENT.
Standard-library bisection; outputs are floating approximations, not a
machine-checked confidence-coverage certificate. No coverage simulation.
"""

import json
import math
from pathlib import Path


def log_mixture(n, s, q):
    if q == 0:
        return -math.log(n + 1) if s == 0 else math.inf
    if q == 1:
        return -math.log(n + 1) if s == n else math.inf
    log_beta = math.lgamma(s + 1) + math.lgamma(n - s + 1) - math.lgamma(n + 2)
    return log_beta - s * math.log(q) - (n - s) * math.log1p(-q)


def complete_interval(n, s, allowance):
    if not (0 <= s <= n and 0 < allowance < 1):
        raise ValueError("Require 0 <= s <= n and 0 < allowance < 1")
    if n == 0:
        return [0.0, 1.0]
    limit = -math.log(allowance)
    qhat = s / n
    if s == 0:
        lower = 0.0
    else:
        rejected, accepted = 0.0, qhat
        for _ in range(80):
            mid = (rejected + accepted) / 2
            if log_mixture(n, s, mid) > limit:
                rejected = mid
            else:
                accepted = mid
        lower = rejected
    if s == n:
        upper = 1.0
    else:
        accepted, rejected = qhat, 1.0
        for _ in range(80):
            mid = (accepted + rejected) / 2
            if log_mixture(n, s, mid) > limit:
                rejected = mid
            else:
                accepted = mid
        upper = rejected
    return [lower, upper]


def censored_interval(n, slo, shi, allowance):
    if not (0 <= slo <= shi <= n):
        raise ValueError("Require 0 <= slo <= shi <= n")
    return [complete_interval(n, slo, allowance)[0],
            complete_interval(n, shi, allowance)[1]]


def additive_interval(n, slo, shi, radius):
    return [max(0.0, slo / n - radius), min(1.0, shi / n + radius)]


def probe():
    alpha, cuts = 0.05, 16
    allowance = alpha / cuts
    cases = [(n, s, s) for n in (64, 256, 1024) for s in (0, n // 2)]
    cases.append((256, 0, 8))
    cases.append((256, 64, 72))
    rows = []
    for n, slo, shi in cases:
        intervals = {
            "beta_uniform_anytime": censored_interval(n, slo, shi, allowance),
            "hoeffding_per_cut_anytime": additive_interval(
                n, slo, shi, math.sqrt(math.log(2 * n * (n + 1) / allowance) / (2 * n))),
            "dkw_anytime": additive_interval(
                n, slo, shi, math.sqrt(math.log(2 * n * (n + 1) / alpha) / (2 * n))),
            "dkw_fixed_n": additive_interval(
                n, slo, shi, math.sqrt(math.log(2 / alpha) / (2 * n))),
        }
        rows.append({"n": n, "slo": slo, "shi": shi,
                     "intervals": intervals,
                     "widths": {name: hi - lo for name, (lo, hi) in intervals.items()}})

    # Targeted implementation checks for the analytic endpoint/overlap proof.
    checked_pairs = 0
    max_zero_endpoint_error = 0.0
    for a in (0.05, allowance):
        for n in range(1, 65):
            intervals = [complete_interval(n, s, a) for s in range(n + 1)]
            explicit_upper = -math.expm1((math.log(a) - math.log(n + 1)) / n)
            max_zero_endpoint_error = max(max_zero_endpoint_error,
                                          abs(intervals[0][1] - explicit_upper))
            for s in range(n):
                lo0, hi0 = intervals[s]
                lo1, hi1 = intervals[s + 1]
                assert lo0 <= lo1 + 1e-12 and hi0 <= hi1 + 1e-12
                assert lo1 <= hi0 + 1e-12
                qstar = (s + 1) / (n + 1)
                assert log_mixture(n, s, qstar) <= 1e-10
                assert log_mixture(n, s + 1, qstar) <= 1e-10
                checked_pairs += 1
    assert max_zero_endpoint_error < 1e-12
    return {
        "status": "DEVELOPMENT deterministic numerical width comparison",
        "contributor": "ChatGPT (GPT-6 Astra Pro)",
        "alpha_family": alpha, "threshold_cuts": cuts,
        "alpha_per_cut": allowance,
        "scope": {
            "beta_uniform_anytime": "all cuts and every sample count; uniform Beta(1,1) mixture",
            "hoeffding_per_cut_anytime": "all cuts and every sample count; a/[n(n+1)] spending",
            "dkw_anytime": "all thresholds and every sample count; alpha/[n(n+1)] spending",
            "dkw_fixed_n": "all thresholds at one prespecified sample count",
        },
        "rows": rows,
        "checks": {"adjacent_count_pairs": checked_pairs,
                   "n_range": [1, 64], "allowances": [0.05, allowance],
                   "max_zero_count_endpoint_abs_error": max_zero_endpoint_error},
        "limitation": "Floating approximations. The note supplies the coverage argument; these are not coverage simulations."
    }


if __name__ == "__main__":
    result = probe()
    destination = Path(__file__).with_name("threshold_mixture_results.json")
    destination.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("n Slo Shi | mixture | per-cut Hoeffding anytime | DKW anytime | DKW fixed-n")
    for row in result["rows"]:
        widths = " | ".join(f"{width:.4f}" for width in row["widths"].values())
        print(f"{row['n']} {row['slo']} {row['shi']} | {widths}")
    print(json.dumps(result["checks"], sort_keys=True))
