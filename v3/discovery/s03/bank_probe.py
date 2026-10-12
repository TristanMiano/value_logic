"""Small checked-arithmetic and explicitly supplied partial-value example."""
from decimal import Decimal,localcontext
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,random,sys,time
from bank_bounds import log_interval,certificate,propose


def serial(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [serial(v) for v in x]
    return x


def main(out):
    assert not out.exists();start=time.perf_counter_ns();checks=[];rng=random.Random(15916)
    for k in range(-60,61,3):
        x=(F(2)**k)*F(rng.randrange(1,100),rng.randrange(1,100));lo,hi=log_interval(x)
        with localcontext() as ctx:
            ctx.prec=100;ref=(Decimal(x.numerator)/Decimal(x.denominator)).ln()
            assert Decimal(lo.numerator)/Decimal(lo.denominator)<=ref<=Decimal(hi.numerator)/Decimal(hi.denominator)
        a,b=log_interval(1/x);assert lo+a<=0<=hi+b
        checks.append({'x':x,'lower':lo,'upper':hi,'decimal_reference':str(ref)})
    N,K=48,6
    # A supplied developmental value table, not a measured external evaluator.
    truth=[[min(F(1),max(F(0),F(rng.randrange(-3,4),8)+F(2+theta,8))) for _ in range(N)] for theta in range(K)]
    means=[sum(row)/N for row in truth];P=(F(1,K),)*K;lam=F(1,2);alpha=F(1,20)
    samples=[];levels=[[F(0)]*N for _ in range(K)];stages=[];partial_releases=upgrades=0
    def sums():return [sum(levels[g][i]*truth[g][i] for i in samples) for g in range(K)]
    def snapshot(kind):
        begin=time.perf_counter_ns();S=sums();Q=propose(S,P,lam);proposal=time.perf_counter_ns()-begin
        begin=time.perf_counter_ns();bound=certificate(S,len(samples),Q,P,lam,alpha);checking=time.perf_counter_ns()-begin
        actual=sum(q*mu for q,mu in zip(Q,means))
        row={'kind':kind,'draws':len(samples),'unique_contexts':len(set(samples)),'sums':S,'posterior':Q,'bound':bound,
             'diagnostic_true_mixture_mean':actual,'realized_bound_valid':bound['lower']<=actual,'proposal_and_sum_ns':proposal,'bound_check_ns':checking,
             'partial_release_events':partial_releases,'upgrade_events':upgrades}
        stages.append(row);return Q
    for t in range(1,257):
        i=rng.randrange(N);samples.append(i)
        for g in range(K):
            if levels[g][i]==0:levels[g][i]=F(1,2);partial_releases+=1
        if t in (16,32,64,128,256):
            Q=snapshot('partial');chosen=max(range(K),key=lambda g:Q[g])
            for i in set(samples):
                if levels[chosen][i]<1:levels[chosen][i]=F(1);upgrades+=1
            snapshot('delayed_upgrade')
    result={'status':'complete','evidence':'DEVELOPMENT','contributor':'Codex (GPT-6)','seed':15916,'python':sys.version,
            'sources':{p:hashlib.sha256(Path(__file__).with_name(p).read_bytes()).hexdigest() for p in ('bank_bounds.py','bank_probe.py')},
            'log_checks':checks,'truth':truth,'population_means':means,'prior':P,'lambda':lam,'alpha':alpha,'sampled_contexts':samples,'stages':stages,
            'cost_scope':'Supplied value table and artificial half/full receipt releases; release/upgrade counts are events, not measured solver effort. Timings cover advice/sum and bound arithmetic only.',
            'statistical_scope':'One exposed source/path; realized bound checks do not validate the general confidence level.',
            'elapsed_ns':time.perf_counter_ns()-start}
    out.write_text(json.dumps(serial(result),indent=2)+'\n',encoding='utf-8')
    print(json.dumps(serial({'status':'complete','log_checks':len(checks),'stages':[{k:s[k] for k in ('kind','draws','diagnostic_true_mixture_mean','realized_bound_valid','bound_check_ns')}|{'lower':s['bound']['lower']} for s in stages],'elapsed_ns':result['elapsed_ns']})))


if __name__=='__main__':main(Path(sys.argv[1]))
