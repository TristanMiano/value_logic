#!/usr/bin/env python3
"""Complete logical quotations using the objective's integer lattice.

DEVELOPMENT. ChatGPT (GPT-6 Astra Pro), 2026-10-12. The integer gcd is an
objective-only consequence, not logical model enumeration or an outcome law.
`complete=True` requires the separately admitted finite-provider contract.
"""
from fractions import Fraction as F
from pathlib import Path
import sys

S06 = Path(__file__).resolve().parent.parent / "s06"
sys.path.insert(0, str(S06))
import anchor_quotes as aq


def objective_lattice(q, meter):
    if not q or any(type(x) is not int or x < 0 for x in q):
        raise ValueError("A nonempty nonnegative integer query objective is required")
    g, divisions = 0, 0
    for weight in q:
        a, b = g, weight
        while b:
            a, b = b, a % b
            divisions += 1
        g = a
    meter.pay("lattice_quote", "query_validation_and_euclidean_gcd", len(q) + divisions + 2)
    return g


def _enclosure(modes, possible, lowers, q, meter):
    n, m = len(possible), len(q)
    if any(F(x) < 0 for x in lowers):
        raise ValueError("This interface uses nonnegative admitted anchor lower bounds")
    if not n or any(len(v) != m for v in modes):
        raise ValueError("Matching objective dimensions and nonempty cost cohort required")
    hi = [sum((max(F(modes[h][j]) for h in row) for row in possible), F(0))
          for j in range(m)]
    alpha = sum((max(F(0), hi_j - q_j) for hi_j, q_j in zip(hi, q)), F(0))
    lower = sum((min(F(lowers[h]) / n for h in row) for row in possible), F(0))
    losses = [sum((max(F(0), q_j - n * F(w_j)) for q_j, w_j in zip(q, mode)), F(0))
              for mode in modes]
    meter.pay("lattice_quote", "coordinate_enclosure_and_scalar_cut_transport",
              3 * m * sum(map(len, possible)) + 3 * m * len(modes) + 12)
    return alpha, lower, losses


def quote(masks, modes, possible, lowers, price, q, budget, meter, complete=True):
    """Quote both checked outcomes, with gcd-rounded SAT and UNSAT endpoints.

    A zero objective returns an uninformative quote: it cannot refine an
    unclosed state through the two-outcome acquisition interface. Each mask
    must already have an admitted feasible witness on this logical source.
    """
    if type(budget) is not int or F(price) < 0:
        raise ValueError("Integral budget and nonnegative replacement price required")
    g = objective_lattice(q, meter)
    before = aq.best(masks, modes, possible, lowers, price, meter)["bound"]
    if g == 0:
        return dict(weights=list(q), budget=budget, objective_lattice=0,
                    before=before, SAT_bound=before, UNSAT_bound=before,
                    UNSAT_anchor_lowers=list(map(F, lowers)), worst_bound=before,
                    guaranteed_gain=F(0), no_progress_outcome=True,
                    informative=False, reason="Identically zero objective; no nontrivial complete purchase")
    alpha, lower, losses = _enclosure(modes, possible, lowers, q, meter)
    sat_objective = g * (budget // g)
    unsat_objective = sat_objective + g
    price = F(price)
    positive = min(before, max(F(0), min(price, sat_objective + alpha) - min(price, lower)))
    next_lowers = [max(F(old), F(0), unsat_objective - loss)
                   for old, loss in zip(lowers, losses)]
    negative = min(before, aq.best(masks, modes, possible, next_lowers, price, meter)["bound"])
    worst = max(positive, negative) if complete else before
    meter.pay("lattice_quote", "lattice_endpoint_rounding_and_complete_outcome_maximum", 10)
    return dict(weights=list(q), budget=budget, objective_lattice=g,
                before=before, SAT_objective_upper=sat_objective,
                UNSAT_objective_lower=unsat_objective,
                SAT_uniform_cost_upper=sat_objective + alpha,
                positive_box_margin=alpha, current_uniform_lower=lower,
                SAT_bound=positive, UNSAT_anchor_lowers=next_lowers,
                UNSAT_bound=negative, no_progress_outcome=not complete,
                worst_bound=worst, guaranteed_gain=before - worst,
                informative=True,
                premise="Both answers independently checked under an admitted complete-call contract; a capped or interrupted attempt retains the old bound")


def closing_query(masks, modes, possible, lowers, price, q, tolerance, meter,
                  *, complete=True, known_query_upper=None, exact_interval=False):
    """Find a closing canonical budget with one negative-branch evaluation.

    For an unclosed state and g>0, canonical budgets are g*k. SAT closes iff
    k <= floor((L + tolerance - alpha)/g). UNSAT closure is monotone in k.
    Consequently checking the largest SAT-feasible k decides existence for
    this quotation. Optional integer bisection returns the exact lower end
    of the same interval. `known_query_upper`, when given, must itself be an
    admitted feasible q-objective value; budgets are capped below it.
    """
    tolerance, price = F(tolerance), F(price)
    if tolerance < 0 or price < 0:
        raise ValueError("Nonnegative tolerance and replacement price required")
    g = objective_lattice(q, meter)
    before = aq.best(masks, modes, possible, lowers, price, meter)["bound"]
    base = dict(weights=list(q), objective_lattice=g, before=before,
                tolerance=tolerance, quotation_scope="Exact existence within the conservative scalar-anchor, coordinate-enclosure quotation")
    if before <= tolerance:
        return base | dict(status="already_closed", closes=True, needs_purchase=False, quote=None)
    if g == 0:
        return base | dict(status="zero_objective", closes=False, needs_purchase=False, quote=None)
    alpha, lower, _ = _enclosure(modes, possible, lowers, q, meter)
    # Replacement is one available output, so B>tau implies L+tau<p.
    if not lower + tolerance < price:
        raise AssertionError("Unclosed state contradicts its retained replacement certificate")
    high = (lower + tolerance - alpha) // g
    if known_query_upper is not None:
        if type(known_query_upper) is not int or known_query_upper < 0 or known_query_upper % g:
            raise ValueError("Known feasible query upper must lie on the objective lattice")
        high = min(high, known_query_upper // g - 1)
    base.update(current_uniform_lower=lower, positive_box_margin=alpha,
                largest_SAT_feasible_lattice_index=high,
                largest_SAT_feasible_budget=g * high)
    meter.pay("lattice_quote", "exact_sat_interval_endpoint", 9)
    if high < 0:
        return base | dict(status="no_SAT_feasible_nonnegative_budget", closes=False,
                           needs_purchase=False, quote=None, nonempty_budget_interval=False)
    got = quote(masks, modes, possible, lowers, price, q, g * high, meter, complete=complete)
    closes = got["worst_bound"] <= tolerance
    result = base | dict(status="closing_query" if closes else "no_closing_query",
                         closes=closes, needs_purchase=closes, quote=got,
                         nonempty_budget_interval=closes,
                         integer_budget_high=g * (high + 1) - 1,
                         canonical_budget=g * high,
                         negative_branch_evaluations=1)
    if closes and exact_interval:
        low_fail, high_pass = -1, high
        while high_pass - low_fail > 1:
            mid = (low_fail + high_pass) // 2
            trial = quote(masks, modes, possible, lowers, price, q, g * mid, meter, complete=True)
            result["negative_branch_evaluations"] += 1
            if trial["UNSAT_bound"] <= tolerance:
                high_pass = mid
            else:
                low_fail = mid
        result.update(smallest_UNSAT_feasible_lattice_index=high_pass,
                      integer_budget_low=g * high_pass,
                      exact_budget_interval=True)
    return result
