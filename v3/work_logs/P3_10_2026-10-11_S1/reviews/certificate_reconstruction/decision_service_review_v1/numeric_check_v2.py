#!/usr/bin/env python3
"""Post-outcome arithmetic on saved JSON, with no scientific-module imports.

This review does not enumerate a feasible domain, evaluate a truth predicate,
generate an input, execute a paid policy, or call any scorer/analyzer. It binds
the original input and four amended public records to the earlier independent
lineage inventory, and checks the draft's arithmetic on their recorded tables.
Hypothetical transformations remain mathematical examples, not paid services.
"""

import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time
import traceback


W = Path("v3/work_logs/P3_10_2026-10-11_S1")
OWN = W / "reviews/certificate_reconstruction"
REVIEW = OWN / "decision_service_review_v1"
AMENDED = Path("v3/experiments/final_v1_amended_A1")
ORIGINAL = Path("v3/experiments/final_v1")
INVENTORY = OWN / "final_observation_v4/source_hashes.json"
INVENTORY_SHA = "58b51d1f1379ddf41ed34f8949fdc315de524aa5e61a3f38fe5d2aba7e0c75fb"
CERT_RESULT = OWN / "final_observation_v4/results.json"
CERT_SHA = "6e3e00caf1d91c15f3aaea240006f6933aab2db93bed214d6ec379266414035c"
DRAFT_SHA = "8e9c2766a7ed6f4239139e55befe682aff124db0a229fbdd318dcee3a68738a9"
REVIEWER = "ChatGPT (GPT-6 Astra Pro), /root/certificate_reconstruction"
ORIGINAL_BINDING = {
    "freeze_id": "P3-09-v1",
    "manifest_sha256": "69d4d4a84c649698a006bce00a87b0038d5f7d19f2da4e96e6ef3d4e42e37c70",
    "protocol_sha256": "dde9fe405ad39e65db3d49cb47d298e3ab6e498d7c5c485ff215ff884466b88f",
}
AMENDED_BINDING = dict(ORIGINAL_BINDING, amendment_id="P3-10-A1",
    amendment_manifest_sha256="36ddd4abc335afebf1e46d5c58e016adbc8d356a72809d14ad95338e05342359")
CASES = ("counterpossible_tied_minima", "external_sources_not_repairs")


def digest(b):
    return hashlib.sha256(b).hexdigest()


def canonical(j):
    return json.dumps(j, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def encode(j):
    if isinstance(j, F):
        return str(j)
    if isinstance(j, dict):
        return {str(k): encode(v) for k, v in j.items()}
    if isinstance(j, (list, tuple)):
        return [encode(v) for v in j]
    return j


def write_json(p, obj):
    with p.open("x", encoding="utf-8") as f:
        json.dump(encode(obj), f, sort_keys=True, indent=2, allow_nan=False)
        f.write("\n")


class Reader:
    def __init__(self, root):
        self.root = root
        self.checks = []
        self.files = {}
        self.inventory = {}

    def eq(self, name, actual, expected):
        self.checks.append({"id": name, "pass": actual == expected})
        if actual != expected:
            raise AssertionError(f"{name}: {actual!r} != {expected!r}")

    def read_bytes(self, rel, expected=None, enrolled=False):
        rel = str(rel)
        b = (self.root / rel).read_bytes()
        h = digest(b)
        if enrolled:
            item = self.inventory[rel]
            self.eq("inventory.sha256:" + rel, h, item["sha256"])
            self.eq("inventory.bytes:" + rel, len(b), item["bytes"])
        if expected is not None:
            self.eq("pinned.sha256:" + rel, h, expected)
        item = {"path": rel, "sha256": h, "bytes": len(b)}
        if rel in self.files:
            self.eq("same.bytes.on.reread:" + rel, item, self.files[rel])
        self.files[rel] = item
        return b

    def read_json(self, rel, expected=None, enrolled=False):
        return json.loads(self.read_bytes(rel, expected, enrolled))

    def sealed(self, entry, stage, binding, origin):
        uid = entry["unit_id"]
        self.eq(uid + ":origin", entry["origin_root"], str(origin))
        seal_path = origin / entry["seal_path"]
        result_path = origin / entry["result_path"]
        start_path = seal_path.with_name("start.json")
        seal = self.read_json(seal_path, entry["seal_sha256"], True)
        result = self.read_json(result_path, entry["result_sha256"], True)
        start = self.read_json(start_path, seal["start_sha256"], True)
        self.eq(uid + ":seal.result", seal["result_sha256"], entry["result_sha256"])
        self.eq(uid + ":seal.unit", seal["unit_sha256"], digest(canonical(start["unit"]) + b"\n"))
        self.eq(uid + ":unit", result["unit"], start["unit"])
        self.eq(uid + ":unit.id", result["unit"]["id"], uid)
        self.eq(uid + ":identity.start", result["identity"], start["identity"])
        self.eq(uid + ":identity.seal", result["identity"], seal["identity"])
        self.eq(uid + ":binding", result["identity"]["binding"], binding)
        self.eq(uid + ":stage", result["identity"]["stage"], stage)
        self.eq(uid + ":attempts", [start["attempt"], result["attempt"], seal["attempt"]], [1, 1, 1])
        chronology = [datetime.fromisoformat(v) for v in
                      [start["started_utc"], result["finished_utc"], seal["sealed_utc"]]]
        self.eq(uid + ":chronology", chronology, sorted(chronology))
        return result


def inspect(root, r):
    inv = r.read_json(INVENTORY, INVENTORY_SHA)
    r.inventory = {row["path"]: row for row in inv["consumed_files"]}
    snapshots = r.read_json(REVIEW / "source_snapshot_manifest.json")
    for item in snapshots["files"]:
        r.read_bytes(item["path"], item["sha256"])
        r.read_bytes(item["snapshot"], item["sha256"])
    r.read_bytes(W / "decision_service_interpretation.md", DRAFT_SHA)

    binding = r.read_json(AMENDED / "amendment_binding.json", enrolled=True)
    r.eq("amended.binding", binding, AMENDED_BINDING)
    comp = r.read_json(AMENDED / "composite_public.json", enrolled=True)
    r.eq("composite.binding", comp["binding"], AMENDED_BINDING)
    r.eq("composite.counts", [comp[k] for k in
         ["completed_units", "expected_units", "original_units", "amended_units"]], [500, 500, 440, 60])
    r.eq("composite.roster.size", len(comp["seals"]), 500)
    r.eq("composite.unique.ids", len({e["unit_id"] for e in comp["seals"]}), 500)
    r.eq("original.public.not.complete", comp["original_public_stage_complete"], False)
    r.eq("original.public.completion.file.absent", (root / ORIGINAL / "stages/public/complete.json").exists(), False)
    refs = r.read_json(AMENDED / "input_reference.json", enrolled=True)
    r.eq("input.reference.binding", refs["binding"], AMENDED_BINDING)
    r.eq("input.reference.counts", [refs[k] for k in
         ["completed_units", "expected_units", "new_generations"]], [12, 12, 0])
    inp_entry = next(e for e in refs["seals"] if e["unit_id"] == "conformance_structural_legacy")
    r.eq("input.evidence", inp_entry["evidence_class"], "original_prospective_input")
    inp = r.sealed(inp_entry, "inputs", ORIGINAL_BINDING, ORIGINAL)
    specs = {s["name"]: s for s in inp["value"]["inputs"]}
    r.eq("legacy.input.fixture.count", len(specs), 9)
    comp_by_id = {e["unit_id"]: e for e in comp["seals"]}
    records = []
    terminals = {}
    for case in CASES:
        spec = specs[case]
        for method in ("candidate", "ordinary"):
            uid = f"conformance_structural_legacy__{case}__{method}"
            entry = comp_by_id[uid]
            r.eq(uid + ":evidence", entry["evidence_class"], "post_exposure_amended_inherited_conformance")
            record = r.sealed(entry, "public", AMENDED_BINDING, AMENDED)
            paid = record["value"]["paid_result"]
            terminal = paid["inner_record"]["output"]
            r.eq(uid + ":input.result", record["value"]["input_result_sha256"], inp_entry["result_sha256"])
            r.eq(uid + ":input.value", paid["public_input_sha256"], digest(canonical(inp["value"])))
            r.eq(uid + ":case.digest", paid["case_sha256"], digest(canonical(spec)))
            r.eq(uid + ":inner.case.digest", paid["inner_record"]["input_sha256"], paid["case_sha256"])
            r.eq(uid + ":method", record["unit"]["worker_method"], method)
            r.eq(uid + ":statuses", [paid["status"], terminal["status"]], ["SUCCESS", "SUCCESS"])
            r.eq(uid + ":state.meaning", terminal["hypothetical_interpretation"],
                 "Declared paired-support evaluation; not a truth probability.")
            r.eq(uid + ":ordinary.satisfying.count", terminal["ordinary_satisfying_valuations"], 0)
            r.eq(uid + ":source.ids", [s["source_id"] for s in terminal["sources"]], [s["id"] for s in spec["sources"]])
            for source, source_spec in zip(terminal["sources"], spec["sources"]):
                sid = uid + ":" + source["source_id"]
                scope = json.loads(source["scope_record"])
                r.eq(sid + ":request.scope", scope["request"], spec)
                r.eq(sid + ":source.scope", scope["source"], source_spec)
                r.eq(sid + ":quantifier", scope["source_quantifier"], "EXTERNAL_UNRESOLVED_CASE_NOT_A_REPAIR")
                r.eq(sid + ":complete", source["identities_complete"], True)
                r.eq(sid + ":nonempty", source["feasibility"], "NONEMPTY")
                r.eq(sid + ":saved.states", source["models"], [row["state"] for row in source["case_values"]])
                r.eq(sid + ":two.saved.minima", len(source["case_values"]), 2)
                for action, image in source["loss_images"].items():
                    r.eq(sid + ":loss.image:" + action,
                         sorted({F(row["losses"][action]) for row in source["case_values"]}), [F(v) for v in image])
            actions = [a for a, _ in spec["actions"]]
            case_rows = [row for s in terminal["sources"] for row in s["case_values"]]
            worst = {a: max(F(row["losses"][a]) for row in case_rows) for a in actions}
            unique_best = [a for a in actions if worst[a] == min(worst.values())]
            dec = terminal["decision"]
            r.eq(uid + ":worst.values", worst, {a: F(v) for a, v in dec["worst_loss_by_fixed_action"].items()})
            r.eq(uid + ":unique.minimax", unique_best, ["fallback"])
            r.eq(uid + ":delivered.action", dec["action"], unique_best[0])
            r.eq(uid + ":delivered.value", F(dec["fixed_action_worst_loss"]), F(3))
            r.eq(uid + ":selection.order", dec["selection_order"], "ONE_ACTION_THEN_ALL_UNRESOLVED_SOURCES_THEN_ALL_PER_SOURCE_MINIMA")
            r.eq(uid + ":all.ties", dec["all_ties_preserved"], True)
            r.eq(uid + ":oracle.not.policy", dec["oracle_is_policy"], False)
            r.eq(uid + ":pointwise.oracle.value", F(dec["nonimplementable_pointwise_action_oracle"]), F(0))
            r.eq(uid + ":joint.not.admitted", dec["forbidden_joint_source_repair_minimum"]["is_an_admissible_service"], False)
            terminals[(case, method)] = terminal
            records.append({"unit_id": uid, "result_sha256": entry["result_sha256"],
                            "seal_sha256": entry["seal_sha256"], "case_sha256": paid["case_sha256"],
                            "evidence_class": entry["evidence_class"], "source_count": len(terminal["sources"]),
                            "retained_source_state_count": len(case_rows), "worst_loss_by_action": worst})
        r.eq(case + ":complete.candidate.ordinary.output.equality",
             terminals[(case, "candidate")], terminals[(case, "ordinary")])

    tied = terminals[(CASES[0], "ordinary")]
    rows = tied["sources"][0]["case_values"]
    actions = ["take_p", "take_r", "fallback"]
    table = {a: [F(row["losses"][a]) for row in rows] for a in actions}
    r.eq("tied.table", table, {"take_p": [F(4), F(0)], "take_r": [F(0), F(4)], "fallback": [F(3), F(3)]})
    r.eq("tied.lexicographic.rank", tied["sources"][0]["optimal_rank"], ["1", "1"])
    coefficients = {a: {"constant": v[1], "coefficient_of_p": v[0] - v[1]} for a, v in table.items()}
    lower = F(3, 4)
    upper = F(1, 4)
    r.eq("fallback.bayes.infeasible", lower <= upper, False)
    half_values = {a: sum(v, F(0)) / 2 for a, v in table.items()}
    r.eq("bayes.crossing.values", half_values, {"take_p": F(2), "take_r": F(2), "fallback": F(3)})
    row_sum = [table["take_p"][i] + table["take_r"][i] for i in range(2)]
    contrast = [table["fallback"][i] - row_sum[i] / 2 for i in range(2)]
    robust = {a: max(v) for a, v in table.items()}
    robust_contrast = robust["fallback"] - (robust["take_p"] + robust["take_r"]) / 2
    r.eq("known.unit.row.sum", row_sum, [F(4), F(4)])
    r.eq("all.calibrations.loss.row.contrast", contrast, [F(1), F(1)])
    r.eq("robust.contrast", robust_contrast, F(-1))
    lottery = [(table["take_p"][i] + table["take_r"][i]) / 2 for i in range(2)]
    realized = max(table["take_p"] + table["take_r"])
    lottery_delta = {a: [table[a][i] - table["fallback"][i] for i in range(2)] for a in actions[:2]}
    r.eq("lottery.statewise.means", lottery, [F(2), F(2)])
    r.eq("lottery.worst.realization", realized, F(4))
    r.eq("lottery.max.realized.loss.minus.fallback", max(v for row in lottery_delta.values() for v in row), F(1))
    h = [F(100), F(0)]
    shifted = {a: [v[i] + h[i] for i in range(2)] for a, v in table.items()}
    shifted_max = {a: max(v) for a, v in shifted.items()}
    r.eq("state.offset.table", shifted, {"take_p": [F(104), F(0)], "take_r": [F(100), F(4)], "fallback": [F(103), F(3)]})
    r.eq("state.offset.maxima", shifted_max, {"take_p": F(104), "take_r": F(100), "fallback": F(103)})
    r.eq("state.offset.unique.minimax", [a for a in actions if shifted_max[a] == min(shifted_max.values())], ["take_r"])
    for a in actions:
        for b in actions:
            r.eq("state.offset.pairwise:" + a + ":" + b,
                 [shifted[a][i] - shifted[b][i] for i in range(2)],
                 [table[a][i] - table[b][i] for i in range(2)])
    fallback_difference = [table["fallback"][i] - table["take_p"][i] for i in range(2)]
    r.eq("fallback.minus.take_p", fallback_difference, [F(-1), F(3)])
    r.eq("fallback.minus.take_p.bound", max(fallback_difference), F(3))

    external = terminals[(CASES[1], "ordinary")]
    ranks = {s["source_id"]: tuple(F(v) for v in s["optimal_rank"]) for s in external["sources"]}
    r.eq("external.scalar.ranks", ranks, {"q0_cheaper_rank": (F(1),), "q1_dearer_rank": (F(2),)})
    rank_offsets = []
    for shift, expected in [(0, ["q0_cheaper_rank"]), (1, ["q0_cheaper_rank", "q1_dearer_rank"]), (2, ["q1_dearer_rank"])]:
        values = {s: (v[0] + (shift if s == "q0_cheaper_rank" else 0),) for s, v in ranks.items()}
        joint_kept = [s for s, v in values.items() if v == min(values.values())]
        r.eq(f"forbidden.joint.offset.{shift}", joint_kept, expected)
        rank_offsets.append({"first_source_offset": shift, "minimum_rank_values": values, "forbidden_joint_retained_sources": joint_kept})
    r.eq("saved.forbidden.joint.retained", external["decision"]["forbidden_joint_source_repair_minimum"]["retained_sources"], ["q0_cheaper_rank"])

    cert = r.read_json(CERT_RESULT, CERT_SHA)
    r.eq("prior.certificate.review.pass", cert["status"], "PASS")
    r.eq("global.complete.outer.accounting.remains.false", cert["complete_outer_paid_attempt_accounting"], False)
    cert_refs = []
    for group in cert["B1"]["input_diagnostics"]:
        for req in group["current_requests"]:
            bound = F(req["bound"])
            r.eq(req["request_id"] + ":recorded.bound.attained", bound, F(req["diagnostics"]["exact_upper"]))
            r.eq(req["request_id"] + ":recorded.bound.positive", bound > 0, True)
            r.eq(req["request_id"] + ":recorded.bound.valid", req["holds"], True)
            cert_refs.append({"request_id": req["request_id"], "bound": bound, "recorded_exact_upper": F(req["diagnostics"]["exact_upper"])})
    r.eq("prior.certificate.current.requests", len(cert_refs), 16)
    r.eq("prior.certificate.distinct.bounds", sorted({x["bound"] for x in cert_refs}), [F(1), F(3, 2)])

    for item in tuple(r.files.values()):
        r.eq("unchanged.at.end:" + item["path"], digest((root / item["path"]).read_bytes()), item["sha256"])
    return {
        "status": "PASS", "reviewed_draft_sha256": DRAFT_SHA,
        "scope": "Post-outcome saved-JSON arithmetic plus separate source proof; no new empirical evidence or service.",
        "denominators": {"named_fixtures": 2, "paid_records_read": 4,
                         "complete_candidate_ordinary_output_pairs_equal": 2,
                         "distinct_retained_source_state_rows_across_two_fixtures": 6,
                         "previously_reconstructed_current_certificate_request_identities_read": 16},
        "record_bindings": records,
        "tied_fixture": {"name": CASES[0], "source_id": "q0", "rank": ["1", "1"],
                         "retained_states": [r["state"] for r in rows], "loss_table": table,
                         "robust_values": robust, "unique_pure_minimax_action": "fallback"},
        "expected_loss": {"p_meaning": "Probability of the first saved paired-support state in this hypothetical common law.",
                          "affine_in_p": coefficients, "fallback_optimality_requires_p_at_least": lower,
                          "fallback_optimality_requires_p_at_most": upper, "requirements_compatible": False,
                          "analytic_all_p_proof": "For p <= 1/2, 4p <= 2. For p >= 1/2, 4(1-p) <= 2. Fallback is 3.",
                          "known_unit_specialized_row_sum": row_sum,
                          "base_fallback_minus_average_specialized_rows": contrast,
                          "shared_affine_contrast_identity": "v_fallback - (v_take_p + v_take_r)/2 = s > 0 for v = s Lp + b1, s > 0.",
                          "robust_vector_contrast": robust_contrast,
                          "calibrations_excluded": ["known_units", "unknown_common_offset", "unknown_positive_common_scale", "unknown_positive_common_scale_and_offset"]},
        "hypothetical_lottery": {"specialized_action_probabilities": [F(1, 2), F(1, 2)],
                                 "statewise_expected_losses": lottery, "worst_state_expected_loss": max(lottery),
                                 "worst_state_and_draw_realized_loss": realized,
                                 "realized_difference_from_fallback_by_action": lottery_delta,
                                 "added_paid_policy": False, "new_random_draws": 0},
        "state_dependent_offset": {"offset": h, "loss_table": shifted, "maxima": shifted_max,
                                   "unique_minimax_action": "take_r", "all_same_state_pairwise_differences_preserved": True,
                                   "transformed_fixture_executed": False},
        "fixed_pair": {"orientation": "fallback minus take_p", "differences": fallback_difference,
                       "attained_uniform_upper_bound": max(fallback_difference), "nonpositive_bound": False},
        "source_rank_offsets": {"fixture_name": CASES[1], "sourcewise_minimum_ranks": ranks,
                                "sourcewise_retained_sources": list(ranks), "hypothetical_offsets": rank_offsets,
                                "general_rank_type": "Lexicographic vector; positive scalar a_s and same-dimensional vector b_s.",
                                "sourcewise_argmin_invariance": "The first unequal rank coordinate preserves its sign under positive scaling; translation cancels.",
                                "sourcewise_offsets_executed": False, "joint_minimization_admitted": False},
        "incumbent_identity_scope": "For a checked feasible w in the fixed hard domain, r(x)<=r(w) iff ar(x)+b<=ar(w)+b, a>0. Deployed receiver is scalar; admissible encoding, current binding and cost are separate.",
        "prior_certificate_record_references": cert_refs,
        "global_complete_outer_paid_attempt_accounting": False,
        "scientific_worker_generator_truth_scorer_analyzer_calls": 0,
        "principal_research_credit_seconds": 0,
        "observer_failures_this_execution": 0,
        "preserved_prior_read_probe_diagnostics": [str(REVIEW / "read_probe_failure_01.json"), str(REVIEW / "read_probe_failure_02.json")],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    output = (root / args.output).resolve()
    if not output.is_relative_to((root / REVIEW).resolve()):
        raise ValueError("Output must remain in this owned review directory")
    output.mkdir(parents=True, exist_ok=False)
    start = datetime.now(timezone.utc).isoformat()
    started_ns = time.perf_counter_ns()
    reader = Reader(root)
    exception = None
    try:
        result = inspect(root, reader)
    except Exception as exc:
        exception = exc
        trace = traceback.format_exc()
        (output / "failure_traceback.txt").write_text(trace, encoding="utf-8")
        result = {"status": "OBSERVER_FAILURE_PRESERVED", "error_type": type(exc).__name__,
                  "error": str(exc), "scientific_worker_generator_truth_scorer_analyzer_calls": 0,
                  "principal_research_credit_seconds": 0}
    result.update({"schema": "p310.independent_decision_service_arithmetic.v2",
                   "reviewer": REVIEWER, "started_utc": start,
                   "finished_utc": datetime.now(timezone.utc).isoformat(),
                   "elapsed_ns": time.perf_counter_ns() - started_ns,
                   "checks": len(reader.checks), "failed_checks": sum(not c["pass"] for c in reader.checks)})
    write_json(output / "results.json", result)
    write_json(output / "check_log.json", reader.checks)
    write_json(output / "source_hashes.json", {
        "consumed_files": sorted(reader.files.values(), key=lambda x: x["path"]),
        "observer_source": {"path": str(Path(__file__).resolve().relative_to(root)),
                            "sha256": digest(Path(__file__).read_bytes()), "bytes": len(Path(__file__).read_bytes())}})
    write_json(output / "run_manifest.json", {"reviewer": REVIEWER, "principal_research_credit_seconds": 0,
        "files": [{"path": str(p.relative_to(root)), "sha256": digest(p.read_bytes()), "bytes": len(p.read_bytes())}
                  for p in sorted(output.iterdir()) if p.is_file()]})
    print(json.dumps({k: result[k] for k in ["status", "checks", "failed_checks", "elapsed_ns"]}, sort_keys=True))
    if exception is not None:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
