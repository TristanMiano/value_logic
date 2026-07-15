"""Regression witnesses for the Task 18 loss and calibration choices."""

from __future__ import annotations

from math import isinf
import unittest

from verification.kernel import AtomValue, Outcome
from verification.losses import (
    RouterPair,
    StatisticExample,
    atom_cross_entropy,
    decode_upper_region,
    derive_public_outcome,
    expand_interval,
    interval_score,
    normalized_positive_surplus,
    pairwise_router_loss,
    proposed_calibration_radius,
    residual_nonconformity,
    selective_metrics,
    structured_statistic_loss,
    validate_disjoint_splits,
    weighted_binary_cross_entropy,
)


class StructuredStatisticLossTests(unittest.TestCase):
    def test_interval_score_penalizes_width_and_misses(self) -> None:
        self.assertEqual(interval_score(1.0, 1.0, 1.0, 0.1), 0.0)
        self.assertEqual(interval_score(1.0, 0.5, 1.5, 0.1), 1.0)
        self.assertGreater(interval_score(2.0, 0.5, 1.5, 0.1), 1.0)

    def test_missing_target_is_masked_not_imputed_as_zero(self) -> None:
        records = (
            StatisticExample("observed", "risk", "source:1", 2.0, 2.0, 0.0, 1.0),
            StatisticExample("missing", "risk", "source:missing", None, 100.0, 0.0, 1.0),
        )
        loss = structured_statistic_loss(records, miscoverage=0.1)
        self.assertEqual(loss.total, 0.0)
        self.assertEqual(loss.included_examples, 1)

    def test_schema_balancing_prevents_frequency_only_dominance(self) -> None:
        records = (
            StatisticExample("a1", "frequent", "s1", 0.0, 1.0, 0.0, 1.0),
            StatisticExample("a2", "frequent", "s2", 0.0, 1.0, 0.0, 1.0),
            StatisticExample("b", "rare", "s3", 0.0, 3.0, 0.0, 1.0),
        )
        loss = structured_statistic_loss(
            records, miscoverage=0.5, interval_weight=0.0
        )
        self.assertEqual(loss.center, 5.0)
        self.assertEqual(loss.included_schemas, 2)

    def test_standardized_objective_is_covariant_under_unit_change(self) -> None:
        base = StatisticExample("a", "risk", "s", 2.0, 1.5, 0.2, 0.5)
        rescaled = StatisticExample("a", "risk", "s", 20.0, 15.0, 2.0, 5.0)
        left = structured_statistic_loss((base,), miscoverage=0.2)
        right = structured_statistic_loss((rescaled,), miscoverage=0.2)
        self.assertAlmostEqual(left.total, right.total)


class CalibrationAndDecodingTests(unittest.TestCase):
    def test_residual_quantile_and_expansion(self) -> None:
        residuals = tuple(
            residual_nonconformity(target, lower, upper)
            for target, lower, upper in (
                (1.0, 0.9, 1.1),
                (1.3, 0.9, 1.1),
                (0.6, 0.9, 1.1),
                (1.5, 0.9, 1.1),
            )
        )
        proposal = proposed_calibration_radius(residuals, 0.4)
        self.assertEqual(proposal.rank, 3)
        self.assertAlmostEqual(proposal.radius, 0.3)
        lower, upper = expand_interval(0.9, 1.1, proposal.radius)
        self.assertAlmostEqual(lower, 0.6)
        self.assertAlmostEqual(upper, 1.4)

    def test_too_little_calibration_data_returns_unbounded_proposal(self) -> None:
        proposal = proposed_calibration_radius((0.1, 0.2, 0.3), 0.1)
        self.assertTrue(isinf(proposal.radius))

    def test_decoder_preserves_boundary_polarity_and_validity(self) -> None:
        self.assertIs(
            decode_upper_region(0.8, 1.0, 1.0, evidence_usable=True),
            AtomValue.SUPPORTED,
        )
        self.assertIs(
            decode_upper_region(1.0, 1.2, 1.0, evidence_usable=True),
            AtomValue.OPEN,
        )
        self.assertIs(
            decode_upper_region(1.1, 1.2, 1.0, evidence_usable=True),
            AtomValue.REFUTED,
        )
        self.assertIs(
            decode_upper_region(1.1, 1.2, 1.0, evidence_usable=False),
            AtomValue.OPEN,
        )

    def test_public_outcome_is_symbolic(self) -> None:
        self.assertIs(
            derive_public_outcome(
                well_formed=True,
                required_atom_values=(AtomValue.SUPPORTED, AtomValue.SUPPORTED),
            ),
            Outcome.GRANTED,
        )
        self.assertIs(
            derive_public_outcome(
                well_formed=True,
                required_atom_values=(AtomValue.SUPPORTED, AtomValue.OPEN),
            ),
            Outcome.WITHHELD,
        )
        self.assertIs(
            derive_public_outcome(
                well_formed=False,
                required_atom_values=(AtomValue.SUPPORTED,),
            ),
            Outcome.UNDEFINED,
        )


class AuxiliaryAndRouterTests(unittest.TestCase):
    def test_cross_entropy_is_independent_per_atom(self) -> None:
        correct = atom_cross_entropy(
            {
                AtomValue.SUPPORTED: 4.0,
                AtomValue.OPEN: 0.0,
                AtomValue.REFUTED: -1.0,
            },
            AtomValue.SUPPORTED,
        )
        incorrect = atom_cross_entropy(
            {
                AtomValue.SUPPORTED: -1.0,
                AtomValue.OPEN: 0.0,
                AtomValue.REFUTED: 4.0,
            },
            AtomValue.SUPPORTED,
        )
        self.assertLess(correct, incorrect)

    def test_weighted_validity_loss_can_prioritize_missed_rejects(self) -> None:
        ordinary = weighted_binary_cross_entropy(True, 0.2)
        conservative = weighted_binary_cross_entropy(True, 0.2, reject_weight=5.0)
        self.assertAlmostEqual(conservative, 5.0 * ordinary)

    def test_router_loss_ignores_inactive_and_unresolved_pairs(self) -> None:
        good = RouterPair(3.0, 1.0, 0.1, 0.5)
        bad = RouterPair(1.0, 3.0, 0.1, 0.5)
        ignored_inactive = RouterPair(100.0, -100.0, 1.0, 0.0, left_active=False)
        ignored_unknown = RouterPair(100.0, -100.0, 1.0, 0.0, comparison_resolved=False)
        good_loss = pairwise_router_loss((good, ignored_inactive, ignored_unknown))
        bad_loss = pairwise_router_loss((bad,))
        self.assertEqual(good_loss.included, 1)
        self.assertLess(good_loss.value, bad_loss.value)

    def test_selective_metrics_report_fallback_instead_of_free_rejection(self) -> None:
        metrics = selective_metrics(
            selected_losses=(0.1, 0.9, 0.2, 0.8),
            accepted=(True, False, True, False),
            fallback_losses=(0.4, 0.4, 0.4, 0.4),
        )
        self.assertEqual(metrics.coverage, 0.5)
        self.assertAlmostEqual(metrics.selective_risk, 0.15)
        self.assertAlmostEqual(metrics.deployed_risk, 0.275)
        empty = selective_metrics((0.1,), (False,), (0.7,))
        self.assertIsNone(empty.selective_risk)
        self.assertEqual(empty.deployed_risk, 0.7)

    def test_dual_use_surplus_is_scale_covariant_and_symbolically_gated(self) -> None:
        self.assertEqual(
            normalized_positive_surplus(2.0, 4.0, supported=True),
            normalized_positive_surplus(20.0, 40.0, supported=True),
        )
        self.assertEqual(
            normalized_positive_surplus(20.0, 40.0, supported=False),
            0.0,
        )

    def test_train_calibration_test_splits_must_be_disjoint(self) -> None:
        validate_disjoint_splits(("train",), ("cal",), ("test",))
        with self.assertRaises(ValueError):
            validate_disjoint_splits(("same",), ("same",), ("test",))


if __name__ == "__main__":
    unittest.main()
