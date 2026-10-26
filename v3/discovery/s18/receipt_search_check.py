"""Exact finite development probe; source frozen before its first execution.

Check the contact-set formula against adaptive decision trees over all compatible
nonempty feasible subsets, for every nontrivial antichain on four actions.
No learned law, benchmark fee saving or general theorem is inferred from a pass.
"""
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import hashlib
import json
import platform
import time

start = time.monotonic_ns()
n = 4
full = (1 << n) - 1
edges = tuple(range(1, full + 1))
antichains = []
for bits in range(1, 1 << len(edges)):
    family = tuple(edges[i] for i in range(len(edges)) if bits >> i & 1)
    if all((a & b) not in (a, b) for a, b in combinations(family, 2)):
        antichains.append(family)
assert len(antichains) == 166

profiles = ((1, 1, 1, 1), (1, 2, 3, 5))
checks = 0
infeasible_targets = 0
states = 0
for family in antichains:
    worlds = tuple(f for f in range(1, full + 1)
                   if all(f & edge for edge in family))
    for good in range(1, full + 1):
        contained = tuple(e for e in family if e & good == e)
        guaranteed = all(f & good for f in worlds)
        assert bool(contained) == guaranteed
        if not guaranteed:
            infeasible_targets += 1
            continue
        for costs in profiles:
            @lru_cache(None)
            def value(current):
                global states
                states += 1
                common = full
                for f in current:
                    common &= f
                if common & good:
                    return 0
                choices = []
                for j in range(n):
                    yes = tuple(f for f in current if f >> j & 1)
                    no = tuple(f for f in current if not (f >> j & 1))
                    if yes and no:
                        choices.append(costs[j] + max(value(yes), value(no)))
                assert choices
                return min(choices)

            formula = min(sum(costs[j] for j in range(n) if e >> j & 1)
                          - max(costs[j] for j in range(n) if e >> j & 1)
                          for e in contained)
            actual = value(worlds)
            assert actual == formula, (family, good, costs, actual, formula)
            checks += 1

result = dict(
    status="pass", development=True, model="Codex (GPT-6)",
    n_actions=n, antichains=len(antichains), cost_profiles=profiles,
    feasible_target_cost_cases=checks,
    infeasible_target_families=infeasible_targets,
    dynamic_program_states=states,
    source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    python=platform.python_version(), runtime_ns=time.monotonic_ns()-start,
    scope="finite four-action oracle interface; no runtime or economic superiority claim",
)
print(json.dumps(result, indent=2))
