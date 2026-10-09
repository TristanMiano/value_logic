"""Focused independent allocation implementation checks; no policy-source edits.

This is a code/arithmetic diagnostic, not an additional scientific arm. The
private label evaluator is used only after execution to reconstruct the trace.
The only altered provider is the actual trusted provider with a smaller budget.
"""
from dataclasses import fields, is_dataclass
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import random
import sys
import types

FOLDER = Path(__file__).resolve().parent
ROOT = FOLDER.parents[4]
ALLOCATION_SHA = "eaf79ecb0c4b297ffeec3de4026a025fabc23058ec3c119abe5fdd23434da070"
CORE_SHA = "f872ec2eb07df4722720763730932c33055e380f0ab76ddc3c848d79a5e70f48"
SERVICE_SHA = "68c8f04f7d893cb89fb63a29c98dcc71977d06318d9ef74252b4f38569b5ef32"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(snapshot, name, source_name):
    source = (FOLDER / snapshot).read_bytes()
    module = types.ModuleType(name)
    module.__file__ = str(ROOT / "v3/checks" / source_name)
    sys.modules[name] = module
    exec(compile(source, str(FOLDER / snapshot), "exec"), module.__dict__)
    return module


def normalize_reference(weights, losses, gamma):
    mass, n = sum(weights), len(weights)
    values = tuple(F(w) * (1 - gamma * loss) for w, loss in zip(weights, losses))
    shares = tuple((mass - n) * value / sum(values) for value in values)
    result = [1 + value.numerator // value.denominator for value in shares]
    residual = mass - sum(result)
    assert 0 <= residual < n
    return tuple(weight + int(i < residual) for i, weight in enumerate(result))


def actions(query):
    return (0, 1, query.a & 1, int(2 * query.a < query.m))


def operation_total(meter, prefix):
    return sum(row["units"] for row in meter["operations"]
               if row["operation"].startswith(prefix))


def success_reconstruction(A):
    contract = A.Contract(16, 4, 4, 16, 16)
    raw = (1, 2, 3, 16, 2, 16, 1, 6, 3, 2, 1, 16, 2, 6, 4, 8)
    tape = tuple(A.S.make_query(17, a, f"allocation-reference-{i}")
                 for i, a in enumerate(raw))
    seed, events = 17, []
    original_advice, original_purchase = A.S.expert_predictions, A.S.checked_purchase
    original_issue = A.AllocatedProd.issue

    def observed_advice(query, meter):
        events.append(("advice", query.query_id))
        return original_advice(query, meter)

    def observed_issue(self, query, advice):
        events.append(("issue", query.query_id, tuple(self.weights)))
        return original_issue(self, query, advice)

    def observed_purchase(query):
        events.append(("purchase", query.query_id))
        return original_purchase(query)

    A.S.expert_predictions, A.S.checked_purchase = observed_advice, observed_purchase
    A.AllocatedProd.issue = observed_issue
    try:
        run = A.execute(tape, contract, seed=seed)
    finally:
        A.S.expert_predictions, A.S.checked_purchase = original_advice, original_purchase
        A.AllocatedProd.issue = original_issue
    rng = random.Random(seed)
    stream = sum(rng.getrandbits(64) << (64 * i)
                 for i in range((contract.random_bits + 63) // 64))
    position, weights, expected_events = 0, (1 << contract.state_bits,) * 4, []
    selections = []
    for block, start in enumerate(range(0, contract.horizon, contract.block_size)):
        queries = tape[start:start + contract.block_size]
        expected_events.extend(("advice", query.query_id) for query in queries)
        scores = [sum(w * a for w, a in zip(weights, actions(query))) for query in queries]
        scores = [positive * (contract.mass - positive) for positive in scores]
        proxies = [128 if query.a in (1, query.m - 1) else 304 for query in queries]
        favorite = max(range(contract.block_size), key=lambda j: F(scores[j], proxies[j]))
        draw = (stream >> position) & ((1 << contract.selector_bits) - 1)
        position += contract.selector_bits
        selected = draw if draw < contract.block_size else favorite
        tickets = contract.block_size + 1 if selected == favorite else 1
        pi = F(tickets, 2 * contract.block_size)
        gamma = (1 / pi - 1) / (contract.h_bound * contract.k)
        record = run["allocations"][block]
        assert record["favorite"] == favorite and record["selected"] == selected
        assert record["selected_tickets"] == tickets and record["ticket_total"] == 8
        assert record["scores"] == scores and record["cost_proxies"] == proxies
        assert tuple(record["frozen_weights"]) == weights
        feedback = None
        for offset, query in enumerate(queries):
            expected_events.append(("issue", query.query_id, weights))
            row = run["transcript"][start + offset]
            advice = actions(query)
            ideal = F(sum(w * a for w, a in zip(weights, advice)), sum(weights))
            scaled = ideal * (1 << contract.action_bits)
            numerator = scaled.numerator // scaled.denominator
            action_draw = (stream >> position) & ((1 << contract.action_bits) - 1)
            position += contract.action_bits
            assert row.issue.expert_actions == advice
            assert (row.issue.numerator, row.issue.denominator) == (numerator, 1 << contract.action_bits)
            assert row.issue.prospective_action == int(action_draw < numerator)
            assert row.purchased == (offset == selected)
            if row.purchased:
                expected_events.append(("purchase", query.query_id))
                label = int(pow(query.a, query.n, query.m) == query.r)
                assert row.purchased_label == row.terminal_action == label
                feedback = tuple(int(a != label) for a in advice)
            else:
                assert row.purchased_label is None
                assert row.terminal_action == row.issue.prospective_action
        assert feedback is not None
        weights = normalize_reference(weights, feedback, gamma)
        selections.append({"block": block, "favorite": favorite, "selected": selected,
                           "tickets": tickets, "gamma": str(gamma)})
    assert events == expected_events
    learner, meter = run["learner"], run["meter"]
    assert tuple(learner["final_weights"]) == weights
    assert learner["completed"] and learner["purchases"] == contract.quota
    assert position == learner["random_bits_consumed"] == contract.random_bits
    assert learner["peak_weight_bits"] <= contract.individual_weight_bits
    assert learner["peak_prediction_working_bits"] <= contract.prediction_working_bits
    assert learner["peak_buffer_words"] <= contract.buffer_word_cap
    assert not meter["reservations"]
    assert meter["total"] == sum(meter["by_category"].values())
    assert meter["total"] == sum(row["units"] for row in meter["operations"])
    service = sum(receipt.resources.total for receipt in run["invoices"])
    assert service == operation_total(meter, "checked_purchase:")
    generator = operation_total(meter, "development_mt_")
    controller = meter["total"] - service - generator
    assert controller <= contract.controller_cap() and meter["total"] <= run["funded_cap"]
    return {"seed": seed, "contract": contract.record(), "selections": selections,
            "rounds_reconstructed": contract.horizon, "all_reference_comparisons_pass": True,
            "advice_before_selection_and_issue_chronology_pass": True,
            "frozen_weights_on_every_issue_pass": True, "final_weights": list(weights),
            "controller_units": controller, "controller_cap": contract.controller_cap(),
            "service_units": service, "development_generator_units": generator,
            "total_units": meter["total"], "funded_cap": run["funded_cap"],
            "peak_buffer_words": learner["peak_buffer_words"],
            "peak_prediction_working_bits": learner["peak_prediction_working_bits"]}


def low_level_branch(A, *, all_ones, misreport=False):
    contract = A.Contract(4, 4, 4, 8, 16)
    meter = A.C.CostMeter()
    value = (1 << 64) - 1 if all_ones else 0
    bits = A.C.BitTape((value,), contract.random_bits, meter,
                       provenance="explicit branch diagnostic; not a probability experiment")
    learner = A.AllocatedProd(contract, meter, bits)
    queries = tuple(A.S.make_query(17, a, f"ticket-branch-{i}")
                    for i, a in enumerate((2, 6, 1, 3)))
    cached, selected, tickets, record = learner.prepare_block(queries)
    assert record["favorite"] == 2
    assert selected == (2 if all_ones else 0)
    assert tickets == (5 if all_ones else 1)
    actual_gamma = (F(8, tickets) - 1) / 49
    passed_tickets = 1 if misreport else tickets
    used_gamma = (F(8, passed_tickets) - 1) / 49
    old_weights, losses = learner.weights, None
    for offset, (query, advice) in enumerate(cached):
        issued = learner.issue(query, advice)
        receipt = A.S.checked_purchase(query) if offset == selected else None
        if receipt:
            meter.absorb(receipt.resources, "checked_purchase")
            losses = tuple(int(a != receipt.answer) for a in advice)
        learner.close(issued, receipt, tickets=passed_tickets if receipt else None)
    expected = normalize_reference(old_weights, losses, used_gamma)
    correct = normalize_reference(old_weights, losses, actual_gamma)
    assert learner.completed and learner.purchase_count == 1
    assert bits.position == contract.random_bits
    assert learner.weights == expected
    if misreport:
        assert expected != correct
    return {"selector_words": "ones" if all_ones else "zeros", "selected": selected,
            "actual_tickets": tickets, "passed_tickets": passed_tickets,
            "actual_gamma": str(actual_gamma), "used_gamma": str(used_gamma),
            "final_weights": list(learner.weights), "correct_weights": list(correct),
            "exact_reference_match_for_passed_propensity": True,
            "low_level_wrong_valid_ticket_accepted": misreport}


def large_denominator(A):
    contract = A.Contract(1024, 1024, 4, 32, 32)
    meter = A.C.CostMeter()
    bits = A.C.BitTape((0,) * ((contract.random_bits + 63) // 64),
                       contract.random_bits, meter, provenance="valid-state arithmetic diagnostic")
    learner = A.AllocatedProd(contract, meter, bits)
    mass = contract.mass
    states = ((mass // 4,) * 4, (mass - 3, 1, 1, 1),
              (mass // 2, mass // 4, mass // 8, mass // 8))
    count = 0
    for weights in states:
        for tickets in (1, 1025):
            gamma = (F(2048, tickets) - 1) / (2047 * 2047)
            advice, label = (0, 1, 0, 1), 1
            losses = tuple(int(a != label) for a in advice)
            learner.weights = weights
            learner.feedback = (advice, label)
            learner.propensity_tickets = tickets
            learner._end_block()
            assert learner.weights == normalize_reference(weights, losses, gamma)
            assert sum(learner.weights) == mass and min(learner.weights) >= 1
            count += 1
    assert contract.maximum_update_denominator < (1 << 64)
    assert 64 < learner.peak_prediction_working_bits <= contract.prediction_working_bits
    return {"scope": "Six valid arithmetic states; not a 1024-round performance run.",
            "comparisons": count, "maximum_denominator": contract.maximum_update_denominator,
            "maximum_denominator_bits": contract.maximum_update_denominator.bit_length(),
            "peak_prediction_working_bits": learner.peak_prediction_working_bits,
            "declared_prediction_working_bits": contract.prediction_working_bits,
            "exact_fraction_reference_match": True}


def failed_invoice(A):
    contract = A.Contract(8, 4, 4, 16, 16)
    tape = tuple(A.S.make_query(17, 3, f"adaptive-failed-invoice-{i}") for i in range(8))
    original, calls = A.S.checked_purchase, []

    def limited(query):
        receipt = original(query, limit_total=20)
        calls.append(receipt)
        return receipt

    A.S.checked_purchase = limited
    try:
        A.execute(tape, contract, seed=17)
    except A.C.Rejected as exc:
        assert len(calls) == 1 and not calls[0].successful
        meter = exc.meter
        paid = operation_total(meter, "checked_purchase:")
        assert paid == calls[0].resources.total > 0 and exc.purchases == 0
        assert meter["reservations"] == {"checked_query_quota": 1088}
        return {"real_provider_limit": 20, "status": calls[0].status,
                "failed_invoice_units_retained": paid, "whole_meter_units_retained": meter["total"],
                "admitted_labels": exc.purchases, "rounds_closed": exc.rounds_closed,
                "remaining_reservation": meter["reservations"], "no_success_returned": True}
    finally:
        A.S.checked_purchase = original
    raise AssertionError("The failed paid receipt was admitted.")


def canonical(value):
    if is_dataclass(value):
        return {field.name: canonical(getattr(value, field.name)) for field in fields(value)}
    if isinstance(value, dict):
        return {key: canonical(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [canonical(item) for item in value]
    if isinstance(value, str):
        return value.replace("r-p3-b-a-blocked-prod-v1.1", "CORE-VERSION").replace(
            "r-p3-b-a-blocked-prod-v1.2", "CORE-VERSION")
    return value


def core_guard_identity():
    old = load("implementation_source_final.py", "_proof_core_11", "07_selective_feedback.py")
    new = load("core_v1_2_source_reviewed.py", "_proof_core_12", "07_selective_feedback.py")
    outputs = []
    zero = []
    for module in (old, new):
        contract = module.Contract(16, 4, 4, 16, 16)
        tape = tuple(module.S.make_query(17, (2, 6, 1, 3)[i % 4], f"core-identity-{i}")
                     for i in range(16))
        outputs.append(canonical(module.execute(tape, contract, seed=23)))
        try:
            module.execute(tape, contract, seed=23, unit_limit=0)
        except module.BudgetExceeded as exc:
            attached = getattr(exc, "meter", None)
            if module is new:
                assert attached is not None and attached["total"] == 0 and attached["denials"] == 1
            else:
                assert attached is None
            zero.append({"version": module.VERSION, "meter_attached": attached is not None,
                         "total": None if attached is None else attached["total"]})
        else:
            raise AssertionError("Zero-funded execution unexpectedly returned.")
    assert outputs[0] == outputs[1]
    digest = hashlib.sha256(json.dumps(outputs[0], sort_keys=True).encode()).hexdigest()
    return {"old_sha256": sha(FOLDER / "implementation_source_final.py"),
            "new_sha256": sha(FOLDER / "core_v1_2_source_reviewed.py"),
            "success_rounds": 16, "seed": 23, "full_output_equal_after_version_normalization": True,
            "normalized_output_sha256": digest, "operational_units": outputs[1]["meter"]["total"],
            "source_registry_setup_included": False,
            "qualification": "Registry bytes differ and must be priced using each actual source; version metadata differs.",
            "zero_funding_guard": zero}


def main():
    assert sha(ROOT / "v3/checks/07_selective_feedback.py") == CORE_SHA
    assert sha(ROOT / "v3/checks/07_selective_feedback_allocation.py") == ALLOCATION_SHA
    A = load("adaptive_allocation_source_initial.py", "_proof_allocated_prod", "07_selective_feedback_allocation.py")
    assert sha(A.S.__file__) == SERVICE_SHA
    report = {"schema": "value_logic.selective_feedback.adaptive_implementation_probe.v1",
              "allocation_sha256": ALLOCATION_SHA, "core_sha256": CORE_SHA,
              "service_sha256": SERVICE_SHA, "principal_time_credit_ns": 0,
              "success_reference": success_reconstruction(A),
              "both_ticket_branches": [low_level_branch(A, all_ones=False),
                                       low_level_branch(A, all_ones=True)],
              "low_level_contract_misuse_diagnostic": low_level_branch(A, all_ones=True, misreport=True),
              "large_denominator": large_denominator(A),
              "failed_invoice": failed_invoice(A),
              "core_v12_guard_identity": core_guard_identity(),
              "result": "PASS for trusted execute; low-level ticket truth is an explicit caller precondition."}
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
