"""Two edited values sharing one old source; Codex (GPT-6), DEVELOPMENT.

New question: can independent sharp endpoint subtraction overstate a contrast?
Eight small cases. Approximate SDP only, with prospective feasibility tolerance
5e-7 and comparison tolerance 1e-6. No complete-cost or runtime gain claim.
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
OUT = HERE/'paired_result.json'
if OUT.exists():
    raise SystemExit('Refusing to overwrite observed evidence.')


def endpoints(C, c, e):
    lam, Q = np.linalg.eigh(C)
    weight = (Q.T @ c)**2
    E = e*e
    h = (E+np.sqrt(E*E+4*E))/2
    lr, ur = 1/(1+h), h/(1+h)

    def lower(r):
        return 0. if r == 0 else float(weight @ (1/(1+(1/lam-1)/r+E/(1-r))))

    def upper(r):
        if r == 0:
            return 1.
        a, b = 1/(1-r), 1+E/r
        return float(weight @ (a*b*lam/(a+(b-a)*lam)))

    lp = minimize_scalar(lambda r: -lower(r), bounds=(0, lr),
                         method='bounded', options={'xatol': 1e-13})
    up = minimize_scalar(upper, bounds=(0, ur),
                         method='bounded', options={'xatol': 1e-13})
    assert lp.success and up.success
    return dict(lower=max(lower(r) for r in (0, lr, lp.x)),
                upper=min(upper(r) for r in (0, ur, up.x)))


def paired(C, cs, es):
    k = len(cs[0])
    G = cp.Variable((2*k+4, 2*k+4), symmetric=True)
    H = cp.Variable((k+4, k+4), symmetric=True)
    rs, us = [2*k, 2*k+2], [2*k+1, 2*k+3]
    xs, zs = [k, k+2], [k+1, k+3]
    cons = [G >> 0, H >> 0, G[:k, :k] == np.eye(k),
            G[:k, k:2*k] == C,
            G[k:2*k, k:2*k]+H[:k, :k] == C]
    values = []
    for i in range(2):
        r, u, x, z, c, E = rs[i], us[i], xs[i], zs[i], cs[i], es[i]**2
        f = c @ G[:k, r]
        values.append(f)
        cons += [G[k:2*k, :k] @ c-G[k:2*k, r]-G[k:2*k, u] == H[:k, x],
                 G[:k, r]-G[k:2*k, r] == H[:k, x]-H[:k, z],
                 G[r, u] == H[x, z],
                 G[u, u] <= E*H[x, x], H[z, z] <= E*G[r, r]]
    # These four entries include each new normal equation and both off-diagonal
    # compatibility equations for the single shared, unbounded old operator M.
    for i in range(2):
        for j in range(2):
            cons += [G[rs[i], :k] @ cs[j]-G[rs[i], rs[j]]-G[rs[i], us[j]]
                     == H[xs[i], xs[j]]-H[zs[i], xs[j]]]
    problem = cp.Problem(cp.Maximize(values[0]-values[1]), cons)
    start = perf_counter_ns()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        value = problem.solve(solver='CLARABEL', tol_gap_abs=1e-9,
                              tol_gap_rel=1e-9, tol_feas=1e-9, max_iter=300)
    return dict(value=float(value), values=[float(f.value) for f in values],
                status=problem.status, elapsed_ns=perf_counter_ns()-start,
                iterations=problem.solver_stats.num_iters,
                max_constraint_violation=max(float(np.max(q.violation())) for q in cons),
                warnings=[str(w.message) for w in caught],
                gram_output=G.value.tolist(), gram_input=H.value.tolist(),
                duals=[np.asarray(q.dual_value).tolist() for q in cons])


unit = np.array([1.])
equal = np.ones(2)/np.sqrt(2)
cases = [('scalar_caps', np.array([[.1]]), [unit, unit], [1., 1.]),
         ('scalar_caps_small', np.array([[.1]]), [unit, unit], [.1, .1]),
         ('scalar_interiors', np.array([[.8]]), [unit, unit], [.1, .1]),
         ('scalar_cancellation', np.array([[.8]]), [unit, unit], [1., 1.]),
         ('two_caps', np.diag([.1, .2]), [equal, equal], [1., 1.]),
         ('mixed', np.diag([.1, .9]), [equal, equal], [.1, .1]),
         ('orthogonal_targets', np.diag([.1, .2]),
          [np.array([1., 0.]), np.array([0., 1.])], [1., 1.]),
         ('asymmetric_edits', np.array([[.1]]), [unit, unit], [.5, 1.])]
start = perf_counter_ns()
rows = []
for name, C, cs, es in cases:
    independent = endpoints(C, cs[0], es[0])['upper']-endpoints(C, cs[1], es[1])['lower']
    result = paired(C, cs, es)
    gap = independent-result['value']
    passed = (result['status'] in ('optimal', 'optimal_inaccurate')
              and result['max_constraint_violation'] <= 5e-7 and gap >= -1e-6)
    row = dict(case=name, C=C.tolist(), targets=[c.tolist() for c in cs], edit_radii=es,
               separate_endpoint_contrast=independent, shared_source=result,
               apparent_contrast_reduction=gap, passed=passed)
    rows.append(row)
    print(json.dumps(dict(case=name, passed=passed, separate=independent,
                          joint=result['value'], gap=gap, status=result['status'])))
record = dict(status='PASS' if all(r['passed'] for r in rows) else 'FAIL',
              scope='Eight approximate shared-source Gram screens, not a rigorous certificate.',
              elapsed_ns=perf_counter_ns()-start, cases=rows,
              versions=dict(python=platform.python_version(), numpy=np.__version__,
                            scipy=scipy.__version__, cvxpy=cp.__version__),
              source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
OUT.write_text(json.dumps(record, indent=2)+'\n', encoding='utf-8', newline='\n')
print(json.dumps(dict(status=record['status'], elapsed_ns=record['elapsed_ns'])))
if record['status'] != 'PASS':
    raise SystemExit(1)
