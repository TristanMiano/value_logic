#!/usr/bin/env python3
"""Small actual robust-witness purchases with raw-checked source evidence.

DEVELOPMENT. ChatGPT (GPT-6 Astra Pro), 2026-10-12. Five capped MIP calls
on two declared constructed sources; no acquisition on the historical cohort.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import sys
import time

import robust_witness as robust
from robust_witness import native
import joint_repair as joint
import native_stream as stream
import source_anchor
from repair_interface import RepairEvaluator


HERE = Path(__file__).resolve().parent


def jsonable(value):
    if isinstance(value, F):
        return value.numerator if value.denominator == 1 else str(value)
    if isinstance(value, dict):
        return {k: jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(v) for v in value]
    return value


def identified(instance):
    instance['identity'] = native.kernel.digest(instance)
    return instance


def cost_manifest(modes, hidden):
    record = dict(version='s07-robust-witness-constructed-cost-source-v1',
                  possible_cost_modes=modes, cohort_size=len(hidden), hidden_modes=hidden)
    record['source_identity'] = native.kernel.digest(record)
    return record


def admit_tree(instance, budget, proof, meter):
    native.kernel.check_negative(instance, budget, proof, meter)
    leaves = native.profile_kernel.compile_tree(proof, meter)
    return dict(original_budget=budget, leaf_masks=leaves,
                receipt_id=native.kernel.digest(dict(source=instance['identity'], budget=budget, proof=proof)))


def start(instance, source, initial_proof):
    meter = native.kernel.Meter()
    costs = joint.CostState(source['possible_cost_modes'], source['cohort_size'], source['source_identity'], meter)
    oracle = joint.CostOracle(source)
    witness = native.profile_kernel.compile_witness(instance, instance['public_incumbent'], meter)
    witness['receipt_id'] = native.kernel.digest(dict(source=instance['identity'], model=witness['model'],
                                                     violation_mask=witness['violation_mask']))
    tree = admit_tree(instance, 0, initial_proof, meter)
    bank = stream.CompactBank([dict(row=0, source_identity=instance['identity'], witnesses=[witness], trees=[tree])], meter)
    evaluator = RepairEvaluator([instance], bank, costs, meter)
    proposer = robust.RobustWitness(instance, costs, meter)
    return meter, costs, oracle, bank, evaluator, proposer


def proposal(stage, instance, costs, bank, evaluator, proposer, price, caps=None):
    before = evaluator(0, price)
    lowers = evaluator.mode_anchor_lowers(0)
    result = proposer.propose(costs, lowers, price, **(caps or {}))
    if result['witness'] is not None:
        # Proposer has checked this exact action against the original source.
        # Retain the witness only; there is deliberately no lower receipt.
        bank.retain(0, result, stage)
    after = evaluator(0, price)
    assert result['checked_lower_receipt'] is None
    assert result['independently_checked_lower'] is False
    assert after['bound'] <= before['bound']
    assert result['state_before']['highs_object_id'] == result['state_after']['highs_object_id']
    return dict(stage=stage, costs=costs.snapshot(), anchor_lowers=lowers,
                before=before, proposal=result, after=after)


def diagnostics(instance, source, stages):
    """Enumerate only after the actual proposals; never supply an optimum."""
    meter = native.kernel.Meter()
    feasible = []
    for model in range(1 << instance['variables']):
        try:
            feasible.append(native.profile_kernel.compile_witness(instance, model, meter))
        except ValueError:
            pass
    records = []
    for stage in stages:
        possible = stage['costs']['possible_modes']
        modes = source['possible_cost_modes']
        price = stage['after']['price']
        surrogate = [(source_anchor.bound(w['violation_mask'], modes, possible, stage['anchor_lowers'], price, meter)['bound'], w['model'])
                     for w in feasible]
        optimum, best_model = min(surrogate)
        candidate = stage['proposal']['witness']
        candidate_surrogate = None if candidate is None else next(b for b, m in surrogate if m == candidate['model'])
        actual_worst, configurations = F(0), 0
        for latent in product(*possible):
            weights = [sum(modes[k][j] for k in latent) for j in range(len(modes[0]))]
            values = {w['model']: sum(value for j, value in enumerate(weights) if w['violation_mask'] & (1 << j)) for w in feasible}
            true_best = min([price] + list(values.values()))
            action = stage['after']
            true_cost = price if action['action'] == 'replace' else values[action['model']]
            regret = true_cost - true_best
            assert regret <= action['bound']
            actual_worst = max(actual_worst, regret)
            configurations += 1
            meter.pay('post_proposal_diagnostic', 'actual_finite_configuration_costs_and_regret',
                      len(weights) * (len(feasible) + len(latent)) + len(feasible) + 8)
        records.append(dict(stage=stage['stage'], exact_best_scalar_repair_bound=optimum,
                            one_best_model=best_model, proposed_model=None if candidate is None else candidate['model'],
                            proposed_scalar_bound=candidate_surrogate,
                            proposal_suboptimality=None if candidate_surrogate is None else candidate_surrogate - optimum,
                            final_evaluator_bound=stage['after']['bound'], actual_worst_regret=actual_worst,
                            compatible_configurations=configurations))
    return dict(records=records, invoice=meter.record(),
                scope='Post-call exact small-source diagnostics only; no optimum/native bound feeds any proposal or certificate')


def run(output):
    if output.exists():
        raise FileExistsError('Preserve actual robust witness calls')
    wall, cpu = time.perf_counter_ns(), time.process_time_ns()
    weak_proof = ['b', 0, ['b', 1, ['h', 0], ['w', [1]]], ['w', [0]]]
    first = identified(dict(row=0, variables=2, hard=[[1, 2]],
                            soft=[dict(weight=1, clause=[-1]), dict(weight=1, clause=[-2])],
                            public_incumbent=3, objective_max=2))
    first_source = cost_manifest([[3, 1], [1, 3]], [0])
    meter, costs, oracle, bank, evaluator, engine = start(first, first_source, weak_proof)
    initial_state = engine.state()
    first_stages = [proposal('initial_full_source', first, costs, bank, evaluator, engine, 8)]
    first_stages.append(proposal('zero_search_cap_retains_paid_attempt', first, costs, bank, evaluator, engine, 8,
                                 dict(seconds=0, nodes=0)))
    first_record = dict(source=first, cost_manifest=first_source, raw_initial_proof=weak_proof,
                        initial_native_state=initial_state, stages=first_stages,
                        final_native_state=engine.state(), setup_invoice=engine.setup_invoice,
                        setup_timing=engine.setup_timing, operation_invoice=meter.record(),
                        actual_audits=[], final_profiles=bank.rows)

    second = identified(dict(row=0, variables=3, hard=[[1, 2], [-1, 3]],
                             soft=[dict(weight=1, clause=[-1]), dict(weight=1, clause=[-2]),
                                   dict(weight=1, clause=[-3]), dict(weight=1, clause=[1, -2])],
                             public_incumbent=7, objective_max=4))
    second_source = cost_manifest([[4, 1, 2, 3], [1, 4, 3, 1], [2, 2, 1, 4]], [0, 1])
    meter2, costs2, oracle2, bank2, evaluator2, engine2 = start(second, second_source, weak_proof)
    initial_state2 = engine2.state()
    second_stages = [proposal('weak_admitted_anchors', second, costs2, bank2, evaluator2, engine2, 15)]
    strong_proof = ['b', 0,
                    ['b', 1, ['h', 0], ['b', 2, ['w', [1, 3]], ['w', [1, 2, 3]]]],
                    ['b', 2, ['h', 1], ['b', 1, ['w', [0, 2]], ['w', [0, 1, 2]]]]]
    new_tree = admit_tree(second, 1, strong_proof, meter2)
    bank2.retain(0, dict(source_identity=second['identity'], witness=None,
                        checked_lower_receipt=dict(checked=True, budget=1, leaf_masks=new_tree['leaf_masks'],
                                                   receipt_id=new_tree['receipt_id'])), 'hand_constructed_checked_stronger_tree')
    second_stages.append(proposal('stronger_raw_checked_anchors', second, costs2, bank2, evaluator2, engine2, 15))
    observed = oracle2.audit(0, 0)
    costs2.observe(observed)
    second_stages.append(proposal('after_actual_row_zero_coordinate_zero_audit', second, costs2, bank2, evaluator2, engine2, 15))
    second_record = dict(source=second, cost_manifest=second_source,
                         raw_initial_proof=weak_proof, raw_stronger_proof=dict(budget=1, proof=strong_proof),
                         initial_native_state=initial_state2, stages=second_stages,
                         final_native_state=engine2.state(), setup_invoice=engine2.setup_invoice,
                         setup_timing=engine2.setup_timing, operation_invoice=meter2.record(),
                         actual_audits=oracle2.calls, final_profiles=bank2.rows)
    # Persistence includes all retained rows/columns and explicit assignment
    # starts; it does not assert retained internal native branch trees.
    for record in (first_record, second_record):
        states = [record['initial_native_state']] + [s['proposal']['state_after'] for s in record['stages']]
        assert len({s['highs_object_id'] for s in states}) == 1
        assert len({s['native_row_count'] for s in states}) == 1
        assert len({s['native_column_count'] for s in states}) == 1

    # The actual calls have all finished before the finite enumeration.
    first_record['post_call_diagnostic'] = diagnostics(first, first_source, first_stages)
    second_record['post_call_diagnostic'] = diagnostics(second, second_source, second_stages)
    all_stages = first_stages + second_stages
    comparisons = [dict(source=i, stage=s['stage'], before=s['before']['bound'], after=s['after']['bound'],
                        new_bound_reduction=s['before']['bound'] - s['after']['bound'],
                        proposed_model=s['proposal']['model'], native_status=s['proposal'].get('native', {}).get('model_status'),
                        proposal_status=s['proposal']['status'], named_units=s['proposal']['invoice']['total'])
                   for i, record in enumerate((first_record, second_record)) for s in record['stages']]
    files = [Path(__file__), Path(robust.__file__), HERE / 'repair_interface.py',
             Path(native.__file__), Path(native.profile_kernel.__file__), Path(native.kernel.__file__),
             Path(robust.highspy.__file__), Path(robust.highspy._core.__file__)]
    result = dict(status='passed', evidence='DEVELOPMENT actual small constructed native proposals',
                  contributor='ChatGPT (GPT-6 Astra Pro)', created_utc=datetime.now(timezone.utc).isoformat(),
                  hashes={p.name: native.sha(p) for p in files}, highspy_version=engine.hs.version(),
                  API_basis='Installed HiGHS 1.11.0 method docstrings plus the already source-bound native_repair.py addCol/addRow/changeRowBounds/setSolution/run/getSolution interface; no unsupported persistence claim.',
                  sources=[first_record, second_record], comparisons=comparisons,
                  summary=dict(native_mip_calls=sum(s['proposal']['state_after']['calls'].get('native_mip_calls', 0)
                                                   for s in [first_stages[-1], second_stages[-1]]),
                               checked_witness_proposals=sum(s['proposal']['status'] == 'CHECKED_WITNESS' for s in all_stages),
                               unresolved_proposals=sum(s['proposal']['status'] == 'UNRESOLVED' for s in all_stages),
                               strict_post_proposal_bound_improvements=sum(c['new_bound_reduction'] > 0 for c in comparisons),
                               cost_observations=len(oracle2.calls), raw_negative_trees_checked=3,
                               separate_SAT_IHS_LP_or_proof_search_calls=0,
                               setup_units=engine.setup_invoice['total'] + engine2.setup_invoice['total'],
                               proposal_units=sum(s['proposal']['invoice']['total'] for s in all_stages),
                               total_common_operation_units=first_record['operation_invoice']['total'] + second_record['operation_invoice']['total'],
                               audit_provider_software_units=4 * len(oracle2.calls)),
                  timings=dict(native_process_ns=sum(s['proposal']['native_timing']['process_ns'] for s in all_stages),
                               native_wall_ns=sum(s['proposal']['native_timing']['wall_ns'] for s in all_stages),
                               whole_process_ns=time.process_time_ns() - cpu, whole_wall_ns=time.perf_counter_ns() - wall),
                  scope='An ordinary persistent robust-action comparator, available equally to later controllers. No acquisition on the 16-source historical workload and no strict superiority or native lower-certificate claim.',
                  prices=dict(external_cost_audit=None, native_search_operation_conversion=None, CPU_memory_monetary_conversion=None))
    output.write_text(json.dumps(jsonable(result), indent=2) + '\n')
    print(json.dumps(jsonable(dict(status=result['status'], summary=result['summary'], comparisons=comparisons))))


if __name__ == '__main__':
    run(Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / 'robust_witness_results.json')
