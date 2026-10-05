"""Independent F14 statistical-contract checks; development streams only."""
import copy
from itertools import product
import math
import unittest

import numpy as np

from v2.experiments import analysis, neural


class F14NeuralContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        smoke = neural.development_smoke()
        cls.result = smoke["results"]
        cls.config = {"neural": smoke["config"], "analysis": analysis.defaults()}

    def assess(self, result=None, config=None):
        return analysis.neural_assessment([self.result if result is None else result],
                                         self.config if config is None else config,
                                         development=True)

    def test_finite_claim_family_has_exact_planned_count(self):
        assessment = self.assess()
        self.assertEqual(assessment["actual_interval_rows"], 112)
        self.assertTrue(assessment["development_only"])
        self.assertFalse(assessment["pilot_support_criterion_met"])
        too_small = copy.deepcopy(self.config)
        too_small["analysis"]["maximum_interval_rows"] = 111
        with self.assertRaisesRegex(ValueError, "family was exceeded"):
            self.assess(config=too_small)

    def test_hoeffding_width_and_union_bound_are_applied(self):
        interval = analysis.bounded_interval(.02, 8192)
        radius = math.sqrt(math.log(2 * 560 / .05) / (2 * 8192))
        self.assertAlmostEqual(interval["radius"], radius)
        delta = analysis.bounded_interval(.03, 5 * 8192, lower=-1, upper=1)
        self.assertAlmostEqual(delta["radius"], 2 * radius / math.sqrt(5))
        self.assertEqual(interval["lower"], 0)

    def test_equal_stratum_pooling_targets_the_equal_mixture(self):
        strata = [np.array([a - .03, a, a + .03]) for a in (-.2, -.1, .0, .1, .3)]
        cells = [neural._comparison_statistics(s) for s in strata]
        mean, count = analysis._pooled(cells)
        self.assertEqual(count, 15)
        self.assertAlmostEqual(mean, float(np.mean([s.mean() for s in strata])))
        cells[0]["n"] = 4
        with self.assertRaises(ValueError):
            analysis._pooled(cells)

    def test_comparison_constant_array_rounding_is_not_a_false_failure(self):
        row = neural._comparison_statistics(np.full(3, .1))
        mean, count = analysis._comparison(row)
        self.assertEqual(count, 3)
        self.assertAlmostEqual(mean, .1)

    def test_comparison_moments_cannot_be_inconsistent(self):
        row = neural._comparison_statistics(np.array([.1, .2, .3]))
        row["sum"] = 1.5
        with self.assertRaises(ValueError):
            analysis._comparison(row)

    def test_adjusted_effect_bound_uses_each_conditional_baseline(self):
        assessment = self.assess()
        for g in neural.G_FAMILY:
            for role in assessment["models"][0]["hypotheses"][g]["roles"]:
                for stratum in neural.STRATA:
                    self.assertAlmostEqual(role["derived_adjusted_effect_mae_upper"][stratum],
                        min(2, role["absolute"][stratum]["upper"] + role["conditional_base"][stratum]["upper"]))

    def test_bad_conditional_baseline_blocks_an_otherwise_adequate_relation(self):
        # Synthetic reporting fixture: relax unrelated criteria only in this
        # unit test, retaining development=True. No frozen run is changed.
        config = copy.deepcopy(self.config)
        config["analysis"].update({"intervention_mae_max": 1.,
                                  "conditional_base_probability_mae_max": .8,
                                  "adjusted_effect_mae_max": 2.,
                                  "far_decision_disagreement_max": 1.,
                                  "near_decision_disagreement_max": 1.})
        baseline = self.assess(config=config)
        self.assertTrue(baseline["models"][0]["hypotheses"]["identity"]["adequate"])
        mutated = copy.deepcopy(self.result)
        mutated["alignments"]["identity/aligned"]["roles"][0]["mixed_far"]["base_prediction"]["mae"] = 1.
        changed = self.assess(mutated, config)
        for g in neural.G_FAMILY:
            self.assertFalse(changed["models"][0]["hypotheses"][g]["adequate"])

    def test_conditional_baseline_count_must_match_pairs(self):
        mutated = copy.deepcopy(self.result)
        mutated["alignments"]["identity/aligned"]["roles"][0]["mixed_far"]["base_prediction"]["n"] += 1
        with self.assertRaises(ValueError):
            self.assess(mutated)

    def test_task_regret_normalization_is_the_exact_domain_bound(self):
        vertices = np.array(list(product((-1., 1.), (-1., 1.), (.5, 2.), (.5, 2.))))
        costs = neural.action_costs(vertices)
        wrong_action_regret = np.max(costs, axis=1) - np.min(costs, axis=1)
        self.assertEqual(float(wrong_action_regret.max()), 11 / 8)
        task = self.result["task"]
        self.assertEqual(task["decision_regret_bound"], 11 / 8)
        self.assertAlmostEqual(task["mean_normalized_decision_regret"], task["mean_decision_regret"] / (11 / 8))

    def test_scale_separating_generator_produces_fixed_full_denominators(self):
        n = self.result["pairs_per_stratum"]
        for g in neural.G_FAMILY[1:]:
            for role in (0, 1):
                cell = self.result["alternative_comparisons"][g][f"{role}/scale_separating"]
                self.assertEqual(cell["total_pairs"], n)
                self.assertEqual(cell["separating_pairs"], n)
                self.assertEqual(cell["separating_fraction"], 1)
                self.assertEqual(cell["same_identity_subset_comparison"]["n"], n)

    def test_scale_total_denominator_mismatch_rejected(self):
        mutated = copy.deepcopy(self.result)
        mutated["alternative_comparisons"]["inv_eta"]["0/scale_separating"]["total_pairs"] += 1
        with self.assertRaises(ValueError):
            self.assess(mutated)

    def test_scale_comparison_partial_denominator_rejected(self):
        mutated = copy.deepcopy(self.result)
        cell = mutated["alternative_comparisons"]["inv_eta"]["0/scale_separating"]
        cell["same_identity_subset_comparison"]["n"] = self.config["neural"]["g_min_separating_pairs"]
        with self.assertRaises(ValueError):
            self.assess(mutated)

    def test_missing_rival_gauge_cannot_be_a_numerical_pass(self):
        mutated = copy.deepcopy(self.result)
        del mutated["gauges_by_g"]["inv_total_cost"]
        try:
            assessment = self.assess(mutated)
        except ValueError:
            return
        self.assertFalse(assessment["models"][0]["numerical_controls_valid"])

    def test_gauge_boolean_cannot_override_observed_transport_error(self):
        mutated = copy.deepcopy(self.result)
        gauge = mutated["gauges_by_g"]["inv_eta"]
        gauge["errors"]["decoder_value"] = .1
        self.assertTrue(gauge["passed"])
        assessment = self.assess(mutated)
        self.assertFalse(assessment["models"][0]["numerical_controls_valid"])


if __name__ == "__main__":
    unittest.main()
