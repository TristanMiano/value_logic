"""Prospectively planned R-P3-B-A DEVELOPMENT comparison; not final evaluation.

ChatGPT (GPT-6 Astra Pro), 2026-10-09 UTC. Separate implementation assignment;
zero principal clock credit. The fixed public affine tape computes no answers.
Every learner execute() finishes and its public transcript is saved before a
separate evaluator computes unpurchased labels. Full controls are fresh cold
deployments with independently charged source closures and construction.

Seeded traces are reproducible illustrations. Conditional action expectations
integrate action bits for the realized selector path; they do not integrate
selector uncertainty or establish the randomized theorem from sample means.
All source/plan hashes, completed arms, actual invoices and failures are saved.
Outputs are refused if already present; there is no implicit retry or tuning.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import signal
import sys
import time
import traceback


HERE = Path(__file__).resolve().parent
CONTROLLER_PATH = HERE / "07_selective_feedback.py"
SPEC = importlib.util.spec_from_file_location("_r_p3ba_development_controller", CONTROLLER_PATH)
assert SPEC is not None and SPEC.loader is not None
C = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = C
SPEC.loader.exec_module(C)
S = C.S  # exact-class identity: never import a second service adapter here

VERSION = "r-p3ba-selective-development-v1"
EXPECTED_CONTROLLER_VERSION = "r-p3-b-a-blocked-prod-v1.1"
EXPECTED_SERVICE_VERSION = "r-p3ba-euler-services-v1.2"
UNIT_PRICE = F(1, 1000)
TASK_PRICES = (1, 100)


def utc():
    return datetime.now(timezone.utc).isoformat()


def write(path, value):
    temporary = path.with_name(path.name + ".writing")
    temporary.write_text(json.dumps(value, indent=2, default=str) + "\n")
    temporary.replace(path)


def jsonl(path, rows):
    with path.open("x") as stream:
        for row in rows:
            stream.write(json.dumps(row, separators=(",", ":"), default=str) + "\n")
        stream.flush()


def digest_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_paths():
    return (CONTROLLER_PATH, HERE / "07_selective_feedback_service.py", S.ADAPTER_PATH,
            Path(__file__).resolve())


def hashes(paths):
    return {str(path): digest_file(path) for path in paths}


def check_sources(expected):
    for path, digest in expected.items():
        if digest_file(Path(path)) != digest:
            raise RuntimeError("Source or plan changed during the declared batch: " + path)


def validate_plan(plan):
    if plan["stage"] != "DEVELOPMENT" or plan["saved_before_planned_runs"] is not True:
        raise ValueError("A prospective development run plan is required.")
    if plan["tape"]["horizons"] != [992, 3968]:
        raise ValueError("Unexpected planned horizons.")
    if plan["tape"]["index_at_t"] != "(73*t+19) mod 248, with t starting at zero":
        raise ValueError("Unexpected public input generator.")
    main = plan["main_arms"]
    if (main["block_sizes"] != [2, 4, 8, 16] or main["state_bits"] != [None, 16]
            or main["action_bits"] != 16 or main["seed"] != 307201
            or tuple(main["experts"]) != S.EXPERT_NAMES):
        raise ValueError("Unexpected main-arm contract.")
    variation = plan["variation_arms"]
    if (variation["horizon"] != 992 or variation["block_size"] != 8
            or variation["state_bits"] != [None, 16]
            or variation["additional_seeds"] != [307203, 307207]):
        raise ValueError("Unexpected variation-arm contract.")
    if C.VERSION != EXPECTED_CONTROLLER_VERSION or S.VERSION != EXPECTED_SERVICE_VERSION:
        raise ValueError("Source versions changed before execution.")


def arm_definitions(plan):
    arms = []
    for horizon in plan["tape"]["horizons"]:
        for block in plan["main_arms"]["block_sizes"]:
            for state in plan["main_arms"]["state_bits"]:
                arms.append(("main", horizon, block, state, plan["main_arms"]["seed"]))
    variation = plan["variation_arms"]
    for seed in variation["additional_seeds"]:
        for state in variation["state_bits"]:
            arms.append(("variation", variation["horizon"], variation["block_size"], state, seed))
    assert len(arms) == 20 and sum(a[0] == "main" for a in arms) == 16
    return arms


def arm_name(kind, horizon, block, state, seed):
    return f"{kind}_T{horizon}_B{block}_state{'exact' if state is None else state}_seed{seed}"


def public_tape(horizon, identity):
    population = tuple((p, a) for p in S.PRIMES for a in range(1, p))
    tape = tuple(S.make_query(*population[(73 * t + 19) % S.POPULATION_SIZE],
                              f"{identity}:{t:04d}") for t in range(horizon))
    counts = Counter(q.claim_key for q in tape)
    if len(counts) != 248 or set(counts.values()) != {horizon // 248}:
        raise AssertionError("The answer-free affine tape does not cover whole domain cycles.")
    return tape


def query_record(query):
    return {"query_id": query.query_id, "a": query.a, "n": query.n, "m": query.m,
            "r": query.r, "source_version": query.source_version,
            "semantics_version": query.semantics_version, "claim_key": list(query.claim_key)}


def public_closed_record(closed):
    issue = closed.issue
    row = {"index": issue.index, "block": issue.block, "query": query_record(issue.query),
           "expert_actions": list(issue.expert_actions),
           "issued_dyadic_probability": {"numerator": issue.numerator, "denominator": issue.denominator},
           "prospective_action": issue.prospective_action, "purchased": closed.purchased,
           "terminal_action": closed.terminal_action}
    if closed.purchased:
        row["purchased_label"] = closed.purchased_label
    return row


def add_resource(records, component):
    meter = C.CostMeter()
    for record in records:
        meter.absorb(record, component)
    return meter.snapshot()


def invoice_sum_check(invoice):
    if invoice["total"] != sum(invoice["by_category"].values()):
        raise AssertionError("Invoice category totals do not sum.")
    if invoice["total"] != sum(row["units"] for row in invoice["operations"]):
        raise AssertionError("Invoice named operations do not sum.")


def private_labels(tape, directory, closure):
    """Independent repeated-multiplication evaluator, called after closure.

    This is private diagnostic computation. Its invoice covers its supplied
    source registry, one-word truth arithmetic and label retention; report
    serialization and later rational-bound algebra are external analysis.
    """
    started = time.perf_counter_ns()
    registry = S.registry_setup(tuple(closure))
    meter = C.CostMeter()
    meter.absorb(registry.resources, "private_evaluator_setup")
    labels, rows = [], []
    try:
        for index, query in enumerate(tape):
            meter.pay_many((("admission", "private_evaluator_public_scalar_read", 4),
                            ("solve", "private_evaluator_initial_modular_reduce", 2),
                            ("storage", "private_evaluator_initial_state_word_write", 3)))
            residue, base, cursor = 1 % query.m, query.a % query.m, 0
            while True:
                meter.pay("solve", "private_evaluator_loop_bound_compare", 1)
                if cursor == query.n:
                    break
                meter.pay_many((("solve", "private_evaluator_modular_multiply", 1),
                                ("solve", "private_evaluator_modular_reduce", 1),
                                ("storage", "private_evaluator_residue_word_write", 1),
                                ("solve", "private_evaluator_cursor_increment", 1),
                                ("storage", "private_evaluator_cursor_word_write", 1)))
                residue = (residue * base) % query.m
                cursor += 1
            meter.pay_many((("solve", "private_evaluator_target_comparison", 1),
                            ("storage", "private_evaluator_label_word_retention", 1)))
            label = int(residue == query.r)
            labels.append(label)
            rows.append({"index": index, "query_id": query.query_id, "private_label": label,
                         "private_residue": residue})
    except Exception as error:
        write(directory / "private_evaluator_failure_invoice.json", meter.snapshot())
        raise error
    invoice = meter.snapshot()
    invoice_sum_check(invoice)
    jsonl(directory / "private_evaluator_labels.jsonl", rows)
    write(directory / "private_evaluator_invoice.json", invoice)
    write(directory / "private_evaluator_scope.json", {
        "algorithm": "Repeated modular multiplication, separate from the bought binary producer/checker.",
        "called_only_after_learner_or_control_closed": True,
        "label_calls": len(labels), "source_registry": registry.record(),
        "elapsed_runtime_ns": time.perf_counter_ns() - started,
        "billing_boundary": "Private truth computation and label retention are priced separately from deployment. JSON serialization and subsequent Fraction-based report algebra are external analysis.",
    })
    return tuple(labels)


def log_upper(n, terms=32):
    """Rational upper enclosure from the positive atanh power series.

    z=(n-1)/(n+1); log(n)=2 sum_{j>=0} z^(2j+1)/(2j+1).
    The omitted tail after `terms` terms is at most
    2*z^(2*terms+1)/((2*terms+1)*(1-z*z)).
    """
    if n == 1:
        return F(0), F(0)
    z = F(n - 1, n + 1)
    lower = 2 * sum((z ** (2 * j + 1) / (2 * j + 1) for j in range(terms)), F(0))
    tail = 2 * z ** (2 * terms + 1) / ((2 * terms + 1) * (1 - z * z))
    return lower, lower + tail


def theorem_bounds(contract, best_loss):
    t, b, m, k = contract.horizon, contract.block_size, contract.quota, contract.k
    low, high = log_upper(contract.expert_count)
    alpha = F(b - 1, b) * (1 + F(1, k))
    action_state = F(0) if contract.state_bits is None else F((b - 1) * m * k, (1 << contract.state_bits) - 1)
    brier_state = F(0) if contract.state_bits is None else F(b * m * k, (1 << contract.state_bits) - 1)
    action_rounding = F(t - m, 1 << contract.action_bits)
    brier_rounding = F(2 * t, 1 << contract.action_bits)
    action = alpha * best_loss + (b - 1) * k * high + action_state + action_rounding
    brier = (1 + F(1, k)) * best_loss + b * k * high + brier_state + brier_rounding
    return {
        "kind": "Unconditional expectation bounds over independent fair selectors/action bits on the fixed tape; not per-seed acceptance tests.",
        "log_N_lower": low, "log_N_upper": high,
        "log_enclosure": "32 positive atanh-series terms plus explicit geometric upper tail; Fraction arithmetic.",
        "alpha": alpha, "best_fixed_all_issued_loss": best_loss,
        "action_state_allowance": action_state, "action_rounding_allowance": action_rounding,
        "brier_state_allowance": brier_state, "brier_rounding_allowance": brier_rounding,
        "terminal_expectation_upper_raw": action,
        "terminal_expectation_upper_clipped": min(F(t - m), action),
        "brier_expectation_upper_raw": brier,
        "brier_expectation_upper_clipped": min(F(t), brier),
    }


def priced(loss, units, task_price):
    return F(task_price) * loss + UNIT_PRICE * units


def evaluate_learner(run, contract, labels, directory):
    denominator = 1 << contract.action_bits
    prospective = terminal = conditional_prospective_numerator = conditional_terminal_numerator = brier_numerator = 0
    expert_losses = [0] * len(S.EXPERT_NAMES)
    corrected_losses = [0] * len(S.EXPERT_NAMES)
    annotations, selector_positions = [], []
    per_block_purchases = Counter()
    for closed, y in zip(run["transcript"], labels):
        issue = closed.issue
        if issue.denominator != denominator:
            raise AssertionError("Issued scalar denominator changed within the declared arm.")
        if closed.purchased:
            if closed.purchased_label != y or closed.terminal_action != y:
                raise AssertionError("Purchased receipt disagrees with independent private evaluator.")
            per_block_purchases[issue.block] += 1
            selector_positions.append(issue.index % contract.block_size)
        elif closed.purchased_label is not None:
            raise AssertionError("Unpurchased learner row contains a label.")
        prospective_error = int(issue.prospective_action != y)
        terminal_error = int(closed.terminal_action != y)
        expected_numerator = issue.numerator if y == 0 else denominator - issue.numerator
        prospective += prospective_error
        terminal += terminal_error
        conditional_prospective_numerator += expected_numerator
        if not closed.purchased:
            conditional_terminal_numerator += expected_numerator
        brier_piece = (issue.numerator - denominator * y) ** 2
        brier_numerator += brier_piece
        losses = [int(action != y) for action in issue.expert_actions]
        for i, loss in enumerate(losses):
            expert_losses[i] += loss
            if not closed.purchased:
                corrected_losses[i] += loss
        annotations.append({"index": issue.index, "query_id": issue.query.query_id,
                            "private_label": y, "prospective_error": prospective_error,
                            "terminal_error": terminal_error,
                            "conditional_prospective_error": str(F(expected_numerator, denominator)),
                            "conditional_terminal_error": str(F(0) if closed.purchased else F(expected_numerator, denominator)),
                            "issued_brier": str(F(brier_piece, denominator ** 2)),
                            "expert_errors": losses,
                            "visibility": "Postclosed evaluator annotation; unavailable to learner issue/update."})
    if set(per_block_purchases) != set(range(contract.quota)) or set(per_block_purchases.values()) != {1}:
        raise AssertionError("The successful arm does not have exactly one purchase in each block.")
    if run["learner"]["random_bits_consumed"] != contract.random_bits:
        raise AssertionError("Random bit use differs from the admitted finite contract.")
    if run["learner"]["peak_weight_bits"] > contract.individual_weight_bits:
        raise AssertionError("Retained weight size exceeds the admitted bound.")
    if run["learner"]["peak_prediction_working_bits"] > contract.prediction_working_bits:
        raise AssertionError("Prediction arithmetic exceeds the admitted bound.")
    invoice_sum_check(run["meter"])
    if run["meter"]["reservations"] or run["meter"]["denials"]:
        raise AssertionError("Successful development arm has residual reservations or denied charges.")
    condition_terminal = F(conditional_terminal_numerator, denominator)
    condition_prospective = F(conditional_prospective_numerator, denominator)
    bounds = theorem_bounds(contract, min(expert_losses))
    cold_units = run["meter"]["total"]
    summary = {
        "prospective_sampled_01_loss": prospective,
        "terminal_sampled_01_loss": terminal,
        "conditional_expected_prospective_01_loss": condition_prospective,
        "conditional_expected_terminal_01_loss": condition_terminal,
        "conditional_expectation_scope": "Only action bits averaged for this realized selector/label path; fixed-tape weights do not depend on sampled actions. No selector average or IID confidence statement.",
        "immutable_issued_brier": F(brier_numerator, denominator ** 2),
        "fixed_expert_all_issued_losses": dict(zip(S.EXPERT_NAMES, expert_losses)),
        "fixed_expert_role": "Four fixed-library hindsight diagnostics; no post-hoc best expert is claimed to be a prospectively deployed policy.",
        "same_selector_corrected_expert_losses": dict(zip(S.EXPERT_NAMES, corrected_losses)),
        "corrected_expert_cost_basis": "Counterfactual substitution of each fixed expert's unbought terminal action, retaining the SAME COMPLETE executed learner invoice, selected receipts, internal updates and exogenous tape. Not a separately optimized or deployed control.",
        "theorem_bounds": bounds,
        "price_cases": {},
        "ordinary_blocked_Prod": "Algorithmic equivalence; no duplicate renamed run or superiority claim.",
    }
    for task_price in TASK_PRICES:
        summary["price_cases"][str(task_price)] = {
            "task_price": task_price, "common_primitive_unit_price": UNIT_PRICE,
            "realized_cold_total": priced(terminal, cold_units, task_price),
            "conditional_action_mean_cold_total": priced(condition_terminal, cold_units, task_price),
            "corrected_expert_same_complete_invoice_totals": {
                name: priced(loss, cold_units, task_price)
                for name, loss in zip(S.EXPERT_NAMES, corrected_losses)},
            "probability_boundary": "This conditional action-mean cost uses this path's actual resource invoice. It is not the unconditional expected-cost bound over selectors.",
        }
    jsonl(directory / "postclosed_evaluator_annotations.jsonl", annotations)
    write(directory / "selector_path.json", {"selected_offsets": selector_positions, "blocks": contract.quota})
    return summary


def run_learner(arm, directory, expected, closure):
    kind, horizon, block, state, seed = arm
    name = arm_name(*arm)
    directory.mkdir(exist_ok=False)
    check_sources(expected)
    contract = C.Contract(horizon, block, len(S.EXPERT_NAMES), action_bits=16, state_bits=state)
    tape = public_tape(horizon, name)
    started_ns = time.perf_counter_ns()
    write(directory / "started.json", {"stage": "DEVELOPMENT", "name": name, "started_utc": utc(),
                                        "contract": contract.record(), "seed": seed, "source_plan_hashes": expected})
    registry = S.registry_setup(tuple(closure))
    write(directory / "source_registry.json", registry.record())
    execution_start = time.perf_counter_ns()
    try:
        run = C.execute(tape, contract, seed=seed, setup_resources=registry.resources)
        execution_ns = time.perf_counter_ns() - execution_start
        # Close and save every learner-visible row before opening the private
        # evaluator. Unbought labels have no field in this transcript.
        jsonl(directory / "transcript.jsonl", (public_closed_record(row) for row in run["transcript"]))
        jsonl(directory / "purchase_invoices.jsonl", (receipt.record() for receipt in run["invoices"]))
        write(directory / "deployment_invoice.json", run["meter"])
        write(directory / "learner_state.json", run["learner"])
        write(directory / "closed_before_evaluation.json", {
            "closed_utc": utc(), "rounds": len(run["transcript"]), "purchases": len(run["invoices"]),
            "transcript_sha256": digest_file(directory / "transcript.jsonl"),
            "purchase_invoices_sha256": digest_file(directory / "purchase_invoices.jsonl"),
            "learner_execute_elapsed_runtime_ns": execution_ns,
        })
        check_sources(expected)
        labels = private_labels(tape, directory, source_paths())
        evaluation = evaluate_learner(run, contract, labels, directory)
        purchase_invoice = add_resource((r.resources for r in run["invoices"]), "checked_purchase")
        write(directory / "purchases_aggregate_invoice.json", purchase_invoice)
        registry_units = registry.resources.total
        cold_units = run["meter"]["total"]
        summary = {
            "status": "PASS", "stage": "DEVELOPMENT", "name": name,
            "kind": kind, "horizon": horizon, "block_size": block, "state_bits": state, "seed": seed,
            "contract": contract.record(), "learner": run["learner"],
            "resource_units": {"cold_total": cold_units, "source_registry": registry_units,
                               "ongoing_including_learner_initialization": cold_units - registry_units,
                               "purchased_checked_services": purchase_invoice["total"],
                               "nonpurchase_excluding_registry": cold_units - registry_units - purchase_invoice["total"],
                               "funded_cap": run["funded_cap"]},
            "evaluation": evaluation,
            "execution_elapsed_runtime_ns": execution_ns,
            "arm_elapsed_runtime_ns": time.perf_counter_ns() - started_ns,
            "source_plan_hashes": expected,
            "finished_utc": utc(),
        }
        write(directory / "summary.json", summary)
        return summary
    except BaseException as error:
        failure = {"status": "FAIL", "name": name, "error": repr(error),
                   "traceback": traceback.format_exc(), "finished_utc": utc(),
                   "elapsed_runtime_ns": time.perf_counter_ns() - started_ns,
                   "source_plan_hashes": expected,
                   "reported_partial_meter": getattr(error, "meter", None),
                   "reported_closed_rounds": getattr(error, "rounds_closed", None),
                   "reported_purchases": getattr(error, "purchases", None),
                   "source_registry_already_procured": registry.record(),
                   "disposition": "Preserve completed files and actual reported spending; no retry or inferred unobserved work."}
        write(directory / "failure.json", failure)
        raise


def run_control(name, horizon, directory, expected, closure):
    directory.mkdir(exist_ok=False)
    check_sources(expected)
    started = time.perf_counter_ns()
    write(directory / "started.json", {"stage": "DEVELOPMENT", "name": name, "horizon": horizon,
                                        "started_utc": utc(), "source_plan_hashes": expected})
    tape = public_tape(horizon, f"control_{name}_T{horizon}")
    registry = S.registry_setup(tuple(closure))
    meter = C.CostMeter()
    meter.absorb(registry.resources, "control_registry")
    object_setup = None
    service = None
    try:
        if name == "semantic_cache":
            service = S.ExactCache(capacity=248)
        elif name == "quadratic_residue_table":
            service = S.QuadraticResidueTable()
        if service is not None:
            object_setup = service.setup_resources
            meter.absorb(object_setup, "control_construction")
        rows, actions = [], []
        first_cycle_units = after_first_cycle_units = 0
        for index, query in enumerate(tape):
            if name == "direct_exact":
                receipt = S.direct_exact(query)
            elif name == "checked_always_buy":
                receipt = S.checked_purchase(query)
            else:
                receipt = service.answer(query)
            meter.absorb(receipt.resources, "control_answer")
            rows.append({"index": index, "query": query_record(query), "result": receipt.record()})
            if not receipt.successful or receipt.query_id != query.query_id or receipt.claim_key != query.claim_key:
                raise AssertionError("Control did not complete its bound exact answer.")
            actions.append(receipt.answer)
            if index < 248:
                first_cycle_units += receipt.resources.total
            else:
                after_first_cycle_units += receipt.resources.total
        invoice = meter.snapshot()
        invoice_sum_check(invoice)
        jsonl(directory / "control_transcript_and_invoices.jsonl", rows)
        write(directory / "deployment_invoice.json", invoice)
        write(directory / "source_registry.json", registry.record())
        if object_setup is not None:
            write(directory / "construction_invoice.json", object_setup.record())
        write(directory / "closed_before_evaluation.json", {
            "closed_utc": utc(), "rounds": horizon,
            "transcript_sha256": digest_file(directory / "control_transcript_and_invoices.jsonl"),
        })
        labels = private_labels(tape, directory, source_paths())
        loss = sum(a != y for a, y in zip(actions, labels))
        if loss != 0:
            raise AssertionError("An exact control disagrees with the private evaluator.")
        check_sources(expected)
        construction = 0 if object_setup is None else object_setup.total
        summary = {
            "status": "PASS", "stage": "DEVELOPMENT", "name": name, "horizon": horizon,
            "terminal_01_loss": loss,
            "resource_units": {"cold_total": invoice["total"], "source_registry": registry.resources.total,
                               "construction": construction, "ongoing_calls": invoice["total"] - registry.resources.total - construction,
                               "first_domain_cycle_calls": first_cycle_units, "later_domain_cycle_calls": after_first_cycle_units},
            "price_cases": {str(p): {"task_price": p, "common_primitive_unit_price": UNIT_PRICE,
                                     "cold_total": priced(loss, invoice["total"], p)} for p in TASK_PRICES},
            "cache_scope": "Initially empty 248-key cache; repeats have fresh request IDs." if name == "semantic_cache" else "Not a learned/cache-history policy.",
            "elapsed_runtime_ns": time.perf_counter_ns() - started,
            "source_plan_hashes": expected, "finished_utc": utc(),
        }
        write(directory / "summary.json", summary)
        return summary
    except BaseException as error:
        write(directory / "failure.json", {"status": "FAIL", "error": repr(error),
                                            "traceback": traceback.format_exc(), "meter": meter.snapshot(),
                                            "elapsed_runtime_ns": time.perf_counter_ns() - started,
                                            "source_plan_hashes": expected, "finished_utc": utc(),
                                            "disposition": "Preserve actual debits; no retry."})
        raise


def interrupt_as_exception(signum, frame):
    raise InterruptedError(f"Received signal {signum}; preserving observed completed work.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    plan_path = Path(args.plan).resolve()
    plan = json.loads(plan_path.read_text())
    validate_plan(plan)
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=False)
    (out / "sources").mkdir()
    expected = hashes((*source_paths(), plan_path))
    for path in source_paths():
        (out / "sources" / path.name).write_bytes(path.read_bytes())
    (out / "sources" / "run_plan_v1.json").write_bytes(plan_path.read_bytes())
    write(out / "manifest.json", {
        "stage": "DEVELOPMENT", "version": VERSION,
        "controller_version": C.VERSION, "service_version": S.VERSION,
        "started_utc": utc(), "command": sys.argv, "cwd": str(Path.cwd()),
        "source_plan_hashes": expected,
        "environment": {"python": sys.version, "python_executable": sys.executable,
                        "platform": platform.platform(), "machine": platform.machine()},
        "public_generator": "(73*t+19) mod 248; no answer computation; input supplier common to all methods.",
        "planned_learner_arms": 20, "planned_controls": 8,
        "principal_clock_credit_ns": 0,
        "not_claimed": "No final freeze, IID confidence, new ordinary algorithm, or P3-08 activation.",
    })
    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, interrupt_as_exception)
    learner_results, controls = [], []
    started = time.perf_counter_ns()
    result = {"status": "FAIL"}
    try:
        (out / "learner_arms").mkdir()
        (out / "controls").mkdir()
        for arm in arm_definitions(plan):
            name = arm_name(*arm)
            write(out / "progress.json", {"active": name, "completed_learner_arms": len(learner_results),
                                           "completed_controls": len(controls), "updated_utc": utc()})
            summary = run_learner(arm, out / "learner_arms" / name, expected, source_paths()[:3])
            learner_results.append(summary)
            print(json.dumps({"completed": name, "cold_units": summary["resource_units"]["cold_total"],
                              "terminal_loss": summary["evaluation"]["terminal_sampled_01_loss"]}), flush=True)
        for horizon in plan["tape"]["horizons"]:
            for name in ("direct_exact", "checked_always_buy", "semantic_cache", "quadratic_residue_table"):
                identity = f"{name}_T{horizon}"
                write(out / "progress.json", {"active": identity, "completed_learner_arms": len(learner_results),
                                               "completed_controls": len(controls), "updated_utc": utc()})
                summary = run_control(name, horizon, out / "controls" / identity, expected, source_paths()[1:3])
                controls.append(summary)
                print(json.dumps({"completed": identity, "cold_units": summary["resource_units"]["cold_total"],
                                  "terminal_loss": summary["terminal_01_loss"]}), flush=True)
        check_sources(expected)
        result.update(status="PASS", stage="DEVELOPMENT", version=VERSION,
                      learner_arms=learner_results, controls=controls,
                      source_plan_hashes=expected, principal_clock_credit_ns=0)
    except BaseException as error:
        result.update(error=repr(error), traceback=traceback.format_exc(),
                      completed_learner_arms=learner_results, completed_controls=controls,
                      disposition="Stopped at the first observed failure/interruption. No implicit retry, source change, tuning or inferred missing work.",
                      source_plan_hashes=expected)
    result.update(finished_utc=utc(), elapsed_runtime_ns=time.perf_counter_ns() - started)
    write(out / "result.json", result)
    write(out / "progress.json", {"active": None, "status": result["status"],
                                   "completed_learner_arms": len(learner_results), "completed_controls": len(controls),
                                   "updated_utc": utc()})
    print(json.dumps({"status": result["status"], "learner_arms": len(learner_results),
                      "controls": len(controls), "elapsed_runtime_ns": result["elapsed_runtime_ns"]}), flush=True)
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
