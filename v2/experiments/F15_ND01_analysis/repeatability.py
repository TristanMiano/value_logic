"""Post-outcome ND01 algebra diagnostic from already saved discovery moments.

No network execution, new pairs, fitting, selection or validation. It measures
the logit drift caused by applying an existing fractional edit twice.
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


def load_verified(path):
    expected = Path(str(path) + ".sha256").read_text().strip().split()[0]
    assert digest(path) == expected, str(path)
    return json.loads(path.read_text())


def array_hash(*arrays):
    h = hashlib.sha256()
    for value in arrays:
        a = np.ascontiguousarray(value, dtype=np.float64)
        h.update(json.dumps(list(a.shape), separators=(",", ":")).encode("ascii"))
        h.update(a.tobytes())
    return h.hexdigest()


def analyze():
    mechanism_path = HERE / "mechanism_results.json"
    mechanism = load_verified(mechanism_path)
    manifest_path = RUN / "preparation_complete.json"
    assert digest(manifest_path) == mechanism["preparation_manifest_sha256"]
    manifest = load_verified(manifest_path)
    quadratics = {(r["model_index"], r["role"]): r for r in mechanism["discovery_quadratics"]}
    inputs = {str(mechanism_path.relative_to(ROOT)): digest(mechanism_path),
              str(manifest_path.relative_to(ROOT)): digest(manifest_path)}
    rows = []
    for unit in manifest["units"]:
        if unit["kind"] != "soft_mask":
            continue
        path = RUN / unit["file"]
        preparation = load_verified(path)
        inputs[str(path.relative_to(ROOT))] = digest(path)
        for role in (0, 1):
            fitted = preparation["roles"][role]
            q = quadratics[(unit["index"], role)]
            gram = np.asarray(q["gram"], dtype=np.float64)
            linear = np.asarray(q["linear"], dtype=np.float64)
            constant = np.asarray([q["constant"]], dtype=np.float64)
            assert array_hash(gram, linear, constant) == q["quadratic_hash"]
            assert q["quadratic_hash"] == fitted["binary_global"]["quadratic_coefficients_hash"]
            mask = np.asarray(fitted["mask"]["values"], dtype=np.float64)
            drift = mask * (1 - mask)
            mse = float(drift @ gram @ drift)
            assert mse >= -1e-12
            original = np.zeros(32)
            original[fitted["original_subset"]] = 1
            binary = np.zeros(32)
            binary[fitted["binary_global"]["subset"]] = 1
            assert np.count_nonzero(original * (1 - original)) == 0
            assert np.count_nonzero(binary * (1 - binary)) == 0
            rows.append({"model_index": unit["index"], "role": role,
                         "discovery_pair_count": 640,
                         "fractional_repeated_application_logit_mse": max(0., mse),
                         "fractional_repeated_application_logit_rms": float(np.sqrt(max(0., mse))),
                         "fractional_replacement_drift_weights": drift.tolist(),
                         "original_binary_structurally_idempotent": True,
                         "global_binary_structurally_idempotent": True,
                         "new_validation_or_support_test": False})
    assert len(rows) == 10
    return {"schema": "F15-ND01-repeatability-from-saved-moments-v1",
            "contributor": "ChatGPT (GPT-6 Astra Pro)",
            "development_only": True, "post_outcome_supplementary": True,
            "diagnostic": "second application minus first application, using the same donor and base",
            "formula": "b=m*(1-m); E[(delta_logit)^2]=b.T @ (A.T @ A/n) @ b",
            "new_pairs": 0, "new_fits": 0, "new_model_executions": 0,
            "rows": rows,
            "mean_role_logit_rms": float(np.mean([r["fractional_repeated_application_logit_rms"] for r in rows])),
            "logit_rms_range": [min(r["fractional_repeated_application_logit_rms"] for r in rows),
                                max(r["fractional_repeated_application_logit_rms"] for r in rows)],
            "inputs": inputs, "script_sha256": digest(Path(__file__)),
            "scope": "saved finite discovery moments; not a validation population, probability MAE, or amended endpoint"}


def main():
    target = HERE / "repeatability.json"
    value = analyze()
    encoded = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
    if sys.argv[1:] == ["--check"]:
        assert target.read_bytes() == encoded
        assert Path(str(target) + ".sha256").read_text().strip() == digest(target)
        print("Repeatability report reproduced byte for byte.")
        return
    assert not sys.argv[1:]
    with target.open("xb") as handle:
        handle.write(encoded)
    with Path(str(target) + ".sha256").open("x") as handle:
        handle.write(digest(target) + "\n")
    print(json.dumps({"output": str(target), "sha256": digest(target),
                      "rows": len(value["rows"]), "logit_rms_range": value["logit_rms_range"]}))


if __name__ == "__main__":
    main()
