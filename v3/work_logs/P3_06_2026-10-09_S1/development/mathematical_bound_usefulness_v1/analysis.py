"""Post hoc finite-bound analysis of immutable P3-06 development v1 records.

No forecaster is run, no inputs are generated, no method is tuned. Fractions
reconstruct reported metrics, per-copy potential terms, and elementary bounds.
Also records the v1->v2 resource correction and v3 receipt-repair equivalence.
Contributor: ChatGPT (GPT-6 Astra Pro), October 9, 2026 UTC.
"""
from fractions import Fraction as F
import hashlib
import json
from math import isqrt
from pathlib import Path
import traceback


HERE = Path(__file__).resolve()
BASE = HERE.parents[1]
OUT = HERE.parent
V1, V2, V3 = (BASE / ("mathematical_queries_v" + str(i)) for i in (1, 2, 3))
METHODS = ("scalar_without_decision", "scalar_with_decision")
EXPERTS = ("constant_half", "residue_frequency", "partial_exact_shortcut", "fallible_parity")


def encoded(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): encoded(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [encoded(v) for v in value]
    return value


def dump(path, value):
    path.write_text(json.dumps(encoded(value), sort_keys=True, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text())


def interval_sqrt(value, bits=32):
    numerator = value.numerator << (2 * bits)
    denominator = value.denominator
    root = isqrt(numerator // denominator)
    lower = F(root, 1 << bits)
    upper = lower if root * root * denominator == numerator else F(root + 1, 1 << bits)
    assert lower * lower <= value <= upper * upper
    return lower, upper


def verify_run(directory, archive=False):
    manifest = load(directory / "manifest.json")
    assert manifest["status"] == "completed"
    for name, expected in manifest["artifacts_sha256"].items():
        assert sha(directory / name) == expected, name
    for name, expected in manifest["source_sha256"].items():
        path = directory / "source_snapshot" / name if archive else HERE.parents[5] / name
        assert sha(path) == expected, str(path)
    return manifest


def report_projection(record):
    return {key: record[key] for key in ("query", "tick", "scheduled_admission_tick", "weight",
            "actions", "experts", "outcome", "admission_tick", "status")} | {
        "reports": {name: {k: v for k, v in report.items() if k != "detail"}
                    for name, report in record["reports"].items()}}


def correction_case(old, peak, repaired):
    assert old["records"] == peak["records"]
    assert old["metrics"] == peak["metrics"] == repaired["metrics"]
    assert old["core_audits"] == peak["core_audits"] == repaired["core_audits"]
    assert [report_projection(r) for r in old["records"]] == [report_projection(r) for r in repaired["records"]]
    rows = []
    for method in METHODS:
        previous = old["resource_counters"][method]["max_state_fraction_bits"]
        current = peak["resource_counters"][method]
        assert previous == current["final_accumulator_max_fraction_bits"]
        running = 0
        trace = peak["state_fraction_bit_observations"][method]
        for observation in trace:
            bits = max([observation["settings"], observation["retained_report_max"]]
                       + [n for copy in observation["copies"] for key, n in copy.items() if key != "copy"])
            running = max(running, bits)
            assert bits == observation["current_state_max_fraction_bits"]
            assert running == observation["peak_state_max_fraction_bits"]
        assert running == current["peak_state_max_fraction_bits"]
        assert running == repaired["resource_counters"][method]["peak_state_max_fraction_bits"]
        first_peak = next(o for o in trace if o["peak_state_max_fraction_bits"] == running)
        rows.append({"case": old["case"], "method": method,
            "v1_misnamed_max_state_fraction_bits": previous,
            "v2_final_accumulator_max_fraction_bits": current["final_accumulator_max_fraction_bits"],
            "v2_final_state_max_fraction_bits": current["final_state_max_fraction_bits"],
            "v2_and_v3_peak_state_max_fraction_bits": running,
            "observations": len(trace), "first_peak_phase": first_peak["phase"],
            "first_peak_tick": first_peak["tick"], "first_peak_query_id": first_peak["query_id"]})
    assert all(p["evidence_and_cores_unchanged"] for p in repaired["rejected_receipts"])
    return rows


def analyze(data, method):
    audit = data["core_audits"][method]
    pool = audit["pool"]
    saved = data["metrics"][method]["all_admitted"]
    h = F(audit["certified_calibration_absolute_residual_upper"])
    copies = [{"copy": i, "settled": 0, "pending": 0, "weight": F(0),
               "variance": F(0), "allowance": F(0)} for i in range(pool["copies"])]
    brier, weight, unknown_weight, mixed, hard = (F(0) for _ in range(5))
    expert_losses = {name: F(0) for name in EXPERTS}
    expert_distances = {name: F(0) for name in EXPERTS}
    brier_envelopes = {name: F(0) for name in EXPERTS}
    fixed, action_envelopes, forecast_gaps = ([F(0), F(0)] for _ in range(3))
    table_range = F(0)
    negative, positive, masses, residuals = ([F(0)] * 5 for _ in range(4))
    for record in data["records"]:
        report = record["reports"][method]
        detail = report["detail"]
        if record["outcome"] is None:
            if "copy" in detail:
                copies[detail["copy"]]["pending"] += 1
            continue
        p, s, w, y = F(report["probability"]), F(report["action_one_probability"]), F(record["weight"]), record["outcome"]
        known = record["status"] == "known_at_issue"
        if known:
            assert p == y
            assert all(F(q) == y for q in record["experts"].values())
        allowed = (y,) if known else (0, 1)
        weight += w
        brier += w * (p - y) ** 2
        if not known:
            unknown_weight += w
            pred = detail["core_prediction"]
            copy = copies[detail["copy"]]
            copy["settled"] += 1
            copy["weight"] += w
            copy["variance"] += p * (1 - p) * sum((F(x) ** 2 for x in pred["features"]), F(0))
            copy["allowance"] += F(pred["allowance"])
        for name in EXPERTS:
            q = F(record["experts"][name])
            expert_losses[name] += w * (q - y) ** 2
            expert_distances[name] += w * (q - p) ** 2
            brier_envelopes[name] += w * max((p - z) ** 2 - (q - z) ** 2 for z in allowed)
        rows = [[F(x) for x in row] for row in record["actions"]["rows"]]
        forecast_costs = [(1 - p) * row[0] + p * row[1] for row in rows]
        forecast_mix = (1 - s) * forecast_costs[0] + s * forecast_costs[1]
        mixed += w * ((1 - s) * rows[0][y] + s * rows[1][y])
        hard += w * rows[report["hard_action"]][y]
        for i in (0, 1):
            fixed[i] += w * rows[i][y]
            forecast_gaps[i] += w * (forecast_mix - forecast_costs[i])
            action_envelopes[i] += w * max((1 - s) * rows[0][z] + s * rows[1][z] - rows[i][z] for z in allowed)
        table_range += w * max(abs(rows[0][z] - rows[1][z]) for z in allowed)
        for j in range(5):
            tent = max(F(0), 1 - abs(4 * p - j))
            masses[j] += w * tent
            residuals[j] += w * tent * (y - p)
            if not known:
                negative[j] += w * tent * p
                positive[j] += w * tent * (1 - p)
    assert weight == F(saved["settled_weight"])
    assert unknown_weight == F(pool["settled_weight"])
    assert brier == F(saved["task_weighted_brier"])
    assert mixed == F(saved["mixed_action_loss"])
    assert hard == F(saved["hard_action_loss"])
    assert expert_losses == {k: F(v) for k, v in saved["expert_brier"].items()}
    assert fixed == list(map(F, saved["fixed_action_losses"]))
    assert masses == list(map(F, saved["calibration_bin_masses"]))
    assert residuals == list(map(F, saved["calibration_bin_residuals"]))
    for copy in copies:
        copy["bound"] = copy["variance"] + copy["allowance"]
        assert copy["bound"] == F(pool["copy_bounds"][copy["copy"]])
        copy["sqrt_lower"], copy["sqrt_upper"] = interval_sqrt(copy["bound"])
    h_lower = sum((c["sqrt_lower"] for c in copies), F(0))
    h_upper = sum((c["sqrt_upper"] for c in copies), F(0))
    assert h_upper == F(pool["sum_sqrt_upper"])
    assert h == h_upper  # True on this finite tape, not asserted for every core audit.
    allowance = sum((c["allowance"] for c in copies), F(0))
    variance = sum((c["variance"] for c in copies), F(0))
    assert allowance == F(audit["settled_root_allowance"])
    positive_copies = sum(c["bound"] > 0 for c in copies)
    assert positive_copies == pool["positive_bound_copies"]
    best = min(EXPERTS, key=lambda name: expert_losses[name])
    brier_bound = F(audit["certified_brier_regret_upper"])
    assert brier_bound == 2 * h
    for name in EXPERTS:
        actual = brier - expert_losses[name]
        assert actual <= brier_envelopes[name]
        assert actual <= brier_bound - expert_distances[name]
    action_bound = None if audit["certified_mixed_action_regret_upper"] is None else F(audit["certified_mixed_action_regret_upper"])
    gap_bound = None
    if action_bound is not None:
        slack = F(pool["smoothing_slack"])
        assert action_bound == slack + h
        assert max(forecast_gaps) <= slack
        for i in (0, 1):
            assert mixed - fixed[i] == forecast_gaps[i] + F(pool["residual"][-2 + i])
            assert mixed - fixed[i] <= h + forecast_gaps[i]
        gap_bound = h + max(forecast_gaps)
    bins = []
    for j in range(5):
        elementary = max(negative[j], positive[j])
        assert abs(residuals[j]) <= elementary <= masses[j]
        assert abs(residuals[j]) <= h
        bins.append({"bin": j, "mass": masses[j], "actual_residual": residuals[j],
            "trivial_mass_bound": masses[j], "trivial_forecast_range_bound": elementary,
            "potential_bound": h, "combined_available_bound": min(h, elementary),
            "potential_improves_mass_bound": h < masses[j],
            "potential_improves_forecast_range_bound": h < elementary,
            "actual_normalized_residual": residuals[j] / masses[j] if masses[j] else None,
            "potential_normalized_bound": h / masses[j] if masses[j] else None,
            "elementary_normalized_bound": elementary / masses[j] if masses[j] else None})
    return {"case": data["case"], "method": method,
        "settled_weight": weight, "unknown_settled_weight": unknown_weight,
        "created_copies": len(copies), "copies_with_settlements": sum(c["settled"] > 0 for c in copies),
        "positive_bound_copies": positive_copies, "copy_terms": copies,
        "H_exact_dyadic_enclosure": [h_lower, h_upper], "H_certificate_used": h,
        "settled_variance_total": variance, "settled_allowance_total": allowance,
        "allowance_fraction_of_sum_copy_bounds": allowance / (variance + allowance),
        "pending_reported_allowance_excluded": F(audit["pending_reported_allowance"]),
        "brier": {"actual_regret_best_expert": brier - expert_losses[best], "actual_best_expert": best,
            "reported_bound": brier_bound, "coarse_unknown_weight_bound": unknown_weight,
            "elementary_envelope_each_expert": brier_envelopes,
            "elementary_envelope_all_fixed_experts": max(brier_envelopes.values()),
            "elementary_envelope_retrospective_best_expert": brier_envelopes[best],
            "expert_distances": expert_distances,
            "distance_retained_bound_each_expert": {name: brier_bound - expert_distances[name] for name in EXPERTS},
            "distance_retained_bound_all_fixed_experts": brier_bound - min(expert_distances.values()),
            "distance_retained_bound_retrospective_best_expert": brier_bound - expert_distances[best],
            "reported_improves_coarse_bound": brier_bound < unknown_weight,
            "reported_improves_uniform_envelope": brier_bound < max(brier_envelopes.values()),
            "reported_improves_retrospective_best_envelope": brier_bound < brier_envelopes[best],
            "distance_retained_improves_retrospective_best_envelope": brier_bound - expert_distances[best] < brier_envelopes[best]},
        "actions": {"actual_mixed_regret_best_fixed_action": mixed - min(fixed),
            "actual_hard_regret_best_fixed_action": hard - min(fixed),
            "reported_mixed_bound": action_bound, "coarse_table_range_bound": table_range,
            "elementary_envelope_each_fixed_action": action_envelopes,
            "elementary_envelope_best_fixed_action": max(action_envelopes),
            "forecast_gap_each_fixed_action": forecast_gaps,
            "forecast_gap_retained_mixed_bound": gap_bound,
            "reported_improves_elementary_envelope": action_bound < max(action_envelopes) if action_bound is not None else None,
            "hard_decision_potential_bound": None},
        "calibration": {"bins": bins, "populated_bins": sum(m > 0 for m in masses),
            "potential_improves_mass_count": sum(h < m for m in masses),
            "potential_improves_elementary_count": sum(b["potential_improves_forecast_range_bound"] for b in bins),
            "H_per_total_weight": h / weight,
            "elementary_max_residual_per_total_weight": max(b["trivial_forecast_range_bound"] for b in bins) / weight,
            "actual_max_absolute_residual_per_total_weight": max(map(abs, residuals)) / weight}}


def num(value, digits=3):
    return "—" if value is None else f"{float(value):.{digits}f}"


def markdown(rows, corrections):
    text = r"""# P3-06 finite bound usefulness and resource correction

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 9, 2026 UTC.

## What this analysis establishes

The saved certificates are mathematically valid on the enumerated records, but
their finite usefulness depends on the comparator and denominator. Every
reported Brier bound beats the coarse total-unknown-weight bound. Three of the
four decision-feature Brier bounds fail to improve an elementary bound obtained
from the actual issued expert forecasts. The decision-feature calibration bound
adds no improvement over elementary bin bounds in the delayed and varying-stake
cases. The mixed-action certificates do improve their elementary action bounds
in all four cases. None of those comparisons establishes predictive superiority.

This analysis reads [v1 records](../mathematical_queries_v1/REPORT.md); it does
not run or tune a learner. It reconstructs scores and per-copy potential terms
with exact rational arithmetic. The public synthetic generator, small declared
expert library, and availability of cheap ordinary exact computation retain
their original limitations. Results for matched ordinary K29 adapters coincide
and are not duplicated in the tables.

## Comparisons and interpretation

Let $`I`$ denote admitted unknown-at-issue records, and include cache-at-issue
records in the full score set. For each cached record this analysis checks
$`p_t=y_t`$ and exact expert reports. Their Brier loss and calibration residual
are zero. Let $`W_u=\sum_{t\in I}w_t`$ and let $`H`$ be the sum of square roots
of the settled per-copy potential bounds. The rational upper enclosure actually
reported is used in all numerical comparisons below. The
[existing derivation](../../../../derivations/06_cost_forecast_refinement.md)
supplies the potential and regret identities; this note does not change it.

The coarse Brier regret bound is $`W_u`$. A sharper elementary comparator-specific
bound uses the issued forecasts alone:

```math
T_i^{\mathrm{B}}=\sum_t w_t\max_{y\in Y_t}
       \bigl((p_t-y)^2-(q_{t,i}-y)^2\bigr),\qquad
L-L_i\le T_i^{\mathrm{B}}.
```

Here $`Y_t=\{y_t\}`$ for a checked answer already known at issue and
$`Y_t=\{0,1\}`$ otherwise. Consequently $`\max_i T_i^{\mathrm{B}}`$ bounds regret
to the best fixed expert. The smaller bound for the particular observed best
expert is also reported, with that expert named retrospectively. This does not
identify the best expert in advance. Neither maximization claims that all
roundwise worst outcomes are jointly realizable by this mathematical generator.
Each inequality holds on the realized adaptive tape.

The recorded generic Brier certificate is $`2H`$. Retaining the already established
distance term gives $`2H-D_i`$, where
$`D_i=\sum_t w_t(q_{t,i}-p_t)^2`$. This is a sharper reading of the same saved
identity, without a new run. It is useful to distinguish the universal
fixed-comparator statement from a bound for the expert that happened to win.

For actions, write $`\bar c_t(y)=(1-s_t)c_{t,0}(y)+s_tc_{t,1}(y)`$. The
elementary envelope is

```math
T_i^{\mathrm{A}}=\sum_t w_t\max_{y\in Y_t}
                  (\bar c_t(y)-c_{t,i}(y)).
```

Then $`\max_iT_i^{\mathrm{A}}`$ bounds regret to the best fixed action. This
is at least as strong as using the sum of maximum row differences. The
decision-feature certificate is $`H+\sum_{t\in I}w_t\eta_t/8`$. Retaining actual
forecast gaps $`G_i=\sum_t w_t(\bar C_t(p_t)-C_{t,i}(p_t))`$ sharpens it to
$`H+\max_iG_i`$. The known-cache records have zero residual and nonpositive
forecast gaps. No action certificate is inferred for the mode without decision
features, and no mixed-action certificate is assigned to hard rounded actions.

For tent $`h_j`$, let $`M_j=\sum_t w_th_j(p_t)`$ include all scored records.
The elementary calibration bound is

```math
|E_j|\le T_j^{\mathrm{C}}
 =\max\left\{\sum_{t\in I}w_th_j(p_t)p_t,
             \sum_{t\in I}w_th_j(p_t)(1-p_t)\right\}\le M_j.
```

Exact cache reports are essential for their omitted numerator contribution.
The certificate $`|E_j|\le H`$ only improves this elementary bound when
$`H<T_j^{\mathrm{C}}`$. Conditional calibration divides by $`M_j`$, not by total
weight. Empty bins have zero residual and no conditional ratio. A populated
bin consisting only of known exact answers already has elementary bound zero.
The inequalities were independently checked by the same-model proof reviewer;
the arithmetic in this artifact is implementation-author analysis.

## Settled copies and root allowances

| Case / mode | Created / settled / positive-bound copies | Unknown weight | H | Actual allowance | Allowance / sum B |
|---|---:|---:|---:|---:|---:|
"""
    for r in rows:
        text += f"| {r['case']} / {r['method']} | {r['created_copies']} / {r['copies_with_settlements']} / {r['positive_bound_copies']} | {num(r['unknown_settled_weight'])} | {num(r['H_certificate_used'])} | {num(r['settled_allowance_total'],6)} | {num(100*r['allowance_fraction_of_sum_copy_bounds'],6)}% |\n"
    text += """
The delayed run creates eight copies. Four contain admitted feedback and four
contain only pending forecasts at this boundary. Only the first four contribute
positive settled potential. Their individual variance, allowance, bounds and
square-root enclosures are in `analysis.json`. All eight pending queries remain
excluded from scores and settled potential; their issue-time allowances are
retained separately. The allowance fractions show that feature variance, rather
than insufficient root accuracy, dominates these finite bound sizes. These
figures do not license setting a nonzero actual allowance to zero.

## Brier nonvacuity

| Case / mode | Actual best-expert regret | Reported 2H | Coarse W_u | Elementary, all fixed experts | Elementary, observed best | 2H−D, observed best |
|---|---:|---:|---:|---:|---:|---:|
"""
    for r in rows:
        b = r["brier"]
        text += f"| {r['case']} / {r['method']} | {num(b['actual_regret_best_expert'])} | {num(b['reported_bound'])} | {num(b['coarse_unknown_weight_bound'])} | {num(b['elementary_envelope_all_fixed_experts'])} | {num(b['elementary_envelope_retrospective_best_expert'])} | {num(b['distance_retained_bound_retrospective_best_expert'])} |\n"
    text += """
The plain scalar's generic bound improves the uniform elementary envelope in
all four cases; the decision scalar does so only in the shortcut case. Against
the envelope for the actual winning expert, none of the unsharpened `2H`
bounds improves it. Retaining the distance term gives such an improvement for
the plain scalar on the null and delayed cases. The elementary bound against
an endpoint-valued exact shortcut equals the actual squared loss on the
shortcut family, so the potential certificate cannot sharpen that particular
comparison. This is not evidence that the potential inequality is incorrect.

## Mixed actions and hard decisions

| Case | Actual mixed regret | H + smoothing slack | Elementary action envelope | H + observed forecast gap | Actual hard regret |
|---|---:|---:|---:|---:|---:|
"""
    for r in rows:
        if r["method"] != "scalar_with_decision":
            continue
        a = r["actions"]
        text += f"| {r['case']} | {num(a['actual_mixed_regret_best_fixed_action'])} | {num(a['reported_mixed_bound'])} | {num(a['elementary_envelope_best_fixed_action'])} | {num(a['forecast_gap_retained_mixed_bound'])} | {num(a['actual_hard_regret_best_fixed_action'])} |\n"
    text += """
Every displayed mixed-action certificate improves the corresponding elementary
action envelope. In the shortcut case the retained-gap bound is negative: this
particular certificate establishes an advantage over both fixed action indices
on the admitted tape. It compares fixed indices across changing loss tables,
not an outcome-aware optimal action or the competing adaptive methods. The
plain scalar, AA and ordinary exact baseline still have better observed action
performance in these runs. Positive delayed mixed regret and negative shortcut
regret are both compatible with the one-sided theorem. Hard-action observations
remain separate; their proximity to mixed losses does not transfer a guarantee.

## Calibration denominators

| Case / mode | H / total weight | Actual max residual / total weight | Populated bins | H improves mass bound | H improves elementary forecast-range bound |
|---|---:|---:|---:|---:|---:|
"""
    for r in rows:
        c = r["calibration"]
        text += f"| {r['case']} / {r['method']} | {num(c['H_per_total_weight'],6)} | {num(c['actual_max_absolute_residual_per_total_weight'],6)} | {c['populated_bins']} | {c['potential_improves_mass_count']} | {c['potential_improves_elementary_count']} |\n"
    text += """
Total-weight normalization alone can make a correct bound look useful even
when it says nothing new about any conditional bin. In particular, the delayed
and varying-stake decision-feature bounds do not improve a single elementary
bin bound. Other cases improve some bins and not others. `analysis.json` gives
every exact mass, residual, elementary bound, potential bound, and conditional
ratio, including zero-mass/known-only cases. The valid combined bound is the
minimum of the elementary and potential bounds; it never needs to be weakened
to the larger one for presentation.

## Resource-metric correction and receipt repair

Version 1's `max_state_fraction_bits` measured final accumulators, not a peak.
Its script and core are byte-preserved under
`../mathematical_queries_v1/source_snapshot/v3/checks/`. Version 2 retains the
v1 generation identifier and measures state after every issue/reveal boundary,
including pending predictions. Former pending reports cover the fractions
retained in immutable history. It distinguishes final accumulators, final state,
and the temporal maximum; it does not measure peak RAM or transient arithmetic.

| Case / mode | V1 final accumulator | V2 final state | V2/V3 peak | Boundary observations |
|---|---:|---:|---:|---:|
"""
    for c in corrections:
        text += f"| {c['case']} / {c['method']} | {c['v1_misnamed_max_state_fraction_bits']} | {c['v2_final_state_max_fraction_bits']} | {c['v2_and_v3_peak_state_max_fraction_bits']} | {c['observations']} |\n"
    text += """
Four peaks exceed the old final-accumulator counter. Inputs, complete issue
records, metrics and core audits match exactly between v1 and v2. The v2 source
and output were then preserved before a separately reviewed receipt repair.
Python dataclass equality had admitted Boolean/numeric aliases, and receipt
counter dictionaries were mutable. Version 3 uses strict scalar types,
immutable counter tuples and a registration-time canonical digest. Its malformed
receipt probes check evidence and all core states remain unchanged. Saved v1/v2
ordinary integer receipts were valid; this defect invalidated the broader
receipt-interface claim, not their recorded forecast scores. V3 retains the
same input population and exactly matches projected numerical reports, metrics,
core audits and measured fraction peaks. Receipt encodings/digests change as
intended, so complete v3 receipt byte equality is not claimed.

All completed run files and archived source hashes were checked before analysis.
No failed development execution was produced in these revisions. One source
patch initially failed context verification before applying and was retried;
it did not run a partially patched method. The independent review's defect
witness remains separate evidence. No source or result from v1/v2 was overwritten.

## Boundary conclusion

Nonvacuity means improvement over an explicitly named bound on the same
records. It does not establish favorable finite predictive performance,
asymptotic convergence, originality, or a reason to prefer fallible forecasting
to the cheap exact solver in this domain. The useful result is a checked
restricted forecast/decision/evidence integration with explicit finite limits.
This analysis introduces no parameter sweep, final controls, paid-computation
policy, contribution gate, P3-07 work or principal Research90 credit.
"""
    return text


def main():
    outputs = [OUT / name for name in ("analysis.json", "ANALYSIS.md", "manifest.json", "failure.json")]
    if any(p.exists() for p in outputs):
        raise FileExistsError("Existing analysis output is preserved; use a new version.")
    manifest = {"version": "mathematical-bound-usefulness-v1", "stage": "posthoc_development_analysis",
                "source_sha256": {"analysis.py": sha(HERE)}, "status": "running",
                "clock_credit": "unmeasured subagent; zero principal credit"}
    dump(OUT / "manifest.json", manifest)
    try:
        manifests = [verify_run(V1, True), verify_run(V2, True), verify_run(V3)]
        rows, corrections = [], []
        for case in manifests[0]["completed_cases"]:
            inputs = [load(directory / (case + ".json")) for directory in (V1, V2, V3)]
            corrections.extend(correction_case(*inputs))
            rows.extend(analyze(inputs[0], method) for method in METHODS)
        dump(OUT / "analysis.json", {"basis": "original immutable v1 issue/admission records",
             "source_runs": ["mathematical_queries_v1", "mathematical_queries_v2", "mathematical_queries_v3"],
             "methods": rows, "resource_corrections": corrections,
             "verification": {"v1_v2_original_files_unchanged": True, "v1_v2_records_equal": True,
                 "v1_v2_v3_numerical_projections_metrics_audits_equal": True,
                 "v2_v3_fraction_peaks_equal": True, "v3_receipt_rejections_leave_evidence_and_cores_unchanged": True}})
        (OUT / "ANALYSIS.md").write_text(markdown(rows, corrections))
        manifest["status"] = "completed"
        manifest["input_manifests_sha256"] = {directory.name: sha(directory / "manifest.json") for directory in (V1, V2, V3)}
        manifest["artifacts_sha256"] = {p.name: sha(p) for p in outputs[:2]}
        dump(OUT / "manifest.json", manifest)
        print(json.dumps({"status": "completed", "analyzed_configurations": len(rows),
            "fraction_peak_corrections": sum(r["v2_and_v3_peak_state_max_fraction_bits"] > r["v1_misnamed_max_state_fraction_bits"] for r in corrections),
            "new_forecasts_or_queries": 0}))
    except BaseException as exc:
        dump(OUT / "failure.json", {"type": type(exc).__name__, "message": str(exc), "traceback": traceback.format_exc()})
        manifest["status"] = "failed"
        dump(OUT / "manifest.json", manifest)
        raise


if __name__ == "__main__":
    main()
