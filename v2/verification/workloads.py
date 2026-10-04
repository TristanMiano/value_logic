"""Declared F12 development workloads; no native answers or proof imports.

Codex (GPT-6), 2026-10-03. These generators are fixed before comparison runs.
They extend earlier N01 development cases and are not held-out evaluation data.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product
import random

from .model import Evidence, Query

SEED = 20261003
JOINT = (Q(0), Q(1, 16), Q(1, 4), Q(1), Q(2), None)
CAP = (Q(0), Q(1, 64), Q(1, 4), Q(1), None)
ACTIONS = ('T1', 'T2', 'R')


def sources(family):
    """900 grid, 257 seeded rational, 9 boundary and 4 off-grid sources."""
    if family == 'grid':
        values = tuple(product(JOINT, JOINT, CAP, CAP))
    elif family == 'rational':
        rng = random.Random(SEED)
        values = tuple(tuple(None if (i >> j) & 1 else
                             Q(rng.randrange(limit + 1), 997)
                             for j, limit in enumerate((1994, 1994, 997, 997)))
                       for i in range(257))
    elif family == 'boundary':
        values = tuple(state for offset in (-Q(1, 1024), Q(0), Q(1, 1024))
                       for state in ((Q(3, 32)+offset, Q(3, 32)+offset, Q(1), Q(1)),
                                     (None, None, Q(1, 48)+offset, Q(1)),
                                     (None, None, Q(1), Q(1, 4)+offset)))
    elif family == 'offgrid':
        values = ((Q(8, 85), Q(8, 85), Q(0), Q(1)),
                  (Q(1, 10), Q(1, 10), Q(1), Q(0)),
                  (Q(2), Q(2), Q(0), Q(16, 63)),
                  (Q(0), Q(0), Q(1), Q(16, 49)))
    else:
        raise ValueError('Unknown F12 workload family.')
    return tuple(Evidence(*state, revision=f'f12-{family}-{i:04d}')
                 for i, state in enumerate(values))


@dataclass(frozen=True)
class Revision:
    name: str
    old: Evidence
    new: Evidence
    relation: str  # declared source-set direction, or incomparable/same


def revisions():
    """Twenty-four controlled revisions, three actions each; no random order."""
    result = []
    for i, (b, g) in enumerate(((Q(0), Q(0)), (Q(1, 64), Q(1, 4)),
                               (Q(1, 4), Q(1)), (Q(1), Q(1)))):
        old = Evidence(beta=b, gamma=g, revision=f'old-{i}')
        candidates = (
            ('version', Evidence(beta=b, gamma=g), 'same'),
            ('strengthen', Evidence(beta=b/2, gamma=g/2), 'subset'),
            ('relax', Evidence(beta=(1+b)/2, gamma=(1+g)/2), 'superset'),
            ('withdraw-beta', Evidence(gamma=g), 'superset'),
            ('withdraw-all', Evidence(), 'superset'),
            ('joint-alternative', Evidence(Q(0), Q(0), b, None), 'incomparable'),
        )
        for name, new, relation in candidates:
            new = Evidence(*new.bounds, revision=f'new-{i}-{name}')
            result.append(Revision(f'{i}-{name}', old, new, relation))
    return tuple(result)


def sequence(name, cycles=1):
    """Fixed query order, charged initial event, and reproducible revisions."""
    if type(cycles) is not int or not 1 <= cycles <= 4:
        raise ValueError('Sequence cycles must be in 1..4.')
    if name == 'fixed-directions':
        states = ((Q(0), Q(0)), (Q(0), Q(8, 85)), (Q(1, 64), Q(1, 4)),
                  (Q(1, 4), Q(1)), (Q(0), Q(0)), (Q(1), Q(1)))
        base = tuple(Evidence(beta=b, gamma=g) for b, g in states)
    elif name == 'withdrawals':
        base = (Evidence(0, 0, 0, 0), Evidence(beta=0, gamma=Q(8, 85)),
                Evidence(gamma=Q(1, 4)), Evidence(), Evidence(beta=0),
                Evidence(0, 0, 0, 0))
    elif name == 'stable-revisions':
        base = (Evidence(beta=Q(1, 64), gamma=Q(1, 4)),)*6
    else:
        raise ValueError('Unknown F12 sequence.')
    return tuple((Evidence(*e.bounds, revision=f'{name}-{cycle}-{i}'), Query(action))
                 for cycle in range(cycles) for i, e in enumerate(base)
                 for action in ACTIONS)
