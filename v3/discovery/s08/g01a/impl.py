#!/usr/bin/env python3
"""G01 paid geometry/threshold DEVELOPMENT service, Codex (GPT-6), 2026-10-13.

New acquisitions only with an exclusive output directory. No historical file
is rewritten. Ordinary controls receive the same admitted geometry and proofs.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
from itertools import product
import copy
import hashlib
import json
from pathlib import Path
import platform
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 's06'))
import contract_guard
import contract_quote as complete

kernel = complete.source
profiles = complete.compilation
VERSION = 's08-g01-v1'


def encode(x):
    if isinstance(x, F):
        return x.numerator if x.denominator == 1 else str(x)
    raise TypeError(type(x).__name__)


def save(path, data):
    path.write_text(json.dumps(data, indent=2, default=encode) + '\n', encoding='utf-8')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def seal(data):
    data = dict(data)
    data['identity'] = kernel.digest(data)
    return data


def source(n):
    mandatory = list(range(4, n + 4))
    aux = list(range(n + 4, n + 7))
    hard = [[-1, 3], [1, -3], [-2, -3], [2, 3]]
    hard += [clause for y in mandatory for clause in ([3, y], [-3, y])]
    hard += [[aux[0], aux[1]], [aux[1], aux[2]], [aux[2], aux[0]]]
    features = [1, 2, *mandatory, *aux]
    witness = sum(1 << (v - 1) for v in [1, 3, *mandatory, *aux[:2]])
    original = seal(dict(row=f'g01-n{n}', variables=n + 6, hard=hard,
        soft=[dict(weight=4 if j < 2 else 1, clause=[-v]) for j, v in enumerate(features)],
        public_incumbent=witness, objective_max=11 + n))
    auxiliary = seal(dict(row='g01-aux-triangle', variables=3,
        hard=[[1, 2], [2, 3], [3, 1]],
        soft=[dict(weight=1, clause=[-v]) for v in (1, 2, 3)],
        public_incumbent=3, objective_max=3))
    # These are construction proposals, not trusted certificates.
    resolution = [dict(left=0, right=2, pivot=3), dict(left=1, right=3, pivot=3)]
    resolution += [dict(left=4 + 2*j, right=5 + 2*j, pivot=3) for j in range(n)]
    return dict(original=original, auxiliary=auxiliary,
                auxiliary_variables=aux, mandatory_variables=mandatory,
                resolution_proposal=resolution)


def admit_geometry(data, meter):
    original = data['original']
    if original['identity'] != kernel.digest({k: v for k, v in original.items() if k != 'identity'}):
        raise ValueError('Original source identity mismatch')
    n = len(data['mandatory_variables'])
    meter.pay('admission', 'original_source_words', 8 + sum(1 + len(c) for c in original['hard'])
              + sum(2 + len(s['clause']) for s in original['soft']))
    clauses = [set(c) for c in original['hard']]
    derived = []
    for proposal in data['resolution_proposal']:
        left, right, pivot = proposal['left'], proposal['right'], proposal['pivot']
        if type(pivot) is not int or pivot <= 0 or not (0 <= left < len(clauses) and 0 <= right < len(clauses)):
            raise ValueError('Malformed resolution proposal')
        a, b = clauses[left], clauses[right]
        if pivot in a and -pivot in b:
            resolvent = (a - {pivot}) | (b - {-pivot})
        elif -pivot in a and pivot in b:
            resolvent = (a - {-pivot}) | (b - {pivot})
        else:
            raise ValueError('Resolution pivot missing')
        if any(-v in resolvent for v in resolvent):
            raise ValueError('Tautological resolution cannot establish requested geometry')
        meter.pay('resolution_acquisition', 'emit_parent_indices_pivot_and_literals', 3 + len(a) + len(b))
        meter.pay('resolution_check', 'independent_exact_set_resolution', 6 + 2*(len(a) + len(b)))
        clauses.append(resolvent)
        derived.append(sorted(resolvent))
    expected = [[-2, -1], [1, 2]] + [[v] for v in data['mandatory_variables']]
    if derived != expected:
        raise ValueError('Resolution does not prove the specified geometry')
    expected_features = [1, 2, *data['mandatory_variables'], *data['auxiliary_variables']]
    if [s['clause'] for s in original['soft']] != [[-v] for v in expected_features]:
        raise ValueError('Ordered feature polarity mismatch')
    meter.pay('geometry_compile', 'bind_units_pair_and_ordered_violations', 16 + 4*len(expected_features))
    return seal(dict(original_source=original['identity'], n=n,
        pair=[0, 1], pair_sum=1, mandatory_features=list(range(2, n+2)),
        mandatory_value=1, raw_resolution=data['resolution_proposal'], derived=derived))


def admit_auxiliary(data, receipt, meter):
    auxiliary = data['auxiliary']
    original = data['original']
    variables = data['auxiliary_variables']
    if len(variables) != auxiliary['variables'] or len(set(variables)) != len(variables):
        raise ValueError('Invalid auxiliary variable map')
    def lift(clause):
        return [variables[abs(v)-1] * (1 if v > 0 else -1) for v in clause]
    hard = [set(c) for c in original['hard']]
    if any(set(lift(c)) not in hard for c in auxiliary['hard']):
        raise ValueError('Auxiliary constraints are not consequences supplied by source inclusion')
    mapped_soft = [lift(s['clause']) for s in auxiliary['soft']]
    if mapped_soft != [s['clause'] for s in original['soft'][-3:]]:
        raise ValueError('Auxiliary objective mapping mismatch')
    if any(s['weight'] != 1 for s in auxiliary['soft']):
        raise ValueError('This auxiliary lift admits unit weights only')
    if receipt['source_id'] != kernel.digest(auxiliary):
        raise ValueError('Proof receipt has another auxiliary source')
    if receipt['receipt_id'] != kernel.digest({k:v for k,v in receipt.items() if k != 'receipt_id'}):
        raise ValueError('Changed auxiliary receipt')
    response = receipt['provider_response']
    if response['status'] == 'UNSAT':
        kernel.check_negative(auxiliary, receipt['budget'], response['proof'], meter)
        lower = receipt['budget'] + 1
        witness = auxiliary['public_incumbent']
    elif response['status'] == 'SAT':
        witness = response['model']
        value = kernel.checked_objective(auxiliary, witness, meter)
        if value > receipt['budget']:
            raise ValueError('Positive receipt exceeds its budget')
        lower = None
    else:
        raise ValueError('Unresolved receipt does not improve the logical bank')
    checked = profiles.compile_witness(auxiliary, witness, meter)
    meter.pay('auxiliary_lift', 'clause_inclusion_ordered_map_and_binding', 24 + 3*sum(map(len, auxiliary['hard'])))
    return dict(lower=lower, upper=checked['original_cost'], witness=witness,
                source=original['identity'], raw_receipt=receipt['receipt_id'])


def combine(data, aux_model, bit, meter):
    model = 0
    # bit 0 chooses feature0 at zero cost; bit1 chooses feature1.
    for v in ([1, 3] if bit == 0 else [2]) + data['mandatory_variables']:
        model |= 1 << (v - 1)
    for j, v in enumerate(data['auxiliary_variables']):
        model |= ((aux_model >> j) & 1) << (v - 1)
    return profiles.compile_witness(data['original'], model, meter)


class Oracle:
    def __init__(self, contract, hidden):
        self.contract = contract
        self._hidden = tuple(hidden)
        self.bought = set()
        self.events = []

    def audit(self, coordinate):
        n = self.contract['n']
        if type(coordinate) is not int or not 0 <= coordinate <= n or coordinate in self.bought:
            raise ValueError('Invalid or repeated physical audit')
        self.bought.add(coordinate)
        value = self._hidden[coordinate] if coordinate < n else 4*self._hidden[n]
        receipt = seal(dict(cost_source=self.contract['identity'], coordinate=coordinate,
                            value=value, sequence=len(self.events), provider_software_units=4))
        self.events.append(receipt)
        return receipt


def observe(contract, known, receipt, meter):
    if receipt['cost_source'] != contract['identity'] or receipt['identity'] != kernel.digest({
            k:v for k,v in receipt.items() if k != 'identity'}):
        raise ValueError('Unbound cost observation')
    j = receipt['coordinate']
    if type(j) is not int or not 0 <= j <= contract['n'] or j in known:
        raise ValueError('Bad observation coordinate')
    if receipt['value'] not in ([1, 2] if j < contract['n'] else [0, 4]):
        raise ValueError('Observation outside declared support')
    known[j] = receipt['value']
    meter.pay('audit_check', 'source_receipt_support_and_state_update', 20)


def ceil(x):
    x = F(x)
    return -((-x.numerator)//x.denominator)


def floor(x):
    x = F(x)
    return x.numerator//x.denominator


def compile_candidate(n, lower, upper, price, tau, meter):
    # The gap guard is essential: a small replacement uncertainty does not
    # imply a warranted retained repair while the auxiliary optimum is open.
    meter.pay('policy_compile', 'thresholds_gap_and_complete_cap', 22)
    return dict(R=ceil(price-tau-lower-n), L=n-floor(price+tau-upper-n),
                gap=upper-lower, max_audits=n+1, residual_proof=upper-lower > tau)


def compile_ordinary(n, lower, upper, price, tau, meter):
    # Independent conventional derivation: required number of expensive
    # observations for replacement, cheap observations for retained repair.
    replace = F(price)-tau-lower-n
    repair = F(upper)+2*n-price-tau
    meter.pay('policy_compile', 'thresholds_gap_and_complete_cap', 22)
    return dict(high_needed=ceil(replace), low_needed=ceil(repair),
                gap=upper-lower, max_audits=n+1, residual_proof=upper-lower > tau)


def candidate_step(plan, n, highs, lows, lower, upper, price, tau, meter):
    meter.pay('policy_select', 'two_threshold_tests_gap_and_action', 9)
    if highs >= plan['R']:
        return 'replace'
    if lows >= plan['L']:
        return 'proof' if plan['gap'] > tau else 'repair'
    return 'audit' if highs+lows < n else 'proof'


def ordinary_step(plan, n, highs, lows, lower, upper, price, tau, meter):
    meter.pay('policy_select', 'two_threshold_tests_gap_and_action', 9)
    if highs >= plan['high_needed']:
        return 'replace'
    if lows >= plan['low_needed'] and upper-lower <= tau:
        return 'repair'
    if lows >= plan['low_needed'] or highs+lows == n:
        return 'proof'
    return 'audit'


def interval_step(plan, n, highs, lows, lower, upper, price, tau, meter):
    meter.pay('policy_select', 'direct_interval_arithmetic_gap_and_action', 15)
    lo, hi = n+highs, 2*n-lows
    if lower+lo >= price-tau:
        return 'replace'
    if upper+hi <= price+tau:
        return 'proof' if upper-lower > tau else 'repair'
    return 'audit' if highs+lows < n else 'proof'


def certify(data, geometry, bank, contract, known, kind, meter):
    n, price, tau = contract['n'], F(contract['price']), F(contract['tolerance'])
    if geometry['original_source'] != data['original']['identity'] or bank['source'] != geometry['original_source']:
        raise ValueError('Certificate mixes logical sources')
    highs = sum(v == 2 for j,v in known.items() if j < n)
    lows = sum(v == 1 for j,v in known.items() if j < n)
    lo, hi = n+highs, 2*n-lows
    lower, upper = bank['lower'], bank['upper']
    if kind == 'replace':
        bound = max(F(0), price-lower-lo)
        witness = None
    else:
        if n not in known:
            raise ValueError('Fixed repair needs the decision observation')
        witness = combine(data, bank['witness'], known[n]//4, meter)
        bound = max(F(0), upper-lower, upper+hi-price)
    meter.pay('output_certificate', 'source_geometry_logical_receipt_and_uniform_bound', 32)
    if bound > tau:
        raise ValueError('Attempted unwarranted output')
    return dict(kind=kind, bound=bound, witness=witness, source=geometry['original_source'],
        cost_source=contract['identity'], proof=bank['raw_receipt'],
        geometry=geometry['identity'], remaining_modes=1 << (n+1-len(known)),
        lower=lower, upper=upper, mandatory_interval=[lo,hi])


def execute_request(data, geometry, bank, contract, oracle, policy, output):
    meter = kernel.Meter()
    start_wall, start_cpu = time.perf_counter_ns(), time.process_time_ns()
    n, price, tau = contract['n'], F(contract['price']), F(contract['tolerance'])
    known, events = {}, []
    result = dict(contract=contract, policy=policy, initial_bank=copy.deepcopy(bank), events=events)
    def persist(status):
        result.update(status=status, local_invoice=meter.record(),
            timing=dict(wall_ns=time.perf_counter_ns()-start_wall, process_ns=time.process_time_ns()-start_cpu))
        save(output, result)
    def buy(j):
        result['pending'] = dict(kind='audit', coordinate=j)
        persist('before_actual_audit')
        raw = oracle.audit(j)
        events.append(dict(kind='audit', receipt=raw))
        persist('raw_audit_saved')
        observe(contract, known, raw, meter)
    try:
        meter.pay('request_admission', 'contract_public_support_price_tolerance', 16+n)
        plan = None
        if policy in ('quotient', 'ordinary_compiled'):
            compiler = compile_candidate if policy == 'quotient' else compile_ordinary
            plan = compiler(n,bank['lower'],bank['upper'],price,tau,meter)
        result['complete_quote'] = dict(maximum_mandatory_audits=n, maximum_decision_audits=1,
            maximum_additional_proof_calls=int(bank['upper']-bank['lower'] > tau),
            proof_outcomes=['SAT: checked cost1 witness', 'UNSAT: checked lower2'] if bank['upper']-bank['lower'] > tau else [],
            proof_named_cap=complete.finite_call_quote(data['auxiliary'])['complete_wrapper_units'] if bank['upper']-bank['lower'] > tau else 0,
            tariff='n*A + D + optional(P + complete proof named cap); source/local/check/host/storage additional')
        meter.pay('quote', 'complete_audit_and_proof_reserve', 12)
        persist('complete_route_quoted')
        if policy == 'full_identification':
            for j in range(n+1):
                buy(j)
        while True:
            highs = sum(v == 2 for j,v in known.items() if j<n)
            lows = sum(v == 1 for j,v in known.items() if j<n)
            stepper = {'quotient': candidate_step, 'ordinary_compiled':ordinary_step}.get(policy,interval_step)
            step = stepper(plan,n,highs,lows,bank['lower'],bank['upper'],price,tau,meter)
            if step == 'replace':
                answer = certify(data,geometry,bank,contract,known,'replace',meter)
                break
            if step == 'repair':
                if n not in known:
                    buy(n)
                answer = certify(data,geometry,bank,contract,known,'repair',meter)
                break
            if step == 'audit':
                buy(next(j for j in range(n) if j not in known))
                continue
            if bank['upper']-bank['lower'] != 1 or bank['lower'] != 1:
                raise ValueError('Residual-proof policy admits only the declared one-unit gap')
            result['pending'] = dict(kind='proof',budget=1)
            persist('before_actual_residual_proof')
            raw = complete.execute_complete(data['auxiliary'],1)
            events.append(dict(kind='proof',receipt=raw))
            persist('raw_residual_proof_saved')
            lifted = admit_auxiliary(data,raw,meter)
            if lifted['lower'] is None:
                lifted['lower'] = bank['lower']
            if lifted['lower'] != lifted['upper']:
                raise AssertionError('Both declared complete proof branches must close the gap')
            bank.update(lifted)
            if policy in ('quotient','ordinary_compiled'):
                compiler = compile_candidate if policy == 'quotient' else compile_ordinary
                plan = compiler(n,bank['lower'],bank['upper'],price,tau,meter)
        result.pop('pending',None)
        result['answer'] = answer
        result['known'] = known
        result['final_bank'] = copy.deepcopy(bank)
        proof_units = sum(e['receipt']['total_operation_units'] for e in events if e['kind']=='proof')
        counts = Counter(e['kind'] for e in events)
        result['invoice'] = dict(named_units=meter.total+4*counts['audit']+proof_units,
            local_units=meter.total,provider_software_units=4*counts['audit']+proof_units,
            mandatory_audits=sum(j<n for j in known),decision_audits=int(n in known),
            proof_calls=counts['proof'])
        persist('complete')
        return result
    except BaseException as exc:
        result['error'] = dict(type=type(exc).__name__,message=str(exc))
        persist('failed_or_interrupted_prefix')
        raise


def diagnostic(data, contract, result):
    """Exhaustive finite validation after the controller saved its output."""
    n, price = contract['n'], F(contract['price'])
    known = {int(j):v for j,v in result['known'].items()}
    feasible = []
    instance = data['original']
    for model in range(1 << instance['variables']):
        if all(any(((model>>(abs(v)-1))&1)==int(v>0) for v in c) for c in instance['hard']):
            mask = sum((not any(((model>>(abs(v)-1))&1)==int(v>0) for v in s['clause'])) << j
                       for j,s in enumerate(instance['soft']))
            feasible.append(mask)
    worst = F(0)
    compatible = 0
    for costs in product((1,2),repeat=n):
        for bit in (0,1):
            if any((costs[j] if j<n else 4*bit)!=v for j,v in known.items()):
                continue
            compatible += 1
            w = ([0,4] if bit==0 else [4,0]) + list(costs) + [1,1,1]
            def value(mask):
                return sum(v for j,v in enumerate(w) if mask & (1<<j))
            optimum = min(price,min(map(value,feasible)))
            chosen = price if result['answer']['kind']=='replace' else value(result['answer']['witness']['violation_mask'])
            worst = max(worst,chosen-optimum)
    if worst > F(result['answer']['bound']) or compatible != result['answer']['remaining_modes']:
        raise AssertionError('Uniform output fails exhaustive diagnostic')
    return dict(worst_regret=worst, compatible_costs=compatible, feasible_models=len(feasible),
                source='post-output enumeration; not supplied to any controller')


def run(directory):
    directory.mkdir(exist_ok=False)
    (directory/'impl.py').write_bytes(Path(__file__).read_bytes())
    sources = [source(n) for n in (0,2,4)]
    code_paths = [Path(__file__),Path(complete.__file__),Path(kernel.__file__),Path(profiles.__file__)]
    design = dict(version=VERSION,contributor='Codex (GPT-6)',stage='DEVELOPMENT',
        created_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),
        code={str(p.relative_to(HERE.parents[2])):sha(p) for p in code_paths},
        declaration_sha256=sha(HERE/'g01_design.md'),sources=sources,
        n_values=[0,2,4],tolerances=[0,1],price_recipe=['2+n-1','2+3*n/2','2+2*n+1'],
        policies=['quotient','ordinary_compiled','ordinary_interval','full_identification'],
        logical_banks=['exact','gap1'],hidden_schedule='lexicographic exhaustive independent binary supports; new audit source per request',
        setup_accounting='Actual physical geometry/proofs acquired once per n and starting bank; each matched arm is billed the same setup allocation. No duplicate physical acquisition count.')
    save(directory/'design.json',design)
    admission = contract_guard.admit()
    summary = dict(version=VERSION,status='acquiring',setup=[],arms=[],diagnostics=[],code_admission=admission)
    save(directory/'results.json',summary)
    for data in sources:
        n = len(data['mandatory_variables'])
        meter = kernel.Meter()
        geometry = admit_geometry(data,meter)
        save(directory/f'g{n}.json',dict(geometry=geometry,invoice=meter.record()))
        for initial in ('exact','gap1'):
            budget = 1 if initial=='exact' else 0
            save(directory/f'p{n}{initial}_intent.json',dict(source=data['auxiliary'],budget=budget))
            raw = complete.execute_complete(data['auxiliary'],budget)
            save(directory/f'p{n}{initial}.json',raw)
            bank_meter = kernel.Meter()
            bank = admit_auxiliary(data,raw,bank_meter)
            for bit in (0,1):
                combine(data,bank['witness'],bit,bank_meter)
            setup = dict(n=n,initial=initial,geometry_units=meter.total,proof_units=raw['total_operation_units'],
                lift_witness_units=bank_meter.total,code_admission_units=admission['declared_admission_units'])
            setup['named_units'] = sum(setup[k] for k in ('geometry_units','proof_units','lift_witness_units','code_admission_units'))
            summary['setup'].append(setup)
            prices = sorted({F(1+n),F(2)+F(3*n,2),F(3+2*n)})
            for policy in design['policies']:
                arm_bank = copy.deepcopy(bank)
                totals = Counter()
                request_number = 0
                trace_digest = []
                for price in prices:
                    for tau in (0,1):
                        for hidden in product((1,2),repeat=n):
                            for bit in (0,1):
                                request_id=f'n{n}-{initial}-{policy}-{request_number}'
                                contract = seal(dict(request=request_id,n=n,price=str(price),tolerance=tau,
                                    supports='mandatory1or2; decision0or4; auxiliary1fixed',original_source=data['original']['identity']))
                                oracle = Oracle(contract,(*hidden,bit))
                                stem=f'{n}{initial[0]}{policy[:2]}{request_number:03d}'
                                # ordinary names share first two letters: use unambiguous code.
                                stem=f'{n}{initial[0]}{design["policies"].index(policy)}{request_number:03d}'
                                save(directory/f'{stem}h.json',dict(contract=contract,hidden=[*hidden,bit]))
                                result=execute_request(data,geometry,arm_bank,contract,oracle,policy,directory/f'{stem}.json')
                                diag=diagnostic(data,contract,result)
                                totals.update(result['invoice'])
                                totals['outputs']+=1
                                totals['remaining_modes']+=result['answer']['remaining_modes']
                                trace_digest.append(dict(kind=result['answer']['kind'],bound=str(result['answer']['bound']),
                                    acquisitions=[(e['kind'],e['receipt'].get('coordinate'),e['receipt'].get('value')) for e in result['events']]))
                                summary['diagnostics'].append(dict(file=f'{stem}.json',**diag))
                                request_number+=1
                summary['arms'].append(dict(n=n,initial=initial,policy=policy,totals=dict(totals),
                    setup_named_units=setup['named_units'],full_horizon_named_units=setup['named_units']+totals['named_units'],
                    action_purchase_digest=kernel.digest(trace_digest)))
                save(directory/'results.json',summary)
    summary['status']='complete'
    summary['completed_utc']=datetime.now(timezone.utc).isoformat()
    summary['physical_initial_proof_calls']=6
    summary['physical_resolution_steps']=sum(n+2 for n in (0,2,4))
    summary['evidence_bytes']=sum(p.stat().st_size for p in directory.glob('*.json'))
    save(directory/'results.json',summary)
    print(json.dumps({k:v for k,v in summary.items() if k in ('status','arms','physical_initial_proof_calls','physical_resolution_steps','evidence_bytes')},default=encode))


if __name__=='__main__':
    run(Path(sys.argv[1]))
