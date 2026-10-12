"""Developmental exact planner for monotone truth chains.

ChatGPT (GPT-6 Astra Pro), October 12, 2026.
Prices are exogenous upper bounds for COMPLETE checked answers, including the
declared interval update. No supplied CNF prices, learned source law, censoring
guarantee, or solver-performance result is asserted by this model.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


def signature(h: int, masks: tuple[int, ...]) -> tuple[int, ...]:
    """Parity-error vector when H is the first UNSAT index."""
    return tuple((mask >> h).bit_count() % 2 for mask in masks)


def plan(costs, masks, mode="minimax", weights=None, allowed_queries=None, interval=None):
    """Plan complete feature acquisition over H=0,...,len(costs).

    A truth query at j returns UNSAT iff H<=j and SAT otherwise. A leaf is
    allowed only when every requested feature is constant over its full
    remaining interval. Expected mode requires a strictly positive fixed law.
    """
    costs = tuple(Fraction(c) for c in costs)
    n = len(costs)
    masks = tuple(masks)
    if not n or any(c <= 0 for c in costs):
        raise ValueError("Require nonempty positive complete-answer prices")
    if any(mask < 0 or mask >= 1 << n or mask.bit_count() % 2 for mask in masks):
        raise ValueError("Targets must be even boundary masks on the chain")
    if mode not in ("minimax", "expected"):
        raise ValueError("Unknown planning mode")
    if mode == "expected":
        if weights is None or len(weights) != n + 1 or any(w <= 0 for w in weights):
            raise ValueError("Expected mode requires positive fixed source weights")
        weights = tuple(Fraction(w) for w in weights)
    allowed = frozenset(range(n) if allowed_queries is None else allowed_queries)
    if any(j not in range(n) for j in allowed):
        raise ValueError("Query outside chain")
    lo, hi = (0, n) if interval is None else tuple(interval)
    if not (0 <= lo <= hi <= n):
        raise ValueError("Invalid retained threshold interval")
    sig = tuple(signature(h, masks) for h in range(n + 1))
    changes = [0]
    for h in range(1, n + 1):
        changes.append(changes[-1] + (sig[h] != sig[h - 1]))
    cumulative = [Fraction(0)]
    if weights is not None:
        for weight in weights:
            cumulative.append(cumulative[-1] + weight)

    def mass(lo, hi):
        return cumulative[hi + 1] - cumulative[lo]

    @lru_cache(None)
    def solve(lo, hi):
        if changes[hi] == changes[lo]:
            return Fraction(0), ("leaf", sig[lo])
        options = []
        for j in range(lo, hi):
            if j not in allowed:
                continue
            left = solve(lo, j)
            right = solve(j + 1, hi)
            if left is None or right is None:
                continue
            if mode == "minimax":
                value = costs[j] + max(left[0], right[0])
            else:
                value = costs[j] + (
                    mass(lo, j) * left[0] + mass(j + 1, hi) * right[0]
                ) / mass(lo, hi)
            options.append((value, j, ("query", j, left[1], right[1])))
        if not options:
            return None
        value, _, tree = min(options, key=lambda item: (item[0], item[1]))
        return value, tree

    result = solve(lo, hi)
    if result is None:
        raise ValueError("Allowed query menu cannot determine all targets")
    return result


def execute(tree, h, costs):
    """Independent explicit rollout on one latent threshold."""
    work = Fraction(0)
    trace = []
    while tree[0] == "query":
        _, j, unsat, sat = tree
        work += costs[j]
        truth = "UNSAT" if h <= j else "SAT"
        trace.append((j, truth))
        tree = unsat if h <= j else sat
    return work, tuple(tree[1]), trace


def brute_trees(n, masks):
    """Enumerate every ordered query tree stopping only at a constant vector."""
    @lru_cache(None)
    def all_trees(lo, hi):
        values = {signature(h, masks) for h in range(lo, hi + 1)}
        if len(values) == 1:
            return (("leaf", next(iter(values))),)
        result = []
        for j in range(lo, hi):
            for left in all_trees(lo, j):
                for right in all_trees(j + 1, hi):
                    result.append(("query", j, left, right))
        return tuple(result)
    return all_trees(0, n)


def score_tree(tree, costs, masks, mode, weights):
    values = []
    for h in range(len(costs) + 1):
        cost, output, _ = execute(tree, h, costs)
        assert output == signature(h, masks)
        values.append(cost)
    if mode == "minimax":
        return max(values)
    return sum(w * value for w, value in zip(weights, values)) / sum(weights)


def example(costs, pair, weights):
    masks = ((1 << pair[0]) | (1 << pair[1]),)
    result = {"costs": costs, "target_pair": pair, "fixed_source_weights": weights}
    for mode in ("minimax", "expected"):
        unrestricted, tree = plan(costs, masks, mode, weights)
        endpoint, endpoint_tree = plan(costs, masks, mode, weights, pair)
        result[mode] = {
            "unrestricted_value": str(unrestricted),
            "endpoint_only_value": str(endpoint),
            "unrestricted_first_query": tree[1] if tree[0] == "query" else None,
            "unrestricted_tree": tree,
            "endpoint_tree": endpoint_tree,
            "per_threshold": [
                {
                    "h": h,
                    "work": str(execute(tree, h, costs)[0]),
                    "trace": execute(tree, h, costs)[2],
                }
                for h in range(len(costs) + 1)
            ],
        }
    return result


def probe():
    """One bounded DP-versus-enumeration screen; no learned-price fixture."""
    systems = mode_checks = explicit_rollouts = 0
    for n in (2, 3, 4):
        pairs = tuple((1 << a) | (1 << b) for a, b in combinations(range(n), 2))
        families = [(mask,) for mask in pairs]
        if len(pairs) > 1:
            families.append(pairs)
        price_vectors = (
            tuple(1 for _ in range(n)),
            tuple(j + 1 for j in range(n)),
            tuple(1 if j % 2 else 7 for j in range(n)),
        )
        weights = tuple(1 + h % 3 for h in range(n + 1))
        for masks in families:
            trees = brute_trees(n, masks)
            for costs in price_vectors:
                systems += 1
                for mode in ("minimax", "expected"):
                    expected = min(score_tree(t, costs, masks, mode, weights) for t in trees)
                    got, tree = plan(costs, masks, mode, weights)
                    assert got == expected
                    assert score_tree(tree, costs, masks, mode, weights) == expected
                    mode_checks += 1
                    explicit_rollouts += (len(trees) + 1) * (n + 1)
    robust_bridge = example([10, 1, 12, 10], (0, 3), [1, 1, 1, 1, 1])
    assert robust_bridge["minimax"]["unrestricted_value"] == "11"
    assert robust_bridge["minimax"]["endpoint_only_value"] == "20"
    assert robust_bridge["minimax"]["unrestricted_first_query"] == 1
    conditional_bridge = example([1, 10, 10], (1, 2), [1, 1, 1, 1])
    assert conditional_bridge["expected"]["unrestricted_value"] == "27/2"
    assert conditional_bridge["expected"]["endpoint_only_value"] == "15"
    assert conditional_bridge["minimax"]["unrestricted_value"] == "20"
    return {
        "contributor": "ChatGPT (GPT-6 Astra Pro)",
        "date_utc": "2026-10-12",
        "status": "DEVELOPMENT",
        "scope": "Exogenous complete-answer query prices; source-independent minimax and explicitly supplied-law expected planning",
        "probe_plan": "All single pair targets and the all-pair vector for 2,3,4 vertices; three price vectors; enumerate all stopping query trees and roll out every threshold",
        "systems": systems,
        "mode_checks": mode_checks,
        "explicit_threshold_rollouts": explicit_rollouts,
        "robust_intermediate_bridge": robust_bridge,
        "expected_weak_ancestor_bridge": conditional_bridge,
        "cnf_performance_claim": False,
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
    }


if __name__ == "__main__":
    result = probe()
    destination = Path(__file__).with_name("threshold_plan_results.json")
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "path": str(destination),
        "systems": result["systems"],
        "mode_checks": result["mode_checks"],
        "explicit_threshold_rollouts": result["explicit_threshold_rollouts"],
        "robust_bridge_minimax": result["robust_intermediate_bridge"]["minimax"]["unrestricted_value"],
        "endpoint_minimax": result["robust_intermediate_bridge"]["minimax"]["endpoint_only_value"],
    }))
