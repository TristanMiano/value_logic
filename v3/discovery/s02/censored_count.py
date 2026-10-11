"""DEVELOPMENT: exact two-endpoint hull for censored count evidence.

Codex (GPT-6), 2026-10-11. Callers must bind distinct sampled identities and
sound label receipts; these count arithmetic functions do not authenticate them.
"""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
from math import comb
from pathlib import Path
import hashlib
import json
import sys
import time
import traceback
import sampling_v2 as sampling


def partial_interval(N,s,ones,zeros,alpha,rho=F(1,2),counter=None):
    if any(type(v) is not int for v in (N,s,ones,zeros)) or not 0<=ones+zeros<=s<=N or min(ones,zeros)<0:
        raise ValueError('Malformed prefix counts')
    if not 0<=rho<1:raise ValueError('Working mixture must retain uniform support')
    counter=counter if counter is not None else Counter()
    low=sampling.interval(N,s,ones,alpha,counter,rho)[0]
    high=sampling.interval(N,s,s-zeros,alpha,counter,rho)[1]
    return low,high


def reference_hull(N,s,k,z,alpha,rho):
    candidates=set()
    for e in range(k,s-z+1):
        q=F(1) if s==0 else (1-rho)/F(s+1)+rho/2*int(e in (0,s))
        for M in range(e,N-s+e+1):
            if F(comb(M,e)*comb(N-M,s-e),comb(N,s))>alpha*q:candidates.add(M)
    return min(candidates),max(candidates)


def screen():
    monotone=0;partial=0
    for N in range(1,21):
        for rho in (F(0),F(1,2),F(9,10)):
            for alpha in (F(1,5),F(1,20)):
                for s in range(N+1):
                    intervals=[sampling.interval(N,s,e,alpha,rho=rho) for e in range(s+1)]
                    lower=[a for a,b in intervals];upper=[b for a,b in intervals]
                    assert lower==sorted(lower) and upper==sorted(upper)
                    monotone+=1
                    if N<=8:
                        for k in range(s+1):
                            for z in range(s-k+1):
                                got=partial_interval(N,s,k,z,alpha,rho)
                                assert got==reference_hull(N,s,k,z,alpha,rho)
                                partial+=1
    return dict(monotone_prefix_families=monotone,exact_partial_hulls=partial,
                monotonicity_max_N=20,full_mass_union_max_N=8)


def main(output):
    assert not output.exists()
    paths=[Path(__file__),Path(sampling.__file__),Path(sampling.first.__file__)]
    result=dict(status='running',evidence='DEVELOPMENT',contributor='Codex (GPT-6)',
                start_utc=datetime.now(timezone.utc).isoformat(),command=sys.argv,
                sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
                scope='Direct exact hypergeometric-mass union checks at N<=8, endpoint monotonicity at N<=20 for stated mixtures/levels. Larger single-pass timers compare count arithmetic only; source/receipt authentication and input acquisition are not included.')
    start=time.monotonic_ns()
    try:
        result['checks']=screen();rows=[]
        for N,s,k,z in ((1000,64,20,10),(10000,256,80,40)):
            counts=Counter();before=time.perf_counter_ns()
            got=partial_interval(N,s,k,z,F(1,20),counter=counts)
            shortcut_ns=time.perf_counter_ns()-before
            all_counts=Counter();before=time.perf_counter_ns()
            intervals=[sampling.interval(N,s,e,F(1,20),all_counts) for e in range(k,s-z+1)]
            expected=min(a for a,b in intervals),max(b for a,b in intervals)
            enumeration_ns=time.perf_counter_ns()-before
            assert got==expected
            rows.append(dict(N=N,s=s,known_ones=k,known_zeros=z,unknown=s-k-z,bounds=got,
                             shortcut_ns=shortcut_ns,enumeration_ns=enumeration_ns,
                             shortcut_counts=dict(counts),enumeration_counts=dict(all_counts)))
        result.update(status='complete',rows=rows)
    except Exception:
        result.update(status='failed',failure=traceback.format_exc());raise
    finally:
        result.update(elapsed_ns=time.monotonic_ns()-start,end_utc=datetime.now(timezone.utc).isoformat())
        output.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8')
        print(json.dumps(result,default=str))


if __name__=='__main__':main(Path(sys.argv[1]))
