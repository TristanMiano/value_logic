#!/usr/bin/env python3
"""Guarded source reduction DEVELOPMENT, Codex (GPT-6), 2026-10-13.

An intentionally narrow independently checkable substitution interface. This
does not call VeriPB or assume unproved implications from a checksum.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import copy
import json
import sys
import time
import g01

VERSION = 's08-improving-maps-v1'
Meter = g01.kernel.Meter
seal, save = g01.seal, g01.save


def make_source(n):
    source = seal(dict(variables=n+1,hard=[[n+1,i+1] for i in range(n)],
                       features=[[ -(i+1)] for i in range(n+1)]))
    rows = []
    for i in range(n):
        rows.append([[value if j in (i,n) else 0 for j in range(n+1)] for value in (1,100)])
    rows += [[[2 if j==0 else 0 for j in range(n+1)]],
             [[value if j==n else 0 for j in range(n+1)] for value in (0,4)]]
    costs = seal(dict(rows=rows,dimension=n+1,source=source['identity']))
    return source,costs


def admit(source,costs,meter):
    n=source['variables']-1
    for obj in (source,costs):
        if obj['identity']!=g01.kernel.digest({k:v for k,v in obj.items() if k!='identity'}):
            raise ValueError('Changed source bytes')
    if costs['source']!=source['identity'] or costs['dimension']!=n+1 or n<1:
        raise ValueError('Wrong structural or cost source')
    if source['features']!=[[-i] for i in range(1,n+2)]:
        raise ValueError('This map admits exactly ordered atomic violations')
    hard=[set(c) for c in source['hard']]
    if any({n+1,i+1} not in hard for i in range(n)):
        raise ValueError('Missing conditional mandatory clause')
    substitution={i:-(n+1) for i in range(1,n+1)}
    steps=[]
    for clause in source['hard']:
        mapped=set()
        for lit in clause:
            replacement=substitution.get(abs(lit),abs(lit))
            mapped.add(replacement if lit>0 else -replacement)
        taut=any(-v in mapped for v in mapped)
        if not taut and mapped not in hard:
            raise ValueError('Feasibility of mapped hard clause is unproved')
        steps.append(dict(original=clause,substituted=sorted(mapped),reason='tautology' if taut else 'existing clause'))
        meter.pay('map_structure','literal_substitution_and_clause_obligation',4+3*len(clause))
    mins=[sum(min(mode[j] for mode in row) for row in costs['rows']) for j in range(n+1)]
    if any(v<0 for v in mins):
        raise ValueError('Nonincrease guard cannot admit negative feature weights')
    meter.pay('cost_guard','product_source_coordinate_lower_bounds',sum(len(row)*(n+1) for row in costs['rows'])+n+1)
    # Feasible s=0 assignments already have y=1. At s=1 the map only
    # removes y violations. The checked clauses and nonnegative guard imply
    # this for every original assignment, without enumerating them.
    meter.pay('map_objective','two_case_nonincrease_from_checked_clauses_and_signs',6+5*n)
    meter.pay('range_compile','representative_equalities_y_plus_s_equals_one',4+3*n)
    return seal(dict(original_source=source['identity'],cost_region=costs['identity'],
        substitution=substitution,structural_steps=steps,coordinate_lower=mins,error=0,
        range_equalities=[dict(features=[i,n],sum=1) for i in range(n)],
        conclusion='optimum preserving on this cost region; not an all-feasible equality'))


def map_model(model,n):
    s=(model>>n)&1
    return (s<<n) | ((1<<n)-1 if s==0 else 0)


def witness(source,model,meter):
    if not 0<=model<(1<<source['variables']):
        raise ValueError('Malformed witness')
    for clause in source['hard']:
        meter.pay('witness_check','source_clause_and_literals',1+len(clause))
        if not any(((model>>(abs(v)-1))&1)==int(v>0) for v in clause):
            raise ValueError('Infeasible original witness')
    return model


def support(costs,possible,coeff,meter):
    total=0
    for row,indices in zip(costs['rows'],possible):
        values=[sum(a*b for a,b in zip(row[h],coeff)) for h in indices]
        meter.pay('support','row_signed_dot_and_max',len(indices)*(2*len(coeff)+1))
        total+=max(values)
    return total


def gate(source,costs,receipt,possible,price,policy,meter):
    if receipt['original_source']!=source['identity'] or receipt['cost_region']!=costs['identity']:
        raise ValueError('Wrong reduction receipt')
    n=source['variables']-1
    # Two source-bound representatives, selected only after observations.
    inside=(1<<n)-1
    outside=1<<n
    if policy=='ordinary_star':
        # Ordinary weighted star cover: choose all leaves or the center.
        contrast=[1]*n+[-1]
        leaf_minus_center=support(costs,possible,contrast,meter)
        center_minus_leaf=support(costs,possible,[-a for a in contrast],meter)
        leaf_hi=support(costs,possible,[1]*n+[0],meter)
        center_hi=support(costs,possible,[0]*n+[1],meter)
        options=[(max(0,leaf_minus_center,leaf_hi-price),inside),
                 (max(0,center_minus_leaf,center_hi-price),outside)]
    else:
        options=[]
        for u,v in ((inside,outside),(outside,inside)):
            ub=[(u>>j)&1 for j in range(n+1)]
            vb=[(v>>j)&1 for j in range(n+1)]
            contrast=support(costs,possible,[a-b for a,b in zip(ub,vb)],meter)
            upper=support(costs,possible,ub,meter)
            options.append((max(0,contrast,upper-price),u))
    meter.pay('selection','checked_representative_minimum_and_binding',12)
    bound,model=min(options)
    witness(source,model,meter)
    return dict(bound=bound,model=model,source=source['identity'],cost_source=costs['identity'],
                reduction=receipt['identity'])


def diagnostic(source,costs,hidden,answer,possible):
    n=source['variables']-1
    feasible=[x for x in range(1<<(n+1)) if all(any(((x>>(abs(v)-1))&1)==int(v>0) for v in c) for c in source['hard'])]
    bad_equality=sum(any(((x>>i)&1)+((x>>n)&1)!=1 for i in range(n)) for x in feasible)
    worst=0
    for modes in product(*possible):
        weights=[sum(row[h][j] for row,h in zip(costs['rows'],modes)) for j in range(n+1)]
        def value(x): return sum(w for j,w in enumerate(weights) if x&(1<<j))
        best=min(value(x) for x in feasible)
        if any(value(map_model(x,n))>value(x) for x in feasible):
            raise AssertionError('Map is not improving')
        if min(value(map_model(x,n)) for x in feasible)!=best:
            raise AssertionError('Reduced optimum differs')
        worst=max(worst,value(answer['model'])-best)
    if worst>answer['bound']:
        raise AssertionError('False uniform output')
    return dict(feasible_models=len(feasible),global_equality_countermodels=bad_equality,
                worst_regret=worst,remaining_cost_modes=len(list(product(*possible))))


def epsilon_checks():
    # A signed-cost example demonstrates why the error and the negative
    # lower must both be retained. This is outside the nonnegative service.
    feasible=[3,4,5,6,7]  # n2: s0/y11, or s1/arbitrary y
    weights=[-3,5,0]
    cost=lambda x:sum(w for j,w in enumerate(weights) if x&(1<<j))
    reduced={map_model(x,2) for x in feasible}
    epsilon=max(0,max(cost(map_model(x,2))-cost(x) for x in feasible))
    original=min(map(cost,feasible)); new=min(map(cost,reduced))
    assert (original,new,epsilon)==(-3,0,3)
    assert new-epsilon<=original<=new
    return dict(weights=weights,original_optimum=original,reduced_optimum=new,error=epsilon,
        selected_reduced_cost=0,actual_regret=3,naive_no_error_bound=0,corrected_bound=3,
        replacement_price=10,actual_replacement_regret=13,wrong_nonnegative_clamp_bound=10,
        correct_unclamped_replacement_bound=13)


def run(directory):
    directory.mkdir(exist_ok=False)
    (directory/'impl.py').write_bytes(Path(__file__).read_bytes())
    all_sources=[make_source(n) for n in (1,3,5)]
    design=dict(version=VERSION,contributor='Codex (GPT-6)',stage='DEVELOPMENT',
        created_utc=datetime.now(timezone.utc).isoformat(),sources=all_sources,n_values=[1,3,5],
        implementation_sha256=g01.sha(__file__),declaration_sha256=g01.sha(HERE/'improving_maps.md'),
        dependencies={str(Path(g01.__file__).relative_to(HERE.parents[2])):g01.sha(g01.__file__)},
        policy='Admit map; audit only the d row; choose checked representative. Full-id is diagnostic.',
        prices='p=100*n+5; tau=0',complete_audit_tariff='D; add map/source/check/output/CPU/retention costs',
        source_prices='A,D in [1,4] symbolic positive audit tariffs; all unmeasured remaining rates explicit')
    save(directory/'design.json',design)
    results=dict(version=VERSION,status='acquiring',setups=[],arms=[],negative_controls=[],epsilon=epsilon_checks())
    for source,costs in all_sources:
        n=source['variables']-1
        setup=Meter()
        receipt=admit(source,costs,setup)
        save(directory/f'g{n}.json',dict(receipt=receipt,invoice=setup.record()))
        results['setups'].append(dict(n=n,named_units=setup.total))
        for policy in ('quotient','ordinary_star','full_identification'):
            rows=[]
            totals=Counter()
            for hidden_theta in product((0,1),repeat=n):
                for decision in (0,1):
                    hidden=(*hidden_theta,0,decision)
                    possible=[tuple(range(len(row))) for row in costs['rows']]
                    meter=Meter()
                    before=gate(source,costs,receipt,possible,100*n+5,policy,meter)
                    record=dict(hidden=hidden,before=before,events=[])
                    # This finite channel reads one physical row's selected
                    # coordinate. Its support and raw identity are checked.
                    for row_id in ([*range(n),n+1] if policy=='full_identification' else [n+1]):
                        coordinate=n
                        observation=costs['rows'][row_id][hidden[row_id]][coordinate]
                        raw=seal(dict(source=costs['identity'],row=row_id,coordinate=coordinate,value=observation))
                        record['events'].append(raw)
                        possible[row_id]=tuple(h for h in possible[row_id] if costs['rows'][row_id][h][coordinate]==observation)
                        if not possible[row_id]: raise ValueError('Cost source conflict')
                        meter.pay('audit','provider_source_binding_check_and_update',24)
                        totals['decision_audits' if row_id==n+1 else 'theta_audits']+=1
                    answer=gate(source,costs,receipt,possible,100*n+5,policy,meter)
                    if before['bound']!=2 or answer['bound']!=0:
                        raise AssertionError('Constructed partial audit failed')
                    record.update(answer=answer,invoice=meter.record())
                    # Save the actual outcome before the independent diagnostic.
                    rows.append(record)
                    save(directory/f'{n}{policy}.json',dict(status='acquiring',rows=rows))
                    record['diagnostic']=diagnostic(source,costs,hidden,answer,possible)
                    totals['outputs']+=1
                    totals['named_units']+=meter.total
            save(directory/f'{n}{policy}.json',dict(status='complete',rows=rows))
            results['arms'].append(dict(n=n,policy=policy,totals=dict(totals)))
            save(directory/'results.json',results)
    source,costs=make_source(1)
    for name,mutate in (
        ('infeasible_map',lambda s,c:s['hard'].append([1])),
        ('negative_weight_guard',lambda s,c:c['rows'][0].__setitem__(0,[-5,1]))):
        s,c=copy.deepcopy(source),copy.deepcopy(costs)
        mutate(s,c)
        s=seal({k:v for k,v in s.items() if k!='identity'})
        c['source']=s['identity'];c=seal({k:v for k,v in c.items() if k!='identity'})
        try: admit(s,c,Meter())
        except ValueError as exc: results['negative_controls'].append(dict(name=name,rejected=True,reason=str(exc)))
        else: raise AssertionError('Invalid reduction admitted')
    results.update(status='complete',completed_utc=datetime.now(timezone.utc).isoformat())
    save(directory/'results.json',results)
    print(json.dumps(results))


if __name__=='__main__':run(Path(sys.argv[1]))
