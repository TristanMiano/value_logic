"""P3-09 preparation and P3-10-only staged execution entry point.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-11.
Preparation never calls any final generator, runner, or private scorer.
"""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True
import argparse
from contextlib import redirect_stdout
from datetime import datetime, timezone
import hashlib
import importlib
import io
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sysconfig

import p309_lifecycle as L

REPO = Path(__file__).resolve().parents[2]
PROTOCOL = Path("v3/experiments/protocol.v1.json")
PROSE = Path("v3/experiments/protocol.md")
FROZEN = Path("v3/experiments/frozen_v1")
FINAL = Path("v3/experiments/final_v1")
PREPARATION = Path("v3/experiments/preparation_v1")
ADAPTERS = {"broker": "p309_broker", "certificates": "p309_certificates",
            "conformance": "p309_conformance"}
CORE_SOURCES = ["v3/experiments/p309_lifecycle.py", "v3/experiments/p309_freeze.py",
                "v3/experiments/p309_analyze.py"]
CONTRACT_SOURCES = ["v3/RESEARCH_PROTOCOL.md", "v3/foundations/01_problem_contract.md",
                    "v3/foundations/01_observation_contract.md", "v3/foundations/01_desiderata.md"]
STAGES = ("inputs", "public", "evaluation", "analysis")


def adapters():
    loaded = {name: importlib.import_module(module) for name, module in ADAPTERS.items()}
    for name, module in loaded.items():
        expected = (REPO / "v3/experiments" / (ADAPTERS[name] + ".py")).resolve()
        if Path(module.__file__).resolve() != expected:
            raise L.IntegrityError("Adapter resolved outside its frozen source path: " + name)
    if Path(L.__file__).resolve() != (REPO / "v3/experiments/p309_lifecycle.py").resolve():
        raise L.IntegrityError("Lifecycle module resolved outside its frozen source path.")
    return loaded


def validate_loaded_local_sources(paths):
    declared = {str((REPO / path).resolve()) for path in paths}
    actual = []
    for name, module in list(sys.modules.items()):
        filename = getattr(module, "__file__", None)
        if not filename:
            continue
        path = Path(filename).resolve()
        if path.is_relative_to(REPO) and path.suffix == ".py":
            if str(path) not in declared:
                raise L.IntegrityError("Loaded local module absent from source closure: " + str(path))
            actual.append({"module": name, "path": path.relative_to(REPO).as_posix()})
    return sorted(actual, key=lambda row: (row["path"], row["module"]))


def relative_source(path):
    path = Path(path)
    if path.is_absolute() or ".." in path.parts or path.as_posix() != str(path):
        raise L.IntegrityError("Source closure requires canonical repository-relative paths.")
    if not (REPO / path).is_file() or (REPO / path).is_symlink():
        raise L.IntegrityError("Missing or symbolic frozen source: " + str(path))
    return path.as_posix()


def source_record(paths):
    return [{"path": path, "bytes": (REPO / path).stat().st_size,
             "sha256": L.sha256_file(REPO / path)}
            for path in sorted({relative_source(p) for p in paths})]


def default_protocol():
    loaded = adapters()
    return {
        "schema": "value_logic.p309.protocol.v1", "freeze_id": "P3-09-v1",
        "contributor": "ChatGPT (GPT-6 Astra Pro)",
        "entry_commit": "f2a240b87d4df07ac91874b092db20b8c4378889",
        "stage_at_freeze": "PREPARATION", "final_population_generated": False,
        "paths": {"frozen": FROZEN.as_posix(), "final": FINAL.as_posix()},
        "runtime_requirements": {"implementation": "cpython", "version": [3, 12, 14],
                                 "platform": "Linux", "byteorder": "little"},
        "arms": {name: module.default_config() for name, module in loaded.items()},
        "analysis": {
            "primary_scope": "exact descriptive fixed finite cohort",
            "loss_improvement_threshold": [1, 100], "saving_ratio_threshold": [19, 20],
            "repricing_grid": [[0, 1], [1, 100000], [1, 10000], [1, 1000], [1, 100]],
            "ties": "retain all exact equalities; no arbitrary winner",
            "missing": "retain scheduled denominator and all measured costs; withhold full-denominator positive ranking",
            "ordinary_catalogue": "mean whole fixed configurations before taking a descriptive minimum",
            "deterministic_controls": "one execution per population; repeated seed slots are algebraic weights only",
            "certificate_dominance": "nonempty exact covered-request superset and total all-attempt cost ratio at most19/20",
            "coverage_inference": False, "p_values": False,
            "cross_tariff_aggregation": False},
        "lifecycle": {
            "stages": list(STAGES), "max_attempts_per_stage": 2,
            "retry_classification": "unexplained_infrastructure",
            "retry": "unchanged binding and fixed paths; verify and preserve completed units",
            "deterministic_defect": "versioned amendment; preserve freeze, exposure and every attempted output",
            "post_exposure_amendment": "affected exposed data loses original confirmatory status; no hidden replacement cohort",
            "completion_authority": "immutable unit seals binding exact result bytes and source/config/input hashes",
            "unit_boundaries": "one public recipe; one complete stateful method episode/history; one private score per method unit; one aggregate analysis"}}


def validate_protocol(config, loaded=None):
    loaded = loaded or adapters()
    if config != default_protocol():
        raise L.IntegrityError("Protocol differs from the prospective code-defined configuration.")
    requirement = config["runtime_requirements"]
    if (sys.implementation.name != requirement["implementation"]
            or list(sys.version_info[:3]) != requirement["version"]
            or platform.system() != requirement["platform"] or sys.byteorder != requirement["byteorder"]):
        raise L.IntegrityError("Interpreter is outside the frozen execution contract.")
    groups, units = [], []
    for arm, module in loaded.items():
        arm_config = config["arms"][arm]
        if hasattr(module, "validate_config"):
            module.validate_config(arm_config)
        arm_groups = module.groups(arm_config)
        L.checked_schedule(arm_groups)
        for group in arm_groups:
            if group.get("arm") != arm:
                raise L.IntegrityError("Group belongs to the wrong arm.")
            arm_units = module.units(group, arm_config)
            L.checked_schedule(arm_units)
            for unit in arm_units:
                if unit.get("group_id") != group["id"] or unit.get("arm") != arm:
                    raise L.IntegrityError("Method unit is not bound to its public group.")
            groups.append(group)
            units.extend(arm_units)
    L.checked_schedule(groups)
    L.checked_schedule(units)
    return groups, units


def runtime_record():
    """Byte-bind the interpreter, complete supplied stdlib, and native closure.

    Paths and host identifiers are descriptive. Compatibility is based on
    content, version, ABI and machine; boot ID and current time are not required
    to match in a later P3-10 process.
    """
    stdlib = Path(sysconfig.get_path("stdlib")).resolve()
    files = []
    binaries = {Path(sys.executable).resolve()}
    for directory, subdirs, names in os.walk(stdlib):
        subdirs[:] = sorted(name for name in subdirs if name not in ("site-packages", "__pycache__"))
        for name in sorted(names):
            path = Path(directory) / name
            rel = path.relative_to(stdlib)
            if path.is_file() and (path.suffix == ".py" or ".so" in path.name):
                files.append({"path": rel.as_posix(), "bytes": path.stat().st_size,
                              "sha256": L.sha256_file(path)})
                if ".so" in path.name:
                    binaries.add(path.resolve())
    files.sort(key=lambda row: row["path"])
    native = set(binaries)
    unavailable_optional = []
    for binary in sorted(binaries):
        result = subprocess.run(["ldd", str(binary)], capture_output=True, text=True, check=False)
        if result.returncode not in (0, 1):
            raise L.IntegrityError("Could not inspect native dependency closure.")
        for line in result.stdout.splitlines():
            # ldd lists the transitive loader closure. Never execute its output.
            parts = line.strip().split()
            for token in parts:
                if token.startswith("/") and Path(token).is_file():
                    native.add(Path(token).resolve())
            if "not found" in line:
                # The supplied runtime ships an unused Tk extension without
                # Tcl9. No frozen worker imports tkinter. Record the absence
                # exactly instead of asserting that this optional GUI exists.
                if not binary.name.startswith("_tkinter."):
                    raise L.IntegrityError("Missing required native interpreter dependency: " + binary.name)
                unavailable_optional.append({"module": binary.name, "dependency": parts[0],
                                             "scope": "unused optional GUI extension; excluded from the CLI service"})
    native_files = [{"name": path.name, "bytes": path.stat().st_size,
                     "sha256": L.sha256_file(path)} for path in sorted(native)]
    native_files.sort(key=lambda row: (row["name"], row["sha256"]))
    return {"schema": "value_logic.p309.runtime.v1", "implementation": sys.implementation.name,
            "version": list(sys.version_info[:3]), "full_version": sys.version,
            "cache_tag": sys.implementation.cache_tag, "soabi": sysconfig.get_config_var("SOABI"),
            "system": platform.system(), "machine": platform.machine(), "byteorder": sys.byteorder,
            "int_bits_per_digit": sys.int_info.bits_per_digit,
            "python_binary_sha256": L.sha256_file(Path(sys.executable).resolve()),
            "stdlib_files": files, "native_files": native_files,
            "unavailable_optional_native_dependencies": unavailable_optional}


def development_checks():
    loaded = adapters()
    config = L.read_json(REPO / PROTOCOL)
    groups, units = validate_protocol(config, loaded)
    checks = {"lifecycle": L.selfcheck()}
    for arm, module in loaded.items():
        captured = io.StringIO()
        with redirect_stdout(captured):
            value = module.selfcheck()
        checks[arm] = {"result": value, "captured_stdout": captured.getvalue(),
                       "configuration_sha256": L.digest(config["arms"][arm]),
                       "prospective_units_validated": sum(u["arm"] == arm for u in units)}
    import p309_analyze
    if Path(p309_analyze.__file__).resolve() != (REPO / "v3/experiments/p309_analyze.py").resolve():
        raise L.IntegrityError("Analyzer resolved outside its frozen source path.")
    checks["analysis"] = p309_analyze.selfcheck()
    for name, check in checks.items():
        value = check["result"] if name in ADAPTERS else check
        if not isinstance(value, dict) or value.get("status") != "PASS":
            raise L.IntegrityError("Development suite did not explicitly pass: " + name)
    paths = CORE_SOURCES + CONTRACT_SOURCES + [PROTOCOL.as_posix(), PROSE.as_posix()]
    for module in loaded.values():
        paths.extend(module.source_paths())
    origins = validate_loaded_local_sources(paths)
    # Only opaque schedule metadata has been enumerated above. No call to an
    # adapter's generate/run/score endpoint is made by the preparation driver.
    return {"schema": "value_logic.p309.preparation_checks.v1", "stage": "DEVELOPMENT",
            "final_population_generated": False, "schedule_groups": len(groups),
            "schedule_method_units": len(units), "checks": checks,
            "loaded_local_source_origins": origins, "status": "PASS"}


def initialize_config():
    if (REPO / FROZEN).exists() or (REPO / FINAL).exists():
        raise L.IntegrityError("An existing freeze or final root forbids implicit reconfiguration.")
    L.publish_json(REPO / PROTOCOL, default_protocol())
    return {"written": PROTOCOL.as_posix(), "stage": "PREPARATION"}


def prepare():
    with L.exclusive_lock(REPO / "v3/experiments/p309-preparation.lock"):
        if (REPO / FROZEN).exists() or (REPO / FINAL).exists():
            raise L.IntegrityError("Existing freeze/final root: inspect it, do not overwrite preparation.")
        config = L.read_json(REPO / PROTOCOL)
        loaded = adapters()
        groups, units = validate_protocol(config, loaded)
        paths = CORE_SOURCES + CONTRACT_SOURCES + [PROTOCOL.as_posix(), PROSE.as_posix()]
        for module in loaded.values():
            paths.extend(module.source_paths())
        sources = source_record(paths)
        runtime = runtime_record()
        preparation_root = REPO / PREPARATION
        preparation_root.mkdir(parents=True, exist_ok=True)
        attempts = sorted(preparation_root.glob("attempt_*"))
        work = preparation_root / ("attempt_%02d" % (len(attempts) + 1))
        work.mkdir(exist_ok=False)
        L.publish_json(work / "started.json", {"stage": "PREPARATION", "created_utc": L.utc_now(),
                       "final_population_generated": False, "protocol_sha256": L.sha256_file(REPO / PROTOCOL),
                       "source_manifest_sha256": L.digest(sources)})
        try:
            snapshot = work / "source"
            for row in sources:
                L.publish_bytes(snapshot / row["path"], (REPO / row["path"]).read_bytes())
            L.publish_json(work / "runtime.json", runtime)
            L.publish_json(work / "schedule.json", {"groups": groups, "units": units})
            # Exercise the copied source, including every selected method's
            # development preparation checks, in a fresh isolated interpreter.
            command = [sys.executable, "-B", str(snapshot / "v3/experiments/p309_freeze.py"),
                       "development-checks"]
            process = subprocess.run(command, cwd=snapshot, text=True, capture_output=True)
            L.publish_bytes(work / "checks.stdout.txt", process.stdout.encode())
            L.publish_bytes(work / "checks.stderr.txt", process.stderr.encode())
            if process.returncode != 0:
                raise L.IntegrityError("Prepared source development checks failed; see retained stdout/stderr.")
            checks = json.loads(process.stdout)
            if checks.get("status") != "PASS" or checks.get("final_population_generated") is not False:
                raise L.IntegrityError("Development preparation lacks a no-final-generation declaration.")
            L.publish_json(work / "checks.json", checks)
            # A source edit racing the snapshot invalidates preparation.
            if source_record(paths) != sources or runtime_record() != runtime:
                raise L.IntegrityError("Source or runtime changed during preparation.")
            prepared_methods = []
            identities = set()
            for unit in units:
                representation = {k: v for k, v in unit.items()
                                  if k not in ("id", "group_id", "seed", "pairing", "segments")}
                key = L.digest(representation)
                if key not in identities:
                    identities.add(key)
                    prepared_methods.append({"sha256": key, "representation": representation,
                        "validation": {"source_and_configuration": "saved and hash-bound",
                                       "schedule": "validated against the exact code-defined arm configuration",
                                       "new_execution_evidence": "checks.json, arm-specific development operations only",
                                       "inherited_evidence": "source-bound published finite worker evidence; see protocol and arm receipt",
                                       "final_cases_executed_for_validation": False}})
            L.publish_json(work / "methods.json", {"stage": "PREPARATION", "methods": prepared_methods})
            manifest = {"schema": "value_logic.p309.freeze.v1", "freeze_id": config["freeze_id"],
                        "created_utc": L.utc_now(), "contributor": config["contributor"],
                        "entry_commit": config["entry_commit"], "final_population_generated": False,
                        "protocol_sha256": L.sha256_file(REPO / PROTOCOL),
                        "runtime_sha256": L.sha256_file(work / "runtime.json"),
                        "schedule_sha256": L.sha256_file(work / "schedule.json"),
                        "preparation_checks_sha256": L.sha256_file(work / "checks.json"),
                        "prepared_methods_sha256": L.sha256_file(work / "methods.json"),
                        "sources": sources, "preparation_attempt": work.name,
                        "final_root": FINAL.as_posix(), "expected_groups": len(groups),
                        "expected_public_units": len(units),
                        "runtime_closure": "complete supplied standard-library bytes and required CLI native closure; unavailable unused Tk dependencies explicitly inventoried"}
            L.publish_json(work / "manifest.json", manifest)
            L.publish_json(work / "receipt.json", {
                "schema": "value_logic.p309.preparation_receipt.v1", "status": "PREPARED",
                "manifest_sha256": L.sha256_file(work / "manifest.json"),
                "final_population_generated": False, "created_utc": L.utc_now()})
            # The prepared directory itself becomes the freeze; no source or
            # receipt is regenerated between successful checks and publication.
            os.rename(work, REPO / FROZEN)
            L.fsync_directory((REPO / FROZEN).parent)
            return verify()
        except BaseException as error:
            if work.exists() and not (work / "failure.json").exists():
                L.publish_json(work / "failure.json", {"stage": "PREPARATION", "error_type": type(error).__name__,
                               "error": str(error), "created_utc": L.utc_now(), "final_population_generated": False})
            raise


def verify():
    frozen = REPO / FROZEN
    manifest = L.read_json(frozen / "manifest.json")
    receipt = L.read_json(frozen / "receipt.json")
    if receipt.get("status") != "PREPARED" or receipt.get("manifest_sha256") != L.sha256_file(frozen / "manifest.json"):
        raise L.IntegrityError("Preparation receipt does not bind this freeze.")
    if manifest.get("final_population_generated") is not False or receipt.get("final_population_generated") is not False:
        raise L.IntegrityError("Preparation receipt was not prospective.")
    check_files = {"runtime.json": "runtime_sha256", "schedule.json": "schedule_sha256",
                   "checks.json": "preparation_checks_sha256", "methods.json": "prepared_methods_sha256"}
    for name, key in check_files.items():
        if L.sha256_file(frozen / name) != manifest[key]:
            raise L.IntegrityError("Altered frozen preparation artifact: " + name)
    for row in manifest["sources"]:
        for path in (REPO / row["path"], frozen / "source" / row["path"]):
            if not path.is_file() or path.stat().st_size != row["bytes"] or L.sha256_file(path) != row["sha256"]:
                raise L.IntegrityError("Altered frozen source: " + str(path))
    config = L.read_json(REPO / PROTOCOL)
    if L.sha256_file(REPO / PROTOCOL) != manifest["protocol_sha256"]:
        raise L.IntegrityError("Protocol does not match freeze.")
    groups, units = validate_protocol(config)
    if L.read_json(frozen / "schedule.json") != {"groups": groups, "units": units}:
        raise L.IntegrityError("Code-generated schedule differs from prepared schedule.")
    if runtime_record() != L.read_json(frozen / "runtime.json"):
        raise L.IntegrityError("Interpreter/dependency closure differs from the prepared environment.")
    return {"status": "VERIFIED", "freeze_id": manifest["freeze_id"],
            "manifest_sha256": L.sha256_file(frozen / "manifest.json"),
            "protocol_sha256": manifest["protocol_sha256"],
            "expected_groups": len(groups), "expected_public_units": len(units),
            "final_exposure_present": (REPO / FINAL / "exposure.json").exists()}


def require_p310(task):
    if task != "P3-10":
        raise L.IntegrityError("Final execution is reserved for the separately selected P3-10 task.")
    plan = L.read_json(REPO / "v3/plan.v1.json")
    # next_task is the repository's established active pointer. The explicit
    # command task prevents an accidental prepare/run shorthand from exposing.
    if plan.get("next_task") != "P3-10":
        raise L.IntegrityError("Repository pointer does not select P3-10.")


def final_stage(name, task, retry_reason=None, failure_classification=None):
    require_p310(task)
    verification = verify()
    config = L.read_json(REPO / PROTOCOL)
    loaded = adapters()
    schedule = L.read_json(REPO / FROZEN / "schedule.json")
    groups, units = schedule["groups"], schedule["units"]
    group_map = {group["id"]: group for group in groups}
    binding = {"freeze_id": verification["freeze_id"],
               "manifest_sha256": verification["manifest_sha256"],
               "protocol_sha256": verification["protocol_sha256"]}
    root = REPO / FINAL
    # The marker is durably published under the same writer lock before any
    # generator can be called. An existing marker must have the same binding.
    with L.exclusive_lock(root / "writer.lock"):
        path = root / "exposure.json"
        if path.exists():
            if L.read_json(path).get("binding") != binding:
                raise L.IntegrityError("Final root belongs to another freeze.")
        else:
            if name != "inputs":
                raise L.IntegrityError("Input exposure must be the first final stage.")
            L.publish_json(path, {"schema": "value_logic.p309.exposure.v1", "stage": "P3-10",
                           "binding": binding, "created_utc": L.utc_now(),
                           "statement": "Final input generation is exposure; all methods were prepared beforehand.",
                           "command": {"stage": name, "task": task}})
    input_stage = L.Stage(root, "inputs", binding, groups)
    public_stage = L.Stage(root, "public", binding, units)
    score_units = [dict(unit, id="score-" + unit["id"], public_unit_id=unit["id"]) for unit in units]
    evaluation_stage = L.Stage(root, "evaluation", binding, score_units)
    analysis_stage = L.Stage(root, "analysis", binding, [{"id": "all-frozen-endpoints", "arm": "analysis"}])
    options = {"retry_reason": retry_reason, "failure_classification": failure_classification}
    if name == "inputs":
        return input_stage.execute(lambda group: loaded[group["arm"]].generate(
            group, config["arms"][group["arm"]], exposure_token="P3-10-EXPOSED"), **options)
    input_stage.verify_complete()
    inputs = {row["unit"]["id"]: row for row in input_stage.completed()}
    def public_input(unit):
        return inputs[unit["group_id"]]["result"]["value"]
    if name == "public":
        def execute_public(unit):
            return {"input_result_sha256": inputs[unit["group_id"]]["seal"]["result_sha256"],
                    "paid_result": loaded[unit["arm"]].run(unit, public_input(unit), config["arms"][unit["arm"]])}
        return public_stage.execute(execute_public, **options)
    public_stage.verify_complete()
    public = {row["unit"]["id"]: row for row in public_stage.completed()}
    if name == "evaluation":
        original = {unit["id"]: unit for unit in units}
        def evaluate(score_unit):
            unit = original[score_unit["public_unit_id"]]
            row = public[unit["id"]]
            return {"public_result_sha256": row["seal"]["result_sha256"],
                    "input_result_sha256": inputs[unit["group_id"]]["seal"]["result_sha256"],
                    "score": loaded[unit["arm"]].score(unit, row["result"]["value"]["paid_result"],
                                                       public_input(unit), config["arms"][unit["arm"]])}
        return evaluation_stage.execute(evaluate, **options)
    evaluation_stage.verify_complete()
    if name != "analysis":
        raise L.IntegrityError("Unknown frozen stage.")
    import p309_analyze
    scored = evaluation_stage.completed()
    return analysis_stage.execute(lambda unit: p309_analyze.analyze(config, schedule, scored), **options)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("init-config", "development-checks", "prepare", "verify", "run-stage"))
    parser.add_argument("--stage", choices=STAGES)
    parser.add_argument("--task")
    parser.add_argument("--retry-reason")
    parser.add_argument("--failure-classification", choices=("unexplained_infrastructure",))
    args = parser.parse_args()
    if args.command == "init-config":
        result = initialize_config()
    elif args.command == "development-checks":
        result = development_checks()
    elif args.command == "prepare":
        result = prepare()
    elif args.command == "verify":
        result = verify()
    else:
        if args.stage is None:
            parser.error("run-stage requires --stage")
        result = final_stage(args.stage, args.task, args.retry_reason, args.failure_classification)
    print(json.dumps(result, sort_keys=True, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
