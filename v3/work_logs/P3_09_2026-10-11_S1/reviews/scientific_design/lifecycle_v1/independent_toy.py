"""DEVELOPMENT-only lifecycle check; no final adapter/configuration is imported."""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "source/v3/experiments/p309_lifecycle.py"
spec = importlib.util.spec_from_file_location("_p309_independent_lifecycle_toy", SOURCE)
L = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = L
spec.loader.exec_module(L)


def main():
    out = HERE / "run"
    out.mkdir(exist_ok=False)
    checks = []
    units = [{"id": "dev-paid-negative"}, {"id": "dev-interrupted"}]
    stage = L.Stage(out / "toy_episode", "public",
                    {"stage": "DEVELOPMENT", "toy": "explicit statuses and integer bills"}, units)
    calls = []

    def first(unit):
        calls.append(unit["id"])
        if unit["id"] == "dev-paid-negative":
            return {"status": "FAIL", "validity_pass": False, "declared_toy_bill": 7}
        raise OSError("DEVELOPMENT injected interruption before a returned scientific value")

    try:
        stage.execute(first)
    except OSError:
        pass
    else:
        raise AssertionError("Toy interruption did not propagate.")
    sealed = stage.completed_unit(units[0])
    assert sealed["result"]["value"]["validity_pass"] is False
    first_hash = L.sha256_file(stage.root / sealed["result_path"])
    checks.append("returned negative scientific result is sealed as a complete outcome")
    failure_path = stage.path / "attempts/attempt_01/failure.json"
    failure = L.read_json(failure_path)
    assert failure["failed_unit_id"] == units[1]["id"]
    assert failure["automatic_retry"] is False
    assert failure["unmeasured_failed_attempt_cost"].startswith("unknown")
    checks.append("unreturned interruption has an explicit unknown cost, never a zero bill")
    try:
        stage.verify_complete()
    except L.IntegrityError:
        checks.append("incomplete stage blocks a downstream completeness check")
    else:
        raise AssertionError("Incomplete stage acquired completion authority.")

    def resumed(unit):
        calls.append(unit["id"])
        assert unit["id"] == "dev-interrupted"
        return {"status": "PASS", "validity_pass": True, "declared_toy_bill": 11}

    completion = stage.execute(resumed, retry_reason="Explicit unchanged DEVELOPMENT interruption witness",
                               failure_classification="unexplained_infrastructure")
    assert calls == ["dev-paid-negative", "dev-interrupted", "dev-interrupted"]
    assert L.sha256_file(stage.root / sealed["result_path"]) == first_hash
    assert completion["completed_units"] == 2
    assert failure_path.is_file()
    checks.append("single retry preserves the completed negative result and executes only the missing unit")
    rows = stage.completed()
    known_completed_bill = sum(row["result"]["value"]["declared_toy_bill"] for row in rows)
    assert known_completed_bill == 18
    checks.append("completed-path bill includes negative outcome; unknown interrupted overhead remains separate")
    try:
        stage.execute(resumed, retry_reason="Must not replay a completed stage",
                      failure_classification="unexplained_infrastructure")
    except L.RetryError:
        checks.append("completed-stage replay is rejected")
    else:
        raise AssertionError("Completed negative result was exposed to another attempt.")
    result = {"schema": "p309.lifecycle-independent-toy.v1", "stage": "DEVELOPMENT",
              "status": "PASS", "checks": checks, "callback_calls": calls,
              "known_completed_path_toy_bill": known_completed_bill,
              "complete_across_all_infrastructure_attempts_bill": None,
              "unmeasured_interruption_scope": failure["unmeasured_failed_attempt_cost"],
              "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
              "final_generator_calls": 0, "final_seed_reads": 0, "policy_runs": 0,
              "principal_clock_credit_seconds": 0}
    L.publish_json(out / "results.json", result)
    print(json.dumps({"status": result["status"], "checks": len(checks),
                      "result_sha256": L.sha256_file(out / "results.json")}, sort_keys=True))


if __name__ == "__main__":
    main()
