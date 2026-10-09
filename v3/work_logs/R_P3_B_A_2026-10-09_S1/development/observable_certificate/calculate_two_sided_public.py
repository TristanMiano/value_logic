"""Final planned two-sided diagnostic from sealed public sufficient statistics.

ChatGPT (GPT-6 Astra Pro), 2026-10-09 UTC. DEVELOPMENT, zero principal credit.
Only this source, the prospective design, centered public result and its
completion seal are read. No private scores, archives, policies, services,
random numbers or labels are opened/computed. Empty interval intersections
remain explicit and suppress ordinary better/worse certificate labels.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
import argparse
import hashlib
import json
import math
from pathlib import Path
import platform
import sys
import time
import traceback


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
DESIGN = HERE / "two_sided_design.md"
VERSION = "observable-two-sided-public-v1"


def utc():
    return datetime.now(timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write(path, value):
    temporary = path.with_name(path.name + ".writing")
    temporary.write_text(json.dumps(value, indent=2, default=str) + "\n")
    temporary.replace(path)


def ceil_sqrt(value):
    root = math.isqrt(value)
    answer = root + int(root * root < value)
    if not (answer * answer >= value and (answer == 0 or (answer - 1) ** 2 < value)):
        raise AssertionError("The conservative integer action radius did not verify.")
    return answer


def intersect(raw_lower, raw_upper, public_lower, public_upper):
    if public_lower < 0 or public_lower > public_upper:
        raise AssertionError("Public deterministic envelope is invalid.")
    lower, upper = max(raw_lower, public_lower), min(raw_upper, public_upper)
    return {"raw_lower": raw_lower, "raw_upper": raw_upper,
            "public_lower": public_lower, "public_upper": public_upper,
            "lower": lower, "upper": upper, "empty": lower > upper}


def calculate(source):
    t, m = source["T"], source["m"]
    n = t - m
    r = source["baseline_integer_sampling_radius_R"]
    q = F(source["Q_realized_predictable_width_sum"])
    uc, ac = F(source["U_centered_total"]), F(source["A_centered_total"])
    variance_sum = F(source["public_variance_sum"])
    if (r <= 0 or q < 0 or F(source["fixed_lambda"]) != F(8, r)
            or q > F(r * r, 2)):
        raise AssertionError("The sealed predictable-width/fixed-lambda contract is inconsistent.")
    rho = q / r + F(5 * r, 8)
    if rho > F(9 * r, 8):
        raise AssertionError("The two-sided bound is9R/8, not the old one-sidedR bound.")
    action_radicand = (5 * n + 1) // 2
    action_radius = ceil_sqrt(action_radicand)
    v_hi = F(source["public_deterministic_caps"]["conditional_action_mean"])
    f_hi = F(source["public_deterministic_caps"]["immutable_brier"])
    v_lo, f_lo = F(n) - v_hi, F(t) - 2 * variance_sum - f_hi
    intervals = {
        "conditional_action_mean": intersect(uc - rho, uc + rho, v_lo, v_hi),
        "immutable_brier": intersect(ac - rho, ac + rho, f_lo, f_hi),
        "realized_terminal_errors": intersect(uc - rho - action_radius, uc + rho + action_radius, F(0), F(n)),
    }
    empty = [key for key, interval in intervals.items() if interval["empty"]]
    numeric_tests = {
        "brier_lower_above_T_over_4": intervals["immutable_brier"]["lower"] > F(t, 4),
        "conditional_upper_below_n_over_2": intervals["conditional_action_mean"]["upper"] < F(n, 2),
        "conditional_lower_above_n_over_2": intervals["conditional_action_mean"]["lower"] > F(n, 2),
    }
    certificate_labels = {key: None if empty else value for key, value in numeric_tests.items()}
    return {
        "kind": source["kind"], "name": source["name"], "T": t, "B": source["B"], "m": m,
        "unbought_rounds_n": n, "state_bits": source["state_bits"], "action_bits": source["action_bits"], "seed": source["seed"],
        "U_centered_total": uc, "A_centered_total": ac, "Q": q, "R": r, "fixed_lambda": F(8, r),
        "two_sided_sampling_radius": rho, "two_sided_sampling_radius_upper_9R_over_8": F(9 * r, 8),
        "two_sided_action_radius": action_radius,
        "action_integer_enclosure": {"exact_radicand": F(5 * n, 2), "ceiling_radicand": action_radicand,
                                     "ceiling_square_root": action_radius},
        "public_variance_sum": variance_sum,
        "shared_deviation_public_correction": F(source["shared_deviation_public_correction"]),
        "intervals": intervals, "empty_intersections": empty,
        "row_disposition": "confidence_conflict" if empty else "nonempty_intersections",
        "numeric_endpoint_tests_not_valid_labels_if_conflict": numeric_tests,
        "certificate_labels": certificate_labels,
        "nulls": {"immutable_half_forecast_brier": F(t, 4), "same_selected_receipts_conditional_action_mean": F(n, 2)},
        "label_scope": "Strict endpoint tests under the fair-bit theorem premise. On any empty intersection, all ordinary certificate labels are null; the row and conflicting endpoints remain retained.",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--centered-public-stage", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    public_dir, out = Path(args.centered_public_stage).resolve(), Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=False)
    allowed = {DESIGN.resolve(), Path(__file__).resolve(), (public_dir / "result.json").resolve(),
               (public_dir / "public_stage_complete.json").resolve()}
    events, rows = [], []
    started = time.perf_counter_ns()
    result = {"status": "FAIL", "stage": "DEVELOPMENT", "version": VERSION, "principal_clock_credit_ns": 0}

    def consume(path, parse):
        path = path.resolve()
        if path not in allowed:
            raise PermissionError("Only sealed public sufficient statistics/source/design may be read.")
        payload = path.read_bytes()
        record = {"path": str(path.relative_to(ROOT)), "bytes": len(payload), "sha256": sha(payload),
                  "mode": "public_json" if parse else "source_or_design_digest_only", "private_input": False}
        events.append(record)
        return (json.loads(payload) if parse else None), record

    try:
        _, source_binding = consume(Path(__file__), False)
        _, design_binding = consume(DESIGN, False)
        seal, seal_binding = consume(public_dir / "public_stage_complete.json", True)
        public, public_binding = consume(public_dir / "result.json", True)
        if (seal["status"] != "PASS" or seal["private_score_reads_before_closure"] != 0
                or seal["rows"] != 23 or public_binding["sha256"] != seal["result_sha256"]
                or public["status"] != "PASS" or public["version"] != "observable-centered-public-certificate-v1"
                or len(public["rows"]) != 23):
            raise AssertionError("The unchanged sealed centered public result is required.")
        if (sum(r["kind"] == "uniform" for r in public["rows"]) != 20
                or sum(r["kind"] == "adaptive" for r in public["rows"]) != 3):
            raise AssertionError("Retain exactly the existing20 uniform and3 adaptive episodes.")
        exp5_partial_lower = sum((F(5 ** j, math.factorial(j)) for j in range(6)), F(0))
        if exp5_partial_lower <= 80:
            raise AssertionError("Exact partial-series witness must establish log80<5.")
        write(out / "protocol.json", {
            "stage": "DEVELOPMENT", "started_utc": utc(), "command": sys.argv,
            "source_binding": source_binding, "prospective_design_binding": design_binding,
            "sealed_public_result_binding": public_binding, "seal_binding": seal_binding,
            "input_boundary": "Only sealed centered public sufficient statistics, their seal, this source and the saved design. No private score, raw archive or newly computed label is read.",
            "exact_log80_witness": {"sum_j0_through5_of_5_power_j_over_factorial_j": exp5_partial_lower,
                                    "strictly_greater_than80": True},
            "confidence_contract": "One-sided sampling tails1/80 each share the same V/F residual. Two action tails1/80 each give joint fixed-end two-sided V,F,terminal coverage at least19/20 for one fresh-fair-bit episode; no simultaneous23-arm or anytime-terminal guarantee.",
            "development_boundary": "Design was saved after earlier analysis/private scores were exposed; this is additional DEVELOPMENT diagnostic arithmetic, not a new confirmatory experiment. Deterministic seeds do not establish coverage.",
            "override_boundary": "All intervals describe the unchanged base forecasts/purchase/update paths. Lower bounds and the predictability proof do not automatically transfer to paid-answer overrides; no override is analyzed here.",
            "analysis_cost_scope": "Offline analysis only; no observed deployed invoice changes or free online-computation claim.",
            "environment": {"python": sys.version, "platform": platform.platform()}, "principal_clock_credit_ns": 0,
        })
        rows = [calculate(source) for source in public["rows"]]
        if len(rows) != 23:
            raise AssertionError("No diagnostic row may be dropped.")
        # Re-read only the same permitted public/source/design bytes to pin
        # this completed calculation; no post-hoc parameter changes occur.
        for binding in (source_binding, design_binding, public_binding, seal_binding):
            if sha((ROOT / binding["path"]).read_bytes()) != binding["sha256"]:
                raise RuntimeError("Public input or prospective design changed during calculation.")
        result.update(status="PASS", rows=rows, source_binding=source_binding,
                      prospective_design_binding=design_binding, sealed_centered_result_sha256=public_binding["sha256"],
                      all23rows_retained=True, empty_intersection_rows=sum(bool(r["empty_intersections"]) for r in rows),
                      certificate_counts={key: sum(r["certificate_labels"][key] is True for r in rows)
                                          for key in rows[0]["certificate_labels"]},
                      interpretation="Endpoint certificates are formula-based under the per-episode fair-bit theorem premises; fixed seeded rows and their displayed counts do not validate coverage or a simultaneous family guarantee.",
                      new_policy_calls=0, new_service_calls=0, new_rng_calls=0, new_truth_calls=0)
    except BaseException as error:
        result.update(error=repr(error), traceback=traceback.format_exc(), completed_rows=rows,
                      disposition="Failure and partial rows retained; no private comparison, new run, retry or tuning follows.")
    result.update(finished_utc=utc(), elapsed_runtime_ns=time.perf_counter_ns() - started)
    write(out / "reader_audit.json", {"status": result["status"], "events": events,
                                      "private_summaries_opened": 0, "private_members_opened": 0,
                                      "raw_archives_opened": 0, "new_labels_computed": 0,
                                      "rows_retained": len(rows), "principal_clock_credit_ns": 0})
    write(out / "result.json", result)
    if result["status"] == "PASS":
        write(out / "public_stage_complete.json", {"status": "PASS", "closed_utc": utc(), "rows": len(rows),
                                                   "result_sha256": sha((out / "result.json").read_bytes()),
                                                   "reader_audit_sha256": sha((out / "reader_audit.json").read_bytes()),
                                                   "private_input_reads": 0,
                                                   "disposition": "Final planned public-only diagnostic complete. Retain all rows and stop; no further analysis/policy execution selected."})
    print(json.dumps({"status": result["status"], "rows": len(rows),
                      "empty_intersection_rows": result.get("empty_intersection_rows"),
                      "certificate_counts": result.get("certificate_counts"),
                      "elapsed_runtime_ns": result["elapsed_runtime_ns"]}), flush=True)
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
