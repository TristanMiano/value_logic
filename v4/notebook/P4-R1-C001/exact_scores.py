#!/usr/bin/env python3
"""Exact second-order scores of task delineations in small judgment worlds.

P4-R1-C001 check. Written by Claude (Fable 5.2), 2026-11-09.

World: skills theta with probabilities p[t]; task types z with sampling
probabilities q[t][z] (rows equal when tasks are drawn independently of skill);
outcome law f[t][z][y]. A delineation c maps each type to a cell. A judge with
delineation c sees n past (cell, outcome) pairs of one performer and the
target's cell, and issues the Bayes forecast of the target outcome.
V_n(c) = -H(Y_0 | history, target cell) is the best expected log score that c
supports. Everything is computed exactly by enumerating count vectors.
"""
import itertools, json, math, random, sys
import numpy as np

TOL = 1e-10


def partitions(k):
    """All set partitions of range(k) as canonical cell-label tuples."""
    def rec(i, labels, m):
        if i == k:
            yield tuple(labels)
            return
        for lab in range(m + 1):
            yield from rec(i + 1, labels + [lab], max(m, lab + 1))
    yield from rec(0, [], 0)


def refines(c, d):
    """c refines d: same c-cell implies same d-cell."""
    seen = {}
    return all(seen.setdefault(a, b) == b for a, b in zip(c, d))


def canon(labels):
    m = {}
    return tuple(m.setdefault(a, len(m)) for a in labels)


def compositions(n, m):
    if m == 1:
        yield (n,)
        return
    for first in range(n + 1):
        for rest in compositions(n - first, m - 1):
            yield (first,) + rest


def value(p, q, f, c, n):
    """V_n(c) in nats."""
    p, q, f = np.asarray(p, float), np.asarray(q, float), np.asarray(f, float)
    ncell, ny = max(c) + 1, f.shape[2]
    # g[t, cell, y] = P(cell, y | theta = t)
    g = np.zeros((len(p), ncell, ny))
    for z, cell in enumerate(c):
        g[:, cell, :] += q[:, z, None] * f[:, z, :]
    gflat = g.reshape(len(p), ncell * ny)
    total = 0.0
    for counts in compositions(n, ncell * ny):
        coef = math.factorial(n)
        for k in counts:
            coef //= math.factorial(k)
        with np.errstate(divide="ignore", invalid="ignore"):
            like = np.prod(np.where(np.array(counts) > 0, gflat ** np.array(counts), 1.0), axis=1)
        w = p * like                       # joint weight of theta and this history
        joint = np.einsum("t,tky->ky", w, g)   # P(history, target cell, y0)
        marg = joint.sum(axis=1, keepdims=True)
        mask = joint > 0
        total += coef * float((joint[mask] * np.log((joint / np.where(marg > 0, marg, 1))[mask])).sum())
    return total


def twin_partition(p, f, q=None):
    """Types z, z' are twins when f(.|theta,z) = f(.|theta,z') for every skill
    of positive probability; with skill-dependent sampling they must also have
    q(z|theta)/q(z'|theta) constant in theta."""
    p, f = np.asarray(p, float), np.asarray(f, float)
    k = f.shape[1]
    lab = []
    for z in range(k):
        for w in range(z):
            same = np.allclose(f[p > 0, z, :], f[p > 0, w, :], atol=TOL)
            if same and q is not None:
                r = np.asarray(q, float)[p > 0]
                same = np.allclose(r[:, z] * r[0, w], r[:, w] * r[0, z], atol=TOL)
            if same:
                lab.append(lab[w])
                break
        else:
            lab.append(z)
    return canon(lab)


def marginal_partition(p, q, f):
    """Types with the same outcome law for a performer met once."""
    p, q, f = np.asarray(p, float), np.asarray(q, float), np.asarray(f, float)
    k = f.shape[1]
    # P(y | z) for a fresh performer: sum_t p_t q_tz f_tzy / sum_t p_t q_tz
    num = np.einsum("t,tz,tzy->zy", p, q, f)
    fbar = num / num.sum(axis=1, keepdims=True)
    lab = []
    for z in range(k):
        for w in range(z):
            if np.allclose(fbar[z], fbar[w], atol=TOL):
                lab.append(lab[w])
                break
        else:
            lab.append(z)
    return canon(lab)


def analyse(name, p, q, f, nmax, selection=False):
    k = np.asarray(f).shape[1]
    parts = list(partitions(k))
    twin = twin_partition(p, f, q if selection else None)
    marg = marginal_partition(p, q, f)
    out = {"world": name, "twin_partition": twin, "marginal_partition": marg, "by_n": []}
    ok = True
    for n in range(nmax + 1):
        vals = {c: value(p, q, f, c, n) for c in parts}
        best = max(vals.values())
        maxim = sorted(c for c in parts if vals[c] > best - TOL)
        target = marg if n == 0 else twin
        expected = sorted(c for c in parts if refines(c, target))
        mono = all(vals[c] >= vals[d] - TOL for c in parts for d in parts if refines(c, d))
        gap = min((best - vals[c] for c in parts if c not in expected), default=float("nan"))
        row = {"n": n, "best": best, "maximizers_are_refinements_of_target": maxim == expected,
               "target": target, "monotone_in_refinement": mono, "smallest_deficit_of_a_non_refinement": gap,
               "coarsest_value": vals[canon([0] * k)], "finest_value": vals[tuple(range(k))]}
        ok &= row["maximizers_are_refinements_of_target"] and mono
        out["by_n"].append(row)
    out["all_predictions_hold"] = ok
    return out


def indep(qrow, nt):
    return [list(qrow)] * nt


def bern(a):
    return [1 - a, a]


def worlds():
    w = {}
    # W1: two equally hard types that draw on different skills.
    p = [.5, .5]
    f = [[bern(.9), bern(.1)], [bern(.1), bern(.9)]]
    w["W1 two skills, equal difficulty"] = (p, indep([.5, .5], 2), f, 5)
    # W2: four types; 0 and 1 are twins; 2 and 3 have equal marginals but different transfer.
    p = [.25, .25, .25, .25]
    f = [[bern(.8), bern(.8), bern(.9), bern(.2)],
         [bern(.3), bern(.3), bern(.2), bern(.9)],
         [bern(.6), bern(.6), bern(.7), bern(.4)],
         [bern(.5), bern(.5), bern(.4), bern(.7)]]
    w["W2 twins plus an equal-marginal pair"] = (p, indep([.1, .3, .35, .25], 4), f, 4)
    # W4: no skill variation.
    f = [[bern(.8), bern(.8), bern(.5), bern(.2)]]
    w["W4 single skill level"] = ([1.0], indep([.25, .25, .25, .25], 1), f, 3)
    return w


def physics(log_eps, noise=.05):
    """Physics instance. Performers are model builds that include or neglect a
    drag correction and a special-relativistic correction. Regimes: slow vacuum,
    slow with drag, fast vacuum. A build is adequate in a regime when every
    correction it neglects is below tolerance there; the judged outcome is
    adequacy flipped with probability `noise`. Sizes are log10 of the leading
    neglected term (illustrative, after llm_convos/claude.txt)."""
    size = {"drag": [-6.0, -1.2, -6.0], "sr": [-15.0, -15.0, -2.0]}
    builds = [("N", ["drag", "sr"]), ("N+drag", ["sr"]), ("SR", ["drag"]), ("SR+drag", [])]
    f = []
    for _, neglected in builds:
        row = []
        for regime in range(3):
            adequate = all(size[c][regime] <= log_eps for c in neglected)
            row.append(bern(1 - noise if adequate else noise))
        f.append(row)
    return [.25] * 4, indep([1 / 3] * 3, 4), f


def random_world(rng, k=4, nt=4, ny=2, force_twin=True, force_equal_marginal=True):
    p = rng.dirichlet(np.ones(nt))
    q = rng.dirichlet(np.ones(k) * 2)
    f = rng.dirichlet(np.ones(ny), size=(nt, k))
    if force_twin:
        f[:, 1, :] = f[:, 0, :]
    if force_equal_marginal and ny == 2:
        # make type 3's marginal equal to type 2's while keeping a different skill profile
        d = f[:, 3, 1] - (p @ f[:, 3, 1]) + (p @ f[:, 2, 1])
        if d.min() > 0.02 and d.max() < 0.98:
            f[:, 3, 1], f[:, 3, 0] = d, 1 - d
    return p.tolist(), indep(q.tolist(), nt), f.tolist()


def main():
    report = {"author": "Claude (Fable 5.2)", "cycle": "P4-R1-C001", "worlds": []}
    for name, (p, q, f, nmax) in worlds().items():
        report["worlds"].append(analyse(name, p, q, f, nmax))
    for log_eps in (-1.0, -1.5, -3.0):
        p, q, f = physics(log_eps)
        report["worlds"].append(analyse(f"physics instance, log10 tolerance {log_eps}", p, q, f, 3))
    rng = np.random.default_rng(20261109)
    bad = 0
    smallest = float("inf")
    for i in range(300):
        ny = 2 if i % 3 else 3
        p, q, f = random_world(rng, ny=ny)
        res = analyse(f"random {i}", p, q, f, 2)
        bad += not res["all_predictions_hold"]
        smallest = min(smallest, res["by_n"][1]["smallest_deficit_of_a_non_refinement"])
    report["random_worlds"] = {"count": 300, "nmax": 2, "violations": bad,
                               "smallest_n1_deficit_of_a_non_refinement": smallest}
    json.dump(report, sys.stdout, indent=1, default=lambda o: o.item() if hasattr(o, "item") else list(o))


if __name__ == "__main__":
    main()
