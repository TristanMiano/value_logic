"""Targeted diagnostics of the preserved initial controller source.

Runtime-only shims are explicitly labeled; they do not change repository
source or establish that the initial controller integrates successfully.
"""

from dataclasses import replace
import hashlib
import json
from pathlib import Path
import sys
import types


FOLDER = Path(__file__).resolve().parent
ROOT = FOLDER.parents[4]
ORIGINAL_PATH = ROOT / "v3/checks/07_selective_feedback.py"
SOURCE_PATH = FOLDER / "implementation_source_initial.py"


def load_initial():
    source = SOURCE_PATH.read_bytes()
    module = types.ModuleType("_independent_initial_controller")
    # Resolve its actual adapter dependencies exactly as the original would.
    module.__file__ = str(ORIGINAL_PATH)
    sys.modules[module.__name__] = module
    exec(compile(source, str(SOURCE_PATH), "exec"), module.__dict__)
    return module, hashlib.sha256(source).hexdigest()


def main():
    M, source_hash = load_initial()
    source_dependency = Path(M.S.__file__).read_bytes()
    result = {
        "source_sha256": source_hash,
        "service_sha256": hashlib.sha256(source_dependency).hexdigest(),
        "source_policy": "Initial controller unchanged; listed in-memory test shims only.",
    }
    contract = M.Contract(4, 2, 4, 8)
    tape = tuple(M.S.make_query(17, i + 1, "initial-audit-" + str(i))
                 for i in range(4))

    try:
        M.execute(tape, contract, seed=0)
    except Exception as exc:
        result["initial_integrated_execution"] = {
            "exception": type(exc).__name__, "message": str(exc),
            "meter_attached": hasattr(exc, "meter"),
        }
    else:
        result["initial_integrated_execution"] = {"completed": True}

    meter = M.CostMeter(100000)
    bits = M.BitTape((0,), contract.random_bits, meter,
                     provenance="explicit all-zero diagnostic bits")
    learner = M.FrozenProd(contract, meter, bits)
    bits.take(contract.selector_bits)
    issued = learner.issue(tape[0], M.S.expert_predictions(tape[0], meter))
    receipt = M.S.checked_purchase(tape[0])
    meter.absorb(receipt.resources, "diagnostic_purchase")
    before = meter.total
    try:
        learner.close(issued, receipt)
    except Exception as exc:
        result["successful_receipt_status_mismatch"] = {
            "receipt_status": receipt.status,
            "receipt_checked": receipt.checked,
            "exception": type(exc).__name__, "message": str(exc),
            "purchase_invoice_paid": receipt.resources.total,
            "close_rejection_additional_spending": meter.total - before,
            "pending_record_preserved": learner.pending is issued,
            "no_success_claim": not learner.completed,
        }
    else:
        raise AssertionError("Initial status mismatch disappeared from preserved source.")

    # Explicit fixture only: adapt the local receipt's status spelling to the
    # initial controller so subsequent state transitions can be examined.
    bridged_receipt = replace(receipt, status="answered")
    initial_weights = learner.weights
    learner.close(issued, bridged_receipt)
    frozen_after_selected = learner.weights == initial_weights
    second = learner.issue(tape[1], M.S.expert_predictions(tape[1], meter))
    learner.close(second)
    expected = tuple(contract.k - int(a != receipt.answer)
                     for a in issued.expert_actions)
    assert frozen_after_selected and learner.weights == expected
    result["state_chronology_with_status_spelling_fixture"] = {
        "fixture": "dataclasses.replace(receipt, status='answered')",
        "weights_frozen_after_bought_first_round": frozen_after_selected,
        "weights_update_only_after_second_round": learner.weights == expected,
        "feedback_cleared_after_block": learner.feedback is None,
        "rounds_closed": learner.index,
        "purchases": learner.purchase_count,
    }

    foreign_meter = M.CostMeter(100000)
    foreign_bits = M.BitTape((0,), contract.random_bits, foreign_meter,
                             provenance="different-meter ownership diagnostic")
    own_meter = M.CostMeter(100000)
    foreign_learner = M.FrozenProd(contract, own_meter, foreign_bits)
    result["low_level_bit_meter_identity"] = {
        "accepted_different_bit_meter": foreign_learner.bits.meter is not own_meter,
        "execute_uses_shared_meter": True,
    }

    # This isolates startup error handling past the independently identified
    # missing constant. The conservative fixture is not source validation.
    M.S.EXPERT_EVALUATION_CAP = 4096
    original_meter_class = M.CostMeter
    meters = []

    def capture_meter(*args, **kwargs):
        instance = original_meter_class(*args, **kwargs)
        meters.append(instance)
        return instance

    M.CostMeter = capture_meter
    setup = M.S.ResourceRecord(1000, (("storage", 1000),),
                              (("storage", "startup_diagnostic_setup", 1000),))
    try:
        M.execute(tape, contract, seed=-1, setup_resources=setup)
    except Exception as exc:
        result["invalid_seed_after_paid_startup"] = {
            "fixtures": ["service feature cap set to 4096 in memory",
                         "CostMeter constructor observed without changing charges"],
            "exception": type(exc).__name__, "message": str(exc),
            "actual_meter_total": meters[-1].total,
            "exception_has_meter": hasattr(exc, "meter"),
        }
        assert meters[-1].total == 1001 and not hasattr(exc, "meter")
    else:
        raise AssertionError("Invalid seed unexpectedly accepted.")

    cross_contract = M.Contract(2, 2, 4, 32)
    offset = 1 + 32
    transient = ((1 << 64) - 1) << (64 - offset)
    result["sampler_transient_width"] = {
        "contract_prediction_working_bits": cross_contract.working_bits,
        "second_action_offset": offset,
        "cross_word_transient_bits": transient.bit_length(),
        "larger_than_named_working_bits": transient.bit_length() > cross_contract.working_bits,
    }
    result["result"] = "Initial source blocked at service interface; qualified state transitions and spending diagnostics recorded."
    print(json.dumps(result, indent=2) + "\n", end="")


if __name__ == "__main__":
    main()
