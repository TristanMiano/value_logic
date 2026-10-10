"""Independent source-bound P3-08 broker checks. DEVELOPMENT ONLY.

ChatGPT (GPT-6 Astra Pro), same-model nonblind reviewer, no principal clock credit.
Runs against the captured relative source closure, not the changing live files.
All case outcomes, including actual failures, are preserved by the top-level runner.
"""
from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import sys
import traceback

HERE = Path(__file__).resolve().parent
SNAPSHOT = HERE / "source_snapshot"
sys.path.insert(0, str(SNAPSHOT / "v3/experiments"))
import p308_common as M
import p308_broker as B
import p308_cnf as S
C = M.C


def require(test, message):
    if not test:
        raise AssertionError(message)


def catches(kind, call):
    try:
        call()
    except kind as exc:
        return {"type": type(exc).__name__, "message": str(exc)}
    raise AssertionError("Expected rejection did not occur")


def tape(count=8, repeated=True):
    forms = [((),), ((1,),), ((-1,), (1,)), ((-2, 1), (2,))]
    return tuple(S.make_query(f"review-q-{i}", 2,
                             forms[0] if repeated else forms[i % len(forms)])
                 for i in range(count))


def construct(queries=None, *, hard=True, capacity=128, bits_word=0):
    queries = queries or tape(4)
    contract = B.Contract(len(queries), block_size=4, expert_count=6,
                          action_bits=4, state_bits=4, hard_capacity=capacity)
    meter = C.CostMeter(2_000_000)
    words = tuple(bits_word for _ in range((contract.random_bits + 63) // 64))
    bits = C.BitTape(words, contract.random_bits, meter,
                     provenance="deterministic-explicit-review-words")
    broker = B.Broker(S, contract, meter, bits,
                      (S.SEMANTICS_VERSION, S.SOURCE_VERSION, "review-epoch"),
                      hard=hard)
    return broker, meter, queries


def drive(broker, queries):
    for start in range(0, len(queries), broker.contract.block_size):
        broker.begin_block(queries[start:start + broker.contract.block_size])
        for _ in range(broker.contract.block_size):
            broker.close(broker.issue())
    return broker.record()


def numeric_uniform():
    queries = tape(8, repeated=False)
    # Privately choose matching old-service mathematical inputs for a pure
    # numerical equivalence check. This does not score or train a policy run.
    labels = [S.checked_purchase(q, limit_total=S.service_cap(q, "enumeration"),
                                 solver="enumeration").answer for q in queries]
    advice_meter = C.CostMeter()
    advice_rows = [S.expert_predictions(q, advice_meter) for q in queries]
    comparisons = []
    for state in (1, 16):
        old_contract = C.Contract(8, 4, 6, 4, state)
        new_contract = B.Contract(8, 4, 6, 4, state, hard_capacity=2)
        old_meter, new_meter = C.CostMeter(), C.CostMeter()
        old_bits = C.BitTape.seeded(old_contract.random_bits, 308771, old_meter)
        new_bits = C.BitTape.seeded(new_contract.random_bits, 308771, new_meter)
        old = C.FrozenProd(old_contract, old_meter, old_bits)
        new = B.NumericProd(new_contract, new_meter)
        weights = []
        for start in (0, 4):
            selected = old_bits.take(old_contract.selector_bits)
            require(selected == new_bits.take(new_contract.selector_bits), "Selector bits differ")
            for offset in range(4):
                i = start + offset
                q = C.S.make_query(17, 1 if labels[i] else 3, f"old-pair-{i}")
                issued = old.issue(q, advice_rows[i])
                numerator = new.numerator(advice_rows[i])
                action = int(new_bits.take(new_contract.action_bits) < numerator)
                require(numerator == issued.numerator, "Uniform numerator differs")
                require(action == issued.prospective_action, "Uniform base action differs")
                receipt = C.S.checked_purchase(q) if offset == selected else None
                if receipt is not None:
                    require(receipt.answer == labels[i], "Private numerical pairing was incorrect")
                old.close(issued, receipt)
            new.update(advice_rows[start + selected], labels[start + selected])
            require(tuple(old.weights) == tuple(new.weights), "Uniform fixed-mass weights differ")
            weights.append(list(new.weights))
        require(old_bits.position == new_bits.position == new_contract.random_bits,
                "Numerical comparison did not consume identical fixed bits")
        comparisons.append({"state_bits": state, "weights_after_each_block": weights,
                            "bits": new_bits.position})
    return {"cases": comparisons, "selected_labels_from_real_cnf": labels}


def numeric_tickets():
    path = SNAPSHOT / "v3/checks/07_selective_feedback_allocation.py"
    spec = importlib.util.spec_from_file_location("_review_original_allocation", path)
    old_module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = old_module
    spec.loader.exec_module(old_module)
    queries = tape(8, repeated=False)
    meter = C.CostMeter()
    advice_rows = [S.expert_predictions(q, meter) for q in queries]
    labels = [S.checked_purchase(q, limit_total=S.service_cap(q, "enumeration"),
                                 solver="enumeration").answer for q in queries]
    comparisons = []
    for state in (1, 16):
        old_contract = old_module.Contract(8, 4, 6, 4, state)
        old_meter = old_module.C.CostMeter()
        old_bits = old_module.C.BitTape.seeded(old_contract.random_bits, 308772, old_meter)
        old = old_module.AllocatedProd(old_contract, old_meter, old_bits)
        new = B.NumericProd(B.Contract(8, 4, 6, 4, state, selector="tickets"), C.CostMeter())
        weights = []
        for i, multiplicity in enumerate((1, 5, 1, 5)):
            old.feedback = (advice_rows[i], labels[i])
            old.propensity_tickets = multiplicity
            old._end_block()
            new.update(advice_rows[i], labels[i], multiplicity)
            require(tuple(old.weights) == tuple(new.weights), "Ticket normalized weights differ")
            weights.append({"multiplicity": multiplicity, "weights": list(new.weights)})
        comparisons.append({"state_bits": state, "rows": weights})
    return {"cases": comparisons,
            "scope": "Numerical recurrence only; no claim that manual feedback is an executable broker"}


def coupling_and_correction():
    rows = tape(8)
    contract = B.Contract(8, 4, 6, 4, 4)
    runs = {}
    for selector in ("uniform", "tickets"):
        selected_contract = replace(contract, selector=selector)
        base = B.execute(S, rows, selected_contract, seed=308773, hard=False)
        live = B.execute(S, rows, selected_contract, seed=308773, hard=True)
        require(base["status"] == live["status"] == "success", "Coupled execution failed")
        for name in ("weights", "random_bits_consumed", "purchases"):
            require(base[name] == live[name], "Coupled base state differs: " + name)
        require(base["blocks"] == live["blocks"], "Hard state altered selectors or numeric updates")
        for a, b in zip(base["trace"], live["trace"]):
            for name in ("base_q", "base_action", "base_terminal", "selected", "propensity", "advice"):
                require(a[name] == b[name], "Hard state altered a base coordinate: " + name)
        # Independent scoring is invoked only after both transcripts close.
        y = S.checked_purchase(rows[0], limit_total=S.service_cap(rows[0]), solver="dpll").answer
        base_brier = sum((Fraction(*r["base_q"]) - y)**2 for r in live["trace"])
        live_brier = sum((Fraction(*r["emitted_q"]) - y)**2 for r in live["trace"])
        base_errors = sum(r["base_terminal"] != y for r in live["trace"])
        live_errors = sum(r["terminal_action"] != y for r in live["trace"])
        require(live_brier <= base_brier and live_errors <= base_errors, "Pointwise domination failed")
        runs[selector] = {"base_brier": str(base_brier), "live_brier": str(live_brier),
                          "base_errors": base_errors, "live_errors": live_errors,
                          "meter_base": base["meter"]["total"], "meter_live": live["meter"]["total"]}
    broker, meter, rows = construct()
    broker.begin_block(rows)
    first = broker.issue()
    saved_q = (first.base_numerator, first.output_numerator, first.denominator)
    broker.close(first)
    second = broker.issue()
    require(first.hard_status == "unresolved" and second.hard_status == "checked", "U04 status was not updated")
    require(second.output_numerator == 0 and second.base_numerator > 0,
            "A same-block repeated false query was not hardened prospectively")
    require((first.base_numerator, first.output_numerator, first.denominator) == saved_q,
            "An old issued forecast changed")
    catches(Exception, lambda: setattr(first, "output_numerator", 0))
    return {"coupled_runs": runs, "same_block": {"first_q": saved_q,
             "second_base_numerator": second.base_numerator,
             "second_emitted_numerator": second.output_numerator}}


def owned_selector_and_issue():
    broker, meter, rows = construct()
    broker.begin_block(rows)
    require(broker.selected == 0, "Explicit zero ticket did not select position zero")
    before = broker.bits.position
    second = catches(C.Rejected, lambda: broker.begin_block(rows))
    require(broker.bits.position == before, "Repeated begin consumed a new selector")
    issued = broker.issue()
    copy = replace(issued)
    forged = catches(C.Rejected, lambda: broker.close(copy))
    broker.close(issued)
    duplicate = catches(C.Rejected, lambda: broker.close(issued))
    return {"second_begin": second, "forged_issued_object": forged, "duplicate_close": duplicate}


class MutatedProvider:
    def __init__(self, field, value):
        self.field, self.value = field, value

    def __getattr__(self, name):
        return getattr(S, name)

    def checked_purchase(self, query, **kwargs):
        receipt = S.checked_purchase(query, **kwargs)
        value = self.value(receipt) if callable(self.value) else self.value
        return replace(receipt, **{self.field: value})


def receipt_binding():
    mutations = [("query_id", lambda r: r.query_id + "-wrong"),
                 ("claim_key", lambda r: r.claim_key + ("wrong",)),
                 ("provider_version", "old-version"),
                 ("provider", "other-provider"), ("checked", False),
                 ("status", "rejected"), ("answer", 2), ("answer", True)]
    cases = []
    rows, contract = tape(4), B.Contract(4, 4, 6, 4, 4)
    for field, value in mutations:
        result = B.execute(MutatedProvider(field, value), rows, contract, seed=308774)
        require(result["status"] == "failed" and not result["expectation_theorem_eligible"],
                "Bad owned receipt was accepted: " + field)
        require(result["meter"]["total"] > 0 and len(result["invoices"]) == 1,
                "Bad-receipt work was erased: " + field)
        require(result["hard_state"]["active_entries"] == 0, "Bad receipt altered hard state")
        cases.append({"field": field, "detail": result["failure_detail"],
                      "actual_total": result["meter"]["total"],
                      "child_total": result["invoices"][0]["resources"]["total"]})
    return {"cases": cases,
            "trust_scope": "Provider facade mutates only the checked response boundary; no external authentication claim"}


def failures_and_funding():
    rows, contract = tape(8), B.Contract(8, 4, 6, 4, 4)
    cases = []
    for selector in ("uniform", "tickets"):
        selected_contract = replace(contract, selector=selector)
        cap = B.funded_cap(S, rows, selected_contract)
        full = B.execute(S, rows, selected_contract, seed=308775, unit_limit=cap)
        require(full["status"] == "success" and full["all_path_funded"], "Exact funded cap failed")
        actual = full["meter"]["total"]
        require(actual < cap, "Cap unexpectedly below actual realization")
        small = B.execute(S, rows, selected_contract, seed=308775, unit_limit=actual)
        require(small["status"] == "success", "Exactly actual paid realization did not finish")
        require(not small["all_path_funded"] and not small["expectation_theorem_eligible"],
                "A merely completed realization was certified as all-path funded")
        cases.append({"selector": selector, "funded_cap": cap, "actual_total": actual,
                      "small_success": small["status"], "small_theorem": small["expectation_theorem_eligible"]})
    denied = B.execute(S, rows, contract, seed=308775, provider_limit=0)
    require(denied["status"] == "failed" and len(denied["invoices"]) == 1,
            "Provider failure did not preserve its failure receipt")
    require(not denied["expectation_theorem_eligible"] and denied["purchases"] == 0,
            "Failed receipt entered selected feedback")
    capacity = B.execute(S, rows, replace(contract, hard_capacity=0), seed=308775)
    require(capacity["status"] == "failed" and capacity["purchases"] == 1,
            "Hard capacity failure did not distinguish acquired receipt")
    require(capacity["hard_state"]["entries_retained"] == 0 and capacity["invoices"][0]["resources"]["total"] > 0,
            "Capacity denial published a hard answer or erased its purchase")
    return {"funding": cases, "provider_zero_budget": denied,
            "hard_capacity_zero": capacity}


def stale_generation():
    broker, meter, rows = construct()
    drive(broker, rows)
    require(broker.hard.lookup(rows[0])["status"] == "checked", "No hard answer to withdraw")
    old_scope = broker.scope
    broker.withdraw(old_scope)
    require(broker.hard.lookup(rows[0])["status"] == "stale", "Same-token withdrawal revived old warrant")
    broker.hard.invalidate((S.SEMANTICS_VERSION, S.SOURCE_VERSION, "other-epoch"))
    broker.hard.invalidate(old_scope)
    require(broker.hard.lookup(rows[0])["status"] == "stale", "Returning to a scope revived historical evidence")
    require(broker.record()["status"] == "failed", "Withdrawn broker is still successful")
    return {"hard_state": broker.hard.record(), "lookup": broker.hard.lookup(rows[0])}


def withdrawal_when_unfunded():
    broker, meter, rows = construct()
    drive(broker, rows)
    # A legitimate final resource debit exhausts the shared budget; no internal
    # counter or resource limit is edited to manufacture the case.
    meter.pay("controller", "review_consume_remaining_budget", meter.limit_total - meter.total)
    rejection = catches(C.BudgetExceeded,
                        lambda: broker.withdraw((S.SEMANTICS_VERSION, S.SOURCE_VERSION, "withdrawn")))
    state = broker.record()
    observed = {"withdrawal_exception": rejection, "result": state,
                "actual_total": meter.total}
    (HERE / "unfunded_withdrawal_observed.json").write_text(json.dumps(observed, indent=2) + "\n")
    require(state["status"] == "failed" and not state["successful_quota_contract"],
            "Denied withdrawal left an active successful broker and old hard warrants")
    return observed


def malformed_solver_typed_failure():
    result = B.execute(S, tape(4), B.Contract(4, 4, 6, 4, 4),
                       seed=308775, purchase_solver="unknown")
    require(result["status"] == "failed" and result["meter"]["total"] > 0,
            "Unknown solver has no typed failure and spent-resource record")
    return result


def malformed_query_typed_failure():
    result = B.execute(S, (object(),) * 4, B.Contract(4, 4, 6, 4, 4), seed=308775)
    require(result["status"] == "failed" and result["meter"]["total"] > 0,
            "Malformed first query has no typed failure record")
    return result


def state_none_admission():
    rejected = catches(C.Rejected, lambda: B.Contract(4, 4, 6, 4, None))
    return {"rejection": rejected}


def scope_type_admission():
    result = B.execute(S, tape(4), B.Contract(4, 4, 6, 4, 4),
                       seed=308775, scope_epoch=[])
    require(result["status"] == "failed" and result["meter"]["total"] > 0,
            "Unbounded/nonhashable epoch was not rejected at admission")
    return result


def history_detachment():
    broker, meter, rows = construct()
    broker.begin_block(rows)
    row = broker.close(broker.issue())
    saved = broker.record()
    original_length = len(saved["trace"])
    broker.close(broker.issue())
    details = {"saved_length_before": original_length, "saved_length_after": len(saved["trace"]),
               "saved_trace_is_live_list": saved["trace"] is broker.trace,
               "returned_row_is_live_record": row is broker.trace[0]}
    (HERE / "history_alias_observed.json").write_text(json.dumps(details, indent=2) + "\n")
    require(len(saved["trace"]) == original_length and saved["trace"] is not broker.trace,
            "An earlier record changed when normal subsequent execution appended a round")
    return details


def completed_block_boundary():
    broker, meter, rows = construct()
    drive(broker, rows)
    paid_before = meter.total
    denied = catches(C.Rejected, lambda: broker.begin_block(rows))
    details = {"rejection": denied, "extra_spent": meter.total - paid_before,
               "advice_block_left_open": broker.advice_block is not None,
               "record_status": broker.record()["status"]}
    (HERE / "post_completion_begin_observed.json").write_text(json.dumps(details, indent=2) + "\n")
    require(broker.advice_block is None,
            "Post-completion begin mutated a new prepared block before exhausting finite bits")
    return details


def maximal_public_shape():
    # A finite maximum-shape query that is immediately SAT avoids a large
    # proof search while checking the public-advice/cap accounting boundary.
    query = S.make_query("maximum-shape", 12, [(-4, -3, -2, -1)] * 64)
    meter = C.CostMeter()
    advice = S.expert_predictions(query, meter)
    require(meter.total <= S.EXPERT_CAP, "Declared expert cap is below admitted shape's invoice")
    queries = tuple(replace(query, query_id=f"max-{i}") for i in range(4))
    contract = B.Contract(4, 4, 6, 32, 32, selector="tickets")
    cap = B.funded_cap(S, queries, contract)
    result = B.execute(S, queries, contract, seed=308776, unit_limit=cap)
    require(result["status"] == "success" and result["meter"]["total"] <= cap,
            "Maximum public shape/precision exceeded funded cap")
    return {"key_words": query.key_words, "expert_actual": meter.total,
            "expert_cap": S.EXPERT_CAP, "advice": advice,
            "funded_cap": cap, "actual": result["meter"]["total"],
            "peak_numeric_bits": result["peak_numeric_bits"]}


CASES = [numeric_uniform, numeric_tickets, coupling_and_correction,
         owned_selector_and_issue, receipt_binding, failures_and_funding,
         stale_generation, withdrawal_when_unfunded,
         malformed_solver_typed_failure, malformed_query_typed_failure,
         state_none_admission, scope_type_admission, history_detachment,
         completed_block_boundary, maximal_public_shape]


def main():
    results = []
    started = datetime.now(timezone.utc).isoformat()
    for case in CASES:
        try:
            detail = case()
            result = {"case": case.__name__, "status": "PASS", "detail": detail}
        except Exception as exc:
            result = {"case": case.__name__, "status": "FAIL",
                      "exception": type(exc).__name__, "message": str(exc),
                      "traceback": traceback.format_exc()}
        results.append(result)
        print(json.dumps({k: result[k] for k in ("case", "status")}
                         | ({"message": result["message"]} if "message" in result else {})), flush=True)
    output = {"stage": "DEVELOPMENT", "started_utc": started,
              "finished_utc": datetime.now(timezone.utc).isoformat(),
              "source_manifest": "plan.json", "script": "check_broker.py",
              "principal_clock_credit_seconds": 0,
              "passed": sum(r["status"] == "PASS" for r in results),
              "failed": sum(r["status"] == "FAIL" for r in results), "results": results}
    (HERE / "results.json").write_text(json.dumps(output, indent=2) + "\n")


if __name__ == "__main__":
    main()
