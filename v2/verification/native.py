"""Encode the declared scientific contract using the existing typed AST."""
from fractions import Fraction as Q

from v2.checks import f06_inference_rules as K
from v2.checks import f07_soundness as A
from .model import Evidence, Query

SCOPE = 'F11-N01-quartic-loss-v1'
ERRORS = {'T1': (Q(1), Q(1)), 'T2': (Q(1, 4), Q(1, 16)),
          'R': (Q(0), Q(-1, 4)), 'F': (Q(1, 16), Q(1, 256))}
EVALUATIONS = {'T1': 2, 'T2': 3, 'R': 3, 'F': 5}
PRICE = Q(1, 32)


def linear(a, b):
    return K.add(K.scale(a, K.src('beta')), K.scale(b, K.src('gamma')))


def loss(action):
    return K.add(K.absolute(linear(*ERRORS[action])),
                 K.num(PRICE * EVALUATIONS[action]))


def context(evidence: Evidence):
    evidence.validate()
    rows = [K.Row(linear(a, b), K.num(1))
            for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))]
    if evidence.plus is not None:
        rows.append(K.Row(linear(1, 1), K.num(evidence.plus)))
    if evidence.minus is not None:
        rows.append(K.Row(linear(-1, -1), K.num(evidence.minus)))
    for cap, directions in ((evidence.beta, ((1, 0), (-1, 0))),
                            (evidence.gamma, ((0, 1), (0, -1)))):
        if cap is not None:
            rows.extend(K.Row(linear(a, b), K.num(cap)) for a, b in directions)
    return K.context(('beta', 'gamma'), rows, {'beta': 0, 'gamma': 0},
                     scope=SCOPE, revision=evidence.revision)


def request(ctx, query: Query):
    query.validate()
    # Constructed from the consumer's declared query, never from a proof root.
    return A.request(ctx, None, loss(query.action), loss('F'), query.budget)


def bound_request(ctx, action, bound):
    """Internal receipt for derived arithmetic, not a new external input.

    Adding admitted rationals can exceed an individual input's 256-bit size.
    The existing receiver still checks exactness, terms and the bound itself.
    """
    Query(action).validate()
    return A.request(ctx, None, loss(action), loss('F'), K.rat(bound))
