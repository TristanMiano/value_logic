"""Focused final-controller checks against independent arithmetic references.

Only the failed-invoice test replaces a provider call in memory, by calling
the real trusted provider with an explicitly smaller budget. No repository
source is edited. Private pow checks happen in this evaluator after execution.
"""

from fractions import Fraction as F
import hashlib
from itertools import product
import json
from pathlib import Path
import random
import sys
import types

FOLDER = Path(__file__).resolve().parent
ROOT = FOLDER.parents[4]


def load_final():
    source = (FOLDER / "implementation_source_final.py").read_bytes()
    module = types.ModuleType("_independent_final_controller")
    module.__file__ = str(ROOT / "v3/checks/07_selective_feedback.py")
    sys.modules[module.__name__] = module
    exec(compile(source, str(FOLDER / "implementation_source_final.py"), "exec"), module.__dict__)
    return module, hashlib.sha256(source).hexdigest()


def reference_normalization(weights, losses, k):
    mass, n = sum(weights), len(weights)
    factors = tuple(F(w) * (1 - F(ell, k)) for w, ell in zip(weights, losses))
    total = sum(factors)
    shares = tuple((mass - n) * value / total for value in factors)
    rounded = [1 + share.numerator // share.denominator for share in shares]
    remainder = mass - sum(rounded)
    return tuple(value + int(i < remainder) for i, value in enumerate(rounded))


def operation_total(snapshot, prefix):
    return sum(row["units"] for row in snapshot["operations"]
               if row["operation"].startswith(prefix))


def execute_and_reconstruct(M, *, horizon, block, action_bits, state_bits, seed, wide=False):
    contract = M.Contract(horizon, block, 4, action_bits, state_bits)
    tape = tuple(M.S.make_query(17, 1 if wide else (2, 6, 3, 4, 7, 8, 1, 5)[i % 8],
                               "final-proof-" + str(i)) for i in range(horizon))
    run = M.execute(tape, contract, seed=seed)
    transcript = run["transcript"]
    generator = random.Random(seed)
    stream = sum(generator.getrandbits(64) << (64 * i)
                 for i in range((contract.random_bits + 63) // 64))
    bit_position = 0
    weights = (1 if state_bits is None else 1 << state_bits,) * 4
    expected_purchases = []
    for start in range(0, horizon, block):
        selected = (stream >> bit_position) & (block - 1)
        bit_position += contract.selector_bits
        feedback = None
        for offset in range(block):
            row = transcript[start + offset]
            query = tape[start + offset]
            actions = (0, 1, query.a & 1, int(2 * query.a < query.m))
            probability = F(sum(w * a for w, a in zip(weights, actions)), sum(weights))
            scaled = probability * (1 << action_bits)
            numerator = scaled.numerator // scaled.denominator
            draw = (stream >> bit_position) & ((1 << action_bits) - 1)
            bit_position += action_bits
            assert row.issue.index == start + offset
            assert row.issue.expert_actions == actions
            assert (row.issue.numerator, row.issue.denominator) == (numerator, 1 << action_bits)
            assert row.issue.prospective_action == int(draw < numerator)
            assert row.purchased == (offset == selected)
            if row.purchased:
                checked = int(pow(query.a, query.n, query.m) == query.r)
                assert row.purchased_label == checked == row.terminal_action
                feedback = tuple(int(a != checked) for a in actions)
                expected_purchases.append(start + offset)
            else:
                assert row.purchased_label is None
                assert row.terminal_action == row.issue.prospective_action
        assert feedback is not None
        if state_bits is None:
            weights = tuple(w * (contract.k - ell) for w, ell in zip(weights, feedback))
        else:
            weights = reference_normalization(weights, feedback, contract.k)
            assert sum(weights) == 4 * (1 << state_bits)
    record, meter = run["learner"], run["meter"]
    assert tuple(record["final_weights"]) == weights
    assert record["completed"] and record["purchases"] == contract.quota
    assert bit_position == record["random_bits_consumed"] == contract.random_bits
    assert record["peak_weight_bits"] <= contract.individual_weight_bits
    assert record["peak_prediction_working_bits"] <= contract.prediction_working_bits
    assert not meter["reservations"]
    assert meter["total"] == sum(meter["by_category"].values())
    assert meter["total"] == sum(row["units"] for row in meter["operations"])
    service_total = sum(receipt.resources.total for receipt in run["invoices"])
    assert service_total == operation_total(meter, "checked_purchase:")
    generator_total = operation_total(meter, "development_mt_")
    controller_total = meter["total"] - service_total - generator_total
    assert controller_total <= contract.controller_cap(M.S.EXPERT_EVALUATION_CAP)
    assert meter["total"] <= run["funded_cap"]
    if wide:
        assert record["peak_weight_bits"] > 64 and record["peak_prediction_working_bits"] > 128
    return {
        "contract": contract.record(), "seed": seed,
        "private_reference_rounds_checked": horizon,
        "purchase_count": len(expected_purchases),
        "first_purchase_positions": expected_purchases[:8],
        "total_units": meter["total"], "funded_cap": run["funded_cap"],
        "controller_units": controller_total,
        "controller_cap": contract.controller_cap(M.S.EXPERT_EVALUATION_CAP),
        "service_units": service_total, "development_generator_units": generator_total,
        "peak_weight_bits": record["peak_weight_bits"],
        "peak_prediction_working_bits": record["peak_prediction_working_bits"],
        "all_reference_comparisons_pass": True,
    }


def failed_invoice(M):
    contract = M.Contract(8, 4, 4, 16, 16)
    tape = tuple(M.S.make_query(17, 3, "failed-invoice-" + str(i)) for i in range(8))
    original = M.S.checked_purchase
    calls = []

    def limited_provider(query):
        receipt = original(query, limit_total=20)
        calls.append(receipt)
        return receipt

    M.S.checked_purchase = limited_provider
    try:
        M.execute(tape, contract, seed=17)
    except M.Rejected as exc:
        assert len(calls) == 1 and not calls[0].successful
        meter = exc.meter
        paid = operation_total(meter, "checked_purchase:")
        assert paid == calls[0].resources.total > 0
        assert exc.purchases == 0
        assert meter["reservations"] == {"checked_query_quota": M.S.CHECKED_PURCHASE_CAP}
        return {"fixture": "Real trusted checked service called with limit_total=20",
                "exception": type(exc).__name__, "status": calls[0].status,
                "actual_failed_service_units": paid,
                "whole_meter_units_retained": meter["total"],
                "rounds_closed_before_failure": exc.rounds_closed,
                "admitted_labels": exc.purchases,
                "remaining_reservation": meter["reservations"],
                "no_success_result_returned": True}
    finally:
        M.S.checked_purchase = original
    raise AssertionError("Failed receipt was accepted.")


def startup_and_ownership_repairs(M):
    contract = M.Contract(4, 2, 4, 8)
    tape = tuple(M.S.make_query(17, 1, "startup-" + str(i)) for i in range(4))
    original_meter = M.CostMeter
    created = []

    def observed_meter(*args, **kwargs):
        instance = original_meter(*args, **kwargs)
        created.append(instance)
        return instance

    M.CostMeter = observed_meter
    try:
        try:
            M.execute(tape, contract, seed=-1)
        except M.Rejected:
            assert not created
        else:
            raise AssertionError("Bad seed accepted.")
    finally:
        M.CostMeter = original_meter
    foreign = M.CostMeter(100000)
    own = M.CostMeter(100000)
    bits = M.BitTape((0,), contract.random_bits, foreign, provenance="ownership diagnostic")
    try:
        M.FrozenProd(contract, own, bits)
    except M.Rejected:
        assert own.total == 0
    else:
        raise AssertionError("Foreign bit meter accepted.")
    return {"invalid_seed_rejected_before_meter_creation": True,
            "foreign_bit_meter_rejected_before_learner_spending": True}


def compositions(total, count):
    if count == 1:
        yield (total,)
    else:
        for first in range(1, total - count + 2):
            for rest in compositions(total - first, count - 1):
                yield (first,) + rest


def normalization_reference(M):
    groups = []
    for precision, block in ((1, 4), (32, 1024)):
        contract = M.Contract(block, block, 4, 32, precision)
        meter = M.CostMeter()
        bits = M.BitTape((0,) * ((contract.random_bits + 63) // 64), contract.random_bits,
                         meter, provenance="normalization-only diagnostic")
        learner = M.FrozenProd(contract, meter, bits)
        mass = 4 * (1 << precision)
        if precision == 1:
            states = tuple(compositions(mass, 4))
        else:
            states = ((mass // 4,) * 4, (mass - 3, 1, 1, 1),
                      (1, mass - 3, 1, 1),
                      (mass // 2, mass // 4, mass // 8, mass // 8),
                      (mass // 2 - 1, mass // 2 - 1, 1, 1))
        checked = 0
        for weights in states:
            for losses in product((0, 1), repeat=4):
                expected = reference_normalization(weights, losses, contract.k)
                actual = tuple(learner._round_to_fixed_mass(
                    [w * (contract.k - ell) for w, ell in zip(weights, losses)]))
                assert actual == expected
                assert sum(actual) == mass and min(actual) >= 1
                assert max(v.bit_length() for v in actual) <= contract.individual_weight_bits
                checked += 1
        assert learner.peak_prediction_working_bits <= contract.prediction_working_bits
        if precision == 32:
            assert learner.peak_prediction_working_bits > 64
        groups.append({"state_bits": precision, "block": block,
                       "state_loss_pairs": checked,
                       "peak_prediction_bits": learner.peak_prediction_working_bits,
                       "proved_prediction_bits": contract.prediction_working_bits,
                       "exact_fraction_reference_match": True})
    return groups


def main():
    M, digest = load_final()
    report = {
        "schema": "value_logic.selective_feedback.final_controller_probe.v1",
        "controller_sha256": digest,
        "service_sha256": hashlib.sha256(Path(M.S.__file__).read_bytes()).hexdigest(),
        "scope": "Targeted state, arithmetic, bit chronology and spending checks; no final evaluation population.",
        "success_cases": [
            execute_and_reconstruct(M, horizon=32, block=4, action_bits=16, state_bits=None, seed=20261009),
            execute_and_reconstruct(M, horizon=32, block=4, action_bits=16, state_bits=16, seed=20261009),
            execute_and_reconstruct(M, horizon=256, block=2, action_bits=32, state_bits=None, seed=23, wide=True),
        ],
        "failed_invoice": failed_invoice(M),
        "startup_and_ownership": startup_and_ownership_repairs(M),
        "normalization_reference": normalization_reference(M),
        "result": "PASS: every focused comparison and required failure disposition passed.",
    }
    print(json.dumps(report, indent=2) + "\n", end="")


if __name__ == "__main__":
    main()
