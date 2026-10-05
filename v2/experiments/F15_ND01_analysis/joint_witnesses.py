"""Deterministic post-outcome witnesses for the proved feasibility condition.

No fit, optimizer, model forward, population or new validation method score.
Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-05.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RUN = ROOT / "v2/work_logs/F15_ND01_v1_run1"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verified(path):
    assert digest(path) == Path(str(path) + ".sha256").read_text().split()[0]
    return json.loads(path.read_text())


def make_mask(role, method):
    if method == "fractional_mask":
        return np.asarray(role["mask"]["values"], dtype=np.float64)
    subset = role[{"frozen_original": "original_subset", "rounded_top8": "rounded_subset"}[method]] if method != "binary_global" else role["binary_global"]["subset"]
    result = np.zeros(32)
    result[subset] = 1
    return result


def construct(v, masks, inactive, record):
    assert record["status"] == "feasible" and record["branch"] == "central_rational"
    w = np.zeros(32)
    w[inactive] = v[inactive] / 2
    t = np.linalg.norm(w)
    assert t > 0  # Verified for every current source; no generic zero-t claim.
    axis = w / t
    orth = None
    for j in inactive:
        candidate = np.zeros(32)
        candidate[j] = 1
        candidate -= axis[j] * axis
        if np.linalg.norm(candidate) > 1e-10:
            orth = candidate / np.linalg.norm(candidate)
            break
    assert orth is not None
    r0 = np.sqrt(record["delta0"] + t * t)
    r1 = np.sqrt(record["delta1"] + t * t)
    x = r1
    along = (x * x + t * t - r0 * r0) / (2 * t)
    across_squared = x * x - along * along
    assert across_squared >= -1e-13
    across = np.sqrt(max(0., across_squared))
    n0 = along * axis + across * orth
    # This is the central-branch minimizing n0. With C>=0, the desired dot
    # product lies between its minimum and maximum against the second sphere.
    cosine = (-record["observable_overlap"] - n0 @ w) / (r1 * x)
    assert -1 - 1e-12 <= cosine <= 1 + 1e-12
    cosine = np.clip(cosine, -1., 1.)
    tangent = (-across * axis + along * orth) / x
    n1 = w + r1 * (cosine * n0 / x + np.sqrt(max(0., 1 - cosine * cosine)) * tangent)
    coefficients = []
    for m, n in zip(masks, (n0, n1)):
        c = m * v
        c[inactive] = 0
        coefficients.append(c + n)
    projectors = [np.outer(q, q) / (q @ q) for q in coefficients]
    active = [j for j in range(32) if j not in inactive]
    errors = {
        "coefficient_orthogonality_abs": float(abs(coefficients[0] @ coefficients[1])),
        "projector_cross_product_max_abs": float(np.max(abs(projectors[0] @ projectors[1]))),
        "projector_idempotence_max_abs": max(float(np.max(abs(p @ p - p))) for p in projectors),
        "head_coefficient_max_abs": max(float(np.max(abs(p @ v - q))) for p, q in zip(projectors, coefficients)),
        "observable_coefficient_max_abs": max(float(np.max(abs((p @ v - m * v)[active]))) for p, m in zip(projectors, masks)),
    }
    assert max(errors.values()) <= 1e-11
    return {"model_index": record["model_index"], "method": record["method"],
            "coefficients": [q.tolist() for q in coefficients],
            "projectors": [p.tolist() for p in projectors], "errors": errors,
            "constructed_after_registered_outcomes": True,
            "new_intervention_population_scored": False,
            "semantic_joint_cost_adequacy_claimed": False}


def analyze():
    path = HERE / "joint_feasibility.json"
    result = verified(path)
    manifest = verified(RUN / "preparation_complete.json")
    inputs = {str(path.relative_to(ROOT)): digest(path)}
    witnesses = []
    by_model = {g["model_index"]: g for g in result["geometries"]}
    soft = {u["index"]: u for u in manifest["units"] if u["kind"] == "soft_mask"}
    for i, source in enumerate(manifest["freeze"]["source_prepared"]):
        source_path = ROOT / source["path"]
        assert digest(source_path) == source["sha256"]
        inputs[str(source_path.relative_to(ROOT))] = digest(source_path)
        v = np.asarray(json.loads(source_path.read_text())["network"]["v"])
        prep_path = RUN / soft[i]["file"]
        preparation = verified(prep_path)
        inputs[str(prep_path.relative_to(ROOT))] = digest(prep_path)
        for row in result["rows"]:
            if row["model_index"] == i and row["status"] == "feasible":
                masks = [make_mask(r, row["method"]) for r in preparation["roles"]]
                witnesses.append(construct(v, masks, by_model[i]["inactive"], row))
    assert len(witnesses) == sum(r["status"] == "feasible" for r in result["rows"])
    return {"schema": "F15-ND01-joint-feasibility-witnesses-v1",
            "contributor": "ChatGPT (GPT-6 Astra Pro)", "development_only": True,
            "post_outcome_analytic_construction": True, "metric": "stored Euclidean hidden geometry",
            "new_model_forwards": 0, "new_fits": 0, "new_populations": 0,
            "new_validation_scores": 0, "witnesses": witnesses,
            "maximum_identity_error": max(max(w["errors"].values()) for w in witnesses),
            "inputs": inputs, "script_sha256": digest(Path(__file__)), "numpy": np.__version__}


def main():
    target = HERE / "joint_witnesses.json"
    value = analyze()
    encoded = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
    if sys.argv[1:] == ["--check"]:
        assert target.read_bytes() == encoded
        assert Path(str(target) + ".sha256").read_text().strip() == digest(target)
        print("Joint witnesses reproduced byte for byte.")
        return
    assert not sys.argv[1:]
    with target.open("xb") as handle:
        handle.write(encoded)
    with Path(str(target) + ".sha256").open("x") as handle:
        handle.write(digest(target) + "\n")
    print(json.dumps({"output": str(target), "sha256": digest(target),
                      "witnesses": len(value["witnesses"]),
                      "maximum_identity_error": value["maximum_identity_error"]}))


if __name__ == "__main__":
    main()
