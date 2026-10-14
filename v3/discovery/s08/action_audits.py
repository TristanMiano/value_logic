#!/usr/bin/env python3
"""Paid action-adaptive bit audits on an admitted forest. DEVELOPMENT.
Codex (GPT-6), 2026-10-14. No external graph or SAT solver is assumed.
"""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
from itertools import product
from pathlib import Path
import copy
import json
import platform
import random
import sys
import time
import g01
import joint_guard

HERE=Path(__file__).resolve().parent
VERSION='s08-action-audits-v1'
Meter=g01.kernel.Meter


def original(edges,costs):
    hard=[];features=[]
    for a,b,w in edges:
        for k in range(2):
            i=len(features)+1
            hard.extend([[i,i+1],[-i,-i-1]])
            features.extend([dict(clause=[-i],node=a,scale=w),dict(clause=[-i-1],node=b,scale=w)])
    return g01.seal(dict(n=len(costs),variables=len(features),hard=hard,
        features=features,audit_costs=costs,edges=edges,bit_source='all independent binary vectors'))


def admit(source):
    meter=Meter()
    if source['identity']!=g01.kernel.digest({k:v for k,v in source.items() if k!='identity'}):
        raise ValueError('Original source identity mismatch')
    edges,costs=source['edges'],source['audit_costs']
    if source['n']!=len(costs) or any(type(c)is not int or c<=0 for c in costs):
        raise ValueError('Positive integer audit costs required')
    if source!=original(edges,costs):
        raise ValueError('Original source is not the declared independent exactly-one product')
    meter.pay('source_admission','read_clauses_features_costs_and_bind_factorization',
        12+len(costs)+sum(len(c)+1 for c in source['hard'])+5*len(source['features']))
    adjacency,parent,order=joint_guard.tree(edges,[[0,1] for _ in costs],meter)
    return adjacency,parent,order,meter.record()


def remaining(edges,chosen):
    return sum(w for a,b,w in edges if not (chosen>>a&1 or chosen>>b&1))


def residual_dp(source,tau):
    """Minimize audit fee with residual-weight states, truncated at tau."""
    adjacency,parent,order,_=admit(source)
    meter=Meter();tables={}
    for i in reversed(order):
        row={(0,0):(0,0),(1,0):(source['audit_costs'][i],1<<i)}
        for j,w in adjacency[i]:
            if parent[j]!=i:continue
            combined={}
            for (x,r),(fee,mask) in row.items():
                for (y,s),(childfee,childmask) in tables[j].items():
                    q=r+s+w*(1-x)*(1-y)
                    meter.pay('planning','residual_dp_transition',9)
                    if q>tau:continue
                    key=(x,q);value=(fee+childfee,mask|childmask)
                    if key not in combined or value<combined[key]:combined[key]=value
            row=combined
        tables[i]=row
        meter.pay('planning','retain_residual_state_words',4*len(row))
    fee,mask=min(tables[0].values())
    meter.pay('planning','select_root_and_emit_audit_set',len(tables[0])+len(source['audit_costs']))
    return dict(mask=mask,fee=fee,residual=remaining(source['edges'],mask),invoice=meter.record(),
        states=sum(len(row) for row in tables.values()))


def ordinary_budget_dp(source,tau):
    """Independent cost-axis graph DP: least uncovered weight at each exact fee."""
    adjacency,parent,order,_=admit(source)
    meter=Meter();tables={}
    for i in reversed(order):
        rows={(0,0):(0,0),(1,source['audit_costs'][i]):(0,1<<i)}
        children=[(j,w) for j,w in adjacency[i] if parent[j]==i]
        for j,weight in children:
            nxt={}
            for (take,budget),(uncovered,mask) in rows.items():
                for (childtake,childbudget),(childuncovered,childmask) in tables[j].items():
                    key=(take,budget+childbudget)
                    value=(uncovered+childuncovered+(weight if not take and not childtake else 0),mask|childmask)
                    meter.pay('planning','ordinary_budget_transition',8)
                    if key not in nxt or value<nxt[key]:nxt[key]=value
            rows=nxt
        tables[i]=rows
        meter.pay('planning','retain_budget_state_words',4*len(rows))
    fee,residual,mask=min((fee,rem,mask) for (take,fee),(rem,mask) in tables[0].items() if rem<=tau)
    meter.pay('planning','choose_sufficient_budget_and_set',len(tables[0])+len(source['audit_costs']))
    return dict(mask=mask,fee=fee,residual=residual,invoice=meter.record(),states=sum(len(row) for row in tables.values()))


def greedy(source,tau):
    meter=Meter();mask=0
    edges,costs=source['edges'],source['audit_costs']
    while remaining(edges,mask)>tau:
        benefits=[]
        for i,c in enumerate(costs):
            if mask>>i&1:continue
            gain=sum(w for a,b,w in edges if i in (a,b) and not(mask>>a&1 or mask>>b&1))
            benefits.append((Fraction(gain,c),-c,-i))
            meter.pay('planning','greedy_uncovered_incidence_scan',4*len(edges)+3)
        _,_,negative_i=max(benefits);mask|=1<<(-negative_i)
    return dict(mask=mask,fee=sum(c for i,c in enumerate(costs) if mask>>i&1),
        residual=remaining(edges,mask),invoice=meter.record(),states=0)


def full(source,tau):
    meter=Meter();meter.pay('planning','full_identification_list',source['n'])
    return dict(mask=(1<<source['n'])-1,fee=sum(source['audit_costs']),residual=0,
        invoice=meter.record(),states=0)


def check_plan(source,tau,plan):
    meter=Meter();mask=plan['mask']
    if type(mask)is not int or not 0<=mask<1<<source['n']:raise ValueError('Invalid audit set')
    fee=sum(c for i,c in enumerate(source['audit_costs']) if mask>>i&1)
    residual=sum(w for a,b,w in source['edges'] if not(mask>>a&1 or mask>>b&1))
    if fee!=plan['fee'] or residual!=plan['residual'] or residual>tau:raise ValueError('Insufficient plan')
    meter.pay('plan_check','audit_set_fee_and_uncovered_edges',3*source['n']+5*len(source['edges']))
    return meter.record()


class PhysicalSource:
    def __init__(self,source,hidden,stream,trace):
        self._hidden=tuple(hidden);self.source=source;self.stream=stream;self.trace=trace;self.seen=set()
    def audit(self,i):
        if i in self.seen:raise ValueError('Duplicate physical audit')
        if not 0<=i<len(self._hidden):raise ValueError('Invalid physical identity')
        receipt=g01.seal(dict(source=self.source['identity'],stream=self.stream,node=i,
            value=self._hidden[i],base_fee=self.source['audit_costs'][i],sequence=len(self.seen)))
        self.seen.add(i)
        with self.trace.open('a',encoding='utf-8') as f:f.write(json.dumps(dict(kind='physical_audit',receipt=receipt))+'\n')
        return receipt


def act(source,receipts):
    meter=Meter();known={}
    for receipt in receipts:
        if receipt['identity']!=g01.kernel.digest({k:v for k,v in receipt.items() if k!='identity'}):
            raise ValueError('Receipt content hash mismatch')
        if receipt['source']!=source['identity'] or receipt['node'] in known or receipt['value'] not in (0,1):
            raise ValueError('Invalid or repeated receipt')
        known[receipt['node']]=receipt['value']
        meter.pay('receipt_admission','bind_identity_value_and_fee',12)
    choices=[]
    for a,b,w in source['edges']:
        if a in known and b in known:chosen=[a,a] if known[a]<=known[b] else [b,b]
        elif a in known:chosen=[a,a] if known[a]==0 else [b,b]
        elif b in known:chosen=[b,b] if known[b]==0 else [a,a]
        else:chosen=[a,b]
        choices.extend(chosen)
        meter.pay('action','construct_two_component_decision',8)
    assignment=0
    for index,node in enumerate(choices):
        a,b,w=source['edges'][index//2]
        assignment|=1<<(2*index+(node==b))
    return dict(choices=choices,assignment=assignment),meter.record()


def check_output(source,receipts,action,tau):
    """Independent direct clause and local regret check; no hidden truth access."""
    meter=Meter();observed={r['node']:r['value'] for r in receipts}
    assignment=action['assignment']
    if not 0<=assignment<1<<source['variables']:raise ValueError('Assignment scope')
    for clause in source['hard']:
        if not any(bool(assignment>>(abs(lit)-1)&1)==(lit>0) for lit in clause):raise ValueError('Infeasible original action')
        meter.pay('output_check','original_clause_evaluation',1+len(clause))
    residual=0
    for index,(a,b,w) in enumerate(source['edges']):
        selected=[]
        for component in range(2):
            f=source['features'][4*index+2*component:4*index+2*component+2]
            selected.extend(feature['node'] for offset,feature in enumerate(f)
                if assignment>>(4*index+2*component+offset)&1)
        if selected!=action['choices'][2*index:2*index+2]:raise ValueError('Action decoding disagreement')
        if a not in observed and b not in observed:
            if sorted(selected)!=sorted((a,b)):raise ValueError('Unbalanced unresolved action')
            residual+=w
        else:
            qa=[observed[a]] if a in observed else [0,1]
            qb=[observed[b]] if b in observed else [0,1]
            for va,vb in product(qa,qb):
                values={a:va,b:vb}
                if sum(values[x] for x in selected)>2*min(va,vb):raise ValueError('Covered edge action is not uniformly optimal')
        meter.pay('output_check','covered_local_cases_or_residual_guard',24)
    if residual>tau:raise ValueError('Regret tolerance not met')
    return residual,meter.record()


def direct_regret(source,assignment,bits):
    # Independently minimize each checked exactly-one factor at actual costs.
    value=sum(f['scale']*bits[f['node']] for i,f in enumerate(source['features']) if assignment>>i&1)
    optimum=sum(min(f['scale']*bits[f['node']] for f in source['features'][i:i+2])
        for i in range(0,len(source['features']),2))
    return value-optimum


def exhaustive_best_set(source,tau):
    return min((sum(c for i,c in enumerate(source['audit_costs']) if mask>>i&1),mask)
        for mask in range(1<<source['n']) if remaining(source['edges'],mask)<=tau)


def execute(source,hidden,tau,plan,stream,trace,enumerate_completions):
    provider=PhysicalSource(source,hidden,stream,trace)
    receipts=[provider.audit(i) for i in range(source['n']) if plan['mask']>>i&1]
    action,construction=act(source,receipts)
    bound,checking=check_output(source,receipts,action,tau)
    output=dict(stream=stream,receipts=receipts,action=action,bound=bound,
        physical_audits=len(receipts),base_audit_fee=sum(r['base_fee'] for r in receipts),
        local_units=construction['total']+checking['total'],construction=construction,checking=checking)
    with trace.open('a',encoding='utf-8') as f:f.write(json.dumps(dict(kind='output',output=output))+'\n')
    # Truth is first consulted outside the provider after the durable output.
    output['post_output_diagnostic']=dict(hidden=list(hidden),realized_regret=direct_regret(source,action['assignment'],hidden))
    assert output['post_output_diagnostic']['realized_regret']<=bound<=tau
    if enumerate_completions:
        known={r['node']:r['value'] for r in receipts}
        candidates=product(*([[known[i]] if i in known else [0,1] for i in range(source['n'])]))
        worst=max(direct_regret(source,action['assignment'],bits) for bits in candidates)
        assert worst==bound
        output['post_output_diagnostic']['exhaustive_worst_regret']=worst
    return output


def run(directory):
    directory.mkdir(exist_ok=False);(directory/'impl.py').write_bytes(Path(__file__).read_bytes())
    rng=random.Random(261014)
    small=[]
    for n in range(2,8):
        for repeat in range(2):
            edges=[[i,rng.randrange(i),rng.randrange(1,5)] for i in range(1,n)]
            source=original(edges,[rng.randrange(1,6) for _ in range(n)])
            small.append(dict(name=f'n{n}r{repeat}',source=source,tolerances=sorted({0,sum(e[2] for e in edges)//3})))
    large=[]
    for n in (32,128):
        edges=[[i,rng.randrange(i),rng.randrange(1,5)] for i in range(1,n)]
        large.append(dict(name=f'large{n}',source=original(edges,[rng.randrange(1,6) for _ in range(n)]),
            tolerances=[0,sum(e[2] for e in edges)//8]))
    design=dict(version=VERSION,stage='DEVELOPMENT',contributor='Codex (GPT-6)',
        created_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),small=small,large=large,
        arms=['residual_dp','ordinary_budget_dp','greedy','full'],large_hidden_seed=26101499,
        dependency_hashes={str(p.relative_to(HERE)):g01.sha(p) for p in (Path(__file__),HERE/'g01.py',HERE/'joint_guard.py')},
        declaration_sha256=g01.sha(HERE/'action_audits.md'),
        cost_scope='Named source/planning/checking operations, actual physical base audit fees, exact serialized trace bytes. Other host and byte-time rates remain explicit unknowns.')
    g01.save(directory/'design.json',design)
    cpu=time.process_time_ns();wall=time.perf_counter_ns();result=dict(status='running',cases=[],negative_controls=[])
    for case in small+large:
        source=case['source'];_,_,_,admission=admit(source)
        for tau in case['tolerances']:
            plans={name:fn(source,tau) for name,fn in (
                ('residual_dp',residual_dp),('ordinary_budget_dp',ordinary_budget_dp),('greedy',greedy),('full',full))}
            assert plans['residual_dp']['fee']==plans['ordinary_budget_dp']['fee']
            if case in small:assert plans['residual_dp']['fee']==exhaustive_best_set(source,tau)[0]
            hidden=list(product((0,1),repeat=source['n'])) if case in small else [tuple(random.Random(26101499+i).randrange(1<<source['n'])>>j&1 for j in range(source['n'])) for i in range(8)]
            # Plans and checks are durable before acquisition starts.
            name=f"{case['name']}t{tau}"
            checks={arm:check_plan(source,tau,p) for arm,p in plans.items()}
            g01.save(directory/f'{name}_plans.json',dict(source=source['identity'],tau=tau,plans=plans,checks=checks))
            row=dict(name=name,n=source['n'],tau=tau,source=source['identity'],admission=admission,arms={})
            for arm,plan in plans.items():
                trace=directory/f'{name}_{arm}.jsonl'
                outputs=[execute(source,bits,tau,plan,f'{name}-{arm}-{k}',trace,case in small) for k,bits in enumerate(hidden)]
                bill=dict(outputs=len(outputs),physical_audits=sum(o['physical_audits'] for o in outputs),
                    base_audit_fee=sum(o['base_audit_fee'] for o in outputs),
                    setup_units=admission['total']+plan['invoice']['total']+checks[arm]['total'],
                    service_units=sum(o['local_units'] for o in outputs),trace_bytes=trace.stat().st_size,
                    realized_regret=sum(o['post_output_diagnostic']['realized_regret'] for o in outputs))
                row['arms'][arm]=dict(plan=plan,plan_check=checks[arm],bill=bill)
                g01.save(directory/f'{name}_{arm}_diagnostics.json',[o['post_output_diagnostic'] for o in outputs])
            result['cases'].append(row);g01.save(directory/'results.json',result)
    source=small[0]['source'];tau=0;plan=residual_dp(source,tau)
    for name in ('extra_hard_clause','negative_scale','cyclic_source','insufficient_plan'):
        try:
            if name=='extra_hard_clause':
                bad=copy.deepcopy(source);bad['hard'].append([1]);bad.pop('identity');bad=g01.seal(bad);admit(bad)
            elif name=='negative_scale':admit(original([[0,1,-1]],[1,1]))
            elif name=='cyclic_source':admit(original([[0,1,1],[1,2,1],[2,0,1]],[1,1,1]))
            else:check_plan(source,0,dict(mask=0,fee=0,residual=0))
        except ValueError as exc:result['negative_controls'].append(dict(name=name,rejected=True,reason=str(exc)))
        else:raise AssertionError(f'{name} accepted')
    summary={}
    for arm in design['arms']:
        summary[arm]=dict(Counter({k:sum(r['arms'][arm]['bill'][k] for r in result['cases'])
            for k in result['cases'][0]['arms'][arm]['bill']}))
    result.update(status='complete',summary=summary,completed_utc=datetime.now(timezone.utc).isoformat(),
        development_resource=dict(cpu_ns=time.process_time_ns()-cpu,wall_ns=time.perf_counter_ns()-wall,
            scope='All arms and exhaustive diagnostics combined; not isolated service speed.'))
    g01.save(directory/'results.json',result)
    print(json.dumps(dict(status=result['status'],cases=len(result['cases']),summary=summary,negative_controls=result['negative_controls'])))


if __name__=='__main__':run(Path(sys.argv[1]))
