"""Cheap exposed arithmetic/support development, not statistical confirmation."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,random,sys,time
from bank_bounds import certificate as old_certificate
from bank_compact import certificate,support


def serial(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [serial(v) for v in x]
    return x


def main(out):
    assert not out.exists();rng=random.Random(48153);begin=time.perf_counter_ns();rows=[]
    source=Path(__file__).with_name('bank01.json');old=json.loads(source.read_text())
    replay=[]
    for s in old['stages']:
        S=list(map(F,s['sums']));Q=tuple(map(F,s['posterior']));P=tuple(map(F,old['prior']));t=s['draws'];lam=F(old['lambda']);alpha=F(old['alpha'])
        start=time.perf_counter_ns();v=certificate(S,t,Q,P,lam,alpha);elapsed=time.perf_counter_ns()-start
        prev=F(s['bound']['lower']);loss=prev-v
        assert 0<=loss<=F(2,1<<40)/(lam*t)
        replay.append(dict(t=t,old_chars=len(str(prev)),new_chars=len(str(v)),loss=loss,ns=elapsed))
    for case in range(100):
        K=rng.randrange(2,10);t=rng.choice([16,32,64,128,256]);P=(F(1,K),)*K;lam=F(1,2);alpha=F(1,20)
        S=[F(rng.randrange(t*8+1),8) for _ in P];w=[F(rng.randrange(-6,13),8) for _ in P]
        start=time.perf_counter_ns();r=support(S,t,P,lam,alpha,w);elapsed=time.perf_counter_ns()-start
        if r['diagnostic']['constraint_active']:
            primal=r['diagnostic']['numerical_primal'];gap=primal-float(r['lower'])
            assert -1e-10<=gap<2e-4,(case,gap)
        else:gap=0
        assert r['lower']<=sum(x for x in w if x>0)
        rows.append(dict(case=case,t=t,sums=S,weights=w,prior=P,lambda_=lam,alpha=alpha,result=r,advice_check_ns=elapsed,numerical_dual_gap=gap))
    examples=[]
    for w in [(F(1),F(1)),(F(1),F(-1)),(F(1,100),F(1))]:
        r=support([F(128),F(0)],128,(F(1,2),)*2,F(1,2),F(1,20),w)
        examples.append(dict(weights=w,result=r))
    result=dict(status='complete',evidence='DEVELOPMENT',contributor='Codex (GPT-6)',python=sys.version,seed=48153,
        sources={p:hashlib.sha256(Path(__file__).with_name(p).read_bytes()).hexdigest() for p in ['bank_bounds.py','bank_compact.py','support_probe.py']},
        reused_bank_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),dyadic_replay=replay,queries=rows,examples=examples,
        scope='Exact algebraic checks plus floating primal diagnostics. No independent optimizer, statistical coverage validation, acquisition economy or confirmation.',elapsed_ns=time.perf_counter_ns()-begin)
    out.write_text(json.dumps(serial(result),indent=2)+'\n')
    print(json.dumps(serial(dict(status='complete',replays=len(replay),queries=len(rows),max_numerical_gap=max(r['numerical_dual_gap'] for r in rows),examples=examples,elapsed_ns=result['elapsed_ns']))))


if __name__=='__main__':main(Path(sys.argv[1]))
