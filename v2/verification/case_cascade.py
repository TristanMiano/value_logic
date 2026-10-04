"""F13 bounded native searches and staged self-assessment, with honest baselines.

Counterfactual full traces are collected by actually executing every version.
The finite development population is declared, not statistically calibrated.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product, combinations

from v2.checks import f06_inference_rules as K
from v2.checks import f07_soundness as A
from .model import exact, InputError


@dataclass(frozen=True)
class Attempt:
    version: str
    status: str
    bound: Q
    proof_nodes: int
    proof: K.Proof


def context(failures, revision='cascade-1'):
    failures = tuple(failures)
    if not 1 <= len(failures) <= 8 or any(type(f) is not int or f not in (0, 1) for f in failures):
        raise InputError('Use one to eight exact 0/1 failure coordinates.')
    if not isinstance(revision, str) or not 0 < len(revision) <= 128:
        raise InputError('A bounded nonempty revision is required.')
    names = ('x',)+tuple(f'y{i}' for i in range(len(failures)))+('z0', 'z1', 'z2')
    rows = []
    for i, cap in enumerate(failures):
        rows += [K.Row(K.src('x'), K.src(f'y{i}')), K.Row(K.src(f'y{i}'), K.num(cap))]
    rows += [K.Row(K.src('x'), K.src('z0')), K.Row(K.src('z0'), K.src('z1')),
             K.Row(K.src('z1'), K.src('z2')), K.Row(K.src('z2'), K.num(0))]
    return K.context(names, rows, dict.fromkeys(names, 0),
                     scope='F13-reset-search-source-v1', revision=revision)


def chain_proof(ctx, indices):
    builder = K.Builder(ctx, 'h')
    pieces = [builder.row(i) for i in indices]
    root = pieces[0]
    for piece in pieces[1:]:
        root = builder.add(root, piece)
    root = builder.rewrite(root, K.src('x'), K.num(0))
    builder.all_cases((root,))
    return builder.proof()


def run(ctx, slot, budget=Q(0)):
    budget = exact(budget)
    k = (len(ctx.cases[0].rows)-4)//2
    if type(slot) is not int or not 0 <= slot < k:
        raise InputError('Unknown bounded search slot.')
    proof = chain_proof(ctx, (2*slot, 2*slot+1))
    bound = proof.steps[proof.root].budget
    # Audit a valid weaker theorem even when it cannot discharge the requested one.
    if bound <= budget:
        A.receive(ctx, proof, A.request(ctx, None, K.src('x'), K.num(0), budget))
        status = 'certified'
    else:
        A.receive(ctx, proof, A.request(ctx, None, K.src('x'), K.num(0), bound))
        status = 'unavailable'
    return Attempt(f'two-row-slot-{slot}@1', status, bound, len(proof.steps), proof)


def fallback(ctx, budget=Q(0)):
    start = len(ctx.cases[0].rows)-4
    proof = chain_proof(ctx, range(start, start+4))
    A.receive(ctx, proof, A.request(ctx, None, K.src('x'), K.num(0), budget))
    return Attempt('four-row-complete@1', 'certified', Q(0), len(proof.steps), proof)


def ordinary(ctx, budget=Q(0)):
    """Same complete source and current receipt guarantee; inspect row budgets first.

    This is allowed to bypass failed proof attempts. Inspection work is distinct
    from the emitted proof's node count; no wall-clock superiority is asserted.
    """
    k = (len(ctx.cases[0].rows)-4)//2
    for slot in range(k):
        _, cap, _, _ = K.normalized_row(ctx, 'h', 2*slot+1)
        if cap <= budget:
            return run(ctx, slot, budget)
    return fallback(ctx, budget)


def collect(k=3, budget=Q(0), revision='calibration-1'):
    records = {}
    for input_caps in product((0, 1), repeat=k):
        ctx = context(input_caps, revision)
        attempts = tuple(run(ctx, slot, budget) for slot in range(k))
        # Behavior columns come from receiver outcomes, not from copying input_caps.
        observed = tuple(int(a.status != 'certified') for a in attempts)
        records[input_caps] = (observed, attempts, fallback(ctx, budget), ordinary(ctx, budget))
    return records


def deploy(ctx, order, penalty, budget=Q(0)):
    """Actually execute the selected next-stage policy against a current request."""
    penalty = exact(penalty)
    if penalty < 0:
        raise InputError('Negative unresolved penalty.')
    if order is None:
        result = fallback(ctx, budget)
        return Q(result.proof_nodes), False, (result,)
    order = tuple(order)
    if len(set(order)) != len(order):
        raise InputError('Reset cascade repeats a procedure.')
    charge, attempts = Q(0), []
    for slot in order:
        result = run(ctx, slot, budget)
        attempts.append(result)
        charge += result.proof_nodes
        if result.status == 'certified':
            return charge, False, tuple(attempts)
    return charge+penalty, True, tuple(attempts)


def parity_population(k, parity):
    if type(k) is not int or not 1 <= k <= 8 or parity not in (0, 1):
        raise InputError('Bounded Boolean population required.')
    return {bits: Q(1, 2**(k-1)) for bits in product((0, 1), repeat=k) if sum(bits) % 2 == parity}


def validate_population(population):
    if not population:
        raise InputError('Empty execution population.')
    k = len(next(iter(population)))
    for bits, weight in population.items():
        if len(bits) != k or any(type(b) is not int or b not in (0, 1) for b in bits):
            raise InputError('Inconsistent execution worlds.')
        if exact(weight) < 0:
            raise InputError('Negative probability.')
    if sum(population.values()) != 1:
        raise InputError('Population must have total mass one.')
    return k


def moment(population, subset):
    validate_population(population)
    return sum((weight for bits, weight in population.items() if all(bits[i] for i in subset)), Q(0))


def summary(population):
    k = validate_population(population)
    return {subset: moment(population, subset)
            for size in range(k+1) for subset in combinations(range(k), size)}


def compiled_cost(moments, order, costs, penalty):
    """Policy-aware ordinary/native affine coefficients in retained moments."""
    total = Q(0)
    for j, index in enumerate(order):
        total += costs[index]*moments[tuple(sorted(order[:j]))]
    return total+penalty*moments[tuple(sorted(order))]


def stateful_example(revision='stateful-1', cached=None):
    """A caches a lemma; B needs that lemma. A alone never resolves the root."""
    ctx = K.context(('x', 'y'), (K.Row(K.src('x'), K.src('y')), K.Row(K.src('y'), K.num(0))),
                    {'x': 0, 'y': 0}, scope='F13-stateful-source-v1', revision=revision)
    if cached is None:
        builder = K.Builder(ctx, 'h')
        root = builder.rewrite(builder.row(0), K.src('x'), K.src('y'))
        proof = builder.proof(root)
        A.receive(ctx, proof, A.request(ctx, 'h', K.src('x'), K.src('y'), 0))
        return ctx, proof
    # The independently reconstructed current request rejects an old-revision lemma.
    A.receive(ctx, cached, A.request(ctx, 'h', K.src('x'), K.src('y'), 0))
    builder = K.Builder(ctx, 'h')
    builder.steps.extend(cached.steps)
    tail = builder.rewrite(builder.row(1), K.src('y'), K.num(0))
    root = builder.trans(cached.root, tail)
    builder.all_cases((root,))
    proof = builder.proof()
    A.receive(ctx, proof, A.request(ctx, None, K.src('x'), K.num(0), 0))
    return ctx, proof


def stateful_run(order, revision='stateful-1', initial_cache=None):
    cache = initial_cache
    trace = []
    for procedure in order:
        if procedure == 'A':
            _, cache = stateful_example(revision)
            trace.append(('A', 'unavailable'))
        elif procedure == 'B':
            if cache is None:
                trace.append(('B', 'unavailable'))
            else:
                _, proof = stateful_example(revision, cache)
                trace.append(('B', 'certified'))
                return 'certified', tuple(trace), cache, proof
        else:
            raise InputError('Unknown stateful procedure.')
    return 'unavailable', tuple(trace), cache, None


def meta_proof(unresolved_cap, revision='meta-1'):
    """Native conditional mean guarantee from prefix rows, not an input score."""
    cap = exact(unresolved_cap)
    if not 0 <= cap <= Q(1, 4):
        raise InputError('Cap must be consistent with this proper-marginal family.')
    names = ('m1', 'm12', 'm123')
    rows = []
    for name, lower, upper in (('m1', Q(1, 2), Q(1, 2)),
                                ('m12', Q(1, 4), Q(1, 4)), ('m123', Q(0), cap)):
        rows.extend((K.Row(K.src(name), K.num(upper, 'P')),
                     K.Row(K.scale(-1, K.src(name)), K.num(-lower, 'P'))))
    conversion = K.Conversion('probability_to_audit_loss', 'P', 'L', Q(1))
    ctx = K.context(tuple((name, 'P') for name in names), rows,
                    {'m1': Q(1, 2), 'm12': Q(1, 4), 'm123': Q(0)},
                    scope='F13-reset-cascade-metalevel-mean-v1', revision=revision,
                    units=('P', 'L'), conversions=(conversion,))
    builder = K.Builder(ctx, 'h')
    new, old = K.num(5, 'L'), K.num(9, 'L')
    root = builder.constant(new, old)
    for index, name, coefficient in ((0, 'm1', 5), (2, 'm12', 5), (4, 'm123', 20)):
        row = builder.scale(coefficient, builder.conversion(conversion.name, builder.row(index)))
        root = builder.add(root, row)
        new = K.add(new, K.scale(coefficient, K.convert(conversion.name, K.src(name))))
    root = builder.rewrite(root, new, old)
    builder.all_cases((root,))
    proof = builder.proof()
    A.receive(ctx, proof, A.request(ctx, None, new, old, proof.steps[proof.root].budget, 'L'))
    return ctx, proof, new, old
