"""Optional ordinary preprocessing of fixed-direction dual templates.

The catalogue reuses arithmetic coefficients, not old source receipts. Every
answer is compiled and checked in the current context. The baseline is equally
entitled to this optimization. Construction, storage and selection are separate
costs; this is not a retention-subset optimizer.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations

from . import native
from .model import InputError
from .producer import Outcome, _compile_selected, _row_data, solve_three


@dataclass(frozen=True)
class Catalogue:
    action: str
    directions: tuple
    branches: tuple
    build_basis_checks: int
    complete: bool  # Exhausted this fixed template list, not a general optimality theorem.

    @property
    def template_count(self):
        return sum(len(branch) for branch in self.branches)


@dataclass(frozen=True)
class Selection:
    outcome: Outcome
    template_evaluations: int
    catalogue_complete: bool


def build(evidence, query, *, max_bases=440):
    evidence.validate(); query.validate()
    if type(max_bases) is not int or not 0 <= max_bases <= 440:
        raise InputError('Catalogue construction is limited to 0..440 bases.')
    rows = _row_data(native.context(evidence))
    directions = tuple((a, b) for a, b, _ in rows)
    v = native.ERRORS['F']
    columns = tuple((a, b, Q(0)) for a, b in directions) + (
        (v[0], v[1], Q(1)), (-v[0], -v[1], Q(1)))
    u = native.ERRORS[query.action]
    branches = []
    checks = 0
    complete = True
    for sign in (1, -1):
        templates = []
        for indices in combinations(range(len(columns)), 3):
            if checks >= max_bases:
                complete = False
                break
            checks += 1
            weights = solve_three(tuple(columns[i] for i in indices),
                                  (sign*u[0], sign*u[1], Q(1)))
            if weights is not None and all(w >= 0 for w in weights):
                templates.append((indices, weights))
        branches.append(tuple(templates))
    return Catalogue(query.action, directions, tuple(branches), checks, complete)


def select(evidence, query, catalogue, *, max_evaluations=440, max_steps=128):
    evidence.validate(); query.validate()
    if type(max_evaluations) is not int or not 0 <= max_evaluations <= 440 or type(max_steps) is not int or not 0 <= max_steps <= 128:
        raise InputError('Catalogue selection limits are 0..440 evaluations and 0..128 steps.')
    ctx = native.context(evidence)
    rows = _row_data(ctx)
    if catalogue.action != query.action or catalogue.directions != tuple((a, b) for a, b, _ in rows):
        return Selection(Outcome('unavailable', 'catalogue_schema_mismatch', None, None, 0, 0), 0, False)
    if len(catalogue.branches) != 2 or catalogue.template_count > 440:
        raise InputError('Malformed or excessive catalogue.')
    costs = tuple(c for _, _, c in rows) + (Q(0), Q(0))
    chosen = []
    evaluations = 0
    for branch in catalogue.branches:
        best = None
        for indices, weights in branch:
            if evaluations >= max_evaluations:
                return Selection(Outcome('unavailable', 'catalogue_selection_limit', None, None, 0, 0), evaluations, catalogue.complete)
            evaluations += 1
            if (len(indices) != 3 or len(weights) != 3
                    or any(type(i) is not int or not 0 <= i < len(costs) for i in indices)
                    or any(isinstance(w, bool) or not isinstance(w, (int, Q)) or w < 0 for w in weights)):
                raise InputError('Malformed catalogue candidate.')
            budget = sum((costs[i]*w for i, w in zip(indices, weights)), Q(0))
            candidate = (indices, weights, budget)
            if best is None or (budget, indices) < (best[2], best[0]):
                best = candidate
        if best is None:
            return Selection(Outcome('unavailable', 'catalogue_missing_sign', None, None, 0, 0), evaluations, catalogue.complete)
        chosen.append(best)
    outcome = _compile_selected(ctx, query, rows, chosen, 0, catalogue.template_count, max_steps)
    return Selection(outcome, evaluations, catalogue.complete)
