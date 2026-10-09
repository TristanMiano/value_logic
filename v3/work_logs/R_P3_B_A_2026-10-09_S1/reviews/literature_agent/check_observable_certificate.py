#!/usr/bin/env python3
"""Exact structural witnesses only; never imports or executes a learner/service."""

from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from math import isqrt, factorial
from pathlib import Path
import json


HERE = Path(__file__).resolve().parent
TARGET = HERE / "observable_certificate_probe_target_v1.json"
B = 2
M = 4
S = 4
LABELS = (0, 1)


def ceil_sqrt(n):
    r = isqrt(n)
    return r if r * r == n else r + 1


def frac(x):
    x = F(x)
    return {"numerator": x.numerator, "denominator": x.denominator}


def policy(history, null):
    favored = history[-1] if history else 0
    pi = tuple(F(3, 4) if j == favored else F(1, 4) for j in range(B))
    q = F(1, 2) if null or history.count(0) % 2 else F(1, 4)
    qs = (q, q)
    d = tuple(qs[j] + (1 - 2 * qs[j]) * LABELS[j] for j in range(B))
    g = tuple((qs[j] - LABELS[j]) ** 2 for j in range(B))
    v = tuple(x * (1 - x) for x in qs)
    r = tuple(x - F(1, 2) for x in d)
    c = max(abs(1 - 2 * qs[j]) / pi[j] for j in range(B))
    return pi, qs, d, g, v, r, c


def exhaustive(null):
    histories = 0
    max_width = F(0)
    max_centered_width = F(0)
    for k in range(M):
        for history in product(range(B), repeat=k):
            pi, qs, d, g, v, r, c = policy(history, null)
            errors = (
                tuple(sum(d) - d[j] / pi[j] for j in range(B)),
                tuple(sum(g) - g[j] / pi[j] for j in range(B)),
                tuple(sum(r) - r[j] / pi[j] for j in range(B)),
            )
            for e in errors:
                assert sum(pi[j] * e[j] for j in range(B)) == 0
            widths = tuple(max(e) - min(e) for e in errors)
            assert widths[0] <= S and widths[1] <= S
            assert widths[2] <= c <= S
            assert all(g[j] == d[j] - v[j] for j in range(B))
            max_width = max(max_width, widths[0], widths[1])
            max_centered_width = max(max_centered_width, widths[2])
            histories += 1

    rows = []
    total_selector_probability = F(0)
    total_joint_probability = F(0)
    action_atoms = 0
    prefix_checks = 0
    for path in product(range(B), repeat=M):
        probability = F(1)
        u = a = vtarget = ftarget = selected_d = public_v = F(0)
        centered_u_sum = centered_a_sum = width_squares = F(0)
        vcap = fcap = F(0)
        action_means = []
        prefix_rows = []
        for k, selected in enumerate(path, start=1):
            pi, qs, d, g, v, r, c = policy(path[:k - 1], null)
            probability *= pi[selected]
            u += (1 / pi[selected] - 1) * d[selected]
            a += g[selected] / pi[selected]
            vtarget += sum(d[j] for j in range(B) if j != selected)
            ftarget += sum(g)
            selected_d += d[selected]
            public_v += sum(v)
            centered_u_sum += (1 / pi[selected] - 1) * r[selected]
            centered_a_sum += r[selected] / pi[selected]
            width_squares += c * c
            vcap += sum(max(qs[j], 1 - qs[j]) for j in range(B) if j != selected)
            fcap += sum(max(x * x, (1 - x) ** 2) for x in qs)
            action_means.extend(d[j] for j in range(B) if j != selected)
            uc = F(k * (B - 1), 2) + centered_u_sum
            ac = F(k * B, 2) - public_v + centered_a_sum
            assert vtarget - uc == ftarget - ac
            assert ftarget - vtarget == selected_d - public_v
            assert uc - u == F(k * B, 2) - sum(
                1 / policy(path[:i], null)[0][path[i]] for i in range(k)
            ) / 2
            assert vtarget <= vcap and ftarget <= fcap
            if null:
                assert width_squares == 0
                assert vtarget == uc == vcap == F(k * (B - 1), 2)
                assert ftarget == ac == fcap == F(k * B, 4)
            prefix_rows.append({
                "blocks": k,
                "shared_deviation": frac(vtarget - uc),
                "public_target_offset": frac(selected_d - public_v),
                "predictable_width_square_sum": frac(width_squares),
            })
            prefix_checks += 1

        conditional_mass = conditional_first = conditional_second = F(0)
        for errors in product((0, 1), repeat=len(action_means)):
            p = F(1)
            for e, d in zip(errors, action_means):
                p *= d if e else 1 - d
            z = sum(errors)
            conditional_mass += p
            conditional_first += p * z
            conditional_second += p * z * z
            total_joint_probability += probability * p
            action_atoms += 1
        assert conditional_mass == 1
        assert conditional_first == vtarget
        assert conditional_second - vtarget ** 2 == sum(d * (1 - d) for d in action_means)
        total_selector_probability += probability
        radius_scale = S * ceil_sqrt(2 * M)
        radius = width_squares / radius_scale + F(radius_scale, 2)
        assert radius <= radius_scale
        rows.append({
            "selector_path": list(path),
            "probability": frac(probability),
            "U": frac(u), "A": frac(a),
            "U_centered": frac(uc), "A_centered": frac(ac),
            "V_conditional_action_mean": frac(vtarget), "F_all_issued_Brier": frac(ftarget),
            "conditional_terminal_variance": frac(conditional_second - vtarget ** 2),
            "centered_radius": frac(radius),
            "public_conditional_mean_cap": frac(vcap), "public_Brier_cap": frac(fcap),
            "prefixes": prefix_rows,
        })
    assert total_selector_probability == total_joint_probability == 1
    return {
        "variant": "constant-half" if null else "history-dependent-quarter-or-half",
        "histories_checked": histories,
        "selector_paths": len(rows),
        "selector_action_atoms": action_atoms,
        "prefix_identity_checks": prefix_checks,
        "total_selector_probability": frac(total_selector_probability),
        "total_joint_probability": frac(total_joint_probability),
        "largest_baseline_conditional_width": frac(max_width),
        "largest_centered_conditional_width": frac(max_centered_width),
        "rows": rows,
    }


def fixed_witnesses():
    probabilities = (F(3, 4), F(1, 4))
    d = (F(0), F(1))
    errors = tuple(sum(d) - d[j] / probabilities[j] for j in range(2))
    assert errors == (F(1), F(-3))
    assert sum(p * e for p, e in zip(probabilities, errors)) == 0
    assert max(errors) - min(errors) == 4

    m = 64
    s = 4
    radius_scale = s * ceil_sqrt(2 * m)
    u = F(0)
    uc = F(m, 2) - F(m, 6)
    width_squares = F(16 * m)
    radius = width_squares / radius_scale + F(radius_scale, 2)
    baseline_upper = min(F(m), u + radius_scale)
    centered_upper = min(F(m), uc + radius)
    assert radius_scale == 48 and radius == F(136, 3)
    assert uc == F(64, 3)
    assert radius < radius_scale and baseline_upper == 48 and centered_upper == 64
    assert centered_upper > baseline_upper

    joint_a1_and_j2 = F(1, 2) * F(3, 4)
    j2_mass = joint_a1_and_j2 + F(1, 2) * F(1, 4)
    conditional_a1 = joint_a1_and_j2 / j2_mass
    assert conditional_a1 == F(3, 4) != F(1, 2)
    exp4_partial = sum(F(4 ** j, factorial(j)) for j in range(6))
    assert exp4_partial == F(643, 15) > 40
    return {
        "sharp_width": {"increments": [frac(x) for x in errors], "width": 4},
        "centered_bound_can_be_larger": {
            "blocks": m, "B": 2, "pi": [frac(x) for x in probabilities],
            "fixed_forecasts": [0, 0], "fixed_labels": [0, 1],
            "path": "position 0 selected in every block",
            "path_probability": frac(F(3, 4) ** m),
            "true_V": m, "U": frac(u), "U_centered": frac(uc),
            "baseline_radius": radius_scale, "centered_radius": frac(radius),
            "baseline_clipped_upper": frac(baseline_upper),
            "centered_clipped_upper": frac(centered_upper),
            "interpretation": "Rare path counterexample to pointwise upper-bound improvement, not a coverage refutation."
        },
        "action_dependent_selector_conditioning": {
            "unconditional_action_one_probability": frac(F(1, 2)),
            "conditional_action_one_probability_given_future_selection": frac(conditional_a1),
            "interpretation": "Shows why full-selector-history conditioning requires the stated action-independent policy."
        },
        "strict_log40_certificate": {"partial_exp4_series": frac(exp4_partial), "greater_than_40": True},
    }


def finite_arithmetic_bounds():
    tmax, bmax, hmax = 8192, 1024, 32
    q0 = 1 << hmax
    m = tmax // bmax
    candidates = {
        "uniform_U": (tmax - m) * q0,
        "uniform_A": tmax * q0 ** 2,
        "ticket_U": m * (bmax + 1) * (2 * bmax - 1) * q0,
        "ticket_A": 2 * tmax * (bmax + 1) * q0 ** 2,
        "uniform_width_square_sum": tmax * bmax * q0 ** 2,
        "ticket_width_square_sum": 4 * tmax * bmax * (bmax + 1) ** 2 * q0 ** 2,
    }
    return {
        "source_caps": {"T": tmax, "B": bmax, "h": hmax},
        "meaning": "Safe raw common-denominator numerator bounds, not generic Fraction intermediate bounds or deployed storage claims.",
        "bounds": {name: {"integer": val, "bit_length": val.bit_length()} for name, val in candidates.items()},
        "dyadic_Brier_denominator_integer_bit_length": (q0 ** 2).bit_length(),
        "centered_estimates_require_signed_storage": True,
    }


def main():
    target_bytes = TARGET.read_bytes()
    target = json.loads(target_bytes)
    assert target["version"] == "observable-certificate-structural-probe-v1"
    results = {
        "version": "observable-certificate-structural-probe-v1",
        "target_sha256": sha256(target_bytes).hexdigest(),
        "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "status": "PASS",
        "method": "Exact exhaustive rational calculation; no random generator or experimental archive inputs.",
        "scope": "Structural reconstruction only. Confidence coverage follows from the written theorem, not this small finite probe.",
        "principal_clock_credit_seconds": 0,
        "exhaustive_cases": [exhaustive(False), exhaustive(True)],
        "fixed_witnesses": fixed_witnesses(),
        "finite_arithmetic_bounds": finite_arithmetic_bounds(),
    }
    path = HERE / "observable_certificate_probe_result_v1.json"
    path.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps({
        "status": "PASS", "result": str(path),
        "variants": len(results["exhaustive_cases"]),
        "total_selector_paths": sum(x["selector_paths"] for x in results["exhaustive_cases"]),
        "total_selector_action_atoms": sum(x["selector_action_atoms"] for x in results["exhaustive_cases"]),
        "fixed_witnesses": 3,
        "source_runs": 0, "principal_clock_credit_seconds": 0,
    }))


if __name__ == "__main__":
    main()
