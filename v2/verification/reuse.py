"""Rebuild one old receipt from current row proofs, without fresh query search.

Ordinary conic combinations of one/two current rows replace old directions.
The reviewed transport recalculates all budgets and the receiver binds the
current query. This is a specified reuse strategy, not optimal retention.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations

from v2.checks import f06_inference_rules as K
from v2.checks import f06_source_transport as T
from v2.checks import f07_soundness as A
from .model import Evidence, InputError, Query
from .producer import _row_data
from . import native, receipts


@dataclass(frozen=True)
class ReuseLimits:
    # At most ten used old rows; each considers ten singleton and 45 pair
    # replacements. The step cap is an output refusal after native transport,
    # not a streaming allocation bound on the inherited transport procedure.
    max_row_candidates: int = 550
    max_steps: int = 128

    def validate(self):
        for value, maximum in ((self.max_row_candidates, 550), (self.max_steps, 128)):
            if type(value) is not int or not 0 <= value <= maximum:
                raise InputError('Reuse limits exceed this fixed fragment.')


@dataclass(frozen=True)
class ReuseOutcome:
    status: str
    reason: str
    proof: K.Proof | None
    upper_bound: Q | None
    row_candidate_checks: int
    replacement_count: int
    templates: tuple = ()


def _row_template(rows, direction, remaining):
    candidates = []
    checked = 0
    for indices in tuple((i,) for i in range(len(rows))) + tuple(combinations(range(len(rows)), 2)):
        if checked >= remaining:
            return None, checked, True
        checked += 1
        if len(indices) == 1:
            a, b, _ = rows[indices[0]]
            component = 0 if a else 1
            denominator = a if component == 0 else b
            if not denominator:
                continue
            weight = direction[component] / denominator
            if weight < 0 or (weight*a, weight*b) != direction:
                continue
            weights = (weight,)
        else:
            a, b, _ = rows[indices[0]]
            c, d, _ = rows[indices[1]]
            determinant = a*d-b*c
            if not determinant:
                continue
            weights = ((direction[0]*d-direction[1]*c)/determinant,
                       (a*direction[1]-b*direction[0])/determinant)
            if any(w < 0 for w in weights):
                continue
        budget = sum((rows[i][2]*w for i, w in zip(indices, weights)), Q(0))
        candidates.append((budget, indices, weights))
    return (min(candidates) if candidates else None), checked, False


def reuse(evidence: Evidence, query: Query, payload, limits: ReuseLimits = ReuseLimits()):
    """Attempt only replay/reconstruction; callers choose fresh fallback explicitly."""
    evidence.validate(); query.validate(); limits.validate()
    old_evidence, old_action, proof = receipts.decode_receipt(payload)
    if old_action != query.action:
        return ReuseOutcome('unavailable', 'query_changed', None, None, 0, 0)
    old, new = native.context(old_evidence), native.context(evidence)
    rows = _row_data(new)
    replacements = {}
    checked = 0
    templates = []
    for case, index in sorted(T.used_rows(old, proof)):
        _, _, _, sparse = K.normalized_row(old, case, index)
        coefficients = dict(sparse)
        direction = (coefficients.get('beta', Q(0)), coefficients.get('gamma', Q(0)))
        candidate, count, exhausted = _row_template(rows, direction, limits.max_row_candidates-checked)
        checked += count
        if exhausted:
            return ReuseOutcome('unavailable', 'row_replacement_limit', None, None, checked, len(templates))
        if candidate is None:
            return ReuseOutcome('unavailable', 'missing_row_replacement', None, None, checked, len(templates))
        budget, indices, weights = candidate
        builder = K.Builder(new, 'h')
        parts = [builder.scale(weight, builder.row(i)) for i, weight in zip(indices, weights) if weight]
        if not parts:
            root = builder.constant(K.num(0), K.num(0))
        else:
            root = parts[0]
            for part in parts[1:]:
                root = builder.add(root, part)
        root = builder.rewrite(root, native.linear(*direction), K.num(0))
        replacements[('h', case, index)] = builder.proof(root)
        templates.append((index, candidate))
    try:
        current = T.transport(old, new, proof, replacements, {'h': 'h'})
    except T.UnavailableProof:
        return ReuseOutcome('unavailable', 'no_retained_reconstruction', None, None, checked, len(templates))
    if len(current.steps) > limits.max_steps:
        return ReuseOutcome('unavailable', 'reused_step_limit', None, None, checked, len(templates))
    root = K.check(new, current)
    A.receive(new, current, native.bound_request(new, query.action, root.budget))
    if root.budget <= query.budget:
        A.receive(new, current, native.request(new, query))
        status, reason = 'certified', 'reused_received'
    else:
        status, reason = 'unavailable', 'reused_bound_exceeds_request'
    return ReuseOutcome(status, reason, current, root.budget, checked, len(templates), tuple(templates))
