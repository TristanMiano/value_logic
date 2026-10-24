"""Focused independent arithmetic checks of the preserved s16 verifier.

DEVELOPMENT, Codex (GPT-6). Determinants/adjugates deliberately do not call
the checker's elimination helpers. These finite checks do not prove a theorem.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import copy
import hashlib
import importlib.util
import json
import platform
import sys
from time import perf_counter_ns

HERE = Path(__file__).resolve().parent
CHECKER = HERE.parent / 's16' / 'block_check.py'
spec = importlib.util.spec_from_file_location('preserved_checker', CHECKER)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def transpose(a):
    return list(map(list, zip(*a)))


def mm(a, b):
    return [[sum((x*y for x, y in zip(row, col)), F(0))
             for col in zip(*b)] for row in a]


def plus(a, b, scale=F(1)):
    return [[x+scale*y for x, y in zip(row, col)] for row, col in zip(a, b)]


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def det(a):
    if not a:
        return F(1)
    return sum(((-1)**j * a[0][j] * det([row[:j]+row[j+1:] for row in a[1:]])
                for j in range(len(a))), F(0))


def adj_inverse(a):
    denominator = det(a)
    assert denominator
    n = len(a)
    return [[(-1)**(i+j)*det([row[:i]+row[i+1:]
                              for r, row in enumerate(a) if r != j])/denominator
             for j in range(n)] for i in range(n)]


def minors_positive(a, strict=False):
    if a != transpose(a):
        return False
    ds = [det([[a[i][j] for j in subset] for i in subset])
          for size in range(1, len(a)+1)
          for subset in combinations(range(len(a)), size)]
    return all(d > 0 if strict else d >= 0 for d in ds)


def trace_product(a, b):
    return sum((a[i][j]*b[j][i] for i in range(len(a)) for j in range(len(a))), F(0))


def encode(a):
    return [[str(z) for z in row] for row in a]


def main():
    out = HERE / 'checker_audit_result.json'
    if out.exists():
        raise SystemExit('Refusing to overwrite an observed result.')
    start = perf_counter_ns()
    comparisons = 0
    for entries in product((-1, 0, 1), repeat=6):
        a, b, c, d, e, f = map(F, entries)
        matrix = [[a, b, c], [b, d, e], [c, e, f]]
        for strict in (False, True):
            assert checker.positive(matrix, strict) == minors_positive(matrix, strict)
            comparisons += 1
    # A zero pivot appears only after the first elimination, both with and
    # without a forbidden remaining off-diagonal entry.
    for matrix in ([[1,1,1],[1,1,1],[1,1,2]], [[1,1,1],[1,1,2],[1,2,5]]):
        matrix = [[F(z) for z in row] for row in matrix]
        assert checker.positive(matrix) == minors_positive(matrix)
        comparisons += 1

    m = [[F(1),F(2)], [F(2),F(-1)], [F(1),F(1)]]
    s = adj_inverse(plus(eye(3), mm(m, transpose(m))))
    c = [row[:2] for row in s[:2]]
    direction = [[F(3,5)], [F(4,5)]]
    v = mm(direction, transpose(direction))
    u = [[F(3,5)], [F(4,5)], [F(0)]]
    right = [[F(5,13),F(12,13)]]
    delta = [[z/F(10) for z in row] for row in mm(u,right)]
    assert mm(transpose(u),u) == [[F(1)]]
    assert mm(right,transpose(right)) == [[F(1)]]
    n = plus(m,delta)
    sn = adj_inverse(plus(eye(3),mm(n,transpose(n))))
    actual = trace_product(v,[row[:2] for row in sn[:2]])
    # These bracket errors do not commute with the true compression.
    left_error = [[F(2,10000),F(1,10000)],[F(1,10000),F(2,10000)]]
    right_error = [[F(3,10000),F(-1,10000)],[F(-1,10000),F(2,10000)]]
    lo, hi = plus(c,left_error,-1), plus(c,right_error)
    assert mm(c,lo) != mm(lo,c) and mm(c,hi) != mm(hi,c)
    for a in (lo,plus(eye(2),hi,-1),left_error,right_error):
        assert minors_positive(a,True)
    receipt = dict(schema='response-block-v1', source_id='s17-exact-3-by-2-source',
                   dimension=2,C_minus=encode(lo),C_plus=encode(hi),V=encode(v),
                   edit_squared='1/100',t_lower='1/5',t_upper='1/4',threshold='1/2')
    result = checker.verify(receipt)
    # Independent adjugate evaluation of the claimed rational functions.
    tl,tu,E = F(1,5),F(1,4),F(1,100)
    al,au = 1+tl,1+tu
    dl,du = tl-E-E/tl,tu-E-E/tu
    l = mm(lo,adj_inverse(plus([[al*z for z in row] for row in eye(2)],lo,-dl)))
    upper = mm(hi,adj_inverse(plus(eye(2),hi,du)))
    lower_value = trace_product(v,l)
    upper_value = au*trace_product(v,upper)
    assert F(result['lower']) == lower_value <= actual <= upper_value == F(result['upper'])

    # An orthogonal change of the retained basis must leave the whole result
    # interval unchanged, with the task weight transformed along with C.
    q = [[F(3,5),F(-4,5)],[F(4,5),F(3,5)]]
    rotated = copy.deepcopy(receipt)
    for key,a in [('C_minus',lo),('C_plus',hi),('V',v)]:
        rotated[key] = encode(mm(transpose(q),mm(a,q)))
    rotated_result = checker.verify(rotated)
    assert [rotated_result[k] for k in ('lower','upper','verdict')] == [result[k] for k in ('lower','upper','verdict')]

    threshold_cases = []
    for threshold, verdict in [(lower_value,'unresolved'),(upper_value,'unresolved'),
                               (lower_value-F(1,1000000),'above'),
                               (upper_value+F(1,1000000),'below')]:
        case = dict(receipt,threshold=str(threshold))
        assert checker.verify(case)['verdict'] == verdict
        threshold_cases.append(dict(threshold=str(threshold),verdict=verdict))
    zero = dict(receipt,edit_squared='0',t_lower='0',t_upper='0')
    zero_result = checker.verify(zero)
    assert F(zero_result['lower']) == trace_product(v,lo)
    assert F(zero_result['upper']) == trace_product(v,hi)

    # The declared maximum dimension and a rank-one weight with nonzero
    # off-diagonal entries are within the implemented contract.
    large_lo = [[F(i == j,3) for j in range(16)] for i in range(16)]
    large = dict(receipt,dimension=16,C_minus=encode(large_lo),C_plus=encode(large_lo),
                 V=encode([[F(1,16)]*16 for _ in range(16)]))
    large_result = checker.verify(large)
    assert F(large_result['lower']) <= F(1,3) <= F(large_result['upper'])

    rejected = []
    changes = [('boolean dimension',{'dimension':True}),
               ('negative residual Schur pivot',{'V':[['1/2','1'],['1','1/2']]}),
               ('cap just below admissible',{'t_upper':'1/10'}),
               ('zero denominator literal',{'edit_squared':'1/0'}),
               ('fraction larger than bit cap',{'edit_squared':str(2**4096)}),
               ('unknown schema',{'schema':'response-block-v2'})]
    for name,change in changes:
        try:
            checker.verify(dict(receipt,**change))
        except checker.InvalidCertificate:
            rejected.append(name)
        else:
            raise AssertionError(name)
    # A false source label is not detected: the contract is conditional.
    relabeled = checker.verify(dict(receipt,source_id='unverified-source-label'))
    assert relabeled['lower'] == result['lower'] and relabeled['upper'] == result['upper']
    record = dict(status='PASS',positive_comparisons=comparisons,
                  rectangular_source_shape=[3,2],retained_dimension=2,
                  exact_compression=encode(c),receipt=receipt,exact_edited_value=str(actual),
                  result=result,rotated_result=rotated_result,threshold_cases=threshold_cases,
                  maximum_dimension_result=large_result,rejected=rejected,
                  source_identity_is_external=True,elapsed_ns=perf_counter_ns()-start,
                  python=platform.python_version(),executable=sys.executable,
                  probe_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  checker_sha256=hashlib.sha256(CHECKER.read_bytes()).hexdigest(),
                  scope='Focused finite arithmetic checks with separate determinant implementation; same-model development, not independent confirmation.')
    out.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:record[k] for k in ('status','positive_comparisons','exact_edited_value','elapsed_ns','python')}))


if __name__ == '__main__':
    main()
