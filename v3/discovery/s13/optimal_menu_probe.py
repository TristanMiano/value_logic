"""Small exact screen of a positive-cost optimal-menu learning obstruction."""
from pathlib import Path
import hashlib
import json
import time

HERE=Path(__file__).resolve().parent


def main():
    start=time.perf_counter_ns()
    subsets=cover_checks=world_checks=0
    for k in (2,4,6):
        grid=[(i,j) for i in range(k//2) for j in range(k//2,k)]
        def covered(z,i,j):return bool(z>>i&1) or not(z>>j&1)
        def executes(z,i,j):
            left=[int(a==i and not(z>>a&1)) for a in range(k)]
            right=[int(a!=j or not(z>>a&1)) for a in range(k)]
            return all(not a or b for a in left for b in right)
        for mask in range(1<<len(grid)):
            observed=[pair for r,pair in enumerate(grid) if mask>>r&1]
            repairs=[z for z in range(1<<k) if all(covered(z,*pair) for pair in observed)]
            assert 0 in repairs and (1<<k)-1 in repairs
            for z in repairs:
                assert sum((z>>i&1)+int(not(z>>i&1)) for i in range(k))==k
                assert all(executes(z,i,i) for i in range(k))
                cover_checks+=1
            common=[]
            for pair in grid:
                values=[executes(z,*pair) for z in repairs]
                assert values==[covered(z,*pair) for z in repairs]
                if all(values):common.append(pair)
                world_checks+=len(repairs)
            assert common==observed
            subsets+=1
    out=dict(status='PASS',contributor='Codex (GPT-6)',subsets=subsets,
             minimum_price_repair_checks=cover_checks,repair_world_checks=world_checks,
             elapsed_ns=time.perf_counter_ns()-start,
             source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             scope='Finite exact construction; no empirical learning-performance claim')
    (HERE/'optimal_menu_probe.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out))


if __name__=='__main__':main()
