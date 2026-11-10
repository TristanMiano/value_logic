#!/usr/bin/env python3
"""Judges evaluated only by judges: exact small-world computations.

P4-R1-C001 session 2. Written by Claude (Fable 5.2), 2026-11-09.

A world has skills t (law p), instances x (law q, independent of skill), a
hidden outcome y ~ f[t][x], an occasion-level shared signal s ~ r ("fashion",
fresh for each performance), and judges j with approval laws g[j][s][x][y][a].
Given (t, x) the panel's approvals on one performance have the joint kernel
K[t][x][a_1..a_m]; performances are independent given skill and instances.
No outcome is ever shown to the evaluator.

pi(S): twin partition of instances under the kernel of the judges in S.
vindicated(c): judges whose approvals on c-labelled performances of a
  performer are statistically dependent on the panel's approvals of another
  performance of the same performer (history length one).
A fixed point is a set S with vindicated(pi(S)) == S.
"""
import itertools, json, sys
import numpy as np
from exact_scores import value, partitions, refines, canon, TOL


def panel_kernel(f, r, g, S):
    """K[t, x, flat approvals of judges in S]."""
    f, r = np.asarray(f, float), np.asarray(r, float)
    nt, nx, ny = f.shape
    S = sorted(S)
    shapes = [np.asarray(g[j]).shape[-1] for j in S]
    K = np.zeros((nt, nx, int(np.prod(shapes)) if S else 1))
    for idx, a in enumerate(itertools.product(*[range(n) for n in shapes])):
        tot = np.zeros((nx, ny))
        for s, rs in enumerate(r):
            term = np.full((nx, ny), rs)
            for j, aj in zip(S, a):
                term = term * np.asarray(g[j], float)[s, :, :, aj]
            tot += term
        K[:, :, idx] = np.einsum("txy,xy->tx", f, tot)
    return K


def twin_partition(p, K):
    p = np.asarray(p, float)
    lab = []
    for x in range(K.shape[1]):
        for w in range(x):
            if np.allclose(K[p > 0, x, :], K[p > 0, w, :], atol=TOL):
                lab.append(lab[w]); break
        else:
            lab.append(x)
    return canon(lab)


def cell_kernel(q, K, c):
    q = np.asarray(q, float)
    out = np.zeros((K.shape[0], max(c) + 1, K.shape[2]))
    mass = np.zeros(max(c) + 1)
    for x, cell in enumerate(c):
        out[:, cell, :] += q[x] * K[:, x, :]; mass[cell] += q[x]
    return out / mass[None, :, None]


def vindicated(p, q, f, r, g, c):
    p = np.asarray(p, float)
    J = range(len(g))
    KJ = cell_kernel(q, panel_kernel(f, r, g, J), c)
    out = set()
    for j in J:
        Kj = cell_kernel(q, panel_kernel(f, r, g, [j]), c)
        mj, mJ = p @ Kj.reshape(len(p), -1), p @ KJ.reshape(len(p), -1)
        cov = np.einsum("t,ta,tb->ab", p, Kj.reshape(len(p), -1), KJ.reshape(len(p), -1)) - np.outer(mj, mJ)
        if np.abs(cov).max() > 1e-9:
            out.add(j)
    return frozenset(out)


def analyse(name, p, q, f, r, g, names, zbar, starts=()):
    m, nx = len(g), np.asarray(f).shape[1]
    pi = lambda S: twin_partition(p, panel_kernel(f, r, g, S)) if S else canon([0] * nx)
    phi = lambda S: vindicated(p, q, f, r, g, pi(S))
    show = lambda S: [names[j] for j in sorted(S)]
    subsets = [frozenset(s) for k in range(m + 1) for s in itertools.combinations(range(m), k)]
    fixed = [S for S in subsets if phi(S) == S]

    def iterate(S):
        seen = [S]
        while True:
            S2 = phi(S)
            if S2 == S:
                return S, len(seen) - 1
            S = S2; seen.append(S)
    low, _ = iterate(frozenset())
    high, _ = iterate(frozenset(range(m)))
    res = {"world": name, "outcome_transfer_partition": zbar,
           "fixed_points": [{"judges": show(S), "delineation": pi(S)} for S in fixed],
           "bootstrap_from_nothing": {"judges": show(low), "delineation": pi(low)},
           "greatest": {"judges": show(high), "delineation": pi(high),
                        "equals_outcome_transfer_partition": pi(high) == tuple(zbar)},
           "panel_partition_all_judges": pi(frozenset(range(m))),
           "single_judge_partitions": {names[j]: pi(frozenset([j])) for j in range(m)}}
    for label, c0 in starts:
        S, steps = iterate(vindicated(p, q, f, r, g, tuple(c0)))
        res.setdefault("from_start", []).append({"start": label, "delineation_0": list(c0), "reaches": show(S),
                                                 "delineation": pi(S), "steps": steps})
    # Theorem 4 check: predicting the later panel vector, optimal delineations = refinements of pi(all)
    K = panel_kernel(f, r, g, range(m))
    vals = {c: value(p, [list(q)] * len(p), K.tolist(), c, 1) for c in partitions(nx)}
    best = max(vals.values())
    mx = sorted(c for c in vals if vals[c] > best - TOL)
    res["approval_prediction_optimum_is_refinements_of_panel_partition"] = \
        mx == sorted(c for c in vals if refines(c, pi(frozenset(range(m)))))
    return res


def bern(a): return [1 - a, a]


def judge(nx, ny, fn, ns=1):
    """g[s][x][y] = approval law from fn(s, x, y) -> P(approve)."""
    return [[[bern(fn(s, x, y)) for y in range(ny)] for x in range(nx)] for s in range(ns)]


def worlds():
    out = []
    noisy = lambda s, x, y: .8 if y else .2
    # A. Pure specialisation (W1) with two outcome-tracking judges, two fashion judges, one random judge.
    p, q = [.5, .5], [.5, .5]
    f = [[bern(.9), bern(.1)], [bern(.1), bern(.9)]]
    g = [judge(2, 2, noisy, 2), judge(2, 2, noisy, 2),
         judge(2, 2, lambda s, x, y: float(s), 2), judge(2, 2, lambda s, x, y: float(s), 2),
         judge(2, 2, lambda s, x, y: .5, 2)]
    out.append(("A specialisation; trackers, fashion pair, random", p, q, f, [.5, .5], g,
                ["tracker1", "tracker2", "fashion1", "fashion2", "random"], [0, 1],
                [("weakly informative split", [0, 1])]))
    # B. A general factor plus specialisation.
    p = [.25] * 4
    f = [[bern(.9), bern(.7)], [bern(.7), bern(.9)], [bern(.3), bern(.1)], [bern(.1), bern(.3)]]
    g = [judge(2, 2, noisy), judge(2, 2, noisy), judge(2, 2, lambda s, x, y: .5)]
    out.append(("B general factor plus specialisation", p, q, f, [1.0], g, ["tracker1", "tracker2", "random"], [0, 1], []))
    # C. Two domains: instances 0,1 share a general factor u; instances 2,3 are pure specialisation on v.
    p, q, f = [], [.25] * 4, []
    for u in (0, 1):
        for v in (0, 1):
            p.append(.25)
            f.append([bern(.85 if u else .25), bern(.75 if u else .15), bern(.9 if v else .1), bern(.1 if v else .9)])
    d1 = lambda s, x, y: (.8 if y else .2) if x < 2 else .5
    d2 = lambda s, x, y: (.8 if y else .2) if x >= 2 else .5
    g = [judge(4, 2, d1), judge(4, 2, d1), judge(4, 2, d2), judge(4, 2, d2)]
    out.append(("C two domains; domain-2 is pure specialisation", p, q, f, [1.0], g,
                ["dom1a", "dom1b", "dom2a", "dom2b"], [0, 1, 2, 3],
                [("split 2 from 3 only", [0, 0, 1, 2])]))
    # D. Outcome twins (instances 0,1) plus a distinct instance 2; a pure task-convention judge and a
    #    biased-but-informative judge.
    p, q = [.5, .5], [1 / 3] * 3
    f = [[bern(.8), bern(.8), bern(.3)], [bern(.3), bern(.3), bern(.8)]]
    conv = lambda s, x, y: .9 if x == 0 else .1                     # ignores the performance entirely
    biased = lambda s, x, y: min(.95, (.8 if y else .2) + (.1 if x == 0 else 0))  # tracks outcome, favours instance 0
    out.append(("D1 trackers plus pure task-convention judge", p, q, f, [1.0],
                [judge(3, 2, noisy), judge(3, 2, noisy), judge(3, 2, conv)],
                ["tracker1", "tracker2", "convention"], [0, 0, 1], []))
    out.append(("D2 trackers plus biased-but-informative judge", p, q, f, [1.0],
                [judge(3, 2, noisy), judge(3, 2, noisy), judge(3, 2, biased)],
                ["tracker1", "tracker2", "biased"], [0, 0, 1], []))
    # F. Reputation: skill is (ability, reputation); one judge approves on reputation alone.
    p, f = [], []
    for ab in (0, 1):
        for rep in (0, 1):
            p.append(.25); f.append([bern(.9 if ab else .1), bern(.1 if ab else .9)])
    # reputation is read from the skill index through a deterministic "outcome-like" channel: add it as a
    # second hidden coordinate by enlarging the outcome alphabet to (result, reputation).
    f4 = [[[row[x][0] * (1 - rep), row[x][1] * (1 - rep), row[x][0] * rep, row[x][1] * rep] for x in range(2)]
          for row, rep in zip(f, (0, 1, 0, 1))]
    track = lambda s, x, y: .8 if y % 2 else .2
    reput = lambda s, x, y: .9 if y >= 2 else .1
    out.append(("F trackers plus pure reputation judge", p, [.5, .5], f4, [1.0],
                [judge(2, 4, track), judge(2, 4, track), judge(2, 4, reput)],
                ["tracker1", "tracker2", "reputation"], [0, 1], [("the true split, proposed from outside", [0, 1])]))
    # G. A panel sees more than its members: outcome is two bits; each judge reports one bit.
    p, q = [1.0], [.5, .5]
    f = [[[.5, 0, 0, .5], [0, .5, .5, 0]]]          # instance 0: bits equal; instance 1: bits differ
    out.append(("G each judge reads one bit of a two-bit outcome", p, q, f, [1.0],
                [judge(2, 4, lambda s, x, y: float(y // 2)), judge(2, 4, lambda s, x, y: float(y % 2))],
                ["bit1", "bit2"], [0, 1], []))
    return out


def fashion_credit():
    """Agreement on the same performance versus vindication across performances (world A)."""
    name, p, q, f, r, g, names, zbar, _ = worlds()[0]
    p, q = np.asarray(p), np.asarray(q)
    res = {}
    for a, b in ((0, 1), (2, 3), (0, 2)):
        K = panel_kernel(f, r, g, [a, b])                       # same performance
        joint = np.einsum("t,x,txa->a", p, q, K).reshape(2, 2)
        same = float((joint * np.log(joint / np.outer(joint.sum(1), joint.sum(0)), where=joint > 0,
                                     out=np.zeros_like(joint))).sum())
        Ka, Kb = panel_kernel(f, r, g, [a]), panel_kernel(f, r, g, [b])   # two performances, labelled by type
        mi = 0.0
        for x1 in range(2):
            for x0 in range(2):
                jt = np.einsum("t,ta,tb->ab", p, Ka[:, x1, :], Kb[:, x0, :])
                mi += q[x1] * q[x0] * float((jt * np.log(jt / np.outer(jt.sum(1), jt.sum(0)), where=jt > 0,
                                                         out=np.zeros_like(jt))).sum())
        res[f"{names[a]} & {names[b]}"] = {"agreement_same_performance_nats": same,
                                           "vindication_across_performances_nats": mi}
    return res


if __name__ == "__main__":
    report = {"author": "Claude (Fable 5.2)", "cycle": "P4-R1-C001", "session": 2,
              "worlds": [analyse(*w[:8], starts=w[8]) for w in worlds()],
              "fashion_credit_world_A": fashion_credit()}
    json.dump(report, sys.stdout, indent=1, default=lambda o: o.item() if hasattr(o, "item") else list(o))
