"""Ordinary shared-cost Pareto proposals; Codex (GPT-6), DEVELOPMENT."""
from itertools import product
from pathlib import Path
import copy
import json
import random
import sys
import shared_frontier as sf

g01=sf.g01;Meter=sf.Meter;HERE=Path(__file__).resolve().parent

def validate(group):
    lo,hi=group['interval'];w=group['weights'];c=group['centers']
    if (type(lo)is not int or type(hi)is not int or not 0<=lo<=hi
        or not w or len(w)!=len(c) or any(type(v)is not int or v<=0 for v in w)
        or any(type(v)is not int or not lo<=v<=hi for v in c)):
        raise ValueError('Integral interval, positive weights and internal observed centers required')
    return lo,hi,w,c

def nondominated(points,meter):
    best={}
    for r,u,witness in points:
        candidate=(u,witness)
        if r not in best or candidate<best[r]:best[r]=candidate
        meter.pay('planning','pareto_point_comparison',5+len(witness))
    result=[];last=None
    for r,(u,witness) in sorted(best.items()):
        if last is None or u<last:result.append((r,u,witness));last=u
        meter.pay('planning','pareto_sorted_scan',4)
    meter.pay('planning','pareto_sort_upper_comparisons',len(best)*max(1,len(best).bit_length()))
    return result

def local(group,meter):
    lo,hi,weights,centers=validate(group);table={0:(0,())};rows=[[[0,0,[]]]]
    for w,c in zip(weights,centers):
        a,b=w*(c-lo),w*(hi-c);nxt={}
        for x,(y,count) in table.items():
            for k in(0,1,2):
                xx=x+k*a;candidate=(y+(2-k)*b,count+(k,))
                if xx not in nxt or candidate<nxt[xx]:nxt[xx]=candidate
                meter.pay('planning','local_frontier_transition',10+len(count))
        table=nxt;rows.append([[x,y,list(count)] for x,(y,count) in sorted(table.items())])
    base=2*sum(w*c for w,c in zip(weights,centers))
    frontier=nondominated([(max(x,y),base+y,count) for x,(y,count) in table.items()],meter)
    return dict(source=g01.kernel.digest(group),rows=rows,frontier=frontier)

def check_local(group,certificate,meter):
    lo,hi,weights,centers=validate(group)
    if certificate['source']!=g01.kernel.digest(group) or len(certificate['rows'])!=len(weights)+1:
        raise ValueError('Changed group or incomplete recurrence')
    previous={0:(0,())}
    if certificate['rows'][0]!=[[0,0,[]]]:raise ValueError('Bad base case')
    states=transitions=0
    for index,(w,c) in enumerate(zip(weights,centers)):
        expected={}
        for x,(y,witness) in previous.items():
            for k in range(3):
                left=x+k*w*(c-lo);right=y+(2-k)*w*(hi-c);action=witness+(k,)
                if left not in expected or (right,action)<expected[left]:expected[left]=(right,action)
                transitions+=1;meter.pay('dp_check','exact_transition_and_argmin',12+len(action))
        rows=certificate['rows'][index+1]
        actual={x:(y,tuple(action)) for x,y,action in rows}
        if len(actual)!=len(rows) or actual!=expected:raise ValueError('Incomplete or incorrect DP row')
        previous=actual;states+=len(rows)
    base=2*sum(w*c for w,c in zip(weights,centers))
    points=[(max(x,y),base+y,count) for x,(y,count) in previous.items()]
    # Independent dominance characterization, avoiding producer's sorted scan.
    representatives={}
    for r,u,action in points:
        if (r,u) not in representatives or action<representatives[r,u]:representatives[r,u]=action
    expected=[]
    for (r,u),action in representatives.items():
        dominated=False
        for rr,uu in representatives:
            meter.pay('dp_check','pairwise_dominance_comparison',5)
            if rr<=r and uu<=u and (rr<r or uu<u):dominated=True;break
        if not dominated:expected.append((r,u,action))
    actual=[(r,u,tuple(a)) for r,u,a in certificate['frontier']]
    if sorted(expected)!=actual:raise ValueError('Wrong frontier')
    for r,u,count in actual:
        if sf.group_metrics(group,count)[:2]!=(r,u):raise ValueError('Bad endpoint witness')
        meter.pay('dp_check','independent_returned_endpoint_bound',12*len(count))
    return dict(states=states,transitions=transitions,frontier_size=len(actual))

def combine(groups,certificates,meter):
    table={0:(0,())};rows=[[[0,0,[]]]]
    for certificate in certificates:
        nxt={}
        for r,(u,counts) in table.items():
            for rr,uu,count in certificate['frontier']:
                R=r+rr;candidate=(u+uu,counts+(tuple(count),))
                if R not in nxt or candidate<nxt[R]:nxt[R]=candidate
                meter.pay('planning','global_menu_convolution',8+sum(map(len,candidate[1])))
        table={r:(u,counts) for r,u,counts in nondominated([(r,u,c) for r,(u,c) in nxt.items()],meter)}
        rows.append([[r,u,[list(x) for x in counts]] for r,(u,counts) in sorted(table.items())])
    return dict(source=g01.kernel.digest(groups),rows=rows,frontier=[(r,u,counts) for r,(u,counts) in sorted(table.items())])

def exhaustive(group):
    return [(*sf.group_metrics(group,count)[:2],count) for count in product((0,1,2),repeat=len(group['weights']))]

def compare_menu(frontier,points):
    targets=0
    for tau in range(max(p[0] for p in points)+1):
        expect=min((u for r,u,_ in points if r<=tau),default=None)
        actual=min((u for r,u,_ in frontier if r<=tau),default=None)
        if actual!=expect:raise AssertionError((tau,actual,expect))
        targets+=1
    return targets

def nominal(group):
    lo,hi,w,c=validate(group);values=sorted(set([lo,hi,*c]));menu=set()
    for z in values:
        options=[(0,) if z<x else (2,) if z>x else (0,1,2) for x in c]
        menu.update(product(*options))
    # Between consecutive thresholds the strict choice already occurs at an endpoint.
    return [(*sf.group_metrics(group,count)[:2],count) for count in sorted(menu)]

def run(directory):
    directory.mkdir(exist_ok=False);(directory/'impl.py').write_bytes(Path(__file__).read_bytes())
    (directory/'declaration.md').write_bytes((HERE/'nominal_bank.md').read_bytes())
    groups=json.loads((HERE/'sf02/design.json').read_text())['groups']
    boundary=dict(name='nominal_boundary',interval=[0,5],weights=[5,2],centers=[2,3]);groups.append(boundary)
    rng=random.Random(8141640)
    for j in range(12):
        degree=6+j%7;lo=rng.randrange(4);hi=rng.randrange(lo+2,12)
        groups.append(dict(name=f'large{j}',interval=[lo,hi],weights=[rng.randrange(1,10) for _ in range(degree)],centers=[rng.randrange(lo,hi+1) for _ in range(degree)]))
    pairs=[(j,j+1) for j in range(12) if len(groups[j]['weights'])<=3 and len(groups[j+1]['weights'])<=3]
    small=[i for i,g in enumerate(groups) if len(g['weights'])<=3]
    pairs=[(small[j%len(small)],small[(j*3+1)%len(small)]) for j in range(12)]
    g01.save(directory/'design.json',dict(groups=groups,pairs=pairs,seed=8141640,source_sha256=g01.sha(__file__),physical_audits=0,stage='DEVELOPMENT'))
    results=[];certificates=[]
    for group in groups:
        meter=Meter();certificate=local(group,meter);check_meter=Meter();checked=check_local(group,certificate,check_meter)
        points=exhaustive(group) if len(group['weights'])<=7 else None
        target_checks=compare_menu(certificate['frontier'],points) if points else 0
        bank=nominal(group);robust=min(r for r,u,k in certificate['frontier']);bank_R=min(r for r,u,k in bank)
        negatives=0
        for variant in('source','row','bound'):
            bad=copy.deepcopy(certificate)
            if variant=='source':bad['source']='0'*64
            elif variant=='row':bad['rows'][-1]=bad['rows'][-1][1:]
            else:
                bad['frontier']=[list(p) for p in bad['frontier']];bad['frontier'][0][0]-=1
            try:check_local(group,bad,Meter())
            except ValueError:negatives+=1
            else:raise AssertionError('Bad certificate accepted')
        record=dict(group=group,certificate=certificate,checked=checked,action_checks=len(points or []),target_checks=target_checks,nominal_actions=len(bank),nominal_regret=bank_R,robust_regret=robust,strict=robust<bank_R,negative_checks=negatives,invoice=meter.record(),checking_invoice=check_meter.record())
        g01.save(directory/f"{group['name']}.json",record);results.append({k:v for k,v in record.items() if k not in('certificate','invoice','checking_invoice')});certificates.append(certificate)
        print(group['name'],robust,bank_R,checked['states'],flush=True)
    combined=[]
    for index,(i,j) in enumerate(pairs):
        two=[groups[i],groups[j]];meter=Meter();certificate=combine(two,[certificates[i],certificates[j]],meter)
        a,b=exhaustive(two[0]),exhaustive(two[1]);points=[(r+s,u+v,(x,y)) for r,u,x in a for s,v,y in b]
        checked=compare_menu(certificate['frontier'],points)
        # Each global witness is reconstructed independently from local endpoint metrics.
        for R,U,counts in certificate['frontier']:
            metrics=[sf.group_metrics(g,k) for g,k in zip(two,counts)]
            assert R==sum(x[0] for x in metrics) and U==sum(x[1] for x in metrics)
        row=dict(groups=[i,j],certificate=certificate,action_products=len(points),target_checks=checked,invoice=meter.record())
        g01.save(directory/f'pair{index}.json',row);combined.append({k:v for k,v in row.items() if k not in('certificate','invoice')})
    b=results[20];assert b['robust_regret']==19 and b['nominal_regret']==20
    g01.save(directory/'results.json',dict(status='complete',groups=results,pairs=combined,physical_audits=0))

if __name__=='__main__':run(Path(sys.argv[1]))
