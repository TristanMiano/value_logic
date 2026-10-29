"""Development check of indexed queries against exposed exact audit records."""
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import platform
import time
import traceback
from range_service import CheckedRange

HERE = Path(__file__).resolve().parent


def exact_source(problem, witness):
    xs = [list(map(F, x)) for x in witness['source']]
    assert len(xs) == len(problem['generators'])
    def form(c, d, x):
        assert len(c) == len(x)
        return sum((F(a) * b for a, b in zip(c, x)), F(d))
    for g, x in zip(problem['generators'], xs):
        assert len(x) == len(g['c'])
        for a, b in zip(g['A'], g['b']):
            assert form(a, '0', x) <= F(b)
    for receipt in problem['receipts']:
        z = min(form(f['c'], f['d'], x) for f, x in zip(receipt['forms'], xs))
        assert F(receipt['lo']) <= z <= F(receipt['hi'])
    z = min(form(g['c'], g['d'], x) for g, x in zip(problem['generators'], xs))
    assert z == F(witness['q'])
    masks = witness['assignment']
    assert len(masks) == len(xs)
    assert sum(m.bit_count() for m in masks) == len(problem['receipts'])
    assert sum(masks) == (1 << len(problem['receipts'])) - 1


def expect_error(operation):
    try:
        operation()
    except (ValueError, TypeError, KeyError):
        return
    raise AssertionError('expected rejection')


def main():
    freeze = json.loads((HERE / 'service_freeze.json').read_text(encoding='utf-8'))
    for name, expected in freeze['sha256'].items():
        assert hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected
    rows = [json.loads(line) for line in (HERE / 'audit_records.jsonl').read_text(encoding='utf-8').splitlines()]
    summaries, all_witnesses = [], []
    for row in rows:
        original = deepcopy(row['problem'])
        problem, cert = deepcopy(original), deepcopy(row['certificate'])
        before = time.perf_counter_ns()
        service = CheckedRange(problem, cert)
        compiled_ns = time.perf_counter_ns() - before
        assert service.ranges() == row['check']['ranges']
        ranges = [tuple(map(F, r)) for r in row['check']['ranges']]
        good, bad = set(), set()
        for lo, hi in ranges:
            good.update([lo, hi, (lo + hi) / 2])
            if lo < hi:
                good.update([(2 * lo + hi) / 3, (lo + 2 * hi) / 3])
        if ranges:
            bad.update([ranges[0][0] - 1, ranges[-1][1] + 1])
            bad.update((ranges[j][1] + ranges[j + 1][0]) / 2 for j in range(len(ranges) - 1))
        else:
            bad.update([F(-1), F(0), F(1)])
        # Caller-owned mutable objects must not change the compiled snapshot.
        problem['generators'][0]['d'] = '999999'
        cert['faces'].clear()
        before = time.perf_counter_ns()
        witnesses = []
        for q in sorted(good):
            assert service.contains(str(q))
            w = service.source(str(q))
            exact_source(original, w)
            witnesses.append(w)
        query_ns = time.perf_counter_ns() - before
        for q in sorted(bad):
            assert not service.contains(str(q))
            expect_error(lambda q=q: service.source(str(q)))
        expect_error(lambda: service.contains(0.5))
        expect_error(lambda: service.band('1', '0'))
        probes = sorted(good | bad)
        bands = [(q, q) for q in probes] + list(zip(probes, probes[1:]))
        bands += [(F(-10**401), F(10**401))]
        for lo, hi in bands:
            expected = any(a <= hi and b >= lo for a, b in ranges)
            answer = service.band(str(lo), str(hi))
            assert (answer['status'] == 'INTERSECTS') == expected
            if expected:
                q = F(answer['q'])
                assert lo <= q <= hi
                exact_source(original, service.source(answer['q']))
            else:
                lefts = [b for a, b in ranges if b < lo]
                rights = [a for a, b in ranges if a > hi]
                assert answer['left'] == (str(max(lefts)) if lefts else None)
                assert answer['right'] == (str(min(rights)) if rights else None)
        damaged = deepcopy(row['certificate'])
        damaged['problem_sha256'] = '0' * 64
        expect_error(lambda: CheckedRange(original, damaged))
        summaries.append(dict(name=row['name'],components=len(ranges),points=len(good),
                              rejected_points=len(bad),bands=len(bands),compile_ns=compiled_ns,
                              witness_query_ns=query_ns))
        all_witnesses.append(dict(name=row['name'],witnesses=witnesses))
    result = dict(status='PASS',label='DEVELOPMENT, exposed inputs, same-model',
                  python=platform.python_version(),cases=summaries,
                  points=sum(r['points'] for r in summaries),
                  rejected_points=sum(r['rejected_points'] for r in summaries),
                  bands=sum(r['bands'] for r in summaries))
    (HERE / 'service_witnesses.json').write_text(json.dumps(all_witnesses,indent=2)+'\n',encoding='utf-8')
    (HERE / 'service_result.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k != 'cases'}))


if __name__ == '__main__':
    try:
        main()
    except BaseException:
        (HERE / 'service_failure.txt').write_text(traceback.format_exc(),encoding='utf-8')
        raise
