"""Exact supplied-table checks for the depth-limited moment controller."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,random,sys,time
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from moment_values import acquire_from_table,plan
from continuation import System,solve


def explicit(m,counts,rows,prices,h,available=None):
    allowed=[i for i in range(m) if available is None or available&(1<<i)]
    costs=tuple(tuple(row[0]+sum(row[i+1]*(1 if not x&(1<<i) else -1) for i in range(m)) for row in rows) for x in range(1<<m))
    system=System(costs,tuple(tuple(prices[i] for i in allowed) for _ in range(1<<m)),
                  tuple(tuple(int(bool(x&(1<<i))) for i in allowed) for x in range(1<<m)),tuple((x,)*len(allowed) for x in range(1<<m)))
    v,first,beliefs=solve(system,tuple(F(w,sum(counts)) for w in counts),h)
    first=tuple(('e'+str(allowed[int(k[1:])])) if k.startswith('e') else k for k in first)
    return v,first,beliefs


def compare(m,counts,rows,prices,h,available=None):
    start=time.perf_counter_ns();moments=acquire_from_table(counts,m,min(m,h+1));acquisition=time.perf_counter_ns()-start
    start=time.perf_counter_ns();small=plan(moments,m,rows,prices,h,available);small_ns=time.perf_counter_ns()-start
    start=time.perf_counter_ns();full=explicit(m,counts,rows,prices,h,available);full_ns=time.perf_counter_ns()-start
    assert small['value']==full[0]
    # Repeated known-bit probes are omitted by the moment controller. At strictly
    # positive prices, such repetitions cannot tie the optimum at the root.
    assert set(small['first_choices'])==set(full[1]),(small,full)
    return {'m':m,'horizon':h,'counts':counts,'terminal':[[str(v) for v in row] for row in rows],
            'prices':list(map(str,prices)),'available_mask':available,
            'value':str(full[0]),'first_choices':list(full[1]),'features':len(moments),'states':1<<m,
            'source_feature_acquisition_ns':acquisition,'moment_plan_ns':small_ns,'explicit_build_and_plan_ns':full_ns,
            'moment_beliefs':small['beliefs'],'explicit_beliefs':full[2],'zero_branches_skipped':small['zero_branches_skipped']}


def main(out):
    assert not out.exists();start=time.perf_counter_ns();rng=random.Random(12613);cases=[]
    for i in range(60):
        m=rng.randrange(2,8);h=rng.randrange(3);counts=[rng.randrange(0,7) for _ in range(1<<m)]
        rows=[tuple(F(rng.randrange(-3,4)) for _ in range(m+1)) for _ in range(2)]
        prices=tuple(F(rng.randrange(1,5),5) for _ in range(m))
        cases.append(compare(m,counts,rows,prices,h))
    rows=((F(0),F(1),F(1)),(F(0),F(0),F(0)))
    pair=[compare(2,c,rows,(F(1,4),)*2,1) for c in ([1,0,0,1],[0,1,1,0])]
    assert pair[0]['value']=='-3/4' and pair[1]['value']=='0'
    parity=[]
    for m in (2,3,4,5):
        h=m-1;rows=[tuple([F(1,2)]+[F(0)]*(m-1)+[F(s,2)]) for s in (-1,1)]
        inputs=[[int(x.bit_count()%2==parity) for x in range(1<<m)] for parity in (0,1)]
        low=[acquire_from_table(c,m,h) for c in inputs];assert low[0]==low[1]
        for counts in inputs:
            row=compare(m,counts,rows,(F(1,10*m),)*m,h,(1<<h)-1)
            assert F(row['value'])==F(h,10*m);parity.append(row)
    delta=compare(4,[1]+[0]*15,((F(0),F(1),F(0),F(0),F(0)),(F(0),)*5),(F(1,10),)*4,2)
    assert delta['zero_branches_skipped']>0
    sources={'moment_values.py':hashlib.sha256(Path(__file__).parent.parent.joinpath('moment_values.py').read_bytes()).hexdigest(),
             's03/moment_probe.py':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             's03/continuation.py':hashlib.sha256(Path(__file__).with_name('continuation.py').read_bytes()).hexdigest()}
    result={'status':'complete','evidence':'DEVELOPMENT','contributor':'Codex (GPT-6)','seed':12613,'python':sys.version,
            'sources':sources,'random_cases':cases,'pair':pair,'parity':parity,'point_mass':delta,'elapsed_ns':time.perf_counter_ns()-start}
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':'complete','random_cases':len(cases),'pair_values':[x['value'] for x in pair],
                      'parity_cases':len(parity),'point_mass_zero_branches':delta['zero_branches_skipped'],'elapsed_ns':result['elapsed_ns']}))


if __name__=='__main__':main(Path(sys.argv[1]))
