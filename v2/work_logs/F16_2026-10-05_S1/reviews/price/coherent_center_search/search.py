"""One predeclared exploratory F16 mathematical search, not an F15 experiment.

ChatGPT (GPT-6 Astra Pro), delegated separate reviewer, zero principal credit.
No old control imports and no frozen populations. Exact certificates are required.
"""
from fractions import Fraction as Q
from itertools import combinations
from math import comb
from pathlib import Path
import hashlib
import json
import shutil
import sys
import traceback


def dump(value):
    return json.dumps(value, default=lambda x: str(x) if isinstance(x, Q) else x)


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), Q(0))


def basis_vertex(equalities, inequalities, numerical, tolerance):
    n = len(numerical)
    proposed = list(equalities)
    for i, x in enumerate(numerical):
        if abs(x) <= tolerance:
            proposed.append((tuple(Q(j == i) for j in range(n)), Q(0)))
    for row, bound in inequalities:
        if abs(sum(float(a)*b for a, b in zip(row, numerical))-float(bound)) <= tolerance:
            proposed.append((row, bound))
    reduced = []
    pivots = []
    for row, bound in proposed:
        row = list(row) + [bound]
        for p, old in zip(pivots, reduced):
            scale = row[p]
            row = [x-scale*y for x, y in zip(row, old)]
        p = next((i for i in range(n) if row[i]), None)
        if p is None:
            continue
        scale = row[p]
        row = [x/scale for x in row]
        pivots.append(p)
        reduced.append(row)
        if len(pivots) == n:
            break
    if len(pivots) != n:
        return None
    result = [Q(0)]*n
    for p, row in reversed(list(zip(pivots, reduced))):
        result[p] = row[-1]-sum((row[j]*result[j] for j in range(n) if j != p), Q(0))
    if (any(x < 0 for x in result) or
        any(dot(a, result) != b for a, b in equalities) or
        any(dot(a, result) > b for a, b in inequalities)):
        return None
    return tuple(result)


def lp_at_fiber(g, f, mu, intervals, free):
    from scipy.optimize import linprog
    n = len(g)
    equalities = [(tuple(Q(1) for _ in g), Q(1)), (g, mu)]
    inequalities = []
    for row, (lo, hi) in zip(f, intervals):
        inequalities.extend(((row, lo+free), (tuple(-x for x in row), free-hi)))
    result = linprog([0.0]*n, A_ub=[[float(x) for x in a] for a, _ in inequalities],
                     b_ub=[float(b) for _, b in inequalities],
                     A_eq=[[float(x) for x in a] for a, _ in equalities],
                     b_eq=[float(b) for _, b in equalities], bounds=[(0, None)]*n,
                     method="highs")
    attempts = [dict(kind="free_radius_feasibility", status=int(result.status),
                     message=result.message, numerical=None if result.x is None else result.x.tolist())]
    if result.success:
        for tolerance in (1e-7, 1e-9, 1e-11):
            witness = basis_vertex(equalities, inequalities, result.x, tolerance)
            attempts.append(dict(kind="exact_basis", tolerance=tolerance, witness=witness))
            if witness is not None:
                return dict(status="exact_feasible_center", center=witness, attempts=attempts)

    eq = [(a+(Q(0),), b) for a, b in equalities]
    iq = []
    for row, (lo, hi) in zip(f, intervals):
        iq.extend(((row+(Q(-1),), lo), (tuple(-x for x in row)+(Q(-1),), -hi)))
    opt = linprog([0.0]*n+[1.0], A_ub=[[float(x) for x in a] for a, _ in iq],
                  b_ub=[float(b) for _, b in iq],
                  A_eq=[[float(x) for x in a] for a, _ in eq],
                  b_eq=[float(b) for _, b in eq], bounds=[(0, None)]*(n+1), method="highs")
    attempts.append(dict(kind="minimum_coherent_radius", status=int(opt.status),
                         message=opt.message, numerical=None if opt.x is None else opt.x.tolist()))
    primal = None
    if opt.success:
        for tolerance in (1e-7, 1e-9, 1e-11):
            primal = basis_vertex(eq, iq, opt.x, tolerance)
            attempts.append(dict(kind="exact_minimum_basis", tolerance=tolerance, witness=primal))
            if primal is not None:
                break
        # Round only to propose a dual. Normalize and impose every inequality
        # exactly; its resulting bound is valid even if it is not optimal.
        alpha = [max(Q(0), Q(float(-a)).limit_denominator(10**12))
                 for a in opt.ineqlin.marginals]
        total = sum(alpha)
        if total:
            alpha = [a/total for a in alpha]
            slope = Q(float(opt.eqlin.marginals[1])).limit_denominator(10**12)
            weights = [alpha[2*r]-alpha[2*r+1] for r in range(len(f))]
            intercept = min(sum((weights[r]*f[r][h] for r in range(len(f))), Q(0))-slope*g[h]
                            for h in range(n))
            lower = intercept+slope*mu+sum(
                (alpha[2*r+1]*hi-alpha[2*r]*lo for r, (lo, hi) in enumerate(intervals)), Q(0))
            assert all(a >= 0 for a in alpha) and sum(alpha) == 1
            assert all(intercept+slope*g[h] <= sum((weights[r]*f[r][h] for r in range(len(f))), Q(0))
                       for h in range(n))
            dual = dict(alpha=alpha, slope=slope, intercept=intercept, lower_bound=lower)
            attempts.append(dict(kind="exact_dual", certificate=dual))
            if lower > free:
                return dict(status="exact_strict_gap", primal=primal, dual=dual, attempts=attempts)
    if primal is not None and primal[-1] <= free:
        return dict(status="exact_feasible_center", center=primal[:-1], attempts=attempts)
    return dict(status="unresolved", attempts=attempts)


def one_case(k, m, mu, g, f):
    vertices = set()
    for i in range(k+1):
        if g[i] == mu:
            vertices.add(tuple(Q(h == i) for h in range(k+1)))
        for j in range(i+1, k+1):
            if g[i] <= mu <= g[j]:
                right = (mu-g[i])/(g[j]-g[i])
                vertices.add(tuple(1-right if h == i else right if h == j else Q(0) for h in range(k+1)))
    intervals = [(min(dot(row, x) for x in vertices), max(dot(row, x) for x in vertices)) for row in f]
    free = max((hi-lo)/2 for lo, hi in intervals)
    singleton = (intervals[0][1]-intervals[0][0])/2
    right = (mu-g[0])/(g[-1]-g[0])
    endpoint = tuple(1-right if h == 0 else right if h == k else Q(0) for h in range(k+1))
    adjacent = next(x for x in sorted(vertices) if
                    len([h for h in range(k+1) if x[h]]) <= 1 or
                    max(h for h in range(k+1) if x[h])-min(h for h in range(k+1) if x[h]) == 1)
    candidate = tuple((a+b)/2 for a, b in zip(endpoint, adjacent))
    assert sum(candidate) == 1 and dot(g, candidate) == mu and all(x >= 0 for x in candidate)
    values = [dot(row, candidate) for row in f]
    radius = max(max(value-lo, hi-value) for value, (lo, hi) in zip(values, intervals))
    assert radius >= free
    record = dict(k=k, M=m, mu=mu, intervals=intervals, free_radius=free,
                  singleton_half_width=singleton, vertex_count=len(vertices),
                  candidate=candidate, candidate_values=values, candidate_radius=radius,
                  candidate_at_free_radius=(radius == free), candidate_at_singleton_radius=(radius <= singleton))
    if radius == free:
        record["disposition"] = dict(status="exact_candidate_center", center=candidate)
    else:
        record["disposition"] = lp_at_fiber(g, f, mu, intervals, free)
    return record


def main():
    base = Path(__file__).resolve().parent
    number = 1
    while (base/f"attempt{number}").exists():
        number += 1
    out = base/f"attempt{number}"
    out.mkdir()
    shutil.copy2(__file__, out/"source.py")
    manifest = dict(scope="Exploratory F16 math probes; no frozen populations or F15 stage",
                    principal_clock_credit=0, k=list(range(2, 9)),
                    M=["0", "1/10", "1", "4", "16"],
                    adjacent_interval_fractions=["0", "1/4", "1/2", "3/4"], include_final_endpoint=True,
                    specified_fibers=735, stop_on_first_exact_gap=True, command=" ".join(sys.argv),
                    source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (out/"manifest.json").write_text(dump(manifest)+"\n")
    counts = dict(checked=0, candidate_pass=0, candidate_singleton_pass=0, lp_no_gap=0,
                  strict_gap=0, unresolved=0)
    candidate_failures = []
    try:
        with (out/"records.jsonl").open("w") as log:
            stop = False
            for k in range(2, 9):
                if stop:
                    break
                for m in map(Q, ("0", "1/10", "1", "4", "16")):
                    if stop:
                        break
                    g = tuple(Q(k+1, k-h+1) for h in range(k))+(Q(k)+m,)
                    f = tuple(tuple(Q(comb(h, r), comb(k, r)) if h >= r else Q(0) for h in range(k+1))
                              for r in range(1, k))
                    means = sorted({g[j]+t*(g[j+1]-g[j]) for j in range(k)
                                    for t in map(Q, ("0", "1/4", "1/2", "3/4"))}|{g[-1]})
                    for mu in means:
                        record = one_case(k, m, mu, g, f)
                        log.write(dump(record)+"\n")
                        log.flush()
                        counts["checked"] += 1
                        counts["candidate_pass"] += int(record["candidate_at_free_radius"])
                        counts["candidate_singleton_pass"] += int(record["candidate_at_singleton_radius"])
                        if not record["candidate_at_free_radius"]:
                            candidate_failures.append(dict(k=k, M=m, mu=mu,
                                                           result=record["disposition"]["status"]))
                        status = record["disposition"]["status"]
                        counts["lp_no_gap"] += int(status == "exact_feasible_center")
                        counts["unresolved"] += int(status == "unresolved")
                        if status == "exact_strict_gap":
                            counts["strict_gap"] += 1
                            (out/"strict_gap.json").write_text(dump(record)+"\n")
                            stop = True
                            break
            summary = dict(counts=counts, specified_but_unrun=735-counts["checked"],
                           candidate_failures=candidate_failures,
                           conclusion="finite evidence only; no universal inference")
            (out/"summary.json").write_text(dump(summary)+"\n")
            print(dump(summary))
            print(str(out))
    except Exception:
        (out/"failure.txt").write_text(traceback.format_exc())
        raise


if __name__ == "__main__":
    main()
