"""Direct two-bit executions and atom-safe tail integration, no native AST."""
from fractions import Fraction as Q
from itertools import product

from .program_model import ProgramEvidence, ProgramQuery
from .model import InputError, exact


def execute(policy, x, y):
    """Return task error plus the actual read costs of this deterministic policy."""
    if type(x) is not int or type(y) is not int or x not in (0, 1) or y not in (0, 1):
        raise InputError('Program inputs are two binary integers.')
    reads = 0
    if policy == 'zero':
        answer = 0
    elif policy == 'adaptive':
        reads += 1
        if x == 0:
            answer = 0
        else:
            reads += 1
            answer = x ^ y
    elif policy == 'full':
        reads += 2
        answer = x ^ y
    else:
        raise ValueError('Unknown execution policy.')
    return Q(answer != (x ^ y)) + Q(3, 20) * reads


def probabilities(error, second):
    error, second = exact(error), exact(second)
    if not 0 <= error <= Q(1, 2) or not 0 <= second <= Q(1, 2):
        raise InputError('Input masses are outside this distribution family.')
    return Q(1, 2)-error, error, second, Q(1, 2)-second


def tail(losses, masses, alpha):
    """Average the worst 1-alpha mass, including fractional boundary atoms."""
    def rational(value):
        if isinstance(value, bool) or not isinstance(value, (int, Q)):
            raise InputError('Tail arithmetic requires exact rational values.')
        return Q(value)
    # These masses may be derived from admitted inputs and need one extra bit
    # (or more after arithmetic). Do not reapply the external input-size cap.
    losses, masses, alpha = tuple(map(rational, losses)), tuple(map(rational, masses)), exact(alpha)
    if (not losses or len(losses) != len(masses) or not 0 <= alpha < 1
            or any(p < 0 for p in masses) or sum(masses) != 1):
        raise InputError('Tail evaluation requires a finite probability law and alpha in [0,1).')
    remaining = Q(1)-alpha
    total = Q(0)
    for value, mass in sorted(zip(losses, masses), reverse=True):
        amount = min(remaining, mass)
        total += amount * value
        remaining -= amount
        if remaining == 0:
            return total / (1-alpha)
    raise AssertionError('Distribution does not supply unit mass.')


def loss_law(policy, error, second):
    result = {}
    for bits, mass in zip(product((0, 1), repeat=2), probabilities(error, second)):
        value = execute(policy, *bits)
        result[value] = result.get(value, Q(0)) + mass
    return tuple((loss, mass) for loss, mass in sorted(result.items()) if mass)


def difference(query: ProgramQuery, error, second):
    query.validate()
    masses = probabilities(error, second)
    outcomes = tuple(product((0, 1), repeat=2))
    values = {policy: tuple(execute(policy, x, y) for x, y in outcomes)
              for policy in ('zero', 'adaptive', 'full')}
    if query.kind == 'mean_edit':
        return sum((p * (new-old) for p, new, old in zip(masses, values['zero'], values['adaptive'])), Q(0))
    return tail(values['adaptive'], masses, query.alpha) - tail(values['full'], masses, query.alpha)


def reference(evidence: ProgramEvidence, query: ProgramQuery, *, reduct=False):
    """Monotone fixed-family objectives attain their maxima at upper endpoints.

    Moving mass from outcome 00 to 01 increases the adaptive program's loss;
    the mean-edit difference increases with the mass of outcome 10. The code
    evaluates all four corners, with duplicate corners harmless.
    """
    evidence.validate(); query.validate()
    error_cap = evidence.error_cap if reduct or not evidence.foreign_zero else Q(0)
    scored = [(difference(query, e, u), (e, u))
              for e, u in product((Q(0), error_cap), (Q(1, 5), evidence.second_cap))]
    return max(scored)
