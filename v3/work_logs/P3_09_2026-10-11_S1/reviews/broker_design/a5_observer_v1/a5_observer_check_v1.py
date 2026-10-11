"""Read saved paid reports and check the new A5 observer; no policy calls."""
import ast
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys
from datetime import datetime, timezone


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    with path.open("x", encoding="ascii") as stream:
        stream.write(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n")


def pair(value):
    value = F(value)
    return [value.numerator, value.denominator]


def main():
    folder = Path(sys.argv[1]).resolve()
    manifest = json.loads((folder / "manifest.json").read_text())
    frozen = folder / "source"
    for row in manifest["sources"]:
        path = frozen / row["path"]
        if path.stat().st_size != row["bytes"] or digest(path) != row["sha256"]:
            raise ValueError("Frozen A5 source mismatch: " + row["path"])
    if digest(Path(__file__)) != manifest["observer_sha256"]:
        raise ValueError("A5 observer changed after its manifest.")
    previous = Path(manifest["saved_input"]["path"])
    if digest(previous) != manifest["saved_input"]["sha256"]:
        raise ValueError("The saved DEVELOPMENT input changed.")
    original = Path(manifest["previous_adapter"]["path"])
    if digest(original) != manifest["previous_adapter"]["sha256"]:
        raise ValueError("The preserved v1 source changed.")
    out = folder / "run"
    out.mkdir(exist_ok=False)
    write(out / "started.json", {"stage": "DEVELOPMENT_OBSERVER_ONLY", "principal_clock_credit": 0,
        "manifest_sha256": digest(folder / "manifest.json"),
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "command": [sys.executable, str(Path(__file__).resolve()), str(folder)],
        "policy_calls": 0, "reporter_calls": 0, "private_truth_calls": 0, "final_generation_calls": 0})
    sys.path.insert(0, str(frozen / "v3/experiments"))
    import p309_broker as adapter
    if Path(adapter.__file__).resolve() != frozen / "v3/experiments/p309_broker.py":
        raise ValueError("A5 adapter import escaped its frozen closure.")
    saved = json.loads(previous.read_text())
    checks, results = [], []

    def check(name, value):
        checks.append({"name": name, "passed": bool(value)})

    before = {node.name: ast.dump(node, include_attributes=False) for node in ast.parse(original.read_bytes()).body
              if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
    now = {node.name: ast.dump(node, include_attributes=False) for node in ast.parse(Path(adapter.__file__).read_bytes()).body
           if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
    for name, body in before.items():
        if name not in ("score", "_invalid_score"):
            check("unchanged_original_function:" + name, now[name] == body)
    check("only_one_added_function", set(now) - set(before) == {"_report_comparison"})

    def examine(identity, optional, horizon, synthetic=False):
        result = adapter._report_comparison(optional, horizon)
        results.append({"id": identity, "synthetic_observer_input": synthetic,
            "horizon": horizon, "optional_report": optional if synthetic else None,
            "comparison": result})
        check(identity + ":no_coverage_claim", result["empirical_coverage_claim"] is False)
        check(identity + ":fixed_threshold", result["practical_threshold_normalized"] == [1, 100])
        check(identity + ":actual_optional_fee", result["additional_units"] == (0 if optional is None else optional["additional_units"]))
        if optional is None:
            check(identity + ":no_report", result["status"] == "not_requested" and result["endpoints"] == {})
            return result
        report = optional["report"]
        if report["status"] != "success":
            check(identity + ":failed_report", result["status"] == report["status"] and result["endpoints"] == {})
            return result
        expected_conflict = False
        original_widths = adapter._report_widths(optional, horizon)
        for name, interval in report["intervals"].items():
            row = result["endpoints"][name]
            lower, upper = F(*interval["lower"]), F(*interval["upper"])
            dl, du = [F(*value) for value in report["deterministic_envelopes"][name]]
            lower_gain, upper_gain = lower - dl, du - upper
            conflict = interval.get("confidence_conflict", False) or upper < lower
            expected_conflict |= conflict
            expected = {"lower": interval["lower"], "upper": interval["upper"],
                "deterministic_lower": report["deterministic_envelopes"][name][0],
                "deterministic_upper": report["deterministic_envelopes"][name][1],
                "deterministic_width": pair(du - dl),
                "deterministic_width_per_horizon": pair((du - dl) / horizon),
                "delivered_signed_span": pair(upper - lower),
                "lower_endpoint_gain": pair(lower_gain), "upper_endpoint_gain": pair(upper_gain),
                "normalized_lower_endpoint_gain": pair(lower_gain / horizon),
                "normalized_upper_endpoint_gain": pair(upper_gain / horizon),
                "width": None if conflict else pair(upper - lower),
                "width_per_horizon": None if conflict else pair((upper - lower) / horizon),
                "normalized_width_reduction": None if conflict else pair((lower_gain + upper_gain) / horizon),
                "practical_width_reduction": not conflict and lower_gain + upper_gain >= F(horizon, 100),
                "practical_lower_endpoint_gain": not conflict and lower_gain >= F(horizon, 100),
                "practical_upper_endpoint_gain": not conflict and upper_gain >= F(horizon, 100),
                "confidence_conflict": bool(conflict),
                "status": "confidence_conflict" if conflict else "success"}
            for field, expected_value in expected.items():
                check(identity + ":" + name + ":" + field, row[field] == expected_value)
            for field in ("lower", "upper", "width", "width_per_horizon", "confidence_conflict"):
                check(identity + ":" + name + ":v1_field_compatible:" + field,
                    row[field] == original_widths[name][field])
        check(identity + ":aggregate_status", result["status"] == ("confidence_conflict" if expected_conflict else "success"))
        return result

    for record in saved["public_records"]:
        examine(record["unit"]["id"], record["optional_reporting"],
            record["unit"]["segments"][0]["stop"])
    cases = (("no_improvement", 0, 100, 0, 100, False),
             ("exact_practical_threshold", 0, 100, 1, 100, False),
             ("adverse_wider", 0, 100, -1, 101, False),
             ("conflict", 0, 4, 3, 2, True))
    synthetic = {}
    for identity, dl, du, lower, upper, conflict in cases:
        report = {"status": "success", "reference_basis": "snapshot", "radius_rule": "grid",
            "intervals": {name: {"lower": [lower, 1], "upper": [upper, 1], "confidence_conflict": conflict}
                          for name in ("V", "F", "Z")},
            "deterministic_envelopes": {name: [[dl, 1], [du, 1]] for name in ("V", "F", "Z")}}
        synthetic[identity] = examine(identity, {"report": report, "additional_units": 17}, 100, True)
    check("synthetic:no_improvement_not_practical", synthetic["no_improvement"]["endpoints"]["F"]["normalized_width_reduction"] == [0, 1]
        and synthetic["no_improvement"]["endpoints"]["F"]["practical_width_reduction"] is False)
    check("synthetic:threshold_inclusive", synthetic["exact_practical_threshold"]["endpoints"]["F"]["normalized_width_reduction"] == [1, 100]
        and synthetic["exact_practical_threshold"]["endpoints"]["F"]["practical_width_reduction"] is True)
    check("synthetic:negative_preserved", synthetic["adverse_wider"]["endpoints"]["F"]["normalized_width_reduction"] == [-1, 50])
    check("synthetic:conflict_no_usable_gain", synthetic["conflict"]["endpoints"]["F"]["normalized_width_reduction"] is None
        and synthetic["conflict"]["endpoints"]["F"]["practical_width_reduction"] is False)
    check("saved_input_unchanged", digest(previous) == manifest["saved_input"]["sha256"])
    check("preserved_adapter_unchanged", digest(original) == manifest["previous_adapter"]["sha256"])
    for row in manifest["sources"]:
        check("source_unchanged:" + row["path"], digest(frozen / row["path"]) == row["sha256"])
    paid_units = sorted({row["common_source_invoice"]["total"] for row in saved["public_records"]})
    core = set(adapter.CORE)
    new_units = sum(2 * max(1, (row["bytes"] + 7) // 8) + (row["bytes"] + 72) // 64
                    for row in manifest["sources"] if row["path"] in core)
    result = {"stage": "DEVELOPMENT_OBSERVER_ONLY", "principal_clock_credit": 0,
        "status": "PASS" if all(row["passed"] for row in checks) else "FAIL",
        "policy_calls": 0, "reporter_calls": 0, "private_truth_calls": 0, "final_generation_calls": 0,
        "results": results, "checks": checks, "saved_paid_source_units": paid_units,
        "prospective_current_source_units": new_units,
        "cost_scope": "Old actual invoices stay bound to old source; the prospective source tariff is a separate byte-only calculation."}
    write(out / "results.json", result)
    summary = {key: result[key] for key in ("stage", "principal_clock_credit", "status", "policy_calls",
        "reporter_calls", "private_truth_calls", "final_generation_calls", "saved_paid_source_units", "prospective_current_source_units")}
    summary.update(assertions=len(checks), saved_records=len(saved["public_records"]), synthetic_cases=len(cases),
        failed_assertions=[row for row in checks if not row["passed"]], result_sha256=digest(out / "results.json"),
        finished_utc=datetime.now(timezone.utc).isoformat())
    write(out / "summary.json", summary)
    print(json.dumps(summary, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
