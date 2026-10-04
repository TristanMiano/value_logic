"""Purpose-built dual-template enumeration and native proof emission.

Two coordinates and the fixed absolute-value comparison only. No semantic
reference or closed-form answer table is imported. Search exhaustion means
unavailable; it never establishes refutation or an optimality theorem.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations

from v2.checks import f06_inference_rules as K
from v2.checks import f07_soundness as A
from .model import Evidence, InputError, Query
from . import native


@dataclass(frozen=True)
class Limits:
    # At most ten source rows plus two absolute-value projections:
    # two signs times C(12, 3) = 440 candidate bases.
    max_basis_checks: int = 440
    max_steps: int = 128

    def validate(self):
        for value in (self.max_basis_checks, self.max_steps):
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise InputError('Search limits must be nonnegative integers.')
        if self.max_basis_checks > 440 or self.max_steps > 128:
            raise InputError('Limits exceed this bounded compiler contract.')


@dataclass(frozen=True)
class Outcome:
    status: str
    reason: str
    proof: K.Proof | None
    upper_bound: Q | None
    basis_checks: int
    feasible_bases: int
    # Source indices and convex weights document the ordinary certificate.
    templates: tuple = ()


class _StepLimit(Exception):
    pass


class _BoundedBuilder(K.Builder):
    def __init__(self, ctx, maximum):
        super().__init__(ctx, 'h')
        self.maximum = maximum

    def emit(self, *args, **kwargs):
        if len(self.steps) >= self.maximum:
            raise _StepLimit
        return super().emit(*args, **kwargs)


def solve_three(columns, target):
    """Tiny exact Gaussian elimination, only for three template columns."""
    matrix = [[Q(columns[j][i]) for j in range(3)] + [Q(target[i])]
              for i in range(3)]
    for col in range(3):
        pivot = next((r for r in range(col, 3) if matrix[r][col]), None)
        if pivot is None:
            return None
        matrix[col], matrix[pivot] = matrix[pivot], matrix[col]
        divisor = matrix[col][col]
        matrix[col] = [x / divisor for x in matrix[col]]
        for row in range(3):
            if row != col:
                factor = matrix[row][col]
                matrix[row] = [x - factor * y
                               for x, y in zip(matrix[row], matrix[col])]
    return tuple(matrix[i][3] for i in range(3))


def _row_data(ctx):
    result = []
    for index in range(len(ctx.cases[0].rows)):
        _, budget, unit, direction = K.normalized_row(ctx, 'h', index)
        if unit != 'U':
            raise InputError('This compiler admits only the frozen one-unit source.')
        coefficients = dict(direction)
        if set(coefficients) - {'beta', 'gamma'}:
            raise InputError('Unexpected coordinate.')
        result.append((coefficients.get('beta', Q(0)),
                       coefficients.get('gamma', Q(0)), budget))
    return tuple(result)


def _emit_branch(builder, rows, template, signed_error):
    indices, weights, _ = template
    count = len(rows)
    parts = []
    fallback = native.linear(*native.ERRORS['F'])
    opposite = K.scale(-1, fallback)
    for index, weight in zip(indices, weights):
        if not weight:
            continue
        if index < count:
            root = builder.row(index)
        else:
            kind = 'max_left' if index == count else 'max_right'
            root = builder.lattice(kind, fallback, opposite)
        parts.append(builder.scale(weight, root))
    if not parts:
        raise AssertionError('A template must have convex weights summing to one.')
    root = parts[0]
    for part in parts[1:]:
        root = builder.add(root, part)
    return builder.rewrite(root, signed_error, K.absolute(fallback))


def produce(evidence: Evidence, query: Query, limits: Limits = Limits()):
    """Return a request-certified result, or explicitly unavailable evidence.

    Even a sound bound that exceeds the consumer's requested budget is marked
    unavailable for that request. Its bound certificate remains inspectable.
    Only the independent semantic route may supply a refuting full-source point.
    """
    evidence.validate(); query.validate(); limits.validate()
    ctx = native.context(evidence)
    rows = _row_data(ctx)
    v = native.ERRORS['F']
    columns = tuple((a, b, Q(0)) for a, b, _ in rows) + (
        (v[0], v[1], Q(1)), (-v[0], -v[1], Q(1)))
    costs = tuple(c for _, _, c in rows) + (Q(0), Q(0))
    checks = feasible = 0
    chosen = []
    u = native.ERRORS[query.action]
    for sign in (1, -1):
        best = None
        for indices in combinations(range(len(columns)), 3):
            if checks >= limits.max_basis_checks:
                return Outcome('unavailable', 'basis_limit', None, None, checks, feasible)
            checks += 1
            weights = solve_three(tuple(columns[i] for i in indices),
                                  (sign * u[0], sign * u[1], Q(1)))
            if weights is None or any(w < 0 for w in weights):
                continue
            feasible += 1
            budget = sum((costs[i] * w for i, w in zip(indices, weights)), Q(0))
            candidate = (indices, weights, budget)
            if best is None or (budget, indices) < (best[2], best[0]):
                best = candidate
        if best is None:
            return Outcome('unavailable', 'no_template', None, None, checks, feasible)
        chosen.append(best)
    return _compile_selected(ctx, query, rows, chosen, checks, feasible, limits.max_steps)


def _compile_selected(ctx, query, rows, chosen, checks, feasible, max_steps):
    """Compile supplied candidate coefficients; only the receiver grants acceptance."""
    expected = native.request(ctx, query)
    u = native.ERRORS[query.action]
    builder = _BoundedBuilder(ctx, max_steps)
    try:
        error = native.linear(*u)
        positive = _emit_branch(builder, rows, chosen[0], error)
        negative = _emit_branch(builder, rows, chosen[1], K.scale(-1, error))
        root = builder.max_common(positive, negative)
        price = builder.constant(K.num(native.PRICE * native.EVALUATIONS[query.action]),
                                 K.num(native.PRICE * native.EVALUATIONS['F']))
        root = builder.rewrite(builder.add(root, price), expected.new, expected.old)
        root = builder.all_cases((root,))
        proof = builder.proof(root)
    except _StepLimit:
        return Outcome('unavailable', 'step_limit', None, None, checks, feasible, tuple(chosen))
    bound = max(t[2] for t in chosen) + native.PRICE * (
        native.EVALUATIONS[query.action] - native.EVALUATIONS['F'])
    # One receiver call checks the trace and independent pair together. The
    # computed metadata must equal the checked root, not merely a weaker bound.
    requested = expected if bound <= query.budget else native.bound_request(ctx, query.action, bound)
    root = A.receive(ctx, proof, requested)
    if root.budget != bound:
        raise AssertionError('Computed bound differs from the checked native root.')
    if bound <= query.budget:
        return Outcome('certified', 'received', proof, bound, checks, feasible, tuple(chosen))
    return Outcome('unavailable', 'bound_exceeds_request', proof, bound,
                   checks, feasible, tuple(chosen))
