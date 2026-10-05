"""Saved-only F15 auxiliary metrics and resource accounting.

Contributor: ChatGPT (GPT-6 Astra Pro). Every statistic is copied from or
descriptively aggregated over saved records. No generators, networks,
decoders, search, new intervals or experimental modules are invoked.
"""
from collections import defaultdict
import hashlib
import json
import math
from pathlib import Path
import statistics
import sys


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
RUN = ROOT / "v2/work_logs/F15_v1_run1"
G = ("identity", "inv_eta", "inv_one_minus_eta", "inv_total_cost")
ARMS = ("aligned", "random", "permuted_concept", "shuffled_donor", "untrained")
STRATA = ("mixed_near", "mixed_far", "preserve_other", "equal_target", "scale_separating")
inputs = []


def read(path):
    raw = path.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    assert Path(str(path) + ".sha256").read_text().strip() == sha
    inputs.append({"path": str(path.relative_to(ROOT)), "bytes": len(raw), "sha256": sha})
    return json.loads(raw)


def stats(values):
    values = list(values)
    return {"n": len(values), "mean": statistics.mean(values),
            "minimum": min(values), "maximum": max(values)}


def weighted_mean(rows, value):
    return sum(r["n"] * value(r) for r in rows) / sum(r["n"] for r in rows)


def main():
    prepared = [read(RUN / f"preparation_attempt_1/model_{i}_prepared.json") for i in range(5)]
    evaluated = [read(RUN / f"evaluation_attempt_1/model_{i}_evaluation.json") for i in range(5)]
    assessment = read(RUN / "evaluation_attempt_1/neural_assessment.json")
    assert len(assessment["models"]) == 5
    groups = []
    decoder_groups = []
    for g in G:
        for arm in ARMS:
            name = f"{g}/{arm}"
            # Observational decoder and log-contribution values belong to the
            # task population, once per model/role, not once per stratum.
            decoder_groups.append({
                "alignment": name,
                "task_population_model_roles": 10,
                "observational_decoder_nrmse": stats(x["alignments"][name]["observational_decoder_nrmse"][role]
                                                       for x in evaluated for role in range(2)),
                "log_contribution_rmse": stats(x["alignments"][name]["log_contribution_rmse"][role]
                                               for x in evaluated for role in range(2)),
                "scope": "mean/range of ten model-role scores; differing normalizers prevent a pooled NRMSE interpretation",
            })
            for stratum in STRATA:
                rows = [x["alignments"][name]["roles"][role][stratum]
                        for x in evaluated for role in range(2)]
                assert len(rows) == 10 and all(r["n"] == 8192 for r in rows)
                row = {"alignment": name, "stratum": stratum, "model_roles": len(rows),
                       "descriptive_total_pair_records": sum(r["n"] for r in rows),
                       "scope": "equal-weight description of the ten fixed model-role populations, not a new confirmatory population or CI",
                       "intervention_mae": weighted_mean(rows, lambda r: r["mae"]),
                       "intervention_rmse": math.sqrt(weighted_mean(rows, lambda r: r["mse"])),
                       "no_swap_mae": weighted_mean(rows, lambda r: r["no_swap"]["mae"]),
                       "whole_layer_swap_mae": weighted_mean(rows, lambda r: r["whole_layer_swap"]["mae"]),
                       "adjusted_effect_rmse": math.sqrt(weighted_mean(rows, lambda r: r["adjusted_effect_rmse"] ** 2)),
                       "expected_effect_rms": math.sqrt(weighted_mean(rows, lambda r: r["expected_effect_rms"] ** 2)),
                       "observed_effect_rms": math.sqrt(weighted_mean(rows, lambda r: r["observed_effect_rms"] ** 2)),
                       "target_decoder_nrmse_scores": stats(r["target_decoder_nrmse"] for r in rows),
                       "untouched_decoder_nrmse_scores": stats(r["untouched_decoder_nrmse"] for r in rows),
                       "selected_mae_lower_than_no_swap_cells": sum(r["mae"] < r["no_swap"]["mae"] for r in rows),
                       "selected_mae_lower_than_whole_layer_cells": sum(r["mae"] < r["whole_layer_swap"]["mae"] for r in rows),
                       "same_model_role_effect_ranges": stats(r["observed_effect_rms"] for r in rows)}
                groups.append(row)
    generation = []
    for i, (prep, result) in enumerate(zip(prepared, evaluated)):
        assert prep["discovery_seed"] == 1500401 + i and result["evaluation_seed"] == 1500491 + i
        for stage, record, intended_name, count in (
            ("discovery", prep, "selection_pair_generation", 128),
            ("evaluation", result, "pair_generation", 8192),
        ):
            for kind, key in (("intended", intended_name), ("incorrect_donor", "wrong_donor_generation")):
                for role in range(2):
                    for stratum in STRATA:
                        r = record[key][role][stratum]
                        assert r["accepted"] == count and r["proposals_generated"] % 4096 == 0
                        assert count <= r["proposals_generated"] <= 4000 * count
                        generation.append({"model": i, "stage": stage, "stream_kind": kind,
                                           "role": role, "stratum": stratum, **r})
    generation_groups = []
    for stage in ("discovery", "evaluation"):
        for kind in ("intended", "incorrect_donor"):
            for stratum in STRATA:
                cells = [r for r in generation if r["stage"] == stage and r["stream_kind"] == kind and r["stratum"] == stratum]
                generated = sum(r["proposals_generated"] for r in cells)
                accepted = sum(r["accepted"] for r in cells)
                generation_groups.append({"stage": stage, "stream_kind": kind, "stratum": stratum,
                                          "stream_count": len(cells), "proposals_generated": generated,
                                          "retained_pairs": accepted, "retained_per_generated": accepted / generated,
                                          "scope": "batch-generated proposals include unused tail candidates; this is not the rejection-test acceptance probability"})
    resources = [{"model": i, "training": p["training"], "preparation_inclusive": p["resource"],
                  "evaluation_inclusive": r["resource"],
                  "discovery_only_wall_by_subtraction": p["resource"]["wall_seconds"] - p["training"]["wall_seconds"],
                  "discovery_only_cpu_by_subtraction": p["resource"]["cpu_seconds"] - p["training"]["cpu_seconds"]}
                 for i, (p, r) in enumerate(zip(prepared, evaluated))]
    witness = [r["unused_duplicate_witness"] for r in evaluated]
    assert all(w == witness[0] for w in witness)
    adjusted = [{"model": i, "hypothesis": g, "role": role,
                 "derived_adjusted_effect_mae_upper": assessment["models"][i]["hypotheses"][g]["roles"][role]["derived_adjusted_effect_mae_upper"]}
                for i in range(5) for g in G for role in range(2)]
    output = {
        "schema": "F15-saved-neural-auxiliary-v1", "contributor": "ChatGPT (GPT-6 Astra Pro)",
        "new_population_generation": False, "new_confirmatory_intervals": 0,
        "primary_support_dispositions_changed": False,
        "intervention_diagnostic_groups": groups,
        "observational_diagnostic_groups": decoder_groups,
        "generation_records": generation,
        "generation_groups": generation_groups,
        "model_resources": resources,
        "resource_scope": "Prepared resource wall/CPU already includes training; do not add nested training twice. Evaluation pair counts exclude additional gauge/diagnostic forwards, whose compute is included in inclusive wall/CPU without exhaustive separate forward counters.",
        "same_constructed_unused_duplicate_witness": witness[0],
        "constructed_witness_occurrences": 5,
        "independent_learned_witness_count": 0,
        "derived_adjusted_effect_bounds": adjusted,
        "task_rows": [{"model": i, "evaluation_seed": r["evaluation_seed"], **r["task"]} for i, r in enumerate(evaluated)],
        "input_manifest": inputs,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    path = HERE / "neural_auxiliary_summary.json"
    raw = (json.dumps(output, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()
    if "--check" in sys.argv:
        assert path.read_bytes() == raw
    else:
        with path.open("xb") as handle:
            handle.write(raw)
        with Path(str(path) + ".sha256").open("x") as handle:
            handle.write(hashlib.sha256(raw).hexdigest() + "\n")
    print(json.dumps({"output": str(path.relative_to(ROOT)), "bytes": len(raw),
                      "sha256": hashlib.sha256(raw).hexdigest(), "diagnostic_groups": len(groups),
                      "generation_records": len(generation)}))


if __name__ == "__main__":
    main()
