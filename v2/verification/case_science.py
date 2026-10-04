"""F13 degree-six scientific case, exact rules and native fixed-action proofs.

Development family only. Sampling/model premises are not empirically validated.
No change to the F06 kernel or F07 request-bound receiver.
"""
from dataclasses import dataclass
from fractions import Fraction as Q

from v2.checks import f06_inference_rules as K
from v2.checks import f07_soundness as A
from .model import exact, InputError


def basis(x):
    x = Q(x)
    t = x-Q(1, 2)
    return 30*x*x*(1-x)**2, -2688*t*t*(t*t-Q(1, 16))*(t*t-Q(1, 4))


def sample(x, a, b, u, v):
    g, h = basis(x)
    return Q(a)+Q(b)*x+Q(u)*g+Q(v)*h


def weights(z):
    z = exact(z)
    g, h = basis(z)
    if not 0 < z < 1 or h == 0:
        raise InputError('Fourth node must be interior and identify the residual.')
    wz = 1/h
    wm = Q(8, 15)*(1-g/h)
    w1 = Q(1, 2)-wm/2-z*wz
    w0 = Q(1, 2)-wm/2-(1-z)*wz
    return ((Q(0), w0), (Q(1, 2), wm), (Q(1), w1), (z, wz))


RULES = {
    'T': ((Q(0), Q(1, 2)), (Q(1), Q(1, 2))),
    'S': ((Q(0), Q(1, 6)), (Q(1, 2), Q(2, 3)), (Q(1), Q(1, 6))),
    'B': tuple((Q(i, 4), Q(w, 90)) for i, w in enumerate((7, 32, 12, 32, 7))),
}


def integrate_samples(rule, values):
    return sum((weight*values[node] for node, weight in rule), Q(0))


@dataclass(frozen=True)
class Source:
    u_cap: Q
    v_cap: Q
    joint_cap: Q | None = None
    revision: str = 'science-1'

    def validate(self):
        for cap in (self.u_cap, self.v_cap, self.joint_cap):
            if cap is not None and exact(cap) < 0:
                raise InputError('Caps must be nonnegative exact rationals.')
        if not isinstance(self.revision, str) or not 0 < len(self.revision) <= 128:
            raise InputError('A bounded revision identity is required.')
        return self


def residual():
    return K.sub(K.scale(Q(1, 4), K.src('u')), K.src('v'))


def context(source):
    source.validate()
    rows = [K.Row(term, K.num(cap)) for term, cap in (
        (K.src('u'), source.u_cap), (K.scale(-1, K.src('u')), source.u_cap),
        (K.src('v'), source.v_cap), (K.scale(-1, K.src('v')), source.v_cap))]
    if source.joint_cap is not None:
        rows.extend(K.Row(term, K.num(source.joint_cap))
                    for term in (residual(), K.scale(-1, residual())))
    return K.context(('u', 'v'), rows, {'u': 0, 'v': 0},
                     scope='F13-degree-six-science-v1', revision=source.revision)


def pair(price):
    price = exact(price)
    if price < 0:
        raise InputError('Sampling price must be nonnegative.')
    return K.add(K.absolute(residual()), K.num(3*price)), K.num(4*price)


def prove(source, price, *, use_joint=True):
    """Build row-based bounds; no semantic reference/answer table is consulted."""
    ctx = context(source)
    new, old = pair(price)
    b = K.Builder(ctx, 'h')
    marginal = exact(source.u_cap)/4+exact(source.v_cap)
    if use_joint and source.joint_cap is not None and source.joint_cap <= marginal:
        positive, negative = b.row(4), b.row(5)
    else:
        positive = b.add(b.scale(Q(1, 4), b.row(0)), b.row(3))
        positive = b.rewrite(positive, residual(), K.num(0))
        negative = b.add(b.scale(Q(1, 4), b.row(1)), b.row(2))
        negative = b.rewrite(negative, K.scale(-1, residual()), K.num(0))
    root = b.max_common(positive, negative)
    root = b.add(root, b.constant(K.num(3*price), K.num(4*price)))
    root = b.rewrite(root, new, old)
    b.all_cases((root,))
    proof = b.proof()
    bound = proof.steps[proof.root].budget
    A.receive(ctx, proof, A.request(ctx, None, new, old, bound))
    return ctx, proof


def prove_shared_error(source, price, discrepancy, noise, z=Q(1, 12)):
    """Native proof with unbounded common J; source component rows supply the bound."""
    source.validate()
    price, discrepancy, noise = map(exact, (price, discrepancy, noise))
    if min(price, discrepancy, noise) < 0:
        raise InputError('Nonnegative prices and component error bounds required.')
    quadrature = weights(z)
    nodes = tuple(x for x, _ in quadrature)
    qweights = dict(quadrature)
    sweights = dict(RULES['S'])
    base = context(source)
    rows = list(base.cases[0].rows)
    names = ['u', 'v', 'J']
    signed_rows = {}
    for prefix, cap in (('r', discrepancy), ('e', noise)):
        for j in range(4):
            name = f'{prefix}{j}'
            names.append(name)
            signed_rows[name] = len(rows), len(rows)+1
            rows.extend((K.Row(K.src(name), K.num(cap)), K.Row(K.scale(-1, K.src(name)), K.num(cap))))
    ctx = K.context(names, rows, dict.fromkeys(names, 0),
                    scope='F13-shared-error-unbounded-reference-v1', revision=source.revision)
    eq, es = K.src('J'), K.add(K.src('J'), residual())
    for j, node in enumerate(nodes):
        perturbation = K.add(K.src(f'r{j}'), K.src(f'e{j}'))
        eq = K.add(eq, K.scale(qweights[node], perturbation))
        es = K.add(es, K.scale(sweights.get(node, Q(0)), perturbation))
    builder = K.Builder(ctx, 'h')
    directional = []
    for sign in (1, -1):
        marginal = exact(source.u_cap)/4+exact(source.v_cap)
        if source.joint_cap is not None and source.joint_cap <= marginal:
            root = builder.row(4 if sign == 1 else 5)
        else:
            root = builder.add(builder.scale(Q(1, 4), builder.row(0 if sign == 1 else 1)),
                               builder.row(3 if sign == 1 else 2))
        for j, node in enumerate(nodes):
            coefficient = sign*(sweights.get(node, Q(0))-qweights[node])
            if coefficient:
                for prefix in ('r', 'e'):
                    row = signed_rows[f'{prefix}{j}'][0 if coefficient > 0 else 1]
                    root = builder.add(root, builder.scale(abs(coefficient), builder.row(row)))
        root = builder.rewrite(root, K.scale(sign, K.sub(es, eq)), K.num(0))
        projection = builder.lattice('max_left' if sign == 1 else 'max_right', eq, K.scale(-1, eq))
        root = builder.add(root, projection)
        root = builder.rewrite(root, K.scale(sign, es), K.absolute(eq))
        directional.append(root)
    root = builder.max_common(*directional)
    root = builder.add(root, builder.constant(K.num(3*price), K.num(4*price)))
    new, old = K.add(K.absolute(es), K.num(3*price)), K.add(K.absolute(eq), K.num(4*price))
    root = builder.rewrite(root, new, old)
    builder.all_cases((root,))
    proof = builder.proof()
    A.receive(ctx, proof, A.request(ctx, None, new, old, proof.steps[proof.root].budget))
    return ctx, proof, new, old
