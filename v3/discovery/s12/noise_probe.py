"""Small DEVELOPMENT calculation; fixed inputs, no statistical benchmark.

Codex (GPT-6). Standard library only. Preserve this executed source and outputs.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
from math import ceil, exp, erfc, sqrt, log
import hashlib
import json
import platform
import sys

HERE = Path(__file__).resolve().parent


def serial(x):
    if isinstance(x, Q):
        return {"numerator": x.numerator, "denominator": x.denominator,
                "decimal": float(x)}
    if isinstance(x, dict):
        return {str(k): serial(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [serial(v) for v in x]
    return x


def exp_bounds(x, terms=64):
    """Exact rational lower/upper bounds for exp(x), x>=0."""
    assert 0 <= x < terms + 2
    term = total = Q(1)
    for k in range(1, terms + 1):
        term *= x / k
        total += term
    nxt = term * x / (terms + 1)
    return total, total + nxt / (1 - x / (terms + 2))


def enumerate_design(fees, target, cap, sigma):
    others = [j for j in range(len(fees)) if j not in target]
    base = sum(fees[j] for j in target)
    rows = []
    for size in range(1, min(len(others), cap-len(target)) + 1):
        for bundle in combinations(others, size):
            increment = sum(fees[j] for j in bundle)
            variance_proxy = 1 + Q(4) * sigma**2 / increment**2
            rows.append(dict(bundle=bundle, base=base, increment=increment,
                             depth=len(target)+size, cost=base+increment,
                             variance_proxy=variance_proxy,
                             cost_proxy=(base+increment)*variance_proxy))
    assert rows
    best = min(rows, key=lambda r: (r["cost_proxy"], r["cost"], r["bundle"]))
    return dict(fees=fees, target=target, cap=cap, sigma=sigma,
                candidates=len(rows), best=best, all=rows)


def main():
    # Enclose log(40) by proving exp(lo)<40<exp(hi) using rational sums.
    hi = Q(3688879454113937, 10**15)
    lo = hi-Q(1, 10**15)
    assert exp_bounds(lo)[1] < 40 < exp_bounds(hi)[0]
    target_radius = Q(1, 5)
    headline = []
    for d in [Q(1), Q(8)]:
        v = 1+Q(64)/d**2
        n_lo = ceil(2*v*lo/target_radius**2)
        n_hi = ceil(2*v*hi/target_radius**2)
        assert n_lo == n_hi
        headline.append(dict(marker=d, proxy=v, samples=n_hi,
                             worst_fee=n_hi*(2+d),
                             maximum_queries=3*n_hi))

    menus = [enumerate_design(tuple(map(Q, (1,1,1,8))), (0,1), 3, Q(4))]
    for cap in range(3,8):
        for sigma in [Q(0), Q(1), Q(4)]:
            menus.append(enumerate_design((Q(1),)*7, (0,1), cap, sigma))
    fees = tuple(map(Q, (1,1,1,1,2,3,5,8,13,21,34,55)))
    for cap in [3,4,6]:
        menus.append(enumerate_design(fees, (0,1), cap, Q(4)))

    # Semantic check against all worlds, independent of the cost proxy.
    semantic_cases = 0
    for menu in menus:
        if len(menu["fees"]) > 7:
            continue
        for row in menu["all"]:
            for bits in product([0,1], repeat=len(menu["fees"])):
                truth = (-1)**sum(bits[j] for j in menu["target"])
                acquired = list(menu["target"])
                if truth == 1:
                    acquired += list(row["bundle"])
                assert len(acquired) == len(set(acquired)) <= menu["cap"]
                actual = sum(menu["fees"][j] for j in acquired)
                decoded = 2*(actual-row["base"])/row["increment"]-1
                assert decoded == truth
                semantic_cases += 1

    # Analytical comparisons; exp/erfc values are floating diagnostics only.
    reset_rows = []
    radius = Q(1,4)
    n = ceil(8*hi/radius**2)
    for k in [1,2,4,8,16,32,64]:
        m = max(1, ceil(8*log(4*k/float(radius))))
        kappa = 1-erfc(sqrt(m)/(2*sqrt(2)))
        linear_m = max(1,4*(k-1))
        reset_rows.append(dict(groups=k, linear_unaveraged_second_moment=5**k,
            linear_averaged_repetitions=linear_m,
            linear_averaged_second_moment=(1+Q(4,linear_m))**k,
            decode_repetitions=m, decode_fresh_worlds=n,
            decode_worst_fee=n*k*m*2,
            decode_bias_upper_float=2*k*exp(-m/8),
            gaussian_exact_worst_bias_float=1-kappa**k,
            gaussian_debiased_second_moment_float=kappa**(-2*k)))
        assert 2*k*exp(-m/8) <= float(radius)/2

    result = dict(contributor="Codex (GPT-6)", status="DEVELOPMENT",
        scope="Exact finite menu arithmetic; floating reset diagnostics; no empirical coverage claim",
        python=sys.version, platform=platform.platform(),
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        log40_enclosure=dict(lower=lo, upper=hi, certified_by="rational Taylor bounds"),
        headline=headline,
        headline_fee_reduction=1-headline[1]["worst_fee"]/headline[0]["worst_fee"],
        menu_count=len(menus), semantic_cases=semantic_cases,
        menus=menus, reset_rows=reset_rows)
    out = HERE/"noise_probe.json"
    out.write_bytes((json.dumps(serial(result), indent=2)+"\n").encode())
    print(json.dumps(serial({k:result[k] for k in
          ["status","headline","headline_fee_reduction","menu_count","semantic_cases"]})))


if __name__ == "__main__":
    main()
