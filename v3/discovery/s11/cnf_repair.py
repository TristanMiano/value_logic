"""DEVELOPMENT conditional CNF-mask menus with native advice, Codex (GPT-6)."""
from itertools import combinations,product
from pathlib import Path
import argparse
import hashlib
import json
import os
import platform
import sys
import time
sys.path.insert(0,str(Path(os.environ['TEMP'])/'value_logic_s10_deps'))
import pysat
from pysat.solvers import Solver


def satisfies(mask,clauses):
    return all(any(bool(mask&(1<<(abs(lit)-1)))==(lit>0) for lit in clause) for clause in clauses)


def consistent(mask,assumptions):
    return all(bool(mask&(1<<(abs(lit)-1)))==(lit>0) for lit in assumptions)


def models(diagram):
    n=diagram['variables'];nodes=diagram['nodes'];order=diagram['order'];out=[];visits=0
    stack=[(diagram['root'],0,0)]
    while stack:
        node,depth,mask=stack.pop();visits+=1
        if node==0:continue
        if node==1:
            assert depth==n;out.append(mask);continue
        record=nodes[node];assert record['depth']==depth
        stack.append((record['low'],depth+1,mask))
        stack.append((record['high'],depth+1,mask|(1<<(order[depth]-1))))
    assert len(out)==len(set(out)) and out
    return sorted(out),visits


def run_arm(source,worlds,masks,histories,reuse):
    n=source['variables'];clauses=source['hard'];worldset=set(worlds)
    stats={'native_calls':0,'valid_core_reuses':0,'invalid_witness_reuses':0,
           'universal_model_checks':0,'core_generalization_model_checks':0,'witness_checks':0,
           'cache_literal_checks':0,'cache_world_checks':0,'affected_clause_checks':0}
    positive={mask:[] for mask in masks};negative={mask:[] for mask in masks};rows=[];start=time.perf_counter_ns()
    affected={mask:[i for i,clause in enumerate(clauses) if any(mask&(1<<(abs(lit)-1)) for lit in clause)] for mask in masks}
    with Solver(name='g3',bootstrap_with=clauses) as solver:
        for h in histories:
            hset=frozenset(h);compatible=[x for x in worlds if consistent(x,h)]
            stats['native_calls']+=1;live=solver.solve(assumptions=h)
            assert live==bool(compatible)
            if not live:
                rows.append({'history':h,'reachable':False});continue
            valid=[];generalized=[];invalid=[]
            for mask in masks:
                answer=None;needed=None;counter=None;origin=None
                if reuse:
                    for core in positive[mask]:
                        stats['cache_literal_checks']+=len(core)
                        if core<=hset:answer=True;needed=core;origin='valid_core';stats['valid_core_reuses']+=1;break
                    if answer is None:
                        for x in negative[mask]:
                            stats['cache_world_checks']+=1
                            if consistent(x,h):answer=False;counter=x;origin='invalid_witness';stats['invalid_witness_reuses']+=1;break
                if answer is None:
                    needed=set();answer=True;origin='native'
                    for ci in affected[mask]:
                        stats['affected_clause_checks']+=1
                        transformed=[-lit if mask&(1<<(abs(lit)-1)) else lit for lit in clauses[ci]]
                        negated=[-lit for lit in transformed]
                        assumptions=list(dict.fromkeys(h+negated));stats['native_calls']+=1
                        sat=solver.solve(assumptions=assumptions)
                        if sat:
                            counter=sum(1<<(lit-1) for lit in solver.get_model() if 1<=lit<=n)
                            assert satisfies(counter,clauses) and consistent(counter,h)
                            assert not satisfies(counter^mask,clauses);stats['witness_checks']+=1
                            answer=False
                            if counter not in negative[mask]:negative[mask].append(counter)
                            break
                        core=set(solver.get_core() or []);assert core<=set(assumptions)
                        needed|=core&hset
                    if answer:
                        needed=frozenset(needed)
                        for x in worlds:
                            if consistent(x,needed):
                                stats['core_generalization_model_checks']+=1
                                assert (x^mask) in worldset,(h,mask,needed,x)
                        if not any(core<=needed for core in positive[mask]):
                            positive[mask]=[core for core in positive[mask] if not needed<=core]+[needed]
                exact=True
                for x in compatible:
                    stats['universal_model_checks']+=1
                    if (x^mask) not in worldset:exact=False;break
                assert answer==exact,(h,mask,answer,exact)
                if answer:
                    valid.append(mask);generalized.append({'mask':mask,'needed_literals':sorted(needed),'origin':origin})
                else:invalid.append({'mask':mask,'world':counter,'origin':origin})
            rows.append({'history':h,'reachable':True,'worlds':len(compatible),'valid_masks':valid,
                         'valid_records':generalized,'invalid_records':invalid})
        native_stats=solver.accum_stats()
    root=set(rows[0]['valid_masks'])
    for row in rows:
        if row['reachable']:row['newly_enabled_masks']=sorted(set(row['valid_masks'])-root)
    return {'reuse':reuse,'counts':stats,'native_stats':native_stats,'histories':rows,
            'elapsed_ns':time.perf_counter_ns()-start,
            'distinct_new_masks':sorted(set().union(*(set(row.get('newly_enabled_masks',[])) for row in rows)))}


def case(index):
    prior=Path(__file__).resolve().parent.parent/'s10';name=['uf20-01','uf20-02','uf20-03','uf50-01','uf50-02','uf50-03'][index]
    if index<3:
        source_path=prior/'uf01'/name/'source.json';source=json.loads(source_path.read_text(encoding='utf-8'))
        diagram_path=prior/'up01'/name/'unit.json';record=json.loads(diagram_path.read_text(encoding='utf-8'))
        diagram=record['transformed']['diagram'];historical_invoice=record['invoice'];expected_count=None
    else:
        source_path=prior/'up50'/'design.json';design=json.loads(source_path.read_text(encoding='utf-8'))
        source=next(v['source'] for v in design['sources'] if v['source']['name']==name)
        diagram_path=prior/'up50'/name/'unit'/'diagram.json';diagram=json.loads(diagram_path.read_text(encoding='utf-8'))['diagram']
        result_path=prior/'up50'/name/'unit'/'results.json';old=json.loads(result_path.read_text(encoding='utf-8'))
        historical_invoice=old['compilation'];expected_count=int(old['model_count'])
    assert source['id']==diagram['source_id'];n=source['variables'];worlds,visits=models(diagram)
    assert all(satisfies(x,source['hard']) for x in worlds)
    if expected_count is not None:assert len(worlds)==expected_count
    query_vars=[1,(n+1)//2]
    histories=sorted(([v*s for v,s in zip(query_vars,values) if s] for values in product((-1,0,1),repeat=2)),key=lambda h:(len(h),h))
    masks=[0]+[1<<j for j in range(n)]+[sum(1<<j for j in pair) for pair in combinations(range(n),2)]
    arms=[run_arm(source,worlds,masks,histories,reuse) for reuse in (False,True)]
    for a,b in zip(arms[0]['histories'],arms[1]['histories']):assert a.get('valid_masks')==b.get('valid_masks')
    return {'contributor':'Codex (GPT-6)','status':'DEVELOPMENT','case':index,'name':name,'n':n,'query_variables':query_vars,
        'total_operation_cap':4,'max_mask_weight':2,'candidate_masks':len(masks),'source_model_count':len(worlds),
        'diagram_path_visits':visits,'source_models':worlds,'arms':arms,'historical_source_admission':historical_invoice,
        'physical_truth_purchases':0,'new_source_admission_purchases':0,
        'inputs':{str(p.relative_to(prior.parent).as_posix()):hashlib.sha256(p.read_bytes()).hexdigest() for p in (source_path,diagram_path)},
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'environment':{'python':sys.version,'platform':platform.platform(),'pysat':pysat.__version__,'solver':'Glucose3'},
        'scope':'Development conditional-mask compilation on inherited checked source diagrams. Native cores are advice; universal model checks inherit prior source completeness. No complete economic invoice.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',type=int,required=True);p.add_argument('--out',required=True)
    a=p.parse_args();result=case(a.case)
    with open(a.out,'x',encoding='utf-8',newline='\n') as out:out.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('case','name','n','candidate_masks','source_model_count')}|
      {'arms':[{'reuse':v['reuse'],'counts':v['counts'],'native_stats':v['native_stats'],
                'new_masks':len(v['distinct_new_masks']),'menus':[len(h.get('valid_masks',[])) for h in v['histories']],
                'elapsed_ns':v['elapsed_ns']} for v in result['arms']]}))
