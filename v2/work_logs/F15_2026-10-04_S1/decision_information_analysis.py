"""Post-exposure diagnostic of decision information in saved F15 rows.

Contributor: ChatGPT (GPT-6 Astra Pro), October 5 UTC / October 4 local 2026.
This reads original hash-checked units only. It generates no population,
reruns no model, changes no criterion and adds no confidence statement.

Question: how often does the saved same-law action certificate survive when
the six marginal numerical intervals alone would not certify any action?
The rectangular relaxation treats different action costs as independent but
keeps C_a-C_a=0 exactly. It is a descriptive information-loss calculation,
not an additional registered control or an independently novel finding.

Run once without arguments; --check compares existing output byte-for-byte.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
import json
import os
from pathlib import Path


SESSION = Path(__file__).resolve().parent
ROOT = SESSION.parents[2]
RUN = ROOT / "v2/work_logs/F15_v1_run1/evaluation_attempt_1"
OUT = SESSION / "decision_information_analysis.json"


def canonical(value):
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read_checked(path, inputs):
    raw = path.read_bytes()
    expected = Path(str(path) + ".sha256").read_text().strip()
    assert digest(raw) == expected, path
    inputs.append({"path": str(path.relative_to(ROOT)), "sha256": expected})
    return json.loads(raw)


def group_summary(rows):
    def count(key):
        return sum(row[key] for row in rows)

    certified = [r for r in rows if r["decision_certified"]]
    return {
        "rows": len(rows),
        "decision_certified": len(certified),
        "all_six_numeric_admitted": count("all_six_numeric_admitted"),
        "all_six_numeric_exact": count("all_six_numeric_exact"),
        "decision_certified_with_some_numeric_refused": sum(
            not r["all_six_numeric_admitted"] for r in certified),
        "decision_certified_with_all_six_numeric_refused": sum(
            r["admitted_numeric_count"] == 0 for r in certified),
        "certified_order_selected_numeric_refused": count("certified_order_selected_numeric_refused"),
        "certified_selected_action_not_rectangular_certifiable": sum(
            not r["selected_rectangular_certifiable"] for r in certified),
        "certified_decision_but_no_rectangular_action_certifiable": sum(
            not r["any_rectangular_action_certifiable"] for r in certified),
        "useful_native_but_no_rectangular_action_certifiable": sum(
            r["useful_native"] and not r["any_rectangular_action_certifiable"] for r in rows),
        "joint_dispositions": [
            {"admitted_numeric_count": k[0], "decision_status": k[1],
             "native_status": k[2], "native_role": k[3], "rows": n}
            for k, n in sorted(Counter((r["admitted_numeric_count"], r["decision_status"],
                                        r["native_status"], r["native_role"]) for r in rows).items())],
        "largest_selected_rectangular_minus_coherent_regret": str(max(
            (Q(r["selected_rectangular_regret"])-Q(r["selected_coherent_regret"]) for r in rows),
            default=Q(0))),
    }


def analyze():
    config_path = ROOT / "v2/experiments/config.v1.json"
    raw_config = config_path.read_bytes()
    config = json.loads(raw_config)["retention"]
    epsilon = Q(config["decision_regret_tolerance"])
    fallback = Q(config["fallback_cost"])
    inputs = [{"path": str(config_path.relative_to(ROOT)), "sha256": digest(raw_config)}]
    rows = []
    inequality_checks = 0
    for seed in config["evaluation_seeds"]:
        for variant in config["variants"]:
            case = read_checked(RUN / f"retention_{seed}_{variant}.json", inputs)
            for r in case["methods"]:
                intervals = [(Q(q["lower"]), Q(q["upper"])) for q in r["numeric"]]
                assert len(intervals) == 6
                intervals.append((fallback, fallback))
                # Excluding b=a matters: an action cannot incur regret against
                # itself merely because its absolute cost interval is wide.
                rectangular = [max(Q(0), max(hi-intervals[b][0]
                                             for b in range(7) if b != a))
                               for a, (_, hi) in enumerate(intervals)]
                selected = r["selected_index"]
                coherent = Q(r["coherent_worst_regret"])
                assert Q(0) <= coherent <= rectangular[selected]
                inequality_checks += 1
                certified = r["decision_status"] != "refusal_to_fallback"
                assert certified == (coherent <= epsilon) == (not r["refused"])
                if certified:
                    assert selected == r["executed_index"]
                    assert Q(r["scoring"]["realized_regret"]) <= coherent
                else:
                    # Coherent regret describes the rejected recommendation,
                    # not the fallback that is subsequently executed.
                    assert r["executed_index"] == 6
                numeric_count = sum(q["status"] != "refused" for q in r["numeric"])
                rows.append({
                    "seed": seed, "variant": variant, "method": r["method"], "access": r["access"],
                    "selected_index": selected, "executed_index": r["executed_index"],
                    "selected_coherent_regret": str(coherent),
                    "selected_rectangular_regret": str(rectangular[selected]),
                    "best_rectangular_regret": str(min(rectangular)),
                    "rectangular_regrets_by_action": list(map(str, rectangular)),
                    "decision_status": r["decision_status"], "decision_certified": certified,
                    "actual_executed_regret": r["scoring"]["realized_regret"],
                    "admitted_numeric_count": numeric_count,
                    "all_six_numeric_admitted": numeric_count == 6,
                    "all_six_numeric_exact": all(q["status"] == "exact" for q in r["numeric"]),
                    "certified_order_selected_numeric_refused": (
                        r["decision_status"] == "certified_order" and
                        r["numeric"][selected]["status"] == "refused"),
                    "selected_rectangular_certifiable": rectangular[selected] <= epsilon,
                    "any_rectangular_action_certifiable": min(rectangular) <= epsilon,
                    "native_status": r["native"]["status"],
                    "native_role": r["native_certificate_role"],
                    "useful_native": r["native"]["useful_derivation_candidate"],
                    "numeric_intervals": [[str(lo), str(hi)] for lo, hi in intervals],
                })
    assert len(rows) == inequality_checks == 1920
    groups = [dict(access=access, method=method, **group_summary([
        r for r in rows if (r["access"], r["method"]) == (access, method)]))
        for access in config["access_regimes"] for method in config["methods"]]
    # The strongest registered ordinary methods retain the same information;
    # no diagnostic here upgrades a native-specific superiority claim.
    lookup = {(r["seed"], r["variant"], r["access"], r["method"]): r for r in rows}
    pair_checks = 0
    for row in rows:
        if row["method"] != "tailored":
            continue
        other = lookup[(row["seed"], row["variant"], row["access"], "exact_intervals")]
        for key in ("selected_coherent_regret", "rectangular_regrets_by_action",
                    "selected_index", "decision_status", "admitted_numeric_count"):
            assert row[key] == other[key]
            pair_checks += 1
    examples = [r for r in rows if r["method"] == "tailored" and
                r["access"] == "no_reacquisition" and r["variant"] == "program_edit"
                and r["useful_native"] and r["admitted_numeric_count"] == 0
                and not r["any_rectangular_action_certifiable"]]
    distinct = {(r["seed"], r["variant"]) for r in rows
                if r["useful_native"] and not r["any_rectangular_action_certifiable"]}
    return {
        "schema": "F15-post-exposure-decision-information-v1",
        "contributor": "ChatGPT (GPT-6 Astra Pro)",
        "script_sha256": digest(Path(__file__).read_bytes()),
        "scope": "Saved-data descriptive information relaxation; not a new registered control, inference family or novelty claim",
        "new_population_generation": False, "new_confirmatory_intervals": 0,
        "registered_decision_regret_tolerance": str(epsilon),
        "rectangular_definition": "For action a: max(0, max_{b != a}(upper[a]-lower[b])); include the exact fallback interval",
        "coherent_bound_target": "selected recommendation; equals the executed action only for certified decisions",
        "input_manifest": inputs,
        "coherent_below_rectangular_checks": inequality_checks,
        "tailored_exact_interval_field_checks": pair_checks,
        "summary": group_summary(rows), "by_method": groups,
        "useful_no_rectangular_action_distinct_episodes": len(distinct),
        "first_program_illustration": examples[0] if examples else None,
        "illustration_selection_rule": "First frozen-order tailored/no-reacquisition useful program-edit row with all six numeric refusals and no rectangular-certifiable action",
        "rows": rows,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    output = analyze()
    raw = canonical(output)
    sidecar = (digest(raw) + "\n").encode()
    if args.check:
        assert OUT.read_bytes() == raw
        assert Path(str(OUT) + ".sha256").read_bytes() == sidecar
    else:
        for path, data in [(OUT, raw), (Path(str(OUT) + ".sha256"), sidecar)]:
            with path.open("xb") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
        directory = os.open(SESSION, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "sha256": digest(raw),
                      "mode": "check" if args.check else "write", "summary": output["summary"],
                      "useful_no_rectangular_action_distinct_episodes": output["useful_no_rectangular_action_distinct_episodes"]},
                     indent=2))


if __name__ == "__main__":
    main()
