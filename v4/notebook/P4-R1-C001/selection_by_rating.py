#!/usr/bin/env python3
"""Ratings that cause recurrence: who determines what is seen again.

P4-R1-C001 session 5. Written by Claude (Fable 5.2), 2026-11-10.
Things w have an environmental fitness phi(w). Raters j have rating vectors r_j (centred, unit norm over things).
A thing's log growth is  g = beta * rbar + e * phi, where rbar is the weighted mean rating: beta is how strongly
ratings cause recurrence (the same agent or other agents repeat what is rated well) and e how strongly the
environment does. A rater is vindicated to the extent its ratings forecast growth: s_j = <r_j, g>.
(1) Fixed raters, weights follow vindication (replicator).  (2) Raters adapt their ratings toward vindication.
"""
import json, sys
import numpy as np

rng = np.random.default_rng(20261110)


def unit(v):
    v = v - v.mean(axis=-1, keepdims=True)
    return v / np.linalg.norm(v, axis=-1, keepdims=True)


def replicator(G, h, beta, e, w0, steps=200000, dt=.05):
    w = np.array(w0, float)
    for _ in range(steps):
        s = beta * G @ w + e * h
        w = w * np.exp(dt * (s - w @ s)); w /= w.sum()
    return w


def fixed_raters():
    n_things, m = 60, 6
    phi = unit(rng.standard_normal(n_things))
    R = unit(rng.standard_normal((m, n_things)))
    for j, a in enumerate((.1, .3, .5, .7, .0, -.3)):            # raters with different alignment to the environment
        R[j] = unit(a * phi + np.sqrt(1 - a * a) * unit(R[j] - (R[j] @ phi) * phi))
    G, h = R @ R.T, R @ phi
    rows = []
    for ratio in (0.0, .2, 1.0, 3.0, 10.0):                      # e / beta
        beta, e = 1.0, ratio
        predicted = [bool(all(e * (h[k] - h[j]) < beta * (1 - G[k, j]) for k in range(m) if k != j)) for j in range(m)]
        observed = []
        for j in range(m):
            w0 = np.full(m, .02 / (m - 1)); w0[j] = .98
            observed.append(bool(replicator(G, h, beta, e, w0, steps=40000)[j] > .9))
        wu = replicator(G, h, beta, e, np.full(m, 1 / m), steps=40000)
        rows.append({"environment_to_rating_ratio": ratio, "consensus_stable_predicted": predicted,
                     "consensus_stable_observed": observed, "from_equal_weights_winner_alignment": round(float(h[int(np.argmax(wu))]), 2)})
    return {"alignments_with_environment": np.round(h, 2).tolist(), "by_ratio": rows}


def adaptive_raters():
    n_things, m = 60, 8
    phi = unit(rng.standard_normal(n_things))
    conv = unit(rng.standard_normal(n_things)); conv = unit(conv - (conv @ phi) * phi)   # a convention unrelated to fitness
    out = []
    for beta, e in ((1.0, 0.0), (1.0, .01), (1.0, .1), (10.0, .1), (1.0, 1.0)):
        R = unit(conv + .05 * rng.standard_normal((m, n_things)))
        t_half, dt = None, .01
        for step in range(400000):
            rbar = R.mean(axis=0)
            drift = beta * rbar + e * phi
            R = unit(R + dt * (drift - (R @ drift)[:, None] * R))
            if t_half is None and (R @ phi).mean() > .5:
                t_half = step * dt
                break
        out.append({"beta": beta, "e": e, "start_alignment": 0.0,
                    "time_to_alignment_one_half": t_half,
                    "alignment_when_stopped": round(float((R @ phi).mean()), 3)})
    return out


if __name__ == "__main__":
    json.dump({"author": "Claude (Fable 5.2)", "cycle": "P4-R1-C001", "session": 5, "seed": 20261110,
               "fixed_raters": fixed_raters(), "adaptive_raters": adaptive_raters()}, sys.stdout, indent=1)
