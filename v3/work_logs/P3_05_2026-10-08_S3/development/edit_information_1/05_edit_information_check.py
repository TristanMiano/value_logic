#!/usr/bin/env python3
"""DEVELOPMENT: edit congruence, decision covers and complete finite subfamilies.

A separate set/trace evaluator audits the certificate outputs. Internal
self-review, not independent-agent validation or a frozen experiment.
"""
from __future__ import annotations
from dataclasses import replace
from datetime import datetime,timezone
from fractions import Fraction as F
from itertools import product,combinations
from pathlib import Path
import argparse,hashlib,importlib.util,json,platform,sys,time,traceback
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('p305_edit_target',HERE/'05_edit_information.py');E=importlib.util.module_from_spec(sp);sys.modules[sp.name]=E;sp.loader.exec_module(E)
sp=importlib.util.spec_from_file_location('p305_edit_fixture',HERE/'05_portfolio_check.py');T=importlib.util.module_from_spec(sp);sys.modules[sp.name]=T;sp.loader.exec_module(T)
COUNT=0;CASES=[];OUT=None

def ok(x,m):
    global COUNT
    COUNT+=1
    if not x:raise AssertionError(m)

def rejection(f):
    global COUNT
    COUNT+=1
    try:f()
    except ValueError as exc:return str(exc)
    raise AssertionError('Invalid certificate accepted.')

def save(case):
    CASES.append(case)
    if OUT is not None:
        with (OUT/'completed_units.jsonl').open('a') as f:f.write(json.dumps(case,default=str)+'\n')

def partitions(n):
    """Independent restricted-growth-word enumeration of ALL set partitions."""
    def visit(word):
        if len(word)==n:
            yield tuple(tuple(i for i,c in enumerate(word) if c==b) for b in range(max(word)+1));return
        for b in range(max(word)+2):yield from visit(word+(b,))
    yield from visit((0,))

def partition_oracle(g,blocks,allowed=None,edges=False):
    code={s:i for i,b in enumerate(blocks) for s in b}
    for block in blocks:
        if allowed is None:
            if len({g.outputs[s] for s in block})!=1:return False
        elif not set.intersection(*(set(allowed[s]) for s in block)):return False
        for e in g.edits:
            if len({code[e.successors[s]] for s in block})!=1:return False
            if edges and len({e.observations[s] for s in block})!=1:return False
    return True

def simulate_cover(system,pf,depth):
    """Direct table simulation; no production quotient or receiver is invoked."""
    for start in range(len(system.graph.states)):
        for k in range(depth+1):
            for word in product(range(len(system.graph.edits)),repeat=k):
                s,c=start,pf.initial_codes[start]
                ok(pf.actions[c] in system.acceptable[s],'Initial readable action fails.')
                for e in word:
                    s=system.graph.edits[e].successors[s];c=pf.successors[c][e]
                    ok(pf.actions[c] in system.acceptable[s],'Edited readable action fails.')

def graph(n,outputs,transitions=(),labels=None,scope='fixture'):
    edits=tuple(E.Edit(f'e{i}',tuple(ts),tuple('unit-work' for _ in range(n)) if labels is None else tuple(labels[i])) for i,ts in enumerate(transitions))
    return E.Graph(scope,tuple(f's{i}' for i in range(n)),tuple(outputs),edits)

def exact_cases():
    xs=list(product((0,1),repeat=3));ix={x:i for i,x in enumerate(xs)}
    shift=tuple(ix[(x[1],x[2],0)] for x in xs)
    g=graph(8,tuple(str(x[0]) for x in xs),(shift,),scope='three-bit-shift')
    work={};p=E.build_quotient(g,work=work);verify={};r=E.verify_quotient(p,g,g.record(),verify)
    ok(r['classes']==8,'Two-step observable future was lost.')
    w=E.distinguishing_word(g,ix[(0,0,0)],ix[(0,0,1)])
    ok(w==(0,0),'The separator must need exactly two edits.')
    initial=(tuple(i for i,x in enumerate(xs) if x[0]==0),tuple(i for i,x in enumerate(xs) if x[0]==1))
    forged=replace(p,blocks=initial,separations=())
    errors={'current_only':rejection(lambda:E.verify_quotient(forged,g,g.record()))}
    errors['false_word']=rejection(lambda:E.verify_quotient(replace(p,separations=tuple((a,b,()) for a,b,w in p.separations)),g,g.record()))
    errors['missing_pairs']=rejection(lambda:E.verify_quotient(replace(p,separations=p.separations[:-1]),g,g.record()))
    errors['stale_edit']=rejection(lambda:E.verify_quotient(p,replace(g,scope='renamed-without-transport'),g.record()))
    errors['partial_edit']=rejection(lambda:graph(2,('x','x'),((0,),)).validate())
    errors['boolean_index']=rejection(lambda:graph(2,('x','x'),((False,1),)).validate())
    identity=graph(8,g.outputs,(tuple(range(8)),),scope='identity-only')
    pi=E.build_quotient(identity);ri=E.verify_quotient(pi,identity,identity.record());ok(ri['classes']==2,'Unobservable bits were unnecessarily retained.')
    # Reverse the state ordering, including every edge, output and identity.
    perm=tuple(reversed(range(8)));inv={old:new for new,old in enumerate(perm)}
    renamed=E.Graph('transported',tuple(g.states[s] for s in perm),tuple(g.outputs[s] for s in perm),
        tuple(E.Edit(e.name,tuple(inv[e.successors[s]] for s in perm),tuple(e.observations[s] for s in perm)) for e in g.edits))
    pn=E.build_quotient(renamed);rn=E.verify_quotient(pn,renamed,renamed.record());ok(rn['classes']==r['classes'],'Full table transport failed.')
    save({'suite':'exact_output_and_two_edit_separator','graph':g.record(),'proof':p.record(),'report':r,
          'producer_work':work,'receiver_work':verify,'word':w,'identity_only':ri,'renamed':rn,'rejections':errors})

def decision_cases():
    g=graph(3,('losses:0,1','losses:0,0','losses:1,0'),((1,2,2),(0,0,1)),scope='overlap-example')
    s=E.DecisionSystem(g,('a','b'),(('a',),('a','b'),('b',)))
    work={};c=E.minimum_cover(s,work=work);p=E.minimum_cover(s,partition=True)
    ok(c['upper_bound']==2 and p['upper_bound']==3,'Relational cover must strictly beat a canonical action quotient.')
    r=E.verify_cover(c['proof'],s,s.record());E.verify_cover(p['proof'],s,s.record(),require_partition=True)
    simulate_cover(s,c['proof'],6)
    errors={}
    errors['action_switch']=rejection(lambda:E.verify_cover(replace(c['proof'],actions=('a','a')),s,s.record()))
    errors['missing_state']=rejection(lambda:E.verify_cover(replace(c['proof'],blocks=((0,1),)),s,s.record()))
    errors['wrong_update']=rejection(lambda:E.verify_cover(replace(c['proof'],successors=((0,0),(0,0))),s,s.record()))
    errors['wrong_initial']=rejection(lambda:E.verify_cover(replace(c['proof'],initial_codes=(1,0,0)),s,s.record()))
    errors['claim_partition']=rejection(lambda:E.verify_cover(c['proof'],s,s.record(),require_partition=True))
    truncated=E.minimum_cover(s,max_trials=0)
    ok(truncated['status']=='SEARCH_BUDGET_EXHAUSTED' and truncated['lower_bound']==1 and truncated['upper_bound']==3,'Search budget exhaustion claimed a minimum.')
    E.verify_cover(truncated['proof'],s,s.record())
    save({'suite':'overlap_saves_a_code','system':s.record(),'cover':c|{'proof':c['proof'].record()},
        'partition':p|{'proof':p['proof'].record()},'report':r,'producer_work':work,'rejections':errors,
        'budget_exhaustion':truncated|{'proof':truncated['proof'].record()}})
    g2=graph(3,('A1','A2','A3'),(tuple(range(3)),),scope='pairwise-is-not-joint')
    s2=E.DecisionSystem(g2,('a','b','c'),(('a','b'),('b','c'),('a','c')))
    for i,j in combinations(range(3),2):ok(bool(set(s2.acceptable[i])&set(s2.acceptable[j])),'Fixture pairs should all be compatible.')
    ok(not set.intersection(*(set(a) for a in s2.acceptable)),'Fixture joint intersection should be empty.')
    c2=E.minimum_cover(s2);ok(c2['upper_bound']==2,'Triple must not receive one code.')
    bad=E.CoverProof(s2.record(),((0,1,2),),('a',),((0,),),(0,0,0))
    rejected=rejection(lambda:E.verify_cover(bad,s2,s2.record()))
    save({'suite':'pairwise_not_joint','system':s2.record(),'minimum':c2|{'proof':c2['proof'].record()},'false_one_code_rejected':rejected})

def cost_scope():
    g=graph(2,('value:0','value:0'),((0,1),),labels=(('steps:1','steps:2'),),scope='same-answer-different-cost')
    p=E.build_quotient(g);pe=E.build_quotient(g,True)
    ok(len(p.blocks)==1 and len(pe.blocks)==2,'Output equality concealed an explicitly requested cost observation.')
    E.verify_quotient(pe,g,g.record(),preserve_edges=True)
    rej=rejection(lambda:E.verify_quotient(p,g,g.record(),preserve_edges=True))
    s=E.DecisionSystem(g,('a',),(('a',),('a',)))
    c=E.minimum_cover(s);ce=E.minimum_cover(s,preserve_edges=True)
    ok(c['upper_bound']==1 and ce['upper_bound']==2,'Decision cover did not retain requested costs.')
    E.verify_cover(ce['proof'],s,s.record(),preserve_edges=True)
    rej2=rejection(lambda:E.verify_cover(c['proof'],s,s.record(),preserve_edges=True))
    save({'suite':'cost_scope_is_part_of_request','graph':g.record(),'ordinary':p.record(),'cost_preserving':pe.record(),
        'downgrade_rejected':rej,'cover_downgrade_rejected':rej2,'decision_codes':[c['upper_bound'],ce['upper_bound']]})

def complete_small_families():
    # All 3-state, one-edit deterministic tables with every binary output vector.
    count=0
    for ts in product(range(3),repeat=3):
        for outs in product(('0','1'),repeat=3):
            g=graph(3,outs,(ts,),scope=f'all-exact-{count}')
            p=E.build_quotient(g);r=E.verify_quotient(p,g,g.record())
            reference=min(len(bs) for bs in partitions(3) if partition_oracle(g,bs))
            ok(r['classes']==reference,'Exact-output class count disagrees with full partition enumeration.')
            count+=1
    ok(count==216,'Incomplete exact corpus.')
    save({'suite':'all_three_state_one_edit_binary_output_graphs','graphs':count,'reference':'independent full set-partition enumeration'})
    # All nonempty two-action acceptability patterns, over all one-edit tables.
    subsets=(('a',),('b',),('a','b'));count=0;hist={}
    for ts in product(range(3),repeat=3):
        for aa in product(subsets,repeat=3):
            g=graph(3,('not-requested',)*3,(ts,),scope=f'all-decision-{count}')
            s=E.DecisionSystem(g,('a','b'),aa)
            c=E.minimum_cover(s);p=E.minimum_cover(s,partition=True)
            E.verify_cover(c['proof'],s,s.record());E.verify_cover(p['proof'],s,s.record(),require_partition=True)
            reference=min(len(bs) for bs in partitions(3) if partition_oracle(g,bs,aa))
            ok(p['upper_bound']==reference,'Action quotient disagrees with independent partitions.')
            ok(c['upper_bound']<=p['upper_bound'],'Cover more restrictive than partitions.')
            simulate_cover(s,c['proof'],2)
            key=f"{c['upper_bound']}/{p['upper_bound']}";hist[key]=hist.get(key,0)+1;count+=1
    ok(count==729,'Incomplete decision corpus.')
    save({'suite':'all_three_state_one_edit_two_action_systems','systems':count,'code_count_histogram':hist,
        'scope':'Finite family, complete enumeration within it; not an empirical distribution of practical tasks.'})

def premise_versions():
    K=T.K;n=3;p,q,r=(K.bit(i) for i in range(n));lib=(K.neg(p),K.neg(q),K.eq(p,q),K.neg(r));d=K.sub(p,q)
    records=[];bounds=[];ranges=[];build_work={'source_assignments_tested':0,'formula_values_requested':0}
    for mask in range(16):
        f=T.frame(n,hard=tuple(h for j,h in enumerate(lib) if mask>>j&1),d=d,scope=f'premise-mask-{mask}')
        xs=[]
        for x in product((0,1),repeat=n):
            build_work['source_assignments_tested']+=1;build_work['formula_values_requested']+=len(f.request.hard)
            if all(T.point(h,x)==1 for h in f.request.hard):xs.append(x)
        ok(bool(xs),'Expected consistent finite premise version.')
        vals=[T.point(d,x) for x in xs];build_work['formula_values_requested']+=len(vals)
        records.append(f.record());bounds.append(str(max(vals)));ranges.append(f'{min(vals)},{max(vals)}')
    edits=[]
    for j in range(4):
        for add in (False,True):
            edits.append(E.Edit(('add-' if add else 'withdraw-')+str(j),tuple((m|(1<<j)) if add else (m&~(1<<j)) for m in range(16)),('declared-unit-work',)*16))
    gu=E.Graph('current-upper-bound',tuple(records),tuple(bounds),tuple(edits));gr=replace(gu,scope='exact-range',outputs=tuple(ranges))
    u=E.build_quotient(gu);rr=E.build_quotient(gr);ru=E.verify_quotient(u,gu,gu.record());rv=E.verify_quotient(rr,gr,gr.record())
    ok(ru['classes']==4 and rv['classes']==8,'Expected task-specific irrelevance of q or r did not hold.')
    # p=0 and p=q give the same upper bound but react differently to withdrawing p=0.
    ok(bounds[1]==bounds[4]=='0','Current bound fixture differs.')
    w=E.distinguishing_word(gu,1,4);ok(w is not None,'Withdrawing evidence must expose the support difference.')
    save({'suite':'actual_finite_premise_versions','upper_graph':gu.record(),'range_graph':gr.record(),
          'upper_proof':u.record(),'range_proof':rr.record(),'upper_codes':ru['classes'],'range_codes':rv['classes'],
          'construction_work':build_work,'support_separation_word':w,'meaning':'Observable evidence versions, not hidden truth assignments supplied to the online decoder.'})

def main():
    global OUT
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();OUT=args.out;OUT.mkdir(parents=True,exist_ok=False)
    names=['05_edit_information.py','05_edit_information_check.py','05_portfolio_check.py','05_portfolio_transport.py','05_counterfactual_transport.py','04_counterfactual_repair.py'];hashes={}
    for name in names:
        b=(HERE/name).read_bytes();(OUT/name).write_bytes(b);hashes[name]=hashlib.sha256(b).hexdigest()
    manifest={'schema':'p305.edit_information.development.v1','stage':'DEVELOPMENT','version':E.VERSION,'sources_sha256':hashes,
        'prepared_utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,'platform':platform.platform(),'command':sys.argv,
        'fixed_corpora':['216 exact-output graphs','729 two-action systems','three-record overlap separator','16 actual premise versions'],
        'review':'Self-review with separate set/trace evaluation; no frozen challenge.'}
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');start=time.monotonic_ns();err=None
    try:exact_cases();decision_cases();cost_scope();complete_small_families();premise_versions()
    except Exception:err=traceback.format_exc()
    result={'cases':CASES,'assertions':COUNT,'error':err};raw=(json.dumps(result,indent=2,default=str)+'\n').encode();(OUT/'results.json').write_bytes(raw)
    summary={'status':'FAIL' if err else 'PASS','assertions':COUNT,'suites':len(CASES),'elapsed_ns':time.monotonic_ns()-start,
        'sources_sha256':hashes,'results_sha256':hashlib.sha256(raw).hexdigest(),'error':err}
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
    if err:raise SystemExit(1)
if __name__=='__main__':main()
