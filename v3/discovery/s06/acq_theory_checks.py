"""Small exact arithmetic constructions for acq_theory.md.

ChatGPT (GPT-6 Astra Pro), 2026-10-12. DEVELOPMENT.
This does not call a solver, learn a population law, or model provider runtime.
"""

from __future__ import annotations

import itertools
import json
from fractions import Fraction as F
from pathlib import Path


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def support(vertices, c):
    return max(dot(v, c) for v in vertices)


def dual_budget(q, c, b):
    knots = {F(0)} | {F(cj, qj) for qj, cj in zip(q, c) if qj > 0}
    rows = [
        (lam * b + sum(max(F(0), cj - lam * qj) for qj, cj in zip(q, c)), lam)
        for lam in knots
    ]
    return min(rows)


def check_bundle():
    rows = []
    for k in range(9):
        y = F(k, 8)
        fixed = min(y, 1 - y)
        mix = y * (1 - y)
        q_star = y
        assert max(q_star * (1 - y), (1 - q_star) * y) == mix
        # The maximum is one of two lines; their intersection is minimax.
        for q in {F(k, 16) for k in range(17)} | {q_star}:
            assert max(q * (1 - y), (1 - q) * y) >= mix
        assert fixed <= F(1, 2)
        assert mix <= F(1, 4)
        rows.append({"audit_y": y, "audit_only": y, "joined_fixed": fixed,
                     "mix_probability_first": q_star, "joined_expected": mix})
    return {"initial": F(1), "proof_only": F(1),
            "worst_audit_only": max(r["audit_only"] for r in rows),
            "worst_joined_fixed": max(r["joined_fixed"] for r in rows),
            "worst_joined_expected": max(r["joined_expected"] for r in rows),
            "rows": rows}


def check_common_support():
    # Independent row sets as epistemic constraints, not random assumptions.
    # Row one has known difference 1; row two has known difference -1/2.
    q1 = [(F(1), F(0)), (F(3), F(2))]
    q2 = [(F(0), F(1, 2)), (F(2), F(5, 2))]
    c = (F(1), F(-1))
    mean_vertices = [tuple((x + y) / 2 for x, y in zip(a, b))
                     for a in q1 for b in q2]
    whole = support(mean_vertices, c)
    additive = (support(q1, c) + support(q2, c)) / 2
    assert whole == additive == F(1, 4)
    box_hi = [max(v[j] for v in mean_vertices) for j in range(2)]
    box_lo = [min(v[j] for v in mean_vertices) for j in range(2)]
    box_upper = box_hi[0] - box_lo[1]
    assert box_upper == F(9, 4) > whole
    return {"exact_common_contrast": whole, "coordinate_box_upper": box_upper,
            "retained_rows": 2, "enumerated_vertex_pairs": len(mean_vertices)}


def check_quotes():
    lo, hi, b = (2, 3, 0), (4, 5, 6), 3
    vectors = list(itertools.product((0, 1), repeat=3))
    budget_vectors = [z for z in vectors if dot(lo, z) <= b]
    exact = max(dot(hi, z) for z in budget_vectors)
    dual, lam = dual_budget(lo, hi, b)
    coarse = b + sum(h - l for l, h in zip(lo, hi))
    assert exact == 11 and dual == F(35, 3) and coarse == 13
    assert all(dot(hi, z) <= dual for z in budget_vectors)
    signed_rows = []
    weight_corners = list(itertools.product(*zip(lo, hi)))
    for v in [(1, 0, 0), (0, 1, 0)]:
        c = tuple(l if vi else h for vi, l, h in zip(v, lo, hi))
        offset = dot(v, lo)
        direct = max(support(weight_corners, tuple(zi - vi for zi, vi in zip(z, v)))
                     for z in budget_vectors)
        reduced = max(dot(c, z) - offset for z in budget_vectors)
        quoted, quote_lam = dual_budget(lo, c, b)
        quoted -= offset
        assert direct == reduced <= quoted
        signed_rows.append({"support_v": v, "exact_budget_contrast": direct,
                            "fractional_bound": quoted, "lambda": quote_lam})
    return {"lower": lo, "upper": hi, "budget": b,
            "enumerated_boolean_vectors": len(vectors),
            "budget_compatible_vectors": len(budget_vectors),
            "coarse_cost_quote": coarse, "exact_objective_only_quote": exact,
            "fractional_quote": dual, "fractional_lambda": lam,
            "signed_quotes": signed_rows}


def encode(x):
    if isinstance(x, F):
        return str(x)
    raise TypeError(type(x).__name__)


def main():
    result = {
        "contributor": "ChatGPT (GPT-6 Astra Pro)",
        "status": "DEVELOPMENT arithmetic reconstruction",
        "scope": "finite arithmetic only; no provider calls or population observations",
        "provider_calls": 0,
        "bundle": check_bundle(),
        "common_support": check_common_support(),
        "bounded_query_quotes": check_quotes(),
    }
    path = Path(__file__).with_name("acq_theory_results.json")
    path.write_text(json.dumps(result, indent=2, default=encode) + "\n")
    print(json.dumps({"result_path": str(path), "checks": "passed", "provider_calls": 0}))


if __name__ == "__main__":
    main()
