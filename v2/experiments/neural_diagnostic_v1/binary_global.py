"""Auditable wrapper for exhaustive binary-mask discovery optimization.

All size-eight masks are visited.  The optimum is the minimum of the C++
enumerator's fixed-order float64 quadratic calculation, with exact equalities
resolved lexicographically.  It is not a certified exact-real optimum.  The
chosen subset is recomputed directly from the original discovery residuals.

Contributor: ChatGPT (GPT-6 Astra Pro), F15-ND01.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import resource
import subprocess
import time
from typing import Any

import numpy as np

from .. import neural as N


HERE = Path(__file__).resolve().parent
SOURCE_NAME = "binary_global.cpp"
BINARY_NAME = "binary_global_solver"
BUILD_NAME = "binary_global_build.json"
FLAGS = ["-O3", "-std=c++17", "-ffp-contract=off", "-fno-fast-math"]
TIE_POLICY = "strict_float64_minimum_exact_equal_lexicographic_first"


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_build():
    record = json.loads((HERE / BUILD_NAME).read_text(encoding="utf-8"))
    if (record.get("source_sha256") != file_hash(HERE / SOURCE_NAME)
            or record.get("binary_sha256") != file_hash(HERE / BINARY_NAME)
            or record.get("flags") != FLAGS
            or record.get("single_thread") is not True
            or record.get("fast_math") is not False):
        raise ValueError("Binary-global solver source, binary or build record mismatch.")
    return {"source_sha256": record["source_sha256"],
            "binary_sha256": record["binary_sha256"],
            "build_record_sha256": file_hash(HERE / BUILD_NAME),
            "compiler": record["compiler"], "flags": FLAGS.copy()}


def _payload(gram: np.ndarray, linear: np.ndarray, constant: float, mass: int):
    width = len(linear)
    lines = [f"{width} {mass} {constant:.17g}",
             " ".join(f"{float(x):.17g}" for x in linear)]
    lines.extend(" ".join(f"{float(x):.17g}" for x in row) for row in gram)
    return "\n".join(lines) + "\n"


def solve_quadratic(gram: np.ndarray, linear: np.ndarray, constant: float,
                    mass: int, validate_native: bool = True):
    """Run the generic enumerator; synthetic pre-freeze checks can use n<32."""
    gram, linear = np.asarray(gram, dtype=np.float64), np.asarray(linear, dtype=np.float64)
    width = len(linear)
    if (not 0 < width <= 32 or not 0 < mass <= min(width, 8)
            or gram.shape != (width, width) or not np.isfinite(gram).all()
            or not np.isfinite(linear).all() or not math.isfinite(constant)
            or not np.array_equal(gram, gram.T)):
        raise ValueError("Native quadratic requires finite symmetric coefficients and supported dimensions.")
    build = validate_build() if validate_native else None
    payload = _payload(gram, linear, constant, mass)
    child_before = resource.getrusage(resource.RUSAGE_CHILDREN)
    wall = time.perf_counter()
    process = subprocess.run([str(HERE / BINARY_NAME)], input=payload, text=True,
                             encoding="ascii", capture_output=True, check=False)
    elapsed = time.perf_counter() - wall
    child_after = resource.getrusage(resource.RUSAGE_CHILDREN)
    if process.returncode != 0 or process.stderr:
        raise RuntimeError(f"Binary-global enumerator failed: exit={process.returncode}, stderr={process.stderr!r}")
    result = json.loads(process.stdout)
    expected_count = math.comb(width, mass)
    expected_nodes = sum(math.comb(width - mass + depth, depth) for depth in range(mass + 1))
    subset = result.get("subset", [])
    if (result.get("schema") != "f15-nd01-binary-global-native-v1"
            or result.get("width") != width or result.get("mass") != mass
            or result.get("enumerated_subsets") != expected_count
            or result.get("recursion_nodes") != expected_nodes
            or len(subset) != mass or sorted(set(subset)) != subset
            or any(type(i) is not int or not 0 <= i < width for i in subset)
            or not math.isfinite(result.get("minimum_computed_quadratic", float("nan")))):
        raise ValueError("Binary-global enumeration result/count/subset validation failed.")
    result.update({
        "tie_policy": TIE_POLICY, "unpruned_full_enumeration": True,
        "certified_exact_real_optimum": False,
        "input_sha256": hashlib.sha256(payload.encode("ascii")).hexdigest(),
        "stdout_sha256": hashlib.sha256(process.stdout.encode("ascii")).hexdigest(),
        "native_build": build,
        "resource": {"subprocess_wall_seconds": elapsed,
            "child_user_cpu_seconds": child_after.ru_utime - child_before.ru_utime,
            "child_system_cpu_seconds": child_after.ru_stime - child_before.ru_stime,
            "exit_code": process.returncode, "stderr": process.stderr,
            "single_thread": True},
    })
    return result


def solve_discovery(a: np.ndarray, target: np.ndarray, settings: dict[str, Any]):
    """Exhaust the same finite-discovery logit quadratic as the fractional fit."""
    a, target = np.asarray(a, dtype=np.float64), np.asarray(target, dtype=np.float64)
    if (a.ndim != 2 or a.shape[1] != settings["binary_global_width"]
            or target.shape != (len(a),) or not len(a)
            or not np.isfinite(a).all() or not np.isfinite(target).all()):
        raise ValueError("Binary-global discovery arrays have invalid shape or values.")
    gram = a.T @ a / len(a)
    gram = (gram + gram.T) * 0.5
    linear, constant = a.T @ target / len(a), float(np.mean(target ** 2))
    result = solve_quadratic(gram, linear, constant, settings["binary_global_mass"])
    if (result["enumerated_subsets"] != settings["binary_global_expected_subsets"]
            or result["tie_policy"] != settings["binary_global_tie_policy"]):
        raise ValueError("Exhaustive binary settings differ from their prospective registration.")
    mask = np.zeros(a.shape[1], dtype=np.float64)
    mask[result["subset"]] = 1.0
    direct = float(np.mean((a @ mask - target) ** 2))
    quadratic = float(mask @ gram @ mask - 2 * linear @ mask + constant)
    native = result["minimum_computed_quadratic"]
    discrepancy = max(abs(direct - native), abs(quadratic - native), abs(direct - quadratic))
    allowed = settings["binary_global_recomputation_tolerance"] * max(1.0, abs(direct), abs(quadratic), abs(native))
    if discrepancy > allowed:
        raise ArithmeticError("Binary-global chosen objective disagrees with direct residual recomputation.")
    result.update({
        "scope": "finite_discovery_logit_mse_same_as_fractional_mask",
        "discovery_matrix_hash": N.array_hash(a, target),
        "quadratic_coefficients_hash": N.array_hash(gram, linear, np.asarray([constant])),
        "direct_discovery_logit_mse": direct,
        "numpy_quadratic_recomputed": quadratic,
        "maximum_objective_recomputation_discrepancy": discrepancy,
        "objective_recomputation_allowed_discrepancy": allowed,
        "probability_mse_global_optimum_claimed": False,
        "validation_population_optimum_claimed": False,
    })
    return result


def validate_result(result: dict[str, Any], settings: dict[str, Any]):
    """Check saved structure/build/counts without refitting or new inputs."""
    build = validate_build()
    subset = result.get("subset", [])
    n, k = settings["binary_global_width"], settings["binary_global_mass"]
    if (result.get("native_build") != build
            or result.get("width") != n or result.get("mass") != k
            or result.get("enumerated_subsets") != math.comb(n, k)
            or result.get("recursion_nodes") != sum(math.comb(n - k + d, d) for d in range(k + 1))
            or result.get("tie_policy") != TIE_POLICY
            or result.get("unpruned_full_enumeration") is not True
            or result.get("certified_exact_real_optimum") is not False
            or len(subset) != k or sorted(set(subset)) != subset
            or any(type(j) is not int or not 0 <= j < n for j in subset)
            or result.get("maximum_objective_recomputation_discrepancy", float("inf"))
                > result.get("objective_recomputation_allowed_discrepancy", -1)
            or result.get("resource", {}).get("exit_code") != 0
            or result.get("resource", {}).get("stderr") != ""):
        raise ValueError("Saved exhaustive binary result, source or count is inconsistent.")
    return True
