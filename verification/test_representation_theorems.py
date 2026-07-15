"""Regression witnesses for the Task 17 representation results."""

from __future__ import annotations

import unittest

from verification.representation_theorems import (
    AffineMap,
    CPWLPlanNode,
    RobustValue,
    affine_consumer,
    balanced_relu_max,
    canonical_partition,
    dual_use_code,
    evaluate_cpwl_plan,
    factorization_collisions,
    fixed_indexed_lookup,
    ideal_upper_risk,
    jacobian_difference_rank,
    propagated_affine_error,
    relu_max,
    robust_upper_risk,
    shared_candidate_scores,
    traces_agree,
    undominated_in_evaluated_set,
)


class FactorizationTests(unittest.TestCase):
    def test_equal_code_must_preserve_wf_and_query_class(self) -> None:
        samples = (
            {"margin": 0.2, "normal": ("Well", "grant")},
            {"margin": 0.2, "normal": ("Well", "refuse")},
            {"margin": -0.1, "normal": ("Ill", "missing-tolerance")},
        )
        collisions = factorization_collisions(
            samples,
            code=lambda sample: sample["margin"],
            observation=lambda sample: sample["normal"],
        )
        self.assertEqual(collisions, ((0, 1),))
        self.assertEqual(
            factorization_collisions(
                samples,
                code=lambda sample: sample["normal"],
                observation=lambda sample: sample["normal"],
            ),
            (),
        )

    def test_canonical_quotient_is_the_observation_partition(self) -> None:
        samples = ("grant:a", "grant:b", "open:a", "grant:c")
        partition = canonical_partition(samples, lambda value: value.split(":")[0])
        self.assertEqual(partition, (frozenset({0, 1, 3}), frozenset({2})))


class RobustMarginTests(unittest.TestCase):
    def test_affine_error_propagation(self) -> None:
        self.assertAlmostEqual(
            propagated_affine_error((2.0, -3.0, 0.5), (0.1, 0.2, 0.4)),
            1.0,
        )

    def test_conservative_decoder_is_sound(self) -> None:
        threshold = 1.0
        cases = (
            (0.70, 0.75, RobustValue.SUPPORTED),
            (1.30, 1.25, RobustValue.REFUTED),
        )
        for truth, estimate, expected in cases:
            decoded = robust_upper_risk(estimate, threshold, 0.10)
            self.assertEqual(decoded, expected)
            self.assertEqual(decoded, ideal_upper_risk(truth, threshold))

    def test_inner_band_opens_and_one_sided_mode_withholds(self) -> None:
        self.assertEqual(robust_upper_risk(1.0, 1.0, 0.1), RobustValue.OPEN)
        self.assertEqual(
            robust_upper_risk(1.3, 1.0, 0.1, can_refute=False),
            RobustValue.OPEN,
        )


class CPWLAndSeamTests(unittest.TestCase):
    def test_relu_max_identities_are_exact_on_boundary_cases(self) -> None:
        for left, right in ((-2.0, -5.0), (-1.0, -1.0), (0.0, 3.0), (4.0, 2.0)):
            self.assertEqual(relu_max(left, right), max(left, right))
        self.assertEqual(balanced_relu_max((-2.0, 4.0, 1.0, 4.0, 3.0)), 4.0)

    def test_conforming_affine_traces_and_rank_one_change(self) -> None:
        left = AffineMap(((1.0, 2.0), (0.0, 1.0)), (0.0, 0.0))
        right = AffineMap(((4.0, 2.0), (-2.0, 1.0)), (0.0, 0.0))
        face = ((0.0, -2.0), (0.0, 0.0), (0.0, 3.0))
        self.assertTrue(traces_agree(left, right, face))
        self.assertEqual(jacobian_difference_rank(left, right), 1)

    def test_disagreeing_trace_is_a_hard_seam(self) -> None:
        left = AffineMap(((1.0,),), (0.0,))
        right = AffineMap(((1.0,),), (1.0,))
        self.assertFalse(traces_agree(left, right, ((0.0,),)))


class LibraryTests(unittest.TestCase):
    def test_fixed_index_has_no_new_candidate_coordinate(self) -> None:
        self.assertEqual(fixed_indexed_lookup(("old", "new"), (0.2, 0.5), "new"), 0.5)
        with self.assertRaises(KeyError):
            fixed_indexed_lookup(("old", "new"), (0.2, 0.5), "future")

    def test_shared_scoring_is_permutation_equivariant(self) -> None:
        candidates = (("old", (2.0, 1.0)), ("new", (1.0, 4.0)))
        scorer = lambda pair: pair[0] - pair[1]
        self.assertEqual(
            shared_candidate_scores(candidates, scorer),
            shared_candidate_scores(reversed(candidates), scorer),
        )

    def test_evaluated_nondomination_is_not_global(self) -> None:
        self.assertTrue(undominated_in_evaluated_set("g", ("g", "h"), ()))
        self.assertFalse(
            undominated_in_evaluated_set(
                "g", ("g", "h", "future"), (("future", "g"),)
            )
        )


class DualUseTests(unittest.TestCase):
    def test_named_surplus_is_both_grade_and_affine_feature(self) -> None:
        code = dual_use_code(
            (RobustValue.SUPPORTED, RobustValue.SUPPORTED, RobustValue.OPEN),
            (0.2, 5.0, 9.0),
            (1.0, 1.0, 1.0),
        )
        self.assertEqual(code.normalized_surplus, (0.2, 5.0, 0.0))
        self.assertEqual(affine_consumer(code, ((1.0, -1.0, 0.0),), (0.5,)), (-4.3,))

    def test_boundary_requires_exact_state_beside_relu_value(self) -> None:
        boundary = dual_use_code((RobustValue.SUPPORTED,), (0.0,), (1.0,))
        open_case = dual_use_code((RobustValue.OPEN,), (-2.0,), (1.0,))
        self.assertEqual(boundary.normalized_surplus, open_case.normalized_surplus)
        self.assertNotEqual(boundary.states, open_case.states)

    def test_normalization_makes_unit_rescaling_invariant(self) -> None:
        original = dual_use_code((RobustValue.SUPPORTED,), (2.0,), (4.0,))
        rescaled = dual_use_code((RobustValue.SUPPORTED,), (20.0,), (40.0,))
        self.assertEqual(original, rescaled)

    def test_adequacy_only_code_cannot_recover_unequal_payloads(self) -> None:
        samples = (
            {"adequacy": (RobustValue.SUPPORTED, 0.5), "payload": "cat"},
            {"adequacy": (RobustValue.SUPPORTED, 0.5), "payload": "dog"},
        )
        self.assertEqual(
            factorization_collisions(
                samples,
                code=lambda sample: sample["adequacy"],
                observation=lambda sample: sample["payload"],
            ),
            ((0, 1),),
        )


class AnnotatedPlanTests(unittest.TestCase):
    @staticmethod
    def plan() -> tuple[CPWLPlanNode, ...]:
        return (
            CPWLPlanNode("x", "input", weights=(1.0,)),
            CPWLPlanNode("minus-x", "input", weights=(-1.0,)),
            CPWLPlanNode("payload", "max", ("x", "minus-x")),
            CPWLPlanNode("grade-affine", "affine", ("payload",), (0.25,), -0.5),
            CPWLPlanNode("grade", "relu", ("grade-affine",)),
        )

    def test_finite_proof_erased_plan_jointly_computes_payload_and_grade(self) -> None:
        for point, expected in ((-3.0, (3.0, 0.25)), (0.0, (0.0, 0.0)), (4.0, (4.0, 0.5))):
            self.assertEqual(
                evaluate_cpwl_plan((point,), self.plan(), ("payload", "grade")),
                expected,
            )

    def test_plan_rejects_undeclared_non_cpwl_primitive(self) -> None:
        with self.assertRaises(ValueError):
            evaluate_cpwl_plan(
                (1.0,),
                (
                    CPWLPlanNode("x", "input", weights=(1.0,)),
                    CPWLPlanNode("bad", "multiply", ("x",)),
                ),
                ("bad",),
            )


if __name__ == "__main__":
    unittest.main()
