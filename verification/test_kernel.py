"""Unit tests for the compact ``WF + K_3`` semantic kernel."""

from __future__ import annotations

from dataclasses import replace
import unittest

import verification.kernel as kernel
from verification.kernel import (
    AtomValue,
    Diagnostic,
    DiagnosticCompletenessError,
    Interval,
    Outcome,
    assess_certified_undominated,
    assess_relative_undefeated,
    assess_request,
    meet,
    open_atom,
    refuted,
    render_legacy_label,
    supported,
)
from verification.witness import WITNESS


class KernelTests(unittest.TestCase):
    def test_meet_is_strong_kleene_conjunction(self) -> None:
        self.assertEqual(meet((AtomValue.SUPPORTED, AtomValue.SUPPORTED)), AtomValue.SUPPORTED)
        self.assertEqual(meet((AtomValue.SUPPORTED, AtomValue.OPEN)), AtomValue.OPEN)
        self.assertEqual(meet((AtomValue.OPEN, AtomValue.REFUTED)), AtomValue.REFUTED)
        with self.assertRaises(ValueError):
            meet(())

    def test_four_public_outcomes_are_derived_from_wf_and_k3(self) -> None:
        expected = {
            "r_t0_O_rely": Outcome.GRANTED,
            "r_t0_Q_rely": Outcome.REFUSED,
            "r_t0_S_expanded": Outcome.WITHHELD,
            "r_t0_O_wrong_frame": Outcome.UNDEFINED,
        }
        for request_id, outcome in expected.items():
            with self.subTest(request_id=request_id):
                self.assertIs(WITNESS.assessment("t0", request_id).outcome, outcome)

    def test_well_formed_atoms_never_have_undefined_as_a_value(self) -> None:
        self.assertEqual(set(AtomValue), {AtomValue.REFUTED, AtomValue.OPEN, AtomValue.SUPPORTED})
        for stage, state in WITNESS.states.items():
            for request_id, diagnostics in state.diagnostics.items():
                with self.subTest(stage=stage, request_id=request_id):
                    self.assertIsNot(WITNESS.assessment(stage, request_id).outcome, Outcome.UNDEFINED)
                    self.assertTrue(all(isinstance(item.value, AtomValue) for item in diagnostics.values()))

    def test_well_formedness_failure_is_separate_from_atom_diagnostics(self) -> None:
        for request_id, label in (
            ("r_t0_O_wrong_frame", "FrameMismatch"),
            ("r_t0_O_bare", "MissingLicenseProfile"),
        ):
            assessment = WITNESS.assessment("t0", request_id)
            self.assertIs(assessment.outcome, Outcome.UNDEFINED)
            self.assertEqual(assessment.required, {})
            self.assertIsNotNone(assessment.wf_error)
            self.assertEqual(render_legacy_label(assessment.wf_error), label)

    def test_diagnostics_are_lossless_and_value_indexed(self) -> None:
        samples = (
            supported("a", "proof", ("node",)),
            open_atom("a", "missing premise", ("node",)),
            refuted("a", "counterexample", ("node",)),
        )
        self.assertEqual(samples[0].support, ("proof",))
        self.assertEqual(samples[1].obstacles, ("missing premise",))
        self.assertEqual(samples[2].counterwitness, ("counterexample",))
        for item in samples:
            self.assertEqual(item.provenance, ("node",))

    def test_malformed_diagnostics_are_rejected(self) -> None:
        fields = {
            AtomValue.SUPPORTED: {},
            AtomValue.OPEN: {},
            AtomValue.REFUTED: {},
        }
        for value, extra in fields.items():
            with self.subTest(value=value), self.assertRaises(ValueError):
                Diagnostic("atom", value, provenance=("node",), **extra)
        with self.assertRaises(ValueError):
            supported("atom", "proof", ())
        mixed_payloads = (
            dict(value=AtomValue.SUPPORTED, support=("w",), obstacles=("o",)),
            dict(value=AtomValue.OPEN, obstacles=("o",), counterwitness=("c",)),
            dict(value=AtomValue.REFUTED, counterwitness=("c",), support=("w",)),
        )
        for fields in mixed_payloads:
            with self.subTest(fields=fields), self.assertRaises(ValueError):
                Diagnostic("atom", provenance=("node",), **fields)

    def test_missing_required_atom_is_an_fixture_error_not_a_semantic_outcome(self) -> None:
        state = WITNESS.states["t0"]
        diagnostics = {key: dict(value) for key, value in state.diagnostics.items()}
        del diagnostics["r_t0_O_rely"]["trace"]
        broken = replace(state, diagnostics=diagnostics)
        with self.assertRaises(DiagnosticCompletenessError):
            assess_request(broken, "r_t0_O_rely")

    def test_missing_report_diagnostic_is_also_an_invalid_fixture(self) -> None:
        state = WITNESS.states["t0"]
        diagnostics = {key: dict(value) for key, value in state.diagnostics.items()}
        del diagnostics["r_t0_O_rely"]["comparison_report"]
        broken = replace(state, diagnostics=diagnostics)
        with self.assertRaisesRegex(DiagnosticCompletenessError, "open diagnostic"):
            assess_request(broken, "r_t0_O_rely")

    def test_invalid_or_missing_comparison_search_is_open(self) -> None:
        constructors = (assess_relative_undefeated, assess_certified_undominated)
        for constructor in constructors:
            for validity, obstacle in ((False, "InvalidSearchTrace"), (None, "MissingSearchTrace")):
                with self.subTest(constructor=constructor.__name__, validity=validity):
                    diagnostic = constructor(
                        "comparison",
                        "K",
                        ("search",),
                        search_trace_valid=validity,
                    )
                    self.assertIs(diagnostic.value, AtomValue.OPEN)
                    self.assertEqual(diagnostic.obstacles, (obstacle,))

    def test_valid_dominator_refutes_even_if_search_trace_is_invalid(self) -> None:
        diagnostic = assess_relative_undefeated(
            "comparison",
            "K",
            ("pair",),
            certified_dominators=("d",),
            search_trace_valid=False,
        )
        self.assertIs(diagnostic.value, AtomValue.REFUTED)

    def test_safety_projection_preserves_the_counterwitness(self) -> None:
        assessment = WITNESS.assessment("t0", "r_t0_Q_rely")
        self.assertEqual(assessment.alarms, ("hard_constraints",))
        alarm = assessment.required[assessment.alarms[0]]
        self.assertTrue(alarm.safety)
        self.assertEqual(alarm.counterwitness, ("k_resource_Q",))
        self.assertEqual(alarm.provenance, ("k_resource_Q",))

    def test_open_safety_projection_preserves_the_obstacle(self) -> None:
        state = WITNESS.states["t0"]
        diagnostics = {key: dict(value) for key, value in state.diagnostics.items()}
        diagnostics["r_t0_Q_rely"]["hard_constraints"] = open_atom(
            "hard_constraints", "RobustnessAuditPending", ("pending:Q",), safety=True
        )
        modified = replace(state, diagnostics=diagnostics)
        assessment = assess_request(modified, "r_t0_Q_rely")
        self.assertIs(assessment.outcome, Outcome.WITHHELD)
        self.assertEqual(assessment.open_safety, ("hard_constraints",))
        item = assessment.required[assessment.open_safety[0]]
        self.assertEqual(item.obstacles, ("RobustnessAuditPending",))
        self.assertEqual(item.provenance, ("pending:Q",))

    def test_reason_code_is_not_a_closed_semantic_type(self) -> None:
        self.assertFalse(hasattr(kernel, "ReasonCode"))

    def test_interval_comparison_requires_separation(self) -> None:
        self.assertTrue(Interval(0.048, 0.050).strictly_better_than(Interval(0.054, 0.056)))
        self.assertFalse(Interval(0.045, 0.060).strictly_better_than(Interval(0.050, 0.070)))
        self.assertTrue(Interval(0.045, 0.060).overlaps(Interval(0.050, 0.070)))


if __name__ == "__main__":
    unittest.main()
