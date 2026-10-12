#!/usr/bin/env python3
"""Compile uniform regret regions from saved witness/tree supports.

ChatGPT (GPT-6 Astra Pro), 2026-10-12. DEVELOPMENT. No solver calls.
Exact diagnostic optima are not read by any gate-selection function.
See reprice_regions_findings.md for the fixed-pair versus union distinction.
"""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time


DIRECTORY = Path(__file__).resolve().parent
PRICE, TAU = F(6), F(1)


class Meter:
    def __init__(self):
        self.counts = Counter()

    def pay(self, operation, units=1):
        self.counts[operation] += units

    def record(self):
        return dict(total=sum(self.counts.values()), operations=dict(sorted(self.counts.items())))


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def admitted(path, meter):
    raw = path.read_bytes()
    meter.pay('input_read_eight_byte_words', (len(raw)+7)//8)
    meter.pay('sha256_message_blocks', (len(raw)+9+63)//64)
    return raw


def inequality(coefficients, price_coefficient, weights, price, tau, meter,
               kind, leaf_mask=None):
    center, sensitivity = price_coefficient*price, F(0)
    meter.pay('price_coefficient_multiply')
    for d, w in zip(coefficients, weights):
        meter.pay('coefficient_read_multiply_accumulate', 4)
        center += d*w
        sensitivity += abs(d)*w
    slack = tau-center
    meter.pay('slack_subtraction_and_comparison', 2)
    cap = None if not sensitivity else slack/sensitivity
    meter.pay('radius_division' if sensitivity else 'constant_inequality_case')
    return dict(coefficients=list(coefficients), price_coefficient=price_coefficient,
                kind=kind, leaf_mask=leaf_mask, center_value=str(center),
                weighted_absolute_sum=str(sensitivity), slack=str(slack),
                radius_limit=None if cap is None else str(cap),
                center_admitted=slack >= 0)


def compile_region(profile, tree_index, tree, witness, weights, price, tau, meter):
    n = len(weights)
    leaves = tree['leaf_masks']
    upper = None if witness is None else witness['violation_mask']
    action = 'replacement' if witness is None else 'repair'
    inequalities = []
    for leaf in leaves:
        meter.pay('leaf_support_admission', n+1)
        coefficients = [((upper >> j) & 1)-((leaf >> j) & 1)
                        if upper is not None else -((leaf >> j) & 1)
                        for j in range(n)]
        inequalities.append(inequality(coefficients, 0 if upper is not None else 1,
                            weights, price, tau, meter, 'tree_leaf', leaf))
    if upper is not None:
        coefficients = [(upper >> j) & 1 for j in range(n)]
        inequalities.append(inequality(coefficients, -1, weights, price, tau,
                                        meter, 'replacement_comparator'))
    feasible = all(q['center_admitted'] for q in inequalities)
    radius, limiting = (F(1), None) if feasible else (None, None)
    if feasible:
        for j, q in enumerate(inequalities):
            meter.pay('radius_cap_comparison')
            cap = None if q['radius_limit'] is None else F(q['radius_limit'])
            if cap is not None and cap < radius:
                radius, limiting = cap, j
    center_cost = price if upper is None else sum(w for j, w in enumerate(weights)
                                                 if upper & (1 << j))
    meter.pay('retained_action_center_cost', n if upper is not None else 1)
    return dict(row=profile['row'], source_identity=profile['source_identity'],
                action=action, witness_model=None if witness is None else witness['model'],
                violation_mask=upper, tree_index=tree_index,
                tree_origin=tree.get('origin', 'checked_archived_tree'),
                original_tree_budget=tree['original_budget'],
                tree_leaf_masks=list(leaves), center_action_cost=str(center_cost),
                center_admitted=feasible,
                maximum_fixed_pair_radius=None if radius is None else str(radius),
                limiting_inequality=limiting, inequalities=inequalities)


def compile_profiles(profiles, weights, price, tau, meter):
    result = []
    for profile in profiles:
        trees = list(enumerate(profile['trees']))
        if not trees:
            trees = [(None, dict(original_budget=None, leaf_masks=[0],
                                 origin='nonnegative_objective'))]
        regions = []
        for index, tree in trees:
            for witness in profile['witnesses']:
                regions.append(compile_region(profile, index, tree, witness,
                                               weights, price, tau, meter))
            regions.append(compile_region(profile, index, tree, None,
                                           weights, price, tau, meter))
        candidates = [j for j, region in enumerate(regions) if region['center_admitted']]
        if not candidates:
            result.append(dict(row=profile['row'], source_identity=profile['source_identity'],
                               regions=regions, selected_region=None,
                               maximum_fixed_pair_radius=None))
            continue
        selected = min(candidates, key=lambda j: (
            -F(regions[j]['maximum_fixed_pair_radius']),
            F(regions[j]['center_action_cost']),
            regions[j]['action'],
            -1 if regions[j]['witness_model'] is None else regions[j]['witness_model'], j))
        meter.pay('fixed_pair_selection', len(candidates))
        region = regions[selected]
        result.append(dict(row=profile['row'], source_identity=profile['source_identity'],
                           regions=regions, selected_region=selected,
                           maximum_fixed_pair_radius=region['maximum_fixed_pair_radius']))
    return result


def box_membership(profile, weights, original_weights, price, tau, source_identity, meter):
    meter.pay('source_price_and_tolerance_binding', 3)
    if (profile['selected_region'] is None or source_identity != profile['source_identity']
            or F(price) != PRICE or F(tau) != TAU):
        return dict(accepted=False)
    radius = F(profile['maximum_fixed_pair_radius'])
    if len(weights) != len(original_weights):
        return dict(accepted=False)
    for w, old in zip(weights, original_weights):
        meter.pay('relative_box_lower_upper_checks', 6)
        if not (1-radius)*old <= F(w) <= (1+radius)*old:
            return dict(accepted=False)
    region = profile['regions'][profile['selected_region']]
    return dict(accepted=True, action=region['action'],
                witness_model=region['witness_model'], tree_index=region['tree_index'],
                uniform_regret_bound=str(TAU))


def check_action(instance, region, meter):
    if region['action'] == 'replacement':
        meter.pay('available_replacement_action')
        return dict(feasible=True, action='replacement', fixed_price=str(PRICE))
    model = region['witness_model']
    if type(model) is not int or not 0 <= model < 1 << instance['variables']:
        raise ValueError('Malformed selected witness')
    def satisfied(clause):
        meter.pay('selected_witness_clause')
        for lit in clause:
            meter.pay('selected_witness_literal')
            if ((model >> (abs(lit)-1)) & 1) == int(lit > 0):
                return True
        return False
    if not all(satisfied(clause) for clause in instance['hard']):
        raise ValueError('Selected repair is not hard-feasible')
    mask = 0
    for j, soft in enumerate(instance['soft']):
        if not satisfied(soft['clause']):
            mask |= 1 << j
    if mask != region['violation_mask']:
        raise ValueError('Selected action differs from its compiled objective vector')
    return dict(feasible=True, action='repair', witness_model=model,
                violation_mask=mask, hard_clauses_checked=len(instance['hard']))


def main():
    target = DIRECTORY/'reprice_regions_results.json'
    if target.exists():
        raise FileExistsError('Preserve existing development evidence')
    start, cpu = time.perf_counter_ns(), time.process_time_ns()
    admission, compilation, membership, action_check = (Meter() for _ in range(4))
    files = {name: admitted(DIRECTORY/name, admission) for name in
             ('maxsat_reprice_results.json', 'maxsat_repair_results.json',
              'maxsat_reprice.py', 'maxsat_repair.py')}
    archive = json.loads(files['maxsat_reprice_results.json'])
    original = json.loads(files['maxsat_repair_results.json'])
    if archive['status'] != 'complete' or original['status'] != 'complete':
        raise ValueError('Incomplete archive')
    if (digest(files['maxsat_reprice.py']) != archive['implementation_sha256']
            or digest(files['maxsat_repair.py']) != original['implementation_sha256']
            or digest(files['maxsat_repair_results.json']) != archive['input_result_sha256']
            or archive['input_source_identity'] != original['source_identity']):
        raise ValueError('Archive source/implementation binding changed')
    # These are the only old result fields that feed region construction.
    weights = tuple(map(F, archive['old_weights']))
    profiles = archive['compiled_profiles']
    if any(w <= 0 for w in weights):
        raise ValueError('Positive original weights required')
    for profile in profiles:
        instance = original['instances'][profile['row']]
        if (instance['identity'] != profile['source_identity']
                or tuple(F(s['weight']) for s in instance['soft']) != weights):
            raise ValueError('Profile or weight-vector identity mismatch')
    rows = compile_profiles(profiles, weights, PRICE, TAU, compilation)
    membership_results, action_checks = [], []
    for row in rows:
        membership_results.append(box_membership(row, weights, weights, PRICE, TAU,
                                                 row['source_identity'], membership))
        assert membership_results[-1]['accepted']
        region = row['regions'][row['selected_region']]
        action_checks.append(check_action(original['instances'][row['row']],
                                          region, action_check))
        radius = F(row['maximum_fixed_pair_radius'])
        for inequality in region['inequalities']:
            # Algebraic support-function certificate, not sampled parameters.
            assert (F(inequality['center_value'])
                    + radius*F(inequality['weighted_absolute_sum'])) <= TAU
        limiting = region['limiting_inequality']
        if limiting is not None:
            inequality = region['inequalities'][limiting]
            assert (F(inequality['center_value'])
                    + radius*F(inequality['weighted_absolute_sum'])) == TAU
            row['limiting_box_corner'] = [str(w*(1+radius*(1 if d > 0 else -1 if d < 0 else 0)))
                                         for w, d in zip(weights, inequality['coefficients'])]
    radii = [F(row['maximum_fixed_pair_radius']) for row in rows]
    result = dict(status='complete', evidence='DEVELOPMENT',
                  contributor='ChatGPT (GPT-6 Astra Pro)',
                  generated_utc=datetime.now(timezone.utc).isoformat(),
                  command=['python', 'v3/discovery/s05/reprice_regions.py'],
                  implementation_sha256=digest(Path(__file__).read_bytes()),
                  source_files={name:dict(sha256=digest(raw), bytes=len(raw))
                                for name, raw in files.items()},
                  input_source_identity=archive['input_source_identity'],
                  original_weights=list(map(str, weights)), price=str(PRICE), tolerance=str(TAU),
                  allowed_weight_box='w_j=w0_j*(1+e_j), |e_j|<=rho<=1; nonnegative real weights',
                  maximum_scope='Largest box certified by one fixed feasible action and one '
                                'retained tree (or nonnegativity) per row; not general union-cover optimization.',
                  gate_inputs=['old_weights', 'compiled_profiles'],
                  diagnostic_optima_used=False, new_solver_calls=0,
                  tariff='Each listed named operation is one service unit. File admission charges '
                         'eight-byte input words and SHA-256 message blocks; coefficient '
                         'compilation and box membership are separately counted. These are '
                         'operation tariffs, not currency or constant-bit complexity.',
                  inherited_paid_compilation=archive['compilation'],
                  invoices=dict(source_admission=admission.record(), region_compilation=compilation.record(),
                                box_membership=membership.record(), selected_action_checks=action_check.record()),
                  rows=rows, membership_at_original_weights=membership_results,
                  selected_action_checks=action_checks,
                  summary=dict(rows=len(rows), positive_radius_rows=sum(r > 0 for r in radii),
                               zero_radius_rows=sum(r == 0 for r in radii),
                               common_fixed_profile_radius=str(min(radii)),
                               largest_individual_radius=str(max(radii)),
                               regions=sum(len(row['regions']) for row in rows),
                               center_infeasible_regions=sum(not reg['center_admitted']
                                                            for row in rows for reg in row['regions'])),
                  process_ns=time.process_time_ns()-cpu, elapsed_wall_ns=time.perf_counter_ns()-start)
    target.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(summary=result['summary'],
                          invoices={key:value['total'] for key,value in result['invoices'].items()},
                          radii=[dict(row=row['row'], rho=row['maximum_fixed_pair_radius'],
                                      action=row['regions'][row['selected_region']]['action'],
                                      model=row['regions'][row['selected_region']]['witness_model']) for row in rows])))


if __name__ == '__main__':
    main()
