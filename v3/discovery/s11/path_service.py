"""DEVELOPMENT ordinary path semi-bandit, no extra truth queries."""
from pathlib import Path
import argparse,hashlib,json,math,random,time
from matching_core import logadd
from local_service import stream,Oracle


class PathLearner:
    def __init__(self,n,d,fees,T,rng):
        self.n=n;self.d=d;self.fees=fees;self.rng=rng
        self.layers=[[0]];self.edges=[];self.out={};self.incoming={0:[]}
        for k in range(n):
            following=set();required=(1<<max(0,k+1-d))-1
            for S in self.layers[-1]:
                self.out[S]=[]
                for j in range(max(0,k-d),min(n,k+d+1)):
                    if S&(1<<j):continue
                    after=S|(1<<j)
                    if after&required!=required:continue
                    e=len(self.edges);self.edges.append((S,j,after));self.out[S].append(e)
                    self.incoming.setdefault(after,[]).append(e);following.add(after)
            self.layers.append(sorted(following))
        self.terminal=(1<<n)-1;self.out[self.terminal]=[]
        paths={self.terminal:1}
        for layer in reversed(self.layers[:-1]):
            for S in layer:paths[S]=sum(paths[self.edges[e][2]] for e in self.out[S])
        assert all(v>0 for v in paths.values())
        self.path_count=paths[0];self.D=len(self.edges);self.logweights=[0.]*self.D
        self.eta=math.sqrt(2*math.log(self.path_count)/(n*self.D*max(fees)**2*T))
        self.counts={'forward_backward_logadd':0,'edge_probability_exponentials':0,
          'sampling_exponentials':0,'sampling_coins':0,'weight_updates':0,'zero_probabilities':0}
        self.max_flow_error=0.;self.min_probability=1.
    def prepare(self):
        self.back={self.terminal:0.}
        for layer in reversed(self.layers[:-1]):
            for S in layer:
                z=-math.inf
                for e in self.out[S]:
                    z=logadd(z,self.logweights[e]+self.back[self.edges[e][2]])
                    self.counts['forward_backward_logadd']+=1
                self.back[S]=z
        forward={0:0.}
        for layer in self.layers[1:]:
            for S in layer:
                z=-math.inf
                for e in self.incoming[S]:
                    z=logadd(z,forward[self.edges[e][0]]+self.logweights[e])
                    self.counts['forward_backward_logadd']+=1
                forward[S]=z
        self.probabilities=[]
        for e,(S,j,after) in enumerate(self.edges):
            p=math.exp(forward[S]+self.logweights[e]+self.back[after]-self.back[0])
            self.counts['edge_probability_exponentials']+=1
            if p==0:self.counts['zero_probabilities']+=1
            assert 0<p<=1+1e-8,('probability precision failure',e,p)
            self.probabilities.append(p);self.min_probability=min(self.min_probability,p)
        for layer in self.layers:
            for S in layer:
                incoming=sum(self.probabilities[e] for e in self.incoming.get(S,[])) if S else 1.
                outgoing=sum(self.probabilities[e] for e in self.out[S]) if S!=self.terminal else 1.
                self.max_flow_error=max(self.max_flow_error,abs(incoming-outgoing))
        assert self.max_flow_error<1e-8
    def execute(self,oracle,threshold):
        self.prepare();S=0;total=0;trace=[]
        while S!=self.terminal and total<threshold:
            coin=self.rng.random();self.counts['sampling_coins']+=1;cumulative=0.;chosen=self.out[S][-1]
            for e in self.out[S]:
                p=math.exp(self.logweights[e]+self.back[self.edges[e][2]]-self.back[S])
                self.counts['sampling_exponentials']+=1;cumulative+=p
                if coin<cumulative:chosen=e;break
            _,j,after=self.edges[chosen];total+=oracle.buy(j,'execution');trace.append((chosen,j));S=after
        for e,j in trace:
            self.logweights[e]-=self.eta*self.fees[j]/self.probabilities[e]
            assert math.isfinite(self.logweights[e]);self.counts['weight_updates']+=1
        return trace


def case(index):
    if index<4:worlds,fees,threshold=stream(index);d=1
    else:
        rng=random.Random(33004);worlds=[[int(rng.random()<.4) for _ in range(8)] for _ in range(256)]
        fees=[1+3*i%5 for i in range(8)];threshold=2;d=2
    n=len(fees);T=len(worlds);start=time.perf_counter_ns()
    learner=PathLearner(n,d,fees,T,random.Random(34000+index));bill=queries=0;trajectory=hashlib.sha256()
    for world in worlds:
        oracle=Oracle(world,fees);trace=learner.execute(oracle,threshold)
        assert oracle.bill['feedback']==0 and len(trace)==len(oracle.receipts)
        bill+=oracle.bill['execution'];queries+=oracle.purchases['execution']
        trajectory.update(json.dumps(trace).encode())
    root=Path(__file__).resolve().parent;worldhash=hashlib.sha256(json.dumps(worlds,separators=(',',':')).encode()).hexdigest()
    comparison=None
    if index<4:
        path=root/'ls01'/('c%02da0.json'%index);old=json.loads(path.read_text())
        assert worldhash==old['worlds_sha256']
        comparison={'input':path.relative_to(root).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                    'fees':{a['kind']:a['total_query_fees'] for a in old['arms']}}
    return {'contributor':'Codex (GPT-6)','status':'DEVELOPMENT','case':index,'n':n,'bandwidth':d,'rounds':T,
        'threshold':threshold,'fees':fees,'eta':learner.eta,'path_count':learner.path_count,
        'states':sum(map(len,learner.layers)),'edges':learner.D,'execution_fees':bill,'feedback_fees':0,
        'truth_purchases':queries,'feedback_purchases':0,'counts':learner.counts,
        'max_flow_error':learner.max_flow_error,'min_inclusion_probability':learner.min_probability,
        'sampling_seed':34000+index,'worlds_sha256':worldhash,'trajectory_sha256':trajectory.hexdigest(),
        'comparison':comparison,'final_logweights':learner.logweights,'elapsed_ns':time.perf_counter_ns()-start,
        'hashes':{s:hashlib.sha256((root/s).read_bytes()).hexdigest() for s in ('path_service.py','matching_core.py','local_service.py')},
        'scope':'Fixed ordinary semi-bandit tuning; four exposed service streams and one small new mechanics case. Compute and setup prices unknown, float conformance only, no external-population claim.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',type=int,required=True);p.add_argument('--out',required=True)
    a=p.parse_args();assert a.case in range(5);result=case(a.case)
    with open(a.out,'x',encoding='utf-8',newline='\n') as out:out.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('case','n','bandwidth','execution_fees','truth_purchases','states','edges','path_count','eta','counts','max_flow_error','min_inclusion_probability','elapsed_ns')}))
