#!/usr/bin/env python3
"""Fresh P3-04 development evidence; independent point/set oracles, not S1 runs.
Run: python -B v3/checks/04_counterfactual_repair_check.py --output NEW_DIRECTORY
The output directory must not exist. This is a finite diagnostic, not a benchmark.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import argparse, hashlib, importlib.util, json, platform, sys, time, traceback
from datetime import datetime,timezone
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('p304_replacement',HERE/'04_counterfactual_repair.py')
k=importlib.util.module_from_spec(spec);sys.modules[spec.name]=k;spec.loader.exec_module(k)
COUNT=0;DETAILS={}
def ck(ok,msg='assertion'):
    global COUNT
    COUNT+=1
    if not ok:raise AssertionError(msg)
def throws(fn):
    try:fn()
    except (ValueError,TypeError,ZeroDivisionError):ck(True);return
    ck(False,'Expected input rejection.')
def points(n):return list(product((0,1),repeat=n))
def ev(e,x):
    """Separate exact point evaluator. Does not call interval or production Search."""
    op=e[0]
    if op=='lit':return F(e[1])
    if op=='bit':return F(x[e[1]])
    if op=='not':return F(not ev(e[1],x))
    if op=='scale':return F(e[1])*ev(e[2],x)
    a,b=ev(e[1],x),ev(e[2],x)
    if op=='and':return F(bool(a) and bool(b))
    if op=='or':return F(bool(a) or bool(b))
    if op=='eq':return F(a==b)
    if op=='add':return a+b
    if op=='min':return min(a,b)
    if op=='max':return max(a,b)
    raise ValueError(op)
def oracle(r):
    feasible=[x for x in points(r.nbits) if all(ev(h,x)==1 for h in r.hard)]
    ranks={x:tuple(sum((F(s.weight) for s in r.soft if s.tier==t and not ev(s.formula,x)),F(0)) for t in range(r.tiers)) for x in feasible}
    minimum=min(ranks.values()) if ranks else None
    return feasible,{x for x in feasible if ranks[x]==minimum},minimum

def source_expr(accepted,n):
    e=k.lit(0)
    for x in accepted:
        c=k.lit(1)
        for i,b in enumerate(x):c=k.AND(c,k.bit(i) if b else k.neg(k.bit(i)))
        e=k.OR(e,c)
    return e

def audit_search(r,seed=None):
    feasible,S,minimum=oracle(r);search=k.Search(r)
    if seed is not None:search.seed(seed)
    prefixes=0
    while True:
        report=search.report();cover=search.cover();prefixes+=1
        for x in S:ck(any(all(a is None or a==b for a,b in zip(c,x)) for c in cover),'All-optimum cover lost a case.')
        if report['feasibility']=='NONEMPTY':ck(bool(feasible))
        if report['feasibility']=='INFEASIBLE':ck(not feasible)
        if report['rank_exact']:ck(report['incumbent_rank']==minimum)
        for name,e in r.losses:
            item=report['losses'][name]
            vals={ev(e,x) for x in S}
            if vals:
                lo,hi=item['outer'];ck(all(lo<=v<=hi for v in vals),'Loss enclosure unsound.')
                if item['value_exact']:ck(len(vals)==1 and lo==next(iter(vals)))
                if item['hull_exact']:ck((lo,hi)==(min(vals),max(vals)))
                if item['image'] is not None:ck(set(item['image'])==vals)
        if report['identities_complete']:
            ck(set(report['best_witnesses'])==S);break
        ck(prefixes<=2**(r.nbits+1)+1,'Finite search did not terminate.')
        search.advance(1)
    ck(search.work['expression_nodes']>0 or not r.hard and not r.soft and not r.losses)
    return search,prefixes


def selectors():
    cases=prefixes=0;n=2;P=points(n);forms=[k.bit(0),k.neg(k.bit(0)),k.AND(k.bit(0),k.bit(1)),k.eq(k.bit(0),k.bit(1))]
    for mask in range(16):
        hard=(source_expr([p for i,p in enumerate(P) if mask>>i&1],n),)
        for a,b in product(range(4),repeat=2):
            for tier in (0,1):
                r=k.Request(n,hard,(k.Soft('a',forms[a],F(2,3),0),k.Soft('b',forms[b],F(3,2),tier)),
                    (('linear',k.sub(k.scale(3,k.bit(0)),k.bit(1))),('nonlinear',('max',k.bit(0),k.neg(k.bit(0))))),'enumerated')
                _,p=audit_search(r);prefixes+=p;cases+=1
    # All ranks 0: seeing one witness must not discard the unseen equal-rank loss 4.
    r=k.Request(1,(),(),(('loss',k.scale(4,k.bit(0))),),'ties');s=k.Search(r);s.seed((0,));rep=s.report()
    ck(rep['rank_exact'] and not rep['identities_complete']);ck(rep['losses']['loss']['outer']==(0,4));ck(not rep['losses']['loss']['value_exact'])
    # This demonstrates the exact failure of >= pruning, rather than testing only the fixed path.
    lower=(F(0),);ck(lower>=s.incumbent and not lower>s.incumbent);ck(4 in {ev(r.losses[0][1],x) for x in oracle(r)[1]})
    audit_search(r,(0,))
    # A worse incumbent cannot refute an eventual universal support.
    r=k.Request(1,(),(k.Soft('prefer',k.bit(0)),),(('constant',k.lit(7)),),'early');s=k.Search(r);s.seed((0,))
    ck(s.report()['losses']['constant']['value_exact']);ck(not s.report()['rank_exact'])
    ck(s.support_report(k.bit(0),k.neg(k.bit(0)))['positive']=='UNRESOLVED')
    s.advance(100);ck(s.support_report(k.bit(0),k.neg(k.bit(0)))=={'positive':'YES','negative':'NO'})
    # Shared loss difference can be settled without absolute levels.
    r=k.Request(1,(),(),(('A',k.scale(10,k.bit(0))),('B',k.add(k.scale(10,k.bit(0)),k.lit(1))),('A-B',k.lit(-1))),'common-action')
    s=k.Search(r);s.seed((0,));rep=s.report();ck(rep['losses']['A-B']['value_exact']);ck(not rep['losses']['A']['value_exact'])
    # Scope change is a new query; stale mutable request replacement is rejected.
    s.request=k.Request(1,(k.bit(0),),(),r.losses,'changed');throws(s.report)
    DETAILS['selectors']={'requests':cases,'prefixes':prefixes,'ties_retained':True,'ordinary_comparator':'separate full enumeration over same cases, no performance claim'}


def intervals_and_validation():
    b=[k.bit(0),k.bit(1),k.lit(0),k.lit(1)];expressions=b+[k.neg(x) for x in b]
    for x,y in product(b,repeat=2):expressions += [k.AND(x,y),k.OR(x,y),k.eq(x,y),k.add(x,k.scale(-3,y)),('min',x,y),('max',x,y)]
    for e in expressions:
        for c in product((None,0,1),repeat=2):
            lo,hi=k.interval(e,c)
            for x in points(2):
                if all(v is None or v==a for v,a in zip(c,x)):ck(lo<=ev(e,x)<=hi)
    bad=[lambda:k.Request(13,(),(),(),'cap'),lambda:k.Request(1,(k.lit(2),),(),(),'hard'),
         lambda:k.Request(1,(),(k.Soft('z',k.bit(0),F(0)),),(),'zero'),
         lambda:k.Request(1,(),(k.Soft('z',k.bit(0)),k.Soft('z',k.bit(0))),(),'duplicate'),
         lambda:k.Request(1,(),(),(('a',k.bit(1)),),'index'),lambda:k.rational(0.5),lambda:k.rational(True),lambda:k.rational('1/0'),
         lambda:k.rational(1<<129),lambda:k.Search(k.Request(1,(),(),(),'x')).advance(-1),
         lambda:k.Search(k.Request(1,(),(),(),'x')).seed((True,))]
    for fn in bad:throws(fn)
    # Huge shared quoted tree gets rejected before exponential expansion.
    huge=('atom','p')
    for _ in range(20):huge=('and',huge,huge)
    throws(lambda:k.paired(huge,('p',)))
    DETAILS['intervals']={'expressions':len(expressions),'partial_cells_each':9,'input_rejections':len(bad)+1}


def supports():
    atoms=('p','q');p=('atom','p');q=('atom','q')
    basic=[p,q,('not',p),('top',),('bottom',)]
    forms=basic+[('not',a) for a in basic]+[(op,a,b) for op in ('and','or') for a,b in product(basic,repeat=2)]
    def four(e,state):
        if e[0]=='atom':
            i=atoms.index(e[1]);return ({1} if state[2*i] else set())|({0} if state[2*i+1] else set())
        if e==('top',):return {1}
        if e==('bottom',):return {0}
        if e[0]=='not':return {1-v for v in four(e[1],state)}
        a,b=four(e[1],state),four(e[2],state)
        if e[0]=='and':return ({1} if 1 in a and 1 in b else set())|({0} if 0 in a or 0 in b else set())
        return ({1} if 1 in a or 1 in b else set())|({0} if 0 in a and 0 in b else set())
    for f in forms:
        t,n=k.paired(f,atoms)
        for x in points(4):
            v=four(f,x);ck(ev(t,x)==int(1 in v));ck(ev(n,x)==int(0 in v))
            if all(x[2*i]+x[2*i+1]==1 for i in range(2)):ck(ev(t,x)+ev(n,x)==1)
    theta=('and',p,('not',p));losses=(('continue',k.scale(4,k.bit(2))),('fallback',k.lit(1)))
    req=k.paired_request(atoms,theta,(0,0),('p',),('q',),losses=losses)
    s,_=audit_search(req);ck(s.best=={(1,1,0,1)})
    ck(s.support_report(*k.paired(p,atoms))=={'positive':'YES','negative':'YES'})
    ck(s.support_report(*k.paired(q,atoms))=={'positive':'NO','negative':'YES'})
    s,_=audit_search(k.paired_request(atoms,theta,(0,0),('p',),losses=losses));ck(s.report()['losses']['continue']['image']==[0,4])
    s,_=audit_search(k.paired_request(atoms,theta,(0,0),(),losses=losses));ck(s.report()['feasibility']=='INFEASIBLE')
    s,_=audit_search(k.paired_request(atoms,('bottom',),(0,0),atoms));ck(s.report()['feasibility']=='INFEASIBLE')
    # Normality-first overlap and centering; no scalar big-M claim.
    for f in forms:
        r=k.paired_request(atoms,f,(0,0),atoms,preserve_baseline=True)
        S=oracle(r)[1]
        normal=[x for x in points(4) if x[0]+x[1]==x[2]+x[3]==1 and ev(r.hard[0],x)]
        if normal:ck(all(x[0]+x[1]==x[2]+x[3]==1 for x in S))
        if ev(r.hard[0],(0,1,0,1)):ck(S=={(0,1,0,1)})
        if S:ck(all(x[0]+x[1]>=1 and x[2]+x[3]>=1 for x in S),'Gap-free theorem.')
    # Material modus ponens is not a signed inference rule.
    x=(1,1,0,1);ck(1 in four(p,x) and 1 in four(('or',('not',p),q),x) and 1 not in four(q,x))
    ck(ev(k.bit(0),(1,1))!=ev(k.sub(k.lit(1),k.bit(1)),(1,1)))
    DETAILS['supports']={'formulas':len(forms),'states_each':16,'GC01_selected':[1,1,0,1],'unframed_continue_image':['0','4'],'unsupported_bottom':'INFEASIBLE'}


def horn():
    policies=[(),(((0,),2),),(((0,),2),((2,),0)),(((),0),),(((1,2),3),)]
    count=0
    for ref in points(2):
        initial={2*i if b else 2*i+1 for i,b in enumerate(ref)}
        for seedmask in range(16):
            seed=tuple(i for i in range(4) if seedmask>>i&1)
            for permission in range(4):
                allowed=tuple(i for i in range(2) if permission>>i&1)
                for rules in policies:
                    ans=k.horn_closure(ref,seed,rules,allowed)
                    states=[]
                    for x in points(4):
                        S={i for i,v in enumerate(x) if v}
                        if not initial|set(seed)<=S:continue
                        if any(not(sum(x[2*i:2*i+2])==1) for i in range(2) if i not in allowed):continue
                        if any(set(b)<=S and h not in S for b,h in rules):continue
                        states.append(x)
                    if not states:ck(ans['status']=='INFEASIBLE')
                    else:
                        r=lambda x:sum(x[2*i] and x[2*i+1] for i in allowed)
                        m=min(map(r,states));selected={x for x in states if r(x)==m}
                        ck(ans['status']=='NONEMPTY_UNIQUE_MINIMUM' and selected=={ans['bits']})
                        ck(ans['passes']<=5)
                    count+=1
    add_only=k.horn_closure((0,0,0),(0,),(((0,),2),),(0,1));ck(add_only['bits']==(1,1,1,1,0,1))
    cancel=k.horn_closure((0,0,0),(0,),(((0,),2),((0,),4)),(0,1));ck(cancel['status']=='INFEASIBLE')
    all_allowed=k.horn_closure((0,0,0),(0,),(((0,),2),((0,),4)),(0,1,2));ck(all_allowed['bits']==(1,1,1,1,1,1))
    DETAILS['horn']={'cases':count,'arithmetic_quotations':['2=3','4=6','0=1'],'add_only':add_only,'cancellation_without_permission':cancel,'cancellation_permitted':all_allowed}


def graphs():
    ident=(((0,),0),((1,),1));A=k.Equation('A',(0,1),('U',),ident)
    D=(A,k.Equation('B',(0,1),('A',),ident));C=(A,k.Equation('B',(0,1),('U',),ident))
    for u in (0,1):ck(k.structural(D,{'U':u})==k.structural(C,{'U':u}))
    x=k.structural(D,{'U':0},{'A':1});y=k.structural(C,{'U':0},{'A':1});ck(2+x['A']-2*x['B']==1);ck(2+y['A']-2*y['B']==3)
    original=(0,0,1);replacement=(1,0,1)
    actor=k.route_replacement(original,replacement,0,(('A',True),('B',False),('predict_original',False)))
    shared=k.route_replacement(original,replacement,0,(('A',True),('B',True),('predict_original',False)))
    ck(actor['outputs']=={'A':1,'B':0,'predict_original':0});ck(shared['outputs']=={'A':1,'B':1,'predict_original':0})
    ck(actor['hamming_distance']==1 and shared['hamming_distance']==1)
    throws(lambda:k.structural((k.Equation('A',(0,1),('A',),ident),),{}))
    throws(lambda:k.structural((k.Equation('A',(0,1),('U',),()),),{'U':0}))
    throws(lambda:k.route_replacement(original,original,0,(('A',True),)))
    ck(not [x for x in points(3) if x[0]==0 and x[1]==x[0] and x[2]==x[0] and x[1]==1])
    DETAILS['graphs']={'conditioned_family':'empty','direct_intervention_loss':1,'common_cause_intervention_loss':3,'actor':actor,'shared':shared}


def encodings_and_repairs():
    b0,b1=k.bit(0),k.bit(1)
    formulas=[b0,k.neg(b0),k.AND(b0,b1),k.OR(b0,b1),k.eq(b0,b1),k.lit(0),k.lit(1)]
    for f in formulas:
        r=k.Request(2,(),(k.Soft('s',f,F(3,2),0),k.Soft('t',k.neg(b0),F(2,3),1)),(),'cnf')
        c=k.compile_cnf(r);w=k.scalar_weights(r)
        ranks=[];scalars=[]
        for x in points(2):
            ext=[]
            for tail in points(c['variables']-2):
                full=x+tail
                if all(any(bool(full[abs(v)-1])==(v>0) for v in clause) for clause in c['hard_clauses']):ext.append(full)
            ck(len(ext)==1,'Unique CNF extension.')
            full=ext[0]
            for s,row in zip(r.soft,c['soft_roots']):ck(full[row['root']-1]==ev(s.formula,x))
            ranks.append(tuple(sum((F(s.weight)*(1-ev(s.formula,x)) for s in r.soft if s.tier==t),F(0)) for t in range(2)))
            scalars.append(sum(wi*(1-ev(s.formula,x)) for wi,s in zip(w,r.soft)))
        for i,j in product(range(4),repeat=2):ck((ranks[i]<ranks[j])==(scalars[i]<scalars[j]));ck((ranks[i]==ranks[j])==(scalars[i]==scalars[j]))
    r=k.Request(2,(k.eq(b0,b1),),(k.Soft('both',k.AND(b0,b1),F(3)),k.Soft('notp',k.neg(b0),F(4))),(),'grouped')
    ck(oracle(r)[1]=={(0,0)})
    bad=k.Request(2,r.hard,(k.Soft('p',b0,F(3)),k.Soft('q',b1,F(3)),r.soft[1]),(),'split');ck(oracle(bad)[1]=={(1,1)})
    # Direct deletion-pair enumeration for original (positive) weights.
    Fset,S,m=oracle(r);repairs=[]
    for x in Fset:
        for mask in range(4):
            R={j for j in range(2) if mask>>j&1}
            if all(ev(s.formula,x) or j in R for j,s in enumerate(r.soft)):
                repairs.append((sum((s.weight for j,s in enumerate(r.soft) if j in R),F(0)),R,x))
    opt=min(p for p,_,_ in repairs);ck({x for p,_,x in repairs if p==opt}==S)
    for p,R,x in repairs:
        if p==opt:ck(R=={i for i,s in enumerate(r.soft) if not ev(s.formula,x)})
    # CE04-1 all minimal Boolean violation sets attainable by the constructive weights.
    profiles=points(3)
    for mask in range(1,256):
        B=[p for i,p in enumerate(profiles) if mask>>i&1]
        for p in B:
            minimal=not any(q!=p and all(a<=b for a,b in zip(q,p)) for q in B)
            w=[F(1,4) if b else F(1) for b in p]
            val=lambda x:sum(a*b for a,b in zip(w,x))
            ck((val(p)==min(map(val,B)))==minimal)
    DETAILS['encoding']={'gate_formulas':len(formulas),'objective_reversal_observed':True,'boolean_profile_families':255}


def policy_and_extension_checks():
    lines=((F(1),F(0)),(F(-1),F(1)));regions=k.line_regions(lines,(F(1,4),F(3,4)))
    ck(regions==[(F(1,4),F(1,2)),(F(1,2),F(3,4))]);ck(k.envelope_gap((0,F(3,5)),lines,(0,1))==F(1,10));ck(k.envelope_gap((0,F(1,2)),lines,(0,1))==0)
    # Exhaust independent bounded interval boxes; endpoint choices suffice for individual attainability.
    intervals=[(F(a),F(b)) for a in (-1,0,1) for b in (0,1,2) if a<=b]
    count=0
    for bounds in product(intervals,repeat=3):
        ans=k.independent_rank_box(bounds);possible=set()
        for r in product(*[(a,b) for a,b in bounds]):
            possible|={i for i,v in enumerate(r) if v==min(r)}
        ck(possible==set(ans['possible_winners']))
        witness=ans['simultaneous_witness'];ck(all(a<=r<=b for (a,b),r in zip(bounds,witness)))
        ck({i for i,r in enumerate(witness) if r==min(witness)}==possible);count+=1
    # Correlated ranks and coupled selected payoffs cannot be replaced by independent boxes.
    ck(k.line_regions(((0,0),(1,0),(-1,1)),(0,1))==[(0,1),(0,0),(1,1)])
    ck(k.independent_rank_box(((0,0),(0,10)))['selected_rank_range']==(0,0))
    # CE04-6 sourcewise and joint selection, plus CE04-12 failed old-minimum survival.
    source_rows={0:[('x',0,0)],1:[('y',1,10)]}
    source_values={loss for rows in source_rows.values() for _,rank,loss in rows if rank==min(r for _,r,_ in rows)}
    joint=[x for rows in source_rows.values() for x in rows];jm=min(r for _,r,_ in joint)
    ck(source_values=={0,10} and {l for _,r,l in joint if r==jm}=={0})
    Frows=[('x',0,0),('y',1,10)];ck(min(Frows,key=lambda x:x[1])[2]==0 and min(Frows[1:],key=lambda x:x[1])[2]==10)
    # Rank-sensitive projection: u=1 makes x=1 optimal, despite a local x=0 preference.
    costs={(x,u):int(x!=0)+2*int(x!=u) for x,u in points(2) if u==1}
    ck(min(costs,key=costs.get)==(1,1))
    # Finite tests of term and source graph; not a proof of the unbounded Lipschitz obstruction.
    samples=0
    for lo in (-3,-1,0):
        for hi in (0,1,4):
            for z in range(9):
                w=F(lo)+F(z,8)*(hi-lo)
                for b in (0,1):
                    term=k.gate_term(lo,hi,k.lit(w),k.bit(0));ck(ev(term,(b,))==w*b);samples+=1
    rows=k.gate_source()
    def satisfies(row,x):return all(sum(F(a)*b for a,b in zip(A,x))<=rhs for A,rhs in zip(row['A'],row['b']))
    for row in rows:ck(satisfies(row,row['witness']))
    for w in (F(-10**9),F(-2,3),F(0),F(5,7),F(10**9)):
        for b in (0,1):
            for g in (F(-1),F(0),w,w+1):ck(any(satisfies(row,(w,b,g)) for row in rows)==(g==w*b))
    # Uniform fixed scalarization fails although every fixed rational request can be scalarized.
    for M in (1,2,10,10000):
        d=F(1,2*M);ck((1+d,0)>(1,1));ck(M*(1+d)<M+1)
    DETAILS['extensions']={'independent_rank_boxes':count,'bounded_gate_points':samples,'unbounded_graph_extreme_weights':True,'sourcewise_loss_image':[0,10],'joint_loss_image':[0]}


def consequence_laws():
    # Fixed rank/universe; set oracles, rather than new learned/relevance claims.
    atoms=('p','q');p=('atom','p');q=('atom','q')
    forms=[p,('not',p),q,('not',q),('and',p,('not',p)),('or',p,q),('and',p,q)]
    universe=points(4);gapfree=[x for x in universe if x[0]+x[1] and x[2]+x[3]]
    def rank(x):return int(x[0]==x[1])+int(x[2]==x[3])
    ts={repr(f):k.paired(f,atoms) for f in forms}
    def selected(f):
        cases=[x for x in gapfree if ev(ts[repr(f)][0],x)]
        return [] if not cases else [x for x in cases if rank(x)==min(map(rank,cases))]
    comparisons=0
    for A,B,C in product(forms,repeat=3):
        SA=selected(A)
        if not SA:continue
        at,af=ts[repr(B)];ct,cf=ts[repr(C)]
        if all(ev(at,x) for x in SA):
            full=[x for x in gapfree if ev(ts[repr(A)][0],x) and ev(at,x)]
            ck(set(SA)=={x for x in full if rank(x)==min(map(rank,full))})
        if all(ev(ct,x) for x in SA) and not all(ev(af,x) for x in SA):
            full=[x for x in gapfree if ev(ts[repr(A)][0],x) and ev(at,x)]
            ck(bool(full));ck(all(ev(ct,x) for x in full if rank(x)==min(map(rank,full))))
        comparisons+=1
    # Two stated ranked states witness failure without the gap premise.
    old={'A':(1,0),'B':(0,0),'C':(1,0)};new={'A':(1,0),'B':(1,0),'C':(0,1)}
    ck(old['A'][0] and old['C'][0] and not old['B'][1]);ck(new['A'][0] and new['B'][0] and not new['C'][0])
    DETAILS['consequence']={'formula_triples':comparisons,'gap_countermodel':True}


def run(out:Path):
    out.mkdir(parents=True,exist_ok=False)
    inputs=[HERE/'04_counterfactual_repair.py',Path(__file__).resolve()]
    manifest={'kind':'DEVELOPMENT_RECONSTRUCTION','version':k.VERSION,'python':sys.version,'platform':platform.platform(),
              'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
              'command':['python','-B','v3/checks/04_counterfactual_repair_check.py','--output',str(out)],
              'started_utc':datetime.now(timezone.utc).isoformat(),'historical_S1_evidence_recovered':False}
    for p in inputs:(out/p.name).write_bytes(p.read_bytes())
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    start=time.monotonic_ns();results=[];status='PASS';error=None
    try:
        for fn in (selectors,intervals_and_validation,supports,horn,graphs,encodings_and_repairs,policy_and_extension_checks,consequence_laws):
            before=COUNT;beg=time.monotonic_ns();fn()
            row={'suite':fn.__name__,'assertions':COUNT-before,'elapsed_ns':time.monotonic_ns()-beg,'status':'PASS'};results.append(row)
            with (out/'progress.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
    except Exception:
        status='FAIL';error=traceback.format_exc();print(error,file=sys.stderr)
    summary={'status':status,'label':'DEVELOPMENT','assertions':COUNT,'suites':results,'elapsed_ns':time.monotonic_ns()-start,
             'ended_utc':datetime.now(timezone.utc).isoformat(),'details':DETAILS,'error':error}
    (out/'summary.json').write_text(json.dumps(summary,indent=2,default=str)+'\n')
    print(json.dumps({'status':status,'suites':len(results),'assertions':COUNT,'output':str(out)}))
    if status!='PASS':raise SystemExit(1)
if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True);run(ap.parse_args().output)
