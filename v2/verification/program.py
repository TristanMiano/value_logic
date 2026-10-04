"""Optional fixed-program producer using weighted native minimum projections.

The old adaptive and proposed zero-read programs, outcome probabilities and
tail confidence are fixed by this adapter. It is not general program analysis.
"""
from fractions import Fraction as Q
from itertools import combinations

from v2.checks import f06_inference_rules as K
from v2.checks import f07_soundness as A
from .producer import Outcome, _BoundedBuilder, _StepLimit, solve_three
from .program_model import ProgramEvidence, ProgramQuery


def context(evidence: ProgramEvidence):
    evidence.validate()
    e, u = K.src('error'), K.src('second')
    conversions = (K.Conversion('probability_to_loss', 'P', 'L', Q(1)),
                   K.Conversion('probability_to_audit', 'P', 'A', Q(1)))
    rows = [K.Row(K.num(0, 'P'), e), K.Row(e, K.num(evidence.error_cap, 'P')),
            K.Row(K.num(Q(1, 5), 'P'), u), K.Row(u, K.num(evidence.second_cap, 'P'))]
    if evidence.foreign_zero:
        rows.append(K.Row(K.convert('probability_to_audit', e), K.num(0, 'A')))
    return K.context((('error', 'P'), ('second', 'P')), rows, {'error': 0, 'second': Q(1, 5)},
                     scope='F11-two-bit-program-v1', revision=evidence.revision,
                     units=('P', 'L', 'A'), conversions=conversions)


def _probabilities():
    e, u = K.src('error'), K.src('second')
    return K.sub(K.num(Q(1, 2), 'P'), e), e, u, K.sub(K.num(Q(1, 2), 'P'), u)


def _expectation(losses):
    parts = [K.scale(loss, p) for loss, p in zip(losses, _probabilities())]
    total = K.num(0, 'P')
    for part in parts:
        total = K.add(total, part)
    return K.convert('probability_to_loss', total)


def terms(query: ProgramQuery):
    query.validate()
    adaptive = (Q(3, 20), Q(23, 20), Q(3, 10), Q(3, 10))
    if query.kind == 'mean_edit':
        new = _expectation((Q(0), Q(1), Q(1), Q(0)))
        old = _expectation(adaptive)
        return new, old, (new,)
    branches = tuple(K.add(K.num(t, 'L'), K.scale(Q(1)/(Q(1)-Q(query.alpha)),
                     _expectation(tuple(max(value-t, Q(0)) for value in adaptive))))
                     for t in sorted(set(adaptive)))
    new = branches[0]
    for branch in branches[1:]:
        new = K.minimum(new, branch)
    return new, K.num(Q(3, 10), 'L'), branches


def request(ctx, query):
    new, old, _ = terms(query)
    return A.request(ctx, None, new, old, query.budget, 'L')


def _min_projections(builder, branches):
    term = branches[0]
    projections = [builder.constant(term, term)]
    for branch in branches[1:]:
        left = builder.lattice('min_left', term, branch)
        projections = [builder.trans(left, p) for p in projections]
        projections.append(builder.lattice('min_right', term, branch))
        term = K.minimum(term, branch)
    return projections


def produce(evidence: ProgramEvidence, query: ProgramQuery, *, max_bases=35, max_steps=128):
    evidence.validate(); query.validate()
    from .model import InputError
    if type(max_bases) is not int or not 0 <= max_bases <= 35 or type(max_steps) is not int or not 0 <= max_steps <= 128:
        raise InputError('Program-adapter limits are 0..35 bases and 0..128 steps.')
    ctx = context(evidence)
    new, old, branches = terms(query)
    # Rows in A cannot reach L. P rows have the declared positive conversion.
    accessible = []
    for index in range(len(ctx.cases[0].rows)):
        _, budget, unit, direction = K.normalized_row(ctx, 'h', index)
        if unit == 'P':
            coeff = dict(direction)
            accessible.append((index, coeff.get('error', Q(0)), coeff.get('second', Q(0)), budget))
    branch_forms = [K.affine(branch, ctx.signature) for branch in branches]
    old_coeff, old_offset = K.affine(old, ctx.signature)
    columns = tuple((a, b, Q(0)) for _, a, b, _ in accessible) + tuple(
        (-c.get('error', Q(0)), -c.get('second', Q(0)), Q(1)) for c, _ in branch_forms)
    costs = tuple(budget for _, _, _, budget in accessible) + tuple(c for _, c in branch_forms)
    target = (-old_coeff.get('error', Q(0)), -old_coeff.get('second', Q(0)), Q(1))
    best = None
    checks = feasible = 0
    for indices in combinations(range(len(columns)), 3):
        if checks >= max_bases:
            return Outcome('unavailable', 'program_basis_limit', None, None, checks, feasible)
        checks += 1
        weights = solve_three(tuple(columns[i] for i in indices), target)
        if weights is None or any(w < 0 for w in weights):
            continue
        feasible += 1
        bound = sum((costs[i]*w for i, w in zip(indices, weights)), Q(0))-old_offset
        candidate = (bound, indices, weights)
        if best is None or candidate < best:
            best = candidate
    if best is None:
        return Outcome('unavailable', 'no_program_template', None, None, checks, feasible)
    bound, indices, weights = best
    builder = _BoundedBuilder(ctx, max_steps)
    try:
        projections = _min_projections(builder, branches)
        source_parts = []
        projection_parts = []
        offset = Q(0)
        for index, weight in zip(indices, weights):
            if not weight:
                continue
            if index < len(accessible):
                row = builder.row(accessible[index][0])
                source_parts.append(builder.scale(weight, builder.conversion('probability_to_loss', row)))
            else:
                j = index-len(accessible)
                projection_parts.append(builder.scale(weight, projections[j]))
                offset += weight*branch_forms[j][1]
        projection = projection_parts[0]
        for part in projection_parts[1:]:
            projection = builder.add(projection, part)
        mixture = builder.steps[projection].old
        projection = builder.rewrite(projection, new, mixture)
        row_bound = builder.constant(K.num(offset-old_offset, 'L'), K.num(0, 'L'))
        for part in source_parts:
            row_bound = builder.add(row_bound, part)
        row_bound = builder.rewrite(row_bound, mixture, old)
        root = builder.trans(projection, row_bound)
        root = builder.rewrite(root, new, old)
        root = builder.all_cases((root,))
        proof = builder.proof(root)
    except _StepLimit:
        return Outcome('unavailable', 'program_step_limit', None, None, checks, feasible)
    expected = request(ctx, query) if bound <= query.budget else A.request(ctx, None, new, old, bound, 'L')
    root = A.receive(ctx, proof, expected)
    if root.budget != bound:
        raise AssertionError('Program template bound differs from its checked root.')
    if bound <= query.budget:
        return Outcome('certified', 'program_received', proof, bound, checks, feasible, (best,))
    return Outcome('unavailable', 'program_bound_exceeds_request', proof, bound, checks, feasible, (best,))
