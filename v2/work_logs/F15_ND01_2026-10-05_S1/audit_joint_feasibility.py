"""Independent rational audit of existing-mask joint feasibility.

No model forwards, input populations, fits or numerical optimizers. Does not
import the joint-feasibility implementation or its geometry/rank helpers.
Contributor: ChatGPT (GPT-6 Astra Pro), independent relaxation-analysis agent.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import datetime
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SESSION = Path(__file__).resolve().parent
ANALYSIS = ROOT / "v2/experiments/F15_ND01_analysis"
RUN = ROOT / "v2/work_logs/F15_ND01_v1_run1"
COUNTS = Counter()
FAILURES = []
INPUTS = {}


def digest(path):
    encoded = path.read_bytes()
    value = hashlib.sha256(encoded).hexdigest()
    INPUTS[str(path.relative_to(ROOT))] = {"sha256": value, "bytes": len(encoded)}
    return value


def load(path):
    digest(path)
    return json.loads(path.read_text(encoding="utf-8"))


def check(condition, category, label):
    COUNTS[category] += 1
    if not condition:
        FAILURES.append({"category": category, "label": label})


def check_exact(saved, expected, category, label):
    check(Fraction(saved) == expected, category, label + "/rational")
    check(str(expected) == saved, category, label + "/canonical string")


def rat(value):
    return Fraction.from_float(float(value))


def rank_by_elimination(matrix):
    a = [row[:] for row in matrix]
    if not a or not a[0]:
        return 0
    row = 0
    for col in range(len(a[0])):
        selected = next((j for j in range(row, len(a)) if a[j][col]), None)
        if selected is None:
            continue
        a[row], a[selected] = a[selected], a[row]
        # Eliminate with cross multiplication, no row normalization.
        pivot = a[row][col]
        for j in range(row + 1, len(a)):
            factor = a[j][col]
            a[j] = [pivot * x - factor * y for x, y in zip(a[j], a[row])]
        row += 1
        if row == len(a):
            break
    return row


def masks_from_role(role, method):
    if method == "fractional_mask":
        return [rat(x) for x in role["mask"]["values"]]
    subset = {"frozen_original": role["original_subset"],
              "binary_global": role["binary_global"]["subset"],
              "rounded_top8": role["rounded_subset"]}[method]
    return [Fraction(int(j in subset)) for j in range(32)]


def main():
    output = SESSION / "audit_joint_feasibility.json"
    note = SESSION / "audit_joint_feasibility.md"
    if output.exists() or note.exists():
        raise FileExistsError("Preserve prior joint-feasibility audit output.")
    target = ANALYSIS / "joint_feasibility.json"
    result = load(target)
    check(digest(target) == target.with_suffix(".json.sha256").read_text().strip(), "provenance", "joint output sidecar")
    check(result["script_sha256"] == digest(ANALYSIS / "joint_feasibility.py"), "provenance", "joint source binding")
    digest(ANALYSIS / "joint_feasibility.md")
    for name, expected in result["inputs"].items():
        check(digest(ROOT / name) == expected, "provenance", name)
    mechanism = load(ANALYSIS / "mechanism_results.json")
    manifest = load(RUN / "preparation_complete.json")
    check(digest(RUN / "preparation_complete.json") == mechanism["preparation_manifest_sha256"], "provenance", "mechanism preparation binding")
    check(manifest["status"] == "preparation_complete" and len(manifest["units"]) == 15, "provenance", "fifteen completed preparations")
    check(manifest["freeze"] == mechanism["freeze"], "provenance", "common freeze binding")
    check(mechanism["freeze"]["manifest_sha256"] == digest(ROOT / "v2/experiments/neural_diagnostic_v1/freeze.json"), "provenance", "current diagnostic freeze")
    geometries = {row["model_index"]: row for row in result["geometries"]}
    source_records = manifest["freeze"]["source_prepared"]
    soft_records = {u["index"]: u for u in manifest["units"] if u["kind"] == "soft_mask"}
    sources, prepared, exact_geometry = {}, {}, {}
    plane_comparisons = 0
    for index in range(5):
        record, soft_record = source_records[index], soft_records[index]
        source_path, soft_path = ROOT / record["path"], RUN / soft_record["file"]
        check(digest(source_path) == record["sha256"], "provenance", f"source model {index}")
        check(digest(soft_path) == soft_record["sha256"], "provenance", f"soft preparation {index}")
        source, soft = load(source_path), load(soft_path)
        sources[index], prepared[index] = source, soft
        check(source["network"] == soft["network"], "provenance", f"unaltered network {index}")
        check(soft["original_prepared_artifact_hash"] == source["artifact_hash"], "provenance", f"original artifact identity {index}")
        network, geo = source["network"], geometries[index]
        w = [[rat(x) for x in row] for row in network["w"]]
        b = [rat(x) for x in network["b"]]
        box = [(Fraction(-1), Fraction(1)), (Fraction(-1), Fraction(1)),
               (Fraction(1, 2), Fraction(2)), (Fraction(1, 2), Fraction(2))]
        classified = {"inactive": [], "active": [], "variable": []}
        for j, unit in enumerate(geo["units"]):
            # Exact sign-based bounds, independent of the source corner loop.
            low = b[j] + sum(min(w[i][j] * lo, w[i][j] * hi) for i, (lo, hi) in enumerate(box))
            high = b[j] + sum(max(w[i][j] * lo, w[i][j] * hi) for i, (lo, hi) in enumerate(box))
            group = "inactive" if high <= 0 else "active" if low >= 0 else "variable"
            classified[group].append(j)
            check(unit["unit"] == j and unit["group"] == group, "geometry", f"group {index}/{j}")
            check_exact(unit["min_exact"], low, "geometry", f"minimum {index}/{j}")
            check_exact(unit["max_exact"], high, "geometry", f"maximum {index}/{j}")
            if group == "variable":
                check(low < 0 < high and any(w[i][j] for i in range(4)), "geometry", f"interior kink prerequisite {index}/{j}")
        for group, indices in classified.items():
            check(geo[group] == indices, "geometry", f"{group} indices {index}")
        duplicates = []
        for j, k in itertools.combinations(classified["variable"], 2):
            left = [w[i][j] for i in range(4)] + [b[j]]
            right = [w[i][k] for i in range(4)] + [b[k]]
            # Two nonzero 5-vectors define the same unoriented hyperplane iff
            # every 2x2 minor vanishes. This avoids the source normalization.
            distinct = any(left[p] * right[q] != left[q] * right[p]
                           for p, q in itertools.combinations(range(5), 2))
            check(distinct, "hyperplanes", f"distinct interior kink {index}/{j}/{k}")
            if not distinct:
                duplicates.append([j, k])
            plane_comparisons += 1
        active = classified["active"]
        active_rank = rank_by_elimination([[w[i][j] for j in active] for i in range(4)])
        span_rank = len(classified["variable"]) + active_rank
        prerequisites = not duplicates and active_rank == len(active) and len(classified["inactive"]) >= 2
        check(duplicates == geo["duplicate_variable_hyperplanes"], "geometry", f"hyperplane equality result {index}")
        check(geo["pairwise_variable_hyperplane_comparisons"] == math.comb(len(classified["variable"]), 2), "geometry", f"pair count {index}")
        check(active_rank == geo["exact_active_weight_rank"], "geometry", f"active rank {index}")
        check(geo["unique_kink_rank_formula_applies"] == (not duplicates), "geometry", f"rank formula prerequisites {index}")
        check(geo["exact_difference_span_rank"] == span_rank, "geometry", f"complete difference span rank {index}")
        check(geo["nullspace_is_exactly_inactive_coordinates"] == (not duplicates and active_rank == len(active)), "geometry", f"nullspace specialization {index}")
        check(geo["two_sphere_specialization_prerequisites"] == prerequisites, "geometry", f"all two-sphere prerequisites {index}")
        check(prerequisites and 32 - span_rank == len(classified["inactive"]), "geometry", f"certified applicable dimension {index}")
        exact_geometry[index] = {"inactive": classified["inactive"], "difference_span_rank": span_rank,
                                 "nullspace_dimension": 32 - span_rank}
    counts = {method: Counter() for method in ("frozen_original", "binary_global", "rounded_top8", "fractional_mask")}
    recomputed_rows = []
    for row in result["rows"]:
        index, method = row["model_index"], row["method"]
        v = [rat(x) for x in sources[index]["network"]["v"]]
        masks = [masks_from_role(role, method) for role in prepared[index]["roles"]]
        inactive = exact_geometry[index]["inactive"]
        observable = [j for j in range(32) if j not in inactive]
        check(all(0 <= value <= 1 for mask in masks for value in mask), "feasibility", f"mask domain {index}/{method}")
        # Compute c.v-c.c directly, independently of source m*(1-m)*v^2.
        coefficients = [[mask[j] * v[j] for j in observable] for mask in masks]
        deltas = [sum(c * v[j] - c * c for c, j in zip(coefficient, observable)) for coefficient in coefficients]
        overlap = sum(c0 * c1 for c0, c1 in zip(*coefficients))
        t2 = sum(v[j] * v[j] for j in inactive) / 4
        check(all(delta >= 0 for delta in deltas) and overlap >= 0 and t2 >= 0, "feasibility", f"nonnegative sphere quantities {index}/{method}")
        radii_squared = [delta + t2 for delta in deltas]
        central_discriminant = 4 * radii_squared[0] * radii_squared[1] - (sum(deltas) + t2) ** 2
        check(central_discriminant >= 0 and row["branch"] == "central_rational", "feasibility", f"exact central branch {index}/{method}")
        capacity = (deltas[0] + deltas[1] + t2) / 2
        margin = capacity - overlap
        status = "feasible" if margin >= 0 else "infeasible"
        check(row["status"] == status, "feasibility", f"exact status {index}/{method}")
        exact = {
            "delta0_exact": deltas[0], "delta1_exact": deltas[1],
            "observable_overlap_exact": overlap,
            "inactive_head_quarter_energy_exact": t2,
            "maximum_cancellation_lower_exact": capacity,
            "maximum_cancellation_upper_exact": capacity,
            "feasibility_margin_lower_exact": margin,
            "feasibility_margin_upper_exact": margin,
        }
        for name, value in exact.items():
            check_exact(row[name], value, "feasibility", f"{index}/{method}/{name}")
        displays = {"delta0": deltas[0], "delta1": deltas[1],
                    "observable_overlap": overlap, "inactive_head_quarter_energy": t2,
                    "maximum_cancellation": capacity, "feasibility_margin": margin}
        for name, value in displays.items():
            check(row[name] == float(value), "feasibility", f"float display {index}/{method}/{name}")
        check(row["certified_interval_width"] == 0.0, "feasibility", f"rational point interval {index}/{method}")
        binary = all(value in (0, 1) for mask in masks for value in mask)
        disjoint = all(masks[0][j] * masks[1][j] == 0 for j in range(32))
        check(row["native_disjoint_binary_witness"] == (binary and disjoint), "feasibility", f"native disjoint witness {index}/{method}")
        check(not (binary and disjoint) or status == "feasible", "feasibility", f"known disjoint feasibility {index}/{method}")
        counts[method][status] += 1
        recomputed_rows.append({"model_index": index, "method": method, "status": status,
            "central_branch_discriminant_exact": str(central_discriminant),
            "observable_overlap_exact": str(overlap), "capacity_exact": str(capacity),
            "margin_exact": str(margin), "margin": float(margin)})
    expected_statuses = ("feasible", "infeasible", "unresolved_interval_boundary", "prerequisite_not_established")
    count_dict = {method: {status: values[status] for status in expected_statuses} for method, values in counts.items()}
    check(count_dict == result["counts"], "cardinality", "reported feasibility counts")
    check(len(recomputed_rows) == 20 and len(exact_geometry) == 5, "cardinality", "all existing masks/models")
    check(result["native_metric_not_gauge_invariant"] is True and result["post_outcome_supplementary"] is True
          and result["development_only"] is True, "scope", "metric and supplementary labels")
    check(result["new_fits"] == result["new_populations"] == result["model_forwards"] == 0, "scope", "no experiment generation")
    check(set(result["does_not_establish"]) >= {"semantic joint cost adequacy", "unique native representation", "DAS execution", "approximate infeasibility", "F15 support"}, "scope", "claim boundaries")
    fractional = [r for r in recomputed_rows if r["method"] == "fractional_mask"]
    report = {"schema": "F15-ND01-independent-joint-feasibility-audit-v1",
        "contributor": "ChatGPT (GPT-6 Astra Pro), independent relaxation-analysis agent",
        "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "all_checks_passed": not FAILURES, "total_checks": sum(COUNTS.values()), "checks": dict(COUNTS),
        "failures": FAILURES, "inputs": INPUTS, "recomputed_counts": count_dict,
        "recomputed_rows": recomputed_rows,
        "geometry": exact_geometry, "pairwise_hyperplane_comparisons": plane_comparisons,
        "rational_central_cases": 20, "square_root_boundary_helper_needed": False,
        "model_forwards": 0, "new_populations": 0, "new_fits": 0, "optimizers_called": 0,
        "interpretation": "Exact feasibility for reproducing the existing masks' single-role output effects over the entire input box by mutually orthogonal projectors in the stored native Euclidean metric. It does not establish semantic joint cost adequacy or ND02 execution; it is not F16."}
    encoded = (json.dumps(report, sort_keys=True, indent=2) + "\n").encode()
    output.write_bytes(encoded)
    output.with_suffix(".json.sha256").write_text(hashlib.sha256(encoded).hexdigest() + "\n")
    rows = "\n".join(f"| {method} | {values['feasible']} | {values['infeasible']} |" for method, values in count_dict.items())
    fractional_rows = "\n".join(f"| {r['model_index']} | {r['status']} | {r['margin']:.12f} |" for r in fractional)
    verdict = "PASS" if not FAILURES else "FAIL"
    note.write_text(f"""# F15-ND01 independent joint-feasibility audit

Contributor: ChatGPT (GPT-6 Astra Pro), independent relaxation-analysis agent.
Concurrent review adds zero separate root-clock minutes. This is not F16.

**Verdict: {verdict}; {sum(COUNTS.values()):,} checks, {len(FAILURES)} failures.**

The saved output, source, mechanism result, preparation manifest, five source
networks and five soft-mask preparations have matching hashes and bindings.
The audit uses exact rational arithmetic on saved binary64 parameters and masks.
No model forwards, input populations, fits, projection searches, or numerical
optimizers were run.

## Independent prerequisites and arithmetic

The affine extrema were computed by a sign-based formula independently of the
source's corner enumeration. All 160 unit classifications agree. All
**{plane_comparisons:,} pairs of interior variable-unit kink hyperplanes** are
distinct, verified via their rational 2-by-2 minors rather than the source's
canonical normalization. Exact active-weight ranks have full column rank.
The complete activation-difference ranks are
**{[exact_geometry[i]['difference_span_rank'] for i in range(5)]}** and their
nullspace dimensions are **{[exact_geometry[i]['nullspace_dimension'] for i in range(5)]}**.
Each nullspace is exactly the coordinate subspace of the inactive units, with
dimension at least two. These establish the stated two-sphere prerequisites.

All twenty masks fall in the exact rational central branch. Independent
computation of `c.v - c.c`, observable role overlap, inactive head energy,
the branch discriminant, cancellation capacity and margin agrees exactly with
every saved rational value. Float display values and all dispositions agree.
No square-root enclosure helper was needed.

| Existing mask method | Feasible | Infeasible |
|---|---:|---:|
{rows}

For the fractional masks specifically:

| Model index | Disposition | Exact-margin decimal display |
|---|---|---:|
{fractional_rows}

## Meaning and limits

The kink argument is applicable because each variable affine hyperplane crosses
the box interior and can be locally crossed away from all other distinct
hyperplanes. A constant linear combination of activations therefore has zero
coefficient on every variable unit. Full active-weight rank leaves only inactive
coordinates in the difference nullspace.

For the compatible-projector question, the sphere-dot-product minimum yields
the saved central capacity `(delta0 + delta1 + t_squared)/2`. The admissible
dot-product range is connected in nullspace dimension at least two, and its
upper endpoint is nonnegative. Thus comparing that capacity to the nonnegative
observable overlap decides the exact existing-effect feasibility question.

These are exact statements about the real-valued ReLU function with stored
binary64 coefficients treated as rationals, over the entire declared input box,
in the **stored native Euclidean hidden metric**. Positive rescaling changes
that metric and can change feasibility while preserving ordinary network outputs
and transported coordinate interventions. The numerical dispositions should
therefore not be presented as gauge-invariant facts about semantic features.

A feasible pair establishes existence of compatible output-effect coefficients
for these particular masks. It does not establish semantic joint cost adequacy,
an identified native representation, a successful future approximate alignment,
DAS/ND02 execution, or new F15 support. The infeasible fractional model rules out
exact matching of those two particular effects in this metric/domain, not every
approximate or differently parameterized joint representation.

Machine-readable evidence: [audit_joint_feasibility.json](audit_joint_feasibility.json).
""", encoding="utf-8")
    print(json.dumps({"all_checks_passed": not FAILURES, "checks": sum(COUNTS.values()),
        "failures": FAILURES, "counts": count_dict, "fractional_rows": fractional}, indent=2))
    if FAILURES:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
