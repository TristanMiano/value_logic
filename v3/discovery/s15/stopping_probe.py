"""Exact small-instance binary-prior stopping comparison, DEVELOPMENT."""
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import permutations, product
from math import comb, prod
from pathlib import Path
import json
import time

HERE = Path(__file__).resolve().parent

def fall(a, b):
    return prod(range(a-b+1, a+1)) if 0 <= b <= a else 0

def solve(n, H):
    m = n//2
    prior = [(m, F(1,2), 0), (m-1, F(1,4), 1), (m+1, F(1,4), 1)]

    @lru_cache(None)
    def masses(t, k):
        t = min(t, n)
        out = [F(0), F(0)]
        for w, pi, lab in prior:
            out[lab] += pi * F(fall(w,k)*fall(n-w,t-k), fall(n,t))
        return tuple(out)

    best = None
    for mask in range(1 << H):
        labels = [0]+[(mask >> (t-1)) & 1 for t in range(1,H+1)]
        policy = {}

        @lru_cache(None)
        def dp(t, k):
            mass = masses(t,k)
            total = sum(mass)
            if not total:
                return F(0), F(0)
            stop = (mass[labels[t]]/total, F(0))
            if t == H:
                policy[t,k] = True
                return stop
            if t == n:
                child = dp(t+1,k)
                cont = (child[0], 1+child[1])
            else:
                p1 = sum(masses(t+1,k+1))/total
                p0 = sum(masses(t+1,k))/total
                assert p0+p1 == 1
                z, o = dp(t+1,k), dp(t+1,k+1)
                cont = (p0*z[0]+p1*o[0], 1+p0*z[1]+p1*o[1])
            choose_stop = t>0 and (stop[0],-stop[1]) >= (cont[0],-cont[1])
            policy[t,k] = choose_stop
            return stop if choose_stop else cont

        score = dp(0,0)
        if best is None or (score[0],-score[1]) > (best[0][0],-best[0][1]):
            best = score, labels, dict(policy)
    (accuracy, cost), labels, policy = best
    d=H-1
    folded_accuracy = sum(max(masses(d,k))*comb(d,k) for k in range(d+1))
    assert accuracy == folded_accuracy
    assert all(policy.get((t,k)) == policy.get((t,t-k))
               for t in range(min(H,n)+1) for k in range(t+1)
               if sum(masses(t,k)) and sum(masses(t,t-k)))

    def law(w):
        live={(0,0):F(1)}
        out=defaultdict(F)
        for t in range(H+1):
            nxt=defaultdict(F)
            for (tt,k), p in live.items():
                assert tt==t
                if policy.get((t,k), True) or t==H:
                    out[t]+=p
                elif t==n:
                    nxt[t+1,k]+=p
                else:
                    nxt[t+1,k+1]+=p*F(w-k,n-t)
                    nxt[t+1,k]+=p*F(n-w-t+k,n-t)
            live={s:p for s,p in nxt.items() if p}
        assert not live and sum(out.values())==1
        return dict(out)

    laws={w:law(w) for w in (m-1,m,m+1)}
    assert laws[m-1]==laws[m+1]
    ac=F(0); co=F(0)
    for w,pi,lab in prior:
        ac+=pi*sum(p for t,p in laws[w].items() if labels[t]==lab)
        co+=pi*sum(t*p for t,p in laws[w].items())
    assert (ac,co)==(accuracy,cost)

    # Whole d-bit sample followed by the binary Bayes answer, with the more
    # probable answer assigned to the shorter invoice. Ties use label zero.
    answer_masses=[F(0),F(0)]
    for k in range(d+1):
        ma=masses(d,k)
        lab=int(ma[1]>ma[0])
        answer_masses[lab]+=sum(ma)*comb(d,k)
    fixed_cost=d+min(answer_masses)
    assert cost<=fixed_cost

    perm_checks=0
    if n==4:
        for w in (m-1,m,m+1):
            x=(1,)*w+(0,)*(n-w)
            counts=defaultdict(int)
            for order in permutations(range(n)):
                t=k=0
                while t<H and not policy.get((t,k),True):
                    if t<n:
                        k+=x[order[t]]
                    t+=1
                counts[t]+=1
                perm_checks+=1
            total=sum(counts.values())
            assert {t:F(c,total) for t,c in counts.items()}==laws[w]

    return dict(n=n,cap=H,decoder=labels[1:],accuracy=str(accuracy),
                mean_queries=str(cost),fixed_depth_mean_queries=str(fixed_cost),
                saving_vs_that_wrapper=float(1-cost/fixed_cost),
                count_laws={str(w):{str(t):str(p) for t,p in v.items()} for w,v in laws.items()},
                stop_states=[list(s) for s,b in sorted(policy.items()) if b],
                enumerated_decoders=1<<H,permutation_checks=perm_checks)

def main():
    start=time.perf_counter_ns()
    results=[solve(n,H) for n in (4,6,8) for H in range(2,n+2)]
    elapsed=time.perf_counter_ns()-start
    out=dict(status='PASS',attribution='Codex (GPT-6), DEVELOPMENT',
             source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
             elapsed_ns=elapsed,results=results,
             note='Exact binary-prior enumeration, not all-summary/worst-case risk or total CPU comparison.')
    (HERE/'stopping_probe.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2))

if __name__=='__main__':
    main()
