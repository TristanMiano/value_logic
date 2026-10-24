"""Exact dual enclosure for one shared-source contrast; DEVELOPMENT.

The floating solver only proposes multipliers. This script rebuilds the
linear identity with rational coefficients and checks positive definiteness.
"""
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter_ns
import hashlib
import json
import platform

HERE = Path(__file__).resolve().parent
OUT = HERE/'paired_cert_result.json'
if OUT.exists():
    raise SystemExit('Refusing to overwrite observed evidence.')
start = perf_counter_ns()
proposal_path = HERE/'paired_result.json'
proposal = json.loads(proposal_path.read_text())['cases'][0]
assert proposal['case'] == 'scalar_caps'
raw_duals = proposal['shared_source']['duals']
assert len(raw_duals) == 19


def scalar(x):
    while isinstance(x, list):
        assert len(x) == 1
        x = x[0]
    return F(round(float(x)*10**8), 10**8)


def form(*terms):
    result = {}
    for space, i, j, coefficient in terms:
        key = (space, min(i, j), max(i, j))
        result[key] = result.get(key, F(0))+F(coefficient)
    return {k: v for k, v in result.items() if v}


def add(target, source, multiplier=F(1)):
    for key, value in source.items():
        target[key] = target.get(key, F(0))+multiplier*value


# G = Gram[W,R,r0,u0,r1,u1], H = Gram[X,x0,z0,x1,z1].
# Each row represents A(G,H)=b or A(G,H)<=b in the numerical proposal order.
rows = [(form(('G', 0, 0, 1)), F(1), 'eq'),
        (form(('G', 0, 1, 1)), F(1, 10), 'eq'),
        (form(('G', 1, 1, 1), ('H', 0, 0, 1)), F(1, 10), 'eq')]
rs, us, xs, zs = [2, 4], [3, 5], [1, 3], [2, 4]
for r, u, x, z in zip(rs, us, xs, zs):
    rows += [
        (form(('G', 1, 0, 1), ('G', 1, r, -1), ('G', 1, u, -1),
              ('H', 0, x, -1)), F(0), 'eq'),
        (form(('G', 0, r, 1), ('G', 1, r, -1), ('H', 0, x, -1),
              ('H', 0, z, 1)), F(0), 'eq'),
        (form(('G', r, u, 1), ('H', x, z, -1)), F(0), 'eq'),
        (form(('G', u, u, 1), ('H', x, x, -1)), F(0), 'le'),
        (form(('H', z, z, 1), ('G', r, r, -1)), F(0), 'le')]
for i in range(2):
    for j in range(2):
        rows.append((form(('G', rs[i], 0, 1), ('G', rs[i], rs[j], -1),
                          ('G', rs[i], us[j], -1), ('H', xs[i], xs[j], -1),
                          ('H', zs[i], xs[j], 1)), F(0), 'eq'))
assert len(rows) == 17
multipliers = [scalar(q) for q in raw_duals[2:]]
objective = form(('G', 0, 2, 1), ('G', 0, 4, -1))
slack_form = {}
add(slack_form, objective, F(-1))
constant = F(0)
for multiplier, (affine, rhs, kind) in zip(multipliers, rows):
    if kind == 'le':
        assert multiplier >= 0
    add(slack_form, affine, multiplier)
    constant += multiplier*rhs


def matrix(space, size):
    result = [[F(0) for _ in range(size)] for _ in range(size)]
    for (sp, i, j), value in slack_form.items():
        if sp != space:
            continue
        if i == j:
            result[i][j] += value
        else:
            result[i][j] += value/2
            result[j][i] += value/2
    return result


def positive_pivots(a):
    a = [row[:] for row in a]
    pivots = []
    for k in range(len(a)):
        pivot = a[k][k]
        assert pivot > 0, (k, str(pivot))
        pivots.append(pivot)
        for i in range(k+1, len(a)):
            for j in range(k+1, len(a)):
                a[i][j] -= a[i][k]*a[k][j]/pivot
    return pivots


shift = F(1, 10**6)
SG, SH = matrix('G', 6), matrix('H', 5)
for mat in (SG, SH):
    for i in range(len(mat)):
        mat[i][i] += shift
pg, ph = positive_pivots(SG), positive_pivots(SH)
# ||r_i||^2+||x_i||^2=F_i<=1, ||u_i||^2<=||x_i||^2,
# ||z_i||^2<=||r_i||^2. The conservative separate trace bounds suffice.
TG, TH = F(51, 10), F(41, 10)
upper = constant+shift*(TG+TH)
assert upper < F(27, 125)
assert F(27, 125) < F(11, 50)
assert F(11, 5)**2 < 5  # Separate sharp width sqrt(5)/10 exceeds 11/50.

# A genuine finite two-output source giving a near-matching contrast.
# M=diag(a,L), W=(sqrt(p),sqrt(1-p))^T, and edits diag(-1,0),diag(1,0).
a, big, s = F(63, 40), F(1000), F(1, 10)
lam, nu = 1/(1+a*a), 1/(1+big*big)
p = (s-nu)/(lam-nu)
assert 0 < p < 1 and p*lam+(1-p)*nu == s
plus = p/(1+(a-1)**2)+(1-p)*nu
minus = p/(1+(a+1)**2)+(1-p)*nu
witness = plus-minus
limit = s/lam*(1/(1+(a-1)**2)-1/(1+(a+1)**2))
assert F(2159, 10000) < witness < upper

encode = lambda a: [[str(q) for q in row] for row in a]
record = dict(status='PASS', scope='Exact universal contrast upper bound at C=1/10, e0=e1=1, plus a genuine finite lower witness; not the exact optimum.',
              upper_bound=str(upper), upper_decimal=float(upper),
              unshifted_constant=str(constant), psd_shift=str(shift),
              trace_bounds=[str(TG), str(TH)], multipliers=list(map(str, multipliers)),
              shifted_output_slack=encode(SG), shifted_input_slack=encode(SH),
              exact_positive_pivots=[list(map(str, pg)), list(map(str, ph))],
              finite_witness=dict(a=str(a), L=str(big), weight=str(p),
                                  old_value=str(s), upper_value=str(plus), lower_value=str(minus),
                                  contrast=str(witness), contrast_decimal=float(witness),
                                  limiting_contrast=str(limit), limiting_decimal=float(limit)),
              elapsed_ns=perf_counter_ns()-start, python=platform.python_version(),
              source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              proposal_sha256=hashlib.sha256(proposal_path.read_bytes()).hexdigest())
OUT.write_text(json.dumps(record, indent=2)+'\n', encoding='utf-8', newline='\n')
print(json.dumps(dict(status='PASS', upper=float(upper), witness=float(witness),
                     elapsed_ns=record['elapsed_ns'])))
