"""Executable witnesses for the focused Task 14B repairs."""

from __future__ import annotations

from dataclasses import replace
import unittest

from verification.footprints import (
    certificate_writes,
    comparison_footprint,
    evaluated_set_writes,
    improvement_footprint,
    key,
    pair_writes,
    projection,
    region_footprint,
    search_writes,
    trace_footprint,
    trace_writes,
    write_disjoint,
)
from verification.kernel import (
    AtomValue,
    Edge,
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
from verification.witness import WITNESS


class AuditRepairWitnessTests(unittest.TestCase):
    def test_negative_evidence_and_trace_reads_use_collection_indices(self) -> None:
        region_reads = region_footprint("adequacy", "m", ())
        trace_reads = trace_footprint("trace", "m", ())
        self.assertIn(key("cert-index", "adequacy", "m"), region_reads)
        self.assertIn(key("region-index", "adequacy"), region_reads)
        self.assertIn(key("trace-index", "trace", "m"), trace_reads)
        self.assertFalse(write_disjoint(region_reads, certificate_writes("adequacy", "m", "k-new")))
        self.assertFalse(write_disjoint(trace_reads, trace_writes("trace", "m", "t-new")))

    def test_improvement_reads_both_candidate_and_fallback_indices(self) -> None:
        reads = improvement_footprint(
            "improvement",
            "candidate-risk",
            "fallback-risk",
            "q",
            "m",
        )
        self.assertIn(key("region-index", "candidate-risk"), reads)
        self.assertIn(key("region-index", "fallback-risk"), reads)
        self.assertIn(key("fallback", "q"), reads)

    def test_comparison_footprint_catches_future_set_search_and_pair_writes(self) -> None:
        evaluated = ("g", "d")
        reads = comparison_footprint(
            "certified",
            "g",
            "q",
            evaluated,
            "risk",
            "m",
        )
        self.assertFalse(write_disjoint(reads, evaluated_set_writes("q", "new-plan")))
        self.assertFalse(
            write_disjoint(reads, search_writes("g", "q", evaluated, "risk", "search-new"))
        )
        self.assertFalse(write_disjoint(reads, pair_writes("g", "d", "q", "risk", "pair-new")))

    def test_disjoint_write_preserves_the_typed_projection(self) -> None:
        reads = region_footprint("adequacy", "m", ("k",))
        before = {
            key("cert-index", "adequacy", "m"): ("k",),
            key("certificate", "k"): "payload",
            key("region-index", "adequacy"): ("k",),
            key("region", "k", "adequacy"): (0.0, 0.1),
            key("current", "k"): True,
        }
        after = dict(before)
        after[key("archive", "z")] = "added"
        writes = {key("archive", "z")}
        self.assertTrue(write_disjoint(reads, writes))
        self.assertEqual(projection(before, reads), projection(after, reads))

    def test_spurious_impact_path_does_not_preclude_real_assessment_invariance(self) -> None:
        before = WITNESS.states["t0"]
        request_id = "r_t0_O_rely"
        event = "event:add-irrelevant-model:Z"
        status = f"status:{request_id}"
        extra_plan = UsePlan("Z", frozenset({"z"}), 1.0, 1.0, Interval(0.0, 0.1))
        graph = ProvenanceGraph(
            nodes=before.graph.nodes | {event},
            edges=before.graph.edges + (Edge(event, status, "conservative_may_affect"),),
        )
        after = replace(
            before,
            name="t0-plus-irrelevant-Z",
            plans={**before.plans, "Z": extra_plan},
            archive=before.archive | {"Z"},
            graph=graph,
        )
        assessment_before = assess_request(before, request_id)
        assessment_after = assess_request(after, request_id)
        self.assertTrue(after.graph.path_exists(event, status))
        self.assertEqual(assessment_before, assessment_after)
        self.assertIs(assessment_after.outcome, Outcome.GRANTED)

    def test_component_grants_do_not_grant_the_composite_plan(self) -> None:
        plans = {
            name: UsePlan(name, frozenset({"x"}), 1.0, 1.0, Interval(0.0, 0.0))
            for name in ("c1", "c2", "composite")
        }
        context = EvaluationContext(
            "q",
            frozenset({"x"}),
            tolerance=0.10,
            fallback=None,
            fallback_risk=None,
            required_advantage=0.0,
        )
        profile = Profile("P_adequacy", ("adequacy",), action_authorizing=False)
        requests = {
            name: Request(name, name, "q", "P_adequacy")
            for name in plans
        }
        bounds = {"c1": 0.06, "c2": 0.06, "composite": 0.12}
        diagnostics = {
            name: {
                "adequacy": assess_upper_bound(
                    "adequacy",
                    Interval(bound, bound),
                    context.tolerance,
                    f"cert:{name}",
                    (f"cert:{name}",),
                )
            }
            for name, bound in bounds.items()
        }
        state = EpistemicState(
            name="composition",
            plans=plans,
            contexts={"q": context},
            profiles={"P_adequacy": profile},
            requests=requests,
            diagnostics=diagnostics,
            deployment_requests={},
            routes={},
            archive=frozenset(plans),
            graph=ProvenanceGraph(
                nodes=frozenset(f"cert:{name}" for name in plans),
                edges=(),
            ),
        )
        self.assertIs(assess_request(state, "c1").outcome, Outcome.GRANTED)
        self.assertIs(assess_request(state, "c2").outcome, Outcome.GRANTED)
        composite = assess_request(state, "composite")
        self.assertIs(composite.outcome, Outcome.REFUSED)
        self.assertIs(composite.required["adequacy"].value, AtomValue.REFUTED)


if __name__ == "__main__":
    unittest.main()
