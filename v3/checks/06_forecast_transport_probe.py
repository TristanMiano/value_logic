"""Exact finite witnesses for CF-8/9; new P3-06 development, not recovered work.

Contributor: ChatGPT (GPT-6 Astra Pro), October 9, 2026 UTC.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import platform
import time


def encoded(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): encoded(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [encoded(v) for v in value]
    return value


def run():
    count = 0

    def check(condition, message):
        nonlocal count
        count += 1
        if not condition:
            raise AssertionError(message)

    # Each context occurs four times; the conditional report counts realize
    # exactly the two announced report distributions in CF-8.
    contexts = ["A"] * 4 + ["B"] * 4
    labels = [0] * 4 + [1] * 4
    sampled = [F(1, 4)] * 3 + [F(3, 4)] + [F(1, 4)] + [F(3, 4)] * 3
    means = [F(3, 8)] * 4 + [F(5, 8)] * 4
    original_residuals = {
        p: sum((F(y) - q for q, y in zip(sampled, labels) if q == p), F(0))
        for p in set(sampled)}
    mean_residuals = {
        p: sum((F(y) - q for q, y in zip(means, labels) if q == p), F(0))
        for p in set(means)}
    check(all(v == 0 for v in original_residuals.values()), "Original grid is exactly calibrated.")
    check(mean_residuals == {F(3, 8): F(-3, 2), F(5, 8): F(3, 2)}, "Means have nonzero residuals.")
    old_loss = sum(((p - y) ** 2 for p, y in zip(sampled, labels)), F(0)) / 8
    mean_loss = sum(((p - y) ** 2 for p, y in zip(means, labels)), F(0)) / 8
    check(old_loss == F(3, 16), "Original Brier score.")
    check(mean_loss == F(9, 64), "Mean Brier score.")
    check(old_loss - mean_loss == F(3, 64), "Jensen improvement coexists with calibration failure.")

    # Independent exhaustive rational checks of the local inequality, including
    # tent knots, endpoints, non-dyadic resolution and both binary outcomes.
    grid = [F(i, 12) for i in range(13)]
    cases = 0
    for m in (1, 2, 3, 8):
        for p in grid:
            for changed in grid:
                distance = abs(changed - p)
                for y in (0, 1):
                    check(abs((changed - y) ** 2 - (p - y) ** 2) <= 2 * distance,
                          "Brier displacement bound.")
                    for j in range(m + 1):
                        left = max(F(0), 1 - abs(m * p - j))
                        right = max(F(0), 1 - abs(m * changed - j))
                        difference = abs(right * (y - changed) - left * (y - p))
                        check(difference <= (m + 1) * distance, "Tent residual displacement bound.")
                        cases += 1

    # Check a rounded tape with changing prices and a fixed expert tape. This
    # validates transport of recorded outputs, not rerunning a different learner.
    tape = []
    for t in range(1, 49):
        p = F((17 * t) % 101, 100)
        rounded = F((p * 8 + F(1, 2)).numerator // (p * 8 + F(1, 2)).denominator, 8)
        y = (t // 3 + t) % 2
        w = (F(0), F(1, 2), F(1), F(5))[t % 4]
        q = F(t % 5, 4)
        tape.append((p, rounded, y, w, q))
    displacement = sum((w * abs(q - p) for p, q, y, w, expert in tape), F(0))
    old = sum((w * (p - y) ** 2 for p, q, y, w, expert in tape), F(0))
    new = sum((w * (q - y) ** 2 for p, q, y, w, expert in tape), F(0))
    expert_loss = sum((w * (expert - y) ** 2 for p, q, y, w, expert in tape), F(0))
    check(new - expert_loss <= old - expert_loss + 2 * displacement, "Whole-tape regret transport.")
    bin_comparison = []
    for j in range(9):
        a = sum((w * max(F(0), 1 - abs(8 * p - j)) * (y - p)
                 for p, q, y, w, expert in tape), F(0))
        b = sum((w * max(F(0), 1 - abs(8 * q - j)) * (y - q)
                 for p, q, y, w, expert in tape), F(0))
        check(abs(b) <= abs(a) + 9 * displacement, "Whole-tape calibration transport.")
        bin_comparison.append({"bin": j, "old": a, "rounded": b})

    # A common outcome-dependent cost leaves action comparison unchanged, while
    # adding its whole forecast error to the absolute reported action loss.
    common_cost = []
    for p in (F(1, 8), F(1, 2), F(7, 8)):
        for y in (0, 1):
            for magnitude in (F(-1000), F(0), F(1000000)):
                original = ((F(0), F(2)), (F(3), F(0)))
                changed = tuple((a, b + magnitude) for a, b in original)
                expected = tuple(a + (b - a) * p for a, b in original)
                revised_expected = tuple(a + (b - a) * p for a, b in changed)
                check(revised_expected[1] - revised_expected[0] == expected[1] - expected[0],
                      "Common outcome cost cancels forecast decision difference.")
                check(changed[1][y] - changed[0][y] == original[1][y] - original[0][y],
                      "Common outcome cost cancels actual decision difference.")
                for action in (0, 1):
                    delta = (revised_expected[action] - changed[action][y]) - (expected[action] - original[action][y])
                    check(delta == magnitude * (p - y), "Absolute forecast error changes at full common scale.")
                common_cost.append({"p": p, "y": y, "common_slope": magnitude,
                                    "absolute_error_change": magnitude * (p - y)})

    return {"status": "PASS", "checks": count, "local_tent_cases": cases,
            "mean_counterexample": {"contexts": contexts, "labels": labels, "sampled_reports": sampled,
                "mean_reports": means, "original_residuals": original_residuals,
                "mean_residuals": mean_residuals, "original_average_brier": old_loss,
                "mean_average_brier": mean_loss},
            "rounding_tape": tape, "weighted_displacement": displacement,
            "rounding_bins": bin_comparison, "common_cost_cases": common_cost,
            "scope": "Exact finite witnesses and probes of separately proved CF-8/CF-9; development only."}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError("Preserve prior result; choose an explicitly new development output.")
    start_utc = datetime.now(timezone.utc).isoformat()
    start = time.monotonic_ns()
    result = {"status": "FAIL"}
    try:
        result = run()
    except Exception as exc:
        result["failure"] = {"type": type(exc).__name__, "message": str(exc)}
        raise
    finally:
        result.update(start_utc=start_utc, end_utc=datetime.now(timezone.utc).isoformat(),
                      execution_ns=time.monotonic_ns() - start, python=platform.python_version(),
                      source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      contributor="ChatGPT (GPT-6 Astra Pro)", research_time_credit_ns=0,
                      final_evaluation=False)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(encoded(result), indent=2) + "\n")
    print(json.dumps({"status": result["status"], "checks": result["checks"],
                      "output": str(args.output)}))


if __name__ == "__main__":
    main()
