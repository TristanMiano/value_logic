#!/usr/bin/env python3
"""Independent P3-10 certificate observer; JSON input only, no worker imports.

Contributor/reviewer: ChatGPT (GPT-6 Astra Pro), certificate reconstruction
agent, 2026-10-11. Same-model, source-aware reconstruction; zero principal
clock credit. This script neither generates cases nor calls any frozen paid
method, private scorer, or analyzer. It is run only after the principal releases
the completed mixed-provenance public/evaluation/analysis stages under P3-10-A1.
Its expression-table interpretation is
an independent observer of already exposed JSON, never deployed service.
"""
from __future__ import annotations

import argparse
import base64
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import resource
import sys
import time
import traceback

SIGNATURE = "ChatGPT (GPT-6 Astra Pro), /root/certificate_reconstruction"
COVERAGE = "ENTIRE_CURRENT_INCUMBENT_SUBLEVEL_INCLUDING_ALL_MINIMIZERS"
EXPECTED_MANIFEST = "69d4d4a84c649698a006bce00a87b0038d5f7d19f2da4e96e6ef3d4e42e37c70"
EXPECTED_PROTOCOL = "dde9fe405ad39e65db3d49cb47d298e3ab6e498d7c5c485ff215ff884466b88f"
READS = {}
ROOT = None


def canonical(value, newline=False):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True, allow_nan=False)
            + ("\n" if newline else "")).encode("ascii")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def object_digest(value):
    return digest(canonical(value, newline=True))


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def pairs(items):
    result = {}
    for key, value in items:
        require(key not in result, "Duplicate JSON key: " + key)
        result[key] = value
    return result


def loads(text):
    def reject(value):
        raise ValueError("Nonfinite JSON value: " + value)
    return json.loads(text, object_pairs_hook=pairs, parse_constant=reject)


def read(path, *, json_value=True):
    path = Path(path)
    data = path.read_bytes()
    key = str(path.resolve().relative_to(ROOT)) if path.resolve().is_relative_to(ROOT) else str(path.resolve())
    record = {"path": key, "bytes": len(data), "sha256": digest(data)}
    require(key not in READS or READS[key] == record, "Input changed during observer: " + key)
    READS[key] = record
    return loads(data) if json_value else data


def rational_pair(value):
    value = Fraction(value)
    return [value.numerator, value.denominator]


def when(value):
    return datetime.fromisoformat(value)


def table_for_expression(expression, points):
    """Evaluate a whole assignment table directly from the JSON syntax tree.

    This uses independent vector tables and exact fractions, with no imported
    Frame, interval, ADD, certificate checker, generator, or scalar reference.
    """
    memo = {}

    def visit(node):
        key = canonical(node)
        if key in memo:
            return memo[key]
        operation = node[0]
        if operation == "lit":
            result = (Fraction(node[1]),) * len(points)
        elif operation == "bit":
            require(type(node[1]) is int, "Integer coordinate required")
            result = tuple(Fraction(point[node[1]]) for point in points)
        elif operation == "not":
            result = tuple(1 - value for value in visit(node[1]))
        elif operation == "scale":
            result = tuple(Fraction(node[1]) * value for value in visit(node[2]))
        else:
            left, right = visit(node[1]), visit(node[2])
            operations = {
                "add": lambda a, b: a + b,
                "min": min,
                "max": max,
                "eq": lambda a, b: Fraction(a == b),
                "and": lambda a, b: Fraction(a == b == 1),
                "or": lambda a, b: Fraction(a == 1 or b == 1),
            }
            require(operation in operations, "Unknown JSON expression operation")
            result = tuple(operations[operation](a, b) for a, b in zip(left, right))
        memo[key] = result
        return result

    return visit(expression)


def interpret_case(case):
    frame = loads(case["frame_record"])
    require(canonical(frame).decode("ascii") == case["frame_record"], "Noncanonical frame")
    request = frame["request"]
    nbits = request["nbits"]
    require(type(nbits) is int and 1 <= nbits <= 10, "Finite observer dimension")
    points = tuple(itertools.product((0, 1), repeat=nbits))
    witness = tuple(case["witness"])
    require(witness in points, "Complete supplied witness required")
    hard = [table_for_expression(formula, points) for formula in request["hard"]]
    feasible = tuple(all(values[index] == 1 for values in hard) for index in range(len(points)))
    ranks = [Fraction(0)] * len(points)
    for soft in request["soft"]:
        require(soft["tier"] == 0 and Fraction(soft["weight"]) > 0,
                "Positive single-tier rank required")
        values = table_for_expression(soft["formula"], points)
        ranks = [old + Fraction(soft["weight"]) * (1 - value)
                 for old, value in zip(ranks, values)]
    loss = table_for_expression(dict(request["losses"])[frame["loss"]], points)
    wi = points.index(witness)
    require(feasible[wi], "Supplied incumbent must be feasible")
    cutoff = ranks[wi]
    eligible = [i for i in range(len(points)) if feasible[i]]
    domain = [i for i in eligible if ranks[i] <= cutoff]
    require(domain, "Current sublevel must be nonempty")
    minimum_rank = min(ranks[i] for i in eligible)
    minimizers = [i for i in eligible if ranks[i] == minimum_rank]
    lower = min(loss[i] for i in domain)
    upper = max(loss[i] for i in domain)
    bad = [i for i in domain if loss[i] > Fraction(case["bound"])]
    diagnostics = {
        "assignments_enumerated": len(points), "hard_domain_count": len(eligible),
        "sublevel_count": len(domain), "minimum_rank": str(minimum_rank),
        "minimizer_count": len(minimizers), "exact_lower": str(lower), "exact_upper": str(upper),
        "lower_witness": list(points[next(i for i in domain if loss[i] == lower)]),
        "upper_witness": list(points[next(i for i in domain if loss[i] == upper)]),
        "counterexample": list(points[bad[0]]) if bad else None,
    }
    return {
        "frame": frame, "request_id": case.get("id"), "frame_sha256": digest(case["frame_record"].encode("ascii")),
        "bound": str(Fraction(case["bound"])), "incumbent_rank": str(cutoff),
        "holds": not bad, "status": "CURRENT_BOUND_CERTIFIED" if not bad else "BOUND_VIOLATED",
        "diagnostics": diagnostics,
        "incumbent_is_minimizer": cutoff == minimum_rank,
        "minimizers_are_all_in_sublevel": set(minimizers).issubset(domain),
        "strictly_nonoptimal_sublevel_members": sum(ranks[i] > minimum_rank for i in domain),
        "sublevel_assignments": [list(points[i]) for i in domain],
        "full_assignment_loss_values": [str(value) for value in loss],
    }


def check_source_recipe_expectations(payload, current, old):
    """Check the source-only derivation fixed before the final-data release."""
    nbits = payload["nbits"]
    require(nbits in (4, 7), "Frozen structural dimension")
    total = 1 << nbits
    hard = 3 * total // 4
    minima = 3 * total // 8
    counts = [(total, total, total, "0"), (hard, minima, minima, "0"),
              (hard, hard, minima, "1"), (hard, minima, minima, "0")]
    points = tuple(itertools.product((0, 1), repeat=nbits))
    for index, (item, (hard_count, sub_count, min_count, cutoff)) in enumerate(zip(current, counts)):
        diagnostic = item["diagnostics"]
        expected = {"assignments_enumerated": total, "hard_domain_count": hard_count,
                    "sublevel_count": sub_count, "minimum_rank": "0", "minimizer_count": min_count,
                    "exact_lower": "-1/2" if index == 3 else "-1",
                    "exact_upper": "3/2" if index == 3 else "1", "counterexample": None}
        require(all(diagnostic[key] == value for key, value in expected.items()),
                "Observed current domain/loss differs from pre-result source derivation")
        require(item["incumbent_rank"] == cutoff and item["bound"] == ("3/2" if index == 3 else "1"),
                "Observed cutoff or bound differs from source derivation")
        shift = Fraction(1, 2) if index == 3 else Fraction(0)
        exact_loss = [str(2 * point[0] - 1 + shift) for point in points]
        require(item["full_assignment_loss_values"] == exact_loss,
                "Structural identity fails at an actual full-cube assignment")
    require(len(old) == 2, "Two complementary old domains required")
    for index, item in enumerate(old):
        diagnostic = item["diagnostics"]
        sign = str(2 * index - 1)
        expected = {"assignments_enumerated": total, "hard_domain_count": total // 2,
                    "sublevel_count": total // 2, "minimum_rank": "0", "minimizer_count": total // 2,
                    "exact_lower": sign, "exact_upper": sign, "counterexample": None}
        require(all(diagnostic[key] == value for key, value in expected.items())
                and item["incumbent_rank"] == "0" and item["bound"] == sign,
                "Observed old domain/loss differs from source derivation")
        require(all(point[0] == index for point in item["sublevel_assignments"]),
                "Old domain selector half-cube mismatch")
    return True


def invoice_from_rows(invoice, unit):
    stages = invoice["by_stage"]
    primitive, consumer = Counter(), 0
    stage_totals = {}
    for name, category_counts in stages.items():
        require(type(name) is str and type(category_counts) is dict, "Stage category map required")
        require(all(type(value) is int and value >= 0 for value in category_counts.values()),
                "Nonnegative integer category counts required")
        primitive.update(category_counts)
        amount = sum(category_counts.values())
        stage_totals[name] = amount
        if name.startswith("receiver_") or name in {"terminal", "failure_terminal", "common_source"}:
            consumer += amount
    total = sum(primitive.values())
    require(total == invoice["total_units"], "Raw invoice total mismatch")
    require(consumer == invoice["consumer_units"], "Raw invoice consumer mismatch")
    require(invoice["budget"] == unit["budget"] and invoice["consumer_budget"] == unit["consumer_budget"],
            "Actual account differs from frozen schedule")
    require(total <= unit["budget"] and consumer <= total, "Total budget exceeded")
    require(unit["consumer_budget"] is None or consumer <= unit["consumer_budget"], "Consumer cap exceeded")
    require(invoice["failure_terminal_reserve"] == 1024, "Failure reserve changed")
    if invoice["failure"] is not None:
        require(stages.get("failure_terminal") == {
            "delivery_events": 1, "state_eviction_events": 1, "terminal_bytes": 111},
            "Failed service omitted exact terminal/eviction bill")
    else:
        require("failure_terminal" not in stages, "Successful service billed failure terminal")
    named = {
        "producer": total - consumer,
        "consumer": consumer,
        "output": sum(value for name, value in primitive.items()
                      if name.endswith("_output_bytes") or name == "terminal_bytes"),
        "storage": primitive.get("live_serialized_byte_periods", 0),
        "source": sum(stages.get("common_source", {}).values()),
    }
    require(named["producer"] + named["consumer"] == total, "Partition mismatch")
    return {"total_units": total, "consumer_units": consumer,
            "category_totals": dict(sorted(named.items())),
            "tariff_category_totals": dict(sorted(primitive.items())),
            "stage_totals": dict(sorted(stage_totals.items()))}


def bound_repo_path(relative):
    require(type(relative) is str, "String bound path required")
    path = Path(relative)
    require(not path.is_absolute() and ".." not in path.parts and path.as_posix() == relative,
            "Noncanonical repository-relative bound path")
    full = ROOT / path
    require(full.is_file() and not full.is_symlink(), "Missing or symbolic bound path: " + relative)
    return full


def stage_identity(final, stage_name, expected_units, expected_binding):
    stage = final / "stages" / stage_name
    schedule = read(stage / "schedule.json")
    require(schedule["units"] == expected_units, stage_name + " schedule mismatch")
    identity = {"stage": stage_name, "binding": expected_binding,
                "schedule_sha256": object_digest(expected_units)}
    require(all(schedule[key] == value for key, value in identity.items()),
            "Stage source/configuration/schedule binding mismatch")
    return identity


def sealed_unit(final, stage_name, unit, identity, selected, expected_entry=None):
    directory = final / "stages" / stage_name / "units" / unit["id"]
    matches = list(directory.glob("attempt_*/seal.json"))
    require(len(matches) == 1, "Exactly one seal per completed unit required: " + unit["id"])
    seal_path = matches[0]
    seal_relative = str(seal_path.relative_to(final))
    seal_bytes = read(seal_path, json_value=False)
    if expected_entry is not None:
        require(expected_entry == {"unit_id": unit["id"], "path": seal_relative,
                                   "sha256": digest(seal_bytes)}, "Completion seal pointer mismatch")
    seal = loads(seal_bytes)
    require(seal["identity"] == identity and seal["unit_sha256"] == object_digest(unit),
            "Sealed unit identity mismatch")
    require(type(seal["attempt"]) is int and seal_path.parent.name == "attempt_%02d" % seal["attempt"],
            "Seal attempt path mismatch")
    start_bytes = read(seal_path.parent / "start.json", json_value=False)
    require(digest(start_bytes) == seal["start_sha256"], "Start-receipt hash mismatch")
    start = loads(start_bytes)
    require(start["identity"] == identity and start["unit"] == unit and start["attempt"] == seal["attempt"],
            "Unit start binding mismatch")
    result_path = seal_path.parent / "result.json"
    result_bytes = read(result_path, json_value=False)
    require(digest(result_bytes) == seal["result_sha256"], "Completed-result hash mismatch")
    result = loads(result_bytes)
    require(result["identity"] == identity and result["unit"] == unit and result["attempt"] == seal["attempt"],
            "Completed-result binding mismatch")
    require(result["started_utc"] == start["started_utc"]
            and when(start["started_utc"]) <= when(result["finished_utc"]) <= when(seal["sealed_utc"]),
            "Start/result/seal chronology mismatch")
    if not selected:
        # All result bytes and outer identities are independently validated.
        # Keep only cross-stage links for unselected (noncertificate) values.
        value = result["value"]
        result = {key: item for key, item in result.items() if key != "value"}
        result["value"] = {key: value[key] for key in ("input_result_sha256", "public_result_sha256") if key in value}
    return {"result": result, "seal": seal, "start": start,
            "seal_path": seal_relative, "seal_sha256": digest(seal_bytes),
            "result_path": str(result_path.relative_to(final))}


def stage_summary(stage_name, expected_units, records, selected_ids, *, complete):
    return {"stage": stage_name, "scheduled_units": len(expected_units),
            "sealed_units": len(records), "selected_result_count": len(set(records) & set(selected_ids)),
            "all_schedule_seals_starts_and_result_hashes_validated": complete,
            "stage_completion_index_required": complete,
            "earliest_start_utc": min(when(row["start"]["started_utc"]) for row in records.values()).isoformat(),
            "latest_seal_utc": max(when(row["seal"]["sealed_utc"]) for row in records.values()).isoformat()}


def stage_records(final, stage_name, expected_units, selected_ids, expected_binding):
    identity = stage_identity(final, stage_name, expected_units, expected_binding)
    stage = final / "stages" / stage_name
    complete = read(stage / "complete.json")
    require(all(complete[key] == value for key, value in identity.items()), "Completion identity mismatch")
    require(complete["expected_units"] == complete["completed_units"] == len(expected_units),
            "Incomplete stage cannot be observed")
    require(len(complete["seals"]) == len(expected_units), "Completion index length mismatch")
    index = {item["unit_id"]: item for item in complete["seals"]}
    require(len(index) == len(expected_units), "Duplicate completion-index units")
    require([item["unit_id"] for item in complete["seals"]] == [unit["id"] for unit in expected_units],
            "Completion roster/order mismatch")
    directories = {path.name for path in (stage / "units").iterdir() if path.is_dir()}
    require(directories == set(index), "Unscheduled or missing stage unit directory")
    records = {unit["id"]: sealed_unit(final, stage_name, unit, identity, unit["id"] in selected_ids,
                                      index[unit["id"]]) for unit in expected_units}
    return records, stage_summary(stage_name, expected_units, records, selected_ids, complete=True)


def reference_for(unit_id, row, final, evidence_class):
    return {"unit_id": unit_id, "origin_root": str(final.relative_to(ROOT)),
            "seal_path": row["seal_path"], "seal_sha256": row["seal_sha256"],
            "result_path": row["result_path"], "result_sha256": row["seal"]["result_sha256"],
            "evidence_class": evidence_class}


def amended_lineage(repo, release, schedule, config, selected_groups, selected_units):
    """Validate explicit A1 dual provenance without importing the continuation."""
    original = repo / "v3/experiments/final_v1"
    amended = repo / "v3/experiments/final_v1_amended_A1"
    amendment_dir = repo / "v3/experiments/amendments/P3_10_A1"
    original_binding = {"freeze_id": config["freeze_id"], "manifest_sha256": EXPECTED_MANIFEST,
                        "protocol_sha256": EXPECTED_PROTOCOL}
    manifest_bytes = read(amendment_dir / "manifest.json", json_value=False)
    manifest_hash = digest(manifest_bytes)
    manifest = loads(manifest_bytes)
    require(release["amendment_id"] == manifest["amendment_id"] == "P3-10-A1"
            and release["amendment_manifest_sha256"] == manifest_hash,
            "Principal release must explicitly bind the sealed A1 manifest")
    require(manifest["status"] == "SEALED_BEFORE_AMENDED_EXECUTION"
            and manifest["original_manifest_sha256"] == EXPECTED_MANIFEST
            and manifest["original_protocol_sha256"] == EXPECTED_PROTOCOL,
            "Unexpected amendment identity or original freeze")
    amended_binding = dict(original_binding, amendment_id="P3-10-A1",
                           amendment_manifest_sha256=manifest_hash)
    require(read(amended / "amendment_binding.json") == amended_binding, "Wrong flat amendment binding")
    for filename, field in (("protocol.json", "amendment_protocol_sha256"),
                            ("protocol.md", "amendment_prose_sha256")):
        require(digest(read(amendment_dir / filename, json_value=False)) == manifest[field],
                "Amendment protocol bytes differ")
    require(len({row["path"] for row in manifest["new_sources"]}) == len(manifest["new_sources"]),
            "Duplicate amendment source path")
    require("v3/experiments/amendments/P3_10_A1/continue.py" in {row["path"] for row in manifest["new_sources"]},
            "Amendment driver missing from source binding")
    for source in manifest["new_sources"]:
        require(source["path"].startswith("v3/experiments/amendments/P3_10_A1/"),
                "Amendment source unexpectedly replaces an original source")
        data = read(bound_repo_path(source["path"]), json_value=False)
        require(len(data) == source["bytes"] and digest(data) == source["sha256"], "Amended source changed")
    actual_original_paths = {str(path.relative_to(repo)) for path in original.rglob("*")
                             if path.is_file() and path.name != "writer.lock"}
    evidence_rows = manifest["original_evidence"]
    require(len({row["path"] for row in evidence_rows}) == len(evidence_rows)
            and actual_original_paths == {row["path"] for row in evidence_rows},
            "Original evidence inventory was replaced, extended or truncated")
    for row in evidence_rows:
        data = read(bound_repo_path(row["path"]), json_value=False)
        require(len(data) == row["bytes"] and digest(data) == row["sha256"],
                "Pre-amendment original evidence changed")
    require(not (original / "stages/public/complete.json").exists()
            and not (original / "stages/evaluation").exists()
            and not (original / "stages/analysis").exists(),
            "Incomplete original lineage was altered into a completion or scoring path")
    require(not (amended / "stages/inputs").exists(), "Amendment unexpectedly generated another input stage")
    exposure_bytes = read(original / "exposure.json", json_value=False)
    require(loads(exposure_bytes)["binding"] == original_binding, "Original exposure has wrong binding")
    failure_bytes = read(original / "stages/public/attempts/attempt_01/failure.json", json_value=False)
    require(digest(failure_bytes) == manifest["original_failure_sha256"], "Original failure changed")
    failure = loads(failure_bytes)
    groups, all_units = schedule["groups"], schedule["units"]
    retained_units = [unit for unit in all_units if unit["arm"] in ("broker", "certificates")]
    remaining = [unit for unit in all_units if unit["arm"] == "conformance"]
    require(len(groups) == 12 and len(all_units) == 500 and len(retained_units) == 440 and len(remaining) == 60,
            "Original finite roster changed")
    require(manifest["remaining_public_units"] == remaining
            and manifest["reused_public_unit_ids"] == [unit["id"] for unit in retained_units],
            "Amendment changes retained/remaining original units")
    require(failure["error_type"] == "AttributeError" and failure["failed_unit_id"] == remaining[0]["id"],
            "Original failure is outside the source-reviewed A1 initialization scope")
    inputs, input_stage = stage_records(original, "inputs", groups, selected_groups, original_binding)
    require(when(loads(exposure_bytes)["created_utc"]) <= when(input_stage["earliest_start_utc"]),
            "Original exposure marker postdates input generation")
    input_reference = read(amended / "input_reference.json")
    require(input_reference["schema"] == "value_logic.p310_a1.input_reference.v1"
            and input_reference["binding"] == amended_binding
            and input_reference["expected_units"] == input_reference["completed_units"] == 12
            and input_reference["new_generations"] == 0
            and input_reference["original_exposure_sha256"] == digest(exposure_bytes)
            and input_reference["seals"] == [reference_for(group["id"], inputs[group["id"]], original,
                 "original_prospective_input") for group in groups], "Input-reference provenance mismatch")
    original_identity = stage_identity(original, "public", all_units, original_binding)
    original_records = {unit["id"]: sealed_unit(original, "public", unit, original_identity,
                       unit["id"] in selected_units) for unit in retained_units}
    actual_sealed_original = {path.parent.parent.name for path in (original / "stages/public/units").glob("*/attempt_*/seal.json")}
    require(actual_sealed_original == set(original_records), "Original sealed public subset differs")
    original_stage = stage_summary("original_public_incomplete", all_units, original_records, selected_units, complete=False)
    original_stage["all_440_retained_seals_starts_and_result_hashes_validated"] = True
    amended_records, amended_stage = stage_records(amended, "public", remaining, set(), amended_binding)
    amended_stage["stage"] = "amended_public_conformance"
    public = dict(original_records, **amended_records)
    references = [reference_for(unit["id"], public[unit["id"]],
                  original if unit["id"] in original_records else amended,
                  "original_prospective_unchanged_public_record" if unit["id"] in original_records
                  else "post_exposure_amended_inherited_conformance") for unit in all_units]
    composite = read(amended / "composite_public.json")
    require(composite["schema"] == "value_logic.p310_a1.composite_public.v1"
            and composite["binding"] == amended_binding
            and composite["expected_units"] == composite["completed_units"] == 500
            and composite["original_units"] == 440 and composite["amended_units"] == 60
            and composite["original_public_stage_complete"] is False
            and composite["original_failure_sha256"] == digest(failure_bytes)
            and composite["seals"] == references, "Composite public barrier/provenance mismatch")
    public_stage = stage_summary("composite_public", all_units, public, selected_units, complete=True)
    public_stage["stage_completion_index_required"] = False
    public_stage["composite_seal_reference_required"] = True
    all_score_units = [dict(unit, id="score-" + unit["id"], public_unit_id=unit["id"]) for unit in all_units]
    evaluation, evaluation_stage = stage_records(amended, "evaluation", all_score_units,
                                                {"score-" + item for item in selected_units}, amended_binding)
    require(when(input_stage["latest_seal_utc"]) <= when(public_stage["earliest_start_utc"]),
            "Public execution preceded all original input seals")
    require(when(public_stage["latest_seal_utc"]) <= when(evaluation_stage["earliest_start_utc"]),
            "Private evaluation preceded the complete mixed-provenance public barrier")
    require(when(evaluation_stage["latest_seal_utc"]) <= when(release["recorded_utc"]),
            "Observation release preceded evaluation completion")
    for unit in all_units:
        input_hash = inputs[unit["group_id"]]["seal"]["result_sha256"]
        pub = public[unit["id"]]
        score = evaluation["score-" + unit["id"]]
        require(pub["result"]["value"]["input_result_sha256"] == input_hash
                and score["result"]["value"]["input_result_sha256"] == input_hash
                and score["result"]["value"]["public_result_sha256"] == pub["seal"]["result_sha256"],
                "Composite input/public/evaluation result-byte link mismatch")
    unknown = []
    for final in (original, amended):
        for attempt in sorted((final / "stages/public/units").glob("*/attempt_*")):
            if not (attempt / "seal.json").is_file():
                start_path = attempt / "start.json"
                unknown.append({"stage": "public", "unit_id": attempt.parent.name,
                                "attempt_directory": attempt.name,
                                "start_sha256": digest(read(start_path, json_value=False)) if start_path.exists() else None,
                                "origin_root": str(final.relative_to(repo))})
    require(any(row["origin_root"] == str(original.relative_to(repo)) for row in unknown),
            "Original failed public prefix was erased")
    lineage = {"amendment_id": "P3-10-A1", "amendment_manifest_sha256": manifest_hash,
               "original_binding": original_binding, "amended_binding": amended_binding,
               "original_evidence_files_preserved": len(evidence_rows),
               "original_public_units_retained": len(original_records), "amended_conformance_units": len(amended_records),
               "input_generations_added": 0, "original_public_stage_complete": False,
               "all_500_score_input_and_public_links_independently_validated": True,
               "original_failure": {key: failure.get(key) for key in ("failed_unit_id", "error_type", "error",
                                     "unmeasured_failed_attempt_cost", "observed_utc")},
               "unknown_unsealed_public_attempts": unknown,
               "complete_outer_paid_attempt_accounting": False,
               "evidence_scope": "Original prospectively frozen unchanged broker/certificate paths; conformance and overall continuation amended"}
    return (inputs, public, evaluation, [input_stage, original_stage, amended_stage, public_stage, evaluation_stage], lineage)


def compare(left, right, *, complete_outer=True):
    covered_left = set(left["delivered_request_ids"])
    covered_right = set(right["delivered_request_ids"])
    require(set(left["all_request_ids"]) == set(right["all_request_ids"]), "Unequal planned coverage universes")
    eligible = (left["validity_pass"] and right["validity_pass"]
                and left["total_units"] is not None and right["total_units"] is not None)
    qualifies = eligible and bool(covered_left) and covered_left >= covered_right
    lt, rt = left["total_units"], right["total_units"]
    primitives = sorted(set(left["tariff_category_totals"]) | set(right["tariff_category_totals"]))
    named = sorted(set(left["category_totals"]) | set(right["category_totals"]))
    practical_path = bool(qualifies and rt > 0 and 20 * lt <= 19 * rt)
    return {
        "scope": left["scope"], "recipient": left["recipient"], "budget_condition": left["budget_condition"],
        "left": left["method"], "right": right["method"],
        "coverage_superset": covered_left >= covered_right,
        "identical_coverage": covered_left == covered_right,
        "both_complete": left["complete_service"] and right["complete_service"],
        "left_weakly_dominates": bool(qualifies and lt <= rt),
        "left_practical_cost_dominance": practical_path and complete_outer,
        "completed_path_cost_threshold_met": practical_path,
        "left_to_right_total_cost_ratio": rational_pair(Fraction(lt, rt)) if eligible and rt > 0 else None,
        "right_minus_left_total_units": rt - lt if eligible else None,
        "componentwise_named_diagnostic_dominance": bool(qualifies and named
            and set(left["category_totals"]) == set(right["category_totals"])
            and all(left["category_totals"][key] <= right["category_totals"][key] for key in named)),
        "componentwise_primitive_tariff_dominance": bool(qualifies and primitives
            and all(left["tariff_category_totals"].get(key, 0) <= right["tariff_category_totals"].get(key, 0)
                    for key in primitives)),
    }


def aggregate(rows, scope):
    unit = rows[0]["unit"]
    all_ids = [item for row in rows for item in row["all_request_ids"]]
    covered = [item for row in rows for item in row["delivered_request_ids"]]
    require(len(all_ids) == len(set(all_ids)) and len(covered) == len(set(covered)), "Repeated request in aggregate")
    named, primitive = Counter(), Counter()
    for row in rows:
        named.update(row["category_totals"])
        primitive.update(row["tariff_category_totals"])
    valid = all(row["validity_pass"] for row in rows)
    total = sum(row["total_units"] for row in rows)
    return {
        "scope": scope, "recipient": unit["recipient"], "budget_condition": unit["budget_condition"],
        "method": unit["method"], "method_kind": unit["method_kind"],
        "planned_histories": len(rows), "request_count": len(all_ids),
        "all_request_ids": sorted(all_ids), "delivered_request_ids": sorted(covered),
        "delivered_count": len(covered), "failed_count": len(all_ids) - len(covered),
        "validity_pass": valid, "complete_service": valid and set(all_ids) == set(covered),
        "known_all_attempt_units": total, "unknown_cost_histories": 0, "total_units": total,
        "category_totals": dict(sorted(named.items())),
        "tariff_category_totals": dict(sorted(primitive.items())), "category_totals_complete": True,
    }


def resource_price_comparison(direct, candidate):
    """Exploratory exact repricing of fixed logs, never another execution."""
    direct_categories = direct["tariff_category_totals"]
    candidate_categories = candidate["tariff_category_totals"]
    categories = sorted(set(direct_categories) | set(candidate_categories))
    delta = {key: direct_categories.get(key, 0) - candidate_categories.get(key, 0) for key in categories}
    d_total, c_total = direct["total_units"], candidate["total_units"]
    crossovers = []
    for key, difference in delta.items():
        if difference <= 0:
            continue
        # All other primitive prices remain one. Equality occurs at this
        # category's price, with direct service more expensive above it.
        price = Fraction(c_total - d_total + difference, difference)
        crossovers.append({"category": key, "ordinary_direct_minus_reuse_count": difference,
                           "equal_total_price_other_prices_one": rational_pair(price)})
    relation = compare(direct, candidate)
    return {
        "scope": direct["scope"], "recipient": direct["recipient"], "budget_condition": direct["budget_condition"],
        "covered_superset": relation["coverage_superset"], "identical_coverage": relation["identical_coverage"],
        "both_complete": relation["both_complete"],
        "ordinary_direct_minus_reuse_primitive_counts": delta,
        "ordinary_direct_cheaper_under_all_nonnegative_primitive_prices": relation["componentwise_primitive_tariff_dominance"],
        "ordinary_direct_worse_categories": [key for key in categories if delta[key] > 0],
        "ordinary_direct_better_categories": [key for key in categories if delta[key] < 0],
        "one_category_price_crossovers": crossovers,
        "interpretation": "dot(nonnegative primitive prices, ordinary_direct-minus-reuse counts) <= 0; exact fixed-record diagnostic, no new run",
    }


def selfcheck():
    # Deliberately synthetic, not a generator, service, source-bundle selfcheck,
    # final recipe, or paid method. These check observer aggregation logic.
    def row(method, delivered, total, primitive):
        return {"scope": "observer-DEVELOPMENT", "recipient": "fresh", "budget_condition": "full",
                "method": method, "all_request_ids": ["a", "b"], "delivered_request_ids": delivered,
                "validity_pass": True, "complete_service": set(delivered) == {"a", "b"},
                "total_units": total, "category_totals": {"producer": total, "consumer": 0},
                "tariff_category_totals": primitive}
    require(not compare(row("l", ["a"], 90, {"x": 90}), row("r", ["b"], 100, {"x": 100}))["left_practical_cost_dominance"],
            "Equal count is not equal coverage")
    require(not compare(row("l", [], 0, {}), row("r", [], 100, {"x": 100}))["left_weakly_dominates"],
            "Empty coverage must not dominate")
    require(compare(row("l", ["a", "b"], 95, {"x": 95}), row("r", ["a"], 100, {"x": 100}))["left_practical_cost_dominance"],
            "Exact 95-percent boundary must qualify")
    require(not compare(row("l", ["a"], 90, {"x": 80, "new": 10}), row("r", ["a"], 100, {"x": 100}))["componentwise_primitive_tariff_dominance"],
            "Absent categories must be zero")
    points = tuple(itertools.product((0, 1), repeat=2))
    require(table_for_expression(["add", ["bit", 0], ["scale", "-1/2", ["bit", 1]]], points)
            == (Fraction(0), Fraction(-1, 2), Fraction(1), Fraction(1, 2)), "Independent table arithmetic")
    return {"status": "PASS", "synthetic_checks": 5, "final_inputs_read": False,
            "paid_worker_or_private_scorer_or_generator_calls": 0, "principal_clock_credit_ns": 0}


def reconstruct(repo, release_path):
    global ROOT
    ROOT = repo
    release = read(release_path)
    require(release["principal_authorized_completed_stage_observation"] is True,
            "Principal completion release required before final observation")
    frozen = repo / "v3/experiments/frozen_v1"
    final = repo / "v3/experiments/final_v1"
    manifest_bytes = read(frozen / "manifest.json", json_value=False)
    protocol_bytes = read(repo / "v3/experiments/protocol.v1.json", json_value=False)
    require(digest(manifest_bytes) == EXPECTED_MANIFEST, "Unexpected frozen manifest")
    require(digest(protocol_bytes) == EXPECTED_PROTOCOL, "Unexpected frozen protocol")
    manifest, config = loads(manifest_bytes), loads(protocol_bytes)
    schedule_bytes = read(frozen / "schedule.json", json_value=False)
    require(digest(schedule_bytes) == manifest["schedule_sha256"], "Frozen schedule hash differs")
    schedule = loads(schedule_bytes)
    for source in manifest["sources"]:
        snapshot = read(frozen / "source" / source["path"], json_value=False)
        current = read(repo / source["path"], json_value=False)
        require(len(snapshot) == source["bytes"] and digest(snapshot) == source["sha256"], "Frozen source changed")
        require(current == snapshot, "Current source differs from frozen source")
    groups = [group for group in schedule["groups"] if group["arm"] == "certificates"]
    units = [unit for unit in schedule["units"] if unit["arm"] == "certificates"]
    require(len(groups) == 4 and len(units) == 104, "Certificate planned denominator changed")
    group_map = {group["id"]: group for group in groups}
    inputs, public, evaluation, stage_checks, lineage = amended_lineage(
        repo, release, schedule, config, set(group_map), {unit["id"] for unit in units})
    final = repo / "v3/experiments/final_v1_amended_A1"
    unknown_public = lineage["unknown_unsealed_public_attempts"]
    complete_outer = not unknown_public
    require(complete_outer is False, "A1 must preserve the unknown original paid prefix")
    cc = config["arms"]["certificates"]
    truths = {}
    input_diagnostics = []
    for group in groups:
        payload = inputs[group["id"]]["result"]["value"]
        require(payload["group_id"] == group["id"] and payload["recipe"] == group["recipe"], "Input recipe routing mismatch")
        require(payload["stage"] == "FINAL_EXPOSED" and len(payload["cases"]) == 4, "Final certificate input contract")
        current = [interpret_case(case) for case in payload["cases"]]
        old = [interpret_case(case) for case in payload["old_specs"]]
        check_source_recipe_expectations(payload, current, old)
        for case, result in zip(payload["cases"], current):
            truths[case["id"]] = result
        old_sets = [set(map(tuple, item["sublevel_assignments"])) for item in old]
        input_diagnostics.append({
            "group_id": group["id"], "recipe": group["recipe"],
            "current_requests": [{key: value for key, value in item.items() if key != "frame"} for item in current],
            "old_bound_diagnostics": [{key: value for key, value in item.items() if key != "frame"} for item in old],
            "old_domains_pairwise_disjoint": all(not (a & b) for a, b in itertools.combinations(old_sets, 2)),
            "old_domain_union_count": len(set().union(*old_sets)),
            "distinct_full_scope_records": len({case["frame_record"] for case in payload["cases"] + payload["old_specs"]}),
        })
    histories, attempts = [], []
    invoice_mismatches = []
    packet_count = 0
    for unit in units:
        group_id = unit["group_id"]
        payload = inputs[group_id]["result"]["value"]
        public_outer = public[unit["id"]]
        scored_outer = evaluation["score-" + unit["id"]]
        value = public_outer["result"]["value"]
        scored = scored_outer["result"]["value"]
        require(value["input_result_sha256"] == inputs[group_id]["seal"]["result_sha256"], "Public/input byte link mismatch")
        require(scored["input_result_sha256"] == inputs[group_id]["seal"]["result_sha256"], "Evaluation/input byte link mismatch")
        require(scored["public_result_sha256"] == public_outer["seal"]["result_sha256"], "Evaluation/public byte link mismatch")
        paid, score = value["paid_result"], scored["score"]
        require(paid["unit"] == score["unit"] == unit, "Inner configuration mismatch")
        require(paid["truth_reference_called"] is False and len(paid["rows"]) == 4, "Paid history contamination or missing attempts")
        require(paid["request_count"] == score["request_count"] == 4, "History denominator changed")
        history_attempts, delivered_ids = [], []
        source_enrollment_confirmed = False
        named, primitive = Counter(), Counter()
        for index, (case, raw, evaluated) in enumerate(zip(payload["cases"], paid["rows"], score["requests"]), 1):
            truth = truths[case["id"]]
            receipt_id = group_id + ":" + str(index)
            require(raw["request_id"] == receipt_id and raw["shared_request_id"] == case["id"]
                    and raw["request_index"] == index and raw["method"] == unit["method"]
                    and raw["recipient"] == unit["recipient"] and raw["stream"] == group_id,
                    "Attempt identity or current ordering differs")
            require(raw["observer_previous_receipt_stale"] is True, "Old receipt retained as current")
            invoice = invoice_from_rows(raw["invoice"], unit)
            require(raw["invoice"]["tariff"] == cc["tariff"], "Different certificate tariff")
            output = loads(raw["output"])
            require(evaluated["oracle"] == truth["diagnostics"], "Independent truth table differs from sealed scalar diagnostic")
            require(evaluated["incumbent_rank"] == truth["incumbent_rank"] and evaluated["truth_status"] == truth["status"],
                    "Sealed reference cutoff or truth status differs")
            require(evaluated["request_id"] == case["id"] and evaluated["receipt_id"] == receipt_id,
                    "Private diagnostic routing mismatch")
            if raw["status"] == "DELIVERED":
                expected = {
                    "schema": "rp3bb.current-bound.v1", "status": "CURRENT_BOUND_CERTIFIED",
                    "current_record": case["frame_record"], "bound": truth["bound"],
                    "incumbent_rank": truth["incumbent_rank"], "feasibility": "NONEMPTY", "coverage": COVERAGE,
                    "request_id": receipt_id, "unit": truth["frame"]["unit"], "witness": case["witness"],
                    "source_record": cc["expected_source_record"],
                }
                require(truth["holds"] and canonical(output) == canonical(expected), "False or wrong-scope delivered warrant")
                require(raw["observer_current_receipt_present"] is True and raw["invoice"]["failure"] is None
                        and raw["error"] is None, "Incorrect current-success state")
                delivered_ids.append(case["id"])
            else:
                require(raw["status"] == "NO_CURRENT_CERTIFICATE", "Unknown service outcome")
                require(output == {"schema": "rp3bb.current-bound.v1", "status": "NO_CURRENT_CERTIFICATE",
                                  "reason": "RESOURCE_OR_VALIDATION_FAILURE"}, "Wrong failure terminal")
                require(raw["observer_current_receipt_present"] is False and raw["invoice"]["failure"] is not None
                        and raw["error"] is not None, "Failed attempt published current certificate or lost failure")
            for packet in raw["audit_packets"]:
                captured = base64.b64decode(packet["payload_base64"], validate=True)
                require(len(captured) == packet["bytes"] and digest(captured) == packet["sha256"], "Captured packet hash mismatch")
                packet_count += 1
            require(evaluated["delivery_status"] == raw["status"] and evaluated["request_validity_pass"] is True,
                    "Sealed validity diagnostic disagrees")
            source_charge = invoice["stage_totals"].get("common_source", 0)
            post_enrollment_stages = sorted(name for name in invoice["stage_totals"]
                if name not in {"coordination", "common_source", "failure_terminal"})
            confirmed_before = source_enrollment_confirmed
            if confirmed_before:
                require(source_charge == 0, "Completed source enrollment was unexpectedly recharged")
            if post_enrollment_stages or raw["status"] == "DELIVERED":
                require(index != 1 or source_charge > 0, "First history reached service without source enrollment")
                source_enrollment_confirmed = True
            inferred_prior_installation = bool(index > 1 and not confirmed_before and source_charge == 0
                                               and post_enrollment_stages)
            classification = None
            eviction_size_check = None
            if raw["status"] == "NO_CURRENT_CERTIFICATE":
                require(raw["error"]["type"] == raw["invoice"]["failure"]["type"]
                        and raw["error"]["message"] == raw["invoice"]["failure"]["message"],
                        "Error and invoice failure descriptors disagree")
                classification = ("EXPECTED_DECLARED_BUDGET_EXHAUSTION" if raw["error"]["type"] == "ResourceExhausted"
                                  else "REQUIRES_SEPARATE_NONBUDGET_ERROR_DISPOSITION")
                old_requests = payload["old_specs"] if unit["method"] in {"P-REUSE", "O-ADD-PORTFOLIO"} else []
                evicted = {"source_record": cc["expected_source_record"], "epoch": "rp3bb:" + group_id,
                           "method": unit["method"], "input_adapter": cc["version"], "old_inputs": [],
                           "old_request_inputs": [{"frame_record": item["frame_record"], "witness": item["witness"],
                                                   "bound": item["bound"]} for item in old_requests],
                           "old_packets": [], "portfolio_domains": None, "add_manager": None,
                           "acknowledged_cursor": None}
                if unit["method"] == "O-ADD-WARM-PRUNED":
                    evicted["prune_limit_steps"] = cc["limits"]["pruner_dependency_steps"]
                eviction_size_check = len(canonical(evicted)) == raw["producer_retained_bytes"]
                require(eviction_size_check and raw["receiver_retained_bytes"] == 0,
                        "Post-failure retained sizes differ from evicted scientific-cache state")
            named.update(invoice["category_totals"])
            primitive.update(invoice["tariff_category_totals"])
            attempt = dict(invoice, unit_id=unit["id"], group_id=group_id,
                           method=unit["method"], recipient=unit["recipient"], budget_condition=unit["budget_condition"],
                           slot=index, request_id=case["id"], receipt_id=receipt_id,
                           status=raw["status"], failure=raw["invoice"]["failure"], error=raw["error"],
                           observer_previous_receipt_stale=raw["observer_previous_receipt_stale"],
                           audit_packet_count=len(raw["audit_packets"]),
                           source_enrollment_units_this_attempt=source_charge,
                           source_enrollment_confirmed_before=confirmed_before,
                           source_enrollment_confirmed_after=source_enrollment_confirmed,
                           prior_source_installation_inferred_from_no_recharge=inferred_prior_installation,
                           source_enrollment_evidence="Paid post-enrollment stages or success; complete prior enrollment persists through scientific-cache eviction",
                           paid_post_enrollment_stages=post_enrollment_stages,
                           follows_failed_attempt=bool(history_attempts and history_attempts[-1]["status"] != "DELIVERED"),
                           bootstrap_or_rebuild_stages=sorted(name for name in invoice["stage_totals"]
                               if name.startswith("bootstrap_") or name in {"producer_init", "producer_old_materialization"}),
                           producer_retained_bytes=raw["producer_retained_bytes"],
                           receiver_retained_bytes=raw["receiver_retained_bytes"],
                           producer_live_snapshot_bytes=raw["producer_live_snapshot_bytes"],
                           receiver_live_snapshot_bytes=raw["receiver_live_snapshot_bytes"],
                           post_failure_evicted_producer_record_size_consistent=eviction_size_check,
                           failure_classification=classification,
                           budget=unit["budget"], consumer_budget=unit["consumer_budget"])
            history_attempts.append(attempt)
            attempts.append(attempt)
        total = sum(attempt["total_units"] for attempt in history_attempts)
        ids = [case["id"] for case in payload["cases"]]
        checks = {"total_units": total, "consumer_units": named["consumer"],
                  "all_request_ids": ids, "delivered_request_ids": delivered_ids,
                  "full_service_delivered": len(delivered_ids) == 4,
                  "category_totals": dict(sorted(named.items())),
                  "tariff_category_totals": dict(sorted(primitive.items()))}
        for key, expected in checks.items():
            if score[key] != expected:
                invoice_mismatches.append({"unit_id": unit["id"], "field": key, "expected": expected, "observed": score[key]})
        require(score["validity_pass"] is True and score["status"] == "PASS" and score["errors"] == [], "Private certificate validity failed")
        require(score["category_totals_complete"] is True and score["failed_attempt_costs_included"] is True,
                "Incomplete paid invoice scope")
        histories.append(dict(checks, unit=unit, validity_pass=True, attempts=history_attempts))
    require(not invoice_mismatches, "Raw invoice reconstruction differs from score: " + str(invoice_mismatches[:2]))
    require(len(attempts) == 416, "Missing scheduled certificate attempt")
    buckets = defaultdict(list)
    for history in histories:
        unit = history["unit"]
        family = group_map[unit["group_id"]]["recipe"]["family"]
        for scope in (unit["group_id"], "family:" + family):
            buckets[(scope, unit["recipient"], unit["budget_condition"], unit["method"])].append(history)
    summaries = [aggregate(bucket, key[0]) for key, bucket in sorted(buckets.items())]
    cells = defaultdict(list)
    for summary in summaries:
        cells[(summary["scope"], summary["recipient"], summary["budget_condition"])].append(summary)
    comparisons = [compare(left, right, complete_outer=complete_outer)
                   for _, cell in sorted(cells.items()) for left in cell for right in cell
                   if left["method"] != right["method"]]
    prices = []
    ordinary_winners = []
    for key, cell in sorted(cells.items()):
        by_method = {item["method"]: item for item in cell}
        prices.append(resource_price_comparison(by_method["O-ENUM-RECEIVER"], by_method["P-REUSE"]))
        ordinary = [item for item in cell if item["method_kind"] == "ordinary" and item["complete_service"]]
        minimum = min((item["total_units"] for item in ordinary), default=None)
        ordinary_winners.append({"scope": key[0], "recipient": key[1], "budget_condition": key[2],
            "minimum_complete_ordinary_total_units": minimum,
            "all_tied_complete_ordinary_minimizers": sorted(item["method"] for item in ordinary if item["total_units"] == minimum),
            "candidate_delivered_count": by_method["P-REUSE"]["delivered_count"],
            "candidate_total_units": by_method["P-REUSE"]["total_units"]})
    per_history = {(h["unit"]["group_id"], h["unit"]["recipient"], h["unit"]["method"], h["unit"]["budget_condition"]): h
                   for h in histories}
    cap_comparisons = []
    for key, capped in sorted(per_history.items()):
        if key[-1] != "capped":
            continue
        full = per_history[key[:-1] + ("full",)]
        capped_set = set(capped["delivered_request_ids"])
        cap = capped["unit"]["consumer_budget"]
        retrospective = {attempt["request_id"] for attempt in full["attempts"]
                         if attempt["status"] == "DELIVERED" and attempt["consumer_units"] <= cap}
        cap_comparisons.append({
            "group_id": key[0], "recipient": key[1], "method": key[2],
            "full_statuses": [a["status"] for a in full["attempts"]],
            "actual_capped_statuses": [a["status"] for a in capped["attempts"]],
            "actual_capped_delivered_request_ids": sorted(capped_set),
            "full_trace_retrospective_threshold_ids": sorted(retrospective),
            "retrospective_equals_actual_ids": retrospective == capped_set,
            "full_total_units": full["total_units"], "actual_capped_total_units": capped["total_units"],
            "disposition": "Actual separately executed capped history is authoritative; retrospective flags are descriptive only",
        })
    prefixes = []
    for history in histories:
        unit = history["unit"]
        if unit["method"] != "P-REUSE":
            continue
        for other in histories:
            ou = other["unit"]
            if (ou["method"] == "P-REUSE" or (ou["group_id"], ou["recipient"], ou["budget_condition"])
                    != (unit["group_id"], unit["recipient"], unit["budget_condition"])):
                continue
            for length in range(1, 5):
                def prefix(source):
                    copy = dict(source)
                    kept = source["attempts"][:length]
                    named, primitive = Counter(), Counter()
                    for a in kept:
                        named.update(a["category_totals"])
                        primitive.update(a["tariff_category_totals"])
                    copy.update(all_request_ids=[a["request_id"] for a in kept],
                                delivered_request_ids=[a["request_id"] for a in kept if a["status"] == "DELIVERED"],
                                total_units=sum(a["total_units"] for a in kept),
                                category_totals=dict(named), tariff_category_totals=dict(primitive))
                    return aggregate([copy], unit["group_id"])
                p, o = prefix(history), prefix(other)
                prefixes.append(dict(compare(p, o, complete_outer=complete_outer),
                                     prefix_length=length, left_total_units=p["total_units"], right_total_units=o["total_units"],
                                     left_delivered_request_ids=p["delivered_request_ids"], right_delivered_request_ids=o["delivered_request_ids"]))
    # Read the already sealed frozen analysis, but never call or import it.
    analysis_rows, analysis_stage = stage_records(final, "analysis", [{"id": "all-frozen-endpoints", "arm": "analysis"}],
                                                   {"all-frozen-endpoints"}, lineage["amended_binding"])
    require(when(stage_checks[-1]["latest_seal_utc"]) <= when(analysis_stage["earliest_start_utc"])
            and when(analysis_stage["latest_seal_utc"]) <= when(release["recorded_utc"]),
            "Analysis barrier or principal observation release chronology mismatch")
    stage_checks.append(analysis_stage)
    frozen_analysis = analysis_rows["all-frozen-endpoints"]["result"]["value"]
    require(frozen_analysis["freeze_id"] == config["freeze_id"]
            and frozen_analysis["configuration_sha256"] == object_digest(config)
            and frozen_analysis["expected_score_units"] == frozen_analysis["received_score_units"] == 500,
            "Frozen analysis configuration or full denominator differs")
    require(frozen_analysis["complete_outer_attempt_economic_claim_permitted"] == complete_outer,
            "Outer attempt accounting disagrees with frozen analysis")
    execution_audit = frozen_analysis["execution_attempt_audit"]
    require(execution_audit["schema"] == "value_logic.p310_a1.merged_execution_history.v1"
            and execution_audit["amendment_id"] == "P3-10-A1"
            and execution_audit["complete_outer_paid_attempt_accounting"] is False
            and execution_audit["complete_physical_run_accounting"] is False
            and execution_audit["original_public_stage_complete"] is False
            and sorted(execution_audit["unknown_unsealed_public_attempts"], key=canonical)
                == sorted(unknown_public, key=canonical), "Merged global unknown-prefix audit differs")
    frozen_certificates = frozen_analysis["certificates"]
    def index(rows, keys):
        out = {tuple(row[key] for key in keys): row for row in rows}
        require(len(out) == len(rows), "Duplicate comparison or summary key")
        return out
    summary_keys = ("scope", "recipient", "budget_condition", "method")
    comparison_keys = ("scope", "recipient", "budget_condition", "left", "right")
    observed_s = index(summaries, summary_keys)
    frozen_s = index(frozen_certificates["complete_histories"], summary_keys)
    observed_c = index(comparisons, comparison_keys)
    frozen_c = index(frozen_certificates["coverage_cost_comparisons"], comparison_keys)
    require(set(observed_s) == set(frozen_s) and set(observed_c) == set(frozen_c), "Frozen analysis roster differs")
    mismatches = []
    for kind, observed, reported in (("summary", observed_s, frozen_s), ("comparison", observed_c, frozen_c)):
        for key, row in observed.items():
            for field, value in row.items():
                if reported[key].get(field) != value:
                    mismatches.append({"kind": kind, "key": list(key), "field": field, "independent": value, "frozen": reported[key].get(field)})
    delivered_count = sum(a["status"] == "DELIVERED" for a in attempts)
    failures = [a for a in attempts if a["status"] != "DELIVERED"]
    failure_kinds = Counter((a["method"], a["recipient"], a["budget_condition"], a["failure"]["type"], a["failure"]["stage"]) for a in failures)
    return {
        "schema": "value_logic.p310.independent_certificate_reconstruction.v4",
        "status": "PASS" if not mismatches else "FAIL", "signed_by": SIGNATURE,
        "review_type": "Independent implementation, same model, source-aware, not blind; JSON observer of sealed records",
        "worker_generator_private_scorer_frozen_analyzer_calls": 0, "principal_clock_credit_ns": 0,
        "stage_checks": stage_checks, "amendment_lineage": lineage,
        "unknown_unsealed_public_attempts": unknown_public, "complete_outer_paid_attempt_accounting": complete_outer,
        "source_bundle_files_verified_current_and_frozen": len(manifest["sources"]),
        "B0": {"planned_attempts": 416, "observed_attempts": len(attempts), "delivered": delivered_count,
               "unavailable": len(failures), "false_or_wrong_scope_delivered_warrants": 0,
               "independent_truth_tables_agree_with_all_sealed_diagnostics": True, "packet_hashes_verified": packet_count},
        "B1": {"unique_current_requests": len(truths), "all_old_receipts_observed_stale": True,
               "source_derived_recipe_counts_and_pointwise_loss_identities_verified": True,
               "full_input_scope_and_current_source_bindings_checked": True,
               "all_minimizers_in_each_current_sublevel": all(t["minimizers_are_all_in_sublevel"] for t in truths.values()),
               "nonoptimal_incumbent_requests": sum(not t["incumbent_is_minimizer"] for t in truths.values()),
               "input_diagnostics": input_diagnostics},
        "B2": {"histories": len(histories), "separately_executed_full_histories": sum(h["unit"]["budget_condition"] == "full" for h in histories),
               "separately_executed_capped_histories": sum(h["unit"]["budget_condition"] == "capped" for h in histories),
               "complete_service_histories": sum(len(h["delivered_request_ids"]) == 4 for h in histories),
               "known_all_attempt_units_descriptive_arm_sum": sum(h["total_units"] for h in histories),
               "failed_attempt_units": sum(a["total_units"] for a in failures),
               "resource_exhausted_failure_count": sum(a["failure_classification"] == "EXPECTED_DECLARED_BUDGET_EXHAUSTION" for a in failures),
               "nonbudget_errors_requiring_separate_disposition": [a for a in failures
                   if a["failure_classification"] != "EXPECTED_DECLARED_BUDGET_EXHAUSTION"],
               "source_enrollment_history_scope": "Scientific-cache eviction does not reset a completed installed source; a source fee by itself is not treated as completed enrollment",
               "comparison_threshold": [19, 20], "frozen_aggregate_records_reconstructed": len(summaries),
               "frozen_directed_comparisons_reconstructed": len(comparisons),
               "named_coordinates_overlap": "producer+consumer is the total; output/storage/source must not be added again",
               "all_attempts": attempts, "per_history": [{key: value for key, value in h.items() if key != "attempts"} for h in histories],
               "complete_histories": summaries, "coverage_cost_comparisons": comparisons,
               "all_tied_complete_ordinary_winners": ordinary_winners,
               "actual_cap_history_comparisons": cap_comparisons,
               "prefix_comparisons_descriptive": prefixes,
               "primitive_price_diagnostics_exploratory": prices,
               "failures_by_method_recipient_budget_type_stage": [dict(zip(("method", "recipient", "budget_condition", "failure_type", "failure_stage"), key), count=count)
                                                                  for key, count in sorted(failure_kinds.items(), key=lambda item: canonical(list(item[0])))]},
        "frozen_analysis_mismatches": mismatches,
        "limitations": ["Observer computation is not a delivered paid certificate or a new endpoint.",
                        "This is exact finite input/service checking, not a probability-coverage or asymptotic theorem.",
                        "Economic outcomes retain actual capped histories and every failure bill; primitive repricing holds paths fixed.",
                        "Certificate tariff is never added to the broker or conformance tariff."],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path)
    parser.add_argument("--release", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--selfcheck", action="store_true")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    started_utc = datetime.now(timezone.utc).isoformat()
    start_wall, start_cpu = time.monotonic_ns(), time.process_time_ns()
    global ROOT
    ROOT = args.repo.resolve() if args.repo else Path.cwd().resolve()
    source = Path(__file__).resolve()
    source_bytes = source.read_bytes()
    try:
        if args.selfcheck:
            answer = selfcheck()
        else:
            require(args.repo is not None and args.release is not None, "Explicit repo and principal release required")
            answer = reconstruct(args.repo.resolve(), args.release.resolve())
        output_name = "results.json"
        exit_code = 0 if answer["status"] == "PASS" else 1
    except BaseException as error:
        answer = {"status": "OBSERVER_FAILURE", "error_type": type(error).__name__, "error": str(error),
                  "traceback": traceback.format_exc(), "signed_by": SIGNATURE,
                  "failed_observer_preserved": True, "paid_worker_calls": 0, "principal_clock_credit_ns": 0}
        output_name = "failure.json"
        exit_code = 1
    output_bytes = canonical(answer, newline=True)
    (args.out / output_name).write_bytes(output_bytes)
    source_record = {"path": str(source.relative_to(ROOT)) if source.is_relative_to(ROOT) else str(source),
                     "bytes": len(source_bytes), "sha256": digest(source_bytes)}
    inputs_bytes = canonical({"observer_source": source_record, "consumed_files": sorted(READS.values(), key=lambda row: row["path"])}, newline=True)
    (args.out / "source_hashes.json").write_bytes(inputs_bytes)
    receipt = {
        "schema": "value_logic.p310.certificate_observer_run.v1", "signed_by": SIGNATURE,
        "started_utc": started_utc, "finished_utc": datetime.now(timezone.utc).isoformat(),
        "wall_ns": time.monotonic_ns() - start_wall, "process_cpu_ns": time.process_time_ns() - start_cpu,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "argv": sys.argv, "python": sys.version, "exit_code": exit_code,
        "observer_source": source_record,
        "outputs": [{"path": output_name, "bytes": len(output_bytes), "sha256": digest(output_bytes)},
                    {"path": "source_hashes.json", "bytes": len(inputs_bytes), "sha256": digest(inputs_bytes)}],
        "principal_clock_credit_ns": 0,
    }
    (args.out / "run_receipt.json").write_bytes(canonical(receipt, newline=True))
    print(json.dumps({"status": answer["status"], "output": str(args.out / output_name), "exit_code": exit_code}, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
