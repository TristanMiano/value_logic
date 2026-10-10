"""Independent public-only P3-08 reporter audit. DEVELOPMENT, 2026-10-10.

Contributor: ChatGPT (GPT-6 Astra Pro), delegated reconstruction reviewer.
Expected values use Fraction and the displayed derivation, never the subject's
integer calculator. New labels enter only through paid selected broker calls.
This evaluator does not add principal-clock credit or deployment capabilities.
"""
from __future__ import annotations

import argparse
import ast
from copy import deepcopy
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import importlib
import json
import math
from pathlib import Path
import platform
import shutil
import sys

VERSION = "p308-reporting-independent-v1"
SOURCE_PATHS = (
    "v3/experiments/p308_reporting.py", "v3/experiments/p308_broker.py",
    "v3/experiments/p308_cnf.py", "v3/experiments/p308_common.py",
    "v3/checks/07_selective_feedback.py",
    "v3/checks/07_selective_feedback_service.py",
    "v3/checks/07_computation_adapter.py",
    "v3/derivations/08_live_hard_performance.md",
    "v3/RESEARCH_PROTOCOL.md",
)
SMOKE = "v3/work_logs/P3_08_2026-10-10_S1/development/reporting_smoke_v1/public_results.json"


def utc():
    return datetime.now(timezone.utc).isoformat()


def encode(value):
    if isinstance(value, F):
        return [value.numerator, value.denominator]
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(v) for v in value]
    return value


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(encode(value), indent=2, sort_keys=True) + "\n")


def fingerprint(path, relative):
    data = path.read_bytes()
    return {"path": relative, "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest()}


def frozen(value):
    return tuple(frozen(x) for x in value) if isinstance(value, (list, tuple)) else value


def ceil_root(n):
    # Separate implementation, used only on nonnegative public integers.
    lower, upper = 0, n + 1
    while lower < upper:
        midpoint = (lower + upper) // 2
        if midpoint * midpoint >= n:
            upper = midpoint
        else:
            lower = midpoint + 1
    return lower


def derive_public(episode):
    """Direct rational formulas from derivation sections 3–5.

    There is deliberately no provider, query solver, or production reporter
    argument. The only label reads are current selected invoices and earlier
    selected invoices indexed by the complete key.
    """
    contract = episode["contract"]
    t, b = contract["horizon"], contract["block_size"]
    m = t // b
    rows = episode["trace"]
    by_key = {}
    delta_f = delta_v = F(0)
    delta_z = n_live = 0
    base_v, base_f = F(t - m, 2), F(t, 2)
    v_min = v_max = f_min = f_max = F(0)
    squared_widths = F(0)
    selected_brier = live_unselected_variance = F(0)
    read_labels = []
    chronology = []
    for k in range(m):
        block_width = F(0)
        selected = episode["blocks"][k]["selected"]
        for offset in range(b):
            row = rows[k * b + offset]
            key = frozen(row["claim_key"])
            q, live_q = F(*row["base_q"]), F(*row["emitted_q"])
            pi = F(*row["propensity"])
            hard = row["hard_before"] == "checked"
            prior = by_key.get(key)
            is_selected = offset == selected
            if hard:
                if prior is None or live_q != prior:
                    raise ValueError("Independent chronology rejected unsupported prior hard answer")
                delta_f += (q - prior) ** 2
                if not is_selected:
                    delta_v += q + (1 - 2 * q) * prior
                    delta_z += int(row["base_action"] != prior)
            elif not is_selected:
                n_live += 1
                v_min += min(q, 1 - q)
                v_max += max(q, 1 - q)
            known_label = prior if hard else None
            if is_selected:
                invoice = episode["invoices"][k]
                if frozen(invoice["claim_key"]) != key:
                    raise ValueError("Independent selected receipt key mismatch")
                label = invoice["answer"]
                if type(label) is not int or label not in (0, 1):
                    raise ValueError("Independent selected receipt label type")
                residual_half = q + (1 - 2 * q) * label - F(1, 2)
                base_v += (1 / pi - 1) * residual_half
                base_f += residual_half / pi
                known_label = label
                if prior is not None and prior != label:
                    raise ValueError("Independent contradictory receipt check")
                # Current receipt is admitted only after pre-issuance H was read.
                by_key[key] = label
                read_labels.append({"row": row["index"], "query_id": invoice["query_id"]})
                selected_brier += (live_q - label) ** 2
            else:
                live_unselected_variance += live_q * (1 - live_q)
            if known_label is None:
                f_min += min(live_q ** 2, (1 - live_q) ** 2)
                f_max += max(live_q ** 2, (1 - live_q) ** 2)
            else:
                f_min += (live_q - known_label) ** 2
                f_max += (live_q - known_label) ** 2
            base_f -= q * (1 - q)
            block_width = max(block_width, abs(1 - 2 * q) / pi)
            chronology.append({"row": row["index"], "hard": hard,
                               "earlier_receipt": prior is not None,
                               "selected": is_selected})
        squared_widths += block_width ** 2
    s = b if contract["selector"] == "uniform" else 2 * b
    rate = s * ceil_root(2 * m)
    radius = squared_widths / rate + F(5 * rate, 8)
    action_radius = ceil_root((5 * n_live + 1) // 2)
    live_v, live_f = base_v - delta_v, base_f - delta_f

    def intersect(center, half_width, left, right):
        low, high = max(center - half_width, left), min(center + half_width, right)
        return {"lower": low, "upper": high, "confidence_conflict": low > high}

    if n_live == 0:
        if f_min != f_max:
            raise AssertionError("No unresolved unselected row must make all Brier losses observable")
        intervals = {"V": intersect(F(0), F(0), F(0), F(0)),
                     "F": intersect(f_min, F(0), f_min, f_max),
                     "Z": intersect(F(0), F(0), F(0), F(0))}
    else:
        intervals = {"V": intersect(live_v, radius, v_min, v_max),
                     "F": intersect(live_f, radius, f_min, f_max),
                     "Z": intersect(live_v, radius + action_radius, F(0), F(n_live))}
    identity_left = live_f - live_v
    identity_right = selected_brier - live_unselected_variance
    if identity_left != identity_right:
        raise AssertionError("Independent public shared-residual difference identity failed")
    return {"base_centers": {"V": base_v, "F": base_f},
            "live_centers": {"V": live_v, "F": live_f},
            "corrections": {"F": delta_f, "V": delta_v, "Z": delta_z},
            "Q": squared_widths, "R": rate, "sampling_radius": radius,
            "action_radius": action_radius, "n_live": n_live,
            "exact_all_remaining_known": n_live == 0,
            "intervals": intervals,
            "deterministic_envelopes": {"V": [v_min, v_max], "F": [f_min, f_max],
                                        "Z": [F(0), F(n_live)]},
            "rows_read": t, "purchased_labels_read": m,
            "retained_checked_keys": len(by_key),
            "audit": {"label_reads": read_labels, "chronology": chronology,
                      "public_center_difference": identity_left,
                      "selected_brier_minus_unselected_variance": identity_right}}


def differences(expected, actual, prefix=""):
    errors = []
    if isinstance(expected, F):
        try:
            equal = F(*actual) == expected
        except (TypeError, ValueError, ZeroDivisionError):
            equal = False
        if not equal:
            errors.append({"field": prefix, "expected": encode(expected), "actual": actual})
    elif isinstance(expected, dict):
        for key, value in expected.items():
            if key == "audit":
                continue
            if not isinstance(actual, dict) or key not in actual:
                errors.append({"field": prefix + "." + key, "missing": True})
            else:
                errors.extend(differences(value, actual[key], prefix + "." + key))
    elif isinstance(expected, list):
        if not isinstance(actual, list) or len(expected) != len(actual):
            errors.append({"field": prefix, "wrong_length": True})
        else:
            for i, value in enumerate(expected):
                errors.extend(differences(value, actual[i], prefix + f"[{i}]"))
    elif type(expected) is not type(actual) or expected != actual:
        errors.append({"field": prefix, "expected": expected, "actual": actual})
    return errors


def finite_bounds(reporter_source):
    """Independent absolute bounds over public maximum contracts.

    Endpoints are monotone in T and D for fixed B. Every prefix sum is bounded
    by the sum of absolute terms; no cancellation is used. A separate coarse
    power bound in analysis.md covers all operation prebounds by 134 bits.
    """
    t, d, key_words = 8192, 1 << 32, 1024
    table = []
    for exponent in range(1, 11):
        b, m = 1 << exponent, t // (1 << exponent)
        for selector in ("uniform", "tickets"):
            p, multiple = (b, 1) if selector == "uniform" else (2 * b, b + 1)
            u = (t - m) * d * multiple // 2 + m * (p - 1) * (d // 2) * multiple
            a = t * d*d * multiple // 2 + m * p * (d // 2) * d * multiple + t * (d*d // 4) * multiple
            width = d * p * multiple
            q_num, q_den = m * width*width, d*d * multiple*multiple
            rate = p * ceil_root(2 * m)
            common = 8 * rate * q_den
            rho = 8 * q_num + 5 * rate*rate * q_den
            assert common % (d * multiple) == common % (d*d * multiple) == 0
            u_scaled, a_scaled = u * (common // (d * multiple)), a * (common // (d*d * multiple))
            live_u, live_a = u_scaled + t*d * (common // d), a_scaled + t*d*d * (common // (d*d))
            z_radius = rho + ceil_root((5*t + 1)//2) * common
            named = {"U_numerator_abs": u, "A_numerator_abs": a,
                     "width_numerator": width, "Q_numerator": q_num,
                     "Q_denominator": q_den, "R": rate, "common": common,
                     "rho_numerator": rho, "scaled_U_abs": u_scaled,
                     "scaled_A_abs": a_scaled, "live_U_abs": live_u,
                     "live_A_abs": live_a, "Z_radius_numerator": z_radius,
                     "largest_interval_endpoint_abs": max(live_u, live_a) + z_radius,
                     "deterministic_envelope_numerator": t * common}
            table.append({"selector": selector, "T": t, "B": b, "D": d,
                          "named_bounds": named,
                          "largest_named_bits": max(x.bit_length() for x in named.values())})
    parsed = ast.parse(reporter_source)
    report_function = next(x for x in parsed.body if isinstance(x, ast.FunctionDef) and x.name == "report_owned_episode")
    row_loop = next(x for x in ast.walk(report_function) if isinstance(x, ast.For)
                    and isinstance(x.target, ast.Name) and x.target.id == "offset")
    integer_calls = [x for x in ast.walk(row_loop) if isinstance(x, ast.Call)
                     and isinstance(x.func, ast.Attribute)
                     and isinstance(x.func.value, ast.Name) and x.func.value.id == "integer"]
    row_call_count = len(integer_calls)
    assert row_call_count <= 100
    assert all(x.func.attr not in ("pair", "ceil_sqrt") for x in integer_calls)
    key_comparisons = t * 4096 * (4 * key_words + 4) + 4096 * (2 * key_words + 4)
    # <100 row integer calls at <=52 units each; the 100000 bundle also
    # dominates all row headers, shape/key reads, storage and receipt binding.
    other_rows = t * 100000
    block_records = 4096 * (48 + 4 * 1024)
    # Two <=256-bit square-root envelopes, <=64 rational outputs, <=1000
    # nonrow integer calls, fixed header/retention. 2^24 is a loose ceiling.
    global_bound = 1 << 24
    total = key_comparisons + other_rows + block_records + global_bound
    return {"finite_contract_table": table,
            "largest_named_magnitude_bits": max(x["largest_named_bits"] for x in table),
            "conservative_all_preoperation_bits": 134,
            "declared_width": 256,
            "per_row_integer_call_sites_counting_both_branches": row_call_count,
            "key_scan_and_selected_key_comparison_bound": key_comparisons,
            "other_row_bound": other_rows, "block_record_bound": block_records,
            "global_arithmetic_output_bound": global_bound,
            "total_report_tariff_bound": total,
            "total_below_2_power_38": total < 1 << 38,
            "funding_cap": 1 << 48, "funding_cap_sufficient": total < 1 << 48,
            "cost_scope": "declared owned word-record report tariff; source enrollment is separate; not CPU or Python heap"}


class IdentityOnly:
    def __init__(self, service):
        self.PROVIDER, self.VERSION = service.PROVIDER, service.VERSION

    def __getattr__(self, name):
        raise AssertionError("Reporter requested a nonidentity provider capability: " + name)


class PurchaseBoundary:
    """Only broker-public operations; selected purchase calls are logged."""
    def __init__(self, service):
        for name in ("PROVIDER", "VERSION", "EXPERT_NAMES", "EXPERT_CAP",
                     "Query", "Receipt", "Rejected", "service_cap",
                     "expert_predictions", "cost_proxy"):
            setattr(self, name, getattr(service, name))
        self._service, self.calls = service, []

    def checked_purchase(self, query, **kwargs):
        self.calls.append(query.query_id)
        return self._service.checked_purchase(query, **kwargs)


def run(repo, out):
    if out.exists():
        raise FileExistsError("Use a fresh output directory; prior evidence is preserved")
    out.mkdir(parents=True)
    before = []
    for relative in SOURCE_PATHS:
        src, dst = repo / relative, out / "source" / relative
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        before.append(fingerprint(src, relative))
    shutil.copyfile(Path(__file__), out / "audit_reporting.py")
    shutil.copyfile(Path(__file__).with_name("plan.md"), out / "plan.md")
    shutil.copyfile(repo / SMOKE, out / "prior_public_smoke.json")
    save(out / "manifest_before.json", {"stage": "DEVELOPMENT", "version": VERSION,
         "created_utc": utc(), "sources": before,
         "audit_script": fingerprint(Path(__file__), "audit_reporting.py"),
         "input_smoke": fingerprint(repo / SMOKE, SMOKE),
         "runtime": {"python": sys.version, "implementation": platform.python_implementation(),
                     "platform": platform.platform()},
         "principal_time_credit_seconds": 0,
         "expected_values": "independent Fraction formulas; no unpurchased label reads"})
    sys.path.insert(0, str(out / "source/v3/experiments"))
    reporter = importlib.import_module("p308_reporting")
    broker = importlib.import_module("p308_broker")
    service = importlib.import_module("p308_cnf")
    identity = IdentityOnly(service)
    completed, cases, checks = [], [], []

    def complete(name, passed, details):
        row = {"case": name, "passed": bool(passed), "details": details}
        completed.append(row)
        with (out / "completed.jsonl").open("a") as handle:
            handle.write(json.dumps(encode(row), sort_keys=True) + "\n")
        return row

    def compare(name, episode, report):
        expected = derive_public(episode)
        errors = differences(expected, report)
        if report.get("status") != "success":
            errors.append({"status": report.get("status"), "failure": report.get("failure_detail")})
        result = {"name": name, "episode": episode, "report": report,
                  "expected": expected, "differences": errors}
        cases.append(result)
        save(out / "cases" / (name + ".json"), result)
        complete(name, not errors, {"mismatches": errors, "n_live": expected["n_live"],
                                 "report_units": report["meter"]["total"],
                                 "peak_integer_bits": report.get("peak_integer_bits")})
        return result

    for row in json.loads((repo / SMOKE).read_text()):
        name = "smoke_" + row["selector"] + ("_hard" if row["hard"] else "_base")
        compare(name + "_historical", row["episode"], row["report"])
        compare(name + "_current", row["episode"], reporter.report_owned_episode(identity, row["episode"]))

    # Public encodings only. No labels, private evaluator, or search selection
    # are used to construct this mixed repeat/distinct-key development tape.
    shapes = (((1,), (-2,)), ((-1, 2), (1, 2)), ((-1,), (1,)),
              ((), (2,)), ((-1, -2), (1, 2)), ((1, 2), (-1, 2), (1, -2)))
    order = (0, 0, 1, 2, 0, 3, 3, 4, 1, 4, 5, 5)
    tag = "s" * 128
    tape = tuple(service.make_query(f"independent-{i}", 2, shapes[j], source_version=tag)
                 for i, j in enumerate(order))
    save(out / "public_input.json", {"queries": [q.record() for q in tape],
                                    "seed": 3080801, "source_tag_length": len(tag),
                                    "private_labels": "not computed or supplied"})
    fresh = []
    for selector in ("uniform", "tickets"):
        for hard in (False, True):
            boundary = PurchaseBoundary(service)
            contract = broker.Contract(12, 4, 6, 16, 16, selector, 128)
            episode = broker.execute(boundary, tape, contract, seed=3080801, hard=hard,
                                     purchase_solver="enumeration", scope_epoch="independent-128")
            name = "tag128_" + selector + ("_hard" if hard else "_base")
            report = reporter.report_owned_episode(identity, episode)
            result = compare(name, episode, report)
            fresh.append(result)
            selected_ids = [r["query_id"] for r in episode["trace"] if r["selected"]]
            checks.append(complete(name + "_purchases_only", boundary.calls == selected_ids,
                                   {"paid_purchase_calls": boundary.calls, "selected_rows": selected_ids}))
            checks.append(complete(name + "_non_all_known", result["expected"]["n_live"] > 0,
                                   {"n_live": result["expected"]["n_live"]}))
    boundary = PurchaseBoundary(service)
    edge_tape = tuple(service.make_query(f"one-bit-{i}", 2, shapes[j], source_version=tag)
                      for i, j in enumerate((0, 1, 0, 1)))
    edge = broker.execute(boundary, edge_tape, broker.Contract(4, 2, 6, 1, 1, "tickets", 128),
                          seed=3080802, hard=True, purchase_solver="enumeration")
    compare("one_action_bit_tickets", edge, reporter.report_owned_episode(identity, edge))

    template = fresh[1]["episode"]
    def reject(name, source, mutation):
        changed = deepcopy(source)
        mutation(changed)
        report = reporter.report_owned_episode(identity, changed)
        record = {"name": name, "input": changed, "report": report}
        save(out / "mutations" / (name + ".json"), record)
        checks.append(complete(name, report["status"] == "failed" and not report["confidence_eligible"],
                               {"failure": report.get("failure_detail"), "spent": report["meter"]["total"]}))

    first_selected = next(i for i, r in enumerate(template["trace"]) if r["selected"])
    def current_purchase_cannot_be_prior(e):
        row = e["trace"][first_selected]
        y = e["invoices"][0]["answer"]
        row.update(hard_before="checked", emitted_q=[y * row["base_q"][1], row["base_q"][1]], prospective_action=y)
    reject("current_receipt_cannot_retroactively_correct_forecast", template, current_purchase_cannot_be_prior)
    smoke_hard = next(x["episode"] for x in cases if x["name"] == "smoke_uniform_hard_current")
    hard_row = next(i for i, r in enumerate(smoke_hard["trace"]) if r["hard_before"] == "checked" and not r["selected"])
    def wrong_override(e):
        row = e["trace"][hard_row]
        row["emitted_q"][0] = row["emitted_q"][1] - row["emitted_q"][0]
        row["prospective_action"] = 1 - row["prospective_action"]
    reject("hard_override_must_equal_earlier_answer", smoke_hard, wrong_override)
    reject("hard_answer_requires_complete_key", smoke_hard,
           lambda e: e["trace"][hard_row]["claim_key"].__setitem__(2, 3))
    reject("scope_epoch_mismatch", template,
           lambda e: e["trace"][0].__setitem__("scope", list(e["scope"][:2]) + ["stale-epoch"]))
    reject("stale_provider_version", template,
           lambda e: e["invoices"][0].__setitem__("provider_version", "stale-provider"))
    reject("false_row_propensity", template,
           lambda e: e["trace"][0].__setitem__("propensity", [1, 8]))
    reject("false_block_propensity", template,
           lambda e: e["blocks"][0]["propensities"].__setitem__(0, [1, 8]))
    reject("ticket_selection_binding", template,
           lambda e: e["blocks"][0].__setitem__("ticket", (e["blocks"][0]["ticket"] + 1) % 4))
    reject("selected_terminal_requires_checked_correction", template,
           lambda e: e["trace"][first_selected].__setitem__("terminal_action", 1 - e["invoices"][0]["answer"]))
    reject("unselected_cannot_admit_unpurchased_label", template,
           lambda e: next(r for r in e["trace"] if not r["selected"]).__setitem__("purchased_label", 0))
    reject("129_character_source_tag", template,
           lambda e: e["trace"][0].__setitem__("claim_key", [e["trace"][0]["claim_key"][0], "s" * 129,
                                                          e["trace"][0]["claim_key"][2], e["trace"][0]["claim_key"][3]]))
    try:
        service.make_query("too-long-source", 2, shapes[0], source_version="s" * 129)
        too_long_rejected = False
    except service.Rejected:
        too_long_rejected = True
    checks.append(complete("query_and_reporter_source_cap_agree", too_long_rejected,
                           {"valid_length": 128, "rejected_length": 129}))

    full = reporter.report_owned_episode(identity, template, unit_limit=1 << 48)
    below_cap = reporter.report_owned_episode(identity, template, unit_limit=(1 << 48) - 1)
    unfunded = deepcopy(template)
    unfunded["all_path_funded"] = False
    no_execution_premise = reporter.report_owned_episode(identity, unfunded, unit_limit=1 << 48)
    denied = reporter.report_owned_episode(identity, template, unit_limit=full["meter"]["total"] - 1)
    budget_records = {"at_cap": full, "successful_below_cap": below_cap,
                      "execution_premise_missing": no_execution_premise, "last_bundle_denial": denied}
    save(out / "budget_checks.json", budget_records)
    checks.append(complete("funding_eligibility_boundary",
                           full["status"] == below_cap["status"] == no_execution_premise["status"] == "success"
                           and full["confidence_eligible"] and not below_cap["confidence_eligible"]
                           and not no_execution_premise["confidence_eligible"],
                           {"at_cap_eligible": full["confidence_eligible"],
                            "below_cap_eligible": below_cap["confidence_eligible"],
                            "missing_execution_premise_eligible": no_execution_premise["confidence_eligible"]}))
    checks.append(complete("failed_reporting_retains_paid_prefix_and_suppresses_intervals",
                           denied["status"] == "failed" and 0 < denied["meter"]["total"] < full["meter"]["total"]
                           and "intervals" not in denied and not denied["confidence_eligible"],
                           {"failed_paid_prefix": denied["meter"]["total"],
                            "successful_report_bill": full["meter"]["total"], "detail": denied.get("failure_detail")}))
    meter = broker.C.CostMeter(100000)
    integer = reporter.IntegerMeter(meter)
    integer.add(1, 1)
    prior_bill = meter.total
    try:
        integer.mul(1 << 128, 1 << 128)
        width_rejected = False
    except broker.C.Rejected:
        width_rejected = True
    checks.append(complete("overwidth_operation_rejected_before_operation_charge",
                           width_rejected and meter.total == prior_bill,
                           {"paid_prior_operation": prior_bill, "after_rejection": meter.total}))

    bounds = finite_bounds((out / "source/v3/experiments/p308_reporting.py").read_text())
    save(out / "finite_bounds.json", bounds)
    checks.append(complete("finite_width_and_report_funding_bounds",
                           bounds["conservative_all_preoperation_bits"] < reporter.MAX_BITS
                           and bounds["funding_cap_sufficient"],
                           {key: value for key, value in bounds.items() if key != "finite_contract_table"}))
    after = [fingerprint(repo / relative, relative) for relative in SOURCE_PATHS]
    snapshot_after = [fingerprint(out / "source" / relative, relative) for relative in SOURCE_PATHS]
    save(out / "manifest_after.json", {"created_utc": utc(), "sources": after,
                                       "snapshot_sources": snapshot_after,
                                       "repo_matches_before": after == before,
                                       "snapshot_matches_before": snapshot_after == before})
    checks.append(complete("source_snapshot_unchanged", before == after == snapshot_after, {}))
    ticket_kinds = sorted({("favorite" if block["selected"] == block["favorite"] else "nonfavorite",
                            "low_ticket" if block["ticket"] < item["episode"]["contract"]["block_size"] else "extra_ticket")
                           for item in cases if item["episode"]["contract"]["selector"] == "tickets"
                           for block in item["episode"]["blocks"]})
    summary = {"stage": "DEVELOPMENT", "version": VERSION, "subject_version": reporter.VERSION,
               "created_utc": utc(), "completed_checks": len(completed),
               "passed_checks": sum(x["passed"] for x in completed),
               "failed_checks": [x for x in completed if not x["passed"]],
               "formula_comparisons": len(cases),
               "fresh_owned_episodes": len(fresh) + 1,
               "ticket_branches_observed": ticket_kinds,
               "public_only": True, "private_truth_evaluations": 0,
               "principal_time_credit_seconds": 0,
               "report_unit_range": [min(x["report"]["meter"]["total"] for x in cases),
                                     max(x["report"]["meter"]["total"] for x in cases)],
               "largest_observed_integer_bits": max(x["report"]["peak_integer_bits"] for x in cases),
               "reproduce": "python " + str(Path(__file__)) + " --repo " + str(repo) + " --out /tmp/p308_reporting_independent_replay"}
    save(out / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.repo.resolve(), args.out.resolve())
    raise SystemExit(bool(result["failed_checks"]))
