"""Tiny exact completion screen; Codex (GPT-6), 2026-10-23. No solver claim."""
import hashlib
import itertools
import json
import math
from pathlib import Path
import random
import time


def rank(vectors):
    pivots = {}
    for value in vectors:
        while value:
            bit = value.bit_length() - 1
            if bit in pivots:
                value ^= pivots[bit]
            else:
                pivots[bit] = value
                break
    return len(pivots)


def affine(base, directions):
    values = {base}
    for direction in directions:
        values |= {value ^ direction for value in values}
    return sorted(values)


def deficiency(sets):
    n = len(sets)
    candidates = []
    for mask in range(1 << n):
        union = [v for i, values in enumerate(sets) if mask >> i & 1
                 for v in values]
        candidates.append((n - mask.bit_count() + rank(union), mask))
    return min(candidates)


def main():
    started = time.perf_counter_ns()
    rng = random.Random(1427001)
    panels = comparisons = strict_improvements = refinement_checks = 0
    for r in range(1, 5):
        for n in range(1, 6):
            for _ in range(12):
                sets, compact = [], []
                for i in range(n):
                    base = rng.randrange(1 << r)
                    directions = [rng.randrange(1 << r)
                                  for _ in range(rng.randrange(3))]
                    sets.append(affine(base, directions))
                    compact.append(sorted({base, *(base ^ d for d in directions)}))
                maximum = max(rank(values) for values in itertools.product(*sets))
                sparse_maximum = max(rank(values) for values in itertools.product(*compact))
                bound, certificate = deficiency(sets)
                sparse_bound, _ = deficiency(compact)
                assert maximum == sparse_maximum == bound == sparse_bound
                comparisons += math.prod(map(len, sets))
                naive = min(n, rank(v for values in sets for v in values))
                assert bound <= naive
                strict_improvements += bound < naive
                # Every singleton refinement is truthful for that completion.
                chosen = [rng.choice(values) for values in sets]
                refined = [[v] if i % 2 == 0 else values
                           for i, (v, values) in enumerate(zip(chosen, sets))]
                refined_bound, _ = deficiency(refined)
                assert rank(chosen) <= refined_bound <= bound
                refinement_checks += 1
                panels += 1
    n, delta = 200, 0.05
    confidence = lambda k: 2 / (n - 2 * k) * (
        k * math.log(4) + math.log((k + 1) * (k + 2) / delta))
    result = {
        "contributor": "Codex (GPT-6)", "status": "PASS",
        "scope": "tiny exhaustive completions; no implemented matroid-intersection algorithm",
        "panels": panels, "completion_comparisons": comparisons,
        "strict_improvements_over_naive_rank": strict_improvements,
        "refinement_checks": refinement_checks,
        "structured_example": {
            "N": n, "delta": delta, "ambient_rank": 1000,
            "zero_cases": 199, "remaining_case_subspace_dimension": 20,
            "retained_equation_rank": 980,
            "union_span_rank": 20, "hidden_rank_upper_bound": 1,
            "confidence_bound_naive": confidence(20),
            "confidence_bound_certificate": confidence(1),
            "note": "formula evaluation; not an acquisition cost or superiority comparison"
        },
        "elapsed_ns": time.perf_counter_ns() - started,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    }
    Path(__file__).with_suffix('.json').write_text(
        json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
