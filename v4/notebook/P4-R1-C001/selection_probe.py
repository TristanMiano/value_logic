#!/usr/bin/env python3
"""Limiting case: performers choose tasks in a skill-dependent way.

P4-R1-C001 exploratory probe. Written by Claude (Fable 5.2), 2026-11-09.
Uses exact_scores.value with a skill-dependent sampling matrix q[theta][z].
"""
import json, sys
import numpy as np
from exact_scores import value, partitions, refines, twin_partition, canon, bern, TOL


def maximizers(p, q, f, n):
    k = np.asarray(f).shape[1]
    vals = {c: value(p, q, f, c, n) for c in partitions(k)}
    best = max(vals.values())
    return vals, sorted(c for c in vals if vals[c] > best - TOL)


out = {"author": "Claude (Fable 5.2)", "cycle": "P4-R1-C001"}

# (i) Disjoint specialists: skill 0 only attempts type 0, skill 1 only type 1.
p = [.5, .5]
f = [[bern(.9), bern(.1)], [bern(.1), bern(.9)]]
q = [[1.0, 0.0], [0.0, 1.0]]
vals, mx = maximizers(p, q, f, 2)
out["disjoint_specialists"] = {"outcome_twins": twin_partition(p, f), "values_n2": {str(c): v for c, v in vals.items()},
                               "merged_is_optimal": (0, 0) in mx}
# same world with a share e of skill-independent assignment
rows = []
for e in (0.0, 0.01, 0.1, 0.5, 1.0):
    q = [[(1 - e) * a + e * .5 for a in row] for row in ([1.0, 0.0], [0.0, 1.0])]
    vals, mx = maximizers(p, q, f, 2)
    rows.append({"exploration_share": e, "deficit_of_merging_n2": vals[(0, 1)] - vals[(0, 0)]})
out["exploration_repair"] = rows

# (ii) Outcome twins chosen differently by skill; a third type whose outcome depends on skill.
p = [.5, .5]
f = [[bern(.5), bern(.5), bern(.9)], [bern(.5), bern(.5), bern(.1)]]
q = [[.6, .1, .3], [.1, .6, .3]]
vals, mx = maximizers(p, q, f, 2)
out["twins_chosen_by_skill"] = {"outcome_twins": twin_partition(p, f), "joint_twins": twin_partition(p, f, q),
                                "gain_from_splitting_outcome_twins_n2": vals[(0, 1, 2)] - vals[(0, 0, 1)]}
# (ii') same but no type's outcome depends on skill: the split is then worthless
f2 = [[bern(.5), bern(.5), bern(.7)], [bern(.5), bern(.5), bern(.7)]]
vals, mx = maximizers(p, q, f2, 2)
out["twins_chosen_by_skill_no_skill_effect"] = {"gain_from_splitting_n2": vals[(0, 1, 2)] - vals[(0, 0, 1)]}

# (iii) Random full-support selection worlds.
rng = np.random.default_rng(20261109)
tally = {"worlds": 0, "maximizers_equal_refinements_of_joint_twins": 0,
         "some_non_outcome_twins_merged_at_optimum": 0, "smallest_deficit_merging_non_outcome_twins": float("inf")}
for i in range(200):
    nt, k = 3, 3
    p = rng.dirichlet(np.ones(nt)).tolist()
    q = rng.dirichlet(np.ones(k) * 2, size=nt)
    f = rng.dirichlet(np.ones(2), size=(nt, k))
    if i % 2:
        f[:, 1, :] = f[:, 0, :]          # outcome twins, generically chosen differently
    q, f = q.tolist(), f.tolist()
    jt, ot = twin_partition(p, f, q), twin_partition(p, f)
    vals, mx = maximizers(p, q, f, 1)
    expected = sorted(c for c in vals if refines(c, jt))
    tally["worlds"] += 1
    tally["maximizers_equal_refinements_of_joint_twins"] += mx == expected
    bad = [c for c in mx if not refines(c, ot)]
    tally["some_non_outcome_twins_merged_at_optimum"] += bool(bad)
    best = max(vals.values())
    d = min((best - vals[c] for c in vals if not refines(c, ot)), default=float("inf"))
    tally["smallest_deficit_merging_non_outcome_twins"] = min(tally["smallest_deficit_merging_non_outcome_twins"], d)
out["random_full_support_selection_n1"] = tally
json.dump(out, sys.stdout, indent=1, default=lambda o: o.item() if hasattr(o, "item") else list(o))
