"""Executable witnesses for Task 14C proof-carrying plans and stratification."""

from __future__ import annotations

from dataclasses import replace
import unittest

from verification.kernel import (
    EpistemicState,
    EvaluationContext,
    Interval,
    Outcome,
    Profile,
    ProvenanceGraph,
    Request,
    UsePlan,
    assess_request,
    assess_upper_bound,
)
from verification.proof_plans import (
    EvidenceRecord,
    EvaluationNode,
    PlanContractError,
    PlanDAG,
    PlanNode,
    ResourceBound,
    SupportNode,
    evaluate_stratified,
    execute_annotated,
    execute_plain,
    grounded_sources,
    verify_proof_term,
)


ENERGY = ("energy", "J", "sum")
LATENCY_MAX = ("latency", "ms", "max")


def resource(dimension: str, unit: str, amount: float) -> ResourceBound:
    return ResourceBound(dimension, unit, amount)


def witness_plan() -> tuple[PlanDAG, dict[str, EvidenceRecord]]:
    nodes = (
        PlanNode(
            name="left",
            predecessors=(),
            input_types=(),
            input_frames=(),
            input_metrics=(),
            output_type="scalar",
            output_frame="model",
            output_metric="abs-model",
            transform=lambda external, _: float(external) + 1.0,
            sensitivities=(),
            local_error_bound=0.05,
            local_resources=(resource("energy", "J", 1.0), resource("latency", "ms", 2.0)),
            resource_operators=(ENERGY, LATENCY_MAX),
            certificate_id="cert:left",
        ),
        PlanNode(
            name="right",
            predecessors=(),
            input_types=(),
            input_frames=(),
            input_metrics=(),
            output_type="scalar",
            output_frame="model",
            output_metric="abs-model",
            transform=lambda external, _: 2.0 * float(external),
            sensitivities=(),
            local_error_bound=0.10,
            local_resources=(resource("energy", "J", 2.0), resource("latency", "ms", 3.0)),
            resource_operators=(ENERGY, LATENCY_MAX),
            certificate_id="cert:right",
        ),
        PlanNode(
            name="parallel-join",
            predecessors=("left", "right"),
            input_types=("scalar", "scalar"),
            input_frames=("model", "model"),
            input_metrics=("abs-model", "abs-model"),
            output_type="scalar",
            output_frame="model",
            output_metric="abs-model",
            transform=lambda _, inputs: float(inputs[0]) + float(inputs[1]),
            sensitivities=(2.0, 1.0),
            local_error_bound=0.02,
            local_resources=(resource("energy", "J", 0.5), resource("latency", "ms", 1.0)),
            resource_operators=(ENERGY, LATENCY_MAX),
            certificate_id="cert:parallel-join",
        ),
        PlanNode(
            name="frame-bridge",
            predecessors=("parallel-join",),
            input_types=("scalar",),
            input_frames=("model",),
            input_metrics=("abs-model",),
            output_type="scalar",
            output_frame="world",
            output_metric="abs-world",
            transform=lambda _, inputs: 10.0 * float(inputs[0]),
            sensitivities=(10.0,),
            local_error_bound=0.01,
            local_resources=(resource("energy", "J", 0.2), resource("latency", "ms", 0.5)),
            resource_operators=(ENERGY, ("latency", "ms", "sum")),
            certificate_id="cert:frame-bridge",
        ),
    )
    plan = PlanDAG(nodes=nodes, root="frame-bridge")
    registry = {
        node.certificate_id: EvidenceRecord(
            certificate_id=node.certificate_id,
            node=node.name,
            checker="independent-checker:v1",
            accepted=True,
            metric=node.output_metric,
            local_error_bound=node.local_error_bound,
            local_resources=node.local_resources,
            sources=(f"base:{node.name}",),
        )
        for node in nodes
    }
    return plan, registry


class ProofCarryingPlanTests(unittest.TestCase):
    def test_annotated_executor_erases_to_plain_computation(self) -> None:
        plan, registry = witness_plan()
        annotated = execute_annotated(plan, 3.0, registry)
        self.assertEqual(annotated.payload, execute_plain(plan, 3.0))
        self.assertEqual(annotated.payload, 100.0)
        self.assertTrue(verify_proof_term(plan, annotated.certificate, registry))

    def test_path_sensitivity_and_typed_resource_transformers(self) -> None:
        plan, registry = witness_plan()
        result = execute_annotated(plan, 3.0, registry)
        # join = .02 + 2(.05) + .10 = .22; bridge = .01 + 10(.22) = 2.21
        self.assertAlmostEqual(result.grade.error_bound, 2.21)
        resources = {
            (bound.dimension, bound.unit): bound.amount
            for bound in result.grade.resources
        }
        self.assertAlmostEqual(resources[("energy", "J")], 3.7)
        # The join runs branches in parallel: 1 + max(2,3) = 4 ms.
        # The sequential bridge adds .5 ms.
        self.assertAlmostEqual(resources[("latency", "ms")], 4.5)

    def test_unregistered_or_self_asserted_certificate_cannot_build_the_proof(self) -> None:
        plan, registry = witness_plan()
        registry = dict(registry)
        registry["cert:parallel-join"] = replace(
            registry["cert:parallel-join"],
            accepted=False,
        )
        with self.assertRaises(PlanContractError):
            execute_annotated(plan, 3.0, registry)

    def test_cycle_is_not_silently_treated_as_a_recursive_plan(self) -> None:
        plan, registry = witness_plan()
        nodes = list(plan.nodes)
        nodes[0] = replace(
            nodes[0],
            predecessors=("frame-bridge",),
            input_types=("scalar",),
            input_frames=("world",),
            input_metrics=("abs-world",),
            sensitivities=(1.0,),
        )
        with self.assertRaises(PlanContractError):
            execute_annotated(PlanDAG(tuple(nodes), plan.root), 3.0, registry)

    def test_valid_composite_certificate_lifts_through_the_actual_kernel(self) -> None:
        plan, registry = witness_plan()
        result = execute_annotated(plan, 3.0, registry)
        self.assertTrue(verify_proof_term(plan, result.certificate, registry))
        diagnostic = assess_upper_bound(
            "adequacy",
            Interval(result.grade.error_bound, result.grade.error_bound),
            2.30,
            "composite-proof:frame-bridge",
            result.certificate.provenance,
        )
        state = EpistemicState(
            name="composite-license",
            plans={
                "composite": UsePlan(
                    "composite",
                    frozenset({"case"}),
                    deployment_cost=3.7,
                    memory=1.0,
                    robustness=Interval(0.0, 2.21),
                )
            },
            contexts={
                "q": EvaluationContext(
                    "q",
                    frozenset({"case"}),
                    tolerance=2.30,
                    fallback=None,
                    fallback_risk=None,
                    required_advantage=0.0,
                )
            },
            profiles={"P": Profile("P", ("adequacy",), action_authorizing=False)},
            requests={"r": Request("r", "composite", "q", "P")},
            diagnostics={"r": {"adequacy": diagnostic}},
            deployment_requests={},
            routes={},
            archive=frozenset({"composite"}),
            graph=ProvenanceGraph(nodes=frozenset(result.certificate.provenance), edges=()),
        )
        self.assertIs(assess_request(state, "r").outcome, Outcome.GRANTED)

    def test_grounded_provenance_reaches_typed_base_sources(self) -> None:
        graph = (
            SupportNode("dataset", base_kind="empirical"),
            SupportNode("checker", base_kind="formal"),
            SupportNode("local-bound", ("dataset",)),
            SupportNode("composite-bound", ("local-bound", "checker")),
            SupportNode("required-atom", ("composite-bound",)),
        )
        self.assertEqual(
            grounded_sources(graph, "required-atom"),
            ("empirical:dataset", "formal:checker"),
        )

    def test_closed_mutual_support_is_rejected_by_the_dag_fragment(self) -> None:
        graph = (
            SupportNode("grant-a", ("grant-b",)),
            SupportNode("grant-b", ("grant-a",)),
        )
        with self.assertRaises(PlanContractError):
            grounded_sources(graph, "grant-a")

    def test_ranked_system_assessment_is_unique_and_order_independent(self) -> None:
        nodes = (
            EvaluationNode("system-trace", 0, ("held-out-errors",), lambda xs: max(xs[0])),
            EvaluationNode("e_VL-audit", 1, ("system-trace",), lambda xs: xs[0] <= 0.1),
            EvaluationNode("meta-license", 2, ("e_VL-audit",), lambda xs: "Granted" if xs[0] else "Refused"),
        )
        exogenous = {"held-out-errors": (0.02, 0.08, 0.05)}
        forward = evaluate_stratified(nodes, exogenous)
        reverse = evaluate_stratified(tuple(reversed(nodes)), exogenous)
        self.assertEqual(forward, reverse)
        self.assertEqual(forward["meta-license"], "Granted")

    def test_same_rank_self_evaluation_is_outside_the_stratified_fragment(self) -> None:
        nodes = (
            EvaluationNode("e_VL", 1, ("meta-license",), lambda xs: xs[0]),
            EvaluationNode("meta-license", 1, ("e_VL",), lambda xs: xs[0]),
        )
        with self.assertRaises(PlanContractError):
            evaluate_stratified(nodes, {})


if __name__ == "__main__":
    unittest.main()
