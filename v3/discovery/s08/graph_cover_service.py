"""gc02 paid original graph cover, Codex (GPT-6), DEVELOPMENT."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import heapq
import json
import random
import sys
import time
import graph_cover as gc
g01=gc.g01;Meter=gc.Meter;HERE=gc.HERE

def compile_source(case,data,cut,geometry,meter):
    K=gc.admit(case,data,cut,geometry,meter);n=data['nodes'];H=data['H'];W=sum(w for a,b,w in data['edges']);adj=[[] for _ in range(n)]
    for a,b,w in data['edges']:adj[a].append((b,w));adj[b].append((a,w));meter.pay('compilation','source_edge_adjacency',8)
    degrees=[sum(w for j,w in row) for row in adj];base=[[2*(H-v)*d for v in data['supports'][0]] for d in degrees]
    balanced=gc.model(data,[1]*len(data['edges']))
    for clause in data['hard']:
        if not any(bool(balanced>>(abs(l)-1)&1)==(l>0) for l in clause):raise ValueError('Balanced original action infeasible')
        meter.pay('compiled_action','one_time_original_clause_check',1+len(clause))
    meter.pay('compilation','node_response_marginal_and_balanced_action_words',6*n+len(data['edges'])+max(1,data['variables']//64+1))
    return dict(source=data['identity'],K=K,adj=adj,base=base,balanced=balanced,Q=H*(2*W-K),tau=H*K,A=10*H*W)

class State:
    def __init__(self,data,compiled,mode,meter):
        self.data=data;self.c=compiled;self.mode=mode;self.meter=meter;self.n=data['nodes'];self.known=[None]*(self.n+1);self.d=[0]*self.n;self.G=0;self.epoch=0;self.heap=[]
        meter.pay('state','request_coordinate_and_score_storage',3*self.n+6)
        if mode=='lazy':
            self.M=[list(row) for row in compiled['base']];meter.pay('state','copy_initial_response_marginals',sum(map(len,self.M)))
            self.heap=[(-self.score(i),i,0) for i in range(self.n+1)];heapq.heapify(self.heap);meter.pay('selection','initial_heap_upper_comparisons',3*(self.n+1))
    def remaining(self):return max(0,self.c['Q']-self.G)
    def score(self,i):
        rem=self.remaining()
        if i==self.n:return F(rem,self.data['audit_costs'][i])
        if self.mode=='lazy':
            total=sum(min(rem,v) for v in self.M[i]);self.meter.pay('selection','cap_cached_response_marginals',4*len(self.M[i]))
        else:
            total=0
            for v in self.data['supports'][i]:
                gain=sum(2*w*max(0,self.data['H']-v-self.d[j]) for j,w in self.c['adj'][i]);total+=min(rem,gain)
                self.meter.pay('selection','adjacency_response_gain_scan',4+8*len(self.c['adj'][i]))
        self.meter.pay('selection','rational_score_construction',8)
        return F(total,len(self.data['supports'][i])*self.data['audit_costs'][i])
    def select(self):
        if self.remaining()==0:return None
        if self.mode=='anchor':return self.n
        if self.mode=='scan':
            best=None
            for i,v in enumerate(self.known):
                if v is not None:continue
                proposal=(-self.score(i),i)
                if best is None or proposal<best:best=proposal
                self.meter.pay('selection','current_score_scan_comparison',4)
            return best[1]
        while self.heap:
            previous,i,epoch=heapq.heappop(self.heap);self.meter.pay('selection','lazy_heap_pop_upper_comparisons',4+max(1,len(self.heap).bit_length()))
            if self.known[i] is not None:continue
            if epoch==self.epoch:return i
            score=self.score(i)
            if score>-previous:raise AssertionError('Stale score was not an upper bound')
            heapq.heappush(self.heap,(-score,i,self.epoch));self.meter.pay('selection','lazy_heap_refresh_comparisons',4+max(1,len(self.heap).bit_length()))
        raise AssertionError('Uncovered source with no available query')
    def observe(self,i,value):
        if self.known[i] is not None or value not in self.data['supports'][i]:raise ValueError('Wrong repeated/unsupported observation')
        self.known[i]=value;self.epoch+=1
        if i==self.n:self.G=self.c['Q'];return
        d=self.data['H']-value
        for j,w in self.c['adj'][i]:
            self.G+=2*w*max(0,d-self.d[j]);self.meter.pay('state','incident_cover_increment',8)
            if self.mode=='lazy' and self.known[j] is None:
                for k,v in enumerate(self.data['supports'][j]):
                    self.M[j][k]-=2*w*min(self.data['H']-v,d)
                    if self.M[j][k]<0:raise AssertionError('Negative marginal table')
                    self.meter.pay('state','neighbor_marginal_decrement',8)
        self.d[i]=d

def proposal(data,compiled,known,meter):
    if known[-1]==compiled['A']:return dict(kind='replace',basis='high_anchor',model=None,bound=0)
    if known[-1]==0:return dict(kind='repair',basis='balanced_cut',model=compiled['balanced'],bound=compiled['tau'])
    upper=[data['H'] if v is None else v for v in known[:-1]];count=[2 if upper[a]<=upper[b] else 0 for a,b,w in data['edges']]
    U=sum(2*w*min(upper[a],upper[b]) for a,b,w in data['edges']);model=gc.model(data,count)
    meter.pay('action_proposal','upper_cost_original_pair_action',14*len(data['edges'])+len(upper))
    if U>compiled['tau']:raise ValueError('Incomplete cover')
    return dict(kind='repair',basis='upper_cost',model=model,bound=U)

def check(data,compiled,receipts,request,decision,meter):
    if compiled['source']!=data['identity']:raise ValueError('Wrong persistent source')
    n=data['nodes'];known=[None]*(n+1)
    for r in receipts:
        i=r['coordinate']
        if(r['identity']!=g01.kernel.digest({k:v for k,v in r.items() if k!='identity'}) or r['source']!=data['identity'] or r['request']!=request or type(i)is not int or not 0<=i<=n
            or known[i] is not None or r['sequence']!=sum(v is not None for v in known) or r['value'] not in data['supports'][i] or r['fee']!=data['audit_costs'][i]):raise ValueError('Invalid receipt')
        known[i]=r['value'];meter.pay('receipt_check','source_request_coordinate_sequence_value_fee',20)
    if decision['basis']=='high_anchor':
        if known[-1]!=compiled['A'] or decision['kind']!='replace' or decision['model'] is not None:raise ValueError('Replacement not warranted')
        bound=0
    elif decision['basis']=='balanced_cut':
        if known[-1]!=0 or decision['kind']!='repair' or decision['model']!=compiled['balanced']:raise ValueError('Wrong prechecked balanced action')
        meter.pay('action_check','exact_prechecked_source_model_words',4+data['variables']//64+1);bound=compiled['tau']
    elif decision['basis']=='upper_cost':
        mask=decision['model']
        if decision['kind']!='repair' or known[-1] is not None or type(mask)is not int or not 0<=mask<(1<<data['variables']) or not(mask>>(data['variables']-1)&1):raise ValueError('Invalid original action range/anchor')
        upper=[data['H'] if v is None else v for v in known[:-1]];bound=0
        for j,(a,b,w) in enumerate(data['edges']):
            bits=(mask>>(4*j))&15
            if bits not in(5,6,9,10):raise ValueError('Original exactly-one pair violated')
            k=int(bool(bits&1))+int(bool(bits&4));bound+=w*(k*upper[a]+(2-k)*upper[b]);meter.pay('action_check','admitted_original_pair_and_upper_contribution',13)
    else:raise ValueError('Unknown bound basis')
    if bound!=decision['bound'] or bound>compiled['tau']:raise ValueError('Wrong action bound')
    return known

def rows(case,data):
    rng=random.Random(case['seed']);return [[rng.choice(support) for support in data['supports']] for _ in range(64)]

def prepare(root):
    root.mkdir(exist_ok=False);rng=random.Random(8141700);cases=[]
    for n in(8,16,32):
        for shape in('path','cycle','clique','sparse'):
            edges={(i,i+1) for i in range(n-1)}
            if shape=='cycle':edges.add((0,n-1))
            if shape=='clique':edges=set(combinations(range(n),2))
            if shape=='sparse':edges.update((a,b) for a,b in combinations(range(n),2) if rng.random()<.2)
            weighted=[[a,b,1 if shape!='sparse' else rng.randrange(1,6)] for a,b in sorted(edges)]
            cases.append(dict(name=f'n{n}_{shape}',n=n,H=4,edges=weighted,fees=[rng.randrange(1,8) for _ in range(n)]+[2*n+9],seed=8141710+len(cases)))
    design=dict(stage='DEVELOPMENT',contributor='Codex (GPT-6)',cases=cases,arms=['lazy','ordinary_lazy','scan','anchor'],source_sha256=g01.sha(__file__),dependencies={name:g01.sha(HERE/name) for name in('graph_cover.py','action_audits.py','frontier_service.py','replacement_frontier.py','g01.py','joint_guard.py')},requests_per_case_arm=64,complete_sat_calls=0)
    g01.save(root/'design.json',design);(root/'impl.py').write_bytes(Path(__file__).read_bytes());(root/'declaration.md').write_bytes((HERE/'graph_cover_service.md').read_bytes())
    for name in design['dependencies']:(root/name).write_bytes((HERE/name).read_bytes())
    for case in cases:
        data=gc.source(case);meter=Meter();cut=gc.propose_cut(data,meter);geometry=gc.fs.acquire_geometry(data);gc.admit(case,data,cut,geometry,meter)
        g01.save(root/f"{case['name']}_evidence.json",dict(source=data,cut=cut,geometry=geometry,cut_acquisition_and_initial_check=meter.record()))
    print('prepared',len(cases),'actual source certificates',flush=True)

def run(root,case,arm,directory):
    evidence=json.loads((root/f"{case['name']}_evidence.json").read_text());data=evidence['source'];meter=Meter();compiled=compile_source(case,data,evidence['cut'],evidence['geometry'],meter)
    meter.pay('shared_acquisition','actual_cut_proposal_and_initial_admission',evidence['cut_acquisition_and_initial_check']['total']);meter.pay('shared_acquisition','actual_mandatory_resolution',evidence['geometry']['invoice']['total']);setup=meter.total
    fee=audits=outputs=maximum=0;cpu=time.process_time_ns();wall=time.perf_counter_ns();directory.mkdir(exist_ok=False);g01.save(directory/'source.json',data)
    with(directory/'trace.jsonl').open('w') as trace,(directory/'diagnostics.jsonl').open('w') as diagnostics:
        trace.write(json.dumps(dict(kind='header',source=data['identity'],arm=arm,price=compiled['A'],tau=compiled['tau'],cut=evidence['cut']['identity']))+'\n');trace.flush()
        for t,row in enumerate(rows(case,data)):
            request=f"{case['name']}-{arm}-{t}";before=meter.total;state=State(data,compiled,'lazy' if arm in('lazy','ordinary_lazy') else arm,meter);receipts=[];provider=gc.fs.Provider(data,row,request,trace,meter)
            while True:
                i=state.select()
                if i is None:break
                r=provider.audit(i);receipts.append(r);state.observe(i,r['value'])
            decision=proposal(data,compiled,state.known,meter);check(data,compiled,receipts,request,decision,meter);paid=sum(r['fee'] for r in receipts)
            meter.pay('export','complete_original_action_and_source_bill_words',24+(0 if decision['model'] is None else data['variables']//64+1))
            trace.write(json.dumps(dict(kind='output',request=request,decision=decision,base_fee=paid,physical_audits=len(receipts),named_units=meter.total-before))+'\n');trace.flush()
            opt=row[-1]+sum(2*w*min(row[a],row[b]) for a,b,w in data['edges'])
            if decision['kind']=='replace':cost=compiled['A']
            else:
                cost=row[-1]
                for j,(a,b,w) in enumerate(data['edges']):
                    k=int(bool(decision['model']>>(4*j)&1))+int(bool(decision['model']>>(4*j+2)&1));cost+=w*(k*row[a]+(2-k)*row[b])
            assert cost-min(compiled['A'],opt)<=decision['bound']<=compiled['tau'];diagnostics.write(json.dumps(dict(request=request,hidden=row,regret=cost-min(compiled['A'],opt)))+'\n')
            fee+=paid;audits+=len(receipts);outputs+=1;maximum=max(maximum,paid)
    g01.save(directory/'result.json',dict(outputs=outputs,base_audit_fee=fee,physical_audits=audits,named_units=meter.total,setup_units=setup,invoice=meter.record(),observed_max_fee=maximum,declared_query_cap=data['nodes']+1,cpu_ns=time.process_time_ns()-cpu,wall_ns=time.perf_counter_ns()-wall))

if __name__=='__main__':
    root=Path(sys.argv[2])
    if sys.argv[1]=='prepare':prepare(root)
    else:
        design=json.loads((root/'design.json').read_text())
        if g01.sha(__file__)!=design['source_sha256']:raise ValueError('Changed implementation')
        for name,digest in design['dependencies'].items():
            if g01.sha(HERE/name)!=digest:raise ValueError('Changed dependency '+name)
        case=next(c for c in design['cases'] if c['name']==sys.argv[3]);run(root,case,sys.argv[4],Path(sys.argv[5]))
