"""Exact-box, native-metric joint feasibility from saved weights and masks only.

No model forward, fit, optimizer or population generator is used.
Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-05.
"""
from __future__ import annotations

from fractions import Fraction as F
import hashlib
import itertools
import json
import math
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RUN = ROOT / "v2/work_logs/F15_ND01_v1_run1"
SCALE = 10 ** 60
METHODS = ("frozen_original", "binary_global", "rounded_top8", "fractional_mask")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verified(path):
    assert digest(path) == Path(str(path) + ".sha256").read_text().split()[0]
    return json.loads(path.read_text())


def rational(x):
    return F.from_float(float(x))


def rank(matrix):
    a = [row.copy() for row in matrix]
    if not a or not a[0]:
        return 0
    row = 0
    for col in range(len(a[0])):
        pivot = next((j for j in range(row, len(a)) if a[j][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        value = a[row][col]
        a[row] = [x / value for x in a[row]]
        for j in range(row + 1, len(a)):
            factor = a[j][col]
            a[j] = [x - factor * y for x, y in zip(a[j], a[row])]
        row += 1
        if row == len(a):
            break
    return row


def geometry(network):
    w = [[rational(x) for x in row] for row in network["w"]]
    b = [rational(x) for x in network["b"]]
    corners = list(itertools.product((F(-1), F(1)), (F(-1), F(1)),
                                     (F(1, 2), F(2)), (F(1, 2), F(2))))
    groups = {"inactive": [], "active": [], "variable": []}
    planes, duplicate_pairs, units = {}, [], []
    for j in range(32):
        values = [b[j] + sum(w[i][j] * x[i] for i in range(4)) for x in corners]
        lo, hi = min(values), max(values)
        group = "inactive" if hi <= 0 else "active" if lo >= 0 else "variable"
        groups[group].append(j)
        units.append({"unit": j, "group": group, "min_exact": str(lo), "max_exact": str(hi)})
        if group == "variable":
            affine = tuple([w[i][j] for i in range(4)] + [b[j]])
            pivot = next(x for x in affine if x)
            canonical = tuple(x / pivot for x in affine)
            if canonical in planes:
                duplicate_pairs.append([planes[canonical], j])
            planes[canonical] = j
    active_rank = rank([[w[i][j] for j in groups["active"]] for i in range(4)])
    prerequisites = not duplicate_pairs and active_rank == len(groups["active"]) and len(groups["inactive"]) >= 2
    return {**groups, "units": units, "duplicate_variable_hyperplanes": duplicate_pairs,
            "pairwise_variable_hyperplane_comparisons": math.comb(len(groups["variable"]), 2),
            "exact_active_weight_rank": active_rank,
            "unique_kink_rank_formula_applies": not duplicate_pairs,
            "exact_difference_span_rank": len(groups["variable"]) + active_rank if not duplicate_pairs else None,
            "nullspace_is_exactly_inactive_coordinates": not duplicate_pairs and active_rank == len(groups["active"]),
            "two_sphere_specialization_prerequisites": prerequisites}


def sqrt_bounds(x):
    assert x >= 0
    root = math.isqrt((x.numerator * SCALE * SCALE) // x.denominator)
    lo, hi = F(root, SCALE), F(root + 1, SCALE)
    assert lo * lo <= x < hi * hi
    return lo, hi


def mask(role, method):
    if method == "fractional_mask":
        return [rational(x) for x in role["mask"]["values"]]
    subset = {"frozen_original": role["original_subset"],
              "binary_global": role["binary_global"]["subset"],
              "rounded_top8": role["rounded_subset"]}[method]
    return [F(int(j in subset)) for j in range(32)]


def classify(v, masks, inactive):
    active = [j for j in range(32) if j not in inactive]
    for m in masks:
        assert all(0 <= x <= 1 for x in m)
    deltas = [sum(m[j] * (1 - m[j]) * v[j] ** 2 for j in active) for m in masks]
    overlap = sum(masks[0][j] * masks[1][j] * v[j] ** 2 for j in active)
    t2 = sum(v[j] ** 2 for j in inactive) / 4
    r2 = [x + t2 for x in deltas]
    central = (sum(deltas) + t2) ** 2 <= 4 * r2[0] * r2[1]
    if central:
        lower = upper = (sum(deltas) + t2) / 2
        branch = "central_rational"
    else:
        small, large = sorted(r2)
        sl, su = sqrt_bounds(small)
        ll, lu = sqrt_bounds(large)
        tl, tu = sqrt_bounds(t2)
        lower = (sl + tl) * max(F(0), ll - tu)
        upper = (su + tu) * (lu - tl)
        branch = "outer_certified_sqrt_intervals"
    lo, hi = lower - overlap, upper - overlap
    status = "feasible" if lo >= 0 else "infeasible" if hi < 0 else "unresolved_interval_boundary"
    # With exactly binary disjoint supports, their native projectors witness feasibility.
    disjoint = not any(masks[0][j] * masks[1][j] for j in range(32))
    binary = all(x in (0, 1) for m in masks for x in m)
    if disjoint and binary:
        assert status == "feasible"
    return {"status": status, "delta0_exact": str(deltas[0]), "delta1_exact": str(deltas[1]),
            "observable_overlap_exact": str(overlap), "inactive_head_quarter_energy_exact": str(t2),
            "delta0": float(deltas[0]), "delta1": float(deltas[1]),
            "observable_overlap": float(overlap), "inactive_head_quarter_energy": float(t2),
            "maximum_cancellation_lower_exact": str(lower), "maximum_cancellation_upper_exact": str(upper),
            "feasibility_margin_lower_exact": str(lo), "feasibility_margin_upper_exact": str(hi),
            "maximum_cancellation": float((lower + upper) / 2),
            "feasibility_margin": float((lo + hi) / 2), "branch": branch,
            "certified_interval_width": float(hi - lo),
            "native_disjoint_binary_witness": disjoint and binary}


def analyze():
    mechanism_path = HERE / "mechanism_results.json"
    mechanism = verified(mechanism_path)
    manifest_path = RUN / "preparation_complete.json"
    manifest = verified(manifest_path)
    assert digest(manifest_path) == mechanism["preparation_manifest_sha256"]
    inputs = {str(mechanism_path.relative_to(ROOT)): digest(mechanism_path),
              str(manifest_path.relative_to(ROOT)): digest(manifest_path)}
    sources = manifest["freeze"]["source_prepared"]
    soft = {u["index"]: u for u in manifest["units"] if u["kind"] == "soft_mask"}
    geometries, rows = [], []
    for i in range(5):
        source_path = ROOT / sources[i]["path"]
        assert digest(source_path) == sources[i]["sha256"]
        source = json.loads(source_path.read_text())
        prep_path = RUN / soft[i]["file"]
        prepared = verified(prep_path)
        inputs[str(source_path.relative_to(ROOT))] = digest(source_path)
        inputs[str(prep_path.relative_to(ROOT))] = digest(prep_path)
        geo = geometry(source["network"])
        geo["model_index"] = i
        geometries.append(geo)
        v = [rational(x) for x in source["network"]["v"]]
        for method in METHODS:
            result = classify(v, [mask(r, method) for r in prepared["roles"]], geo["inactive"]) if geo["two_sphere_specialization_prerequisites"] else {"status": "prerequisite_not_established"}
            rows.append({"model_index": i, "method": method, **result})
    counts = {method: {status: sum(r["method"] == method and r["status"] == status for r in rows)
                       for status in ("feasible", "infeasible", "unresolved_interval_boundary", "prerequisite_not_established")}
              for method in METHODS}
    return {"schema": "F15-ND01-joint-feasibility-v1", "contributor": "ChatGPT (GPT-6 Astra Pro)",
            "development_only": True, "post_outcome_supplementary": True,
            "scope": "exact output effects of existing masks over the whole declared input box, stored Euclidean hidden metric, rational stored coefficients",
            "native_metric_not_gauge_invariant": True, "new_fits": 0, "new_populations": 0, "model_forwards": 0,
            "sqrt_enclosure_decimal_places": 60, "geometries": geometries, "rows": rows, "counts": counts,
            "inputs": inputs, "script_sha256": digest(Path(__file__)),
            "does_not_establish": ["semantic joint cost adequacy", "unique native representation", "DAS execution", "approximate infeasibility", "F15 support"]}


def main():
    target = HERE / "joint_feasibility.json"
    value = analyze()
    encoded = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
    if sys.argv[1:] == ["--check"]:
        assert target.read_bytes() == encoded
        assert Path(str(target) + ".sha256").read_text().strip() == digest(target)
        print("Joint feasibility reproduced byte for byte.")
        return
    assert not sys.argv[1:]
    with target.open("xb") as handle:
        handle.write(encoded)
    with Path(str(target) + ".sha256").open("x") as handle:
        handle.write(digest(target) + "\n")
    print(json.dumps({"output": str(target), "sha256": digest(target), "counts": value["counts"]}, indent=2))


if __name__ == "__main__":
    main()
