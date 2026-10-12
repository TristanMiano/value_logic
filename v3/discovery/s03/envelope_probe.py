"""A declared-box flow service; source construction and membership are charged."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,random,sys,time
from flow_v2 import exact,check


def serial(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [serial(v) for v in x]
    return x


def digest(x):return hashlib.sha256(json.dumps(serial(x),sort_keys=True,separators=(',',':')).encode()).hexdigest()


def prepare(masks,reward_high,price_low,version):
    terms=tuple(zip(masks,reward_high));prices=tuple(price_low)
    allocation,witness=exact(terms,prices);bound=check(terms,prices,allocation)
    # Capture immutable state only after checking the certificate.
    hi=tuple(reward_high);lo=tuple(price_low);identity=version;upper=bound['upper']
    def answer(rewards,query_prices,query_version):
        assert query_version==identity and len(rewards)==len(hi) and len(query_prices)==len(lo)
        assert all(isinstance(r,F) and 0<=r<=h for r,h in zip(rewards,hi))
        assert all(isinstance(q,F) and q>=l for q,l in zip(query_prices,lo))
        return upper
    return answer,dict(allocation=allocation,flow_witness=witness,bound=bound,graph_version=version)


def main(out):
    assert not out.exists();base=Path(__file__).parent;source=base/'flow01.json';old=json.loads(source.read_text());row=old['workloads'][0]
    start=time.perf_counter_ns();masks=[mask for mask,_ in row['terms']];rewards0=[F(r) for _,r in row['terms']];prices0=list(map(F,row['prices']))
    hi=[r+F(1,2) for r in rewards0];lo=[max(F(0),q-F(1,2)) for q in prices0];version=digest(dict(masks=masks,meaning='fixed supplied primitive and term identities'))
    begin=time.perf_counter_ns();answer,certificate=prepare(masks,hi,lo,version);prepare_ns=time.perf_counter_ns()-begin
    seed=16393;rng=random.Random(seed);queries=[]
    for i in range(96):
        rewards=[max(F(0),r+F(rng.randrange(-32,33),64)) for r in rewards0]
        prices=[max(F(0),q+F(rng.randrange(-32,33),64)) for q in prices0]
        begin=time.perf_counter_ns();upper=answer(rewards,prices,version);membership_ns=time.perf_counter_ns()-begin
        begin=time.perf_counter_ns();a,w=exact(list(zip(masks,rewards)),prices);oracle=check(list(zip(masks,rewards)),prices,a)['upper'];cold_ns=time.perf_counter_ns()-begin
        assert oracle<=upper
        queries.append(dict(index=i,input_sha256=digest(dict(rewards=rewards,prices=prices,version=version)),upper=upper,oracle=oracle,
            membership_ns=membership_ns,cold_exact_and_check_ns=cold_ns))
    rejected=[]
    for label,r,q,v in [('wrong_version',rewards0,prices0,'different'),('reward_above_box',[hi[0]+1]+rewards0[1:],prices0,version),('price_below_box',rewards0,[lo[0]-1]+prices0[1:],version)]:
        try:answer(r,q,v)
        except AssertionError:rejected.append(label)
        else:raise AssertionError('invalid query accepted')
    result=dict(status='complete',evidence='DEVELOPMENT',contributor='Codex (GPT-6)',python=sys.version,seed=seed,
        sources={p:hashlib.sha256((base/p).read_bytes()).hexdigest() for p in ['flow_v2.py','envelope_probe.py']},reused_input_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        graph_masks=masks,base_rewards=rewards0,base_prices=prices0,reward_high=hi,price_low=lo,certificate=certificate,preparation_ns=prepare_ns,queries=queries,rejected_queries=rejected,
        reconstruction='The saved seed, interpreter version and source regenerate all 96 query arrays in order; each canonical input SHA256 is recorded. The envelope is constructed before this lottery.',
        source_and_all_queries_ns=prepare_ns+sum(r['membership_ns'] for r in queries),cold_all_queries_ns=sum(r['cold_exact_and_check_ns'] for r in queries),elapsed_ns=time.perf_counter_ns()-start,
        limits='Fixed supplied graph and tariff/reward envelope; ordinary flow-envelope service is identical. Cold recomputation is a narrower comparison. Source semantic authentication and external deployment costs not measured. One exposed trace, not confirmation.')
    out.write_text(json.dumps(serial(result),indent=2)+'\n')
    print(json.dumps(serial(dict(status='complete',queries=len(queries),envelope_upper=certificate['bound']['upper'],all_queries_exact=sum(q['oracle']==q['upper'] for q in queries),
        preparation_ns=prepare_ns,source_and_all_queries_ns=result['source_and_all_queries_ns'],cold_all_queries_ns=result['cold_all_queries_ns'],rejected=rejected,elapsed_ns=result['elapsed_ns']))))


if __name__=='__main__':main(Path(sys.argv[1]))
