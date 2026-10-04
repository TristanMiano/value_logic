"""Strong ordinary analytic baseline from N01, with identical source access.

An answer here is a numerical bound, not a free native receipt. Source reading
and the eventual cost of any requested proof/checking guarantee remain due.
"""
from fractions import Fraction as Q

from .model import Evidence, Query


def analytic_bound(evidence: Evidence, query: Query):
    evidence.validate(); query.validate()
    b = Q(1) if evidence.beta is None else Q(evidence.beta)
    g = Q(1) if evidence.gamma is None else Q(evidence.gamma)
    r = max(Q(2) if evidence.plus is None else Q(evidence.plus),
            Q(2) if evidence.minus is None else Q(evidence.minus))
    forms = {
        'T1': (256*r, 255*r+15*b, 240*r+15*g, 240*b+255*g),
        'T2': (48*b+15*g, 33*b+15*r, 48*r+33*g),
        'R': (64*g, 63*g+16*b, 49*g+16*r, 79*b+63*r, 49*b+65*r),
    }
    deduction = 24 if query.action == 'T1' else 16
    return (min(forms[query.action]) - deduction) / 256
