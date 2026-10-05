"""Descriptive F15 parameter/saved-statistic diagnostics, with no new samples.

Contributor: delegated ChatGPT (GPT-6 Astra Pro), F15 analysis audit.
Does not import experimental modules, train, evaluate a network, fit/select
alignments, or compute inferential intervals. Outputs are created exclusively.
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
RUN = ROOT / "v2/work_logs/F15_v1_run1"
OUTPUT_JSON = HERE / "model_diagnostics.json"
OUTPUT_MD = HERE / "model_diagnostics.md"
G = ("identity", "inv_eta", "inv_one_minus_eta", "inv_total_cost")
ARMS = ("aligned", "random", "permuted_concept", "shuffled_donor", "untrained")
STRATA = ("mixed_near", "mixed_far", "preserve_other", "equal_target", "scale_separating")
BOX = ((Fraction(-1), Fraction(1)), (Fraction(-1), Fraction(1)),
       (Fraction(1, 2), Fraction(2)), (Fraction(1, 2), Fraction(2)))
SUBSET_SPACE = math.comb(32, 8)
started_wall, started_cpu = time.perf_counter(), time.process_time()
if OUTPUT_JSON.exists() or OUTPUT_MD.exists():
    raise FileExistsError("Descriptive outputs already exist; preserved without overwrite.")
input_hashes = {}


def read(path, sidecar=False):
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    input_hashes[str(path.relative_to(ROOT))] = digest
    if sidecar and Path(str(path)+".sha256").read_text().strip() != digest:
        raise ValueError(f"Sidecar mismatch: {path}")
    return json.loads(data)


def canonical(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def rounded_outward(q, *, lower):
    result = float(q)
    if lower and Fraction(result) > q:
        return math.nextafter(result, -math.inf)
    if not lower and Fraction(result) < q:
        return math.nextafter(result, math.inf)
    return result


def sign_class(lower, upper):
    if upper <= 0:
        return "always_zero_after_relu"
    if lower > 0:
        return "strictly_active"
    if lower == 0:
        return "nonnegative_boundary"
    return "sign_switching"


def parameter_diagnostics(net):
    """Exact extrema of each stored affine neuron over the declared box.

    Fraction(float) treats each serialized binary64 coefficient as its exact
    rational value. No domain points or network predictions are generated.
    Extrema are sums of the four independent linear-coordinate extrema.
    """
    neurons = []
    for unit in range(32):
        weights = [Fraction(net["w"][axis][unit]) for axis in range(4)]
        bias = Fraction(net["b"][unit])
        lower = bias + sum(min(w*lo, w*hi) for w, (lo, hi) in zip(weights, BOX))
        upper = bias + sum(max(w*lo, w*hi) for w, (lo, hi) in zip(weights, BOX))
        hidden_lower, hidden_upper = max(Fraction(0), lower), max(Fraction(0), upper)
        neurons.append({"unit": unit, "preactivation_exact_lower": str(lower),
            "preactivation_exact_upper": str(upper),
            "preactivation_float_outward_lower": rounded_outward(lower, lower=True),
            "preactivation_float_outward_upper": rounded_outward(upper, lower=False),
            "relu_exact_lower": str(hidden_lower), "relu_exact_upper": str(hidden_upper),
            "class": sign_class(lower, upper), "output_weight": net["v"][unit],
            "output_weight_exact": str(Fraction(net["v"][unit]))})
    return {"classification_counts": dict(Counter(n["class"] for n in neurons)), "neurons": neurons}


def selected_status(subset, neurons):
    selected = [neurons[i] for i in subset]
    return {"subset": subset, "classification_counts": dict(Counter(n["class"] for n in selected)),
            "classes_by_unit": {str(n["unit"]): n["class"] for n in selected},
            "zero_output_weight_units": [n["unit"] for n in selected if n["output_weight"] == 0]}


# These hashes identify the source of the conventions; the script executes no
# code from the frozen modules. The contract supplies the domain and budgets.
config = read(ROOT / "v2/experiments/config.v1.json")
for name in ("neural.py", "protocol.md", "neural_design.md", "freeze.v1.json"):
    path = ROOT / "v2/experiments" / name
    input_hashes[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
if config["neural"]["width"] != 32 or config["neural"]["subset_size"] != 8:
    raise ValueError("Unexpected frozen coordinate space.")

models, search_rows, pool_sets, overlap_rows = [], [], {}, []
for index in range(5):
    prepared = read(RUN / f"preparation_attempt_1/model_{index}_prepared.json", True)
    evaluation = read(RUN / f"evaluation_attempt_1/model_{index}_evaluation.json", True)
    if canonical({k: v for k, v in prepared.items() if k != "artifact_hash"}) != prepared["artifact_hash"]:
        raise ValueError("Prepared internal artifact hash mismatch.")
    if evaluation["discovery_artifact_hash"] != prepared["artifact_hash"]:
        raise ValueError("Evaluation/preparation mismatch.")
    parameter_sets = {name: parameter_diagnostics(prepared[key])
                      for name, key in (("trained", "network"), ("untrained", "untrained_network"))}
    transition_counts = Counter((a["class"], b["class"]) for a, b in zip(
        parameter_sets["untrained"]["neurons"], parameter_sets["trained"]["neurons"]))
    models.append({"model_index": index, "discovery_seed": prepared["discovery_seed"],
        "evaluation_seed": evaluation["evaluation_seed"], "parameter_sets": parameter_sets,
        "activation_class_transitions": [{"from": a, "to": b, "units": count}
            for (a, b), count in sorted(transition_counts.items())],
        "selected_alternative_from_discovery": prepared["selected_alternative"]})
    for g in G:
        for arm in ARMS:
            name = f"{g}/{arm}"
            alignment = prepared["alignments"][name]
            network_kind = "untrained" if arm == "untrained" else "trained"
            neurons = parameter_sets[network_kind]["neurons"]
            for role in range(2):
                discovery = alignment["roles"][role]
                cells = evaluation["alignments"][name]["roles"][role]
                if len(discovery["candidate_pool"]) != 128 or any(cells[s]["n"] != 8192 for s in STRATA):
                    raise ValueError("Unexpected discovery/evaluation count.")
                pool = {tuple(s) for s in discovery["candidate_pool"]}
                pool_sets[index, g, arm, role] = pool
                final_mse = math.fsum(cells[s]["mse"] for s in STRATA)/5
                discovery_mse = discovery["selection_score"]["probability_mse"]
                search_rows.append({"model_index": index, "discovery_seed": prepared["discovery_seed"],
                    "evaluation_seed": evaluation["evaluation_seed"], "g": g, "arm": arm,
                    "role": role, "network_kind": network_kind,
                    "selected_discovery_probability_mse": discovery_mse,
                    "saved_final_equal_stratum_probability_mse": final_mse,
                    "final_minus_discovery_probability_mse": final_mse-discovery_mse,
                    "final_to_discovery_mse_ratio": None if discovery_mse == 0 else final_mse/discovery_mse,
                    "saved_final_equal_stratum_probability_mae": math.fsum(cells[s]["mae"] for s in STRATA)/5,
                    "discovery_pair_count": 640, "final_pair_count": 40960,
                    "candidate_draws": 128, "unique_candidate_subsets": len(pool),
                    "duplicate_candidate_draws": 128-len(pool),
                    "subset_space_size": SUBSET_SPACE,
                    "unique_subset_fraction_of_coordinate_space": len(pool)/SUBSET_SPACE,
                    "units_appearing_anywhere_in_pool": sorted({unit for subset in pool for unit in subset}),
                    "selected_candidate_index": discovery["selected_index"],
                    "selected_unit_status": selected_status(discovery["subset"], neurons)})
            overlap = sorted(set(alignment["roles"][0]["subset"]) & set(alignment["roles"][1]["subset"]))
            overlap_rows.append({"model_index": index, "g": g, "arm": arm, "network_kind": network_kind,
                "overlap": overlap, "overlap_size": len(overlap),
                "overlap_activation_counts": dict(Counter(neurons[u]["class"] for u in overlap)),
                "overlap_output_weights": {str(u): neurons[u]["output_weight"] for u in overlap},
                "saved_identity_composition": evaluation["composition"] if g == "identity" and arm == "aligned" else None})

group_summaries = []
for g in G:
    for arm in ARMS:
        rows = [r for r in search_rows if r["g"] == g and r["arm"] == arm]
        status_counts = Counter()
        for row in rows:
            status_counts.update(row["selected_unit_status"]["classification_counts"])
        group_summaries.append({"g": g, "arm": arm, "model_role_rows": len(rows),
            "mean_selected_discovery_mse": math.fsum(r["selected_discovery_probability_mse"] for r in rows)/len(rows),
            "mean_saved_final_mse": math.fsum(r["saved_final_equal_stratum_probability_mse"] for r in rows)/len(rows),
            "mean_final_minus_discovery_mse": math.fsum(r["final_minus_discovery_probability_mse"] for r in rows)/len(rows),
            "final_exceeds_discovery_rows": sum(r["final_minus_discovery_probability_mse"] > 0 for r in rows),
            "min_unique_candidates": min(r["unique_candidate_subsets"] for r in rows),
            "max_unique_candidates": max(r["unique_candidate_subsets"] for r in rows),
            "selected_slot_activation_counts": dict(status_counts)})

pool_overlap_summary = []
for model in range(5):
    for role in range(2):
        union = set().union(*(pool_sets[model, g, arm, role] for g in G for arm in ARMS))
        random_pool = pool_sets[model, "identity", "random", role]
        pool_overlap_summary.append({"model_index": model, "role": role,
            "candidate_draws_all_hypotheses_arms": 2560,
            "unique_subsets_all_hypotheses_arms": len(union),
            "union_fraction_of_coordinate_space": len(union)/SUBSET_SPACE,
            "random_pool_identical_across_hypotheses": all(pool_sets[model, g, "random", role] == random_pool for g in G),
            "aligned_and_incorrect_donor_pools_identical_by_hypothesis": {
                g: pool_sets[model, g, "aligned", role] == pool_sets[model, g, "shuffled_donor", role] for g in G}})

identity = [r for r in search_rows if r["g"] == "identity" and r["arm"] == "aligned"]
identity_overlap = [r for r in overlap_rows if r["g"] == "identity" and r["arm"] == "aligned"]
overall = {"model_count": 5, "neurons_with_exact_box_ranges": 320,
    "descriptive_search_rows": len(search_rows), "candidate_draws_all_models": sum(r["candidate_draws"] for r in search_rows),
    "unique_candidates_per_search_range": [min(r["unique_candidate_subsets"] for r in search_rows), max(r["unique_candidate_subsets"] for r in search_rows)],
    "duplicate_candidate_draws_all_searches": sum(r["duplicate_candidate_draws"] for r in search_rows),
    "all_search_rows_final_mse_exceeds_discovery": sum(r["final_minus_discovery_probability_mse"] > 0 for r in search_rows),
    "identity_aligned_rows_final_mse_exceeds_discovery": sum(r["final_minus_discovery_probability_mse"] > 0 for r in identity),
    "subset_space_size": SUBSET_SPACE,
    "single_pool_128_draw_maximum_coverage_percent": 100*128/SUBSET_SPACE,
    "union_pool_unique_subsets_per_model_role_range": [min(r["unique_subsets_all_hypotheses_arms"] for r in pool_overlap_summary), max(r["unique_subsets_all_hypotheses_arms"] for r in pool_overlap_summary)],
    "trained_activation_counts": dict(sum((Counter(m["parameter_sets"]["trained"]["classification_counts"]) for m in models), Counter())),
    "untrained_activation_counts": dict(sum((Counter(m["parameter_sets"]["untrained"]["classification_counts"]) for m in models), Counter()))}

output = {"schema": "f15-descriptive-saved-model-diagnostics-v1",
    "contributor": "delegated ChatGPT (GPT-6 Astra Pro), F15 analysis audit",
    "created_utc": datetime.now(timezone.utc).isoformat(), "python": sys.version,
    "input_sha256": input_hashes,
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "operations": {"parameter_functions": True, "saved_statistic_functions": True,
        "population_generation": False, "network_evaluation": False, "training": False,
        "fitting_or_alignment_selection": False, "new_inferential_intervals": False,
        "primary_output_modification": False, "F16": False},
    "input_box": [[str(a), str(b)] for a, b in BOX],
    "weight_convention": "hidden_j(x) = max(sum_axis x_axis*w[axis][j] + b[j], 0)",
    "exact_range_scope": "real affine functions with exact rational values of stored binary64 parameters on the closed declared input box; outward decimal displays enclose those exact endpoints, not a claim about every BLAS rounding path",
    "discovery_final_scope": "equal-stratum descriptive saved means for the discovery-selected subset; unequal sample sizes and discovery selection preclude causal attribution of any gap",
    "coverage_scope": "fraction of all C(32,8) coordinate subsets appearing in saved pools; not probability of finding a valid representation, coverage of all abstractions, or evidence that additional search would succeed",
    "summary": overall, "models": models, "search_rows": search_rows,
    "by_hypothesis_arm": group_summaries, "pool_overlap_summary": pool_overlap_summary,
    "selected_role_overlaps": overlap_rows,
    "compute_wall_seconds": time.perf_counter()-started_wall,
    "compute_cpu_seconds": time.process_time()-started_cpu,
    "additional_principal_engaged_minutes_claimed": 0}

md = ["# F15 descriptive saved-model diagnostics", "",
      "Contributor: **delegated ChatGPT (GPT-6 Astra Pro), F15 analysis audit**.", "",
      "These are parameter calculations and descriptive functions of already saved statistics. No input population, network prediction, training, decoder fit, alignment selection, additional confidence interval or F16 reconstruction was performed. The frozen primary conclusions are unchanged.", "",
      "The complete [machine record](model_diagnostics.json) includes exact rational neuron bounds, every search row, candidate coverage and input/script SHA256 hashes. The [script](model_diagnostics.py) uses only the Python standard library and preserves existing outputs by exclusive creation.", "",
      "## 1. Discovery-selected versus saved final MSE", "",
      "The selection score averages 640 discovery pairs per role; the saved final MSE below averages five equal strata of 8,192 pairs, totaling 40,960. Both concern the same discovery-selected subset. The following means average the ten fixed model/role rows descriptively; they are not new population estimates or confidence tests.", "",
      "| Hypothesis | Arm | Mean discovery MSE | Mean final MSE | Final > discovery, /10 |",
      "|---|---|---:|---:|---:|"]
for row in group_summaries:
    md.append(f"| {row['g']} | {row['arm']} | {row['mean_selected_discovery_mse']:.7f} | {row['mean_saved_final_mse']:.7f} | {row['final_exceeds_discovery_rows']} |")
md += ["", f"Across all 200 hypothesis/arm/model/role rows, final MSE exceeds selected discovery MSE in {overall['all_search_rows_final_mse_exceeds_discovery']} cases; identity-aligned does so in {overall['identity_aligned_rows_final_mse_exceeds_discovery']} of ten. The signs and sizes describe the saved run. They do not isolate discovery selection bias from finite-sample composition, identify the cause of unsupported intervention criteria, or justify additional fitting.", "",
       "## 2. Actual candidate-pool coverage", "",
       f"The declared coordinate-subset space has **{SUBSET_SPACE:,}** elements. A unique 128-candidate pool covers **{100*128/SUBSET_SPACE:.6f}%** of that space. Saved pools contain {overall['unique_candidates_per_search_range'][0]}–{overall['unique_candidates_per_search_range'][1]} unique subsets; {overall['duplicate_candidate_draws_all_searches']} duplicate draws appear across the 25,600 charged candidate evaluations. Duplicate draws still consumed their frozen budget.", "",
       f"The union across all four hypotheses and five arms contains {overall['union_pool_unique_subsets_per_model_role_range'][0]}–{overall['union_pool_unique_subsets_per_model_role_range'][1]} distinct subsets per fixed model/role, from 2,560 charged proposals. Random pools are identical across hypotheses for the same model/role. Aligned and incorrect-donor pools are also identical within each hypothesis/model/role; their scoring donors differ. Shared pools support matched comparisons and should not be mistaken for independent exploration.", "",
       "These fractions measure saved coordinate coverage only. They do not estimate the chance of a valid representation, establish search insufficiency as the cause of the result, or show that a larger search would succeed. Many different subsets could be redundant or equally poor.", "",
       "## 3. Exact preactivation ranges from stored parameters", "",
       "The frozen [input generator and MLP convention](../../experiments/neural.py) use raw inputs `(x1,x2,cFN,cFP)` on `[-1,1]² × [1/2,2]²`, a `4 × 32` input-weight array, and `h_j=max(sum_i x_i*w_ij+b_j,0)`. The [design](../../experiments/neural_design.md) explains the affine-output restriction. For each neuron, summing each coefficient's two endpoint products gives the exact affine minimum/maximum on this box. The calculation treats every stored binary64 coefficient as an exact rational number; displayed float endpoints round outward. It makes no claim about every implementation's final-bit BLAS rounding.", "",
       "`Always zero` means the upper preactivation bound is nonpositive; `strictly active` means its lower bound is positive; `sign switching` means the interval spans zero. These are parameter properties over the full box, not empirical activation frequencies.", "",
       "| Model seed | Network | Always zero | Strictly active | Sign switching | Boundary nonnegative |",
       "|---|---|---:|---:|---:|---:|"]
for model in models:
    for network in ("untrained", "trained"):
        counts = model["parameter_sets"][network]["classification_counts"]
        md.append(f"| {model['discovery_seed']} | {network} | {counts.get('always_zero_after_relu',0)} | {counts.get('strictly_active',0)} | {counts.get('sign_switching',0)} | {counts.get('nonnegative_boundary',0)} |")
md += ["", "### Identity-aligned selected coordinates", "",
       "| Evaluation seed | Role | Selected always-zero units | Selected strictly-active units | Selected sign-switching units |",
       "|---|---:|---:|---:|---:|"]
for row in identity:
    counts = row["selected_unit_status"]["classification_counts"]
    md.append(f"| {row['evaluation_seed']} | {row['role']} | {counts.get('always_zero_after_relu',0)} | {counts.get('strictly_active',0)} | {counts.get('sign_switching',0)} |")
md += ["", "Each role retains exactly eight coordinate slots, but a slot need not contribute a varying hidden feature throughout the declared domain. Always-zero units are constant in this stored mathematical network; strictly-active units contribute affine functions. Neither fact identifies cost semantics, establishes which units ordinary task behavior needs, or explains a final-error difference by itself. Every hypothesis/control's selected-unit classes and output weights are retained in JSON.", "",
       "## 4. Selected-role overlaps", "",
       "| Model seed | Identity overlap units | Overlap activation classes | Saved maximum composition-order probability difference |",
       "|---|---|---|---:|"]
for row in identity_overlap:
    md.append(f"| {1500401+row['model_index']} | {', '.join(map(str,row['overlap'])) or 'none'} | {json.dumps(row['overlap_activation_counts'],sort_keys=True)} | {row['saved_identity_composition']['order_probability_max_difference']:.9f} |")
md += ["", "Overlap count alone is not an effect-size measure: activation ranges and output coefficients also matter. The composition figures here are copied from the frozen secondary diagnostic, with no new intervention. They retain the distinction between separate role relations and joint independently composable variables.", "",
       "## Interpretation and accounting", "",
       "These diagnostics make the saved models and finite search easier to inspect. They do not attribute the unsupported full neural criterion to optimization, capacity, inactive neurons, search coverage or discovery selection. Those explanations remain possible follow-up questions requiring a separately authorized experiment. The primary report's ordinary-learning, support-versus-falsification, control and scale dispositions remain unchanged.", "",
       "This work is overlapping delegated F15 analysis, with zero additional principal engaged minutes claimed. Output files were created exclusively; exact input hashes and measured script compute time are in the JSON record.", ""]

with OUTPUT_JSON.open("x") as handle:
    json.dump(output, handle, indent=2, sort_keys=True, allow_nan=False)
    handle.write("\n")
with OUTPUT_MD.open("x") as handle:
    handle.write("\n".join(md))
print(json.dumps({"outputs": [str(OUTPUT_JSON.relative_to(ROOT)), str(OUTPUT_MD.relative_to(ROOT))],
                  "sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (OUTPUT_JSON, OUTPUT_MD)},
                  "summary": overall}, indent=2))
