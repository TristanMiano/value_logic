"""DEVELOPMENT no-extra-query matching estimates, Codex (GPT-6)."""
import math
from matching_core import MatchingTree,IDENTITY,logadd


class EventTree(MatchingTree):
    def __init__(self,n):
        super().__init__(n)
        self.counts['interval_queries']=0

    def interval(self,a,b):
        self.counts['interval_queries']+=1
        if b-a<=1:return 0.
        left=a+self.size;right=b-1+self.size;front=IDENTITY;back=IDENTITY
        while left<right:
            if left%2:front=self.mul(front,self.tree[left]);left+=1
            if right%2:right-=1;back=self.mul(self.tree[right],back)
            left//=2;right//=2
        result=self.mul(front,back)
        return logadd(result[0],result[1])

    def event_probability(self,j,kind):
        denominator=logadd(self.tree[1][0],self.tree[1][1])
        numerator=self.interval(0,j)+self.interval(j+(2 if kind=='edge' else 1),self.n)
        if kind=='edge':numerator+=self.logweights[j]
        value=math.exp(numerator-denominator)
        assert -1e-12<=value<=1+1e-9,(j,kind,value)
        return min(1.,value)


class FreeLearner:
    def __init__(self,n,fees,horizon,rng):
        self.n=n;self.fees=fees;self.rng=rng;self.tree=EventTree(n)
        self.uniform=[1,1]
        for _ in range(2,n+1):self.uniform.append(self.uniform[-1]+self.uniform[-2])
        logN=math.log(self.uniform[n]);cmax=max(fees)
        self.gamma=min(.5,(3*logN/(4*horizon))**(1/3))
        self.eta=min(self.gamma/(5*cmax),math.sqrt(logN/(horizon*cmax*cmax*(3/self.gamma+2/(1-self.gamma)))))
        self.counts={'mixture_coins':0,'uniform_coins':0,'uniform_partition_additions':n-1,
                     'feedback_estimates':0,'nonzero_updates':0,'event_probability_evaluations':0}

    def sample(self):
        self.counts['mixture_coins']+=1
        uniform=self.rng.random()<self.gamma;j=0
        while j<self.n:
            if j<self.n-1:
                if uniform:
                    p=self.uniform[self.n-j-2]/self.uniform[self.n-j]
                    self.counts['uniform_coins']+=1
                else:
                    p=self.tree.swap_probability(j);self.tree.counts['coin_choices']+=1
                swap=self.rng.random()<p
            else:swap=False
            if swap:
                yield j+1,j,'edge';yield j,None,None;j+=2
            else:
                yield j,j,'singleton' if j<self.n-1 else None;j+=1

    def update(self,j,kind):
        self.counts['feedback_estimates']+=1
        if kind is None:return None
        self.counts['event_probability_evaluations']+=1
        q=self.tree.event_probability(j,kind)
        u=self.uniform[j]*self.uniform[self.n-j-(2 if kind=='edge' else 1)]/self.uniform[self.n]
        probability=(1-self.gamma)*q+self.gamma*u
        coefficient=(-self.fees[j]) if kind=='edge' else self.fees[j+1]
        estimate=coefficient/probability
        assert abs(self.eta*estimate)<=1+1e-10
        self.tree.update(j,-self.eta*estimate);self.counts['nonzero_updates']+=1
        return j,estimate,probability
