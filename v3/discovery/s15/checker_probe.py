"""Exact finite screens of private_checker.md and approx_checker.md."""
from fractions import Fraction as F
from itertools import product
import hashlib
import json
from pathlib import Path
from time import perf_counter_ns

HERE = Path(__file__).resolve().parent
OUT = HERE/'checker_probe.json'
assert not OUT.exists(), 'Preserve exposed outputs.'
started = perf_counter_ns()
dot = lambda a,b: sum(x*y for x,y in zip(a,b))
norm2 = lambda a: dot(a,a)
def center(a):
    mean = F(sum(a),len(a))
    return tuple(x-mean for x in a)


moments, smallball = 0, 0
worst = F(0)
for n in range(1,6):
    signs = list(product([-1,1],repeat=n))
    for d in product([-1,0,1],repeat=n):
        mu = norm2(d)
        if mu == 0:
            continue
        z = [dot(r,d) for r in signs]
        assert F(sum(t*t for t in z),len(z)) == mu
        assert F(sum(t**4 for t in z),len(z)) == 3*mu**2-2*sum(t**4 for t in d)
        moments += 1
        for tau2 in [F(1,4),F(1),F(4),F(9)]:
            if mu <= tau2:
                continue
            prob = F(sum(4*t*t<=tau2 for t in z),len(z))
            assert prob <= F(13,16)
            worst = max(worst,prob)
            smallball += 1

# The same seed used after a rejection can accept a false claim surely.
field_reuse = []
for r in product([0,1],repeat=2):
    vals = [dot(r,d)%2==0 for d in [(1,0),(0,1),(1,1)]]
    assert any(vals)
    field_reuse.append(dict(seed=r,accepts=vals,fail_stop_bad=vals[0],continue_bad=any(vals)))
assert sum(x['fail_stop_bad'] for x in field_reuse)==2

# Imperfect completeness can yield conditional error one while unconditional
# failure remains delta. Correctness and release-conditioned error differ.
imperfect = []
for seed in range(8):
    true_accept = seed==0
    false_accept = seed==0
    imperfect.append(dict(seed=seed,true_accept=true_accept,
                          false_release=true_accept and false_accept))
assert sum(x['false_release'] for x in imperfect)==1

A = ((2,-1,1),(0,3,-1),(-2,1,2),(1,1,-2))
u, v = (1,-1,2,0),(1,0,-1)
seeds = list(product(list(product([-1,1],repeat=4)),repeat=2))
epoch_rows = []
accepted_true = 0
for scenario in range(12):
    any_false = 0
    lengths = []
    for R in seeds:
        # G is genuinely acquired from A and centering, outside the proposer.
        columns = [center(tuple(A[i][j] for i in range(4))) for j in range(3)]
        G = [tuple(dot(r,col) for col in columns) for r in R]
        x = (1,scenario%3-1,(scenario//3)%3-1)
        bad = False
        length = 0
        for t in range(15):
            amplitude = dot(v,x)
            bias = 20*(t+scenario+1)
            b = tuple(z*amplitude+bias for z in u)
            cb = center(b)
            tau2 = [F(1),F(8),F(32),F(128)][(scenario+t)//3%4]
            sketch = [dot(r,cb)-dot(g,x) for r,g in zip(R,G)]
            # These exact full residuals are oracle analysis, never available
            # to the proposing or accepting policy.
            truth = tuple(dot(row,x) for row in A)
            d = center(tuple(bb-ff for bb,ff in zip(b,truth)))
            assert sketch == [dot(r,d) for r in R]
            accept = all(4*z*z<=tau2 for z in sketch)
            if not accept:
                break
            length += 1
            bad |= norm2(d)>tau2
            if norm2(d)<=tau2:
                cost = tuple(F((t+i*scenario)%7,3) for i in range(4))
                selected = min(range(4),key=lambda i:b[i]+cost[i])
                best = min(truth[i]+cost[i] for i in range(4))
                regret = truth[selected]+cost[selected]-best
                assert regret >= 0 and regret**2 <= 2*tau2
                accepted_true += 1
            # Adaptive input depends on proposed/accepted values, not on R,G
            # or the private residual. The bias cancels from its contrasts.
            x = (x[1],x[2],(b[0]-b[1]+t)%5-2)
        any_false += bad
        lengths.append(length)
    failure = F(any_false,len(seeds))
    assert failure <= F(13,16)**2
    epoch_rows.append(dict(scenario=scenario,failure=str(failure),
                           min_length=min(lengths),max_length=max(lengths),
                           mean_length=str(F(sum(lengths),len(lengths)))))

# Every centered model residual is zero despite an arbitrary common error.
for x in product([-1,0,1],repeat=3):
    truth = tuple(dot(row,x) for row in A)
    for bias in [-1000,0,1000]:
        b = tuple(z+bias for z in truth)
        assert norm2(center(tuple(bb-ff for bb,ff in zip(b,truth))))==0

result = dict(status='PASS',classification='DEVELOPMENT; exact finite arithmetic',
              source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              elapsed_ns=perf_counter_ns()-started,moment_cases=moments,
              false_claim_smallball_cases=smallball,worst_one_row_probability=str(worst),
              rows_for_under_one_percent=23,ceiling_23=str(F(13,16)**23),
              epoch_cases=len(epoch_rows),private_seeds_per_epoch=len(seeds),
              checked_true_action_warrants=accepted_true,
              field_reuse=field_reuse,imperfect_completeness=imperfect,epochs=epoch_rows,
              limits='Enumeration does not establish general soundness or measured performance; proof and all costs remain separate.')
OUT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ('field_reuse','imperfect_completeness','epochs')},indent=2))
