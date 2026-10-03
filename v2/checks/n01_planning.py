"""Exact N01 planning probes; not the F11 native producer or benchmark.

Codex (GPT-6), 2026-10-02. Run: python -m v2.checks.n01_planning
The geometric oracle enumerates the arrangement of source boundaries and
absolute-value break lines, independently of the derived closed forms.
"""

from fractions import Fraction as Q
from itertools import combinations, product
import json
import random


ERRORS = ((Q(1), Q(1)), (Q(1, 4), Q(1, 16)), (Q(0), Q(-1, 4)))
FALLBACK = (Q(1, 16), Q(1, 256))
PRICES = (Q(-3, 32), Q(-1, 16), Q(-1, 16))


def source_rows(state):
    """Unmerged original source rows, preserving optional evidence slots."""
    plus, minus, beta, gamma = state
    rows = [(Q(1), Q(0), Q(1)), (Q(-1), Q(0), Q(1)),
            (Q(0), Q(1), Q(1)), (Q(0), Q(-1), Q(1))]
    if plus is not None:
        rows.append((Q(1), Q(1), plus))
    if minus is not None:
        rows.append((Q(-1), Q(-1), minus))
    if beta is not None:
        rows.extend([(Q(1), Q(0), beta), (Q(-1), Q(0), beta)])
    if gamma is not None:
        rows.extend([(Q(0), Q(1), gamma), (Q(0), Q(-1), gamma)])
    return rows


def geometric_reference(state, action):
    rows = source_rows(state)
    u, v = ERRORS[action], FALLBACK
    lines = rows + [(u[0], u[1], Q(0)), (v[0], v[1], Q(0))]
    candidates = {(Q(0), Q(0))}
    for (a, b, c), (d, e, f) in combinations(lines, 2):
        det = a * e - b * d
        if not det:
            continue
        point = ((c * e - b * f) / det, (a * f - c * d) / det)
        if all(r * point[0] + s * point[1] <= t for r, s, t in rows):
            candidates.add(point)
    scored = [(abs(u[0] * x + u[1] * y)
               - abs(v[0] * x + v[1] * y) + PRICES[action], (x, y))
              for x, y in candidates]
    return max(scored)


def canonical(state):
    plus, minus, beta, gamma = state
    b = Q(1) if beta is None else min(Q(1), beta)
    g = Q(1) if gamma is None else min(Q(1), gamma)
    r = max(Q(2) if plus is None else plus,
            Q(2) if minus is None else minus)
    return b, g, r


def affine_forms(b, g, r):
    return ((256 * r, 255 * r + 15 * b, 240 * r + 15 * g, 240 * b + 255 * g),
            (48 * b + 15 * g, 33 * b + 15 * r, 48 * r + 33 * g),
            (64 * g, 63 * g + 16 * b, 49 * g + 16 * r,
             79 * b + 63 * r, 49 * b + 65 * r))


def derived_bounds(state):
    m1, m2, mr = map(min, affine_forms(*canonical(state)))
    return ((m1 - 24) / 256, (m2 - 16) / 256, (mr - 16) / 256)


def choice(bounds, thresholds=(24, 16, 16), order=(0, 1, 2)):
    return next((i for i in order if bounds[i] <= thresholds[i]), 3)


def policy_check(state):
    forms = affine_forms(*canonical(state))
    complete = tuple(map(min, forms))
    retained = (complete[0], complete[1], min(forms[2][0], forms[2][2]))
    for price in (Q(1, 512), Q(1, 32), Q(1, 4), Q(1)):
        thresholds = (768 * price, 512 * price, 512 * price)
        assert choice(complete, thresholds) == choice(retained, thresholds), (state, price)


def verify_retention_claims():
    """Rational boundary witnesses plus an oracle independent of the envelopes."""
    witnesses = (
        (0, 0, Q(1, 2), Q(1, 2), Q(3, 32)),
        (0, 1, Q(1, 320), Q(1, 2), Q(511, 5440)),
        (0, 2, Q(1, 2), Q(1, 20), Q(31, 320)),
        (0, 3, Q(1, 32), Q(11, 170), Q(1)),
        (1, 0, Q(17, 96), Q(1, 2), Q(1)),
        (1, 1, Q(113, 264), Q(3, 4), Q(1, 8)),
        (1, 2, Q(3, 4), Q(10, 33), Q(1, 8)),
        (2, 0, Q(1, 2), Q(1, 4), Q(1)),
        (2, 1, Q(1, 128), Q(127, 504), Q(1)),
        (2, 2, Q(1, 2), Q(15, 49), Q(1, 16)),
        (2, 3, Q(1, 128), Q(1, 2), Q(1969, 8064)),
        (2, 4, Q(191, 784), Q(1, 2), Q(1, 16)),
    )
    for action, index, b, g, r in witnesses:
        assert 0 < b < 1 and 0 < g < 1 and 0 < r < 2
        forms = affine_forms(b, g, r)
        threshold = (24, 16, 16)[action]
        assert forms[action][index] == threshold
        assert all(value > threshold for i, value in enumerate(forms[action]) if i != index)
        assert geometric_reference((r, r, b, g), action)[0] == 0
        if action == 1:
            assert min(forms[0]) > 24  # T2 witnesses survive the priority policy.
            assert min(forms[2]) > 16  # Also survive the reversed R/T2 order.

    # D22's additional R witness and D24's reversed-priority witness.
    for index, b, g, r in ((2, Q(1, 2), Q(13, 50), Q(163, 800)),
                          (4, Q(9, 56), Q(1, 2), Q(1, 8))):
        forms = affine_forms(b, g, r)
        assert forms[2][index] == 16
        assert all(value > 16 for i, value in enumerate(forms[2]) if i != index)
        assert min(forms[0]) > 24
        assert geometric_reference((r, r, b, g), 2)[0] == 0
        if index == 2:
            assert min(forms[1]) == Q(459, 25) > 16
        policy_check((r, r, b, g))

    # Four true continuum answers missed by the grid-optimal eight-form subset.
    for action, b, g, r in ((0, Q(0), Q(1), Q(8, 85)),
                            (0, Q(1), Q(0), Q(1, 10)),
                            (2, Q(0), Q(16, 63), Q(2)),
                            (2, Q(1), Q(16, 49), Q(0))):
        forms = affine_forms(b, g, r)
        indices = (0, 3) if action == 0 else (0, 3, 4)
        threshold = (24, 16, 16)[action]
        assert min(forms[action]) == threshold
        assert min(forms[action][i] for i in indices) > threshold
        assert geometric_reference((r, r, b, g), action)[0] == 0

    # Current answers do not suffice for delta revisions (D20).
    r0, r1, delta = Q(0), Q(4, 85), Q(8, 85)
    assert verify_state((r0, r0, Q(0), Q(1))) == verify_state((r1, r1, Q(0), Q(1)))
    assert verify_state((r0+delta, r0+delta, Q(0), Q(1)))[0]
    assert not verify_state((r1+delta, r1+delta, Q(0), Q(1)))[0]
    return len(witnesses)


def verify_state(state):
    predicted = derived_bounds(state)
    for action in range(3):
        actual, witness = geometric_reference(state, action)
        if actual != predicted[action]:
            raise AssertionError((state, action, actual, predicted[action], witness))
    return tuple(bound <= 0 for bound in predicted)


def direct_trapezoid(beta, gamma, n):
    b, c = 6 * beta + 60 * gamma, -30 * gamma
    def f(t):
        return Q(7, 3) - Q(2, 5) * t + b * t**2 + c * t**4
    estimate = ((f(Q(0)) + f(Q(1))) / 2
                + sum(f(Q(k, n)) for k in range(1, n))) / n
    integral = Q(7, 3) - Q(1, 5) + b / 3 + c / 5
    return estimate - integral


def run_checks():
    polynomial_cases = 0
    for beta, gamma in product((Q(-1), Q(-1, 7), Q(0), Q(1, 11), Q(1)), repeat=2):
        for n in (1, 2, 4, 8):
            assert direct_trapezoid(beta, gamma, n) == beta / n**2 + gamma / n**4
            polynomial_cases += 1
        assert (4 * direct_trapezoid(beta, gamma, 2)
                - direct_trapezoid(beta, gamma, 1)) / 3 == -gamma / 4

    cpwa_cases = 0
    for u, v, k in product((Q(-3), Q(-1, 2), Q(0), Q(1, 3), Q(2)), repeat=3):
        assert abs(u) - abs(v) + k == max(min(u-v+k, u+v+k),
                                         min(-u-v+k, -u+v+k))
        cpwa_cases += 1

    joint = (Q(0), Q(1, 16), Q(1, 4), Q(1), Q(2), None)
    cap = (Q(0), Q(1, 64), Q(1, 4), Q(1), None)
    choices = set()
    grid_states = 0
    for state in product(joint, joint, cap, cap):
        answers = verify_state(state)
        policy_check(state)
        forms = affine_forms(*canonical(state))
        grid_vector = (min(forms[0][i] for i in (0, 3)), min(forms[1]),
                       min(forms[2][i] for i in (0, 3, 4)))
        assert tuple(x <= t for x, t in zip(grid_vector, (24, 16, 16))) == answers
        grid_policy = (grid_vector[0], grid_vector[1], forms[2][0])
        assert choice(grid_policy) == choice(tuple(map(min, forms)))
        choices.add(next((i for i, good in enumerate(answers) if good), 3))
        grid_states += 1
    assert choices == {0, 1, 2, 3}

    rng = random.Random(20261002)
    for index in range(257):
        state = tuple(None if (index >> slot) & 1 else Q(rng.randrange(limit + 1), 64)
                      for slot, limit in enumerate((128, 128, 64, 64)))
        verify_state(state)
        policy_check(state)

    # Exact equality and rational perturbations on both sides: no epsilon tolerance.
    delta = Q(1, 1024)
    for offset in (-delta, Q(0), delta):
        boundary_states = ((Q(3, 32)+offset, Q(3, 32)+offset, Q(1), Q(1)),
                           (None, None, Q(1, 48)+offset, Q(1)),
                           (None, None, Q(1), Q(1, 4)+offset))
        for action, state in enumerate(boundary_states):
            answers = verify_state(state)
            policy_check(state)
            assert answers[action] == (offset <= 0)
            if not offset:
                assert derived_bounds(state)[action] == 0

    # D11's countermodels demonstrate that parameter vertices alone do not suffice.
    assert min(2 * Q(3, 8), Q(3, 8) + Q(3, 4)) == Q(3, 4)
    assert Q(3, 8) + Q(3, 4) == Q(9, 8)
    assert min(2 * Q(1, 2), 2 - 2 * Q(1, 2)) == 1
    threshold_witnesses = verify_retention_claims()
    # Exact centered moments avoid approximating the irrational Gaussian nodes.
    for degree in range(6):
        observed = (2 * Q(5, 18) * Q(3, 20)**(degree // 2)
                    + (Q(4, 9) if degree == 0 else Q(0))) if degree % 2 == 0 else Q(0)
        integral = Q(1, 2**degree * (degree + 1)) if degree % 2 == 0 else Q(0)
        assert observed == integral
    assert Q(1, 12)**2 - Q(1, 80) == Q(-1, 180)
    return {"polynomial_error_checks": polynomial_cases,
            "richardson_checks": 25, "cpwa_identity_checks": cpwa_cases,
            "exhaustive_development_states": grid_states,
            "seeded_rational_states": 257, "seed": 20261002,
            "boundary_states": 9, "queries_per_state": 3,
            "uniform_threshold_interior_witnesses": threshold_witnesses,
            "additional_priority_witnesses": 2, "grid_portfolio_off_grid_failures": 4,
            "policy_prices_per_main_state": 4, "gaussian_moment_checks": 7,
            "operational_choices_observed": sorted(choices),
            "scope": "N01 planning arithmetic; no native certificates or timing benchmark"}


if __name__ == "__main__":
    print(json.dumps(run_checks(), indent=2))
