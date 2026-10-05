"""Auditable F15-ND01 DEVELOPMENT preparation and validation runner.

Save, hash, reload and validate all 15 prepared units before any validation
population.  No retention experiment or ordinary network training is called.
One unchanged retry per stage requires --retry-reason; completed units survive.
Contributor: ChatGPT (GPT-6 Astra Pro), F15-ND01.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
from pathlib import Path
import resource
import time
import traceback
from typing import Any

from .. import freeze as F
from .. import neural as N
from . import calibration_endpoint as C
from . import search_methods as S
from . import soft_mask as M


ROOT = F.ROOT
HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "freeze.json"
OUTPUT = ROOT / "v2/work_logs/F15_ND01_v1_run1"
KINDS = ("calibration", "search", "soft_mask")
UNITS = [(kind, index) for kind in KINDS for index in range(5)]


def _utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def _timers():
    children = resource.getrusage(resource.RUSAGE_CHILDREN)
    return time.perf_counter(), time.process_time(), children.ru_utime, children.ru_stime


def _cost(started):
    children = resource.getrusage(resource.RUSAGE_CHILDREN)
    child_user = children.ru_utime - started[2]
    child_system = children.ru_stime - started[3]
    own_cpu = time.process_time() - started[1]
    return {"wall_seconds": time.perf_counter() - started[0],
            "cpu_seconds": own_cpu,
            "native_child_user_cpu_seconds": child_user,
            "native_child_system_cpu_seconds": child_system,
            "native_child_cpu_seconds": child_user + child_system,
            "parent_plus_child_cpu_seconds": own_cpu + child_user + child_system}


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _mkdir(path: Path) -> None:
    path.mkdir(parents=False, exist_ok=False)
    _fsync_directory(path.parent)


def _write(path: Path, data: Any) -> str:
    """Exclusive complete JSON and sidecar; fsync both files and directory."""
    raw = F.canonical_bytes(data)
    digest = F.digest_bytes(raw)
    with path.open("xb") as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())
    with Path(str(path) + ".sha256").open("x", encoding="ascii") as handle:
        handle.write(digest + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    _fsync_directory(path.parent)
    return digest


def _read(path: Path, expected: str | None = None) -> Any:
    digest = F.file_digest(path)
    sidecar = Path(str(path) + ".sha256").read_text(encoding="ascii").strip()
    if digest != sidecar or (expected is not None and digest != expected):
        raise ValueError(f"Artifact digest mismatch: {path}")
    return F.load_json(path)


def _repo_path(name: str) -> Path:
    path = (ROOT / name).resolve()
    path.relative_to(ROOT)
    if Path(name).is_absolute() or path.relative_to(ROOT).as_posix() != name:
        raise ValueError(f"Expected a normalized repository-relative path: {name}")
    return path


def _output(path: Path) -> Path:
    path = path.resolve()
    if path != OUTPUT.resolve():
        raise ValueError("This diagnostic uses its declared output directory; do not reset attempts by changing directories.")
    return path


def verify_freeze():
    """Verify the diagnostic manifest, the original 34-file freeze, and inputs."""
    manifest = F.load_json(MANIFEST)
    if manifest.get("schema") != "f15-nd01-freeze-v1":
        raise ValueError("Unknown diagnostic freeze schema.")
    original_verification = F.verify_manifest()
    if original_verification["manifest_sha256"] != manifest["source_f14_manifest_sha256"]:
        raise ValueError("The original F14 freeze identity changed.")
    files = manifest["files"]
    names = [entry["path"] for entry in files]
    if len(names) != len(set(names)):
        raise ValueError("Repeated diagnostic manifest file.")
    for entry in [*files, *manifest["source_prepared"]]:
        path = _repo_path(entry["path"])
        if (not path.is_file() or F.file_digest(path) != entry["sha256"]
                or path.stat().st_size != entry["bytes"]):
            raise ValueError(f"Registered diagnostic dependency changed: {entry['path']}")
    config_path = _repo_path(manifest["config_path"])
    if F.file_digest(config_path) != manifest["config_sha256"]:
        raise ValueError("Diagnostic config digest mismatch.")
    required = {str(path.relative_to(ROOT)) for path in
                (HERE / "runner.py", HERE / "calibration_endpoint.py",
                 HERE / "search_methods.py", HERE / "soft_mask.py",
                 HERE / "protocol.md", config_path)}
    if not required.issubset(set(names)):
        raise ValueError("Diagnostic freeze omits its runner, methods, config or protocol.")
    config = F.load_json(config_path)
    if (config.get("schema") != "f15-nd01-config-v1"
            or config.get("protocol_id") != "F15-ND01-v1"
            or config.get("scientific_status") != "development_only"
            or _repo_path(config["output_path"]) != OUTPUT.resolve()
            or config["source_config_path"] != manifest["source_config_path"]):
        raise ValueError("Diagnostic identity, output registry or source configuration changed.")
    if config["soft_mask"].get("binary_global"):
        binary_dependencies = {str((HERE / name).relative_to(ROOT)) for name in (
            "binary_global.py", "binary_global.cpp", "binary_global_solver",
            "binary_global_build.json")}
        if not binary_dependencies.issubset(set(names)):
            raise ValueError("Enabled exhaustive binary optimization is missing a registered dependency.")
    source_config = F.validate_config(F.load_json(_repo_path(manifest["source_config_path"])))
    if _repo_path(manifest["source_config_path"]) != F.DEFAULT_CONFIG.resolve():
        raise ValueError("Source config must be the unchanged F14 configuration.")
    paths = [entry["path"] for entry in manifest["source_prepared"]]
    if len(paths) != 5 or paths != config["source_prepared"] or len(set(paths)) != 5:
        raise ValueError("The five original prepared model paths changed or are incomplete.")
    originals = []
    for index, entry in enumerate(manifest["source_prepared"]):
        original = _read(_repo_path(entry["path"]), entry["sha256"])
        F.validate_prepared(original, source_config, source_config["neural"]["model_seeds"][index])
        originals.append(original)
    bound = {"manifest_sha256": F.file_digest(MANIFEST),
             "config_sha256": manifest["config_sha256"],
             "source_f14_manifest_sha256": manifest["source_f14_manifest_sha256"],
             "source_prepared": manifest["source_prepared"]}
    return config, source_config, originals, bound


def _prepare(kind, index, config, source_config, originals):
    if kind == "calibration":
        return C.prepare_one(config["calibration"], index)
    if kind == "search":
        return S.prepare_one(originals[index], config["search"], index)
    return M.prepare_one(originals[index], source_config, index, config["soft_mask"])


def _validate(kind, index, prepared, config, source_config, originals):
    if kind == "calibration":
        C.validate_prepared(prepared, config["calibration"], index)
    elif kind == "search":
        S.validate_prepared(prepared, config["search"], index)
        if (prepared["source_original_artifact_hash"] != originals[index]["artifact_hash"]
                or prepared["network_hash"] != N.canonical_hash(originals[index]["network"])):
            raise ValueError("Search artifact changed the saved source network.")
    else:
        M.validate_prepared(prepared, originals[index], source_config, index, config["soft_mask"])


def _evaluate(kind, index, prepared, config, source_config, originals):
    if kind == "calibration":
        return C.evaluate_one(prepared, config["calibration"], index)
    if kind == "search":
        return S.evaluate_one(prepared, config["search"], index)
    return M.evaluate_one(prepared, originals[index], source_config, index, config["soft_mask"])


def _validate_evaluation(kind, index, result, prepared, config):
    if kind == "calibration":
        if (result["discovery_artifact_hash"] != prepared["artifact_hash"]
                or result["evaluation_seed"] != config["calibration"]["neural"]["evaluation_seeds"][index]
                or result["diagnostic"]["development_only"] is not True):
            raise ValueError("Compiled evaluation provenance changed.")
    else:
        if (result["prepared_artifact_hash"] != prepared["artifact_hash"]
                or result["validation_seed"] != config[kind]["validation_seeds"][index]
                or result["model_index"] != index or result["development_only"] is not True):
            raise ValueError("Diagnostic validation provenance changed.")
        unhashed = {k: v for k, v in result.items() if k != "artifact_hash"}
        if result["artifact_hash"] != N.canonical_hash(unhashed):
            raise ValueError("Diagnostic validation internal hash changed.")


def _name(kind, index, stage):
    suffix = "prepared" if stage == "preparation" else "evaluation"
    return f"{kind}_{index}_{suffix}.json"


def _prior_units(output, stage, retry):
    found, partial = {}, []
    if not retry:
        return found, partial
    folder = output / f"{stage}_attempt_1"
    for kind, index in UNITS:
        path = folder / _name(kind, index, stage)
        sidecar = Path(str(path) + ".sha256")
        if path.exists() and sidecar.exists():
            found[(kind, index)] = (path, _read(path))
        elif path.exists() or sidecar.exists():
            partial.append(path.relative_to(output).as_posix())
    return found, partial


def _pid_alive(pid):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _begin(output, stage, bound, environment, reason, extra):
    retry = reason is not None
    marker = output / f"{stage}_start.json"
    if (output / f"{stage}_complete.json").exists():
        raise ValueError("This stage is complete; repeated execution is prohibited.")
    if retry:
        if len(reason.strip()) < 10:
            raise ValueError("An unchanged retry requires a concrete unexplained-failure reason.")
        previous = _read(marker)
        if previous["freeze"] != bound or previous["bound_inputs"] != extra:
            raise ValueError("A retry cannot change the freeze or prepared inputs; an explicit amendment is required.")
        if _pid_alive(previous["pid"]):
            raise ValueError("The original stage process is still live; concurrent retry is prohibited.")
        failure = output / f"{stage}_attempt_1/failure.json"
        if failure.exists() and _read(failure).get("deterministic_defect_requires_amendment"):
            raise ValueError("The recorded deterministic defect requires an explicit amendment, not an unchanged retry.")
    elif marker.exists():
        raise ValueError("A previous attempt exists; use the single unchanged retry only for an unexplained failure.")
    number = 2 if retry else 1
    folder = output / f"{stage}_attempt_{number}"
    if folder.exists():
        raise ValueError("The allowed attempt already exists; no third attempt or overwritten stage is permitted.")
    record = {"schema": "f15-nd01-stage-attempt-v1", "stage": stage, "attempt": number,
              "started_utc": _utc(), "pid": os.getpid(), "development_only": True,
              "freeze": bound, "environment": environment, "bound_inputs": extra,
              "retry_reason": reason, "unchanged_unexplained_retry": retry,
              "maximum_stage_attempts": 2, "automatic_retry": False,
              "new_ordinary_training_steps": 0, "retention_executed": False,
              "events": [], "units": [], "generated_units": [], "reused_units": []}
    if not retry:
        _write(marker, record)
    _mkdir(folder)
    _write(folder / "start.json", record)
    return folder, record


def _event(output, folder, record, event, kind=None, index=None, **extra):
    row = {"utc": _utc(), "event": event, "kind": kind, "model_index": index,
           "development_only": True, "freeze_sha256": record["freeze"]["manifest_sha256"], **extra}
    name = f"event_{len(record['events']):03}_{event}.json"
    digest = _write(folder / name, row)
    record["events"].append({"file": (folder / name).relative_to(output).as_posix(), "sha256": digest})
    print(json.dumps(row, sort_keys=True), flush=True)


def _finish(output, folder, record, started):
    _, _, _, current_bound = verify_freeze()
    if current_bound != record["freeze"]:
        raise ValueError("The diagnostic freeze changed during execution.")
    record.update({"status": f"{record['stage']}_complete", "completed_utc": _utc(),
                   **_cost(started)})
    _write(folder / "complete.json", record)
    _write(output / f"{record['stage']}_complete.json", record)
    return record


def _failure(folder, record, started, error):
    failed = dict(record, status="failed", failed_utc=_utc(), exception_type=type(error).__name__,
                  exception=repr(error), traceback=traceback.format_exc(),
                  **_cost(started),
                  deterministic_defect_requires_amendment=isinstance(error, (
                      ValueError, TypeError, KeyError, AssertionError, NotImplementedError)),
                  exposed_data_disposition="preserve all generated, completed and partial artifacts as DEVELOPMENT")
    _write(folder / "failure.json", failed)


def _load_prepared(output, bound, config, source_config, originals):
    completion = _read(output / "preparation_complete.json")
    if completion["freeze"] != bound or completion.get("evaluation_generated") is not False:
        raise ValueError("Preparation belongs to another freeze or already exposed population.")
    if [(u["kind"], u["index"]) for u in completion["units"]] != UNITS:
        raise ValueError("All 15 prepared units must be present in the declared order.")
    loaded = {}
    for unit in completion["units"]:
        kind, index = unit["kind"], unit["index"]
        expected = {f"preparation_attempt_{attempt}/{_name(kind, index, 'preparation')}" for attempt in (1, 2)}
        if unit["file"] not in expected:
            raise ValueError("Prepared artifact path changed.")
        data = _read(output / unit["file"], unit["sha256"])
        _validate(kind, index, data, config, source_config, originals)
        if data["artifact_hash"] != unit["artifact_hash"]:
            raise ValueError("Preparation manifest internal artifact identity changed.")
        loaded[(kind, index)] = data
    return completion, loaded


def prepare(output, reason=None):
    config, source_config, originals, bound = verify_freeze()
    environment = F.verify_environment(source_config)
    output = _output(output)
    if reason is None:
        _mkdir(output)
    elif not output.is_dir():
        raise ValueError("A retry requires the existing declared output directory.")
    if (output / "evaluation_start.json").exists() or (output / "evaluation_exposure.json").exists():
        raise ValueError("Preparation cannot continue after validation exposure.")
    folder, record = _begin(output, "preparation", bound, environment, reason, {})
    started = _timers()
    try:
        prior, partial = _prior_units(output, "preparation", reason is not None)
        record["preserved_partial_units"] = partial
        record["evaluation_generated"] = False
        for kind, index in UNITS:
            _event(output, folder, record, "unit_started", kind, index)
            if (kind, index) in prior:
                path, prepared = prior[(kind, index)]
                _validate(kind, index, prepared, config, source_config, originals)
                record["reused_units"].append(path.relative_to(output).as_posix())
            else:
                prepared = _prepare(kind, index, config, source_config, originals)
                _validate(kind, index, prepared, config, source_config, originals)
                path = folder / _name(kind, index, "preparation")
                _write(path, prepared)
                record["generated_units"].append(path.relative_to(output).as_posix())
            # Validate the bytes that actually reached the durable artifact.
            prepared = _read(path)
            _validate(kind, index, prepared, config, source_config, originals)
            record["units"].append({"kind": kind, "index": index,
                "file": path.relative_to(output).as_posix(), "sha256": F.file_digest(path),
                "artifact_hash": prepared["artifact_hash"]})
            _event(output, folder, record, "unit_durable_validated", kind, index,
                   artifact_hash=prepared["artifact_hash"], file_sha256=F.file_digest(path))
        # Check the whole durable collection again, rather than relying only
        # on checks made at different points in the preparation loop.
        for unit in record["units"]:
            durable = _read(output / unit["file"], unit["sha256"])
            _validate(unit["kind"], unit["index"], durable, config, source_config, originals)
            if durable["artifact_hash"] != unit["artifact_hash"]:
                raise ValueError("The global prepared collection changed before completion.")
        _event(output, folder, record, "all_15_prepared_durable", unit_count=len(record["units"]))
        return _finish(output, folder, record, started)
    except BaseException as error:
        _failure(folder, record, started, error)
        raise


def evaluate(output, reason=None):
    config, source_config, originals, bound = verify_freeze()
    environment = F.verify_environment(source_config)
    output = _output(output)
    preparation, prepared = _load_prepared(output, bound, config, source_config, originals)
    preparation_hash = F.file_digest(output / "preparation_complete.json")
    extra = {"preparation_manifest_sha256": preparation_hash}
    folder, record = _begin(output, "evaluation", bound, environment, reason, extra)
    started = _timers()
    try:
        prior, partial = _prior_units(output, "evaluation", reason is not None)
        record["preserved_partial_units"] = partial
        # All prepared artifacts were reloaded and validated above; no method
        # evaluation function has run at this point in this process.
        _event(output, folder, record, "global_15_unit_validation_gate_passed",
               unit_count=len(prepared), preparation_manifest_sha256=preparation_hash)
        exposure = output / "evaluation_exposure.json"
        if reason is None or not exposure.exists():
            _write(exposure, {"schema": "f15-nd01-exposure-v1", "utc": _utc(),
                "development_only": True, "freeze": bound,
                "creation_attempt": record["attempt"],
                "all_15_prepared_durable_reloaded_validated": True,
                "prepared_units": preparation["units"],
                "preparation_manifest_sha256": preparation_hash,
                "first_population_generation_occurs_after_this_marker": True})
        else:
            exposed = _read(exposure)
            if exposed["freeze"] != bound or exposed["preparation_manifest_sha256"] != preparation_hash:
                raise ValueError("Retry changed the original exposure binding.")
        record["evaluation_exposure_sha256"] = F.file_digest(exposure)
        results = {kind: [] for kind in KINDS}
        for kind, index in UNITS:
            _event(output, folder, record, "unit_started", kind, index,
                   prepared_artifact_hash=prepared[(kind, index)]["artifact_hash"])
            if (kind, index) in prior:
                path, result = prior[(kind, index)]
                record["reused_units"].append(path.relative_to(output).as_posix())
            else:
                result = _evaluate(kind, index, prepared[(kind, index)], config, source_config, originals)
                _validate_evaluation(kind, index, result, prepared[(kind, index)], config)
                path = folder / _name(kind, index, "evaluation")
                _write(path, result)
                record["generated_units"].append(path.relative_to(output).as_posix())
            result = _read(path)
            _validate_evaluation(kind, index, result, prepared[(kind, index)], config)
            results[kind].append(result)
            record["units"].append({"kind": kind, "index": index,
                "file": path.relative_to(output).as_posix(), "sha256": F.file_digest(path),
                "prepared_artifact_hash": prepared[(kind, index)]["artifact_hash"]})
            _event(output, folder, record, "unit_durable_complete", kind, index,
                   file_sha256=F.file_digest(path))
        assessment = C.assess(results["calibration"], config["calibration"])
        assessment_path = folder / "calibration_assessment.json"
        assessment_hash = _write(assessment_path, assessment)
        record["calibration_assessment"] = {
            "file": assessment_path.relative_to(output).as_posix(), "sha256": assessment_hash}
        record["calibration_complete_endpoint_layouts"] = assessment["diagnostic"]["calibration_complete_endpoint_layouts"]
        record["original_F15_unchanged"] = True
        _event(output, folder, record, "all_15_evaluations_complete", unit_count=len(record["units"]))
        return _finish(output, folder, record, started)
    except BaseException as error:
        _failure(folder, record, started, error)
        raise


def verify(output):
    config, source_config, originals, bound = verify_freeze()
    environment = F.verify_environment(source_config)
    output = _output(output)
    report = {"verified": True, "development_only": True, "freeze": bound,
              "environment": environment, "output_exists": output.exists(),
              "prepared_units_verified": 0, "evaluation_units_verified": 0}
    if (output / "preparation_complete.json").exists():
        _, prepared = _load_prepared(output, bound, config, source_config, originals)
        report["prepared_units_verified"] = len(prepared)
        if (output / "evaluation_complete.json").exists():
            completion = _read(output / "evaluation_complete.json")
            if completion["freeze"] != bound or [(u["kind"], u["index"]) for u in completion["units"]] != UNITS:
                raise ValueError("Evaluation completion belongs to another freeze or omits units.")
            exposure = _read(output / "evaluation_exposure.json", completion["evaluation_exposure_sha256"])
            if (exposure["freeze"] != bound
                    or exposure["preparation_manifest_sha256"] != F.file_digest(output / "preparation_complete.json")
                    or exposure["all_15_prepared_durable_reloaded_validated"] is not True):
                raise ValueError("The evaluation exposure marker lost its preparation binding.")
            for unit in completion["units"]:
                kind, index = unit["kind"], unit["index"]
                allowed = {f"evaluation_attempt_{attempt}/{_name(kind, index, 'evaluation')}" for attempt in (1, 2)}
                if unit["file"] not in allowed:
                    raise ValueError("Evaluation artifact path changed.")
                result = _read(output / unit["file"], unit["sha256"])
                _validate_evaluation(kind, index, result, prepared[(kind, index)], config)
                if unit["prepared_artifact_hash"] != prepared[(kind, index)]["artifact_hash"]:
                    raise ValueError("Evaluation completion names a different prepared artifact.")
                report["evaluation_units_verified"] += 1
            assessment = completion["calibration_assessment"]
            _read(output / assessment["file"], assessment["sha256"])
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "evaluate", "verify"))
    parser.add_argument("--out", type=Path, default=OUTPUT)
    parser.add_argument("--retry-reason", help="Concrete unexplained failure reason for the only unchanged retry.")
    args = parser.parse_args(argv)
    if args.action == "verify" and args.retry_reason is not None:
        parser.error("Verification is read-only and is not a retry.")
    result = verify(args.out) if args.action == "verify" else (
        prepare(args.out, args.retry_reason) if args.action == "prepare"
        else evaluate(args.out, args.retry_reason))
    # Unit progress was streamed already. Keep the terminal summary compact.
    if args.action != "verify":
        result = {"status": result["status"], "attempt": result["attempt"],
                  "development_only": True, "unit_count": len(result["units"]),
                  "wall_seconds": result["wall_seconds"], "cpu_seconds": result["cpu_seconds"],
                  "native_child_cpu_seconds": result["native_child_cpu_seconds"],
                  "parent_plus_child_cpu_seconds": result["parent_plus_child_cpu_seconds"],
                  "output": str(args.out.resolve())}
    print(json.dumps(result, sort_keys=True, indent=2), flush=True)


if __name__ == "__main__":
    main()
