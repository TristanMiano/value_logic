"""Finite regression witnesses for Task 14A transport/routing bounds.

The proofs and full hypotheses are in ``formalism/08a_transport_routing.md``.
"""

from __future__ import annotations

from itertools import combinations
import unittest


def positive_subsets(size: int):
    for length in range(1, size + 1):
        yield from combinations(range(size), length)


def conditional_mean(values: tuple[float, ...], subset: tuple[int, ...]) -> float:
    return sum(values[index] for index in subset) / len(subset)


class TransportRoutingFiniteWitnessTests(unittest.TestCase):
    def test_all_subdomain_means_match_pointwise_bound_on_finite_space(self) -> None:
        epsilon = 0.3
        losses = (0.0, 0.1, 0.2, 0.3)
        self.assertTrue(all(loss <= epsilon for loss in losses))
        self.assertTrue(
            all(
                conditional_mean(losses, subset) <= epsilon
                for subset in positive_subsets(len(losses))
            )
        )

        violating = (0.0, 0.1, 0.2, 0.4)
        bad_index = (3,)
        self.assertGreater(conditional_mean(violating, bad_index), epsilon)

    def test_parent_average_can_hide_bad_subdomain(self) -> None:
        losses = (1.0,) + (0.0,) * 9
        self.assertEqual(conditional_mean(losses, tuple(range(10))), 0.1)
        self.assertEqual(conditional_mean(losses, (0,)), 1.0)

    def test_hard_router_exact_decomposition_and_penalty_bound(self) -> None:
        # Four equiprobable cases: correct, misrouted, correct, fallback.
        routed_losses = (0.1, 0.8, 0.2, 0.4)
        global_risk = sum(routed_losses) / 4
        correct = (0.1 + 0.2) / 4
        misroute = 0.8 / 4
        fallback = 0.4 / 4
        self.assertAlmostEqual(global_risk, correct + misroute + fallback)

        penalty_bound = (0.25 * 0.1) + (0.25 * 0.2) + (0.25 * 0.8) + (0.25 * 0.4)
        self.assertAlmostEqual(global_risk, penalty_bound)

    def test_selected_subset_invalidates_naive_mean_rescaling(self) -> None:
        whole_cell_losses = (0.0, 1.0)
        whole_mean = conditional_mean(whole_cell_losses, (0, 1))
        selected_mass = 0.5
        actual_selected_integral = 0.5 * whole_cell_losses[1]
        naive_rescaling = selected_mass * whole_mean
        self.assertEqual(actual_selected_integral, 0.5)
        self.assertEqual(naive_rescaling, 0.25)

    def test_lipschitz_bridge_and_blend_risk_bounds(self) -> None:
        # lambda(y,0)=2*abs(y) is 2-Lipschitz.
        k = 2.0
        f = (0.0, 0.0)
        g = (0.1, 0.1)
        delta = sum(abs(left - right) for left, right in zip(f, g)) / len(f)
        risk_f = sum(2 * abs(value) for value in f) / len(f)
        risk_g = sum(2 * abs(value) for value in g) / len(g)
        self.assertLessEqual(abs(risk_f - risk_g), k * delta)

        blend = tuple(0.5 * left + 0.5 * right for left, right in zip(f, g))
        risk_blend = sum(2 * abs(value) for value in blend) / len(blend)
        self.assertLessEqual(risk_blend, risk_f + k * 0.5 * delta)

    def test_plan_dag_path_sensitivity_matches_recurrence(self) -> None:
        # Edges: 0->1 (3), 0->2 (2), 1->2 (4).
        delta_0, delta_1, delta_2 = 0.1, 0.2, 0.05
        error_0 = delta_0
        error_1 = delta_1 + 3 * error_0
        error_2 = delta_2 + 2 * error_0 + 4 * error_1

        weight_0_to_2 = 2 + (3 * 4)
        path_sum_bound = weight_0_to_2 * delta_0 + 4 * delta_1 + delta_2
        self.assertAlmostEqual(error_2, path_sum_bound)

    def test_additive_group_cycle_condition_characterizes_potentials(self) -> None:
        potentials = (2.0, 5.0, -1.0)
        g_01 = potentials[1] - potentials[0]
        g_12 = potentials[2] - potentials[1]
        g_20 = potentials[0] - potentials[2]
        self.assertAlmostEqual(g_01 + g_12 + g_20, 0.0)

        inconsistent_cycle = (0.0, 0.0, 1.0)
        self.assertNotEqual(sum(inconsistent_cycle), 0.0)


if __name__ == "__main__":
    unittest.main()
