#!/usr/bin/env python3
"""Excellence exemplars: which objects are ever chosen as "best" by diverse judges.

P4-R1-C001 session 2 (W1.5). Written by Claude (Fable 5.2), 2026-11-09.
Objects have latent causes h (standard Gaussian in R^r) and D criterion scores
v = B h (+ noise). A linear judge with positive weights w picks argmax <w, v>,
which depends on w only through u = B^T w. Seeded Monte Carlo; counts are
exact for each sampled world where stated.
"""
import json, math, sys
import numpy as np

rng = np.random.default_rng(20261109)


def hull_2d(pts):
    """Convex hull vertices (counter-clockwise) by Andrew's monotone chain."""
    idx = np.lexsort((pts[:, 1], pts[:, 0]))
    def half(order):
        out = []
        for i in order:
            while len(out) >= 2:
                a, b = pts[out[-2]], pts[out[-1]]
                if (b[0] - a[0]) * (pts[i][1] - a[1]) - (b[1] - a[1]) * (pts[i][0] - a[0]) <= 0:
                    out.pop()
                else:
                    break
            out.append(i)
        return out
    lower, upper = half(idx), half(idx[::-1])
    return lower[:-1] + upper[:-1]


def exemplars_in_arc(pts, lo, hi):
    """Objects that maximise <u, h> for some direction u with angle in (lo, hi)."""
    hv = hull_2d(pts)
    P = pts[hv]
    nxt = np.roll(P, -1, axis=0)
    ang = np.arctan2(-(nxt[:, 0] - P[:, 0]), (nxt[:, 1] - P[:, 1]))   # outward normal of edge i -> i+1 (ccw hull)
    inside = (ang > lo) & (ang < hi)
    return 1 + int(inside.sum()), len(hv)


def planar_counts():
    rows = []
    for N in (1000, 10000, 100000):
        for alpha_deg in (10, 45, 90):
            lo = math.radians(20); hi = lo + math.radians(alpha_deg)
            ex, hv = zip(*(exemplars_in_arc(rng.standard_normal((N, 2)), lo, hi) for _ in range(300)))
            rows.append({"N": N, "arc_degrees": alpha_deg, "mean_exemplars": float(np.mean(ex)),
                         "predicted_1_plus_share_of_hull": 1 + alpha_deg / 360 * float(np.mean(hv)),
                         "mean_hull_vertices": float(np.mean(hv)),
                         "asymptotic_2sqrt(2 pi ln N)": 2 * math.sqrt(2 * math.pi * math.log(N))})
    return rows


def chosen(V, W, chunk=2000):
    out = set()
    for i in range(0, len(W), chunk):
        out.update(np.argmax(W[i:i + chunk] @ V.T, axis=1).tolist())
    return out


def chosen_min_type(V, W, ref, chunk=500):
    out = set()
    for i in range(0, len(W), chunk):
        out.update(np.argmax(np.min((V[None, :, :] - ref) / W[i:i + chunk, None, :], axis=2), axis=1).tolist())
    return out


def invariance_and_rank():
    N, r, D = 5000, 2, 6
    h = rng.standard_normal((N, r))
    ang = np.radians(np.linspace(5, 95, D))
    B = np.stack([np.cos(ang), np.sin(ang)], axis=1)          # six criteria, all in a 90-degree cone of causes
    V = h @ B.T
    exact, _ = exemplars_in_arc(h, math.radians(5), math.radians(95))
    pops = {"uniform weights": rng.dirichlet(np.ones(D), 100000),
            "concentrated weights": rng.dirichlet(np.full(D, .15), 100000),
            "lognormal weights": rng.lognormal(0, 1.5, (100000, D))}
    sets = {k: chosen(V, W) for k, W in pops.items()}
    union = set().union(*sets.values())
    # drop four criteria that are positive combinations of the two extreme ones: same cone, same exemplars
    V2 = h @ B[[0, D - 1]].T
    two = chosen(V2, rng.dirichlet(np.full(2, .3), 100000)) | chosen(V2, rng.dirichlet(np.ones(2), 100000))
    # add a criterion outside the cone
    b_new = np.array([math.cos(math.radians(150)), math.sin(math.radians(150))])
    V3 = np.hstack([V, (h @ b_new)[:, None]])
    wider = chosen(V3, rng.dirichlet(np.ones(D + 1), 100000)) | chosen(V3, rng.dirichlet(np.full(D + 1, .15), 100000))
    return {"objects": N, "criteria": D, "latent_causes": r, "exact_exemplar_count": exact,
            "chosen_by_population": {k: len(v) for k, v in sets.items()},
            "populations_choose_subsets_of_one_set": all(v <= union for v in sets.values()),
            "union_size": len(union), "two_extreme_criteria_only": len(two), "same_set_with_two_criteria": two == union,
            "after_adding_a_criterion_outside_the_cone": len(wider), "old_exemplars_kept": union <= wider}


def noise_and_dimension():
    """How the chosen set grows with the number of criteria when excellences share causes or do not."""
    N, judges = 5000, 100000
    out = []
    for D in (2, 4, 8, 16):
        h = rng.standard_normal((N, 2))
        B = np.abs(rng.standard_normal((D, 2)))
        eps = rng.standard_normal((N, D))
        W = rng.dirichlet(np.ones(D), judges)
        row = {"criteria": D}
        for name, V in (("two shared causes", h @ B.T), ("shared causes plus 30% idiosyncratic", h @ B.T + .3 * eps),
                        ("independent criteria", eps)):
            row[name] = len(chosen(V, W))
        out.append(row)
    return out


def nonlinear():
    """Linear judges reach only hull exemplars; min-type (Chebyshev) judges reach every undominated object."""
    res = []
    for trial in range(200):
        N = 10000
        V = rng.standard_normal((N, 2))
        order = np.argsort(-V[:, 0]); best, pareto = -np.inf, 0
        for i in order:
            if V[i, 1] > best:
                pareto += 1; best = V[i, 1]
        lin, _ = exemplars_in_arc(V, 0.0, math.pi / 2)
        ref = V.min(axis=0) - 1.0
        W = rng.dirichlet(np.ones(2), 20000)
        cheb = len(chosen_min_type(V, W, ref)) if trial < 5 else None
        res.append((pareto, lin, cheb))
    par, lin, cheb = zip(*res)
    return {"objects": 10000, "mean_undominated": float(np.mean(par)), "harmonic_number": sum(1 / k for k in range(1, 10001)),
            "mean_linear_exemplars": float(np.mean(lin)),
            "mean_chosen_by_20000_min_type_judges_first_5_worlds": float(np.mean([c for c in cheb if c is not None])),
            "mean_undominated_first_5_worlds": float(np.mean(par[:5]))}


if __name__ == "__main__":
    json.dump({"author": "Claude (Fable 5.2)", "cycle": "P4-R1-C001", "session": 2, "seed": 20261109,
               "planar_counts": planar_counts(), "invariance_and_rank": invariance_and_rank(),
               "growth_with_criteria": noise_and_dimension(), "linear_versus_min_type": nonlinear()},
              sys.stdout, indent=1)
