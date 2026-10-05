"""F14 development checks. No prospectively held-out evaluation seed is used."""
import copy
import unittest
from unittest.mock import patch

import numpy as np

from v2.experiments import neural as n


class F14NeuralTests(unittest.TestCase):
    def small_config(self):
        c = n.defaults()
        c.update({"training_steps": 4, "batch_size": 32, "fit_samples": 64,
                  "candidate_count": 4, "selection_pairs_per_stratum": 4,
                  "evaluation_pairs_per_stratum": 8, "task_evaluation_samples": 32,
                  "g_min_separating_pairs": 2})
        return c

    def test_default_config_freezes_disjoint_streams_and_capacity(self):
        c = n.validate_config(n.defaults())
        self.assertEqual(c["width"], 32)
        self.assertEqual(c["subset_size"], 8)
        self.assertEqual(c["training_steps"] * c["batch_size"], 768000)
        bad = copy.deepcopy(c)
        bad["evaluation_seeds"][0] = c["development_seed"]
        with self.assertRaises(ValueError):
            n.validate_config(bad)
        bad = copy.deepcopy(c)
        bad["subset_size"] = 32
        with self.assertRaises(ValueError):
            n.validate_config(bad)

    def test_outcome_training_labels_are_stochastic_binary(self):
        x, y = n.training_batch(n._rng(1400401, 901), 4096)
        self.assertEqual(set(y), {0.0, 1.0})
        self.assertTrue(np.all(np.abs(x[:, :2]) <= 1))
        self.assertTrue(np.all((x[:, 2:] >= 0.5) & (x[:, 2:] <= 2)))
        self.assertTrue(np.all((n.eta(x) >= 0.25) & (n.eta(x) <= 0.75)))
        self.assertFalse(np.array_equal(y, n.action_costs(x)[:, 0]))

    def test_weighted_bce_gradient_by_finite_difference(self):
        rng = n._rng(1400401, 902)
        x, y = n.training_batch(rng, 11)
        net = n.MLP.initialize(5, rng)
        # Move away from ReLU kinks, whose derivative is intentionally one-sided.
        net.b += 3.0
        _, gradients = n.loss_and_gradients(net, x, y)
        parameters = [net.w, net.b, net.v]
        epsilon = 1e-6
        for parameter, gradient in zip(parameters, gradients):
            for index in list(np.ndindex(parameter.shape))[:6]:
                original = parameter[index]
                parameter[index] = original + epsilon
                plus = n.loss_and_gradients(net, x, y)[0]
                parameter[index] = original - epsilon
                minus = n.loss_and_gradients(net, x, y)[0]
                parameter[index] = original
                self.assertAlmostEqual((plus - minus) / (2 * epsilon), gradient[index], places=7)
        original = net.beta
        net.beta = original + epsilon
        plus = n.loss_and_gradients(net, x, y)[0]
        net.beta = original - epsilon
        minus = n.loss_and_gradients(net, x, y)[0]
        self.assertAlmostEqual((plus - minus) / (2 * epsilon), gradients[3], places=7)

    def test_training_reproducible_and_counts_actual_outcomes(self):
        c = self.small_config()
        first, initial, resources = n.train_network(c, c["development_seed"])
        second, _, _ = n.train_network(c, c["development_seed"])
        self.assertEqual(first.to_dict(), second.to_dict())
        self.assertNotEqual(first.to_dict(), initial.to_dict())
        self.assertEqual(resources["expected_cost_training_labels"], 0)
        self.assertEqual(resources["stochastic_outcome_labels"], 128)
        self.assertEqual(resources["parameter_count"], 193)

    def test_network_training_cannot_access_expected_cost_targets(self):
        c = self.small_config()
        with patch.object(n, "action_costs", side_effect=AssertionError("Post-hoc only")), \
                patch.object(n, "concepts", side_effect=AssertionError("Post-hoc only")):
            _, _, resources = n.train_network(c, c["development_seed"])
        self.assertEqual(resources["expected_cost_training_labels"], 0)

    def test_pair_strata_enforce_nontrivial_counterfactuals(self):
        c = n.defaults()
        for role in (0, 1):
            pairs, _ = n.make_pairs(c, 1400401, 64, role, 910 + role * 10)
            for stratum, (base, donor) in pairs.items():
                jb, jd = n.action_costs(base), n.action_costs(donor)
                ph = n.high_prediction(base, donor, role)
                pb, pd = n.optimal_probability(base), n.optimal_probability(donor)
                self.assertTrue(np.all((donor[:, 2:] >= 0.5) & (donor[:, 2:] <= 2)))
                if stratum.startswith("mixed"):
                    self.assertTrue(np.all(np.abs(ph - pb) >= 0.05 - 1e-12))
                    self.assertTrue(np.all(np.abs(ph - pd) >= 0.05 - 1e-12))
                if stratum == "mixed_near":
                    self.assertTrue(np.all(np.abs(ph - 0.5) <= 0.04 + 1e-12))
                elif stratum == "mixed_far":
                    self.assertTrue(np.all(np.abs(ph - 0.5) >= 0.15 - 1e-12))
                elif stratum == "preserve_other":
                    np.testing.assert_allclose(jb[:, 1 - role], jd[:, 1 - role], atol=1e-12)
                    np.testing.assert_allclose(ph, pd, atol=1e-12)
                elif stratum == "equal_target":
                    np.testing.assert_allclose(jb[:, role], jd[:, role], atol=1e-12)
                    np.testing.assert_allclose(ph, pb, atol=1e-12)
                    self.assertTrue(np.all(np.abs(n.eta(base) - n.eta(donor)) >= 0.08 - 1e-12))
                else:
                    difference = np.column_stack([np.abs(ph - n.high_prediction(base, donor, role, g)) for g in n.G_FAMILY[1:]])
                    self.assertTrue(np.all(np.min(difference, axis=1) >= c["g_separation_min"] - 1e-12))

    def test_wrong_donor_stream_is_fresh_same_stratum_marginal(self):
        c = n.defaults()
        first, _ = n.make_pairs(c, 1400401, 16, 0, 950)
        wrong, _ = n.make_pairs(c, 1400401, 16, 0, 960)
        for stratum in n.STRATA:
            a, b = first[stratum][1], wrong[stratum][1]
            # Fresh independently generated donors, not reused/permuted rows.
            self.assertFalse(np.any(np.all(a[:, None, :] == b[None, :, :], axis=2)))

    def test_global_and_input_dependent_scales_are_distinct_controls(self):
        x = n.sample_inputs(n._rng(1400401, 970), 256)
        d = n.sample_inputs(n._rng(1400401, 971), 256)
        for g in n.G_FAMILY:
            concept = n.concepts(x, g)
            np.testing.assert_allclose(concept[:, 0] / concept.sum(axis=1), n.optimal_probability(x), atol=1e-15)
        self.assertGreater(float(np.max(np.abs(n.high_prediction(x, d, 0) - n.high_prediction(x, d, 0, "inv_eta")))), 0.05)
        jx, jd = 2 * n.action_costs(x), 2 * n.action_costs(d)
        np.testing.assert_allclose(jd[:, 0] / (jd[:, 0] + jx[:, 1]), n.high_prediction(x, d, 0), atol=1e-15)

    def test_inverse_total_cost_is_the_normalized_probability_explanation(self):
        x = n.sample_inputs(n._rng(1400401, 972), 256)
        d = n.sample_inputs(n._rng(1400401, 973), 256)
        p, pd = n.optimal_probability(x), n.optimal_probability(d)
        normalized = n.concepts(x, "inv_total_cost")
        np.testing.assert_allclose(normalized[:, 0], p, atol=1e-15)
        np.testing.assert_allclose(normalized[:, 1], 1 - p, atol=1e-15)
        np.testing.assert_allclose(n.high_prediction(x, d, 0, "inv_total_cost"), pd / (pd + 1 - p), atol=1e-15)
        np.testing.assert_allclose(n.high_prediction(x, d, 1, "inv_total_cost"), p / (p + 1 - pd), atol=1e-15)

    def test_decoder_and_intervention_transport_without_refitting(self):
        rng = n._rng(1400401, 980)
        net = n.MLP.initialize(32, rng)
        x, d = n.sample_inputs(rng, 64), n.sample_inputs(rng, 64)
        roles = []
        for role in (0, 1):
            subset = list(range(role * 4, role * 4 + 8))
            decoder, _ = n.fit_decoder(net.hidden(x), n.action_costs(x)[:, role], subset, 1e-6)
            roles.append({"subset": subset, "decoder": decoder})
        alignment = {"roles": roles, "overlap": list(range(4, 8))}
        permutation, scales = rng.permutation(32), np.exp(rng.uniform(-2, 2, 32))
        gauged = net.gauge(permutation, scales)
        transported = n.transport_alignment(alignment, permutation, scales)
        np.testing.assert_allclose(gauged.probability(x), net.probability(x), atol=1e-14)
        for role in (0, 1):
            old, new = alignment["roles"][role], transported["roles"][role]
            np.testing.assert_allclose(n.decode(net.hidden(x), old["decoder"]), n.decode(gauged.hidden(x), new["decoder"]), atol=1e-12)
            np.testing.assert_allclose(n._swap_probabilities(net, net.hidden(x), net.hidden(d), old["subset"]), n._swap_probabilities(gauged, gauged.hidden(x), gauged.hidden(d), new["subset"]), atol=1e-14)

    def test_unused_duplicate_refutes_decoding_as_causal_sufficiency(self):
        result = n.unused_duplicate_witness()
        self.assertTrue(result["decoding_passes_and_unused_causal_use_fails"])
        self.assertEqual(result["unused_logit_effect_max"], 0)
        self.assertGreater(result["used_logit_effect_max"], 1)

    def test_candidate_ranking_does_not_let_decodability_hide_bad_interventions(self):
        scores = [{"probability_mse": .1, "effect_mse": .001, "decoder_nmse": .001},
                  {"probability_mse": .01, "effect_mse": .2, "decoder_nmse": 20.0}]
        self.assertEqual(n._choose_candidate(scores, 1e-12), 1)

    def test_discovery_budgets_and_hashes_are_explicit(self):
        c = self.small_config()
        calls = []
        original = n.make_pairs
        def observed(config, seed, *args, **kwargs):
            calls.append(seed)
            return original(config, seed, *args, **kwargs)
        with patch.object(n, "make_pairs", side_effect=observed):
            prepared = n.prepare_neural(c, c["development_seed"])
        self.assertEqual(set(calls), {c["development_seed"]})
        self.assertFalse(prepared["evaluation_generated"])
        self.assertEqual(len(prepared["alignments"]), 20)
        self.assertEqual(prepared["resource"]["candidate_evaluations"], 160)
        for alignment in prepared["alignments"].values():
            for role in alignment["roles"]:
                self.assertEqual(role["decoder_fits"], 4)
                self.assertEqual(role["candidate_evaluations"], 4)
                self.assertTrue(all(len(s) == 8 and len(set(s)) == 8 for s in role["candidate_pool"]))
                self.assertEqual(role["subset"], role["candidate_pool"][role["selected_index"]])
        self.assertEqual(len(prepared["selection_data_hashes"]["decoder_inputs"]), 64)

    def test_hash_failure_precedes_evaluation_generation(self):
        c = self.small_config()
        prepared = n.prepare_neural(c, c["development_seed"])
        prepared["selected_alternative"] = "identity"
        with patch.object(n, "make_pairs", side_effect=AssertionError("Must not generate evaluation")):
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                n.evaluate_neural(prepared, c, c["development_evaluation_seed"])

    def test_small_development_end_to_end_reports_controls_without_scientific_pass(self):
        c = self.small_config()
        prepared = n.prepare_neural(c, c["development_seed"])
        result = n.evaluate_neural(prepared, c, c["development_evaluation_seed"])
        self.assertEqual(result["evaluation_seed"], c["development_evaluation_seed"])
        self.assertTrue(result["gauge"]["passed"])
        self.assertTrue(all(g["passed"] for g in result["gauges_by_g"].values()))
        self.assertEqual(result["gauge"]["refits"], 0)
        self.assertEqual(result["resource"]["alignment_refits"], 0)
        self.assertIn("same_identity_subset_comparison", result["alternative_comparisons"]["inv_eta"]["0/mixed_near"])
        self.assertIn("untouched_decoder_nrmse", result["alignments"]["identity/aligned"]["roles"][0]["mixed_near"])
        self.assertEqual(set(result["matched_control_comparisons_by_g"]), set(n.G_FAMILY))
        self.assertEqual(result["global_scale_prediction_error"], 0)
        self.assertNotIn("scientific_pass", result)
        self.assertEqual(result["discovery_artifact_hash"], prepared["artifact_hash"])


if __name__ == "__main__":
    unittest.main()
