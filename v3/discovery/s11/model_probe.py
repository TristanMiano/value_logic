"""DEVELOPMENT sparse forecast selection; worlds stay in the evaluator."""
from pathlib import Path
import argparse,hashlib,json,math,random
from free_core import FreeLearner
from matching_core import matching_orders
from local_service import Oracle

T=512;FEES=(1,3,2,4,1,2)


class SelectedLearner(FreeLearner):
    def __init__(self,rng,zero=False):
        super().__init__(6,FEES,T,rng)
        self.zero=zero;self.d=2;self.M=3;self.A=math.log(self.uniform[6]);c=max(FEES)
        self.gamma=5*math.sqrt(self.d*(self.A+2*math.log(self.M))/(22*T))
        assert self.gamma<=.5
        self.eta=self.gamma/(5*self.d*c);self.B=25*self.d*c*c/self.gamma**2
        self.model_logweights=[0.]*self.M
        self.counts.update(model_score_terms=0,model_exponentials=0,model_predictions=0)
    def probabilities(self,j):
        qe=self.tree.event_probability(j,'edge');qs=self.tree.event_probability(j,'singleton')
        ue=self.uniform[j]*self.uniform[self.n-j-2]/self.uniform[self.n]
        us=self.uniform[j]*self.uniform[self.n-j-1]/self.uniform[self.n]
        return qe,(1-self.gamma)*qe+self.gamma*ue,(1-self.gamma)*qs+self.gamma*us
    def prepare(self):
        qe,e,s=self.probabilities(0)
        self.baselines=[0.,(e*FEES[1]+s*FEES[0])/(e+s),max(FEES)/2]
        if self.zero:self.baselines=[0.]*self.M
        top=max(self.model_logweights);weights=[math.exp(v-top) for v in self.model_logweights]
        self.weights=[v/sum(weights) for v in weights];self.baseline=sum(a*b for a,b in zip(self.weights,self.baselines))
        self.counts['model_predictions']+=0 if self.zero else self.M
        self.pre_probabilities={0:(qe,e,s)}
    def encode(self,events):
        scores=[0.]*self.M;estimates={};mixture_score=0.
        for j,kind,certified in events:
            if j!=0 and not certified:continue
            if j not in self.pre_probabilities:self.pre_probabilities[j]=self.probabilities(j)
            qe,e,s=self.pre_probabilities[j];prob=s if kind=='singleton' else e
            base=self.baseline if j==0 else 0.
            response=FEES[j+1]*certified if kind=='singleton' else FEES[j]*certified
            sign=1 if kind=='singleton' else -1
            estimate=sign*(response-base)/prob
            if estimate:estimates[j]=estimate
            mixture_score+=qe*estimate*estimate
            for k in range(self.M):
                b=self.baselines[k] if j==0 else 0.
                scores[k]+=qe*(response-b)**2/prob**2
        return estimates,scores,mixture_score
    def execute(self,oracle):
        self.prepare();events=[];observed=[];certified=False
        for i,j,kind in self.sample():
            value=oracle.buy(i,'execution');observed.append(i);certified=bool(value)
            if kind is not None:events.append((j,kind,int(certified)))
            if certified:break
        estimates,scores,mixture_score=self.encode(events)
        assert len(estimates)<=self.d
        assert max(scores)<=self.B+1e-8
        average=sum(w*s for w,s in zip(self.weights,scores))
        assert mixture_score<=average+1e-8
        if not self.zero:
            for k,v in enumerate(scores):self.model_logweights[k]-=v/self.B
            self.counts['model_score_terms']+=len(events)*self.M
            self.counts['model_exponentials']+=self.M
        return observed,events,estimates,scores,mixture_score,average
    def finish(self,estimates):
        for j,v in estimates.items():self.tree.update(j,-self.eta*v)


def enumerate_events(world,edges):
    events=[];j=0;edges=set(edges)
    while j<6:
        if j in edges:
            value=world[j+1];events.append((j,'edge',value))
            if value:break
            if world[j]:break
            j+=2
        else:
            value=world[j]
            if j<5:events.append((j,'singleton',value))
            if value:break
            j+=1
    return events


def case(index):
    rng=random.Random(31000+index)
    worlds=[[int(rng.random()<.4) for _ in range(6)] if index==0 else [int(index==1)]*6 for _ in range(T)]
    family=matching_orders(6);outputs=[]
    for zero in (False,True):
        learner=SelectedLearner(random.Random(32000+index),zero)
        fee=queries=checks=validation_reads=0;score_sums=[0.]*3;mixture_sum=weighted_sum=0.
        estimated_action_totals=[0.]*len(family);q_estimated=second=0.;max_eta_loss=0.;trace=hashlib.sha256()
        for t,world in enumerate(worlds):
            logs=[sum(learner.tree.logweights[j] for j in edges) for _,edges in family]
            top=max(logs);Q=[math.exp(v-top) for v in logs];Z=sum(Q);Q=[v/Z for v in Q]
            P=[(1-learner.gamma)*q+learner.gamma/len(family) for q in Q]
            oracle=Oracle(world,FEES);observed,events,estimate,scores,mixed,weighted=learner.execute(oracle)
            assert oracle.bill['feedback']==0 and len(observed)==len(set(observed))
            fee+=oracle.bill['execution'];queries+=oracle.purchases['execution']
            for k,v in enumerate(scores):score_sums[k]+=v
            mixture_sum+=mixed;weighted_sum+=weighted
            losses=[sum(estimate.get(j,0.) for j in edges) for _,edges in family]
            max_eta_loss=max(max_eta_loss,max(abs(learner.eta*v) for v in losses));assert max_eta_loss<=1+1e-8
            q_estimated+=sum(q*l for q,l in zip(Q,losses));second+=sum(q*l*l for q,l in zip(Q,losses))
            for k,v in enumerate(losses):estimated_action_totals[k]+=v
            assert sum(q*l*l for q,l in zip(Q,losses))<=learner.d*mixed+1e-8
            if t%32==0:
                means=[0.]*5
                for p,(_,edges) in zip(P,family):
                    all_events=enumerate_events(world,edges);validation_reads+=6
                    result,_,_=learner.encode(all_events)
                    for j,v in result.items():means[j]+=p*v
                live=True
                for j in range(5):
                    true=(FEES[j+1]*world[j]-FEES[j]*world[j+1]) if live else 0
                    assert abs(means[j]-true)<1e-8,(index,t,j,means[j],true)
                    live=live and not world[j];checks+=1
            trace.update(json.dumps([observed,events,estimate,scores]).encode())
            learner.finish(estimate)
        assert weighted_sum<=2*min(score_sums)+2*learner.B*math.log(3)+1e-6
        estimated_regret=q_estimated-min(estimated_action_totals)
        estimated_bound=learner.A/learner.eta+learner.eta*second
        assert estimated_regret<=estimated_bound+1e-6
        outputs.append({'kind':'zero_same_tuning' if zero else 'learned_model','execution_fees':fee,
            'truth_purchases':queries,'feedback_purchases':0,'model_score_sums':score_sums,
            'weighted_model_score_sum':weighted_sum,'mixture_score_sum':mixture_sum,
            'small_loss_upper':2*min(score_sums)+2*learner.B*math.log(3),
            'estimated_matching_regret':estimated_regret,'estimated_matching_bound':estimated_bound,
            'max_eta_estimated_matching_loss':max_eta_loss,'finite_mean_checks':checks,
            'validation_world_reads':validation_reads,'gamma':learner.gamma,'eta':learner.eta,'B':learner.B,
            'final_model_logweights':learner.model_logweights,'counts':learner.counts,'matrix_counts':learner.tree.counts,
            'trajectory_sha256':trace.hexdigest()})
    return {'contributor':'Codex (GPT-6)','status':'DEVELOPMENT','case':index,'n':6,'rounds':T,
        'stream':('seeded_bits','all_one','all_zero')[index],'world_seed':31000+index,'sampling_seed':32000+index,
        'fees':FEES,'K':1,'models':['zero','both_first_queries_certify','half_max_fee_first_edge'],
        'worlds_sha256':hashlib.sha256(json.dumps(worlds).encode()).hexdigest(),'arms':outputs,
        'hashes':{name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() for name in ('model_probe.py','free_core.py','matching_core.py','local_service.py')},
        'scope':'Joint-update and purchase-boundary screen; floats checked with declared tolerances, not formal arithmetic. Observed score inequalities do not certify realized expected regret. Compute unpriced; no broad service advantage.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',type=int,required=True);p.add_argument('--out',required=True)
    a=p.parse_args();assert a.case in (0,1,2);result=case(a.case)
    with open(a.out,'x',encoding='utf-8',newline='\n') as out:out.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'case':a.case,'arms':[{k:v[k] for k in ('kind','execution_fees','truth_purchases','feedback_purchases','finite_mean_checks','model_score_sums','final_model_logweights')} for v in result['arms']]}))
