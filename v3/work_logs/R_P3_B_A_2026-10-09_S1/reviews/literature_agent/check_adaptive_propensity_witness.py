"""Exact finite calculation for a prospectively recorded missing-propensity witness.

This is a pure task-loss calculation. It does not call a mathematical service,
estimate wall-clock costs, edit the stable learner, or earn principal time.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from math import comb
from pathlib import Path
import datetime
import json


HERE = Path(__file__).resolve().parent


def sha_file(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def fraction_record(value: Fraction) -> dict:
    """Record rigorous short bounds and an exact rational digest without huge JSON."""
    scale = 10**12
    floor = value.numerator * scale // value.denominator
    ceiling = -((-value.numerator * scale) // value.denominator)
    sign = b"-" if value.numerator < 0 else b"+"
    magnitude = abs(value.numerator)
    numerator = magnitude.to_bytes(max(1, (magnitude.bit_length() + 7) // 8), "big")
    denominator = value.denominator.to_bytes(
        max(1, (value.denominator.bit_length() + 7) // 8), "big"
    )
    digest = sha256(
        sign + len(numerator).to_bytes(8, "big") + numerator + denominator
    ).hexdigest()
    return {
        "lower_numerator": floor,
        "upper_numerator": ceiling,
        "common_denominator": scale,
        "numerator_bits": magnitude.bit_length(),
        "denominator_bits": value.denominator.bit_length(),
        "exact_fraction_sha256": digest,
        "digest_encoding": "sign byte; unsigned numerator-byte length in 8 big-endian bytes; magnitude in minimal nonempty big-endian bytes; denominator in minimal nonempty big-endian bytes",
    }


def expected_loss(m: int, aware: bool) -> tuple[Fraction, list[dict]]:
    cumulative = Fraction(0)
    checkpoints = []
    for k in range(m):
        mean_a0 = Fraction(0)
        mass = Fraction(0)
        for z in range(k + 1):
            probability = Fraction(comb(k, z) * 5**z * 3 ** (k - z), 8**k)
            if aware:
                # Common denominator 245^k; label-0 loss factor 242/245,
                # label-1 loss factor 210/245 = 6/7.
                w0 = 245**z * 210 ** (k - z)
                w1 = 245 ** (k - z) * 242**z
            else:
                # Common denominator 7^k; loss factor 6/7 at every query.
                w0 = 7**z * 6 ** (k - z)
                w1 = 7 ** (k - z) * 6**z
            mean_a0 += probability * Fraction(w0, w0 + w1)
            mass += probability
        assert mass == 1
        block_loss = Fraction(3, 8) + Fraction(9, 4) * mean_a0
        cumulative += block_loss
        if k in (0, m - 1):
            checkpoints.append(
                {
                    "completed_blocks_before_prediction": k,
                    "mean_action_zero_probability": fraction_record(mean_a0),
                    "expected_terminal_block_loss": fraction_record(block_loss),
                }
            )
    return cumulative, checkpoints


def main() -> None:
    target_path = HERE / "adaptive_propensity_witness_target_v1.json"
    target = json.loads(target_path.read_text())
    assert target["status"] == "PROSPECTIVE_TARGET_BEFORE_PROBE"
    assert (target["B"], target["m"], target["H"], target["K"]) == (4, 64, 7, 7)
    m = target["m"]
    results = {}
    for name, aware in (("naive_unweighted_update", False), ("propensity_aware_update", True)):
        terminal, checkpoints = expected_loss(m, aware)
        regret = terminal - m
        results[name] = {
            "expected_terminal_loss": fraction_record(terminal),
            "expected_regret_to_best_full_tape_expert": fraction_record(regret),
            "exceeds_343_over_10": regret > Fraction(343, 10),
            "regret_is_nonpositive": regret <= 0,
            "checkpoints": checkpoints,
        }
    # exp(7/10) > 1 + 7/10 + (7/10)^2/2 + (7/10)^3/6 > 2,
    # hence ln 2 < 7/10 and 49 ln 2 < 343/10.
    taylor_lower = sum((Fraction(7, 10) ** r) / (1, 1, 2, 6)[r] for r in range(4))
    assert taylor_lower > 2
    result = {
        "schema": "value_logic.r_p3b_a.literature_adaptive_witness_result.v1",
        "recorded_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "task": "R-P3-B-A",
        "research_credit_ns": 0,
        "target_sha256": sha_file(target_path),
        "calculator_sha256": sha_file(Path(__file__)),
        "method": "Exact Fraction sums over binomial sufficient statistic; no Monte Carlo",
        "B": 4,
        "m": m,
        "T": 4 * m,
        "best_expert_full_tape_loss": m,
        "claims": {
            "49_log_2_strict_upper_bound": "343/10",
            "justification": "exp(7/10) > 1+7/10+49/200+343/6000 = 12013/6000 > 2",
            "naive_variant_refutes_claimed_bound": results["naive_unweighted_update"]["exceeds_343_over_10"],
            "aware_variant_satisfies_bound_in_this_witness": results["propensity_aware_update"]["regret_is_nonpositive"],
        },
        "results": results,
        "exclusions": ["No service-cost measurement", "No theorem proof by empirical checking", "No stable-core or planned-experiment mutation"],
    }
    output_path = HERE / "adaptive_propensity_witness_result_v1.json"
    if output_path.exists():
        old = json.loads(output_path.read_text())
        for volatile in ("recorded_utc",):
            old.pop(volatile, None)
            result.pop(volatile, None)
        assert old == result, "Reconstruction changed; preserve old result and investigate."
        print("Verified existing exact witness result.")
    else:
        output_path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "claims": result["claims"],
        "regret_enclosures": {name: data["expected_regret_to_best_full_tape_expert"] for name, data in results.items()},
    }, indent=2))


if __name__ == "__main__":
    main()
