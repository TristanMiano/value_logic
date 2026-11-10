#!/usr/bin/env python3
"""Which facts about tasks survive judges' task-specific conventions.

P4-R1-C001 session 3. Written by Claude (Fable 5.2), 2026-11-10.
Approvals are performance-mediated with a channel that may depend on the task:
k(a | theta, x) = sum_y f(y | theta, z(x)) G_x(a | y). From approvals on two
performances of one performer we can form, for task types x, x',
  cross second moments  E_theta[k(a|theta,x) k(a'|theta,x')]
(also for x = x', from two separate performances). Everything below is
computed from those moments only, never from f or G directly.
"""
import json, sys
import numpy as np

rng = np.random.default_rng(20261110)


def moments(p, K):
    """mean[x, a] and second[x, a, x', a'] of the approval kernel K[t, x, a] under skill law p."""
    mean = np.einsum("t,txa->xa", p, K)
    second = np.einsum("t,txa,tyb->xayb", p, K, K)
    return mean, second


def transfer_corr_binary(mean, second):
    """Disattenuated correlation of approval rates across performers (binary approvals, a = 1)."""
    m = mean[:, 1]
    cov = second[:, 1, :, 1] - np.outer(m, m)
    return cov / np.sqrt(np.outer(np.diag(cov), np.diag(cov)))


def canonical_corrs(mean, second, x, y):
    """Canonical correlations between the skill-function spaces of task types x and y (centred)."""
    def block(u, v):
        return second[u, :, v, :] - np.outer(mean[u], mean[v])
    def inv_sqrt(S):
        w, V = np.linalg.eigh(S)
        keep = w > 1e-10
        return V[:, keep] / np.sqrt(w[keep])
    A, B = inv_sqrt(block(x, x)), inv_sqrt(block(y, y))
    return np.clip(np.linalg.svd(A.T @ block(x, y) @ B, compute_uv=False), 0, 1)


def binary_world():
    # skills: two independent binary abilities (u, v); success rates per type
    p, phi = [], []
    for u in (0, 1):
        for v in (0, 1):
            p.append(.25)
            a = .2 + .6 * u                       # type A: ability u
            phi.append([a, .15 + .5 * a,          # type B: same ability, flatter and harder (positive affine in A)
                        .2 + .6 * v,              # type C: ability v
                        .1 + .3 * u + .4 * v,     # type D: a blend
                        1 - a])                   # type E: the reverse of A
    p, phi = np.array(p), np.array(phi)
    truth = np.corrcoef(phi.T * 1.0, aweights=p) if False else None
    m = p @ phi
    cov = (phi - m).T @ np.diag(p) @ (phi - m)
    truth = cov / np.sqrt(np.outer(np.diag(cov), np.diag(cov)))
    out = {"types": ["A", "B same skill as A, harder", "C other skill", "D blend", "E reverse of A"],
           "true_transfer_correlation": np.round(truth, 6).tolist(), "communities": []}
    f = np.stack([1 - phi, phi], axis=2)                     # f[t, z, y]
    for name in ("lenient to some tasks", "harsh to others", "random leniency"):
        lo = rng.uniform(.02, .45, 5)                        # P(approve | failure, task)
        hi = lo + rng.uniform(.1, .5, 5)                     # P(approve | success, task) > lo: better than chance
        G = np.stack([np.stack([1 - lo, lo], 1), np.stack([1 - hi, hi], 1)], axis=1)   # G[x, y, a]
        K = np.einsum("tzy,zya->tza", f, G)
        r = transfer_corr_binary(*moments(p, K))
        out["communities"].append({"community": name, "approve_given_failure": np.round(lo, 2).tolist(),
                                   "approve_given_success": np.round(hi, 2).tolist(),
                                   "max_abs_error_vs_truth": float(np.abs(r - truth).max())})
    return out


def general_world():
    nt, nz, ny = 6, 4, 3
    p = rng.dirichlet(np.ones(nt))
    f = rng.dirichlet(np.ones(ny), size=(nt, nz))
    f[:, 1, :] = f[:, 0, :] @ np.array([[.7, .2, .1], [.1, .8, .1], [.2, .1, .7]])   # type 1: a recalibration of type 0
    base = [[canonical_corrs(*moments(p, f), x, y).round(6).tolist() for y in range(nz)] for x in range(nz)]
    err = 0.0
    for trial in range(20):
        na = int(rng.integers(3, 6))
        G = rng.dirichlet(np.ones(na), size=(nz, ny))                               # full column rank almost surely
        K = np.einsum("tzy,zya->tza", f, G)
        mom = moments(p, K)
        for x in range(nz):
            for y in range(nz):
                c = canonical_corrs(*mom, x, y)
                b = np.array(base[x][y])
                k = min(len(c), len(b))
                err = max(err, float(np.abs(np.sort(c)[::-1][:k] - np.sort(b)[::-1][:k]).max()))
    return {"outcome_values": ny, "types": nz, "canonical_correlations_from_outcomes": base,
            "note": "type 1 is a fixed recalibration of type 0, so their spaces coincide (all correlations 1)",
            "max_abs_difference_over_20_random_task_dependent_channels": err}


def tree_world():
    """Objects with r shared causes, D criteria. Two independent noisy ratings per object and criterion, each with
    its own unknown scale and offset per criterion. Recover the cosines between loadings and the number of causes."""
    N, r, D = 40000, 2, 7
    B = np.abs(rng.standard_normal((D, r)))
    h = rng.standard_normal((N, r))
    v = h @ B.T
    def rate():
        scale, off = rng.uniform(.5, 3, D), rng.uniform(-2, 2, D)
        return off + scale * v + rng.standard_normal((N, D)) * np.linalg.norm(B, axis=1) * .8
    r1, r2 = rate(), rate()
    c = np.cov(np.hstack([r1, r2]).T)[:D, D:]
    # c[d, d'] = Cov(first rating on d, second rating on d'). The two ratings use different unknown scales, so the
    # scale-free quantity is the geometric mean of c[d, d'] and c[d', d] over the same-criterion covariances.
    R = np.sign(c) * np.sqrt(np.abs(c * c.T)) / np.sqrt(np.outer(np.diag(c), np.diag(c)))
    cos = (B @ B.T) / np.outer(np.linalg.norm(B, axis=1), np.linalg.norm(B, axis=1))
    naive = np.corrcoef(r1.T)
    eig = np.sort(np.linalg.eigvalsh(R))[::-1]
    return {"objects": N, "criteria": D, "shared_causes": r, "rating_noise_sd_relative_to_signal": .8,
            "max_abs_error_recovered_cosines": float(np.abs(R - cos).max()),
            "max_abs_error_naive_single_rating_correlations": float(np.abs(naive - cos)[~np.eye(D, dtype=bool)].max()),
            "eigenvalues_of_recovered_matrix": np.round(eig, 3).tolist()}


if __name__ == "__main__":
    json.dump({"author": "Claude (Fable 5.2)", "cycle": "P4-R1-C001", "session": 3, "seed": 20261110,
               "binary_world": binary_world(), "general_world": general_world(), "tree_world": tree_world()},
              sys.stdout, indent=1)
