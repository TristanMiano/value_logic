#!/usr/bin/env python3
"""Cell-local judges: forecasts use only the performer's past results in the target's own cell.

P4-R1-C001 session 2. Written by Claude (Fable 5.2), 2026-11-09.
V_loc_n(c) = -H(Y_0 | same-cell part of an n-long history, target cell), computed exactly.
Such a judge knows the law of each cell's outcome kernel but pools nothing across cells.
"""
import json, math, sys
import numpy as np
from exact_scores import value, partitions, refines, canon, bern, twin_partition, TOL


def v_local(p, q, f, c, n):
    p, q, f = np.asarray(p, float), np.asarray(q, float), np.asarray(f, float)
    total = 0.0
    for cell in range(max(c) + 1):
        members = [z for z, k in enumerate(c) if k == cell]
        mass = q[members].sum()
        ker = (f[:, members, :] * q[members][None, :, None]).sum(axis=1) / mass   # cell kernel [t, y]
        one = ker[:, None, :].tolist()
        for m in range(n + 1):
            w = math.comb(n, m) * mass ** m * (1 - mass) ** (n - m)
            if w > 0:
                total += mass * w * value(p, [[1.0]] * len(p), one, (0,), m)
    return total


def scan(name, p, q, f, ns):
    k = np.asarray(f).shape[1]
    zbar = twin_partition(p, f)
    rows = []
    for n in ns:
        vals = {c: v_local(p, q, f, c, n) for c in partitions(k)}
        best = max(vals.values())
        mx = sorted(c for c in vals if vals[c] > best - TOL)
        strict_ref = [c for c in vals if refines(c, zbar) and c != zbar]
        rows.append({"n": n, "optimal": mx, "value_at_zbar_minus_best": vals[zbar] - best,
                     "worst_gain_of_any_strict_refinement_over_zbar": max((vals[c] - vals[zbar] for c in strict_ref), default=None)})
    return {"world": name, "transfer_partition": zbar, "by_n": rows}


if __name__ == "__main__":
    out = {"author": "Claude (Fable 5.2)", "cycle": "P4-R1-C001", "session": 2, "worlds": []}
    # Types: 0 and 1 are twins; 2 is a near-twin of them; 3 draws on the opposite skill.
    p, q = [.5, .5], [.25] * 4
    for gap in (.02, .05, .15):
        f = [[bern(.8), bern(.8), bern(.8 - gap), bern(.2)], [bern(.3), bern(.3), bern(.3 + gap), bern(.9)]]
        out["worlds"].append(scan(f"near-twin gap {gap}", p, q, f, [0, 1, 2, 4, 8, 16, 32, 64]))
    json.dump(out, sys.stdout, indent=1, default=lambda o: o.item() if hasattr(o, "item") else list(o))
