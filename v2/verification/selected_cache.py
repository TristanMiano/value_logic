"""Ordinary two-template reuse, with current native emission on success.

Caches coefficients, not a source certificate or optimality claim. A numerical
screen can trigger fresh fallback; it never supplies a proof by itself.
"""
from dataclasses import dataclass
from fractions import Fraction as Q

from . import native
from .model import InputError
from .producer import Outcome, _compile_selected, _row_data


@dataclass(frozen=True)
class Selected:
    action: str
    directions: tuple
    branches: tuple


def from_outcome(evidence, query, outcome):
    if outcome.proof is None or len(outcome.templates) != 2:
        raise InputError('Two native scientific templates are required.')
    rows = _row_data(native.context(evidence))
    return Selected(query.action, tuple((a, b) for a, b, _ in rows),
                    tuple((indices, weights) for indices, weights, _ in outcome.templates))


def replay(evidence, query, selected):
    evidence.validate(); query.validate()
    ctx = native.context(evidence)
    rows = _row_data(ctx)
    if selected.action != query.action or selected.directions != tuple((a, b) for a, b, _ in rows):
        return Outcome('unavailable', 'selected_schema_changed', None, None, 0, 0)
    if len(selected.branches) != 2:
        raise InputError('Exactly two sign templates are required.')
    costs = tuple(c for _, _, c in rows)+(Q(0), Q(0))
    candidates = []
    for indices, weights in selected.branches:
        if len(indices) != 3 or len(weights) != 3 or any(type(i) is not int or not 0 <= i < len(costs) for i in indices):
            raise InputError('Malformed selected template.')
        if any(isinstance(w, bool) or not isinstance(w, (int, Q)) or w < 0 for w in weights):
            raise InputError('Invalid selected coefficients.')
        bound = sum((costs[i]*w for i, w in zip(indices, weights)), Q(0))
        candidates.append((indices, weights, bound))
    bound = max(x[2] for x in candidates)+native.PRICE*(native.EVALUATIONS[query.action]-native.EVALUATIONS['F'])
    if bound > query.budget:
        # No native proof has been emitted/received here. Do not advertise an
        # unchecked upper bound or refutation from the numeric screen alone.
        return Outcome('unavailable', 'selected_screen_fallback', None, None, 0, 2)
    return _compile_selected(ctx, query, rows, candidates, 0, 2, 128)
