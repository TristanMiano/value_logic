"""Finite regression witnesses for the Task 14 metatheory.

These tests check the small cardinality and separation countermodels.  They are
not a substitute for the proofs in ``formalism/08_metatheory.md``.
"""

from __future__ import annotations

from itertools import product
import math
import unittest

from verification.kernel import AtomValue, Outcome


VALUES = tuple(AtomValue)


def profile_outcome(vector: tuple[AtomValue, ...], required: tuple[int, ...]) -> Outcome:
    meet = min(vector[index] for index in required)
    return {
        AtomValue.REFUTED: Outcome.REFUSED,
        AtomValue.OPEN: Outcome.WITHHELD,
        AtomValue.SUPPORTED: Outcome.GRANTED,
    }[meet]


def respects_support_refinements(
    vector: tuple[AtomValue, ...], edges: tuple[tuple[int, int], ...]
) -> bool:
    """An edge ``a -> b`` means support for ``a`` entails support for ``b``."""

    return all(
        vector[strong] is not AtomValue.SUPPORTED
        or vector[weak] is AtomValue.SUPPORTED
        for strong, weak in edges
    )


class MetatheoryFiniteWitnessTests(unittest.TestCase):
    def test_independent_singletons_distinguish_three_to_the_n_vectors(self) -> None:
        n = 3
        vectors = tuple(product(VALUES, repeat=n))
        signatures = {
            tuple(profile_outcome(vector, (index,)) for index in range(n))
            for vector in vectors
        }
        self.assertEqual(len(vectors), 3**n)
        self.assertEqual(len(signatures), 3**n)
        self.assertEqual(math.ceil(math.log2(len(signatures))), math.ceil(n * math.log2(3)))

    def test_refinement_reduces_two_atom_realizable_space_to_seven(self) -> None:
        vectors = tuple(
            vector
            for vector in product(VALUES, repeat=2)
            if respects_support_refinements(vector, ((0, 1),))
        )
        self.assertEqual(len(vectors), 7)
        self.assertNotIn((AtomValue.SUPPORTED, AtomValue.OPEN), vectors)
        self.assertNotIn((AtomValue.SUPPORTED, AtomValue.REFUTED), vectors)

        signatures = {
            (profile_outcome(vector, (0,)), profile_outcome(vector, (1,)))
            for vector in vectors
        }
        self.assertEqual(len(signatures), 7)

    def test_missing_profile_refinement_has_a_finite_separator(self) -> None:
        # Only atom 0 entails atom 1.  Requiring atom 1 therefore does not
        # syntactically refine a profile requiring atom 0.
        separator = (AtomValue.OPEN, AtomValue.SUPPORTED)
        self.assertTrue(respects_support_refinements(separator, ((0, 1),)))
        self.assertEqual(profile_outcome(separator, (1,)), Outcome.GRANTED)
        self.assertEqual(profile_outcome(separator, (0,)), Outcome.WITHHELD)

    def test_spurious_impact_path_does_not_preclude_invariance(self) -> None:
        graph_reaches_atom = True
        allowed_endpoint_values = (AtomValue.SUPPORTED,)
        robustly_invariant = all(
            value is AtomValue.SUPPORTED for value in allowed_endpoint_values
        )
        self.assertTrue(graph_reaches_atom)
        self.assertTrue(robustly_invariant)

    def test_component_adequacy_does_not_imply_composite_adequacy(self) -> None:
        tolerance = 0.10
        component_errors = (0.06, 0.06)
        self.assertTrue(all(error <= tolerance for error in component_errors))
        self.assertGreater(sum(component_errors), tolerance)


if __name__ == "__main__":
    unittest.main()
