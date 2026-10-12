#!/usr/bin/env python3
"""S30: checked repair from a common CDF source and partial paid audits.

DEVELOPMENT. ChatGPT (GPT-6 Astra Pro), 2026-10-12. A new constructed
source, not F01 confirmation or an economic win over direct contrast audits.
Every draw is fixed before inspection. Repeated identities share observations
but retain their statistical multiplicity. Controllers never see hidden H.
"""
from __future__ import annotations
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
import copy
import json
import math
from pathlib import Path
import random
import sys
import time

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'s05'))
sys.path.insert(0,str(HERE.parent/'s06'))
import cdf_sweep
import contract_guard
import contract_quote
import joint_repair as joint
import native_repair as native

VERSION='s07-common-cdf-repair-v2'


def encode(v):
    if isinstance(v,F):
        return v.numerator if v.denominator==1 else str(v)
    raise TypeError(type(v).__name__)


def canonical(v):
    return json.dumps(v,sort_keys=True,separators=(',',':'),default=encode).encode()


def prepare():
    rng=random.Random(261012730)
    population=[rng.randrange(4) for _ in range(64)]
    draws=[rng.randrange(len(population)) for _ in range(128)]
    instance=dict(row='s30-two-repair-common-law',variables=2,hard=[[1,2]],
        soft=[dict(weight=1,clause=[-1]),dict(weight=1,clause=[-2])],
        public_incumbent=3,objective_max=2)
    instance['identity']=native.kernel.digest(instance)
    source=dict(version=VERSION,hidden_population=population,draws=draws,
        population_size=len(population),support_max=3,
        modes=[[0,4],[0,4],[4,0],[4,0]],sample_size=128,
        radius='1/8',failure_probability='1/20',seed=261012730,
        law='Draw all 128 identities iid uniformly with replacement from the fixed 64-row source before any inspections. No source probabilities or H values are supplied to controllers.',
        price=6,tolerance=2,initial_checked_models=[1,2],logical_source=instance,
        policies=['relevant_cut','full_latent','direct_contrast'],
        policy_contract='Fixed first-appearance row order. relevant_cut/direct_contrast inspect cut1 only; full_latent completes ordinary binary identification of each inspected H before reevaluating the gate. Each arm buys its own common q=(1,1),b=0 proof.')
    source['source_identity']=native.kernel.digest(source)
    return source


class CutOracle:
    def __init__(self,data):
        if native.kernel.digest({k:v for k,v in data.items() if k!='source_identity'})!=data['source_identity']:
            raise ValueError('Cost source changed')
        self.hidden=data['hidden_population']
        self.source_id=data['source_identity']
        self.calls=[]

    def audit(self,row,cut):
        cpu,wall=time.process_time_ns(),time.perf_counter_ns()
        receipt=dict(source_id=self.source_id,row=row,cut=cut,
            at_or_below=self.hidden[row]<=cut,provider_call=len(self.calls),
            observed_utc=datetime.now(timezone.utc).isoformat(),provider_software_units=4,
            timing=dict(process_ns=time.process_time_ns()-cpu,wall_ns=time.perf_counter_ns()-wall))
        receipt['receipt_id']=native.kernel.digest(receipt)
        self.calls.append(receipt)
        return receipt


class PopulationCosts:
    """Exact support of mean costs over a warranted finite CDF probability box."""
    def __init__(self,public,meter):
        self.modes=tuple(tuple(v) for v in public['modes'])
        self.m=len(self.modes[0]); self.n=public['sample_size']
        self.source_id=public['source_identity']; self.meter=meter
        self.radius=F(public['radius']); self.delta=F(public['failure_probability'])
        self.draws=tuple(public['draws']); self.multiplicity=Counter(self.draws)
        self.intervals={row:[0,public['support_max']] for row in self.draws}
        self.receipts=[]; self.support_cache={}; self.support_records=[]
        if self.n!=len(self.draws) or self.n!=128 or self.radius!=F(1,8) or self.delta!=F(1,20):
            raise ValueError('This construction uses its fixed n=128 outward radius1/8 contract')
        # 2*n*radius^2=4, and exp(4) exceeds this exact positive partial sum.
        partial=sum(F(4**k,math.factorial(k)) for k in range(6))
        if 2/partial>self.delta:
            raise ValueError('Outward DKW radius fails exact conservative tail check')
        self.tail_upper=2/partial
        meter.pay('population_admission','fixed_draws_mode_source_and_radius_words',
                  3*self.n+len(self.modes)*self.m+len(self.intervals)*4+32)
        self._rebuild()

    def _rebuild(self):
        size=len(self.modes)
        lower=[max(F(0),F(sum(self.multiplicity[i]*(u<=j) for i,(l,u) in self.intervals.items()),self.n)-self.radius)
               for j in range(size-1)]
        upper=[min(F(1),F(sum(self.multiplicity[i]*(l<=j) for i,(l,u) in self.intervals.items()),self.n)+self.radius)
               for j in range(size-1)]
        self.sweep=cdf_sweep.CDFSweep(lower,upper)
        self.band_id=(tuple(lower),tuple(upper))
        self.meter.pay('population_update','weighted_partial_cdf_envelopes_and_quantile_windows',
                       6*len(self.intervals)*(size-1)+12*size+8*len(self.sweep.windows))

    def observe(self,receipt):
        if receipt['source_id']!=self.source_id or native.kernel.digest({k:v for k,v in receipt.items() if k!='receipt_id'})!=receipt['receipt_id']:
            raise ValueError('Wrong cost source or modified audit')
        row,cut=receipt['row'],receipt['cut']
        if row not in self.intervals or type(cut) is not int:
            raise ValueError('Audit outside the fixed sampled source')
        l,u=self.intervals[row]
        if not l<=cut<u or type(receipt['at_or_below']) is not bool:
            raise ValueError('Noninformative or malformed audit')
        self.intervals[row]=[l,cut] if receipt['at_or_below'] else [cut+1,u]
        self.receipts.append(receipt['receipt_id'])
        self.meter.pay('population_observation','source_receipt_interval_and_occurrence_binding',18+self.multiplicity[row])
        self._rebuild()

    def support(self,coefficient):
        coefficient=tuple(coefficient)
        key=(self.band_id,coefficient)
        self.meter.pay('population_lookup','band_and_contrast_key',2*len(self.modes)+self.m+3)
        if key in self.support_cache:
            return self.support_cache[key]
        g=tuple(sum(a*b for a,b in zip(coefficient,mode)) for mode in self.modes)
        neg=tuple(-v for v in g)
        answer=self.sweep.minimum(neg)
        if not cdf_sweep.verify_minimum(self.sweep,neg,answer):
            raise ValueError('CDF support certificate failed independent range check')
        probability=list(map(F,answer['probability']))
        witness=[sum(p*mode[j] for p,mode in zip(probability,self.modes)) for j in range(self.m)]
        value=-F(answer['value'])
        if sum(a*b for a,b in zip(coefficient,witness))!=value:
            raise ValueError('CDF support mean-cost witness mismatch')
        ops=answer['operations']
        check_words=sum(b-a+1 for left,right,a,b in self.sweep.windows)
        self.meter.pay('population_support','payoff_compile_quantile_sweep_and_independent_certificate',
                       2*len(g)*self.m+8*sum(ops.values())+5*check_words+6*len(g)+12)
        self.support_cache[key]=(value,witness)
        self.support_records.append(dict(band=dict(lower=self.sweep.lower,upper=self.sweep.upper),
            coefficient=coefficient,payoff=g,value=value,mean_cost_witness=witness,negative_minimum=answer))
        self.meter.pay('population_storage','support_witness_and_trace_words',8+len(g)+self.m+6*len(answer['trace']))
        return value,witness

    def snapshot(self):
        return dict(source_id=self.source_id,draw_occurrences=self.n,physical_sampled_rows=len(self.intervals),
            radius=self.radius,tail_upper=self.tail_upper,
            lower_cdf=self.sweep.lower,upper_cdf=self.sweep.upper,
            physical_intervals={str(i):v for i,v in self.intervals.items()},
            fully_identified_rows=sum(l==u for l,u in self.intervals.values()),
            occurrence_weighted_unresolved=sum(self.multiplicity[i] for i,(l,u) in self.intervals.items() if l<u),
            receipt_ids=list(self.receipts))


def check_common_proof(instance,receipt,meter):
    if receipt['source_id']!=native.kernel.digest(instance) or receipt['budget']!=0:
        raise ValueError('Wrong common q-proof')
    raw=receipt['provider_response']
    if raw['status']!='UNSAT':
        raise ValueError('Common positive objective lower needs the paid negative proof')
    native.kernel.check_negative(instance,0,raw['proof'],meter)
    leaves=native.profile_kernel.compile_tree(raw['proof'],meter)
    if leaves!=receipt['leaf_masks']:
        raise ValueError('New tree compilation changed')
    return leaves


def arm(public,oracle,policy,progress):
    cpu,wall=time.process_time_ns(),time.perf_counter_ns()
    meter=native.kernel.Meter()
    costs=PopulationCosts(public,meter)
    instance=public['logical_source']
    profile=dict(source_identity=instance['identity'],witnesses=[],trees=[])
    for model in public['initial_checked_models']:
        witness=native.profile_kernel.compile_witness(instance,model,meter)
        witness['receipt_id']=native.kernel.digest(dict(source=instance['identity'],model=model,mask=witness['violation_mask']))
        profile['witnesses'].append(witness)
    meter.pay('source_admission','logical_source_and_witness_words',32+sum(len(c)+1 for c in instance['hard']))
    # All arms compile the same public two-value action contrast once.
    # The direct conventional policy then uses exactly the same cut without
    # a deliberately repeated planning charge.
    g=[mode[0]-mode[1] for mode in costs.modes]
    if g!=[-4,-4,4,4]:
        raise ValueError('Common direct contrast-to-cut compilation changed')
    meter.pay('shared_planning','compile_direct_two_value_contrast_once',2*len(g)*costs.m+4)
    events=[]
    def save(status):
        progress(dict(policy=policy,status=status,events=events,cost_state=costs.snapshot(),
                      local_invoice=meter.record()))
    save('initial_costs_and_witnesses_admitted')
    common=contract_quote.execute_complete(instance,0)
    leaves=check_common_proof(instance,common,meter)
    profile['trees'].append(dict(leaf_masks=leaves,receipt_id=common['receipt_id']))
    events.append(dict(kind='complete_logical',response=common))
    save('logical_proof_admitted')
    stages=[]
    def evaluate():
        result=joint.certificate(profile,costs,public['price'])
        meter.pay('output','checked_population_repair_source_and_bound',24)
        stages.append(dict(observations=len(oracle.calls),answer=result,cost_state=costs.snapshot()))
        return result
    result=evaluate()
    while result['bound']>public['tolerance']:
        row=next((i for i,(l,u) in costs.intervals.items() if l<=1<u),None)
        if row is None:
            break
        receipt=oracle.audit(row,1)
        costs.observe(receipt); events.append(dict(kind='cut_audit',receipt=receipt))
        save('audited_relevant_cut')
        if policy=='full_latent':
            l,u=costs.intervals[row]
            if l<u:
                receipt=oracle.audit(row,(l+u)//2)
                costs.observe(receipt); events.append(dict(kind='cut_audit',receipt=receipt))
                save('fully_resolved_latent_row')
        result=evaluate()
    save('completed' if result['bound']<=public['tolerance'] else 'unresolved')
    # The comparison needs acquisition/certificate costs as well as final cost.
    payload=dict(profile=profile,events=events,stages=stages,cost_state=costs.snapshot(),support_records=costs.support_records)
    serialized=len(canonical(payload))
    meter.pay('output','final_population_result_record',32)
    return dict(policy=policy,status='checked_action' if result['bound']<=public['tolerance'] else 'unresolved',
        answer=result,events=events,stages=stages,cost_state=costs.snapshot(),profile=profile,
        support_records=costs.support_records,
        summary=dict(checked_outputs=int(result['bound']<=public['tolerance']),requested_outputs=1,
            complete_logical_calls=1,external_cut_audits=len(oracle.calls),fixed_iid_draw_occurrences=public['sample_size'],
            distinct_audited_rows=len({r['row'] for r in oracle.calls}),
            fully_identified_rows=sum(l==u for l,u in costs.intervals.values()),
            final_bound=result['bound']),
        invoice=dict(named_units=meter.total+common['total_operation_units']+4*len(oracle.calls),
            local=meter.record(),complete_wrapper_units=common['total_operation_units'],
            audit_provider_software_units=4*len(oracle.calls),external_audits=len(oracle.calls),draws=public['sample_size'],
            full_cost='U + a*A + d*128 + rho*T + s*B + remaining actual fees; positive external rates are not supplied',
            native_calls=0,final_serialized_payload_bytes=serialized,
            note='Named sampling/admission work is charged above. External draw/audit prices, byte-time, final export and host peak memory require separate pricing; no missing term is assigned zero.'),
        timing=dict(process_ns=time.process_time_ns()-cpu,wall_ns=time.perf_counter_ns()-wall))


def execute(output):
    if output.exists():
        raise FileExistsError('Preserve constructed source and actual acquisitions')
    data=prepare()
    result=dict(version=VERSION,status='prospectively_prepared',evidence='DEVELOPMENT constructed common-law service',
        contributor='ChatGPT (GPT-6 Astra Pro)',start_utc=datetime.now(timezone.utc).isoformat(),source=data,
        implementation_sha256=native.sha(__file__),dependencies={p.name:native.sha(p) for p in
            [Path(cdf_sweep.__file__),Path(joint.__file__),Path(contract_quote.__file__)]},arms=[])
    def save():
        output.write_text(json.dumps(result,indent=2,default=encode)+'\n')
    save()
    result['code_admission']=contract_guard.admit()
    public={k:copy.deepcopy(v) for k,v in data.items() if k!='hidden_population'}
    try:
        for policy in public['policies']:
            def progress(prefix):
                result['active_prefix']=prefix;save()
            got=arm(public,CutOracle(data),policy,progress)
            result['arms'].append(got);result.pop('active_prefix',None);save()
            print(json.dumps(got['summary']|dict(policy=policy,named_units=got['invoice']['named_units']),default=encode),flush=True)
        # This diagnostic checks the one realized population, not the stated
        # confidence level. No unknown population law was an input to policies.
        counts=Counter(data['hidden_population']);size=data['population_size']
        probability=[F(counts[h],size) for h in range(4)]
        true_weights=[sum(p*mode[j] for p,mode in zip(probability,data['modes'])) for j in range(2)]
        diagnostic=[]
        for got in result['arms']:
            state=got['cost_state'];sweep=cdf_sweep.CDFSweep(state['lower_cdf'],state['upper_cdf'])
            mask=got['answer']['mask']
            cost=data['price'] if mask is None else sum(w for j,w in enumerate(true_weights) if mask&(1<<j))
            regret=cost-min(data['price'],*true_weights)
            diagnostic.append(dict(policy=got['policy'],true_source_in_band=sweep.feasible(probability),true_mean_costs=true_weights,
                                   realized_population_regret=regret,claimed_bound=got['answer']['bound']))
            if sweep.feasible(probability) and regret>got['answer']['bound']:
                raise AssertionError('Conditional population repair guarantee failed')
        result.update(status='complete',end_utc=datetime.now(timezone.utc).isoformat(),diagnostic=diagnostic,
            comparison='Direct-contrast ordinary control has the same actual information purchases. Fewer audits than full latent resolution establish task relevance, not superiority over strong conventional acquisition.',
            forecast='Separate S30 construction; does not alter F01 domain or establish new promotion readiness')
    except BaseException as exc:
        result.update(status='interrupted_or_failed',error=dict(type=type(exc).__name__,message=str(exc)));save();raise
    save()


if __name__=='__main__':
    execute(Path(sys.argv[1]))
