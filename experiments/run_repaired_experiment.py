"""Versioned, resumable entry point for the Task 20R execution repair.

Task 20R may run ``--preflight`` and ``--pilot`` only.  The four production
stages remain separately authorized for the later Task 21 prompt.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict
from hashlib import sha256
import json
import os
from pathlib import Path
import sys
import time
from typing import Any, Mapping, Sequence

import numpy as np
import torch

from experiments.build_cpp_kernel import build_cpp_kernel
from experiments.cpp_kernel import (
    KernelInputs,
    assert_kernel_equivalence,
    built_cpp_kernel,
    numpy_decode_block,
)
from experiments.implementation import (
    FEATURE_NAMES,
    CalibrationBundle,
    CalibrationGroup,
    implementation_preflight,
)
from experiments.learner import (
    FitConfig,
    JointSelection,
    ReluMLP,
    TrialScore,
    matched_architectures,
    model_parameter_hash,
    state_dict_arrays,
)
from experiments.protocol import FIT_SEEDS, Role, Schema
from experiments.repaired_evaluator import (
    FLOAT_TRACE_EQUIVALENCE_ATOL,
    assert_evaluation_equivalence,
    assert_fast_adapter_equivalence,
    assert_training_adapter_equivalence,
    calibrate_structured_pair,
    evaluate_model_on_block,
    materialize_training_panel_fast,
    prepare_evaluation_block,
)
from experiments.run_experiment import (
    MANIFESTS_PATH,
    PROTOCOL_PATH,
    _fit_final_models,
    _fit_grid,
    _selection,
    _subpanel,
    _summary,
    _evaluate_one_world_seed,
)
from experiments.system_witness import deterministic_system_witness


ROOT = Path(__file__).resolve().parents[1]
IMPLEMENTATION_PATH = ROOT / "experiments" / "implementation_v1_1.json"
PILOT_RECORD_PATH = ROOT / "experiments" / "implementation_repair_pilot_v1_1.json"
SELECTION_PATH = ROOT / "experiments" / "selection_checkpoint_v1_1.json"
MODELS_PATH = ROOT / "experiments" / "model_states_v1_1.npz"
FIT_PATH = ROOT / "experiments" / "fit_checkpoint_v1_1.json"
CALIBRATION_PATH = ROOT / "experiments" / "calibration_checkpoint_v1_1.json"
RESULTS_PATH = ROOT / "experiments" / "raw_results_v1_1.json"
TRACE_DIRECTORY = ROOT / "experiments" / "trace_shards_v1_1"
PROGRESS_DIRECTORY = ROOT / "experiments" / "confirmation_progress_v1_1"

IMPLEMENTATION_VERSION = "value-logic-implementation-v1.1.0"
STAGE_TOKEN = "PREPARE-VALUE-LOGIC-REPAIR-V1-1"
FINAL_TOKEN = "RUN-VALUE-LOGIC-REPAIR-FINAL-V1-1"
SOURCE_FILES = (
    "experiments/learner.py",
    "experiments/implementation.py",
    "experiments/system_witness.py",
    "experiments/run_experiment.py",
    "experiments/build_cpp_kernel.py",
    "experiments/cpp_kernel.py",
    "experiments/repaired_evaluator.py",
    "experiments/run_repaired_experiment.py",
    "experiments/cpp/CMakeLists.txt",
    "experiments/cpp/value_logic_kernel.h",
    "experiments/cpp/value_logic_kernel.cpp",
    "experiments/cpp/value_logic_kernel_self_test.cpp",
)


def _sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _json(path: Path) -> Mapping[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _atomic_json(path: Path, value: Mapping[str, Any] | Sequence[Any]) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def _atomic_models(path: Path, arrays: Mapping[str, np.ndarray]) -> None:
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("wb") as handle:
        np.savez_compressed(handle, **arrays)
    os.replace(temporary, path)


def verify_repaired_sources() -> Mapping[str, Any]:
    if not IMPLEMENTATION_PATH.exists():
        raise FileNotFoundError("Task 20R implementation_v1_1.json has not been frozen")
    contract = _json(IMPLEMENTATION_PATH)
    observed = {name: _sha256(ROOT / name) for name in SOURCE_FILES}
    mismatches = {
        name: {"expected": contract["source_sha256"].get(name), "observed": digest}
        for name, digest in observed.items()
        if contract["source_sha256"].get(name) != digest
    }
    if mismatches:
        raise RuntimeError(f"repaired implementation source drift: {mismatches}")
    if contract["protocol_sha256"] != _sha256(PROTOCOL_PATH):
        raise RuntimeError("frozen protocol hash drift")
    if contract["manifests_sha256"] != _sha256(MANIFESTS_PATH):
        raise RuntimeError("frozen role-manifest hash drift")
    return contract


def _random_kernel_check() -> None:
    rng = np.random.default_rng(20_026_071_5)
    count = 10_000
    inputs = KernelInputs(
        rng.normal(size=(count, 4)).astype(np.float32),
        rng.normal(size=(count, 3)).astype(np.float32),
        rng.integers(0, 2, count, dtype=np.int8),
        rng.normal(size=count),
        rng.integers(0, 2, count, dtype=np.uint8),
        rng.integers(0, 2, count, dtype=np.uint8),
        rng.integers(0, 2, count, dtype=np.uint8),
        rng.integers(0, 2, count, dtype=np.uint8),
        rng.random(count),
        rng.random(count),
        rng.integers(0, 2, count, dtype=np.uint8),
        rng.integers(0, 2, count, dtype=np.uint8),
    )
    assert_kernel_equivalence(numpy_decode_block(inputs), built_cpp_kernel().decode(inputs))


def run_preflight() -> Mapping[str, Any]:
    verify_repaired_sources()
    build = build_cpp_kernel(verify_debug=True)
    _random_kernel_check()
    assert_training_adapter_equivalence(worlds=4)
    assert_fast_adapter_equivalence(worlds=4)
    base = implementation_preflight(PROTOCOL_PATH, MANIFESTS_PATH)
    return {
        "status": "pass",
        "implementation_version": IMPLEMENTATION_VERSION,
        "source_hashes_verified": True,
        "cpp_kernel": build,
        "numpy_cpp_rows_checked": 10_000,
        "legacy_adapter_pilot_worlds_checked": 4,
        "float_trace_equivalence_atol": FLOAT_TRACE_EQUIVALENCE_ATOL,
        "final_payloads_generated": RESULTS_PATH.exists(),
        "old_attempt2_partial_model_retained": (ROOT / "experiments" / "model_states_v1.npz").exists(),
        "base_preflight": dict(base),
        "system_witness": deterministic_system_witness(),
        "contract_sha256": _sha256(IMPLEMENTATION_PATH),
    }


def _pilot_models():
    panel = materialize_training_panel_fast(Role.PILOT, 0, 256)
    train = _subpanel(panel, 0, 32)
    validation = _subpanel(panel, 32, 48)
    structured_spec, ce_spec = matched_architectures(len(FEATURE_NAMES), 12_000)
    config = FitConfig(
        0.001,
        0.0,
        12_000,
        batch_worlds=16,
        max_epochs=4,
        patience_epochs=2,
        validation_cadence=1,
        center_epochs=2,
        radius_epochs=2,
    )
    from experiments.learner import fit_cross_entropy, fit_structured

    structured, structured_summary = fit_structured(
        train, validation, structured_spec, config, FIT_SEEDS[0]
    )
    ce, ce_summary = fit_cross_entropy(
        train, validation, ce_spec, config, FIT_SEEDS[0]
    )
    common = {
        "scorer_parameter_hash": structured_summary.parameter_hash,
        "training_manifest_hash": "pilot-fast-training-v1-1",
        "calibration_manifest_hash": "pilot-fast-calibration-v1-1",
    }
    calibrations = calibrate_structured_pair(structured, panel, **common)
    return structured, ce, structured_summary, ce_summary, calibrations


def run_pilot() -> Mapping[str, Any]:
    preflight = run_preflight()
    structured, ce, structured_summary, ce_summary, calibrations = _pilot_models()
    kernel = built_cpp_kernel()

    equivalence_block = prepare_evaluation_block(Role.PILOT, 48, 4)
    repaired = evaluate_model_on_block(
        equivalence_block,
        structured,
        ce,
        structured_summary.parameter_hash,
        calibrations[0],
        calibrations[1],
        kernel,
        fit_seed=FIT_SEEDS[0],
    )
    for local, world_index in enumerate(range(48, 52)):
        legacy_metrics, legacy_trace = _evaluate_one_world_seed(
            world_index,
            structured,
            ce,
            structured_summary.parameter_hash,
            calibrations[0],
            calibrations[1],
            role=Role.PILOT,
        )
        assert_evaluation_equivalence(
            legacy_metrics,
            legacy_trace,
            repaired.metrics[local],
            repaired.traces[local],
        )

    benchmark_worlds = 100
    started = time.perf_counter()
    block = prepare_evaluation_block(Role.PILOT, 100, benchmark_worlds)
    preparation_seconds = time.perf_counter() - started
    features = block.combined_features()
    started = time.perf_counter()
    for seed in FIT_SEEDS:
        evaluate_model_on_block(
            block,
            structured,
            ce,
            structured_summary.parameter_hash,
            calibrations[0],
            calibrations[1],
            kernel,
            fit_seed=seed,
            combined_features=features,
        )
    eight_seed_seconds = time.perf_counter() - started
    projected_confirmation_seconds = 50.0 * (preparation_seconds + eight_seed_seconds)
    performance_gate = projected_confirmation_seconds <= 900.0
    if not performance_gate:
        raise RuntimeError(
            "Task 20R performance gate failed: projected confirmation exceeds 15 minutes"
        )
    result = {
        "status": "pass",
        "date": "2026-07-16",
        "evidence_grade": "pilot_role_execution_repair_only",
        "implementation_version": IMPLEMENTATION_VERSION,
        "contract_sha256": preflight["contract_sha256"],
        "cpp_source_sha256": preflight["cpp_kernel"]["source_sha256"],
        "equivalence_worlds": 4,
        "discrete_trace_fields_exact": True,
        "float_trace_equivalence_atol": FLOAT_TRACE_EQUIVALENCE_ATOL,
        "feature_arrays_bitwise_equal": True,
        "calibration_pair_reuses_one_prediction": True,
        "benchmark": {
            "worlds_per_block": benchmark_worlds,
            "block_preparation_seconds": preparation_seconds,
            "eight_seed_evaluation_seconds": eight_seed_seconds,
            "projected_fifty_block_confirmation_seconds": projected_confirmation_seconds,
            "maximum_allowed_projected_seconds": 900.0,
            "performance_gate": performance_gate,
        },
        "structured": _summary(structured_summary),
        "cross_entropy": _summary(ce_summary),
        "production_payloads_generated": False,
        "final_payloads_generated": False,
        "empirical_claim_adjudicated": False,
    }
    _atomic_json(PILOT_RECORD_PATH, result)
    return result


def _require_stage_token(token: str) -> None:
    if token != STAGE_TOKEN:
        raise PermissionError("the exact repaired-stage authorization token is required")


def _require_passed_pilot() -> Mapping[str, Any]:
    if not PILOT_RECORD_PATH.exists():
        raise FileNotFoundError("the Task 20R equivalence/performance pilot must pass first")
    pilot = _json(PILOT_RECORD_PATH)
    if (
        pilot.get("status") != "pass"
        or pilot.get("implementation_version") != IMPLEMENTATION_VERSION
        or pilot.get("contract_sha256") != _sha256(IMPLEMENTATION_PATH)
        or not pilot.get("benchmark", {}).get("performance_gate", False)
    ):
        raise RuntimeError("the Task 20R pilot is stale or did not pass")
    return pilot


def _require_current_contract(record: Mapping[str, Any], label: str) -> None:
    if record.get("implementation_version") != IMPLEMENTATION_VERSION:
        raise RuntimeError(f"{label} belongs to another implementation version")
    if record.get("contract_sha256") != _sha256(IMPLEMENTATION_PATH):
        raise RuntimeError(f"{label} is not bound to the current v1.1 contract")


def _selection_from_record(record: Mapping[str, Any]) -> JointSelection:
    selected = record["selection"]
    structured_config = FitConfig(**selected["structured"]["config"])
    ce_config = FitConfig(**selected["cross_entropy"]["config"])
    return JointSelection(
        int(selected["parameter_budget"]),
        TrialScore(
            "structured",
            structured_config,
            float(selected["structured"]["validation_loss"]),
        ),
        TrialScore(
            "cross_entropy",
            ce_config,
            float(selected["cross_entropy"]["validation_loss"]),
        ),
        float(selected["normalized_joint_regret"]),
    )


def run_selection_stage(token: str) -> Mapping[str, Any]:
    _require_stage_token(token)
    verify_repaired_sources()
    _require_passed_pilot()
    if SELECTION_PATH.exists():
        record = _json(SELECTION_PATH)
        _require_current_contract(record, "selection checkpoint")
        return {"status": "resume_existing", "checkpoint": str(SELECTION_PATH), "sha256": _sha256(SELECTION_PATH)}
    if any(path.exists() for path in (FIT_PATH, CALIBRATION_PATH, RESULTS_PATH)):
        raise RuntimeError("later repaired-stage artifact exists without selection checkpoint")
    started = time.perf_counter()
    train = materialize_training_panel_fast(Role.TRAIN, 0, 20_000)
    selection, trials = _fit_grid(_subpanel(train, 0, 16_000), _subpanel(train, 16_000, 20_000), _json(PROTOCOL_PATH))
    record = {
        "status": "selection_complete",
        "implementation_version": IMPLEMENTATION_VERSION,
        "contract_sha256": _sha256(IMPLEMENTATION_PATH),
        "selection": _selection(selection),
        "trials": trials,
        "elapsed_seconds": time.perf_counter() - started,
        "final_payloads_generated": False,
    }
    _atomic_json(SELECTION_PATH, record)
    return {"status": record["status"], "checkpoint": str(SELECTION_PATH), "sha256": _sha256(SELECTION_PATH)}


def _save_models(
    structured_models: Sequence[ReluMLP],
    ce_models: Sequence[ReluMLP],
) -> str:
    arrays: dict[str, np.ndarray] = {}
    for seed, structured, ce in zip(FIT_SEEDS, structured_models, ce_models):
        for name, value in state_dict_arrays(structured).items():
            arrays[f"structured_{seed}_{name}"] = value
        for name, value in state_dict_arrays(ce).items():
            arrays[f"cross_entropy_{seed}_{name}"] = value
    _atomic_models(MODELS_PATH, arrays)
    return _sha256(MODELS_PATH)


def run_fit_stage(token: str) -> Mapping[str, Any]:
    _require_stage_token(token)
    verify_repaired_sources()
    if FIT_PATH.exists() and MODELS_PATH.exists():
        record = _json(FIT_PATH)
        _require_current_contract(record, "fit checkpoint")
        if record.get("selection_checkpoint_sha256") != _sha256(SELECTION_PATH):
            raise RuntimeError("repaired fit checkpoint/selection hash mismatch")
        if record["models_sha256"] != _sha256(MODELS_PATH):
            raise RuntimeError("repaired fit checkpoint/model hash mismatch")
        return {"status": "resume_existing", "checkpoint": str(FIT_PATH), "sha256": _sha256(FIT_PATH)}
    if not SELECTION_PATH.exists():
        raise FileNotFoundError("selection stage must complete before final fitting")
    if any(path.exists() for path in (CALIBRATION_PATH, RESULTS_PATH)):
        raise RuntimeError("later repaired-stage artifact exists without fit checkpoint")
    started = time.perf_counter()
    selection_record = _json(SELECTION_PATH)
    selection = _selection_from_record(selection_record)
    train = materialize_training_panel_fast(Role.TRAIN, 0, 20_000)
    structured, ce, summaries = _fit_final_models(
        _subpanel(train, 0, 16_000),
        _subpanel(train, 16_000, 20_000),
        selection,
    )
    model_hash = _save_models(structured, ce)
    record = {
        "status": "final_fits_complete",
        "implementation_version": IMPLEMENTATION_VERSION,
        "contract_sha256": _sha256(IMPLEMENTATION_PATH),
        "selection_checkpoint_sha256": _sha256(SELECTION_PATH),
        "models_sha256": model_hash,
        "fits": [
            {"structured": _summary(pair[0]), "cross_entropy": _summary(pair[1])}
            for pair in summaries
        ],
        "elapsed_seconds": time.perf_counter() - started,
        "final_payloads_generated": False,
    }
    _atomic_json(FIT_PATH, record)
    return {"status": record["status"], "checkpoint": str(FIT_PATH), "sha256": _sha256(FIT_PATH)}


def _load_models() -> tuple[list[ReluMLP], list[ReluMLP], Mapping[str, Any]]:
    if not (FIT_PATH.exists() and MODELS_PATH.exists()):
        raise FileNotFoundError("repaired fit checkpoint and model archive are required")
    fit = _json(FIT_PATH)
    _require_current_contract(fit, "fit checkpoint")
    if fit["models_sha256"] != _sha256(MODELS_PATH):
        raise RuntimeError("model archive does not match repaired fit checkpoint")
    structured_models: list[ReluMLP] = []
    ce_models: list[ReluMLP] = []
    with np.load(MODELS_PATH, allow_pickle=False) as arrays:
        for seed, summaries in zip(FIT_SEEDS, fit["fits"]):
            pair = []
            for arm_name, output_dim in (("structured", 4), ("cross_entropy", 3)):
                summary = summaries[arm_name]
                architecture = summary["architecture"]
                model = ReluMLP(
                    int(architecture["input_dim"]),
                    int(architecture["hidden_width"]),
                    output_dim,
                )
                prefix = f"{arm_name}_{seed}_"
                state = {
                    name[len(prefix):]: torch.from_numpy(arrays[name].copy())
                    for name in arrays.files
                    if name.startswith(prefix)
                }
                model.load_state_dict(state, strict=True)
                if model_parameter_hash(model) != summary["parameter_hash"]:
                    raise RuntimeError(f"loaded {arm_name} model hash mismatch for seed {seed}")
                pair.append(model)
            structured_models.append(pair[0])
            ce_models.append(pair[1])
    return structured_models, ce_models, fit


def _bundle_record(bundle: CalibrationBundle) -> Mapping[str, Any]:
    return {
        "scorer_parameter_hash": bundle.scorer_parameter_hash,
        "arm_variant": bundle.arm_variant,
        "training_manifest_hash": bundle.training_manifest_hash,
        "calibration_manifest_hash": bundle.calibration_manifest_hash,
        "calibration_id": bundle.calibration_id,
        "groups": {
            schema.value: asdict(group)
            for schema, group in bundle.groups.items()
        },
    }


def _bundle_from_record(record: Mapping[str, Any]) -> CalibrationBundle:
    groups = {
        schema: CalibrationGroup(
            schema,
            float(record["groups"][schema.value]["eta_normalized"]),
            int(record["groups"][schema.value]["calibration_worlds"]),
            int(record["groups"][schema.value]["score_count"]),
            int(record["groups"][schema.value]["rank"]),
        )
        for schema in (Schema.LOSS, Schema.LATENCY)
    }
    return CalibrationBundle(
        str(record["scorer_parameter_hash"]),
        str(record["arm_variant"]),
        str(record["training_manifest_hash"]),
        str(record["calibration_manifest_hash"]),
        groups,
        str(record["calibration_id"]),
    )


def run_calibration_stage(token: str) -> Mapping[str, Any]:
    _require_stage_token(token)
    verify_repaired_sources()
    if CALIBRATION_PATH.exists():
        record = _json(CALIBRATION_PATH)
        _require_current_contract(record, "calibration checkpoint")
        if record.get("fit_checkpoint_sha256") != _sha256(FIT_PATH):
            raise RuntimeError("repaired calibration checkpoint/fit hash mismatch")
        return {"status": "resume_existing", "checkpoint": str(CALIBRATION_PATH), "sha256": _sha256(CALIBRATION_PATH)}
    if RESULTS_PATH.exists():
        raise RuntimeError("result exists without repaired calibration checkpoint")
    structured, _, fit = _load_models()
    started = time.perf_counter()
    data = materialize_training_panel_fast(Role.CALIBRATION, 0, 5_000)
    protocol = _json(PROTOCOL_PATH)
    records = []
    for model, summary in zip(structured, fit["fits"]):
        common = {
            "scorer_parameter_hash": summary["structured"]["parameter_hash"],
            "training_manifest_hash": protocol["roles"][Role.TRAIN.value]["manifest_hash"],
            "calibration_manifest_hash": protocol["roles"][Role.CALIBRATION.value]["manifest_hash"],
        }
        pair = calibrate_structured_pair(model, data, **common)
        records.append({bundle.arm_variant: _bundle_record(bundle) for bundle in pair})
    record = {
        "status": "fit_and_calibration_complete_before_repaired_final_materialization",
        "implementation_version": IMPLEMENTATION_VERSION,
        "contract_sha256": _sha256(IMPLEMENTATION_PATH),
        "fit_checkpoint_sha256": _sha256(FIT_PATH),
        "models_sha256": _sha256(MODELS_PATH),
        "calibrations": records,
        "elapsed_seconds": time.perf_counter() - started,
        "final_payloads_generated": False,
    }
    _atomic_json(CALIBRATION_PATH, record)
    return {"status": record["status"], "checkpoint": str(CALIBRATION_PATH), "sha256": _sha256(CALIBRATION_PATH)}


def _write_trace_shard(
    path: Path,
    traces: Sequence[Mapping[str, np.ndarray]],
) -> str:
    keys = set(traces[0])
    if any(set(trace) != keys for trace in traces):
        raise ValueError("trace shard rows do not share one schema")
    combined = {
        key: np.concatenate([trace[key] for trace in traces], axis=0)
        for key in sorted(keys)
    }
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("wb") as handle:
        np.savez_compressed(handle, **combined)
    os.replace(temporary, path)
    return _sha256(path)


def _block_paths(start: int, stop: int) -> tuple[Path, Path]:
    stem = f"worlds_{start:05d}_{stop - 1:05d}"
    return (
        PROGRESS_DIRECTORY / f"{stem}_metrics.json",
        PROGRESS_DIRECTORY / f"{stem}_complete.json",
    )


def _validate_complete_block(marker: Mapping[str, Any], metrics_path: Path) -> None:
    _require_current_contract(marker, "confirmation block marker")
    if marker.get("fit_checkpoint_sha256") != _sha256(FIT_PATH):
        raise RuntimeError("completed confirmation block/fit hash mismatch")
    if marker.get("calibration_checkpoint_sha256") != _sha256(CALIBRATION_PATH):
        raise RuntimeError("completed confirmation block/calibration hash mismatch")
    if marker["metrics_sha256"] != _sha256(metrics_path):
        raise RuntimeError("completed confirmation block metrics hash mismatch")
    for trace in marker["trace_shards"]:
        path = ROOT / trace["path"]
        if not path.exists() or trace["sha256"] != _sha256(path):
            raise RuntimeError("completed confirmation trace shard hash mismatch")


def run_confirmation_stage(token: str) -> Mapping[str, Any]:
    if token != FINAL_TOKEN:
        raise PermissionError("the exact repaired final-confirmation token is required")
    contract = verify_repaired_sources()
    build = build_cpp_kernel()
    if RESULTS_PATH.exists():
        existing = _json(RESULTS_PATH)
        _require_current_contract(existing, "raw result")
        return {"status": "resume_existing", "results": str(RESULTS_PATH), "sha256": _sha256(RESULTS_PATH)}
    if not CALIBRATION_PATH.exists():
        raise FileNotFoundError("selection, fit, and calibration stages must complete first")
    structured, ce, fit = _load_models()
    calibration_record = _json(CALIBRATION_PATH)
    _require_current_contract(calibration_record, "calibration checkpoint")
    if calibration_record["fit_checkpoint_sha256"] != _sha256(FIT_PATH):
        raise RuntimeError("calibration checkpoint is not bound to the fit checkpoint")
    calibrations = [
        (
            _bundle_from_record(pair["structured"]),
            _bundle_from_record(pair["center_only"]),
        )
        for pair in calibration_record["calibrations"]
    ]
    TRACE_DIRECTORY.mkdir(exist_ok=True)
    PROGRESS_DIRECTORY.mkdir(exist_ok=True)
    kernel = built_cpp_kernel()
    started = time.perf_counter()
    all_metrics: list[Mapping[str, Any]] = []
    all_traces: list[Mapping[str, Any]] = []
    for block_start in range(0, 5_000, 100):
        block_stop = min(5_000, block_start + 100)
        metrics_path, marker_path = _block_paths(block_start, block_stop)
        if marker_path.exists() and metrics_path.exists():
            marker = _json(marker_path)
            _validate_complete_block(marker, metrics_path)
            all_metrics.extend(json.loads(metrics_path.read_text(encoding="utf-8")))
            all_traces.extend(marker["trace_shards"])
            continue
        if metrics_path.exists() or marker_path.exists():
            raise RuntimeError("partial repaired block marker requires manual audit")
        block = prepare_evaluation_block(
            Role.FINAL_CONFIRMATION,
            block_start,
            block_stop - block_start,
            allow_final=True,
        )
        features = block.combined_features()
        block_metrics: list[Mapping[str, Any]] = []
        trace_records: list[Mapping[str, Any]] = []
        for seed, structured_model, ce_model, fit_pair, calibration_pair in zip(
            FIT_SEEDS,
            structured,
            ce,
            fit["fits"],
            calibrations,
        ):
            evaluation = evaluate_model_on_block(
                block,
                structured_model,
                ce_model,
                fit_pair["structured"]["parameter_hash"],
                calibration_pair[0],
                calibration_pair[1],
                kernel,
                fit_seed=seed,
                combined_features=features,
            )
            block_metrics.extend(evaluation.metrics)
            trace_path = TRACE_DIRECTORY / (
                f"worlds_{block_start:05d}_{block_stop - 1:05d}_seed_{seed}.npz"
            )
            trace_records.append(
                {
                    "world_start": block_start,
                    "world_stop_exclusive": block_stop,
                    "fit_seed": seed,
                    "path": str(trace_path.relative_to(ROOT)).replace("\\", "/"),
                    "sha256": _write_trace_shard(trace_path, evaluation.traces),
                }
            )
        _atomic_json(metrics_path, block_metrics)
        marker = {
            "status": "block_complete_unadjudicated",
            "implementation_version": IMPLEMENTATION_VERSION,
            "contract_sha256": _sha256(IMPLEMENTATION_PATH),
            "world_start": block_start,
            "world_stop_exclusive": block_stop,
            "metrics_sha256": _sha256(metrics_path),
            "trace_shards": trace_records,
            "fit_checkpoint_sha256": _sha256(FIT_PATH),
            "calibration_checkpoint_sha256": _sha256(CALIBRATION_PATH),
        }
        _atomic_json(marker_path, marker)
        all_metrics.extend(block_metrics)
        all_traces.extend(trace_records)

    seed_order = {seed: index for index, seed in enumerate(FIT_SEEDS)}
    all_metrics.sort(key=lambda row: (seed_order[int(row["fit_seed"])], int(row["world_index"])))
    all_traces.sort(key=lambda row: (seed_order[int(row["fit_seed"])], int(row["world_start"])))
    result = {
        "status": "raw_repaired_run_complete_unadjudicated",
        "implementation_version": IMPLEMENTATION_VERSION,
        "contract_sha256": _sha256(IMPLEMENTATION_PATH),
        "protocol_version": contract["protocol_version"],
        "execution_repair": {
            "original_attempts": [
                "task21_failure_attempt1.json",
                "task21_interruption_attempt2.json",
            ],
            "scientific_estimand_changed": False,
            "block_first_world_reuse": True,
            "batched_inference": True,
            "cpp_kernel": build,
            "float_trace_equivalence_atol": FLOAT_TRACE_EQUIVALENCE_ATOL,
        },
        "selection_checkpoint_sha256": _sha256(SELECTION_PATH),
        "fit_checkpoint_sha256": _sha256(FIT_PATH),
        "calibration_checkpoint_sha256": _sha256(CALIBRATION_PATH),
        "models_sha256": _sha256(MODELS_PATH),
        "world_seed_metrics": all_metrics,
        "trace_shards": all_traces,
        "system_witness": deterministic_system_witness(),
        "hard_moe": "omitted_prospectively",
        "confirmation_elapsed_seconds": time.perf_counter() - started,
        "adjudication": None,
    }
    _atomic_json(RESULTS_PATH, result)
    return {
        "status": result["status"],
        "results": str(RESULTS_PATH),
        "sha256": _sha256(RESULTS_PATH),
        "trace_shards": len(all_traces),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--preflight", action="store_true")
    mode.add_argument("--pilot", action="store_true")
    mode.add_argument("--task21-select", metavar="TOKEN")
    mode.add_argument("--task21-fit", metavar="TOKEN")
    mode.add_argument("--task21-calibrate", metavar="TOKEN")
    mode.add_argument("--task21-confirm", metavar="TOKEN")
    args = parser.parse_args(argv)
    try:
        if args.pilot:
            result = run_pilot()
        elif args.task21_select is not None:
            result = run_selection_stage(args.task21_select)
        elif args.task21_fit is not None:
            result = run_fit_stage(args.task21_fit)
        elif args.task21_calibrate is not None:
            result = run_calibration_stage(args.task21_calibrate)
        elif args.task21_confirm is not None:
            result = run_confirmation_stage(args.task21_confirm)
        else:
            result = run_preflight()
    except Exception as error:
        print(f"repaired experiment entry point failed: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
