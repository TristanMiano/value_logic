"""Paid-source development of row-preserving value bounds; no new labels."""
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import platform
import random
import sys
import time

import numpy as np
from scipy.optimize import linprog
import scipy

from cdf_sweep import CDFSweep
from row_flow import RowFlow


def lp_reference(source, payoff):
    # An independently assembled p/z LP checks the network reduction.
    m, n = source.size, len(source.intervals)
    variables = [(i,h) for i,(a,b) in enumerate(source.intervals) for h in range(a,b+1)]
    count = m+len(variables)
    objective = np.array([*map(float,payoff), *([0.0]*len(variables))])
    equality, rhs = [], []
    total = [0]*count
    total[:m] = [1]*m
    equality.append(total)
    rhs.append(1)
    for i, w in enumerate(source.weights):
        row = [0]*count
        for k,(owner,h) in enumerate(variables):
            if owner == i:
                row[m+k] = 1
        equality.append(row)
        rhs.append(float(w))
    inequalities, bounds = [], []
    for j in range(m-1):
        row = [int(h<=j) for h in range(m)] + [-int(h<=j) for i,h in variables]
        inequalities.extend((row, [-x for x in row]))
        bounds.extend((float(source.epsilon), float(source.epsilon)))
    result = linprog(objective, A_ub=np.array(inequalities) if inequalities else None,
                     b_ub=np.array(bounds) if inequalities else None,
                     A_eq=np.array(equality), b_eq=np.array(rhs), bounds=(0,None), method='highs')
    assert result.success, result.message
    return result.fun


def band(size, intervals, epsilon):
    n = len(intervals)
    return ([max(F(0), F(sum(u<=j for l,u in intervals),n)-epsilon) for j in range(size-1)],
            [min(F(1), F(sum(l<=j for l,u in intervals),n)+epsilon) for j in range(size-1)])


def run(destination):
    if destination.exists():
        raise FileExistsError('Choose a new result path')
    here = Path(__file__).resolve().parent
    threshold_path = here/'threshold_cnf_results.json'
    queries_path = here/'threshold_query_results.json'
    raw, querybank = json.loads(threshold_path.read_text()), json.loads(queries_path.read_text())
    examples = []
    seed = 261012211
    rng = random.Random(seed)
    fixture_inputs = [(3,[(0,2),(1,1)],F(0),[0,1,0]),
                      (3,[(0,2),(1,1)],F(1,10),[0,1,0])]
    for size in (2,4,6):
        for variant in range(3):
            intervals=[]
            for i in range(4):
                a,b=sorted((rng.randrange(size),rng.randrange(size)))
                intervals.append((a,b))
            g=[rng.randrange(-5,6) for _ in range(size)]
            fixture_inputs.append((size,intervals,F(variant,8),g))
    max_lp_error=0
    for size, intervals, eps, g in fixture_inputs:
        source=RowFlow(size,intervals,eps)
        answer=source.interval(g)
        reference=(lp_reference(source,g),-lp_reference(source,[-x for x in g]))
        difference=max(abs(float(F(answer['lower']))-reference[0]),
                       abs(float(F(answer['upper']))-reference[1]))
        max_lp_error=max(max_lp_error,difference)
        assert difference<1e-9
        lo,hi=band(size,intervals,eps)
        cheap=CDFSweep(lo,hi).interval(g)
        assert F(cheap['lower'])<=F(answer['lower'])<=F(answer['upper'])<=F(cheap['upper'])
        examples.append(dict(size=size,intervals=intervals,epsilon=str(eps),payoff=g,
                             cdf_interval=[cheap['lower'],cheap['upper']],answer=answer,
                             independent_lp=reference))

    paid=[]
    flow_ns=0
    exact_certificates=0
    strict_endpoints=0
    strict_beyond_intersection=0
    # One acquisition arm is enough to develop the representation; repeated
    # policies sharing the same rows are not counted as new source evidence.
    arm=raw['arms'][0]
    prior_by_stage={row['stage']:row for row in querybank['rows'] if row['mode']==arm['mode']}
    for stage in arm['stages']:
        eps=F(stage['cdf_band']['radius'])
        source=RowFlow(9,stage['draw_intervals'],eps)
        for name,g in querybank['query_definitions'].items():
            start=time.perf_counter_ns()
            answer=source.interval(g)
            elapsed=time.perf_counter_ns()-start
            flow_ns+=elapsed
            exact_certificates+=2
            previous=prior_by_stage[stage['stage']]['outputs'][name]
            lower,upper=F(answer['lower']),F(answer['upper'])
            assert F(previous['lower'])<=lower<=upper<=F(previous['upper'])
            assert F(previous['intersection'][0])<=lower<=upper<=F(previous['intersection'][1])
            strict_endpoints+=int(lower>F(previous['lower']))+int(upper<F(previous['upper']))
            strict_beyond_intersection+=int(lower>F(previous['intersection'][0]))+int(upper<F(previous['intersection'][1]))
            paid.append(dict(stage=stage['stage'],query=name,
                             cdf_interval=[previous['lower'],previous['upper']],
                             old_intersection=previous['intersection'],answer=answer,flow_ns=elapsed))
    result=dict(status='DEVELOPMENT',contributor='ChatGPT (GPT-6 Astra Pro)',
                generated_utc=datetime.now(timezone.utc).isoformat(),command=sys.argv,seed=seed,
                environment=dict(python=platform.python_version(),scipy=scipy.__version__),
                sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                         (Path(__file__),here/'row_flow.py',here/'cdf_sweep.py',threshold_path,queries_path)},
                new_truth_purchases=0,exact_paid_certificates=exact_certificates,
                strict_vs_cdf_endpoints=strict_endpoints,
                strict_vs_previous_intersection_endpoints=strict_beyond_intersection,
                paid_flow_ns=flow_ns,independent_lp_max_error=max_lp_error,
                examples=examples,paid=paid,
                scope='Same exposed iid threshold sample and its fixed-n DKW event. Exact flow certificates optimize the stated convex outer source. This small reference solver is not the economical default; use simpler bounds when adequate.')
    destination.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('examples','paid','sources')}))
    print(json.dumps([dict(stage=x['stage'],query=x['query'],old=x['old_intersection'],
                          new=[x['answer']['lower'],x['answer']['upper']]) for x in paid]))


if __name__=='__main__':
    run(Path(sys.argv[1]))
