"""Prospective exact-control comparison for the greatest-point shortcut."""
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
import gzip
import hashlib
import json
import sys
import time
import traceback
import scipy.optimize
import greatest as G
from cert_audit import produce as full_produce, source_value

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def reject(label, operation):
    try: operation()
    except (ValueError,KeyError,TypeError) as e:
        return dict(label=label,error=str(e))
    raise AssertionError('invalid input accepted: '+label)


def main():
    dest = HERE/'greatest_runs'/sys.argv[1]
    dest.mkdir(parents=True,exist_ok=False)
    freeze_path = HERE/'greatest_freeze.json'
    freeze = json.loads(freeze_path.read_text())
    for name,expected in freeze['sha256'].items():
        assert sha(ROOT/name) == expected,name
    (dest/'freeze.json').write_bytes(freeze_path.read_bytes())
    calls = 0
    actual = scipy.optimize.linprog
    def counted(*args,**kwargs):
        nonlocal calls
        calls += 1
        return actual(*args,**kwargs)
    scipy.optimize.linprog = counted
    started = time.perf_counter_ns()
    summaries = []
    try:
        with gzip.open(dest/'records.jsonl.gz','wt',encoding='utf-8') as out:
            def save(record):
                out.write(json.dumps(record,sort_keys=True)+'\n')
                out.flush()
            inputs = json.loads((HERE/'greatest_inputs.json').read_text())
            for row in inputs:
                p = row['problem']
                save(dict(name=row['name'],problem=p))
                before = calls
                cert = G.produce(p)
                short_calls = calls-before
                save(dict(name=row['name'],shortcut_certificate=cert,optimizer_calls=short_calls))
                checked = G.CheckedGreatest(p,cert)
                before = calls
                control = full_produce(p)
                full_calls = calls-before
                save(dict(name=row['name'],full_certificate=control,optimizer_calls=full_calls))
                verification = G.V.verify(p,control)
                assert checked.ranges() == verification['ranges']
                witnesses = []
                if cert['kind'] == 'interval':
                    assert short_calls == 2*len(p['generators'])
                    points = [list(map(F,e['point'])) for e in cert['peaks']]
                    masks = G.forced_masks(p,points)
                    direct = []
                    for i in range(len(points)):
                        mask = 0
                        for j,r in enumerate(p['receipts']):
                            values = [G.response(p,j,h,x) for h,x in enumerate(points) if h != i]
                            if not values or min(values) > F(r['hi']):
                                mask |= 1 << j
                        direct.append(mask)
                    assert masks == direct
                    lo,hi = map(F,cert['range'])
                    for q in sorted({lo,hi,(lo+hi)/2,(2*lo+hi)/3,(lo+2*hi)/3}):
                        w = checked.source(str(q))
                        assert source_value(p,[list(map(F,x)) for x in w['source']]) == q
                        witnesses.append(w)
                else:
                    assert not checked.ranges()
                summary = dict(name=row['name'],kind=cert['kind'],range=checked.ranges(),
                               shortcut_optimizer_calls=short_calls,full_optimizer_calls=full_calls,
                               witnesses=len(witnesses),shortcut_certificate_bytes=len(json.dumps(cert).encode()),
                               full_certificate_bytes=len(json.dumps(control).encode()))
                summaries.append(summary)
                save(dict(summary=summary,witnesses=witnesses))
            p = deepcopy(inputs[6]['problem'])
            # Use saved certificate rather than repeating successful production.
            out.flush()
        with gzip.open(dest/'records.jsonl.gz','rt',encoding='utf-8') as f:
            records = [json.loads(line) for line in f]
        cert = next(r['shortcut_certificate'] for r in records if r.get('name') == 'tied_outside' and 'shortcut_certificate' in r)
        negatives = []
        for label,mutate in [
            ('two_positive_row',lambda q:q['generators'][0].update(A=[['1','1'],['-1','0'],['0','-1']],b=['1','0','0'],c=['1','1'])),
            ('positive_receipt',lambda q:q['receipts'][0]['forms'][0].update(c=['1'])),
            ('negative_future',lambda q:q['generators'][0].update(c=['-1'])),
        ]:
            bad = deepcopy(p)
            mutate(bad)
            if label == 'two_positive_row':
                bad['receipts'][0]['forms'][0]['c'] = ['-1','0']
            negatives.append(reject(label,lambda bad=bad:G.prepare(bad)))
        for label,mutate in [
            ('binding',lambda e:e.update(problem_sha256='0'*64)),
            ('missing_peak',lambda e:e['peaks'].pop()),
            ('missing_lower',lambda e:e['lows'].pop()),
            ('wrong_range',lambda e:e.update(range=['-1','2'])),
            ('bad_primal',lambda e:e['peaks'][0].update(point=['2'])),
            ('bad_dual',lambda e:e['peaks'][0].update(dual=['0']*len(e['peaks'][0]['dual']))),
        ]:
            bad = deepcopy(cert)
            mutate(bad)
            negatives.append(reject(label,lambda bad=bad:G.CheckedGreatest(p,bad)))
        false_empty = dict(kind='missed_receipt',problem_sha256=G.V.digest(p),peaks=cert['peaks'],receipt=0)
        negatives.append(reject('false_miss',lambda:G.CheckedGreatest(p,false_empty)))
        checked = G.CheckedGreatest(p,cert)
        negatives.append(reject('query_outside',lambda:checked.source('2')))
        negatives.append(reject('float_query',lambda:checked.source(0.5)))
        expected = checked.ranges()
        p['generators'][0]['d'] = '100'
        cert['peaks'].clear()
        assert checked.ranges() == expected
        result = dict(status='PASS',label='DEVELOPMENT; same-model; finite exact controls',
                      cases=summaries,negative_controls=negatives,
                      shortcut_optimizer_calls=sum(r['shortcut_optimizer_calls'] for r in summaries),
                      full_optimizer_calls=sum(r['full_optimizer_calls'] for r in summaries),
                      witnesses=sum(r['witnesses'] for r in summaries),
                      elapsed_ns=time.perf_counter_ns()-started,freeze_sha256=sha(freeze_path),
                      records_sha256=sha(dest/'records.jsonl.gz'))
        (dest/'result.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({k:v for k,v in result.items() if k not in ('cases','negative_controls')}))
    except BaseException:
        (dest/'failure.txt').write_text(traceback.format_exc(),encoding='utf-8')
        raise
    finally:
        scipy.optimize.linprog = actual


if __name__ == '__main__':
    main()
