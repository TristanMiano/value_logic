"""Frozen-source asymmetric policy execution, then separate private scoring.

P3-08 DEVELOPMENT; no principal-clock credit. This harness never modifies a
policy. Public mode reads only common_v2 public inputs/records and source;
score mode reads already sealed principal reference answers after a new seal.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
from fractions import Fraction as F
import gzip
import hashlib
import json
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parents[4]
LOG = REPO / "v3/work_logs/P3_08_2026-10-10_S1"
PARENT = LOG / "development/common_v2"
VERSION = "p308-asymmetric-harness-v1"
SEEDS = (11, 29, 47)
PRICES = ("0", "1/10000")
STAKES = (("fp_low", "1/2", "3/2"), ("fp_high", "3/2", "1/2"),
          ("symmetric", "1", "1"))


def utc():
    return datetime.now(timezone.utc).isoformat()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pair(value):
    value = F(value)
    return [value.numerator, value.denominator]


def verify_files(root, seal):
    for row in seal["files"]:
        assert sha(root / row["path"]) == row["sha256"], row["path"]


def jobs():
    for stake, fp, fn in STAKES:
        for price in PRICES:
            for method in ("probability_cost", "ordinary_combo_hashed"):
                for seed in SEEDS:
                    job = {"stake": stake, "fp": fp, "fn": fn, "policy_price": price,
                           "method": method, "seed": seed, "role": "normalized",
                           "evaluation_prices": [price]}
                    job["run_id"] = f"{stake}__{method}__seed{seed}__price{price.replace('/', '_')}"
                    yield job
        for method in ("exact_dpll", "no_compute_0", "no_compute_1"):
            yield {"stake": stake, "fp": fp, "fn": fn, "policy_price": "0",
                   "method": method, "seed": 11, "role": "fixed_normalized",
                   "evaluation_prices": list(PRICES),
                   "run_id": f"{stake}__{method}__seed11__pricefixed"}
    for price in PRICES:
        for method in ("probability_cost", "ordinary_combo_hashed"):
            for seed in SEEDS:
                raw_price = str(2 * F(price))
                yield {"stake": "raw_fp1_fn3", "fp": "1", "fn": "3",
                       "policy_price": raw_price, "method": method, "seed": seed,
                       "role": "raw_scale_check", "evaluation_prices": [raw_price],
                       "normalized_run": f"fp_low__{method}__seed{seed}__price{price.replace('/', '_')}",
                       "run_id": f"raw_fp1_fn3__{method}__seed{seed}__price{raw_price.replace('/', '_')}"}


def invocation(job, C, source_units):
    method = job["method"]
    actual = "ordinary_combo" if method == "ordinary_combo_hashed" else method
    kwargs = {"seed": job["seed"], "unit_limit": C.MAX_UNITS - source_units}
    if method.startswith("no_compute_"):
        actual = "no_compute"
        kwargs["fallback_action"] = int(method[-1])
    if method == "ordinary_combo_hashed":
        kwargs["cache_kind"] = "hashed"
        kwargs["unit_price"] = job["policy_price"]
    elif job["policy_price"] != "0":
        kwargs["unit_price"] = job["policy_price"]
    if job["stake"] != "symmetric":
        kwargs["false_positive_price"] = job["fp"]
        kwargs["false_negative_price"] = job["fn"]
    return actual, kwargs


def reference_id(job):
    if job["stake"] != "symmetric":
        return None
    if job["method"] == "probability_cost" and job["policy_price"] != "0":
        return None
    suffix = job["policy_price"].replace("/", "_") if job["method"] == "ordinary_combo_hashed" else "fixed"
    return f"cold_mixed__{job['method']}__seed{job['seed']}__price{suffix}"


def load_modules(out):
    sys.path.insert(0, str(out / "source/v3/experiments"))
    import p308_run as R
    import p308_ordinary as O
    import p308_cnf as S
    from p308_common import C, registry_setup
    return R, O, S, C, registry_setup


def public_checks(records):
    checks = []
    for record in records.values():
        job, episode = record["configuration"], record["episode"]
        assert episode["status"] == "success" and len(episode["trace"]) == 64
        assert all(row["index"] == i for i, row in enumerate(episode["trace"]))
        assert episode["price_record"] == {"false_positive": pair(job["fp"]),
                                             "false_negative": pair(job["fn"]),
                                             "unit": pair(job["policy_price"])}
        if job["method"] in ("probability_cost", "ordinary_combo_hashed"):
            for row in episode["trace"]:
                q = F(*row["base_q"])
                assert row["base_action"] == int(F(job["fp"]) * (1 - q) < F(job["fn"]) * q)
    checks.append({"name": "all_completed_price_records_and_exact_greedy_thresholds", "records": len(records)})

    same_history = []
    for seed in SEEDS:
        reference = records[f"symmetric__probability_cost__seed{seed}__price0"]["episode"]
        for stake, _, _ in STAKES:
            for price in PRICES:
                episode = records[f"{stake}__probability_cost__seed{seed}__price{price.replace('/', '_')}"]["episode"]
                assert episode["blocks"] == reference["blocks"]
                assert episode["weights"] == reference["weights"]
                assert episode["invoices"] == reference["invoices"]
                for a, b in zip(episode["trace"], reference["trace"]):
                    assert all(a[key] == b[key] for key in (
                        "index", "query_id", "claim_key", "advice", "base_q", "emitted_q",
                        "selected", "propensity", "purchased_label"))
        same_history.append(seed)
    checks.append({"name": "probability_readout_own_feedback_and_numeric_path_fixed", "seeds": same_history})

    scale = []
    for record in records.values():
        job = record["configuration"]
        if job["role"] != "raw_scale_check":
            continue
        raw, norm = record["episode"], records[job["normalized_run"]]["episode"]
        assert raw["blocks"] == norm["blocks"] and raw["weights"] == norm["weights"]
        assert raw["invoices"] == norm["invoices"]
        assert all(raw[key] == norm[key] for key in (
            "purchases", "successful_purchases", "cache_hits", "provider_failures",
            "feedback_updates", "cost_history", "random_bits_consumed"))
        for a, b in zip(raw["trace"], norm["trace"]):
            assert {k: v for k, v in a.items() if k != "estimated_error_cost"} == {
                k: v for k, v in b.items() if k != "estimated_error_cost"}
            assert F(*a["estimated_error_cost"]) == 2 * F(*b["estimated_error_cost"])
        scale.append({"raw_run": record["run_id"], "normalized_run": job["normalized_run"],
                      "actions_acquisitions_state_equal": True,
                      "raw_minus_normalized_local_units": raw["meter"]["total"] - norm["meter"]["total"]})
    checks.append({"name": "raw_price_homogeneity_public_path", "cases": scale})
    return checks


def public(out):
    out.mkdir(parents=True, exist_ok=False)
    parent_run = PARENT / "run"
    parent_seal = json.loads((parent_run / "public_seal.json").read_text())
    verify_files(parent_run, parent_seal)
    source_rows = json.loads((parent_run / "source_before.json").read_text())["sources"]
    for row in source_rows:
        source = PARENT / "source" / row["path"]
        assert sha(source) == row["sha256"]
        target = out / "source" / row["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())
    for name in ("asymmetric_plan_v1.md", "asymmetric_development_run.py"):
        target = out / "research" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(Path(__file__).with_name(name).read_bytes())
    R, O, S, C, registry_setup = load_modules(out)
    assert O.VERSION == "p308-ordinary-controllers-v1.4"
    assert R.source_manifest() == source_rows
    save(out / "source_before.json", {"created_utc": utc(), "sources": source_rows})
    supplied = json.loads((parent_run / "public_inputs.json").read_text())["tapes"]["cold_mixed"]
    tape = tuple(S.Query(row["query_id"], row["variables"], tuple(tuple(c) for c in row["clauses"]),
                         row["source_version"], row["semantics_version"]) for row in supplied)
    assert len(tape) == 64
    save(out / "public_inputs.json", {"stage": "DEVELOPMENT", "scenario": "cold_mixed", "tape": supplied,
         "parent_public_inputs_sha256": sha(parent_run / "public_inputs.json"), "already_development_exposed": True})
    declared = list(jobs())
    assert len(declared) == 57 and len({j["run_id"] for j in declared}) == 57
    needed = {reference_id(j) for j in declared if reference_id(j) is not None}
    parent_index = {r["run_id"]: r for r in json.loads((parent_run / "public_index.json").read_text())["records"]}
    references = {}
    with gzip.open(parent_run / "public_records.jsonl.gz", "rt") as archive:
        for line in archive:
            record = json.loads(line)
            if record["run_id"] in needed:
                assert hashlib.sha256(line.rstrip("\n").encode()).hexdigest() == parent_index[record["run_id"]]["record_sha256"]
                references[record["run_id"]] = record
    assert set(references) == needed and len(needed) == 12
    save(out / "run_contract.json", {"stage": "DEVELOPMENT", "version": VERSION, "created_utc": utc(),
         "python": sys.version, "principal_clock_credit_ns": 0, "jobs": declared,
         "CORE_SOURCES": list(R.CORE_SOURCES), "expected_source_units": 48274,
         "plan_sha256": sha(out / "research/asymmetric_plan_v1.md"),
         "parent_public_seal_sha256": sha(parent_run / "public_seal.json"),
         "fresh_runs_expected": 45, "reused_records_expected": 12,
         "private_reference_answers_read": False, "held_out": False})
    records, index = {}, []
    with (out / "public_records.jsonl.gz").open("wb") as raw:
        with gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as archive:
            for number, job in enumerate(declared, 1):
                setup = C.CostMeter()
                sources = registry_setup([R.REPO / path for path in R.CORE_SOURCES], setup)
                assert setup.total == 48274
                actual, kwargs = invocation(job, C, setup.total)
                ref = reference_id(job)
                if ref is None:
                    episode = O.run_method(tape, actual, **kwargs)
                    execution_kind = "fresh_execution"
                else:
                    prior = references[ref]
                    conf = prior["configuration"]
                    old_kwargs = {"seed": conf["seed"], "unit_limit": C.MAX_UNITS - prior["common_source_invoice"]["total"]}
                    old_kwargs.update({key: conf[key] for key in (
                        "proof_cap", "proof_solver", "unit_price", "cache_kind", "fallback_action") if key in conf})
                    assert actual == conf["ordinary_method"] and kwargs == old_kwargs
                    assert prior["common_source_invoice"] == setup.snapshot()
                    assert prior["common_sources"] == sources
                    episode = prior["episode"]
                    execution_kind = "reused_identical_common_v2_record"
                record = {"stage": "DEVELOPMENT", "run_id": job["run_id"], "scenario": "cold_mixed",
                          "configuration": job, "invocation": {"method": actual, "kwargs": kwargs},
                          "execution_kind": execution_kind, "reference_run": ref,
                          "reference_record_sha256": None if ref is None else parent_index[ref]["record_sha256"],
                          "common_source_invoice": setup.snapshot(), "common_sources": sources,
                          "episode": episode}
                encoded = canonical(record).encode()
                archive.write(encoded + b"\n")
                records[job["run_id"]] = record
                index.append({"run_id": job["run_id"], "configuration": job, "execution_kind": execution_kind,
                              "record_sha256": hashlib.sha256(encoded).hexdigest(), "status": episode["status"],
                              "rounds_closed": episode["rounds_closed"], "local_units": episode["meter"]["total"],
                              "source_units": setup.total, "purchases": episode["purchases"]})
                if number % 6 == 0 or number == len(declared):
                    print(canonical({"public_records_completed": number, "total": len(declared),
                                     "latest": job["run_id"], "status": episode["status"]}), flush=True)
    checks = public_checks(records)
    save(out / "public_checks.json", {"stage": "DEVELOPMENT", "status": "PASS", "checks": checks})
    after = R.source_manifest()
    assert after == source_rows
    save(out / "source_after.json", {"created_utc": utc(), "sources": after, "unchanged": True})
    save(out / "public_index.json", {"stage": "DEVELOPMENT", "records": index})
    seal_names = ["public_inputs.json", "run_contract.json", "public_records.jsonl.gz", "public_index.json",
                  "public_checks.json", "source_before.json", "source_after.json",
                  "research/asymmetric_plan_v1.md", "research/asymmetric_development_run.py"]
    seal_names += ["source/" + row["path"] for row in source_rows]
    save(out / "public_seal.json", {"stage": "DEVELOPMENT", "sealed_utc": utc(),
         "private_scoring_performed": False,
         "files": [{"path": name, "sha256": sha(out / name), "bytes": (out / name).stat().st_size} for name in seal_names]})
    return {"public_status": "sealed", "records": len(index), "fresh": 45, "reused": 12,
            "public_seal_sha256": sha(out / "public_seal.json")}


def score(out):
    public_seal = json.loads((out / "public_seal.json").read_text())
    verify_files(out, public_seal)
    assert sha(Path(__file__)) == sha(out / "research/asymmetric_development_run.py")
    private = out / "private"
    private.mkdir(exist_ok=False)
    parent_private = PARENT / "run/private"
    parent_seal = json.loads((parent_private / "seal.json").read_text())
    truth_ref = next(row for row in parent_seal["files"] if row["path"] == "truth.json")
    assert sha(parent_private / "truth.json") == truth_ref["sha256"]
    truth = json.loads((parent_private / "truth.json").read_text())["answers"]["cold_mixed"]
    original_tape = json.loads((PARENT / "run/public_inputs.json").read_text())["tapes"]["cold_mixed"]
    assert json.loads((out / "public_inputs.json").read_text())["tape"] == original_tape
    save(private / "reference.json", {"stage": "DEVELOPMENT", "created_utc": utc(),
         "parent_truth_path": str((parent_private / "truth.json").relative_to(REPO)),
         "parent_truth_sha256": truth_ref["sha256"], "public_seal_sha256": sha(out / "public_seal.json"),
         "reference_read_after_new_public_seal": True, "new_truth_evaluation": False,
         "principal_clock_credit_ns": 0})
    index = {row["run_id"]: row for row in json.loads((out / "public_index.json").read_text())["records"]}
    scored, economic, full = {}, [], {}
    with gzip.open(out / "public_records.jsonl.gz", "rt") as archive:
        for line in archive:
            record = json.loads(line)
            rid, episode, job = record["run_id"], record["episode"], record["configuration"]
            assert hashlib.sha256(line.rstrip("\n").encode()).hexdigest() == index[rid]["record_sha256"]
            assert episode["status"] == "success" and len(episode["trace"]) == len(truth) == 64
            fp = fn = 0
            brier = F(0)
            for i, (row, y) in enumerate(zip(episode["trace"], truth)):
                assert row["index"] == i and row["query_id"] == original_tape[i]["query_id"]
                fp += int(row["terminal_action"] == 1 and y == 0)
                fn += int(row["terminal_action"] == 0 and y == 1)
                brier += (F(*row["emitted_q"]) - y)**2
                if row["purchased_label"] is not None:
                    assert row["purchased_label"] == y
                if row["hard_after"]["status"] == "checked":
                    assert row["hard_after"]["answer"] == y
            task_loss = F(job["fp"]) * fp + F(job["fn"]) * fn
            units = episode["meter"]["total"] + record["common_source_invoice"]["total"]
            native = task_loss + F(job["policy_price"]) * units
            summary = {**index[rid], "false_positives": fp, "false_negatives": fn,
                       "terminal_errors": fp + fn, "task_loss": pair(task_loss), "issued_brier": pair(brier),
                       "cold_units": units, "native_objective": pair(native),
                       "cache_hits": episode["cache_hits"], "feedback_updates": episode["feedback_updates"],
                       "provider_failures": episode["provider_failures"], "full_horizon": True}
            scored[rid], full[rid] = summary, record
            if job["role"] != "raw_scale_check":
                for price in job["evaluation_prices"]:
                    economic.append({"run_id": rid, "stake": job["stake"], "method": job["method"],
                                     "seed": job["seed"], "evaluation_price": price,
                                     "evaluation_kind": "fixed_record_repricing" if job["role"] == "fixed_normalized" else "native_policy_price",
                                     "false_positives": fp, "false_negatives": fn, "task_loss": pair(task_loss),
                                     "local_units": episode["meter"]["total"], "source_units": record["common_source_invoice"]["total"],
                                     "total_objective": pair(task_loss + F(price) * units),
                                     "purchases": episode["purchases"], "cache_hits": episode["cache_hits"],
                                     "feedback_updates": episode["feedback_updates"], "provider_failures": episode["provider_failures"]})
    scales = []
    for rid, row in scored.items():
        job = row["configuration"]
        if job["role"] != "raw_scale_check":
            continue
        normal = scored[job["normalized_run"]]
        assert F(*row["task_loss"]) == 2 * F(*normal["task_loss"])
        delta_units = row["cold_units"] - normal["cold_units"]
        difference = F(*row["native_objective"]) - 2 * F(*normal["native_objective"])
        assert difference == F(job["policy_price"]) * delta_units
        scales.append({"raw_run": rid, "normalized_run": job["normalized_run"],
                       "task_loss_exactly_doubled": True, "raw_minus_normalized_units": delta_units,
                       "objective_exactly_doubled": difference == 0,
                       "objective_minus_twice_normalized": pair(difference)})
    groups = defaultdict(list)
    for row in economic:
        groups[(row["stake"], row["evaluation_price"], row["method"])].append(row)
    aggregate = []
    for (stake, price, method), rows in sorted(groups.items()):
        mean = lambda key: sum((F(*row[key]) if isinstance(row[key], list) else F(row[key]) for row in rows), F(0)) / len(rows)
        aggregate.append({"stake": stake, "evaluation_price": price, "method": method,
                          "record_count": len(rows), "coverage_claim": False,
                          **{"mean_" + key: pair(mean(key)) for key in (
                              "false_positives", "false_negatives", "task_loss", "local_units", "source_units",
                              "total_objective", "purchases", "cache_hits", "feedback_updates", "provider_failures")}})
    behavior = []
    for method in ("probability_cost", "ordinary_combo_hashed"):
        for price in PRICES:
            for seed in SEEDS:
                sym_id = f"symmetric__{method}__seed{seed}__price{price.replace('/', '_')}"
                sym = full[sym_id]["episode"]
                for stake in ("fp_low", "fp_high"):
                    rid = f"{stake}__{method}__seed{seed}__price{price.replace('/', '_')}"
                    ep = full[rid]["episode"]
                    behavior.append({"run_id": rid, "symmetric_run": sym_id,
                        "base_action_changes": sum(a["base_action"] != b["base_action"] for a, b in zip(ep["trace"], sym["trace"])),
                        "terminal_action_changes": sum(a["terminal_action"] != b["terminal_action"] for a, b in zip(ep["trace"], sym["trace"])),
                        "base_forecast_changes": sum(a["base_q"] != b["base_q"] for a, b in zip(ep["trace"], sym["trace"])),
                        "purchase_delta": ep["purchases"] - sym["purchases"],
                        "feedback_update_delta": ep["feedback_updates"] - sym["feedback_updates"],
                        "same_provider_invoice_sequence": ep["invoices"] == sym["invoices"]})
    save(private / "scores.json", {"stage": "DEVELOPMENT", "runs": list(scored.values()),
         "economic_rows": economic, "aggregates": aggregate, "homogeneity_checks": scales,
         "behavior_against_symmetric_reference": behavior, "principal_clock_credit_ns": 0,
         "interpretation": "Post-inspection development behavior and units; fixed-record repricing is separate from new paid acquisition/online-update paths."})
    verify_files(out, public_seal)
    save(private / "seal.json", {"stage": "DEVELOPMENT", "scored_utc": utc(),
         "public_seal_sha256": sha(out / "public_seal.json"),
         "files": [{"path": name, "sha256": sha(private / name)} for name in ("reference.json", "scores.json")]})
    return {"private_status": "sealed", "public_records_scored": len(scored),
            "economic_rows": len(economic), "raw_homogeneity_checks": len(scales),
            "all_raw_objectives_exactly_doubled": all(row["objective_exactly_doubled"] for row in scales),
            "scores_sha256": sha(private / "scores.json")}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("public", "score"))
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    print(canonical(public(args.out.resolve()) if args.command == "public" else score(args.out.resolve())))
