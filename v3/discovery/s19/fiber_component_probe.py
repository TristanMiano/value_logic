"""Small exact cover-reconfiguration screen; a conjecture test, not confirmation."""
from itertools import product, combinations_with_replacement
from pathlib import Path
import hashlib, json, math, random, sys, time, traceback

HERE = Path(__file__).resolve().parent


def maximal(menu):
    return tuple(sorted(a for a in set(menu) if not any(a != b and a & b == a for b in menu)))


def menus(k):
    out = set()
    for bits in range(1, 1 << (1 << k)):
        out.add(maximal([a for a in range(1 << k) if bits >> a & 1]))
    return sorted(out)


def components(menu, k):
    full = (1 << k) - 1
    feasible = set()
    for state in product(*menu):
        union = 0
        for a in state:
            union |= a
        if union == full:
            feasible.add(state)
    total, sizes, reps = len(feasible), [], []
    while feasible:
        seed = min(feasible)
        feasible.remove(seed)
        stack, size = [seed], 0
        reps.append(seed)
        while stack:
            current = stack.pop()
            size += 1
            for i, choices in enumerate(menu):
                for a in choices:
                    if a == current[i]:
                        continue
                    neighbor = current[:i] + (a,) + current[i+1:]
                    if neighbor in feasible:
                        feasible.remove(neighbor)
                        stack.append(neighbor)
        sizes.append(size)
    return len(sizes), total, sorted(sizes), reps


def run():
    cases = []
    for k, top in ((2,6),(3,4),(4,2)):
        options = menus(k)
        for n in range(1,top+1):
            cases.extend((k, ms) for ms in combinations_with_replacement(options,n))
    rng = random.Random(191930)
    for trial in range(350):
        k, n = 4 + trial % 3, 2 + trial % 5
        ms = [maximal([rng.randrange(1<<k) for _ in range(1+rng.randrange(5))])
              for _ in range(n)]
        cases.append((k,ms))
    for k in range(1,7):
        cases.append((k, [[1<<j for j in range(k)]]*k))
    raw = (json.dumps(cases,separators=(',',':'))+'\n').encode()
    (HERE/'fiber_component_inputs.json').write_bytes(raw)
    maxima, violations, feasible_count, products = {}, [], 0, 0
    for index,(k, ms) in enumerate(cases):
        count, total, sizes, reps = components(ms,k)
        feasible_count += total
        products += math.prod(len(x) for x in ms)
        key = f'{k},{len(ms)}'
        if key not in maxima or count > maxima[key]['components']:
            maxima[key] = dict(components=count, case=index, sizes=sizes, representatives=reps)
        if count > math.factorial(k):
            violations.append(dict(case=index,k=k,components=count,menu=ms,sizes=sizes))
    return dict(cases=len(cases),cartesian_states=products,feasible_states=feasible_count,
                maxima=maxima,violations=violations,input_sha256=hashlib.sha256(raw).hexdigest())


if __name__ == '__main__':
    plan = json.loads((HERE/'fiber_component_plan.json').read_text())
    digest = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    assert digest == plan['source_sha256']
    assert not (HERE/'fiber_component_result.json').exists()
    started = time.perf_counter_ns()
    try:
        result = dict(status='COMPLETED_SCREEN',results=run(),source_sha256=digest,
                      runtime_ns=time.perf_counter_ns()-started,python=sys.version)
        (HERE/'fiber_component_result.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
        print(json.dumps({k:v for k,v in result.items() if k!='results'}))
        print(json.dumps({k:v for k,v in result['results'].items() if k!='maxima'}))
        print(json.dumps({k:v['components'] for k,v in result['results']['maxima'].items()}))
    except Exception:
        failure = dict(status='FAIL',traceback=traceback.format_exc(),runtime_ns=time.perf_counter_ns()-started)
        (HERE/'fiber_component_failure.json').write_bytes((json.dumps(failure,indent=2)+'\n').encode())
        raise
