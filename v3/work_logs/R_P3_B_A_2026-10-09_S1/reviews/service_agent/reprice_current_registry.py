"""Registry-only v1.1 -> v1.2 transfer; no learner/scientific execution."""
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[5]
OUT = ROOT / "v3/work_logs/R_P3_B_A_2026-10-09_S1/development/service_comparison"
OLD = OUT / "run_001/sources/07_selective_feedback.py"
CURRENT = ROOT / "v3/checks/07_selective_feedback.py"
SERVICE = ROOT / "v3/checks/07_selective_feedback_service.py"
ADAPTER = ROOT / "v3/checks/07_computation_adapter.py"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    old = OLD.read_text()
    expected = old.replace('VERSION = "r-p3-b-a-blocked-prod-v1.1"',
                           'VERSION = "r-p3-b-a-blocked-prod-v1.2"', 1)
    line = '    meter.pay("admission", "whole_service_funding_check", 1)\n'
    guard = ('    try:\n'
             '        meter.pay("admission", "whole_service_funding_check", 1)\n'
             '    except BudgetExceeded as error:\n'
             '        error.meter = meter.snapshot()\n'
             '        raise\n')
    assert expected.count(line) == 1
    expected = expected.replace(line, guard, 1)
    assert CURRENT.read_text() == expected
    assert digest(OLD) == "d103cfdf9356c7e977df53c27bd57c26adc8df59a954c7c4dac2a0d537ad3af4"
    assert digest(CURRENT) == "f872ec2eb07df4722720763730932c33055e380f0ab76ddc3c848d79a5e70f48"
    assert digest(SERVICE) == "68c8f04f7d893cb89fb63a29c98dcc71977d06318d9ef74252b4f38569b5ef32"
    spec = importlib.util.spec_from_file_location("_r_p3ba_registry_reprice_service", SERVICE)
    S = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = S
    spec.loader.exec_module(S)
    current_registry = S.registry_setup((CURRENT, SERVICE, ADAPTER))
    results = json.loads((OUT / "run_001/result.json").read_text())
    transfers = []
    for arm in results["learner_arms"]:
        previous_registry = arm["resource_units"]["source_registry"]
        delta = current_registry.resources.total - previous_registry
        assert previous_registry == 18970
        transfers.append({
            "arm": arm["name"],
            "observed_version": "r-p3-b-a-blocked-prod-v1.1",
            "transferred_version": "r-p3-b-a-blocked-prod-v1.2",
            "observed_cold_units": arm["resource_units"]["cold_total"],
            "registry_only_delta_units": delta,
            "derived_current_cold_units": arm["resource_units"]["cold_total"] + delta,
            "unchanged_observed_ongoing_units": arm["resource_units"]["ongoing_including_learner_initialization"],
            "derived_current_price_totals": {
                price: {"realized_action_cold_total": str(F(case["realized_cold_total"]) + F(delta, 1000)),
                        "conditional_action_mean_cold_total": str(F(case["conditional_action_mean_cold_total"]) + F(delta, 1000))}
                for price, case in arm["evaluation"]["price_cases"].items()},
        })
    assert len({x["registry_only_delta_units"] for x in transfers}) == 1
    record = {
        "schema": "value_logic.selective_feedback.registry_transfer.v1",
        "status": "PASS", "stage": "DEVELOPMENT", "recorded_utc": datetime.now(timezone.utc).isoformat(),
        "kind": "Fresh registry-only procurement and exact source-diff transfer; no scientific rerun.",
        "textual_diff_verification": "Exact equality after only the version-marker replacement and the initial-charge BudgetExceeded annotation guard.",
        "successful_path_transfer": "The original charge executes once with identical inputs. Its new except clause is unentered in the 20 successful funded executions. No action, selector, feedback, arithmetic, resource-charge or capacity code changes. Version metadata changes separately.",
        "current_registry": current_registry.record(),
        "old_registry_units": 18970,
        "registry_only_delta_units": transfers[0]["registry_only_delta_units"],
        "transfers": transfers,
        "controls": "Control code and service+adapter closure unchanged; retain observed control costs.",
        "physical_runtime": "Retain v1.1 observed runtime only; no v1.2 runtime inferred.",
        "source_hashes": {str(p.relative_to(ROOT)): digest(p) for p in (OLD, CURRENT, SERVICE, ADAPTER, Path(__file__).resolve())},
        "principal_clock_credit_ns": 0,
    }
    target = OUT / "current_registry_reprice_v1.json"
    target.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({"status": record["status"], "current_registry_units": current_registry.resources.total,
                      "registry_only_delta_units": record["registry_only_delta_units"],
                      "transferred_arms": len(transfers), "scientific_reruns": 0}, indent=2))


if __name__ == "__main__":
    main()
