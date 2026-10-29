"""Frozen finite check for certificate_transport; one directory per attempt."""
from copy import deepcopy
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import platform
import random
import sys
import time
import traceback
from audit_inputs import encoded
from cert_audit import produce
import certificate_transport as T

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contained(interval, union):
    lo, hi = interval
    return any(a <= lo and hi <= b for a, b in union)


def contains_band(union, band):
    return any(a <= band[1] and band[0] <= b for a, b in union)


def expanded(problem, amount):
    p = deepcopy(problem)
    for r in p['receipts']:
        r['lo'] = str(F(r['lo'])-amount)
        r['hi'] = str(F(r['hi'])+amount)
    return p


def exact_control(p, outer, existing=None):
    cert = produce(p) if existing is None else existing
    check = T.V.verify(p, cert)
    exact = [tuple(map(F, pair)) for pair in check['ranges']]
    assert all(contained(pair, outer['ranges']) for pair in exact)
    for i, row in enumerate(cert['faces']):
        for mask, e in enumerate(row):
            if e['kind'] == 'bounded':
                o = outer['faces'][i][mask]
                assert o['kind'] == 'outer'
                assert o['lo'] <= F(e['lo']) <= F(e['hi']) <= o['hi']
    # Each nonempty face asks for both extrema; an empty face asks once
    # for a minimization and once for its Farkas proposal in this producer.
    return dict(problem=p, certificate=cert, check=check,
                minimum_extrema_calls=2*sum(len(row) for row in cert['faces']) if existing is None else 0,
                reused_control_certificate=existing is not None)


def exhaustive_radius(families, k, band):
    best = None
    for owners in product(range(len(families)), repeat=k):
        masks = [0]*len(families)
        for j, owner in enumerate(owners):
            masks[owner] |= 1 << j
        times, down = [], []
        for family, mask in zip(families, masks):
            activation, lo, hi, p, q = family[mask]
            up = T.maximum(activation, T.deficit_time(band[0]-hi, q))
            times.append(up)
            down.append(T.deficit_time(lo-band[1], p))
        all_up = F(0)
        for value in times:
            all_up = T.maximum(all_up, value)
        one_down = None
        for value in down:
            one_down = T.minimum(one_down, value)
        best = T.minimum(best, T.maximum(all_up, one_down))
    return best


def direct_union(families, k, t):
    intervals = []
    for owners in product(range(len(families)), repeat=k):
        masks = [0]*len(families)
        for j, owner in enumerate(owners):
            masks[owner] |= 1 << j
        pieces = []
        for family, mask in zip(families, masks):
            activation, lo, hi, p, q = family[mask]
            if activation is None or activation > t:
                break
            pieces.append((lo-t*p, hi+t*q))
        else:
            intervals.append((min(a for a, b in pieces), min(b for a, b in pieces)))
    return T.V.normalize(intervals)


def run(attempt):
    out = HERE/'transport_runs'/attempt
    out.mkdir(parents=True, exist_ok=False)
    freeze = json.loads((HERE/'transport_freeze.json').read_text())
    for name, sha in freeze['sha256'].items():
        assert digest(ROOT/name) == sha, name
    (out/'freeze.json').write_text(json.dumps(freeze, indent=2)+'\n')
    records = out/'records.jsonl'
    def save(value):
        with records.open('a', encoding='utf-8') as f:
            f.write(json.dumps(encoded(value), sort_keys=True)+'\n')
    before = time.perf_counter_ns()
    try:
        old_records = [json.loads(s) for s in (HERE/'audit_records.jsonl').read_text().splitlines()]
        bank = {r['name']: r for r in old_records}
        old = bank['noisy_envelope']
        p, cert = old['problem'], old['certificate']
        rng = random.Random(202820)
        controls, lp_calls = 0, 0
        for j in range(16):
            changed = deepcopy(p)
            scale = F(j+1, 200)
            for r in changed['receipts']:
                r['lo'] = str(F(r['lo'])-scale)
                r['hi'] = str(F(r['hi'])+scale)
                for f in r['forms']:
                    f['c'] = [str(F(c)+scale*F(rng.randrange(-2, 3), 10)) for c in f['c']]
                    f['d'] = str(F(f['d'])+scale*F(rng.randrange(-2, 3), 10))
            for g in changed['generators']:
                g['c'] = [str(F(c)+scale*F(rng.randrange(-2, 3), 10)) for c in g['c']]
                g['d'] = str(F(g['d'])+scale*F(rng.randrange(-2, 3), 10))
            outer = T.transport(p, cert, changed)
            control = exact_control(changed, outer)
            controls += 1
            lp_calls += control['minimum_extrema_calls']
            save(dict(kind='changed_model', index=j, outer=outer, control=control))
        inconsistent = bank['inconsistent_constant']
        changed = deepcopy(inconsistent['problem'])
        changed['receipts'][0]['lo'], changed['receipts'][0]['hi'] = '-1', '1'
        outer = T.transport(inconsistent['problem'], inconsistent['certificate'], changed)
        control = exact_control(changed, outer)
        assert outer['ranges'] and control['check']['ranges']
        assert all(e['reason'] == 'old_empty_reintroduced' for row in outer['faces'] for e in row)
        controls += 1
        lp_calls += control['minimum_extrema_calls']
        save(dict(kind='empty_revival', outer=outer, control=control,
                  shortcut_wrong_answer=[]))
        # Exact one-dimensional residual counterexample, no optimizer needed:
        # old min x on [0,1] has y=(0,1); new objective 2x has max 2.
        one = dict(kind='bounded', dlo=['0','1'], dhi=['1','0'])
        lohi = T.local_outer([[F(1)],[F(-1)]],[F(1),F(0)], [F(2)],F(0),[(F(0),F(1))],one)
        assert lohi['hi'] == 2 and F(2) > F(1)
        save(dict(kind='residual_counterexample', sound=lohi, ignored_residual_upper='1',
                  feasible_point=['1'], actual_value='2'))
        family = T.receipt_expansion_families(p, cert)
        band = (F(-5,4), F(-6,5))
        answer = T.band_radius(family, 2, band)
        radius = answer['first_outer_hit']
        assert radius is not None and radius > 0
        for t in (F(0), radius/2, radius, radius*2):
            union = T.evaluate_families(family, 2, t)
            assert contains_band(union, band) == (t >= radius)
            changed = expanded(p, t)
            outer = T.transport(p, cert, changed)
            control = exact_control(changed, outer, cert if t == 0 else None)
            assert all(contained(tuple(map(F, pair)), union) for pair in control['check']['ranges'])
            controls += 1
            lp_calls += control['minimum_extrema_calls']
            save(dict(kind='receipt_radius', time=t, band=band, radius=radius,
                      families=family, union=union, answer=answer, direct_outer=outer, control=control))
        rng = random.Random(202821)
        finite, infinite, zero = 0, 0, 0
        for j in range(120):
            n, k = 1+j%4, (j//4)%5
            families = []
            for i in range(n):
                f = {}
                for mask in range(1 << k):
                    a = None if rng.randrange(6) == 0 else F(rng.randrange(4), 3)
                    lo = F(rng.randrange(-4, 5), 2)
                    hi = lo+F(rng.randrange(4), 2)
                    f[mask] = (a, lo, hi, F(rng.randrange(3), 2), F(rng.randrange(3), 2))
                families.append(f)
            h = F(rng.randrange(-6, 7), 2)
            band = h, h+F(rng.randrange(3), 2)
            answer = T.band_radius(families, k, band)
            radius = answer['first_outer_hit']
            assert radius == exhaustive_radius(families, k, band)
            if radius is None:
                infinite += 1
                times = (F(0), F(10), F(100))
            else:
                finite += 1
                zero += int(radius == 0)
                times = sorted(set((F(0), radius/2, radius, radius+F(1,7))))
            for t in times:
                union = direct_union(families, k, t)
                assert union == T.evaluate_families(families, k, t)
                assert contains_band(union, band) == (radius is not None and t >= radius)
            save(dict(kind='artificial', index=j, n=n, k=k, families=families,
                      band=band, answer=answer, checked_times=times))
        rejects = []
        broken = deepcopy(p); broken['generators'][0]['A'].append(['0','0']);broken['generators'][0]['b'].append('1')
        no_box = deepcopy(p); no_box['generators'][0]['A'][0] = ['1','1']
        badfamily = deepcopy(family); badfamily[0][0] = (F(0), F(0), F(1), F(-1), F(0))
        omitted = deepcopy(family); del omitted[0][0]
        for name, action in (
            ('changed_indexing', lambda:T.transport(p,cert,broken)),
            ('missing_coordinate_bound', lambda:T.transport(p,cert,no_box)),
            ('negative_slope', lambda:T.band_radius(badfamily,2,band)),
            ('missing_slice', lambda:T.band_radius(omitted,2,band))):
            try:
                action()
            except ValueError as error:
                rejects.append(dict(name=name,error=str(error)))
            else:
                raise AssertionError('accepted '+name)
        result = dict(status='PASS', classification='same-model DEVELOPMENT extension',
                      changed_model_controls=controls, producer_linprog_calls=lp_calls,
                      reuse_lp_calls=0, artificial_cases=120,
                      finite_radii=finite,infinite_radii=infinite,zero_radii=zero,
                      noisy_band_first_outer_hit=T.band_radius(family,2,(F(-5,4),F(-6,5))),
                      misuse_rejections=rejects, elapsed_ns=time.perf_counter_ns()-before,
                      python=sys.version,platform=platform.platform(),
                      records_sha256=digest(records),freeze_sha256=digest(out/'freeze.json'))
        (out/'result.json').write_text(json.dumps(encoded(result),indent=2)+'\n')
        print(json.dumps(encoded(result)),flush=True)
    except Exception:
        (out/'failure.txt').write_text(traceback.format_exc(),encoding='utf-8')
        raise


if __name__ == '__main__':
    run(sys.argv[1])
