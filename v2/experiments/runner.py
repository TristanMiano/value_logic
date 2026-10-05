"""F14 development and the frozen, explicitly separate F15 execution path.

F14 uses ``develop``. F15 first runs ``prepare --task F15``, which serializes
all five trained models/alignments, then ``evaluate --task F15``. Evaluation
never chooses an alignment, a seed, a threshold or an extra training step.
Contributor: ChatGPT (GPT-6 Astra Pro), F14.
"""
from __future__ import annotations

import argparse
import copy
import datetime
import json
import os
from pathlib import Path
import time
import traceback

from . import analysis as A
from . import calibration as C
from . import freeze as F
from . import neural as N
from . import retention as R


def _utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def _write_artifact(path, data):
    F.write_json(path, data, exclusive=True)
    digest = F.file_digest(path)
    with Path(str(path)+".sha256").open("x", encoding="ascii") as handle:
        handle.write(digest+"\n")
        handle.flush()
        os.fsync(handle.fileno())
    return digest


def _read_artifact(path, expected_hash=None):
    digest = F.file_digest(path)
    sidecar = Path(str(path)+".sha256").read_text(encoding="ascii").strip()
    if digest != sidecar or (expected_hash is not None and digest != expected_hash):
        raise ValueError(f"Artifact hash mismatch: {path}")
    return F.load_json(path)


def _new_directory(output):
    output = Path(output).resolve()
    if output.exists() and any(output.iterdir()):
        raise ValueError("Output directory is nonempty; preserve it and use a new directory.")
    output.mkdir(parents=True, exist_ok=True)
    return output


def develop(config, output):
    """Executable smoke at declared development seeds only."""
    output = _new_directory(output)
    started = time.perf_counter()
    record = {"schema": "f14-development-run-v1", "started_utc": _utc(),
              "evidence_type": "development_only", "environment": F.environment(),
              "held_out_evaluation_executed": False,
              "configuration_canonical_sha256": F.digest_bytes(F.canonical_bytes(config)),
              "source_sha256_at_start": {str(p.relative_to(F.ROOT)).replace(os.sep, "/"): F.file_digest(p)
                                         for p in F.manifest_paths(F.DEFAULT_CONFIG)}}
    _write_artifact(output/"development_start.json", record)
    _write_artifact(output/"configuration.json", config)
    try:
        retention = R.run_development(config["retention"])
        _write_artifact(output/"retention.json", retention)
        _write_artifact(output/"retention_sentinels.json", R.development_sentinels())
        ra = A.retention_assessment(retention["cases"], config, development=True)
        _write_artifact(output/"retention_assessment.json", ra)
        # Explicit two-stage preparation also in development: serialize first.
        nc = copy.deepcopy(config["neural"])
        nc.update(nc["smoke"])
        prepared = N.prepare_neural(nc, nc["development_seed"])
        _write_artifact(output/"neural_prepared.json", prepared)
        prepared = _read_artifact(output/"neural_prepared.json")
        result = N.evaluate_neural(prepared, nc, nc["development_evaluation_seed"])
        _write_artifact(output/"neural.json", result)
        assessment_config = dict(config, neural=nc)
        assessment = A.neural_assessment([result], assessment_config, development=True)
        _write_artifact(output/"neural_assessment.json", assessment)
        calibration = C.development_calibration(config)
        _write_artifact(output/"constructed_calibration.json", calibration)
        record.update({"completed_utc": _utc(), "status": "development_complete",
            "wall_seconds": time.perf_counter()-started,
            "constructed_calibration_passed": calibration["passed"],
            "neural_interval_rows": assessment["actual_interval_rows"]})
        _write_artifact(output/"development_complete.json", record)
        return record
    except Exception as exc:
        record.update({"failed_utc": _utc(), "status": "development_failed",
                       "exception": repr(exc), "traceback": traceback.format_exc()})
        _write_artifact(output/"development_failure.json", record)
        raise


def _prior_units(output, stage, names, retry):
    """Reuse complete hash-checked units; preserve every incomplete file."""
    if not retry:
        return {}, []
    found, partial = {}, []
    folder = output/f"{stage}_attempt_1"
    for name in names:
        path = folder/name
        sidecar = Path(str(path)+".sha256")
        if path.exists() and sidecar.exists():
            found[name] = (path, _read_artifact(path))
        elif path.exists() or sidecar.exists():
            partial.append(str(path.relative_to(output)))
    return found, partial


def _begin_attempt(output, stage, freeze, environment, retry, reason, partial, extra=None):
    if (output/f"{stage}_complete.json").exists():
        raise ValueError("This stage already completed; repeated evaluation is prohibited.")
    number = 2 if retry else 1
    root_start = output/f"{stage}_start.json"
    if retry:
        if not reason or len(reason.strip()) < 10:
            raise ValueError("An unchanged retry requires a concrete unexplained-failure note.")
        previous = _read_artifact(root_start)
        if previous["freeze"] != freeze:
            raise ValueError("A retry cannot change the freeze, configuration or implementation.")
        if any(previous.get(key) != value for key, value in (extra or {}).items()):
            raise ValueError("A retry cannot change the artifacts bound before exposure.")
    elif root_start.exists():
        raise ValueError("A prior attempt exists; classify it before using the single permitted retry.")
    folder = output/f"{stage}_attempt_{number}"
    folder.mkdir(parents=False, exist_ok=False)
    record = {"schema": f"f15-{stage}-attempt-v1", "freeze": freeze,
              "started_utc": _utc(), "environment": environment, "attempt": number,
              "unchanged_unexplained_retry": retry, "failure_note": reason if retry else None,
              "preserved_incomplete_artifacts": partial,
              "reused_units": [], "generated_units": []}
    record.update(extra or {})
    _write_artifact(folder/"start.json", record)
    if not retry:
        _write_artifact(root_start, record)
    return folder, record


def _finish_attempt(output, folder, stage, record, started_wall, started_cpu, status):
    record.update({"completed_utc": _utc(), "status": status,
                   "observed_wall_seconds": time.perf_counter()-started_wall,
                   "observed_cpu_seconds": time.process_time()-started_cpu})
    _write_artifact(folder/"complete.json", record)
    _write_artifact(output/f"{stage}_complete.json", record)
    return record


def _fail_attempt(folder, record, started_wall, started_cpu, exc):
    record.update({"failed_utc": _utc(), "status": "failed",
                   "exception_type": type(exc).__name__, "exception": repr(exc),
                   "traceback": traceback.format_exc(),
                   "observed_wall_seconds": time.perf_counter()-started_wall,
                   "observed_cpu_seconds": time.process_time()-started_cpu,
                   "automatic_retry": False})
    _write_artifact(folder/"failure.json", record)


def prepare(config, output, manifest_path, *, retry=False, failure_note=None):
    """F15 discovery only; an unchanged retry reuses completed model files."""
    freeze = F.bound_configuration(config, manifest_path)
    environment = F.verify_environment(config)
    output = Path(output).resolve() if retry else _new_directory(output)
    if (output/"evaluation_start.json").exists():
        raise ValueError("Discovery may not be rerun after evaluation exposure.")
    seeds = config["neural"]["model_seeds"]
    names = [f"model_{i}_prepared.json" for i in range(len(seeds))]
    prior, partial = _prior_units(output, "preparation", names, retry)
    for i, seed in enumerate(seeds):
        if names[i] in prior:
            F.validate_prepared(prior[names[i]][1], config, seed)
    folder, record = _begin_attempt(output, "preparation", freeze, environment, retry, failure_note, partial)
    record.update({"evaluation_started": False, "models": []})
    started_wall, started_cpu = time.perf_counter(), time.process_time()
    try:
        for i, seed in enumerate(seeds):
            name = names[i]
            if name in prior:
                path, prepared = prior[name]
                record["reused_units"].append(str(path.relative_to(output)))
            else:
                prepared = N.prepare_neural(config, seed)
                F.validate_prepared(prepared, config, seed)
                path = folder/name
                _write_artifact(path, prepared)
                record["generated_units"].append(str(path.relative_to(output)))
            record["models"].append({"index": i, "discovery_seed": seed,
                "file": str(path.relative_to(output)).replace(os.sep, "/"),
                "sha256": F.file_digest(path), "alignment_artifact_hash": prepared["artifact_hash"]})
        complete = _finish_attempt(output, folder, "preparation", record, started_wall, started_cpu, "all_models_prepared")
        return {"status": complete["status"], "models": len(complete["models"]),
                "evaluation_started": False, "attempt": complete["attempt"], "output": str(output)}
    except BaseException as exc:
        _fail_attempt(folder, record, started_wall, started_cpu, exc)
        raise


def _load_preparation(output, freeze, config):
    preparation = _read_artifact(output/"preparation_complete.json")
    if preparation["freeze"] != freeze or preparation["evaluation_started"] is not False:
        raise ValueError("Prepared models do not belong to this untouched freeze.")
    if len(preparation["models"]) != len(config["neural"]["model_seeds"]):
        raise ValueError("All five alignments must be durable before evaluation starts.")
    prepared_models = []
    for i, info in enumerate(preparation["models"]):
        seed = config["neural"]["model_seeds"][i]
        if info["index"] != i or info["discovery_seed"] != seed:
            raise ValueError("Prepared model seed/index changed.")
        expected_paths = {f"preparation_attempt_{a}/model_{i}_prepared.json" for a in (1, 2)}
        if info["file"] not in expected_paths:
            raise ValueError("Unexpected discovery artifact path.")
        prepared = _read_artifact(output/info["file"], info["sha256"])
        F.validate_prepared(prepared, config, seed)
        if prepared["artifact_hash"] != info["alignment_artifact_hash"]:
            raise ValueError("Discovery manifest's alignment digest changed.")
        prepared_models.append(prepared)
    return preparation, prepared_models


def evaluate(config, output, manifest_path, *, retry=False, failure_note=None):
    """F15 evaluation; every model is preflighted before any case generation."""
    output = Path(output).resolve()
    freeze = F.bound_configuration(config, manifest_path)
    environment = F.verify_environment(config)
    preparation, prepared_models = _load_preparation(output, freeze, config)
    rc = config["retention"]
    cases = [(seed, variant) for seed in rc["evaluation_seeds"] for variant in rc["variants"]]
    retention_names = [f"retention_{s}_{v}.json" for s, v in cases]
    neural_names = [f"model_{i}_evaluation.json" for i in range(len(prepared_models))]
    prior, partial = _prior_units(output, "evaluation", retention_names+neural_names, retry)
    for name, (seed, variant) in zip(retention_names, cases):
        if name in prior and (prior[name][1]["seed"], prior[name][1]["variant"]) != (seed, variant):
            raise ValueError("A retained evaluation result belongs to a different case.")
    for i, name in enumerate(neural_names):
        if name in prior:
            r = prior[name][1]
            if (r["discovery_artifact_hash"] != prepared_models[i]["artifact_hash"]
                    or r["evaluation_seed"] != config["neural"]["evaluation_seeds"][i]):
                raise ValueError("A retained neural evaluation belongs to a different discovery.")
    folder, record = _begin_attempt(output, "evaluation", freeze, environment, retry, failure_note, partial,
        {"preparation_manifest_sha256": F.file_digest(output/"preparation_complete.json")})
    started_wall, started_cpu = time.perf_counter(), time.process_time()
    try:
        retention_results = []
        for name, (seed, variant) in zip(retention_names, cases):
            if name in prior:
                path, result = prior[name]
                record["reused_units"].append(str(path.relative_to(output)))
            else:
                result = R.run_generated_case(seed, variant, rc)
                path = folder/name
                _write_artifact(path, result)
                record["generated_units"].append(str(path.relative_to(output)))
            retention_results.append(result)
        _write_artifact(folder/"retention_results.json", retention_results)
        retention_assessment = A.retention_assessment(retention_results, config)
        _write_artifact(folder/"retention_assessment.json", retention_assessment)
        results = []
        for i, (prepared, seed) in enumerate(zip(prepared_models, config["neural"]["evaluation_seeds"])):
            name = neural_names[i]
            if name in prior:
                path, result = prior[name]
                record["reused_units"].append(str(path.relative_to(output)))
            else:
                result = N.evaluate_neural(prepared, config, seed)
                path = folder/name
                _write_artifact(path, result)
                record["generated_units"].append(str(path.relative_to(output)))
            results.append(result)
        assessment = A.neural_assessment(results, config)
        _write_artifact(folder/"neural_assessment.json", assessment)
        record.update({"retention_cases": len(retention_results), "neural_models": len(results),
            "retention_bounded_application_criterion_met": retention_assessment["bounded_application_criterion_met"],
            "neural_pilot_support_criterion_met": assessment["pilot_support_criterion_met"],
            "retention_assessment_file": str((folder/"retention_assessment.json").relative_to(output)),
            "neural_assessment_file": str((folder/"neural_assessment.json").relative_to(output))})
        return _finish_attempt(output, folder, "evaluation", record, started_wall, started_cpu, "evaluation_complete")
    except BaseException as exc:
        _fail_attempt(folder, record, started_wall, started_cpu, exc)
        raise

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("develop", "prepare", "evaluate"))
    parser.add_argument("--task", choices=("F14", "F15"), default="F14")
    parser.add_argument("--config", type=Path, default=F.DEFAULT_CONFIG)
    parser.add_argument("--manifest", type=Path, default=F.DEFAULT_MANIFEST)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--retry-unexplained", action="store_true")
    parser.add_argument("--failure-note")
    args = parser.parse_args(argv)
    if args.action != "develop" and args.task != "F15":
        parser.error("Preparation/evaluation belongs to F15; use --task F15 only in that task.")
    if args.action == "develop" and args.retry_unexplained:
        parser.error("Development preserves attempts in separate output directories.")
    config = F.validate_config(F.load_json(args.config))
    result = develop(config, args.out) if args.action == "develop" else (
        prepare(config, args.out, args.manifest, retry=args.retry_unexplained, failure_note=args.failure_note) if args.action == "prepare" else
        evaluate(config, args.out, args.manifest, retry=args.retry_unexplained, failure_note=args.failure_note))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
