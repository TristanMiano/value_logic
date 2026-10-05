"""Adversarial positive/negative measurement calibration, not learned results."""
import unittest

import numpy as np

from v2.experiments import calibration as C
from v2.experiments import neural as N


class CalibrationTests(unittest.TestCase):
    def test_cancelling_pair_blocks_ordinary_necessity_inference(self):
        result = C.cancellation_witness()
        self.assertTrue(result["passed"])
        self.assertFalse(result["original_F14_training_task"])
        self.assertFalse(result["interchange_implies_ordinary_necessity"])
        self.assertEqual(result["pair_removal_ordinary_effect_max"], 0)
        self.assertGreater(result["isolated_intervention_effect_max"], 0.3)

    def test_compiled_interchange_obeys_analytic_uniform_bound(self):
        result = C.development_calibration(n=64)
        self.assertTrue(result["passed"])
        self.assertFalse(result["learned_structure_evidence"])
        self.assertEqual(result["ordinary_training_steps"], 0)
        self.assertLess(result["uniform_probability_bound"], 0.01)
        self.assertEqual(len(result["rows"]), 10)

    def test_wrong_role_and_whole_layer_do_not_pass_as_intermediates(self):
        net, subsets, bound = C.compiled_cost_network()
        cfg = N.defaults()
        pairs, _ = N.make_pairs(cfg, cfg["development_seed"], 128, 0, stream=9300)
        base, donor = pairs["mixed_far"]
        target = N.high_prediction(base, donor, 0)
        right = C._swap(net, base, donor, subsets[0])
        wrong = C._swap(net, base, donor, subsets[1])
        whole = net.probability(donor)
        self.assertLessEqual(float(np.max(np.abs(right-target))), bound)
        self.assertGreater(float(np.mean(np.abs(wrong-target))), 0.05)
        self.assertGreater(float(np.mean(np.abs(whole-target))), 0.04)

    def test_two_disjoint_role_swaps_compose_and_commute(self):
        net, subsets, bound = C.compiled_cost_network()
        rng = N._rng(N.defaults()["development_seed"], 9400)
        base, d0, d1 = [N.sample_inputs(rng, 128) for _ in range(3)]
        h0, h1 = net.hidden(d0), net.hidden(d1)
        first, second = net.hidden(base), net.hidden(base)
        first[:, subsets[0]] = h0[:, subsets[0]]
        first[:, subsets[1]] = h1[:, subsets[1]]
        second[:, subsets[1]] = h1[:, subsets[1]]
        second[:, subsets[0]] = h0[:, subsets[0]]
        np.testing.assert_array_equal(first, second)
        j0, j1 = N.action_costs(d0)[:, 0], N.action_costs(d1)[:, 1]
        target = j0/(j0+j1)
        actual = N.sigmoid(first @ net.v + net.beta)
        self.assertLessEqual(float(np.max(np.abs(actual-target))), bound)


if __name__ == "__main__":
    unittest.main()
