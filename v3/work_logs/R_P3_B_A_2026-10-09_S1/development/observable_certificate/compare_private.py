"""Separate second stage: compare sealed observable bounds to saved scores.

ChatGPT (GPT-6 Astra Pro), 2026-10-09 UTC. DEVELOPMENT, zero principal credit.
This program reads already existing private score summaries only after it
verifies the public-stage completion seal. It runs no policy, service, RNG
or truth calculation. A saved inequality holding is descriptive, not a
coverage experiment or an acceptance test for a random theorem.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time
import traceback


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
DEVELOPMENT = HERE.parent
PRIVATE_PATHS = {
    "uniform": DEVELOPMENT / "service_comparison/run_001/result.json",
    "adaptive": DEVELOPMENT / "allocation_comparison/run_001/result.json",
}
METRICS = {
    "conditional_action_mean": ("conditional_action_mean_upper_clipped", "conditional_expected_terminal_01_loss"),
    "realized_terminal": ("realized_terminal_upper_clipped", "terminal_sampled_01_loss"),
    "immutable_brier": ("immutable_brier_upper_clipped", "immutable_issued_brier"),
}


def utc():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    temporary = path.with_name(path.name + ".writing")
    temporary.write_text(json.dumps(value, indent=2, default=str) + "\n")
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--public-stage", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    public_dir, out = Path(args.public_stage).resolve(), Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter_ns()
    opened, rows = [], []
    result = {"status": "FAIL", "stage": "DEVELOPMENT", "version": "observable-private-comparison-v1",
              "principal_clock_credit_ns": 0}
    try:
        seal = json.loads((public_dir / "public_stage_complete.json").read_text())
        if (seal["status"] != "PASS" or seal["rows"] != 23 or seal["private_score_reads_before_closure"] != 0
                or sha(public_dir / "result.json") != seal["result_sha256"]
                or sha(public_dir / "reader_audit.json") != seal["reader_audit_sha256"]
                or sha(public_dir / "selected_observations.zip") != seal["selected_observations_archive_sha256"]):
            raise AssertionError("A complete immutable public-only first stage is required.")
        public = json.loads((public_dir / "result.json").read_text())
        if public["status"] != "PASS" or len(public["rows"]) != 23:
            raise AssertionError("Public-only result did not complete all23 rows.")
        comparison_started = utc()
        if datetime.fromisoformat(comparison_started) < datetime.fromisoformat(seal["closed_utc"]):
            raise AssertionError("Comparison clock precedes public-stage closure.")
        # The first private file open occurs strictly after every seal check.
        private, private_hashes = {}, {}
        for kind, path in PRIVATE_PATHS.items():
            payload = path.read_bytes()
            value = json.loads(payload)
            if value["status"] != "PASS":
                raise AssertionError("Existing observed score result was not PASS.")
            digest = hashlib.sha256(payload).hexdigest()
            private[kind], private_hashes[kind] = value, digest
            opened.append({"kind": kind, "path": str(path.relative_to(ROOT)), "sha256": digest,
                           "bytes": len(payload), "opened_after_public_stage_closed": True})
        for certificate in public["rows"]:
            kind = certificate["kind"]
            observed = next(r for r in private[kind]["learner_arms"] if r["name"] == certificate["name"])
            if (observed["horizon"] != certificate["T"] or observed["block_size"] != certificate["B"]
                    or observed["seed"] != certificate["seed"]):
                raise AssertionError("Private comparison does not bind the certified episode.")
            bindings = certificate["input_bindings"]
            if kind == "uniform":
                if private_hashes[kind] != bindings["expected_prior_private_result_sha256_from_manifest_only"]:
                    raise AssertionError("Uniform private score file differs from the public manifest's recorded digest.")
            elif observed["source_plan_hashes"] != bindings["observed_policy_source_plan_hashes"]:
                raise AssertionError("Adaptive private summary has a different observed source/plan closure.")
            metrics = {}
            for metric, (bound_field, score_field) in METRICS.items():
                bound = F(certificate[bound_field])
                score = F(observed["evaluation"][score_field])
                metrics[metric] = {"public_only_upper": bound, "saved_private_score": score,
                                   "upper_minus_saved_score": bound - score,
                                   "saved_inequality_holds": score <= bound}
            rows.append({"kind": kind, "name": certificate["name"], "T": certificate["T"],
                         "B": certificate["B"], "state_bits": certificate["state_bits"], "seed": certificate["seed"],
                         "public_certificate_result_sha256": seal["result_sha256"],
                         "existing_private_result_sha256": private_hashes[kind], "comparisons": metrics})
        if sha(public_dir / "result.json") != seal["result_sha256"] or sha(public_dir / "reader_audit.json") != seal["reader_audit_sha256"]:
            raise AssertionError("The first-stage outputs changed during comparison.")
        result.update(status="PASS", rows=rows, public_method_version=public["version"],
                      public_stage_closed_utc=seal["closed_utc"], private_comparison_started_utc=comparison_started,
                      public_result_sha256=seal["result_sha256"], public_reader_audit_sha256=seal["reader_audit_sha256"],
                      comparison_source_sha256=sha(Path(__file__)),
                      descriptive_inequality_counts={metric: sum(r["comparisons"][metric]["saved_inequality_holds"] for r in rows)
                                                    for metric in METRICS},
                      interpretation="Fixed seeded traces instantiate formulas; these comparisons do not estimate, validate or jointly establish the stated confidence coverage. No policy selection or new scientific run follows.",
                      new_policy_calls=0, new_service_calls=0, new_rng_calls=0, new_truth_calls=0)
    except BaseException as error:
        result.update(error=repr(error), traceback=traceback.format_exc(), completed_rows=rows,
                      disposition="Comparison failure retained; public-only output is unchanged and no procedure is retried.")
    result.update(finished_utc=utc(), elapsed_runtime_ns=time.perf_counter_ns() - started)
    write(out / "reader_audit.json", {"status": result["status"], "private_score_reads": opened,
                                      "kind": "Separate comparison stage only; existing private summaries, no private truth recomputation.",
                                      "command": sys.argv, "principal_clock_credit_ns": 0})
    write(out / "result.json", result)
    print(json.dumps({"status": result["status"], "rows": len(rows),
                      "descriptive_inequality_counts": result.get("descriptive_inequality_counts"),
                      "elapsed_runtime_ns": result["elapsed_runtime_ns"]}), flush=True)
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
