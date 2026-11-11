#!/usr/bin/env python3
"""Judgment as a forecast that what was seen will be seen again.

P4-R1-C001 session 4. Written by Claude (Fable 5.2), 2026-11-10, after the
author's statement of November 10. What is seen, W, is conditionally i.i.d.
given a persistent state theta. A conceptualisation c groups the things that
can be seen. I(c) = I(c(W_1); c(W_2)) is the information that the kind of
thing seen once carries about the kind of thing seen next.
"""
import json, sys
import numpy as np
from exact_scores import partitions, refines, canon

rng = np.random.default_rng(20261110)
TOL = 1e-10


def info(p, L, c):
    """I(c(W1); c(W2)) in nats; L[t, w] = P(w | theta = t)."""
    k = max(c) + 1
    g = np.zeros((len(p), k))
    for w, cell in enumerate(c):
        g[:, cell] += L[:, w]
    joint = np.einsum("t,ta,tb->ab", p, g, g)
    ind = np.outer(joint.sum(1), joint.sum(0))
    m = joint > 1e-300
    return float((joint[m] * np.log(joint[m] / ind[m])).sum())


def likelihood_partition(p, L):
    """Merge things whose likelihood functions over theta are proportional."""
    lab = []
    for w in range(L.shape[1]):
        for v in range(w):
            a, b = L[p > 0, w], L[p > 0, v]
            if np.allclose(a * b.sum(), b * a.sum(), atol=TOL):
                lab.append(lab[v]); break
        else:
            lab.append(w)
    return canon(lab)


def theorem_check(trials=200, nw=6, nt=4):
    parts = list(partitions(nw))
    bad, smallest = 0, float("inf")
    for i in range(trials):
        p = rng.dirichlet(np.ones(nt))
        L = rng.dirichlet(np.ones(nw), size=nt)
        if i % 2:                                   # force two things to be equally diagnostic
            ratio = rng.uniform(.3, 3)
            s = L[:, 0] + L[:, 1]
            L[:, 0], L[:, 1] = s / (1 + ratio), s * ratio / (1 + ratio)
        cstar = likelihood_partition(p, L)
        vals = {c: info(p, L, c) for c in parts}
        best = max(vals.values())
        mx = sorted(c for c in parts if vals[c] > best - TOL)
        exp = sorted(c for c in parts if refines(c, cstar))
        mono = all(vals[c] >= vals[d] - TOL for c in parts for d in parts if refines(c, d))
        bad += (mx != exp) or not mono
        smallest = min(smallest, min(best - vals[c] for c in parts if c not in exp))
    return {"random_worlds": trials, "things": nw, "partitions_each": len(parts), "violations": bad,
            "smallest_loss_of_a_non_refinement_nats": smallest}


def hierarchy_world(amps=(1.0, .4, .15)):
    """16 things indexed by 4 bits, 8 states indexed by 3 bits. Bit l of the thing interacts with bit l of the
    state with strength amps[l]; the fourth bit of the thing is not diagnostic of anything."""
    nt, nw = 8, 16
    L = np.zeros((nt, nw))
    for t in range(nt):
        for w in range(nw):
            e = sum(a * (1 if (w >> (3 - l)) & 1 else -1) * (1 if (t >> (2 - l)) & 1 else -1) for l, a in enumerate(amps))
            L[t, w] = np.exp(e)
        L[t] /= L[t].sum()
    return np.full(nt, 1 / nt), L


def level(l, nw=16):
    return canon([w >> (4 - l) for w in range(nw)]) if l else canon([0] * nw)


def ladder():
    p, L = hierarchy_world()
    vals = [info(p, L, level(l)) for l in range(5)]
    return {"levels": ["one kind", "2 types", "4 sub-types", "8 sub-sub-types", "16 (splits non-diagnostic pairs)"],
            "information_nats": vals, "gain_of_each_refinement": [vals[i + 1] - vals[i] for i in range(4)],
            "likelihood_partition_has_cells": max(likelihood_partition(p, L)) + 1}


def bounded(ns=(1, 2, 4, 8, 16, 32, 64, 128, 256, 512), draws=40000, alpha=1.0):
    """A judge who must learn this state's frequencies from n sightings. It estimates cell frequencies at its own
    granularity (add-alpha smoothing toward population rates), spreads each cell's probability over its members by
    population rates, and is scored by expected log probability of the next thing seen."""
    p, L = hierarchy_world()
    base = p @ L
    rows = []
    for n in ns:
        t = rng.integers(0, len(p), draws)
        counts = np.stack([rng.multinomial(n, L[s]) for s in t])          # [draw, thing]
        scores = []
        for l in range(5):
            c = np.array(level(l))
            k = c.max() + 1
            onehot = np.eye(k)[c]                                          # [thing, cell]
            cell_counts = counts @ onehot
            cell_base = base @ onehot
            est = (cell_counts + alpha * cell_base) / (n + alpha)
            phat = est[:, c] * (base / cell_base[c])[None, :]
            scores.append(float((L[t] * np.log(phat)).sum(axis=1).mean()))
        rows.append({"n": n, "score_by_level": [round(s, 4) for s in scores], "best_level": int(np.argmax(scores))})
    return rows


if __name__ == "__main__":
    json.dump({"author": "Claude (Fable 5.2)", "cycle": "P4-R1-C001", "session": 4, "seed": 20261110,
               "theorem_check": theorem_check(), "ladder": ladder(), "bounded_judges": bounded()}, sys.stdout, indent=1)
