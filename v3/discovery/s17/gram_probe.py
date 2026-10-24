"""Small approximate conventional SDP comparison; DEVELOPMENT, Codex (GPT-6).

Run with the ignored task-local CVXPY environment. No result is a certificate.
Question: do the two-Gram constraints agree with the pinned scalar formula?
Prespecified tolerance: endpoint discrepancy <=1e-6, constraint violation <=5e-7.
"""
from pathlib import Path
from time import perf_counter_ns
import hashlib
import json
import platform
import warnings
import cvxpy as cp
import numpy as np
import scipy
from scipy.optimize import minimize_scalar

HERE = Path(__file__).resolve().parent
out = HERE / 'gram_result.json'
if out.exists():
    raise SystemExit('Refusing to overwrite an observed result.')


def endpoints(C, c, e):
    lam, Q = np.linalg.eigh(C)
    weight = (Q.T @ c) ** 2
    E = e * e
    h = (E + np.sqrt(E*E + 4*E)) / 2
    lr, ur = 1/(1+h), h/(1+h)

    def lower(r):
        if r == 0:
            return 0.0
        return float(weight @ (1/(1+(1/lam-1)/r+E/(1-r))))

    def upper(r):
        if r == 0:
            return 1.0
        a, b = 1/(1-r), 1+E/r
        return float(weight @ (a*b*lam/(a+(b-a)*lam)))

    lp = minimize_scalar(lambda r: -lower(r), bounds=(0, lr),
                         method='bounded', options={'xatol': 1e-13})
    up = minimize_scalar(upper, bounds=(0, ur),
                         method='bounded', options={'xatol': 1e-13})
    low = max([(lower(r), r) for r in (0, lr, float(lp.x))])
    high = min([(upper(r), r) for r in (0, ur, float(up.x))])
    return dict(lower=low[0], lower_r=low[1], upper=high[0], upper_r=high[1],
                scipy_success=bool(lp.success and up.success))


def solve(C, c, e):
    k = len(c)
    G = cp.Variable((2*k+2, 2*k+2), symmetric=True)
    H = cp.Variable((k+2, k+2), symmetric=True)
    r, u, x, z = 2*k, 2*k+1, k, k+1
    f = c @ G[:k, r]
    cons = [G >> 0, H >> 0, G[:k, :k] == np.eye(k),
            G[:k, k:2*k] == C,
            G[k:2*k, k:2*k] + H[:k, :k] == C,
            G[k:2*k, :k] @ c-G[k:2*k, r]-G[k:2*k, u] == H[:k, x],
            G[:k, r]-G[k:2*k, r] == H[:k, x]-H[:k, z],
            f == G[r, r]+H[x, x], G[r, u] == H[x, z],
            G[u, u] <= e*e*H[x, x], H[z, z] <= e*e*G[r, r]]
    records = {}
    for side, objective in [('lower', cp.Minimize(f)), ('upper', cp.Maximize(f))]:
        problem = cp.Problem(objective, cons)
        start = perf_counter_ns()
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            value = problem.solve(solver='CLARABEL', tol_gap_abs=1e-9,
                                  tol_gap_rel=1e-9, tol_feas=1e-9,
                                  max_iter=300)
        records[side] = dict(value=float(value), status=problem.status,
                             elapsed_ns=perf_counter_ns()-start,
                             iterations=problem.solver_stats.num_iters,
                             warnings=[str(w.message) for w in caught],
                             max_constraint_violation=max(float(np.max(q.violation())) for q in cons),
                             gram_output=G.value.tolist(), gram_input=H.value.tolist(),
                             duals=[np.asarray(q.dual_value).tolist() for q in cons])
    return records


rotation = np.array([[.6, -.8], [.8, .6]])
a = np.array([2., 3., 6.])/7
house = np.eye(3)-2*np.outer(a, a)
cases = [('scalar_caps', np.array([[.1]]), np.array([1.]), 1.),
         ('scalar_interiors', np.array([[.8]]), np.array([1.]), .1),
         ('scalar_cancellation', np.array([[.8]]), np.array([1.]), 1.),
         ('decision', np.diag([.1, .9]), np.ones(2)/np.sqrt(2), .1),
         ('dense_two', rotation @ np.diag([.2, .7]) @ rotation.T, np.array([.6, .8]), .3),
         ('dense_three', house @ np.diag([.15, .4, .8]) @ house.T, a, .2)]
start = perf_counter_ns()
rows = []
for name, C, c, e in cases:
    reference = endpoints(C, c, e)
    result = solve(C, c, e)
    discrepancy = max(abs(result[side]['value']-reference[side]) for side in ('lower', 'upper'))
    passed = (reference['scipy_success'] and discrepancy <= 1e-6 and
              all(result[side]['status'] in ('optimal', 'optimal_inaccurate') and
                  result[side]['max_constraint_violation'] <= 5e-7 for side in ('lower', 'upper')))
    rows.append(dict(case=name, C=C.tolist(), c=c.tolist(), e=e, scalar=reference,
                     sdp=result, max_endpoint_discrepancy=discrepancy, passed=passed))
    print(json.dumps(dict(case=name, passed=passed, discrepancy=discrepancy,
                          lower=result['lower']['value'], upper=result['upper']['value'])))
record = dict(status='PASS' if all(r['passed'] for r in rows) else 'FAIL',
              scope='Six approximate SDP comparisons; no rigorous certificate or runtime speedup claim.',
              elapsed_ns=perf_counter_ns()-start, cases=rows,
              versions=dict(python=platform.python_version(), numpy=np.__version__,
                            scipy=scipy.__version__, cvxpy=cp.__version__),
              source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
out.write_text(json.dumps(record, indent=2)+'\n', encoding='utf-8', newline='\n')
print(json.dumps(dict(status=record['status'], elapsed_ns=record['elapsed_ns'])))
if record['status'] != 'PASS':
    raise SystemExit(1)
