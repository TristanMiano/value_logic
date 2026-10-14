"""Paid original-source replacement-aware witness frontiers. Codex (GPT-6)."""
from itertools import product
from pathlib import Path
import json
import random
import sys
import time
import replacement_frontier as rf
import action_audits as aa
import g01
Meter=g01.kernel.Meter;HERE=Path(__file__).resolve().parent

def source(weights,fees,H):
    n=len(weights);data=aa.original([[0,i+1,w] for i,w in enumerate(weights)],fees)
    data.pop('identity');h=data['variables']+1;data['variables']=h
    data['hard'] += [[1,h],[-1,h]];data['features'].append(dict(clause=[-h],node=n+1,scale=1))
    data['bit_source']='all supported cost vectors; common mandatory anchor';data['supports']=[[0,1,2]]*(n+1)+[[0,H]]
    data['weights']=weights;return g01.seal(data)

def acquire_geometry(data):
    meter=Meter();j=len(data['hard'])-2;a=set(data['hard'][j]);b=set(data['hard'][j+1]);h=data['variables']
    if 1 not in a or -1 not in b:raise ValueError('Unavailable proposed resolution')
    derived=sorted((a-{1})|(b-{-1}));meter.pay('geometry_acquisition','read_parents_and_emit_exact_resolvent',7+len(a)+len(b))
    receipt=g01.seal(dict(source=data['identity'],parents=[j,j+1],pivot=1,derived=derived,mandatory_variable=h))
    return dict(receipt=receipt,invoice=meter.record(),physical_resolution_steps=1)

def admit(data,geometry,meter):
    if not data['weights'] or any(type(w)is not int or w<=0 for w in data['weights']):raise ValueError('Positive integral edge weights required')
    if len(data['audit_costs'])!=len(data['weights'])+2 or any(type(c)is not int or c<=0 for c in data['audit_costs']):raise ValueError('Positive audit fees required')
    if data!=source(data['weights'],data['audit_costs'],data['supports'][-1][-1]):raise ValueError('Malformed original source')
    r=geometry['receipt']
    if r['identity']!=g01.kernel.digest({k:v for k,v in r.items() if k!='identity'}) or r['source']!=data['identity']:raise ValueError('Unbound geometry')
    left,right=r['parents'];pivot=r['pivot']
    if any(type(j)is not int or not 0<=j<len(data['hard']) for j in(left,right)) or type(pivot)is not int or pivot<=0:raise ValueError('Invalid proof parent or pivot')
    a=data['hard'][left];b=data['hard'][right]
    if pivot not in a or -pivot not in b:raise ValueError('Resolution pivot missing')
    exact=sorted(set(x for x in a if x!=pivot)|set(x for x in b if x!=-pivot))
    if exact!=r['derived'] or exact!=[data['variables']] or r['mandatory_variable']!=data['variables']:raise ValueError('Mandatory unit unproved')
    meter.pay('source','original_clauses_ordered_features_supports_and_fees',20+sum(1+len(c) for c in data['hard'])+5*len(data['features'])+sum(map(len,data['supports'])))
    meter.pay('geometry_check','independent_resolution_and_mandatory_feature_binding',20+len(a)+len(b))

def options(data,known,i):return [known[i]] if i in known else data['supports'][i]

def bounds(data,known,count,meter):
    n=len(data['weights']);R=U=0;L=None
    for center in options(data,known,0):
        rr=uu=ll=0
        for i,(w,k) in enumerate(zip(data['weights'],count),1):
            values=options(data,known,i)
            rr+=w*max(k*center+(2-k)*v-2*min(center,v) for v in values)
            uu+=w*max(k*center+(2-k)*v for v in values)
            ll+=2*w*min(min(center,v) for v in values)
            meter.pay('bounds','conditional_center_leaf_regret_upper_optimum_lower',18*len(values))
        R=max(R,rr);U=max(U,uu);L=ll if L is None else min(L,ll)
    anchor=options(data,known,n+1)
    return R,U+max(anchor),L+min(anchor)

def choose(data,known,price,tau,arm,meter):
    n=len(data['weights']);center=known.get(0);leaf_known={i-1:v for i,v in known.items() if 1<=i<=n}
    if center is None:count=[1]*n
    elif center==0:count=[2]*n
    elif center==2:count=[0]*n
    elif arm in('frontier','ordinary_frontier'):
        proposal=rf.propose(data['weights'],leaf_known,tau,meter)
        count=proposal['count'] if proposal else [((2 if leaf_known[i]>=1 else 0) if i in leaf_known else 1) for i in range(n)]
    else:count=[((2 if leaf_known[i]>=1 else 0) if i in leaf_known else 1) for i in range(n)]
    R,U,L=bounds(data,known,count,meter);replace=max(0,price-L);repair=max(R,U-price)
    meter.pay('selection','replacement_and_repair_full_duty',8)
    if replace<=tau and replace<=repair:return dict(kind='replace',bound=replace,count=None,R=R,U=U,L=L)
    if repair<=tau:return dict(kind='repair',bound=repair,count=count,R=R,U=U,L=L)
    if replace<=tau:return dict(kind='replace',bound=replace,count=None,R=R,U=U,L=L)
    return dict(kind='audit',R=R,U=U,L=L,count=count)

def model(data,count):
    mask=1<<(data['variables']-1)
    for i,k in enumerate(count):
        for j in range(2):mask|=1<<(4*i+2*j+(0 if j<k else 1))
    return mask

def check(data,geometry,receipts,request,price,tau,decision,meter):
    if geometry['receipt']['source']!=data['identity']:raise ValueError('Wrong admitted geometry')
    known={}
    for r in receipts:
        if r['identity']!=g01.kernel.digest({k:v for k,v in r.items() if k!='identity'}):raise ValueError('Changed receipt')
        i=r['coordinate']
        if r['source']!=data['identity'] or r['request']!=request or i in known or r['sequence']!=len(known) or type(i)is not int or not 0<=i<len(data['supports']):raise ValueError('Receipt scope')
        if type(r['value'])is not int or r['value'] not in data['supports'][i] or r['fee']!=data['audit_costs'][i]:raise ValueError('Receipt value or fee')
        known[i]=r['value'];meter.pay('receipt_check','source_request_coordinate_support_fee',18)
    if decision['kind']=='replace':
        _,_,low=bounds(data,known,[1]*len(data['weights']),meter);bound=max(0,price-low)
    elif decision['kind']=='repair':
        mask=decision['model'];count=[]
        for clause in data['hard']:
            if not any(bool(mask>>(abs(l)-1)&1)==(l>0) for l in clause):raise ValueError('Original action infeasible')
            meter.pay('action_check','original_hard_clause',1+len(clause))
        for i in range(len(data['weights'])):count.append(int(bool(mask>>(4*i)&1))+int(bool(mask>>(4*i+2)&1)))
        if count!=decision['count']:raise ValueError('Action encoding')
        R,U,L=bounds(data,known,count,meter);bound=max(R,U-price)
    else:raise ValueError('No completed action')
    if bound!=decision['bound'] or bound>tau:raise ValueError('Unwarranted combined regret')
    return known

class Provider:
    def __init__(self,data,row,request,trace,meter):self.data=data;self._row=row;self.request=request;self.trace=trace;self.meter=meter;self.seen=set()
    def audit(self,i):
        if i in self.seen or not 0<=i<len(self._row):raise ValueError('Repeated/invalid query')
        r=g01.seal(dict(source=self.data['identity'],request=self.request,coordinate=i,value=self._row[i],fee=self.data['audit_costs'][i],sequence=len(self.seen)))
        self.seen.add(i);self.trace.write(json.dumps(dict(kind='audit',receipt=r))+'\n');self.trace.flush();self.meter.pay('provider','physical_cost_receipt_export',13);return r

def rows(case):
    rng=random.Random(case['seed']);n=len(case['weights']);H=case['H'];answer=[]
    for t in range(32):answer.append([1 if t<16 else rng.randrange(3)]+[rng.randrange(3) for _ in range(n)]+[H*rng.randrange(2)])
    return answer

def run(directory,case,arm,geometry):
    data=source(case['weights'],case['fees'],case['H']);g01.save(directory/'source.json',data);meter=Meter();admit(data,geometry,meter)
    meter.pay('shared_acquisition','allocated_once_per_star_geometry_units',geometry['invoice']['total']);setup=meter.total
    n=len(case['weights']);outputs=fees=audits=0;max_queries=0;costs=[];start=time.perf_counter_ns();cpu=time.process_time_ns()
    with(directory/'trace.jsonl').open('w') as trace,(directory/'diagnostics.jsonl').open('w') as diag:
        trace.write(json.dumps(dict(kind='header',source=data['identity'],arm=arm,geometry=geometry['receipt']['identity']))+'\n');trace.flush()
        for price,tau in case['duties']:
            for t,row in enumerate(rows(case)):
                request=f"{case['name']}-{price}-{tau}-{arm}-{t}";before=meter.total;receipts=[];known={};provider=Provider(data,row,request,trace,meter)
                while True:
                    decision=choose(data,known,price,tau,arm,meter)
                    if arm=='full' and len(known)<n+2:decision['kind']='audit'
                    trace.write(json.dumps(dict(kind='gate',request=request,price=price,tau=tau,decision=decision))+'\n');trace.flush()
                    if decision['kind']!='audit':break
                    if 0 not in known:i=0
                    elif known[0]==1 and sum(w for j,w in enumerate(case['weights'],1) if j not in known)>tau:
                        i=min((j for j in range(1,n+1) if j not in known),key=lambda j:(case['fees'][j],j))
                    else:i=min((j for j in range(n+2) if j not in known),key=lambda j:(case['fees'][j],j))
                    r=provider.audit(i);receipts.append(r);known[i]=r['value'];meter.pay('selection','choose_useful_cheapest_unknown',3*(n+2))
                if decision['kind']=='repair':decision['model']=model(data,decision['count'])
                check(data,geometry,receipts,request,price,tau,decision,meter);paid=sum(r['fee'] for r in receipts)
                meter.pay('export','completed_original_action_and_bound',20+(len(decision['count']) if decision['count'] else 0))
                trace.write(json.dumps(dict(kind='output',request=request,price=price,tau=tau,decision=decision,physical_audits=len(receipts),base_fee=paid,named_units=meter.total-before))+'\n');trace.flush()
                true_opt=row[-1]+sum(2*w*min(row[0],row[i]) for i,w in enumerate(case['weights'],1))
                realized=price if decision['kind']=='replace' else row[-1]+sum(w*(k*row[0]+(2-k)*row[i]) for i,(w,k) in enumerate(zip(case['weights'],decision['count']),1))
                actual_regret=realized-min(price,true_opt);assert actual_regret<=decision['bound']<=tau
                diag.write(json.dumps(dict(request=request,hidden=row,regret=actual_regret))+'\n')
                outputs+=1;fees+=paid;audits+=len(receipts);max_queries=max(max_queries,len(receipts));costs.append(paid)
    result=dict(outputs=outputs,base_audit_fee=fees,physical_audits=audits,named_units=meter.total,setup_units=setup,invoice=meter.record(),
        declared_complete_query_cap=n+2,observed_max_queries=max_queries,trace_bytes=(directory/'trace.jsonl').stat().st_size,
        arm_cpu_ns=time.process_time_ns()-cpu,arm_wall_ns=time.perf_counter_ns()-start)
    g01.save(directory/'result.json',result)

if __name__=='__main__':
    directory=Path(sys.argv[1]);directory.mkdir(exist_ok=False);design=json.loads(Path(sys.argv[2]).read_text())
    if g01.sha(__file__)!=design['source_sha256']:raise ValueError('Service source changed')
    for name,digest in design['dependencies'].items():
        if g01.sha(HERE/name)!=digest:raise ValueError('Dependency changed '+name)
    case=next(c for c in design['cases'] if c['name']==sys.argv[3]);geometry=json.loads((Path(sys.argv[2]).parent/f"{case['name']}_geometry.json").read_text())
    run(directory,case,sys.argv[4],geometry)
