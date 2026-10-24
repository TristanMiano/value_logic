"""DEVELOPMENT: fixed-source maximum, including the singular dual endpoint."""
from pathlib import Path
from time import perf_counter_ns
import hashlib
import json
import math
import platform
import numpy as np
import scipy
from scipy.optimize import brentq

here = Path(__file__).resolve().parent
out = here / 'fixed_output_probe.json'
assert not out.exists(), 'Preserve original evidence.'
started = perf_counter_ns()


def maximum(M, v, e):
    E = e * e
    b, V = np.linalg.eigh(M @ M.T)
    b = np.maximum(b, 0)
    w = V.T @ v
    bmin = float(b[0])
    abar = 2 / (1 + E - bmin + math.sqrt((1 + E - bmin)**2 + 4*bmin))
    kernel = abs(b-bmin) < 1e-10

    def point(alpha, endpoint=False):
        den = alpha*b + 1-E*alpha/(1-alpha)
        z = np.zeros(len(b))
        active = ~kernel if endpoint else np.ones(len(b), dtype=bool)
        z[active] = w[active] / den[active]
        derivative = -float(z @ ((b-E/(1-alpha)**2)*z))
        return float(w@z), derivative, z

    if E >= float(v @ M @ M.T @ v)-1e-12:
        kind = 'cancellation'
        alpha, expected = 0., 1.
        Delta = -np.outer(v, M.T@v)
    elif np.linalg.norm(w[kernel]) < 1e-10 and point(abar, True)[1] <= 0:
        kind = 'singular'
        alpha = abar
        expected, derivative, z = point(alpha, True)
        extra = -derivative/(E/(1-alpha)**2-bmin)
        assert extra >= -1e-11
        z[np.flatnonzero(kernel)[0]] = math.sqrt(max(0, extra))
        z = V@z
        mz = M.T@z
        Delta = -e*np.outer(z/np.linalg.norm(z), mz/np.linalg.norm(mz))
    else:
        kind = 'interior'
        alpha = brentq(lambda a: point(a)[1], 0, abar*(1-1e-11), xtol=2e-14)
        expected, derivative, z = point(alpha)
        z = V@z
        mz = M.T@z
        Delta = -e*np.outer(z/np.linalg.norm(z), mz/np.linalg.norm(mz))
    N = M+Delta
    direct = float(v@np.linalg.solve(np.eye(len(v))+N@N.T, v))
    assert np.linalg.norm(Delta, 2) <= e+2e-10
    assert abs(direct-expected) < 3e-8, (direct, expected, kind)
    assert direct >= float(v@np.linalg.solve(np.eye(len(v))+M@M.T, v))-1e-10
    return {'kind': kind, 'alpha': alpha, 'alpha_end': abar,
            'value': expected, 'direct_value': direct,
            'edit_norm': float(np.linalg.norm(Delta, 2))}


rows = []
sources = [np.array([[3.]]), np.array([[0.]]), np.diag([0., 3.]),
           np.diag([1., 3.]), np.array([[0.], [3.]]),
           np.diag([0., 1., 4.]), np.array([[1., 2., 0.], [0., 1., 3.]])]
for M in sources:
    directions = [np.eye(len(M))[i] for i in range(len(M))]
    directions += [np.ones(len(M))/math.sqrt(len(M))]
    for vi, v in enumerate(directions):
        for e in (.1, 1., 3.):
            rows.append({'shape': list(M.shape), 'M': M.tolist(), 'direction': vi,
                         'e': e, **maximum(M, v, e)})

rng = np.random.default_rng(1638)
for n, m in [(1, 3), (2, 1), (2, 2), (3, 2), (3, 4)]:
    for _ in range(8):
        M = rng.normal(size=(n, m))
        v = rng.normal(size=n); v /= np.linalg.norm(v)
        e = float(rng.choice([.1, .7, 2.]))
        rows.append({'shape': [n, m], 'random': True, 'e': e, **maximum(M, v, e)})

scalar = maximum(np.array([[3.]]), np.array([1.]), 1.)
hard = maximum(np.array([[0.], [3.]]), np.array([0., 1.]), 1.)
assert abs(scalar['value']-1/5) < 1e-10
assert hard['kind'] == 'singular' and abs(hard['value']-2/9) < 1e-10
counts = {kind: sum(row['kind'] == kind for row in rows)
          for kind in ['cancellation', 'interior', 'singular']}
assert all(counts.values())
result = {'status': 'PASS', 'scope': 'Finite constructed maximizer screen; not independent confirmation.',
          'python': platform.python_version(), 'numpy': np.__version__, 'scipy': scipy.__version__,
          'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'seed': 1638, 'elapsed_ns': perf_counter_ns()-started,
          'case_counts': counts, 'cases': rows,
          'scalar_value': scalar['value'], 'singular_value': hard['value']}
out.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
print(json.dumps({k: result[k] for k in ['status', 'case_counts', 'elapsed_ns', 'scalar_value', 'singular_value']}))
