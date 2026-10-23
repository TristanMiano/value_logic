"""Finite arithmetic screen, not a stochastic service experiment."""
from pathlib import Path
import hashlib
import json
import math
import platform
import time
import scipy
from scipy.stats import chi2

start = time.monotonic_ns()
rows = []
for delta in (0.01, 1e-6):
    for rank in (1, 4, 32):
        for ratio in (0.1, 0.25, 0.5, 0.9):
            alpha = 0.01
            L = math.log(1 / delta)
            c = math.sqrt(rank) + math.sqrt(2 * math.log(1 / alpha))
            z = (math.sqrt(L) + ratio**2 * c + math.sqrt(
                L + 2 * ratio**2 * c * math.sqrt(L) + ratio**2 * c**2
            )) / (1 - ratio**2)
            k = math.ceil(z*z)
            def gap(j):
                t = j - 2 * math.sqrt(j * L)
                return -math.inf if t <= 0 else math.sqrt(t) - ratio * (math.sqrt(j) + c)
            assert gap(k) >= -1e-10 and gap(k-1) < 0
            threshold2 = k - 2 * math.sqrt(k * L)
            boundary_pass_probability = float(chi2.cdf(threshold2, k))
            assert boundary_pass_probability <= delta
            denominator = 1_000_000 - 100_000 - 2000*k
            rows.append(dict(delta=delta, alpha=alpha, rank=rank, sigma_over_tau=ratio,
                             rows=k, availability_gap=gap(k),
                             false_boundary_pass=boundary_pass_probability,
                             ideal_dense_setup_calls=k,
                             ideal_dense_break_even_cases=(k*1_000_000/denominator
                                                          if denominator>0 else None)))
out = dict(status='PASS', cases=len(rows), rows=rows,
           source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           python=platform.python_version(), scipy=scipy.__version__,
           elapsed_ns=time.monotonic_ns()-start,
           scope='Finite parameter arithmetic and numerical chi-square CDF. No measured runtime saving or service reliability experiment.')
Path(__file__).with_suffix('.json').write_text(json.dumps(out, indent=2)+'\n', encoding='utf-8')
print(json.dumps(out))
