"""Immutable staged execution for the prospective P3-09 protocol.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-11.
This module generates no research cases. Its selfcheck uses development toys.
"""
from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import tempfile
import time
import traceback
import uuid


class IntegrityError(RuntimeError):
    pass


class RetryError(RuntimeError):
    pass


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True, allow_nan=False) + "\n").encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise IntegrityError("Duplicate JSON key: " + key)
        result[key] = value
    return result


def read_json(path):
    def reject(value):
        raise IntegrityError("Nonfinite JSON number: " + value)
    return json.loads(Path(path).read_text(encoding="utf-8"),
                      object_pairs_hook=_pairs, parse_constant=reject)


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def safe_id(value):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,179}", value):
        raise IntegrityError("Unsafe or missing record identifier.")
    return value


def fsync_directory(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def publish_bytes(path, data):
    """Publish once, never overwrite; an incomplete temporary file is evidence."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise IntegrityError("Refusing to replace durable record: " + str(path))
    temporary = path.with_name(path.name + ".pending-" + uuid.uuid4().hex)
    with temporary.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    # A hard link publishes without overwriting a competing writer's file.
    os.link(temporary, path)
    fsync_directory(path.parent)
    temporary.unlink()
    fsync_directory(path.parent)


def publish_json(path, value):
    publish_bytes(path, canonical(value))


@contextmanager
def exclusive_lock(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+b") as stream:
        try:
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise IntegrityError("Another writer holds the stage lock.") from error
        try:
            yield
        finally:
            fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def checked_schedule(units):
    if not isinstance(units, list) or not units:
        raise IntegrityError("A stage requires a nonempty fixed unit schedule.")
    identifiers = [safe_id(unit["id"]) for unit in units]
    if len(set(identifiers)) != len(identifiers):
        raise IntegrityError("Duplicate scheduled unit.")
    canonical(units)
    return identifiers


class Stage:
    """One fixed schedule, two attempts at most, and immutable completion seals.

    Callback-returned service failures are ordinary completed outcomes. Only an
    unreturned/interrupted callback or orchestration exception can leave a unit
    unsealed. Retrying requires a recorded investigator reason and unchanged
    binding; deterministic defects must be amended outside this class.
    """
    def __init__(self, root, name, binding, units):
        self.root = Path(root)
        self.name = safe_id(name)
        self.path = self.root / "stages" / self.name
        self.units = units
        self.ids = checked_schedule(units)
        self.binding = binding
        self.schedule_hash = digest(units)
        self.identity = {"stage": name, "binding": binding,
                         "schedule_sha256": self.schedule_hash}

    def _initialize(self):
        expected = dict(self.identity, schema="value_logic.p309.stage.v1", units=self.units)
        path = self.path / "schedule.json"
        if path.exists():
            if read_json(path) != expected:
                raise IntegrityError("Stage binding or scheduled units changed.")
        else:
            publish_json(path, expected)

    def completed_unit(self, unit):
        unit_root = self.path / "units" / safe_id(unit["id"])
        seals = sorted(unit_root.glob("attempt_*/seal.json"))
        if not seals:
            return None
        if len(seals) != 1:
            raise IntegrityError("Multiple completion seals for one unit.")
        seal_path = seals[0]
        seal = read_json(seal_path)
        result_path = seal_path.parent / "result.json"
        start_path = seal_path.parent / "start.json"
        if seal.get("identity") != self.identity or seal.get("unit_sha256") != digest(unit):
            raise IntegrityError("Sealed unit has wrong source/configuration/unit binding.")
        if not result_path.is_file() or sha256_file(result_path) != seal.get("result_sha256"):
            raise IntegrityError("Missing or altered completed unit bytes.")
        if not start_path.is_file() or sha256_file(start_path) != seal.get("start_sha256"):
            raise IntegrityError("Missing or altered unit start receipt.")
        result = read_json(result_path)
        if result.get("identity") != self.identity or result.get("unit") != unit:
            raise IntegrityError("Completed unit content does not match its binding.")
        if result.get("attempt") != seal.get("attempt"):
            raise IntegrityError("Completed unit attempt disagrees with seal.")
        return {"unit": unit, "seal": seal, "seal_path": str(seal_path.relative_to(self.root)),
                "result": result, "result_path": str(result_path.relative_to(self.root))}

    def completed(self, require_all=True):
        self._initialize()
        scheduled = set(self.ids)
        known_root = self.path / "units"
        if known_root.exists():
            unknown = {p.name for p in known_root.iterdir() if p.is_dir()} - scheduled
            if unknown:
                raise IntegrityError("Unscheduled unit directories: " + repr(sorted(unknown)))
        result = [self.completed_unit(unit) for unit in self.units]
        if require_all and any(row is None for row in result):
            raise IntegrityError("Stage has missing completion seals.")
        return result

    def _completion(self):
        rows = self.completed()
        expected = dict(self.identity, schema="value_logic.p309.stage_completion.v1",
                        expected_units=len(self.units), completed_units=len(rows),
                        seals=[{"unit_id": row["unit"]["id"], "path": row["seal_path"],
                                "sha256": sha256_file(self.root / row["seal_path"])} for row in rows])
        path = self.path / "complete.json"
        if path.exists():
            if read_json(path) != expected:
                raise IntegrityError("Stage completion index disagrees with immutable seals.")
        else:
            # This is a derived index, reconstructible only from valid seals.
            publish_json(path, expected)
        return expected

    def verify_complete(self):
        if not (self.path / "complete.json").exists():
            raise IntegrityError("Previous stage is not sealed complete.")
        return self._completion()

    def execute(self, callback, *, retry_reason=None, failure_classification=None):
        with exclusive_lock(self.root / "writer.lock"):
            self._initialize()
            rows = self.completed(require_all=False)
            if (self.path / "complete.json").exists():
                if retry_reason is not None:
                    raise RetryError("A completed stage cannot be retried.")
                return self._completion()
            if all(row is not None for row in rows):
                # A crash between the last unit seal and the derived index needs
                # no method replay and consumes no extra execution attempt.
                return self._completion()
            attempts_root = self.path / "attempts"
            starts = sorted(attempts_root.glob("attempt_*/start.json"))
            for index, path in enumerate(starts, 1):
                start = read_json(path)
                if start.get("identity") != self.identity or start.get("attempt") != index:
                    raise IntegrityError("Attempt history is not contiguous or bound.")
            if len(starts) >= 2:
                raise RetryError("The stage's one unchanged retry is exhausted.")
            if starts:
                if failure_classification != "unexplained_infrastructure" or not retry_reason or not retry_reason.strip():
                    raise RetryError("Retry requires a recorded unexplained-infrastructure disposition.")
                previous = starts[-1].parent
                if not (previous / "failure.json").exists():
                    publish_json(previous / "interruption.json", {
                        "schema": "value_logic.p309.interruption.v1", "identity": self.identity,
                        "observed_utc": utc_now(), "reason": retry_reason,
                        "statement": "Prior attempt had no terminal receipt; unsealed bytes are preserved.",
                        "unmeasured_attempt_cost": "unknown"})
            elif retry_reason is not None or failure_classification is not None:
                raise RetryError("Initial execution is not a retry.")
            attempt = len(starts) + 1
            attempt_root = attempts_root / ("attempt_%02d" % attempt)
            publish_json(attempt_root / "start.json", {
                "schema": "value_logic.p309.attempt.v1", "identity": self.identity,
                "attempt": attempt, "started_utc": utc_now(), "retry_reason": retry_reason,
                "failure_classification": failure_classification,
                "preserved_complete_units": [row["unit"]["id"] for row in rows if row is not None]})
            current_id = None
            try:
                for unit, completed in zip(self.units, rows):
                    if completed is not None:
                        continue
                    current_id = unit["id"]
                    unit_root = self.path / "units" / current_id / ("attempt_%02d" % attempt)
                    started = {"schema": "value_logic.p309.unit_start.v1", "identity": self.identity,
                               "unit": unit, "attempt": attempt, "started_utc": utc_now(),
                               "started_monotonic_ns": time.monotonic_ns()}
                    publish_json(unit_root / "start.json", started)
                    wall_start, cpu_start = time.monotonic_ns(), time.process_time_ns()
                    value = callback(unit)
                    result = {"schema": "value_logic.p309.unit_result.v1", "identity": self.identity,
                              "unit": unit, "attempt": attempt, "value": value,
                              "started_utc": started["started_utc"], "finished_utc": utc_now(),
                              "resource_observation": {
                                  "wall_ns": time.monotonic_ns() - wall_start,
                                  "process_cpu_ns": time.process_time_ns() - cpu_start,
                                  "process_peak_rss_kib_at_end": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                                  "rss_scope": "whole process high-water mark, not an additive unit allocation"}}
                    publish_json(unit_root / "result.json", result)
                    publish_json(unit_root / "seal.json", {
                        "schema": "value_logic.p309.unit_seal.v1", "identity": self.identity,
                        "unit_sha256": digest(unit), "attempt": attempt,
                        "start_sha256": sha256_file(unit_root / "start.json"),
                        "result_sha256": sha256_file(unit_root / "result.json"),
                        "sealed_utc": utc_now()})
                completion = self._completion()
                publish_json(attempt_root / "complete.json", {
                    "identity": self.identity, "attempt": attempt, "finished_utc": utc_now(),
                    "completion_sha256": digest(completion)})
                return completion
            except BaseException as error:
                failure_path = attempt_root / "failure.json"
                if not failure_path.exists():
                    publish_json(failure_path, {
                        "schema": "value_logic.p309.failure.v1", "identity": self.identity,
                        "attempt": attempt, "failed_unit_id": current_id, "observed_utc": utc_now(),
                        "error_type": type(error).__name__, "error": str(error),
                        "traceback": traceback.format_exc(), "automatic_retry": False,
                        "classification": "unclassified; deterministic defects require a versioned amendment",
                        "unmeasured_failed_attempt_cost": "unknown unless preserved method evidence measures it"})
                raise


def execution_history(root, current_stage=None, current_unit_id=None):
    """Preserve outer attempts without inventing lost callback invoices.

    Internal paid service failures are already in sealed results. An unsealed
    interrupted callback is a different source of possible cost and is never
    silently charged zero when a later unchanged retry supplies a complete path.
    """
    root = Path(root)
    stages = []
    unknown_public, unknown_other = [], []
    for stage_path in sorted((root / "stages").glob("*")):
        if not stage_path.is_dir():
            continue
        attempts = []
        for attempt in sorted((stage_path / "attempts").glob("attempt_*")):
            documents = []
            for path in sorted(attempt.glob("*.json")):
                documents.append({"path": str(path.relative_to(root)), "sha256": sha256_file(path),
                                  "record": read_json(path)})
            attempts.append({"attempt_directory": attempt.name, "documents": documents})
        units = []
        for unit_path in sorted((stage_path / "units").glob("*")):
            for attempt in sorted(unit_path.glob("attempt_*")):
                start_path = attempt / "start.json"
                seal_path = attempt / "seal.json"
                active = (stage_path.name == current_stage and unit_path.name == current_unit_id
                          and not seal_path.exists()
                          and attempt.name == (attempts[-1]["attempt_directory"] if attempts else None))
                inventory = [{"path": str(path.relative_to(root)), "bytes": path.stat().st_size,
                              "sha256": sha256_file(path)}
                             for path in sorted(attempt.iterdir()) if path.is_file()]
                row = {"unit_id": unit_path.name, "attempt_directory": attempt.name,
                       "sealed": seal_path.is_file(), "current_analysis_unit": active,
                       "preserved_files": inventory}
                if not row["sealed"] and not active:
                    row["unmeasured_attempt_cost"] = "unknown; no authoritative complete invoice"
                    target = unknown_public if stage_path.name == "public" else unknown_other
                    target.append({"stage": stage_path.name, "unit_id": unit_path.name,
                                   "attempt_directory": attempt.name,
                                   "start_sha256": sha256_file(start_path) if start_path.exists() else None})
                units.append(row)
        stages.append({"stage": stage_path.name, "attempt_count": len(attempts),
                       "retried": len(attempts) > 1, "attempts": attempts, "units": units})
    return {"schema": "value_logic.p309.execution_history.v1", "stages": stages,
            "unknown_unsealed_public_attempts": unknown_public,
            "unknown_other_stage_attempts": unknown_other,
            "complete_outer_paid_attempt_accounting": not unknown_public,
            "complete_physical_run_accounting": not unknown_public and not unknown_other,
            "invoice_scope": "sealed completed-path invoices include all internal attempts; unsealed outer attempts remain separately unknown",
            "current_analysis_cost_location": "the surrounding sealed analysis-unit resource observation"}


def selfcheck():
    """Adversarial DEVELOPMENT lifecycle tests; no final adapter is imported."""
    checks = []
    with tempfile.TemporaryDirectory(prefix="p309-development-lifecycle-") as directory:
        base = Path(directory)
        units = [{"id": "dev-a", "number": 1}, {"id": "dev-b", "number": 2}]
        binding = {"stage": "DEVELOPMENT", "fixture": "explicit integers 1 and 2"}
        calls = []
        stage = Stage(base / "resume", "public", binding, units)
        def initial(unit):
            calls.append(unit["id"])
            if unit["id"] == "dev-b":
                raise OSError("DEVELOPMENT injected interrupted transport")
            return {"answer": unit["number"] * 2}
        try:
            stage.execute(initial)
        except OSError:
            pass
        else:
            raise AssertionError("Injected failure was lost.")
        first = stage.completed_unit(units[0])
        first_hash = sha256_file(stage.root / first["result_path"])
        try:
            stage.execute(lambda unit: None)
        except RetryError:
            checks.append("unexplained failure needs explicit retry disposition")
        else:
            raise AssertionError("Implicit retry accepted.")
        stage.execute(lambda unit: calls.append(unit["id"]) or {"answer": 4},
                      retry_reason="Injected development transport failure; code and schedule unchanged.",
                      failure_classification="unexplained_infrastructure")
        assert calls == ["dev-a", "dev-b", "dev-b"]
        assert sha256_file(stage.root / first["result_path"]) == first_hash
        checks.append("completed unit preserved byte-for-byte and never rerun")
        history = execution_history(stage.root)
        assert len(history["unknown_unsealed_public_attempts"]) == 1
        assert history["unknown_unsealed_public_attempts"][0]["unit_id"] == "dev-b"
        assert history["complete_outer_paid_attempt_accounting"] is False
        checks.append("lost outer-attempt cost survives successful unchanged retry")
        try:
            stage.execute(lambda unit: None, retry_reason="extra")
        except RetryError:
            checks.append("completed stage cannot be replayed as a retry")
        else:
            raise AssertionError("Completed stage replay accepted.")
        # Missing derived completion is reconstructible from all valid seals.
        (stage.path / "complete.json").unlink()
        stage.execute(lambda unit: (_ for _ in ()).throw(AssertionError("must not execute")))
        checks.append("derived completion reconstructed only from valid unit seals")
        (stage.root / first["result_path"]).write_text("{}\n")
        try:
            stage.verify_complete()
        except IntegrityError:
            checks.append("altered completed bytes rejected despite completion index")
        else:
            raise AssertionError("Altered output accepted.")
        failed = Stage(base / "exhaustion", "public", binding, [{"id": "dev-fail"}])
        def boom(unit):
            raise OSError("DEVELOPMENT failure")
        for attempt in (1, 2):
            try:
                failed.execute(boom, **({} if attempt == 1 else {
                    "retry_reason": "Injected unchanged failure", "failure_classification": "unexplained_infrastructure"}))
            except OSError:
                pass
        try:
            failed.execute(boom, retry_reason="third", failure_classification="unexplained_infrastructure")
        except RetryError:
            checks.append("one unchanged retry exhausted after two failed attempts")
        else:
            raise AssertionError("Third attempt accepted.")
        wrong = Stage(base / "exhaustion", "public", dict(binding, changed=True), [{"id": "dev-fail"}])
        try:
            wrong.completed(False)
        except IntegrityError:
            checks.append("changed source or configuration binding rejected")
        else:
            raise AssertionError("Changed binding accepted.")
        try:
            Stage(base, "bad", binding, [{"id": "same"}, {"id": "same"}])
        except IntegrityError:
            checks.append("duplicate scheduled units rejected")
        else:
            raise AssertionError("Duplicate accepted.")
        try:
            safe_id("../outside")
        except IntegrityError:
            checks.append("unit path traversal rejected")
        else:
            raise AssertionError("Unsafe identifier accepted.")
        with exclusive_lock(base / "dev.lock"):
            try:
                with exclusive_lock(base / "dev.lock"):
                    raise AssertionError("Concurrent lock accepted.")
            except IntegrityError:
                checks.append("simultaneous writer blocked")
        orphan = Stage(base / "orphan", "inputs", binding, [{"id": "dev-orphan"}])
        orphan._initialize()
        publish_json(orphan.path / "units/dev-orphan/attempt_01/result.json", {"unsealed": True})
        assert orphan.completed(False) == [None]
        checks.append("unsealed orphan output is not completion")
        missing = Stage(base / "missing", "public", binding, [{"id": "dev-missing"}])
        try:
            missing.verify_complete()
        except IntegrityError:
            checks.append("downstream stage blocked by missing completion")
        else:
            raise AssertionError("Missing stage accepted.")
    return {"stage": "DEVELOPMENT", "status": "PASS", "fixture_scope": "explicit toy integers only",
            "final_population_generated": False, "checks": checks, "passed": len(checks)}
