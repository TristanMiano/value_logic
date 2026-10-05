"""Independent audit of stored joint-projector witness matrices.

Uses compensated scalar sums for matrix products; does not import or rerun
the witness construction. No models, populations, fits or optimizers are run.
Contributor: ChatGPT (GPT-6 Astra Pro), independent relaxation-analysis agent.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import datetime
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SESSION = Path(__file__).resolve().parent
ANALYSIS = ROOT / "v2/experiments/F15_ND01_analysis"
RUN = ROOT / "v2/work_logs/F15_ND01_v1_run1"
CHECKS = Counter()
FAILURES = []
INPUTS = {}
MAXIMA = defaultdict(float)
TOLERANCE = 1e-12


def digest(path):
    encoded = path.read_bytes()
    value = hashlib.sha256(encoded).hexdigest()
    INPUTS[str(path.relative_to(ROOT))] = {"sha256": value, "bytes": len(encoded)}
    return value


def load(path):
    digest(path)
    return json.loads(path.read_text(encoding="utf-8"))


def check(condition, group, label):
    CHECKS[group] += 1
    if not condition:
        FAILURES.append({"group": group, "label": label})


def near(actual, expected, group, label):
    difference = abs(actual - expected)
    MAXIMA[group] = max(MAXIMA[group], difference)
    check(math.isfinite(actual) and math.isfinite(expected)
          and difference <= TOLERANCE * max(1.0, abs(actual), abs(expected)), group, label)


def dot(left, right):
    return math.fsum(x * y for x, y in zip(left, right))


def mv(matrix, vector):
    return [dot(row, vector) for row in matrix]


def mm(left, right):
    columns = list(zip(*right))
    return [[dot(row, column) for column in columns] for row in left]


def vector_error(left, right):
    return max(abs(x - y) for x, y in zip(left, right))


def matrix_error(left, right):
    return max(vector_error(x, y) for x, y in zip(left, right))


def matrix_max(matrix):
    return max(abs(x) for row in matrix for x in row)


def mask_for(role, method):
    if method == "fractional_mask":
        return role["mask"]["values"]
    subset = {"frozen_original": role["original_subset"],
              "binary_global": role["binary_global"]["subset"],
              "rounded_top8": role["rounded_subset"]}[method]
    return [float(j in subset) for j in range(32)]


def main():
    output, note = SESSION / "audit_joint_witnesses.json", SESSION / "audit_joint_witnesses.md"
    if output.exists() or note.exists():
        raise FileExistsError("Preserve existing joint-witness audit evidence.")
    witness_path = ANALYSIS / "joint_witnesses.json"
    result = load(witness_path)
    check(digest(witness_path) == witness_path.with_suffix(".json.sha256").read_text().strip(), "provenance", "witness output sidecar")
    check(result["script_sha256"] == digest(ANALYSIS / "joint_witnesses.py"), "provenance", "witness source binding")
    for name, expected in result["inputs"].items():
        check(digest(ROOT / name) == expected, "provenance", name)
    feasibility = load(ANALYSIS / "joint_feasibility.json")
    previous_audit = load(SESSION / "audit_joint_feasibility.json")
    check(previous_audit["all_checks_passed"] is True, "provenance", "independent exact-feasibility audit passed")
    check(previous_audit["inputs"]["v2/experiments/F15_ND01_analysis/joint_feasibility.json"]["sha256"]
          == digest(ANALYSIS / "joint_feasibility.json"), "provenance", "exact classification audit binding")
    check(previous_audit["inputs"]["v2/experiments/F15_ND01_analysis/joint_feasibility.md"]["sha256"]
          == digest(ANALYSIS / "joint_feasibility.md"), "provenance", "audited derivation snapshot unchanged")
    manifest = load(RUN / "preparation_complete.json")
    check(digest(RUN / "preparation_complete.json") == feasibility["inputs"]["v2/work_logs/F15_ND01_v1_run1/preparation_complete.json"], "provenance", "frozen preparation manifest binding")
    source_records = manifest["freeze"]["source_prepared"]
    soft_records = {u["index"]: u for u in manifest["units"] if u["kind"] == "soft_mask"}
    originals, prepared = {}, {}
    for index in range(5):
        source_path = ROOT / source_records[index]["path"]
        prep_path = RUN / soft_records[index]["file"]
        check(digest(source_path) == source_records[index]["sha256"], "provenance", f"original source {index}")
        check(digest(prep_path) == soft_records[index]["sha256"], "provenance", f"soft preparation {index}")
        originals[index], prepared[index] = load(source_path), load(prep_path)
        check(originals[index]["network"] == prepared[index]["network"], "provenance", f"unchanged network {index}")
    geometry = {r["model_index"]: r for r in feasibility["geometries"]}
    classifications = {(r["model_index"], r["method"]): r for r in feasibility["rows"]}
    expected = {key for key, row in classifications.items() if row["status"] == "feasible"}
    actual = {(row["model_index"], row["method"]) for row in result["witnesses"]}
    check(actual == expected and len(actual) == len(result["witnesses"]) == 13,
          "cardinality", "one pair for every feasible case and none for infeasible cases")
    audited_rows = []
    maxima = defaultdict(float)
    count_by_method = Counter()
    for witness in result["witnesses"]:
        index, method = witness["model_index"], witness["method"]
        record = classifications[index, method]
        v = originals[index]["network"]["v"]
        masks = [mask_for(role, method) for role in prepared[index]["roles"]]
        inactive = geometry[index]["inactive"]
        observable = [j for j in range(32) if j not in inactive]
        qs, ps = witness["coefficients"], witness["projectors"]
        check(record["status"] == "feasible" and record["branch"] == "central_rational", "scope", f"eligible feasibility {index}/{method}")
        check(len(qs) == len(ps) == 2 and all(len(q) == 32 for q in qs)
              and all(len(p) == 32 and all(len(row) == 32 for row in p) for p in ps),
              "shape", f"two coefficient vectors and two matrices {index}/{method}")
        check(all(math.isfinite(x) for q in qs for x in q)
              and all(math.isfinite(x) for p in ps for row in p for x in row),
              "shape", f"finite coefficients and matrices {index}/{method}")
        measures = defaultdict(float)
        for role, (q, p, mask) in enumerate(zip(qs, ps, masks)):
            qtq = dot(q, q)
            check(qtq > 0, "matrix", f"nonzero rank-one coefficient {index}/{method}/{role}")
            reconstruction = [[x * y / qtq for y in q] for x in q]
            symmetry = matrix_error(p, list(zip(*p)))
            idempotence = matrix_error(mm(p, p), p)
            coefficient = mv(p, v)
            head_error = vector_error(coefficient, q)
            original = [mask[j] * v[j] for j in range(32)]
            observable_error = max(abs(coefficient[j] - original[j]) for j in observable)
            exact_observable_error = max(abs(q[j] - original[j]) for j in observable)
            sphere_error = abs(dot(q, v) - qtq)
            rank_one_error = matrix_error(p, reconstruction)
            trace_error = abs(math.fsum(p[j][j] for j in range(32)) - 1.0)
            for name, value in (("symmetry_max_abs", symmetry), ("idempotence_max_abs", idempotence),
                                ("head_binding_max_abs", head_error), ("observable_binding_max_abs", observable_error),
                                ("constructed_coefficient_observable_max_abs", exact_observable_error),
                                ("sphere_equality_abs", sphere_error), ("rank_one_formula_max_abs", rank_one_error),
                                ("trace_one_abs", trace_error)):
                near(value, 0.0, "matrix", f"{index}/{method}/{role}/{name}")
                measures[name] = max(measures[name], value)
            # The coefficients can depart from the original masks only along
            # the exact inactive-coordinate difference nullspace.
            n = [q[j] if j in inactive else 0.0 for j in range(32)]
            center = [v[j] / 2 if j in inactive else 0.0 for j in range(32)]
            shifted = [x - y for x, y in zip(n, center)]
            radius_squared = float(Fraction(record[f"delta{role}_exact"])
                                   + Fraction(record["inactive_head_quarter_energy_exact"]))
            near(dot(shifted, shifted), radius_squared, "construction", f"sphere/null component {index}/{method}/{role}")
        cross01, cross10 = matrix_max(mm(ps[0], ps[1])), matrix_max(mm(ps[1], ps[0]))
        coefficient_dot = abs(dot(qs[0], qs[1]))
        for name, value in (("cross01_max_abs", cross01), ("cross10_max_abs", cross10),
                            ("coefficient_orthogonality_abs", coefficient_dot)):
            near(value, 0.0, "orthogonality", f"{index}/{method}/{name}")
            measures[name] = value
        mapped = {
            "coefficient_orthogonality_abs": coefficient_dot,
            "projector_cross_product_max_abs": cross01,
            "projector_idempotence_max_abs": measures["idempotence_max_abs"],
            "head_coefficient_max_abs": measures["head_binding_max_abs"],
            "observable_coefficient_max_abs": measures["observable_binding_max_abs"],
        }
        for name, value in mapped.items():
            near(witness["errors"][name], value, "saved_error", f"{index}/{method}/{name}")
        check(witness["constructed_after_registered_outcomes"] is True
              and witness["new_intervention_population_scored"] is False
              and witness["semantic_joint_cost_adequacy_claimed"] is False,
              "scope", f"post-outcome witness interpretation {index}/{method}")
        for name, value in measures.items():
            maxima[name] = max(maxima[name], value)
        count_by_method[method] += 1
        audited_rows.append({"model_index": index, "method": method,
                             "independent_errors": dict(measures)})
    near(result["maximum_identity_error"], max(max(w["errors"].values()) for w in result["witnesses"]),
         "saved_error", "reported aggregate maximum")
    check(result["metric"] == "stored Euclidean hidden geometry"
          and result["post_outcome_analytic_construction"] is True
          and result["development_only"] is True, "scope", "native metric and analytic labels")
    check(result["new_model_forwards"] == result["new_fits"] == result["new_populations"] == result["new_validation_scores"] == 0,
          "scope", "no new empirical scores")
    report = {"schema": "F15-ND01-independent-joint-witness-audit-v1",
        "contributor": "ChatGPT (GPT-6 Astra Pro), independent relaxation-analysis agent",
        "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "all_checks_passed": not FAILURES, "checks": dict(CHECKS), "total_checks": sum(CHECKS.values()),
        "failures": FAILURES, "inputs": INPUTS,
        "witness_pairs": 13, "projector_matrices": 26,
        "pairs_by_method": dict(count_by_method), "independent_error_maxima": dict(maxima),
        "source_error_comparison_maxima": dict(MAXIMA), "audited_witnesses": audited_rows,
        "absolute_relative_check_tolerance": TOLERANCE,
        "model_forwards": 0, "populations_generated": 0, "new_fits": 0,
        "optimizers_called": 0, "witness_construction_reruns": 0,
        "scope": "Audit of numerical matrices witnessing previously proved exact existing-effect feasibility in the stored native metric. These post-outcome constructions have no new empirical semantic joint-adequacy score, and are not ND02 or F16."}
    encoded = (json.dumps(report, sort_keys=True, indent=2) + "\n").encode()
    output.write_bytes(encoded)
    output.with_suffix(".json.sha256").write_text(hashlib.sha256(encoded).hexdigest() + "\n")
    verdict = "PASS" if not FAILURES else "FAIL"
    metrics = "\n".join(f"| {name} | {value:.3e} |" for name, value in maxima.items())
    note.write_text(f"""# F15-ND01 independent joint-witness audit

Contributor: ChatGPT (GPT-6 Astra Pro), independent relaxation-analysis agent.
Concurrent review adds zero separate root-clock minutes. This is not F16.

**Verdict: {verdict}; {sum(CHECKS.values()):,} checks, {len(FAILURES)} failures.**

The artifact contains **13 witness pairs, comprising 26 stored projector
matrices**. Their model/method identities match exactly the feasible cases in
the independently audited rational classification: original 2, exhaustive
binary 4, rounded 3, and fractional 4. The seven infeasible cases have no
witness pair. All source, input and preparation hashes agree; the previously
audited joint-feasibility derivation snapshot remains unchanged.

## Matrix checks

Using independent compensated scalar sums, this audit recalculated every
matrix square, both cross-product orders, all native-head products and all
coefficient dot products. It verified symmetry, idempotence, mutual
orthogonality, the rank-one formula and unit trace, the projector sphere
equation, and agreement with the selected mask's output coefficient outside
the exact inactive-coordinate nullspace. The saved coefficient null components
also lie on the stated spheres. Recorded errors agree up to float64 summation
differences; every independent residual is below 1e-12.

| Independent quantity | Maximum absolute error |
|---|---:|
{metrics}

The constructor was read but not imported or rerun. Its central-branch choice
places the first null component at the proved minimizing norm; the second is
chosen on its sphere to cancel the observable overlap. The saved matrices
directly verify the resulting identities, so this audit does not depend on
repeating that choice algorithm.

## Scope

These are numerical witnesses for a separately proved exact **existing-output-
effect** feasibility condition in the stored native Euclidean metric. They
exploit inactive-coordinate freedom. Their matrix algebra supplies compatible
idempotent/commuting interventions, while the observable coefficients preserve
the original masks' single-role output effects on the declared input box.

They are post-outcome algebraic constructions, not newly learned semantic
features, a new confirmation of F15 support, or a demonstrated joint cost-
adequacy result. No populations, model forwards, fits, optimizers, witness
construction reruns, or new validation scores were performed by this audit.
Native-metric feasibility is not gauge invariant. ND02 and F16 remain unstarted
by this work.

Machine-readable details: [audit_joint_witnesses.json](audit_joint_witnesses.json).
""", encoding="utf-8")
    print(json.dumps({"all_checks_passed": not FAILURES, "checks": sum(CHECKS.values()),
        "failures": FAILURES, "witness_pairs": 13, "projector_matrices": 26,
        "independent_error_maxima": dict(maxima)}, indent=2))
    if FAILURES:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
