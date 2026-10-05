"""Pre-freeze generic solver checks: no F15 models or pair populations.

Contributor: ChatGPT (GPT-6 Astra Pro), F15-ND01.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
import platform
import subprocess
import sys

import numpy as np

from v2.experiments.neural_diagnostic_v1 import binary_global as B


def main():
    here = B.HERE
    build_path = here / B.BUILD_NAME
    if build_path.exists():
        raise RuntimeError("Build evidence already exists; do not overwrite it.")
    compiler = subprocess.run(["g++", "--version"], capture_output=True, text=True, check=True).stdout
    record = {
        "schema": "f15-nd01-binary-global-build-v1",
        "source_sha256": B.file_hash(here / B.SOURCE_NAME),
        "binary_sha256": B.file_hash(here / B.BINARY_NAME),
        "compiler": compiler, "compiler_executable": "/usr/bin/g++",
        "flags": B.FLAGS, "single_thread": True, "fast_math": False,
        "command_from_repository_root": ["g++", *B.FLAGS,
            "v2/experiments/neural_diagnostic_v1/binary_global.cpp", "-o",
            "v2/experiments/neural_diagnostic_v1/binary_global_solver"],
        "platform": platform.platform(), "machine": platform.machine(),
        "generic_pre_freeze_build": True, "model_data_used": False,
    }
    build_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    rng = np.random.Generator(np.random.PCG64(20261005))
    rows = []
    for width, mass in ((8, 3), (10, 4), (12, 5), (16, 6)):
        a = rng.normal(size=(40, width))
        target = rng.normal(size=40)
        gram = a.T @ a / len(a)
        gram = (gram + gram.T) * 0.5
        linear, constant = a.T @ target / len(a), float(np.mean(target ** 2))
        result = B.solve_quadratic(gram, linear, constant, mass)
        oracle_value, oracle_subset = min(
            (float(np.mean((a[:, subset].sum(axis=1) - target) ** 2)), list(subset))
            for subset in itertools.combinations(range(width), mass))
        discrepancy = abs(oracle_value - result["minimum_computed_quadratic"])
        assert result["subset"] == oracle_subset and discrepancy < 1e-12
        rows.append({"case": "small_psd_direct_residual_oracle", "width": width,
                     "mass": mass, "oracle_value": oracle_value,
                     "recomputation_discrepancy": discrepancy, "passed": True,
                     "native": result})
    zero = B.solve_quadratic(np.zeros((32, 32)), np.zeros(32), 0.0, 8)
    assert zero["subset"] == list(range(8)) and zero["minimum_computed_quadratic"] == 0.0
    rows.append({"case": "full_size_exact_ties_lexicographic_first", "passed": True, "native": zero})
    indices = np.arange(1, 33, dtype=np.float64)
    gram = np.outer(indices, indices) * 1e-6 + np.diag(1 + (indices - 1) * 0.001)
    structured = B.solve_quadratic(gram, indices * 0.03, 10.0, 8)
    assert structured["subset"] == list(range(24, 32))
    rows.append({"case": "full_size_diagonal_plus_rank_one", "passed": True, "native": structured})
    report = {"schema": "f15-nd01-binary-generic-checks-v1", "synthetic_only": True,
              "model_data_used": False, "F15_pair_populations_used": False,
              "python": sys.version, "numpy": np.__version__,
              "cases": rows, "all_passed": True}
    out = Path(__file__).with_suffix(".json")
    if out.exists():
        raise RuntimeError("Generic audit evidence already exists; do not overwrite it.")
    encoded = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8")
    out.write_bytes(encoded)
    out.with_suffix(out.suffix + ".sha256").write_text(hashlib.sha256(encoded).hexdigest() + "\n", encoding="ascii")
    print(json.dumps({"all_passed": True, "cases": len(rows), "synthetic_only": True,
        "full_size_times": [r["native"]["wall_seconds"] for r in rows[-2:]],
        "source_sha256": record["source_sha256"], "binary_sha256": record["binary_sha256"]}))


if __name__ == "__main__":
    main()
