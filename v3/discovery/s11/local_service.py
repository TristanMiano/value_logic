"""DEVELOPMENT priced local-feedback service. Codex (GPT-6).

Four fixed generated streams, no tuning after exposure. See local_service_plan.md.
The evaluator alone receives worlds; deployment arms see an Oracle's receipts.
"""
import argparse
import hashlib
import json
import math
import random
from pathlib import Path
from matching_core import MatchingTree

T=2000
RHO=0.1


class Oracle:
    def __init__(self,world,fees):
        self.__world=world
        self.fees=fees
        self.receipts={}
        self.bill={'execution':0,'feedback':0}
        self.purchases={'execution':0,'feedback':0}

    def buy(self,i,kind):
        if i not in self.receipts:
            self.receipts[i]=self.__world[i]
            self.bill[kind]+=self.fees[i]
            self.purchases[kind]+=1
        return self.receipts[i]


def stream(case):
    n=16 if case==0 else 64
    threshold=(1,1,3,32)[case]
    fees=[1+(i*7%9) for i in range(n)]
    rng=random.Random(11000+case)
    worlds=[]
    for t in range(T):
        if case==0:
            x=[int(rng.random() < (0.6 if i%3==1 else 0.05)) for i in range(n)]
        elif case==1:
            u=rng.random();phase=(t//200)%2
            x=[int(u < (0.75 if (i+phase)%2 else 0.10)) for i in range(n)]
        elif case==2:
            u=rng.random()
            x=[int(u < (0.85 if i%4 in (1,3) else 0.12)) for i in range(n)]
        else:
            u=rng.random()
            x=[int((u < 0.45 and i%2==1) or (u >= 0.45 and rng.random()<0.55))
               for i in range(n)]
        worlds.append(x)
    return worlds,fees,threshold


def deltas(receipts,fees,threshold,counts):
    n=len(fees);prefix=[0];reference=0;L=0
    while L<n and prefix[-1]<threshold:
        assert L in receipts,(L,sorted(receipts))
        prefix.append(prefix[-1]+receipts[L]);reference+=fees[L];L+=1
        counts['delta_data_reads']+=1;counts['delta_additions']+=2
    if prefix[-1]<threshold:return {},reference
    out={}
    if L>=2:
        j=L-2;B=int(prefix[j]+receipts[j+1]>=threshold)
        counts['delta_data_reads']+=1;counts['delta_additions']+=1
        if B:out[j]=-fees[j]
    if L<n:
        j=L-1;assert j+1 in receipts
        B=int(prefix[j]+receipts[j+1]>=threshold)
        counts['delta_data_reads']+=1;counts['delta_additions']+=1
        delta=fees[j+1]-fees[j]*B
        if delta:out[j]=delta
    return out,reference


def best_matching(edge_costs):
    n=len(edge_costs)+1;values=[0.]*(n+2);edges=[]
    for j in range(n-2,-1,-1):
        values[j]=min(values[j+1],edge_costs[j]+values[j+2])
    j=0
    while j<n-1:
        if edge_costs[j]+values[j+2]<values[j+1]-1e-10:
            edges.append(j);j+=2
        else:j+=1
    return values[0],edges


def order_for(n,edges):
    edge_set=set(edges);j=0
    while j<n:
        if j in edge_set:
            yield j+1;yield j;j+=2
        else:yield j;j+=1


class Service:
    def __init__(self,n,fees,threshold,kind,case):
        self.n=n;self.fees=fees;self.threshold=threshold;self.kind=kind
        self.order_rng=random.Random(12000+case)
        self.audit_rng=random.Random(13000+case)
        self.tree=MatchingTree(n) if kind in ('local','full') else None
        a,b=1,1
        for _ in range(n):a,b=b,a+b
        self.policy_count=a
        self.eta=math.sqrt(8*RHO*math.log(a)/((2*max(fees))**2*T))
        self.fixed_edges=best_matching([fees[j+1]-fees[j] for j in range(n-1)])[1]
        self.bandit_eta=math.sqrt(math.log(2)/(2*T));self.gamma=2*self.bandit_eta
        self.bandit_weights=[[0.,0.] for _ in range(n)]
        self.counts={k:0 for k in ('execution_data_reads','threshold_additions',
            'delta_data_reads','delta_additions','audit_coins','bandit_coins',
            'bandit_scalar_updates')}
        self.totals={'execution_fees':0,'feedback_fees':0,
                     'execution_receipts':0,'feedback_receipts':0,'feedback_rounds':0}
        self.digest=hashlib.sha256();self.actions=[]

    def bandit_order(self,offset):
        j=0
        if offset:
            yield 0,None,None,None;j=1
        while j<self.n:
            if j+1==self.n:
                yield j,None,None,None;break
            w=self.bandit_weights[j];pivot=max(w)
            e=[math.exp(v-pivot) for v in w]
            p=(1-self.gamma)*e[0]/sum(e)+self.gamma/2
            arm=int(self.order_rng.random()>=p);self.counts['bandit_coins']+=1
            probability=(1-p) if arm else p
            yield j+arm,j,arm,probability
            yield j+1-arm,j,arm,probability
            j+=2

    def round(self,oracle):
        if self.tree:iterator=((i,None,None,None) for i in self.tree.sample_lazy(self.order_rng))
        elif self.kind=='identity':iterator=((i,None,None,None) for i in range(self.n))
        elif self.kind=='fixed_fee':iterator=((i,None,None,None) for i in order_for(self.n,self.fixed_edges))
        else:iterator=self.bandit_order(int(self.kind[-1]))
        total=0;executed=[];active=None;blockbill=0
        while total<self.threshold and len(executed)<self.n:
            i,j,arm,p=next(iterator)
            if j!=active:blockbill=0;active=j
            blockbill+=self.fees[i]
            total+=oracle.buy(i,'execution');executed.append(i)
            self.counts['execution_data_reads']+=1;self.counts['threshold_additions']+=1
        if self.kind.startswith('bandit') and total>=self.threshold and active is not None:
            low=min(self.fees[active:active+2]);scale=max(self.fees[active:active+2])
            loss=(blockbill-low)/scale
            assert 0<=loss<=1
            self.bandit_weights[active][arm]-=self.bandit_eta*loss/p
            self.counts['bandit_scalar_updates']+=1
        used_delta={}
        if self.tree:
            self.counts['audit_coins']+=1
            if self.audit_rng.random()<RHO:
                self.totals['feedback_rounds']+=1
                end=self.n if self.kind=='full' else min(self.n,max(executed)+2)
                for i in range(end):oracle.buy(i,'feedback')
                used_delta,_=deltas(oracle.receipts,self.fees,self.threshold,self.counts)
                for j,delta in used_delta.items():self.tree.update(j,-self.eta*delta/RHO)
        self.digest.update(json.dumps([executed,sorted(used_delta.items())]).encode())
        self.actions.append((tuple(executed),oracle.bill['execution'],tuple(sorted(used_delta.items()))))
        for kind in ('execution','feedback'):
            self.totals[kind+'_fees']+=oracle.bill[kind]
            self.totals[kind+'_receipts']+=oracle.purchases[kind]

    def summary(self):
        return {'kind':self.kind,**self.totals,'total_query_fees':self.totals['execution_fees']+
            self.totals['feedback_fees'],'counts':self.counts,
            'matrix_counts':None if self.tree is None else self.tree.counts,
            'trajectory_sha256':self.digest.hexdigest(),
            'parameters':{'eta':self.eta,'rho':RHO,'bandit_eta':self.bandit_eta,
                          'bandit_gamma':self.gamma},
            'retained_logweights':None if self.tree is None else self.tree.logweights}


def run(case):
    worlds,fees,threshold=stream(case);n=len(fees)
    arms=[Service(n,fees,threshold,k,case) for k in
          ('local','full','identity','fixed_fee','bandit0','bandit1')]
    for world in worlds:
        for arm in arms:arm.round(Oracle(world,fees))
    assert arms[0].actions==arms[1].actions
    assert arms[0].tree.logweights==arms[1].tree.logweights
    assert arms[0].counts==arms[1].counts
    assert arms[0].tree.counts==arms[1].tree.counts
    edge_sums=[0]*(n-1);reference=0
    evaluator_counts={'delta_data_reads':0,'delta_additions':0}
    for world in worlds:
        delta,cost=deltas(dict(enumerate(world)),fees,threshold,evaluator_counts)
        reference+=cost
        for j,v in delta.items():edge_sums[j]+=v
    delta,edges=best_matching(edge_sums)
    return {'contributor':'Codex (GPT-6)','status':'DEVELOPMENT','case':case,
       'n':n,'rounds':T,'threshold':threshold,'fees':fees,
       'seeds':{'world':11000+case,'order':12000+case,'audit':13000+case},
       'worlds_sha256':hashlib.sha256(json.dumps(worlds,separators=(',',':')).encode()).hexdigest(),
       'matching_policy_count':arms[0].policy_count,'identical_local_full_trajectory':True,
       'arms':[arm.summary() for arm in arms],
       'hindsight_matching':{'execution_fees':reference+delta,'edges':edges,
           'edge_sums':edge_sums,'evaluator_counts':evaluator_counts},
       'limitations':['Generated streams; exposed developmental evidence.',
          'Only query fees priced. Computation categories have no common price.',
          'No-extra-query bandit controls have smaller, fixed-pair policy families.',
          'An ordinary implementation of the local interface ties it.',
          'Private random seeds coupled only for paired local/full comparison.']}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',type=int,required=True)
    p.add_argument('--out',required=True);a=p.parse_args()
    output=run(a.case)
    Path(a.out).write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'case':a.case,'arms':[(x['kind'],x['total_query_fees']) for x in output['arms']]}))
