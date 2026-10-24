"""DEVELOPMENT: finite screen of an unproved universal relative-regret bound.
Codex (GPT-6), 2026-10-24. Does not establish the general conjecture.
"""
import hashlib
import json
import platform
from pathlib import Path
import time
import numpy as np

t0 = time.perf_counter_ns()
rng = np.random.default_rng(1629)
rows = []
for n, m in [(1, 1), (2, 2), (2, 3), (3, 2), (4, 5)]:
    for e in [.1, 1., 3.]:
        largest = 0.
        for _ in range(80):
            M = rng.normal(size=(n, m)) * 10 ** rng.uniform(-2, 2)
            D = rng.normal(size=(n, m))
            D *= e / np.linalg.norm(D, 2)
            N = M + D
            G = np.eye(n) + N @ N.T
            old = np.linalg.solve(np.eye(n) + M @ M.T, M)
            new = np.linalg.solve(G, N)
            err = old - new
            R = np.eye(m) + N.T @ N
            w, V = np.linalg.eigh(R)
            root = (V * np.sqrt(w)) @ V.T
            rel = np.linalg.eigvalsh(root @ err.T @ G @ err @ root)[-1]
            normalized = float(rel / (e * e * (1 + e * e / 4)))
            if normalized > largest:
                largest = normalized
                witness = {"M": M.tolist(), "Delta": D.tolist(),
                           "relative_excess": float(rel)}
        rows.append({"n": n, "m": m, "e": e,
                     "largest_normalized": largest, "witness": witness})
result = {"status": "NO_FINITE_COUNTEREXAMPLE" if max(r["largest_normalized"] for r in rows) <= 1 + 1e-8 else "CONJECTURE_COUNTEREXAMPLE",
          "seed": 1629, "cases": 1200, "rows": rows,
          "elapsed_ns": time.perf_counter_ns() - t0,
          "python": platform.python_version(), "numpy": np.__version__,
          "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(result["status"], max(r["largest_normalized"] for r in rows))
