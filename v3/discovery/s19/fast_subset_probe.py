"""Developmental adaptation check; no performance-superiority claim."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib, json, math, random, sys, time, traceback
import fast_subset as fast
import anchor_range_check as anchor

HERE = Path(__file__).resolve().parent


def direct(f, g, k):
    values = []
    for mask in range(1 << k):
        sub, best = mask, math.inf
        while True:
            best = min(best, max(f[sub], g[mask ^ sub]))
            if not sub:
                break
            sub = (sub - 1) & mask
        values.append(best)
    return values


def anchored_fast(tables, k, counts):
    size, n = 1 << k, len(tables)
    empty = [math.inf] + [-math.inf] * (size - 1)
    ups = [[t.get(m, (None, -math.inf))[1] for m in range(size)] for t in tables]
    pref, pb = [empty], [None]
    for row in ups:
        vals, left = fast.maxmin(pref[-1], row, k, counts)
        pref.append(vals)
        pb.append({m: m ^ left[m] for m in range(size) if vals[m] != -math.inf})
    suff, sb = [None] * (n + 1), [None] * n
    suff[n] = empty
    for i in range(n-1, -1, -1):
        suff[i], left = fast.maxmin(suff[i+1], ups[i], k, counts)
        sb[i] = {m: m ^ left[m] for m in range(size) if suff[i][m] != -math.inf}
    ob, intervals = [], []
    for i, tab in enumerate(tables):
        outside, left = fast.maxmin(pref[i], suff[i+1], k, counts)
        ob.append({m: left[m] for m in range(size) if outside[m] != -math.inf})
        for mask, (lo, hi) in tab.items():
            cap = min(hi, outside[(size-1) ^ mask])
            if lo <= cap:
                intervals.append((lo, cap, i, mask))
    return dict(ranges=anchor.old.merged([(a,b) for a,b,_,_ in intervals]),
                intervals=intervals, pb=pb, sb=sb, ob=ob, k=k)


def decode(x):
    if isinstance(x, str):
        return Q(x)
    if isinstance(x, list):
        return tuple(decode(a) for a in x)
    if isinstance(x, dict):
        return {k: decode(v) for k,v in x.items()}
    return x


def run():
    rng = random.Random(191929)
    triples = list(product((-1,0,1), repeat=4))
    cases = [(2, f, g) for f in triples for g in triples]
    for trial in range(160):
        k = trial % 8
        pool = [-math.inf, -2, -1, 0, 0, 0, 1, 2, math.inf]
        cases.append((k, [rng.choice(pool) for _ in range(1<<k)],
                         [rng.choice(pool) for _ in range(1<<k)]))
    portable = [(k, [str(x) for x in f], [str(x) for x in g]) for k,f,g in cases]
    raw = (json.dumps(portable,separators=(',',':'))+'\n').encode()
    (HERE/'fast_subset_inputs.json').write_bytes(raw)
    counts, entries, splits = {}, 0, 0
    for k, f, g in cases:
        got, back = fast.minmax(f,g,k,counts)
        expected = direct(f,g,k)
        assert got == expected, (k,f,g,got,expected)
        for mask,left in enumerate(back):
            assert left & mask == left and max(f[left],g[mask^left]) == got[mask]
            splits += 1
        entries += len(got)
    oldcases = decode(json.loads((HERE/'anchor_range_inputs.json').read_text()))
    oldresult = json.loads((HERE/'anchor_range_result.json').read_text())['results']['rows']
    witnesses = 0
    for trial, case in enumerate(oldcases):
        tabs, ends = anchor.local_tables(**case)
        result = anchored_fast(tabs, len(case['hs']), counts)
        expected = [tuple(Q(v) for v in pair) for pair in oldresult[trial]['ranges']]
        assert result['ranges'] == expected, trial
        for lo, hi in result['ranges']:
            for q in sorted({lo,hi,(lo+hi)/2}):
                xs = anchor.recover(result,tabs,ends,q)
                assert all(anchor.contains(poly,x) for poly,x in zip(case['polys'],xs))
                assert all(a <= min(anchor.dot(h,x) for x in xs) <= b
                           for h,a,b in zip(case['hs'],case['los'],case['his']))
                assert min(anchor.dot(obj[0],x)+obj[1] for obj,x in zip(case['objs'],xs)) == q
                witnesses += 1
    return dict(kernel_cases=len(cases), exhaustive_ternary_k2=len(triples)**2,
                seeded_cases=160, kernel_entries=entries, split_checks=splits,
                polygon_cases=len(oldcases), source_witnesses=witnesses,
                input_sha256=hashlib.sha256(raw).hexdigest(), **counts)


if __name__ == '__main__':
    plan = json.loads((HERE/'fast_subset_plan.json').read_text())
    for name,digest in plan['dependencies'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest() == digest, name
    assert not (HERE/'fast_subset_result.json').exists()
    assert not (HERE/'fast_subset_failure.json').exists()
    started = time.perf_counter_ns()
    try:
        result = dict(status='PASS', results=run(), python=sys.version)
        result['runtime_ns'] = time.perf_counter_ns()-started
        (HERE/'fast_subset_result.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
        print(json.dumps(result))
    except Exception:
        failure = dict(status='FAIL',traceback=traceback.format_exc(),runtime_ns=time.perf_counter_ns()-started)
        (HERE/'fast_subset_failure.json').write_bytes((json.dumps(failure,indent=2)+'\n').encode())
        raise
