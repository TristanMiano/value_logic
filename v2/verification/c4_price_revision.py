"""Exact C4 price-revision discriminator; ordinary mathematics, not native K.

Contributor: Codex (GPT-6), October 4, 2026.
The reference matrices in tests come from direct world execution, separately
from these predicted ranks and the constructive moment-recovery formulas.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb

from . import case_retention as T


def equal_price_geometry(k, penalty):
    """Hamming-level costs and prefix reach probabilities, for unit attempts."""
    if k < 2 or Q(penalty) < 0:
        raise ValueError('At least two procedures and nonnegative penalty required.')
    costs = tuple(Q(k+1, k-h+1) for h in range(k))+(Q(k)+Q(penalty),)
    reaches = tuple(tuple(Q(comb(h, r), comb(k, r)) if h >= r else Q(0)
                          for h in range(k+1)) for r in range(k))
    return costs, reaches


def equal_price_diameters(k, penalty):
    """Worst compatible-law reach widths from exact old full-order means."""
    costs, reaches = equal_price_geometry(k, penalty)
    return tuple(max(abs(values[j]-((costs[l]-costs[j])*values[i]
                                    +(costs[j]-costs[i])*values[l])/(costs[l]-costs[i]))
                     for i, j, l in combinations(range(k+1), 3)) for values in reaches)


def retain_equal_price(population, penalty):
    """Minimal linear summary: within-level contrasts plus average old cost.

    World/penalty metadata are public, not retained measurements. The nonlinear
    remainder representation is derived later without consulting population.
    """
    population = {tuple(w): Q(p) for w, p in population.items()}
    if not population:
        raise ValueError('Population is empty.')
    k = len(next(iter(population)))
    worlds = tuple(product((0, 1), repeat=k))
    if any(w not in worlds or p < 0 for w, p in population.items()) or sum(population.values()) != 1:
        raise ValueError('A normalized Boolean law is required.')
    costs, _ = equal_price_geometry(k, penalty)
    contrasts = {}
    for h in range(k+1):
        level = tuple(w for w in worlds if sum(w) == h)
        reference = population.get(level[0], Q(0))
        contrasts.update({w: population.get(w, Q(0))-reference for w in level[1:]})
    average = sum((p*costs[sum(w)] for w, p in population.items()), Q(0))
    return k, Q(penalty), average, contrasts


def equal_price_remainder(summary):
    """Nonnegative fixed residues, remaining mass, and remaining mean cost."""
    k, penalty, average, contrasts = summary
    costs, _ = equal_price_geometry(k, penalty)
    residues = {}
    for h in range(k+1):
        level = tuple(w for w in product((0, 1), repeat=k) if sum(w) == h)
        minimum = min(contrasts.get(w, Q(0)) for w in level)
        residues.update({w: contrasts.get(w, Q(0))-minimum for w in level})
    mass = 1-sum(residues.values())
    mean = average-sum((p*costs[sum(w)] for w, p in residues.items()), Q(0))
    return residues, mass, mean


def equal_price_reach_interval(summary, subset):
    """Sharp interval and attaining laws, by at most two residual levels.

    This is a development control for valid summaries emitted by
    retain_equal_price, not a decoder for untrusted serialized inputs.
    """
    k, penalty, _, _ = summary
    subset = tuple(subset)
    if len(set(subset)) != len(subset) or any(i not in range(k) for i in subset) or len(subset) >= k:
        raise ValueError('A proper subset of procedure indices is required.')
    costs, reaches = equal_price_geometry(k, penalty)
    values = reaches[len(subset)]
    residues, mass, mean = equal_price_remainder(summary)
    offset = sum((p for w, p in residues.items() if all(w[i] for i in subset)), Q(0))
    if mass == 0:
        return (offset, residues), (offset, residues.copy())
    if mass < 0 or not costs[0]*mass <= mean <= costs[-1]*mass:
        raise ValueError('Infeasible summary.')
    target, candidates = mean/mass, []
    for i in range(k+1):
        for j in range(i, k+1):
            if not costs[i] <= target <= costs[j]:
                continue
            left = Q(1) if i == j else (costs[j]-target)/(costs[j]-costs[i])
            weights = {i: mass*left}
            weights[j] = weights.get(j, Q(0))+mass*(1-left)
            law = {w: p+weights.get(sum(w), Q(0))/comb(k, sum(w)) for w, p in residues.items()}
            value = offset+sum((weight*values[h] for h, weight in weights.items()), Q(0))
            candidates.append((value, law))
    return min(candidates, key=lambda item: item[0]), max(candidates, key=lambda item: item[0])


def repair_reach_from_prefix_estimates(summary, subset, estimates):
    """A3 raw estimate from one canonical chain and exact old contrasts.

    estimates[r] measures failure of the first r procedures, for r=0..k-1.
    Raw values may leave [0,1] and need not define a coherent joint law.
    This routine does not create or validate a statistical confidence claim.
    """
    k = summary[0]
    subset, estimates = tuple(subset), tuple(map(Q, estimates))
    if (len(estimates) != k or estimates[0] != 1 or len(set(subset)) != len(subset)
            or any(i not in range(k) for i in subset) or len(subset) >= k):
        raise ValueError('A proper subset and normalized canonical-prefix estimates are required.')
    residues, _, _ = equal_price_remainder(summary)
    r = len(subset)
    offset = sum((p*(int(all(w[i] for i in subset))-int(all(w[i] for i in range(r))))
                  for w, p in residues.items()), Q(0))
    return estimates[r]+offset


def profiles_exact(profiles):
    profiles = tuple((tuple(map(Q, costs)), Q(penalty)) for costs, penalty in profiles)
    if not profiles or len(profiles[0][0]) < 2:
        raise ValueError('At least one profile and two procedures are required.')
    k = len(profiles[0][0])
    if any(len(c) != k or any(x <= 0 for x in c) or m < 0 for c, m in profiles):
        raise ValueError('Same dimension, positive attempts, nonnegative penalties required.')
    return profiles


def predicted_ranks(profiles):
    """All means, within-profile differences, and all cross-profile differences."""
    profiles = profiles_exact(profiles)
    base = profiles[0][0]
    k, n = len(base), 2**len(base)-1
    proportional = all(all(c[i]*base[0] == c[0]*base[i] for i in range(k))
                       for c, _ in profiles)
    penalties = tuple(m for _, m in profiles)
    if not proportional:
        return {'numeric': n if any(penalties) else n-1,
                'within': n-1, 'cross': n if len(set(penalties)) > 1 else n-1}
    parameters = [(c[0]/base[0], m) for c, m in profiles]
    differences = [tuple(a-b for a, b in zip(row, parameters[0])) for row in parameters]
    return {'numeric': n-k+T.rank(parameters), 'within': n-k,
            'cross': n-k+T.rank(differences)}


def chain_probe_orders(k, positive_penalty=True):
    """The changed procedure is last in the old reference order, index k-1."""
    if k < 2:
        raise ValueError('At least two procedures are required.')
    count = k-1 if positive_penalty else k-2
    return tuple(tuple(range(r))+(k-1,)+tuple(range(r, k-1))
                 for r in range(1, count+1))


def invert_moments(moments, k):
    """Boolean inclusion-exclusion; requires all subset moments including empty."""
    subsets = tuple(tuple(c) for size in range(k+1) for c in combinations(range(k), size))
    if set(moments) != set(subsets) or moments[()] != 1:
        raise ValueError('A complete normalized moment table is required.')
    population = {}
    for bits in product((0, 1), repeat=k):
        active = {i for i, bit in enumerate(bits) if bit}
        population[bits] = sum(((-1)**(len(s)-len(active))*moments[s]
                                for s in subsets if active.issubset(s)), Q(0))
    if any(p < 0 for p in population.values()) or sum(population.values()) != 1:
        raise ValueError('The supplied aggregate observations are not a probability law.')
    return population


def repair_from_chain(summary, costs, penalty, change, new_means):
    """Recover all moments when M>0, only proper moments when M=0.

    The old summary is T.retain's minimal exact numeric summary. New means
    correspond exactly to chain_probe_orders and share the original outcome
    law. No access to that law is made by this reconstruction.
    """
    costs = tuple(map(Q, costs))
    penalty, change = Q(penalty), Q(change)
    profiles_exact(((costs, penalty),))
    if not change or costs[-1]+change <= 0:
        raise ValueError('A nonzero edit preserving the last positive price is required.')
    k = len(costs)
    orders = chain_probe_orders(k, penalty > 0)
    new_means = tuple(map(Q, new_means))
    if len(new_means) != len(orders):
        raise ValueError('Wrong number of new order means.')
    chain = {r: (new-T.recover(summary, order, costs))/change
             for r, (new, order) in enumerate(zip(new_means, orders), 1)}
    coefficients = {}
    for r in range(1, len(chain)+1):
        coefficients[r] = (chain[r]-sum(
            (coefficients[j]*T.elementary(costs[:r], j) for j in range(1, r)), Q(0)
        ))/T.elementary(costs[:r], r)
    base, residuals = summary
    if not penalty:
        coefficients[k-1] = (base-costs[0]-sum(
            (coefficients[j]*T.elementary(costs, j+1) for j in range(1, k-1)), Q(0)
        ))/T.elementary(costs, k)
    moments = {(): Q(1)}
    for size in range(1, k):
        for subset in combinations(range(k), size):
            moments[subset] = residuals.get(subset, Q(0))+sum(
                (coefficients[j]*T.elementary(tuple(costs[i] for i in subset), j)
                 for j in range(1, size+1)), Q(0))
    if penalty:
        moments[tuple(range(k))] = (base-costs[0]-sum(
            (coefficients[j]*T.elementary(costs, j+1) for j in range(1, k)), Q(0)
        ))/penalty
    return moments
