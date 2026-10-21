"""Exact small cap-three oracle; prospective under60s, one linear source."""
from functools import lru_cache
from itertools import combinations,product
from pathlib import Path
import hashlib
import json
import time

HERE=Path(__file__).resolve().parent


def main():
    began=time.perf_counter_ns()
    forms=(1,2,4,8,9,10,12)
    target=7
    worlds=tuple(range(16))
    allmask=(1<<16)-1
    ones={a:sum(1<<x for x in worlds if (a&x).bit_count()%2) for a in forms}
    target_ones=sum(1<<x for x in worlds if (target&x).bit_count()%2)
    shortest=None
    for k in range(1,len(forms)+1):
        for subset in combinations(forms,k):
            value=0
            for a in subset:
                value^=a
            if value==target:
                shortest=k
                break
        if shortest is not None:
            break
    maps=set()
    for root in forms:
        options=[(allmask,0,0),(0,allmask,0),(0,0,allmask)]
        for second in forms:
            if second!=root:
                options += [(0,ones[second],allmask^ones[second]),
                            (0,allmask^ones[second],ones[second])]
        for left,right in product(options,repeat=2):
            masks=tuple((left[k]&(allmask^ones[root]))|(right[k]&ones[root])
                        for k in range(3))
            assert masks[0]|masks[1]|masks[2]==allmask
            maps.add(masks)
    maps=sorted(maps)
    examined=0
    chosen={}

    @lru_cache(None)
    def value(w):
        nonlocal examined
        if not(w&target_ones) or not(w&(allmask^target_ones)):
            return 0
        best=10**9
        choice=None
        distinct=set()
        for m in maps:
            groups=tuple(w&x for x in m)
            if w in groups or groups in distinct:
                continue
            distinct.add(groups)
            examined+=1
            immediate=sum((k+1)*g.bit_count() for k,g in enumerate(groups))
            if immediate>=best:
                continue
            total=immediate+sum(value(g) for g in groups if g)
            if total<best:
                best,choice=total,groups
        assert choice is not None
        chosen[w]=choice
        return best

    total=value(allmask)
    root=chosen[allmask]
    out=dict(status='PASS',contributor='Codex (GPT-6)',forms=forms,target=target,
             shortest_support=shortest,worlds=len(worlds),count_maps=len(maps),
             states=value.cache_info().currsize,examined_splits=examined,
             expected_fee_numerator=total,expected_fee_denominator=16,
             expected_fee=total/16,conjectured_lower_bound=3.5,
             root_groups=[[x for x in worlds if g>>x&1] for g in root],
             elapsed_ns=time.perf_counter_ns()-began,
             source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             scope='finite exact ordinary oracle; shortest-support rate is not assumed')
    (HERE/'linear_probe.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out))


if __name__=='__main__':
    main()
