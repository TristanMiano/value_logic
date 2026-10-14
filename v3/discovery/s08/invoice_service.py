"""Paid full-feedback invoice learning, with ordinary own-invoice control.
DEVELOPMENT, Codex (GPT-6), 2026-10-14.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import sys
import time
import circuit_targets as ct
import invoice_syntax as sy
import check_invoice_syntax as sc
import invoice_bandit as ib
import invoice_completion as ic
import markov_paths as mk
import markov_service as ms
import star_learning as base
import paired_invoices as pi
import continuum_policy as cp
import g01

HERE=Path(__file__).resolve().parent
ARMS=('replay','circuit','ordinary_circuit','on_policy')
Meter=g01.kernel.Meter
VERSION='s08-paid-invoice-service-v1'
CALIBRATION=128


def prepare(directory,data,arm,meter):
    costs=data['audit_costs'];n=len(costs);proposals=[];all_policies={};vectors={};groups={}
    for r in mk.MENU:
        p=mk.plan(costs,r);proposals.append((f'r{r}',p['roots']));meter.pay('preparation','ordinary_model_policy_proposals',p['invoice']['total'])
    for rule in('left','right','middle'):
        roots={(a,b):(a if rule=='left' else b if rule=='right' else(a+b)//2) for a in range(n) for b in range(a+1,n)}
        proposals.append((rule,roots));meter.pay('preparation','ordinary_simple_policy_proposals',3*len(roots))
    for name,roots in proposals:
        ic.validate(costs,roots,{})
        if roots in all_policies.values():continue
        all_policies[name]=roots;values=[]
        for bits in product((0,1),repeat=n):
            fee,queries=pi.direct_fee(costs,roots,bits)
            _,checked=mk.conditional_trace(bits,roots)
            if queries!=checked or fee!=sum(costs[i] for i in checked):raise ValueError('Invoice admission failed')
            values.append(fee);meter.pay('preparation','produce_and_independently_check_invoice_world',18*n+12*len(queries))
        vectors[name]=tuple(values);groups.setdefault(tuple(values),[]).append(name)
    representatives=[members[0] for members in groups.values()];dominated={}
    for a in representatives:
        for b in representatives:
            if a==b:continue
            meter.pay('preparation','whole_world_dominance_check',2*2**n)
            if all(x>=y for x,y in zip(vectors[a],vectors[b])) and any(x>y for x,y in zip(vectors[a],vectors[b])):
                dominated[a]=b;break
    bank={r:all_policies[r] for r in representatives if r not in dominated};ranges={r:(min(vectors[r]),max(vectors[r])) for r in bank}
    arena=sy.Arena();edges={};syntax={}
    if arm in('circuit','ordinary_circuit') and len(bank)>1:
        for r,roots in bank.items():
            edge,tables=sy.compile_policy(arena,costs,roots);checked=sc.check(arena.nodes,costs,roots,tables,edge)
            edges[r]=edge;syntax[r]=dict(edge=edge,tables=tables,checking=checked)
            meter.pay('preparation','original_source_syntax_check',checked['total'])
        meter.pay('preparation','invoice_circuit_compilation',arena.meter.total)
    artifact=cp.normalize(dict(source=data,all_policies=all_policies,invoice_vectors=vectors,groups=list(groups.values()),dominated=dominated,
        retained=list(bank),ranges=ranges,syntax=syntax,nodes=arena.nodes))
    g01.save(directory/'bank.json',artifact)
    return bank,ranges,arena,edges


def run_arm(directory,case,rows,arm):
    data=ib.source(case['costs']);costs=case['costs'];n=len(costs);meter=Meter();cpu=time.process_time_ns();wall=time.perf_counter_ns()
    meter.pay('source','original_source_admission',24+n+sum(len(c)+1 for c in data['hard'])+5*len(data['features']))
    bank,ranges,arena,edges=prepare(directory,data,arm,meter);setup=meter.total;evaluator=ct.Evaluator(arena,costs)
    previous_eval=0;previous_arena=arena.meter.total;counts={r:0 for r in bank};sums={r:0 for r in bank};intervals=dict(ranges)
    chosen_counts=Counter();action_fee=pilot_fee=action_audits=pilot_audits=0;label_vectors=0;rank={r:i for i,r in enumerate(bank)}
    action_values={};final_bound=F(0);coverage_failures=0
    # Diagnostic true means are computed from the admitted finite function only,
    # kept out of all controller selection and learning updates.
    raw=json.loads((directory/'bank.json').read_text());worlds=list(product((0,1),repeat=n))
    diagnostic_means={r:sum(mk.world_probability(bits,case['r'])*v for bits,v in zip(worlds,raw['invoice_vectors'][r])) for r in bank}
    expected_excess=F(0)
    with (directory/'trace.jsonl').open('w') as trace,(directory/'diagnostics.jsonl').open('w') as diag:
        trace.write(json.dumps(dict(kind='header',source=data['identity'],arm=arm,version=VERSION,bank_sha256=g01.sha(directory/'bank.json')))+'\n');trace.flush()
        for t,row in enumerate(rows):
            before=meter.total
            if arm=='on_policy':chosen=min(bank,key=lambda r:(intervals[r][0],counts[r],rank[r]))
            else:chosen=min(bank,key=lambda r:(F(sums[r],counts[r]) if counts[r] else F(0),rank[r]))
            meter.pay('selection','choose_policy_from_observed_invoice_state',4*len(bank));chosen_counts[chosen]+=1
            request=f"{case['name']}-{arm}-{t}"
            trace.write(json.dumps(dict(kind='plan',request=request,policy=chosen,calibration=(arm!='on_policy' and t<CALIBRATION and len(bank)>1)))+'\n');trace.flush()
            provider=base.Provider(data,row,request,trace,meter);receipts=ms.acquire(provider,n,bank[chosen],meter)
            action=base.construct(data,receipts,request,meter);base.check(data,receipts,action,meter)
            own=sum(r['base_fee'] for r in receipts);action_fee+=own;action_audits+=len(receipts);known={r['node']:int(r['value']==1) for r in receipts}
            trace.write(json.dumps(dict(kind='output',request=request,action=action,base_fee=own,physical_audits=len(receipts)),separators=(',',':'))+'\n');trace.flush()
            labels={chosen:own};pilots=[]
            if arm!='on_policy' and t<CALIBRATION and len(bank)>1:
                for other in bank:
                    if other==chosen:continue
                    if arm=='replay':
                        state=[known.get(i,-1) for i in range(n)]
                        while True:
                            var=mk.pc.next_query(state,bank[other]);meter.pay('learning','counterfactual_trace_replay',5*n)
                            if var is None:break
                            receipt=provider.audit(var);pilots.append(receipt);known[var]=int(receipt['value']==1);state[var]=known[var]
                        value,queries=pi.direct_fee(costs,bank[other],[known.get(i,0) for i in range(n)])
                        if any(i not in known for i in queries):raise ValueError('Unobserved counterfactual label')
                        labels[other]=value;meter.pay('learning','reconstruct_from_scratch_policy_invoice',5*n+3*len(queries))
                    else:
                        while True:
                            offset,terms,support=evaluator.residual(edges[chosen],edges[other],known)
                            if not terms:labels[other]=own-offset;break
                            options=[i for i in range(n) if support>>i&1];var=min(options,key=lambda i:(costs[i],i))
                            if var in known:raise ValueError('Repeated target coordinate')
                            receipt=provider.audit(var);pilots.append(receipt);known[var]=int(receipt['value']==1)
                            evaluator.meter.pay('evaluation','choose_cheapest_remaining_target_variable',3*len(options))
                    trace.write(json.dumps(dict(kind='counterfactual_invoice',request=request,policy=other,from_scratch_fee=labels[other],observed_indicators=known),separators=(',',':'))+'\n');trace.flush()
                if set(labels)!=set(bank):raise ValueError('Incomplete feedback vector')
                label_vectors+=1
            extra=sum(r['base_fee'] for r in pilots);pilot_fee+=extra;pilot_audits+=len(pilots)
            if arm=='on_policy' or(t<CALIBRATION and len(bank)>1):
                for r,value in labels.items():
                    lo,hi=ranges[r]
                    if not lo<=value<=hi:raise ValueError('Invoice outside admitted source range')
                    counts[r]+=1;sums[r]+=value;meter.pay('learning','retain_observed_complete_invoice',8+counts[r].bit_length()+sums[r].bit_length())
                    if arm=='on_policy' and hi>lo:
                        a,b=base.confidence(counts[r],F(sums[r]-counts[r]*lo,hi-lo),len(bank),meter)
                        intervals[r]=(max(intervals[r][0],lo+(hi-lo)*a),min(intervals[r][1],lo+(hi-lo)*b))
                        if intervals[r][0]>intervals[r][1]:raise ValueError('Empty invoice confidence interval')
            if arm in('circuit','ordinary_circuit'):
                meter.pay('learning','receipt_conditioned_target_evaluation',evaluator.meter.total-previous_eval);previous_eval=evaluator.meter.total
                meter.pay('learning','retained_target_circuit_growth',arena.meter.total-previous_arena);previous_arena=arena.meter.total
            trace.write(json.dumps(dict(kind='request_end',request=request,pilot_fee=extra,pilot_audits=len(pilots),labels=labels,
                named_units=meter.total-before,counts=counts,sums=sums),separators=(',',':'))+'\n');trace.flush()
            # Diagnostics receive the full world only after the service update.
            bits=[int(v==1) for v in row]
            exact={r:pi.direct_fee(costs,roots,bits)[0] for r,roots in bank.items()}
            if any(exact[r]!=value for r,value in labels.items()):raise ValueError('Diagnostic invoice mismatch')
            assert ib.aa.direct_regret(data,action['assignment'],row)==0
            excess=diagnostic_means[chosen]-min(diagnostic_means.values());expected_excess+=excess
            diag.write(json.dumps(dict(request=t,hidden=row,action_regret=0,all_actual_policy_invoices=exact,conditional_expected_fee_excess=excess),default=g01.encode)+'\n')
        final_choice=min(bank,key=lambda r:(F(sums[r],counts[r]) if counts[r] else F(0),rank[r])) if arm!='on_policy' else min(bank,key=lambda r:(intervals[r][0],counts[r],rank[r]))
        if arm!='on_policy' and len(bank)>1:
            for r in bank:
                lo,hi=ranges[r]
                a,b=base.confidence(counts[r],F(sums[r]-counts[r]*lo,hi-lo) if hi>lo else F(0),len(bank),meter)
                intervals[r]=(lo+(hi-lo)*a,lo+(hi-lo)*b)
        final_bound=max(F(0),intervals[final_choice][1]-min(lo for lo,hi in intervals.values())) if len(bank)>1 else F(0)
        coverage_failures=sum(not lo<=diagnostic_means[r]<=hi for r,(lo,hi) in intervals.items())
        trace.write(json.dumps(dict(kind='final_statistical_report',choice=final_choice,intervals=intervals,mean_fee_regret_upper=final_bound),default=g01.encode)+'\n')
    if arm in('circuit','ordinary_circuit'):
        g01.save(directory/'target_cache.json',cp.normalize(dict(nodes=arena.nodes,cofactor_cache=evaluator.cache,supports=evaluator.supports)))
    result=dict(outputs=len(rows),base_audit_fee=action_fee+pilot_fee,action_fee=action_fee,pilot_fee=pilot_fee,
        physical_audits=action_audits+pilot_audits,action_audits=action_audits,pilot_audits=pilot_audits,
        named_units=meter.total,setup_units=setup,invoice=meter.record(),retained_policies=list(bank),selected_policies=chosen_counts,
        complete_calibration_vectors=label_vectors,counts=counts,sums=sums,final_choice=final_choice,final_intervals=intervals,
        final_mean_fee_regret_upper=final_bound,diagnostic_means=diagnostic_means,cumulative_expected_action_fee_regret=expected_excess,
        final_observed_coverage_failures=coverage_failures,trace_bytes=(directory/'trace.jsonl').stat().st_size,
        target_cache_bytes=(directory/'target_cache.json').stat().st_size if(directory/'target_cache.json').exists() else 0,
        arm_cpu_ns=time.process_time_ns()-cpu,arm_wall_ns=time.perf_counter_ns()-wall)
    g01.save(directory/'result.json',result)


if __name__=='__main__':
    directory=Path(sys.argv[1]);directory.mkdir(exist_ok=False);design=json.loads(Path(sys.argv[2]).read_text())
    case=next(c for c in design['cases'] if c['name']==sys.argv[3]);arm=sys.argv[4]
    if arm not in ARMS:raise ValueError('Unknown arm')
    for name,digest in design['dependencies'].items():
        if g01.sha(HERE/name)!=digest:raise ValueError('Dependency changed after declaration')
    if g01.sha(__file__)!=design['source_sha256']:raise ValueError('Service source changed')
    rows=ms.draw(len(case['costs']),case['r'],design['requests'],case['seed'])
    run_arm(directory,case,rows,arm)
