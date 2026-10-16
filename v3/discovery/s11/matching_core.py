"""DEVELOPMENT sparse matching weights, Codex (GPT-6)."""
import math

NEG=-math.inf
IDENTITY=(0.,NEG,NEG,0.)


def logadd(a,b):
    if a==NEG:return b
    if b==NEG:return a
    if a<b:a,b=b,a
    return a+math.log1p(math.exp(b-a))


def multiply(a,b):
    return (logadd(a[0]+b[0],a[1]+b[2]),logadd(a[0]+b[1],a[1]+b[3]),
            logadd(a[2]+b[0],a[3]+b[2]),logadd(a[2]+b[1],a[3]+b[3]))


class MatchingTree:
    def __init__(self,n):
        assert n>=2
        self.n=n;self.size=1
        while self.size<n-1:self.size*=2
        self.logweights=[0.]*(n-1);self.tree=[IDENTITY]*(2*self.size)
        self.counts={'matrix_products':0,'updates':0,'suffix_queries':0,'coin_choices':0}
        for j in range(n-1):self.tree[self.size+j]=(0.,0.,0.,NEG)
        for j in range(self.size-1,0,-1):self.tree[j]=self.mul(self.tree[2*j],self.tree[2*j+1])

    def mul(self,a,b):
        self.counts['matrix_products']+=1
        return multiply(a,b)

    def update(self,j,increment):
        self.counts['updates']+=1;self.logweights[j]+=increment
        k=self.size+j;self.tree[k]=(0.,self.logweights[j],0.,NEG)
        while k>1:
            k//=2;self.tree[k]=self.mul(self.tree[2*k],self.tree[2*k+1])

    def suffix(self,j):
        self.counts['suffix_queries']+=1
        if j>=self.n-1:return 0.
        left=j+self.size;right=self.n-1+self.size
        front=IDENTITY;back=IDENTITY
        while left<right:
            if left%2:front=self.mul(front,self.tree[left]);left+=1
            if right%2:right-=1;back=self.mul(self.tree[right],back)
            left//=2;right//=2
        answer=self.mul(front,back)
        return logadd(answer[0],answer[1])

    def swap_probability(self,j):
        if j>=self.n-1:return 0.
        result=math.exp(self.logweights[j]+self.suffix(j+2)-self.suffix(j))
        assert -1e-12<=result<=1+1e-9,(j,result)
        return min(1.,result)

    def sample_lazy(self,rng):
        j=0
        while j<self.n:
            if j<self.n-1:
                self.counts['coin_choices']+=1
                swap=rng.random()<self.swap_probability(j)
            else:swap=False
            if swap:
                yield j+1;yield j;j+=2
            else:
                yield j;j+=1


def matching_orders(n):
    if n==0:return [((),())]
    if n==1:return [((0,),())]
    out=[]
    for order,edges in matching_orders(n-1):
        out.append(((0,)+tuple(i+1 for i in order),tuple(j+1 for j in edges)))
    for order,edges in matching_orders(n-2):
        out.append(((1,0)+tuple(i+2 for i in order),(0,)+tuple(j+2 for j in edges)))
    return out


def sparse_delta(observed,n,fees,stop):
    receipts={};L=0;reference=0
    while L<n and not stop(receipts):
        receipts[L]=observed[L];reference+=fees[L];L+=1
    if not stop(receipts):return {},reference,False
    result={}
    for j in (L-2,L-1):
        if j<0 or j>=n-1:continue
        prefix={i:observed[i] for i in range(j)}
        A=int(stop(prefix|{j:observed[j]}))
        B=int(stop(prefix|{j+1:observed[j+1]}))
        delta=fees[j+1]*A-fees[j]*B
        if delta:result[j]=delta
    return result,reference,True
