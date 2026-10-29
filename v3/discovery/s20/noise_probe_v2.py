"""Frozen exact finite checks of the constant-noise SAT reduction."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import gzip
import hashlib
import json
import platform
import sys
import time
import traceback
from audit_inputs import encoded
from cert_audit import produce, source_value, V
from lp_witness import dot

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def model(p, clauses):
    n = p+1
    d = 2*n
    rows, rhs = [], []
    for j in range(d):
        row = [F(int(j == a)) for a in range(d)]
        rows.extend([row, [-v for v in row]])
        rhs.extend([F(1), F(0)])
    for j in range(n):
        row = [F(int(a//2 == j)) for a in range(d)]
        rows.extend([row, [-v for v in row]])
        rhs.extend([F(21,20), F(-19,20)])
    gs = []
    for i in range(2):
        a, b = [r[:] for r in rows], rhs[:]
        if i == 0:
            for clause in clauses:
                row = [F(0)]*d
                row[2*p] = F(-1)
                for literal in clause:
                    assert 1 <= abs(literal) <= p
                    row[2*(abs(literal)-1)+int(literal < 0)] -= 1
                a.append(row)
                b.append(F(-1,2))
        c = [F(0)]*d
        if i == 0:
            c[2*p] = F(1)
        gs.append(dict(A=a, b=b, c=c, d=F(2*i)))
    rs = []
    for j in range(d):
        row = [F(-int(j == a)) for a in range(d)]
        rs.append(dict(lo=F(-1), hi=F(-19,20),
                       forms=[dict(c=row[:], d=F(0)) for _ in range(2)]))
    return encoded(dict(generators=gs, receipts=rs))


def satisfies(bits, clauses):
    return all(any(bits[abs(l)-1] == (l > 0) for l in clause) for clause in clauses)


def source(bits, gate, interior=False):
    high, low = (F(39,40), F(1,40)) if interior else (F(1), F(0))
    first = []
    for bit in list(bits)+[gate]:
        first.extend([high,low] if bit else [low,high])
    return [first, [F(1)-v for v in first]]


def with_gate(bits, q):
    points = source(bits, q >= F(19,20))
    if q >= F(19,20):
        points[0][-2:] = [q,F(0)]
        points[1][-2:] = [F(0),F(1)]
    else:
        points[0][-2:] = [q,F(19,20)]
        points[1][-2:] = [F(19,20),F(1,20)]
    return points


def strict_ball(problem, points):
    radius = F(1,100)
    for g, point in zip(problem['generators'], points):
        for row, b in zip(g['A'], g['b']):
            a = list(map(F,row))
            assert dot(a,point)+radius*sum(map(abs,a)) < F(b)
    for receipt in problem['receipts']:
        # All old minima remain above lo; at least one remains below hi.
        upper = []
        for form, point in zip(receipt['forms'], points):
            c = list(map(F,form['c']))
            center = dot(c,point)+F(form['d'])
            deviation = radius*sum(map(abs,c))
            assert center-deviation > F(receipt['lo'])
            upper.append(center+deviation)
        assert min(upper) < F(receipt['hi'])


def run(name):
    frozen = json.loads((HERE/'noise_freeze_v2.json').read_text())
    for path, digest in frozen['sha256'].items():
        assert sha(ROOT/path) == digest, path
    out = HERE/'noise_runs'/name
    out.mkdir(parents=True,exist_ok=False)
    (out/'freeze.json').write_text(json.dumps(frozen,indent=2)+'\n')
    path = out/'records.jsonl.gz'
    start = time.perf_counter_ns()
    summaries = []
    try:
        with gzip.open(path,'wt',encoding='utf-8') as records:
            for case in json.loads((HERE/'noise_inputs.json').read_text()):
                p, clauses = case['variables'], case['clauses']
                satisfying = [bits for bits in product((False,True),repeat=p)
                              if satisfies(bits,clauses)]
                problem = model(p,clauses)
                known = source([True]*p,True,True)
                assert source_value(problem,known) == F(39,40)
                strict_ball(problem,known)
                # Full-dimensionality of each unconditioned base.
                for g in problem['generators']:
                    midpoint = [F(1,2)]*len(g['c'])
                    assert all(dot(list(map(F,r)),midpoint)<F(b)
                               for r,b in zip(g['A'],g['b']))
                records.write(json.dumps(encoded(dict(kind='input',case=case,problem=problem)),sort_keys=True)+'\n')
                records.flush()
                cert = produce(problem)
                records.write(json.dumps(dict(kind='produced',name=case['name'],certificate=cert),sort_keys=True)+'\n')
                records.flush()
                answer = V.verify(problem,cert)
                expected = ([['0','1/10']] if satisfying else [])+[['19/20','1']]
                assert answer['ranges'] == expected
                sources = []
                points = [(F(19,20),[True]*p),(F(39,40),[True]*p),(F(1),[True]*p)]
                if satisfying:
                    points += [(q,satisfying[0]) for q in (F(0),F(1,20),F(1,10))]
                    strict_ball(problem,source(satisfying[0],False,True))
                for q,bits in points:
                    witness = with_gate(bits,q)
                    assert source_value(problem,witness) == q
                    sources.append(dict(q=q,source=witness))
                row = dict(case=case,satisfying_assignments=satisfying,problem=problem,
                           known_source=known,radius=F(1,100),certificate=cert,
                           answer=answer,source_checks=sources)
                records.write(json.dumps(encoded(row),sort_keys=True)+'\n')
                records.flush()
                summaries.append(dict(name=case['name'],satisfying=len(satisfying),
                                      ranges=answer['ranges'],source_checks=len(sources),
                                      local_slices=sum(map(len,cert['faces']))))
        result = dict(status='PASS',classification='same-model DEVELOPMENT extension',
                      cases=summaries,elapsed_ns=time.perf_counter_ns()-start,
                      records_sha256=sha(path),freeze_sha256=sha(out/'freeze.json'),
                      python=sys.version,platform=platform.platform())
        (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result),flush=True)
    except Exception:
        (out/'failure.txt').write_text(traceback.format_exc(),encoding='utf-8')
        raise


if __name__ == '__main__':
    run(sys.argv[1])
