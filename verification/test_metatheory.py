"""Finite regression witnesses for the Task 14 metatheory.

These tests check the small cardinality and separation countermodels.  They are
not a substitute for the proofs in ``formalism/08_metatheory.md``.
"""

from __future__ import annotations

from itertools import product
import math
import unittest

from verification.kernel import AtomValue, Interval, Outcome, assess_upper_bound


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

    def test_seven_vectors_have_concrete_region_atom_witnesses(self) -> None:
        regions = (
            (Interval(0.21, 0.22), Interval(0.21, 0.22)),
            (Interval(0.06, 0.07), Interval(0.19, 0.21)),
            (Interval(0.15, 0.18), Interval(0.15, 0.18)),
            (None, Interval(0.21, 0.22)),
            (None, None),
            (Interval(0.04, 0.06), Interval(0.04, 0.06)),
            (Interval(0.04, 0.05), Interval(0.04, 0.05)),
        )
        realized = {
            (
                assess_upper_bound("a", strict, 0.05, "ka", ("ka",)).value,
                assess_upper_bound("b", weak, 0.20, "kb", ("kb",)).value,
            )
            for strict, weak in regions
        }
        expected = {
            (AtomValue.REFUTED, AtomValue.REFUTED),
            (AtomValue.REFUTED, AtomValue.OPEN),
            (AtomValue.REFUTED, AtomValue.SUPPORTED),
            (AtomValue.OPEN, AtomValue.REFUTED),
            (AtomValue.OPEN, AtomValue.OPEN),
            (AtomValue.OPEN, AtomValue.SUPPORTED),
            (AtomValue.SUPPORTED, AtomValue.SUPPORTED),
        }
        self.assertEqual(realized, expected)

    def test_missing_profile_refinement_has_a_finite_separator(self) -> None:
        # Only atom 0 entails atom 1.  Requiring atom 1 therefore does not
        # syntactically refine a profile requiring atom 0.
        separator = (AtomValue.OPEN, AtomValue.SUPPORTED)
        self.assertTrue(respects_support_refinements(separator, ((0, 1),)))
        self.assertEqual(profile_outcome(separator, (1,)), Outcome.GRANTED)
        self.assertEqual(profile_outcome(separator, (0,)), Outcome.WITHHELD)

if __name__ == "__main__":
    unittest.main()
