#!/usr/bin/env python3
"""One paid evaluator for admitted finite-source repair evidence.

DEVELOPMENT. ChatGPT (GPT-6 Astra Pro), 2026-10-12.

The live ``CompactBank`` must come from actual raw-tree admission, followed
only by independently checked retention. Its compact tree masks are an
internal admitted-data boundary, not proof bytes that this module can check.
This module binds that bank to the fixed instances, actually checks candidate
assignments, and derives every scalar lower from the bank's own tree masks or
from raw RUP exports checked by ``admit_cut_dual``. A serialized checked flag,
an optimum, or a source checksum never supplies a new logical lower.

All weights are nonnegative; cost rows and ordered features have one fixed
source. Optional hull construction is capped. No method performs LP, SAT,
logical-model enumeration, or proof search. Named operation units are charged
to the caller's common meter; they are not an economic or CPU-time conversion.
"""
from __future__ import annotations

import copy
from fractions import Fraction as F
from pathlib import Path
import sys

S06 = Path(__file__).resolve().parent.parent / 's06'
if str(S06) not in sys.path:
    sys.path.insert(0, str(S06))

import cohort_hull
import cut_dual
import joint_repair as joint
import native_repair as native
import rup_bridge_v2 as rup
import source_anchor
import vertex_repair as vertex


VERSION = 's07-admitted-repair-evaluator-v1'
METHODS = ('tree', 'scalar_anchor', 'dual_box', 'hull')


class RepairEvaluator:
    """Bind a live s06 CompactBank and CostState to reusable evaluators.

    ``evaluate(row, price, tolerance=0, *, costs=None,
    methods=('tree', 'scalar_anchor'), hull_cap=256)`` returns a fixed checked
    action and a uniform regret bound. ``costs=`` may be a hypothetical outcome
    branch with the same modes, cohort, source ID and meter. Branch selection
    and any actual observation admission remain the controller's duties.

    The bank is retained by reference so checked new witnesses/trees become
    available on the next query. Instances are copied and source-bound once.
    All outputs are exact numbers (possibly Fraction); serialization belongs
    to the caller. Each controller should receive its own equivalent instance
    of this class and pay its own admission, compilation and query work.
    """

    def __init__(self, instances, bank, costs, meter):
        self.instances = copy.deepcopy(list(instances))
        self.bank, self.costs, self.meter = bank, costs, meter
        self.source_id = costs.source_id
        self.modes = tuple(tuple(v) for v in costs.modes)
        self.n, self.m = costs.n, costs.m
        self.duals = {r: [] for r in range(len(self.instances))}
        self.cuts = {r: [] for r in range(len(self.instances))}
        self._checked_witnesses, self._tree_bindings = {}, {}
        self._anchor_cache, self._hull_cache = {}, {}
        if len(self.instances) != len(bank.rows) or bank.meter is not meter:
            raise ValueError('One source-bound bank row per instance and one common meter required')
        self._state(costs)
        self.structural_ids = []
        for row, instance in enumerate(self.instances):
            if (instance['identity'] != native.kernel.digest({k: v for k, v in instance.items() if k != 'identity'})
                    or len(instance['soft']) != self.m):
                raise ValueError('Logical source identity or ordered objective changed')
            self.structural_ids.append(native.structural_id(instance))
            words = 8 + sum(1 + len(c) for c in instance['hard'])
            words += sum(2 + len(s['clause']) for s in instance['soft'])
            meter.pay('interface_admission', 'fixed_logical_source_and_feature_binding', words)
            self._profile(row)
        meter.pay('interface_admission', 'fixed_cost_source_and_mode_binding', self.n + self.m * len(self.modes) + 8)

    def _state(self, costs):
        if (costs.meter is not self.meter or costs.source_id != self.source_id
                or costs.n != self.n or costs.m != self.m
                or tuple(tuple(v) for v in costs.modes) != self.modes):
            raise ValueError('Cost source, cohort, ordered modes or invoice meter changed')
        if (not self.modes or self.n <= 0 or self.m <= 0
                or any(len(v) != self.m or any(type(w) is not int or w < 0 for w in v) for v in self.modes)
                or len(costs.possible) != self.n):
            raise ValueError('Nonempty fixed cohort and integral nonnegative objective modes required')
        possible = tuple(tuple(row) for row in costs.possible)
        if any(not row or len(set(row)) != len(row)
               or any(type(k) is not int or not 0 <= k < len(self.modes) for k in row) for row in possible):
            raise ValueError('Every fixed cost row needs a nonempty set of admitted mode IDs')
        self.meter.pay('interface_binding', 'source_and_nonempty_mode_sets', self.m * len(self.modes) + sum(map(len, possible)) + 8)
        return possible

    def _profile(self, row):
        if type(row) is not int or not 0 <= row < len(self.instances):
            raise ValueError('Unknown logical source row')
        profile, instance = self.bank.rows[row], self.instances[row]
        if profile['row'] != row or profile['source_identity'] != instance['identity']:
            raise ValueError('Compact profile belongs to a different logical source')
        if not profile['witnesses']:
            raise ValueError('At least one actually checked feasible repair required')
        for witness in profile['witnesses']:
            key = (row, witness['model'], witness['violation_mask'])
            if not isinstance(witness.get('receipt_id'), str):
                raise ValueError('Checked witness receipt identity required')
            if key not in self._checked_witnesses:
                got = native.profile_kernel.compile_witness(instance, witness['model'], self.meter)
                if got['violation_mask'] != witness['violation_mask']:
                    raise ValueError('Candidate mask differs from the actual hard-feasible assignment')
                self._checked_witnesses[key] = witness['receipt_id']
                self.meter.pay('interface_admission', 'checked_candidate_binding_storage', 4)
        signature = []
        for tree in profile['trees']:
            leaves = tuple(tree['leaf_masks'])
            receipt = tree.get('receipt_id')
            if (not isinstance(receipt, str) or not leaves
                    or any(type(z) is not int or not 0 <= z < (1 << self.m) for z in leaves)):
                raise ValueError('Admitted tree identity and nonempty ordered Boolean supports required')
            key = (row, receipt)
            if key in self._tree_bindings and self._tree_bindings[key] != leaves:
                raise ValueError('A retained tree receipt changed its admitted masks')
            self._tree_bindings[key] = leaves
            signature.append((receipt, leaves))
        self.meter.pay('interface_binding', 'projected_action_and_proof_fields',
                       4 + 3 * len(profile['witnesses']) + sum(2 + len(t['leaf_masks']) for t in profile['trees']))
        return profile, tuple(signature)

    def admit_cut_dual(self, row, raw_exports, multipliers):
        """Actually check supplied raw RUP exports, then combine their cuts.

        ``multipliers`` contains one nonnegative exact rational per export.
        This performs no LP proposal or global search. Fresh consumers must
        bring the original exported proof bytes, not saved cut/dual flags.
        """
        self._profile(row)
        cuts = [rup.check_export(self.instances[row], raw, self.meter) for raw in raw_exports]
        certificate = cut_dual.rational_dual(cuts, multipliers, self.structural_ids[row], self.meter)
        if not any(c['receipt_id'] == certificate['receipt_id'] for c in self.duals[row]):
            self.duals[row].append(certificate)
            self.cuts[row].extend(c for c in cuts if not any(old['receipt_id'] == c['receipt_id'] for old in self.cuts[row]))
            self.meter.pay('interface_admission', 'checked_dual_dependency_storage', len(cuts) + 4)
        return copy.deepcopy(certificate)

    def _point_lower(self, row, profile, weights):
        options = [(F(0), 'nonnegative_objective')]
        for tree in profile['trees']:
            value = min(vertex.dot(z, weights, self.meter) for z in tree['leaf_masks'])
            options.append((F(value), tree['receipt_id']))
            self.meter.pay('interface_compile', 'admitted_tree_point_minimum', len(tree['leaf_masks']) + 1)
        for certificate in self.duals[row]:
            value = cut_dual.point_lower(certificate, weights, self.meter,
                                         integral=all(type(w) is int for w in weights))
            options.append((F(value), certificate['receipt_id']))
        self.meter.pay('interface_compile', 'same_source_point_lower_maximum', len(options))
        return max(options, key=lambda x: x[0])

    def _anchors(self, row, profile, tree_signature):
        signature = (tree_signature, tuple(c['receipt_id'] for c in self.duals[row]))
        cached = self._anchor_cache.get(row)
        if cached is None or cached['signature'] != signature:
            weights = [[self.n * w for w in mode] for mode in self.modes]
            self.meter.pay('interface_compile', 'full_cohort_mode_scaling', self.m * len(self.modes))
            values = [self._point_lower(row, profile, v) for v in weights]
            cached = dict(signature=signature, weights=weights,
                          lowers=[value for value, _ in values], proof_ids=[receipt for _, receipt in values])
            self._anchor_cache[row] = cached
            self.meter.pay('interface_compile', 'scalar_anchor_storage', (self.m + 2) * len(self.modes))
        self.meter.pay('interface_query', 'scalar_anchor_cache_lookup_and_read', 1 + 2 * len(self.modes))
        return cached

    def mode_anchor_lowers(self, row, *, costs=None):
        """Own admitted lower at each exact full-cohort objective N*mode[k]."""
        self._state(self.costs if costs is None else costs)
        profile, signature = self._profile(row)
        return list(self._anchors(row, profile, signature)['lowers'])

    @staticmethod
    def _action(witness, **fields):
        return dict(action='replace' if witness is None else 'repair',
                    model=None if witness is None else witness['model'],
                    mask=None if witness is None else witness['violation_mask'],
                    witness_id=None if witness is None else witness['receipt_id'], **fields)

    @staticmethod
    def _best(options):
        return min(options, key=lambda r: (r['bound'], r['mask'] is None,
                                          -1 if r['model'] is None else r['model']))

    def evaluate(self, row, price, tolerance=0, *, costs=None,
                 methods=('tree', 'scalar_anchor'), hull_cap=256):
        """Return the best requested uniform bound and one fixed checked action.

        ``tree`` uses joint finite-row support and one proof at a time;
        ``scalar_anchor`` transports the strongest admitted N*mode lowers;
        ``dual_box`` uses retained checked rational cuts over a warranted box;
        ``hull`` constructs capped grouped cohort generators and permits proof
        choice separately at each generator. An unavailable optional method is
        reported explicitly; it never becomes a zero-bound fallback.
        """
        before = self.meter.total
        costs = self.costs if costs is None else costs
        possible = self._state(costs)
        profile, signature = self._profile(row)
        price, tolerance = F(price), F(tolerance)
        if price < 0 or tolerance < 0:
            raise ValueError('Nonnegative replacement price and requested regret required')
        methods = tuple(methods)
        if not methods or len(set(methods)) != len(methods) or any(m not in METHODS for m in methods):
            raise ValueError('Choose distinct supported evaluator methods')
        actions = profile['witnesses'] + [None]
        answers, unavailable = {}, {}
        if 'tree' in methods:
            got = joint.certificate(profile, costs, price)
            witness = next((w for w in profile['witnesses'] if w['model'] == got['model']), None)
            got['witness_id'] = None if witness is None else witness['receipt_id']
            answers['tree'] = got
        if 'scalar_anchor' in methods:
            anchors = self._anchors(row, profile, signature)
            options = [self._action(w, **source_anchor.bound(None if w is None else w['violation_mask'],
                       self.modes, possible, anchors['lowers'], price, self.meter)) for w in actions]
            answers['scalar_anchor'] = self._best(options) | dict(anchor_proof_ids=list(anchors['proof_ids']))
        if 'dual_box' in methods:
            if self.duals[row]:
                lo = [sum(min(self.modes[k][j] for k in p) for p in possible) for j in range(self.m)]
                hi = [sum(max(self.modes[k][j] for k in p) for p in possible) for j in range(self.m)]
                self.meter.pay('interface_compile', 'warranted_coordinate_enclosure', 2 * self.m * sum(map(len, possible)))
                options = [self._action(w, bound=cut_dual.fixed_box_bound(c,
                           None if w is None else w['violation_mask'], lo, hi, price, self.meter),
                           proof_id=c['receipt_id']) for c in self.duals[row] for w in actions]
                answers['dual_box'] = self._best(options)
            else:
                unavailable['dual_box'] = 'No raw-checked cut dual has been admitted for this logical source'
        if 'hull' in methods:
            key = (possible, hull_cap)
            if key not in self._hull_cache:
                self._hull_cache[key] = cohort_hull.generators(self.modes, possible, self.meter, hull_cap)
            hull = self._hull_cache[key]
            self.meter.pay('interface_query', 'grouped_hull_cache_lookup')
            if hull['status'] == 'complete':
                point = [self._point_lower(row, profile, v) for v in hull['vertices']]
                lowers = [lower for lower, _ in point]
                options = [self._action(w, bound=vertex.anchor_certificate(
                           None if w is None else w['violation_mask'], hull['vertices'], lowers, price, self.meter))
                           for w in actions]
                answers['hull'] = self._best(options) | dict(
                    anchor_weights=hull['vertices'], anchor_lowers=lowers,
                    anchor_proof_ids=[receipt for _, receipt in point],
                    generating_points=hull['generating_points'], group_product_size=hull['group_product_size'])
            else:
                unavailable['hull'] = hull['reason']
        if not answers:
            raise ValueError('No requested evaluator is available within the admitted evidence and construction cap')
        self.meter.pay('interface_query', 'method_comparison_and_source_bound_output', len(answers) + 18)
        chosen = self._best([answer | dict(method=method) for method, answer in answers.items()])
        return chosen | dict(version=VERSION, row=row, price=price, tolerance=tolerance,
                             status='checked_action' if chosen['bound'] <= tolerance else 'unresolved',
                             logical_source_id=self.instances[row]['identity'],
                             structural_source_id=self.structural_ids[row], cost_source_id=self.source_id,
                             possible_modes=[list(p) for p in possible],
                             method_bounds={method: answer['bound'] for method, answer in answers.items()},
                             method_answers=answers, unavailable=unavailable,
                             evidence=dict(tree_receipt_ids=[t['receipt_id'] for t in profile['trees']],
                                           cut_receipt_ids=[c['receipt_id'] for c in self.cuts[row]],
                                           dual_receipt_ids=[c['receipt_id'] for c in self.duals[row]],
                                           cost_receipt_ids=list(costs.receipts)),
                             invoice=dict(evaluation_units=self.meter.total - before,
                                          cumulative_common_meter_units=self.meter.total),
                             domain='One checked action over all compatible finite-row configurations and their convex hull; nonnegative objective costs',
                             admission='Compact trees require upstream actual raw-proof admission; candidate assignments and new cut exports are checked here')

    __call__ = evaluate
