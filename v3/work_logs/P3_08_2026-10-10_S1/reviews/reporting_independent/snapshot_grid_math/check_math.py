"""Independent snapshot/grid algebra and public contract bound checks.

ChatGPT (GPT-6 Astra Pro), 2026-10-10; P3-08 DEVELOPMENT. Hypothetical supplied
toy labels only; no production calculator, service, or main private scores.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import math
import sys


def pair(value):
    return [value.numerator, value.denominator] if isinstance(value, F) else value


def digest(path):
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def root(n):
    result = math.isqrt(n)
    return result + (result * result < n)


def check_algebra():
    tests = mean_checks = 0
    grid = (F(0), F(1, 4), F(1, 2), F(3, 4), F(1))
    selector_vectors = ((F(1, 2), F(1, 2)), (F(3, 4), F(1, 4)),
                        (F(1, 4), F(3, 4)))
    for q in product(grid, repeat=2):
        for y in product((0, 1), repeat=2):
            d = tuple(q[t] + (1 - 2*q[t])*y[t] for t in range(2))
            for h0 in product((0, 1), repeat=2):
                a = tuple(F(1-h0[t], 2) for t in range(2))
                r = tuple((1-h0[t]) * (d[t]-F(1, 2)) for t in range(2))
                variance = tuple((1-h0[t])*q[t]*(1-q[t]) for t in range(2))
                for pi in selector_vectors:
                    errors = []
                    width = max((1-h0[t])*abs(1-2*q[t])/pi[t] for t in range(2))
                    raw_width = max(abs(1-2*q[t])/pi[t] for t in range(2))
                    assert width <= raw_width
                    for selected in range(2):
                        us = sum(a[t] for t in range(2) if t != selected) + (1/pi[selected]-1)*r[selected]
                        ass = sum(a[t]-variance[t] for t in range(2)) + r[selected]/pi[selected]
                        qs = tuple(F(y[t]) if h0[t] else q[t] for t in range(2))
                        vs = sum(qs[t]+(1-2*qs[t])*y[t] for t in range(2) if t != selected)
                        fs = sum((qs[t]-y[t])**2 for t in range(2))
                        error = sum(r)-r[selected]/pi[selected]
                        assert vs-us == fs-ass == error
                        errors.append(error)
                        for h1 in product((0, 1), repeat=2):
                            if any(h0[t] > h1[t] for t in range(2)):
                                continue
                            qlive = tuple(F(y[t]) if h1[t] else q[t] for t in range(2))
                            f1 = sum((qlive[t]-y[t])**2 for t in range(2))
                            v1 = sum(qlive[t]+(1-2*qlive[t])*y[t] for t in range(2) if t != selected)
                            df = sum((q[t]-y[t])**2 for t in range(2) if h1[t] and not h0[t])
                            dv = sum(d[t] for t in range(2) if t != selected and h1[t] and not h0[t])
                            assert f1 == fs-df and v1 == vs-dv
                            assert f1-(ass-df) == v1-(us-dv) == error
                            tests += 1
                    assert sum(pi[j]*errors[j] for j in range(2)) == 0
                    assert max(errors)-min(errors) <= width
                    mean_checks += 1
    return {"toy_scope": "B=2; q in {0,1/4,1/2,3/4,1}; supplied binary y; all monotone mask pairs; uniform and both ticket favorites",
            "translation_cases": tests, "conditional_mean_and_width_cases": mean_checks,
            "all_equalities_and_bounds_passed": True,
            "meaning": "finite algebra checks supplement the symbolic proof; masks include hypothetical monotone configurations beyond owned receipt reachability"}


def check_contracts():
    count = 0
    max_j = max_c = max_r = max_cross_bits = 0
    extremal = None
    per_block_maximum = []
    d = 1 << 32
    for exponent in range(1, 11):
        b = 1 << exponent
        row = {"B": b, "max_grid_size": 0, "max_grid_rate": 0,
               "max_radius_cross_product_prebits": 0}
        for m in range(1, 8192//b + 1):
            for selector in ("uniform", "tickets"):
                s, multiple = (b, 1) if selector == "uniform" else (2*b, b+1)
                rstar = s*root(2*m)
                rates, rate = [s], s
                while rate < rstar:
                    rate *= 2
                    rates.append(rate)
                rates = sorted(set(rates + [rstar]))
                j = len(rates)
                c = (80*j-1).bit_length()
                assert 2**c >= 80*j and (c == 0 or 2**(c-1) < 80*j)
                # This rational bound suffices since exp(c)>2**c.
                assert F(2*j, 2**c) <= F(1, 40)
                qden = d*d*multiple*multiple
                qnum = m*s*s*qden
                numerators = [8*qnum+c*r*r*qden for r in rates]
                denominators = [8*r*qden for r in rates]
                prebits = max(n.bit_length()+den.bit_length() for n in numerators for den in denominators)
                assert max(rates) < 2**15 and prebits < 256
                count += 1
                max_j, max_c, max_r = max(max_j, j), max(max_c, c), max(max_r, max(rates))
                row["max_grid_size"] = max(row["max_grid_size"], j)
                row["max_grid_rate"] = max(row["max_grid_rate"], max(rates))
                row["max_radius_cross_product_prebits"] = max(row["max_radius_cross_product_prebits"], prebits)
                if prebits > max_cross_bits:
                    max_cross_bits = prebits
                    extremal = {"T": b*m, "B": b, "m": m, "selector": selector,
                                "D": d, "rates": rates, "J": j, "c": c,
                                "numerator_upper_bound": max(numerators),
                                "denominator_upper_bound": max(denominators)}
        per_block_maximum.append(row)
    return {"public_contract_cases": count, "maximum_J": max_j, "maximum_c": max_c,
            "maximum_grid_R": max_r, "maximum_comparison_prebits": max_cross_bits,
            "coarse_symbolic_comparison_prebits": 229,
            "extremal_comparison": extremal, "per_B_maximum": per_block_maximum,
            "all_bounds_passed": True,
            "scope": "every admitted T=mB, 2<=B<=1024 power of two, T<=8192, both selectors; maximum D by monotonicity"}


def main(repo, out):
    if out.exists():
        raise FileExistsError("Preserve earlier evidence; use a fresh output directory")
    out.mkdir(parents=True)
    sources = ("v3/derivations/08_snapshot_live_reporting.md",
               "v3/derivations/08_live_hard_performance.md",
               "v3/derivations/07_observable_performance.md",
               "v3/experiments/p308_broker.py")
    before = {path: digest(repo/path) for path in sources}
    for relative in sources:
        dest = out/"source"/relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes((repo/relative).read_bytes())
    (out/"check_math.py").write_bytes(Path(__file__).read_bytes())
    (out/"plan.md").write_bytes(Path(__file__).with_name("plan.md").read_bytes())
    (out/"manifest_before.json").write_text(json.dumps({"sources": before,
        "checker": digest(Path(__file__)), "created_utc": datetime.now(timezone.utc).isoformat(),
        "runtime": sys.version, "stage": "DEVELOPMENT", "principal_time_credit_seconds": 0}, indent=2)+"\n")
    result = {"algebra": check_algebra(), "grid_and_width": check_contracts(),
              "private_score_reads": 0, "principal_time_credit_seconds": 0}
    after = {path: digest(repo/path) for path in sources}
    result["source_unchanged"] = before == after
    (out/"manifest_after.json").write_text(json.dumps({"sources": after,
        "created_utc": datetime.now(timezone.utc).isoformat(), "unchanged": before==after}, indent=2)+"\n")
    (out/"results.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"algebra": result["algebra"], "source_unchanged": result["source_unchanged"],
                     "grid_and_width": {k:v for k,v in result["grid_and_width"].items()
                                        if k not in ("per_B_maximum", "extremal_comparison")}}, indent=2))


if __name__ == "__main__":
    main(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve())
