#!/usr/bin/env python3
"""Graded judge weights under reinforcement by weighted vindication.

P4-R1-C001 session 3. Written by Claude (Fable 5.2), 2026-11-10.
M_c[j, l] = I(A_j on one performance ; A_l on another performance of the same performer | both cell labels), in nats.
Update: w <- M_c w / |M_c w|_1  ("a judge is credited when borne out by judges who are themselves credited").
"""
import json, sys
import numpy as np
from judge_society import worlds, panel_kernel, cell_kernel, twin_partition, judge, bern, canon


def vindication_matrix(p, q, f, r, g, c):
    p, q = np.asarray(p, float), np.asarray(q, float)
    m = len(g)
    mass = np.zeros(max(c) + 1)
    for x, cell in enumerate(c):
        mass[cell] += q[x]
    Kc = [cell_kernel(q, panel_kernel(f, r, g, [j]), c) for j in range(m)]      # [t, cell, a]
    M = np.zeros((m, m))
    for j in range(m):
        for l in range(m):
            tot = 0.0
            for k1 in range(len(mass)):
                for k0 in range(len(mass)):
                    jt = np.einsum("t,ta,tb->ab", p, Kc[j][:, k1, :], Kc[l][:, k0, :])
                    ind = np.outer(jt.sum(1), jt.sum(0))
                    mask = jt > 1e-300
                    tot += mass[k1] * mass[k0] * float((jt[mask] * np.log(jt[mask] / ind[mask])).sum())
            M[j, l] = max(tot, 0.0)
    M[M < 1e-12] = 0.0
    return M


def components(M):
    m, seen, out = len(M), set(), []
    for s in range(m):
        if s in seen or M[s].sum() == 0:
            continue
        comp, stack = [], [s]
        while stack:
            u = stack.pop()
            if u in seen:
                continue
            seen.add(u); comp.append(u)
            stack.extend(v for v in range(m) if M[u, v] > 0 and v not in seen)
        out.append(sorted(comp))
    return out


def limit(M, w0, steps=5000):
    w = np.asarray(w0, float)
    for _ in range(steps):
        v = M @ w
        if v.sum() == 0:
            return v
        w = v / v.sum()
    return w


def analyse(name, p, q, f, r, g, names, c):
    M = vindication_matrix(p, q, f, r, g, tuple(c))
    comps = components(M)
    roots = [float(np.linalg.eigvalsh(M[np.ix_(cc, cc)]).max()) for cc in comps]
    w = limit(M, np.ones(len(g)) / len(g))
    # count-based reinforcement: add credit earned from the current shares
    counts = np.ones(len(g))
    for _ in range(200000):
        counts += M @ (counts / counts.sum()) / max(M.max(), 1e-12)
    return {"world": name, "delineation": list(c),
            "components": [{"judges": [names[j] for j in cc], "perron_root_nats": rt} for cc, rt in zip(comps, roots)],
            "limit_weights_from_uniform": {names[j]: round(float(w[j]), 4) for j in range(len(g))},
            "count_based_shares_after_200000_steps": {names[j]: round(float(counts[j] / counts.sum()), 4) for j in range(len(g))}}


if __name__ == "__main__":
    out = {"author": "Claude (Fable 5.2)", "cycle": "P4-R1-C001", "session": 3, "worlds": []}
    W = {w[0][:1]: w for w in worlds()}
    for key in ("A", "B", "C"):
        name, p, q, f, r, g, names, zbar, _ = W[key]
        out["worlds"].append(analyse(name, p, q, f, r, g, names, zbar))
    # World C with correlated abilities: the two domains' skills now go together in the population.
    name, p, q, f, r, g, names, zbar, _ = W["C"]
    for rho_p in ([.3, .2, .2, .3], [.4, .1, .1, .4]):
        out["worlds"].append(analyse(f"C with abilities correlated, skill law {rho_p}", rho_p, q, f, r, g, names, zbar))
    # World F with a reputation judge of varying consistency.
    name, p, q, f4, r, g, names, zbar, _ = W["F"]
    for hi in (.9, .7, .6):
        reput = lambda s, x, y, hi=hi: hi if y >= 2 else 1 - hi
        g2 = [g[0], g[1], judge(2, 4, reput)]
        out["worlds"].append(analyse(f"F reputation judge approves with probability {hi}/{round(1 - hi, 1)}", p, q, f4, r, g2, names, zbar))
    json.dump(out, sys.stdout, indent=1)
