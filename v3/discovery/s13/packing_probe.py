"""Exact cap-three oracle for a genuine fractional/support gap, <=60s budget."""
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import time

HERE=Path(__file__).resolve().parent


def main():
    began=time.perf_counter_ns()
    forms=tuple(range(9,16)); target=8
    worlds=tuple(range(16)); allmask=(1<<16)-1
    parity=lambda a,x:(a&x).bit_count()%2
    ones={a:sum(1<<x for x in worlds if parity(a,x)) for a in forms}
    target_ones=sum(1<<x for x in worlds if parity(target,x))
    assert all(a!=target for a in forms)
    assert all(a^b!=target for a,b in combinations(forms,2))
    assert any(a^b^c==target for a,b,c in combinations(forms,3))
    assert all(sum(parity(a,u|8) for u in range(1,8))==3 for a in forms)
    assert all(sum(parity(a,u|8) for a in forms)>=3 for u in range(8))
    maps=set()
    for root in forms:
        options=[(allmask,0,0),(0,allmask,0),(0,0,allmask)]
        for second in forms:
            if second!=root:
                options.extend([(0,ones[second],allmask^ones[second]),
                                (0,allmask^ones[second],ones[second])])
        for left,right in product(options,repeat=2):
            masks=tuple((left[k]&(allmask^ones[root]))|(right[k]&ones[root])
                        for k in range(3))
            assert masks[0]|masks[1]|masks[2]==allmask
            maps.add(masks)
    maps=sorted(maps);examined=0;chosen={}

    @lru_cache(None)
    def value(w):
        nonlocal examined
        if time.perf_counter_ns()-began>60_000_000_000:
            raise TimeoutError('prospective60 second scientific budget')
        if not(w&target_ones) or not(w&(allmask^target_ones)):return 0
        best=10**9;choice=None;distinct=set()
        for m in maps:
            groups=tuple(w&x for x in m)
            if w in groups or groups in distinct:continue
            distinct.add(groups);examined+=1
            immediate=sum((k+1)*g.bit_count() for k,g in enumerate(groups))
            if immediate>=best:continue
            total=immediate+sum(value(g) for g in groups if g)
            if total<best:best,choice=total,groups
        assert choice is not None
        chosen[w]=choice
        return best

    total=value(allmask)
    out=dict(status='PASS',contributor='Codex (GPT-6)',forms=forms,target=target,
             shortest_support=3,packing='7/3',packing_invoice_lower='49/18',
             ordinary_query_lower=3,worlds=16,count_maps=len(maps),
             states=value.cache_info().currsize,examined_splits=examined,
             expected_fee_numerator=total,expected_fee_denominator=16,
             expected_fee=total/16,conjectured_support_lower='7/2',
             root_groups=[[x for x in worlds if g>>x&1] for g in chosen[allmask]],
             elapsed_ns=time.perf_counter_ns()-began,
             source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             scope='Finite exact ordinary oracle; packing gap is analytic; no general theorem')
    (HERE/'packing_probe.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out))


if __name__=='__main__':main()
