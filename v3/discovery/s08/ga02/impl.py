"""Incremental ordinary graph controllers, Codex (GPT-6), DEVELOPMENT."""
from pathlib import Path
import json
import graph_audits as ga
import graph_service as gs
Meter=ga.Meter;g01=ga.g01;HERE=Path(__file__).resolve().parent

class Heap:
    def __init__(self,meter):self.a=[];self.meter=meter
    def less(self,a,b):
        self.meter.pay('execution','heap_integer_ratio_comparison',6)
        x=a[0]*b[1];y=b[0]*a[1]
        return x<y or(x==y and a[1:]<b[1:])
    def push(self,item):
        a=self.a;a.append(item);i=len(a)-1;self.meter.pay('execution','heap_push_words',4)
        while i:
            j=(i-1)//2
            if not self.less(a[i],a[j]):break
            a[i],a[j]=a[j],a[i];i=j;self.meter.pay('execution','heap_sift_words',4)
    def pop(self):
        a=self.a;out=a[0];last=a.pop();self.meter.pay('execution','heap_pop_words',4)
        if a:
            a[0]=last;i=0
            while 2*i+1<len(a):
                j=2*i+1
                if j+1<len(a) and self.less(a[j+1],a[j]):j+=1
                if not self.less(a[j],a[i]):break
                a[i],a[j]=a[j],a[i];i=j;self.meter.pay('execution','heap_sift_words',4)
        return out
    def __bool__(self):return bool(self.a)

def adjacency(data,meter):
    adj=[[] for _ in range(data['n'])]
    for a,b,w in data['edges']:adj[a].append(b);adj[b].append(a)
    meter.pay('preparation','graph_adjacency_words',data['n']+4*len(data['edges']))
    return adj

def greedy(data,adj,get,meter):
    known={};degree=[len(x) for x in adj];choice=Heap(meter);forced=Heap(meter);pending=set()
    for i,d in enumerate(degree):
        if d:choice.push((-d,data['audit_costs'][i],i))
    meter.pay('execution','initialize_unknown_degrees',data['n'])
    while True:
        i=None
        while forced:
            _,_,j=forced.pop();pending.discard(j)
            if j not in known:i=j;break
        if i is None:
            while choice:
                nd,c,j=choice.pop();meter.pay('execution','discard_stale_degree_heap_entry',4)
                if j not in known and degree[j]>0 and degree[j]==-nd:i=j;break
        if i is None:return known
        known[i]=get(i)
        for j in adj[i]:
            meter.pay('execution','remove_observed_vertex_incidence',5)
            if j in known:continue
            degree[j]-=1
            if degree[j]>0:choice.push((-degree[j],data['audit_costs'][j],j))
            if known[i]==1 and j not in pending:forced.push((-1,1,j));pending.add(j)

def adaptive_dual(data,adj,get,meter):
    known={};residual=list(data['audit_costs']);dual=[0]*len(data['edges']);forced=Heap(meter);pending=set();tight=[];forced_queries=[]
    def query(i,is_forced):
        if i in known:return
        known[i]=get(i)
        (forced_queries if is_forced else tight).append(i)
        meter.pay('execution','record_tight_or_mandatory_query',5)
        if known[i]==1:
            for j in adj[i]:
                meter.pay('execution','middle_neighbor_mandatory_expansion',3)
                if j not in known and j not in pending:forced.push((-1,1,j));pending.add(j)
    for e,(a,b,w) in enumerate(data['edges']):
        while forced:
            _,_,i=forced.pop();pending.discard(i);query(i,True)
        meter.pay('execution','adaptive_dual_edge_state',5)
        if a in known or b in known:continue
        value=min(residual[a],residual[b]);dual[e]=value;residual[a]-=value;residual[b]-=value
        meter.pay('execution','adaptive_dual_edge_raise',7)
        # Query one newly tight endpoint. Another zero-residual endpoint may
        # become unnecessary; a later uncovered edge can select it at zero raise.
        query(a if residual[a]==0 else b,False)
    while forced:
        _,_,i=forced.pop();pending.discard(i);query(i,True)
    meter.pay('execution','initialize_and_emit_dynamic_dual',2*data['n']+len(dual))
    return known,dict(source=data['identity'],dual=dual,cover=tight,forced=forced_queries)

def check_cases(directory):
    directory.mkdir(exist_ok=False);(directory/'impl.py').write_bytes(Path(__file__).read_bytes())
    old=json.loads((HERE/'ga01/design.json').read_text())['cases'];result=[]
    from itertools import product
    for case in old:
        data=ga.source(case['costs'],case['edges']);meter=Meter();adj=adjacency(data,meter);checks=0;ratios=[]
        for bits in product((0,1),repeat=data['n']):
            row=[1 if b else 2*(i%2) for i,b in enumerate(bits)];old_order=[];new_order=[]
            gs.greedy(data,lambda i:old_order.append(i) or row[i],Meter())
            greedy(data,adj,lambda i:new_order.append(i) or row[i],Meter());assert old_order==new_order
            receipts=[];request='conditional'
            def get(i):
                receipts.append(g01.seal(dict(source=data['identity'],request=request,node=i,value=row[i],base_fee=case['costs'][i],sequence=len(receipts))))
                return row[i]
            known,plan=adaptive_dual(data,adj,get,meter);ga.check_dual(data,plan,meter,False)
            cert=ga.lower_certificate(data,plan,known,meter);lower=ga.check_lower(data,plan,receipts,request,cert,meter)
            action=ga.base.construct(data,receipts,request,meter);ga.base.check(data,receipts,action,meter)
            fee=sum(case['costs'][i] for i in known);opt=ga.offline(data,row);assert lower<=opt<=fee<=2*lower
            assert all(sum(y for (a,b,w),y in zip(data['edges'],plan['dual']) if i in(a,b))==case['costs'][i] for i in plan['cover'])
            assert set(plan['forced'])<=set(cert['mandatory'])
            ratios.append((fee,opt,lower));checks+=1
        result.append(dict(name=case['name'],worlds=checks,ratios=ratios));g01.save(directory/'progress.json',result)
        print(case['name'],checks,flush=True)
    # Independently replay the incremental choices on all exposed gs01 rows.
    service=json.loads((HERE/'gs01/design.json').read_text());replays=0
    for case in service['cases']:
        data=ga.source(case['costs'],case['edges']);adj=adjacency(data,Meter())
        for row in gs.rows(data['n'],case['seed']):
            a=[];b=[];gs.greedy(data,lambda i:a.append(i) or row[i],Meter());greedy(data,adj,lambda i:b.append(i) or row[i],Meter());assert a==b;replays+=1
    g01.save(directory/'results.json',dict(status='checked',small_worlds=sum(x['worlds'] for x in result),cases=result,gs01_replays=replays,physical_audits=0))

if __name__=='__main__':
    import sys
    check_cases(Path(sys.argv[1]))
