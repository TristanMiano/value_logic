"""Exactly three prospective adaptive R-P3-B-A DEVELOPMENT illustrations.

ChatGPT (GPT-6 Astra Pro), 2026-10-09 UTC. Zero principal-clock credit.
The immutable public affine input tape computes no answers. A learner arm
closes, then its public records and actual invoices are archived and verified
before the separate private evaluator runs. JSONL is streamed directly into
deterministic ZIPs; no large loose raw files are produced. Existing uniform
and exact-control results are read-only, source-bound prior observations.

Conditional action expectations average only action bits for the realized
adaptive selector path. The theorem separately averages selectors, with a
rational log upper enclosure and the admitted 1088-unit purchase cap. No
seed-average proof, accuracy-superiority inference, retuning or retries.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import platform
import signal
import sys
import time
import traceback
import zipfile
import zlib


HERE = Path(__file__).resolve().parent
ALLOCATION_PATH = HERE / "07_selective_feedback_allocation.py"
SPEC = importlib.util.spec_from_file_location("_r_p3ba_allocation_development", ALLOCATION_PATH)
assert SPEC is not None and SPEC.loader is not None
AL = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = AL
SPEC.loader.exec_module(AL)
C, S = AL.C, AL.C.S  # preserve the source-bound exact-class API identities

VERSION = "r-p3ba-allocation-development-v1"
PINNED = {
    "07_selective_feedback_allocation.py": "eaf79ecb0c4b297ffeec3de4026a025fabc23058ec3c119abe5fdd23434da070",
    "07_selective_feedback.py": "f872ec2eb07df4722720763730932c33055e380f0ab76ddc3c848d79a5e70f48",
    "07_selective_feedback_service.py": "68c8f04f7d893cb89fb63a29c98dcc71977d06318d9ef74252b4f38569b5ef32",
    "07_computation_adapter.py": "06324b8b02a8dca3d8fbb423a7adf20708d5cc6cb39c60e60e38e720a7b97615",
}
PLAN_SHA256 = "a7f0675bae1f4f62cc9847ca4f42301029a696e20cf77400bdb45e000bdbfaed"
UNIT_PRICE = F(1, 1000)
TASK_PRICES = (1, 100)
PLANNED_ARMS = (
    {"T": 992, "B": 4, "s": 16, "h": 16, "seed": 307201},
    {"T": 992, "B": 8, "s": 16, "h": 16, "seed": 307201},
    {"T": 3968, "B": 8, "s": 16, "h": 16, "seed": 307201},
)


def utc():
    return datetime.now(timezone.utc).isoformat()


def digest_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    temporary = path.with_name(path.name + ".writing")
    temporary.write_text(json.dumps(value, indent=2, default=str) + "\n")
    temporary.replace(path)


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), default=str) + "\n").encode("utf-8")


def source_paths():
    return (ALLOCATION_PATH, HERE / "07_selective_feedback.py",
            HERE / "07_selective_feedback_service.py", S.ADAPTER_PATH,
            Path(__file__).resolve())


def hashes(paths):
    return {str(path): digest_file(path) for path in paths}


def check_sources(expected):
    for path, digest in expected.items():
        if digest_file(Path(path)) != digest:
            raise RuntimeError("Source, plan or cited evidence changed: " + path)


def validate_plan(plan, plan_path):
    if (digest_file(plan_path) != PLAN_SHA256 or plan["stage"] != "DEVELOPMENT"
            or plan["saved_before_runs"] is not True or plan["no_further_tuning"] is not True
            or tuple(plan["arms"]) != PLANNED_ARMS):
        raise ValueError("Require the exact prospective three-arm allocation plan.")
    if (AL.VERSION != "r-p3-b-a-propensity-allocation-v1"
            or C.VERSION != "r-p3-b-a-blocked-prod-v1.2"
            or S.VERSION != "r-p3ba-euler-services-v1.2"):
        raise ValueError("A source version changed before execution.")
    for name, digest in PINNED.items():
        if digest_file(HERE / name) != digest:
            raise ValueError("A pinned source changed before execution: " + name)


def arm_name(arm):
    return f"adaptive_T{arm['T']}_B{arm['B']}_state{arm['s']}_seed{arm['seed']}"


def public_tape(horizon, identity):
    population = tuple((p, a) for p in S.PRIMES for a in range(1, p))
    tape = tuple(S.make_query(*population[(73 * t + 19) % 248], f"{identity}:{t:04d}")
                 for t in range(horizon))
    counts = Counter(q.claim_key for q in tape)
    if len(counts) != 248 or set(counts.values()) != {horizon // 248}:
        raise AssertionError("The public tape must cover whole affine domain cycles.")
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


def zip_info(name):
    info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info._compresslevel = 9
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    return info


def _build_zip(target, producers, source_hashes, mode):
    entries = []
    with zipfile.ZipFile(target, mode, compression=zipfile.ZIP_DEFLATED,
                         compresslevel=9, allowZip64=True) as archive:
        for name in sorted(producers):
            digest, length, row_count = hashlib.sha256(), 0, 0
            with archive.open(zip_info(name), "w") as stream:
                for row in producers[name]():
                    data = canonical(row)
                    stream.write(data)
                    digest.update(data)
                    length += len(data)
                    row_count += 1
            entries.append({"name": name, "bytes": length, "rows": row_count,
                            "sha256": digest.hexdigest()})
        manifest = {"schema": "value_logic.raw_jsonl_archive.v1", "stage": "DEVELOPMENT",
                    "source_plan_hashes": source_hashes, "entries": entries,
                    "encoding": "Canonical sorted-key UTF-8 JSONL with LF; fixed ZIP metadata; DEFLATE 9."}
        archive.writestr(zip_info("MANIFEST.json"), canonical(manifest))
    return manifest


def verified_zip(path, producers, source_hashes):
    """Stream raw rows to ZIP, compare every decompressed row, rebuild in RAM.

    Producers traverse already completed immutable records; this verification
    performs no query calls, learner execution, random draw or private truth.
    """
    manifest = _build_zip(path, producers, source_hashes, "x")
    expected_names = sorted(producers) + ["MANIFEST.json"]
    with zipfile.ZipFile(path) as archive:
        if archive.namelist() != expected_names or archive.testzip() is not None:
            raise AssertionError("Archive entry order or CRC verification failed.")
        for entry in manifest["entries"]:
            digest, length, row_count = hashlib.sha256(), 0, 0
            with archive.open(entry["name"]) as stream:
                for row in producers[entry["name"]]():
                    expected = canonical(row)
                    actual = stream.readline()
                    if actual != expected:
                        raise AssertionError("Archived bytes differ from completed source record.")
                    digest.update(actual)
                    length += len(actual)
                    row_count += 1
                if stream.read(1):
                    raise AssertionError("Unexpected trailing archived bytes.")
            if (length, row_count, digest.hexdigest()) != (entry["bytes"], entry["rows"], entry["sha256"]):
                raise AssertionError("Raw archive manifest mismatch.")
        if archive.read("MANIFEST.json") != canonical(manifest):
            raise AssertionError("Embedded archive manifest differs from its exact source bytes.")
    duplicate = io.BytesIO()
    duplicate_manifest = _build_zip(duplicate, producers, source_hashes, "w")
    if duplicate_manifest != manifest or duplicate.getvalue() != path.read_bytes():
        raise AssertionError("Two deterministic builds produced different bytes.")
    receipt = {"status": "PASS", "archive": path.name, "archive_bytes": path.stat().st_size,
               "archive_sha256": digest_file(path), "manifest": manifest,
               "verification": "Every decompressed JSONL row byte-for-byte against its completed in-memory record, entry SHA256/length/row count, embedded manifest and CRC; two complete builds byte-identical.",
               "loose_raw_jsonl_written": False}
    write(path.with_name(path.stem + "_manifest.json"), receipt)
    return receipt


def invoice_sum_check(invoice):
    if (invoice["total"] != sum(invoice["by_category"].values())
            or invoice["total"] != sum(row["units"] for row in invoice["operations"])):
        raise AssertionError("Named/category invoice arithmetic is inconsistent.")


def public_protocol_audit(run, contract, tape):
    """Reconstruct issue and update equations using only paid public receipts.

    This external evidence audit is not a second deployed learner/control.
    No private labels, service calls or new selector/action draws occur.
    """
    t, b, n, mass = contract.horizon, contract.block_size, contract.expert_count, contract.mass
    transcript, allocations, receipts = run["transcript"], run["allocations"], run["invoices"]
    if (len(transcript), len(allocations), len(receipts)) != (t, contract.quota, contract.quota):
        raise AssertionError("Incomplete transcript, allocation record or purchase count.")
    weights = [1 << contract.state_bits] * n
    favorite_purchases = 0
    for block, record in enumerate(allocations):
        rows = transcript[block * b:(block + 1) * b]
        if record["block"] != block or record["frozen_weights"] != weights:
            raise AssertionError("Block allocation does not bind its frozen settled history.")
        if min(weights) < 1 or sum(weights) != mass:
            raise AssertionError("Fixed-mass positive representation failed.")
        scores, proxies = [], []
        for offset, row in enumerate(rows):
            issue, query = row.issue, row.issue.query
            index = block * b + offset
            actions = (0, 1, query.a & 1, int(2 * query.a < query.m))
            if issue.index != index or issue.block != block or query != tape[index] or issue.expert_actions != actions:
                raise AssertionError("Issued request or public stateless advice mismatch.")
            positive = sum(w * a for w, a in zip(weights, actions))
            scores.append(positive * (mass - positive))
            proxies.append(AL.PROXY_CHEAP if query.a in (1, query.m - 1) else AL.PROXY_GENERAL)
            if (issue.numerator != (positive << contract.action_bits) // mass
                    or issue.denominator != 1 << contract.action_bits):
                raise AssertionError("Issued forecast did not retain this block's frozen weights.")
            if row.purchased != (offset == record["selected"]):
                raise AssertionError("Selected allocation does not match the purchased round.")
            if not row.purchased and (row.purchased_label is not None or row.terminal_action != issue.prospective_action):
                raise AssertionError("Unpurchased public row contains feedback or changed action.")
        favorite = max(range(b), key=lambda j: F(scores[j], proxies[j]))
        selected = record["selected"]
        tickets = b + 1 if selected == favorite else 1
        if (not 0 <= selected < b or record["scores"] != scores or record["cost_proxies"] != proxies
                or record["favorite"] != favorite or record["selected_tickets"] != tickets
                or record["ticket_total"] != 2 * b):
            raise AssertionError("Public score, favorite or propensity ticket mismatch.")
        favorite_purchases += selected == favorite
        receipt, bought = receipts[block], rows[selected]
        if (receipt.query_id != bought.issue.query.query_id or receipt.claim_key != bought.issue.query.claim_key
                or receipt.status != "success" or receipt.checked is not True
                or receipt.provider != "cold_checked_modular_adapter"
                or receipt.provider_version != S.VERSION + ";adapter=" + S.A.VERSION
                or receipt.answer != bought.purchased_label or receipt.answer != bought.terminal_action):
            raise AssertionError("Checked receipt identity/status/action binding failed.")
        invoice_sum_check(receipt.resources.record())
        if receipt.resources.total > S.CHECKED_PURCHASE_CAP:
            raise AssertionError("Actual checked receipt exceeded the reserved completion cap.")
        numerator = 1 if tickets == 1 else b - 1
        denominator = contract.h_bound if tickets == 1 else contract.maximum_update_denominator
        products = [w * (denominator - numerator * int(action != receipt.answer))
                    for w, action in zip(weights, bought.issue.expert_actions)]
        total = sum(products)
        rounded = [1 + (mass - n) * value // total for value in products]
        residual = mass - sum(rounded)
        if not 0 <= residual < n:
            raise AssertionError("Independent normalization residual is inadmissible.")
        weights = [value + int(i < residual) for i, value in enumerate(rounded)]
    state = run["learner"]
    if (state["final_weights"] != weights or state["completed"] is not True
            or state["rounds_closed"] != t or state["purchases"] != contract.quota
            or state["random_bits_consumed"] != contract.random_bits
            or state["peak_weight_bits"] > contract.individual_weight_bits
            or state["peak_prediction_working_bits"] > contract.prediction_working_bits
            or state["peak_buffer_words"] != max(r["buffer_words"] for r in allocations)
            or state["peak_buffer_words"] > contract.buffer_word_cap):
        raise AssertionError("Terminal state or finite resource capacity did not verify.")
    invoice_sum_check(run["meter"])
    if run["meter"]["reservations"] or run["meter"]["denials"] or run["meter"]["total"] > run["funded_cap"]:
        raise AssertionError("Completed arm has a funding, reservation or denial defect.")
    return {"status": "PASS", "public_rows_checked": t, "blocks_checked": contract.quota,
            "receipt_bindings_checked": len(receipts), "favorite_purchases": favorite_purchases,
            "nonfavorite_purchases": contract.quota - favorite_purchases,
            "selected_propensity_histogram": dict(Counter(str(F(r["selected_tickets"], 2 * b)) for r in allocations)),
            "state_update": "Exact reconstruction of each propensity factor and positive fixed-mass rounding from the selected paid label; current-block forecasts use unchanged weights.",
            "randomness_boundary": "Ticket multiplicity and consumed bit count checked; stored selection draws are not replayed or used to claim statistical randomness.",
            "access_boundary": "Source order plus immutable transcript shows issue before the selected receipt and update at block end; private evaluator has not yet run.",
            "external_audit_not_deployed_policy": True}


def private_labels(tape, directory, closure):
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
    except BaseException:
        write(directory / "private_evaluator_failure_invoice.json", meter.snapshot())
        raise
    invoice_sum_check(meter.snapshot())
    write(directory / "private_evaluator_invoice.json", meter.snapshot())
    write(directory / "private_evaluator_scope.json", {
        "algorithm": "Repeated modular multiplication independent of bought binary production/checking.",
        "called_only_after_public_archive_closed_and_verified": True,
        "source_registry": registry.record(), "label_calls": len(labels),
        "elapsed_runtime_ns": time.perf_counter_ns() - started,
        "billing_boundary": "Private truth arithmetic and label retention, including source registry, priced separately from deployment. ZIP/JSON serialization, public protocol audit and Fraction report algebra are external evidence work.",
    })
    return tuple(labels), tuple(rows)


def log_upper(n, terms=32):
    z = F(n - 1, n + 1)
    lower = 2 * sum((z ** (2 * j + 1) / (2 * j + 1) for j in range(terms)), F(0))
    tail = 2 * z ** (2 * terms + 1) / ((2 * terms + 1) * (1 - z * z))
    return lower, lower + tail


def theorem_bounds(contract, best_loss, registry_units):
    t, m, h, k = contract.horizon, contract.quota, contract.h_bound, contract.k
    low, high = log_upper(contract.expert_count)
    state = F(h * m * k, (1 << contract.state_bits) - 1)
    rounding = F(t - m, 1 << contract.action_bits)
    raw = best_loss + h * k * high + state + rounding
    action = min(F(t - m), raw)
    rng_cap = 1248 + (contract.random_bits + 63) // 64
    resource_cap = registry_units + contract.controller_cap() + rng_cap + m * S.CHECKED_PURCHASE_CAP
    return {
        "kind": "Unconditional expectation over adaptive selectors and action bits under the fixed public tape; not a per-realized-seed requirement.",
        "formula": "min(T-m, L_* + H*K*ln(N) + H*m*K/(2^s-1) + (T-m)/2^h), H=K=2B-1",
        "best_fixed_all_issued_loss": best_loss, "H": h, "K": k,
        "log_N_lower": low, "log_N_upper": high,
        "log_enclosure": "32 positive atanh-series terms plus exact geometric upper-tail enclosure; all arithmetic Fraction.",
        "state_allowance": state, "action_rounding_allowance": rounding,
        "terminal_expectation_upper_raw": raw, "terminal_expectation_upper_clipped": action,
        "brier_scope": "Issued Brier is reported diagnostically. No adaptive Brier theorem is inferred from the uniform selector bound.",
        "all_in_resource_certificate": {
            "kind": "Pathwise admitted cap, hence also an unconditional expectation bound.",
            "source_registry": registry_units, "controller_cap": contract.controller_cap(),
            "random_setup_cap": rng_cap, "purchase_completion_cap_per_call": S.CHECKED_PURCHASE_CAP,
            "purchase_quota_cap": m * S.CHECKED_PURCHASE_CAP, "total": resource_cap,
            "choice": "Use the 1088-unit admitted completion cap, not the realized selector's fee sum or the empirically attained maximum.",
        },
        "all_in_expected_cost_upper": {
            str(price): F(price) * action + UNIT_PRICE * resource_cap for price in TASK_PRICES},
    }


def evaluate(run, contract, labels, registry_units):
    denominator = 1 << contract.action_bits
    prospective = terminal = conditional_prospective = conditional_terminal = brier = 0
    expert_losses, corrected_losses = [0] * len(S.EXPERT_NAMES), [0] * len(S.EXPERT_NAMES)
    annotations = []
    for closed, y in zip(run["transcript"], labels):
        issue = closed.issue
        if closed.purchased and (closed.purchased_label != y or closed.terminal_action != y):
            raise AssertionError("Independent evaluator disagrees with a checked purchased answer.")
        p_error, t_error = int(issue.prospective_action != y), int(closed.terminal_action != y)
        expected_numerator = issue.numerator if y == 0 else denominator - issue.numerator
        prospective += p_error
        terminal += t_error
        conditional_prospective += expected_numerator
        conditional_terminal += 0 if closed.purchased else expected_numerator
        brier_piece = (issue.numerator - denominator * y) ** 2
        brier += brier_piece
        losses = [int(a != y) for a in issue.expert_actions]
        for i, loss in enumerate(losses):
            expert_losses[i] += loss
            corrected_losses[i] += 0 if closed.purchased else loss
        annotations.append({"index": issue.index, "query_id": issue.query.query_id, "private_label": y,
                            "prospective_error": p_error, "terminal_error": t_error,
                            "conditional_prospective_error": F(expected_numerator, denominator),
                            "conditional_terminal_error": F(0) if closed.purchased else F(expected_numerator, denominator),
                            "issued_brier": F(brier_piece, denominator ** 2), "expert_errors": losses,
                            "visibility": "Postclosed evaluator annotation; unavailable to learner issue/allocation/update."})
    action_mean = F(conditional_terminal, denominator)
    units = run["meter"]["total"]
    summary = {
        "prospective_sampled_01_loss": prospective, "terminal_sampled_01_loss": terminal,
        "conditional_expected_prospective_01_loss": F(conditional_prospective, denominator),
        "conditional_expected_terminal_01_loss": action_mean,
        "conditional_expectation_scope": "Action bits only, for this realized adaptive selector/paid-label path. Sampled actions do not affect weights or future allocation on this fixed tape. This is not an unconditional selector mean.",
        "immutable_issued_brier": F(brier, denominator ** 2),
        "fixed_expert_all_issued_losses": dict(zip(S.EXPERT_NAMES, expert_losses)),
        "same_selector_corrected_expert_losses": dict(zip(S.EXPERT_NAMES, corrected_losses)),
        "corrected_expert_cost_basis": "Counterfactual substitution only of unbought actions, retaining this same selected receipt path, adaptive controller updates and COMPLETE actual invoice. Not a newly deployed or optimized control.",
        "theorem_bounds": theorem_bounds(contract, min(expert_losses), registry_units),
        "price_cases": {
            str(price): {
                "task_price": price, "common_primitive_unit_price": UNIT_PRICE,
                "realized_cold_total": F(price) * terminal + UNIT_PRICE * units,
                "conditional_action_mean_cold_total": F(price) * action_mean + UNIT_PRICE * units,
                "corrected_expert_same_complete_invoice_totals": {
                    name: F(price) * loss + UNIT_PRICE * units for name, loss in zip(S.EXPERT_NAMES, corrected_losses)},
                "probability_boundary": "Actual realized-selector resource invoice. This conditional cost is separate from the unconditional all-in certificate.",
            } for price in TASK_PRICES},
        "algorithmic_baseline": "An ordinary propensity-corrected blocked product-weights method receives the identical public lookahead, feedback, update and tariff; no renamed duplicate run.",
    }
    return summary, tuple(annotations)


def prior_comparison(summary, prior, transfer):
    name = f"main_T{summary['horizon']}_B{summary['block_size']}_state{summary['state_bits']}_seed{summary['seed']}"
    old = next(r for r in prior["learner_arms"] if r["name"] == name)
    change = next(r for r in transfer["transfers"] if r["arm"] == name)
    controls = [r for r in prior["controls"] if r["horizon"] == summary["horizon"]]
    table = next(r for r in controls if r["name"] == "quadratic_residue_table")
    ru, table_ru = summary["resource_units"], table["resource_units"]
    setup_free_bound = 11 * summary["horizon"] + ru["purchased_checked_services"]
    observed_ongoing_difference = ru["ongoing_including_learner_initialization"] - table_ru["ongoing_calls"]
    if observed_ongoing_difference < setup_free_bound:
        raise AssertionError("Saved invoices violate the source-level table dominance lower bound.")
    return {
        "scope": "Read-only previous DEVELOPMENT observations on the same affine mathematical tape, not new controls. Random-bit schedules differ, so losses are not paired action paths or a causal accuracy comparison.",
        "uniform_fixed_state": {
            "arm": name, "observed_core_version": "r-p3-b-a-blocked-prod-v1.1",
            "observed_cold_units": old["resource_units"]["cold_total"],
            "derived_current_v1_2_cold_units": change["derived_current_cold_units"],
            "registry_only_transfer_delta": change["registry_only_delta_units"],
            "terminal_sampled_01_loss": old["evaluation"]["terminal_sampled_01_loss"],
            "conditional_expected_terminal_01_loss": old["evaluation"]["conditional_expected_terminal_01_loss"],
            "bought_services_units": old["resource_units"]["purchased_checked_services"],
        },
        "ordinary_exact_controls": [{"name": r["name"], "observed_cold_units": r["resource_units"]["cold_total"],
                                      "terminal_01_loss": r["terminal_01_loss"], "resource_units": r["resource_units"]}
                                     for r in controls],
        "table_obstruction": {
            "observed_cold_unit_gap": ru["cold_total"] - table_ru["cold_total"],
            "observed_ongoing_minus_table_lookup_units": observed_ongoing_difference,
            "source_bound_setup_free_ongoing_gap_lower": setup_free_bound,
            "source_bound_setup_free_gap_after_paying_table_construction": setup_free_bound - table_ru["construction"],
            "argument": "Expert calls cost A(q)+9 while table calls cost A(q)+10; each learner close additionally pays 12. All remaining adaptive allocation/controller work is nonnegative. Thus ongoing learner minus table lookups is at least 11T plus actual purchases, even if all learner setup is free. Table construction is 1611; T>=147 covers it without purchase costs. Legal equal-block horizons then begin at 148.",
            "economic_scope": "The exact table has zero task loss. Dominance uses nonnegative task price and a shared nonnegative 64-bit-word primitive unit price. No claim for arbitrary category weights, physical runtime, or other query families.",
        },
    }


def run_arm(arm, directory, expected, prior, transfer):
    name = arm_name(arm)
    directory.mkdir(exist_ok=False)
    check_sources(expected)
    contract = AL.Contract(arm["T"], arm["B"], len(S.EXPERT_NAMES), arm["h"], arm["s"])
    tape = public_tape(contract.horizon, name)
    started = time.perf_counter_ns()
    registry = None
    write(directory / "started.json", {"stage": "DEVELOPMENT", "name": name, "started_utc": utc(),
                                        "contract": contract.record(), "seed": arm["seed"],
                                        "source_plan_hashes": expected, "principal_clock_credit_ns": 0})
    try:
        registry = S.registry_setup(tuple(source_paths()[:4]))
        write(directory / "source_registry.json", registry.record())
        execution_start = time.perf_counter_ns()
        run = AL.execute(tape, contract, seed=arm["seed"], setup_resources=registry.resources)
        execution_ns = time.perf_counter_ns() - execution_start
        public_archive = verified_zip(directory / "public_raw.zip", {
            "allocation_records.jsonl": lambda: iter(run["allocations"]),
            "purchase_invoices.jsonl": lambda: (r.record() for r in run["invoices"]),
            "transcript.jsonl": lambda: (public_closed_record(r) for r in run["transcript"]),
        }, expected)
        write(directory / "deployment_invoice.json", run["meter"])
        write(directory / "learner_state.json", run["learner"])
        write(directory / "closed_before_evaluation.json", {
            "closed_utc": utc(), "rounds": len(run["transcript"]), "purchases": len(run["invoices"]),
            "public_archive_sha256": public_archive["archive_sha256"],
            "public_archive_verified_before_evaluator": True,
            "learner_execute_elapsed_runtime_ns": execution_ns,
        })
        check_sources(expected)
        audit = public_protocol_audit(run, contract, tape)
        write(directory / "public_protocol_audit.json", audit)
        labels, private_rows = private_labels(tape, directory, source_paths())
        evaluation, annotations = evaluate(run, contract, labels, registry.resources.total)
        private_archive = verified_zip(directory / "evaluation_raw.zip", {
            "private_evaluator_labels.jsonl": lambda: iter(private_rows),
            "postclosed_evaluator_annotations.jsonl": lambda: iter(annotations),
        }, expected)
        purchase_meter = C.CostMeter()
        for receipt in run["invoices"]:
            purchase_meter.absorb(receipt.resources, "checked_purchase")
        purchase_invoice = purchase_meter.snapshot()
        invoice_sum_check(purchase_invoice)
        write(directory / "purchases_aggregate_invoice.json", purchase_invoice)
        cold, setup, purchases = run["meter"]["total"], registry.resources.total, purchase_invoice["total"]
        if evaluation["theorem_bounds"]["all_in_resource_certificate"]["total"] != run["funded_cap"]:
            raise AssertionError("The all-in certificate differs from the admitted whole-service cap.")
        summary = {
            "status": "PASS", "stage": "DEVELOPMENT", "name": name,
            "horizon": contract.horizon, "block_size": contract.block_size,
            "state_bits": contract.state_bits, "action_bits": contract.action_bits, "seed": arm["seed"],
            "contract": contract.record(), "learner": run["learner"], "public_protocol_audit": audit,
            "resource_units": {
                "cold_total": cold, "source_registry": setup,
                "ongoing_including_learner_initialization": cold - setup,
                "purchased_checked_services": purchases, "nonpurchase_excluding_registry": cold - setup - purchases,
                "maximum_actual_purchased_service_units": max(r.resources.total for r in run["invoices"]),
                "funded_cap": run["funded_cap"],
            },
            "evaluation": evaluation,
            "archives": [{k: a[k] for k in ("archive", "archive_bytes", "archive_sha256")} for a in (public_archive, private_archive)],
            "execution_elapsed_runtime_ns": execution_ns,
            "arm_elapsed_runtime_ns": time.perf_counter_ns() - started,
            "source_plan_hashes": expected, "finished_utc": utc(), "principal_clock_credit_ns": 0,
        }
        summary["prior_same_tape_comparison"] = prior_comparison(summary, prior, transfer)
        check_sources(expected)
        write(directory / "summary.json", summary)
        return summary
    except BaseException as error:
        write(directory / "failure.json", {
            "status": "FAIL", "name": name, "error": repr(error), "traceback": traceback.format_exc(),
            "finished_utc": utc(), "elapsed_runtime_ns": time.perf_counter_ns() - started,
            "source_plan_hashes": expected, "reported_partial_meter": getattr(error, "meter", None),
            "reported_closed_rounds": getattr(error, "rounds_closed", None),
            "reported_purchases": getattr(error, "purchases", None),
            "source_registry_already_procured": None if registry is None else registry.record(),
            "disposition": "Preserve completed artifacts and reported spent resources; stop with no retry, retuning or inferred work.",
            "principal_clock_credit_ns": 0,
        })
        raise


def interrupt_as_exception(signum, frame):
    raise InterruptedError(f"Received signal {signum}; preserving observed completed work.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", required=True)
    parser.add_argument("--prior-result", required=True)
    parser.add_argument("--prior-registry-transfer", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    plan_path, prior_path, transfer_path = (Path(p).resolve() for p in
                                           (args.plan, args.prior_result, args.prior_registry_transfer))
    plan = json.loads(plan_path.read_text())
    validate_plan(plan, plan_path)
    prior, transfer = json.loads(prior_path.read_text()), json.loads(transfer_path.read_text())
    if prior["status"] != "PASS" or transfer["status"] != "PASS" or transfer["registry_only_delta_units"] != 26:
        raise ValueError("Prior results and exact registry-only transfer must be verified PASS records.")
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=False)
    (out / "sources").mkdir()
    expected = hashes((*source_paths(), plan_path, prior_path, transfer_path))
    for path in source_paths():
        (out / "sources" / path.name).write_bytes(path.read_bytes())
    for path, target in ((plan_path, "allocation_run_plan_v1.json"),
                         (prior_path, "prior_uniform_result.json"),
                         (transfer_path, "prior_registry_transfer.json")):
        (out / "sources" / target).write_bytes(path.read_bytes())
    check_sources(expected)
    write(out / "manifest.json", {
        "stage": "DEVELOPMENT", "version": VERSION, "allocation_version": AL.VERSION,
        "controller_version": C.VERSION, "service_version": S.VERSION,
        "started_utc": utc(), "command": sys.argv, "cwd": str(Path.cwd()),
        "source_plan_hashes": expected,
        "environment": {"python": sys.version, "python_executable": sys.executable,
                        "platform": platform.platform(), "machine": platform.machine(),
                        "zlib_build_version": zlib.ZLIB_VERSION, "zlib_runtime_version": zlib.ZLIB_RUNTIME_VERSION},
        "planned_arms": list(PLANNED_ARMS), "new_controls": 0, "initial_probe_repeated": False,
        "public_tape": "Ordered p in (17,31,47,61,97), a=1..p-1; index (73*t+19) mod 248. No labels computed by input supplier.",
        "input_contract": "Immutable full current public block available before allocation; frozen advice and weights. Private unbought labels computed only after execute and verified public archive closure.",
        "paid_deployment_closure": [str(p) for p in source_paths()[:4]],
        "analysis_scope": "The separate driver, archives, audits and evaluator are external DEVELOPMENT evidence work, not a deployed forecasting method; evaluator has its own full source registry and named one-word arithmetic invoice.",
        "principal_clock_credit_ns": 0,
    })
    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, interrupt_as_exception)
    completed = []
    started = time.perf_counter_ns()
    result = {"status": "FAIL", "stage": "DEVELOPMENT", "version": VERSION,
              "source_plan_hashes": expected, "principal_clock_credit_ns": 0}
    try:
        (out / "learner_arms").mkdir()
        for arm in plan["arms"]:
            name = arm_name(arm)
            write(out / "progress.json", {"active": name, "completed_arms": len(completed), "updated_utc": utc()})
            summary = run_arm(arm, out / "learner_arms" / name, expected, prior, transfer)
            completed.append(summary)
            print(json.dumps({"completed": name, "cold_units": summary["resource_units"]["cold_total"],
                              "terminal_loss": summary["evaluation"]["terminal_sampled_01_loss"]}), flush=True)
        check_sources(expected)
        result.update(status="PASS", learner_arms=completed, new_controls=0, initial_probe_repeated=False)
    except BaseException as error:
        result.update(error=repr(error), traceback=traceback.format_exc(), completed_learner_arms=completed,
                      disposition="Stopped at first failure/interruption. Preserve completed units; no retry, changed-source execution, tuning or inferred work.")
    result.update(finished_utc=utc(), elapsed_runtime_ns=time.perf_counter_ns() - started)
    write(out / "result.json", result)
    write(out / "progress.json", {"active": None, "status": result["status"],
                                   "completed_arms": len(completed), "updated_utc": utc()})
    print(json.dumps({"status": result["status"], "completed_arms": len(completed),
                      "new_controls": 0, "elapsed_runtime_ns": result["elapsed_runtime_ns"]}), flush=True)
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
