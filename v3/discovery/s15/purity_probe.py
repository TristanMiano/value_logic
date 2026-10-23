"""Finite numerical screen of approximate count purity and binary capacity."""
from hashlib import sha256
from itertools import product
import json
import math
from pathlib import Path
import platform
from time import perf_counter_ns

start=perf_counter_ns()
def h(x):
    x=max(0.,min(1.,x))
    return -(x*math.log(x) if x else 0)-((1-x)*math.log1p(-x) if x<1 else 0)
def capacity(eta):
    return math.log1p(math.exp(-h(eta)/eta))
channels=0
affine_checks=0
maximum_excess=0.
examples=[]
for eta in (.001,.01,.1,.5,.9):
    cap=capacity(eta)
    for i in range(41):
        left=(1-eta)*i/40
        for j in range(101):
            t=j/100
            info=h(left+eta*t)-(1-t)*h(left)-t*h(left+eta)
            maximum_excess=max(maximum_excess,info-cap)
            assert info<=cap+1e-12
            channels+=1
    for signs in product((-1,0,1),repeat=4):
        b=[eta*s/4 for s in signs]
        a=.5-sum(b)/2
        probs={x:a+sum(bi*xi for bi,xi in zip(b,x)) for x in product((0,1),repeat=4)}
        comp=max(abs(p-probs[tuple(1-xi for xi in x)]) for x,p in probs.items())
        osc=max(probs.values())-min(probs.values())
        assert abs(comp-sum(map(abs,b)))<1e-12
        assert abs(osc-comp)<1e-12 and osc<=eta+1e-12
        affine_checks+=1
    eps=.01
    examples.append(dict(eta=eta,capacity_nats=cap,
        two_values_fixed_horizon_lower=math.ceil(math.log(2*eps)/math.log1p(-eta)),
        five_values_fixed_horizon_fano_lower=math.ceil((math.log(5)-h(eps)-eps*math.log(4))/cap),
        five_values_zero_error_mean_episode_lower=math.log(5)/cap,
        eight_bit_exact_construction_mean_episode_upper=16/eta))
result=dict(status='PASS',model='Codex (GPT-6)',python=platform.python_version(),
    source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
    binary_channel_grid=channels,affine_complement_checks=affine_checks,
    maximum_capacity_excess=maximum_excess,examples=examples,
    elapsed_ns=perf_counter_ns()-start,
    scope='Finite floating-point screens and analytical resource illustrations; changed approximate-purity contract, no timing or fee benchmark.')
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
