#!/usr/bin/env python3
"""Focused semantic probe for the admitted evaluator, without solver calls.

ChatGPT (GPT-6 Astra Pro), 2026-10-12. DEVELOPMENT. A new two-variable
construction, not an old-workload replay or independent empirical validation.
"""
from datetime import datetime, timezone
import copy
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import sys
import time

import repair_interface as interface
from repair_interface import joint, native, rup
import native_stream


HERE = Path(__file__).resolve().parent


def jsonable(value):
    if isinstance(value, F):
        return value.numerator if value.denominator == 1 else str(value)
    if isinstance(value, dict):
        return {k: jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(v) for v in value]
    return value


def expect_rejection(name, call, records):
    try:
        call()
    except ValueError as exc:
        records.append(dict(case=name, result='rejected', reason=str(exc)))
    else:
        raise AssertionError(f'Invalid boundary accepted: {name}')


def run(output):
    if output.exists():
        raise FileExistsError('Preserve earlier semantic-probe evidence')
    wall, cpu = time.perf_counter_ns(), time.process_time_ns()
    meter = native.kernel.Meter()
    instance = dict(row=0, variables=2, hard=[[1, 2]],
                    soft=[dict(weight=1, clause=[-1]), dict(weight=1, clause=[-2])],
                    public_incumbent=1, objective_max=2)
    instance['identity'] = native.kernel.digest(instance)
    # A hand-constructed complete budget-zero tree. All feasible assignments
    # violate at least one of the two soft clauses. The checker, not its shape
    # or the ensuing compact mask list, establishes this fact.
    proof = ['b', 0, ['b', 1, ['h', 0], ['w', [1]]], ['w', [0]]]
    native.kernel.check_negative(instance, 0, proof, meter)
    leaves = native.profile_kernel.compile_tree(proof, meter)
    witnesses = []
    for model in (1, 2):
        witness = native.profile_kernel.compile_witness(instance, model, meter)
        witness['receipt_id'] = native.kernel.digest(dict(source=instance['identity'], model=model,
                                                         violation_mask=witness['violation_mask']))
        witnesses.append(witness)
    tree_id = native.kernel.digest(dict(source=instance['identity'], budget=0, proof=proof))
    bank = native_stream.CompactBank([dict(row=0, source_identity=instance['identity'], witnesses=witnesses,
               trees=[dict(original_budget=0, leaf_masks=leaves, receipt_id=tree_id)])], meter)
    modes, cohort = [[1, 3], [3, 1]], 2
    cost_source = native.kernel.digest(dict(modes=modes, cohort=cohort, meaning='Two distinct fixed cost rows'))
    costs = joint.CostState(modes, cohort, cost_source, meter)
    evaluator = interface.RepairEvaluator([instance], bank, costs, meter)
    first = evaluator(0, 7, methods=interface.METHODS)
    assert first['unavailable'].keys() == {'dual_box'}
    assert first['method_bounds'] == dict(tree=4, scalar_anchor=4, hull=4)
    anchors = evaluator.mode_anchor_lowers(0)
    compilation_before = meter.operations['interface_compile', 'scalar_anchor_storage']
    assert evaluator.mode_anchor_lowers(0) == anchors == [2, 2]
    assert meter.operations['interface_compile', 'scalar_anchor_storage'] == compilation_before

    # This exact threshold CNF is unit-inconsistent. The empty RUP line is a
    # proposal; check_export actually reconstructs and checks it. No SAT call
    # or LP proposal is used to obtain the cut or rational multiplier.
    exported = dict(structural_source_id=native.structural_id(instance), original_source_id=instance['identity'],
                    weights=[1, 1], budget=0,
                    encoding=rup.encode(instance, [1, 1], 0, meter), raw_proof=['0'])
    dual = evaluator.admit_cut_dual(0, [exported], [2])
    assert dual['multipliers'] == ['2']

    # Post-evaluator diagnostics enumerate only this new finite probe. Their
    # optima are never supplied to evaluator compilation or action selection.
    diagnostic = native.kernel.Meter()
    feasible_masks = []
    for model in range(4):
        try:
            feasible_masks.append(native.profile_kernel.compile_witness(instance, model, diagnostic)['violation_mask'])
        except ValueError:
            pass
    cases = []
    for possible in product(((0, 1), (0,), (1,)), repeat=2):
        branch = copy.copy(costs)
        branch.possible = list(possible)
        for price in (3, 7):
            answer = evaluator(0, price, costs=branch, methods=interface.METHODS)
            checked = []
            for method, action in answer['method_answers'].items():
                actual_worst = F(0)
                for latent in product(*possible):
                    weights = [sum(modes[k][j] for k in latent) for j in range(2)]
                    optimum = min([price] + [sum(w for j, w in enumerate(weights) if z & (1 << j)) for z in feasible_masks])
                    cost = price if action['mask'] is None else sum(w for j, w in enumerate(weights) if action['mask'] & (1 << j))
                    actual_worst = max(actual_worst, cost - optimum)
                    diagnostic.pay('diagnostic', 'finite_source_actual_regret', 2 * len(feasible_masks) + 8)
                assert actual_worst <= action['bound']
                checked.append(dict(method=method, bound=action['bound'], actual_worst=actual_worst))
            cases.append(dict(possible=possible, price=price, best_method=answer['method'],
                              best_bound=answer['bound'], methods=checked))
    assert len(cases) == 18
    assert all(len(c['methods']) == 4 for c in cases)

    # A second independently checked tree may enter the existing live bank.
    # Equivalent support still requires refreshed paid anchor compilation.
    proof2 = ['b', 0, ['b', 1, ['h', 0], ['w', [1]]], ['b', 1, ['w', [0]], ['w', [0, 1]]]]
    native.kernel.check_negative(instance, 0, proof2, meter)
    leaves2 = native.profile_kernel.compile_tree(proof2, meter)
    proof2_id = native.kernel.digest(dict(source=instance['identity'], budget=0, proof=proof2))
    bank.retain(0, dict(source_identity=instance['identity'], witness=None,
                       checked_lower_receipt=dict(checked=True, budget=0, leaf_masks=leaves2,
                                                  receipt_id=proof2_id)), 'focused_probe_checked_retention')
    compilation_before = meter.operations['interface_compile', 'scalar_anchor_storage']
    assert evaluator.mode_anchor_lowers(0) == anchors
    assert meter.operations['interface_compile', 'scalar_anchor_storage'] > compilation_before

    rejected = []
    alien = copy.copy(costs)
    alien.source_id = 'different-cost-source'
    expect_rejection('foreign_cost_source', lambda: evaluator(0, 7, costs=alien), rejected)
    negative = copy.copy(costs)
    negative.modes = ((-1, 3), (3, 1))
    expect_rejection('negative_or_changed_cost_modes', lambda: evaluator(0, 7, costs=negative), rejected)
    empty = copy.copy(costs)
    empty.possible = [(), (0, 1)]
    expect_rejection('empty_cost_row', lambda: evaluator(0, 7, costs=empty), rejected)
    expect_rejection('negative_replacement_price', lambda: evaluator(0, -1), rejected)
    bad_export = copy.deepcopy(exported)
    bad_export['structural_source_id'] = 'foreign-logical-source'
    expect_rejection('foreign_raw_cut', lambda: evaluator.admit_cut_dual(0, [bad_export], [1]), rejected)
    old_leaves = bank.rows[0]['trees'][0]['leaf_masks']
    bank.rows[0]['trees'][0]['leaf_masks'] = [3]
    expect_rejection('mutated_retained_tree', lambda: evaluator(0, 7), rejected)
    bank.rows[0]['trees'][0]['leaf_masks'] = old_leaves
    old_mask = bank.rows[0]['witnesses'][0]['violation_mask']
    bank.rows[0]['witnesses'][0]['violation_mask'] = 0
    expect_rejection('false_candidate_violation_mask', lambda: evaluator(0, 7), rejected)
    bank.rows[0]['witnesses'][0]['violation_mask'] = old_mask
    capped = evaluator(0, 7, methods=('tree', 'hull'), hull_cap=1)
    assert capped['unavailable']['hull'] == 'Generator construction cap'
    assert capped['bound'] == capped['method_bounds']['tree']

    files = [Path(interface.__file__), Path(__file__),
             Path(joint.__file__), Path(native_stream.__file__), Path(rup.__file__),
             Path(interface.source_anchor.__file__), Path(interface.vertex.__file__),
             Path(interface.cohort_hull.__file__), Path(interface.cut_dual.__file__),
             Path(native.kernel.__file__), Path(native.profile_kernel.__file__)]
    result = dict(status='passed', evidence='DEVELOPMENT finite semantic probe',
                  contributor='ChatGPT (GPT-6 Astra Pro)', created_utc=datetime.now(timezone.utc).isoformat(),
                  hashes={p.name: native.sha(p) for p in files}, source=instance,
                  raw_tree=proof, raw_retained_tree=proof2, raw_cut_export=exported,
                  cost_contract=dict(modes=modes, cohort_size=cohort, source_id=cost_source),
                  summary=dict(compatible_source_price_cases=18, method_regret_checks=72,
                               admission_rejections=len(rejected), optional_hull_cap_falls_back=True,
                               scalar_cache_reused=True, retained_tree_invalidates_anchor_cache=True),
                  cases=cases, rejected=rejected, admitted_dual=dual,
                  new_LP_SAT_IHS_proof_search_or_audit_calls=0,
                  invoice=meter.record(), post_evaluation_diagnostic_invoice=diagnostic.record(),
                  timing=dict(wall_ns=time.perf_counter_ns() - wall, process_ns=time.process_time_ns() - cpu),
                  scope='All 18 declared price/refinement cases on this two-variable construction; no transfer claim or economic ranking')
    output.write_text(json.dumps(jsonable(result), indent=2) + '\n')
    print(json.dumps(result['summary'] | dict(status=result['status'], units=meter.total,
                                            diagnostic_units=diagnostic.total)))


if __name__ == '__main__':
    run(Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / 'repair_interface_results.json')
