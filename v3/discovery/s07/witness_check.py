#!/usr/bin/env python3
"""Receipt-only reconstruction of the expanded robust-witness schedules.

DEVELOPMENT. ChatGPT (GPT-6 Astra Pro), 2026-10-12. No native search or
acquisition API is invoked. Original raw proofs and positive models are checked;
the fixed schedule and named meter are reconstructed with saved responses.
Exact feasible-mask enumeration is diagnostic only and unavailable to policies.
"""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
import copy
import json
from pathlib import Path
import sys
import time

import trace_check as trace
import bundle_service as shared

HERE = Path(__file__).resolve().parent
native = trace.native
same = trace.same


def normalized(value):
    return json.loads(json.dumps(value, default=trace.encode))


def mark(meter):
    return meter.total, Counter(meter.operations)


def delta(meter, before):
    difference = meter.operations - before[1]
    categories = Counter()
    for (category, operation), units in difference.items():
        categories[category] += units
    return dict(total=meter.total-before[0], by_category=dict(categories),
                operations=[dict(category=c, operation=o, units=u)
                            for (c, o), u in sorted(difference.items())])


def timing(value):
    if not all(type(value[k]) is int and value[k] >= 0 for k in ('process_ns', 'wall_ns')):
        raise AssertionError('Malformed recorded timing; measured values are not rerun')


def scalar_bound(mask, possible, modes, lowers, price, diagnostic):
    """Independent exact objective of the robust witness epigraph MIP."""
    mode_cost = [sum(w for j, w in enumerate(mode) if mask & (1 << j)) for mode in modes]
    n = len(possible)
    gap = sum(max(F(mode_cost[k])-lowers[k]/n for k in row) for row in possible)
    upper = sum(max(mode_cost[k] for k in row) for row in possible)
    diagnostic.pay('diagnostic', 'exact_scalar_objective',
                   2*len(modes)*len(modes[0])+5*sum(map(len, possible))+2*n+4)
    return max(F(0), gap, upper-price)


class RecordedEngine:
    """Independently count frozen API tariffs, without constructing HiGHS."""
    def __init__(self, instance, costs, meter, setup):
        before = mark(meter)
        self.instance, self.costs, self.meter = instance, costs, meter
        self.n, self.m, self.N, self.K = instance['variables'], len(instance['soft']), costs.n, len(costs.modes)
        clauses = instance['hard']+[s['clause'] for s in instance['soft']]
        self.columns = self.n+self.m+2*self.N+1
        self.rows = len(instance['hard'])+sum(1+len(s['clause']) for s in instance['soft'])+2*self.N*self.K+2
        self.pay_modes()
        meter.pay('robust_admission', 'logical_source_and_clause_words', 8+self.m+sum(1+len(c) for c in clauses))
        incumbent = native.profile_kernel.compile_witness(instance, instance['public_incumbent'], meter)
        meter.pay('robust_setup', 'native_option_dispatch', 10)
        meter.pay('robust_setup', 'native_column_and_integrality', 8*(self.n+self.m)+6*(2*self.N+1))
        meter.pay('robust_encoding', 'clause_literal_linear_truth', 4*sum(map(len, clauses)))

        def nonzero(clause):
            coefficient = Counter()
            for literal in clause:
                coefficient[abs(literal)] += 1 if literal > 0 else -1
            return sum(value != 0 for value in coefficient.values())

        words = sum(2*nonzero(c)+6 for c in instance['hard'])
        words += sum(2*(nonzero(s['clause'])+1)+6+10*len(s['clause']) for s in instance['soft'])
        words += 2*self.N*sum(2*(sum(w != 0 for w in mode)+1)+6 for mode in costs.modes)
        words += 2*(2*(self.N+1)+6)
        meter.pay('robust_encoding', 'native_linear_row_and_coefficient_words', words)
        same(delta(meter, before), setup['invoice'], 'independently reconstructed native setup invoice')
        timing(setup['timing'])
        self.current = copy.deepcopy(setup['state'])
        expected = dict(structural_source_id=native.structural_id(instance), cost_source_id=costs.source_id,
                        native_row_count=self.rows, native_column_count=self.columns,
                        last_checked_model=incumbent['model'], last_checked_mask=incumbent['violation_mask'], calls={})
        for key, value in expected.items():
            same(self.current[key], value, 'persistent initial '+key)
        if not self.current['state_id'].startswith('robust-') or type(self.current['highs_object_id']) is not int:
            raise AssertionError('Missing persistent native identity')
        self.bounds = {'price': F(0)}

    def pay_modes(self):
        self.meter.pay('robust_admission', 'public_mode_and_possible_source_words',
                       self.K*self.m+sum(map(len, self.costs.possible))+self.N+8)

    def response(self, saved, lowers, price, feasible, diagnostic):
        before = mark(self.meter)
        same(saved['version'], 's07-persistent-robust-witness-v1', 'native representation version')
        for key, expected in [('source_identity', self.instance['identity']),
                              ('structural_source_id', native.structural_id(self.instance)),
                              ('cost_source_id', self.costs.source_id),
                              ('possible_modes', [list(p) for p in self.costs.possible]),
                              ('anchor_lowers', normalized(lowers)), ('price', price),
                              ('caps', dict(seconds=.1, nodes=1000)),
                              ('checked_lower_receipt', None), ('independently_checked_lower', False),
                              ('native_lower_is_guidance_only', True), ('state_before', self.current)]:
            same(saved[key], expected, 'native actual source/state '+key)
        # The particular saved execution contains only this successful path.
        # A numerical status is never used to admit a lower or skip a model check.
        same(saved['status'], 'CHECKED_WITNESS', 'recorded positive witness path')
        self.pay_modes()
        self.meter.pay('robust_admission', 'anchor_price_and_cap_words', 2*self.K+8)
        changed = 0
        for i, choices in enumerate(self.costs.possible):
            self.meter.pay('robust_update', 'active_mode_set', len(choices)+1)
            for k in range(self.K):
                for kind, value in [('contrast', -lowers[k]/self.N), ('upper', F(0))]:
                    value = value if k in choices else None  # disabled: native -infinity
                    key = (i, k, kind)
                    changed += key not in self.bounds or self.bounds[key] != value
                    self.bounds[key] = value
        changed += self.bounds['price'] != -price
        self.bounds['price'] = -price
        same(saved['changed_native_row_bounds'], changed, 'only actual changed native row bounds')
        self.meter.pay('robust_update', 'row_bound_lookup_and_comparison', 2*(2*self.N*self.K+1))
        self.meter.pay('robust_update', 'native_row_bound_change_and_storage', 5*changed)
        self.meter.pay('robust_update', 'native_time_and_node_caps', 4)
        self.meter.pay('robust_start', 'exact_row_epigraph_values', 3*sum(map(len, self.costs.possible))+4*self.N)
        self.meter.pay('robust_start', 'checked_assignment_and_full_mip_start',
                       self.n+self.m+2*self.K*self.m+self.columns+2*self.N+8)
        self.meter.pay('robust_dispatch', 'native_mip_run')
        self.meter.pay('robust_result', 'native_status_and_primal_values', self.columns+12)
        self.meter.pay('robust_result', 'native_binary_primal_admission', 3*(self.n+self.m))
        checked = native.profile_kernel.compile_witness(self.instance, saved['model'], self.meter)
        checked['receipt_id'] = native.kernel.digest(dict(source=self.instance['identity'], model=checked['model'],
                                                         violation_mask=checked['violation_mask']))
        same(checked, saved['witness'], 'original hard clauses, exact soft mask and positive receipt')
        same(saved['repeats_previous_model'], saved['model'] == self.current['last_checked_model'], 'warm model repetition')
        self.current['last_checked_model'], self.current['last_checked_mask'] = checked['model'], checked['violation_mask']
        for name in ('proposals', 'explicit_mip_starts', 'native_mip_calls', 'checked_witnesses'):
            self.current['calls'][name] = self.current['calls'].get(name, 0)+1
        same(saved['state_after'], self.current, 'persistent state after checked proposal')
        self.meter.pay('robust_retention', 'checked_proposal_and_warm_assignment', self.n+self.m+8)
        self.meter.pay('robust_output', 'source_caps_witness_and_invoice_fields', 28)
        same(delta(self.meter, before), saved['invoice'], 'independently reconstructed proposal invoice')
        for field in ('timing', 'native_timing'):
            timing(saved[field])
        same(saved['native']['timing'], saved['native_timing'], 'native timing fields')
        same(saved['native']['value_valid'], True, 'recorded primal admission path')
        if not 0 <= saved['native']['nodes'] <= saved['caps']['nodes']:
            raise AssertionError('Reported native node cap exceeded')
        proposed = scalar_bound(checked['violation_mask'], self.costs.possible, self.costs.modes, lowers, price, diagnostic)
        optimum = min(scalar_bound(mask, self.costs.possible, self.costs.modes, lowers, price, diagnostic) for mask in feasible)
        # These are newly computed finite diagnostics; hints confer no authority.
        return dict(proposed_scalar_bound=proposed, exact_scalar_optimum=optimum,
                    scalar_optimum_gap=proposed-optimum, native_objective_hint=saved['native']['objective_hint'],
                    native_status=saved['native']['model_status'], checked_model=checked['model'])


def check_arm(arm, data, instances, initial, feasible, diagnostic):
    meter = native.kernel.Meter()
    initialization = []
    before = mark(meter)
    costs = trace.compiled.CompiledCosts(data['possible_cost_modes'], data['cohort_size'], data['source_identity'], meter)
    initialization.append(dict(part='cost_state', invoice=delta(meter, before)))
    before = mark(meter)
    bank = trace.stream.CompactBank(initial, meter)
    initialization.append(dict(part='projected_bank', invoice=delta(meter, before)))
    before = mark(meter)
    evaluator = trace.RepairEvaluator(instances, bank, costs, meter)
    initialization.append(dict(part='repair_evaluator', invoice=delta(meter, before)))
    initial_total = meter.total
    engines, queried = {}, set()
    cursor, wrapper, audits = 0, 0, 0
    requests, proposals = [], []
    native_setup_units = native_proposal_units = 0

    def event(kind, index, row=None):
        nonlocal cursor
        if cursor >= len(arm['events']):
            raise AssertionError('Schedule requires an unrecorded purchase')
        got = arm['events'][cursor]
        same((got['kind'], got['request']), (kind, index), 'prospective purchase ordering')
        if row is not None:
            same(got['row'], row, 'logical purchase row')
        cursor += 1
        return got, cursor-1

    def answer(actual, stored, row, price, label):
        same(normalized(actual), stored, label+' complete reconstructed evaluator output and invoice')
        exact = trace.semantic_regret(actual['mask'], F(price), feasible[row], costs, diagnostic)
        if exact > actual['bound']:
            raise AssertionError('Output gate is below independently enumerated finite-source regret')
        return dict(bound=actual['bound'], exact_finite_regret=exact, slack=actual['bound']-exact)

    for index, (duty, stored) in enumerate(zip(data['schedule'], arm['requests'], strict=True)):
        row, price, tau = duty['row'], duty['price'], duty['tolerance']
        same((stored['request'], stored['row'], stored['price'], stored['tolerance']), (index, row, price, tau), 'fixed request duty')
        request_mark, first = mark(meter), cursor
        initial_answer = evaluator.evaluate(row, price, tau)
        initial_check = answer(initial_answer, stored['before'], row, price, 'request before')
        current = initial_answer
        for step in range(data['limits']['max_actions_per_request']):
            if current['bound'] <= tau:
                break
            action = trace.compiled.fixed_audit(costs)
            if arm['policy'] == 'witness_before_audit' or action is None:
                lowers = evaluator.mode_anchor_lowers(row)
                key = (row, price, tuple(tuple(p) for p in costs.possible), tuple(lowers))
                meter.pay('controller', 'actual_evidence_state_proposal_lookup', 8+sum(map(len, costs.possible))+len(lowers))
                if key not in queried:
                    queried.add(key)
                    purchase, purchase_index = event('robust_witness', index, row)
                    if row not in engines:
                        if purchase['setup'] is None:
                            raise AssertionError('Native engine initialization missing')
                        engines[row] = RecordedEngine(instances[row], costs, meter, purchase['setup'])
                        native_setup_units += purchase['setup']['invoice']['total']
                    else:
                        same(purchase['setup'], None, 'persistent engine reused without new setup')
                    prior = evaluator.evaluate(row, price, tau)
                    answer(prior, purchase['before'], row, price, 'proposal before')
                    proposal = engines[row].response(purchase['response'], lowers, price, feasible[row], diagnostic)
                    native_proposal_units += purchase['response']['invoice']['total']
                    bank.retain(row, purchase['response'], purchase_index)
                    after = evaluator.evaluate(row, price, tau)
                    answer(after, purchase['after'], row, price, 'proposal after')
                    same(purchase['strict_bound_improvement'], after['bound'] < prior['bound'], 'actual proposal improvement')
                    meter.pay('output', 'native_proposal_and_checked_gate_record', 28)
                    proposals.append(proposal | dict(event=purchase_index, request=index, row=row,
                        before=prior['bound'], after=after['bound'], closes=prior['bound']>tau and after['bound']<=tau))
                current = evaluator.evaluate(row, price, tau)
                if current['bound'] <= tau:
                    break
            if action is not None:
                purchase, purchase_index = event('audit', index)
                receipt = purchase['receipt']
                same((receipt['row'], receipt['coordinate']), (action['row'], action['coordinate']), 'actual first informative audit')
                same(receipt['provider_call'], audits, 'actual physical audit chronology')
                same(receipt['provider_software_units'], 4, 'audit provider named tariff')
                same(receipt['value'], data['possible_cost_modes'][data['hidden_modes'][receipt['row']]][receipt['coordinate']], 'committed audit truth, verifier only')
                costs.observe(receipt)
                audits += 1
                meter.pay('output', 'cost_audit_record', 16)
                same(costs.snapshot(), purchase['cost_state'], 'post-audit source state')
            else:
                if any(len(p) != 1 for p in costs.possible):
                    raise AssertionError('Complete fallback before singleton cost state')
                q = [sum(costs.modes[p[0]][j] for p in costs.possible) for j in range(costs.m)]
                bank.set_weights(q)
                interval = bank.bounds(row)
                budget = min(interval['upper'], price)-tau-1
                purchase, purchase_index = event('complete', index, row)
                same((purchase['weights'], purchase['budget']), (q, budget), 'singleton closing query')
                retained, status = trace.check_complete(purchase, instances[row], diagnostic)
                bank.retain(row, retained, purchase_index)
                wrapper += purchase['response']['total_operation_units']
                meter.pay('output', 'complete_fallback_receipt_record', 20)
            if audits > data['limits']['max_observations'] or cursor-audits > data['limits']['max_logical_purchases']:
                raise AssertionError('Recorded acquisition cap exceeded')
            current = evaluator.evaluate(row, price, tau)
        meter.pay('output', 'final_checked_action_source_invoice', 28)
        final_check = answer(current, stored['answer'], row, price, 'request final')
        same(stored['status'], 'checked_action' if current['bound'] <= tau else 'unresolved', 'actual action gate')
        same(stored['closed_from_cache'], initial_answer['bound'] <= tau, 'cache closure')
        same(stored['event_indices'], list(range(first, cursor)), 'contiguous chronological request events')
        same(stored['cost_state'], costs.snapshot(), 'request output source state')
        requests.append(dict(request=index, row=row, before=initial_check, after=final_check,
                             local_meter_before=request_mark[0], local_meter_after=meter.total,
                             local_invoice=delta(meter, request_mark)))
    same(cursor, len(arm['events']), 'all recorded events consumed in schedule order')
    same(bank.rows, arm['final_profiles'], 'retained profiles built only from checked receipts')
    same(costs.snapshot(), arm['final_cost_state'], 'final source state')
    same({str(row):engine.current for row, engine in engines.items()}, arm['native_final_states'], 'persistent final native identities and counters')
    same(meter.record(), arm['invoice']['breakdown'], 'entire local named operation meter')
    same(meter.total, arm['invoice']['controller_and_interface_units'], 'local named invoice')
    same(wrapper, arm['invoice']['complete_wrapper_units'], 'actual complete wrapper sum')
    same(4*audits, arm['invoice']['audit_provider_software_units'], 'physical audit tariff sum')
    same(meter.total+wrapper+4*audits, arm['invoice']['operation_units'], 'total named arm invoice')
    same(costs.storage(), arm['storage']['cost_support'], 'cost support storage and cache counters')
    same(len(shared.canonical(bank.rows)), arm['storage']['profile_bytes'], 'retained profile bytes')
    same(len(shared.canonical(arm['events'])), arm['storage']['events_bytes'], 'saved event bytes')
    counts = Counter(e['kind'] for e in arm['events'])
    summary = dict(requests=len(requests), checked=sum(r['status']=='checked_action' for r in arm['requests']),
        cache_hits=sum(r['closed_from_cache'] for r in arm['requests']), cost_observations=audits,
        complete_calls=counts['complete'], robust_witness_calls=counts['robust_witness'],
        logical_purchases=counts['complete']+counts['robust_witness'],
        witness_calls_with_strict_bound_improvement=sum(p['after']<p['before'] for p in proposals),
        native_unresolved=0, unresolved=sum(r['status']=='unresolved' for r in arm['requests']),
        largest_final_bound=max(F(r['answer']['bound']) for r in arm['requests']))
    same(normalized(summary), arm['summary'], 'all reported summary metrics')
    return dict(policy=arm['policy'], summary=summary, initialization=initialization,
                local_initialization_units=initial_total, local_subsequent_units=meter.total-initial_total,
                native_setup_units=native_setup_units, native_proposal_units=native_proposal_units,
                reconstructed_invoice=meter.record(), proposal_caused_request_closures=sum(p['closes'] for p in proposals),
                finite_scalar_optimal_proposals=sum(p['scalar_optimum_gap']==0 for p in proposals),
                proposals=proposals, requests=requests)


def run(output, path):
    if output.exists():
        raise FileExistsError('Preserve independent checker attempts')
    cpu, wall = time.process_time_ns(), time.perf_counter_ns()
    result = dict(status='checking', evidence='DEVELOPMENT independent reconstruction; no new acquisitions',
                  contributor='ChatGPT (GPT-6 Astra Pro)', created_utc=datetime.now(timezone.utc).isoformat(),
                  checker_sha256=trace.sha(__file__), result_sha256=trace.sha(path), arms=[], actual_new_acquisition_calls=0)
    try:
        saved = json.loads(path.read_text())
        data = json.loads((HERE.parent/'s06'/'joint_source.json').read_text())
        same(saved['status'], 'complete', 'saved execution completed')
        same(saved['implementation_sha256'], trace.sha(HERE/'witness_service.py'), 'executed controller bytes')
        same(saved['source_sha256'], trace.sha(HERE.parent/'s06'/'joint_source.json'), 'fixed source bytes')
        same(saved['source_identity'], data['source_identity'], 'fixed source identity')
        same(data['source_identity'], native.kernel.digest({k:v for k,v in data.items() if k!='source_identity'}), 'committed cost source identity')
        dependency_paths = {name: HERE/name for name in saved['dependencies']}
        dependency_paths['native_stream.py'] = HERE.parent/'s06'/'native_stream.py'
        for name, expected in saved['dependencies'].items():
            same(trace.sha(dependency_paths[name]), expected, 'executed dependency '+name)
        archive, initial, admission = trace.stream.admit_existing_cache()
        same({k:v for k,v in admission.items() if k!='timing'}, {k:v for k,v in saved['initial_admission'].items() if k!='timing'}, 'raw initial source/proof admission and all tariffs')
        code = shared.contract_guard.admit()
        same({k:v for k,v in code.items() if k!='timing'}, {k:v for k,v in saved['code_admission'].items() if k!='timing'}, 'complete code admission')
        same(saved['common_current_units'], admission['total_declared_units']+code['declared_admission_units'], 'common current admission sum')
        diagnostic = native.kernel.Meter()
        feasible = [trace.finite_masks(instance, diagnostic) for instance in archive['instances']]
        same(saved['policies'], ['witness_before_audit', 'audit_before_witness'], 'matched expanded-menu policies')
        same([a['policy'] for a in saved['arms']], saved['policies'], 'all saved matched arms')
        for arm in saved['arms']:
            result['arms'].append(check_arm(arm, data, archive['instances'], initial, feasible, diagnostic))
        result.update(status='passed', initial_raw_admission=admission, code_admission=code,
            common_current_units=saved['common_current_units'], historical_acquisition_units=saved['historical_acquisition_units'],
            feasible_mask_counts=list(map(len, feasible)), diagnostic_invoice=diagnostic.record(),
            executed_bindings=dict(controller=saved['implementation_sha256'], dependencies=saved['dependencies']),
            checker_dependencies={str(p.relative_to(HERE.parent.parent.parent)): trace.sha(p) for p in
                [HERE/'trace_check.py', HERE.parent/'s06'/'joint_repair_v2.py', HERE.parent/'s06'/'joint_repair.py',
                 HERE.parent/'s06'/'native_repair.py', HERE.parent/'s06'/'contract_quote.py']},
            scope='No HiGHS model, solver run, complete provider solve, or cost-oracle audit is invoked. Source enumeration and saved hidden outcomes occur only in the diagnostic checker. Numerical native statuses/bounds and timing are recorded observations, not newly verified native execution or lower certificates. Full native primal column arrays were not retained; every exported original-source model and exact violation mask is checked afresh.')
    except BaseException as exc:
        result.update(status='failed', error=dict(type=type(exc).__name__, message=str(exc)))
        raise
    finally:
        result['timing'] = dict(process_ns=time.process_time_ns()-cpu, wall_ns=time.perf_counter_ns()-wall)
        output.write_text(json.dumps(result, indent=2, default=trace.encode)+'\n')
    print(json.dumps(dict(status=result['status'], arms=len(result['arms']), checked_outputs=sum(a['summary']['checked'] for a in result['arms']), actual_new_acquisition_calls=0)))


if __name__ == '__main__':
    run(Path(sys.argv[1]), Path(sys.argv[2]) if len(sys.argv)>2 else HERE/'witness_service_results.json')
