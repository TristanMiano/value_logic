"""Exact finite full-simplex information certificates, P3-02 DEVELOPMENT.

ChatGPT (GPT-6 Astra Pro), 2026-10-07.

Input JSON: n_states, losses (rows), optional targets (default identity), and
calibration in {known, unknown_offset, unknown_scale, unknown_affine}.
Integers and rational strings are exact; binary floats are rejected.

Every old and added row is a known statewise loss under one common law. The
four contracts are v=Lp, v=Lp+b1, v=sLp, v=sLp+b1, with s>0 and unrestricted b.
Known units have already been converted to the canonical s=1,b=0 convention.
The tool cannot establish these semantic premises from the numbers. It does
not analyze learned or realized losses, restricted law families, arbitrary
nuisance mechanisms, native unit eligibility, access cost or decision-only
sufficiency. Ordinary probability methods can use these same certificates.

The output either supplies exact row identities or actual distinct-law
collisions, and freely-selected fixed linear-query repair counts. It is not
a generic LP solver, learner, final challenge or contribution-support test.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import platform
try:
    import resource
except ModuleNotFoundError:  # CPU counters are unavailable on some platforms.
    resource = None
import sys
import time

sys.dont_write_bytecode = True
CALIBRATIONS = {'known', 'unknown_offset', 'unknown_scale', 'unknown_affine'}


def rational(value):
    if type(value) is int:
        return F(value)
    if type(value) is str:
        try:
            return F(value)
        except (ValueError, ZeroDivisionError) as exc:
            raise ValueError('Expected a finite exact rational string.') from exc
    raise ValueError('Use integers or rational strings; floats and booleans are not exact inputs.')


def matrix(value, n, name):
    if not isinstance(value, list):
        raise ValueError(f'{name} must be a list of rows.')
    result = []
    for row in value:
        if not isinstance(row, list) or len(row) != n:
            raise ValueError(f'Every {name} row must have n_states entries.')
        result.append([rational(x) for x in row])
    return result


def dot(a, b):
    if len(a) != len(b):
        raise ValueError('Dot-product dimensions do not match.')
    return sum((x*y for x, y in zip(a, b)), F(0))


def rref(rows, n):
    """Reduced rows and pivots, with zero/redundant rows and empty matrices allowed."""
    a = [list(row) for row in rows]
    if any(len(row) != n for row in a):
        raise ValueError('Matrix dimensions do not match.')
    pivots = []
    k = 0
    for col in range(n):
        pivot = next((i for i in range(k, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[k], a[pivot] = a[pivot], a[k]
        divisor = a[k][col]
        a[k] = [v/divisor for v in a[k]]
        for i in range(len(a)):
            if i != k and a[i][col]:
                factor = a[i][col]
                a[i] = [u-factor*v for u, v in zip(a[i], a[k])]
        pivots.append(col)
        k += 1
        if k == len(a):
            break
    return a, pivots


def rank(rows, n):
    return len(rref(rows, n)[1])


def coefficients(rows, target):
    """Return coefficients of target in the row span, or None; no rank assumption."""
    n, k = len(target), len(rows)
    augmented = [[rows[j][i] for j in range(k)] + [target[i]] for i in range(n)]
    reduced, pivots = rref(augmented, k+1)
    if k in pivots:
        return None
    result = [F(0)]*k
    for row, pivot in zip(reduced, pivots):
        result[pivot] = row[-1]
    return result


def nullspace(rows, n):
    reduced, pivots = rref(rows, n)
    result = []
    for free in (j for j in range(n) if j not in pivots):
        vector = [F(0)]*n
        vector[free] = F(1)
        for row, pivot in zip(reduced, pivots):
            vector[pivot] = -row[free]
        result.append(vector)
    return result


def is_constant(row):
    return all(x == row[0] for x in row)


def effective_rows(losses, calibration):
    if calibration in {'unknown_offset', 'unknown_affine'}:
        return [[x-y for x, y in zip(row, losses[0])] for row in losses[1:]] if losses else []
    return [list(row) for row in losses]


def observation(losses, p, scale=F(1), offset=F(0)):
    return [scale*dot(row, p)+offset for row in losses]


def collision(losses, effective, target, n, unknown_scale, unknown_offset):
    """Construct a same-record pair, including actual positive scales and offsets."""
    one = [F(1)]*n
    hidden = nullspace(effective if unknown_scale else [one]+effective, n)
    uniform = [F(1, n)]*n
    candidates = [uniform]
    if unknown_scale:
        candidates += [[(uniform[j]+F(i == j))/2 for j in range(n)] for i in range(n)]
    for h in hidden:
        total_h = sum(h, F(0))
        for p in candidates:
            if dot(target, h)-total_h*dot(target, p) == 0:
                continue
            step = min(p)/(2*max(map(abs, h)))
            x = [u+step*v for u, v in zip(p, h)]
            total = sum(x, F(0))
            if not unknown_scale and total != 1:
                raise AssertionError('A known-scale hidden direction lost normalization.')
            q = [u/total for u in x]
            scale_q = total if unknown_scale else F(1)
            offset_q = dot(losses[0], p)-scale_q*dot(losses[0], q) if unknown_offset and losses else F(0)
            y_p = observation(losses, p)
            y_q = observation(losses, q, scale_q, offset_q)
            if not (min(p)>0 and min(q)>0 and sum(p)==sum(q)==1 and scale_q>0):
                raise AssertionError('Invalid collision law or scale.')
            if y_p != y_q or dot(target, p) == dot(target, q):
                raise AssertionError('The proposed collision does not witness information loss.')
            return {'p':p, 'q':q, 'scale_p':F(1), 'scale_q':scale_q,
                    'offset_p':F(0), 'offset_q':offset_q, 'observation':y_p,
                    'target_p':dot(target,p), 'target_q':dot(target,q),
                    'hidden_direction':h, 'positive_step':step}
    raise AssertionError('A nonrecoverable row had no constructed collision witness.')


def target_certificate(losses, effective, target, n, calibration):
    unknown_scale = calibration in {'unknown_scale', 'unknown_affine'}
    unknown_offset = calibration in {'unknown_offset', 'unknown_affine'}
    one = [F(1)]*n
    if is_constant(target):
        return {'recoverable':True, 'kind':'constant', 'value':target[0]}
    if unknown_scale:
        normalizer = coefficients(effective, one)
        numerator = coefficients(effective, target)
        if normalizer is not None and numerator is not None:
            return {'recoverable':True, 'kind':'ratio_of_scaled_linear_targets',
                    'normalizer_coefficients':normalizer, 'numerator_coefficients':numerator,
                    'denominator_semantics':'the same positive scale s; not a new numerical premise'}
    else:
        weights = coefficients([one]+effective, target)
        if weights is not None:
            return {'recoverable':True, 'kind':'affine',
                    'constant':weights[0], 'effective_coefficients':weights[1:]}
    return {'recoverable':False, 'kind':'indistinguishable_laws',
            'witness':collision(losses,effective,target,n,unknown_scale,unknown_offset)}


def repair(losses, effective, targets, n, calibration):
    """Sharp repair for arbitrary fixed known rows under the shared-nuisance contract."""
    if all(is_constant(c) for c in targets):
        return {'minimum_extra_raw_queries':0, 'extra_loss_rows':[],
                'effective_rank_deficit':0, 'new_reference_queries':0}
    unknown_scale = calibration in {'unknown_scale', 'unknown_affine'}
    unknown_offset = calibration in {'unknown_offset', 'unknown_affine'}
    one = [F(1)]*n
    basis = [list(row) for row in effective] if unknown_scale else [one]+[list(row) for row in effective]
    required = [one]+targets if unknown_scale else targets
    initial_basis = [list(row) for row in basis]
    initial_rank = rank(basis,n)
    selected = []
    current_rank = initial_rank
    for row in required:
        new_rank = rank(basis+[row],n)
        if new_rank>current_rank:
            selected.append(list(row))
            basis.append(list(row))
            current_rank=new_rank
    new_reference = int(unknown_offset and not losses)
    reference = losses[0] if unknown_offset and losses else [F(0)]*n
    extra = ([[F(0)]*n] if new_reference else [])
    extra += [[a+b for a,b in zip(reference,q)] if unknown_offset else q for q in selected]
    equations = initial_basis + selected
    transposed = [[row[i] for row in equations] for i in range(n)]
    hidden_pairing = []
    for j in range(len(selected)):
        rhs = [F(0)]*len(initial_basis) + [F(i==j) for i in range(len(selected))]
        h = coefficients(transposed,rhs)
        if h is None:
            raise AssertionError('Repair rows were not independent modulo old information.')
        hidden_pairing.append(h)
    return {'minimum_extra_raw_queries':current_rank-initial_rank+new_reference,
            'extra_loss_rows':extra, 'added_effective_rows':selected,
            'lower_bound_hidden_directions':hidden_pairing,
            'effective_rank_deficit':current_rank-initial_rank,
            'new_reference_queries':new_reference,
            'scope':'freely chosen fixed known rational rows, all sharing the original law and nuisance; no restricted-menu or decision-only minimum'}


def audit(request):
    if not isinstance(request,dict):
        raise ValueError('Input must be a JSON object.')
    if set(request)-{'n_states','losses','targets','calibration'}:
        raise ValueError('Unsupported input fields; this tool accepts only its declared full-simplex contract.')
    n=request.get('n_states')
    if type(n) is not int or n<1:
        raise ValueError('n_states must be a positive integer.')
    calibration=request.get('calibration','known')
    if type(calibration) is not str or calibration not in CALIBRATIONS:
        raise ValueError('Unsupported calibration contract.')
    losses=matrix(request.get('losses'),n,'losses')
    default=[[int(i==j) for j in range(n)] for i in range(n)]
    targets=matrix(request.get('targets',default),n,'targets')
    effective=effective_rows(losses,calibration)
    unknown_scale=calibration in {'unknown_scale','unknown_affine'}
    base=effective if unknown_scale else [[F(1)]*n]+effective
    rows=[target_certificate(losses,effective,c,n,calibration) for c in targets]
    full_law = n==1 or rank(base,n)==n
    law_rows = []
    for i, c in enumerate([[F(i==j) for j in range(n)] for i in range(n)]):
        cert = target_certificate(losses,effective,c,n,calibration)
        law_rows.append(cert)
        if not full_law and not cert['recoverable']:
            law_certificate = {'kind':'separating_coordinate','coordinate':i,'certificate':cert}
            break
    else:
        if not full_law:
            raise AssertionError('Full-law flag contradicts coordinate certificates.')
        law_certificate = {'kind':'coordinate_decoders','coordinates':law_rows}
    repair_record = repair(losses,effective,targets,n,calibration)
    enlarged = losses + repair_record['extra_loss_rows']
    enlarged_effective = effective_rows(enlarged,calibration)
    repair_record['repaired_target_certificates'] = [
        target_certificate(enlarged,enlarged_effective,c,n,calibration) for c in targets]
    if not all(c['recoverable'] for c in repair_record['repaired_target_certificates']):
        raise AssertionError('Proposed repair did not recover every requested target.')
    return {'schema':'P3-02-finite-information-audit/v1','stage':'development',
            'n_states':n,'calibration':calibration,'losses':losses,'targets':targets,
            'effective_rows':effective,'effective_rank':rank(effective,n),
            'normalization_augmented_rank':rank([[F(1)]*n]+effective,n),
            'full_law_recoverable':full_law,'law_certificate':law_certificate,
            'all_targets_recoverable':all(r['recoverable'] for r in rows),
            'target_certificates':rows,'repair':repair_record,
            'semantic_boundary':'Conditional on known statewise rows, one fixed supplied law in the full simplex, exact expected losses and the declared shared nuisance. Numeric validation does not establish those premises.'}


def jsonable(value):
    if isinstance(value,F): return str(value)
    if isinstance(value,list): return [jsonable(x) for x in value]
    if isinstance(value,dict): return {k:jsonable(v) for k,v in value.items()}
    return value


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,required=True)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    if args.output and args.output.exists():
        raise SystemExit('Refusing to overwrite an existing result.')
    source_bytes=Path(__file__).read_bytes()
    input_bytes=args.input.read_bytes()
    start_utc=datetime.now(timezone.utc).isoformat()
    start_ns=time.monotonic_ns()
    before=resource.getrusage(resource.RUSAGE_SELF) if resource is not None else None
    result=audit(json.loads(input_bytes))
    after=resource.getrusage(resource.RUSAGE_SELF) if resource is not None else None
    end_ns=time.monotonic_ns()
    result['execution']={'start_utc':start_utc,'end_utc':datetime.now(timezone.utc).isoformat(),
                         'elapsed_ns':end_ns-start_ns,'user_cpu_seconds':after.ru_utime-before.ru_utime if after is not None else None,
                         'system_cpu_seconds':after.ru_stime-before.ru_stime if after is not None else None,'python':platform.python_version(),
                         'argv':sys.argv,'script_sha256':hashlib.sha256(source_bytes).hexdigest(),
                         'input_sha256':hashlib.sha256(input_bytes).hexdigest()}
    rendered=json.dumps(jsonable(result),indent=2)+'\n'
    if args.output:
        with args.output.open('x') as stream:
            stream.write(rendered)
        print(json.dumps({'output':str(args.output),'all_targets_recoverable':result['all_targets_recoverable'],
                          'minimum_extra_raw_queries':result['repair']['minimum_extra_raw_queries']}))
    else:
        print(rendered,end='')


if __name__=='__main__':
    main()
