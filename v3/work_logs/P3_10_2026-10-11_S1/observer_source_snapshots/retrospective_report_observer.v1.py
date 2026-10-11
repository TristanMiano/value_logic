"""Public-only supplemental retrospective report bounds on sealed P3-10 paths.

Contributor: ChatGPT (GPT-6 Astra Pro), principal /root, 2026-10-11.
This observer never imports a frozen module, calls a service or evaluates CNF.
It durably writes public-only bounds before optional private validation using
the separate numeric observer. The new bounds are unbilled audit calculations,
not frozen endpoints, deployed reports, or a claim about sampling coverage.
"""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json
import os
import time
import traceback

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
FINAL = REPO / "v3/experiments/final_v1"
CHECKS = Counter()
SOURCES = {}


def stamp():
    return {"utc": datetime.now(timezone.utc).isoformat(),
            "monotonic_ns": time.monotonic_ns(),
            "boot_id": Path("/proc/sys/kernel/random/boot_id").read_text().strip()}


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True, allow_nan=False) + "\n").encode()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    SOURCES[str(path.relative_to(REPO))] = digest(path)
    return json.loads(path.read_text())


def require(condition, name, detail):
    CHECKS[name] += 1
    if not condition:
        raise AssertionError(f"{name}: {detail}")


def rat(value):
    return F(*value) if isinstance(value, (list, tuple)) else F(value)


def pair(value):
    value = F(value)
    return [value.numerator, value.denominator]


def encoded(value):
    if isinstance(value, F):
        return pair(value)
    if isinstance(value, dict):
        return {str(k): encoded(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [encoded(v) for v in value]
    return value


def save(path, value):
    with path.open("x") as file:
        json.dump(encoded(value), file, indent=2, sort_keys=True, allow_nan=False)
        file.write("\n")
        file.flush()
        os.fsync(file.fileno())


def sealed(stage, identifier):
    seals = list((FINAL / "stages" / stage / "units" / identifier).glob("attempt_*/seal.json"))
    require(len(seals) == 1, "one_result_seal", [stage, identifier])
    path = seals[0]
    seal = read(path)
    require(digest(path.parent / "result.json") == seal["result_sha256"], "result_hash", identifier)
    require(digest(path.parent / "start.json") == seal["start_sha256"], "start_hash", identifier)
    result = read(path.parent / "result.json")
    require(hashlib.sha256(canonical(result["unit"])).hexdigest() == seal["unit_sha256"],
            "unit_hash", identifier)
    return result, seal


def key(value):
    require(isinstance(value, list) and len(value) == 4, "complete_claim_key_shape", value)
    return canonical(value)


def audit(unit, paid):
    episode = paid["episode"]
    report = (paid.get("optional_reporting") or {}).get("report", {})
    header = {"unit_id": unit["id"], "group_id": unit["group_id"],
              "configuration_id": unit["configuration_id"], "stakes": unit["stakes"],
              "horizon": episode["contract"]["horizon"],
              "episode_status": episode["status"], "report_status": report.get("status"),
              "additional_reporting_units": (paid.get("optional_reporting") or {}).get("additional_units")}
    if episode["status"] != "success" or report.get("status") != "success":
        return dict(header, status="unavailable", reason="Complete successful parent and report required.")
    rows = episode["trace"]
    t = header["horizon"]
    require(len(rows) == t and [r["index"] for r in rows] == list(range(t)),
            "complete_scheduled_chronology", unit["id"])
    require(episode["hard_state"]["generation"] == 0
            and episode["hard_state"]["conflicts"] == 0
            and episode["hard_state"]["withdrawals"] == 0,
            "unchanged_sound_epoch", unit["id"])
    provider = ("bounded_cnf_checked", "p308-bounded-cnf-services-v1.1") if unit["parameters"]["provider"] == "cold" else (
                "owned_cached_cnf_receipt", "p308-selected-receipt-cache-v1.1")
    invoice_by_id = {}
    known = {}
    for receipt in episode["invoices"]:
        require(receipt["query_id"] not in invoice_by_id, "distinct_paid_request_ids", unit["id"])
        require(receipt["status"] == "success" and receipt["checked"] is True
                and type(receipt["answer"]) is int and receipt["answer"] in (0, 1)
                and (receipt["provider"], receipt["provider_version"]) == provider,
                "admitted_current_paid_label", receipt["query_id"])
        invoice_by_id[receipt["query_id"]] = receipt
        k = key(receipt["claim_key"])
        require(k not in known or known[k] == receipt["answer"], "no_conflicting_paid_labels", unit["id"])
        require(receipt["claim_key"][:2] == episode["scope"][:2], "paid_label_epoch", unit["id"])
        known[k] = receipt["answer"]
    coefficients = {name: defaultdict(lambda: [F(0), F(0), F(0)]) for name in ("F", "V", "Z")}
    chronology = {name: [F(0), F(0)] for name in coefficients}
    prior = {}
    n_live = 0
    counts = Counter()
    all_keys = set()
    for row in rows:
        k = key(row["claim_key"])
        all_keys.add(k)
        require(row["scope"] == episode["scope"] and row["claim_key"][:2] == episode["scope"][:2],
                "row_current_epoch", [unit["id"], row["index"]])
        q, a = rat(row["emitted_q"]), row["terminal_action"]
        require(0 <= q <= 1 and type(a) is int and a in (0, 1), "issued_target_domain", unit["id"])
        hard = row["hard_before"] == "checked"
        require(hard == (episode["hard_enabled"] and k in prior), "chronological_hard_applicability", unit["id"])
        label = prior.get(k) if hard else None
        if hard:
            require(q == label and row["prospective_action"] == label, "sound_hard_issue", unit["id"])
        if row["selected"]:
            receipt = invoice_by_id[row["query_id"]]
            require(key(receipt["claim_key"]) == k and receipt["answer"] == row["purchased_label"],
                    "selected_receipt_binding", unit["id"])
            label = receipt["answer"]
            require(a == label, "selected_terminal_correction", unit["id"])
            prior[k] = label
        else:
            require(row["purchased_label"] is None, "no_unpurchased_row_label", unit["id"])
            n_live += int(not hard)
        terms = {"F": (q * q, 1 - 2 * q), "Z": (F(a), F(1 - 2 * a))}
        if not row["selected"]:
            terms["V"] = (q, 1 - 2 * q)
        for name, (constant, coefficient) in terms.items():
            block = coefficients[name][k]
            block[0] += constant
            block[1] += coefficient
            block[2] += abs(coefficient)
            if label is None:
                low, high = min(constant, constant + coefficient), max(constant, constant + coefficient)
            else:
                low = high = constant + coefficient * label
            chronology[name][0] += low
            chronology[name][1] += high
        counts.update(positions=1, selected_positions=int(row["selected"]),
                      chronology_unresolved_positions=int(label is None),
                      retrospective_known_positions=int(k in known),
                      retrospectively_resolved_positions=int(label is None and k in known))
    require(n_live == report["n_live"], "live_denominator", unit["id"])
    require(set(prior) == set(known), "complete_paid_label_map", unit["id"])
    require(chronology["Z"] == [0, n_live], "terminal_chronology_envelope", unit["id"])
    endpoints = {}
    for name, groups in coefficients.items():
        det = [rat(value) for value in report["deterministic_envelopes"][name]]
        require(chronology[name] == det, "original_deterministic_envelope", [unit["id"], name])
        low = high = position_width = cancellation = F(0)
        for k, (constant, coefficient, absolute_sum) in groups.items():
            if k in known:
                low += constant + coefficient * known[k]
                high += constant + coefficient * known[k]
            else:
                low += constant + min(F(0), coefficient)
                high += constant + max(F(0), coefficient)
                position_width += absolute_sum
                cancellation += absolute_sum - abs(coefficient)
        grouped_width = high - low
        det_width = det[1] - det[0]
        receipt_gain = det_width - position_width
        require(det[0] <= low <= high <= det[1], "retrospective_containment", [unit["id"], name])
        require(receipt_gain >= 0 and cancellation >= 0
                and det_width - grouped_width == receipt_gain + cancellation,
                "nonnegative_gain_decomposition", [unit["id"], name])
        delivered = report["intervals"][name]
        delivered_low, delivered_high = rat(delivered["lower"]), rat(delivered["upper"])
        conflict = bool(delivered.get("confidence_conflict")) or delivered_low > delivered_high
        center = rat(report["live_centers"]["V" if name == "Z" else name])
        radius = rat(report["sampling_radius"]) + (report["action_radius"] if name == "Z" else 0)
        covering_radius = max(center - det[0], det[1] - center)
        if n_live:
            require((delivered_low, delivered_high) == (max(center - radius, det[0]), min(center + radius, det[1])),
                    "delivered_intersection_rule", [unit["id"], name])
        widths = {"original_deterministic_width": det_width,
                  "frozen_delivered_width": None if conflict else delivered_high - delivered_low,
                  "end_position_width": position_width, "end_key_width": grouped_width,
                  "retrospective_receipt_gain": receipt_gain, "same_key_cancellation_gain": cancellation,
                  "total_deterministic_gain": det_width - grouped_width,
                  "frozen_width_minus_end_key_width": None if conflict else delivered_high - delivered_low - grouped_width}
        endpoints[name] = {"public_only_lower": low, "public_only_upper": high,
            "original_deterministic_lower": det[0], "original_deterministic_upper": det[1],
            "confidence_conflict": conflict, "widths": widths,
            "normalized": {field: None if value is None else value / t for field, value in widths.items()},
            "sampling_radius": radius, "radius_required_to_cover_original_envelope": covering_radius,
            "radius_slack_over_full_envelope": radius - covering_radius,
            "exact_all_remaining_known": n_live == 0,
            "frozen_sampling_interval_equals_its_deterministic_envelope": (delivered_low, delivered_high) == tuple(det)}
    return dict(header, status="available", n_live=n_live, counts=dict(counts),
                paid_known_keys=len(known), all_distinct_keys=len(all_keys),
                unresolved_distinct_keys=len(all_keys - known.keys()), endpoints=endpoints)


def aggregate(records, family_by_group):
    cells = defaultdict(list)
    for row in records:
        cells[(family_by_group[row["group_id"]], row["configuration_id"], canonical(row["stakes"]).decode().strip())].append(row)
    results = []
    for (family, configuration, stakes), rows in sorted(cells.items()):
        complete = all(r["status"] == "available" for r in rows)
        result = {"family": family, "configuration_id": configuration, "stakes": json.loads(stakes),
                  "planned_reports": len(rows), "available_reports": sum(r["status"] == "available" for r in rows),
                  "complete_denominator": complete, "endpoints": {},
                  "weighting": "equal scheduled seed slots within population, then equal populations",
                  "unit_ids": [r["unit_id"] for r in rows]}
        if complete:
            for name in ("F", "V", "Z"):
                fields = rows[0]["endpoints"][name]["normalized"]
                means = {}
                for field in fields:
                    populations = defaultdict(list)
                    for row in rows:
                        populations[row["group_id"]].append(row["endpoints"][name]["normalized"][field])
                    if any(v is None for values in populations.values() for v in values):
                        means[field] = None
                    else:
                        means[field] = sum((sum(values, F(0)) / len(values) for values in populations.values()), F(0)) / len(populations)
                result["endpoints"][name] = {"means_per_scheduled_horizon": means,
                    "reports_with_sampling_tightening": sum(not r["endpoints"][name]["frozen_sampling_interval_equals_its_deterministic_envelope"] for r in rows),
                    "reports_with_receipt_gain": sum(r["endpoints"][name]["widths"]["retrospective_receipt_gain"] > 0 for r in rows),
                    "reports_with_cancellation_gain": sum(r["endpoints"][name]["widths"]["same_key_cancellation_gain"] > 0 for r in rows)}
        results.append(result)
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    parser.add_argument("--numeric", help="Optional completed independent numeric observer results.json for subsequent validation.")
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=False)
    start = stamp()
    try:
        for stage in ("inputs", "public", "evaluation", "analysis"):
            marker = FINAL / "stages" / stage / "complete.json"
            require(marker.is_file(), "frozen_stage_barrier", stage)
            read(marker)
        schedule = read(REPO / "v3/experiments/frozen_v1/schedule.json")
        families = {g["id"]: g["recipe"]["family"] for g in schedule["groups"] if g["arm"] == "broker"}
        records, paid_by_id = [], {}
        for unit in schedule["units"]:
            if unit["arm"] != "broker" or unit["engine"] not in ("broker", "mirror"):
                continue
            public, _ = sealed("public", unit["id"])
            require(public["unit"] == unit, "unchanged_scheduled_unit", unit["id"])
            paid = public["value"]["paid_result"]
            require(paid["unit"] == unit, "paid_unit_binding", unit["id"])
            paid_by_id[unit["id"]] = paid
            records.append(audit(unit, paid))
        public_result = {"schema": "value_logic.p310.retrospective_public_bounds.v1",
            "contributor": "ChatGPT (GPT-6 Astra Pro)", "status": "PASS", "start": start,
            "public_only_completion": stamp(), "source_sha256": digest(Path(__file__)),
            "checks_by_kind": dict(CHECKS), "source_records": dict(SOURCES),
            "planned_reports": len(records), "records": records, "summaries": aggregate(records, families),
            "private_truth_reads_before_bounds_saved": 0,
            "frozen_endpoint_replacement": False, "economic_advantage_claim": False,
            "fair_bits_or_coverage_inferred": False,
            "uncertainty_set": "One binary label per unresolved full semantic key; a relaxation, not all logically realizable CNF worlds."}
        bounds_path = out / "public_bounds.json"
        save(bounds_path, public_result)
        validation = {"public_bounds_sha256": digest(bounds_path), "private_validation_requested": bool(args.numeric)}
        if args.numeric:
            private_start = stamp()
            numeric_path = Path(args.numeric).resolve()
            numeric = read(numeric_path)
            require(numeric["status"] == "PASS", "independent_numeric_source_passed", str(numeric_path))
            truths_by_id = {r["unit_id"]: [x["truth"] for block in r["blocks"] for x in block["rows"]]
                            for r in numeric["per_episode"]}
            private_checks = []
            for record in records:
                if record["status"] != "available":
                    continue
                identifier = record["unit_id"]
                rows, truths = paid_by_id[identifier]["episode"]["trace"], truths_by_id[identifier]
                require(len(rows) == len(truths) == record["horizon"], "private_target_denominator", identifier)
                targets = {"F": sum(((rat(r["emitted_q"]) - y) ** 2 for r, y in zip(rows, truths)), F(0)),
                           "V": sum((rat(r["emitted_q"]) + (1 - 2 * rat(r["emitted_q"])) * y for r, y in zip(rows, truths) if not r["selected"]), F(0)),
                           "Z": F(sum(r["terminal_action"] != y for r, y in zip(rows, truths)))}
                for name, target in targets.items():
                    endpoint = record["endpoints"][name]
                    require(endpoint["public_only_lower"] <= target <= endpoint["public_only_upper"],
                            "subsequent_private_target_containment", [identifier, name])
                scored, _ = sealed("evaluation", "score-" + identifier)
                score = scored["value"]["score"]
                require(targets["F"] == rat(score["issued_brier_sum"]) and targets["Z"] == score["terminal_errors"],
                        "private_frozen_target_agreement", identifier)
                private_checks.append({"unit_id": identifier, "targets": targets, "all_contained": True})
            validation.update(private_start=private_start, private_end=stamp(),
                              numeric_source_sha256=digest(numeric_path), validated_reports=len(private_checks),
                              checks=private_checks, bounds_unchanged_after_validation=digest(bounds_path) == validation["public_bounds_sha256"])
        validation.update(end=stamp(), status="PASS", checks_by_kind=dict(CHECKS))
        save(out / "validation.json", validation)
        print(json.dumps({"status": "PASS", "planned_reports": len(records),
                          "available_reports": sum(r["status"] == "available" for r in records),
                          "configuration_summaries": len(public_result["summaries"]),
                          "public_bounds_sha256": validation["public_bounds_sha256"],
                          "checks_total": sum(CHECKS.values()), "private_validated": bool(args.numeric)}, indent=2))
    except BaseException as error:
        save(out / "failure.json", {"status": "OBSERVER_FAILURE", "start": start, "end": stamp(),
            "source_sha256": digest(Path(__file__)), "error_type": type(error).__name__, "error": str(error),
            "traceback": traceback.format_exc(), "checks_completed": dict(CHECKS),
            "scientific_stage_failure": False})
        raise


if __name__ == "__main__":
    main()
