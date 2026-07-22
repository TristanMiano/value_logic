"""Regression witnesses for the Task 22B policy/value bridge."""

from __future__ import annotations

import unittest

from verification.policy_value_reconstruction import (
    ArgmaxDecoder,
    FiniteDistribution,
    FinitePolicy,
    ValueDecisionHarness,
    canonical_score_encoding,
    certified_event_mass_risk_bound,
    conservative_decode_state,
    coordinate_error,
    coordinate_gap_radius,
    iid_disagreement_upper_bound,
    is_in_canonical_encoder_image,
    modal_action,
    oracle_reconstruction_bound,
    policy_action_gap,
    total_variation,
    trajectory_divergence_union_bound,
)


class CanonicalRoundTripTests(unittest.TestCase):
    def setUp(self) -> None:
        self.decoder = ArgmaxDecoder(
            "decoder-v1",
            {"x": ("a", "b"), "forced": ("stay",)},
            {"x": ("b", "a"), "forced": ("stay",)},
        )
        self.policy = FinitePolicy(
            "policy-v3", "decoder-v1", {"x": "a", "forced": "stay"}
        )

    def test_policy_round_trip_is_exact_and_forced_gap_is_safe(self) -> None:
        encoded = canonical_score_encoding(self.policy, self.decoder)
        self.assertEqual(self.decoder.decode(encoded), dict(self.policy.choices))
        self.assertTrue(is_in_canonical_encoder_image(encoded, self.decoder))

        result = oracle_reconstruction_bound(
            self.policy,
            encoded,
            encoded,
            self.decoder,
            FiniteDistribution("all-states", "mu-v1", {"x": 0.6, "forced": 0.4}),
            rho=0.49,
        )
        self.assertEqual(result.disagreement, 0.0)
        self.assertEqual(result.small_gap_event_mass, 0.0)

    def test_reverse_composite_is_identity_only_on_encoder_image(self) -> None:
        off_image = {"x": {"a": 8.0, "b": -3.0}, "forced": {"stay": 4.0}}
        self.assertEqual(self.decoder.decode(off_image), dict(self.policy.choices))
        self.assertFalse(is_in_canonical_encoder_image(off_image, self.decoder))
        self.assertNotEqual(canonical_score_encoding(self.policy, self.decoder), off_image)

    def test_version_mismatch_is_rejected(self) -> None:
        wrong = FinitePolicy("policy-v3", "decoder-v0", self.policy.choices)
        with self.assertRaises(ValueError):
            canonical_score_encoding(wrong, self.decoder)


class OracleBoundTests(unittest.TestCase):
    def test_disagreement_is_covered_by_error_or_small_gap_mass(self) -> None:
        decoder = ArgmaxDecoder(
            "d1",
            {"safe": ("a", "b"), "tie": ("a", "b"), "forced": ("z",)},
            {"safe": ("a", "b"), "tie": ("a", "b"), "forced": ("z",)},
        )
        policy = FinitePolicy(
            "p1", "d1", {"safe": "a", "tie": "a", "forced": "z"}
        )
        intended = {
            "safe": {"a": 1.0, "b": 0.0},
            "tie": {"a": 0.0, "b": 0.0},
            "forced": {"z": -20.0},
        }
        approximate = {
            "safe": {"a": 0.95, "b": 0.05},
            "tie": {"a": 0.0, "b": 0.01},
            "forced": {"z": 100.0},
        }
        distribution = FiniteDistribution(
            "deployment", "mu-2026-07", {"safe": 0.5, "tie": 0.3, "forced": 0.2}
        )
        result = oracle_reconstruction_bound(
            policy, intended, approximate, decoder, distribution, rho=0.1
        )
        self.assertAlmostEqual(result.disagreement, 0.3)
        self.assertAlmostEqual(result.error_event_mass, 0.2)
        self.assertAlmostEqual(result.small_gap_event_mass, 0.3)
        self.assertLessEqual(result.disagreement, result.union_upper_bound)
        self.assertAlmostEqual(certified_event_mass_risk_bound(0.2, 0.3), 0.5)

    def test_factor_two_is_tight_at_a_tie_and_below_it_at_a_flip(self) -> None:
        decoder = ArgmaxDecoder(
            "d-tight", {"x": ("a", "b")}, {"x": ("b", "a")}
        )
        policy = FinitePolicy("p-tight", "d-tight", {"x": "a"})
        distribution = FiniteDistribution("point", "mu1", {"x": 1.0})

        tied = oracle_reconstruction_bound(
            policy,
            {"x": {"a": 2.0, "b": 0.0}},
            {"x": {"a": 1.0, "b": 1.0}},
            decoder,
            distribution,
            rho=1.0,
        )
        self.assertEqual(tied.disagreement, 1.0)
        self.assertEqual(tied.error_event_mass, 0.0)
        self.assertEqual(tied.small_gap_event_mass, 1.0)

        flipped = oracle_reconstruction_bound(
            policy,
            {"x": {"a": 1.9, "b": 0.0}},
            {"x": {"a": 0.9, "b": 1.0}},
            decoder,
            distribution,
            rho=1.0,
        )
        self.assertEqual(flipped.disagreement, 1.0)
        self.assertEqual(flipped.error_event_mass, 0.0)
        self.assertEqual(flipped.small_gap_event_mass, 1.0)

    def test_large_error_event_covers_a_large_gap_flip(self) -> None:
        decoder = ArgmaxDecoder("d", {"x": (0, 1)}, {"x": (0, 1)})
        policy = FinitePolicy("p", "d", {"x": 0})
        result = oracle_reconstruction_bound(
            policy,
            {"x": {0: 1.0, 1: 0.0}},
            {"x": {0: -0.1, 1: 0.1}},
            decoder,
            FiniteDistribution("point", "mu", {"x": 1.0}),
            rho=0.1,
        )
        self.assertEqual(result.error_event_mass, 1.0)
        self.assertEqual(result.small_gap_event_mass, 0.0)
        self.assertEqual(result.disagreement, 1.0)


class ConservativeCertificateTests(unittest.TestCase):
    def test_coordinate_radius_gives_pairwise_radius_and_strict_certificate(self) -> None:
        decoder = ArgmaxDecoder("d", {"x": ("a", "b")}, {"x": ("a", "b")})
        policy = FinitePolicy("p", "d", {"x": "a"})
        rho = 0.1
        self.assertAlmostEqual(coordinate_gap_radius(rho), 0.2)

        truth_above = {"x": {"a": 0.41, "b": 0.0}}
        above_four_rho = {"x": {"a": 0.31, "b": 0.10}}
        self.assertAlmostEqual(
            coordinate_error(truth_above, above_four_rho, decoder, "x"), rho
        )
        self.assertGreater(policy_action_gap(policy, truth_above, decoder, "x"), 4 * rho)
        self.assertEqual(
            conservative_decode_state(
                above_four_rho, decoder, "x", coordinate_gap_radius(rho)
            ),
            "a",
        )

        truth_at = {"x": {"a": 0.40, "b": 0.0}}
        at_four_rho = {"x": {"a": 0.30, "b": 0.10}}
        self.assertAlmostEqual(
            coordinate_error(truth_at, at_four_rho, decoder, "x"), rho
        )
        self.assertAlmostEqual(policy_action_gap(policy, truth_at, decoder, "x"), 4 * rho)
        self.assertIsNone(
            conservative_decode_state(
                at_four_rho, decoder, "x", coordinate_gap_radius(rho)
            )
        )

    def test_direct_gap_certificate_can_use_its_own_smaller_radius(self) -> None:
        decoder = ArgmaxDecoder("d", {"x": ("a", "b")}, {"x": ("a", "b")})
        scores = {"x": {"a": 0.20, "b": 0.10}}
        self.assertEqual(conservative_decode_state(scores, decoder, "x", 0.05), "a")
        self.assertIsNone(conservative_decode_state(scores, decoder, "x", 0.10))


class SemanticVariantTests(unittest.TestCase):
    def test_suboptimal_policy_is_not_a_q_round_trip_fixed_point(self) -> None:
        decoder = ArgmaxDecoder("q-d", {"s": ("low", "high")}, {"s": ("low", "high")})
        source = FinitePolicy("suboptimal", "q-d", {"s": "low"})
        q_pi = {"s": {"low": 0.0, "high": 1.0}}
        self.assertEqual(decoder.decode(q_pi), {"s": "high"})
        with self.assertRaisesRegex(ValueError, "intended policy action must win"):
            oracle_reconstruction_bound(
                source,
                q_pi,
                q_pi,
                decoder,
                FiniteDistribution("point", "mu", {"s": 1.0}),
                rho=0.0,
            )

        self_greedy = FinitePolicy("self-greedy", "q-d", {"s": "high"})
        fixed_point = oracle_reconstruction_bound(
            self_greedy,
            q_pi,
            q_pi,
            decoder,
            FiniteDistribution("point", "mu", {"s": 1.0}),
            rho=0.0,
        )
        self.assertEqual(fixed_point.disagreement, 0.0)

    def test_scalar_value_error_propagates_through_declared_harness(self) -> None:
        decoder = ArgmaxDecoder("v-d", {"s": ("left", "right")}, {"s": ("left", "right")})
        harness = ValueDecisionHarness(
            "h-v2",
            decoder,
            {
                ("s", "left"): (("left-terminal", 1.0),),
                ("s", "right"): (("right-terminal", 1.0),),
            },
            {("s", "left"): 0.2, ("s", "right"): 0.1},
            0.9,
            {"s": 1},
        )
        truth = harness.action_scores({"left-terminal": 1.0, "right-terminal": 0.0})
        estimate = harness.action_scores({"left-terminal": 0.9, "right-terminal": 0.1})
        envelope = harness.score_error_envelope(
            {"left-terminal": 0.1, "right-terminal": 0.1}
        )
        self.assertAlmostEqual(abs(truth["s"]["left"] - estimate["s"]["left"]), 0.09)
        self.assertAlmostEqual(abs(truth["s"]["right"] - estimate["s"]["right"]), 0.09)
        self.assertAlmostEqual(envelope["s"]["left"], 0.09)
        self.assertAlmostEqual(envelope["s"]["right"], 0.09)
        self.assertEqual(decoder.decode(truth), {"s": "left"})
        self.assertEqual(decoder.decode(estimate), {"s": "left"})

    def test_modal_agreement_does_not_establish_distributional_fidelity(self) -> None:
        left = {"a": 0.51, "b": 0.49}
        right = {"a": 0.99, "b": 0.01}
        self.assertEqual(modal_action(left, ("a", "b")), "a")
        self.assertEqual(modal_action(right, ("a", "b")), "a")
        self.assertAlmostEqual(total_variation(left, right), 0.48)


class ScopeCountermodelTests(unittest.TestCase):
    def test_training_equality_allows_arbitrary_off_support_disagreement(self) -> None:
        decoder = ArgmaxDecoder(
            "d", {"train": (0, 1), "deploy": (0, 1)}, {"train": (0, 1), "deploy": (0, 1)}
        )
        policy = FinitePolicy("p", "d", {"train": 0, "deploy": 0})
        intended = canonical_score_encoding(policy, decoder)
        approximate = {"train": {0: 1.0, 1: 0.0}, "deploy": {0: 0.0, 1: 1.0}}
        train = oracle_reconstruction_bound(
            policy,
            intended,
            approximate,
            decoder,
            FiniteDistribution("train", "mu-train", {"train": 1.0}),
            rho=0.0,
        )
        deploy = oracle_reconstruction_bound(
            policy,
            intended,
            approximate,
            decoder,
            FiniteDistribution("deploy", "mu-deploy", {"deploy": 1.0}),
            rho=0.0,
        )
        self.assertEqual(train.disagreement, 0.0)
        self.assertEqual(deploy.disagreement, 1.0)

    def test_hidden_policy_lookup_makes_a_scalar_value_claim_vacuous(self) -> None:
        hidden_policy = {"s": "a"}

        def opaque_harness(_value: float, state: str) -> str:
            return hidden_policy[state]

        self.assertEqual(opaque_harness(-1000.0, "s"), "a")
        self.assertEqual(opaque_harness(1000.0, "s"), "a")

    def test_state_aliasing_blocks_state_only_reconstruction(self) -> None:
        histories = (("visible-x", "left-history"), ("visible-x", "right-history"))
        required_actions = {histories[0]: "a", histories[1]: "b"}
        state_only_choice = {"visible-x": "a"}
        recovered = tuple(state_only_choice[visible] for visible, _ in histories)
        target = tuple(required_actions[history] for history in histories)
        self.assertNotEqual(recovered, target)

    def test_iid_and_trajectory_bounds_have_different_premises(self) -> None:
        held_out = iid_disagreement_upper_bound(5, 100, 0.05)
        self.assertGreater(held_out, 0.05)
        self.assertLess(held_out, 0.2)
        self.assertAlmostEqual(trajectory_divergence_union_bound((0.02,) * 5), 0.1)
        self.assertEqual(trajectory_divergence_union_bound((0.4, 0.4, 0.4)), 1.0)


if __name__ == "__main__":
    unittest.main()
