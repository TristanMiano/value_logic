"""Source-sealed public execution and separate private scoring for P3-08.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-10. DEVELOPMENT only.
This is experiment infrastructure, not a deployed policy or a final challenge.
Run a copied full source closure. Public execution never calls private_score.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
import gzip
import hashlib
import json
from pathlib import Path
import platform
import sys

import p308_broker as B
import p308_cnf as S
import p308_mirrors as M
import p308_ordinary as O
import p308_reporting as P
from p308_common import C, REPO, canonical, fraction_record, registry_setup

VERSION = "p308-development-runner-v1"
SEEDS = (11, 29, 47)
PRICES = ("0", "1/100000", "1/10000", "1/1000", "1/100")
CORE_SOURCES = (
    "v3/experiments/p308_common.py", "v3/experiments/p308_broker.py",
    "v3/experiments/p308_cnf.py", "v3/experiments/p308_ordinary.py",
    "v3/experiments/p308_mirrors.py", "v3/checks/07_selective_feedback.py",
    "v3/checks/07_selective_feedback_service.py", "v3/checks/07_computation_adapter.py")
ALL_SOURCES = CORE_SOURCES + ("v3/experiments/p308_reporting.py", "v3/experiments/p308_run.py")


def utc():
    return datetime.now(timezone.utc).isoformat()


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def source_manifest():
    return [{"path": name, "bytes": (REPO/name).stat().st_size,
             "sha256": sha(REPO/name)} for name in ALL_SOURCES]


def cohorts():
    cold = S.make_development_queries(seed=3081013, count=64, prefix="cold-mixed")
    repeat = tuple(S.Query(f"repeat-online-{i:05d}", cold[i % 32].variables,
                           cold[i % 32].clauses, cold[i % 32].source_version)
                   for i in range(128))
    shapes = (((-1,), (1,)), tuple((i,) for i in range(1, 13)), (), ((),))
    easy = tuple(S.make_query(f"cheap-structure-{i:05d}", 12, shapes[i % 4])
                 for i in range(64))
    return {"cold_mixed": cold, "repeat_online": repeat, "cheap_structure": easy}


def jobs():
    for seed in SEEDS:
        for selector in ("uniform", "tickets"):
            for hard in (False, True):
                yield {"method": ("value_" if hard else "finite_") + selector,
                       "kind": "broker", "seed": seed, "selector": selector,
                       "hard": hard, "solver": "dpll"}
        yield {"method": "finite_uniform_enumeration", "kind": "broker", "seed": seed,
               "selector": "uniform", "hard": False, "solver": "enumeration"}
        yield {"method": "probability_cost", "kind": "ordinary", "seed": seed,
               "ordinary_method": "probability_cost"}
        for price in PRICES:
            yield {"method": "ordinary_combo", "kind": "ordinary", "seed": seed,
                   "ordinary_method": "ordinary_combo", "unit_price": price}
    # These deterministic policies need one execution, not three duplicate seeds.
    for method, kwargs in (
        ("proof_enumeration", {"ordinary_method": "proof_only", "proof_solver": "enumeration", "proof_cap": 2048}),
        ("proof_dpll", {"ordinary_method": "proof_only", "proof_solver": "dpll", "proof_cap": 2048}),
        ("exact_enumeration", {"ordinary_method": "proof_only", "proof_solver": "enumeration", "proof_cap": 1 << 32}),
        ("exact_dpll", {"ordinary_method": "exact_dpll"}),
        ("exact_cache", {"ordinary_method": "exact_cache"}),
    ):
        yield {"method": method, "kind": "ordinary", "seed": SEEDS[0], **kwargs}


def public_run(out):
    out = Path(out).resolve()
    out.mkdir(parents=True, exist_ok=False)
    before = source_manifest()
    save(out/"source_before.json", {"created_utc": utc(), "sources": before})
    save(out/"run_contract.json", {"stage": "DEVELOPMENT", "version": VERSION,
         "python": sys.version, "platform": platform.platform(),
         "seeds": SEEDS, "resource_prices": PRICES, "jobs": list(jobs()),
         "policy_truth_access": False, "random_seed_is_coverage_evidence": False,
         "plan": "comparison_plan_v1.md", "public_generation_seed": 3081013,
         "core_sources": CORE_SOURCES,
         "report_source": "v3/experiments/p308_reporting.py",
         "ordinary_mirrors": "Same executable kernel and bill; representation controls, not extra trials."})
    tapes = cohorts()
    inputs = {name: [q.record() for q in tape] for name, tape in tapes.items()}
    save(out/"public_inputs.json", {"created_utc": utc(), "stage": "DEVELOPMENT", "tapes": inputs})
    index = []
    record_path = out/"public_records.jsonl.gz"
    with record_path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as archive:
            for name, tape in tapes.items():
                for job in jobs():
                    suffix = job.get("unit_price", "fixed").replace("/", "_")
                    run_id = f"{name}__{job['method']}__seed{job['seed']}__price{suffix}"
                    setup = C.CostMeter()
                    sources = registry_setup([REPO/p for p in CORE_SOURCES], setup)
                    if job["kind"] == "broker":
                        contract = B.Contract(len(tape), selector=job["selector"])
                        episode = B.execute(S, tape, contract, seed=job["seed"], hard=job["hard"],
                                            purchase_solver=job["solver"], unit_limit=C.MAX_UNITS-setup.total)
                        report_setup = C.CostMeter()
                        report_source = registry_setup([REPO/"v3/experiments/p308_reporting.py"], report_setup)
                        report = P.report_owned_episode(S, episode,
                            unit_limit=C.MAX_UNITS-setup.total-episode["meter"]["total"]-report_setup.total)
                        optional = {"source_invoice": report_setup.snapshot(), "source": report_source,
                                    "report": report, "additional_units": report_setup.total+report["meter"]["total"]}
                    else:
                        kwargs = {key: job[key] for key in ("proof_cap", "proof_solver", "unit_price") if key in job}
                        episode = O.run_method(tape, job["ordinary_method"], seed=job["seed"],
                                               unit_limit=C.MAX_UNITS-setup.total, **kwargs)
                        optional = None
                    record = {"run_id": run_id, "stage": "DEVELOPMENT", "scenario": name,
                              "configuration": job, "common_source_invoice": setup.snapshot(),
                              "common_sources": sources, "episode": episode, "optional_reporting": optional}
                    encoded = canonical(record).encode()
                    archive.write(encoded+b"\n")
                    entry = {"run_id": run_id, "scenario": name, "configuration": job,
                             "record_sha256": hashlib.sha256(encoded).hexdigest(),
                             "status": episode["status"], "rounds_closed": episode["rounds_closed"],
                             "local_units": episode["meter"]["total"], "source_units": setup.total,
                             "cold_units": setup.total+episode["meter"]["total"],
                             "purchases": episode["purchases"], "optional_reporting_units": None if optional is None else optional["additional_units"]}
                    index.append(entry)
                    print(canonical({k: entry[k] for k in ("run_id", "status", "local_units", "purchases")}), flush=True)
    # A small executable identity check, not a second trial for every arm.
    tape = tuple(S.make_query(f"mirror-{i}", 2, ((1,), (-2,))) for i in range(8))
    mirrors = []
    for hard in (False, True):
        contract = B.Contract(8)
        direct = B.execute(S, tape, contract, seed=11, hard=hard, purchase_solver="dpll")
        ordinary = M.run_ordinary_mixture(S, tape, contract, seed=11, hard=hard, purchase_solver="dpll")
        mirrors.append({"hard": hard, "exact_record_equal": direct == ordinary,
                        "direct_sha256": hashlib.sha256(canonical(direct).encode()).hexdigest(),
                        "ordinary_sha256": hashlib.sha256(canonical(ordinary).encode()).hexdigest(),
                        "units": direct["meter"]["total"]})
        assert direct == ordinary
    save(out/"ordinary_mirrors.json", {"stage": "DEVELOPMENT", "cases": mirrors,
         "interpretation": "Identical implementation/representation, not independent evidence or a separate random trial."})
    after = source_manifest()
    assert before == after, "Source closure changed during execution. Preserve this failed run."
    save(out/"source_after.json", {"created_utc": utc(), "sources": after, "unchanged": True})
    save(out/"public_index.json", {"stage": "DEVELOPMENT", "count": len(index), "records": index})
    seal_files = ("public_inputs.json", "public_records.jsonl.gz", "public_index.json", "ordinary_mirrors.json", "source_before.json", "source_after.json", "run_contract.json")
    save(out/"public_seal.json", {"sealed_utc": utc(), "stage": "DEVELOPMENT", "private_scoring_performed": False,
                                "files": [{"path": p, "sha256": sha(out/p), "bytes": (out/p).stat().st_size} for p in seal_files]})
    return {"out": str(out), "runs": len(index), "archive_bytes": record_path.stat().st_size}


def independent_truth(record):
    """Evaluator-only finite bit-mask enumeration, independent of both solvers."""
    n, clauses = record["variables"], record["clauses"]
    masks = []
    for clause in clauses:
        pos = sum(1 << (x-1) for x in set(clause) if x > 0)
        neg = sum(1 << (-x-1) for x in set(clause) if x < 0)
        masks.append((pos, neg))
    for assignment in range(1 << n):
        if all((assignment & pos) or ((~assignment) & neg) for pos, neg in masks):
            return 1
    return 0


def private_score(out):
    out = Path(out).resolve()
    private = out/"private"
    private.mkdir(exist_ok=False)
    seal = json.loads((out/"public_seal.json").read_text())
    assert all(sha(out/r["path"]) == r["sha256"] for r in seal["files"])
    raw_inputs = json.loads((out/"public_inputs.json").read_text())["tapes"]
    truths, unique = {}, {}
    for name, tape in raw_inputs.items():
        answers = []
        for query in tape:
            key = canonical([query["semantics_version"], query["source_version"], query["variables"], query["clauses"]])
            if key not in unique:
                unique[key] = independent_truth(query)
            answers.append(unique[key])
        truths[name] = answers
    save(private/"truth.json", {"stage": "DEVELOPMENT", "evaluator_only": True,
         "evaluator": "independent finite bit-mask enumeration in p308_run.py",
         "created_after_public_seal": True, "public_seal_sha256": sha(out/"public_seal.json"),
         "unique_programs": len(unique), "answers": truths})
    scored = []
    records = {}
    index = json.loads((out/"public_index.json").read_text())["records"]
    by_id = {r["run_id"]: r for r in index}
    with gzip.open(out/"public_records.jsonl.gz", "rt") as archive:
        for line in archive:
            record = json.loads(line)
            run_id, episode = record["run_id"], record["episode"]
            assert hashlib.sha256(line.rstrip("\n").encode()).hexdigest() == by_id[run_id]["record_sha256"]
            tape_truth = truths[record["scenario"]]
            error = fp = fn = base_error = known_wrong = 0
            f_live = f_base = v_live = v_base = F(0)
            for row, y in zip(episode["trace"], tape_truth):
                q, q0 = F(*row["emitted_q"]), F(*row["base_q"])
                error += int(row["terminal_action"] != y)
                fp += int(row["terminal_action"] == 1 and y == 0)
                fn += int(row["terminal_action"] == 0 and y == 1)
                base_error += int(row["base_terminal"] != y)
                f_live += (q-y)**2
                f_base += (q0-y)**2
                if not row["selected"]:
                    v_live += q+(1-2*q)*y
                    v_base += q0+(1-2*q0)*y
                if row["hard_after"]["status"] == "checked":
                    known_wrong += int(row["hard_after"]["answer"] != y)
                if row["purchased_label"] is not None:
                    assert row["purchased_label"] == y
            assert known_wrong == 0
            report_audit = None
            optional = record["optional_reporting"]
            if optional is not None and optional["report"]["status"] == "success":
                report = optional["report"]
                correction = report["corrections"]
                assert f_base-f_live == F(*correction["F"])
                assert v_base-v_live == F(*correction["V"])
                assert base_error-error == correction["Z"]
                assert v_live-F(*report["live_centers"]["V"]) == f_live-F(*report["live_centers"]["F"])
                covered = {target: F(*report["intervals"][target]["lower"]) <= value <= F(*report["intervals"][target]["upper"])
                           for target, value in (("V", v_live), ("F", f_live), ("Z", F(error)))}
                report_audit = {"exact_corrections_pass": True, "shared_residual_pass": True,
                                "coverage_diagnostic_only": covered,
                                "confidence_conflicts": {key: val["confidence_conflict"] for key, val in report["intervals"].items()}}
            entry = {**by_id[run_id], "terminal_errors": error, "false_positives": fp, "false_negatives": fn,
                     "base_terminal_errors": base_error, "issued_brier": fraction_record(f_live),
                     "base_issued_brier": fraction_record(f_base),
                     "lottery_mean_diagnostic": fraction_record(v_live),
                     "base_lottery_mean_diagnostic": fraction_record(v_base),
                     "known_wrong": known_wrong, "report_audit": report_audit,
                     "full_horizon": len(episode["trace"]) == len(tape_truth)}
            if record["configuration"]["kind"] != "broker":
                entry["lottery_mean_is_actual_action_mean"] = False
            else:
                entry["lottery_mean_is_actual_action_mean"] = True
            scored.append(entry)
            records[run_id] = record
    # Exact paired-path obligations; action and label tapes must coincide.
    paired = []
    for name in truths:
        for seed in SEEDS:
            for selector in ("uniform", "tickets"):
                prefix = f"{name}__"
                base_id = prefix+f"finite_{selector}__seed{seed}__pricefixed"
                live_id = prefix+f"value_{selector}__seed{seed}__pricefixed"
                base, live = records[base_id]["episode"], records[live_id]["episode"]
                for a, z in zip(base["trace"], live["trace"]):
                    assert all(a[k] == z[k] for k in ("base_q", "base_action", "base_terminal", "selected", "purchased_label", "propensity", "advice"))
                assert base["blocks"] == live["blocks"]
                assert base["random_bits_consumed"] == live["random_bits_consumed"]
                paired.append({"scenario": name, "seed": seed, "selector": selector,
                               "base_run": base_id, "live_run": live_id, "exact_shadow_path_equal": True})
    save(private/"scores.json", {"stage": "DEVELOPMENT", "runs": scored,
         "paired_shadow_checks": paired,
         "free_truth_oracle_diagnostic": [{"scenario": name, "terminal_errors": 0, "forecast_brier": [0,1], "charged_units": 0,
             "implementable": False, "information": "private evaluator truth supplied without computation cost"} for name in truths]})
    save(private/"seal.json", {"scored_utc": utc(), "stage": "DEVELOPMENT",
         "sources_unchanged": source_manifest() == json.loads((out/"source_before.json").read_text())["sources"],
         "files": [{"path": p, "sha256": sha(private/p)} for p in ("truth.json", "scores.json")]})
    return {"out": str(out), "runs": len(scored), "paired_checks": len(paired), "unique_programs": len(unique),
            "all_full_horizon": all(r["full_horizon"] for r in scored)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("public", "score"))
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    print(canonical(public_run(args.out) if args.command == "public" else private_score(args.out)))
