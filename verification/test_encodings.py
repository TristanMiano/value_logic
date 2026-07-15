"""Regression witnesses for the Task 15 architecture-neutral encodings."""

from __future__ import annotations

import unittest

from verification.encodings import (
    AtomAddress,
    TypedPlanDAG,
    TypedPlanNode,
    candidate_conditioned_scores,
    comparison_counts,
    dependency_input,
    plan_isomorphism_holds,
    sufficiency_violations,
)
from verification.footprints import key, region_footprint


class DependencyEncodingTests(unittest.TestCase):
    def test_projection_ignores_outside_records_and_exposes_missingness(self) -> None:
        address = AtomAddress("Adeq", "plan-a", "domain-a", "risk", "empirical")
        footprint = region_footprint("adequacy-a", "empirical", ("cert-1",))
        base = {
            record_key: f"value:{record_key.namespace}"
            for record_key in footprint
            if record_key.namespace != "region"
        }
        first = dependency_input(
            address,
            base,
            footprint,
            opaque_namespaces=("certificate", "verifier"),
        )
        changed_outside = dict(base)
        changed_outside[key("unrelated", "record")] = "new"
        second = dependency_input(
            address,
            changed_outside,
            footprint,
            opaque_namespaces=("certificate", "verifier"),
        )
        self.assertEqual(first, second)
        self.assertEqual(first.missing, (key("region", "cert-1", "adequacy-a"),))
        self.assertEqual(
            {record_key.namespace for record_key, _ in first.opaque_handles},
            {"certificate", "verifier"},
        )

    def test_changing_a_read_value_changes_the_input(self) -> None:
        address = AtomAddress("Trace", "plan-a", "domain-a", "trace", "formal")
        footprint = {key("verifier", "formal")}
        old = dependency_input(address, {key("verifier", "formal"): "v1"}, footprint)
        new = dependency_input(address, {key("verifier", "formal"): "v2"}, footprint)
        self.assertNotEqual(old, new)


class LibraryEncodingTests(unittest.TestCase):
    def test_shared_candidate_scores_are_permutation_equivariant(self) -> None:
        candidates = (("newton", (2.0, 1.0)), ("relativity", (1.0, 4.0)))
        scorer = lambda values: values[0] - values[1]
        forward = candidate_conditioned_scores(candidates, scorer)
        reverse = candidate_conditioned_scores(reversed(candidates), scorer)
        self.assertEqual(forward, reverse)

    def test_sparse_comparison_count_does_not_claim_dense_resolution(self) -> None:
        dense, sparse = comparison_counts(
            ("a", "b", "c", "d"),
            (("a", "b"), ("a", "c"), ("d", "a")),
        )
        self.assertEqual(dense, 12)
        self.assertEqual(sparse, 3)


class PlanEncodingTests(unittest.TestCase):
    @staticmethod
    def plan(prefix: str, *, root_checker: str = "grade-checker") -> TypedPlanDAG:
        leaf = TypedPlanNode(
            name=f"{prefix}-leaf",
            operator="primitive",
            version="1",
            predecessors=(),
            output_type="scalar",
            frame="world",
            metric="absolute",
            grade_schema=(("error", "scalar", "sum"),),
            checker="primitive-checker",
            checker_version="1",
            assumptions=("finite-input",),
            rank=0,
        )
        root = TypedPlanNode(
            name=f"{prefix}-root",
            operator="frame-bridge",
            version="1",
            predecessors=(("input", leaf.name),),
            output_type="scalar",
            frame="display",
            metric="absolute",
            grade_schema=(("error", "scalar", "path-weighted"),),
            checker=root_checker,
            checker_version="2",
            assumptions=("tube-valid",),
            rank=1,
        )
        return TypedPlanDAG(root.name, (leaf, root))

    def test_typed_plan_is_invariant_to_node_renaming(self) -> None:
        left = self.plan("left")
        right = self.plan("right")
        self.assertTrue(
            plan_isomorphism_holds(
                left,
                right,
                {"left-leaf": "right-leaf", "left-root": "right-root"},
            )
        )

    def test_checker_change_is_not_a_plan_isomorphism(self) -> None:
        left = self.plan("left")
        right = self.plan("right", root_checker="self-asserted-score")
        self.assertFalse(
            plan_isomorphism_holds(
                left,
                right,
                {"left-leaf": "right-leaf", "left-root": "right-root"},
            )
        )


class JointSufficiencyTests(unittest.TestCase):
    def test_equal_adequacy_scalar_can_hide_unequal_payload(self) -> None:
        samples = (
            {"margin": 0.5, "status": "granted", "payload": "cat"},
            {"margin": 0.5, "status": "granted", "payload": "dog"},
        )
        violations = sufficiency_violations(
            samples,
            code=lambda item: max(0.0, item["margin"]),
            consumers={
                "license": lambda item: item["status"],
                "classifier-payload": lambda item: item["payload"],
            },
        )
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0].consumer, "classifier-payload")

    def test_joint_code_separates_the_payload_counterexample(self) -> None:
        samples = (
            {"margin": 0.5, "status": "granted", "payload": "cat"},
            {"margin": 0.5, "status": "granted", "payload": "dog"},
        )
        violations = sufficiency_violations(
            samples,
            code=lambda item: (max(0.0, item["margin"]), item["payload"]),
            consumers={
                "license": lambda item: item["status"],
                "classifier-payload": lambda item: item["payload"],
            },
        )
        self.assertEqual(violations, ())


if __name__ == "__main__":
    unittest.main()
