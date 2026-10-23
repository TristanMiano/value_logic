"""High-precision illustration of a finite risk-budget frontier."""
from decimal import Decimal as D, getcontext, ROUND_CEILING
from hashlib import sha256
from pathlib import Path
import json
import time

getcontext().prec=90
HERE=Path(__file__).resolve().parent
ONE=D(1); N=D(1000); ETA=ONE; DELTA=D('.05'); A=ONE-(-ONE).exp()

def kl(q):
    return ((q*(2*q).ln()) if q else D(0))+(((1-q)*(2*(1-q)).ln()) if q<1 else D(0))

def run(scheap, eps):
    se=D(10); sc=D(scheap); epsilon=D(eps)
    K=-N*(1-A*epsilon).ln()-(1/DELTA).ln()
    def j(q):
        return kl(q)+q*se+(1-q)*sc
    def bound(q):
        return (1-(-(j(q)+(1/DELTA).ln())/N).exp())/A
    q0=ONE/(ONE+(se-sc).exp())
    assert j(q0)<=K
    if j(D(0))<=K:
        q=D(0)
    else:
        lo=D(0); hi=q0
        for _ in range(250):
            mid=(lo+hi)/2
            if j(mid)<=K:
                hi=mid
            else:
                lo=mid
        q=(hi*10**6).to_integral_value(rounding=ROUND_CEILING)/10**6
    assert j(q)<=K
    # Independently inspect the Gibbs curve's two monotone quantities.
    lastc=D('Infinity'); lastj=D('-Infinity')
    for i in range(101):
        beta=D(i)/100
        qb=ONE/(ONE+(se-sc+99*beta).exp())
        cb=1+99*qb; jb=j(qb)
        assert cb<=lastc and jb>=lastj-D('1e-75')
        lastc,lastj=cb,jb
    return dict(cheap_loss_upper_sum=scheap,risk_target=eps,
                expensive_probability=str(q),certified_mean_cost=str(1+99*q),
                risk_bound=str(bound(q)),risk_slack=str(epsilon-bound(q)),
                cheap_only_risk_bound=str(bound(D(0))),
                expensive_only_risk_bound=str(bound(D(1))))

def main():
    start=time.perf_counter_ns()
    cases=[run(sc,eps) for sc in (30,35,40,45) for eps in ('.04','.05','.06','.07')]
    for eps in ('.04','.05','.06','.07'):
        values=[D(x['certified_mean_cost']) for x in cases if x['risk_target']==eps]
        assert values==sorted(values)
    out=dict(status='PASS',attribution='Codex (GPT-6), DEVELOPMENT',
             source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
             elapsed_ns=time.perf_counter_ns()-start,cases=cases,
             note='Separate fixed two-policy prior (1/2,1/2), exact declared costs (100,1). Decimal illustration, not outward interval certification or an operational workload.')
    (HERE/'program_probe.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2))

if __name__=='__main__':
    main()
