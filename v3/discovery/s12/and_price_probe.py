"""DEVELOPMENT screen of and_price.md; Codex (GPT-6).

The enumerator is reused unchanged from the already frozen parity probe.
This new public oracle accepts arbitrary truth tables and does not assume
short-circuit blocks or the closed conjunction formula.
"""
from functools import lru_cache
from pathlib import Path
import hashlib
import json
import platform
import sys
import time

from parity_price_probe import all_invoice_functions, partitions

HERE=Path(__file__).resolve().parent


def oracle(n, bank, ones, overhead):
    stats=dict(states=0,program_checks=0)
    @lru_cache(None)
    def value(source):
        if not (source&ones) or (source&ones)==source:
            return 0
        stats['states']+=1
        best=float('inf')
        for program in bank:
            groups=[(cost,subset&source) for cost,subset in program if subset&source]
            if len(groups)<=1:
                continue
            stats['program_checks']+=1
            worst=0
            for cost,subset in groups:
                worst=max(worst,cost+overhead+value(subset))
                if worst>=best:
                    break
            best=min(best,worst)
        assert best!=float('inf')
        return best
    return value,stats


def formula(fees,cap,overhead,target):
    k=target.bit_count()
    if k==0:
        return 0
    base=sum(c for i,c in enumerate(fees) if (target>>i)&1)
    outside=min((c for i,c in enumerate(fees) if not (target>>i)&1),default=float('inf'))
    if k==1:
        return base+outside+overhead
    q=(k+cap-2)//(cap-1)
    if q>=2:
        return base+min(fees)+q*overhead
    return base+min(outside+overhead,min(fees)+2*overhead)


def main():
    begun=time.perf_counter_ns()
    n=3
    totals=dict(comparisons=0,bellman_states=0,program_checks=0)
    panels=[]
    for fees in [(1,1,1),(1,2,7),(2,3,5),(1,1,100)]:
        for cap in [2,3]:
            bank=partitions(all_invoice_functions(fees,cap))
            panel=dict(fees=fees,cap=cap,private_invoice_functions=len(bank),full_target=[])
            for overhead in [0,1,10,98,100]:
                for target in range(1,1<<n):
                    expected=formula(fees,cap,overhead,target)
                    values=set()
                    for wanted in range(1<<n):
                        if wanted&~target:
                            continue
                        ones=sum(1<<x for x in range(1<<n) if (x&target)==wanted)
                        solve,stats=oracle(n,bank,ones,overhead)
                        actual=solve((1<<(1<<n))-1)
                        assert actual==expected,(fees,cap,overhead,target,wanted,actual,expected)
                        values.add(actual)
                        totals['comparisons']+=1
                        totals['bellman_states']+=stats['states']
                        totals['program_checks']+=stats['program_checks']
                    assert len(values)==1
                    if target==(1<<n)-1:
                        panel['full_target'].append(dict(overhead=overhead,optimum=expected))
            panels.append(panel)
    result=dict(contributor='Codex (GPT-6)',status='DEVELOPMENT',python=sys.version,
                platform=platform.platform(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                dependency_sha256=hashlib.sha256((HERE/'parity_price_probe.py').read_bytes()).hexdigest(),
                elapsed_ns=time.perf_counter_ns()-begun,totals=totals,panels=panels,result='PASS')
    (HERE/'and_price_probe.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({key:result[key] for key in ('result','elapsed_ns','totals')}))


if __name__=='__main__':
    main()
