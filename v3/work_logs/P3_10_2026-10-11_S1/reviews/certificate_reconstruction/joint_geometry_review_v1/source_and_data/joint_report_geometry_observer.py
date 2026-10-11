"""Exact public joint report geometry on already sealed P3-10 paths.

Contributor: ChatGPT (GPT-6 Astra Pro), principal /root, 2026-10-11.
Post-outcome exploratory observer; no worker, generator, CNF truth evaluator,
frozen module import, endpoint replacement, or billed-service claim.
"""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction as F
from functools import cmp_to_key
from pathlib import Path
import argparse
import hashlib
import json
import os
import time
import traceback

from amended_lineage_reader import Lineage

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
CHECKS = Counter()


def stamp():
    return {"utc": datetime.now(timezone.utc).isoformat(),
            "monotonic_ns": time.monotonic_ns(),
            "boot_id": Path("/proc/sys/kernel/random/boot_id").read_text().strip()}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, name, detail=None):
    CHECKS[name] += 1
    if not condition:
        raise AssertionError(f"{name}: {detail}")


def rat(value):
    return F(*value) if isinstance(value, (tuple, list)) else F(value)


def encoded(value):
    if isinstance(value, F):
        return [value.numerator, value.denominator]
    if isinstance(value, dict):
        return {str(k): encoded(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [encoded(v) for v in value]
    return value


def save(path, value):
    with path.open("x") as stream:
        json.dump(encoded(value), stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    descriptor = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def key(value):
    require(isinstance(value, list) and len(value) == 4, "full_key_shape", value)
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def neg(a):
    return (-a[0], -a[1])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def polygon(origin, vectors):
    """Exact upper-half-plane edge ordering, with binary vertex witnesses."""
    start = origin
    active = set()
    positive = []
    for index, vector in enumerate(vectors):
        if vector == (0, 0):
            continue
        flip = vector[1] < 0 or (vector[1] == 0 and vector[0] < 0)
        if flip:
            start = add(start, vector)
            active.add(index)
        positive.append({"vector": neg(vector) if flip else vector,
                         "members": [(index, flip)]})

    def compare(a, b):
        value = cross(a["vector"], b["vector"])
        return -1 if value > 0 else (1 if value < 0 else 0)

    positive.sort(key=cmp_to_key(compare))
    groups = []
    for entry in positive:
        if groups and cross(groups[-1]["vector"], entry["vector"]) == 0:
            require(dot(groups[-1]["vector"], entry["vector"]) > 0,
                    "parallel_vectors_have_same_orientation")
            groups[-1]["vector"] = add(groups[-1]["vector"], entry["vector"])
            groups[-1]["members"].extend(entry["members"])
        else:
            groups.append({"vector": entry["vector"], "members": list(entry["members"])})

    vertices, witnesses = [], []
    current = start

    def append_vertex():
        represented = origin
        for index in active:
            represented = add(represented, vectors[index])
        require(represented == current, "binary_vertex_witness")
        vertices.append(current)
        witnesses.append(hex(sum(1 << index for index in active)))

    append_vertex()
    for forward in (True, False):
        for group in groups:
            current = add(current, group["vector"] if forward else neg(group["vector"]))
            for index, _ in group["members"]:
                if index in active:
                    active.remove(index)
                else:
                    active.add(index)
            append_vertex()
    require(current == start, "closed_polygon_walk")
    if groups:
        vertices.pop()
        witnesses.pop()
    dimension = 0 if not groups else (1 if len(groups) == 1 else 2)
    require(len(vertices) == max(1, 2 * len(groups)), "vertex_count")
    if dimension == 2:
        require(all(cross(sub(vertices[(i + 1) % len(vertices)], v),
                          sub(vertices[(i + 2) % len(vertices)], vertices[(i + 1) % len(vertices)])) > 0
                    for i, v in enumerate(vertices)), "strict_convex_orientation")
    twice_area = sum((cross(v, vertices[(i + 1) % len(vertices)])
                      for i, v in enumerate(vertices)), F(0))
    require(twice_area >= 0 and ((twice_area > 0) == (dimension == 2)), "area_dimension")
    return {"vertices": vertices, "binary_witness_masks": witnesses,
            "nonparallel_directions": len(groups), "dimension": dimension,
            "area": twice_area / 2}


def support(origin, vectors, direction):
    center = dot(origin, direction)
    values = [dot(vector, direction) for vector in vectors]
    return (center + sum((min(F(0), x) for x in values), F(0)),
            center + sum((max(F(0), x) for x in values), F(0)))


def contains(poly, point):
    vertices, dimension = poly["vertices"], poly["dimension"]
    if dimension == 0:
        return point == vertices[0]
    if dimension == 1:
        edge, delta = sub(vertices[1], vertices[0]), sub(point, vertices[0])
        return cross(edge, delta) == 0 and 0 <= dot(edge, delta) <= dot(edge, edge)
    return all(cross(sub(vertices[(i + 1) % len(vertices)], v), sub(point, v)) >= 0
               for i, v in enumerate(vertices))


def construct(unit, paid, prior):
    episode = paid["episode"]
    report = (paid.get("optional_reporting") or {}).get("report", {})
    header = {"unit_id": unit["id"], "group_id": unit["group_id"],
              "configuration_id": unit["configuration_id"], "stakes": unit["stakes"],
              "episode_status": episode["status"], "report_status": report.get("status")}
    if episode["status"] != "success" or report.get("status") != "success":
        return dict(header, status="unavailable", reason="Complete successful parent and paid report required.")
    require(prior["status"] == "available", "earlier_public_bound_available", unit["id"])
    rows = episode["trace"]
    horizon = episode["contract"]["horizon"]
    whole = [s for s in unit["segments"] if s["name"] == "whole"]
    require(len(whole) == 1 and whole[0]["start"] == 0 and whole[0]["stop"] == horizon
            and [r["index"] for r in rows] == list(range(horizon)), "complete_horizon", unit["id"])
    require(all(episode["hard_state"][k] == 0 for k in ("generation", "conflicts", "withdrawals")),
            "sound_unchanged_epoch", unit["id"])
    invoices, known = {}, {}
    for invoice in episode["invoices"]:
        k, query_id = key(invoice["claim_key"]), invoice["query_id"]
        require(query_id not in invoices and invoice["checked"] is True
                and invoice["status"] == "success" and type(invoice["answer"]) is int
                and invoice["answer"] in (0, 1), "checked_paid_invoice", query_id)
        require(invoice["claim_key"][:2] == episode["scope"][:2], "paid_label_current_scope")
        require(k not in known or known[k] == invoice["answer"], "consistent_paid_key_label")
        invoices[query_id], known[k] = invoice, invoice["answer"]
    constants = dict.fromkeys(("F", "V", "Z"), F(0))
    coefficients = {name: defaultdict(F) for name in constants}
    shift = F(0)
    selected_ids, all_keys = set(), set()
    for row in rows:
        k, q, action = key(row["claim_key"]), rat(row["emitted_q"]), row["terminal_action"]
        all_keys.add(k)
        require(row["scope"] == episode["scope"] and row["claim_key"][:2] == episode["scope"][:2],
                "row_current_scope", row["index"])
        require(0 <= q <= 1 and type(action) is int and action in (0, 1), "binary_target_domain")
        terms = {"F": (q * q, 1 - 2 * q), "Z": (F(action), F(1 - 2 * action))}
        if row["selected"]:
            invoice = invoices[row["query_id"]]
            require(key(invoice["claim_key"]) == k and invoice["answer"] == row["purchased_label"] == action,
                    "selected_exact_receipt_binding", row["index"])
            selected_ids.add(row["query_id"])
            shift += (q - invoice["answer"]) ** 2
        else:
            require(row["purchased_label"] is None, "no_unpurchased_label")
            terms["V"] = (q, 1 - 2 * q)
            shift -= q * (1 - q)
        for name, (constant, coefficient) in terms.items():
            constants[name] += constant
            coefficients[name][k] += coefficient
    require(selected_ids == set(invoices), "invoice_selected_coverage")
    for name in constants:
        for k, truth in known.items():
            constants[name] += coefficients[name].pop(k, F(0)) * truth
    unknown = sorted(all_keys - known.keys())
    require(len(unknown) == prior["unresolved_distinct_keys"], "same_unresolved_keys")
    require(all(coefficients["F"][k] == coefficients["V"][k] for k in unknown), "F_V_equal_unknown_coefficients")
    require(constants["F"] - constants["V"] == shift, "public_F_minus_V_shift")
    origin = (constants["F"], constants["Z"])
    vectors = [(coefficients["F"][k], coefficients["Z"][k]) for k in unknown]
    poly = polygon(origin, vectors)
    directions = {(F(a), F(b)) for a in range(-2, 3) for b in range(-2, 3) if a or b}
    for i, vertex in enumerate(poly["vertices"]):
        edge = sub(poly["vertices"][(i + 1) % len(poly["vertices"])], vertex)
        if edge != (0, 0):
            directions.update({(-edge[1], edge[0]), (edge[1], -edge[0])})
    for direction in directions:
        direct = support(origin, vectors, direction)
        values = [dot(v, direction) for v in poly["vertices"]]
        require(direct == (min(values), max(values)), "polygon_direct_support", [unit["id"], direction])
    f_bounds = support(origin, vectors, (F(1), F(0)))
    z_bounds = support(origin, vectors, (F(0), F(1)))
    v_bounds = (f_bounds[0] - shift, f_bounds[1] - shift)
    bounds = {"F": f_bounds, "V": v_bounds, "Z": z_bounds}
    for name, interval in bounds.items():
        expected = prior["endpoints"][name]
        require(interval == (rat(expected["public_only_lower"]), rat(expected["public_only_upper"])),
                "independent_marginal_agreement", [unit["id"], name])
    corners = []
    for sx, f_index in ((-1, 0), (1, 1)):
        for sz, z_index in ((-1, 0), (1, 1)):
            conflicts = [i for i, v in enumerate(vectors) if sx * sz * v[0] * v[1] < 0]
            corner = (f_bounds[f_index], z_bounds[z_index])
            compatible = not conflicts
            require(contains(poly, corner) == compatible, "rectangle_corner_criterion")
            corners.append({"F": "lower" if f_index == 0 else "upper",
                            "Z": "lower" if z_index == 0 else "upper",
                            "point": corner, "jointly_attainable_on_key_cube": compatible,
                            "conflicting_unknown_key_indices": conflicts})
    rectangle_area = (f_bounds[1] - f_bounds[0]) * (z_bounds[1] - z_bounds[0])
    require(0 <= poly["area"] <= rectangle_area, "convex_hull_inside_marginal_rectangle")
    return dict(header, status="available", horizon=horizon, paid_known_keys=len(known),
                unresolved_full_keys=unknown, unresolved_key_vectors=vectors, public_origin=origin,
                F_minus_V_public_shift=shift, marginals=bounds, polygon=poly, rectangle_corners=corners,
                rectangle_area=rectangle_area,
                convex_hull_area_fraction_of_rectangle=None if rectangle_area == 0 else poly["area"] / rectangle_area,
                nonaxis_support_checks=len(directions),
                uncertainty_set="binary labels per unresolved full key; logical relationships between distinct keys relaxed")


def summarize(records, families):
    groups = defaultdict(list)
    for record in records:
        groups[(families[record["group_id"]], record["configuration_id"])].append(record)
    result = []
    for (family, configuration), rows in sorted(groups.items()):
        available = [r for r in rows if r["status"] == "available"]
        def mean(field):
            populations = defaultdict(list)
            for row in available:
                populations[row["group_id"]].append(row[field])
            if len(available) != len(rows) or any(x is None for xs in populations.values() for x in xs):
                return None
            return sum((sum(xs, F(0)) / len(xs) for xs in populations.values()), F(0)) / len(populations)
        result.append({"family": family, "configuration_id": configuration,
                       "scheduled_reports": len(rows), "available_reports": len(available),
                       "dimensions": dict(Counter(str(r["polygon"]["dimension"]) for r in available)),
                       "reports_with_incompatible_rectangle_corners": sum(any(not c["jointly_attainable_on_key_cube"] for c in r["rectangle_corners"]) for r in available),
                       "incompatible_corner_counts": dict(Counter(str(sum(not c["jointly_attainable_on_key_cube"] for c in r["rectangle_corners"])) for r in available)),
                       "mean_convex_hull_area_fraction_of_rectangle": mean("convex_hull_area_fraction_of_rectangle"),
                       "mean_F_minus_V_shift": mean("F_minus_V_public_shift"),
                       "weighting": "equal scheduled seeds within population, then equal populations",
                       "unit_ids": [r["unit_id"] for r in rows]})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    parser.add_argument("--public-bounds", required=True)
    parser.add_argument("--numeric", required=True)
    args = parser.parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=False)
    start = stamp()
    try:
        lineage = Lineage()
        prior_path = Path(args.public_bounds)
        prior = json.loads(prior_path.read_text())
        require(prior["status"] == "PASS" and prior["private_truth_reads_before_bounds_saved"] == 0,
                "public_only_marginal_source")
        prior_records = {r["unit_id"]: r for r in prior["records"]}
        families = {g["id"]: g["recipe"]["family"] for g in lineage.schedule["groups"] if g["arm"] == "broker"}
        records, traces = [], {}
        for unit in lineage.schedule["units"]:
            if unit["arm"] != "broker" or unit["engine"] not in ("broker", "mirror"):
                continue
            result, _ = lineage.record("public", unit["id"])
            paid = result["value"]["paid_result"]
            require(paid["unit"] == unit, "public_scheduled_unit")
            records.append(construct(unit, paid, prior_records[unit["id"]]))
            traces[unit["id"]] = paid["episode"]["trace"]
        require(len(records) == 126 and set(traces) == set(prior_records), "complete_public_report_roster")
        public = {"schema": "value_logic.p310.joint_public_report_geometry.v1", "status": "PASS",
                  "contributor": "ChatGPT (GPT-6 Astra Pro)", "start": start, "public_completion": stamp(),
                  "source_sha256": digest(Path(__file__)), "derivation_sha256": digest(HERE / "joint_report_geometry.md"),
                  "derivation_addendum_sha256": digest(HERE / "joint_report_geometry_addendum.md"),
                  "earlier_public_bounds_sha256": digest(prior_path), "amendment_lineage": lineage.receipt,
                  "research_class": "post-outcome exploratory deterministic information interpretation",
                  "private_truth_reads_before_public_geometry_saved": 0, "frozen_endpoint_replacement": False,
                  "paid_service_or_economic_advantage_claim": False, "new_coverage_claim": False,
                  "scheduled_reports": len(records), "available_reports": sum(r["status"] == "available" for r in records),
                  "records": records, "summaries": summarize(records, families), "checks_by_kind": dict(CHECKS)}
        public_path = output / "public_geometry.json"
        save(public_path, public)
        public_hash = digest(public_path)
        private_start = stamp()
        numeric_path = Path(args.numeric)
        numeric = json.loads(numeric_path.read_text())
        require(numeric["status"] == "PASS", "independent_numeric_source_passed")
        numeric_rows = {r["unit_id"]: [x for block in r["blocks"] for x in block["rows"]]
                        for r in numeric["per_episode"]}
        checks = []
        for record in records:
            if record["status"] != "available":
                continue
            identifier = record["unit_id"]
            rows, checked = traces[identifier], numeric_rows[identifier]
            require(len(rows) == len(checked) == record["horizon"], "private_validation_horizon")
            truths = [r["truth"] for r in checked]
            targets = {"F": sum(((rat(row["emitted_q"]) - y) ** 2 for row, y in zip(rows, truths)), F(0)),
                       "V": sum((rat(row["emitted_q"]) + (1 - 2 * rat(row["emitted_q"])) * y
                                 for row, y in zip(rows, truths) if not row["selected"]), F(0)),
                       "Z": F(sum(row["terminal_action"] != y for row, y in zip(rows, truths)))}
            require(targets["F"] == sum((rat(r["live_brier"]) for r in checked), F(0))
                    and targets["Z"] == sum(r["live_terminal_error"] for r in checked), "independent_row_target_agreement")
            require(targets["F"] - targets["V"] == record["F_minus_V_public_shift"], "private_affine_identity")
            require(contains(record["polygon"], (targets["F"], targets["Z"])), "private_joint_containment")
            score_result, _ = lineage.record("evaluation", "score-" + identifier)
            score = score_result["value"]["score"]
            require(targets["F"] == rat(score["issued_brier_sum"]) and targets["Z"] == score["terminal_errors"],
                    "sealed_frozen_target_agreement")
            checks.append({"unit_id": identifier, "targets": targets, "affine_identity": True, "joint_containment": True})
        require(digest(public_path) == public_hash, "public_geometry_unchanged_after_private_validation")
        validation = {"status": "PASS", "public_geometry_sha256": public_hash, "private_start": private_start,
                      "numeric_source_sha256": digest(numeric_path), "validated_reports": len(checks),
                      "checks": checks, "checks_by_kind": dict(CHECKS), "end": stamp()}
        save(output / "validation.json", validation)
        print(json.dumps({"status": "PASS", "reports": len(records), "validated_reports": len(checks),
                          "checks_total": sum(CHECKS.values()), "public_geometry_sha256": public_hash}, indent=2))
    except BaseException as error:
        save(output / "failure.json", {"status": "OBSERVER_FAILURE", "start": start, "end": stamp(),
             "source_sha256": digest(Path(__file__)), "error_type": type(error).__name__, "error": str(error),
             "traceback": traceback.format_exc(), "checks_completed": dict(CHECKS), "scientific_stage_failure": False})
        raise


if __name__ == "__main__":
    main()
