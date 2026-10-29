"""Prospectively bounded, exposed-input development check of partial.py."""
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
import gzip
import hashlib
import json
import platform
import sys
import time
import traceback
from partial import PartialRange, V
from audit_inputs import encoded
from service_probe import exact_source

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
NAMES = ('no_receipts', 'noisy_envelope', 'degenerate_segment', 'huge_constant',
         'inconsistent_constant', 'maximal_cover_loss')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contained(pair, union):
    return any(a <= pair[0] <= pair[1] <= b for a, b in union)


def pairs(rows):
    return [tuple(map(F, r)) for r in rows]


def snapshot(service, problem, certificate, bands, previous):
    bracket = service.bracket()
    inner, outer, exact = [pairs(r) for r in
                            (bracket['inner'], bracket['outer'], certificate['ranges'])]
    assert all(contained(pair, exact) for pair in inner)
    assert all(contained(pair, outer) for pair in exact)
    if previous:
        assert all(contained(pair, inner) for pair in pairs(previous['inner']))
        assert all(contained(pair, pairs(previous['outer'])) for pair in outer)
    state = service.state()
    for i, row in enumerate(certificate['faces']):
        for mask, entry in enumerate(row):
            if entry['kind'] == 'bounded':
                assert mask in state['outer'][i]
                lo, hi = state['outer'][i][mask]
                assert lo <= F(entry['lo']) <= F(entry['hi']) <= hi
            else:
                assert mask not in state['inner'][i]
            if mask in state['inner'][i]:
                lo, hi, *_ = state['inner'][i][mask]
                assert F(entry['lo']) <= lo <= hi <= F(entry['hi'])
    answers = []
    for lo, hi in bands:
        answer = service.query(str(lo), str(hi))
        hit = any(a <= hi and lo <= b for a, b in exact)
        if answer['status'] == 'ATTAINABLE':
            assert hit and lo <= F(answer['q']) <= hi
            exact_source(problem, answer)
        elif answer['status'] == 'EXCLUDED':
            assert not hit
        else:
            assert answer['status'] == 'UNRESOLVED'
        if bracket['exact']:
            assert (answer['status'] == 'ATTAINABLE') == hit
            assert answer['status'] != 'UNRESOLVED'
        answers.append(dict(band=[str(lo), str(hi)], answer=answer))
    return bracket, answers


def reject(service, label, operation):
    before = service.state()
    try:
        operation()
    except (ValueError, TypeError, KeyError, ZeroDivisionError) as error:
        assert service.state() == before
        return dict(label=label, exception=type(error).__name__, message=str(error))
    raise AssertionError('accepted invalid evidence: '+label)


def manual_problem(infeasible=False):
    g = dict(A=[['1'], ['-1']], b=['1', '0'], c=['1'], d='0')
    first = dict(lo='0', hi='1/5' if infeasible else '1/2', forms=[dict(c=['1'], d='0')])
    second = dict(lo='0', hi='1/5' if infeasible else '1',
                  forms=[dict(c=['-1' if infeasible else '1'], d='1' if infeasible else '0')])
    third = dict(lo='0', hi='1', forms=[dict(c=['0'], d='0')])
    return dict(generators=[g], receipts=[first, second, third])


def manual_controls():
    p = manual_problem()
    service = PartialRange(p)
    digest = service.problem_sha256
    # Base rows 0,1. Receipt lower/upper row pairs 2/3,4/5,6/7.
    upper = ['0']*8
    upper[3] = '1'
    result = service.add_dual(0, 7, 'upper', upper, digest)
    assert result['core'] == 1
    state = service.state()
    assert {t for t, (_, hi) in state['outer'][0].items() if hi == F(1,2)} == {1,3,5,7}
    point = service.add_point(0, ['3/4'], digest)
    assert point['cover'] == 6 and set(service.state()['inner'][0]) == {0,2,4,6}
    # A valid base-only lower certificate has empty core and reaches all masks.
    lower = ['0']*8
    lower[1] = '1'
    assert service.add_dual(0, 7, 'lower', lower, digest)['core'] == 0
    rejects = []
    operations = [
        ('digest', lambda: service.add_point(0, ['0'], '0'*64)),
        ('negative_block', lambda: service.add_point(-1, ['0'], digest)),
        ('bool_block', lambda: service.add_point(False, ['0'], digest)),
        ('negative_mask', lambda: service.add_dual(0, -1, 'upper', upper, digest)),
        ('extra_mask', lambda: service.add_dual(0, 8, 'upper', upper, digest)),
        ('dimension', lambda: service.add_point(0, [], digest)),
        ('float_point', lambda: service.add_point(0, [0.5], digest)),
        ('infeasible_point', lambda: service.add_point(0, ['2'], digest)),
        ('negative_dual', lambda: service.add_dual(0, 7, 'upper', ['-1']+['0']*7, digest)),
        ('wrong_identity', lambda: service.add_dual(0, 7, 'upper', ['0']*8, digest)),
        ('nonstrict_farkas', lambda: service.add_dual(0, 7, 'empty', ['0']*8, digest)),
        ('bad_side', lambda: service.add_dual(0, 7, 'sideways', upper, digest)),
        ('reversed_query', lambda: service.query('1', '0')),
        ('bad_passes', lambda: service.propagate_box(0, 0, -1)),
    ]
    entry = dict(kind='bounded', lo='0', hi='1/2', xlo=['0'], xhi=['1/2'], dlo=lower, dhi=upper)
    broken = deepcopy(entry)
    broken['dhi'] = ['0']*8
    operations.append(('late_bad_dual_atomic', lambda: service.add_certificate(0, 7, broken, digest)))
    extra = dict(entry, note='unrecognized')
    operations.append(('extra_fields', lambda: service.add_certificate(0, 7, extra, digest)))
    wrong = dict(entry, hi='3/4')
    operations.append(('wrong_endpoint', lambda: service.add_certificate(0, 7, wrong, digest)))
    for label, operation in operations:
        rejects.append(reject(service, label, operation))
    service.add_certificate(0, 7, entry, digest)
    assert service.bracket()['exact']
    exact_source(p, service.query('1/4', '1/4'))
    original = service.state()
    p['generators'][0]['d'] = '100'
    entry['xlo'][0] = '100'
    returned = service.state()
    returned['outer'].clear()
    assert service.state() == original
    # Two selected upper rows contradict; the third is irrelevant.
    empty = PartialRange(manual_problem(True))
    weights = ['0']*8
    weights[3] = weights[5] = '1'
    result = empty.add_dual(0, 7, 'empty', weights, empty.problem_sha256)
    assert result['core'] == 3
    assert set(empty.state()['outer'][0]) == {0,1,2,4,5,6}
    assert empty.bracket()['inconsistent']
    assert empty.query('0', '1')['status'] == 'EXCLUDED'
    return dict(support_upper_core=1, point_cover=6, farkas_core=3,
                rejects=rejects, final=service.bracket(), empty=empty.bracket())


def main():
    attempt = HERE/'partial_runs'/sys.argv[1]
    attempt.mkdir(parents=True, exist_ok=False)
    freeze_path = HERE/'partial_freeze.json'
    freeze = json.loads(freeze_path.read_text(encoding='utf-8'))
    for name, expected in freeze['sha256'].items():
        assert sha(ROOT/name) == expected, name
    (attempt/'freeze.json').write_bytes(freeze_path.read_bytes())
    started = time.perf_counter_ns()
    summaries = []
    try:
        with gzip.open(attempt/'records.jsonl.gz', 'wt', encoding='utf-8') as saved:
            def save(record):
                saved.write(json.dumps(encoded(record), sort_keys=True)+'\n')
                saved.flush()
            rows = [json.loads(line) for line in (HERE/'audit_records.jsonl').read_text().splitlines()]
            for name in NAMES:
                row = next(r for r in rows if r['name'] == name)
                p, cert = row['problem'], row['certificate']
                V.verify(p, cert)
                service = PartialRange(p)
                exact = pairs(cert['ranges'])
                probes = {F(-10**401), F(10**401)}
                for lo, hi in exact:
                    probes.update((lo, hi, (lo+hi)/2))
                for (_, hi), (lo, _) in zip(exact, exact[1:]):
                    probes.add((hi+lo)/2)
                if not exact:
                    probes.update((F(-1), F(0), F(1)))
                ordered = sorted(probes)
                bands = [(q, q) for q in ordered]+list(zip(ordered, ordered[1:]))
                previous, answers = snapshot(service, p, cert, bands, None)
                assert previous['inner'] == [] and not previous['inconsistent']
                save(dict(name=name, step='initial', bracket=previous, answers=answers))
                total_answers = len(answers)
                source_answers = sum(a['answer']['status'] == 'ATTAINABLE' for a in answers)
                unknown = service.query('-5/4', '-6/5') if name == 'noisy_envelope' else None
                stats = []
                for i, faces in enumerate(cert['faces']):
                    for mask in range(len(faces)):
                        update = service.propagate_box(i, mask, passes=2)
                        stats.append(update)
                        previous, answers = snapshot(service, p, cert, bands, previous)
                        save(dict(name=name, step='box', block=i, mask=mask, update=update,
                                  bracket=previous, answers=answers))
                        total_answers += len(answers)
                        source_answers += sum(a['answer']['status'] == 'ATTAINABLE' for a in answers)
                after_box = service.query('-5/4', '-6/5') if name == 'noisy_envelope' else None
                delivered, first_exact = 0, 0 if previous['exact'] else None
                for i, faces in enumerate(cert['faces']):
                    for mask, entry in enumerate(faces):
                        update = service.add_certificate(i, mask, entry, service.problem_sha256)
                        delivered += 1
                        previous, answers = snapshot(service, p, cert, bands, previous)
                        save(dict(name=name, step='certificate', block=i, mask=mask, update=update,
                                  bracket=previous, answers=answers))
                        total_answers += len(answers)
                        source_answers += sum(a['answer']['status'] == 'ATTAINABLE' for a in answers)
                        if previous['exact'] and first_exact is None:
                            first_exact = delivered
                assert previous['exact'] and previous['inner'] == cert['ranges']
                summary = dict(name=name, supplied_certificates=delivered,
                               first_exact_after_certificates=first_exact,
                               query_answers=total_answers, source_answers=source_answers,
                               compilations=service.compilations,
                               propagation_row_visits=sum(s['row_visits'] for s in stats),
                               coordinate_updates=sum(s['coordinate_updates'] for s in stats),
                               retained_evidence_bytes=len(json.dumps(encoded(service.state()['evidence'])).encode()),
                               noisy_query_before=unknown, noisy_query_after_box=after_box)
                summaries.append(summary)
                save(dict(summary=summary))
            manual = manual_controls()
            save(dict(manual=manual))
            unsupported = []
            for row in rows:
                if row['name'] in NAMES:
                    continue
                try:
                    PartialRange(row['problem'])
                except ValueError as error:
                    assert 'explicit finite coordinate bounds' in str(error)
                    unsupported.append(dict(name=row['name'], error=str(error)))
                else:
                    raise AssertionError('unexpected explicit box in unselected transformed input')
            save(dict(unsupported=unsupported))
        result = dict(status='PASS', label='DEVELOPMENT; same model; exposed controls',
                      python=platform.python_version(), cases=summaries,
                      unsupported_inputs=unsupported, manual=manual,
                      new_optimizer_calls=0, elapsed_ns=time.perf_counter_ns()-started,
                      records_sha256=sha(attempt/'records.jsonl.gz'), freeze_sha256=sha(freeze_path))
        (attempt/'result.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
        print(json.dumps(dict(status='PASS', cases=len(summaries), elapsed_ns=result['elapsed_ns'],
                             query_answers=sum(r['query_answers'] for r in summaries),
                             source_answers=sum(r['source_answers'] for r in summaries))))
    except BaseException:
        (attempt/'failure.txt').write_text(traceback.format_exc(), encoding='utf-8')
        raise


if __name__ == '__main__':
    main()
