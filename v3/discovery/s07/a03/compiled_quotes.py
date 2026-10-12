#!/usr/bin/env python3
"""Paid reusable arithmetic for the unchanged s07 lattice quotation.

DEVELOPMENT. ChatGPT (GPT-6 Astra Pro), 2026-10-12. This compiles numerical
functions, never logical evidence. The caller must independently admit every
mask and scalar lower on its own fixed logical source, use this fixed ordered
mode table/cohort, and supply the complete-call contract. Equal numbers may
share arithmetic across logical rows; they do not transfer proof authority.
"""
from __future__ import annotations

from fractions import Fraction as F


VERSION = 's07-prepared-lattice-quotes-v1'
SCOPE = 'Exact existence within the conservative scalar-anchor, coordinate-enclosure quotation'
PREMISE = ('Both answers independently checked under an admitted complete-call contract; '
           'a capped or interrupted attempt retains the old bound')


class PreparedQuotes:
    """Same closing_query formulas, with paid immutable numerical caches.

    Public modes may be exact nonnegative rationals; query objectives remain
    nonnegative integer vectors. Possible-mode rows are distinct fixed cohort
    members but exchangeable in these sums, so their multiset is a valid
    arithmetic cache key. Actual row identity/observations stay with the
    caller's source admission and execution controller.
    """

    def __init__(self, modes, cohort_size, meter):
        self.meter = meter
        if type(cohort_size) is not int or cohort_size < 1 or not modes or not modes[0]:
            raise ValueError('A nonempty fixed mode table and positive integral cohort required')
        self.n, self.m = cohort_size, len(modes[0])
        self.modes = tuple(tuple(F(w) for w in v) for v in modes)
        if any(len(v) != self.m or any(w < 0 for w in v) for v in self.modes):
            raise ValueError('One ordered nonnegative cost-feature domain required')
        self.k = len(self.modes)
        self.anchors = tuple(tuple(self.n * w for w in v) for v in self.modes)
        self._mask_costs, self._objectives = {}, {}
        self._raw_states, self._states, self._bases, self._uppers = {}, {}, {}, {}
        self.stats = dict(calls=0, mask_compilations=0, mask_hits=0,
                          objective_compilations=0, objective_hits=0,
                          loss_compilations=0, source_compilations=0,
                          source_hits=0, base_compilations=0, base_hits=0,
                          upper_compilations=0, upper_hits=0)
        self.stored_words = 2 * self.k * self.m + 4
        meter.pay('prepared_admission', 'fixed_modes_fraction_conversion_and_scaling', 3 * self.k * self.m + 4)
        meter.pay('prepared_storage', 'mode_and_full_cohort_anchor_words', self.stored_words)

    def _store(self, words):
        self.stored_words += words
        self.meter.pay('prepared_storage', 'immutable_cache_key_and_value_words', words)

    def _sorted(self, values):
        """Small input canonicalization with actual comparison/move charges."""
        output = []
        for value in values:
            index = len(output)
            output.append(value)
            self.meter.pay('prepared_key', 'canonical_item_append')
            while index:
                self.meter.pay('prepared_key', 'canonical_item_comparison')
                if output[index - 1] <= value:
                    break
                output[index] = output[index - 1]
                index -= 1
                self.meter.pay('prepared_key', 'canonical_item_move', 2)
            output[index] = value
            self.meter.pay('prepared_key', 'canonical_item_store')
        return tuple(output)

    def _state(self, possible):
        if len(possible) != self.n:
            raise ValueError('Fixed cohort size changed')
        raw = tuple(tuple(row) for row in possible)
        if any(not row or len(set(row)) != len(row)
               or any(type(k) is not int or not 0 <= k < self.k for k in row) for row in raw):
            raise ValueError('Each source row needs a nonempty set of admitted mode IDs')
        self.meter.pay('prepared_lookup', 'possible_mode_admission_and_state_key', 2 * sum(map(len, raw)) + self.n + 2)
        if raw in self._raw_states:
            self.stats['source_hits'] += 1
            return self._raw_states[raw]
        key = self._sorted(self._sorted(row) for row in raw)
        self.meter.pay('prepared_lookup', 'canonical_source_lookup', self.n + 1)
        if key in self._states:
            self.stats['source_hits'] += 1
            state = self._states[key]
        else:
            groups = []
            for row in key:
                if groups and groups[-1][0] == row:
                    groups[-1] = (row, groups[-1][1] + 1)
                else:
                    groups.append((row, 1))
                self.meter.pay('prepared_compile', 'exchangeable_mode_set_grouping', len(row) + 3)
            hi = []
            for j in range(self.m):
                total = F(0)
                for choices, count in groups:
                    total += count * max(self.modes[k][j] for k in choices)
                    self.meter.pay('prepared_compile', 'grouped_coordinate_maximum_and_cohort_sum', len(choices) + 4)
                hi.append(total)
            state = dict(key=key, groups=tuple(groups), hi=tuple(hi))
            self._states[key] = state
            self._store(sum(map(len, key)) + self.n + sum(len(p) + 1 for p, _ in groups) + self.m + 4)
            self.stats['source_compilations'] += 1
        self._raw_states[raw] = state
        self._store(sum(map(len, raw)) + self.n + 1)
        return state

    def _mask(self, mask):
        self.meter.pay('prepared_lookup', 'mode_action_cache_lookup')
        if mask in self._mask_costs:
            self.stats['mask_hits'] += 1
            return self._mask_costs[mask]
        costs = []
        for mode in self.modes:
            costs.append(sum((w for j, w in enumerate(mode) if mask & (1 << j)), F(0)))
            self.meter.pay('prepared_compile', 'mask_mode_cost_products_and_sum', 2 * self.m + 1)
        self._mask_costs[mask] = tuple(costs)
        self._store(self.k + 1)
        self.stats['mask_compilations'] += 1
        return self._mask_costs[mask]

    def _objective(self, q):
        q = tuple(q)
        if len(q) != self.m or any(type(w) is not int or w < 0 for w in q):
            raise ValueError('Same ordered nonnegative integral query objective required')
        self.meter.pay('prepared_lookup', 'query_objective_admission_and_cache_key', self.m + 2)
        if q in self._objectives:
            self.stats['objective_hits'] += 1
            return self._objectives[q]
        g, divisions = 0, 0
        for weight in q:
            a, b = g, weight
            while b:
                a, b = b, a % b
                divisions += 1
            g = a
        self.meter.pay('prepared_compile', 'integer_objective_euclidean_gcd', self.m + divisions + 2)
        result = dict(q=q, gcd=g, losses=None)
        self._objectives[q] = result
        self._store(self.m + 3)
        self.stats['objective_compilations'] += 1
        return result

    def _losses(self, objective):
        self.meter.pay('prepared_lookup', 'query_anchor_loss_lookup')
        if objective['losses'] is None:
            objective['losses'] = tuple(sum((max(F(0), q - w) for q, w in zip(objective['q'], anchor)), F(0))
                                        for anchor in self.anchors)
            self.meter.pay('prepared_compile', 'query_anchor_positive_difference_sums', 3 * self.m * self.k)
            self._store(self.k)
            self.stats['loss_compilations'] += 1
        return objective['losses']

    def _upper(self, mask, costs, state):
        key = (mask, state['key'])
        self.meter.pay('prepared_lookup', 'action_source_upper_lookup', 2 + self.n)
        if key in self._uppers:
            self.stats['upper_hits'] += 1
            return self._uppers[key]
        upper = F(0)
        for choices, count in state['groups']:
            upper += count * max(costs[k] for k in choices)
            self.meter.pay('prepared_compile', 'grouped_action_upper_and_sum', len(choices) + 4)
        self._uppers[key] = upper
        self._store(3 + self.n + sum(map(len, state['key'])))
        self.stats['upper_compilations'] += 1
        return upper

    def _base(self, masks, state, lowers, price):
        key = (masks, state['key'], lowers, price)
        self.meter.pay('prepared_lookup', 'anchor_base_numeric_key', len(masks) + self.n + self.k + 4)
        if key in self._bases:
            self.stats['base_hits'] += 1
            return self._bases[key]
        scaled = tuple(ell / self.n for ell in lowers)
        self.meter.pay('prepared_compile', 'scalar_anchor_row_scaling', self.k)
        lower = F(0)
        for choices, count in state['groups']:
            lower += count * min(scaled[k] for k in choices)
            self.meter.pay('prepared_compile', 'grouped_common_lower_and_sum', len(choices) + 4)
        before = max(F(0), price - lower)
        self.meter.pay('prepared_query', 'replacement_bound', 3)
        for mask in masks:
            costs = self._mask(mask)
            contrast = F(0)
            for choices, count in state['groups']:
                contrast += count * max(costs[k] - scaled[k] for k in choices)
                self.meter.pay('prepared_compile', 'grouped_action_anchor_contrast_and_sum', 2 * len(choices) + 4)
            bound = max(F(0), contrast, self._upper(mask, costs, state) - price)
            before = min(before, bound)
            self.meter.pay('prepared_query', 'action_regret_clipping_and_best_selection', 5)
        result = dict(before=before, lower=lower)
        self._bases[key] = result
        self._store(len(masks) + self.n + sum(map(len, state['key'])) + self.k + 5)
        self.stats['base_compilations'] += 1
        return result

    def _quote(self, masks, state, lowers, price, objective, budget, base, alpha, complete):
        g = objective['gcd']
        sat_objective = g * (budget // g)
        unsat_objective = sat_objective + g
        before, lower = base['before'], base['lower']
        positive = min(before, max(F(0), min(price, sat_objective + alpha) - min(price, lower)))
        next_lowers = tuple(max(old, F(0), unsat_objective - loss)
                            for old, loss in zip(lowers, self._losses(objective)))
        negative = min(before, self._base(masks, state, next_lowers, price)['before'])
        worst = max(positive, negative) if complete else before
        self.meter.pay('prepared_query', 'checked_outcome_lattice_bounds_and_record', 3 * self.k + self.m + 28)
        return dict(weights=list(objective['q']), budget=budget, objective_lattice=g,
                    before=before, SAT_objective_upper=sat_objective,
                    UNSAT_objective_lower=unsat_objective,
                    SAT_uniform_cost_upper=sat_objective + alpha,
                    positive_box_margin=alpha, current_uniform_lower=lower,
                    SAT_bound=positive, UNSAT_anchor_lowers=list(next_lowers),
                    UNSAT_bound=negative, no_progress_outcome=not complete,
                    worst_bound=worst, guaranteed_gain=before - worst,
                    informative=True, premise=PREMISE)

    def closing_query(self, masks, possible, lowers, price, q, tolerance,
                      *, complete=True, known_query_upper=None, exact_interval=False):
        """Exact drop-in result for lattice_quotes.closing_query's arguments.

        The modes/cohort/meter are fixed at construction. Mask feasibility,
        source-specific lower proof admission and the complete-provider
        premise are caller obligations, unchanged from lattice_quotes.
        """
        self.stats['calls'] += 1
        price, tolerance = F(price), F(tolerance)
        lowers = tuple(F(v) for v in lowers)
        masks = tuple(masks)
        if (price < 0 or tolerance < 0 or len(lowers) != self.k or any(v < 0 for v in lowers)
                or any(type(z) is not int or not 0 <= z < (1 << self.m) for z in masks)):
            raise ValueError('Admitted nonnegative prices/anchor lowers and checked Boolean masks required')
        self.meter.pay('prepared_lookup', 'scalar_mask_admission_and_conversion', 2 * self.k + len(masks) + 6)
        mask_count = len(masks)
        masks = self._sorted(set(masks))
        self.meter.pay('prepared_key', 'duplicate_action_elimination', mask_count + 1)
        objective = self._objective(q)
        state = self._state(possible)
        base = self._base(masks, state, lowers, price)
        before, g = base['before'], objective['gcd']
        result = dict(weights=list(objective['q']), objective_lattice=g, before=before,
                      tolerance=tolerance, quotation_scope=SCOPE)
        self.meter.pay('prepared_query', 'closing_status_and_base_output', self.m + 12)
        if before <= tolerance:
            return result | dict(status='already_closed', closes=True, needs_purchase=False, quote=None)
        if g == 0:
            return result | dict(status='zero_objective', closes=False, needs_purchase=False, quote=None)
        lower = base['lower']
        alpha = sum((max(F(0), hi - q) for hi, q in zip(state['hi'], objective['q'])), F(0))
        self.meter.pay('prepared_query', 'objective_enclosure_positive_margin', 3 * self.m)
        if not lower + tolerance < price:
            raise AssertionError('Unclosed state contradicts its retained replacement certificate')
        high = (lower + tolerance - alpha) // g
        if known_query_upper is not None:
            if type(known_query_upper) is not int or known_query_upper < 0 or known_query_upper % g:
                raise ValueError('Known feasible query upper must lie on the objective lattice')
            high = min(high, known_query_upper // g - 1)
            self.meter.pay('prepared_query', 'known_feasible_query_upper_limit', 5)
        result.update(current_uniform_lower=lower, positive_box_margin=alpha,
                      largest_SAT_feasible_lattice_index=high,
                      largest_SAT_feasible_budget=g * high)
        self.meter.pay('prepared_query', 'exact_sat_interval_endpoint', 9)
        if high < 0:
            return result | dict(status='no_SAT_feasible_nonnegative_budget', closes=False,
                                 needs_purchase=False, quote=None, nonempty_budget_interval=False)
        got = self._quote(masks, state, lowers, price, objective, g * high, base, alpha, complete)
        closes = got['worst_bound'] <= tolerance
        result.update(status='closing_query' if closes else 'no_closing_query',
                      closes=closes, needs_purchase=closes, quote=got,
                      nonempty_budget_interval=closes, integer_budget_high=g * (high + 1) - 1,
                      canonical_budget=g * high, negative_branch_evaluations=1)
        self.meter.pay('prepared_query', 'closing_result_output', 9)
        if closes and exact_interval:
            low_fail, high_pass = -1, high
            while high_pass - low_fail > 1:
                mid = (low_fail + high_pass) // 2
                trial = self._quote(masks, state, lowers, price, objective, g * mid, base, alpha, True)
                result['negative_branch_evaluations'] += 1
                if trial['UNSAT_bound'] <= tolerance:
                    high_pass = mid
                else:
                    low_fail = mid
                self.meter.pay('prepared_query', 'exact_budget_interval_bisection', 6)
            result.update(smallest_UNSAT_feasible_lattice_index=high_pass,
                          integer_budget_low=g * high_pass, exact_budget_interval=True)
        return result

    def storage(self):
        """Stored numerical-word tariff, not allocator/native physical bytes."""
        self.meter.pay('prepared_query', 'cache_storage_summary', 9)
        return dict(mode_actions=len(self._mask_costs), objectives=len(self._objectives),
                    raw_source_keys=len(self._raw_states), canonical_sources=len(self._states),
                    anchor_bases=len(self._bases), action_source_uppers=len(self._uppers),
                    stored_numerical_words=self.stored_words,
                    scope='Explicit admitted/compiled key-value word tariff; physical bytes and host allocator costs not measured')
