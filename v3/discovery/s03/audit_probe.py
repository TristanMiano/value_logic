"""Small exact validity screens plus labelled synthetic acquisition costs."""
import hashlib,json,math,random,sys,time
from fractions import Fraction as F
from pathlib import Path
from audit_factor import factor

def serial(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [serial(v) for v in x]
    return x

def main(out):
    assert not out.exists();base=Path(__file__).parent;start=time.perf_counter_ns();seed=42168;rng=random.Random(seed)
    sources={p:hashlib.sha256((base/p).read_bytes()).hexdigest() for p in ['audit_factor.py','audit_probe.py']}
    checks=0
    for m in (F(1,4),F(1,2),F(3,4)):
        for b in (F(0),F(1,4),F(1,2),F(1)):
            for lam in (F(1,8),F(1,2),F(1)):
                minimum=lam*b/(1+lam*(b-m))
                for p in (max(minimum,F(1,16)),(1+minimum)/2,F(1)):
                    for y in (F(0),F(1,3),F(1)):
                        fs=[factor(b,p,r,y,lam,m) for r in (0,1)]
                        assert (1-p)*fs[0]+p*fs[1]==1+lam*(y-m)
                        assert factor(b,p,1,F(0),lam,m)<=fs[1]
                        checks+=1
    # Fully enumerate a short adaptive tree under a fair null. Controller uses
    # only previous audited data; a current-feature forecast need not be true.
    states=[(F(1),F(1),0,0)];tree=[]
    for t in range(5):
        future=[]
        for mass,wealth,ones,count in states:
            b=F(ones+1,count+2);p=F(1,2);lam=F(1,2);m=F(1,2)
            for y in (F(0),F(1)):
                for r in (0,1):
                    value=wealth*factor(b,p,r,y,lam,m)
                    future.append((mass/4,value,ones+int(y)*r,count+r))
        states=future;expectation=sum(mass*w for mass,w,_,_ in states)
        assert expectation==1
        tree.append(dict(depth=t+1,paths=len(states),expected_wealth=expectation))
    # A frozen, actual coefficient history with truth-dependent lower receipts.
    ledger=[];ones=0;count=0
    for t in range(96):
        x=rng.randrange(16);y=F(x<12);b=F(ones+1,count+2);p=F(1,2);r=int(rng.randrange(2)==0)
        lower=y if x%3==0 else F(0);lam=F(1,2)
        ledger.append(dict(x=x,y=y,b=b,p=p,r=r,lam=lam,initial_lower=lower))
        if r:ones+=int(lower);count+=1
    full=partial=F(1)
    for row in ledger:
        full*=factor(row['b'],row['p'],row['r'],row['y'],row['lam'],F(1,2))
        partial*=factor(row['b'],row['p'],row['r'],row['initial_lower'],row['lam'],F(1,2))
    assert partial<=full
    refinements=[];previous=partial
    for upto in (24,48,72,96):
        value=F(1)
        for i,row in enumerate(ledger):
            lower=row['y'] if i<upto else row['initial_lower']
            value*=factor(row['b'],row['p'],row['r'],lower,row['lam'],F(1,2))
        assert previous<=value<=full;previous=value
        refinements.append(dict(refined_prefix=upto,wealth=value))
    assert previous==full
    negative=dict(current_label_bet_expected_factor=F(5,4),retrofitted_forecast_expected_factor=F(9,8),unsafe_small_audit_factor=F(-17,2))
    # Exact counterexamples: fair Y, lambda(Y)=Y; and p=1/2,lambda=1/2,
    # old b retrospectively set to Y only on audited rows, otherwise b=1.
    assert sum(1+y*(y-F(1,2)) for y in (F(0),F(1)))/2==negative['current_label_bet_expected_factor']
    retrofit=sum(1+F(1,2)*((y if r else F(1))-F(1,2)) for y in (F(0),F(1)) for r in (0,1))/4
    assert retrofit==negative['retrofitted_forecast_expected_factor']
    assert 1+(1+(0-1)/F(1,10)-F(1,2))==negative['unsafe_small_audit_factor']
    # Supplied population, not real solver cost. All paths and censoring are
    # developmental. The same contexts/coins support each displayed method.
    experiments=[]
    for k in range(32):
        xs=[rng.randrange(16) for _ in range(1024)];coins=[rng.random() for _ in xs];rows=[]
        for method in ['full','perfect','imperfect','inverted','online_groups']:
            logw=0.0;audits=0;group_ones=[0]*4;group_count=[0]*4;cross=False
            for t,(x,u) in enumerate(zip(xs,coins),1):
                y=float(x<12);group=x//4
                if method=='full':p=1.0;lam=1.0;b=0.0
                else:
                    p=0.25;lam=0.25
                    if method=='perfect':b=y
                    elif method=='imperfect':b=float((x<12) != (x in (3,15)))
                    elif method=='inverted':b=1-y
                    else:b=(group_ones[group]+1)/(group_count[group]+2)
                r=int(u<p);audits+=r
                z=b+r*(y-b)/p;f=1+lam*(z-0.5);assert f>0
                logw+=math.log(f)
                if r:group_ones[group]+=y;group_count[group]+=1
                if logw>=math.log(20):cross=True;break
            rows.append(dict(method=method,draws=t,audits=audits,crossed=cross,log_wealth=logw,
                charged_units=audits+(0 if method=='full' else 0.01*t)))
        experiments.append(dict(index=k,context_sha256=hashlib.sha256(json.dumps(xs).encode()).hexdigest(),rows=rows))
    summary=[]
    for method in ['full','perfect','imperfect','inverted','online_groups']:
        rs=[next(r for r in e['rows'] if r['method']==method) for e in experiments]
        summary.append(dict(method=method,crossings=sum(r['crossed'] for r in rs),paths=len(rs),mean_capped_audits=sum(r['audits'] for r in rs)/len(rs),mean_capped_charged_units=sum(r['charged_units'] for r in rs)/len(rs)))
    result=dict(status='complete',evidence='DEVELOPMENT',contributor='Codex (GPT-6)',python=sys.version,seed=seed,sources=sources,
        exact_one_step_checks=checks,adaptive_null_tree=tree,delayed_ledger=ledger,initial_partial_wealth=partial,full_wealth=full,refinements=refinements,negative_examples=negative,
        experiments=experiments,summary=summary,elapsed_ns=time.perf_counter_ns()-start,
        cost_scope='Synthetic unit audit price 1 and supplied forecast price .01; no measured external evaluator or model construction cost. Full lambda=1 is optimal for Bernoulli(.75) vs .5. Other arms use safe lambda=.25, p=.25. All capped paths retained.',
        limitation='Single exposed developmental simulation, not calibrated type-I confirmation or real-resource usefulness. Exact rational checks and float simulation distinct. Identical ordinary prediction-powered procedure is a comparator.')
    out.write_text(json.dumps(serial(result),indent=2)+'\n')
    print(json.dumps(dict(status='complete',exact_checks=checks,adaptive_tree_paths=len(states),delayed_refinements=len(refinements),summary=summary,elapsed_ns=result['elapsed_ns'])))

if __name__=='__main__':main(Path(sys.argv[1]))
