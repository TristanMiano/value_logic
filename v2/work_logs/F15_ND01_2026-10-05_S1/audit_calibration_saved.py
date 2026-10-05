"""Independently reconstruct saved calibration endpoint labels.

This reads sufficient statistics only: it does not import the experimental
analysis module, generate pairs, fit models, or select alignments. Contributor:
ChatGPT (GPT-6 Astra Pro), independent F15-ND01 protocol audit sub-agent.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path


STRATA = ("mixed_near", "mixed_far", "preserve_other", "equal_target", "scale_separating")
HYPOTHESES = ("identity", "inv_eta", "inv_one_minus_eta", "inv_total_cost")
CONTROLS = ("random", "permuted_concept", "shuffled_donor", "untrained")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", nargs=5, required=True, type=Path)
    parser.add_argument("--assessment", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    rows = []
    inputs = []
    checks = 0

    def require(condition, message):
        nonlocal checks
        checks += 1
        if not condition:
            raise AssertionError(message)

    def read(path):
        raw = path.read_bytes()
        inputs.append({"path": str(path), "bytes": len(raw),
                       "sha256": hashlib.sha256(raw).hexdigest()})
        sidecar = Path(str(path) + ".sha256")
        if sidecar.exists():
            expected = sidecar.read_text().strip().split()[0]
            require(expected == inputs[-1]["sha256"], f"Sidecar differs: {path}")
        return json.loads(raw)

    def interval(key, mean, n, low=0.0, high=1.0):
        require(type(n) is int and n > 0, f"Invalid count: {key}")
        require(math.isfinite(mean) and low - 1e-12 <= mean <= high + 1e-12,
                f"Invalid bounded mean: {key}")
        radius = (high - low) * math.sqrt(math.log(2 * 560 / 0.05) / (2 * n))
        row = {"id": key, "mean": mean, "n": n, "radius": radius,
               "lower": max(low, mean - radius), "upper": min(high, mean + radius)}
        rows.append(row)
        return row

    def close_dict(actual, expected, message):
        for key in ("mean", "radius", "lower", "upper"):
            require(math.isclose(actual[key], expected[key], rel_tol=1e-12, abs_tol=1e-12),
                    f"{message}/{key}")
        require(actual["n"] == expected["n"], f"{message}/n")

    results = [read(path) for path in args.results]
    saved = read(args.assessment)
    require(len(saved["models"]) == 5, "Assessment must contain all five layouts")
    require(saved["development_only"] is True, "Calibration is development only")
    require(saved["pilot_support_criterion_met"] is False,
            "Constructed calibration cannot change original pilot status")
    require(saved["interval_family_cap"] == 560 and saved["familywise_alpha"] == 0.05,
            "Frozen interval family or alpha changed")
    require([r["evaluation_seed"] for r in results] == list(range(1511691, 1511696)),
            "Missing or reordered calibration seed")
    model_rows = []

    for mi, (result, reported) in enumerate(zip(results, saved["models"])):
        prefix = f"model{mi}"
        n = result["pairs_per_stratum"]
        require(n == 8192 and result["task"]["n"] == 8192, "Incomplete frozen counts")
        require(result["diagnostic"]["ordinary_training_steps"] == 0,
                "Construction must not acquire ordinary-training credit")
        require(result["diagnostic"]["independent_ordinary_training_replicates"] is False,
                "The five models are constructed coordinate layouts")
        require(result["oracle_known_subset_accuracy"]["complete_endpoint_assessed_for_oracle"] is False,
                "Known subsets cannot inherit searched controls")

        task = result["task"]
        base = interval(prefix + "/base_mae", task["mae"], task["n"])
        regret = interval(prefix + "/base_normalized_regret",
                          task["mean_normalized_decision_regret"], task["n"])
        require(task["decision_regret_bound"] == 1.375, "Regret normalization changed")
        require(math.isclose(task["mean_decision_regret"],
                             1.375 * task["mean_normalized_decision_regret"],
                             rel_tol=1e-12, abs_tol=1e-12), "Regret normalization mismatch")
        task_ready = base["upper"] <= 0.05 and 1.375 * regret["upper"] <= 0.05
        require(task_ready == reported["task_ready"], "Task-ready disposition mismatch")
        close_dict(base, reported["base_probability_interval"], prefix + "/base_mae")
        close_dict(regret, reported["base_normalized_regret_interval"], prefix + "/regret")

        conditional = []
        for role in (0, 1):
            group = {}
            for stratum in STRATA:
                metric = result["alignments"]["identity/aligned"]["roles"][role][stratum]["base_prediction"]
                require(metric["n"] == n, "Conditional count mismatch")
                group[stratum] = interval(f"{prefix}/conditional_base/{role}/{stratum}", metric["mae"], n)
            conditional.append(group)

        hypothesis_states = {}
        for g in HYPOTHESES:
            role_states = []
            for role in (0, 1):
                expected_role = reported["hypotheses"][g]["roles"][role]
                metrics = result["alignments"][f"{g}/aligned"]["roles"][role]
                absolute, decisions, advantages = {}, {}, {}
                for stratum in STRATA:
                    require(metrics[stratum]["n"] == n, "Intervention count mismatch")
                    absolute[stratum] = interval(f"{prefix}/{g}/{role}/{stratum}/mae",
                                                 metrics[stratum]["mae"], n)
                    close_dict(absolute[stratum], expected_role["absolute"][stratum],
                               f"{prefix}/{g}/{role}/{stratum}")
                    close_dict(conditional[role][stratum], expected_role["conditional_base"][stratum],
                               f"{prefix}/{g}/{role}/conditional/{stratum}")
                for stratum in ("mixed_near", "mixed_far"):
                    decisions[stratum] = interval(f"{prefix}/{g}/{role}/{stratum}/disagreement",
                                                  1 - metrics[stratum]["decision_agreement"], n)
                    close_dict(decisions[stratum], expected_role["decisions"][stratum],
                               f"{prefix}/{g}/{role}/{stratum}/decision")
                for control in CONTROLS:
                    cells = result["matched_control_comparisons_by_g"][g][control]
                    total = 0.0
                    for stratum in STRATA:
                        cell = cells[f"{role}/{stratum}"]
                        require(cell["n"] == n, "Control count mismatch")
                        require(math.isclose(cell["sum"] / n,
                                             cell["mean_paired_absolute_error_improvement"],
                                             rel_tol=1e-12, abs_tol=1e-12),
                                "Control sum/mean mismatch")
                        require(cell["minimum"] <= cell["mean_paired_absolute_error_improvement"] <= cell["maximum"],
                                "Control mean outside extrema")
                        require(-1 - 1e-12 <= cell["minimum"] <= cell["maximum"] <= 1 + 1e-12,
                                "Control values outside bounded range")
                        require(cell["sum"] ** 2 / n - 1e-10 <= cell["sum_squares"] <= n + 1e-10,
                                "Control variance inequality violated")
                        total += cell["sum"]
                    advantages[control] = interval(f"{prefix}/{g}/{role}/{control}/advantage",
                                                   total / (5 * n), 5 * n, -1.0, 1.0)
                    close_dict(advantages[control], expected_role["control_advantages"][control],
                               f"{prefix}/{g}/{role}/{control}")
                adequate = (all(a["upper"] <= 0.05 for a in absolute.values())
                            and all(a["upper"] <= 0.05 for a in conditional[role].values())
                            and all(absolute[s]["upper"] + conditional[role][s]["upper"] <= 0.10 for s in STRATA)
                            and decisions["mixed_near"]["upper"] <= 0.35
                            and decisions["mixed_far"]["upper"] <= 0.10)
                selective = all(a["lower"] >= 0.01 for a in advantages.values())
                violated = any(a["lower"] > 0.05 for a in absolute.values())
                require(adequate == expected_role["absolute_and_decision_criteria"], "Adequacy mismatch")
                require(selective == expected_role["matched_control_specificity"], "Selectivity mismatch")
                require(violated == expected_role["mae_tolerance_falsified_in_a_stratum"], "Falsification-label mismatch")
                role_states.append({"adequate": adequate, "selective": selective, "mae_violated": violated})
            hypothesis_states[g] = {"adequate": all(r["adequate"] for r in role_states),
                                    "selective": all(r["selective"] for r in role_states),
                                    "roles": role_states}
        distinguished = []
        for g in HYPOTHESES[1:]:
            for role in (0, 1):
                cell = result["alternative_comparisons"][g][f"{role}/scale_separating"]
                require(cell["total_pairs"] == cell["separating_pairs"] == n,
                        "All separating pairs must be retained")
                frequency = interval(f"{prefix}/{g}/{role}/frequency", cell["separating_fraction"], n)
                comparison = cell["same_identity_subset_comparison"]
                require(comparison["n"] == n, "Scale comparison count mismatch")
                require(math.isclose(comparison["sum"] / n, comparison["mean_paired_absolute_error_improvement"],
                                     rel_tol=1e-12, abs_tol=1e-12), "Scale sum/mean mismatch")
                advantage = interval(f"{prefix}/{g}/{role}/scale_advantage",
                                      comparison["mean_paired_absolute_error_improvement"], n, -1.0, 1.0)
                expected_scale = reported["same_subset_scale_tests"][g][role]
                close_dict(frequency, expected_scale["frequency"], "Scale frequency")
                close_dict(advantage, expected_scale["advantage"], "Scale advantage")
                is_distinguished = frequency["lower"] >= 0.90 and advantage["lower"] >= 0.01
                require(is_distinguished == expected_scale["distinguished"], "Scale classification mismatch")
                distinguished.append(is_distinguished)

        numerical = reported["numerical_controls_valid"]
        identity = hypothesis_states["identity"]
        if not numerical:
            disposition = "numerical_or_protocol_failure"
        elif not task_ready:
            disposition = "task_underlearned_at_frozen_criterion"
        elif identity["adequate"] and identity["selective"] and all(distinguished):
            disposition = "expected_cost_interchange_supported_at_declared_scope"
        elif identity["adequate"]:
            disposition = "interchange_adequate_but_not_discriminated_from_controls_or_scales"
        elif any(hypothesis_states[g]["adequate"] and hypothesis_states[g]["selective"] for g in HYPOTHESES[1:]):
            disposition = "competing_cost_scale_supported_original_not_supported"
        else:
            disposition = "specified_subset_hypothesis_not_supported_at_frozen_thresholds"
        require(disposition == reported["disposition"], "Full endpoint disposition mismatch")
        model_rows.append({"evaluation_seed": result["evaluation_seed"], "task_ready": task_ready,
                           "hypotheses": hypothesis_states, "all_scales_distinguished": all(distinguished),
                           "numerical_controls_from_original_validator": numerical,
                           "disposition": disposition})

    require(len(rows) == 560 == saved["actual_interval_rows"], "Full 560-row family not reconstructed")
    supported = sum(m["disposition"] == "expected_cost_interchange_supported_at_declared_scope" for m in model_rows)
    require(supported == saved["supported_prespecified_replicates"], "Supported-layout count mismatch")
    require(supported == saved["diagnostic"]["calibration_complete_endpoint_layouts"], "Diagnostic support count mismatch")
    output = {"schema": "f15-nd01-independent-calibration-statistics-audit-v1", "passed": True,
              "checks": checks, "interval_rows_reconstructed": len(rows), "models": model_rows,
              "complete_endpoint_layouts": supported, "inputs": inputs,
              "scope": "Reconstructed all 560 interval rows and resulting statistical labels from saved sufficient statistics without importing experimental assessment, generating samples, fitting models, or selecting alignments. Numerical-control flags are carried from the original validator rather than independently recomputed here.",
              "reviewer": "ChatGPT (GPT-6 Astra Pro), independent nd01_protocol_audit sub-agent"}
    raw = (json.dumps(output, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()
    with args.out.open("xb") as handle:
        handle.write(raw)
    Path(str(args.out) + ".sha256").write_text(hashlib.sha256(raw).hexdigest() + "\n")
    print(json.dumps({"passed": True, "checks": checks, "interval_rows": len(rows),
                      "complete_endpoint_layouts": supported}))


if __name__ == "__main__":
    main()
