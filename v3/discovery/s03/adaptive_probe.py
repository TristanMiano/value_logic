"""Cheap tree/closure comparison and matching obstruction, Codex GPT-6."""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import hashlib,json,random,sys,time
from adaptive_value import adaptive,closure_upper,relaxation,midpoint,conditional


def serial(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [serial(v) for v in x]
    return x


def matching():
    def search(remaining,counts,edges):
        if not remaining:return edges if counts==[2]*4 else None
        x=min(remaining)
        for j in range(4):
            y=x^(1<<j)
            if y not in remaining or counts[j]>=2:continue
            new=counts.copy();new[j]+=1
            found=search(remaining-{x,y},new,edges+[(x,y,j)])
            if found is not None:return found
        return None
    result=search(set(range(16)),[0]*4,[]);assert result is not None
    return result


def main(out):
    assert not out.exists();rng=random.Random(19583);start=time.perf_counter_ns();rows=[]
    for case in range(36):
        m=rng.randrange(1,6);polys=[]
        for _ in range(rng.randrange(2,5)):
            p={0:F(rng.randrange(-3,4),8)}
            for _ in range(rng.randrange(1,6)):
                mask=rng.randrange(1,1<<m);p[mask]=p.get(mask,F(0))+F(rng.randrange(-4,5),8)
            polys.append({mask:a for mask,a in p.items() if a})
        prices=[F(rng.randrange(1,9),16) for _ in range(m)];truth=adaptive(polys,prices)
        baselines=[{},midpoint(polys)]+[{mask:a for mask,a in p.items() if mask} for p in polys]
        bounds=[]
        for b in baselines:
            upper=closure_upper(polys,prices,b);tight=relaxation(polys,prices,b)
            assert truth['gain']<=tight['upper']<=upper['upper']
            bounds.append(dict(baseline=b,closure=upper,relaxation=tight))
        rows.append(dict(m=m,polys=polys,prices=prices,oracle=truth,bounds=bounds))
    polys=[{1:F(1),2:F(1)},{1:F(-1),2:F(1)},{2:F(-1)}];prices=[F(2,5)]*2;b={2:F(3,10)}
    sharp=dict(polys=polys,prices=prices,baseline=b,oracle=adaptive(polys,prices),upper=closure_upper(polys,prices,b),relaxation=relaxation(polys,prices,b))
    assert sharp['oracle']['gain']==sharp['upper']['upper']==F(9,10)
    edges=matching();labels=[None]*16
    for label,(x,y,j) in enumerate(edges):labels[x]=labels[y]=label
    polys=[]
    for a in range(8):
        p={mask:F(sum((1 if labels[x]==a else 0)*(-1 if (mask&x).bit_count()%2 else 1) for x in range(16)),16) for mask in range(16)}
        polys.append({mask:v for mask,v in p.items() if v})
    q=F(1,100);truth=adaptive(polys,[q]*4)
    @lru_cache(None)
    def queries(A,v):
        worlds=[x for x in range(16) if x&A==v]
        if len({labels[x] for x in worlds})==1:return F(0)
        return 1+min((queries(A|(1<<j),v)+queries(A|(1<<j),v|(1<<j)))/2 for j in range(4) if not A&(1<<j))
    query_cost=queries(0,0);assert query_cost>3 and truth['value']==1-q*query_cost
    # Matching-cell projections preserve expectation for every Fourier basis function,
    # hence by linearity every function g on this finite world space.
    projection=[]
    for mask in range(1,16):
        total=sum(conditional({mask:F(1)},15^(1<<j),x)+conditional({mask:F(1)},15^(1<<j),y) for x,y,j in edges)
        assert total==0;projection.append(total)
    partition=dict(edges=edges,labels=labels,polys=polys,price=q,oracle=truth,minimum_expected_queries=query_cost,
        anticipatory_partition_value=1-3*q,unavoidable_restricted_dual_gap=(1-3*q)-truth['value'],basis_projection_sums=projection,
        proof_scope='All zero-mean terminal common-baseline projections miss at least this gap, because the nonsequential matching partition preserves all their expectations.')
    result=dict(status='complete',evidence='DEVELOPMENT',contributor='Codex (GPT-6)',python=sys.version,seed=19583,
        sources={p:hashlib.sha256(Path(__file__).with_name(p).read_bytes()).hexdigest() for p in ['acquire_flow.py','contrast_plan.py','adaptive_value.py','adaptive_probe.py']},
        random_cases=rows,sharp_example=sharp,partition_obstruction=partition,elapsed_ns=time.perf_counter_ns()-start)
    out.write_text(json.dumps(serial(result),indent=2)+'\n')
    print(json.dumps(serial(dict(status='complete',random_cases=len(rows),sharp_value=sharp['oracle']['gain'],matching_edges=edges,
        minimum_expected_queries=query_cost,partition_value=partition['anticipatory_partition_value'],adaptive_value=truth['value'],dual_gap=partition['unavoidable_restricted_dual_gap'],elapsed_ns=result['elapsed_ns']))))


if __name__=='__main__':main(Path(sys.argv[1]))
