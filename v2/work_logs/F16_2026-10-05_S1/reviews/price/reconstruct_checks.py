"""Fresh F16 mathematical checks. No imports from old proof/control modules.

ChatGPT (GPT-6 Astra Pro), delegated separate reviewer, 2026-10-05.
This is ordinary deterministic arithmetic, not a frozen stage or calibration.
"""
from fractions import Fraction as Q
from itertools import combinations, permutations, product
from math import comb
import json


def rank(rows):
    rows = [list(map(Q, row)) for row in rows]
    if not rows:
        return 0
    pivot = 0
    for col in range(len(rows[0])):
        pick = next((i for i in range(pivot, len(rows)) if rows[i][col]), None)
        if pick is None:
            continue
        rows[pivot], rows[pick] = rows[pick], rows[pivot]
        scale = rows[pivot][col]
        rows[pivot] = [x / scale for x in rows[pivot]]
        for i in range(pivot + 1, len(rows)):
            scale = rows[i][col]
            rows[i] = [x - scale * y for x, y in zip(rows[i], rows[pivot])]
        pivot += 1
        if pivot == len(rows):
            break
    return pivot


def cost(world, order, prices, penalty):
    value = Q(0)
    for i in order:
        value += prices[i]
        if world[i] == 0:
            return value
    return value + penalty


def rows(prices, penalty):
    worlds = tuple(product((0, 1), repeat=len(prices)))
    result = []
    for order in permutations(range(len(prices))):
        values = [cost(w, order, prices, penalty) for w in worlds]
        result.append(tuple(v - values[0] for v in values[1:]))
    return result


def observed_ranks(profiles, known=()):
    groups = [rows(c, m) for c, m in profiles]
    numeric = [r for g in groups for r in g]
    within = [tuple(x - y for x, y in zip(r, g[0])) for g in groups for r in g]
    cross = [tuple(x - y for x, y in zip(r, numeric[0])) for r in numeric]
    return {name: rank(list(known) + a) - rank(known)
            for name, a in (("numeric", numeric), ("within", within), ("cross", cross))}


def expected_ranks(profiles):
    c = profiles[0][0]
    k, n = len(c), 2 ** len(c) - 1
    if any(any(d[i] * c[0] != c[i] * d[0] for i in range(k)) for d, _ in profiles):
        penalties = [m for _, m in profiles]
        return dict(numeric=n if any(penalties) else n - 1,
                    within=n - 1, cross=n if len(set(penalties)) > 1 else n - 1)
    a = [(d[0] / c[0], m) for d, m in profiles]
    diffs = [tuple(x - y for x, y in zip(r, a[0])) for r in a]
    return dict(numeric=n - k + rank(a), within=n - k, cross=n - k + rank(diffs))


def mean(law, order, c, m):
    return sum((mass * cost(w, order, c, m) for w, mass in law.items()), Q(0))


def geometry(k, m):
    g = tuple(Q(k + 1, k - h + 1) for h in range(k)) + (Q(k) + m,)
    f = tuple(tuple(Q(comb(h, r), comb(k, r)) if h >= r else Q(0)
                    for h in range(k + 1)) for r in range(k))
    return g, f


def conditional_vertices(g, b):
    result = []
    for i in range(len(g)):
        if g[i] == b:
            result.append(tuple(Q(j == i) for j in range(len(g))))
        for j in range(i + 1, len(g)):
            if g[i] <= b <= g[j]:
                left = (g[j] - b) / (g[j] - g[i])
                result.append(tuple(left if h == i else 1 - left if h == j else Q(0)
                                    for h in range(len(g))))
    return result


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), Q(0))


def main():
    checked = 0
    lower_checks = 0
    for k in (2, 3, 4):
        for c in (tuple(Q(i + 1, i + 2) for i in range(k)),
                  tuple(Q((-1) ** i * (i + 1)) for i in range(k))):
            d = c[:-1] + (c[-1] + Q(1, 7),)
            families = (((c, Q(0)),), ((c, Q(4)),),
                        ((c, Q(0)), (d, Q(0))),
                        ((c, Q(4)), (d, Q(4))),
                        ((c, Q(4)), (d, Q(2))),
                        ((c, Q(0)), (tuple(2 * x for x in c), Q(0)), (c, Q(3))),
                        ((c, Q(4)), (tuple(2 * x for x in c), Q(4))),
                        ((c, Q(4)), (tuple(2 * x for x in c), Q(8))))
            for family in families:
                assert observed_ranks(family) == expected_ranks(family)
                checked += 1
            if all(x > 0 for x in c):
                worlds = tuple(product((0, 1), repeat=k))
                for s in range(k):
                    known = [tuple(Q(all(w[i] for i in a)) for w in worlds[1:])
                             for r in range(1, s + 1) for a in combinations(range(k), r)]
                    dimension = sum(comb(k, r) for r in range(s + 1, k + 1))
                    for m in (Q(0), Q(4)):
                        expect = dict(numeric=dimension - k + s + 1 if s <= k - 2 else int(m > 0),
                                      within=dimension - k + s, cross=dimension - k + s)
                        assert observed_ranks(((c, m),), known) == expect
                        lower_checks += 1

    zero_profiles = (((Q(1), Q(0), Q(0)), Q(1)),
                     ((Q(0), Q(1), Q(0)), Q(1)))
    p = {(0, 0, 0): Q(1, 2), (1, 1, 0): Q(1, 2)}
    q = {(1, 0, 0): Q(1, 2), (0, 1, 0): Q(1, 2)}
    for c, m in zero_profiles:
        for order in permutations(range(3)):
            assert mean(p, order, c, m) == mean(q, order, c, m)
    zero_ranks = observed_ranks(zero_profiles)
    assert zero_ranks == dict(numeric=6, within=5, cross=5)

    sharp = []
    for m in (Q(0), Q(1, 10), Q(1), Q(4, 3), Q(4), Q(100)):
        g, f = geometry(3, m)
        ds = [max(abs(v[j] - ((g[l] - g[j]) * v[i] + (g[j] - g[i]) * v[l]) /
                          (g[l] - g[i])) for i, j, l in combinations(range(4), 3)) for v in f]
        assert max(ds) == (2 * m + 1) / (3 * (m + 2))
        worlds = tuple(product((0, 1), repeat=3))
        a = {w: Q(1, 3) for w in worlds if sum(w) == 2}
        b = {(0, 0, 0): (m + 1) / (m + 2), (1, 1, 1): 1 / (m + 2)}
        for order in permutations(range(3)):
            assert mean(a, order, (1, 1, 1), m) == mean(b, order, (1, 1, 1), m) == 2
        sharp.append(dict(M=str(m), diameters=list(map(str, ds))))

    k, m, b = 4, Q(1, 10), Q(9, 8)
    g, f = geometry(k, m)
    vertices = conditional_vertices(g, b)
    intervals = [(min(dot(v, x) for x in vertices), max(dot(v, x) for x in vertices))
                 for v in f[1:]]
    mid = [(a + z) / 2 for a, z in intervals]
    assert mid == [Q(41, 496), Q(1, 48), Q(5, 248)]
    top = (b - 1 - sum(mid)) / m
    exact_two_world = mid[1] - 2 * mid[2] + top
    assert top == Q(5, 372) and exact_two_world == Q(-3, 496)
    coherent = (Q(11081, 13144), Q(0), Q(63, 424), Q(0), Q(55, 6572))
    assert sum(coherent) == 1 and dot(g, coherent) == b
    coherent_radius = max(max(abs(dot(v, coherent) - a), abs(dot(v, coherent) - z))
                          for v, (a, z) in zip(f[1:], intervals))
    free_radius = max((z - a) / 2 for a, z in intervals)
    assert coherent_radius == free_radius == Q(21, 496)

    old_population = {w: Q(1, 4) for w in product((0, 1), repeat=2)}
    changed_population = {(0, 0): Q(1, 8), (1, 0): Q(3, 8),
                          (0, 1): Q(3, 8), (1, 1): Q(1, 8)}
    for order in permutations(range(2)):
        assert mean(old_population, order, (1, 1), 1) == Q(7, 4)
        assert mean(changed_population, order, (1, 1), 2) == Q(7, 4)
    assert mean(old_population, (0, 1), (1, 2), 1) == Q(9, 4)
    assert mean(changed_population, (0, 1), (1, 2), 2) == Q(9, 4)

    report = dict(status="all exact assertions passed", old_control_imports=False,
                  principal_time_credit=0, direct_rank_families=checked,
                  lower_moment_rank_cases=lower_checks, zero_price_countermodel_ranks=zero_ranks,
                  A1_cases=sharp,
                  coherence=dict(midpoints=list(map(str, mid)), top=str(top),
                                 negative_two_failure_world_mass=str(exact_two_world),
                                 free_max_radius=str(free_radius), coherent_max_radius=str(coherent_radius)),
                  metadata_countermodel=dict(old_penalty="1", substituted_penalty="2",
                                             common_old_means="7/4", common_chain_probe="9/4",
                                             true_top_moment="1/4", substituted_top_moment="1/8"),
                  scope="Fresh deterministic review arithmetic only; no old stage, native producer, or calibration executed")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
