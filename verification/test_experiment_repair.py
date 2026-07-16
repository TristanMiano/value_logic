"""Differential and guard tests for the Task 20R execution-only repair."""

from __future__ import annotations

import shutil
import unittest

import numpy as np

from experiments.cpp_kernel import (
    KernelInputs,
    assert_kernel_equivalence,
    built_cpp_kernel,
    numpy_decode_block,
)
from experiments.implementation import FEATURE_NAMES, calibrate_structured
from experiments.learner import (
    ReluMLP,
    initialize_paired,
    matched_architectures,
    model_parameter_hash,
)
from experiments.protocol import Role
from experiments.repaired_evaluator import (
    assert_evaluation_equivalence,
    assert_fast_adapter_equivalence,
    assert_training_adapter_equivalence,
    calibrate_structured_pair,
    evaluate_model_on_block,
    materialize_training_panel_fast,
    prepare_evaluation_block,
)
from experiments.run_experiment import _evaluate_one_world_seed
from experiments.run_repaired_experiment import (
    run_confirmation_stage,
    run_selection_stage,
    verify_repaired_sources,
)


class DataAdapterTests(unittest.TestCase):
    def test_fast_training_projection_matches_frozen_object_path(self) -> None:
        assert_training_adapter_equivalence(worlds=2)

    def test_all_evaluation_feature_panels_match_frozen_object_path(self) -> None:
        assert_fast_adapter_equivalence(worlds=2)

    def test_one_prediction_builds_same_two_calibration_bundles(self) -> None:
        panel = materialize_training_panel_fast(Role.PILOT, 0, 16)
        spec, _ = matched_architectures(len(FEATURE_NAMES), 12_000)
        model = ReluMLP(spec.input_dim, spec.hidden_width, spec.output_dim)
        initialize_paired(model, spec, 101)
        common = {
            "scorer_parameter_hash": model_parameter_hash(model),
            "training_manifest_hash": "repair-test-train",
            "calibration_manifest_hash": "repair-test-calibration",
        }
        repaired = calibrate_structured_pair(model, panel, **common)
        frozen = (
            calibrate_structured(model, panel, **common),
            calibrate_structured(model, panel, center_only=True, **common),
        )
        self.assertEqual(repaired, frozen)


@unittest.skipUnless(shutil.which("cmake"), "CMake is required for the native kernel")
class NativeKernelTests(unittest.TestCase):
    def test_cpp_matches_numpy_on_random_block(self) -> None:
        rng = np.random.default_rng(20_026_071_5)
        rows = 1_000
        inputs = KernelInputs(
            rng.normal(size=(rows, 4)).astype(np.float32),
            rng.normal(size=(rows, 3)).astype(np.float32),
            rng.integers(0, 2, rows, dtype=np.int8),
            rng.normal(size=rows),
            rng.integers(0, 2, rows, dtype=np.uint8),
            rng.integers(0, 2, rows, dtype=np.uint8),
            rng.integers(0, 2, rows, dtype=np.uint8),
            rng.integers(0, 2, rows, dtype=np.uint8),
            rng.random(rows),
            rng.random(rows),
            rng.integers(0, 2, rows, dtype=np.uint8),
            rng.integers(0, 2, rows, dtype=np.uint8),
        )
        assert_kernel_equivalence(
            numpy_decode_block(inputs),
            built_cpp_kernel().decode(inputs),
        )

    def test_repaired_world_result_matches_frozen_evaluator(self) -> None:
        calibration_panel = materialize_training_panel_fast(Role.PILOT, 0, 256)
        structured_spec, ce_spec = matched_architectures(len(FEATURE_NAMES), 12_000)
        structured = ReluMLP(
            structured_spec.input_dim,
            structured_spec.hidden_width,
            structured_spec.output_dim,
        )
        ce = ReluMLP(ce_spec.input_dim, ce_spec.hidden_width, ce_spec.output_dim)
        initialize_paired(structured, structured_spec, 101)
        initialize_paired(ce, ce_spec, 101)
        parameter_hash = model_parameter_hash(structured)
        calibrations = calibrate_structured_pair(
            structured,
            calibration_panel,
            scorer_parameter_hash=parameter_hash,
            training_manifest_hash="repair-test-train",
            calibration_manifest_hash="repair-test-calibration",
        )
        world_index = 7
        block = prepare_evaluation_block(Role.PILOT, world_index, 1)
        repaired = evaluate_model_on_block(
            block,
            structured,
            ce,
            parameter_hash,
            calibrations[0],
            calibrations[1],
            built_cpp_kernel(),
            fit_seed=101,
        )
        frozen_metrics, frozen_trace = _evaluate_one_world_seed(
            world_index,
            structured,
            ce,
            parameter_hash,
            calibrations[0],
            calibrations[1],
            role=Role.PILOT,
        )
        assert_evaluation_equivalence(
            frozen_metrics,
            frozen_trace,
            repaired.metrics[0],
            repaired.traces[0],
        )


class StageGuardTests(unittest.TestCase):
    def test_v1_1_contract_hashes_are_current(self) -> None:
        contract = verify_repaired_sources()
        self.assertEqual(contract["implementation_version"], "value-logic-implementation-v1.1.0")

    def test_production_and_final_stages_require_distinct_exact_tokens(self) -> None:
        with self.assertRaises(PermissionError):
            run_selection_stage("wrong-stage-token")
        with self.assertRaises(PermissionError):
            run_confirmation_stage("wrong-final-token")


if __name__ == "__main__":
    unittest.main()
