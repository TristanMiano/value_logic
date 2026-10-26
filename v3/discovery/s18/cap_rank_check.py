"""Two exact cap examples testing the rank-one moment completion in n16_reduction.md."""
from pathlib import Path
import hashlib
import json
import platform
import time
import sympy as sp

started = time.perf_counter_ns()
R = sp.Rational
C = sp.diag(R(1, 8), R(1, 4))
c = sp.Matrix([R(3, 5), R(4, 5)])
H = sp.eye(2) - C
s = (c.T * C * c)[0]
m0 = (c.T * C**2 * c)[0]
g = s - m0
records = []
for branch, root_delta in [('lower', R(1, 3)), ('upper', R(1, 20))]:
    delta = root_delta**2
    m = m0 + delta
    q = s - m
    h = (2*m-s)/(s-m) if branch == 'lower' else s/m-2
    E = h*h/(1+h)
    v = root_delta*C*H*c/g
    Q = C**2 + v*v.T
    T = C-Q
    W = sp.eye(2).col_join(sp.zeros(1, 2))
    residuals = C.col_join(v.T)
    A = W-residuals
    gram = A*T.inv()*A.T
    target = W*c
    w = residuals*c
    mx = A*c
    sign = 1 if branch == 'lower' else -1
    cross = h/m if branch == 'lower' else h/q
    edited = gram + sign*cross*(mx*w.T+w*mx.T) + E/m*w*w.T
    expected = s/(1+h) if branch == 'lower' else (1+h)*s
    actual = (target.T*(sp.eye(3)+edited).inv()*target)[0]
    checks = {
        'strict_moment_range': 0 < delta < g,
        'positive_cap': h > 0,
        'T_positive': T[0,0] > 0 and T.det() > 0,
        'old_normal_identity': residuals.T*A == T,
        'old_inverse_response': (sp.eye(3)+gram)*residuals == W,
        'old_retained_block': W.T*residuals == C,
        'requested_moment': (w.T*w)[0] == m,
        'source_rank_two': gram.rank() == 2,
        'edited_rank_at_most_two': edited.rank() <= 2,
        'edited_gram_positive': edited.is_positive_semidefinite is True,
        'endpoint_equality': sp.factor(actual-expected) == 0,
        'strict_cap_not_realizable_in_two_outputs': m != m0,
    }
    assert all(checks.values()), checks
    records.append(dict(branch=branch, h=str(h), E=str(E), delta=str(delta),
                        n=3, p=2, endpoint=str(actual), checks=checks,
                        Q=[[str(z) for z in row] for row in Q.tolist()]))
result = dict(attribution='Codex (GPT-6), DEVELOPMENT; same-model finite check',
              source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              python=platform.python_version(), sympy=sp.__version__,
              elapsed_ns=time.perf_counter_ns()-started, cases=records,
              scope='Two rational non-eigenvector cap examples; not a universal proof or independent confirmation')
Path(__file__).with_name('cap_rank_result.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
print(json.dumps(result, indent=2))
