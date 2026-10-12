#!/usr/bin/env python3
"""Zero-acquisition replay of the executed complete finite repair service.

DEVELOPMENT. ChatGPT (GPT-6 Astra Pro), 2026-10-12. Rechecks raw evidence and
chronological gates; does not call a provider, audit source or native solver,
and does not enumerate diagnostic optima. Helper time earns no principal credit.
"""
from collections import Counter
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time

import contract_guard as guard
import contract_quote as quotation
import joint_repair as joint
import native_repair as native
import native_stream as stream

HERE = Path(__file__).resolve().parent
source, compiler = quotation.source, quotation.compilation


def no_acquisition(*args, **kwargs):
    raise AssertionError("A zero-acquisition replay attempted a new purchase")


def combined_record(*records):
    result = source.Meter()
    for record in records:
        for entry in record["operations"]:
            result.pay(entry["category"], entry["operation"], entry["units"])
    return result.record()


def check_invoice(record):
    expected = combined_record(record)
    if expected != record:
        raise ValueError("Invoice totals/categories do not reconcile with operation entries")


def direct_bounds(bank, weights, meter):
    """Independent direct objective sums; no production sum-DAG evaluator."""
    def dot(mask):
        if type(mask) is not int or not 0 <= mask < 1 << len(weights):
            raise ValueError("Changed objective mask meaning")
        meter.pay("replay_objective", "mask_weight_products_and_sum", 2*len(weights)+1)
        return sum(w for j,w in enumerate(weights) if mask & (1 << j))
    upper, model, witness_id = min((dot(w["violation_mask"]),w["model"],w["receipt_id"])
                                  for w in bank["witnesses"])
    lower, proof_id = 0, "nonnegative_objective"
    for tree in bank["trees"]:
        value = min(dot(mask) for mask in tree["leaf_masks"])
        if value > lower:
            lower, proof_id = value, tree["receipt_id"]
    if lower > upper:
        raise ValueError("Checked evidence has inconsistent pointwise bounds")
    meter.pay("replay_bound", "selection_and_binding", len(bank["witnesses"])+len(bank["trees"])+6)
    return dict(lower=lower, upper=upper, model=model,
                witness_id=witness_id, proof_id=proof_id)


def reprice(instance, weights):
    result = copy.deepcopy(instance)
    if len(weights) != len(result["soft"]):
        raise ValueError("Changed source/objective indexing")
    for soft,value in zip(result["soft"], weights):
        soft["weight"] = value
    result["objective_max"] = sum(weights)
    result["identity"] = source.digest({k:v for k,v in result.items() if k != "identity"})
    return result


def check_call(call, weighted):
    got = call["checked_call"]
    budget = call["budget"]
    if got["receipt_id"] != source.digest({k:v for k,v in got.items() if k != "receipt_id"}):
        raise ValueError("Changed complete-call receipt bytes")
    if got["source_id"] != source.digest(weighted) or got["budget"] != budget:
        raise ValueError("Foreign source or objective budget")
    quote = quotation.finite_call_quote(weighted)
    if quote != got["quote"]:
        raise ValueError("The recorded complete-operation quote differs")
    raw = got["provider_response"]
    check_invoice(raw["invoice"])
    check_invoice(got["wrapper_invoice"])
    if raw["invoice"]["total"] > quote["provider_units"]:
        raise ValueError("Recorded provider work exceeds the admitted complete cap")
    checker, fees = source.Meter(), source.Meter()
    source.checked_objective(weighted, weighted["public_incumbent"], checker)
    fees.pay("contract_admission", "source_words", quote["admission_units"])
    fees.pay("objective_update", "query_weight_words", quote["objective_update_units"])
    new_witness = new_tree = None
    if raw["status"] == "SAT":
        if raw["proof"] is not None:
            raise ValueError("Malformed positive receipt")
        value = source.checked_objective(weighted, raw["model"], checker)
        if value > budget:
            raise ValueError("Witness violates its query budget")
        new_witness = compiler.compile_witness(weighted, raw["model"], checker)
        if new_witness != got["witness"]:
            raise ValueError("Witness/model/objective projection changed")
        fees.pay("storage", "complete_witness", quote["witness_retention_units"])
    elif raw["status"] == "UNSAT":
        if raw["model"] is not None or got["checked_lower"] != budget+1:
            raise ValueError("Malformed negative receipt")
        source.check_negative(weighted, budget, raw["proof"], checker)
        new_tree = compiler.compile_tree(raw["proof"], checker)
        if new_tree != got["leaf_masks"]:
            raise ValueError("Lower-proof projection changed")
        fees.pay("storage", "complete_negative", 8+source.proof_words(raw["proof"]))
    else:
        raise ValueError("An unresolved attempt cannot enter this completed evidence bank")
    fees.pay("output", "complete_query_response", quote["response_units"])
    expected_wrapper = combined_record(checker.record(), fees.record())
    if expected_wrapper != got["wrapper_invoice"]:
        raise ValueError("Recorded wrapper check/compile/retention invoice differs from replay")
    total = raw["invoice"]["total"]+expected_wrapper["total"]
    if total != got["total_operation_units"] or total > quote["complete_wrapper_units"]:
        raise ValueError("Complete paid wrapper invoice does not match its receipt/ceiling")
    return new_witness, new_tree, checker.record()


def execute():
    output = HERE/"complete_check_results.json"
    if output.exists():
        raise FileExistsError("Preserve completed replay evidence")
    cpu, wall = time.process_time_ns(), time.perf_counter_ns()
    input_path, result_path = HERE/"joint_source.json", HERE/"complete_service_results.json"
    result = json.loads(result_path.read_text())
    data = json.loads(input_path.read_text())
    if result["status"] != "complete":
        raise ValueError("The recorded service did not complete")
    if (result["implementation_sha256"] != native.sha(HERE/"complete_service.py")
            or result["source_sha256"] != native.sha(input_path)
            or result["source_identity"] != data["source_identity"]
            or data["source_identity"] != source.digest({k:v for k,v in data.items() if k != "source_identity"})):
        raise ValueError("Service/source version binding changed")
    # These sentinels make accidental acquisition fail before a new paid call.
    source.budget_provider = no_acquisition
    native.PersistentIHS = no_acquisition
    joint.CostOracle.audit = no_acquisition
    code_admission = guard.admit()
    archive, banks, readmission = stream.admit_existing_cache()
    if native.sha(joint.S05/"maxsat_repair_results.json") != data["logical_archive_sha256"]:
        raise ValueError("Cost manifest logical dependency changed")
    expected_admission = {k:v for k,v in readmission.items() if k != "timing"}
    recorded_admission = {k:v for k,v in result["initial_admission"].items() if k != "timing"}
    if expected_admission != recorded_admission:
        raise ValueError("The initial compact bank lacks the recorded raw admission chain")
    if ({k:v for k,v in code_admission.items() if k != "timing"}
            != {k:v for k,v in result["complete_code_admission"].items() if k != "timing"}):
        raise ValueError("The complete procedure code admission differs")
    meter = source.Meter()
    for path in [input_path,result_path,HERE/"complete_service.py",Path(__file__)]:
        size = path.stat().st_size
        meter.pay("replay_input", "read_words_and_hash_blocks", (size+7)//8+(size+72)//64)
    modes = tuple(tuple(v) for v in data["possible_cost_modes"])
    possible = [tuple(range(len(modes))) for _ in range(data["cohort_size"])]
    receipt_ids, audited_cells = [], set()
    for index,receipt in enumerate(result["audits"]):
        if receipt["receipt_id"] != source.digest({k:v for k,v in receipt.items() if k != "receipt_id"}):
            raise ValueError("Audit receipt bytes changed")
        row,coordinate,value = receipt["row"],receipt["coordinate"],receipt["value"]
        if (receipt["source_id"] != data["source_identity"] or receipt["provider_call"] != index
                or not 0 <= row < len(possible) or coordinate not in (0,1)
                or (row,coordinate) in audited_cells
                or receipt["observation_units"] != 1 or receipt["provider_software_units"] != 4):
            raise ValueError("Audit receipt contract or identity changed")
        # The completed-run checker may inspect the committed finite source.
        # This checks the saved observation; it makes no new oracle call and
        # supplies no unpurchased information to the already finished controller.
        if value != modes[data["hidden_modes"][row]][coordinate]:
            raise ValueError("Audit value disagrees with its committed source")
        possible[row] = tuple(k for k in possible[row] if modes[k][coordinate] == value)
        if not possible[row]:
            raise ValueError("Audit receipts produced an empty source set")
        audited_cells.add((row,coordinate))
        receipt_ids.append(receipt["receipt_id"])
        meter.pay("replay_audit", "source_receipt_and_mode_filter", 16+len(modes))
    if not all(len(v) == 1 for v in possible):
        raise ValueError("Full cost identification was not achieved")
    weights = [sum(modes[ks[0]][j] for ks in possible) for j in range(len(modes[0]))]
    expected_state = dict(source_id=data["source_identity"],representation="joint",
                          cohort_size=data["cohort_size"],possible_modes=[list(v) for v in possible],
                          audit_receipts=receipt_ids)
    if expected_state != result["final_cost_state"]:
        raise ValueError("Saved full-cost state differs from audited identification")
    call_cursor, positive, negative = 0, 0, 0
    call_check_records, final_gates = [], []
    if len(result["requests"]) != len(data["schedule"]):
        raise ValueError("Requested duties were dropped")
    for index,(duty,request) in enumerate(zip(data["schedule"],result["requests"])):
        row,price,tau = duty["row"],duty["price"],duty["tolerance"]
        instance = archive["instances"][row]
        weighted = reprice(instance, weights)
        if (request["request"] != index or request["row"] != row
                or request["logical_source_id"] != instance["identity"]
                or request["cost_source_id"] != data["source_identity"]
                or request["weights"] != weights or request["price"] != price
                or request["tolerance"] != tau):
            raise ValueError("Requested output/source meanings changed")
        before = direct_bounds(banks[row],weights,meter)
        if before != request["before"]:
            raise ValueError("Request used evidence unavailable in its retained bank")
        indices = request["complete_call_indices"]
        if indices != list(range(call_cursor,call_cursor+len(indices))) or len(indices) > 4:
            raise ValueError("Call chronology or complete-call ceiling changed")
        bounds = before
        for call_id in indices:
            call = result["calls"][call_id]
            u,l = min(bounds["upper"],price),min(bounds["lower"],price)
            if (u-l <= tau or call["call"] != call_id or call["request"] != index
                    or call["row"] != row or call["weights"] != weights
                    or call["before"] != bounds or call["budget"] != (u+l)//2):
                raise ValueError("A paid query did not follow its admitted unresolved bracket")
            witness,tree,check_record = check_call(call, weighted)
            call_check_records.append(check_record)
            if witness is not None:
                positive += 1
                if not any(v["model"] == witness["model"] for v in banks[row]["witnesses"]):
                    receipt_id = source.digest(dict(source=weighted["identity"],model=witness["model"],
                                                    violation_mask=witness["violation_mask"]))
                    banks[row]["witnesses"].append(dict(model=witness["model"],violation_mask=witness["violation_mask"],
                                                       receipt_id=receipt_id,purchase=call_id))
            if tree is not None:
                negative += 1
                banks[row]["trees"].append(dict(original_budget=call["budget"],leaf_masks=tree,
                    receipt_id=call["checked_call"]["receipt_id"],dependency=dict(purchase=call_id)))
            bounds = direct_bounds(banks[row],weights,meter)
            if bounds != call["after"] or min(bounds["upper"],price)-min(bounds["lower"],price) > (u-l)//2:
                raise ValueError("Paid evidence did not reconstruct the recorded bound update")
        call_cursor += len(indices)
        if bounds != request["after"]:
            raise ValueError("Final gate bound differs from independently evaluated evidence")
        u,l = min(bounds["upper"],price),min(bounds["lower"],price)
        action = "repair" if bounds["upper"] < price else "replace"
        model = bounds["model"] if action == "repair" else None
        witness_id = bounds["witness_id"] if action == "repair" else None
        if action == "repair" and source.checked_objective(weighted,model,meter) != u:
            raise ValueError("Returned repair does not have its reported feasible cost")
        if (u-l > tau or request["status"] != "checked_action" or request["action"] != action
                or request["model"] != model or request["witness_id"] != witness_id
                or request["proof_id"] != bounds["proof_id"] or request["action_cost"] != u
                or request["regret_bound"] != u-l
                or request["closed_from_cache"] != (min(before["upper"],price)-min(before["lower"],price) <= tau)):
            raise ValueError("Returned action/certificate does not meet the recorded duty")
        final_gates.append(dict(request=index,row=row,action=action,action_cost=u,
                                regret_bound=u-l,tolerance=tau,complete_calls=len(indices)))
    if call_cursor != len(result["calls"]) or banks != result["final_cache"]:
        raise ValueError("Unused calls or ungrounded retained final evidence")
    summary = dict(checked_requests=len(final_gates),cost_observations=len(result["audits"]),
                   complete_branch_calls=len(result["calls"]),new_native_calls=0,
                   cache_hits=sum(r["closed_from_cache"] for r in result["requests"]),
                   summed_action_cost=sum(r["action_cost"] for r in final_gates),
                   largest_certified_regret=max(r["regret_bound"] for r in final_gates))
    if summary != result["summary"] or len(result["audits"]) > 16 or len(result["calls"]) > 64:
        raise ValueError("Summary or planned finite purchase ceiling differs")
    invoice = result["invoice"]
    check_invoice(invoice["controller_and_cost_operations"])
    if (invoice["common_raw_admission_units"] != readmission["total_declared_units"]
            or invoice["complete_code_admission_units"] != code_admission["declared_admission_units"]
            or invoice["complete_call_wrapper_units"] != sum(c["checked_call"]["total_operation_units"] for c in result["calls"])
            or invoice["audit_provider_software_units"] != 4*len(result["audits"])
            or invoice["external_audit_count"] != len(result["audits"])
            or invoice["native_search_units"] != 0):
        raise ValueError("Actual invoice components do not reconcile")
    if result["storage"]["cache_serialized_bytes"] != len(joint.canonical(banks)):
        raise ValueError("Reported retained cache size differs")
    check_result = dict(
        status="PASS",evidence="DEVELOPMENT",contributor="ChatGPT (GPT-6 Astra Pro)",
        created_utc=datetime.now(timezone.utc).isoformat(),implementation_sha256=native.sha(__file__),
        result_sha256=native.sha(result_path),service_sha256=native.sha(HERE/"complete_service.py"),
        source_sha256=native.sha(input_path),
        scope="Raw admission, exact committed cost-audit receipts, new witness/proof checks, chronological independent mask sums, final 16 action gates and arithmetic invoices.",
        original_service_summary=summary,replayed_original_admission=readmission,
        replayed_code_admission=code_admission,replayed_new_witnesses=positive,replayed_new_negative_proofs=negative,
        checked_audit_receipts=len(result["audits"]),checked_final_gates=final_gates,
        new_branch_provider_calls=0,new_native_calls=0,new_external_cost_observations=0,
        diagnostic_optimum_calls=0,
        replay_check_invoice=meter.record(),new_raw_receipt_checker_invoice=combined_record(*call_check_records),
        raw_result_archive_bytes=result_path.stat().st_size,
        retained_cache_bytes=result["storage"]["cache_serialized_bytes"],
        original_named_operation_total=(invoice["common_raw_admission_units"]+invoice["complete_code_admission_units"]
            +invoice["complete_call_wrapper_units"]+invoice["controller_and_cost_operations"]["total"]
            +invoice["audit_provider_software_units"]),
        timing=dict(process_ns=time.process_time_ns()-cpu,wall_ns=time.perf_counter_ns()-wall),
        limitations=["Same-model focused reconstruction, not independent external confirmation",
                     "Provider search operation receipts and timings are retained historical measurements; search is not replayed",
                     "Controller invoice categories reconcile arithmetically; this checker uses separate direct objective sums",
                     "No runtime, monetary efficiency, population cost inference or native-solver comparison is established"],
    )
    output.write_text(json.dumps(check_result,indent=2)+"\n")
    print(json.dumps({k:check_result[k] for k in ["status","replayed_new_witnesses","replayed_new_negative_proofs",
        "checked_audit_receipts","new_branch_provider_calls","new_native_calls","original_named_operation_total"]}))


if __name__ == "__main__":
    execute()
