"""Executable assertions for every table and transition in Task 11A."""

from __future__ import annotations

import unittest

from verification.kernel import AtomValue, Outcome, render_legacy_label
from verification.witness import (
    ADEQUACY,
    CERT_UNDOMINATED,
    COMPARISON_REPORT,
    IMPROVEMENT,
    REL_UNDEFEATED,
    SPLIT_READY,
    WITNESS,
)


class IntegratedWitnessTests(unittest.TestCase):
    def assert_outcomes(self, stage: str, expected: dict[str, Outcome]) -> None:
        for request_id, outcome in expected.items():
            with self.subTest(stage=stage, request_id=request_id):
                self.assertIs(WITNESS.assessment(stage, request_id).outcome, outcome)

    def test_t0_status_table_and_legacy_labels(self) -> None:
        self.assert_outcomes(
            "t0",
            {
                "r_t0_O_rely": Outcome.GRANTED,
                "r_t0_S_rely": Outcome.GRANTED,
                "r_t0_Q_rely": Outcome.REFUSED,
                "r_t0_S_expanded": Outcome.WITHHELD,
                "r_t0_O_wrong_frame": Outcome.UNDEFINED,
                "r_t0_O_bare": Outcome.UNDEFINED,
            },
        )
        q = WITNESS.assessment("t0", "r_t0_Q_rely")
        self.assertEqual(render_legacy_label(q.required["hard_constraints"]), "HardConstraintViolation")
        expanded = WITNESS.assessment("t0", "r_t0_S_expanded")
        self.assertEqual(render_legacy_label(expanded.required[ADEQUACY]), "NoScopeEvidence:e")

    def test_t0_simultaneous_use_comparison_and_route(self) -> None:
        self.assertEqual(WITNESS.active_set("t0", "b"), frozenset({"O", "S"}))
        self.assertEqual(WITNESS.active_set("t0", "c"), frozenset({"O", "S"}))
        self.assert_outcomes(
            "t0",
            {
                "r_t0_O_pref_overlap": Outcome.REFUSED,
                "r_t0_S_pref_overlap": Outcome.GRANTED,
            },
        )
        self.assertEqual(
            WITNESS.states["t0"].routes,
            {"a": "O", "b": "S", "c": "S", "d": "S", "e": "Defer"},
        )

    def test_declared_scopes_resources_and_fallback_arithmetic(self) -> None:
        state = WITNESS.states["t1"]
        self.assertEqual(state.plans["O"].executable_cases, frozenset("abc"))
        self.assertEqual(state.plans["N"].executable_cases, frozenset("bcd"))
        self.assertEqual((state.plans["O"].deployment_cost, state.plans["O"].memory), (1.0, 1.0))
        self.assertEqual((state.plans["S"].deployment_cost, state.plans["S"].memory), (3.0, 3.0))
        self.assertEqual((state.plans["Q"].deployment_cost, state.plans["Q"].memory), (0.5, 1.0))
        self.assertEqual((state.plans["N"].deployment_cost, state.plans["N"].memory), (2.0, 4.0))
        context = state.contexts["D_cloud"]
        self.assertEqual(context.tolerance, 0.20)
        self.assertEqual(context.fallback, "Defer")
        self.assertEqual(context.fallback_risk.lower, 0.30)
        self.assertEqual(context.required_advantage, 0.02)
        self.assertTrue(0.20 + context.required_advantage <= context.fallback_risk.lower)

    def test_recorded_representative_loss_table(self) -> None:
        expected = {
            "O": (0.06, 0.10, 0.14, None),
            "S": (None, 0.04, 0.05, 0.03),
            "Q": (0.08, 0.11, None, None),
            "N": (None, 0.03, 0.04, 0.05),
        }
        for plan, row in expected.items():
            self.assertEqual(tuple(WITNESS.representative_losses[(plan, case)] for case in "abcd"), row)

    def test_certificate_tables_have_the_stated_regions(self) -> None:
        expected = {
            ("t0", "O", "D_O"): (0.09, 0.11),
            ("t0", "S", "D_cloud"): (0.035, 0.055),
            ("t0", "Q", "D_Q"): (0.08, 0.12),
            ("t0", "O", "D_overlap"): (0.11, 0.13),
            ("t0", "S", "D_overlap"): (0.040, 0.050),
            ("t1", "N", "D_cloud"): (0.035, 0.050),
            ("t1", "N", "D_overlap"): (0.035, 0.045),
            ("t2", "S", "D_cloud"): (0.24, 0.27),
        }
        for key, bounds in expected.items():
            interval = WITNESS.risk_certificates[key]
            self.assertEqual((interval.lower, interval.upper), bounds)

    def test_comparison_eligibility_uses_exact_evaluation_scope(self) -> None:
        for plan, context in (
            ("O", "D_overlap"),
            ("N", "D_overlap"),
            ("O", "D_edge"),
            ("S", "D_cloud"),
            ("N", "D_cloud"),
        ):
            self.assertTrue(WITNESS.comparison_eligible("t1", plan, context))
        self.assertFalse(WITNESS.comparison_eligible("t1", "O", "D_cloud"))
        self.assertFalse(WITNESS.comparison_eligible("t1", "N", "D_edge"))
        self.assertFalse(WITNESS.comparison_eligible("t1", "S", "D_overlap"))

    def test_t1_profile_local_supersession_table(self) -> None:
        self.assert_outcomes(
            "t1",
            {
                "r_t1_O_rely": Outcome.GRANTED,
                "r_t1_N_rely": Outcome.GRANTED,
                "r_t1_O_pref_overlap": Outcome.REFUSED,
                "r_t1_N_pref_overlap": Outcome.GRANTED,
                "r_t1_S_rely": Outcome.GRANTED,
                "r_t1_S_pref_cloud": Outcome.REFUSED,
                "r_t1_N_pref_cloud": Outcome.GRANTED,
            },
        )
        self.assertEqual(
            WITNESS.assessment("t0", "r_t0_O_rely").required[ADEQUACY],
            WITNESS.assessment("t1", "r_t1_O_rely").required[ADEQUACY],
        )
        self.assertEqual(
            WITNESS.assessment("t0", "r_t0_S_rely").required[ADEQUACY],
            WITNESS.assessment("t1", "r_t1_S_rely").required[ADEQUACY],
        )

    def test_t1_continued_use_unselected_use_and_archive_only_retention(self) -> None:
        state = WITNESS.states["t1"]
        self.assertEqual(state.routes, {"a": "O", "b": "N", "c": "N", "d": "N", "e": "Defer"})
        self.assertEqual(WITNESS.selected_plans("t1"), frozenset({"O", "N"}))
        self.assertIs(WITNESS.assessment("t1", "r_t1_S_rely").outcome, Outcome.GRANTED)
        self.assertNotIn("S", WITNESS.selected_plans("t1"))
        self.assertIs(WITNESS.assessment("t1", "r_t1_Q_rely").outcome, Outcome.REFUSED)
        self.assertIn("Q", state.archive)
        self.assertTrue(WITNESS.edge_eligible("O"))
        self.assertFalse(WITNESS.edge_eligible("S"))
        self.assertFalse(WITNESS.edge_eligible("N"))

    def test_unknown_pairs_are_report_only_for_relative_profile(self) -> None:
        for plan in ("S", "N"):
            relative = WITNESS.assessment("t1", f"r_t1_{plan}_rel_local")
            certified = WITNESS.assessment("t1", f"r_t1_{plan}_cert_local")
            self.assertIs(relative.outcome, Outcome.GRANTED)
            self.assertIs(relative.required[REL_UNDEFEATED].value, AtomValue.SUPPORTED)
            self.assertIs(relative.reports[COMPARISON_REPORT].value, AtomValue.OPEN)
            self.assertIs(certified.outcome, Outcome.WITHHELD)
            self.assertIs(certified.required[CERT_UNDOMINATED].value, AtomValue.OPEN)
            self.assertEqual(
                render_legacy_label(certified.required[CERT_UNDOMINATED]),
                "UnresolvedComparison:S:N:local",
            )

    def test_successful_and_withheld_split(self) -> None:
        successful = WITNESS.assessment("t1", "r_t1_O_split")
        withheld = WITNESS.assessment("t1", "r_t1_S_split")
        self.assertIs(successful.outcome, Outcome.GRANTED)
        self.assertEqual(successful.required[SPLIT_READY].support, ("certified-partition:edge+overlap",))
        self.assertIs(withheld.outcome, Outcome.WITHHELD)
        self.assertEqual(render_legacy_label(withheld.required[SPLIT_READY]), "LocalSplitUncertified")
        self.assert_outcomes(
            "t1",
            {
                "r_t1_O_pref_edge": Outcome.GRANTED,
                "r_t1_O_pref_overlap": Outcome.REFUSED,
                "r_t1_N_pref_overlap": Outcome.GRANTED,
            },
        )

    def test_all_five_bridge_statuses_coexist(self) -> None:
        by_id = {bridge.bridge_id: bridge for bridge in WITNESS.bridges}
        self.assertEqual(
            {key: item.status for key, item in by_id.items()},
            {
                "beta_OS": "exact",
                "beta_ON": "approximate",
                "beta_SN_decision": "decision-compatible",
                "beta_SN_tight": "incompatible",
                "beta_QN": "unknown",
            },
        )
        self.assertEqual(by_id["beta_ON"].tolerance, 0.03)
        self.assertEqual(by_id["beta_SN_tight"].tolerance, 0.005)
        self.assertEqual(by_id["beta_SN_decision"].cases, by_id["beta_SN_tight"].cases)

    def test_joint_certificates_support_claim_marginals_cannot(self) -> None:
        marginal_n = WITNESS.marginal_scores["N"]
        marginal_s = WITNESS.marginal_scores["S"]
        joint_n = WITNESS.joint_scores["N"]
        joint_s = WITNESS.joint_scores["S"]
        self.assertTrue(marginal_n.overlaps(marginal_s))
        self.assertFalse(marginal_n.strictly_better_than(marginal_s))
        self.assertTrue(joint_n.strictly_better_than(joint_s))

    def test_t2_distinguishes_lapse_from_rebuttal(self) -> None:
        o = WITNESS.assessment("t2", "r_t2_O_rely")
        s = WITNESS.assessment("t2", "r_t2_S_rely")
        self.assertIs(o.outcome, Outcome.WITHHELD)
        self.assertIs(o.required[ADEQUACY].value, AtomValue.OPEN)
        self.assertEqual(render_legacy_label(o.required[ADEQUACY]), "BrokenAssumption")
        self.assertFalse(o.required[ADEQUACY].counterwitness)
        self.assertIs(s.outcome, Outcome.REFUSED)
        self.assertIs(s.required[ADEQUACY].value, AtomValue.REFUTED)
        self.assertEqual(render_legacy_label(s.required[ADEQUACY]), "HardRiskViolation")
        self.assertTrue(s.required[ADEQUACY].counterwitness)
        self.assertIs(s.required[IMPROVEMENT].value, AtomValue.SUPPORTED)
        self.assertEqual(
            WITNESS.states["t2"].routes,
            {"a": "Defer", "b": "N", "c": "N", "d": "N", "e": "Defer"},
        )

    def test_empty_active_set_is_a_selector_case_not_an_atom_reason(self) -> None:
        for stage in ("t0", "t1", "t2"):
            self.assertEqual(WITNESS.active_set(stage, "e"), frozenset())
            self.assertEqual(WITNESS.states[stage].routes["e"], "Defer")
            for diagnostics in WITNESS.states[stage].diagnostics.values():
                self.assertNotIn("NoLicensedModel", (item.atom for item in diagnostics.values()))

    def test_provenance_is_append_only_complete_and_preserves_correction_paths(self) -> None:
        t0 = WITNESS.states["t0"].graph
        t1 = WITNESS.states["t1"].graph
        t2 = WITNESS.states["t2"].graph
        self.assertTrue(t1.extends(t0))
        self.assertTrue(t2.extends(t1))
        self.assertTrue(all(WITNESS.provenance_complete(stage) for stage in WITNESS.states))
        self.assertTrue(t2.path_exists("d_O_leak^2", "status:r_t2_O_rely"))
        self.assertTrue(t2.path_exists("d_S_rebut^2", "status:r_t2_S_rely"))
        for stage, state in WITNESS.states.items():
            for diagnostics in state.diagnostics.values():
                for diagnostic in diagnostics.values():
                    with self.subTest(stage=stage, atom=diagnostic.atom):
                        self.assertTrue(diagnostic.provenance)
                        self.assertTrue(set(diagnostic.provenance).issubset(state.graph.nodes))


if __name__ == "__main__":
    unittest.main()
