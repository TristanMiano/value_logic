"""Regression witnesses for the Task 16 hybrid ReLU semantic boundary."""

from __future__ import annotations

from dataclasses import replace
import unittest

from verification.kernel import AtomValue
from verification.relu_architecture import (
    CandidateRoute,
    CertifiedEnvelope,
    EvidenceGate,
    HypothesisChannelSpec,
    StatisticProposal,
    decode_improvement_margin,
    decode_upper_risk,
    dual_use_feature,
    naive_relu_path,
    select_from_active,
    signed_relu,
    validate_hypothesis_registry,
)


def proposal(center: float, half_width: float = 0.0, error: float = 0.0) -> CertifiedEnvelope:
    return CertifiedEnvelope(StatisticProposal(center, half_width, 0.25), error)


def gate(**changes: object) -> EvidenceGate:
    base = EvidenceGate(
        certificate_id="cert:risk",
        checker_id="interval-checker",
        checker_version="2",
        calibration_id="heldout-calibration",
        calibration_version="4",
        provenance=("record:risk", "record:calibration"),
    )
    return replace(base, **changes)


class MarginChannelTests(unittest.TestCase):
    def test_paired_relu_recovers_signed_margin(self) -> None:
        for margin in (-3.0, 0.0, 2.5):
            positive, negative = signed_relu(margin)
            self.assertEqual(positive - negative, margin)

    def test_inclusive_boundary_is_supported_with_zero_activation(self) -> None:
        channels = decode_upper_risk(
            "adequacy",
            proposal(1.0),
            1.0,
            gate(),
            normalization_scale=1.0,
        )
        self.assertEqual(channels.diagnostic.value, AtomValue.SUPPORTED)
        self.assertEqual(channels.support_margin, 0.0)
        self.assertEqual(channels.positive_surplus, 0.0)

    def test_certified_error_radius_creates_conservative_open_band(self) -> None:
        point = decode_upper_risk(
            "adequacy",
            proposal(0.9),
            1.0,
            gate(),
            normalization_scale=1.0,
        )
        band = decode_upper_risk(
            "adequacy",
            proposal(0.9, error=0.2),
            1.0,
            gate(),
            normalization_scale=1.0,
        )
        self.assertEqual(point.diagnostic.value, AtomValue.SUPPORTED)
        self.assertEqual(band.diagnostic.value, AtomValue.OPEN)

    def test_two_sided_envelope_can_refute_above_threshold(self) -> None:
        channels = decode_upper_risk(
            "adequacy",
            proposal(1.5, half_width=0.1, error=0.1),
            1.0,
            gate(),
            normalization_scale=0.5,
        )
        self.assertEqual(channels.diagnostic.value, AtomValue.REFUTED)
        self.assertGreater(channels.refutation_margin or 0.0, 0.0)
        self.assertEqual(channels.positive_surplus, 0.0)

    def test_one_sided_support_mode_cannot_manufacture_refutation(self) -> None:
        channels = decode_upper_risk(
            "adequacy",
            proposal(1.5),
            1.0,
            gate(can_refute=False),
            normalization_scale=1.0,
        )
        self.assertEqual(channels.diagnostic.value, AtomValue.OPEN)
        self.assertEqual(channels.diagnostic.obstacles, ("CertificateModeCannotRefute",))

    def test_invalid_states_override_a_favorable_learned_margin(self) -> None:
        variants = (
            (gate(present=False), "MissingStatisticEvidence"),
            (gate(current=False), "ExpiredStatisticEvidence"),
            (gate(conflict=True), "EvidenceConflict"),
            (gate(checker_accepted=False), "EnvelopeCheckerRejected"),
            (gate(calibration_accepted=False), "UncalibratedStatistic"),
            (gate(learned_reject=True), "LearnedValidityReject"),
        )
        for evidence, obstacle in variants:
            with self.subTest(obstacle=obstacle):
                channels = decode_upper_risk(
                    "adequacy",
                    proposal(0.1),
                    1.0,
                    evidence,
                    normalization_scale=1.0,
                )
                self.assertEqual(channels.diagnostic.value, AtomValue.OPEN)
                self.assertEqual(channels.diagnostic.obstacles, (obstacle,))
                self.assertEqual(channels.positive_surplus, 0.0)

    def test_improvement_uses_both_candidate_and_fallback_envelopes(self) -> None:
        channels = decode_improvement_margin(
            "improvement",
            proposal(0.5, error=0.05),
            proposal(1.0, error=0.05),
            0.2,
            gate(),
            replace(gate(), certificate_id="cert:fallback"),
            normalization_scale=0.1,
        )
        self.assertEqual(channels.diagnostic.value, AtomValue.SUPPORTED)
        self.assertAlmostEqual(channels.support_margin or 0.0, 0.2)
        self.assertAlmostEqual(channels.positive_surplus, 2.0)


class DualUseRegistryTests(unittest.TestCase):
    @staticmethod
    def spec(hypothesis: str, *, normalization_id: str = "sigma-units") -> HypothesisChannelSpec:
        return HypothesisChannelSpec(
            hypothesis=hypothesis,
            atom_address=f"adequacy:{hypothesis}",
            domain="image-domain:v1",
            normalization_id=normalization_id,
            normalization_scale=0.5,
            calibration_ref="calibration:image:v3",
            consumer_context="multilabel-image-head:v1",
            downstream_consumers=("next-feature-layer", "masked-label-selector"),
        )

    def test_named_supported_margin_is_a_dual_use_feature(self) -> None:
        spec = self.spec("person")
        validate_hypothesis_registry((spec, self.spec("child")))
        channels = decode_upper_risk(
            spec.atom_address,
            proposal(0.5),
            1.0,
            gate(),
            normalization_scale=0.5,
        )
        feature = dual_use_feature(spec, channels)
        self.assertTrue(feature.supported_bit)
        self.assertEqual(feature.positive_surplus, 1.0)

    def test_incomparable_channel_normalizations_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "normalization"):
            validate_hypothesis_registry(
                (self.spec("person"), self.spec("child", normalization_id="raw-loss-units"))
            )


class SelectionBoundaryTests(unittest.TestCase):
    def test_inactive_high_score_cannot_be_selected(self) -> None:
        result = select_from_active(
            (
                CandidateRoute("licensed", True, 1.0, {"prediction": "cat"}),
                CandidateRoute("unlicensed", False, 1000.0, {"prediction": "dog"}),
            ),
            fallback_id="abstain",
            fallback_payload={"prediction": "unknown"},
        )
        self.assertEqual(result.selected_id, "licensed")
        self.assertEqual(result.payload, {"prediction": "cat"})

    def test_empty_active_set_uses_unscaled_fallback_payload(self) -> None:
        fallback = {"prediction": "unknown", "action": "defer"}
        result = select_from_active(
            (CandidateRoute("candidate", False, 100.0, {"prediction": "cat"}),),
            fallback_id="status-quo",
            fallback_payload=fallback,
        )
        self.assertTrue(result.used_fallback)
        self.assertEqual(result.payload, fallback)

    def test_selection_tie_requires_an_explicit_rule(self) -> None:
        candidates = (
            CandidateRoute("a", True, 1.0, "payload-a"),
            CandidateRoute("b", True, 1.0, "payload-b"),
        )
        with self.assertRaisesRegex(ValueError, "priority"):
            select_from_active(candidates, fallback_id="f", fallback_payload="fallback")
        result = select_from_active(
            candidates,
            fallback_id="f",
            fallback_payload="fallback",
            tie_priority={"a": 2, "b": 1},
        )
        self.assertEqual(result.selected_id, "b")

    def test_relu_zero_alone_does_not_quarantine_downstream_output(self) -> None:
        output = naive_relu_path(
            -10.0,
            outgoing_weight=3.0,
            downstream_bias=2.0,
            bypass=5.0,
        )
        self.assertEqual(output, 7.0)


if __name__ == "__main__":
    unittest.main()
