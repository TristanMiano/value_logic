"""Focused checks for the Task 21 frozen-result analysis."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

import numpy as np

from experiments.analyze_results import (
    _finite_row_means,
    bootstrap_means,
    centered_one_sided_p,
    holm_adjust,
)


ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "experiments" / "analysis_v1_1.json"
FIGURES = ROOT / "experiments" / "figures"


class InferencePrimitiveTests(unittest.TestCase):
    def test_world_bootstrap_is_deterministic_and_keeps_endpoints_paired(self) -> None:
        values = np.column_stack((np.arange(20, dtype=float), np.arange(20, dtype=float) + 3.0))
        first = bootstrap_means(values, replicates=200, seed=123, chunk=17)
        second = bootstrap_means(values, replicates=200, seed=123, chunk=31)
        np.testing.assert_array_equal(first, second)
        np.testing.assert_allclose(first[:, 1] - first[:, 0], 3.0)

    def test_centered_one_sided_p_distinguishes_clear_effect_from_null(self) -> None:
        tight_draws = np.linspace(0.18, 0.22, 1_000)
        self.assertLess(centered_one_sided_p(tight_draws, 0.20, 0.05), 0.01)
        self.assertGreater(centered_one_sided_p(tight_draws, 0.20, 0.20), 0.45)

    def test_holm_adjustment_is_step_down_and_familywise(self) -> None:
        adjusted = holm_adjust({"a": 0.01, "b": 0.03, "c": 0.20})
        self.assertAlmostEqual(adjusted["a"]["adjusted_p"], 0.03)
        self.assertAlmostEqual(adjusted["b"]["adjusted_p"], 0.06)
        self.assertAlmostEqual(adjusted["c"]["adjusted_p"], 0.20)
        self.assertTrue(adjusted["a"]["reject"])
        self.assertFalse(adjusted["b"]["reject"])

    def test_finite_row_means_preserve_wholly_missing_worlds(self) -> None:
        values = np.asarray([[1.0, np.nan, 3.0], [np.nan, np.nan, np.nan]])
        means = _finite_row_means(values)
        self.assertEqual(means[0], 2.0)
        self.assertTrue(np.isnan(means[1]))


class FrozenAnalysisArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.analysis = json.loads(ANALYSIS.read_text(encoding="utf-8"))

    def test_minimum_claim_dispositions_are_recorded(self) -> None:
        self.assertEqual(
            self.analysis["minimum_core"]["F35"]["disposition"],
            "mixed_or_inconclusive",
        )
        self.assertEqual(
            self.analysis["minimum_core"]["F36"]["disposition"],
            "supported",
        )

    def test_exact_inactive_selection_check_passed(self) -> None:
        safety = self.analysis["exact_safety_checks"]
        self.assertTrue(safety["inactive_selection_exactly_zero"])
        self.assertEqual(safety["maximum_inactive_selection_rate"], 0.0)

    def test_registered_figures_exist(self) -> None:
        expected = {
            "primary_endpoints_v1_1.png",
            "coverage_v1_1.png",
            "ablations_v1_1.png",
        }
        self.assertEqual(expected, {path.name for path in FIGURES.glob("*_v1_1.png")})


if __name__ == "__main__":
    unittest.main()
