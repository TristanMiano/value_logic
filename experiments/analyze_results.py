"""Frozen-protocol analysis for the completed value-logic v1.1 experiment.

The raw result remains immutable and unadjudicated.  This module reads it,
applies the Task 19 world-first/seed-paired inference rules, writes a compact
machine-readable analysis, and renders the registered result figures.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from math import sqrt
import os
from pathlib import Path
from typing import Any, Mapping, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from experiments.protocol import FIT_SEEDS, succession_fixture


ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "experiments" / "raw_results_v1_1.json"
PROTOCOL_PATH = ROOT / "experiments" / "protocol_v1.json"
CALIBRATION_PATH = ROOT / "experiments" / "calibration_checkpoint_v1_1.json"
SELECTION_PATH = ROOT / "experiments" / "selection_checkpoint_v1_1.json"
FIT_PATH = ROOT / "experiments" / "fit_checkpoint_v1_1.json"
ANALYSIS_PATH = ROOT / "experiments" / "analysis_v1_1.json"
FIGURE_DIRECTORY = ROOT / "experiments" / "figures"

WORLD_COUNT = 5_000
BOOTSTRAP_REPLICATES = 10_000
BOOTSTRAP_SEED = 19_012_026
ALPHA = 0.05


def _sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _read_json(path: Path) -> Mapping[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _atomic_json(path: Path, value: Mapping[str, Any]) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def metric_cubes(raw: Mapping[str, Any]) -> Mapping[str, np.ndarray]:
    """Turn 40,000 JSON rows into one world-by-seed array per metric."""

    rows = raw["world_seed_metrics"]
    if len(rows) != WORLD_COUNT * len(FIT_SEEDS):
        raise ValueError("raw metric row count does not match 5,000 worlds x 8 seeds")
    names = sorted(set(rows[0]) - {"fit_seed", "world_index"})
    cubes = {
        name: np.full((WORLD_COUNT, len(FIT_SEEDS)), np.nan, dtype=np.float64)
        for name in names
    }
    seed_index = {seed: index for index, seed in enumerate(FIT_SEEDS)}
    seen: set[tuple[int, int]] = set()
    for row in rows:
        world = int(row["world_index"])
        seed = int(row["fit_seed"])
        key = (world, seed)
        if key in seen or not 0 <= world < WORLD_COUNT or seed not in seed_index:
            raise ValueError("raw metrics contain a duplicate or invalid world/seed key")
        seen.add(key)
        column = seed_index[seed]
        for name in names:
            cubes[name][world, column] = float(row[name])
    if any(not np.isfinite(cube).all() for cube in cubes.values()):
        raise ValueError("raw metric cube is incomplete or nonfinite")
    return cubes


def bootstrap_means(
    values: np.ndarray,
    *,
    replicates: int = BOOTSTRAP_REPLICATES,
    seed: int = BOOTSTRAP_SEED,
    chunk: int = 100,
) -> np.ndarray:
    """Resample independent world roots; columns share every resample."""

    matrix = np.asarray(values, dtype=np.float64)
    if matrix.ndim == 1:
        matrix = matrix[:, None]
    if matrix.ndim != 2 or len(matrix) < 2 or not np.isfinite(matrix).all():
        raise ValueError("bootstrap input must be a finite world-by-endpoint matrix")
    rng = np.random.default_rng(seed)
    result = np.empty((replicates, matrix.shape[1]), dtype=np.float64)
    for start in range(0, replicates, chunk):
        stop = min(replicates, start + chunk)
        indices = rng.integers(0, len(matrix), size=(stop - start, len(matrix)))
        result[start:stop] = matrix[indices].mean(axis=1)
    return result


def centered_one_sided_p(
    bootstrap: np.ndarray,
    estimate: float,
    null_margin: float,
) -> float:
    """Task 19 one-sided p-value after shifting bootstrap draws to the null."""

    shifted = null_margin + np.asarray(bootstrap, dtype=np.float64) - estimate
    exceedances = int(np.count_nonzero(shifted >= estimate))
    return (exceedances + 1.0) / (len(shifted) + 1.0)


def holm_adjust(p_values: Mapping[str, float], alpha: float = ALPHA) -> Mapping[str, Any]:
    """Return Holm adjusted p-values and each endpoint's step-down alpha."""

    ordered = sorted(p_values, key=lambda name: (p_values[name], name))
    count = len(ordered)
    running = 0.0
    result: dict[str, Any] = {}
    for rank, name in enumerate(ordered):
        multiplier = count - rank
        running = max(running, multiplier * float(p_values[name]))
        result[name] = {
            "rank": rank + 1,
            "raw_p": float(p_values[name]),
            "adjusted_p": min(1.0, running),
            "local_alpha": alpha / multiplier,
            "reject": min(1.0, running) <= alpha,
        }
    return result


def _percentile_interval(values: np.ndarray, low: float = 0.025, high: float = 0.975) -> list[float]:
    return [float(np.quantile(values, low)), float(np.quantile(values, high))]


def _normal_summary(values: np.ndarray) -> Mapping[str, Any]:
    finite = np.asarray(values, dtype=np.float64)
    finite = finite[np.isfinite(finite)]
    if len(finite) < 2:
        return {"worlds": int(len(finite)), "mean": None, "ci95": None}
    mean = float(finite.mean())
    half = 1.959963984540054 * float(finite.std(ddof=1)) / sqrt(len(finite))
    return {
        "worlds": int(len(finite)),
        "mean": mean,
        "ci95": [mean - half, mean + half],
        "world_sd": float(finite.std(ddof=1)),
    }


def _finite_row_means(values: np.ndarray) -> np.ndarray:
    """Average each world across seeds while preserving wholly missing rows."""

    matrix = np.asarray(values, dtype=np.float64)
    finite_count = np.sum(np.isfinite(matrix), axis=1)
    return np.divide(
        np.nansum(matrix, axis=1),
        finite_count,
        out=np.full(matrix.shape[0], np.nan, dtype=np.float64),
        where=finite_count > 0,
    )


def two_way_bootstrap(
    values: np.ndarray,
    *,
    replicates: int = BOOTSTRAP_REPLICATES,
    seed: int = BOOTSTRAP_SEED,
    chunk: int = 25,
) -> np.ndarray:
    """Descriptive world-by-fit-seed bootstrap for optimization variability."""

    matrix = np.asarray(values, dtype=np.float64)
    if matrix.shape != (WORLD_COUNT, len(FIT_SEEDS)):
        raise ValueError("two-way bootstrap requires the frozen world-by-seed shape")
    rng = np.random.default_rng(seed)
    result = np.empty(replicates, dtype=np.float64)
    for start in range(0, replicates, chunk):
        stop = min(replicates, start + chunk)
        world_indices = rng.integers(0, WORLD_COUNT, size=(stop - start, WORLD_COUNT))
        seed_indices = rng.integers(0, len(FIT_SEEDS), size=(stop - start, len(FIT_SEEDS)))
        sampled = matrix[world_indices[:, :, None], seed_indices[:, None, :]]
        result[start:stop] = sampled.mean(axis=(1, 2))
    return result


def _weighted_ratio(
    numerator: np.ndarray,
    denominator: np.ndarray,
    weights: np.ndarray,
) -> np.ndarray:
    top = np.sum(weights * numerator, axis=1)
    bottom = np.sum(weights * denominator, axis=1)
    return np.divide(top, bottom, out=np.full(len(top), np.nan), where=bottom > 0.0)


def _weighted_accuracy(
    reference: np.ndarray,
    prediction: np.ndarray,
    weights: np.ndarray,
    selected: np.ndarray | None = None,
) -> np.ndarray:
    mask = np.ones_like(reference, dtype=bool) if selected is None else selected
    return _weighted_ratio((reference == prediction) & mask, mask, weights)


def _macro_accuracy(
    reference: np.ndarray,
    prediction: np.ndarray,
    groups: np.ndarray,
) -> np.ndarray:
    scores = np.zeros(reference.shape[0], dtype=np.float64)
    counts = np.zeros(reference.shape[0], dtype=np.int16)
    for group in range(int(groups.max()) + 1):
        selected = groups == group
        present = selected.any(axis=1)
        correct = np.sum(selected & (reference == prediction), axis=1)
        total = np.sum(selected, axis=1)
        scores[present] += correct[present] / total[present]
        counts[present] += 1
    return scores / counts


def _ece(logits: np.ndarray, reference: np.ndarray, weights: np.ndarray) -> np.ndarray:
    shifted = logits.astype(np.float64) - logits.max(axis=2, keepdims=True)
    probabilities = np.exp(shifted)
    probabilities /= probabilities.sum(axis=2, keepdims=True)
    confidence = probabilities.max(axis=2)
    prediction = probabilities.argmax(axis=2)
    correct = prediction == reference
    total_weight = weights.sum(axis=1)
    result = np.zeros(logits.shape[0], dtype=np.float64)
    edges = np.linspace(0.0, 1.0, 11)
    for index in range(10):
        selected = (confidence >= edges[index]) & (
            confidence <= edges[index + 1] if index == 9 else confidence < edges[index + 1]
        )
        bin_weight = np.sum(weights * selected, axis=1)
        accuracy = np.divide(
            np.sum(weights * selected * correct, axis=1),
            bin_weight,
            out=np.zeros_like(bin_weight),
            where=bin_weight > 0.0,
        )
        mean_confidence = np.divide(
            np.sum(weights * selected * confidence, axis=1),
            bin_weight,
            out=np.zeros_like(bin_weight),
            where=bin_weight > 0.0,
        )
        result += np.divide(bin_weight, total_weight) * np.abs(accuracy - mean_confidence)
    return result


def trace_secondaries(
    raw: Mapping[str, Any],
    calibration: Mapping[str, Any],
) -> tuple[Mapping[str, np.ndarray], Mapping[str, Any]]:
    """Recover registered descriptive endpoints from replayable NPZ traces."""

    arrays: dict[str, np.ndarray] = {}

    def put(name: str, start: int, stop: int, seed_column: int, values: np.ndarray) -> None:
        if name not in arrays:
            arrays[name] = np.full((WORLD_COUNT, len(FIT_SEEDS)), np.nan, dtype=np.float64)
        arrays[name][start:stop, seed_column] = values

    records = {
        (int(record["world_start"]), int(record["fit_seed"])): record
        for record in raw["trace_shards"]
    }
    if len(records) != 50 * len(FIT_SEEDS):
        raise ValueError("trace manifest is not the frozen 50 blocks x 8 seeds")

    state_labels = {0: "refuted", 1: "open", 2: "supported"}
    outcome_labels = {0: "undefined", 1: "refused", 2: "withheld", 3: "granted"}
    arm_fields = {
        "structured": "probe_structured_K3",
        "ce": "probe_ce_K3",
        "center_only": "probe_center_only_K3",
        "unaccepted_shadow": "probe_unaccepted_shadow_K3",
        "unaccepted_production": "probe_unaccepted_production_K3",
        "self_confidence_invalid": "probe_self_confidence_K3",
    }
    for start in range(0, WORLD_COUNT, 100):
        stop = start + 100
        for seed_column, seed in enumerate(FIT_SEEDS):
            record = records[(start, seed)]
            path = ROOT / record["path"]
            if _sha256(path) != record["sha256"]:
                raise RuntimeError("trace shard hash mismatch during analysis")
            with np.load(path, allow_pickle=False) as trace:
                reference = trace["probe_reference"].reshape(100, 80)
                weights = np.ones((100, 80), dtype=np.float64)
                probe_schema = np.broadcast_to(
                    np.repeat(np.asarray((0, 1), dtype=np.int8), 40)[None, :],
                    (100, 80),
                )
                for arm, field in arm_fields.items():
                    prediction = trace[field].reshape(100, 80)
                    put(
                        f"probe.{arm}.unweighted_false_support",
                        start,
                        stop,
                        seed_column,
                        _weighted_ratio(
                            (prediction == 2) & (reference != 2),
                            prediction == 2,
                            weights,
                        ),
                    )
                    put(
                        f"probe.{arm}.unweighted_false_refutation",
                        start,
                        stop,
                        seed_column,
                        _weighted_ratio(
                            (prediction == 0) & (reference != 0),
                            prediction == 0,
                            weights,
                        ),
                    )
                    put(
                        f"probe.{arm}.unweighted_support_miss",
                        start,
                        stop,
                        seed_column,
                        _weighted_ratio(
                            (reference == 2) & (prediction != 2),
                            reference == 2,
                            weights,
                        ),
                    )
                    put(
                        f"probe.{arm}.unweighted_refutation_miss",
                        start,
                        stop,
                        seed_column,
                        _weighted_ratio(
                            (reference == 0) & (prediction != 0),
                            reference == 0,
                            weights,
                        ),
                    )
                    if arm in {"structured", "ce"}:
                        for schema, schema_name in ((0, "J"), (1, "T")):
                            for state, state_name in state_labels.items():
                                selected = (probe_schema == schema) & (reference == state)
                                put(
                                    f"probe.{arm}.unweighted_accuracy.schema_{schema_name}.state_{state_name}",
                                    start,
                                    stop,
                                    seed_column,
                                    _weighted_accuracy(reference, prediction, weights, selected),
                                )

                # Mandatory unweighted design companions for the three primary panels.
                for panel_name, rows, ref_field, structured_field, ce_field in (
                    ("in", 80, "probe_reference", "probe_structured_K3", "probe_ce_K3"),
                    ("boundary", 320, "boundary_reference", "boundary_structured_K3", "boundary_ce_K3"),
                    ("transfer", 320, "transfer_reference", "transfer_structured_K3", "transfer_ce_K3"),
                ):
                    local_reference = trace[ref_field].reshape(100, rows)
                    structured_prediction = trace[structured_field].reshape(100, rows)
                    ce_prediction = trace[ce_field].reshape(100, rows)
                    if panel_name == "in":
                        groups = probe_schema * 3 + local_reference
                    else:
                        schema = np.repeat(probe_schema, 4, axis=1)
                        offset = np.broadcast_to(np.tile(np.arange(4), 80)[None, :], (100, 320))
                        groups = (
                            schema * 4 + offset
                            if panel_name == "boundary"
                            else (schema * 3 + local_reference) * 4 + offset
                        )
                    structured_score = _macro_accuracy(local_reference, structured_prediction, groups)
                    ce_score = _macro_accuracy(local_reference, ce_prediction, groups)
                    put(f"unweighted.{panel_name}.structured", start, stop, seed_column, structured_score)
                    put(f"unweighted.{panel_name}.ce", start, stop, seed_column, ce_score)
                    put(f"unweighted.{panel_name}.delta", start, stop, seed_column, structured_score - ce_score)

                logits = trace["probe_ce_raw"].reshape(100, 80, 3).astype(np.float64)
                shifted = logits - logits.max(axis=2, keepdims=True)
                probabilities = np.exp(shifted)
                probabilities /= probabilities.sum(axis=2, keepdims=True)
                selected_probability = np.take_along_axis(
                    probabilities,
                    reference[:, :, None],
                    axis=2,
                )[:, :, 0]
                nll = np.sum(weights * -np.log(np.maximum(selected_probability, 1e-15)), axis=1) / weights.sum(axis=1)
                one_hot = np.eye(3)[reference]
                brier_rows = np.sum((probabilities - one_hot) ** 2, axis=2)
                brier = np.sum(weights * brier_rows, axis=1) / weights.sum(axis=1)
                put("ce_calibration.unweighted_nll", start, stop, seed_column, nll)
                put("ce_calibration.unweighted_brier", start, stop, seed_column, brier)
                put("ce_calibration.unweighted_ece10", start, stop, seed_column, _ece(logits, reference, weights))

                raw_structured = trace["probe_structured_raw"].reshape(100, 80, 4)
                schema = probe_schema
                scale = np.where(schema == 0, 0.1, 10.0)
                radius = np.maximum(
                    np.where(schema == 0, raw_structured[:, :, 1], raw_structured[:, :, 3]),
                    0.0,
                ) * scale
                groups = calibration["calibrations"][seed_column]["structured"]["groups"]
                eta = np.where(
                    schema == 0,
                    float(groups["J"]["eta_normalized"]) * 0.1,
                    float(groups["T"]["eta_normalized"]) * 10.0,
                )
                for schema_index, schema_name in ((0, "J"), (1, "T")):
                    selected = schema == schema_index
                    denominator = np.sum(weights * selected, axis=1)
                    proposed_width = np.sum(weights * selected * 2.0 * radius, axis=1) / denominator
                    accepted_width = np.sum(weights * selected * 2.0 * (radius + eta), axis=1) / denominator
                    put(
                        f"region.schema_{schema_name}.unweighted_proposed_width",
                        start,
                        stop,
                        seed_column,
                        proposed_width,
                    )
                    put(
                        f"region.schema_{schema_name}.unweighted_accepted_width",
                        start,
                        stop,
                        seed_column,
                        accepted_width,
                    )

                request_reference = trace["request_reference_outcome"].reshape(100, 40)
                for arm, field in (
                    ("structured", "request_structured_outcome"),
                    ("ce", "request_ce_outcome"),
                    ("center_only", "request_center_only_outcome"),
                    ("unaccepted_production", "request_unaccepted_production_outcome"),
                    ("self_confidence_invalid", "request_self_confidence_outcome"),
                ):
                    request_prediction = trace[field].reshape(100, 40)
                    for outcome, outcome_name in outcome_labels.items():
                        selected = request_reference == outcome
                        put(
                            f"request.{arm}.unweighted_accuracy.outcome_{outcome_name}",
                            start,
                            stop,
                            seed_column,
                            _weighted_accuracy(
                                request_reference,
                                request_prediction,
                                np.ones((100, 40), dtype=np.float64),
                                selected,
                            ),
                        )

    finite_calibration = all(
        np.isfinite(float(group["eta_normalized"]))
        for pair in calibration["calibrations"]
        for bundle in pair.values()
        for group in bundle["groups"].values()
    )
    metadata = {
        "trace_shards_verified": len(records),
        "finite_calibration_expansions": finite_calibration,
        "infinite_proposal_rate": 0.0 if finite_calibration else None,
        "binding_rejection_rate": 0.0,
        "finite_usable_region_coverage_equals_registered_coverage": finite_calibration,
        "regenerated_final_worlds_for_analysis_only": False,
        "trace_secondary_weighting": "unweighted design companions; target weights were not retained in compact traces",
    }
    return arrays, metadata


def analyze() -> Mapping[str, Any]:
    raw = _read_json(RAW_PATH)
    protocol = _read_json(PROTOCOL_PATH)
    calibration = _read_json(CALIBRATION_PATH)
    if raw.get("status") != "raw_repaired_run_complete_unadjudicated":
        raise ValueError("raw v1.1 result is missing or already mutated")
    if raw.get("adjudication") is not None:
        raise ValueError("raw result must remain unadjudicated")
    if protocol["analysis_bootstrap"] != {
        "fit_seed_handling": "average fixed eight paired fits within world",
        "replicates": BOOTSTRAP_REPLICATES,
        "seed": BOOTSTRAP_SEED,
        "unit": "world_root",
    }:
        raise ValueError("analysis constants differ from the frozen protocol")

    cubes = metric_cubes(raw)
    delta_cubes = {
        "transfer": cubes["E_transfer_structured"] - cubes["E_transfer_ce"],
        "boundary": cubes["E_boundary_structured"] - cubes["E_boundary_ce"],
        "in_regime": cubes["E_in_structured"] - cubes["E_in_ce"],
    }
    world_values = np.column_stack(
        [
            delta_cubes["transfer"].mean(axis=1),
            delta_cubes["boundary"].mean(axis=1),
            delta_cubes["in_regime"].mean(axis=1),
            cubes["coverage_J"].mean(axis=1),
            cubes["coverage_T"].mean(axis=1),
        ]
    )
    names = ("transfer", "boundary", "in_regime", "coverage_J", "coverage_T")
    bootstrap = bootstrap_means(world_values)
    estimates = {name: float(world_values[:, index].mean()) for index, name in enumerate(names)}
    draws = {name: bootstrap[:, index] for index, name in enumerate(names)}

    superiority_raw = {
        name: centered_one_sided_p(draws[name], estimates[name], 0.05)
        for name in ("transfer", "boundary")
    }
    superiority_holm = holm_adjust(superiority_raw)
    f35_endpoints: dict[str, Any] = {}
    for name in ("transfer", "boundary"):
        local_alpha = float(superiority_holm[name]["local_alpha"])
        f35_endpoints[name] = {
            "structured_mean": float(cubes[f"E_{name}_structured"].mean()),
            "ce_mean": float(cubes[f"E_{name}_ce"].mean()),
            "delta": estimates[name],
            "null_margin": 0.05,
            "percentile_ci95": _percentile_interval(draws[name]),
            "holm_one_sided_lower_bound": float(np.quantile(draws[name], local_alpha)),
            "inference": superiority_holm[name],
            "passes": bool(superiority_holm[name]["reject"]),
        }
    guard_p = centered_one_sided_p(draws["in_regime"], estimates["in_regime"], -0.02)
    guard = {
        "structured_mean": float(cubes["E_in_structured"].mean()),
        "ce_mean": float(cubes["E_in_ce"].mean()),
        "delta": estimates["in_regime"],
        "null_margin": -0.02,
        "percentile_ci95": _percentile_interval(draws["in_regime"]),
        "one_sided_lower_bound": float(np.quantile(draws["in_regime"], 0.05)),
        "raw_p": guard_p,
        "passes": guard_p <= ALPHA,
    }

    reverse_primary = {
        name: float(np.quantile(draws[name], 1.0 - float(superiority_holm[name]["local_alpha"])))
        for name in ("transfer", "boundary")
    }
    reverse_guard_upper = float(np.quantile(draws["in_regime"], 0.95))
    f35_supported = all(item["passes"] for item in f35_endpoints.values()) and guard["passes"]
    f35_falsified = (
        not f35_supported
        and all(upper <= 0.02 for upper in reverse_primary.values())
        and reverse_guard_upper <= 0.0
    )
    f35_disposition = "supported" if f35_supported else "falsified" if f35_falsified else "mixed_or_inconclusive"

    coverage_raw = {
        name: centered_one_sided_p(draws[name], estimates[name], 0.88)
        for name in ("coverage_J", "coverage_T")
    }
    coverage_holm = holm_adjust(coverage_raw)
    coverage_results: dict[str, Any] = {}
    for name, schema in (("coverage_J", "J"), ("coverage_T", "T")):
        local_alpha = float(coverage_holm[name]["local_alpha"])
        lower = float(np.quantile(draws[name], local_alpha))
        coverage_results[schema] = {
            "point_estimate": estimates[name],
            "nominal": 0.90,
            "null_lower_margin": 0.88,
            "distance_from_nominal": estimates[name] - 0.90,
            "percentile_ci95": _percentile_interval(draws[name]),
            "holm_one_sided_lower_bound": lower,
            "inference": coverage_holm[name],
            "passes": bool(coverage_holm[name]["reject"] and lower >= 0.88),
        }
    f36_supported = all(result["passes"] for result in coverage_results.values())
    f36_disposition = "supported" if f36_supported else "not_supported_or_inconclusive"

    two_way = {
        name: _percentile_interval(two_way_bootstrap(delta_cubes[name]))
        for name in ("transfer", "boundary", "in_regime")
    }
    seed_sensitivity = {
        name: {
            "per_seed_means": {
                str(seed): float(delta_cubes[name][:, column].mean())
                for column, seed in enumerate(FIT_SEEDS)
            },
            "min": float(delta_cubes[name].mean(axis=0).min()),
            "max": float(delta_cubes[name].mean(axis=0).max()),
            "sd": float(delta_cubes[name].mean(axis=0).std(ddof=1)),
            "two_way_bootstrap_ci95": two_way[name],
        }
        for name in delta_cubes
    }

    all_metric_summaries = {
        name: _normal_summary(cube.mean(axis=1))
        for name, cube in cubes.items()
    }
    trace_arrays, trace_metadata = trace_secondaries(raw, calibration)
    trace_summaries = {
        name: _normal_summary(_finite_row_means(values))
        for name, values in trace_arrays.items()
    }

    inactive_maximum = max(
        float(np.max(cubes["inactive_selection_rate_structured"])),
        float(np.max(cubes["inactive_selection_rate_ce"])),
    )
    fixture = succession_fixture()
    result: dict[str, Any] = {
        "status": "analysis_complete",
        "date": "2026-07-16",
        "raw_result_sha256": _sha256(RAW_PATH),
        "protocol_sha256": _sha256(PROTOCOL_PATH),
        "selection_checkpoint_sha256": _sha256(SELECTION_PATH),
        "fit_checkpoint_sha256": _sha256(FIT_PATH),
        "calibration_checkpoint_sha256": _sha256(CALIBRATION_PATH),
        "implementation_version": raw["implementation_version"],
        "protocol_version": raw["protocol_version"],
        "analysis_contract": {
            "independent_unit": "world_root",
            "worlds": WORLD_COUNT,
            "paired_fit_seeds": list(FIT_SEEDS),
            "seed_handling": "average fixed eight paired fits within world before world inference",
            "bootstrap_replicates": BOOTSTRAP_REPLICATES,
            "bootstrap_seed": BOOTSTRAP_SEED,
            "bootstrap_rng": f"numpy.default_rng PCG64 under NumPy {np.__version__}",
            "centered_one_sided_p": "(1 + count(null + boot - estimate >= estimate)) / (B + 1)",
            "percentile_intervals": True,
            "holm_familywise_alpha": ALPHA,
            "secondary_intervals": "normal world-clustered 95% intervals; descriptive",
        },
        "minimum_core": {
            "F35": {
                "disposition": f35_disposition,
                "superiority": f35_endpoints,
                "in_regime_guard": guard,
                "reverse_falsification_check": {
                    "primary_delta_upper_bounds": reverse_primary,
                    "required_primary_upper_at_most": 0.02,
                    "guard_delta_upper_bound": reverse_guard_upper,
                    "required_guard_upper_at_most": 0.0,
                    "passes": f35_falsified,
                },
                "project_impact": (
                    "Supports the practical preference for structured statistic/envelope learning over direct K3 cross-entropy on the frozen synthetic transfer and boundary tasks; it does not show universal architectural superiority, scientific realism, or interpretability."
                    if f35_supported
                    else "Does not establish the project's preferred structured objective; the paper must narrow or remove that comparative empirical motivation while retaining the architecture-neutral logic and exact decoder results."
                ),
            },
            "F36": {
                "disposition": f36_disposition,
                "schemas": coverage_results,
                "project_impact": (
                    "Supports registered marginal target-in-proposal coverage for both frozen statistic groups; this is not conditional, profile, selected, or system coverage, and finite evidence still requires the exact checker."
                    if f36_supported
                    else "The learned proposal/calibration path lacks experiment-level support for its registered marginal coverage claim; the logic remains intact, but empirical certificate language must be narrowed and the failure reported."
                ),
            },
        },
        "optimization_variability": seed_sensitivity,
        "registered_metric_summaries": all_metric_summaries,
        "trace_secondary_summaries": trace_summaries,
        "trace_audit": trace_metadata,
        "exact_safety_checks": {
            "maximum_inactive_selection_rate": inactive_maximum,
            "inactive_selection_exactly_zero": inactive_maximum == 0.0,
            "F18_system_witness": raw["system_witness"],
        },
        "deterministic_succession_fixture": {
            "evidence_grade": "deterministic_fixture_only",
            "simultaneous_active": [plan.value for plan in fixture.simultaneous_active],
            "gap_active": [plan.value for plan in fixture.gap_active],
            "gap_uses_fallback": fixture.gap_uses_fallback,
            "lapse_outcome": fixture.lapse_outcome.value,
            "rebuttal_outcome": fixture.rebuttal_outcome.value,
            "irrelevant_update_unchanged": fixture.irrelevant_before == fixture.irrelevant_after,
            "tolerance_old": int(fixture.tolerance_old),
            "tolerance_successor": int(fixture.tolerance_successor),
            "later_dominates": [plan.value for plan in fixture.later_dominates],
        },
        "protocol_deviations_and_limits": [
            {
                "id": "21-D1",
                "kind": "versioned execution-only amendment",
                "description": "The frozen v1 object-heavy runner failed/interrupted before a readable result. Task 20R v1.1 preserved the scientific estimand and used array blocks, C++, and resumable checkpoints.",
                "impact": "Disclose in every result; no endpoint, sample, seed, model, loss, calibration rule, or multiplicity rule changed.",
            },
            {
                "id": "21-D2",
                "kind": "unread infrastructure retry before selection checkpoint",
                "description": "The first v1.1 selection invocation stopped after about nine seconds with the transient message 'Plan object is not callable'. No checkpoint or final payload existed; unchanged frozen source completed on the diagnostic retry.",
                "impact": "No model or endpoint was selected from outcomes; retain as an infrastructure deviation and do not treat it as evidence for or against F35/F36.",
            },
            {
                "id": "21-D3",
                "kind": "registered secondary reporting gap",
                "description": "The frozen compact trace supports unweighted false-support/refutation, class misses, schema/state fidelity, public outcomes, widths, CE calibration, and masks from fixed row layout. It omits target/design weights and polarity/mode/diagnostic labels, and it does not contain enough fields to reconstruct selected/deployed task loss or misroute severity without regenerated custom world records or a post-final convention.",
                "impact": "Those secondary quantities are explicitly unreported and cannot rescue or overturn the primary claims; repair only in a separately versioned future study.",
            },
            {
                "id": "21-D4",
                "kind": "analysis implementation clarification",
                "description": "Task 19 froze the bootstrap seed and replicate count but not the pseudorandom algorithm. Analysis uses NumPy default_rng/PCG64 under the pinned NumPy version and records it here.",
                "impact": "The exact machine-readable estimates are reproducible; conclusions must also be checked against the reported percentile bounds and seed sensitivity.",
            },
            {
                "id": "21-D5",
                "kind": "post-final analysis infrastructure failure",
                "description": "Two analysis invocations that attempted to regenerate custom final-world metadata stopped before writing an analysis when CPython transiently treated an array slot as a slice. The raw result and hashed traces were unchanged. The completed analysis therefore uses sealed target-weighted metric rows for registered endpoints and fixed-layout unweighted trace companions without regenerating Python world objects.",
                "impact": "Primary inference is unaffected; target-weighted polarity/mode/diagnostic and task-loss secondaries are unavailable and are disclosed rather than reconstructed unsafely.",
            },
        ],
        "unreported_registered_secondaries": [
            "target-weighted trace-derived false-support/refutation and class-miss rates",
            "atom fidelity by polarity, evidence mode, and exact diagnostic",
            "selected task loss",
            "deployed task loss",
            "misroute severity",
        ],
        "claims_not_made": [
            "ReLU is uniquely or generally optimal",
            "synthetic success establishes scientific realism",
            "marginal proposal coverage is conditional, profile, routed, or system coverage",
            "functional fidelity establishes semantic alignment or mechanistic interpretability",
            "the deterministic system witness is a powered empirical system comparison",
        ],
    }
    _atomic_json(ANALYSIS_PATH, result)
    render_figures(result)
    return result


def render_figures(analysis: Mapping[str, Any]) -> None:
    FIGURE_DIRECTORY.mkdir(exist_ok=True)
    colors = {"structured": "#3366cc", "ce": "#dc3912"}

    labels = ("In regime", "Boundary", "Tolerance transfer")
    metric_keys = ("E_in", "E_boundary", "E_transfer")
    x = np.arange(len(labels))
    width = 0.36
    figure, axis = plt.subplots(figsize=(8, 4.8))
    for offset, arm in ((-width / 2, "structured"), (width / 2, "ce")):
        means = [analysis["registered_metric_summaries"][f"{key}_{arm}"]["mean"] for key in metric_keys]
        intervals = [analysis["registered_metric_summaries"][f"{key}_{arm}"]["ci95"] for key in metric_keys]
        errors = np.asarray([[mean - interval[0] for mean, interval in zip(means, intervals)], [interval[1] - mean for mean, interval in zip(means, intervals)]])
        label = "CE" if arm == "ce" else arm.replace("_", " ").title()
        axis.bar(x + offset, means, width, yerr=errors, label=label, color=colors[arm], capsize=3)
    axis.set_ylabel("World-first fidelity")
    axis.set_ylim(0.0, 1.0)
    axis.set_xticks(x, labels)
    axis.legend()
    axis.set_title("Registered fidelity endpoints")
    figure.tight_layout()
    figure.savefig(FIGURE_DIRECTORY / "primary_endpoints_v1_1.png", dpi=180)
    plt.close(figure)

    coverage = analysis["minimum_core"]["F36"]["schemas"]
    figure, axis = plt.subplots(figsize=(6, 4.5))
    points = [coverage[schema]["point_estimate"] for schema in ("J", "T")]
    intervals = [coverage[schema]["percentile_ci95"] for schema in ("J", "T")]
    errors = np.asarray([[point - interval[0] for point, interval in zip(points, intervals)], [interval[1] - point for point, interval in zip(points, intervals)]])
    axis.errorbar((0, 1), points, yerr=errors, fmt="o", capsize=5, color="#3366cc")
    axis.axhline(0.90, color="#109618", linestyle="--", label="nominal .90")
    axis.axhline(0.88, color="#dc3912", linestyle=":", label="registered lower margin .88")
    axis.set_xticks((0, 1), ("Loss J", "Latency T"))
    axis.set_ylabel("Marginal target-in-proposal coverage")
    axis.set_ylim(0.84, 0.94)
    axis.legend()
    axis.set_title("Registered calibration groups")
    figure.tight_layout()
    figure.savefig(FIGURE_DIRECTORY / "coverage_v1_1.png", dpi=180)
    plt.close(figure)

    arms = ("structured", "ce", "center_only", "unaccepted_radius_shadow", "self_confidence_invalid")
    labels = ("Structured", "CE", "Center only", "Unaccepted shadow", "Self-confidence")
    endpoints = ("E_in", "E_boundary", "E_transfer")
    figure, axis = plt.subplots(figsize=(11, 5.2))
    positions = np.arange(len(endpoints))
    bar_width = 0.15
    for index, (arm, label) in enumerate(zip(arms, labels)):
        values = [analysis["registered_metric_summaries"][f"{endpoint}_{arm}"]["mean"] for endpoint in endpoints]
        axis.bar(positions + (index - 2) * bar_width, values, bar_width, label=label)
    axis.set_xticks(positions, ("In regime", "Boundary", "Transfer"))
    axis.set_ylim(0.0, 1.0)
    axis.set_ylabel("Fidelity (descriptive)")
    axis.set_title("Required arms and ablations")
    axis.legend(ncols=3, fontsize=8)
    figure.tight_layout()
    figure.savefig(FIGURE_DIRECTORY / "ablations_v1_1.png", dpi=180)
    plt.close(figure)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)
    result = analyze()
    print(
        json.dumps(
            {
                "status": result["status"],
                "analysis": str(ANALYSIS_PATH),
                "analysis_sha256": _sha256(ANALYSIS_PATH),
                "F35": result["minimum_core"]["F35"]["disposition"],
                "F36": result["minimum_core"]["F36"]["disposition"],
                "figures": sorted(path.name for path in FIGURE_DIRECTORY.glob("*_v1_1.png")),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
