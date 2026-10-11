"""DEVELOPMENT: exact source-expansion bounds and fixed-loss action transport.

Codex (GPT-6), 2026-10-11. Ordinary identical edit-aware kernel is permitted.
No independently checked MaxSAT upper proof or cold performance claim.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from fractions import Fraction as F
from itertools import product
import hashlib
import json
from pathlib import Path
import random
import sys
import time
import traceback

from decision_probe import compatible, initial_model, row, separate


@dataclass(frozen=True)
class Request:
    n: int
    clauses: tuple
    actions: tuple


@dataclass(frozen=True)
class Bound:
    request: Request
    action: tuple
    upper: F


def remove_clause(request, bound, index):
    start = time.perf_counter_ns()
    if bound.request is not request or not 0 <= index < len(request.clauses):
        raise ValueError('Wrong local immutable parent or deletion')
    removed = request.clauses[index]
    rest = request.clauses[:index]+request.clauses[index+1:]
    assert removed, 'Nonempty old source cannot contain an empty clause'
    # Public structural shortcuts are available to every comparator.
    if removed in rest or any(-lit in removed for lit in removed):
        answer = dict(upper=bound.upper,status='structurally_unchanged_source',maxsat_calls=0,source_sat_calls=0)
    else:
        delta = rest+tuple((-lit,) for lit in removed)
        if initial_model(request.n,delta) is None:
            answer = dict(upper=bound.upper,status='empty_delta',maxsat_calls=0,source_sat_calls=1)
        else:
            got = separate(request.n,delta,request.actions,bound.action)
            answer = dict(upper=max(bound.upper,got['upper']),delta_upper=got['upper'],
                          status='delta_separated',delta_witness=got['witness'],
                          maxsat_calls=got['maxsat_calls'],source_sat_calls=1,
                          largest_integer_bits=got['largest_integer_bits'])
    return dict(answer,elapsed_ns=time.perf_counter_ns()-start,remaining_clauses=rest)


def action_transport(request,bound,p):
    assert bound.request is request and sum(p) == sum(bound.action) == 1
    start = time.perf_counter_ns()
    dp = [a-b for a,b in zip(p,bound.action)]
    constant = sum(d*b for d,(b,_) in zip(dp,request.actions))
    weights = [sum(d*w[i] for d,(_,w) in zip(dp,request.actions)) for i in range(request.n)]
    contrast_upper = constant+sum(max(F(0),w) for w in weights)
    return dict(upper=bound.upper+contrast_upper,contrast_upper=contrast_upper,
                elapsed_ns=time.perf_counter_ns()-start)


def main(output):
    assert not output.exists()
    started = time.monotonic_ns()
    result = dict(status='running',evidence='DEVELOPMENT',contributor='Codex (GPT-6)',seed=8404,
                  start_utc=datetime.now(timezone.utc).isoformat(),command=sys.argv,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                           (Path(__file__),Path(__file__).with_name('decision_probe.py'))},
                  scope='fixed action/loss source-expansion upper bounds; local immutable parent identity; old source already checked nonempty; trusted MaxSAT optimality, tiny independent enumeration')
    try:
        rng = random.Random(8404)
        cases, empty_skipped = [], 0
        for n in (4,6,12,20):
            for trial in range(4):
                clauses = []
                for _ in range(2*n):
                    variables = rng.sample(range(1,n+1),3)
                    clauses.append(tuple(v if rng.randrange(2) else -v for v in variables))
                if trial == 1:
                    clauses.append(clauses[0])
                elif trial == 2:
                    clauses.append((1,-1))
                actions = tuple((3*n,tuple(rng.randrange(-2,3) for _ in range(n))) for _ in range(3))
                request = Request(n,tuple(clauses),actions)
                if initial_model(n,request.clauses) is None:
                    empty_skipped += 1
                    continue
                p = (F(1,3),F(1,3),F(1,3))
                old_start = time.perf_counter_ns()
                old = separate(n,request.clauses,actions,p)
                old_ns = time.perf_counter_ns()-old_start
                bound = Bound(request,p,old['upper'])
                for index in (0,len(clauses)-1):
                    delta = remove_clause(request,bound,index)
                    full_start = time.perf_counter_ns()
                    full = separate(n,delta['remaining_clauses'],actions,p)
                    full_ns = time.perf_counter_ns()-full_start
                    assert delta['upper'] == full['upper']
                    enumerated = None
                    if n <= 6:
                        worlds = [x for x in product((0,1),repeat=n) if compatible(x,delta['remaining_clauses'])]
                        enumerated = max(sum(a*b for a,b in zip(p,row(x,actions))) for x in worlds)
                        assert enumerated == delta['upper']
                    cases.append(dict(n=n,trial=trial,request=dict(clauses=request.clauses,actions=actions),
                                      action=p,removed_index=index,old_upper=old['upper'],old_separation_ns=old_ns,
                                      delta=delta,full=full,full_elapsed_ns=full_ns,enumerated_upper=enumerated))
                q = (F(1,2),F(1,4),F(1,4))
                transport = action_transport(request,bound,q)
                exact = separate(n,request.clauses,actions,q)
                assert transport['upper'] >= exact['upper']
                cases[-1]['action_change'] = dict(new_action=q,transport=transport,exact=exact)
        # Identity is a local provenance check, not just equal-looking content.
        clone = Request(request.n,request.clauses,request.actions)
        try:
            remove_clause(clone,bound,0)
        except ValueError:
            identity_rejected = True
        else:
            raise AssertionError('Unbound parent accepted')
        result.update(status='complete',cases=cases,empty_old_sources_skipped=empty_skipped,
                      wrong_parent_rejected=identity_rejected)
    except Exception:
        result.update(status='failed',failure=traceback.format_exc())
        raise
    finally:
        result['elapsed_ns'] = time.monotonic_ns()-started
        result['end_utc'] = datetime.now(timezone.utc).isoformat()
        output.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8')
        print(json.dumps({k:v for k,v in result.items() if k!='cases'}))


if __name__ == '__main__':
    main(Path(sys.argv[1]))
